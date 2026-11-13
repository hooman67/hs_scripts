#!/usr/bin/env python3
"""Freeze, checkpoint, stop, and drain the live V2 runner without resubmission.

The default ``inspect`` command is read-only. ``checkpoint-stop`` requires an
explicit process-group ID and confirmation token. It freezes the whole V2
group, refuses to terminate across a ``submitting`` window, hashes every
durable artifact, and records the exact no-resubmission drain argv before it
stops the processes. Endpoint jobs are never cancelled. ``drain`` resumes only
journaled jobs that can be polled or materialized without a new submission.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
V2_EVAL_ROOT = PROJECT_ROOT / "eval_sets/hp_lifestyle_camera_v2_eval_20261022"
V2_RUN_ROOT = PROJECT_ROOT / "local_data/generation_runs/hp_lifestyle_camera_v2_eval_20261022"
V2_RUNNER = V2_EVAL_ROOT / "generation/run_generation.py"
V2_WATCH = V2_EVAL_ROOT / "generation/watch_generation.py"
V2_MANIFEST = V2_EVAL_ROOT / "manifest.json"
V2_ACCEPTED = V2_EVAL_ROOT / "accepted_prompt_cases.json"
V2_FINAL_SUMMARY = V2_EVAL_ROOT / "validation/final_prompt_summary.json"
CHECKPOINT_ROOT = (
    PROJECT_ROOT
    / "local_data/generation_runs/hp_lifestyle_diversity_v3_eval_20261023/v2_stop_checkpoints"
)
STOP_CONFIRMATION = "V3_READY_STOP_V2"
SENSITIVE_MARKERS = (
    b"x-amz-signature=",
    b"x-amz-credential=",
    b"x-amz-security-token=",
    b'"authorization"',
    b'"presignedurl"',
)
NO_RESUBMIT_DRAIN_STATUSES = frozenset(
    {
        "submitted",
        "completed_response_ready",
        "endpoint_failed",
        "submission_ambiguous",
        "failed_terminal",
        "fatal_config_error",
    }
)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def file_fact(path: Path, root: Path | None = None) -> dict[str, Any]:
    return {
        "path": str(path.resolve()),
        "relative_path": str(path.relative_to(root)) if root else None,
        "bytes": path.stat().st_size,
        "sha256": sha256_path(path),
    }


def json_artifact_facts(directory: Path, run_root: Path) -> list[dict[str, Any]]:
    facts = []
    for path in sorted(directory.glob("*.json")):
        fact = file_fact(path, run_root)
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            fact.update(
                {
                    "valid_json": True,
                    "row_id": value.get("row_id"),
                    "status": value.get("status"),
                    "job_id": value.get("job_id"),
                    "has_result_url": bool(value.get("result_url")),
                    "failure_class": value.get("failure_class"),
                }
            )
        except (OSError, ValueError) as exc:
            fact.update({"valid_json": False, "parse_error": f"{type(exc).__name__}: {exc}"})
        facts.append(fact)
    return facts


def status_counts(facts: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for fact in facts:
        status = fact.get("status") or "<missing>"
        counts[status] = counts.get(status, 0) + 1
    return dict(sorted(counts.items()))


def sensitive_scan(paths: list[Path]) -> dict[str, Any]:
    findings = []
    for path in paths:
        raw = path.read_bytes().lower()
        matched = [marker.decode("ascii") for marker in SENSITIVE_MARKERS if marker in raw]
        if matched:
            findings.append({"path": str(path.resolve()), "markers": matched})
    return {
        "scanned_file_count": len(paths),
        "finding_count": len(findings),
        "findings": findings,
        "passed": not findings,
    }


def rows_requiring_no_resubmit_drain(
    jobs: list[dict[str, Any]], records: list[dict[str, Any]]
) -> list[str]:
    terminal_records = {
        fact["row_id"]
        for fact in records
        if fact.get("row_id") and fact.get("status") in {"done", "failed"}
    }
    rows = set()
    for fact in jobs:
        row_id = fact.get("row_id")
        status = fact.get("status")
        if not row_id or status not in NO_RESUBMIT_DRAIN_STATUSES:
            continue
        if status == "submitted" or row_id not in terminal_records:
            rows.add(row_id)
    return sorted(rows)


def checkpoint_consistency_issues(
    jobs: list[dict[str, Any]], records: list[dict[str, Any]]
) -> list[str]:
    issues = []
    for label, facts in (("job", jobs), ("record", records)):
        if any(not fact.get("valid_json") for fact in facts):
            issues.append(f"invalid {label} JSON exists")
        row_ids = [fact.get("row_id") for fact in facts]
        if any(not row_id for row_id in row_ids):
            issues.append(f"{label} artifact without row_id exists")
        if len({row_id for row_id in row_ids if row_id}) != len([row_id for row_id in row_ids if row_id]):
            issues.append(f"duplicate {label} row_id exists")
    jobs_by_id = {fact.get("row_id"): fact for fact in jobs if fact.get("row_id")}
    records_by_id = {fact.get("row_id"): fact for fact in records if fact.get("row_id")}
    for row_id, record in records_by_id.items():
        if record.get("status") == "pending" and row_id not in jobs_by_id:
            issues.append(f"pending record lacks job journal: {row_id}")
    for row_id, job in jobs_by_id.items():
        if job.get("status") == "materialized" and records_by_id.get(row_id, {}).get("status") != "done":
            issues.append(f"materialized job lacks done record: {row_id}")
        if job.get("status") in {"submitted", "completed_response_ready"}:
            if not job.get("job_id") or not job.get("has_result_url"):
                issues.append(f"pollable job lacks durable job identity: {row_id}")
    return sorted(set(issues))


def drain_argv(checkpoint: dict[str, Any], workers: int = 8) -> list[str]:
    row_ids = checkpoint.get("drain_row_ids") or rows_requiring_no_resubmit_drain(
        checkpoint["jobs"], checkpoint["records"]
    )
    argv = [
        "uv",
        "run",
        str(V2_RUNNER.resolve()),
        "--run-dir",
        checkpoint["run_root"],
        "--workers",
        str(workers),
        "--upload-workers",
        str(workers),
        "--poll-window-seconds",
        "1800",
    ]
    for row_id in row_ids:
        argv.extend(["--row-id", row_id])
    return argv


def build_checkpoint(run_root: Path, process_group_id: int | None) -> dict[str, Any]:
    jobs = json_artifact_facts(run_root / "jobs", run_root)
    records = json_artifact_facts(run_root / "records", run_root)
    images = [file_fact(path, run_root) for path in sorted((run_root / "images").glob("*")) if path.is_file()]
    raw_responses = [
        file_fact(path, run_root)
        for path in sorted((run_root / "raw_responses").glob("*.json"))
        if path.is_file()
    ]
    fixed = [V2_MANIFEST, V2_ACCEPTED, V2_FINAL_SUMMARY, V2_RUNNER, V2_WATCH]
    blob_bindings = run_root / "blob_bindings.json"
    if blob_bindings.exists():
        fixed.append(blob_bindings)
    scan_paths = [Path(fact["path"]) for fact in jobs + records + raw_responses]
    final_prompt = json.loads(V2_FINAL_SUMMARY.read_text(encoding="utf-8"))
    final_expected_rows = (
        final_prompt.get("final_status", {}).get("launchable_generation_row_count")
        or final_prompt.get("facts", {}).get("available_generation_row_count")
    )
    if final_expected_rows != 1318:
        raise ValueError(
            f"Unexpected V2 final generation row count: {final_expected_rows}"
        )
    checkpoint = {
        "checkpoint_version": 1,
        "created_at_utc": utc_now(),
        "reason": "V3 ready; preserve exact live V2 state and drain only known jobs without resubmission",
        "run_root": str(run_root.resolve()),
        "process_group_id": process_group_id,
        "fixed_artifacts": [file_fact(path) for path in fixed],
        "final_expected_generation_row_count": final_expected_rows,
        "jobs": jobs,
        "job_status_counts": status_counts(jobs),
        "records": records,
        "record_status_counts": status_counts(records),
        "images": images,
        "raw_responses": raw_responses,
        "submitting_row_ids": sorted(fact["row_id"] for fact in jobs if fact.get("status") == "submitting"),
        "submitted_jobs": [
            {
                "row_id": fact["row_id"],
                "job_id": fact.get("job_id"),
                "has_result_url": fact.get("has_result_url"),
                "job_path": fact["path"],
                "job_sha256": fact["sha256"],
            }
            for fact in jobs
            if fact.get("status") == "submitted"
        ],
        "ambiguous_row_ids": sorted(fact["row_id"] for fact in jobs if fact.get("status") == "submission_ambiguous"),
        "safe_retry_row_ids": sorted(fact["row_id"] for fact in jobs if fact.get("status") == "failed_retryable_no_job_created"),
        "sensitive_artifact_scan": sensitive_scan(scan_paths),
        "consistency_issues": checkpoint_consistency_issues(jobs, records),
        "stop_completed": False,
    }
    checkpoint["drain_row_ids"] = rows_requiring_no_resubmit_drain(jobs, records)
    checkpoint["exact_drain_command_argv"] = drain_argv(checkpoint)
    return checkpoint


def verify_checkpoint_files(checkpoint: dict[str, Any]) -> dict[str, Any]:
    checked = 0
    mismatches = []
    for collection in ("fixed_artifacts", "jobs", "records", "images", "raw_responses"):
        for fact in checkpoint[collection]:
            path = Path(fact["path"])
            checked += 1
            if not path.is_file():
                mismatches.append({"path": str(path), "reason": "missing"})
                continue
            actual = {"bytes": path.stat().st_size, "sha256": sha256_path(path)}
            if actual["bytes"] != fact["bytes"] or actual["sha256"] != fact["sha256"]:
                mismatches.append({"path": str(path), "reason": "changed", "actual": actual})
    return {"checked_file_count": checked, "mismatch_count": len(mismatches), "mismatches": mismatches, "passed": not mismatches}


def group_alive(process_group_id: int) -> bool:
    return any(
        not member["stat"].startswith("Z")
        for member in group_commands(process_group_id)
    )


def group_commands(process_group_id: int) -> list[dict[str, Any]]:
    completed = subprocess.run(
        ["ps", "-eo", "pid=,ppid=,pgid=,stat=,args="],
        check=True,
        capture_output=True,
        text=True,
    )
    members = []
    for line in completed.stdout.splitlines():
        parts = line.strip().split(None, 4)
        if len(parts) == 5 and int(parts[2]) == process_group_id:
            members.append(
                {"pid": int(parts[0]), "ppid": int(parts[1]), "pgid": int(parts[2]), "stat": parts[3], "argv": parts[4]}
            )
    return members


def verify_v2_process_group(process_group_id: int) -> list[dict[str, Any]]:
    if process_group_id <= 1 or process_group_id == os.getpgrp():
        raise RuntimeError("Refusing an unsafe or self process-group target")
    members = group_commands(process_group_id)
    if not members:
        raise RuntimeError(f"No live members in process group {process_group_id}")
    joined = "\n".join(member["argv"] for member in members)
    if "hp_lifestyle_camera_v2_eval_20261022/generation/watch_generation.py" not in joined:
        raise RuntimeError("Process group does not contain the expected V2 supervisor")
    if "hp_lifestyle_camera_v2_eval_20261022/generation/run_generation.py" not in joined:
        raise RuntimeError("Process group does not contain the expected V2 runner child")
    allowed_fragments = (
        "hp_lifestyle_camera_v2_eval_20261022/generation/watch_generation.py",
        "hp_lifestyle_camera_v2_eval_20261022/generation/run_generation.py",
    )
    unexpected = [
        member
        for member in members
        if not any(fragment in member["argv"] for fragment in allowed_fragments)
    ]
    if unexpected:
        raise RuntimeError(
            f"Process group contains unexpected members; refusing broad kill: {unexpected}"
        )
    return members


def checkpoint_path(checkpoint_root: Path) -> Path:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    return checkpoint_root / f"v2_stop_checkpoint_{timestamp}.json"


def freeze_checkpoint_stop(
    run_root: Path,
    checkpoint_root: Path,
    process_group_id: int,
    confirmation: str,
) -> Path:
    if confirmation != STOP_CONFIRMATION:
        raise ValueError(f"checkpoint-stop requires --confirm {STOP_CONFIRMATION}")
    members = verify_v2_process_group(process_group_id)
    os.killpg(process_group_id, signal.SIGSTOP)
    time.sleep(0.5)
    path = checkpoint_path(checkpoint_root)
    try:
        checkpoint = build_checkpoint(run_root, process_group_id)
        checkpoint["process_members_before_stop"] = members
        checkpoint["process_members_frozen"] = group_commands(process_group_id)
        if not checkpoint["process_members_frozen"] or any(
            not member["stat"].startswith("T")
            for member in checkpoint["process_members_frozen"]
        ):
            checkpoint["stop_aborted_reason"] = "not every V2 process-group member reached stopped state"
            atomic_json(path, checkpoint)
            os.killpg(process_group_id, signal.SIGCONT)
            raise RuntimeError(checkpoint["stop_aborted_reason"])
        checkpoint["checkpoint_verification"] = verify_checkpoint_files(checkpoint)
        if checkpoint["submitting_row_ids"]:
            checkpoint["stop_aborted_reason"] = "submitting window detected; group resumed without termination"
            atomic_json(path, checkpoint)
            os.killpg(process_group_id, signal.SIGCONT)
            raise RuntimeError(
                "V2 has submitting jobs; resumed it without stopping. Retry after journals settle."
            )
        if checkpoint["consistency_issues"]:
            checkpoint["stop_aborted_reason"] = "checkpoint consistency checks failed"
            atomic_json(path, checkpoint)
            os.killpg(process_group_id, signal.SIGCONT)
            raise RuntimeError(
                f"V2 checkpoint has consistency issues; resumed without stopping: "
                f"{checkpoint['consistency_issues']}"
            )
        if not checkpoint["sensitive_artifact_scan"]["passed"]:
            checkpoint["stop_aborted_reason"] = "sensitive URL or credential marker found"
            atomic_json(path, checkpoint)
            os.killpg(process_group_id, signal.SIGCONT)
            raise RuntimeError(
                "Sensitive URL or credential marker found; resumed V2 without stopping"
            )
        if not checkpoint["checkpoint_verification"]["passed"]:
            checkpoint["stop_aborted_reason"] = "checkpoint files changed while frozen"
            atomic_json(path, checkpoint)
            os.killpg(process_group_id, signal.SIGCONT)
            raise RuntimeError("Checkpoint verification failed; V2 resumed without stopping")
        atomic_json(path, checkpoint)
        os.killpg(process_group_id, signal.SIGTERM)
        os.killpg(process_group_id, signal.SIGCONT)
        deadline = time.monotonic() + 15
        while group_alive(process_group_id) and time.monotonic() < deadline:
            time.sleep(0.25)
        if group_alive(process_group_id):
            checkpoint["stop_error"] = "process group remained alive after SIGTERM; no SIGKILL sent"
            atomic_json(path, checkpoint)
            raise RuntimeError(checkpoint["stop_error"])
        checkpoint["stop_completed"] = True
        checkpoint["stopped_at_utc"] = utc_now()
        atomic_json(path, checkpoint)
        return path
    except BaseException:
        if group_alive(process_group_id):
            try:
                os.killpg(process_group_id, signal.SIGCONT)
            except ProcessLookupError:
                pass
        raise


def execute_drain(checkpoint_path_value: Path, workers: int, execute: bool) -> int:
    checkpoint = json.loads(checkpoint_path_value.read_text(encoding="utf-8"))
    if checkpoint.get("stop_completed") is not True:
        raise ValueError("Drain requires a checkpoint with stop_completed=true")
    if checkpoint.get("consistency_issues"):
        raise ValueError("Drain checkpoint contains consistency issues")
    if checkpoint.get("sensitive_artifact_scan", {}).get("passed") is not True:
        raise ValueError("Drain checkpoint did not pass the sensitive-artifact scan")
    verification = verify_checkpoint_files(checkpoint)
    if not verification["passed"]:
        raise ValueError(f"Drain checkpoint files changed before resume: {verification}")
    expected_drain_rows = rows_requiring_no_resubmit_drain(
        checkpoint["jobs"], checkpoint["records"]
    )
    if checkpoint.get("drain_row_ids") != expected_drain_rows:
        raise ValueError("Drain row set differs from immutable checkpoint journals")
    argv = drain_argv(checkpoint, workers)
    if argv != checkpoint.get("exact_drain_command_argv") and workers == 8:
        raise ValueError("Checkpoint drain argv differs from reconstructed submitted-row set")
    if not checkpoint.get("drain_row_ids"):
        print(json.dumps({"status": "nothing_to_drain", "argv": argv}, indent=2))
        return 0
    if not execute:
        print(json.dumps({"status": "dry_run", "argv": argv}, indent=2))
        return 0
    completed = subprocess.run(argv, check=False)
    post = build_checkpoint(Path(checkpoint["run_root"]), None)
    post["checkpoint_verification"] = verify_checkpoint_files(post)
    post["drained_from_checkpoint"] = str(checkpoint_path_value.resolve())
    post["drain_process_exit_code"] = completed.returncode
    records_by_id = {
        fact.get("row_id"): fact for fact in post["records"] if fact.get("row_id")
    }
    post["drain_terminal_record_count"] = sum(
        records_by_id.get(row_id, {}).get("status") in {"done", "failed"}
        for row_id in checkpoint["drain_row_ids"]
    )
    post["drain_expected_row_count"] = len(checkpoint["drain_row_ids"])
    post["drain_complete"] = (
        post["drain_terminal_record_count"] == post["drain_expected_row_count"]
        and not post["submitting_row_ids"]
        and not post["drain_row_ids"]
        and post["sensitive_artifact_scan"]["passed"]
        and post["checkpoint_verification"]["passed"]
    )
    post_path = checkpoint_path_value.with_name(
        checkpoint_path_value.stem + ".post_drain.json"
    )
    atomic_json(post_path, post)
    if completed.returncode or not post["drain_complete"]:
        return 2
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, default=V2_RUN_ROOT)
    parser.add_argument("--checkpoint-root", type=Path, default=CHECKPOINT_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)
    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("--process-group-id", type=int)
    stop_parser = subparsers.add_parser("checkpoint-stop")
    stop_parser.add_argument("--process-group-id", type=int, required=True)
    stop_parser.add_argument("--confirm", required=True)
    drain_parser = subparsers.add_parser("drain")
    drain_parser.add_argument("--checkpoint", type=Path, required=True)
    drain_parser.add_argument("--workers", type=int, default=8, choices=range(1, 9))
    drain_parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    run_root = args.run_root.resolve()
    if args.command == "inspect":
        checkpoint = build_checkpoint(run_root, args.process_group_id)
        checkpoint["checkpoint_verification"] = verify_checkpoint_files(checkpoint)
        if args.process_group_id:
            checkpoint["process_members"] = verify_v2_process_group(args.process_group_id)
        print(json.dumps(checkpoint, indent=2, sort_keys=True))
        return
    if args.command == "checkpoint-stop":
        path = freeze_checkpoint_stop(
            run_root,
            args.checkpoint_root.resolve(),
            args.process_group_id,
            args.confirm,
        )
        print(path)
        return
    raise SystemExit(execute_drain(args.checkpoint.resolve(), args.workers, args.execute))


if __name__ == "__main__":
    main()
