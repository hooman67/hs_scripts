#!/usr/bin/env python3
"""Publish validated progressive gallery snapshots until 120/120 is final."""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PUBLISHER = HERE / "publish_generation.py"
PUBLICATION = HERE / "publication.json"
STATE = HERE / "supervisor_state.json"
LOCK = HERE / "supervisor.lock"
PROJECT_ROOT = HERE.parents[2]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path: Path, default: Any = None) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def atomic_json(path: Path, value: Any) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval-seconds", type=int, default=120)
    parser.add_argument("--max-snapshots", type=int, default=720)
    args = parser.parse_args()
    if args.interval_seconds < 30:
        parser.error("interval must be at least 30 seconds")
    if args.max_snapshots < 1 or args.max_snapshots > 720:
        parser.error("max snapshots must be between 1 and 720")
    lock = LOCK.open("a+")
    try:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit("Another generation gallery publisher holds the lock")
    state = {"version": "hp-ctech-v4.1-generation-publication-supervisor-v1", "status": "running", "started_at_utc": utc_now(), "pid": os.getpid(), "interval_seconds": args.interval_seconds, "max_snapshots": args.max_snapshots, "publish_count": 0, "attempts": []}
    atomic_json(STATE, state)
    while True:
        started = utc_now()
        result = subprocess.run([sys.executable, str(PUBLISHER), "--publish"], cwd=PROJECT_ROOT, text=True, capture_output=True, check=False)
        publication = read_json(PUBLICATION, {})
        attempt = {"started_at_utc": started, "completed_at_utc": utc_now(), "exit_code": result.returncode, "publication_status": publication.get("status"), "status_counts": (publication.get("latest_snapshot") or {}).get("status_counts")}
        state["attempts"].append(attempt)
        state["last_attempt"] = attempt
        if result.returncode:
            attempt["stderr_tail"] = result.stderr[-2000:]
            state["status"] = "stopped_on_error"
            state["completed_at_utc"] = utc_now()
            atomic_json(STATE, state)
            return result.returncode
        state["publish_count"] += 1
        if publication.get("status") in {"final", "terminal_failures"}:
            state["status"] = "complete" if publication["status"] == "final" else "terminal_failures"
            state["completed_at_utc"] = utc_now()
            atomic_json(STATE, state)
            return 0
        if state["publish_count"] >= args.max_snapshots:
            state["status"] = "bounded_limit_reached"
            state["completed_at_utc"] = utc_now()
            atomic_json(STATE, state)
            return 2
        atomic_json(STATE, state)
        time.sleep(args.interval_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
