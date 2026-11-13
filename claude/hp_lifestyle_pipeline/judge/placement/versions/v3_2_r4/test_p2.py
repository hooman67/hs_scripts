"""Offline P2 contracts and mandatory independent-discovery orchestration."""

from __future__ import annotations

import copy
import hashlib
import uuid
from pathlib import Path
from unittest.mock import Mock

import p2
import pytest
from jsonschema import Draft202012Validator, ValidationError


def finding(severity=0, code=None, **changes):
    return {
        "visibility": "observed",
        "severity": severity,
        "confidence": "high",
        "evidence": "The exposed relation supports this finding.",
        "counter_evidence": "",
        "limit": "",
        "consequence": "",
        "issue_codes": [code] if code else [],
        **changes,
    }


def discovery(kind):
    names = {
        "geometry": (
            "support_construction",
            "rigid_alignment",
            "relative_scale_perspective",
            "product_contact",
        ),
        "use": ("support_scenario", "access_usability", "layout_orientation"),
    }[kind]
    return {
        "schema_version": f"placement-{'geometry' if kind == 'geometry' else 'use'}-discovery-v1",
        "product_match": "match",
        "product_match_note": "Visible target matches the reference.",
        "findings": {name: finding() for name in names},
    }


def final_observation():
    scoring = p2.common.LEGACY.SCORING
    reading = {
        name: "Visible relationship assessed."
        for name in p2.common.OBSERVATION_SCHEMA["properties"]["scene_reading"][
            "required"
        ]
    }
    reading["narrative_status"] = "supported"
    return {
        "schema_version": "placement-observations-v3",
        "product_match": "match",
        "product_match_note": "Visible target matches the reference.",
        "scene_reading": reading,
        "components": {
            name: {
                key: value
                for key, value in finding().items()
                if key not in {"counter_evidence", "limit"}
            }
            for name in scoring.COMPONENT_WEIGHTS
        },
        "summary": "Visible natural placement assessed.",
        "suggested_scene_changes": [],
    }


SPECIALISTS = [
    (
        "geometry",
        p2.validate_geometry,
        p2.GEOMETRY_SCHEMA,
        "rigid_alignment",
        "furniture_axis_conflict",
    ),
    (
        "use",
        p2.validate_use,
        p2.USE_SCHEMA,
        "access_usability",
        "blocked_operating_side",
    ),
]


@pytest.mark.parametrize("kind,validate,schema,name,code", SPECIALISTS)
@pytest.mark.parametrize(
    "visibility,severity,confidence,codes",
    [
        ("observed", 0, "high", False),
        ("partial", 1, "medium", True),
        ("observed", 2, "high", True),
        ("partial", 3, "low", True),
        ("observed", 4, "high", True),
        ("unobservable", None, "low", False),
    ],
)
def test_specialist_contract_accepts_assessed_and_unobservable_findings(
    kind,
    validate,
    schema,
    name,
    code,
    visibility,
    severity,
    confidence,
    codes,
):
    value = discovery(kind)
    value["findings"][name] = finding(
        severity,
        code if codes else None,
        visibility=visibility,
        confidence=confidence,
        counter_evidence="A compatible alternative remains visible.",
        limit="One relationship is occluded.",
        consequence="Correction is needed." if codes else "",
    )
    original = copy.deepcopy(value)
    Draft202012Validator(schema).validate(value)
    assert validate(value) is value
    assert value == original


@pytest.mark.parametrize("kind,validate,schema,name,code", SPECIALISTS)
@pytest.mark.parametrize(
    "changes",
    [
        {"visibility": "unobservable", "severity": 0, "confidence": "low"},
        {"visibility": "unobservable", "severity": None, "confidence": "medium"},
        {
            "visibility": "unobservable",
            "severity": None,
            "confidence": "low",
            "issue_codes": ["CODE"],
        },
        {"severity": None},
        {"severity": 0, "issue_codes": ["CODE"]},
        {"severity": 2, "issue_codes": []},
        {"severity": -1},
        {"severity": 5},
        {"severity": True},
        {"severity": 1.0, "issue_codes": ["CODE"]},
        {"severity": 1.5, "issue_codes": ["CODE"]},
        {"severity": "2", "issue_codes": ["CODE"]},
        {"severity": 2, "issue_codes": ["CODE", "CODE"]},
        {"evidence": " \n\t"},
        {"evidence": ""},
        {"counter_evidence": []},
        {"limit": None},
        {"consequence": {}},
        {"recommendation": "Invent an alternate support."},
    ],
)
def test_specialist_malformed_semantics_and_field_types_fail_closed(
    kind,
    validate,
    schema,
    name,
    code,
    changes,
):
    changes = copy.deepcopy(changes)
    if "issue_codes" in changes:
        changes["issue_codes"] = [
            code if item == "CODE" else item for item in changes["issue_codes"]
        ]
    value = discovery(kind)
    value["findings"][name].update(changes)
    with pytest.raises((ValueError, ValidationError)):
        validate(value)


