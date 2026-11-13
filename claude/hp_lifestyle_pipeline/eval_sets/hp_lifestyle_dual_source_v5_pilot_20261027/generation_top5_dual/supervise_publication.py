#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "httpx", "pillow"]
# ///
"""Publish changed progressive galleries, then publish the validated final gallery."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import time
from pathlib import Path

from build_gallery import DEFAULT_RUN_DIR, atomic_json, build, read_json
from publish_gallery import publish


GENERATION_DIR = Path(__file__).resolve().parent
GENERATION_STATE_PATH = GENERATION_DIR / "supervisor_state.json"
LOCK_PATH = GENERATION_DIR / "publication_supervisor.lock"
STATE_PATH = GENERATION_DIR / "publication_supervisor_state.json"
LOG_PATH = GENERATION_DIR / "publication_supervisor.log"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def append_log(message: str) -> None:
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"[{utc_now()}] {message}\n")


def acquire_lock() -> None:
    if LOCK_PATH.exists():
        previous = read_json(LOCK_PATH)
        pid = previous.get("pid")
        try:
            os.kill(int(pid), 0)
        except (ProcessLookupError, ValueError, TypeError):
            LOCK_PATH.unlink()
        else:
            raise RuntimeError(f"Publication supervisor is already running as PID {pid}")
    atomic_json(LOCK_PATH, {"pid": os.getpid(), "started_at_utc": utc_now()})


def generation_status() -> str:
    if not GENERATION_STATE_PATH.exists():
        return "unknown"
    return str(read_json(GENERATION_STATE_PATH).get("status", "unknown"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--interval-seconds", type=int, default=120)
    args = parser.parse_args()
    if args.interval_seconds < 30:
        parser.error("--interval-seconds must be at least 30")
    run_dir = args.run_dir.resolve()
    acquire_lock()
    state = {
        "version": "hp-v5-top5-dual-publication-supervisor-v1",
        "started_at_utc": utc_now(),
        "pid": os.getpid(),
        "run_dir": str(run_dir),
        "status": "running",
    }
    atomic_json(STATE_PATH, state)
    last_counts: dict[str, int] | None = None
    try:
        while True:
            gallery = build(run_dir, final=False)
            counts = gallery["status_counts"]
            state.update(
                {
                    "checked_at_utc": utc_now(),
                    "generation_status": generation_status(),
                    "gallery_status_counts": counts,
                }
            )
            if counts != last_counts:
                final = counts == {"done": 80, "pending": 0, "failed": 0}
                record = publish(run_dir, final=final)
                state.update(
                    {
                        "last_published_at_utc": record["published_at_utc"],
                        "last_publication_mode": record["mode"],
                        "public_url": record["public_url"],
                    }
                )
                append_log(f"published {record['mode']}: {counts}")
                last_counts = dict(counts)
                if final:
                    state.update({"status": "complete", "finished_at_utc": utc_now()})
                    atomic_json(STATE_PATH, state)
                    return 0
            gen_status = state["generation_status"]
            if gen_status in {"complete", "runner_failed"} and counts != {
                "done": 80,
                "pending": 0,
                "failed": 0,
            }:
                state.update({"status": "generation_incomplete", "finished_at_utc": utc_now()})
                atomic_json(STATE_PATH, state)
                append_log(f"generation stopped before final gate: {counts}")
                return 1
            atomic_json(STATE_PATH, state)
            time.sleep(args.interval_seconds)
    except Exception as exc:
        state.update(
            {
                "status": "failed",
                "finished_at_utc": utc_now(),
                "error": f"{type(exc).__name__}: {exc}",
            }
        )
        atomic_json(STATE_PATH, state)
        append_log(state["error"])
        raise
    finally:
        if LOCK_PATH.exists():
            LOCK_PATH.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
