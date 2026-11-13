"""Deterministic product-landmark checks for generated scenes."""

from __future__ import annotations

import math

import cv2
import numpy as np

GUARD_VERSION = "full-affine-v1.3-alpha-textureless-fallback"
THRESHOLDS = {
    "min_inliers": 20,
    "min_inlier_ratio": 0.55,
    "singular_min": 0.98,
    "singular_max": 1.02,
    "max_anisotropy_ratio": 1.02,
    "max_abs_rotation_deg": 1.0,
    "max_column_shear_cos": 0.02,
    "max_residual_median_px": 1.5,
    "max_residual_p95_px": 3.5,
    "min_source_span_x_fraction": 0.45,
    "min_source_span_y_fraction": 0.40,
    "min_source_quadrants": 3,
    "min_source_hull_fraction": 0.12,
    "max_fixed_translation_px": 8.0,
}
TEXTURELESS_THRESHOLDS = {
    "max_translation_px": 8,
    "min_boundary_edge_coverage_2px": 0.80,
    "min_internal_edge_coverage_floor_2px": 0.20,
    "min_internal_edge_coverage_2px": 0.80,
    "min_highpass_ncc_override": 0.80,
    "min_internal_edge_samples": 100,
}


def json_native(value):
    """Recursively convert NumPy containers/scalars to strict JSON-native values."""
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return [json_native(item) for item in value.tolist()]
    if isinstance(value, dict):
        return {str(key): json_native(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_native(item) for item in value]
    return value


def _decode(data: bytes) -> np.ndarray:
    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Invariant guard could not decode image bytes.")
    return image


def _decode_alpha(data: bytes) -> np.ndarray:
    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_UNCHANGED)
    if image is None or image.ndim != 3 or image.shape[2] != 4:
        raise ValueError("Invariant guard expected an RGBA product mask.")
    return image[:, :, 3] > 127


def _assess_fixed_textureless(src: np.ndarray, dst: np.ndarray, alpha: np.ndarray) -> dict:
    """Check a texture-poor fixed product from its persisted alpha silhouette.

    The bounded search permits only the fixed-position tolerance. A candidate
    must preserve the alpha boundary and either its internal edge structure or
    its masked high-frequency appearance, so a similarly dark blob cannot pass.
    """
    thresholds = TEXTURELESS_THRESHOLDS
    if src.shape != dst.shape or src.shape != alpha.shape:
        return {"method": "alpha_mask_fixed_position_fallback", "verdict": "unverifiable",
                "reasons": ["alpha_shape"], "thresholds": thresholds}
    cv2.setNumThreads(1)
    source_edges = cv2.Canny(src, 50, 150) > 0
    output_edges = cv2.Canny(dst, 50, 150) > 0
    kernel3 = np.ones((3, 3), np.uint8)
    boundary = ((cv2.dilate(alpha.astype(np.uint8), kernel3, iterations=2) > 0)
                ^ (cv2.erode(alpha.astype(np.uint8), kernel3, iterations=2) > 0))
    interior = cv2.erode(alpha.astype(np.uint8), np.ones((9, 9), np.uint8), iterations=1) > 0
    internal_edges = source_edges & interior
    distance = cv2.distanceTransform((~output_edges).astype(np.uint8), cv2.DIST_L2, 3)
    source_float, output_float = src.astype(np.float32), dst.astype(np.float32)
    source_high = source_float - cv2.GaussianBlur(source_float, (0, 0), 3)
    output_high = output_float - cv2.GaussianBlur(output_float, (0, 0), 3)
    by, bx = np.where(boundary)
    iy, ix = np.where(internal_edges)
    my, mx = np.where(alpha)
    by, bx = by[::2], bx[::2]
    iy, ix = iy[::2], ix[::2]
    my, mx = my[::16], mx[::16]
    if not len(by) or not len(my):
        return {"method": "alpha_mask_fixed_position_fallback", "verdict": "unverifiable",
                "reasons": ["empty_alpha_support"], "thresholds": thresholds}
    sampled_source_high = source_high[my, mx]
    sampled_source_high -= sampled_source_high.mean()
    height, width = src.shape
    candidates = []
    limit = thresholds["max_translation_px"]
    for dy in range(-limit, limit + 1):
        for dx in range(-limit, limit + 1):
            valid_boundary = ((by + dy >= 0) & (by + dy < height)
                              & (bx + dx >= 0) & (bx + dx < width))
            valid_internal = ((iy + dy >= 0) & (iy + dy < height)
                              & (ix + dx >= 0) & (ix + dx < width))
            valid_mask = ((my + dy >= 0) & (my + dy < height)
                          & (mx + dx >= 0) & (mx + dx < width))
            boundary_distance = distance[by[valid_boundary] + dy, bx[valid_boundary] + dx]
            internal_distance = distance[iy[valid_internal] + dy, ix[valid_internal] + dx]
            target_high = output_high[my[valid_mask] + dy, mx[valid_mask] + dx]
            target_high -= target_high.mean()
            source_values = sampled_source_high[valid_mask]
            denominator = float(np.linalg.norm(source_values) * np.linalg.norm(target_high))
            highpass_ncc = (float(source_values.dot(target_high) / denominator)
                            if denominator > 1e-9 else 0.0)
            candidates.append({
                "translation_x_px": dx,
                "translation_y_px": dy,
                "boundary_edge_coverage_2px": float((boundary_distance <= 2.0).mean()),
                "boundary_distance_p90_px": float(np.percentile(boundary_distance, 90)),
                "internal_edge_coverage_2px": (float((internal_distance <= 2.0).mean())
                                                if len(internal_distance) else 0.0),
                "internal_distance_p90_px": (float(np.percentile(internal_distance, 90))
                                              if len(internal_distance) else None),
                "highpass_ncc": highpass_ncc,
                "source_boundary_samples": int(len(boundary_distance)),
                "source_internal_edge_samples": int(len(internal_distance)),
                "source_appearance_samples": int(valid_mask.sum()),
            })
    best = max(candidates, key=lambda item: (
        item["boundary_edge_coverage_2px"]
        + 0.6 * item["internal_edge_coverage_2px"]
        + 0.3 * item["highpass_ncc"]
        - 0.03 * item["boundary_distance_p90_px"]
    ))
    checks = {
        "boundary": (best["boundary_edge_coverage_2px"]
                     >= thresholds["min_boundary_edge_coverage_2px"]),
        "internal_structure_floor": (best["internal_edge_coverage_2px"]
                                     >= thresholds["min_internal_edge_coverage_floor_2px"]),
        "structure_or_appearance": (
            best["internal_edge_coverage_2px"] >= thresholds["min_internal_edge_coverage_2px"]
            or best["highpass_ncc"] >= thresholds["min_highpass_ncc_override"]
        ),
        "internal_support": (best["source_internal_edge_samples"]
                             >= thresholds["min_internal_edge_samples"]),
    }
    checks = {name: bool(value) for name, value in checks.items()}
    reasons = [name for name, passed in checks.items() if not passed]
    return json_native({"method": "alpha_mask_fixed_position_fallback", "thresholds": thresholds,
                        **best, "checks": checks, "reasons": reasons,
                        "verdict": "pass" if not reasons else "fail"})


