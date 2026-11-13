#!/usr/bin/env python3
"""Offline regressions for the V2 freeze/checkpoint/drain helper."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import checkpoint_v2 as checkpoint


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n", encoding="utf-8")


class CheckpointTests(unittest.TestCase):
    def test_checkpoint_hashes_every_artifact_and_drains_submitted_only(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run = root / "run"
            write_json(run / "jobs/submitted.json", {"row_id": "row-submitted", "status": "submitted", "job_id": "j1", "result_url": "https://endpoint/jobs/j1"})
            write_json(run / "jobs/done.json", {"row_id": "row-done", "status": "materialized", "job_id": "j2"})
            write_json(run / "jobs/response-ready.json", {"row_id": "row-response-ready", "status": "completed_response_ready", "job_id": "j3", "result_url": "https://endpoint/jobs/j3"})
            write_json(run / "jobs/ambiguous.json", {"row_id": "row-ambiguous", "status": "submission_ambiguous"})
            write_json(run / "records/done.json", {"row_id": "row-done", "status": "done"})
            write_json(run / "records/ambiguous.json", {"row_id": "row-ambiguous", "status": "failed"})
            write_json(run / "raw_responses/done.json", {"debugData": {"usedPrompt": "safe"}})
            write_json(run / "blob_bindings.json", {"bindings": {}})
            (run / "images").mkdir(parents=True)
            (run / "images/output.png").write_bytes(b"image-bytes")
            manifest = root / "manifest.json"
            accepted = root / "accepted.json"
            final = root / "final.json"
            write_json(manifest, {"manifest": True})
            write_json(accepted, {"accepted": True})
            write_json(final, {"facts": {"available_generation_row_count": 1318}})
            runner_path = root / "run_generation.py"
            watch_path = root / "watch_generation.py"
            runner_path.write_text("# fixture runner\n", encoding="utf-8")
            watch_path.write_text("# fixture watch\n", encoding="utf-8")
            with mock.patch.multiple(
                checkpoint,
                V2_MANIFEST=manifest,
                V2_ACCEPTED=accepted,
                V2_FINAL_SUMMARY=final,
                V2_RUNNER=runner_path,
                V2_WATCH=watch_path,
            ):
                value = checkpoint.build_checkpoint(run, 123)
                verification = checkpoint.verify_checkpoint_files(value)
                argv = checkpoint.drain_argv(value)
            self.assertTrue(verification["passed"])
            self.assertEqual(value["final_expected_generation_row_count"], 1318)
            self.assertEqual(value["job_status_counts"], {"completed_response_ready": 1, "materialized": 1, "submission_ambiguous": 1, "submitted": 1})
            self.assertEqual(value["record_status_counts"], {"done": 1, "failed": 1})
            self.assertEqual(value["sensitive_artifact_scan"]["finding_count"], 0)
            self.assertEqual(value["consistency_issues"], [])
            self.assertEqual(argv.count("--row-id"), 2)
            self.assertIn("row-submitted", argv)
            self.assertIn("row-response-ready", argv)
            self.assertNotIn("row-done", argv)
            self.assertNotIn("row-ambiguous", argv)
            self.assertNotIn("--all", argv)
            self.assertNotIn("--all-accepted", argv)
            self.assertTrue(all("result_url" not in fact for fact in value["jobs"]))

    def test_sensitive_scan_fails_on_presigned_signature(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text('{"url":"https://x?X-Amz-Signature=secret"}', encoding="utf-8")
            result = checkpoint.sensitive_scan([path])
            self.assertFalse(result["passed"])
            self.assertEqual(result["finding_count"], 1)

    def test_stop_confirmation_is_exact(self) -> None:
        with self.assertRaisesRegex(ValueError, checkpoint.STOP_CONFIRMATION):
            checkpoint.freeze_checkpoint_stop(
                Path("/unused"), Path("/unused"), 123, "wrong-token"
            )

    def test_process_group_rejects_unexpected_member(self) -> None:
        expected = [
            {"pid": 10, "ppid": 1, "pgid": 10, "stat": "S", "argv": "python hp_lifestyle_camera_v2_eval_20261022/generation/watch_generation.py"},
            {"pid": 11, "ppid": 10, "pgid": 10, "stat": "S", "argv": "python hp_lifestyle_camera_v2_eval_20261022/generation/run_generation.py"},
            {"pid": 12, "ppid": 10, "pgid": 10, "stat": "S", "argv": "unrelated-worker"},
        ]
        with mock.patch.object(checkpoint, "group_commands", return_value=expected):
            with self.assertRaisesRegex(RuntimeError, "unexpected members"):
                checkpoint.verify_v2_process_group(10)


if __name__ == "__main__":
    unittest.main()
