from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from astra_provider import MODEL, AstraProvider
from hp_prompt_writer_v6_4.provider import ProviderUnavailable
from hp_prompt_writer_v6_4.runtime import _valid_provider_response


class Chunk:
    def __init__(self, finish=None):
        self.finish = finish

    def model_dump(self, **kwargs):
        return {
            "model": MODEL,
            "id": "test",
            "usage": {},
            "choices": [{"index": 0, "delta": {"content": "{}"}, "finish_reason": self.finish}],
        }


class Stream:
    def __init__(self, finish="stop", close_error=False):
        self.finish, self.close_error = finish, close_error

    def __enter__(self):
        return self

    def __iter__(self):
        yield Chunk(self.finish)

    def __exit__(self, *args):
        if self.close_error:
            raise ConnectionError("connection closed")


class Client:
    def __init__(self, stream):
        self.stream, self.requests = stream, []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

    def with_options(self, **kwargs):
        assert kwargs == {"max_retries": 0, "timeout": 1800}
        return self

    def create(self, **kwargs):
        self.requests.append(kwargs)
        return self.stream


def test_completed_stop_survives_connection_close(tmp_path: Path):
    client = Client(Stream(close_error=True))
    reply = AstraProvider(lambda: client, tmp_path)([], {})
    assert reply["finish_reason"] == "stop" and reply["transport_attempts"] == 1
    assert len(client.requests) == 1
    assert client.requests[0]["reasoning_effort"] == "high"
    assert client.requests[0]["max_completion_tokens"] == 32000
    assert client.requests[0]["response_format"]["json_schema"]["strict"] is True


def test_length_is_returned_for_the_writer_one_repair(tmp_path: Path):
    client = Client(Stream(finish="length"))
    reply = AstraProvider(lambda: client, tmp_path)([], {})
    assert reply["finish_reason"] == "length" and len(client.requests) == 1


def test_unfinished_transport_is_bounded(tmp_path: Path):
    client = Client(Stream(finish=None))
    with pytest.raises(ProviderUnavailable) as error:
        AstraProvider(lambda: client, tmp_path, sleep=lambda delay: None)([], {})
    assert error.value.attempts == 3 and len(client.requests) == 3


def test_writer_requires_the_selected_model_identity():
    response = {
        "model": MODEL,
        "content": "{}",
        "finish_reason": "stop",
        "refusal": None,
        "usage": {},
        "transport_attempts": 1,
    }
    assert _valid_provider_response(response, MODEL)
    assert not _valid_provider_response(response)
    response["model"] = "gpt-5.5"
    assert not _valid_provider_response(response, MODEL)
