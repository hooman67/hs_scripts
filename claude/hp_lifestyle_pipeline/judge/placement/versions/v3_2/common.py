"""Shared immutable evidence I/O for Astra-designed placement candidates."""

import base64
import hashlib
import importlib.util
import json
import mimetypes
import threading
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R1 = ROOT.parent / "v3_1"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LEGACY = load("placement_v32_legacy", R1 / "run_judge.py")
SCORING = LEGACY.SCORING
OBSERVATION_SCHEMA = SCORING.OBSERVATION_SCHEMA
MODEL = "gpt-6-astra"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    )
    temporary.replace(path)


def verify_freeze():
    path = ROOT / "protocol_freeze.json"
    for item in json.loads(path.read_text())["files"]:
        if sha(item["path"]) != item["sha256"]:
            raise ValueError(f"Frozen dependency changed: {item['path']}")
    return sha(path)


def retryable(error):
    import openai

    return isinstance(
        error, (ConnectionError, TimeoutError, openai.APIConnectionError)
    ) or (
        isinstance(error, openai.APIStatusError)
        and (error.status_code in (408, 409, 429) or error.status_code >= 500)
    )


class Collector:
    def __init__(self):
        self.parts, self.models = [], set()
        self.finish, self.usage, self.response_id = None, None, None
        self.count = 0

    def feed(self, frame):
        self.count += 1
        if frame.get("model"):
            self.models.add(frame["model"])
        if frame.get("id"):
            if self.response_id and frame["id"] != self.response_id:
                raise ValueError("Mixed streaming response identities")
            self.response_id = frame["id"]
        if frame.get("usage"):
            self.usage = frame["usage"]
        for choice in frame.get("choices", []):
            if choice["index"] != 0:
                raise ValueError("Multiple semantic choices are not permitted")
            delta = choice.get("delta", {})
            if delta.get("refusal"):
                raise ValueError("Astra refusal; semantic retry forbidden")
            if delta.get("content"):
                self.parts.append(delta["content"])
            if choice.get("finish_reason"):
                if self.finish and self.finish != choice["finish_reason"]:
                    raise ValueError("Conflicting streaming finish")
                self.finish = choice["finish_reason"]

    def result(self):
        if self.finish is None:
            raise ConnectionError("Stream ended without a terminal completion")
        if self.finish != "stop" or self.models != {MODEL}:
            raise ValueError(
                "Wrong model or non-stop semantic completion; no resampling"
            )
        return json.loads("".join(self.parts))


def model_completion(messages, schema, cap, output, client=None):
    """Persist every attempt; retry transport only, never sampled judgments."""
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
        collector = Collector()
        stopped = threading.Event()

        def beat(
            stopped=stopped, attempt=attempt, started=started, collector=collector
        ):
            while not stopped.wait(60):
                write_json(
                    attempt / "heartbeat.json",
                    {
                        "updated_utc": datetime.now(UTC).isoformat(),
                        "started_utc": started,
                        "chunks": collector.count,
                        "content_characters": sum(map(len, collector.parts)),
                        "model": MODEL,
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
                        "schema": LEGACY.wire_schema(schema),
                    },
                }
            )
            with (
                (attempt / "chunks.jsonl").open("x") as raw,
                client.chat.completions.create(
                    model=MODEL,
                    reasoning_effort="high",
                    max_completion_tokens=cap,
                    response_format=response_format,
                    messages=messages,
                    stream=True,
                    stream_options={"include_usage": True},
                ) as stream,
            ):
                for chunk in stream:
                    frame = chunk.model_dump(mode="json")
                    raw.write(json.dumps(frame, ensure_ascii=False) + "\n")
                    raw.flush()
                    collector.feed(frame)
            value = collector.result()
            write_json(attempt / "parsed.json", value)
            receipt = {
                "model_returned": MODEL,
                "finish_reason": collector.finish,
                "response_id": collector.response_id,
                "usage": collector.usage,
                "started_utc": started,
                "finished_utc": datetime.now(UTC).isoformat(),
                "chunks_path": str((attempt / "chunks.jsonl").resolve()),
                "chunks_sha256": sha(attempt / "chunks.jsonl"),
                "transport_attempts": number,
            }
            write_json(attempt / "receipt.json", receipt)
            return value, receipt
        except Exception as error:
            transient = retryable(error)
            write_json(
                attempt / "error.json",
                {
                    "started_utc": started,
                    "finished_utc": datetime.now(UTC).isoformat(),
                    "error_type": type(error).__name__,
                    "status_code": getattr(error, "status_code", None),
                    "retryable_transport_failure": transient,
                    "detail": str(error)
                    if isinstance(error, ValueError)
                    else "API/transport error; see status.",
                },
            )
            if not transient:
                raise
        finally:
            stopped.set()
            monitor.join()
            (attempt / "partial_output.txt").write_text("".join(collector.parts))
        time.sleep(min(60, 10 * number))


