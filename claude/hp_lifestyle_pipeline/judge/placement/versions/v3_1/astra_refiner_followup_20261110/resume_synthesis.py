"""Resume the frozen Astra synthesis with durable streaming and transient retries."""

from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
from importlib.metadata import version
import json
import os
from pathlib import Path
import re
import threading
import time

import openai

from prepare import ROOT, sha, write_json

RUN = ROOT / "synthesis_resumed_20261111"
MODEL = "gpt-6-astra"


def now():
    return datetime.now(timezone.utc).isoformat()


def retryable(error):
    if isinstance(error, (TimeoutError, ConnectionError, openai.APIConnectionError)):
        return True
    return isinstance(error, openai.APIStatusError) and (
        error.status_code in (408, 409, 429) or error.status_code >= 500
    )


class IncompleteStreamError(ConnectionError):
    pass


class Collector:
    def __init__(self):
        self.parts = []
        self.models = set()
        self.finish = None
        self.usage = None
        self.count = 0
        self.response_id = None

    def feed(self, chunk):
        self.count += 1
        if chunk.get("model"):
            self.models.add(chunk["model"])
        if chunk.get("id"):
            if self.response_id and self.response_id != chunk["id"]:
                raise ValueError("stream mixes response IDs")
            self.response_id = chunk["id"]
        if chunk.get("usage"):
            self.usage = chunk["usage"]
        for choice in chunk.get("choices", []):
            if choice["index"] != 0:
                raise ValueError("unexpected additional completion choice")
            delta = choice.get("delta", {})
            if delta.get("refusal"):
                raise ValueError("Astra refused the synthesis; no automatic semantic retry")
            if delta.get("content"):
                self.parts.append(delta["content"])
            if choice.get("finish_reason"):
                if self.finish is not None and self.finish != choice["finish_reason"]:
                    raise ValueError("conflicting completion finish reasons")
                self.finish = choice["finish_reason"]

    def result(self):
        if self.finish is None:
            raise IncompleteStreamError("stream ended without a completion finish event")
        if self.finish != "stop":
            raise ValueError("non-stop model finish; do not resample a truncated/filtered output")
        if self.models != {MODEL}:
            raise ValueError("unexpected model in actual stream")
        return json.loads("".join(self.parts))


def validate_proposals(result, expected_anchors):
    proposals = result["proposals"]
    ids = [row["id"] for row in proposals]
    anchors = [row["case_id"] for row in result["historical_anchor_reconciliation"]]
    if len(ids) != 3 or len(set(ids)) != 3:
        raise ValueError("expected three distinct proposed candidates")
    if len(anchors) != 6 or set(anchors) != expected_anchors:
        raise ValueError("synthesis omitted or rebound historical examples")
    for row in proposals:
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", row["id"]):
            raise ValueError("unsafe proposal directory name")
        names = []
        if not row["system_prompts"]:
            raise ValueError("proposal has no complete prompt artifacts")
        for prompt in row["system_prompts"]:
            name = prompt["artifact_name"]
            if name in (".", "..") or not re.fullmatch(r"[a-zA-Z0-9_.-]+", name):
                raise ValueError("unsafe prompt artifact name")
            if not isinstance(prompt["text"], str) or not prompt["text"].strip():
                raise ValueError("empty proposed prompt")
            names.append(name)
        if len(set(names)) != len(names):
            raise ValueError("duplicate proposed prompt artifact names")


@contextmanager
def heartbeat(directory, state):
    stopped = threading.Event()
    start = time.monotonic()

    def emit():
        snapshot = {
            "updated_at_utc": now(), "pid": os.getpid(),
            "elapsed_seconds": round(time.monotonic() - start, 1),
            "stream_chunks": state.count,
            "content_characters": sum(map(len, state.parts)),
            "finish_reason": state.finish,
        }
        write_json(directory / "heartbeat.json", snapshot)
        print(json.dumps({"attempt": directory.name, **snapshot}), flush=True)

    def monitor():
        while not stopped.wait(60):
            emit()

    worker = threading.Thread(target=monitor, daemon=True)
    worker.start()
    try:
        yield
    finally:
        stopped.set()
        worker.join()
        emit()


