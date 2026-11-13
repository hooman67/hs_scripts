from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import report
import study


class ReportTests(unittest.TestCase):
    def test_restart_retries_only_explicit_orphans_not_completed_or_model_failed_jobs(self):
        import restart

        scene = {"status": "error", "has_image": False,
                 "error": "Endpoint restarted with an incomplete job. No automatic replay; inspect saved call journals."}
        restart.require_interrupted({"done": True, "stages": {"scene": scene}})
        for changed in ({**scene, "has_image": True}, {**scene, "error": "image model rejected request"},
                        {**scene, "status": "done"}):
            with self.assertRaisesRegex(ValueError, "not an explicitly interrupted"):
                restart.require_interrupted({"done": True, "stages": {"scene": changed}})

    def test_restart_redirects_only_four_interrupted_jobs_not_completed_images(self):
        manifest = study.verified_manifest()
        observed = study.load(HERE / "interruption_check_20261110.json")
        keys = {job["row_id"] for job in observed["submitted_unmaterialized_jobs"]
                if job["cell"] == "v6_3_pr4523"}
        self.assertEqual(len(keys), 4)
        retry_dir = HERE / "runs/restart-test-only"
        plan = {"origin_cell": "v6_3_pr4523", "interrupted_attempts": dict.fromkeys(keys),
                "retry_run": {"run_dir": str(retry_dir)}}
        redirected = []
        with patch("restart.verified_plan", return_value=plan):
            for cell in manifest["cells"]:
                reused_keys = {row["prompt_key"] for row in cell["reused"]}
                for prompt in study.load(study.SOURCE)["prompts"]:
                    directory, state, reused = report.binding(cell, prompt)
                    if cell["name"] == plan["origin_cell"] and prompt["prompt_key"] in keys:
                        self.assertEqual(directory, retry_dir)
                        self.assertEqual(state, "new")
                        self.assertIsNone(reused)
                        redirected.append(prompt["prompt_key"])
                    else:
                        expected = cell["prior_run_dir"] if prompt["prompt_key"] in reused_keys else cell["run_dir"]
                        self.assertEqual(directory, Path(expected))
        self.assertEqual(set(redirected), keys)

    def test_restart_rejects_a_fifth_submission_and_changed_preserved_evidence(self):
        import restart

        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            root = Path(directory)
            preserved = root / "preserved.txt"
            preserved.write_text("unchanged")
            retry = {"run_dir": str(root), "new_row_ids": []}
            plan = {"retry_run": retry, "preserved_before_restart": {str(preserved): study.sha(preserved)}}
            with patch.object(restart, "verified_plan", return_value=plan), \
                    patch.object(study, "verified_manifest", return_value={"cells": []}):
                restart.submission_guard()
                preserved.write_text("changed")
                with self.assertRaisesRegex(ValueError, "evidence was changed"):
                    restart.submission_guard()
                plan["preserved_before_restart"] = {}
                with patch.object(restart, "events", return_value=[
                    {"event": "submit_started"} for _ in range(5)
                ]):
                    with self.assertRaisesRegex(ValueError, "four explicitly authorized"):
                        restart.submission_guard()

    def test_native_and_reused_inputs_bind_original_records(self):
        manifest = study.verified_manifest()
        prompts = study.load(study.SOURCE)["prompts"]
        tested = set()
        for cell in manifest["cells"]:
            for prompt in prompts:
                ap = report.audit_path(cell, prompt)
                if not ap.exists():
                    continue
                run_dir, reuse_status, reused = report.binding(cell, prompt)
                case = cell["pr"], reuse_status
                if case in tested:
                    continue
                record_path = study.image_runner().paths(run_dir, study.row_for(prompt))["record"]
                audit = report.checked_audit(ap, record_path)
                self.assertEqual(audit["reuse_status"], reuse_status)
                if reused:
                    self.assertEqual(audit["origin_study_manifest_sha256"], reused["origin_study_manifest_sha256"])
                    self.assertEqual(audit["origin_run_sha256"], reused["run_sha256"])
                self.assertEqual(audit["new_model_calls"], 0)
                tested.add(case)
        self.assertEqual(tested, {("pr4523", "reused"), ("pr4417", "reused"), ("pr4523", "new"), ("pr4417", "new")})

    def test_source_has_full160_rows_and_exact_partition_states(self):
        data = study.load(report.PUBLIC / "data/comparison.json")
        self.assertEqual(len(data["rows"]), 160)
        self.assertEqual(len({tuple(row["key"]) for row in data["rows"]}), 160)
        for cell in data["cells"]:
            self.assertEqual(sum(row["outputs"][cell]["reuse_status"] == "reused" for row in data["rows"]), 30)
            self.assertEqual(sum(row["outputs"][cell]["reuse_status"] == "new" for row in data["rows"]), 130)
        self.assertFalse(any("judge_score" in output for row in data["rows"] for output in row["outputs"].values()))

    def test_foreign_object_and_unallowlisted_file_block_publication(self):
        class ForeignClient:
            def head_object(self, **kwargs):
                return {"Metadata": {"hp-study-sha256": "foreign"}}
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            root = Path(directory)
            (root / "gallery").mkdir()
            page = root / "gallery/index.html"
            page.write_text("test page")
            study.write(root / "asset_manifest.json", {"assets": {"gallery/index.html":
                        {"sha256": study.sha(page), "bytes": page.stat().st_size}}})
            with patch.object(report, "PUBLIC", root), patch.object(report, "s3_client", return_value=ForeignClient()):
                with self.assertRaisesRegex(FileExistsError, "not owned"):
                    report.publish()
                (root / "not-allowed.env").write_text("not a credential; forbidden suffix test")
                with self.assertRaisesRegex(ValueError, "allowlist"):
                    report.publish()

    def test_altered_image_input_rejected(self):
        with self.assertRaisesRegex(ValueError, "differs"):
            report.image_evidence(b"not an image", "0" * 64)


if __name__ == "__main__":
    unittest.main()
