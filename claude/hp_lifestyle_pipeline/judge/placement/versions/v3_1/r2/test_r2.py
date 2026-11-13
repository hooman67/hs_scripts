"""Focused r2 contract tests; no model calls or per-image exceptions."""
import copy

import pytest
from jsonschema import ValidationError

import run_judge as runner
import trace_contract as contract


def component(severity=0, code=None):
    return {"visibility": "observed", "severity": severity, "confidence": "high",
            "evidence": "A visible relationship.", "consequence": "Correction needed." if severity else "",
            "issue_codes": [code] if code else []}


def envelope():
    reading = {key: "Visible relationship; hidden members are not certified." for key in
               runner.SCORING.OBSERVATION_SCHEMA["properties"]["scene_reading"]["required"]}
    reading["narrative_status"] = "supported"
    observation = {
        "schema_version": "placement-observations-v3", "product_match": "match",
        "product_match_note": "Matches the original reference.", "scene_reading": reading,
        "components": {key: component() for key in runner.SCORING.COMPONENT_WEIGHTS},
        "summary": "Visible placement assessed.", "suggested_scene_changes": [],
    }
    trace = {
        "boundary_inventory": [
            {"id": owner, "owner": owner, "role": "width", "visible_location": "Near rigid width edge.",
             "visibility": "observed", "visibility_limits": "Ends partly cropped."}
            for owner in ("product_base", "support_surface")],
        "axis_comparisons": {
            "width": {"boundary_refs": ["product_base", "support_surface"], "relationship": "compatible",
                      "projective_explanation": "Corresponding direction family is compatible.",
                      "counter_evidence": "Depth is hidden.", "visibility_limits": "Some ends cropped."},
            "depth": {"boundary_refs": [], "relationship": "indeterminate",
                      "projective_explanation": "The support depth edges are cropped.",
                      "counter_evidence": "Width remains visible.", "visibility_limits": "Depth unobservable."},
        },
        "surface_construction": {
            "visible_outline": "Continuous visible top.", "thickness_and_joins": "Visible apron continuous.",
            "visibility_limits": "Lower supports hidden.", "counter_evidence": "Hidden attachments unknown.",
        },
        "member_connections": [],
        "focused_findings": {
            focus: {"conclusion": "no_visible_material_defect", "evidence_refs": ["surface"],
                    "evidence": "No material conflict in visible relationships.",
                    "counter_evidence": "Some relationships hidden.", "visibility_limits": "Partial crop.",
                    "consequence": "", "issue_codes": []}
            for focus in ("alignment", "construction")},
    }
    return {"schema_version": contract.VERSION, "trace": trace, "observation": observation}


def test_wrapped_v3_refs_validate_and_only_original_payload_is_scored():
    value = envelope()
    original = copy.deepcopy(value)
    observation = contract.validate(value, runner.SCORING.OBSERVATION_SCHEMA)
    assert observation is value["observation"]
    runner.validate_new_observation(observation)
    result = runner.aggregate_stages(observation, observation)
    assert result["final_decision"]["verdict"] == "pass"
    assert value == original


@pytest.mark.parametrize("focus,dimension,code", [
    ("alignment", "orientation_alignment", "furniture_axis_conflict"),
    ("construction", "scale_perspective", "malformed_support_furniture"),
])
def test_material_trace_cannot_disappear_into_clear_component(focus, dimension, code):
    value = envelope()
    value["trace"]["focused_findings"][focus].update(
        conclusion="material_established", issue_codes=[code], consequence="Visible correction needed.")
    if focus == "alignment":
        value["trace"]["axis_comparisons"]["width"]["relationship"] = "different_direction_family"
    with pytest.raises(ValueError, match="material scored component"):
        contract.validate(value, runner.SCORING.OBSERVATION_SCHEMA)
    value["observation"]["components"][dimension] = component(2, code)
    observed = contract.validate(value, runner.SCORING.OBSERVATION_SCHEMA)
    result = runner.aggregate_stages(observed, observed)
    assert result["final_decision"]["verdict"] == "fail"
    assert [name for name, c in observed["components"].items() if c["severity"]] == [dimension]


@pytest.mark.parametrize("change,message", [
    ("unknown", "unknown/duplicate"),
    ("duplicate", "unique"),
    ("wrong_axis", "geometric role"),
    ("missing_owner", "both product and support"),
])
def test_trace_references_are_auditable(change, message):
    value = envelope()
    if change == "unknown":
        value["trace"]["focused_findings"]["alignment"]["evidence_refs"] = ["invented"]
    elif change == "duplicate":
        value["trace"]["boundary_inventory"][1]["id"] = "product_base"
    elif change == "wrong_axis":
        value["trace"]["boundary_inventory"][0]["role"] = "depth"
    else:
        value["trace"]["axis_comparisons"]["width"]["boundary_refs"] = ["product_base"]
    with pytest.raises(ValueError, match=message):
        contract.validate(value, runner.SCORING.OBSERVATION_SCHEMA)


def test_missing_trace_is_invalid_not_repaired():
    value = envelope()
    del value["trace"]
    with pytest.raises(ValidationError):
        contract.validate(value, runner.SCORING.OBSERVATION_SCHEMA)


def test_occluded_construction_is_not_a_missing_leg_failure():
    value = envelope()
    value["trace"]["focused_findings"]["construction"].update(conclusion="unresolved")
    value["observation"]["components"]["scale_perspective"].update(
        visibility="unobservable", severity=None, confidence="low")
    observation = contract.validate(value, runner.SCORING.OBSERVATION_SCHEMA)
    runner.validate_new_observation(observation)
    assert runner.aggregate_stages(observation, observation)["final_decision"]["verdict"] != "fail"


def test_verifier_cannot_smuggle_findings_outside_requested_components():
    value = envelope()
    names = ["access_usability"]
    value["observation"] = {
        "schema_version": "placement-verifier-components-v1",
        "components": {"access_usability": component()},
    }
    with pytest.raises(ValueError, match="unrequested dimension"):
        contract.validate(value, runner.component_schema(names))
    for finding in value["trace"]["focused_findings"].values():
        finding["conclusion"] = "not_applicable"
    observed = contract.validate(value, runner.component_schema(names))
    runner.validate_components(observed, runner.component_schema(names))


def test_nonmaterial_trace_cannot_inject_issue_codes():
    value = envelope()
    value["trace"]["focused_findings"]["construction"]["issue_codes"] = ["malformed_support_furniture"]
    with pytest.raises(ValueError, match="Non-material"):
        contract.validate(value, runner.SCORING.OBSERVATION_SCHEMA)


def test_labels_still_rejected_before_authentication():
    with pytest.raises(ValueError, match="five runtime"):
        runner.judge({"expected_label": "fail"}, "must-not-exist", client=object())
