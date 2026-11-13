import json
from types import SimpleNamespace
from unittest.mock import Mock

import complete
import pytest


@pytest.fixture
def common():
    return complete.module("test_frozen_common", complete.VERSIONS / "v3_2/common.py")


def stream(path, finish=None):
    frame = {
        "id": "actual-response",
        "model": "gpt-6-astra",
        "choices": [
            {"index": 0, "delta": {"content": '{"value":1}'}, "finish_reason": finish}
        ],
    }
    complete.write(path / "chunks.jsonl", (json.dumps(frame) + "\n").encode())


def test_completed_stop_is_recovered_without_a_model_call(
    tmp_path, common, monkeypatch
):
    stream(tmp_path / "attempt01", "stop")
    call = Mock(side_effect=AssertionError("Must not redraw completed judgment"))
    monkeypatch.setattr(
        complete, "module", lambda *args: SimpleNamespace(model_completion=call)
    )
    complete.install_transport(common)
    value, receipt = common.model_completion([], {}, 12000, tmp_path)
    assert value == {"value": 1}
    assert receipt["finish_reason"] == "stop"
    assert receipt["chunks_sha256"] == complete.sha(tmp_path / "attempt01/chunks.jsonl")
    call.assert_not_called()


@pytest.mark.parametrize("finish", ["length", "content_filter"])
def test_semantic_terminal_is_never_retried(tmp_path, common, monkeypatch, finish):
    stream(tmp_path / "attempt01", finish)
    call = Mock()
    monkeypatch.setattr(
        complete, "module", lambda *args: SimpleNamespace(model_completion=call)
    )
    complete.install_transport(common)
    with pytest.raises(ValueError, match="non-stop semantic completion"):
        common.model_completion([], {}, 12000, tmp_path)
    call.assert_not_called()


def test_interrupted_stream_resumes_in_a_new_preserved_directory(
    tmp_path, common, monkeypatch
):
    stream(tmp_path / "attempt01")
    original = (tmp_path / "attempt01/chunks.jsonl").read_bytes()
    call = Mock(return_value=({"new": 1}, {"receipt": True}))
    monkeypatch.setattr(
        complete, "module", lambda *args: SimpleNamespace(model_completion=call)
    )
    complete.install_transport(common)
    assert common.model_completion([], {}, 12000, tmp_path) == (
        {"new": 1},
        {"receipt": True},
    )
    assert call.call_args.args[3] == tmp_path / "transport_recovery_0001"
    assert (tmp_path / "attempt01/chunks.jsonl").read_bytes() == original


def test_changed_request_cannot_reuse_a_completed_stream(tmp_path, common, monkeypatch):
    stream(tmp_path / "attempt01", "stop")
    call = Mock()
    monkeypatch.setattr(
        complete, "module", lambda *args: SimpleNamespace(model_completion=call)
    )
    complete.install_transport(common)
    common.model_completion([], {}, 12000, tmp_path)
    with pytest.raises(ValueError, match="frozen evidence differs"):
        common.model_completion(
            [{"role": "user", "content": "different"}], {}, 12000, tmp_path
        )
    call.assert_not_called()


def test_explicit_nontransport_error_cannot_be_redrawn(tmp_path, common, monkeypatch):
    stream(tmp_path / "attempt01")
    complete.write(
        tmp_path / "attempt01/error.json",
        {"retryable_transport_failure": False},
    )
    call = Mock()
    monkeypatch.setattr(
        complete, "module", lambda *args: SimpleNamespace(model_completion=call)
    )
    complete.install_transport(common)
    with pytest.raises(ValueError, match="semantic redraw forbidden"):
        common.model_completion([], {}, 12000, tmp_path)
    call.assert_not_called()
