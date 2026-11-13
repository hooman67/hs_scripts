#!/usr/bin/env python3
"""Retry a Codex TUI turn when Astra remote compaction hits its rate limit.

The script is intended to run as a ``tmux pipe-pane`` consumer. It watches the
pane's output without hiding or redirecting it, then queues a continuation in
the same Codex session whenever the exact Astra remote-compaction error is
rendered.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import select
import subprocess
import sys
import time
from pathlib import Path


ERROR_MARKERS = (
    "error running remote compact task",
    "rate limit exceeded",
    "gpt-6-astra",
)
ANSI_PATTERN = re.compile(
    r"\x1b(?:"
    r"\[[0-?]*[ -/]*[@-~]"
    r"|\][^\x07]*(?:\x07|\x1b\\)"
    r"|[()][A-Z0-9]"
    r"|."
    r")",
    re.DOTALL,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="tmux pane, e.g. hs_sess:0.0")
    parser.add_argument("--thread", required=True, help="exact Codex session name")
    parser.add_argument(
        "--message",
        default="Continue where you left off with your previous task.",
    )
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="detect and log without submitting a Codex message",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=1.0,
        help="seconds between rendered-pane checks (default: 1)",
    )
    return parser.parse_args()


class Watcher:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.raw_window = ""
        self.last_submit_at = 0.0
        self.armed = True
        self.screen_error_present: bool | None = None

    def log(self, message: str) -> None:
        timestamp = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
        self.args.log.parent.mkdir(parents=True, exist_ok=True)
        with self.args.log.open("a", encoding="utf-8") as handle:
            handle.write(f"{timestamp} {message}\n")

    def submit(self) -> None:
        now = time.monotonic()
        if now - self.last_submit_at < 2.0:
            return
        self.last_submit_at = now

        if self.args.dry_run:
            self.log("DRY RUN: detected rate limit; would queue continuation")
            return

        key_commands = [
            ["tmux", "send-keys", "-t", self.args.target, "C-u"],
            ["tmux", "send-keys", "-t", self.args.target, "-l", self.args.message],
            ["tmux", "send-keys", "-t", self.args.target, "Enter"],
        ]
        key_results = [
            subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=5,
                check=False,
            )
            for command in key_commands
        ]
        if all(result.returncode == 0 for result in key_results):
            self.log("detected Astra rate limit; submitted continuation via tmux")
            return

        detail = " ".join(
            result.stdout for result in key_results if result.returncode != 0
        ).strip()[-500:]
        self.log(f"tmux input failed: {detail}; falling back to codex queue")
        result = subprocess.run(
            [
                "codex",
                "queue",
                "--thread",
                self.args.thread,
                "--message",
                self.args.message,
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=20,
            check=False,
        )
        if result.returncode == 0:
            self.log("detected Astra rate limit; queued continuation via Codex")
            return

        detail = " ".join(result.stdout.split())[-500:]
        self.log(
            f"codex queue fallback failed with exit {result.returncode}: {detail}"
        )

    @staticmethod
    def clean_terminal_text(text: str) -> str:
        """Remove terminal controls and normalize TUI wrapping/redraw whitespace."""
        cleaned = ANSI_PATTERN.sub(" ", text)
        cleaned = "".join(char if char.isprintable() else " " for char in cleaned)
        return " ".join(cleaned.casefold().split())

    @staticmethod
    def contains_error(cleaned: str) -> bool:
        """Match stable parts of the terminal error instead of its rendered layout."""
        return all(marker in cleaned for marker in ERROR_MARKERS)

    @staticmethod
    def latest_error_position(cleaned: str) -> int:
        """Return the newest complete error marker group in normalized text."""
        search_end = len(cleaned)
        while search_end:
            start = cleaned.rfind(ERROR_MARKERS[0], 0, search_end)
            if start < 0:
                return -1
            tail = cleaned[start : start + 2048]
            if all(marker in tail for marker in ERROR_MARKERS[1:]):
                return start
            search_end = start
        return -1

    def mark_detected(self, source: str) -> None:
        if not self.armed:
            return
        self.armed = False
        self.raw_window = ""
        self.log(f"detected Astra rate limit in {source}")
        self.submit()

    def capture_screen(self) -> str | None:
        result = subprocess.run(
            ["tmux", "capture-pane", "-p", "-J", "-t", self.args.target],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode != 0:
            detail = " ".join(result.stdout.split())[-500:]
            self.log(f"rendered-pane check failed: {detail}")
            return None
        return result.stdout

    def poll_screen(self) -> None:
        """Detect an error in tmux's rendered view when raw TUI output is fragmented."""
        screen = self.capture_screen()
        if screen is None:
            return

        cleaned = self.clean_terminal_text(screen)
        error_position = self.latest_error_position(cleaned)
        normalized_message = self.clean_terminal_text(self.args.message)
        message_position = cleaned.rfind(normalized_message)
        # An old error above the continuation is already handled. A new error
        # below it is actionable even when both remain visible in the pane.
        has_actionable_error = error_position > message_position

        if not self.armed:
            if message_position >= 0:
                self.armed = True
                self.raw_window = ""
                self.log("continuation appeared in rendered pane; watcher re-armed")

        # Treat the first capture as a baseline. This prevents restarting the
        # watcher from acting on an old error that was already on screen.
        if self.screen_error_present is None:
            self.screen_error_present = has_actionable_error
            return

        if not has_actionable_error:
            self.screen_error_present = False
            return

        if not self.screen_error_present:
            self.screen_error_present = True
            self.mark_detected("rendered pane")

    def consume(self, chunk: bytes) -> None:
        decoded = chunk.decode("utf-8", errors="ignore")
        self.raw_window = (self.raw_window + decoded)[-32768:]
        cleaned = self.clean_terminal_text(self.raw_window)

        if not self.armed:
            normalized_message = self.clean_terminal_text(self.args.message)
            if normalized_message not in cleaned:
                return
            self.armed = True
            self.raw_window = ""
            self.log("continuation appeared in pane; watcher re-armed")
            return

        if not self.contains_error(cleaned):
            return

        self.screen_error_present = True
        self.mark_detected("raw tmux stream")

    def run(self) -> int:
        self.log(
            f"watcher started pid={os.getpid()} target={self.args.target} "
            f"thread={self.args.thread!r}"
        )
        if self.args.poll_interval <= 0:
            raise ValueError("--poll-interval must be greater than zero")

        self.poll_screen()
        next_poll = time.monotonic() + self.args.poll_interval
        while True:
            timeout = max(0.0, next_poll - time.monotonic())
            readable, _, _ = select.select([sys.stdin.buffer], [], [], timeout)
            if readable:
                chunk = sys.stdin.buffer.read1(4096)
                if not chunk:
                    self.log("watcher stopped: tmux output pipe closed")
                    return 0
                self.consume(chunk)

            if time.monotonic() >= next_poll:
                self.poll_screen()
                next_poll = time.monotonic() + self.args.poll_interval


def main() -> int:
    return Watcher(parse_args()).run()


if __name__ == "__main__":
    raise SystemExit(main())
