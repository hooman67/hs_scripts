"""Undo GPT's product drift: zoom/shift the generated photo so its product lands exactly on the hero's
product (same size and position), then paste the exact hero product pixels on top."""
import io

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .locate import _masked_ncc, locate
from .mask import WHITE_THRESHOLD

PAD = 8  # edge-replicated border so sub-pixel edges never count as uncovered
REFINE_SCALES = np.linspace(-0.06, 0.06, 13)
REFINE_SHIFT = 10
STAY = 6  # px: fill output counts as 'product kept in place'
BLEND = 41  # px band (inside the covered area) where the outpaint fill fades into the aligned photo


def _png(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def _box(prod: np.ndarray) -> tuple[int, int, int, int]:
    ys, xs = np.where(prod)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def product_alpha(hero_png: bytes) -> bytes:
    """Product alpha from a product-on-white hero: background is the white region connected to the border,
    so near-white details inside the product stay opaque. Edges are eroded 2px (drops the white anti-alias fringe) and softened."""
    hero = Image.open(io.BytesIO(hero_png)).convert("RGB")
    lab = Image.fromarray(np.where(np.asarray(hero).min(-1) < WHITE_THRESHOLD, 255, 0).astype(np.uint8))
    lab = lab.crop((-1, -1, hero.width + 1, hero.height + 1))  # 1px black frame connects the border
    ImageDraw.floodfill(lab, (0, 0), 128)
    a = Image.fromarray(np.where(np.asarray(lab) == 128, 0, 255).astype(np.uint8)).crop((1, 1, hero.width + 1,
                                                                                         hero.height + 1))
    return _png(a.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.0)))


def _refine(out: np.ndarray, hero: Image.Image, prod: np.ndarray, s: float, x: int, y: int):
    """Full-resolution search around the coarse locate result: (scale, top-left x, y)."""
    x0, y0, x1, y1 = _box(prod)
    tmpl, m_full = hero.crop((x0, y0, x1, y1)), Image.fromarray((prod[y0:y1, x0:x1] * 255).astype(np.uint8))
    best = (-np.inf, s, x, y)
    for k in REFINE_SCALES:
        sc = s * (1 + k)
        tw, th = round((x1 - x0) * sc), round((y1 - y0) * sc)
        wx0, wy0 = max(0, x - REFINE_SHIFT), max(0, y - REFINE_SHIFT)
        win = out[wy0:y + th + REFINE_SHIFT, wx0:x + tw + REFINE_SHIFT]
        if tw < 4 or th < 4 or win.shape[0] < th or win.shape[1] < tw:
            continue
        t = np.asarray(tmpl.resize((tw, th), Image.LANCZOS), float) / 255
        m = (np.asarray(m_full.resize((tw, th), Image.BILINEAR), float) > 127).astype(float)
        score = _masked_ncc(win, t, m)
        j, i = np.unravel_index(np.argmax(score), score.shape)
        if score[j, i] > best[0]:
            best = (float(score[j, i]), sc, wx0 + int(i), wy0 + int(j))
    return best[1:]


def align(hero_png: bytes, out_png: bytes, loc: dict, fill=None, window=None) -> tuple[bytes, dict]:
    """loc is locate()'s info (scale, dx, dy relative to the hero product's top-left) for an output with the
    same framing as hero_png. window=(x, y, w, h) crops the final frame from a wider generation canvas.

    fill(image_png, mask_png) -> png extends the photo into uncovered (transparent-mask) areas when the
    output had to be zoomed out; without it those areas are edge-replicated.
    """
    out = Image.open(io.BytesIO(out_png)).convert("RGB")
    hero = Image.open(io.BytesIO(hero_png)).convert("RGB").resize(out.size, Image.LANCZOS)
    prod = np.asarray(hero).min(-1) < WHITE_THRESHOLD
    x0, y0, _, _ = _box(prod)
    s, gx, gy = _refine(np.asarray(out, float) / 255, hero, prod, loc["scale"], x0 + loc["dx"], y0 + loc["dy"])
    wx, wy, ww, wh = window or (0, 0, *out.size)
    hero = hero.crop((wx, wy, wx + ww, wy + wh))
    # aligned(q) = out(s * (q + window_tl - hero_tl) + gpt_tl)
    a, c, f = s, gx - s * (x0 - wx) + PAD, gy - s * (y0 - wy) + PAD
    padded = Image.fromarray(np.pad(np.asarray(out), ((PAD, PAD), (PAD, PAD), (0, 0)), mode="edge"))
    aligned = padded.transform((ww, wh), Image.AFFINE, (a, 0, c, 0, a, f), Image.BICUBIC)
    cover = Image.new("L", padded.size, 255).transform((ww, wh), Image.AFFINE, (a, 0, c, 0, a, f),
                                                       Image.NEAREST, fillcolor=0)
    uncovered = np.asarray(cover) == 0
    info = {"scale": round(s, 4), "upscale": round(1 / s, 3), "gpt_x": gx, "gpt_y": gy,
            "uncovered": round(float(uncovered.mean()), 4), "filled": False,
            "fill_mode": None}
    if uncovered.any() and fill is not None:
        keep = Image.fromarray(np.where(uncovered, 0, 255).astype(np.uint8))
        mask = Image.new("RGBA", hero.size, (0, 0, 0, 0))
        mask.putalpha(keep)
        filled = Image.open(io.BytesIO(fill(_png(aligned), _png(mask)))).convert("RGB").resize(hero.size)
        # GPT regenerates the whole frame with a slight tone shift: match it to the aligned photo on the
        # covered area (per-channel mean/std), then blend over a wide band inside the covered area.
        f, g, cov = np.asarray(filled, float), np.asarray(aligned, float), ~uncovered
        f = (f - f[cov].mean(0)) / (f[cov].std(0) + 1e-6) * g[cov].std(0) + g[cov].mean(0)
        filled = Image.fromarray(np.clip(f, 0, 255).astype(np.uint8))
        # GPT re-composes the whole frame while filling. Seam-free: use that frame (re-aligned exactly when the
        # product moved); blend the border only if the product cannot be found in it.
        _, floc = locate(_png(hero), _png(filled))
        if floc["confident"] and abs(floc["scale"] - 1) < 0.04 and max(abs(floc["dx"]), abs(floc["dy"])) <= STAY:
            aligned, info["fill_mode"] = filled, "full"
        elif floc["confident"]:
            final, info["realign"] = align(_png(hero), _png(filled), floc)
            info.update(filled=True, fill_mode="realigned")
            return final, info
        else:
            soft = keep.filter(ImageFilter.MinFilter(BLEND)).filter(ImageFilter.GaussianBlur(BLEND / 3))
            aligned, info["fill_mode"] = Image.composite(aligned, filled, soft), "blend"
        info["filled"] = True
    alpha = Image.open(io.BytesIO(product_alpha(_png(hero))))
    return _png(Image.composite(hero, aligned, alpha)), info
