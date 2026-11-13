#!/usr/bin/env python3

import json
import tempfile
import unittest
from pathlib import Path

from record_integrity import (
    allocate_and_write_attempt,
    distinct_request_hashes,
    list_attempt_paths,
    newest_matching_attempt,
    write_json_exclusive,
)


class RecordIntegrityTest(unittest.TestCase):
    def test_attempts_are_exclusive_and_resume_uses_newest_request_match(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = allocate_and_write_attempt(root, {"request_sha256": "a", "status": "ok"})
            second = allocate_and_write_attempt(root, {"request_sha256": "b", "status": "failed"})
            third = allocate_and_write_attempt(root, {"request_sha256": "a", "status": "latest"})
            self.assertEqual([p.name for p in list_attempt_paths(root)], [
                "sample_001.json", "sample_002.json", "sample_003.json"
            ])
            self.assertEqual((first.name, second.name, third.name), (
                "sample_001.json", "sample_002.json", "sample_003.json"
            ))
            path, record = newest_matching_attempt(root, "a") or (None, None)
            self.assertEqual(path, third)
            self.assertEqual(record["status"], "latest")
            self.assertEqual(distinct_request_hashes(root), ["a", "b"])

    def test_exclusive_writer_never_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "record.json"
            write_json_exclusive(path, {"value": 1})
            original = path.read_bytes()
            with self.assertRaises(FileExistsError):
                write_json_exclusive(path, {"value": 2})
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(json.loads(original), {"value": 1})


if __name__ == "__main__":
    unittest.main()
