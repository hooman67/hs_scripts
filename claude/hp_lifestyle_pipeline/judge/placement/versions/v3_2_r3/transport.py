"""Streaming recovery for new consultations and prospective successor runtimes."""

import json
import re
import threading
import time
from datetime import UTC, datetime
from pathlib import Path

import common


def api_error_fields(error):
    import openai

    if not isinstance(error, openai.APIError) or not isinstance(error.body, dict):
        return {}
    body = error.body.get("error", error.body)
    if not isinstance(body, dict):
        return {}
    return {
        key: value
        for key in ("type", "code")
        if isinstance(value := body.get(key), str)
        and re.fullmatch(r"[a-z0-9_]{1,80}", value)
    }


def retryable(error):
    if common.retryable(error):
        return True
    fields = api_error_fields(error)
    return fields.get("code") in {
        "server_error",
        "internal_error",
        "internal_server_error",
        "request_timeout",
        "timeout",
        "rate_limit_exceeded",
        "overloaded",
        "service_unavailable",
    } or (not fields.get("code") and fields.get("type") == "server_error")


def model_completion(messages, schema, cap, output, client=None):
    output = Path(output)
    if client is None:
        import foundry_aws_gateway.llm

        client = foundry_aws_gateway.llm.get_openai().with_options(
            max_retries=0, timeout=1800
        )
    number = 0
    while True:
        number += 1
        attempt = output / f"attempt{number:02d}"
        attempt.mkdir(parents=True, exist_ok=False)
        started = datetime.now(UTC).isoformat()
        common.write_json(
            attempt / "config.json",
            {
                "model": common.MODEL,
                "reasoning_effort": "high",
                "max_completion_tokens": cap,
                "sdk_retries": 0,
                "timeout_seconds": 1800,
                "messages_sha256": common.fingerprint(messages),
                "transport_source_sha256": common.sha(__file__),
            },
        )
        collector = common.Collector()
        stopped = threading.Event()
        close_error = None

        def beat(
            stopped=stopped, attempt=attempt, started=started, collector=collector
        ):
            while not stopped.wait(60):
                common.write_json(
                    attempt / "heartbeat.json",
                    {
                        "updated_utc": datetime.now(UTC).isoformat(),
                        "started_utc": started,
                        "chunks": collector.count,
                        "content_characters": sum(map(len, collector.parts)),
                        "model": common.MODEL,
                        "finish_reason": collector.finish,
                    },
                )

        monitor = threading.Thread(target=beat, daemon=True)
        monitor.start()
        try:
            response_format = (
                {"type": "json_object"}
                if schema is None
                else {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "placement_observation",
                        "strict": True,
                        "schema": common.LEGACY.wire_schema(schema),
                    },
                }
            )
            with (attempt / "chunks.jsonl").open("x") as raw:
                try:
                    with client.chat.completions.create(
                        model=common.MODEL,
                        reasoning_effort="high",
                        max_completion_tokens=cap,
                        response_format=response_format,
                        messages=messages,
                        stream=True,
                        stream_options={"include_usage": True},
                    ) as stream:
                        for chunk in stream:
                            frame = chunk.model_dump(mode="json")
                            raw.write(json.dumps(frame, ensure_ascii=False) + "\n")
                            raw.flush()
                            collector.feed(frame)
                except Exception as error:
                    if not retryable(error) or collector.finish != "stop":
                        raise
                    close_error = type(error).__name__
            value = collector.result()
            common.write_json(attempt / "parsed.json", value)
            receipt = {
                "model_returned": common.MODEL,
                "finish_reason": collector.finish,
                "response_id": collector.response_id,
                "usage": collector.usage,
                "started_utc": started,
                "finished_utc": datetime.now(UTC).isoformat(),
                "chunks_path": str((attempt / "chunks.jsonl").resolve()),
                "chunks_sha256": common.sha(attempt / "chunks.jsonl"),
                "transport_attempts": number,
                "post_completion_close_error": close_error,
            }
            common.write_json(attempt / "receipt.json", receipt)
            return value, receipt
        except Exception as error:
            transient = retryable(error) and collector.finish is None
            common.write_json(
                attempt / "error.json",
                {
                    "started_utc": started,
                    "finished_utc": datetime.now(UTC).isoformat(),
                    "error_type": type(error).__name__,
                    "status_code": getattr(error, "status_code", None),
                    "api_error_fields": api_error_fields(error),
                    "retryable_transport_failure": transient,
                    "chunks": collector.count,
                    "models_seen": sorted(collector.models),
                    "finish_reason": collector.finish,
                    "detail": str(error)
                    if isinstance(error, ValueError)
                    else "API/transport error; structured type/code preserved.",
                },
            )
            if not transient:
                raise
        finally:
            stopped.set()
            monitor.join()
            (attempt / "partial_output.txt").write_text("".join(collector.parts))
        time.sleep(min(60, 10 * number))
