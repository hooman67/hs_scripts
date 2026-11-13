#!/usr/bin/env python3
"""Daily auto-commit + push for ~/hs_scripts.

Replaces the prior watchdog-based file watcher. Run once per day via
launchd (~/Library/LaunchAgents/com.user.autocommit.plist).

Behavior:
- Stages every uncommitted change (git add -A).
- Skips entirely if there is nothing to commit.
- One commit with a daily-snapshot message, then `git push`.
- Logs to /tmp/autocommit.log via the launchd StandardOutPath redirect.
- Refuses to operate if HEAD has merge conflicts (lets the user resolve).
"""
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent
TS = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def run(cmd, check=False):
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if check and r.returncode != 0:
        print(f"[{TS}] FAIL: {' '.join(cmd)}\n  stdout: {r.stdout}\n  stderr: {r.stderr}")
        sys.exit(r.returncode)
    return r


def main():
    # Refuse if mid-merge / mid-rebase — leave it for the human.
    git_dir = REPO / ".git"
    for sentinel in ("MERGE_HEAD", "REBASE_HEAD", "CHERRY_PICK_HEAD"):
        if (git_dir / sentinel).exists():
            print(f"[{TS}] Skip: {sentinel} present — repo is mid-operation.")
            return 0

    status = run(["git", "status", "--porcelain"])
    if not status.stdout.strip():
        print(f"[{TS}] Nothing to commit.")
        return 0

    file_count = len(status.stdout.strip().splitlines())

    run(["git", "add", "-A"], check=True)

    msg = f"Auto-commit: daily snapshot at {TS} ({file_count} changes)"
    commit = run(["git", "commit", "-m", msg])
    if commit.returncode != 0:
        # Could be "nothing to commit" if a hook stripped staged content; bail quietly.
        print(f"[{TS}] commit returned {commit.returncode}:\n  stdout: {commit.stdout}\n  stderr: {commit.stderr}")
        return 0

    push = run(["git", "push"])
    if push.returncode != 0:
        print(f"[{TS}] PUSH FAILED:\n  stdout: {push.stdout}\n  stderr: {push.stderr}")
        return 1

    print(f"[{TS}] Committed {file_count} changes and pushed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
