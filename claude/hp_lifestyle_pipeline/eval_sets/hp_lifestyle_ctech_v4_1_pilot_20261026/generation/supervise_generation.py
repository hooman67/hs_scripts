#!/usr/bin/env python3
"""Bounded supervisor for the journaled V4.1 120-row image runner.

The first invocation is allowed without a summary. Every later invocation is
authorized only by durable summary state showing missing records, known
submitted jobs, safely retryable submissions, or pending records. The runner
itself resolves row identity against its job journal before any submission.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any


EXPECTED_ROWS = 120
DEFAULT_MAX_INVOCATIONS = 12
DEFAULT_RUN_DIR = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/"
    "local_data/generation_runs/hp_lifestyle_ctech_v4_1_pilot_20261026_corrected_twins_20261027"
)
RUNNER = Path(__file__).resolve().with_name("run_generation.py")
PROJECT_ROOT = Path(__file__).resolve().parents[3]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path: Path, default: Any = None) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def summary_counts(summary: dict[str, Any]) -> dict[str, int]:
    statuses = summary.get("record_status_counts") or {}
    return {
        "done": int(statuses.get("done", 0)),
        "failed": int(statuses.get("failed", 0)),
        "pending_records": int(statuses.get("pending", 0)),
        "records": int(summary.get("record_count", 0)),
        "missing": int(summary.get("selected_missing_record_count", 0)),
        "pending_jobs": int(summary.get("pending_job_count", 0)),
        "safe_retry": int(summary.get("safe_retry_job_count", 0)),
        "ambiguous": int(summary.get("ambiguous_submission_count", 0)),
    }


def classify_summary(summary: dict[str, Any]) -> dict[str, Any]:
    expected = int(summary.get("expected_generation_row_count", 0))
    selected = int(summary.get("selected_generation_row_count", 0))
    if expected != EXPECTED_ROWS or selected != EXPECTED_ROWS:
        return {
            "action": "stop_review",
            "reason": "summary_row_scope_is_not_exactly_120",
            "counts": summary_counts(summary),
        }
    counts = summary_counts(summary)
    if any(value < 0 for value in counts.values()):
        return {"action": "stop_review", "reason": "summary_contains_negative_counts", "counts": counts}
    actionable = counts["missing"] + counts["pending_jobs"] + counts["safe_retry"] + counts["pending_records"]
    if actionable:
        return {
            "action": "resume",
            "reason": "durable_summary_has_safe_or_known_work",
            "counts": counts,
        }
    if counts["ambiguous"]:
        return {
            "action": "stop_ambiguous",
            "reason": "only_ambiguous_or_terminal_rows_remain",
            "counts": counts,
        }
    if counts["records"] == EXPECTED_ROWS and counts["done"] + counts["failed"] == EXPECTED_ROWS:
        return {
            "action": "stop_complete" if counts["done"] == EXPECTED_ROWS else "stop_terminal",
            "reason": "all_120_rows_done" if counts["done"] == EXPECTED_ROWS else "all_120_rows_accounted_with_terminal_failures",
            "counts": counts,
        }
    return {
        "action": "stop_review",
        "reason": "summary_has_no_safe_action_but_rows_are_not_terminally_accounted",
        "counts": counts,
    }


def runner_command(run_dir: Path, poll_window_seconds: int) -> list[str]:
    return [
        "uv", "run", "--script", str(RUNNER),
        "--run-dir", str(run_dir),
        "--all", "--workers", "8", "--upload-workers", "2",
        "--poll-window-seconds", str(poll_window_seconds),
    ]


def terminal_status(decision: dict[str, Any]) -> tuple[str, int]:
    return {
        "stop_complete": ("complete", 0),
        "stop_terminal": ("terminal_failures", 2),
        "stop_ambiguous": ("ambiguous_review_required", 2),
        "stop_review": ("review_required", 2),
    }[decision["action"]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--poll-window-seconds", type=int, default=1800)
    parser.add_argument("--max-invocations", type=int, default=DEFAULT_MAX_INVOCATIONS)
    parser.add_argument("--classify-summary", type=Path, help="Classify one summary without running anything")
    args = parser.parse_args()
    if args.classify_summary:
        decision = classify_summary(read_json(args.classify_summary))
        print(json.dumps(decision, indent=2))
        return 0 if decision["action"].startswith("stop_") else 3
    if args.poll_window_seconds < 60:
        parser.error("--poll-window-seconds must be at least 60")
    if args.max_invocations < 1 or args.max_invocations > 48:
        parser.error("--max-invocations must be between 1 and 48")

    run_dir = args.run_dir.resolve()
    launch_dir = run_dir / "launch"
    state_path = launch_dir / "generation_supervisor_state.json"
    lock_path = launch_dir / "generation_supervisor.lock"
    summary_path = run_dir / "summary.json"
    launch_dir.mkdir(parents=True, exist_ok=True)
    lock = lock_path.open("a+")
    try:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("Another V4.1 generation supervisor already holds the lock", flush=True)
        return 2

    previous = read_json(state_path, {})
    state: dict[str, Any] = {
        "version": "hp-ctech-v4.1-generation-supervisor-v1",
        "supervisor_run_id": str(uuid.uuid4()),
        "status": "running",
        "pid": os.getpid(),
        "started_at_utc": utc_now(),
        "run_dir": str(run_dir),
        "runner": str(RUNNER),
        "workers": 8,
        "upload_workers": 2,
        "poll_window_seconds": args.poll_window_seconds,
        "max_invocations": args.max_invocations,
        "invocation_count": 0,
        "lifetime_invocation_count": int(previous.get("lifetime_invocation_count", 0)),
        "invocations": [],
    }
    atomic_json(state_path, state)

    summary = read_json(summary_path)
    decision = classify_summary(summary) if summary else {"action": "resume", "reason": "initial_launch_has_no_summary", "counts": {}}
    state["decision"] = decision
    atomic_json(state_path, state)

    while decision["action"] == "resume" and state["invocation_count"] < args.max_invocations:
        before_mtime = summary_path.stat().st_mtime_ns if summary_path.exists() else None
        invocation = {
            "number": state["invocation_count"] + 1,
            "started_at_utc": utc_now(),
            "authorization": decision,
            "command_settings": {
                "all_frozen_rows": True,
                "workers": 8,
                "upload_workers": 2,
                "poll_window_seconds": args.poll_window_seconds,
            },
        }
        state["invocations"].append(invocation)
        state["invocation_count"] += 1
        state["lifetime_invocation_count"] += 1
        atomic_json(state_path, state)
        print(f"[{utc_now()}] V4.1 runner invocation {invocation['number']} authorized: {decision['reason']}", flush=True)
        process = subprocess.Popen(
            runner_command(run_dir, args.poll_window_seconds),
            cwd=PROJECT_ROOT,
            env=os.environ.copy(),
        )
        state["active_runner_pid"] = process.pid
        atomic_json(state_path, state)
        return_code = process.wait()
        state.pop("active_runner_pid", None)
        invocation["completed_at_utc"] = utc_now()
        invocation["exit_code"] = return_code
        after_mtime = summary_path.stat().st_mtime_ns if summary_path.exists() else None
        invocation["summary_updated"] = after_mtime is not None and after_mtime != before_mtime
        if not invocation["summary_updated"]:
            decision = {
                "action": "stop_review",
                "reason": "runner_exited_without_a_fresh_durable_summary",
                "counts": {},
            }
        else:
            summary = read_json(summary_path)
            decision = classify_summary(summary)
            invocation["result"] = decision
        state["decision"] = decision
        state["latest_summary"] = summary
        atomic_json(state_path, state)
        if decision["action"] == "resume" and state["invocation_count"] < args.max_invocations:
            time.sleep(5)

    if decision["action"] == "resume":
        state["status"] = "bounded_limit_reached"
        state["decision"] = {
            **decision,
            "reason": "maximum_supervised_runner_invocations_reached_with_safe_or_known_work_remaining",
        }
        exit_code = 2
    else:
        state["status"], exit_code = terminal_status(decision)
    state["completed_at_utc"] = utc_now()
    atomic_json(state_path, state)
    print(f"[{utc_now()}] V4.1 generation supervisor stopped status={state['status']} decision={state['decision']['reason']}", flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
