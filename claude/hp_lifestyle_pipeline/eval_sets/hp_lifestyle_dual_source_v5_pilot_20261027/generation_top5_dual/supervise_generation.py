#!/usr/bin/env python3
"""Run/resume the authorized V5 inventory and refresh its progressive gallery."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from build_gallery import DEFAULT_RUN_DIR, atomic_json, build


GENERATION_DIR = Path(__file__).resolve().parent
RUNNER = GENERATION_DIR / "run_generation.py"
LOCK_PATH = GENERATION_DIR / "supervisor.lock"
STATE_PATH = GENERATION_DIR / "supervisor_state.json"
LOG_PATH = GENERATION_DIR / "supervisor.log"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def append_log(message: str) -> None:
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"[{utc_now()}] {message}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--gallery-refresh-seconds", type=int, default=30)
    parser.add_argument("--selection", choices=("smart_brief", "ctech"))
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 8:
        parser.error("--workers must be between 1 and 8")
    if args.gallery_refresh_seconds < 5:
        parser.error("--gallery-refresh-seconds must be at least 5")
    if LOCK_PATH.exists():
        previous = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        pid = previous.get("pid")
        try:
            os.kill(int(pid), 0)
        except (ProcessLookupError, ValueError, TypeError):
            LOCK_PATH.unlink()
        else:
            raise RuntimeError(f"Generation supervisor is already running as PID {pid}")
    atomic_json(LOCK_PATH, {"pid": os.getpid(), "started_at_utc": utc_now()})
    command = [
        "uv",
        "run",
        "--script",
        str(RUNNER),
        "--run-dir",
        str(args.run_dir.resolve()),
        "--workers",
        str(args.workers),
    ]
    command.extend(["--selection", args.selection] if args.selection else ["--all"])
    append_log(f"starting: {' '.join(command)}")
    process = subprocess.Popen(
        command,
        cwd=str(GENERATION_DIR),
        stdout=LOG_PATH.open("a", encoding="utf-8"),
        stderr=subprocess.STDOUT,
        text=True,
    )
    state = {
        "version": "hp-v5-top5-dual-generation-supervisor-v1",
        "started_at_utc": utc_now(),
        "supervisor_pid": os.getpid(),
        "runner_pid": process.pid,
        "command": command,
        "run_dir": str(args.run_dir.resolve()),
        "status": "running",
    }
    atomic_json(STATE_PATH, state)
    try:
        while process.poll() is None:
            time.sleep(args.gallery_refresh_seconds)
            try:
                gallery = build(args.run_dir.resolve(), final=False)
                state["last_gallery_refresh_at_utc"] = utc_now()
                state["gallery_status_counts"] = gallery["status_counts"]
                atomic_json(STATE_PATH, state)
            except Exception as exc:  # noqa: BLE001 - runner must continue
                append_log(f"gallery refresh failed: {type(exc).__name__}: {exc}")
        exit_code = process.wait()
        gallery = build(args.run_dir.resolve(), final=False)
        state.update(
            {
                "finished_at_utc": utc_now(),
                "runner_exit_code": exit_code,
                "gallery_status_counts": gallery["status_counts"],
                "status": "complete" if exit_code == 0 else "runner_failed",
            }
        )
        atomic_json(STATE_PATH, state)
        append_log(f"runner exited {exit_code}; gallery={gallery['status_counts']}")
        return exit_code
    finally:
        if LOCK_PATH.exists():
            LOCK_PATH.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
