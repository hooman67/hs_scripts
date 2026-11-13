"""Recorded Astra streaming adapter; no completed answer is transport-resampled."""

from __future__ import annotations

import json
import threading
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import openai

from hp_prompt_writer_v6_4.provider import ProviderUnavailable

MODEL = "gpt-6-astra"


def write(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")


def retryable(error: Exception) -> bool:
    if isinstance(error, (ConnectionError, TimeoutError, openai.APIConnectionError)):
        return True
    if isinstance(error, openai.APIStatusError):
        return error.status_code in (408, 409, 429) or error.status_code >= 500
    if isinstance(error, openai.APIError) and isinstance(error.body, dict):
        body = error.body.get("error", error.body)
        return isinstance(body, dict) and body.get("code") in {
            "server_error",
            "internal_error",
            "internal_server_error",
            "request_timeout",
            "rate_limit_exceeded",
            "overloaded",
            "service_unavailable",
        }
    return False


class Collector:
    def __init__(self) -> None:
        self.parts: list[str] = []
        self.models: set[str] = set()
        self.response_id: str | None = None
        self.finish: str | None = None
        self.refusal: str | None = None
        self.usage: Any = None
        self.count = 0

    def feed(self, frame: dict[str, Any]) -> None:
        self.count += 1
        if frame.get("model"):
            self.models.add(frame["model"])
        if frame.get("id"):
            if self.response_id and self.response_id != frame["id"]:
                raise ValueError("Mixed completion identities")
            self.response_id = frame["id"]
        if frame.get("usage") is not None:
            self.usage = frame["usage"]
        for choice in frame.get("choices", []):
            if choice["index"] != 0:
                raise ValueError("Multiple semantic choices")
            delta = choice.get("delta", {})
            if delta.get("content"):
                self.parts.append(delta["content"])
            if delta.get("refusal"):
                self.refusal = (self.refusal or "") + delta["refusal"]
            finish = choice.get("finish_reason")
            if finish:
                if self.finish and self.finish != finish:
                    raise ValueError("Conflicting terminal completion reasons")
                self.finish = finish


class AstraProvider:
    def __init__(self, factory: Any, journal: Path, *, sleep: Any = time.sleep) -> None:
        self.factory = factory
        self.journal = journal
        self.sleep = sleep
        self.semantic_calls = 0

    def __call__(self, messages: Any, schema: Any) -> dict[str, Any]:
        self.semantic_calls += 1
        semantic = self.journal / f"semantic_{self.semantic_calls}"
        semantic.mkdir(parents=True, exist_ok=False)
        write(
            semantic / "request.json",
            {
                "messages": messages,
                "schema": schema,
                "model": MODEL,
                "reasoning_effort": "high",
                "max_completion_tokens": 32000,
                "sdk_retries": 0,
            },
        )
        try:
            client = self.factory().with_options(max_retries=0, timeout=1800)
        except Exception:
            raise ProviderUnavailable("provider_credentials_unavailable", attempts=0) from None
        events = []
        for number in range(1, 4):
            attempt = semantic / f"transport_{number}"
            attempt.mkdir()
            collector = Collector()
            stopped = threading.Event()

            def heartbeat() -> None:
                while not stopped.wait(60):
                    temporary = attempt / "heartbeat.tmp"
                    temporary.write_text(
                        json.dumps(
                            {
                                "updated_utc": datetime.now(UTC).isoformat(),
                                "chunks": collector.count,
                                "content_characters": sum(map(len, collector.parts)),
                                "finish_reason": collector.finish,
                            }
                        ),
                        encoding="utf-8",
                    )
                    temporary.replace(attempt / "heartbeat.json")

            monitor = threading.Thread(target=heartbeat, daemon=True)
            monitor.start()
            started = datetime.now(UTC).isoformat()
            close_error = None
            try:
                with (attempt / "chunks.jsonl").open("x", encoding="utf-8") as raw:
                    try:
                        with client.chat.completions.create(
                            model=MODEL,
                            reasoning_effort="high",
                            max_completion_tokens=32000,
                            messages=messages,
                            response_format={
                                "type": "json_schema",
                                "json_schema": {"name": "hp_lifestyle_v6_4", "strict": True, "schema": schema},
                            },
                            stream=True,
                            stream_options={"include_usage": True},
                        ) as stream:
                            for chunk in stream:
                                frame = chunk.model_dump(mode="json")
                                raw.write(json.dumps(frame, ensure_ascii=False) + "\n")
                                raw.flush()
                                collector.feed(frame)
                    except Exception as error:
                        if collector.finish is None or not retryable(error):
                            raise
                        close_error = type(error).__name__
                if collector.models != {MODEL}:
                    raise ValueError("Returned model is not the requested Astra")
                if collector.finish is None:
                    raise ConnectionError("Stream ended without a terminal completion")
                reply = {
                    "content": "".join(collector.parts),
                    "refusal": collector.refusal,
                    "finish_reason": collector.finish,
                    "model": MODEL,
                    "usage": collector.usage,
                    "transport_attempts": number,
                    "transport_events": events,
                    "settings": {
                        "model": MODEL,
                        "reasoning_effort": "high",
                        "max_completion_tokens": 32000,
                        "timeout": 1800,
                    },
                }
                write(attempt / "response.json", reply)
                write(
                    attempt / "receipt.json",
                    {
                        "started_utc": started,
                        "completed_utc": datetime.now(UTC).isoformat(),
                        "response_id": collector.response_id,
                        "chunks": collector.count,
                        "post_completion_close_error": close_error,
                    },
                )
                return reply
            except Exception as error:
                transient = retryable(error) and collector.finish is None and collector.refusal is None
                event = {
                    "attempt": number,
                    "error_type": type(error).__name__,
                    "status_code": getattr(error, "status_code", None),
                    "retryable": transient,
                    "started_utc": started,
                    "completed_utc": datetime.now(UTC).isoformat(),
                    "finish_reason": collector.finish,
                    "chunks": collector.count,
                    "models_seen": sorted(collector.models),
                }
                events.append(event)
                write(attempt / "error.json", event)
                if not transient or number == 3:
                    raise ProviderUnavailable("astra_provider_unavailable", attempts=number, events=events) from None
            finally:
                stopped.set()
                monitor.join()
                (attempt / "partial_output.txt").write_text("".join(collector.parts), encoding="utf-8")
            self.sleep(min(60, 10 * number))
        raise RuntimeError("Unreachable transport state")
