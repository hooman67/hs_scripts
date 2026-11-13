#!/usr/bin/env python3
"""Extract credential-free evidence from the historical generation session log."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_events(path: Path) -> dict[int, dict[str, Any]]:
    events: dict[int, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        value = json.loads(line)
        if value.get("type") != "event_msg":
            continue
        item = (value.get("payload") or {}).get("item") or {}
        if item.get("type") == "CommandExecution":
            value["_raw_line_sha256"] = hashlib.sha256(line.encode("utf-8")).hexdigest()
            events[value["ordinal"]] = value
    return events


def command(event: dict[str, Any]) -> str:
    return " ".join(event["payload"]["item"].get("command") or [])


def output(event: dict[str, Any]) -> str:
    return event["payload"]["item"].get("aggregated_output") or ""


def parse_eval_data(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = re.fullmatch(r"const EVAL_DATA = (.*);\n?", text, re.S)
    if not match:
        raise ValueError(f"Could not parse {path}")
    return json.loads(match.group(1))


def matched_line(text: str, pattern: str) -> str:
    match = re.search(pattern, text, re.M)
    if not match:
        raise ValueError(f"Pattern not found: {pattern}")
    return match.group(0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--eval-data", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--historical-commit", required=True)
    parser.add_argument("--runner-repo-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    historical_commit = subprocess.run(
        ["git", "rev-parse", args.historical_commit],
        cwd=args.repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    runner_bytes = subprocess.run(
        ["git", "show", f"{historical_commit}:{args.runner_repo_path}"],
        cwd=args.repo,
        check=True,
        capture_output=True,
    ).stdout

    events = load_events(args.session)
    required = [1206, 1215, 1222, 1256, 2366, 2392, 2417]
    missing = [ordinal for ordinal in required if ordinal not in events]
    if missing:
        raise ValueError(f"Missing historical events: {missing}")

    eval_data = parse_eval_data(args.eval_data)
    first_row = eval_data["rows"][0]
    first_prompt = next(
        prompt for prompt in eval_data["prompts"] if prompt["key"] == first_row["prompt_key"]
    )
    first_twin = next(
        twin for twin in eval_data["twins"] if twin["evalset_item_id"] == first_row["twin_id"]
    )
    baseline_0016_rows = [
        row for row in eval_data["rows"] if row["twin_id"] == "baseline-0016"
    ]

    smoke_upload_output = output(events[1206])
    upload_body = json.loads(smoke_upload_output.splitlines()[-1])
    smoke_blob_id = upload_body["images"][0]["id"]

    smoke_submit = json.loads(output(events[1222]))
    smoke_job_id = smoke_submit["job_id"]

    final_output = output(events[1256])
    debug_marker = "debugData "
    if debug_marker not in final_output:
        raise ValueError("Historical final-output excerpt has no debugData marker")
    smoke_debug = json.loads(final_output.split(debug_marker, 1)[1])

    run_output = output(events[2366])
    relevant_run_lines = [
        line
        for line in run_output.splitlines()
        if (
            "imported successful smoke row" in line
            or "reference blobs:" in line
            or "uploaded reference baseline-0018" in line
            or "uploaded reference baseline-0016" in line
            or "summary:" in line
        )
    ]

    validation_output = output(events[2392])
    publication_output = output(events[2417])

    evidence = {
        "as_of": "2026-10-22",
        "historical_source": {
            "path": str(args.session.resolve()),
            "sha256_at_extraction": sha256(args.session),
            "bytes_at_extraction": args.session.stat().st_size,
            "event_ordinals": required,
            "selected_event_raw_line_sha256": {
                str(ordinal): events[ordinal]["_raw_line_sha256"] for ordinal in required
            },
            "limitation": (
                "The source is the durable Codex session event log from the original run. "
                "The session file remains appendable, so its whole-file hash can change; the "
                "selected raw event-line hashes identify the cited records. "
                "This extract intentionally omits the expired output presigned URL and credential-like query fields."
            ),
        },
        "code_sources": {
            "eval_data": {"path": str(args.eval_data.resolve()), "sha256": sha256(args.eval_data)},
            "historical_runner": {
                "repo": str(args.repo.resolve()),
                "commit": historical_commit,
                "repo_path": args.runner_repo_path,
                "sha256": hashlib.sha256(runner_bytes).hexdigest(),
            },
        },
        "smoke_upload": {
            "event_ordinal": 1206,
            "execution_id": events[1206]["payload"]["item"]["id"],
            "timestamp": events[1206]["timestamp"],
            "uploaded_path_from_command": (
                "/mnt/localssd/hp_lifestyle_pipeline/digital_twin_renders_first_column/"
                "00_baseline-0007.jpg"
            ),
            "returned_blob_id": smoke_blob_id,
            "response_status_excerpt": matched_line(smoke_upload_output, r"^status 200.*$"),
            "command": command(events[1206]),
        },
        "smoke_row": {
            "event_ordinals": [1215, 1222, 1256],
            "execution_ids": [
                events[ordinal]["payload"]["item"]["id"]
                for ordinal in (1215, 1222, 1256)
            ],
            "eval_first_row": first_row,
            "eval_first_prompt": first_prompt,
            "eval_first_twin": first_twin,
            "submitted_blob_id": smoke_blob_id,
            "job_id": smoke_job_id,
            "debugData": smoke_debug,
        },
        "resumable_run": {
            "event_ordinal": 2366,
            "execution_id": events[2366]["payload"]["item"]["id"],
            "timestamp": events[2366]["timestamp"],
            "relevant_log_lines": relevant_run_lines,
            "interpretive_note": (
                "The runner imported the smoke row and one blob mapping, reported one cached mapping, "
                "and uploaded only 29 remaining twins. There is an upload line for baseline-0018 and "
                "no upload line for baseline-0016."
            ),
        },
        "rows_affected_by_cached_baseline_0016_blob": {
            "count": len(baseline_0016_rows),
            "row_ids": [row["row_id"] for row in baseline_0016_rows],
            "rows": baseline_0016_rows,
            "derivation": (
                "generate_row builds every payload from blobs[row['twin_id']]['id']; after the smoke "
                "import cached the uploaded baseline-0007 blob under baseline-0016, every eval row "
                "whose twin_id is baseline-0016 reused that blob."
            ),
        },
        "historical_mechanical_validation": {
            "event_ordinal": 2392,
            "execution_id": events[2392]["payload"]["item"]["id"],
            "timestamp": events[2392]["timestamp"],
            "output": validation_output.strip(),
        },
        "historical_s3_publication_validation": {
            "event_ordinal": 2417,
            "execution_id": events[2417]["payload"]["item"]["id"],
            "timestamp": events[2417]["timestamp"],
            "output": publication_output.strip(),
        },
    }
    serialized = json.dumps(evidence, ensure_ascii=False, indent=2) + "\n"
    forbidden = ("X-Amz-Signature", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN")
    if any(token in serialized for token in forbidden):
        raise ValueError("Credential-like material was about to be preserved")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(serialized, encoding="utf-8")
    print(json.dumps({"output": str(args.output), "bytes": len(serialized)}, indent=2))


if __name__ == "__main__":
    main()