@pytest.mark.parametrize(
    "kind,validate,name,code",
    [
        ("geometry", p2.validate_geometry, "support_construction", "floating"),
        (
            "geometry",
            p2.validate_geometry,
            "rigid_alignment",
            "conflicting_perspective",
        ),
        (
            "geometry",
            p2.validate_geometry,
            "relative_scale_perspective",
            "malformed_support_furniture",
        ),
        ("geometry", p2.validate_geometry, "product_contact", "unsupported_base"),
        ("use", p2.validate_use, "support_scenario", "blocked_user_workspace"),
        ("use", p2.validate_use, "access_usability", "unsupported_base"),
        ("use", p2.validate_use, "layout_orientation", "corner_facing"),
        (
            "geometry",
            p2.validate_geometry,
            "rigid_alignment",
            "chair_alignment_conflict",
        ),
        ("use", p2.validate_use, "layout_orientation", "chair_alignment_conflict"),
        ("use", p2.validate_use, "access_usability", "invented_code"),
    ],
)
def test_codes_cannot_cross_specialist_scopes_or_use_retired_registry(
    kind, validate, name, code
):
    value = discovery(kind)
    value["findings"][name] = finding(2, code)
    with pytest.raises(ValidationError):
        validate(value)


@pytest.mark.parametrize("kind,validate,schema,name,code", SPECIALISTS)
@pytest.mark.parametrize(
    "mutation",
    [
        "missing_finding",
        "extra_finding",
        "missing_string",
        "extra_top_level",
        "wrong_version",
    ],
)
def test_exact_discovery_shapes_cannot_drop_coverage_or_add_outputs(
    kind,
    validate,
    schema,
    name,
    code,
    mutation,
):
    value = discovery(kind)
    if mutation == "missing_finding":
        del value["findings"][name]
    elif mutation == "extra_finding":
        value["findings"]["out_of_scope"] = finding()
    elif mutation == "missing_string":
        del value["findings"][name]["counter_evidence"]
    elif mutation == "extra_top_level":
        value["verdict"] = "pass"
    else:
        value["schema_version"] = "placement-observations-v3"
    with pytest.raises(ValidationError):
        validate(value)


@pytest.fixture
def harness(monkeypatch):
    geometry, use_location, final = (
        discovery("geometry"),
        discovery("use"),
        final_observation(),
    )
    observations = {
        "p2_geometry": geometry,
        "p2_use": use_location,
        "p2_reconcile": final,
    }
    calls, writes = [], []
    failures = {}
    output = Path(__file__).resolve().parent / f".p2-offline-output-{uuid.uuid4().hex}"
    runtime_input = {
        "generated_image": "/offline/generated.png",
        "twin_image": "/offline/twin.png",
        "product_type": "laptop",
        "scene_prompt": "A device on an ordinary working surface.",
        "image_stage": "scene_generation",
    }
    client = object()

    def call_stage(
        runtime_input,
        stage,
        output,
        schema,
        validator,
        *,
        reports=None,
        cap=12000,
        client=None,
    ):
        calls.append(
            {
                "runtime_input": runtime_input,
                "stage": stage,
                "output": output,
                "schema": schema,
                "validator": validator,
                "reports": copy.deepcopy(reports),
                "cap": cap,
                "client": client,
            }
        )
        if stage in failures:
            raise failures[stage]
        observation = observations[stage]
        validator(observation)
        return {
            "ok": True,
            "observation": observation,
            "model_returned": "offline-fake",
            "visual_acquisition": {"record": stage + " neutral acquisition"},
        }

    freeze = Mock(return_value="f" * 64)
    digest = Mock(
        side_effect=lambda path: hashlib.sha256(str(path).encode()).hexdigest()
    )
    aggregate = Mock(wraps=p2.common.LEGACY.SCORING.aggregate_observation)
    monkeypatch.setattr(p2.common, "verify_freeze", freeze)
    monkeypatch.setattr(p2.common, "call_stage", call_stage)
    monkeypatch.setattr(p2.common, "sha", digest)
    monkeypatch.setattr(
        p2.common,
        "write_json",
        lambda path, value: writes.append((path, copy.deepcopy(value))),
    )
    monkeypatch.setattr(p2.common.LEGACY.SCORING, "aggregate_observation", aggregate)
    return {
        "geometry": geometry,
        "use": use_location,
        "final": final,
        "observations": observations,
        "calls": calls,
        "writes": writes,
        "failures": failures,
        "output": output,
        "runtime_input": runtime_input,
        "client": client,
        "freeze": freeze,
        "digest": digest,
        "aggregate": aggregate,
    }


