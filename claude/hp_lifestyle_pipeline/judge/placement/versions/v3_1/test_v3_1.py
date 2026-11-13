"""Focused semantics/ensemble tests; no model calls."""
from __future__ import annotations

import copy

import pytest

import run_judge as runner


def component(severity=0, code=None, confidence="high"):
    return {"visibility": "observed", "severity": severity, "confidence": confidence,
            "evidence": "Visible relation supports this assessment.",
            "consequence": "Material correction required." if severity >= 2 else "",
            "issue_codes": [code] if code else []}


def observation():
    schema = runner.SCORING.OBSERVATION_SCHEMA
    reading = {name: "Visible relation described." for name in
               schema["properties"]["scene_reading"]["required"]}
    reading["narrative_status"] = "supported"
    return {
        "schema_version": "placement-observations-v3",
        "product_match": "match", "product_match_note": "Visible device matches twin.",
        "scene_reading": reading,
        "components": {n: component() for n in runner.SCORING.COMPONENT_WEIGHTS},
        "summary": "Visible placement assessed.", "suggested_scene_changes": [],
    }


def test_retired_chair_code_rejected_in_primary_and_verifier():
    value = observation()
    value["components"]["orientation_alignment"] = component(2, "chair_alignment_conflict")
    runner.SCORING.validate_observation(value)
    with pytest.raises(ValueError, match="historical chair_alignment_conflict"):
        runner.validate_new_observation(value)
    names = ["orientation_alignment"]
    with pytest.raises(Exception):
        runner.validate_components({
            "schema_version": "placement-verifier-components-v1",
            "components": {"orientation_alignment": value["components"]["orientation_alignment"]},
        }, runner.component_schema(names))


@pytest.mark.parametrize("dimension,code", [
    ("orientation_alignment", "furniture_axis_conflict"),
    ("scale_perspective", "malformed_support_furniture"),
])
def test_table_alignment_and_furniture_geometry_each_independently_veto_pass(dimension, code):
    value = observation()
    value["components"][dimension] = component(2, code)
    original = copy.deepcopy(value)
    result = runner.aggregate_stages(value, value)
    assert result["final_decision"]["verdict"] == "fail"
    assert result["application_merged_judgment"]["natural_placement_score"] == 59
    assert value == original
    assert [n for n, c in result["application_merged_judgment"]["observation"]["components"].items()
            if c["severity"]] == [dimension]


def test_cropped_geometry_is_unknown_not_invented_missing_legs():
    value = observation()
    value["components"]["scale_perspective"] = {
        **component(), "visibility": "unobservable", "severity": None,
        "confidence": "low", "evidence": "Legs and attachments are outside the crop.",
    }
    result = runner.aggregate_stages(value, value)
    assert result["final_decision"]["verdict"] != "fail"
    assert result["application_merged_judgment"]["component_scores"]["scale_perspective"] is None


def test_minor_table_offset_preserves_v3_severity_policy():
    value = observation()
    value["components"]["orientation_alignment"] = component(1, "furniture_axis_conflict")
    result = runner.aggregate_stages(value, value)
    assert result["final_decision"]["verdict"] == "pass"


def test_new_material_geometry_requires_both_checks_and_preserves_disagreement():
    baseline = observation()
    compact = observation()
    compact["components"]["scale_perspective"] = component(2, "malformed_support_furniture")
    with pytest.raises(ValueError, match="both independent"):
        runner.aggregate_stages(baseline, compact)
    proposal = {"schema_version": "placement-verifier-components-v1",
                "components": {"scale_perspective": component(2, "malformed_support_furniture")}}
    independent = {"schema_version": "placement-verifier-components-v1",
                   "components": {"scale_perspective": component()}}
    result = runner.aggregate_stages(baseline, compact, proposal, independent)
    assert result["final_decision"]["verdict"] == "pass"
    assert result["final_decision"]["reported_overall_confidence"] == "medium"
    resolution = result["consensus_resolution"]["scale_perspective"]
    assert resolution["status"] == "rejected_confident_clear_or_minor"
    assert resolution["proposal_aware"]["severity"] == 2
    assert resolution["names_only_independent"]["severity"] == 0
    assert compact["components"]["scale_perspective"]["severity"] == 2


def test_material_consensus_retains_only_shared_codes_and_lower_severity():
    baseline, compact = observation(), observation()
    compact["components"]["scale_perspective"] = component(3, "malformed_support_furniture")
    proposal = {"schema_version": "placement-verifier-components-v1",
                "components": {"scale_perspective": {
                    **component(3, "malformed_support_furniture"),
                    "issue_codes": ["malformed_support_furniture", "conflicting_perspective"]}}}
    independent = {"schema_version": "placement-verifier-components-v1",
                   "components": {"scale_perspective": component(
                       2, "malformed_support_furniture", confidence="medium")}}
    result = runner.aggregate_stages(baseline, compact, proposal, independent)
    selected = result["application_merged_judgment"]["observation"]["components"]["scale_perspective"]
    assert selected["severity"] == 2
    assert selected["confidence"] == "medium"
    assert selected["issue_codes"] == ["malformed_support_furniture"]
    assert result["final_decision"]["verdict"] == "fail"


def test_model_input_rejects_target_labels_before_authentication():
    with pytest.raises(ValueError, match="five runtime"):
        runner.judge({"human_feedback": "fail"}, "must-not-exist", client=object())


def test_malformed_verifier_cannot_smuggle_unsupported_code_or_empty_evidence():
    schema = runner.component_schema(["scale_perspective"])
    value = {"schema_version": "placement-verifier-components-v1",
             "components": {"scale_perspective": {
                 **component(2, "malformed_support_furniture"), "evidence": " "}}}
    with pytest.raises(ValueError, match="non-whitespace"):
        runner.validate_components(value, schema)


def test_original_v3_adapter_retains_old_schema_and_chair_code_without_affecting_v31():
    import frozen_v3

    compact = observation()
    baseline = observation()
    baseline["schema_version"] = "placement-observations-v2"
    baseline["scene_reading"] = {
        key: baseline["scene_reading"][key]
        for key in frozen_v3.V2_SCORING.OBSERVATION_SCHEMA["properties"]["scene_reading"]["required"]
    }
    baseline["components"]["orientation_alignment"] = component(2, "chair_alignment_conflict")
    result = frozen_v3.aggregate(baseline, compact)
    assert result["final_decision"]["verdict"] == "fail"
    assert result["application_merged_judgment"]["observation"]["components"][
        "orientation_alignment"]["issue_codes"] == ["chair_alignment_conflict"]
    assert frozen_v3.BASELINE.OBSERVATION_SCHEMA["properties"]["schema_version"]["const"] == (
        "placement-observations-v2")
    assert frozen_v3.COMPACT.OBSERVATION_SCHEMA["properties"]["schema_version"]["const"] == (
        "placement-observations-v3")
