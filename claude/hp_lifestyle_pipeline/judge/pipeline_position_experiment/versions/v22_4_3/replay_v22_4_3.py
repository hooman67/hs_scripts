#!/usr/bin/env python3
"""Read-only V22.4.3 replay over frozen calibration and all compatible prior artifacts."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import cv2
import numpy as np

PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
ROOT = PROJECT / "judge/pipeline_position_experiment"
OUT = ROOT / "versions/v22_4_3"
PACKAGE = Path("/home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25")
sys.path.insert(0, str(PACKAGE))

from hp3p.invariants import (  # noqa: E402
    GUARD_VERSION,
    TEXTURELESS_THRESHOLDS,
    _assess_fixed_textureless,
    assess_product_affine,
)

FROZEN_CALIBRATION = ROOT / "versions/v22_4/textureless_guard_calibration_v3.json"
BASELINE_SOURCE = OUT / "pre_v22_4_3_snapshot/invariants_v22_4_2.py"

spec = importlib.util.spec_from_file_location("invariants_v22_4_2_frozen", BASELINE_SOURCE)
baseline_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(baseline_module)


def load(path: Path):
    return json.loads(path.read_text())


def gray(path: Path):
    value = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if value is None:
        raise RuntimeError(f"cannot read {path}")
    return value


def alpha(path: Path):
    value = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if value is None or value.ndim != 3 or value.shape[2] != 4:
        raise RuntimeError(f"not RGBA: {path}")
    return value[:, :, 3] > 127


def composite(guide, mask, matrix, *, solid=None):
    height, width = guide.shape
    background = np.full_like(guide, 210)
    source = np.full_like(guide, solid, dtype=np.uint8) if solid is not None else guide
    moved = cv2.warpAffine(
        source,
        matrix,
        (width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=210,
    )
    moved_mask = cv2.warpAffine(
        mask.astype(np.uint8) * 255,
        matrix,
        (width, height),
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    ) > 0
    background[moved_mask] = moved[moved_mask]
    return background


def compare_metric(actual, expected):
    keys = [
        "translation_x_px",
        "translation_y_px",
        "boundary_edge_coverage_2px",
        "boundary_distance_p90_px",
        "internal_edge_coverage_2px",
        "internal_distance_p90_px",
        "highpass_ncc",
        "source_boundary_samples",
        "source_internal_edge_samples",
        "source_appearance_samples",
    ]
    for key in keys:
        a, e = actual[key], expected[key]
        if isinstance(e, float):
            if abs(a - e) > 5e-5:
                return False, f"{key}: {a} != {e}"
        elif a != e:
            return False, f"{key}: {a} != {e}"
    return True, None


def replay_real(calibration):
    rows = []
    for frozen in calibration["real"]:
        audit_path = Path(frozen["path"])
        row = audit_path.parent
        attempt = frozen["attempt"]
        audit = load(audit_path)
        arguments = (
            (row / "geometry_guide.png").read_bytes(),
            (row / f"gpt_{attempt}.png").read_bytes(),
            audit["product_bounds_px"],
        )
        keywords = {
            "fixed_position": frozen["fixed_position"],
            "product_mask": (row / "mask.png").read_bytes(),
        }
        baseline = baseline_module.assess_product_affine(*arguments, **keywords)
        candidate = assess_product_affine(*arguments, **keywords)
        rows.append(
            {
                "path": str(audit_path),
                "expected": frozen["label"],
                "baseline": baseline["verdict"],
                "candidate": candidate["verdict"],
                "changed": candidate["verdict"] != baseline["verdict"],
                "primary_verdict": candidate.get("primary_verdict", candidate["verdict"]),
                "primary_reasons": candidate.get("primary_reasons", candidate.get("reasons")),
                "fallback_dispatch_reason": candidate.get("fallback_dispatch_reason"),
                "fallback": candidate.get("textureless_fallback"),
            }
        )
    return rows


def fixture_sources(calibration):
    values = {}
    for frozen in calibration["real"]:
        if not frozen["fixed_position"]:
            continue
        row = Path(frozen["path"]).parent
        key = row.name.split("__retained_control")[0].split("__relocation_demand")[0]
        values.setdefault(key, (row / "geometry_guide.png", row / "mask.png"))
    return values


def replay_synthetic(calibration):
    fixtures = fixture_sources(calibration)
    rows = []
    for frozen in calibration["synthetic"]:
        guide_path, mask_path = fixtures[frozen["fixture"]]
        guide, mask = gray(guide_path), alpha(mask_path)
        matrix = np.asarray(frozen["matrix"], np.float32)
        transform = frozen["transform"]
        if transform == "brightness_shift":
            adjusted = np.clip(guide.astype(np.float32) * 0.72 + 24, 0, 255).astype(np.uint8)
            output = composite(adjusted, mask, matrix)
        else:
            output = composite(
                guide,
                mask,
                matrix,
                solid=28 if transform == "solid_dark_product" else None,
            )
        result = _assess_fixed_textureless(guide, output, mask)
        metrics_match, metric_error = compare_metric(result, frozen["metrics"])
        rows.append(
            {
                "fixture": frozen["fixture"],
                "transform": transform,
                "expected": frozen["label"],
                "actual": result["verdict"],
                "verdict_match": result["verdict"] == frozen["label"],
                "metrics_match_frozen": metrics_match,
                "metric_error": metric_error,
                "metrics": result,
            }
        )
    return rows


def fixed_position(saved):
    density = saved.get("guide_density_class")
    if density is not None:
        return density == "HIGH-FILL/CLOSE"
    guard = saved.get("product_invariant_guard", {})
    if isinstance(guard, dict) and "fixed_position" in guard:
        return bool(guard["fixed_position"])
    return None


def compatible_artifact_rows():
    roots = [ROOT / "smoke"] + sorted(ROOT.glob("full160*"))
    seen = set()
    rows = []
    for search_root in roots:
        if not search_root.is_dir():
            continue
        for result_path in sorted(search_root.rglob("result.json")):
            row = result_path.parent
            if "/run/jobs/" in str(result_path):
                continue
            required = [row / "geometry_guide.png", row / "mask.png"]
            if not all(path.is_file() for path in required) or not list(row.glob("gpt_*.png")):
                continue
            identity = tuple(path.resolve() for path in required) + tuple(
                path.resolve() for path in sorted(row.glob("gpt_*.png"))
            )
            if identity in seen:
                continue
            seen.add(identity)
            rows.append(row)
    return rows


def replay_attempt(row, image, saved, assess):
    fixed = fixed_position(saved)
    bounds = saved.get("guide_info", {}).get("product_bounds_px")
    if fixed is None or bounds is None:
        return None
    result = assess(
        (row / "geometry_guide.png").read_bytes(),
        image.read_bytes(),
        bounds,
        fixed_position=fixed,
        product_mask=(row / "mask.png").read_bytes(),
    )
    return {
        "attempt": int(image.stem.split("_")[-1]),
        "verdict": result["verdict"],
        "reasons": result["reasons"],
        "primary_verdict": result.get("primary_verdict"),
        "primary_reasons": result.get("primary_reasons"),
        "fallback_dispatch_reason": result.get("fallback_dispatch_reason"),
        "fallback": result.get("textureless_fallback"),
    }


def replay_artifact_row(row):
    saved = load(row / "result.json")
    attempts = []
    for image in sorted(row.glob("gpt_*.png")):
        baseline = replay_attempt(row, image, saved, baseline_module.assess_product_affine)
        candidate = replay_attempt(row, image, saved, assess_product_affine)
        if baseline is None or candidate is None:
            return None
        attempts.append({"attempt": baseline["attempt"], "baseline": baseline, "candidate": candidate})
    baseline_selected = next(
        (item["attempt"] for item in attempts if item["baseline"]["verdict"] == "pass"), None
    )
    candidate_selected = next(
        (item["attempt"] for item in attempts if item["candidate"]["verdict"] == "pass"), None
    )
    return {
        "row": str(row),
        "fixed_position": fixed_position(saved),
        "baseline_selected_attempt": baseline_selected,
        "candidate_selected_attempt": candidate_selected,
        "selection_changed": baseline_selected != candidate_selected,
        "attempts": attempts,
    }


def main():
    calibration = load(FROZEN_CALIBRATION)
    real = replay_real(calibration)
    synthetic = replay_synthetic(calibration)
    artifacts = []
    skipped = []
    for row in compatible_artifact_rows():
        try:
            replayed = replay_artifact_row(row)
            if replayed is None:
                skipped.append({"row": str(row), "reason": "missing_density_or_bounds"})
            else:
                artifacts.append(replayed)
        except Exception as exc:
            skipped.append({"row": str(row), "reason": f"{type(exc).__name__}: {exc}"})

    result = {
        "version": "v22.4.3-unreliable-affine-dispatch-replay-v1",
        "guard_version": GUARD_VERSION,
        "thresholds": TEXTURELESS_THRESHOLDS,
        "source_calibration": str(FROZEN_CALIBRATION),
        "calibration": {
            "real_attempts": len(real),
            "real_verdict_changes": sum(item["changed"] for item in real),
            "real_baseline_false_accepts": sum(
                item["expected"] == "fail" and item["baseline"] == "pass" for item in real
            ),
            "real_candidate_false_accepts": sum(
                item["expected"] == "fail" and item["candidate"] == "pass" for item in real
            ),
            "real_induced_false_accepts": sum(
                item["expected"] == "fail"
                and item["baseline"] != "pass"
                and item["candidate"] == "pass"
                for item in real
            ),
            "real_baseline_false_rejects": sum(
                item["expected"] == "pass" and item["baseline"] != "pass" for item in real
            ),
            "real_candidate_false_rejects": sum(
                item["expected"] == "pass" and item["candidate"] != "pass" for item in real
            ),
            "real_induced_false_rejects": sum(
                item["expected"] == "pass"
                and item["baseline"] == "pass"
                and item["candidate"] != "pass"
                for item in real
            ),
            "synthetic_attempts": len(synthetic),
            "synthetic_false_accepts": sum(
                item["expected"] == "fail" and item["actual"] == "pass" for item in synthetic
            ),
            "synthetic_false_rejects": sum(
                item["expected"] == "pass" and item["actual"] != "pass" for item in synthetic
            ),
            "synthetic_metric_mismatches": sum(
                not item["metrics_match_frozen"] for item in synthetic
            ),
            "real": real,
            "synthetic": synthetic,
        },
        "prior_artifacts": {
            "rows": len(artifacts),
            "selection_changes": sum(item["selection_changed"] for item in artifacts),
            "fixed_rows": sum(item["fixed_position"] for item in artifacts),
            "lower_fill_rows": sum(not item["fixed_position"] for item in artifacts),
            "replayed": artifacts,
            "skipped": skipped,
        },
    }
    (OUT / "replay_results.json").write_text(json.dumps(result, indent=2) + "\n")
    summary = {
        "guard_version": GUARD_VERSION,
        "calibration": {
            key: value
            for key, value in result["calibration"].items()
            if key not in {"real", "synthetic"}
        },
        "prior_artifacts": {
            key: value
            for key, value in result["prior_artifacts"].items()
            if key not in {"replayed", "skipped"}
        },
        "changed_artifact_selections": [
            {
                "row": item["row"],
                "baseline": item["baseline_selected_attempt"],
                "candidate": item["candidate_selected_attempt"],
            }
            for item in artifacts
            if item["selection_changed"]
        ],
        "skipped": skipped,
    }
    print(json.dumps(summary, indent=2))
    assert result["calibration"]["real_verdict_changes"] == 0
    assert result["calibration"]["real_induced_false_accepts"] == 0
    assert result["calibration"]["real_induced_false_rejects"] == 0
    assert result["calibration"]["synthetic_false_accepts"] == 0
    assert result["calibration"]["synthetic_false_rejects"] == 0
    assert result["calibration"]["synthetic_metric_mismatches"] == 0


if __name__ == "__main__":
    main()
