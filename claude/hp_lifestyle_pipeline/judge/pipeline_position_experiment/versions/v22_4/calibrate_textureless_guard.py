#!/usr/bin/env python3
"""Calibrate the V22.4 alpha-mask fallback from preserved local attempts.

This script is deliberately read-only with respect to all prior run folders.  It
uses the affine guard's recorded verdict as the label for real attempts, and
adds deterministic product-only perturbations to test false acceptance of
scale, rotation, shear, excessive translation, and featureless dark fills.
"""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np


ROOT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment")
OUT = ROOT / "versions/v22_4"


def _gray(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not read {path}")
    return image


def _alpha(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None or image.ndim != 3 or image.shape[2] != 4:
        raise ValueError(f"Expected RGBA mask at {path}")
    return image[:, :, 3] > 127


def textureless_metrics_arrays(
    guide_gray: np.ndarray,
    output_gray: np.ndarray,
    alpha: np.ndarray,
    max_translation_px: int = 8,
) -> dict:
    """Measure silhouette and internal structure under a bounded translation search."""
    if guide_gray.shape != output_gray.shape or guide_gray.shape != alpha.shape:
        raise ValueError("Guide, output and alpha mask shapes must match")
    cv2.setNumThreads(1)
    source_edges = cv2.Canny(guide_gray, 50, 150) > 0
    output_edges = cv2.Canny(output_gray, 50, 150) > 0
    kernel3 = np.ones((3, 3), np.uint8)
    boundary = ((cv2.dilate(alpha.astype(np.uint8), kernel3, iterations=2) > 0)
                ^ (cv2.erode(alpha.astype(np.uint8), kernel3, iterations=2) > 0))
    interior = cv2.erode(alpha.astype(np.uint8), np.ones((9, 9), np.uint8), iterations=1) > 0
    internal_edges = source_edges & interior
    distance = cv2.distanceTransform((~output_edges).astype(np.uint8), cv2.DIST_L2, 3)

    guide_float = guide_gray.astype(np.float32)
    output_float = output_gray.astype(np.float32)
    guide_high = guide_float - cv2.GaussianBlur(guide_float, (0, 0), 3)
    output_high = output_float - cv2.GaussianBlur(output_float, (0, 0), 3)
    by, bx = np.where(boundary)
    iy, ix = np.where(internal_edges)
    my, mx = np.where(alpha)
    # Deterministic spatial subsampling keeps a full-resolution 2368x1776 check
    # inexpensive without changing the support of any metric.
    by, bx = by[::2], bx[::2]
    iy, ix = iy[::2], ix[::2]
    my, mx = my[::16], mx[::16]
    source_high = guide_high[my, mx]
    source_high = source_high - source_high.mean()
    height, width = guide_gray.shape
    candidates = []
    for dy in range(-max_translation_px, max_translation_px + 1):
        for dx in range(-max_translation_px, max_translation_px + 1):
            vb = ((by + dy >= 0) & (by + dy < height)
                  & (bx + dx >= 0) & (bx + dx < width))
            vi = ((iy + dy >= 0) & (iy + dy < height)
                  & (ix + dx >= 0) & (ix + dx < width))
            vm = ((my + dy >= 0) & (my + dy < height)
                  & (mx + dx >= 0) & (mx + dx < width))
            boundary_distance = distance[by[vb] + dy, bx[vb] + dx]
            internal_distance = distance[iy[vi] + dy, ix[vi] + dx]
            target_high = output_high[my[vm] + dy, mx[vm] + dx]
            target_high = target_high - target_high.mean()
            source_values = source_high[vm]
            denominator = float(np.linalg.norm(source_values) * np.linalg.norm(target_high))
            highpass_ncc = (float(source_values.dot(target_high) / denominator)
                            if denominator > 1e-9 else 0.0)
            candidates.append({
                "translation_x_px": dx,
                "translation_y_px": dy,
                "boundary_edge_coverage_2px": float((boundary_distance <= 2.0).mean()),
                "boundary_distance_p90_px": float(np.percentile(boundary_distance, 90)),
                "internal_edge_coverage_2px": float((internal_distance <= 2.0).mean()),
                "internal_distance_p90_px": float(np.percentile(internal_distance, 90)),
                "highpass_ncc": highpass_ncc,
                "source_boundary_samples": int(len(boundary_distance)),
                "source_internal_edge_samples": int(len(internal_distance)),
                "source_appearance_samples": int(vm.sum()),
            })
    # Selection is fixed independently of final pass thresholds.
    best = max(candidates, key=lambda item: (
        item["boundary_edge_coverage_2px"]
        + 0.6 * item["internal_edge_coverage_2px"]
        + 0.3 * item["highpass_ncc"]
        - 0.03 * item["boundary_distance_p90_px"]
    ))
    return best


def _real_records() -> list[dict]:
    records = []
    for audit in sorted(ROOT.rglob("product_invariant_attempt_*.json")):
        if "smoke/v22_4" in str(audit):
            continue
        data = json.loads(audit.read_text())
        attempt = audit.stem.rsplit("_", 1)[-1]
        row = audit.parent
        guide, output, mask = row / "geometry_guide.png", row / f"gpt_{attempt}.png", row / "mask.png"
        if not all(path.exists() for path in (guide, output, mask)):
            continue
        records.append({
            "kind": "real",
            "path": str(audit),
            "row": row.name,
            "attempt": int(attempt),
            "fixed_position": bool(data.get("fixed_position")),
            "affine_verdict": data["verdict"],
            "affine_reasons": data.get("reasons", []),
            "label": data["verdict"] if data["verdict"] in {"pass", "fail"} else "unlabeled",
            "metrics": textureless_metrics_arrays(_gray(guide), _gray(output), _alpha(mask)),
        })
    return records


def _composite_product(guide: np.ndarray, alpha: np.ndarray, matrix: np.ndarray,
                       *, solid: int | None = None) -> np.ndarray:
    height, width = guide.shape
    # A uniform field prevents unrelated scene texture from helping a candidate.
    background = np.full_like(guide, 210)
    source = np.full_like(guide, solid, dtype=np.uint8) if solid is not None else guide
    warped_source = cv2.warpAffine(source, matrix, (width, height), flags=cv2.INTER_LINEAR,
                                   borderMode=cv2.BORDER_CONSTANT, borderValue=210)
    warped_alpha = cv2.warpAffine(alpha.astype(np.uint8) * 255, matrix, (width, height),
                                  flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT,
                                  borderValue=0) > 0
    background[warped_alpha] = warped_source[warped_alpha]
    return background


def _synthetic_records() -> list[dict]:
    # One fixture per distinct fixed-position camera/product gives real silhouettes
    # without allowing multiple stochastic outputs from one row to dominate.
    fixtures = {}
    for audit in sorted(ROOT.rglob("product_invariant_attempt_*.json")):
        if "smoke/v22_4" in str(audit):
            continue
        data = json.loads(audit.read_text())
        if not data.get("fixed_position"):
            continue
        row = audit.parent
        key = row.name.split("__retained_control")[0].split("__relocation_demand")[0]
        fixtures.setdefault(key, (row / "geometry_guide.png", row / "mask.png"))
    records = []
    for fixture, (guide_path, mask_path) in sorted(fixtures.items()):
        if not guide_path.exists() or not mask_path.exists():
            continue
        guide, alpha = _gray(guide_path), _alpha(mask_path)
        ys, xs = np.where(alpha)
        center = ((float(xs.min() + xs.max())) / 2, (float(ys.min() + ys.max())) / 2)
        identity = np.float32([[1, 0, 0], [0, 1, 0]])
        transforms = [
            ("identity", "pass", identity, None),
            ("allowed_translation_8px", "pass", np.float32([[1, 0, 8], [0, 1, -8]]), None),
            ("brightness_shift", "pass", identity, "brightness"),
            ("excess_translation_12px", "fail", np.float32([[1, 0, 12], [0, 1, 0]]), None),
            ("scale_0.975", "fail", cv2.getRotationMatrix2D(center, 0, 0.975), None),
            ("scale_1.025", "fail", cv2.getRotationMatrix2D(center, 0, 1.025), None),
            ("rotation_1.1deg", "fail", cv2.getRotationMatrix2D(center, 1.1, 1), None),
            ("rotation_minus1.1deg", "fail", cv2.getRotationMatrix2D(center, -1.1, 1), None),
            ("shear_0.025", "fail", np.float32([[1, 0.025, -0.025 * center[1]], [0, 1, 0]]), None),
            ("anisotropic_1.025_0.975", "fail",
             np.float32([[1.025, 0, center[0] * (1 - 1.025)],
                         [0, 0.975, center[1] * (1 - 0.975)]]), None),
            ("solid_dark_product", "fail", identity, 28),
        ]
        for name, label, matrix, mode in transforms:
            if mode == "brightness":
                adjusted = np.clip(guide.astype(np.float32) * 0.72 + 24, 0, 255).astype(np.uint8)
                output = _composite_product(adjusted, alpha, identity)
            else:
                output = _composite_product(guide, alpha, matrix, solid=mode if isinstance(mode, int) else None)
            records.append({
                "kind": "synthetic",
                "fixture": fixture,
                "transform": name,
                "fixed_position": True,
                "label": label,
                "matrix": np.asarray(matrix).tolist(),
                "metrics": textureless_metrics_arrays(guide, output, alpha),
            })
    return records


def _predict(metrics: dict, thresholds: dict) -> str:
    structural = metrics["internal_edge_coverage_2px"] >= thresholds["min_internal_edge_coverage_2px"]
    appearance_override = metrics["highpass_ncc"] >= thresholds["min_highpass_ncc_override"]
    checks = {
        "boundary": metrics["boundary_edge_coverage_2px"] >= thresholds["min_boundary_edge_coverage_2px"],
        "internal_structure_floor": metrics["internal_edge_coverage_2px"] >= thresholds["min_internal_edge_coverage_floor_2px"],
        "structure_or_appearance": structural or appearance_override,
        "internal_support": metrics["source_internal_edge_samples"] >= thresholds["min_internal_edge_samples"],
    }
    return "pass" if all(checks.values()) else "fail"

def main() -> None:
    real, synthetic = _real_records(), _synthetic_records()
    # These thresholds are frozen from the separation margins in the synthetic
    # fallback-only corpus. The affine verdict remains authoritative whenever
    # affine estimation is verifiable; this fallback is invoked only for
    # fixed-position no/too-few-descriptor cases.
    thresholds = {
        "min_boundary_edge_coverage_2px": 0.80,
        "min_internal_edge_coverage_floor_2px": 0.20,
    "min_internal_edge_coverage_2px": 0.80,
        "min_highpass_ncc_override": 0.80,
        "min_internal_edge_samples": 100,
    }
    for record in real + synthetic:
        record["textureless_prediction"] = _predict(record["metrics"], thresholds)
    synthetic_eval = synthetic
    fixed_real_labeled = [r for r in real if r["fixed_position"] and r["label"] in {"pass", "fail"}]
    unlabeled = [r for r in real if r["label"] == "unlabeled"]
    result = {
        "version": "v22.4.1-calibration-v3",
        "scope": "fixed-position texture-poor fallback only; lower-fill remains affine-only",
        "cascade_rule": "Use affine verdict when verifiable. Only fixed-position no/too-few-match cases may use this fallback.",
        "thresholds": thresholds,
        "counts": {
            "real_attempts": len(real),
            "real_affine_pass": sum(r["label"] == "pass" for r in real),
            "real_affine_fail": sum(r["label"] == "fail" for r in real),
            "real_unlabeled_too_few_matches": len(unlabeled),
            "synthetic_attempts": len(synthetic),
            "synthetic_false_accepts": sum(r["label"] == "fail" and r["textureless_prediction"] == "pass"
                                           for r in synthetic_eval),
            "synthetic_false_rejects": sum(r["label"] == "pass" and r["textureless_prediction"] == "fail"
                                           for r in synthetic_eval),
            "fixed_real_affine_fail_fallback_false_accepts": sum(
                r["label"] == "fail" and r["textureless_prediction"] == "pass" for r in fixed_real_labeled),
            "held_out_too_few_matches_passed": sum(r["textureless_prediction"] == "pass" for r in unlabeled),
        },
        "real": real,
        "synthetic": synthetic,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "textureless_guard_calibration_v3.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"thresholds": thresholds, "counts": result["counts"]}, indent=2))


if __name__ == "__main__":
    main()
