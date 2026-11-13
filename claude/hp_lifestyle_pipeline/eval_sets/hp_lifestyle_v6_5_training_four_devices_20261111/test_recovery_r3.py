import json

import pytest

import recover_text_r3 as recovery


def test_valid_unchanged_bank_is_never_sent_to_a_provider():
    def forbidden():
        pytest.fail("valid unchanged bank was redrawn")

    with pytest.raises(ValueError, match="must never be redrawn"):
        recovery.repair_one(
            {"case_id": "valid"}, {"validation": {"passed": True}}, None, forbidden,
        )


def test_one_invalid_extra_reply_is_terminal_without_a_second_provider_call(tmp_path, monkeypatch):
    original = recovery.native.load(recovery.native.SNAPSHOT / "snapshot_manifest.json")
    case = original["cases"][0]
    monkeypatch.setattr(recovery, "SNAPSHOT", tmp_path)
    source_path = tmp_path / case["frozen_input_path"]
    source_path.parent.mkdir(parents=True)
    source_path.write_bytes((recovery.native.SNAPSHOT / case["frozen_input_path"]).read_bytes())
    config = recovery.engine(recovery.RUNTIME_SOURCE, "v6_5_training_r3")
    calls = []

    def provider(messages, schema):
        calls.append((messages, schema))
        return {
            "content": "{}", "refusal": None, "finish_reason": "stop", "model": "gpt-5.5-test",
            "usage": {}, "transport_attempts": 1, "transport_events": [],
            "settings": {"model": "gpt-5.5", "reasoning_effort": "medium",
                         "max_completion_tokens": 16000, "timeout": 180},
        }

    record = {"validation": {"passed": False, "errors": [
        {"code": "unresolved_scene_alternative", "path": "/prompts/0/text", "detail": "choose one"},
    ]}}
    result = recovery.repair_one(case, record, config, lambda: provider)
    assert result["status"] == "error"
    assert result["extra_semantic_calls"] == 1
    assert len(calls) == 1
    assert len(calls[0][0]) == 6
    assert calls[0][0][4]["role"] == "developer"
    assert json.loads(calls[0][0][4]["content"])["instruction"] == (
        recovery.RUNTIME_SOURCE / "repair_addendum.txt"
    ).read_text()
    with pytest.raises(FileExistsError, match="terminal recovery result"):
        recovery.repair_one(case, record, config, lambda: provider)
    assert len(calls) == 1


def test_interrupted_reserved_repair_is_not_reissued(tmp_path, monkeypatch):
    monkeypatch.setattr(recovery, "SNAPSHOT", tmp_path)
    (tmp_path / "journals/interrupted").mkdir(parents=True)
    with pytest.raises(FileExistsError):
        recovery.repair_one(
            {"case_id": "interrupted"}, {"validation": {"passed": False}}, None,
            lambda: pytest.fail("ambiguous request was retried"),
        )
