from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("hp16_runner", HERE / "run_hp16.py")
RUNNER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RUNNER)


class HP16RunnerTests(unittest.TestCase):
    def test_frozen_tasks_are_exact_and_mapped(self):
        tasks, document = RUNNER.load_tasks()
        self.assertEqual(len(tasks), 96)
        self.assertEqual(len({task["prompt_key"] for task in tasks}), 96)
        self.assertEqual(
            {task["digitalTwinId"] for task in tasks},
            {"cashmere_x", "elitebook_13", "tassel", "adf_printer"},
        )
        self.assertEqual(document["counts"]["prompts"], 96)

    def test_catalog_requires_every_exact_pair(self):
        tasks, _ = RUNNER.load_tasks()
        catalogue = {
            "digitalTwins": [
                {
                    "id": sku,
                    "cameras": [{"id": task["cameraId"]} for task in tasks if task["digitalTwinId"] == sku],
                }
                for sku in sorted({task["digitalTwinId"] for task in tasks})
            ]
        }
        RUNNER.validate_catalog(tasks, catalogue)
        catalogue["digitalTwins"][0]["cameras"] = []
        with self.assertRaises(RuntimeError):
            RUNNER.validate_catalog(tasks, catalogue)

    def test_stage_success_requires_all_five_done(self):
        manifest = {"stages": {name: {"status": "done"} for name in RUNNER.REQUIRED_STAGES}}
        self.assertTrue(RUNNER.stage_success(manifest))
        manifest["stages"]["relight"]["status"] = "failed"
        self.assertFalse(RUNNER.stage_success(manifest))

    def test_token_file_must_be_private(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "token.txt"
            path.write_text("synthetic-token\n", encoding="utf-8")
            path.chmod(0o644)
            with self.assertRaises(RuntimeError):
                RUNNER.read_token(path)
            path.chmod(0o600)
            self.assertEqual(RUNNER.read_token(path), "synthetic-token")


if __name__ == "__main__":
    unittest.main()
