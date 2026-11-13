"""Model-free tests for the deterministic V2 + compact V3 ensemble."""

from __future__ import annotations

import copy

import combine


def component(
    severity: int | None,
    *,
    confidence: str = "high",
    visibility: str = "observed",
) -> dict:
    return {
        "visibility": visibility,
        "severity": severity,
        "confidence": confidence,
        "evidence": "Visible evidence.",
        "consequence": "Visible consequence." if severity else "",
        "issue_codes": ["unmotivated_position"] if severity else [],
    }


def test_highest_confirmed_positive_wins() -> None:
    assert combine.choose_component(component(2), component(3)) == (
        "compact_v3",
        "highest_confirmed_positive_severity_tie_baseline",
    )


def test_confirmed_positive_tie_prefers_baseline() -> None:
    assert combine.choose_component(component(2), component(2)) == (
        "baseline_v2",
        "highest_confirmed_positive_severity_tie_baseline",
    )


def test_assessable_baseline_is_kept_when_no_confirmed_positive() -> None:
    assert combine.choose_component(component(0), component(0)) == (
        "baseline_v2",
        "no_confirmed_positive_baseline_assessable",
    )


def test_baseline_low_confidence_material_uncertainty_is_not_erased() -> None:
    assert combine.choose_component(
        component(3, confidence="low"), component(0)
    ) == (
        "baseline_v2",
        "retained_baseline_low_confidence_material_uncertainty",
    )


def test_compact_is_used_when_baseline_unassessable() -> None:
    baseline = component(None, confidence="low", visibility="unobservable")
    assert combine.choose_component(baseline, component(0)) == (
        "compact_v3",
        "no_confirmed_positive_baseline_unassessable",
    )


def observation(product_match: str = "match") -> dict:
    scene = {
        "functional_front": "Front is visible.",
        "support_surface": "Table supports the device.",
        "usable_approach_edge": "Near edge is usable.",
        "actual_user_position": "Chair is at the near edge.",
        "access_path": "Access is clear.",
        "device_support_axes": "Axes align.",
        "neighboring_furniture": "Furniture forms one station.",
        "narrative_status": "supported",
        "narrative_evidence": "The visible use is coherent.",
        "support_placement_in_room": "The table fits the room.",
        "usable_space_distribution": "Useful space remains.",
        "alternative_user_positions": "No alternate position is needed.",
        "prop_relationships": "Props fit the station.",
        "lived_in_evidence": "Ordinary props inhabit the scene.",
    }
    return {
        "schema_version": "placement-observations-v3",
        "product_match": product_match,
        "product_match_note": "Product check.",
        "components": {name: component(0) for name in combine.SCORING.COMPONENT_WEIGHTS},
        "scene_reading": scene,
        "summary": "Stage summary.",
        "suggested_scene_changes": [],
    }


def test_product_uncertainty_from_either_stage_forces_v3_review() -> None:
    baseline = observation("uncertain")
    compact = observation("match")
    compact_scene = copy.deepcopy(compact["scene_reading"])
    merged, provenance = combine.merge_observations(baseline, compact)
    judgment = combine.SCORING.aggregate_observation(merged)
    assert merged["product_match"] == "uncertain"
    assert merged["scene_reading"] == compact_scene
    assert judgment["verdict"] == "review"
    assert judgment["verdict_reasons"] == ["product_match_uncertain"]
    assert all(value["selected_source"] == "baseline_v2" for value in provenance.values())


def test_summary_uses_evidence_and_does_not_merge_free_form_suggestions() -> None:
    baseline = observation()
    compact = observation()
    baseline["components"]["support_scenario"] = component(2)
    baseline["suggested_scene_changes"] = ["Move the table."]
    compact["suggested_scene_changes"] = ["Move the chair."]
    merged, _ = combine.merge_observations(
        baseline,
        compact,
        baseline_verdict="fail",
        compact_verdict="pass",
    )
    assert "Visible evidence." in merged["summary"]
    assert "source assessments disagreed" in merged["summary"]
    assert "support_scenario=" not in merged["summary"]
    assert merged["suggested_scene_changes"] == []


def test_input_whitelist_excludes_comment_fields() -> None:
    request = {
        "input": {
            "generated_image": "/tmp/a.png",
            "twin_image": "/tmp/b.png",
            "product_type": "printer",
            "scene_prompt": "Office.",
            "image_stage": "scene_generation",
        },
        "images": {
            "generated_image": {"sha256": "a" * 64},
            "twin_image": {"sha256": "b" * 64},
        },
    }
    identity = combine._request_identity(request)
    assert set(request["input"]) == combine.INPUT_KEYS
    assert identity["scene_prompt_sha256"]


def test_input_whitelist_rejects_comment_field() -> None:
    request = {
        "input": {
            "generated_image": "/tmp/a.png",
            "twin_image": "/tmp/b.png",
            "product_type": "printer",
            "scene_prompt": "Office.",
            "image_stage": "scene_generation",
            "human_feedback": "fail",
        },
        "images": {},
    }
    try:
        combine._request_identity(request)
    except ValueError as error:
        assert "five-field input whitelist" in str(error)
    else:
        raise AssertionError("feedback-bearing request was accepted")