@pytest.mark.parametrize(
    "criterion,code,component",
    [
        ("support_construction", "malformed_support_furniture", "scale_perspective"),
        ("rigid_alignment", "furniture_axis_conflict", "orientation_alignment"),
        ("relative_scale_perspective", "conflicting_perspective", "scale_perspective"),
        ("product_contact", "floating", "contact_integration"),
    ],
)
@pytest.mark.parametrize("final_severity", [0, 2])
def test_geometry_discovery_is_independent_of_clear_use_and_only_reconciler_is_scored(
    harness,
    criterion,
    code,
    component,
    final_severity,
):
    h = harness
    h["geometry"]["findings"][criterion] = finding(3, code)
    if final_severity:
        h["final"]["components"][component].update(
            severity=final_severity,
            issue_codes=[code],
            evidence="The image independently establishes this material relationship.",
        )
    original = copy.deepcopy(h["observations"])
    result = p2.judge(h["runtime_input"], h["output"], client=h["client"])

    assert [call["stage"] for call in h["calls"]] == [
        "p2_geometry",
        "p2_use",
        "p2_reconcile",
    ]
    assert [call["cap"] for call in h["calls"]] == [12000, 12000, 12000]
    assert [call["reports"] for call in h["calls"][:2]] == [None, None]
    assert h["calls"][2]["reports"] == {
        "geometry": h["geometry"],
        "use_location": h["use"],
        "geometry_acquisition": "p2_geometry neutral acquisition",
        "use_acquisition": "p2_use neutral acquisition",
    }
    assert all(call["runtime_input"] is h["runtime_input"] for call in h["calls"])
    assert all(call["client"] is h["client"] for call in h["calls"])
    assert h["calls"][2]["validator"] is p2.common.LEGACY.validate_new_observation
    h["aggregate"].assert_called_once_with(h["final"])
    assert result["application_merged_judgment"]["observation"] == h["final"]
    assert result["final_decision"] == {"verdict": "fail" if final_severity else "pass"}
    assert result["application_merged_judgment"]["natural_placement_score"] == (
        59 if final_severity else 100
    )
    assert h["observations"] == original
    assert h["writes"] == [(h["output"] / "result.json", result)]
    assert result["protocol_version"] == "placement-v3.2-p2-r4"
    assert result["ok"] is True
    assert result["candidate"] == "p2"
    assert result["runtime_input"] == h["runtime_input"]
    assert result["protocol_freeze_sha256"] == "f" * 64
    assert set(result["stages"]) == {"p2_geometry", "p2_use", "p2_reconcile"}
    for stage, record in result["stages"].items():
        stage_path = h["output"] / stage / "result.json"
        assert record == {
            "path": str(stage_path.resolve()),
            "sha256": hashlib.sha256(str(stage_path).encode()).hexdigest(),
        }
    assert h["digest"].call_count == 3


@pytest.mark.parametrize(
    "stage,expected_calls",
    [
        ("p2_geometry", ["p2_geometry"]),
        ("p2_use", ["p2_geometry", "p2_use"]),
        ("p2_reconcile", ["p2_geometry", "p2_use", "p2_reconcile"]),
    ],
)
def test_mandatory_stage_errors_never_become_passes(harness, stage, expected_calls):
    h = harness
    error = RuntimeError(f"{stage} failed")
    h["failures"][stage] = error
    with pytest.raises(RuntimeError, match=f"{stage} failed") as raised:
        p2.judge(h["runtime_input"], h["output"], client=h["client"])
    assert raised.value is error
    assert [call["stage"] for call in h["calls"]] == expected_calls
    h["aggregate"].assert_not_called()
    assert h["writes"] == []


@pytest.mark.parametrize("stage", ["p2_geometry", "p2_use", "p2_reconcile"])
def test_invalid_mandatory_observations_are_not_repaired_or_scored(harness, stage):
    h = harness
    if stage == "p2_geometry":
        del h["geometry"]["findings"]["product_contact"]
    elif stage == "p2_use":
        h["use"]["findings"]["support_scenario"]["evidence"] = " "
    else:
        h["final"]["components"]["orientation_alignment"].update(
            severity=2,
            issue_codes=["chair_alignment_conflict"],
        )
    with pytest.raises((ValueError, ValidationError)):
        p2.judge(h["runtime_input"], h["output"], client=h["client"])
    h["aggregate"].assert_not_called()
    assert h["writes"] == []


@pytest.mark.parametrize(
    "field,value",
    [
        ("human_feedback", "Known failed case"),
        ("label", "pass"),
        ("image_stage", "relighting"),
        ("product_type", "unknown"),
    ],
)
def test_invalid_or_labeled_runtime_is_rejected_before_freeze_or_stages(
    harness, field, value
):
    h = harness
    runtime_input = {**h["runtime_input"], field: value}
    with pytest.raises(ValueError):
        p2.judge(runtime_input, h["output"], client=h["client"])
    h["freeze"].assert_not_called()
    h["aggregate"].assert_not_called()
    assert h["calls"] == []
    assert h["writes"] == []
