#!/usr/bin/env python3
"""Run/resume all 16 V5 banks and build the final top-six exports."""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
LOCK = HERE / "supervisor.lock"
LOG = HERE / "supervisor.log"
STATE = HERE / "supervisor_state.json"


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write_state(value: dict) -> None:
    tmp = STATE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    tmp.replace(STATE)


def main() -> int:
    if LOCK.exists():
        prior = json.loads(LOCK.read_text(encoding="utf-8"))
        try:
            os.kill(int(prior["pid"]), 0)
        except (ProcessLookupError, ValueError, KeyError):
            LOCK.unlink()
        else:
            raise RuntimeError(f"supervisor already running as PID {prior['pid']}")
    LOCK.write_text(json.dumps({"pid": os.getpid(), "started_at_utc": now()}) + "\n")
    command = [
        "uv", "run", "--script", str(HERE / "run_gpt55.py"),
        "--all-authorized", "--max-concurrency", "2", "--max-transport-attempts", "100",
    ]
    state = {
        "version": "hp-lifestyle-v5-top6-supervisor-v1",
        "status": "running",
        "started_at_utc": now(),
        "pid": os.getpid(),
        "command": command,
    }
    write_state(state)
    try:
        with LOG.open("a", encoding="utf-8") as handle:
            process = subprocess.Popen(command, cwd=HERE, stdout=handle, stderr=subprocess.STDOUT)
            state["runner_pid"] = process.pid
            write_state(state)
            while process.poll() is None:
                time.sleep(10)
            code = process.wait()
            state["runner_exit_code"] = code
            if code not in (0, 2):
                state.update({"status": "runner_failed", "finished_at_utc": now()})
                write_state(state)
                return code
            review = subprocess.run(
                ["python", str(HERE / "build_reviewed.py")],
                cwd=HERE,
                stdout=handle,
                stderr=subprocess.STDOUT,
                check=False,
            )
            state["review_exit_code"] = review.returncode
            if review.returncode != 0:
                state.update({"status": "review_failed", "finished_at_utc": now()})
                write_state(state)
                return review.returncode
            build = subprocess.run(
                ["python", str(HERE / "build_top6.py")],
                cwd=HERE,
                stdout=handle,
                stderr=subprocess.STDOUT,
                check=False,
            )
            state["build_exit_code"] = build.returncode
            state.update(
                {
                    "status": "complete" if build.returncode == 0 else "build_failed",
                    "finished_at_utc": now(),
                }
            )
            write_state(state)
            return build.returncode
    finally:
        if LOCK.exists():
            LOCK.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
