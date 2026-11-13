"""GPT-5.5 adapter with bounded transport retries and no model substitution."""
from __future__ import annotations

import importlib.util
import math
import time
from datetime import timezone
from email.utils import parsedate_to_datetime
from pathlib import Path


class ProviderUnavailable(RuntimeError):
    def __init__(self, code, *, status_code=None, attempts=0, events=None):
        super().__init__(code)  # Never include credentials or provider error bodies.
        self.code = code
        self.status_code = status_code
        self.attempts = attempts
        self.events = [dict(event) for event in (events or [])]


def _retry_delay(headers, *, fallback, now):
    """Resolve a safe Retry-After delay or reject a malformed present header."""

    if headers is None:
        return fallback

    def header(name):
        value = headers.get(name)
        if value is not None:
            return value
        items = getattr(headers, "items", None)
        if items is not None:
            for key, candidate in items():
                if isinstance(key, str) and key.casefold() == name:
                    return candidate
        return None

    retry_after = header("retry-after")
    retry_after_ms = header("retry-after-ms")
    if retry_after is not None:
        try:
            delay = float(retry_after)
        except (TypeError, ValueError):
            try:
                retry_at = parsedate_to_datetime(str(retry_after))
                if retry_at is None:
                    raise ValueError
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)
                delay = max(0.0, retry_at.timestamp() - now())
            except (TypeError, ValueError, OverflowError, OSError):
                raise ValueError("invalid retry-after header") from None
    elif retry_after_ms is not None:
        try:
            delay = float(retry_after_ms) / 1000
        except (TypeError, ValueError, OverflowError):
            raise ValueError("invalid retry-after-ms header") from None
    else:
        return fallback
    if not math.isfinite(delay) or delay < 0:
        raise ValueError("invalid retry delay")
    return max(fallback, delay)


def foundry_client():
    """Reuse the authorized helper/auth route; create clients only on invocation."""
    probe_path = Path(__file__).resolve().parents[2] / "scripts" / "probe_gpt55.py"
    spec = importlib.util.spec_from_file_location("hp_v6_foundry_auth", probe_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    client, _auth_mode = module.client_and_auth_mode()
    return client


class GPT55Provider:
    """Callable accepted by run_writer; client_factory also permits SDK injection."""

    def __init__(self, client_factory=foundry_client, *, max_transport_attempts=3,
                 max_completion_tokens=16000, timeout=180, sleep=time.sleep,
                 now=time.time):
        if not 1 <= max_transport_attempts <= 10:
            raise ValueError("transport attempts must be between 1 and 10")
        if max_completion_tokens < 1000 or timeout <= 0:
            raise ValueError("invalid provider token/timeout settings")
        self.factory = client_factory
        self.client = None
        self.max_transport_attempts = max_transport_attempts
        self.max_completion_tokens = max_completion_tokens
        self.timeout = timeout
        self.sleep = sleep
        self.now = now

    def __call__(self, messages, schema):
        events = []
        if self.client is None:
            try:
                self.client = self.factory().with_options(max_retries=0, timeout=self.timeout)
            except Exception as exc:
                raise ProviderUnavailable("provider_credentials_unavailable") from None
        for attempt in range(1, self.max_transport_attempts + 1):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-5.5", reasoning_effort="medium",
                    max_completion_tokens=self.max_completion_tokens,
                    messages=messages,
                    response_format={"type": "json_schema", "json_schema": {
                        "name": "hp_lifestyle_v6_1", "strict": True, "schema": schema}},
                )
            except Exception as exc:
                code = getattr(exc, "status_code", None)
                transient = code == 429 or (isinstance(code, int) and 500 <= code <= 599)
                transient = transient or type(exc).__name__ in {"APITimeoutError", "APIConnectionError"}
                if not transient or attempt == self.max_transport_attempts:
                    raise ProviderUnavailable(
                        "provider_request_failed", status_code=code,
                        attempts=attempt, events=events
                    ) from None
                fallback = min(2 ** attempt, 30)
                headers = getattr(getattr(exc, "response", None), "headers", {})
                try:
                    delay = _retry_delay(
                        headers, fallback=fallback, now=self.now
                    )
                except (ValueError, TypeError, AttributeError):
                    raise ProviderUnavailable(
                        "provider_retry_header_invalid", status_code=code,
                        attempts=attempt, events=events
                    ) from None
                if delay > 60:
                    raise ProviderUnavailable(
                        "provider_retry_delay_exceeds_budget", status_code=code,
                        attempts=attempt, events=events
                    ) from None
                events.append({"attempt": attempt, "status_code": code, "wait_seconds": delay})
                self.sleep(delay)
                continue
            model = getattr(response, "model", None)
            if not isinstance(model, str) or not (model == "gpt-5.5" or model.startswith("gpt-5.5-")):
                raise ProviderUnavailable(
                    "provider_model_mismatch", attempts=attempt, events=events
                )
            if not response.choices:
                raise ProviderUnavailable(
                    "provider_empty_choices", attempts=attempt, events=events
                )
            choice = response.choices[0]
            usage = getattr(response, "usage", None)
            return {"content": choice.message.content,
                    "refusal": getattr(choice.message, "refusal", None),
                    "finish_reason": choice.finish_reason, "model": model,
                    "usage": usage.model_dump(mode="json") if usage is not None else {},
                    "transport_attempts": attempt, "transport_events": events,
                    "settings": {"model": "gpt-5.5", "reasoning_effort": "medium",
                                 "max_completion_tokens": self.max_completion_tokens, "timeout": self.timeout}}
        raise ProviderUnavailable("provider_request_failed", events=events)
