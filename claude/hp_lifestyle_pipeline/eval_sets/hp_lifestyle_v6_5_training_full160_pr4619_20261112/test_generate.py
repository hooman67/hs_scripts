import base64
import json
from types import SimpleNamespace

import pytest

import generate
import study


class FakeSDK:
    def __init__(self):
        self.requests = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.chat_create))
        self.images = SimpleNamespace(edit=self.image_edit)

    def chat_create(self, **params):
        self.requests.append(params)
        body = {"choices": [{"message": {"content": '{"value":"ok"}'}, "finish_reason": "stop"}]}
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content='{"value":"ok"}'), finish_reason="stop")],
            model_dump=lambda mode: body,
        )

    def image_edit(self, **params):
        self.requests.append(params)
        value = base64.b64encode(b"untouched-native-image").decode()
        return SimpleNamespace(
            data=[SimpleNamespace(b64_json=value)],
            model_dump=lambda mode: {"data": [{"b64_json": value}]},
        )

    def close(self):
        pass


def test_recorder_preserves_both_exact_native_sdk_calls_and_raw_output(tmp_path):
    baseline, recorded = FakeSDK(), FakeSDK()
    native = generate.openai_client.OpenAIClient.__new__(generate.openai_client.OpenAIClient)
    native.client = baseline
    trace = generate.RecordingClient(tmp_path, sdk=recorded)
    for instance in (native, trace):
        assert instance.chat_json("system", "original", [("image/png", b"product")], {}) == {"value": "ok"}
        assert instance.edit_image("final", [("image/png", b"guide")], "2368x1776") == b"untouched-native-image"
    assert generate.serial(baseline.requests) == generate.serial(recorded.requests)
    calls = study.load(tmp_path / "calls.json")
    assert [call["kind"] for call in calls] == ["text", "image"]
    for call, actual in zip(calls, recorded.requests):
        path = tmp_path / call["request"]
        assert study.load(path) == generate.serial(actual)
        assert study.sha(path) == call["request_sha256"]
        assert study.sha(tmp_path / call["response"]) == call["response_sha256"]
    with pytest.raises(RuntimeError, match="One image submission"):
        trace.edit_image("final", [("image/png", b"guide")], "2368x1776")
    assert len(recorded.requests) == 2


def test_transport_errors_propagate_without_serializing_exception_secrets(tmp_path):
    sdk = FakeSDK()

    def reject(**params):
        raise RuntimeError("sensitive-example-not-to-persist")

    sdk.chat.completions.create = reject
    trace = generate.RecordingClient(tmp_path, sdk=sdk)
    with pytest.raises(RuntimeError, match="sensitive-example"):
        trace.chat_json("system", "request", [], {})
    journal = (tmp_path / "calls.json").read_text()
    assert study.load(tmp_path / "calls.json")[0]["status"] == "error"
    assert "sensitive-example" not in journal
    assert not list(tmp_path.glob("*.response.json"))


def test_retry_gate_rejects_successful_or_ambiguous_image_submissions():
    assert generate.may_retry([{"kind": "text", "status": "done"}])
    assert generate.may_retry([{"kind": "image", "status": "error", "status_code": 429}])
    for call in (
        {"kind": "image", "status": "started"},
        {"kind": "image", "status": "done"},
        {"kind": "image", "status": "error", "status_code": None},
        {"kind": "image", "status": "error", "status_code": 500},
    ):
        assert not generate.may_retry([call])


def test_no_statistics_fallback_preserves_semantic_evidence_guards():
    profiles = generate.fallback.FallbackProfiles(generate.PROFILES)
    prompt = "A printer workspace in a cafe."
    selection = {"environment": "Cafe", "prompt_quote": "cafe", "reason": "The original setting is explicit."}
    context = profiles.select(prompt, "printer", selection)
    assert context["statistics_disabled"] is True
    assert context["family"] == "Printer" and context["matched_environment"] is None
    assert context["cohort_n"] is None and context["fields"] == {}
    with pytest.raises(ValueError, match="exact original user prompt quote"):
        profiles.select(prompt, "printer", {**selection, "prompt_quote": "not present"})
    with pytest.raises(ValueError, match="Unknown semantic environment"):
        profiles.select(prompt, "printer", {**selection, "environment": "Invented unrelated cohort"})
    with pytest.raises(ValueError, match="No matching statistics product family"):
        profiles.select(prompt, "desktop", selection)


def test_completed_resume_rejects_changed_native_pixels_or_prompt_binding(tmp_path):
    output = tmp_path / "output.png"
    result = tmp_path / "result.json"
    calls = tmp_path / "calls.json"
    for path in (output, result, calls):
        path.write_bytes(b"frozen")
    case = {"id": "test", "prompt_key": "test::p1", "prompt": {"text_sha256": "source"}}
    record = {
        "prompt_key": case["prompt_key"], "prompt_sha256": "source",
        "image_path": str(output), "image_sha256": study.sha(output),
        "result_path": str(result), "result_sha256": study.sha(result),
        "calls_path": str(calls), "calls_sha256": study.sha(calls),
    }
    study.emit(tmp_path / "completed/test.json", record)
    assert generate.completed(tmp_path, case) == record
    output.write_bytes(b"changed")
    with pytest.raises(ValueError, match="provenance changed"):
        generate.completed(tmp_path, case)
    output.write_bytes(b"frozen")
    altered = json.loads(json.dumps(case))
    altered["prompt"]["text_sha256"] = "different-source"
    with pytest.raises(ValueError, match="provenance changed"):
        generate.completed(tmp_path, altered)
