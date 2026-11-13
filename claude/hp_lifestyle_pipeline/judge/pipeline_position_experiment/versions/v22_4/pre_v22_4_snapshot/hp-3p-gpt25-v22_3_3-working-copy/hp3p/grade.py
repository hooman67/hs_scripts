"""Reference color guidance and optional scene-only or whole-image color transfer."""
import hashlib
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from .catalog import StyleRef

_M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
_WHITE = np.array([0.95047, 1.0, 1.08883])
_TONE_FEATURES = ("L", "L_std", "a", "b")


def _to_lab(rgb: np.ndarray) -> np.ndarray:
    c = rgb / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    xyz = c @ _M.T / _WHITE
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def _to_rgb(lab: np.ndarray) -> np.ndarray:
    fy = (lab[..., 0] + 16) / 116
    f = np.stack([fy + lab[..., 1] / 500, fy, fy - lab[..., 2] / 200], -1)
    xyz = np.where(f > 0.2069, f ** 3, (f - 16 / 116) / 7.787) * _WHITE
    c = xyz @ np.linalg.inv(_M).T
    c = np.where(c > 0.0031308, 1.055 * np.clip(c, 0, None) ** (1 / 2.4) - 0.055, 12.92 * c)
    return np.clip(c * 255, 0, 255)


def _bands(L: np.ndarray) -> np.ndarray:
    """Soft shadow / mid / highlight weights from lightness."""
    sh = 1 / (1 + np.exp((L - 40) / 8))
    hi = 1 / (1 + np.exp((70 - L) / 8))
    return np.stack([sh, np.clip(1 - sh - hi, 0, None), hi])


def _lab(data: bytes, max_side: int | None = 384) -> np.ndarray:
    img = Image.open(io.BytesIO(data)).convert("RGB")
    if max_side:
        img.thumbnail((max_side, max_side))
    return _to_lab(np.asarray(img, float))


def _band_means(lab: np.ndarray, weight: np.ndarray | None = None) -> np.ndarray:
    """[3 bands, (a, b)] weighted mean chroma, plus nothing else."""
    w = _bands(lab[..., 0]) * (1 if weight is None else weight)
    return np.stack([[(wk * lab[..., i]).sum() / max(wk.sum(), 1e-6) for i in (1, 2)] for wk in w])


def lab_stats(data: bytes) -> dict:
    lab = _lab(data)
    (sa, sb), (ma, mb), (ha, hb) = _band_means(lab)
    return {"L": float(lab[..., 0].mean()), "L_std": float(lab[..., 0].std()), "a": float(lab[..., 1].mean()),
            "b": float(lab[..., 2].mean()), "sh_a": sa, "sh_b": sb, "mid_a": ma, "mid_b": mb, "hi_a": ha, "hi_b": hb}


def _reference_signature(catalog: list[StyleRef]) -> dict:
    if not catalog:
        raise ValueError("Reference catalog is empty.")
    if len({r.id for r in catalog}) != len(catalog):
        raise ValueError("Reference catalog IDs must be unique.")
    return {"version": "sRGB_D65_Lab_v1", "max_side": 384,
            "images": [{"id": r.id, "sha256": hashlib.sha256(r.data).hexdigest()}
                       for r in sorted(catalog, key=lambda r: r.id)]}


def _tone_vector(stats: dict) -> np.ndarray:
    values = np.asarray([stats[c] for c in _TONE_FEATURES], dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Tone statistics must be finite.")
    if values[1] < 0.1:
        raise ValueError("Image has insufficient tonal variation to match contrast.")
    return values


def _reference_features(index: dict) -> np.ndarray:
    identities = [{k: entry[k] for k in ("id", "sha256")} for entry in index["entries"]]
    if identities != index["signature"]["images"]:
        raise ValueError("Statistics entries do not match the catalog signature.")
    return np.stack([_tone_vector(entry["stats"]) for entry in index["entries"]])


def reference_statistics(catalog: list[StyleRef], cache: Path) -> dict:
    """Cache reference measurements, invalidating changed images or computation versions."""
    signature = _reference_signature(catalog)
    index = json.loads(cache.read_text()) if cache.exists() else None
    if index is None or index.get("signature") != signature:
        by_id = {r.id: r for r in catalog}
        index = {"signature": signature,
                 "entries": [{**image, "stats": lab_stats(by_id[image["id"]].data)}
                             for image in signature["images"]]}
        _reference_features(index)
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(index, indent=2, allow_nan=False))
    else:
        _reference_features(index)
    return index


def nearest_reference(data: bytes, catalog: list[StyleRef], index: dict) -> tuple[StyleRef, dict]:
    """Choose nearest full-image brightness/contrast/tint, not semantic scene similarity."""
    if index.get("signature") != _reference_signature(catalog):
        raise ValueError("Reference statistics do not match the current catalog.")
    features = _reference_features(index)
    source = _tone_vector(lab_stats(data))
    scales = features.std(axis=0)
    # Constant catalog features cannot change ranking; use unit scale for their common offset.
    scales = np.where(scales > 1e-6, scales, 1.0)
    distances = np.linalg.norm((features - source) / scales, axis=1)
    position = int(np.argmin(distances))
    entry = index["entries"][position]
    chosen = next(r for r in catalog if r.id == entry["id"])
    return chosen, {
        "method": "nearest_global_Lab_catalog_zscore",
        "reference_id": chosen.id, "reference_sha256": entry["sha256"],
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "candidate_count": len(catalog), "distance": float(distances[position]),
        "features": list(_TONE_FEATURES), "scales": dict(zip(_TONE_FEATURES, scales.tolist())),
    }


