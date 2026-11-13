"""Source corrections must never manufacture human coverage requirements."""

import copy

import feedback_requirements as requirements
import pytest


def source():
    corpus = {
        "records": [
            {
                "id": "scene",
                "human_feedback": [
                    {"comment": "The chair has no legs. No workflow props."}
                ],
            }
        ]
    }
    concern = {
        "id": "chair",
        "source_quote": "The chair has no legs.",
        "scope": "supported_in_scope",
        "component": "scale_perspective",
        "issue_codes": ["malformed_support_furniture"],
        "rationale": "Visible chair construction concern.",
    }
    extra = dict(concern, id="extra", source_quote="A tabletop concern.")
    paraphrase = dict(
        concern,
        id="props",
        source_quote="Bare workflow staging.",
        component="support_scenario",
        issue_codes=["bare_staged_setting"],
    )
    result = {
        "cases": [{"case_id": "scene", "concerns": [concern, extra, paraphrase]}],
        "limitations": [],
    }
    repairs = {
        "repairs": [
            {
                "case_id": "scene",
                "concern_id": "extra",
                "origin": "astra_extra_finding",
                "verbatim_human_quote": None,
                "rationale": "Not present in human comment.",
            },
            {
                "case_id": "scene",
                "concern_id": "props",
                "origin": "human_feedback",
                "verbatim_human_quote": "No workflow props.",
                "rationale": "Exact underlying human claim.",
            },
        ]
    }
    return result, corpus, repairs


def test_origin_repair_preserves_findings_but_only_gates_actual_human_claims():
    result, corpus, repairs = source()
    original = copy.deepcopy(result)
    cases = requirements.normalize_cases(result, corpus, repairs)
    human, extra, paraphrase = cases[0]["concerns"]
    assert human["source_quote"] == original["cases"][0]["concerns"][0]["source_quote"]
    assert human["required_for_coverage_gate"] is True
    assert extra["source_quote"] is None
    assert extra["original_model_excerpt"] == "A tabletop concern."
    assert extra["scope"] == "supported_in_scope"
    assert extra["required_for_coverage_gate"] is False
    assert extra["minimum_severity"] is None
    assert paraphrase["source_quote"] == "No workflow props."
    assert paraphrase["original_model_excerpt"] == "Bare workflow staging."
    assert paraphrase["required_for_coverage_gate"] is True
    assert result == original


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "nonverbatim", "matched"])
def test_origin_corrections_cannot_drop_invent_or_reclassify_sources(mutation):
    result, corpus, repairs = source()
    if mutation == "missing":
        repairs["repairs"].pop()
    elif mutation == "duplicate":
        repairs["repairs"].append(repairs["repairs"][0])
    elif mutation == "nonverbatim":
        repairs["repairs"][1]["verbatim_human_quote"] = "Needs more props."
    else:
        repairs["repairs"][0]["concern_id"] = "chair"
    with pytest.raises(ValueError):
        requirements.normalize_cases(result, corpus, repairs)
