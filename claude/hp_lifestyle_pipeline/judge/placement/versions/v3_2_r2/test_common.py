"""Transport evidence, no semantic retry, and P1 trigger regression tests."""

import copy
import json
from pathlib import Path
from types import SimpleNamespace

import common
import p1
import pytest
from jsonschema.exceptions import ValidationError


def observation():
    return {
        "schema_version": "placement-observations-v3",
        "product_match": "match",
        "product_match_note": "Reference product matched.",
        "scene_reading": {
            key: ("supported" if key == "narrative_status" else "Visible relation.")
            for key in common.OBSERVATION_SCHEMA["properties"]["scene_reading"][
                "required"
            ]
        },
        "components": {
            name: {
                "visibility": "observed",
                "severity": 0,
                "confidence": "high",
                "evidence": "Coherent visible support.",
                "consequence": "",
                "issue_codes": [],
            }
            for name in common.SCORING.COMPONENT_WEIGHTS
        },
        "summary": "Visible placement is coherent.",
        "suggested_scene_changes": [],
    }


def frame(text=None, finish=None, model=common.MODEL):
    return {
        "id": "test-response",
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": {"content": text},
                "finish_reason": finish,
            }
        ],
    }


class FakeStream:
    def __init__(self, frames):
        self.frames = frames

    def __enter__(self):
        return iter(
            SimpleNamespace(model_dump=lambda mode, f=f: f) for f in self.frames
        )

    def __exit__(self, *_):
        pass


class FakeClient:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
        self.requests = []
        self.chat = SimpleNamespace(completions=self)

    def create(self, **kwargs):
        self.requests.append(kwargs)
        value = next(self.outcomes)
        if isinstance(value, Exception):
            raise value
        return FakeStream(value)


def test_stream_transport_recovery_preserves_attempts(tmp_path, monkeypatch):
    monkeypatch.setattr(common.time, "sleep", lambda _: None)
    client = FakeClient(
        [ConnectionError("transport"), [frame('{"a":1}'), frame(finish="stop")]]
    )
    value, receipt = common.model_completion([], None, 100, tmp_path, client)
    assert value == {"a": 1}
    assert receipt["transport_attempts"] == 2
    assert (tmp_path / "attempt01/error.json").exists()
    assert common.sha(receipt["chunks_path"]) == receipt["chunks_sha256"]
    assert all(request["model"] == "gpt-6-astra" for request in client.requests)


@pytest.mark.parametrize(
    "finish,model", [("length", common.MODEL), ("stop", "gpt-5.5")]
)
def test_semantic_or_identity_failure_never_resampled(tmp_path, finish, model):
    client = FakeClient([[frame('{"a":1}', finish, model)]])
    with pytest.raises(ValueError):
        common.model_completion([], None, 100, tmp_path, client)
    assert len(client.requests) == 1
    assert not (tmp_path / "attempt02").exists()


def test_partial_stream_is_not_a_pass(tmp_path, monkeypatch):
    monkeypatch.setattr(common.time, "sleep", lambda _: None)
    client = FakeClient([[frame('{"a":')], [frame('{"a":2}', "stop")]])
    value, receipt = common.model_completion([], None, 100, tmp_path, client)
    assert value == {"a": 2}
    assert receipt["transport_attempts"] == 2
    assert (tmp_path / "attempt01/partial_output.txt").read_text() == '{"a":'


@pytest.mark.parametrize("compact_material", [False, True])
def test_p1_verifier_contract_and_blindness(tmp_path, monkeypatch, compact_material):
    monkeypatch.setattr(common, "verify_freeze", lambda: "fixed")
    stages = []

    def stage(runtime_input, name, output, schema, validator, **kwargs):
        stages.append((name, copy.deepcopy(kwargs.get("reports"))))
        value = observation()
        if name == "p1_compact" and compact_material:
            component = value["components"]["orientation_alignment"]
            component.update(
                severity=2,
                evidence="Visible rigid support axis conflict.",
                issue_codes=["furniture_axis_conflict"],
            )
        if name in ("p1_proposal", "p1_independent"):
            assert (
                schema["properties"]["schema_version"]["const"]
                == "placement-verifier-components-v1"
            )
            assert schema["properties"]["components"]["required"] == [
                "orientation_alignment"
            ]
            value = {
                "schema_version": "placement-verifier-components-v1",
                "components": {
                    "orientation_alignment": {
                        "visibility": "observed",
                        "severity": 2,
                        "confidence": "high",
                        "evidence": "Visible rigid axes disagree.",
                        "consequence": "Material skew.",
                        "issue_codes": ["furniture_axis_conflict"],
                    }
                },
            }
        validator(value)
        result = {"observation": value}
        common.write_json(Path(output) / "result.json", result)
        return result

    monkeypatch.setattr(common, "call_stage", stage)
    runtime = {
        "generated_image": "/scene.png",
        "twin_image": "/twin.png",
        "product_type": "laptop",
        "scene_prompt": "A studio.",
        "image_stage": "scene_generation",
    }
    result = p1.judge(runtime, tmp_path)
    assert len(stages) == (4 if compact_material else 2)
    if compact_material:
        assert result["final_decision"]["verdict"] == "fail"
        assert "proposals" in stages[2][1]
        assert stages[3][1] == {"requested_components": ["orientation_alignment"]}
    else:
        assert result["final_decision"]["verdict"] == "pass"


def test_observation_fixture_uses_actual_contract():
    common.LEGACY.validate_new_observation(observation())


def test_collector_does_not_conflate_response_ids():
    collector = common.Collector()
    collector.feed(frame('{"a":'))
    other = frame("1}", "stop")
    other["id"] = "another-response"
    with pytest.raises(ValueError, match="identities"):
        collector.feed(other)


def test_verifier_refuses_full_observation_and_unrequested_components():
    schema = common.LEGACY.component_schema(["orientation_alignment"])
    with pytest.raises(ValidationError):
        common.LEGACY.validate_components(observation(), schema)
    value = {
        "schema_version": "placement-verifier-components-v1",
        "components": observation()["components"],
    }
    with pytest.raises(ValidationError):
        common.LEGACY.validate_components(value, schema)
    assert json.dumps(value)
