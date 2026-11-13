"""Deterministic SIFT/affine product localization and conservative support crop."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageOps

ALGORITHM_VERSION = "hp-placement-support-crop-v4.2.1"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _decode(path: Path) -> tuple[np.ndarray, str]:
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        arr = np.asarray(im)
    return arr, hashlib.sha256(arr.tobytes()).hexdigest()


def _foreground_bbox(twin_rgb: np.ndarray) -> tuple[tuple[int, int, int, int] | None, str, str | None]:
    h, w = twin_rgb.shape[:2]
    # Conservative border-connected nearly-white background removal.
    white = np.all(twin_rgb >= 245, axis=2).astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(white, 8)
    border_labels = set(labels[0, :]) | set(labels[-1, :]) | set(labels[:, 0]) | set(labels[:, -1])
    bg = np.zeros((h, w), np.uint8)
    for label in border_labels:
        if label:
            bg[labels == label] = 1
    fg = bg == 0
    ys, xs = np.where(fg)
    if not len(xs):
        return None, "border_connected_white", "no_foreground_after_mask"
    x0, x1, y0, y1 = int(xs.min()), int(xs.max() + 1), int(ys.min()), int(ys.max() + 1)
    area = float(fg.sum()) / float(h * w)
    touches = sum((x0 == 0, y0 == 0, x1 == w, y1 == h))
    if area < .02 or area > .90 or touches >= 3:
        return None, "border_connected_white", f"unreliable_foreground_mask area={area:.4f} touches={touches}"
    return (x0, y0, x1, y1), "border_connected_white", None


def _resize_for_match(rgb: np.ndarray, max_edge: int = 1600) -> tuple[np.ndarray, float]:
    h, w = rgb.shape[:2]
    scale = min(1.0, max_edge / max(h, w))
    if scale == 1:
        return rgb, 1.0
    return cv2.resize(rgb, (round(w * scale), round(h * scale)), interpolation=cv2.INTER_AREA), scale


def create_support_crop(scene_path: Path | str, twin_path: Path | str, output_dir: Path | str) -> tuple[Path, dict[str, Any]]:
    scene_path, twin_path, output_dir = Path(scene_path), Path(twin_path), Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    scene, scene_pixel_hash = _decode(scene_path)
    twin, twin_pixel_hash = _decode(twin_path)
    sh, sw = scene.shape[:2]
    th, tw = twin.shape[:2]
    provenance: dict[str, Any] = {
        "algorithm_version": ALGORITHM_VERSION,
        "scene_byte_sha256": _sha(scene_path), "scene_pixel_sha256": scene_pixel_hash,
        "twin_byte_sha256": _sha(twin_path), "twin_pixel_sha256": twin_pixel_hash,
        "localization_status": "fallback_full_scene", "mask_method": None,
        "match_count": 0, "inlier_count": 0, "inlier_ratio": 0.0,
        "median_residual": None, "p95_residual": None, "affine_matrix": None,
        "device_box": None, "crop_box_full_scene_pixels": [0, 0, sw, sh],
        "source_dimensions": [sw, sh], "display_dimensions": [sw, sh],
        "fallback_reason": None,
    }
    bbox, mask_method, mask_error = _foreground_bbox(twin)
    provenance["mask_method"] = mask_method
    try:
        if bbox is None:
            raise RuntimeError(mask_error or "foreground_mask_failed")
        scene_m, ss = _resize_for_match(scene)
        twin_m, ts = _resize_for_match(twin)
        gray_scene = cv2.cvtColor(scene_m, cv2.COLOR_RGB2GRAY)
        gray_twin = cv2.cvtColor(twin_m, cv2.COLOR_RGB2GRAY)
        x0, y0, x1, y1 = bbox
        mask = np.zeros(gray_twin.shape, np.uint8)
        mask[round(y0 * ts):round(y1 * ts), round(x0 * ts):round(x1 * ts)] = 255
        sift = cv2.SIFT_create(nfeatures=8000, contrastThreshold=.02, edgeThreshold=10, sigma=1.6)
        kt, dt = sift.detectAndCompute(gray_twin, mask)
        ks, ds = sift.detectAndCompute(gray_scene, None)
        if dt is None or ds is None:
            raise RuntimeError("no_descriptors")
        matcher = cv2.BFMatcher(cv2.NORM_L2)
        t2s = matcher.knnMatch(dt, ds, k=2)
        s2t = matcher.knnMatch(ds, dt, k=2)
        good_t2s = {m.queryIdx: m for m, n in t2s if m.distance <= .70 * n.distance}
        good_s2t = {m.queryIdx: m for m, n in s2t if m.distance <= .70 * n.distance}
        good = [m for q, m in good_t2s.items() if m.trainIdx in good_s2t and good_s2t[m.trainIdx].trainIdx == q]
        provenance["match_count"] = len(good)
        if len(good) < 24:
            raise RuntimeError(f"too_few_mutual_matches:{len(good)}")
        src = np.float32([kt[m.queryIdx].pt for m in good])
        dst = np.float32([ks[m.trainIdx].pt for m in good])
        cv2.setRNGSeed(42)
        affine, inlier_mask = cv2.estimateAffine2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0, maxIters=5000, confidence=.995, refineIters=10)
        if affine is None or inlier_mask is None:
            raise RuntimeError("affine_fit_failed")
        inliers = inlier_mask.ravel().astype(bool)
        count, ratio = int(inliers.sum()), float(inliers.mean())
        projected = cv2.transform(src.reshape(-1, 1, 2), affine).reshape(-1, 2)
        residual = np.linalg.norm(projected - dst, axis=1)[inliers]
        med, p95 = float(np.median(residual)), float(np.percentile(residual, 95))
        provenance.update(inlier_count=count, inlier_ratio=ratio, median_residual=med, p95_residual=p95)
        if count < 18 or ratio < .60 or med > 2 or p95 > 4:
            raise RuntimeError("affine_quality_threshold_failed")
        hull = cv2.convexHull(src[inliers]).reshape(-1, 2)
        hull_area = cv2.contourArea(hull.astype(np.float32))
        fg_area_match = (x1 - x0) * ts * (y1 - y0) * ts
        span = src[inliers].ptp(axis=0)
        if hull_area < .15 * fg_area_match or span[0] < .40 * (x1 - x0) * ts or span[1] < .40 * (y1 - y0) * ts:
            raise RuntimeError("insufficient_inlier_spread")
        cx, cy = ((x0 + x1) * ts / 2, (y0 + y1) * ts / 2)
        quadrants = {(int(p[0] >= cx), int(p[1] >= cy)) for p in src[inliers]}
        if len(quadrants) < 3:
            raise RuntimeError("insufficient_inlier_quadrants")
        linear = affine[:, :2]
        singular = np.linalg.svd(linear, compute_uv=False)
        if np.linalg.det(linear) <= 0 or singular[0] / max(singular[1], 1e-8) > 1.8:
            raise RuntimeError("implausible_affine")
        corners = np.float32([[[x0 * ts, y0 * ts], [x1 * ts, y0 * ts], [x1 * ts, y1 * ts], [x0 * ts, y1 * ts]]])
        pc = cv2.transform(corners, affine)[0] / ss
        dx0, dy0, dx1, dy1 = float(pc[:, 0].min()), float(pc[:, 1].min()), float(pc[:, 0].max()), float(pc[:, 1].max())
        area = max(0, dx1 - dx0) * max(0, dy1 - dy0) / (sw * sh)
        clipped_area = max(0, min(sw, dx1) - max(0, dx0)) * max(0, min(sh, dy1) - max(0, dy0))
        inside = clipped_area / max(1, (dx1 - dx0) * (dy1 - dy0))
        if area < .01 or area > .85 or inside < .95:
            raise RuntimeError("projected_box_threshold_failed")
        provenance["affine_matrix"] = affine.tolist()
        provenance["device_box"] = [round(dx0, 2), round(dy0, 2), round(dx1, 2), round(dy1, 2)]
        # Broad unwarped crop: full width, whole lower scene, upper bound no lower than 25% scene height.
        top = max(0, int(min(dy0 - max(.50 * (dy1 - dy0), .15 * sh), .25 * sh)))
        crop_box = [0, top, sw, sh]
        crop = scene[top:sh, 0:sw]
        provenance["crop_box_full_scene_pixels"] = crop_box
        provenance["localization_status"] = "localized_affine"
        provenance["fallback_reason"] = None
        if crop.shape[:2] == scene.shape[:2] or crop.size / scene.size > .90:
            crop = scene
            provenance["crop_box_full_scene_pixels"] = [0, 0, sw, sh]
            provenance["localization_status"] = "full_scene_equivalent"
    except Exception as exc:
        crop = scene
        provenance["fallback_reason"] = str(exc)
    out = output_dir / "product_support_crop.png"
    Image.fromarray(crop).save(out, format="PNG", optimize=False)
    provenance["display_dimensions"] = [int(crop.shape[1]), int(crop.shape[0])]
    (output_dir / "crop_provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    return out, provenance
