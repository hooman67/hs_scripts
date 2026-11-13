from __future__ import annotations

from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from types import SimpleNamespace

import pytest

from research.source_messaging_v1_to_v6.versions.v6_3.provider import (
    GPT55Provider,
    ProviderUnavailable,
)


class Usage:
    def model_dump(self, *, mode):
        assert mode == "json"
        return {"input_tokens": 12, "output_tokens": 34}


def completion(*, model: str = "gpt-5.5-2026-10-01"):
    message = SimpleNamespace(content='{"ok":true}', refusal=None)
    choice = SimpleNamespace(message=message, finish_reason="stop")
    return SimpleNamespace(model=model, choices=[choice], usage=Usage())


class SDKClient:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.create_calls = []
        self.option_calls = []
        self.chat = SimpleNamespace(
            completions=SimpleNamespace(create=self.create)
        )

    def with_options(self, **kwargs):
        self.option_calls.append(kwargs)
        return self

    def create(self, **kwargs):
        self.create_calls.append(kwargs)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


class ProviderError(RuntimeError):
    def __init__(self, status_code, secret="provider-secret", headers=None):
        super().__init__(secret)
        self.status_code = status_code
        self.response = SimpleNamespace(headers=headers or {})


def call(provider):
    return provider(
        [{"role": "user", "content": "Return JSON."}],
        {"type": "object", "additionalProperties": False},
    )


def test_gpt55_strict_schema_has_no_temperature_or_sdk_retries() -> None:
    client = SDKClient([completion()])
    provider = GPT55Provider(lambda: client, timeout=123, sleep=lambda _: None)

    result = call(provider)

    assert client.option_calls == [{"max_retries": 0, "timeout": 123}]
    assert len(client.create_calls) == 1
    request = client.create_calls[0]
    assert request["model"] == "gpt-5.5"
    assert request["reasoning_effort"] == "medium"
    assert request["response_format"] == {
        "type": "json_schema",
        "json_schema": {
            "name": "hp_lifestyle_v6_3",
            "strict": True,
            "schema": {"type": "object", "additionalProperties": False},
        },
    }
    assert "temperature" not in request
    assert "top_p" not in request
    assert result["model"].startswith("gpt-5.5-")
    assert result["usage"] == {"input_tokens": 12, "output_tokens": 34}


def test_transient_429_retries_are_bounded_and_honor_retry_after() -> None:
    waits = []
    client = SDKClient(
        [
            ProviderError(429, headers={"retry-after": "7"}),
            ProviderError(429, headers={"retry-after-ms": "9000"}),
            completion(model="gpt-5.5"),
        ]
    )
    provider = GPT55Provider(
        lambda: client, max_transport_attempts=3, sleep=waits.append
    )

    result = call(provider)

    assert len(client.create_calls) == 3
    assert waits == [7.0, 9.0]
    assert result["transport_attempts"] == 3
    assert result["transport_events"] == [
        {"attempt": 1, "status_code": 429, "wait_seconds": 7.0},
        {"attempt": 2, "status_code": 429, "wait_seconds": 9.0},
    ]


def test_http_date_retry_after_uses_server_delay() -> None:
    fixed_now = datetime(2026, 10, 28, 19, 0, tzinfo=timezone.utc)
    retry_at = format_datetime(fixed_now + timedelta(seconds=10), usegmt=True)
    waits = []
    client = SDKClient(
        [ProviderError(429, headers={"Retry-After": retry_at}), completion()]
    )
    provider = GPT55Provider(
        lambda: client, sleep=waits.append, now=fixed_now.timestamp
    )

    result = call(provider)

    assert waits == [10.0]
    assert result["transport_attempts"] == 2
    assert result["transport_events"] == [
        {"attempt": 1, "status_code": 429, "wait_seconds": 10.0}
    ]


@pytest.mark.parametrize(
    "headers",
    [
        {"retry-after": "not-a-date-or-number"},
        {"retry-after": "nan"},
        {"retry-after": "-1"},
        {"retry-after-ms": "invalid"},
        {"retry-after-ms": "inf"},
        {"retry-after-ms": "-1"},
    ],
)
def test_invalid_present_retry_header_fails_closed_without_sleep(headers) -> None:
    waits = []
    client = SDKClient([ProviderError(429, headers=headers), completion()])
    provider = GPT55Provider(lambda: client, sleep=waits.append)

    with pytest.raises(ProviderUnavailable) as caught:
        call(provider)

    assert caught.value.code == "provider_retry_header_invalid"
    assert caught.value.attempts == 1
    assert caught.value.events == []
    assert len(client.create_calls) == 1
    assert waits == []


def test_transient_failures_stop_at_configured_attempt_limit() -> None:
    secret = "SECRET-error-body"
    waits = []
    client = SDKClient([ProviderError(503, secret) for _ in range(3)])
    provider = GPT55Provider(
        lambda: client, max_transport_attempts=3, sleep=waits.append
    )

    with pytest.raises(ProviderUnavailable) as caught:
        call(provider)

    assert caught.value.code == "provider_request_failed"
    assert caught.value.status_code == 503
    assert caught.value.attempts == 3
    assert len(client.create_calls) == 3
    assert waits == [2, 4]
    assert caught.value.events == [
        {"attempt": 1, "status_code": 503, "wait_seconds": 2},
        {"attempt": 2, "status_code": 503, "wait_seconds": 4},
    ]
    assert secret not in str(caught.value)


def test_retry_after_over_budget_fails_without_sleeping() -> None:
    waits = []
    client = SDKClient(
        [ProviderError(429, headers={"retry-after": "61"}), completion()]
    )
    provider = GPT55Provider(lambda: client, sleep=waits.append)

    with pytest.raises(ProviderUnavailable) as caught:
        call(provider)

    assert caught.value.code == "provider_retry_delay_exceeds_budget"
    assert caught.value.attempts == 1
    assert len(client.create_calls) == 1
    assert waits == []


def test_permanent_error_is_not_retried_and_hides_provider_body() -> None:
    secret = "SECRET-permanent-provider-body"
    client = SDKClient([ProviderError(400, secret), completion()])
    provider = GPT55Provider(lambda: client, sleep=lambda _: None)

    with pytest.raises(ProviderUnavailable) as caught:
        call(provider)

    assert caught.value.code == "provider_request_failed"
    assert caught.value.status_code == 400
    assert caught.value.attempts == 1
    assert len(client.create_calls) == 1
    assert secret not in str(caught.value)


def test_model_mismatch_is_terminal_without_substitution_or_retry() -> None:
    client = SDKClient([completion(model="gpt-5.6"), completion()])
    provider = GPT55Provider(lambda: client, sleep=lambda _: None)

    with pytest.raises(ProviderUnavailable) as caught:
        call(provider)

    assert caught.value.code == "provider_model_mismatch"
    assert caught.value.attempts == 1
    assert len(client.create_calls) == 1


def test_credentials_failure_does_not_expose_factory_exception() -> None:
    secret = "SECRET-credential-body"

    def fail_factory():
        raise RuntimeError(secret)

    provider = GPT55Provider(fail_factory, sleep=lambda _: None)
    with pytest.raises(ProviderUnavailable) as caught:
        call(provider)

    assert caught.value.code == "provider_credentials_unavailable"
    assert secret not in str(caught.value)
