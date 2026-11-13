#!/usr/bin/env python3
"""Small, dependency-free helpers for immutable GPT attempt records."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any


_SAMPLE_RE = re.compile(r"^sample_(\d+)\.json$")


def sample_index(path: Path) -> int | None:
    match = _SAMPLE_RE.fullmatch(path.name)
    return int(match.group(1)) if match else None


def list_attempt_paths(attempt_dir: Path) -> list[Path]:
    """Return completed attempts in numeric order, including indices above 999."""
    if not attempt_dir.exists():
        return []
    indexed = ((index, path) for path in attempt_dir.iterdir()
               if path.is_file() and (index := sample_index(path)) is not None)
    return [path for _, path in sorted(indexed)]


def newest_matching_attempt(attempt_dir: Path, request_sha256: str) -> tuple[Path, dict[str, Any]] | None:
    """Return only the newest attempt for a request, regardless of its outcome."""
    for path in reversed(list_attempt_paths(attempt_dir)):
        record = json.loads(path.read_text())
        if record.get("request_sha256") == request_sha256:
            return path, record
    return None


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def write_json_exclusive(path: Path, value: Any) -> None:
    """Create one JSON file durably and fail rather than replace existing bytes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json_bytes(value)
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    directory_fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def allocate_and_write_attempt(attempt_dir: Path, record: dict[str, Any]) -> Path:
    """Atomically allocate max(global sample index)+1 and never overwrite a record."""
    attempt_dir.mkdir(parents=True, exist_ok=True)
    while True:
        paths = list_attempt_paths(attempt_dir)
        next_index = max((sample_index(path) or 0 for path in paths), default=0) + 1
        target = attempt_dir / f"sample_{next_index:03d}.json"
        try:
            write_json_exclusive(target, record)
            return target
        except FileExistsError:
            # Another process won this index after our scan. Re-scan globally and retry.
            continue
