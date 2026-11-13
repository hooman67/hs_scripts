"""Deterministic product-landmark checks for generated scenes."""

from __future__ import annotations

import math

import cv2
import numpy as np

GUARD_VERSION = "full-affine-v1.7-strong-low-inlier-exception"
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
    # Retained for frozen V22 fixed-recovery audit compatibility. The all-view
    # verifier searches the full legal frame; fixed recovery applies this limit
    # only after globally localizing the strongest verified placement.
    "max_translation_px": 8,
    "min_boundary_edge_coverage_2px": 0.80,
    "min_internal_edge_coverage_floor_2px": 0.20,
    "min_internal_edge_coverage_2px": 0.80,
    "min_highpass_ncc_override": 0.80,
    "min_internal_edge_samples": 100,
    # This is a deterministic work bound, not an acceptance threshold. If more
    # plausible spatially distinct candidates remain, the result is explicitly
    # unverifiable rather than accepting an arbitrarily truncated search.
    "max_verified_candidate_clusters": 64,
}

# A deliberately narrow alternative reliability path for sparse but unusually
# strong affine evidence. It does not relax any product-transform invariant;
# it only recognizes a 17--19-inlier fit when its spatial distribution and
# ratio are materially stronger than the ordinary 20-inlier path requires.
STRONG_LOW_INLIER_THRESHOLDS = {
    "min_inliers": 17,
    "max_inliers": 19,
    "min_inlier_ratio": 0.70,
    "min_source_span_x_fraction": 0.70,
    "min_source_span_y_fraction": 0.60,
    "min_source_quadrants": 4,
    "min_source_hull_fraction": 0.25,
}


