from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from common import atomic_json, load_json, sha256_file
from config import FREEZE, PIPELINE_VERSION, SOURCE_HASHES
from build_grouped_report import validate_sources_only
from preflight import verify as verify_preflight
from run_full160 import validate_completed


class Full160ContractTest(unittest.TestCase):
    def test_frozen_preflight_and_group_contract(self) -> None:
        result = verify_preflight(allow_progress=True)
        self.assertEqual(result["rows"], 160)
        self.assertEqual(result["banks"], 16)
        self.assertTrue(result["serial_default"])
        grouped = validate_sources_only()
        self.assertEqual(grouped, {"ok": True, "rows": 160, "banks": 16, "prompts_per_bank": 10})

    def test_atomic_json_replaces_complete_document(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "progress.json"
            atomic_json(path, {"done": ["a"]})
            atomic_json(path, {"done": ["a", "b"], "complete": True})
            self.assertEqual(load_json(path), {"done": ["a", "b"], "complete": True})
            self.assertFalse(list(path.parent.glob("*.tmp.*")))

    def test_completed_row_requires_guard_selected_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            slug = "fixture"
            job = root / slug
            job.mkdir()
            provenance = {
                "pipeline_version": PIPELINE_VERSION,
                "source_hashes": SOURCE_HASHES,
                "stage_b_attempts": [{"attempt": 1}],
                "image_calls": 1,
                "product_invariant_guard": {
                    "attempts": [{"verdict": "pass"}],
                    "selected_attempt": 1,
                },
            }
            atomic_json(job / "provenance.json", provenance)
            status = {
                "done": True,
                "stage": "done",
                "pipelineVersion": PIPELINE_VERSION,
                "sourceHashes": SOURCE_HASHES,
                "provenanceSha256": sha256_file(job / "provenance.json"),
            }
            with patch("run_full160.JOB_ROOT", root):
                self.assertEqual(validate_completed(slug, status), provenance)
                provenance["product_invariant_guard"]["attempts"][0]["verdict"] = "fail"
                atomic_json(job / "provenance.json", provenance)
                status["provenanceSha256"] = sha256_file(job / "provenance.json")
                with self.assertRaisesRegex(RuntimeError, "guard has no passing selection"):
                    validate_completed(slug, status)

    def test_freeze_has_exact_bank_ranks(self) -> None:
        freeze = json.loads(FREEZE.read_text())
        groups: dict[str, list[int]] = {}
        for row in freeze["records"]:
            groups.setdefault(f"{row['device_id']}__{row['camera_tag']}", []).append(row["bank_rank"])
        self.assertEqual(len(groups), 16)
        self.assertTrue(all(sorted(ranks) == list(range(1, 11)) for ranks in groups.values()))


if __name__ == "__main__":
    unittest.main()

