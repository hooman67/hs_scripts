"""Appearance penalties are distinct from the retired material-failure gate."""

import common
import evaluate
from test_common import observation

CASE = {
    "expectation": {
        "orientation_alignment": "appearance_furniture_axis_conflict",
        "scale_perspective": "appearance_malformed_support_furniture",
    }
}


def result(geometry_severity):
    value = observation()
    value["components"]["orientation_alignment"].update(
        severity=1, issue_codes=["furniture_axis_conflict"]
    )
    if geometry_severity:
        value["components"]["scale_perspective"].update(
            severity=geometry_severity, issue_codes=["malformed_support_furniture"]
        )
    score = common.LEGACY.SCORING.aggregate_observation(value)
    return {
        "application_merged_judgment": score,
        "final_decision": {"verdict": score["verdict"]},
    }


def test_minor_supported_findings_can_match_without_hard_fail():
    value = result(1)
    assert value["final_decision"]["verdict"] == "pass"
    assert all(evaluate.calibration_checks(CASE, value).values())


def test_alignment_penalty_does_not_hide_a_missing_construction_concern():
    checks = evaluate.calibration_checks(CASE, result(0))
    assert checks["orientation_alignment:appearance_furniture_axis_conflict"]
    assert not checks["scale_perspective:appearance_malformed_support_furniture"]
