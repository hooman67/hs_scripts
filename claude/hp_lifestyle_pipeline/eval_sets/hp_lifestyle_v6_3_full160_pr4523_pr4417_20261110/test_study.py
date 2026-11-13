import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("full_study", HERE / "study.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


class PartitionTests(unittest.TestCase):
    def test_exact_frozen_complement(self):
        source = study.load(study.SOURCE)
        old = study.load(study.OLD / "study_manifest.json")
        for cell in old["cells"]:
            if cell["writer"] != "v6_3":
                continue
            reused = study.load(cell["selection_file"])["row_ids"]
            fresh = study.partition(source, reused)
            self.assertEqual(len(fresh), 130)
            self.assertFalse(set(fresh) & set(reused))
            self.assertEqual(set(fresh) | set(reused), {p["prompt_key"] for p in source["prompts"]})
            for key in reused:
                p = next(p for p in source["prompts"] if p["prompt_key"] == key)
                self.assertIsNotNone(study.image_runner().valid_completed_record(Path(cell["run_dir"]), study.row_for(p)))

    def test_duplicate_and_unknown_reuse_rejected(self):
        source = study.load(study.SOURCE)
        keys = [p["prompt_key"] for p in source["prompts"][:30]]
        for changed in (keys[:-1] + keys[:1], keys[:-1] + ["unknown"]):
            with self.assertRaises(ValueError):
                study.partition(source, changed)

    def test_ambiguous_and_duplicate_posts_blocked(self):
        # Scratch stays under the authorized durable study, never the system temp directory.
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            root = Path(directory)
            (root / "journals").mkdir()
            journal = root / "journals/events.jsonl"
            journal.write_text(json.dumps({"event": "submit_started", "row_id": "one"}) + "\n")
            cell = {"run_dir": str(root), "new_row_ids": ["one"]}
            with self.assertRaisesRegex(ValueError, "ambiguous POST"):
                study.submission_guard(cell)
            (root / "jobs").mkdir()
            (root / "jobs/one.json").write_text(json.dumps({"row_id": "one"}))
            study.submission_guard(cell)
            journal.write_text(journal.read_text() * 2)
            with self.assertRaisesRegex(ValueError, "duplicate"):
                study.submission_guard(cell)

    def test_runner_rejects_modified_selected_record(self):
        source = study.load(study.SOURCE)
        chosen = copy.deepcopy(source["prompts"][:1])
        chosen[0]["text"] += " changed"
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            path = Path(directory) / "selection.json"
            study.write(path, {"source_prompts_sha256": study.SOURCE_SHA,
                               "row_ids": [chosen[0]["prompt_key"]], "rows": chosen})
            with self.assertRaisesRegex(ValueError, "differs"):
                study.image_runner().load_selection_file(path, source, study.SOURCE_SHA)


if __name__ == "__main__":
    unittest.main()
