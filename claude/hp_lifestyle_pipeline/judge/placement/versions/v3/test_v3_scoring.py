"""Focused deterministic scoring checks for the placement V3 policy."""

from __future__ import annotations

import pytest

import scoring


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
    }


def observation() -> dict:
    return {
        "schema_version": "placement-observations-v3",
        "product_match": "match",
        "product_match_note": "The generated device matches the supplied twin.",
        "components": {
            name: component() for name in scoring.COMPONENT_WEIGHTS
        },
        "summary": "The visible placement is assessed across all five components.",
        "suggested_scene_changes": [],
        "scene_reading": dict(SCENE_READING),
    }


def test_minor_background_staging_issue_remains_pass() -> None:
    value = observation()
    value["components"]["support_scenario"] = component(
        1, issue_code="bare_staged_setting"
    )

    result = scoring.aggregate_observation(value)

    assert result["weighted_component_score"] == 95.0
    assert result["natural_placement_score"] == 95.0
    assert result["applied_score_cap"] is None
    assert result["verdict"] == "pass"
    assert result["verdict_reasons"] == ["pass_criteria_met"]


def test_misplaced_support_furniture_severity_two_fails() -> None:
    value = observation()
    value["components"]["support_scenario"] = component(
        2,
        confidence="medium",
        issue_code="misplaced_support_furniture",
    )

    result = scoring.aggregate_observation(value)

    assert result["weighted_component_score"] == 90.0
    assert result["natural_placement_score"] == 59
    assert result["applied_score_cap"] == 59
    assert result["verdict"] == "fail"
    assert result["verdict_reasons"] == ["clear_placement_defect_veto"]


def test_ambiguous_seat_access_severity_two_low_confidence_is_review() -> None:
    value = observation()
    value["components"]["access_usability"] = component(
        2,
        confidence="low",
        issue_code="excessive_reach",
    )

    result = scoring.aggregate_observation(value)

    assert result["weighted_component_score"] == 85.0
    assert result["natural_placement_score"] == 85.0
    assert result["applied_score_cap"] is None
    assert result["confidence"] == "low"
    assert result["verdict"] == "review"
    assert "core_component_low_confidence:access_usability" in result["verdict_reasons"]
    assert "severe_problem_low_confidence" in result["verdict_reasons"]


def test_v3_schema_and_runtime_issue_codes_stay_in_sync() -> None:
    assert scoring.OBSERVATION_SCHEMA["properties"]["schema_version"]["const"] == (
        "placement-observations-v3"
    )
    assert set(
        scoring.OBSERVATION_SCHEMA["properties"]["scene_reading"]["required"]
    ) == set(SCENE_READING)
    definitions = scoring.OBSERVATION_SCHEMA["$defs"]
    for name, runtime_codes in scoring.ISSUE_CODES.items():
        schema_codes = definitions[name]["properties"]["issue_codes"]["items"]["enum"]
        assert len(schema_codes) == len(set(schema_codes))
        assert set(schema_codes) == set(runtime_codes)


def test_new_support_code_cannot_be_used_for_access() -> None:
    value = observation()
    value["components"]["access_usability"] = component(
        1, issue_code="bare_staged_setting"
    )

    with pytest.raises(scoring.PlacementValidationError, match="bare_staged_setting"):
        scoring.validate_observation(value)
