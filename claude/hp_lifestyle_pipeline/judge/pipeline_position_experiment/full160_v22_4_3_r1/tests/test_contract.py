from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from build_grouped_report import validate_sources_only
from common import atomic_json, load_json, sha256_file, sha256_json
from config import (
    FREEZE, JOB_ROOT, MAX_OUTER_JOBS, PACKAGE, PIPELINE_ROOT, PIPELINE_VERSION,
    RETRYABLE_GUARD_ERROR, ROOT, RUN_ROOT, SOURCE_HASHES, WRAPPER_VERSION,
)
from preflight import verify as verify_preflight
from run_full160 import (
    audit_summary, initial_progress, job_id, required_artifact_names,
    should_retry, update_rates, validate_completed, validate_failed,
)


class ContractTest(unittest.TestCase):
    def make_success(self, root: Path, slug="fixture", attempt=1):
        jid = job_id(slug, attempt)
        job = root / jid
        job.mkdir(parents=True)
        submission = {"rowSlug": slug, "outerAttempt": attempt}
        atomic_json(job / "submission_request.json", submission)
        provenance = {
            "job_id": jid, "row_slug": slug, "outer_attempt": attempt,
            "submission_request_sha256": sha256_json(submission),
            "pipeline_version": PIPELINE_VERSION, "wrapper_version": WRAPPER_VERSION,
            "source_hashes": SOURCE_HASHES, "stage_b_attempts": [{"attempt": 1}],
            "image_calls": 1,
            "product_invariant_guard": {"attempts": [{"verdict": "pass"}], "selected_attempt": 1},
            "artifacts": {},
        }
        for name in sorted(required_artifact_names(provenance)):
            path = job / name
            if not path.exists():
                path.write_bytes(b"selected" if name in {"ours.png", "gpt_1.png"} else name.encode())
            provenance["artifacts"][f"fixture/{name}"] = {"path": str(path), "sha256": sha256_file(path), "bytes": path.stat().st_size}
        atomic_json(job / "provenance.json", provenance)
        status = {
            "jobId": jid, "rowSlug": slug, "outerAttempt": attempt, "done": True,
            "stage": "done", "error": None, "pipelineVersion": PIPELINE_VERSION,
            "wrapperVersion": WRAPPER_VERSION, "sourceHashes": SOURCE_HASHES,
            "submissionRequestSha256": sha256_json(submission),
            "artifactManifestSha256": sha256_json(provenance["artifacts"]),
            "provenanceSha256": sha256_file(job / "provenance.json"),
        }
        atomic_json(job / "status.json", status)
        return jid, provenance, status

    def make_failure(self, root: Path, slug="fixture", attempt=1, error=RETRYABLE_GUARD_ERROR):
        jid = job_id(slug, attempt)
        job = root / jid
        job.mkdir(parents=True)
        submission = {"rowSlug": slug, "outerAttempt": attempt}
        atomic_json(job / "submission_request.json", submission)
        artifact = job / "gpt_1.png"
        artifact.write_bytes(b"failed raw attempt")
        artifacts = {"fixture/gpt_1.png": {"path": str(artifact), "sha256": sha256_file(artifact), "bytes": artifact.stat().st_size}}
        failure = {
            "job_id": jid, "row_slug": slug, "outer_attempt": attempt,
            "submission_request_sha256": sha256_json(submission), "error": error,
            "pipeline_version": PIPELINE_VERSION, "wrapper_version": WRAPPER_VERSION,
            "source_hashes": SOURCE_HASHES, "artifacts": artifacts,
        }
        atomic_json(job / "failure_provenance.json", failure)
        status = {
            "jobId": jid, "rowSlug": slug, "outerAttempt": attempt, "done": True,
            "stage": "error", "error": error, "pipelineVersion": PIPELINE_VERSION,
            "wrapperVersion": WRAPPER_VERSION, "sourceHashes": SOURCE_HASHES,
            "submissionRequestSha256": sha256_json(submission),
            "artifactManifestSha256": sha256_json(artifacts),
            "failureProvenanceSha256": sha256_file(job / "failure_provenance.json"),
        }
        atomic_json(job / "status.json", status)
        return jid, failure, status

    def test_frozen_preflight_and_160_by_16_contract(self):
        result = verify_preflight(allow_progress=True)
        self.assertEqual((result["rows"], result["banks"], result["max_outer_jobs_per_row"]), (160, 16, 2))
        self.assertFalse(result["native_reliability_claim"])
        self.assertEqual(validate_sources_only(), {"ok": True, "rows": 160, "banks": 16, "prompts_per_bank": 10})

    def test_job_ids_are_distinct_and_bounded(self):
        self.assertEqual(job_id("row", 1), "row__outer_job_1")
        self.assertEqual(job_id("row", 2), "row__outer_job_2")
        self.assertNotEqual(job_id("row", 1), job_id("row", 2))
        with self.assertRaisesRegex(RuntimeError, "outer attempt"):
            job_id("row", 3)

    def test_retry_only_exact_guard_error_on_first_job(self):
        self.assertTrue(should_retry({"stage": "error", "error": RETRYABLE_GUARD_ERROR}, 1))
        self.assertFalse(should_retry({"stage": "error", "error": RETRYABLE_GUARD_ERROR + " "}, 1))
        self.assertFalse(should_retry({"stage": "error", "error": "TimeoutError: x"}, 1))
        self.assertFalse(should_retry({"stage": "done", "error": None}, 1))
        self.assertFalse(should_retry({"stage": "error", "error": RETRYABLE_GUARD_ERROR}, 2))

    def test_success_audit_selects_first_passing_job(self):
        with tempfile.TemporaryDirectory() as d, patch("run_full160.JOB_ROOT", Path(d)):
            jid, provenance, status = self.make_success(Path(d), attempt=1)
            self.assertEqual(validate_completed("fixture", 1, status), provenance)
            summary = audit_summary("fixture", 1, status)
            self.assertEqual((summary["job_id"], summary["outcome"]), (jid, "done"))
            self.assertFalse((Path(d) / job_id("fixture", 2)).exists())

    def test_failed_job_is_fully_hash_audited(self):
        with tempfile.TemporaryDirectory() as d, patch("run_full160.JOB_ROOT", Path(d)):
            _, failure, status = self.make_failure(Path(d))
            self.assertEqual(validate_failed("fixture", 1, status), failure)
            Path(next(iter(failure["artifacts"].values()))["path"]).write_bytes(b"tampered")
            with self.assertRaisesRegex(RuntimeError, "artifact hash mismatch"):
                validate_failed("fixture", 1, status)

    def test_second_job_success_is_independently_audited(self):
        with tempfile.TemporaryDirectory() as d, patch("run_full160.JOB_ROOT", Path(d)):
            _, _, failed = self.make_failure(Path(d), attempt=1)
            _, success, passed = self.make_success(Path(d), attempt=2)
            validate_failed("fixture", 1, failed)
            self.assertEqual(validate_completed("fixture", 2, passed), success)
            self.assertNotEqual(failed["submissionRequestSha256"], passed["submissionRequestSha256"])

    def test_second_failure_is_terminal_not_retryable(self):
        with tempfile.TemporaryDirectory() as d, patch("run_full160.JOB_ROOT", Path(d)):
            _, _, first = self.make_failure(Path(d), attempt=1)
            _, _, second = self.make_failure(Path(d), attempt=2)
            validate_failed("fixture", 1, first)
            validate_failed("fixture", 2, second)
            self.assertTrue(should_retry(first, 1))
            self.assertFalse(should_retry(second, 2))

    def test_progress_rates_distinguish_protocol_outcomes(self):
        progress = {"counts": {"first_job_pass": 7, "recovered_on_retry": 2, "terminal_failure": 1}}
        update_rates(progress)
        self.assertEqual(progress["rates"]["denominator_rows_attempted"], 10)
        self.assertEqual(progress["rates"]["first_job_pass_rate"], .7)
        self.assertEqual(progress["rates"]["recovered_on_retry_rate"], .2)
        self.assertEqual(progress["rates"]["terminal_failure_rate"], .1)

    def test_initial_progress_disclaims_native_reliability(self):
        freeze = load_json(FREEZE)
        health = {"instanceId": "x", "pipelineVersion": PIPELINE_VERSION, "wrapperVersion": WRAPPER_VERSION, "sourceHashes": SOURCE_HASHES}
        progress = initial_progress(health, freeze)
        self.assertIn("not native V22.4.3", progress["protocol"]["interpretation"])
        self.assertEqual(progress["protocol"]["max_outer_jobs_per_row"], MAX_OUTER_JOBS)

    def test_pipeline_sources_remain_exactly_frozen(self):
        freeze = load_json(FREEZE)
        actual = {name: sha256_file(PACKAGE / name) for name in SOURCE_HASHES}
        self.assertEqual(actual, SOURCE_HASHES)
        self.assertEqual(actual, freeze["treatment"]["source_hashes"])

    def test_old_v2243_tree_is_forbidden_and_distinct(self):
        old = ROOT.parent / "full160_v22_4_3" / "run"
        self.assertNotEqual(RUN_ROOT, old)
        with patch("preflight.RUN_ROOT", old), patch("preflight.PIPELINE_ROOT", old / "pipeline"), patch("preflight.JOB_ROOT", old / "jobs"):
            with self.assertRaisesRegex(RuntimeError, "collides with historical experiment"):
                verify_preflight(allow_progress=True)

    def test_freeze_declares_exact_retry_policy(self):
        policy = load_json(FREEZE)["treatment"]["outer_job_policy"]
        self.assertEqual(policy["maximum_jobs_per_row"], 2)
        self.assertEqual(policy["retry_only_exact_error"], RETRYABLE_GUARD_ERROR)
        self.assertEqual(policy["selection"], "first passing outer job")

    def test_no_run_or_log_tree_created_during_preparation(self):
        self.assertFalse(RUN_ROOT.exists())
        self.assertFalse((ROOT / "logs").exists())


if __name__ == "__main__":
    unittest.main()
