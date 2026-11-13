import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from judge.placement.scoring import (
    COMPONENT_WEIGHTS,
    POLICY_VERSION,
    THRESHOLD_STATUS,
    PlacementValidationError,
    aggregate_observation,
    validate_observation,
    validate_runtime_input,
)


FIRST_CODE = {
    "support_scenario": "inappropriate_support",
    "access_usability": "excessive_reach",
    "orientation_alignment": "corner_facing",
    "scale_perspective": "implausible_scale",
    "contact_integration": "floating",
}


def make_component(name, severity=0, visibility="observed", confidence="high"):
    if visibility == "unobservable":
        severity = None
        confidence = "low"
    return {
        "visibility": visibility,
        "severity": severity,
        "confidence": confidence,
        "evidence": "Visible evidence.",
        "consequence": "Visible consequence." if severity else "No visible problem.",
        "issue_codes": [] if not severity else [FIRST_CODE[name]],
    }


def make_observation(product_match="match"):
    return {
        "schema_version": "placement-observations-v1",
        "product_match": product_match,
        "product_match_note": "The product identity is assessable.",
        "components": {
            name: make_component(name) for name in COMPONENT_WEIGHTS
        },
        "summary": "The placement is fully visible.",
        "suggested_scene_changes": [],
    }


def test_schema_is_valid_and_strict():
    schema_path = Path(__file__).with_name("observation_schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)

    observation = make_observation()
    observation["unexpected"] = True
    with pytest.raises(PlacementValidationError, match="Additional properties"):
        validate_observation(observation)


def test_schema_uses_azure_strict_subset_for_arrays_and_composition():
    schema_path = Path(__file__).with_name("observation_schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    def visit(node, path="$"):
        if isinstance(node, dict):
            assert "allOf" not in node, f"allOf is unsupported at {path}"
            if node.get("type") == "array":
                assert "items" in node, f"array has no items at {path}"
            for key, value in node.items():
                visit(value, f"{path}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                visit(value, f"{path}[{index}]")

    visit(schema)


def test_runtime_input_is_exact_and_stage_limited():
    valid = {
        "generated_image": "/tmp/generated.png",
        "twin_image": "/tmp/twin.png",
        "product_type": "printer",
        "scene_prompt": "A printer on a side table.",
        "image_stage": "scene_generation",
    }
    assert validate_runtime_input(valid) is valid

    invalid = {**valid, "image_stage": "relight"}
    with pytest.raises(PlacementValidationError, match="scene_generation"):
        validate_runtime_input(invalid)


def test_all_unobservable_is_null_score_low_confidence_review_not_zero_or_fail():
    observation = make_observation()
    observation["components"] = {
        name: make_component(name, visibility="unobservable")
        for name in COMPONENT_WEIGHTS
    }

    result = aggregate_observation(observation)

    assert result["natural_placement_score"] is None
    assert set(result["component_scores"].values()) == {None}
    assert result["coverage"] == 0.0
    assert result["confidence"] == "low"
    assert result["verdict"] == "review"
    assert result["verdict_reasons"] == ["no_assessable_components"]


def test_major_problem_veto_beats_high_average():
    observation = make_observation()
    observation["components"]["contact_integration"] = make_component(
        "contact_integration", severity=3, confidence="medium"
    )

    result = aggregate_observation(observation)

    assert result["natural_placement_score"] == 88.8
    assert result["verdict"] == "fail"
    assert result["verdict_reasons"] == ["major_problem_veto"]


def test_hidden_component_does_not_lower_normalized_score():
    observation = make_observation()
    observation["components"]["scale_perspective"] = make_component(
        "scale_perspective", visibility="unobservable"
    )

    result = aggregate_observation(observation)

    assert result["component_scores"]["scale_perspective"] is None
    assert result["natural_placement_score"] == 100.0
    assert result["coverage"] == 0.85


def test_partial_visibility_reduces_coverage_by_half_its_weight():
    observation = make_observation()
    observation["components"]["access_usability"] = make_component(
        "access_usability", severity=0, visibility="partial"
    )

    result = aggregate_observation(observation)

    assert result["natural_placement_score"] == 100.0
    assert result["coverage"] == 0.85
    assert result["confidence"] == "high"


def test_low_confidence_severe_problem_is_review():
    observation = make_observation()
    observation["components"]["contact_integration"] = make_component(
        "contact_integration", severity=3, confidence="low"
    )

    result = aggregate_observation(observation)

    assert result["natural_placement_score"] == 88.8
    assert result["confidence"] == "low"
    assert result["verdict"] == "review"
    assert "severe_problem_low_confidence" in result["verdict_reasons"]


def test_material_problem_blocks_pass_even_with_high_average():
    observation = make_observation()
    observation["components"]["contact_integration"] = make_component(
        "contact_integration", severity=2, confidence="high"
    )

    result = aggregate_observation(observation)

    assert result["natural_placement_score"] == 92.5
    assert result["confidence"] == "high"
    assert result["verdict"] == "review"
    assert "material_component_problem" in result["verdict_reasons"]


def test_product_mismatch_is_review_even_when_otherwise_passable():
    result = aggregate_observation(make_observation(product_match="mismatch"))

    assert result["natural_placement_score"] == 100.0
    assert result["verdict"] == "review"
    assert result["verdict_reasons"] == ["product_mismatch"]


def test_product_uncertain_forces_review():
    result = aggregate_observation(make_observation(product_match="uncertain"))

    assert result["natural_placement_score"] == 100.0
    assert result["verdict"] == "review"
    assert result["verdict_reasons"] == ["product_match_uncertain"]


@pytest.mark.parametrize(
    ("severity", "expected_score"),
    [(0, 100.0), (1, 75.0), (2, 50.0), (3, 25.0), (4, 0.0)],
)
def test_score_bounds(severity, expected_score):
    observation = make_observation()
    observation["components"] = {
        name: make_component(name, severity=severity)
        for name in COMPONENT_WEIGHTS
    }

    result = aggregate_observation(observation)

    assert result["natural_placement_score"] == expected_score
    assert 0 <= result["natural_placement_score"] <= 100


@pytest.mark.parametrize(
    "mutate",
    [
        lambda component: component.update(severity=1),
        lambda component: component.update(confidence="high"),
        lambda component: component.update(issue_codes=["floating"]),
    ],
)
def test_unobservable_visibility_consistency(mutate):
    observation = make_observation()
    component = make_component("support_scenario", visibility="unobservable")
    mutate(component)
    observation["components"]["support_scenario"] = component

    with pytest.raises(PlacementValidationError):
        validate_observation(observation)


def test_observable_or_partial_requires_integer_severity():
    for visibility in ("observed", "partial"):
        observation = make_observation()
        observation["components"]["access_usability"]["visibility"] = visibility
        observation["components"]["access_usability"]["severity"] = None
        with pytest.raises(PlacementValidationError, match="must be an integer"):
            validate_observation(observation)


def test_severity_and_issue_code_consistency():
    positive_without_code = make_observation()
    positive_without_code["components"]["support_scenario"].update(
        severity=1, issue_codes=[]
    )
    with pytest.raises(PlacementValidationError, match="at least one code"):
        validate_observation(positive_without_code)

    zero_with_code = make_observation()
    zero_with_code["components"]["support_scenario"]["issue_codes"] = [
        "inappropriate_support"
    ]
    with pytest.raises(PlacementValidationError, match="severity is 0"):
        validate_observation(zero_with_code)


def test_issue_codes_are_scoped_to_their_component():
    observation = make_observation()
    observation["components"]["support_scenario"].update(
        severity=1, issue_codes=["floating"]
    )

    with pytest.raises(PlacementValidationError, match="not one of"):
        validate_observation(observation)


def test_evidence_cannot_be_whitespace_only():
    observation = make_observation()
    observation["components"]["support_scenario"]["evidence"] = "  \n "

    with pytest.raises(PlacementValidationError, match="non-whitespace"):
        validate_observation(observation)


def test_score_below_60_fails_when_confidence_is_not_low():
    observation = make_observation()
    observation["components"] = {
        name: make_component(name, severity=2, confidence="medium")
        for name in COMPONENT_WEIGHTS
    }

    result = aggregate_observation(observation)

    assert result["natural_placement_score"] == 50.0
    assert result["confidence"] == "medium"
    assert result["verdict"] == "fail"
    assert result["verdict_reasons"] == ["score_below_fail_threshold"]


def test_pass_at_exact_coverage_boundary_with_core_components_assessable():
    observation = make_observation()
    for name in ("scale_perspective", "contact_integration"):
        observation["components"][name] = make_component(
            name, visibility="unobservable"
        )

    result = aggregate_observation(observation)

    assert result["coverage"] == 0.7
    assert result["confidence"] == "medium"
    assert result["verdict"] == "pass"


def test_aggregation_does_not_mutate_or_alias_observation():
    observation = make_observation()
    original = copy.deepcopy(observation)

    result = aggregate_observation(observation)

    assert observation == original
    assert result["observation"] == original
    assert result["observation"] is not observation
    assert result["threshold_status"] == THRESHOLD_STATUS
    assert result["policy_version"] == POLICY_VERSION
    assert set(result) == {
        "observation",
        "natural_placement_score",
        "component_scores",
        "coverage",
        "confidence",
        "verdict",
        "verdict_reasons",
        "threshold_status",
        "policy_version",
    }