def _assess_strong_low_inlier_evidence(metrics: dict, checks: dict) -> dict:
    """Audit whether 17--19 well-distributed inliers may replace count >= 20.

    Every existing check other than the raw inlier-count check must already
    pass. This includes scale, rotation, anisotropy, shear, affine and rigid
    residuals, frame containment, and fixed-translation checks when present.
    """
    t = STRONG_LOW_INLIER_THRESHOLDS
    gates = {
        "inlier_range": t["min_inliers"] <= metrics["inliers"] <= t["max_inliers"],
        "inlier_ratio": metrics["inlier_ratio"] >= t["min_inlier_ratio"],
        "span_x": metrics["source_span_x_fraction"] >= t["min_source_span_x_fraction"],
        "span_y": metrics["source_span_y_fraction"] >= t["min_source_span_y_fraction"],
        "quadrants": metrics["source_quadrants"] >= t["min_source_quadrants"],
        "hull": metrics["source_hull_fraction"] >= t["min_source_hull_fraction"],
        "all_non_count_invariants": all(
            bool(passed) for name, passed in checks.items() if name != "inliers"
        ),
    }
    gates = {name: bool(passed) for name, passed in gates.items()}
    return {
        "eligible": all(gates.values()),
        "checks": gates,
        "thresholds": STRONG_LOW_INLIER_THRESHOLDS,
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


def _candidate_coverage_map(output_edges: np.ndarray, template: np.ndarray) -> np.ndarray:
    """Return exhaustive two-pixel edge coverage for every legal template origin."""
    near_edges = cv2.dilate(
        output_edges.astype(np.uint8), np.ones((5, 5), np.uint8), iterations=1,
    ).astype(np.float32)
    template_float = template.astype(np.float32)
    support = int(template.sum())
    if support == 0:
        return np.zeros(
            (output_edges.shape[0] - template.shape[0] + 1,
             output_edges.shape[1] - template.shape[1] + 1),
            np.float32,
        )
    result = cv2.matchTemplate(near_edges, template_float, cv2.TM_CCORR) / support
    return np.clip(result, 0.0, 1.0)


def _local_maxima_candidates(score: np.ndarray, eligible: np.ndarray) -> list[tuple[int, int]]:
    """List deterministic spatial proposal peaks, strongest then top-to-bottom/left-to-right."""
    local_max = score >= (cv2.dilate(score, np.ones((5, 5), np.uint8)) - 1e-6)
    ys, xs = np.where(eligible & local_max)
    order = sorted(range(len(xs)), key=lambda index: (-float(score[ys[index], xs[index]]),
                                                       int(ys[index]), int(xs[index])))
    return [(int(xs[index]), int(ys[index])) for index in order]


def _assess_translation_textureless(src: np.ndarray, dst: np.ndarray,
                                    alpha: np.ndarray, *, fixed_position: bool = False) -> dict:
    """Localize and verify a texture-poor product under rigid x-y translation only.

    The persisted RGBA silhouette fixes the product's size and shape. Candidate
    proposal exhaustively covers every integer translation whose complete alpha
    support fits in the output frame; it never searches scale, angle, shear, or
    a deformable transform. Existing boundary/internal/high-pass thresholds are
    retained. Ambiguous or computationally truncated evidence fails closed as
    ``unverifiable``.
    """
    thresholds = TEXTURELESS_THRESHOLDS
    method = ("alpha_mask_fixed_position_fallback" if fixed_position
              else "alpha_mask_all_view_translation_fallback")
    if src.shape != dst.shape or src.shape != alpha.shape:
        return {"method": method, "verdict": "unverifiable",
                "reasons": ["alpha_shape"], "thresholds": thresholds}
    cv2.setNumThreads(1)
    ay, ax = np.where(alpha)
    if not len(ax):
        return {"method": method, "verdict": "unverifiable",
                "reasons": ["empty_alpha_support"], "thresholds": thresholds}
    alpha_x0, alpha_y0 = int(ax.min()), int(ay.min())
    alpha_x1, alpha_y1 = int(ax.max()) + 1, int(ay.max()) + 1
    alpha_crop = alpha[alpha_y0:alpha_y1, alpha_x0:alpha_x1]
    crop_height, crop_width = alpha_crop.shape
    height, width = src.shape
    legal_x_min, legal_x_max = -alpha_x0, width - alpha_x1
    legal_y_min, legal_y_max = -alpha_y0, height - alpha_y1
    if crop_height > height or crop_width > width:
        return {"method": method, "verdict": "unverifiable",
                "reasons": ["alpha_bounds"], "thresholds": thresholds}

    source_edges = cv2.Canny(src, 50, 150) > 0
    output_edges = cv2.Canny(dst, 50, 150) > 0
    kernel3 = np.ones((3, 3), np.uint8)
    # Preserve the frozen V22 verification boundary exactly. The inner-only
    # contour below is used solely to propose full-frame translations; it does
    # not replace the accepted verification metric.
    boundary = ((cv2.dilate(alpha.astype(np.uint8), kernel3, iterations=2) > 0)
                ^ (cv2.erode(alpha.astype(np.uint8), kernel3, iterations=2) > 0))
    proposal_boundary = alpha & ~(cv2.erode(
        alpha.astype(np.uint8), kernel3, iterations=2,
    ) > 0)
    interior = cv2.erode(alpha.astype(np.uint8), np.ones((9, 9), np.uint8), iterations=1) > 0
    internal_edges = source_edges & interior
    proposal_boundary_crop = proposal_boundary[alpha_y0:alpha_y1, alpha_x0:alpha_x1]
    internal_crop = internal_edges[alpha_y0:alpha_y1, alpha_x0:alpha_x1]
    boundary_samples = int(boundary.sum())
    internal_samples = int(internal_crop.sum())
    if not boundary_samples:
        return {"method": method, "verdict": "unverifiable",
                "reasons": ["empty_alpha_support"], "thresholds": thresholds}
    if internal_samples < thresholds["min_internal_edge_samples"]:
        return json_native({
            "method": method,
            "verdict": "unverifiable",
            "reasons": ["internal_support"],
            "thresholds": thresholds,
            "source_boundary_samples": boundary_samples,
            "source_internal_edge_samples": internal_samples,
            "legal_translation_x_px": [legal_x_min, legal_x_max],
            "legal_translation_y_px": [legal_y_min, legal_y_max],
        })

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
        return {"method": method, "verdict": "unverifiable",
                "reasons": ["empty_alpha_support"], "thresholds": thresholds}
    sampled_source_high = source_high[my, mx]
    sampled_source_high -= sampled_source_high.mean()
    if float(np.linalg.norm(sampled_source_high)) <= 1e-9:
        return json_native({
            "method": method,
            "verdict": "unverifiable",
            "reasons": ["appearance_unobservable"],
            "thresholds": thresholds,
            "source_boundary_samples": boundary_samples,
            "source_internal_edge_samples": internal_samples,
        })

    # Exhaustive fixed-scale proposal over every legal origin. These maps are
    # translations only; the template dimensions and internal layout never vary.
    boundary_map = _candidate_coverage_map(output_edges, proposal_boundary_crop)
    internal_map = _candidate_coverage_map(output_edges, internal_crop)
    proposal_score = boundary_map + 0.6 * internal_map
    eligible = ((boundary_map >= thresholds["min_boundary_edge_coverage_2px"])
                & (internal_map >= thresholds["min_internal_edge_coverage_floor_2px"]))
    peak_origins = _local_maxima_candidates(proposal_score, eligible)
    if not peak_origins:
        flat_index = int(np.argmax(proposal_score))
        peak_origins = [(flat_index % proposal_score.shape[1],
                         flat_index // proposal_score.shape[1])]
    clustered_peaks = []
    for peak_x, peak_y in peak_origins:
        if all(max(abs(peak_x - saved_x), abs(peak_y - saved_y)) > 8
               for saved_x, saved_y in clustered_peaks):
            clustered_peaks.append((peak_x, peak_y))

    cap = thresholds["max_verified_candidate_clusters"]
    # The proposal maps intentionally omit the more expensive high-pass term.
    # Verify a small deterministic neighborhood around each peak so a one-pixel
    # edge-score preference cannot hide the appearance-correct registration.
    neighborhood_radius = 2
    candidates_per_peak = (2 * neighborhood_radius + 1) ** 2
    max_peaks = max(1, cap // candidates_per_peak)
    if len(clustered_peaks) > max_peaks:
        return json_native({
            "method": method,
            "verdict": "unverifiable",
            "reasons": ["candidate_search_exhausted"],
            "thresholds": thresholds,
            "plausible_candidate_clusters": len(clustered_peaks),
            "verified_candidate_cap": cap,
            "legal_translation_x_px": [legal_x_min, legal_x_max],
            "legal_translation_y_px": [legal_y_min, legal_y_max],
        })
    proposal_origins = sorted({
        (origin_x + offset_x, origin_y + offset_y)
        for origin_x, origin_y in clustered_peaks
        for offset_y in range(-neighborhood_radius, neighborhood_radius + 1)
        for offset_x in range(-neighborhood_radius, neighborhood_radius + 1)
        if 0 <= origin_x + offset_x < proposal_score.shape[1]
        and 0 <= origin_y + offset_y < proposal_score.shape[0]
    }, key=lambda item: (-float(proposal_score[item[1], item[0]]), item[1], item[0]))

    candidates = []
    for origin_x, origin_y in proposal_origins:
        dx, dy = origin_x - alpha_x0, origin_y - alpha_y0
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
            "outer_silhouette_observable": bool(valid_boundary.all()),
            "final_product_bounds_px": [origin_x, origin_y,
                                         origin_x + crop_width, origin_y + crop_height],
        })

    def candidate_rank(item):
        return (
            item["boundary_edge_coverage_2px"]
            + 0.6 * item["internal_edge_coverage_2px"]
            + 0.3 * item["highpass_ncc"]
            - 0.03 * item["boundary_distance_p90_px"],
            -abs(item["translation_x_px"]) - abs(item["translation_y_px"]),
            -item["translation_y_px"],
            -item["translation_x_px"],
        )

    for candidate in candidates:
        candidate["checks"] = {
            "boundary": (candidate["boundary_edge_coverage_2px"]
                         >= thresholds["min_boundary_edge_coverage_2px"]),
            "internal_structure_floor": (
                candidate["internal_edge_coverage_2px"]
                >= thresholds["min_internal_edge_coverage_floor_2px"]),
            "structure_or_appearance": (
                candidate["internal_edge_coverage_2px"]
                >= thresholds["min_internal_edge_coverage_2px"]
                or candidate["highpass_ncc"] >= thresholds["min_highpass_ncc_override"]
            ),
            "internal_support": (candidate["source_internal_edge_samples"]
                                 >= thresholds["min_internal_edge_samples"]),
        }
        candidate["checks"] = {name: bool(value) for name, value in candidate["checks"].items()}
        candidate["reasons"] = [name for name, passed in candidate["checks"].items()
                                if not passed]

    passing = sorted((item for item in candidates if not item["reasons"]),
                     key=candidate_rank, reverse=True)
    if passing:
        selected = passing[0]
        # Nearby maxima are one registration peak. Distinct verified peaks mean
        # a duplicate product or irresolvable localization ambiguity.
        distinct = [item for item in passing[1:]
                    if max(abs(item["translation_x_px"] - selected["translation_x_px"]),
                           abs(item["translation_y_px"] - selected["translation_y_px"])) > 4]
        if distinct:
            return json_native({
                "method": method,
                "verdict": "unverifiable",
                "reasons": ["ambiguous_or_duplicate_product"],
                "thresholds": thresholds,
                "selected_candidate": selected,
                "competing_passing_candidates": distinct,
                "verified_candidate_clusters": len(candidates),
                "legal_translation_x_px": [legal_x_min, legal_x_max],
                "legal_translation_y_px": [legal_y_min, legal_y_max],
            })
        if not selected["outer_silhouette_observable"]:
            return json_native({
                "method": method,
                "thresholds": thresholds,
                **selected,
                "checks": selected["checks"],
                "reasons": ["silhouette_unobservable_at_canvas_boundary"],
                "verdict": "unverifiable",
                "verified_candidate_clusters": len(candidates),
                "legal_translation_x_px": [legal_x_min, legal_x_max],
                "legal_translation_y_px": [legal_y_min, legal_y_max],
            })
        fixed_reasons = []
        if fixed_position:
            limit = thresholds["max_translation_px"]
            if abs(selected["translation_x_px"]) > limit:
                fixed_reasons.append("fixed_translation_x")
            if abs(selected["translation_y_px"]) > limit:
                fixed_reasons.append("fixed_translation_y")
        if fixed_reasons:
            return json_native({
                "method": method,
                "thresholds": thresholds,
                **selected,
                "checks": selected["checks"],
                "reasons": fixed_reasons,
                "verdict": "fail",
                "verified_candidate_clusters": len(candidates),
                "legal_translation_x_px": [legal_x_min, legal_x_max],
                "legal_translation_y_px": [legal_y_min, legal_y_max],
            })
        return json_native({
            "method": method,
            "thresholds": thresholds,
            **selected,
            "checks": selected["checks"],
            "reasons": [],
            "verdict": "pass",
            "verified_candidate_clusters": len(candidates),
            "legal_translation_x_px": [legal_x_min, legal_x_max],
            "legal_translation_y_px": [legal_y_min, legal_y_max],
        })

    best = max(candidates, key=candidate_rank)
    if not best["outer_silhouette_observable"]:
        return json_native({
            "method": method,
            "thresholds": thresholds,
            **best,
            "checks": best["checks"],
            "reasons": ["silhouette_unobservable_at_canvas_boundary"],
            "verdict": "unverifiable",
            "verification_failures": best["reasons"],
            "verified_candidate_clusters": len(candidates),
            "legal_translation_x_px": [legal_x_min, legal_x_max],
            "legal_translation_y_px": [legal_y_min, legal_y_max],
        })
    return json_native({
        "method": method,
        "thresholds": thresholds,
        **best,
        "checks": best["checks"],
        "reasons": best["reasons"],
        "verdict": "fail",
        "verified_candidate_clusters": len(candidates),
        "legal_translation_x_px": [legal_x_min, legal_x_max],
        "legal_translation_y_px": [legal_y_min, legal_y_max],
    })


def _assess_fixed_textureless(src: np.ndarray, dst: np.ndarray, alpha: np.ndarray) -> dict:
    """Compatibility wrapper for the bounded fixed-position recovery verifier."""
    return _assess_translation_textureless(src, dst, alpha, fixed_position=True)


def _merge_textureless_fallback(primary: dict, fallback: dict, **metadata) -> dict:
    """Attach fallback evidence and promote a verified final localization."""
    localization = {}
    if fallback.get("verdict") == "pass":
        for key in ("translation_x_px", "translation_y_px", "final_product_bounds_px"):
            if key in fallback:
                localization[key] = fallback[key]
    return json_native({
        **primary,
        "primary_verdict": primary["verdict"],
        "primary_reasons": primary["reasons"],
        **metadata,
        "textureless_fallback": fallback,
        **localization,
        "verdict": fallback["verdict"],
        "reasons": fallback["reasons"],
    })


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
        if product_mask is not None:
            fallback = _assess_translation_textureless(
                src, dst, _decode_alpha(product_mask), fixed_position=fixed_position,
            )
            return _merge_textureless_fallback(result, fallback)
        return result
    pairs = cv2.BFMatcher().knnMatch(src_desc, dst_desc, k=2)
    good = [first for first, second in pairs if first.distance < 0.65 * second.distance]
    if len(good) < 3:
        result = {**base, "verdict": "unverifiable", "reasons": ["too_few_matches"],
                  "matches": len(good)}
        if product_mask is not None:
            fallback = _assess_translation_textureless(
                src, dst, _decode_alpha(product_mask), fixed_position=fixed_position,
            )
            return _merge_textureless_fallback(result, fallback)
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
        result = {**base, "verdict": "unverifiable", "reasons": ["affine_fit_failed"],
                  "matches": len(good)}
        if product_mask is not None:
            fallback = _assess_translation_textureless(
                src, dst, _decode_alpha(product_mask), fixed_position=fixed_position,
            )
            return _merge_textureless_fallback(result, fallback)
        return result
    keep = full_mask.ravel().astype(bool)
    inlier_source, inlier_target = source[keep], target[keep]
    linear, translation = full[:, :2], full[:, 2]
    predicted = inlier_source @ linear.T + translation
    residuals = np.linalg.norm(predicted - inlier_target, axis=1)
    # Separately fit the only permitted product transform. The full affine fit
    # remains authoritative for detecting rotation/scale/shear; this robust
    # displacement estimate is the final x-y localization persisted downstream.
    rigid_translation = np.median(inlier_target - inlier_source, axis=0)
    rigid_predicted = inlier_source + rigid_translation
    rigid_residuals = np.linalg.norm(rigid_predicted - inlier_target, axis=1)
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
    rigid_corners = corners + rigid_translation
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
        "translation_only_residual_median_px": float(np.median(rigid_residuals)),
        "translation_only_residual_p95_px": float(np.percentile(rigid_residuals, 95)),
        "source_span_x_fraction": float(norm_x.max() - norm_x.min()),
        "source_span_y_fraction": float(norm_y.max() - norm_y.min()),
        "source_quadrants": quadrants,
        "source_hull_fraction": hull_fraction,
        "transformed_product_corners_px": transformed.tolist(),
        "corners_in_frame": corners_in_frame,
        "translation_x_px": float(rigid_translation[0]),
        "translation_y_px": float(rigid_translation[1]),
        "final_product_bounds_px": [
            float(x0 + rigid_translation[0]), float(y0 + rigid_translation[1]),
            float(x1 + rigid_translation[0]), float(y1 + rigid_translation[1]),
        ],
        "rigid_transformed_product_corners_px": rigid_corners.tolist(),
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
        "translation_only_residual_median": (
            metrics["translation_only_residual_median_px"] <= t["max_residual_median_px"]),
        "translation_only_residual_p95": (
            metrics["translation_only_residual_p95_px"] <= t["max_residual_p95_px"]),
        "span_x": metrics["source_span_x_fraction"] >= t["min_source_span_x_fraction"],
        "span_y": metrics["source_span_y_fraction"] >= t["min_source_span_y_fraction"],
        "quadrants": metrics["source_quadrants"] >= t["min_source_quadrants"],
        "hull": metrics["source_hull_fraction"] >= t["min_source_hull_fraction"],
        "corners": corners_in_frame,
    }
    if fixed_position:
        checks["fixed_translation_x"] = (
            abs(metrics["translation_x_px"]) <= t["max_fixed_translation_px"])
        checks["fixed_translation_y"] = (
            abs(metrics["translation_y_px"]) <= t["max_fixed_translation_px"])
    # Comparisons involving NumPy scalars return np.bool_, which the pipeline's
    # strict JSON writer intentionally rejects.  Keep the public audit record
    # composed entirely of standard JSON scalar types.
    checks = {name: bool(passed) for name, passed in checks.items()}
    low_inlier_evidence = _assess_strong_low_inlier_evidence(metrics, checks)
    accepted_inlier_evidence = checks["inliers"] or low_inlier_evidence["eligible"]
    reasons = [name for name, passed in checks.items()
               if not passed and not (name == "inliers" and accepted_inlier_evidence)]
    primary = json_native({**metrics, "checks": checks,
                           "strong_low_inlier_evidence": low_inlier_evidence,
                           "accepted_inlier_evidence": accepted_inlier_evidence,
                           "reasons": reasons,
                           "verdict": "pass" if not reasons else "fail"})
    reliability_checks = ("inliers", "span_x", "span_y", "quadrants", "hull")
    effective_reliability = {
        name: (accepted_inlier_evidence if name == "inliers" else checks[name])
        for name in reliability_checks
    }
    unreliable_affine = any(not passed for passed in effective_reliability.values())
    if product_mask is not None and unreliable_affine:
        fallback = _assess_translation_textureless(
            src, dst, _decode_alpha(product_mask), fixed_position=fixed_position,
        )
        return _merge_textureless_fallback(
            primary,
            fallback,
            fallback_dispatch_reason="structurally_insufficient_affine_evidence",
            affine_evidence_reliability_checks=effective_reliability,
        )
    return primary
