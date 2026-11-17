#!/usr/bin/env python3
"""Recover one local Codex session and release its temporary sleep assertion.

Unlike the tmux watcher, this uses persisted Codex events and thread-scoped
logs. It never infers completion from silence or interrupts built-in retries.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import signal
import sqlite3
import subprocess
import time


CONTINUE = (
    "Continue your existing requested work from the latest checkpoint after "
    "the connection or rate-limit interruption. Preserve the conversation, "
    "model, scope, and all user constraints. Verify completed work before "
    "repeating actions. Leave unanswered user questions pending."
)


def recovery_reason(text: str) -> str | None:
    text = text.casefold()
    if any(marker in text for marker in ("rate limit", "rate_limit", "too many requests")):
        return "rate_limit"
    if any(marker in text for marker in (
        "stream disconnected", "connection reset", "connection closed",
        "connection refused", "network is unreachable", "stream interrupted",
        "stream was interrupted", "error sending request", "request timed out",
        "stream ended before", "failed to connect",
    )):
        return "disconnected"
    return None


def retry_delay(text: str, failures: int) -> float:
    delay = min(900.0, 60.0 * 2 ** min(failures, 4))
    # Honor provider delays longer than our own exponential backoff.
    for match in re.finditer(
        r"(?:retry[-_ ]after\s*[:=]?|try again in|retry in)\s*"
        r"([\d.]+)\s*(milliseconds?|ms|minutes?|m|seconds?|s)?",
        text, re.IGNORECASE,
    ):
        amount = float(match[1])
        unit = (match[2] or "seconds").lower()
        amount *= 0.001 if unit.startswith("ms") or unit.startswith("millisecond") else 60 if unit.startswith("m") else 1
        delay = max(delay, amount + 5)
    for match in re.finditer(
        r"(?:try again at|resets? at|reset at)\s*"
        r"(\d{4}-\d{2}-\d{2}[T ][\d:]+(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)",
        text, re.IGNORECASE,
    ):
        try:
            reset = dt.datetime.fromisoformat(match[1].replace("Z", "+00:00"))
            if reset.tzinfo is not None:
                delay = max(delay, reset.timestamp() - time.time() + 5)
        except ValueError:
            pass
    return delay


@dataclasses.dataclass
class Progress:
    status: str = "watching"
    turn_id: str | None = None
    failures: int = 0
    retry_at: float | None = None
    reason: str | None = None

    def fail(self, text: str, now: float) -> bool:
        reason = recovery_reason(text)
        if not reason:
            return False
        # Do not extend the deadline for every duplicate rendering of an error.
        if self.retry_at is None:
            self.retry_at = now + retry_delay(text, self.failures)
        self.status, self.reason = "retry_pending", reason
        return True

    def event(self, payload: dict, now: float) -> None:
        kind = payload.get("type")
        turn = payload.get("turn_id", payload.get("root_turn_id"))
        if kind == "task_started":
            self.status, self.turn_id = "running", turn
            self.retry_at, self.reason = None, None
        elif kind == "turn_aborted" and (not turn or turn == self.turn_id):
            # A deliberate interruption is not permission to resume it.
            self.status, self.retry_at = "interrupted", None
        elif kind == "error" and not payload.get("will_retry", False):
            self.fail(str(payload.get("message", payload.get("error", ""))), now)
        elif kind == "task_complete" and (not turn or turn == self.turn_id):
            if payload.get("error"):
                self.fail(str(payload["error"]), now)
            elif self.status != "retry_pending":
                message = payload.get("last_agent_message") or ""
                error_prefix = re.match(
                    r"(?:error\b|rate limit exceeded\b|stream disconnected\b|"
                    r"your requests to\b|failed to connect\b)", message.strip(), re.IGNORECASE,
                )
                if error_prefix and recovery_reason(message):
                    self.fail(message, now)
                elif message:
                    self.status, self.retry_at = "complete", None
                else:
                    self.status, self.retry_at = "ended_without_confirmation", None


class Monitor:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.home = args.codex_home
        self.state_dir = args.state_dir
        self.state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.singleton = (self.state_dir / "watcher.lock").open("a")
        fcntl.flock(self.singleton, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.progress = Progress()
        self.child: subprocess.Popen | None = None
        self.stop = False
        self.log_id = 0
        self.offset = 0
        self.queued = False
        self.owner_missing_since: float | None = None
        self.last_event_at = time.time()
        self.turn_started_at = 0.0
        con = self.database("state_5.sqlite")
        row = con.execute("SELECT rollout_path,cwd,model FROM threads WHERE id=?", (args.thread,)).fetchone()
        con.close()
        if not row:
            raise ValueError("The requested saved thread does not exist")
        self.rollout, self.cwd, self.model = Path(row[0]), row[1], row[2]
        if self.model != "gpt-6-astra":
            raise ValueError("Target is not using gpt-6-astra")
        # Read historical lifecycle events only to establish the current state.
        # Historical errors and historical completion never trigger recovery.
        with self.rollout.open("rb") as stream:
            for raw in stream:
                try:
                    item = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                payload = item.get("payload", {})
                if item.get("type") == "event_msg" and payload.get("type") in (
                    "task_started", "task_complete", "turn_aborted",
                ):
                    self.progress.event(payload, time.time())
            self.offset = stream.tell()
        if self.progress.status == "complete" and self.progress.turn_id != getattr(args, "initial_turn_id", None):
            self.progress.status = "idle_at_start"
        con = self.database("logs_2.sqlite")
        self.log_id = con.execute("SELECT COALESCE(MAX(id),0) FROM logs").fetchone()[0]
        con.close()

    def database(self, name: str):
        return sqlite3.connect("file:" + str(self.home / name) + "?mode=ro", uri=True, timeout=5)

    def note(self, message: str):
        print(time.strftime("%Y-%m-%d %H:%M:%S"), message, flush=True)

    def checkpoint(self):
        data = dict(
            thread=self.args.thread, model=self.model, cwd=self.cwd,
            monitor_pid=os.getpid(), keep_awake_pid=self.args.keep_awake_pid,
            rollout_offset=self.offset, last_log_id=self.log_id,
            updated_at=time.time(), continuation_queued=self.queued,
            **dataclasses.asdict(self.progress),
        )
        temporary = self.state_dir / "checkpoint.tmp"
        temporary.write_text(json.dumps(data, indent=2) + "\n")
        temporary.chmod(0o600)
        temporary.replace(self.state_dir / "checkpoint.json")

    def owner_active(self) -> bool:
        lock = self.home / "thread-writer-locks" / (self.args.thread + ".lock")
        with lock.open("a") as stream:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return True
            fcntl.flock(stream, fcntl.LOCK_UN)
        return False

    def read_events(self):
        with self.rollout.open("rb") as stream:
            if self.rollout.stat().st_size < self.offset:
                raise RuntimeError("Rollout was replaced or truncated; refusing to replay it")
            stream.seek(self.offset)
            while True:
                before = stream.tell()
                raw = stream.readline()
                if not raw or not raw.endswith(b"\n"):
                    self.offset = before
                    break
                item = json.loads(raw)
                self.offset = stream.tell()
                self.last_event_at = time.time()
                if item.get("type") == "event_msg":
                    payload = item.get("payload", {})
                    if payload.get("type") == "task_started":
                        self.turn_started_at = dt.datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00")).timestamp()
                    self.progress.event(payload, time.time())
                if self.progress.status == "running":
                    self.queued = False

    def read_errors(self):
        con = self.database("logs_2.sqlite")
        rows = con.execute(
            "SELECT id,ts,level,target,feedback_log_body FROM logs "
            "WHERE thread_id=? AND id>? ORDER BY id",
            (self.args.thread, self.log_id),
        ).fetchall()
        con.close()
        for identity, timestamp, level, target, body in rows:
            self.log_id = identity
            if timestamp < self.turn_started_at:
                continue
            text = body.casefold()
            # Built-in retry diagnostics are evidence that Codex is recovering.
            if "retrying sampling request" in text:
                continue
            # Only terminal model errors qualify; tool errors are not failures
            # of the conversation and can be handled by Astra itself.
            terminal = (
                "turn error" in text or "error running remote compact task" in text
                or (level == "ERROR" and target in (
                    "codex_core::codex", "codex_core::responses_retry",
                    "codex_core::compact_remote",
                ))
            )
            if terminal and self.progress.status not in ("interrupted", "idle_at_start"):
                if self.progress.fail(body, time.time()):
                    self.note("Detected terminal " + str(self.progress.reason) + "; recovery scheduled")

    def recover(self):
        if self.queued or self.args.dry_run:
            return
        if self.owner_active():
            result = subprocess.run(
                [self.args.codex, "queue", "--thread", self.args.thread,
                 "--message", CONTINUE, "--resume"],
                cwd=self.cwd, stdin=subprocess.DEVNULL, capture_output=True,
                text=True, timeout=60,
            )
            if result.returncode != 0:
                self.progress.failures += 1
                self.progress.retry_at = time.time() + retry_delay("", self.progress.failures)
                self.note("Queue attempt failed; will retry with backoff")
                return
            self.queued = True
            self.note("Continuation queued for the same saved Astra conversation")
        else:
            # No active owner: resume non-interactively, preserving the thread
            # and model. Codex's own writer lock also guards a startup race.
            log = (self.state_dir / "resumed-session.log").open("ab", buffering=0)
            try:
                self.child = subprocess.Popen(
                    [self.args.codex, "exec", "resume", self.args.thread,
                     CONTINUE, "--model", self.model],
                    cwd=self.cwd, stdin=subprocess.DEVNULL,
                    stdout=log, stderr=log, start_new_session=True,
                )
            finally:
                log.close()
            self.note("Resuming saved Astra conversation; PID " + str(self.child.pid))
            self.queued = True
        self.progress.failures += 1
        self.progress.status, self.progress.retry_at = "awaiting_resume", None

    def release_sleep_protection(self):
        if self.args.dry_run:
            self.note("Dry run: would release sleep protection")
            return
        # Verify identity before signaling a PID supplied in an earlier turn.
        result = subprocess.run(
            ["/bin/ps", "-p", str(self.args.keep_awake_pid), "-o", "command="],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode != 0:
            self.note("Keep-awake helper has already exited")
            return
        if str(self.args.keep_awake_script) not in result.stdout:
            raise RuntimeError("Keep-awake PID identity changed; refusing to signal it")
        os.kill(self.args.keep_awake_pid, signal.SIGTERM)
        self.note("Released temporary keep-awake helper PID " + str(self.args.keep_awake_pid))

    def run(self):
        self.note("Watching thread " + self.args.thread + "; state=" + self.progress.status)
        (self.state_dir / "monitor.pid").write_text(str(os.getpid()) + "\n")
        while not self.stop:
            self.read_events()
            self.read_errors()
            if self.progress.status == "complete":
                # Allow a short grace period for an immediately starting turn.
                if time.time() - self.last_event_at >= 15:
                    self.release_sleep_protection()
                    self.checkpoint()
                    self.note("Observed completed requested turn; monitor finished")
                    return
            active = self.owner_active()
            if active:
                self.owner_missing_since = None
            elif self.progress.status == "running":
                self.owner_missing_since = self.owner_missing_since or time.time()
                if time.time() - self.owner_missing_since >= 30:
                    self.progress.fail("connection closed: session owner exited", time.time())
                    self.note("Session owner exited; recovery scheduled")
            if self.child is not None and self.child.poll() is not None:
                self.note("Resumed process exited with code " + str(self.child.returncode))
                if self.progress.status not in ("complete", "interrupted"):
                    self.queued = False
                    self.progress.fail("connection closed: resumed process exited", time.time())
                self.child = None
            if self.progress.retry_at is not None and time.time() >= self.progress.retry_at:
                self.recover()
            self.checkpoint()
            for _ in range(self.args.poll_interval):
                if self.stop:
                    break
                time.sleep(1)
        self.note("Monitor stopped by request; Astra and sleep helper left running")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thread", required=True)
    parser.add_argument("--initial-turn-id", help="Allow completion of this already-running turn at startup")
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    parser.add_argument("--codex", default=shutil.which("codex"))
    parser.add_argument("--keep-awake-pid", type=int, required=True)
    parser.add_argument("--keep-awake-script", type=Path, required=True)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.codex or args.poll_interval < 1:
        parser.error("Codex must be installed and poll interval must be positive")
    watcher = Monitor(args)
    def stop(signum, frame):
        watcher.stop = True
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    watcher.run()


if __name__ == "__main__":
    main()
