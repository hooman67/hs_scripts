#!/usr/bin/env python3
"""Offline regression checks for immutable attempt allocation and selection."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from record_integrity import (
    allocate_and_write_attempt,
    list_attempt_paths,
    newest_matching_attempt,
    write_json_exclusive,
)


class RecordIntegrityTest(unittest.TestCase):
    def test_exclusive_write_refuses_existing_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "provider.json"
            write_json_exclusive(target, {"response": "first"})
            before = target.read_bytes()
            with self.assertRaises(FileExistsError):
                write_json_exclusive(target, {"response": "second"})
            self.assertEqual(target.read_bytes(), before)

    def test_allocation_uses_global_max_and_preserves_gap_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            attempts = Path(tmp)
            write_json_exclusive(attempts / "sample_001.json", {"request_sha256": "old-a"})
            protected = attempts / "sample_003.json"
            write_json_exclusive(protected, {"request_sha256": "old-b", "marker": "preserve"})
            before = protected.read_bytes()

            target = allocate_and_write_attempt(attempts, {"request_sha256": "new"})

            self.assertEqual(target.name, "sample_004.json")
            self.assertEqual(protected.read_bytes(), before)

    def test_indices_above_999_remain_visible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            attempts = Path(tmp)
            write_json_exclusive(attempts / "sample_999.json", {"request_sha256": "old"})
            target = allocate_and_write_attempt(attempts, {"request_sha256": "new"})
            self.assertEqual(target.name, "sample_1000.json")
            self.assertEqual([p.name for p in list_attempt_paths(attempts)],
                             ["sample_999.json", "sample_1000.json"])

    def test_concurrent_allocations_are_unique(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            attempts = Path(tmp)
            with ThreadPoolExecutor(max_workers=2) as pool:
                paths = list(pool.map(
                    lambda marker: allocate_and_write_attempt(
                        attempts, {"request_sha256": "same", "marker": marker}),
                    ("a", "b"),
                ))
            self.assertEqual({p.name for p in paths}, {"sample_001.json", "sample_002.json"})
            self.assertEqual({json.loads(p.read_text())["marker"] for p in paths}, {"a", "b"})

    def test_newest_matching_failure_blocks_stale_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            attempts = Path(tmp)
            write_json_exclusive(attempts / "sample_001.json", {
                "request_sha256": "current", "parsed_output": {"prompts": []},
            })
            write_json_exclusive(attempts / "sample_002.json", {
                "request_sha256": "other", "parsed_output": {"prompts": []},
            })
            write_json_exclusive(attempts / "sample_003.json", {
                "request_sha256": "current", "status": "failed_preserved",
            })

            path, record = newest_matching_attempt(attempts, "current") or (None, None)

            self.assertEqual(path.name, "sample_003.json")
            self.assertEqual(record["status"], "failed_preserved")


if __name__ == "__main__":
    unittest.main()
