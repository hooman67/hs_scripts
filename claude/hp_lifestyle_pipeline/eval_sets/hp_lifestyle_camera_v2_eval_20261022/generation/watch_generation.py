#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "pillow"]
# ///
"""Durably supervise progressive accepted prompts through the image runner."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import run_generation as runner


DEFAULT_POLL_SECONDS = 30


def atomic_json(path: Path, value: Any) -> None:
    runner.atomic_write_json(path, value)


def load_summary(run_dir: Path) -> dict[str, Any]:
    path = run_dir / "summary.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def watch_status(
    run_dir: Path,
    state: str,
    accepted: dict[str, Any],
    summary: dict[str, Any],
    last_runner_exit_code: int | None,
    started_at_utc: str,
) -> dict[str, Any]:
    manifest = json.loads(runner.MANIFEST_PATH.read_text(encoding="utf-8"))
    current_rows = runner.build_rows(manifest, accepted)
    expected_row_ids = {row["row_id"] for row in current_rows}
    records_by_id: dict[str, dict[str, Any]] = {}
    for path in (run_dir / "records").glob("*.json"):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        records_by_id[record["row_id"]] = record
    terminal_row_ids = {
        row_id
        for row_id, record in records_by_id.items()
        if record.get("status") in {"done", "failed"}
    }
    current_accepted_sha256 = runner.sha256_path(runner.ACCEPTED_PATH)
    case_count = manifest["counts"]["case_count"]
    accepted_count = int(accepted.get("accepted_case_count") or 0)
    status = {
        "schema_version": 1,
        "state": state,
        "pid": os.getpid(),
        "started_at_utc": started_at_utc,
        "updated_at_utc": runner.utc_now(),
        "manifest_sha256": runner.sha256_path(runner.MANIFEST_PATH),
        "accepted_prompt_cases_snapshot_sha256": current_accepted_sha256,
        "summary_accepted_prompt_cases_snapshot_sha256": summary.get(
            "accepted_prompt_cases_snapshot_sha256"
        ),
        "summary_matches_current_accepted_snapshot": summary.get(
            "accepted_prompt_cases_snapshot_sha256"
        )
        == current_accepted_sha256,
        "manifest_case_count": case_count,
        "accepted_case_count": accepted_count,
        "summary_accepted_case_count": summary.get("accepted_case_count"),
        "held_prompt_case_count": case_count - accepted_count,
        "manual_review_case_count": accepted.get("manual_review_case_count", 0),
        "failed_prompt_attempt_count": accepted.get("failed_case_count", 0),
        "available_generation_row_count": summary.get("available_generation_row_count", 0),
        "current_expected_generation_row_count": len(expected_row_ids),
        "current_terminal_generation_row_count": len(expected_row_ids & terminal_row_ids),
        "current_missing_terminal_row_count": len(expected_row_ids - terminal_row_ids),
        "record_count": summary.get("record_count", 0),
        "record_status_counts": summary.get("record_status_counts", {}),
        "pending_job_count": summary.get("pending_job_count", 0),
        "ambiguous_submission_count": summary.get("ambiguous_submission_count", 0),
        "safe_retry_job_count": summary.get("safe_retry_job_count", 0),
        "selected_missing_record_count": summary.get("selected_missing_record_count", 0),
        "last_runner_exit_code": last_runner_exit_code,
        "summary_path": str((run_dir / "summary.json").resolve()),
        "log_path": str((run_dir / "watch.log").resolve()),
    }
    atomic_json(run_dir / "watch_status.json", status)
    return status


def is_finished(status: dict[str, Any]) -> bool:
    if status["accepted_case_count"] != status["manifest_case_count"]:
        return False
    return (
        status["summary_matches_current_accepted_snapshot"] is True
        and status["summary_accepted_case_count"] == status["manifest_case_count"]
        and status["current_missing_terminal_row_count"] == 0
        and status["pending_job_count"] == 0
        and status["safe_retry_job_count"] == 0
        and status["selected_missing_record_count"] == 0
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=runner.DEFAULT_RUN_DIR)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--upload-workers", type=int, default=8)
    parser.add_argument("--poll-seconds", type=int, default=DEFAULT_POLL_SECONDS)
    parser.add_argument(
        "--runner-poll-window-seconds",
        type=int,
        default=runner.DEFAULT_POLL_WINDOW_SECONDS,
    )
    args = parser.parse_args()
    if not 1 <= args.workers <= runner.MAX_WORKERS:
        parser.error(f"--workers must be 1..{runner.MAX_WORKERS}")
    if not 1 <= args.upload_workers <= runner.MAX_WORKERS:
        parser.error(f"--upload-workers must be 1..{runner.MAX_WORKERS}")
    if args.poll_seconds < 5:
        parser.error("--poll-seconds must be at least 5")

    run_dir = args.run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    started_at_utc = runner.utc_now()
    (run_dir / "watch.pid").write_text(f"{os.getpid()}\n", encoding="utf-8")
    resume_command = (
        f"uv run {Path(__file__).resolve()} --run-dir {run_dir} "
        f"--workers {args.workers} --upload-workers {args.upload_workers} "
        f"--poll-seconds {args.poll_seconds} "
        f"--runner-poll-window-seconds {args.runner_poll_window_seconds}"
    )
    (run_dir / "resume_command.txt").write_text(resume_command + "\n", encoding="utf-8")
    last_processed_snapshot = ""
    last_runner_exit_code: int | None = None

    while True:
        accepted = json.loads(runner.ACCEPTED_PATH.read_text(encoding="utf-8"))
        accepted_snapshot = runner.sha256_path(runner.ACCEPTED_PATH)
        summary = load_summary(run_dir)
        status = watch_status(
            run_dir,
            "checking",
            accepted,
            summary,
            last_runner_exit_code,
            started_at_utc,
        )
        if is_finished(status):
            watch_status(
                run_dir,
                "complete_with_failures" if status["record_status_counts"].get("failed") else "complete",
                accepted,
                summary,
                last_runner_exit_code,
                started_at_utc,
            )
            return

        should_run = accepted.get("accepted_case_count", 0) > 0 and (
            accepted_snapshot != last_processed_snapshot
            or status["pending_job_count"] > 0
            or status["safe_retry_job_count"] > 0
            or status["selected_missing_record_count"] > 0
        )
        if should_run:
            watch_status(
                run_dir,
                "running_image_batch",
                accepted,
                summary,
                last_runner_exit_code,
                started_at_utc,
            )
            command = [
                sys.executable,
                str((Path(__file__).parent / "run_generation.py").resolve()),
                "--run-dir",
                str(run_dir),
                "--all-accepted",
                "--workers",
                str(args.workers),
                "--upload-workers",
                str(args.upload_workers),
                "--poll-window-seconds",
                str(args.runner_poll_window_seconds),
            ]
            print(
                f"[{dt.datetime.now().strftime('%H:%M:%S')}] launch accepted snapshot "
                f"{accepted_snapshot} cases={accepted.get('accepted_case_count', 0)}",
                flush=True,
            )
            completed = subprocess.run(command, check=False)
            last_runner_exit_code = completed.returncode
            last_processed_snapshot = accepted_snapshot
            continue

        watch_status(
            run_dir,
            "waiting_for_accepted_prompts",
            accepted,
            summary,
            last_runner_exit_code,
            started_at_utc,
        )
        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    main()
