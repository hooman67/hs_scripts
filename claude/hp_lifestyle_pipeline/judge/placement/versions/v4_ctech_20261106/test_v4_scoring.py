"""Deterministic checks for the C-Tech-calibrated placement V4 policy."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scoring  # noqa: E402


SCENE_READING = {
    "functional_front": "The operating front is visible at image left.",
    "support_surface": "A rectangular table supports the device.",
    "usable_approach_edge": "The near table edge is available to the user.",
    "actual_user_position": "One chair is placed at the near edge.",
    "access_path": "The visible route from chair to device is clear.",
    "device_support_axes": "The device and table axes are visibly aligned.",
    "neighboring_furniture": "The chair and table form the working area.",
    "narrative_status": "supported",
    "narrative_evidence": "The visible arrangement supports ordinary use.",
    "support_placement_in_room": "The table sits plausibly within the room layout.",
    "usable_space_distribution": "Working and circulation space remain available.",
    "alternative_user_positions": "No imagined alternate seat is needed for use.",
    "prop_relationships": "Nearby props support the visible work activity.",
    "lived_in_evidence": "A small set of work props makes the scene feel inhabited.",
}

CHECK_IDS = tuple(sorted(scoring.INSPECTION_CHECK_IDS))


def clean_check() -> dict:
    return {
        "visibility": "adequate",
        "result": "consistent",
        "evidence": "Visible localized geometry supports this check.",
        "limitation": "none",
        "alternative": "none",
        "alternative_status": "not_applicable",
        "finding_ids": [],
    }


def component(
    severity: int = 0,
    *,
    confidence: str = "high",
    issue_code: str | None = None,
) -> dict:
    return {
        "visibility": "observed",
        "severity": severity,
        "confidence": confidence,
        "evidence": "Concrete visible evidence supports this assessment.",
        "consequence": "A visible placement consequence is present." if severity else "",
        "issue_codes": [issue_code] if issue_code else [],
        "supporting_check_ids": [CHECK_IDS[0]],
        "finding_ids": ["F1"] if severity else [],
    }


def observation() -> dict:
    value = {
        "schema_version": "placement-observations-v4",
        "product_match": "match",
        "product_match_note": "The generated device matches the supplied twin.",
        "view_class": "medium",
        "context_visibility": "adequate",
        "inspection_checks": {check_id: clean_check() for check_id in CHECK_IDS},
        "defect_inventory": [],
        "verification": {
            "structural_contradictions_rechecked": True,
            "severity_zero_evidence_checked": True,
            "hidden_geometry_not_assumed": True,
            "creative_advisories_not_scored": True,
            "corrected_assignments": [],
            "notes": "The evidence and severity assignments were rechecked.",
        },
        "components": {name: component() for name in scoring.COMPONENT_WEIGHTS},
        "summary": "The visible placement is assessed across all five components.",
        "creative_advisories": [],
        "suggested_scene_changes": [],
        "scene_reading": dict(SCENE_READING),
    }
    return value


def add_finding(value: dict, component_name: str, severity: int) -> None:
    check_id = value["components"][component_name]["supporting_check_ids"][0]
    value["defect_inventory"] = [
        {
            "id": "F1",
            "defect_type": "calibration_fixture",
            "image_region": "visible support area",
            "evidence": "A localized visible defect supports the assigned severity.",
            "basis": "physical_geometry",
            "primary_component": component_name,
            "severity_recommendation": min(severity, 3),
        }
    ]
    value["inspection_checks"][check_id]["result"] = "contradiction"
    value["inspection_checks"][check_id]["finding_ids"] = ["F1"]


def test_warning_level_chair_displacement_remains_pass() -> None:
    value = observation()
    value["components"]["orientation_alignment"] = component(
        1, issue_code="chair_alignment_conflict"
    )
    add_finding(value, "orientation_alignment", 1)
    result = scoring.aggregate_observation(value)
    assert result["weighted_component_score"] == 99.0
    assert result["natural_placement_score"] == 99.0
    assert result["verdict"] == "pass"


def test_review_level_chair_relation_caps_at_review() -> None:
    value = observation()
    value["components"]["orientation_alignment"] = component(
        2, confidence="medium", issue_code="chair_alignment_conflict"
    )
    add_finding(value, "orientation_alignment", 2)
    result = scoring.aggregate_observation(value)
    assert result["weighted_component_score"] == 95.0
    assert result["natural_placement_score"] == 79
    assert result["applied_score_cap"] == 79
    assert result["verdict"] == "review"


def test_missing_support_structure_is_a_fail() -> None:
    value = observation()
    value["components"]["scale_perspective"] = component(
        3, confidence="high", issue_code="missing_support_structure"
    )
    add_finding(value, "scale_perspective", 3)
    result = scoring.aggregate_observation(value)
    assert result["weighted_component_score"] == 91.0
    assert result["natural_placement_score"] == 59
    assert result["applied_score_cap"] == 59
    assert result["verdict"] == "fail"


def test_style_advisory_is_unscored() -> None:
    value = observation()
    value["creative_advisories"] = [
        {
            "code": "style_wall_unresolved",
            "evidence": "A broad wall area is plain behind the station.",
        }
    ]
    result = scoring.aggregate_observation(value)
    assert result["natural_placement_score"] == 100.0
    assert result["verdict"] == "pass"


def test_unobservable_chair_does_not_penalize_closeup() -> None:
    value = observation()
    value["components"]["access_usability"] = {
        "visibility": "unobservable",
        "severity": None,
        "confidence": "low",
        "evidence": "The close crop excludes any possible chair position.",
        "consequence": "",
        "issue_codes": [],
        "supporting_check_ids": ["user_access"],
        "finding_ids": [],
    }
    result = scoring.aggregate_observation(value)
    assert result["verdict"] == "review"
    assert "core_component_unassessable:access_usability" in result["verdict_reasons"]


def test_schema_and_runtime_issue_codes_stay_in_sync() -> None:
    assert scoring.OBSERVATION_SCHEMA["properties"]["schema_version"]["const"] == (
        "placement-observations-v4"
    )
    definitions = scoring.OBSERVATION_SCHEMA["$defs"]
    for name, runtime_codes in scoring.ISSUE_CODES.items():
        schema_codes = definitions[name]["properties"]["issue_codes"]["items"]["enum"]
        assert len(schema_codes) == len(set(schema_codes))
        assert set(schema_codes) == set(runtime_codes)


def test_style_code_cannot_be_used_as_scored_issue() -> None:
    value = observation()
    value["components"]["support_scenario"] = component(
        1, issue_code="style_wall_unresolved"
    )
    add_finding(value, "support_scenario", 1)
    with pytest.raises(scoring.PlacementValidationError, match="style_wall_unresolved"):
        scoring.validate_observation(value)


def test_contradiction_requires_a_linked_finding() -> None:
    value = observation()
    value["inspection_checks"]["rigid_edges_corners"]["result"] = "contradiction"
    with pytest.raises(scoring.PlacementValidationError, match="contradiction requires a finding"):
        scoring.validate_observation(value)


def test_positive_component_requires_a_linked_finding() -> None:
    value = observation()
    value["components"]["scale_perspective"] = component(
        3, issue_code="missing_support_structure"
    )
    value["components"]["scale_perspective"]["finding_ids"] = []
    with pytest.raises(scoring.PlacementValidationError, match="at least one finding"):
        scoring.validate_observation(value)