def describe(refs: list[bytes]) -> str:
    """Measured grade of the refs in words + numbers, for the rewriter."""
    s = {k: float(np.mean([lab_stats(r)[k] for r in refs])) for k in lab_stats(refs[0])}

    def tint(a, b):
        cool = "cool blue" if b < -1.5 else "warm yellow" if b > 1.5 else "neutral"
        mag = ", slightly magenta" if a > 1.5 else ", slightly green" if a < -1.5 else ""
        return f"{cool}{mag} (a* {a:+.1f}, b* {b:+.1f})"

    label = "Image 2" if len(refs) == 1 else f"Images 2-{len(refs) + 1}"
    return (f"Measured grade of {label} (whole-image palette hints only): shadows "
            f"{tint(s['sh_a'], s['sh_b'])}; midtones {tint(s['mid_a'], s['mid_b'])}; "
            f"highlights {tint(s['hi_a'], s['hi_b'])}. "
            "People, clothing and furniture influence these statistics; they are not calibrated "
            "exposure or contrast targets. Follow the actual style photographs' softer, more "
            "uniform illumination and gentle tonal transitions, not a dense or dramatic grade.")


def match_reference(out_png: bytes, reference: bytes) -> tuple[bytes, dict]:
    """Match global Lab tint and lightness mean/std; changes product colors too."""
    lab, target = _lab(out_png, max_side=None), _lab(reference)
    mean = lab.mean(axis=(0, 1))
    target_mean = target.mean(axis=(0, 1))
    sd, target_sd = float(lab[..., 0].std()), float(target[..., 0].std())
    # Sub-8-bit compression noise is not usable photographic contrast.
    if sd < 0.1 or target_sd < 0.1:
        raise ValueError("Source or reference has insufficient tonal variation to match contrast.")
    graded = lab.copy()
    graded[..., 0] = np.clip(target_mean[0] + (lab[..., 0] - mean[0]) * (target_sd / sd), 0, 100)
    graded[..., 1:] += target_mean[1:] - mean[1:]
    buf = io.BytesIO()
    Image.fromarray(np.round(_to_rgb(graded)).astype(np.uint8)).save(buf, "PNG")
    output = buf.getvalue()
    return output, {
        "method": "global_Lab_mean_tint_and_lightness_mean_std",
        "scope": "whole_image", "product_colors_preserved": False,
        "contrast_scale": target_sd / sd,
        "before": lab_stats(out_png), "reference": lab_stats(reference), "after": lab_stats(output),
        "limitations": "Content-dependent statistics, not calibrated relighting. RGB gamut clipping "
                      "can prevent exact statistical matching. Reference statistics use a 384px thumbnail.",
    }


def match_grade(out_png: bytes, refs: list[bytes], mask_png: bytes, strength: float = 0.8) -> bytes:
    """Shift scene (non-product) tint per tonal band and exposure toward the refs' average."""
    rgb = np.asarray(Image.open(io.BytesIO(out_png)).convert("RGB"), float)
    lab = _to_lab(rgb)
    alpha = Image.open(io.BytesIO(mask_png)).convert("RGBA").getchannel("A").resize(rgb.shape[1::-1])
    protect = np.asarray(alpha.filter(ImageFilter.GaussianBlur(4)), float) / 255
    scene = 1 - protect

    ref_labs = [_lab(r) for r in refs]
    ref_bands = np.mean([_band_means(r) for r in ref_labs], 0)
    delta = np.clip(ref_bands - _band_means(lab, scene), -12, 12)  # [band, (a, b)]
    w = _bands(lab[..., 0])
    graded = lab.copy()
    graded[..., 1] += np.tensordot(delta[:, 0], w, 1)
    graded[..., 2] += np.tensordot(delta[:, 1], w, 1)

    L, ws = lab[..., 0], scene / max(scene.sum(), 1e-6)
    mu_o, sd_o = (L * ws).sum(), np.sqrt((((L - (L * ws).sum()) ** 2) * ws).sum())
    mu_r = float(np.mean([r[..., 0].mean() for r in ref_labs]))
    sd_r = float(np.mean([r[..., 0].std() for r in ref_labs]))
    graded[..., 0] = np.clip(mu_o + np.clip(mu_r - mu_o, -10, 10) + (L - mu_o) * np.clip(sd_r / max(sd_o, 1e-6),
                                                                                          0.85, 1.25), 0, 100)

    k = (strength * scene)[..., None]
    out = _to_rgb(lab + k * (graded - lab)) * (1 - protect[..., None]) + rgb * protect[..., None]
    buf = io.BytesIO()
    Image.fromarray(np.round(out).astype(np.uint8)).save(buf, "PNG")
    return buf.getvalue()