def attempt(directory, inputs, brief):
    import foundry_aws_gateway.llm

    collector = Collector()
    started = time.monotonic()
    config = {
        "started_at_utc": now(), "pid": os.getpid(),
        "model": MODEL, "reasoning_effort": "high", "max_completion_tokens": 32768,
        "timeout_seconds": 1800, "sdk_max_retries": 0, "stream": True,
        "stream_options": {"include_usage": True}, "concurrency": 1,
        "input_sha256": sha(RUN / "input.json"), "brief_sha256": sha(RUN / "brief.txt"),
        "runner_sha256": sha(Path(__file__)),
        "sdk_versions": {name: version(name) for name in ("openai", "foundry-aws-gateway")},
    }
    write_json(directory / "config.json", config)
    close_error = None
    with heartbeat(directory, collector), (directory / "chunks.jsonl").open("x") as raw:
        try:
            stream = foundry_aws_gateway.llm.get_openai().with_options(
                timeout=1800, max_retries=0,
            ).chat.completions.create(
                model=MODEL, reasoning_effort="high", max_completion_tokens=32768,
                response_format={"type": "json_object"},
                messages=[{"role": "system", "content": brief},
                          {"role": "user", "content": json.dumps(inputs, ensure_ascii=False)}],
                stream=True, stream_options={"include_usage": True},
            )
            with stream:
                for chunk in stream:
                    frame = chunk.model_dump(mode="json")
                    raw.write(json.dumps(frame, ensure_ascii=False) + "\n")
                    raw.flush()
                    collector.feed(frame)
        except Exception as error:
            if not retryable(error) or collector.finish != "stop":
                raise
            close_error = type(error).__name__
        finally:
            (directory / "partial_output.txt").write_text("".join(collector.parts))
            raw.flush()
            os.fsync(raw.fileno())
    result = collector.result()
    expected_anchors = {
        row["id"] for row in json.loads((ROOT / "evidence_manifest.json").read_text())[
            "historical_annotated_examples_and_controls"]
    }
    validate_proposals(result, expected_anchors)
    write_json(directory / "proposals.json", result)
    receipt = {
        "completed_at_utc": now(), "elapsed_seconds": round(time.monotonic() - started, 3),
        "model_returned": sorted(collector.models), "finish_reason": collector.finish,
        "response_id": collector.response_id, "usage": collector.usage,
        "stream_chunk_count": collector.count, "stream_sha256": sha(directory / "chunks.jsonl"),
        "output_sha256": sha(directory / "proposals.json"),
        "transport_close_error_after_normal_finish": close_error,
    }
    write_json(directory / "receipt.json", receipt)
    return result


def export(result, directory):
    artifacts = []
    for proposal in result["proposals"]:
        for prompt in proposal["system_prompts"]:
            path = RUN / "proposals" / proposal["id"] / prompt["artifact_name"]
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                if path.read_text() != prompt["text"]:
                    raise ValueError("existing exported prompt differs from Astra's actual output")
            else:
                with path.open("x") as stream:
                    stream.write(prompt["text"])
            artifacts.append({"proposal": proposal["id"], "role": prompt["role"],
                              "path": str(path), "sha256": sha(path)})
    write_json(RUN / "artifact_manifest.json", artifacts)
    write_json(RUN / "selected_attempt.json", {
        "status": "complete", "attempt": str(directory), "completed_at_utc": now(),
        "proposal_count": len(result["proposals"]), "prompt_artifact_count": len(artifacts),
        "receipt_sha256": sha(directory / "receipt.json"),
        "proposals_sha256": sha(directory / "proposals.json"),
        "new_judge_execution": False, "promoted": False,
    })
    print(json.dumps({"status": "complete", "attempt": directory.name,
                      "proposals": len(result["proposals"]), "prompt_artifacts": len(artifacts)}),
          flush=True)


def main():
    RUN.mkdir(exist_ok=True)
    with (RUN / "run.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        source = ROOT / "synthesis" / "input.json"
        original_config = json.loads((ROOT / "synthesis" / "config.json").read_text())
        if (sha(source) != original_config["input_sha256"]
                or sha(ROOT / "synthesis_brief.txt") != original_config["brief_sha256"]):
            raise ValueError("frozen synthesis input/brief changed")
        for name, original in (("input.json", source), ("brief.txt", ROOT / "synthesis_brief.txt")):
            path = RUN / name
            if path.exists() and sha(path) != sha(original):
                raise ValueError("resumed request input drift")
            if not path.exists():
                path.write_bytes(original.read_bytes())
        inputs = json.loads((RUN / "input.json").read_text())
        brief = (RUN / "brief.txt").read_text()
        previous = sorted(RUN.glob("attempt[0-9][0-9][0-9][0-9]"))
        for directory in previous:
            if (directory / "receipt.json").exists():
                receipt = json.loads((directory / "receipt.json").read_text())
                if receipt["output_sha256"] != sha(directory / "proposals.json"):
                    raise ValueError("previous successful output changed")
                result = json.loads((directory / "proposals.json").read_text())
                expected = {
                    row["id"] for row in json.loads((ROOT / "evidence_manifest.json").read_text())[
                        "historical_annotated_examples_and_controls"]
                }
                validate_proposals(result, expected)
                export(result, directory)
                return
        number = len(previous) + 1
        while True:
            directory = RUN / f"attempt{number:04d}"
            directory.mkdir()
            print(json.dumps({"status": "starting", "attempt": directory.name, "time": now()}), flush=True)
            try:
                result = attempt(directory, inputs, brief)
            except Exception as error:
                transient = retryable(error)
                write_json(directory / "error.json", {
                    "failed_at_utc": now(), "error_type": type(error).__name__,
                    "http_status": getattr(error, "status_code", None),
                    "retryable_transport_failure": transient,
                    "detail": str(error) if isinstance(error, (ValueError, KeyError)) else
                    "Request/transport failure; upstream completion/usage may be unknown.",
                })
                print(json.dumps({"status": "retrying" if transient else "failed",
                                  "attempt": directory.name, "error_type": type(error).__name__}),
                      flush=True)
                if not transient:
                    raise
                time.sleep(min(120, 10 * number))
                number += 1
                continue
            export(result, directory)
            return


if __name__ == "__main__":
    main()
