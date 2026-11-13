"""Find where the generated image actually put the product (GPT may move/rescale it despite the mask)."""
import io

import numpy as np
from PIL import Image, ImageFilter

from .mask import WHITE_THRESHOLD

SCALES = np.geomspace(0.5, 2.0, 29)
# Color-only and color+silhouette matches must overlap this much (box IoU) to trust the location.
AGREEMENT = 0.5


def _corr(img: np.ndarray, kern: np.ndarray) -> np.ndarray:
    """Cross-correlation of each kernel placement (top-left) over img, via FFT (circular; caller crops)."""
    s = img.shape
    return np.fft.irfft2(np.fft.rfft2(img, s) * np.conj(np.fft.rfft2(kern, s)), s)


def _masked_ncc(img: np.ndarray, tmpl: np.ndarray, m: np.ndarray) -> np.ndarray:
    """Masked normalized cross-correlation over all channels (Padfield-style), valid placements only."""
    n = m.sum()
    num = den_i = den_t = 0.0
    for c in range(img.shape[2]):
        i, t = img[..., c], tmpl[..., c] * m
        ci_m = _corr(i, m)
        num = num + _corr(i, t) - ci_m * t.sum() / n
        den_i = den_i + _corr(i * i, m) - ci_m ** 2 / n
        den_t = den_t + (t * tmpl[..., c]).sum() - t.sum() ** 2 / n
    th, tw = m.shape
    score = num / np.sqrt(np.maximum(den_i, 1e-3 * n) * max(den_t, 1e-6))
    return score[: img.shape[0] - th + 1, : img.shape[1] - tw + 1]


def _silhouette_ncc(img: np.ndarray, m: np.ndarray, ring: int) -> np.ndarray:
    """|NCC| of a binary product-vs-surrounding-ring template: rewards the right outline size, not just color.

    Indexed by the top-left of `m` (like _masked_ncc). Placements where the ring leaves the image are NaN
    (caller falls back to the color score there).
    """
    H, W = img.shape[:2]
    out = np.full((H - m.shape[0] + 1, W - m.shape[1] + 1), np.nan)
    big = np.pad(m, ring)
    if big.shape[0] > H or big.shape[1] > W:
        return out
    support = np.asarray(Image.fromarray((big * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * ring + 1)),
                         float) > 127
    score = np.abs(_masked_ncc(img, np.repeat(big[..., None], img.shape[2], -1), support.astype(float)))
    out[ring:ring + score.shape[0], ring:ring + score.shape[1]] = score
    return out


def locate(hero_png: bytes, out_png: bytes, down: int = 2) -> tuple[bytes, dict]:
    """hero_png must already share the output's framing/size (as produced by mask.prepare).

    Returns an RGBA protect mask at the product's found location and match info.
    """
    out = Image.open(io.BytesIO(out_png)).convert("RGB")
    hero = Image.open(io.BytesIO(hero_png)).convert("RGB").resize(out.size)
    prod = np.asarray(hero).min(-1) < WHITE_THRESHOLD
    ys, xs = np.where(prod)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    tmpl_full, m_full = hero.crop((x0, y0, x1, y1)), Image.fromarray((prod[y0:y1, x0:x1] * 255).astype(np.uint8))
    small = np.asarray(out.resize((out.width // down, out.height // down), Image.LANCZOS), float) / 255
    best = {"score": -1.0}
    color_best = {"score": -1.0}
    for s in SCALES:
        tw, th = round((x1 - x0) * s / down), round((y1 - y0) * s / down)
        if tw < 8 or th < 8 or tw >= small.shape[1] or th >= small.shape[0]:
            continue
        t = np.asarray(tmpl_full.resize((tw, th), Image.LANCZOS), float) / 255
        m = (np.asarray(m_full.resize((tw, th), Image.BILINEAR), float) > 127).astype(float)
        ring = max(2, round(0.08 * max(tw, th))) | 1
        color, sil = _masked_ncc(small, t, m), _silhouette_ncc(small, m, ring)
        score = np.where(np.isnan(sil), color, 0.5 * color + 0.5 * np.nan_to_num(sil))
        for res, sc in ((best, score), (color_best, color)):
            y, x = np.unravel_index(np.argmax(sc), sc.shape)
            if sc[y, x] > res["score"]:
                res.update(score=float(sc[y, x]), scale=float(s), x=int(x * down), y=int(y * down))
    s = best["scale"]
    w, h = round((x1 - x0) * s), round((y1 - y0) * s)
    alpha = Image.new("L", out.size, 0)
    alpha.paste(m_full.resize((w, h), Image.BILINEAR), (best["x"], best["y"]))
    alpha = alpha.point(lambda v: 255 if v > 127 else 0).filter(ImageFilter.MaxFilter(9))
    mask = Image.new("RGBA", out.size, (0, 0, 0, 0))
    mask.putalpha(alpha)
    buf = io.BytesIO()
    mask.save(buf, "PNG")
    def box(b):
        return b["x"], b["y"], b["x"] + (x1 - x0) * b["scale"], b["y"] + (y1 - y0) * b["scale"]

    (ax0, ay0, ax1, ay1), (bx0, by0, bx1, by1) = box(best), box(color_best)
    inter = max(0, min(ax1, bx1) - max(ax0, bx0)) * max(0, min(ay1, by1) - max(ay0, by0))
    agree = inter / ((ax1 - ax0) * (ay1 - ay0) + (bx1 - bx0) * (by1 - by0) - inter)
    info = {"score": round(best["score"], 3), "scale": round(s, 3),
            "dx": best["x"] - int(x0), "dy": best["y"] - int(y0), "agreement": round(float(agree), 2),
            "confident": bool(agree >= AGREEMENT)}
    return buf.getvalue(), info
