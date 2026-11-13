"""Completed semantics survive transport-close errors without resampling."""

import httpx
import openai
import pytest
import transport
from test_common import FakeClient, FakeStream, frame


def test_stop_survives_stream_close_connection_error(tmp_path):
    class Stream(FakeStream):
        def __exit__(self, *_):
            raise ConnectionError("Connection closed after the final model choice")

    client = FakeClient([])
    client.create = lambda **kwargs: Stream([frame('{"a":1}', "stop")])
    result, receipt = transport.model_completion([], None, 100, tmp_path, client)
    assert result == {"a": 1}
    assert receipt["transport_attempts"] == 1
    assert receipt["post_completion_close_error"] == "ConnectionError"
    assert not (tmp_path / "attempt02").exists()


def test_invalid_completed_body_never_resampled_after_close_error(tmp_path):
    class Stream(FakeStream):
        def __exit__(self, *_):
            raise ConnectionError("Connection closed after invalid completed JSON")

    client = FakeClient([])
    client.create = lambda **kwargs: Stream([frame('{"a":', "stop")])
    with pytest.raises(ValueError):
        transport.model_completion([], None, 100, tmp_path, client)
    assert not (tmp_path / "attempt02").exists()


def test_explicit_stream_server_error_retries_but_unknown_api_error_does_not(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(transport.time, "sleep", lambda _: None)
    request = httpx.Request("POST", "https://example.invalid")
    known = openai.APIError(
        "server failure", request, body={"error": {"type": "server_error"}}
    )
    unknown = openai.APIError(
        "unknown", request, body={"error": {"code": "unclassified_error"}}
    )
    client = FakeClient([known, [frame('{"a":2}', "stop")]])
    result, receipt = transport.model_completion([], None, 100, tmp_path, client)
    assert result == {"a": 2}
    assert receipt["transport_attempts"] == 2
    assert not transport.retryable(unknown)
    assert (
        transport.api_error_fields(
            openai.APIError(
                "unknown",
                request,
                body={
                    "error": {
                        "code": "Bearer should-not-be-recorded",
                        "message": "private",
                    }
                },
            )
        )
        == {}
    )
