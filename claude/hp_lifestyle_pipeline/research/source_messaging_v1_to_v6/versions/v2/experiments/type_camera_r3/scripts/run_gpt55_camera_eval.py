# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml", "tomli", "jsonschema"]
# ///
"""Run the bounded camera-aware V2 text eval on GPT-5.5, sequentially and resumably."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import jsonschema


V2_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE_ROOT / "scripts"))

from probe_gpt55 import client_and_auth_mode  # noqa: E402
from run_gpt55 import checkpoint, digest, retry_delay, transient  # noqa: E402


SETTINGS = {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000,
}


def read_case(manifest_path: Path, case: dict) -> tuple[Path, str, dict]:
    path = manifest_path.parent / case["input_path"]
    raw = path.read_text(encoding="utf-8")
    value = json.loads(raw)
    raw_sha256 = digest(raw)
    semantic_sha256 = digest(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
    )
    if raw_sha256 != case["input_raw_sha256"]:
        raise RuntimeError(f"Raw input changed after manifest creation: {case['case_id']}")
    if semantic_sha256 != case["input_semantic_sha256"]:
        raise RuntimeError(
            f"Semantic input changed after manifest creation: {case['case_id']}"
        )
    return path, raw, value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--system", type=Path, default=V2_ROOT / "system_prompt.md"
    )
    parser.add_argument(
        "--manifest", type=Path, default=V2_ROOT / "eval/current/manifest.json"
    )
    parser.add_argument(
        "--input-schema", type=Path, default=V2_ROOT / "input.schema.json"
    )
    parser.add_argument(
        "--output-schema", type=Path, default=V2_ROOT / "output.schema.json"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=V2_ROOT / "eval/current/runs/gpt55_type_camera",
    )
    parser.add_argument("--max-attempts", type=int, default=100)
    parser.add_argument(
        "--case", action="append", help="Optional case ID; repeat for multiple cases"
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Validate all local inputs and hashes without loading credentials or calling GPT",
    )
    args = parser.parse_args()
    if not 1 <= args.max_attempts <= 1000:
        parser.error("--max-attempts must be between 1 and 1000")
    if not args.system.is_file():
        raise RuntimeError(f"Compiled system prompt is not ready: {args.system}")

    system = args.system.read_text(encoding="utf-8")
    if not system.strip() or "{{OFFLINE_NOTES}}" in system:
        raise RuntimeError("System prompt is empty or still contains an uncompiled placeholder")
    manifest_raw = args.manifest.read_text(encoding="utf-8")
    manifest = json.loads(manifest_raw)
    manifest_cases = manifest.get("cases", [])
    if (
        not isinstance(manifest.get("case_count"), int)
        or manifest["case_count"] <= 0
        or manifest["case_count"] != len(manifest_cases)
    ):
        raise RuntimeError(
            "Bounded camera eval manifest must contain a positive, consistent case count"
        )
    input_schema_raw = args.input_schema.read_text(encoding="utf-8")
    input_schema = json.loads(input_schema_raw)
    output_schema_raw = args.output_schema.read_text(encoding="utf-8")
    output_schema = json.loads(output_schema_raw)
    jsonschema.Draft202012Validator.check_schema(input_schema)
    jsonschema.Draft202012Validator.check_schema(output_schema)
    if digest(input_schema_raw) != manifest["input_schema_sha256"]:
        raise RuntimeError("Input schema changed after eval manifest creation")
    camera_profiles_path = Path(manifest["camera_profiles_path"])
    camera_profiles_raw = camera_profiles_path.read_text(encoding="utf-8")
    if digest(camera_profiles_raw) != manifest["camera_profiles_sha256"]:
        raise RuntimeError("Camera registry changed after eval manifest creation; rebuild cases")

    selected = []
    known_case_ids = {case["case_id"] for case in manifest["cases"]}
    if args.case:
        unknown = sorted(set(args.case) - known_case_ids)
        if unknown:
            raise RuntimeError(f"Unknown requested case IDs: {unknown}")
    for case in manifest["cases"]:
        if args.case and case["case_id"] not in args.case:
            continue
        path, raw, value = read_case(args.manifest, case)
        jsonschema.validate(value, input_schema)
        source_semantic_sha256 = digest(
            json.dumps(
                value["source_messaging"],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        if source_semantic_sha256 != case["source_semantic_sha256"]:
            raise RuntimeError(f"Unwrapped source changed: {case['case_id']}")
        selected.append((case, path, raw, value))

    system_sha256 = digest(system)
    input_schema_sha256 = digest(input_schema_raw)
    output_schema_sha256 = digest(output_schema_raw)
    if args.preflight_only:
        print(
            json.dumps(
                {
                    "preflight": "ok",
                    "selected_cases": len(selected),
                    "system_prompt_sha256": system_sha256,
                    "input_schema_sha256": input_schema_sha256,
                    "output_schema_sha256": output_schema_sha256,
                    "camera_profiles_sha256": manifest["camera_profiles_sha256"],
                    "api_called": False,
                },
                indent=2,
            )
        )
        return

    args.output_dir.mkdir(parents=True, exist_ok=True)
    run_started_at = datetime.now(timezone.utc).isoformat()
    run_started = time.monotonic()
    run_summary_path = args.output_dir / "run_summary.json"
    run_summary = {
        "started_at": run_started_at,
        "status": "running",
        "selected_case_ids": [case[0]["case_id"] for case in selected],
        "settings": SETTINGS,
        "system_prompt_sha256": system_sha256,
        "input_schema_sha256": input_schema_sha256,
        "output_schema_sha256": output_schema_sha256,
        "camera_profiles_sha256": manifest["camera_profiles_sha256"],
        "completed_case_ids": [],
        "skipped_case_ids": [],
    }
    checkpoint(run_summary_path, run_summary)
    client, auth_mode = client_and_auth_mode()
    run_summary["auth_mode"] = auth_mode
    checkpoint(run_summary_path, run_summary)
    common_key = {
        "system_prompt_sha256": system_sha256,
        "input_schema_sha256": input_schema_sha256,
        "output_schema_sha256": output_schema_sha256,
        "settings": SETTINGS,
    }
    for case, input_path, raw, value in selected:
        request_key = digest(
            json.dumps(
                {**common_key, "input_semantic_sha256": case["input_semantic_sha256"]},
                sort_keys=True,
            )
        )
        target = args.output_dir / f"{case['case_id']}.json"
        previous = None
        if target.exists():
            old = json.loads(target.read_text(encoding="utf-8"))
            if (
                old.get("request_key") != request_key
                or old.get("input_semantic_sha256")
                != case["input_semantic_sha256"]
            ):
                raise RuntimeError(
                    f"Output directory contains a different run for {case['case_id']}"
                )
            if old.get("response"):
                if not old.get("schema_valid"):
                    raise RuntimeError(
                        f"Recorded response needs review before repeating {case['case_id']}"
                    )
                print(f"Already recorded: {case['case_id']}", flush=True)
                run_summary["skipped_case_ids"].append(case["case_id"])
                run_summary["elapsed_seconds"] = round(
                    time.monotonic() - run_started, 3
                )
                checkpoint(run_summary_path, run_summary)
                continue
            previous = old

        record = {
            "case_id": case["case_id"],
            "case": case,
            "request_key": request_key,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "input_path": str(input_path),
            "input_raw_sha256": case["input_raw_sha256"],
            "input_semantic_sha256": case["input_semantic_sha256"],
            "source_semantic_sha256": case["source_semantic_sha256"],
            "raw_request_json": raw,
            "request_input": value,
            "raw_input_json": json.dumps(
                value["source_messaging"], ensure_ascii=False, indent=2
            ),
            "system_prompt": system,
            "system_prompt_sha256": system_sha256,
            "input_schema": input_schema,
            "input_schema_sha256": input_schema_sha256,
            "schema": output_schema,
            "output_schema_sha256": output_schema_sha256,
            "manifest_sha256": digest(manifest_raw),
            "camera_profiles_sha256": manifest["camera_profiles_sha256"],
            "settings": SETTINGS,
            "auth_mode": auth_mode,
            "retry_events": [],
        }
        if previous:
            record["prior_attempts"] = previous

        for attempt in range(1, args.max_attempts + 1):
            request_started = time.monotonic()
            try:
                response = client.chat.completions.create(
                    **SETTINGS,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": raw},
                    ],
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "hp_camera_environment_prompts",
                            "strict": True,
                            "schema": output_schema,
                        },
                    },
                )
                record["attempt"] = attempt
                record["latency_seconds"] = round(
                    time.monotonic() - request_started, 3
                )
                record["response"] = response.model_dump(mode="json")
                record["usage"] = record["response"].get("usage")
                record["completed_at"] = datetime.now(timezone.utc).isoformat()
                checkpoint(target, record)
                if (
                    not response.model.startswith("gpt-5.5")
                    or response.choices[0].finish_reason != "stop"
                ):
                    raise RuntimeError(
                        "Unexpected model or incomplete response; preserved raw result"
                    )
                content = response.choices[0].message.content or ""
                result = json.loads(content)
                jsonschema.validate(result, output_schema)
                record["parsed_output"] = result
                record["schema_valid"] = True
                checkpoint(target, record)
                print(
                    "Recorded:",
                    case["case_id"],
                    "model:",
                    response.model,
                    "prompts:",
                    len(result["prompts"]),
                    "latency_seconds:",
                    record["latency_seconds"],
                    flush=True,
                )
                break
            except Exception as exc:
                if record.get("response") or not transient(exc) or attempt == args.max_attempts:
                    record["failure"] = {
                        "type": type(exc).__name__,
                        "status_code": getattr(exc, "status_code", None),
                        "attempt": attempt,
                    }
                    checkpoint(target, record)
                    run_summary["status"] = "failed"
                    run_summary["failed_case_id"] = case["case_id"]
                    run_summary["failure_type"] = type(exc).__name__
                    run_summary["elapsed_seconds"] = round(
                        time.monotonic() - run_started, 3
                    )
                    checkpoint(run_summary_path, run_summary)
                    raise RuntimeError(
                        f"Case {case['case_id']} stopped: {type(exc).__name__}; "
                        "response/checkpoint preserved"
                    ) from None
                delay = retry_delay(exc, attempt)
                record["retry_events"].append(
                    {
                        "attempt": attempt,
                        "status_code": getattr(exc, "status_code", None),
                        "type": type(exc).__name__,
                        "wait_seconds": delay,
                    }
                )
                pending = target.with_suffix(".pending.json")
                checkpoint(pending, record)
                print(
                    "Retry:",
                    case["case_id"],
                    f"{attempt}/{args.max_attempts}",
                    "wait seconds:",
                    round(delay, 1),
                    flush=True,
                )
                while delay > 0:
                    step = min(30, delay)
                    time.sleep(step)
                    delay -= step
                    if delay > 0:
                        print(
                            "Waiting for provider:",
                            case["case_id"],
                            round(delay, 1),
                            "seconds remaining",
                            flush=True,
                        )
        pending = target.with_suffix(".pending.json")
        if pending.exists():
            pending.unlink()
        run_summary["completed_case_ids"].append(case["case_id"])
        run_summary["elapsed_seconds"] = round(time.monotonic() - run_started, 3)
        checkpoint(run_summary_path, run_summary)
    run_summary["status"] = "complete"
    run_summary["completed_at"] = datetime.now(timezone.utc).isoformat()
    run_summary["elapsed_seconds"] = round(time.monotonic() - run_started, 3)
    checkpoint(run_summary_path, run_summary)


if __name__ == "__main__":
    main()
