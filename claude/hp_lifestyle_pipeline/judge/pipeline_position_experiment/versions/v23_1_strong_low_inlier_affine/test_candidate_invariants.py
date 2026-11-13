"""Focused tests for the candidate 17--19-inlier reliability exception."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "v23_1_candidate_invariants", HERE / "candidate_invariants.py"
)
assert SPEC is not None and SPEC.loader is not None
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)

PILOT_ROW = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/"
    "pipeline_position_experiment/pilot_v23_all_view_translation/run/pipeline/rows/"
    "tassel__printer_FrontWide__p1__outer_job_1"
)


def strong_metrics() -> dict:
    return {
        "inliers": 17,
        "inlier_ratio": 0.70,
        "source_span_x_fraction": 0.70,
        "source_span_y_fraction": 0.60,
        "source_quadrants": 4,
        "source_hull_fraction": 0.25,
    }


def passing_checks() -> dict:
    return {
        "inliers": False,
        "inlier_ratio": True,
        "singular_min": True,
        "singular_max": True,
        "anisotropy": True,
        "rotation": True,
        "shear": True,
        "residual_median": True,
        "residual_p95": True,
        "translation_only_residual_median": True,
        "translation_only_residual_p95": True,
        "span_x": True,
        "span_y": True,
        "quadrants": True,
        "hull": True,
        "corners": True,
        "fixed_translation_x": True,
        "fixed_translation_y": True,
    }


def eligible(metrics: dict | None = None, checks: dict | None = None) -> bool:
    result = GUARD._assess_strong_low_inlier_evidence(
        metrics or strong_metrics(), checks or passing_checks()
    )
    return result["eligible"]


def test_exact_strict_boundary_is_eligible() -> None:
    assert eligible()


def test_only_17_through_19_are_eligible() -> None:
    for count in (17, 18, 19):
        metrics = strong_metrics()
        metrics["inliers"] = count
        assert eligible(metrics)
    for count in (16, 20):
        metrics = strong_metrics()
        metrics["inliers"] = count
        assert not eligible(metrics)


def test_each_strength_gate_fails_closed() -> None:
    weak_values = {
        "inlier_ratio": 0.699999,
        "source_span_x_fraction": 0.699999,
        "source_span_y_fraction": 0.599999,
        "source_quadrants": 3,
        "source_hull_fraction": 0.249999,
    }
    for name, value in weak_values.items():
        metrics = strong_metrics()
        metrics[name] = value
        assert not eligible(metrics), name


def test_every_existing_non_count_invariant_remains_mandatory() -> None:
    for name in passing_checks():
        if name == "inliers":
            continue
        checks = passing_checks()
        checks[name] = False
        assert not eligible(checks=checks), name


def test_tassel_attempts_use_primary_affine_and_pass() -> None:
    guide = (PILOT_ROW / "geometry_guide.png").read_bytes()
    product_mask = (PILOT_ROW / "mask.png").read_bytes()
    for attempt, fixed_position in ((1, False), (2, True)):
        old = json.loads(
            (PILOT_ROW / f"product_invariant_attempt_{attempt}.json").read_text()
        )
        result = GUARD.assess_product_affine(
            guide,
            (PILOT_ROW / f"gpt_{attempt}.png").read_bytes(),
            old["product_bounds_px"],
            fixed_position=fixed_position,
            product_mask=product_mask,
        )
        assert result["verdict"] == "pass"
        assert result["reasons"] == []
        assert result["strong_low_inlier_evidence"]["eligible"] is True
        assert "textureless_fallback" not in result

