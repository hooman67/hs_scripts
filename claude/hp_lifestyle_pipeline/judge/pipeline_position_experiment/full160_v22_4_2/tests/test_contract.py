from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from common import atomic_json, load_json, sha256_file
from config import FREEZE, JOB_ROOT, PIPELINE_ROOT, PIPELINE_VERSION, RUN_ROOT, SOURCE_HASHES
from build_grouped_report import validate_sources_only
from preflight import verify as verify_preflight
from run_full160 import completed_progress_row, validate_completed


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
                "artifacts": {},
            }
            required = [
                "result.json", "ours.png", "input.png", "mask.png", "ref_2.png",
                "geometry_guide.png", "geometry_text.txt", "geometry_request.json",
                "geometry_response.json", "planning_request.json", "planning_response.json",
                "calls.json", "gpt_1.png",
            ]
            for name in required:
                path = job / name
                path.write_bytes(b"selected" if name in {"ours.png", "gpt_1.png"} else name.encode())
                provenance["artifacts"][name] = {
                    "path": str(path),
                    "sha256": sha256_file(path),
                    "bytes": path.stat().st_size,
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

    def test_outputs_are_isolated_from_v2233_failed_tree(self) -> None:
        old = Path(
            "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/"
            "pipeline_position_experiment/full160_v22_3_3"
        )
        for path in (RUN_ROOT, PIPELINE_ROOT, JOB_ROOT):
            self.assertIn("full160_v22_4_2", str(path))
            self.assertNotEqual(path, old / "run")
            self.assertNotIn(old / "run", path.parents)

    def test_preflight_rejects_v2233_failed_tree_as_output(self) -> None:
        old_run = Path(
            "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/"
            "pipeline_position_experiment/full160_v22_3_3/run"
        )
        with (
            patch("preflight.RUN_ROOT", old_run),
            patch("preflight.PIPELINE_ROOT", old_run / "pipeline"),
            patch("preflight.JOB_ROOT", old_run / "jobs"),
        ):
            with self.assertRaisesRegex(RuntimeError, "collides with historical experiment"):
                verify_preflight(allow_progress=True)

    def test_preflight_rejects_v2241_failed_tree_as_output(self) -> None:
        old_run = Path(
            "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/"
            "pipeline_position_experiment/full160_v22_4_1/run"
        )
        with (
            patch("preflight.RUN_ROOT", old_run),
            patch("preflight.PIPELINE_ROOT", old_run / "pipeline"),
            patch("preflight.JOB_ROOT", old_run / "jobs"),
        ):
            with self.assertRaisesRegex(RuntimeError, "collides with historical experiment"):
                verify_preflight(allow_progress=True)

    def test_freeze_has_exact_bank_ranks(self) -> None:
        freeze = json.loads(FREEZE.read_text())
        groups: dict[str, list[int]] = {}
        for row in freeze["records"]:
            groups.setdefault(f"{row['device_id']}__{row['camera_tag']}", []).append(row["bank_rank"])
        self.assertEqual(len(groups), 16)
        self.assertTrue(all(sorted(ranks) == list(range(1, 11)) for ranks in groups.values()))

    def test_progress_row_reads_selected_attempt_from_guard(self) -> None:
        # Representative V22.4.2 smoke provenance intentionally has no
        # duplicate top-level selected_attempt field.
        provenance = {
            "stage_b_attempts": [{"attempt": 1}],
            "image_calls": 2,
            "product_invariant_guard": {
                "attempts": [{"verdict": "fail"}, {"verdict": "pass"}],
                "selected_attempt": 2,
            },
        }
        self.assertNotIn("selected_attempt", provenance)
        self.assertEqual(
            completed_progress_row(provenance, 17),
            {
                "ordinal": 17,
                "stage_b_attempts": 1,
                "image_attempts": 2,
                "guard_verdicts": ["fail", "pass"],
                "selected_attempt": 2,
            },
        )


if __name__ == "__main__":
    unittest.main()