def call_stage(
    runtime_input,
    stage,
    output,
    schema,
    validator,
    *,
    reports=None,
    cap=12000,
    client=None,
):
    LEGACY.SCORING.validate_runtime_input(runtime_input)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    prompt_path = ROOT / "prompts" / (stage + ".txt")
    prompt = prompt_path.read_text()
    request = {
        "runtime_input": runtime_input,
        "stage": stage,
        "model": MODEL,
        "reasoning_effort": "high",
        "max_completion_tokens": cap,
        "route": "foundry_aws_gateway.llm.get_openai",
        "sdk_retries": 0,
        "max_transport_attempts": None,
        "timeout_seconds": 1800,
        "protocol_freeze_sha256": verify_freeze(),
        "prompt_sha256": sha(prompt_path),
        "schema_sha256": fingerprint(schema),
        "reports": reports,
        "images": {
            key: sha(runtime_input[key]) for key in ("generated_image", "twin_image")
        },
        "target_labels_withheld": True,
        "image_transform": "none; exact original bytes",
    }
    key = fingerprint(request)
    result_path = output / "result.json"
    if result_path.exists():
        old = json.loads(result_path.read_text())
        if old.get("fingerprint") != key or not old.get("ok"):
            raise ValueError(
                "Existing stage is failed or belongs to another frozen request"
            )
        if sha(old["chunks_path"]) != old["chunks_sha256"]:
            raise ValueError("Cached raw stream changed")
        collector = Collector()
        for line in Path(old["chunks_path"]).read_text().splitlines():
            collector.feed(json.loads(line))
        value = collector.result()
        validator(value)
        if value != old["observation"]:
            raise ValueError("Cached evidence differs from raw model response")
        return old
    write_json(output / "request.json", {**request, "fingerprint": key})
    write_json(output / "schema.json", schema)
    (output / "system_prompt.txt").write_text(prompt)
    messages = [{"role": "system", "content": prompt}]
    if stage == "p1_baseline":
        anchors, excluded = LEGACY.select_anchors(runtime_input)
        parts = [
            {
                "type": "text",
                "text": "Fixed development rubric exemplars. Current chair-tolerance rules override historical chair-pose interpretations. Judge the target independently.",
            }
        ]
        for anchor in anchors:
            parts += LEGACY.image_parts(anchor["guidance"], anchor["local_path"])
        messages.extend(
            [
                {"role": "user", "content": parts},
                {
                    "role": "assistant",
                    "content": "I will independently assess the target.",
                },
            ]
        )
        write_json(
            output / "exemplars.json", {"selected": anchors, "excluded": excluded}
        )
    payload = {
        key: runtime_input[key]
        for key in ("product_type", "scene_prompt", "image_stage")
    }
    if reports is not None:
        payload["fallible_model_reports"] = reports
        if stage in ("p1_proposal", "p1_independent"):
            payload["requested_components"] = reports["requested_components"]
    parts = [{"type": "text", "text": json.dumps(payload)}]
    for label, key in (
        ("A: scene to assess", "generated_image"),
        ("B: product reference", "twin_image"),
    ):
        path = Path(runtime_input[key])
        mime = mimetypes.guess_type(path.name)[0]
        if mime not in ("image/png", "image/jpeg", "image/webp"):
            raise ValueError("Unsupported image format")
        body = path.read_bytes()
        if hashlib.sha256(body).hexdigest() != request["images"][key]:
            raise ValueError("Scene/reference bytes changed while preparing request")
        parts += [
            {"type": "text", "text": label},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime};base64," + base64.b64encode(body).decode(),
                    "detail": "high",
                },
            },
        ]
    messages.append({"role": "user", "content": parts})
    value, receipt = model_completion(messages, schema, cap, output, client=client)
    validator(value)
    result = {
        "ok": True,
        "fingerprint": fingerprint(request),
        "observation": value,
        **receipt,
    }
    write_json(result_path, result)
    return result