def assess_product_affine(guide: bytes, output: bytes, bounds: list[int], *, fixed_position: bool,
                          product_mask: bytes | None = None) -> dict:
    """Fit product landmarks and return an auditable invariant verdict."""
    src, dst = _decode(guide), _decode(output)
    if src.shape != dst.shape:
        return {"guard_version": GUARD_VERSION, "verdict": "fail", "reasons": ["canvas_size"],
                "guide_shape": list(src.shape), "output_shape": list(dst.shape), "thresholds": THRESHOLDS}
    x0, y0, x1, y1 = map(int, bounds)
    mask = np.zeros_like(src)
    mask[y0:y1, x0:x1] = 255
    cv2.setNumThreads(1)
    sift = cv2.SIFT_create()
    src_points, src_desc = sift.detectAndCompute(src, mask)
    dst_points, dst_desc = sift.detectAndCompute(dst, None)
    base = {"guard_version": GUARD_VERSION, "fixed_position": fixed_position,
            "thresholds": THRESHOLDS, "product_bounds_px": [x0, y0, x1, y1]}
    if src_desc is None or dst_desc is None:
        result = {**base, "verdict": "unverifiable", "reasons": ["no_descriptors"], "matches": 0}
        if fixed_position and product_mask is not None:
            fallback = _assess_fixed_textureless(src, dst, _decode_alpha(product_mask))
            return json_native({**result, "primary_verdict": "unverifiable",
                                "primary_reasons": result["reasons"],
                                "textureless_fallback": fallback,
                                "verdict": fallback["verdict"], "reasons": fallback["reasons"]})
        return result
    pairs = cv2.BFMatcher().knnMatch(src_desc, dst_desc, k=2)
    good = [first for first, second in pairs if first.distance < 0.65 * second.distance]
    if len(good) < 3:
        result = {**base, "verdict": "unverifiable", "reasons": ["too_few_matches"],
                  "matches": len(good)}
        if fixed_position and product_mask is not None:
            fallback = _assess_fixed_textureless(src, dst, _decode_alpha(product_mask))
            return json_native({**result, "primary_verdict": "unverifiable",
                                "primary_reasons": result["reasons"],
                                "textureless_fallback": fallback,
                                "verdict": fallback["verdict"], "reasons": fallback["reasons"]})
        return result
    source = np.float32([src_points[item.queryIdx].pt for item in good])
    target = np.float32([dst_points[item.trainIdx].pt for item in good])
    cv2.setRNGSeed(42)
    full, full_mask = cv2.estimateAffine2D(source, target, method=cv2.RANSAC,
                                           ransacReprojThreshold=3.6, maxIters=4000,
                                           confidence=0.995, refineIters=10)
    cv2.setRNGSeed(42)
    partial, partial_mask = cv2.estimateAffinePartial2D(source, target, method=cv2.RANSAC,
                                                        ransacReprojThreshold=3.6, maxIters=4000,
                                                        confidence=0.995, refineIters=10)
    if full is None or full_mask is None or partial is None or partial_mask is None:
        return {**base, "verdict": "unverifiable", "reasons": ["affine_fit_failed"],
                "matches": len(good)}
    keep = full_mask.ravel().astype(bool)
    inlier_source, inlier_target = source[keep], target[keep]
    linear, translation = full[:, :2], full[:, 2]
    predicted = inlier_source @ linear.T + translation
    residuals = np.linalg.norm(predicted - inlier_target, axis=1)
    u, singular, vt = np.linalg.svd(linear)
    rotation_matrix = u @ vt
    rotation = math.degrees(math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0]))
    shear = abs(float(np.dot(linear[:, 0], linear[:, 1]))) / (
        float(np.linalg.norm(linear[:, 0]) * np.linalg.norm(linear[:, 1])) or 1.0
    )
    norm_x = (inlier_source[:, 0] - x0) / max(x1 - x0, 1)
    norm_y = (inlier_source[:, 1] - y0) / max(y1 - y0, 1)
    quadrants = len({(int(x >= 0.5), int(y >= 0.5)) for x, y in zip(norm_x, norm_y)})
    hull = cv2.convexHull(inlier_source).reshape(-1, 2)
    hull_fraction = (float(cv2.contourArea(hull)) / max((x1 - x0) * (y1 - y0), 1)
                     if len(hull) >= 3 else 0.0)
    corners = np.float32([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
    transformed = corners @ linear.T + translation
    height, width = dst.shape
    corners_in_frame = bool(((transformed[:, 0] >= 0) & (transformed[:, 0] <= width)
                             & (transformed[:, 1] >= 0) & (transformed[:, 1] <= height)).all())
    metrics = {
        **base,
        "matches": len(good),
        "inliers": int(keep.sum()),
        "inlier_ratio": float(keep.mean()),
        "full_affine_matrix": full.tolist(),
        "partial_affine_matrix": partial.tolist(),
        "partial_inliers": int(partial_mask.sum()),
        "singular_values": [float(value) for value in singular],
        "anisotropy_ratio": float(singular.max() / singular.min()),
        "rotation_deg": float(rotation),
        "column_shear_cos": float(shear),
        "residual_median_px": float(np.median(residuals)),
        "residual_p95_px": float(np.percentile(residuals, 95)),
        "source_span_x_fraction": float(norm_x.max() - norm_x.min()),
        "source_span_y_fraction": float(norm_y.max() - norm_y.min()),
        "source_quadrants": quadrants,
        "source_hull_fraction": hull_fraction,
        "transformed_product_corners_px": transformed.tolist(),
        "corners_in_frame": corners_in_frame,
        "translation_x_px": float(translation[0]),
        "translation_y_px": float(translation[1]),
    }
    t = THRESHOLDS
    checks = {
        "inliers": metrics["inliers"] >= t["min_inliers"],
        "inlier_ratio": metrics["inlier_ratio"] >= t["min_inlier_ratio"],
        "singular_min": singular.min() >= t["singular_min"],
        "singular_max": singular.max() <= t["singular_max"],
        "anisotropy": metrics["anisotropy_ratio"] <= t["max_anisotropy_ratio"],
        "rotation": abs(metrics["rotation_deg"]) <= t["max_abs_rotation_deg"],
        "shear": metrics["column_shear_cos"] <= t["max_column_shear_cos"],
        "residual_median": metrics["residual_median_px"] <= t["max_residual_median_px"],
        "residual_p95": metrics["residual_p95_px"] <= t["max_residual_p95_px"],
        "span_x": metrics["source_span_x_fraction"] >= t["min_source_span_x_fraction"],
        "span_y": metrics["source_span_y_fraction"] >= t["min_source_span_y_fraction"],
        "quadrants": metrics["source_quadrants"] >= t["min_source_quadrants"],
        "hull": metrics["source_hull_fraction"] >= t["min_source_hull_fraction"],
        "corners": corners_in_frame,
    }
    if fixed_position:
        checks["fixed_translation_x"] = abs(metrics["translation_x_px"]) <= t["max_fixed_translation_px"]
        checks["fixed_translation_y"] = abs(metrics["translation_y_px"]) <= t["max_fixed_translation_px"]
    # Comparisons involving NumPy scalars return np.bool_, which the pipeline's
    # strict JSON writer intentionally rejects.  Keep the public audit record
    # composed entirely of standard JSON scalar types.
    checks = {name: bool(passed) for name, passed in checks.items()}
    reasons = [name for name, passed in checks.items() if not passed]
    return json_native({**metrics, "checks": checks, "reasons": reasons,
                        "verdict": "pass" if not reasons else "fail"})
