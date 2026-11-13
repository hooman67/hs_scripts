"""Offline contract tests for the isolated V4.1 image runner."""

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import httpx
from PIL import Image


SCRIPT = Path(__file__).with_name("run_generation.py")
SPEC = importlib.util.spec_from_file_location("ctech_v41_runner", SCRIPT)
runner = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


def write_json(path: Path, value: dict) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    return runner.sha256_path(path)


class Fixture:
    tags = (
        ("laptop_FrontRightCloseUp", "laptop", "close_up"),
        ("laptop_FrontRightWide", "laptop", "wide"),
        ("printer_FrontRightCloseUp", "printer", "close_up"),
        ("printer_FrontRightWide", "printer", "wide"),
    )

    def __init__(self, root: Path):
        self.root = root
        self.run_dir = root / "run"
        self.renders = []
        self.prompts = []
        self.cases = {}
        for index, (tag, device, role) in enumerate(self.tags):
            case_id = f"source{index}__{tag}"
            image_path = root / f"{tag}.png"
            Image.new("RGB", (1024, 576), (index * 20, 40, 60)).save(image_path)
            self.renders.append({
                "render_id": f"corrected_{tag}", "device_type": device,
                "camera_tag": tag, "role": role, "path": str(image_path),
                "sha256": runner.sha256_path(image_path), "bytes": image_path.stat().st_size,
                "width": 1024, "height": 576, "format": "PNG",
                "source_s3_uri": f"s3://fixture/{tag}.png",
                "source_gallery_url": f"https://example/{tag}.png",
            })
            candidates = []
            for rank in range(1, 31):
                candidate_id = f"p{rank}"
                key = f"{case_id}::{candidate_id}"
                text = f"Scene {rank} for {tag}."
                text_sha = runner.sha256_bytes(text.encode())
                candidate = {
                    "candidate_key": key, "id": candidate_id, "rank": rank,
                    "text": text, "text_sha256": text_sha,
                }
                candidates.append(candidate)
                self.prompts.append({
                    "candidate_key": key, "case_id": case_id, "source_id": f"source{index}",
                    "device_type": device, "camera_tag": tag, "view_role": role,
                    "rank": rank, "rank_bin": "1-10" if rank <= 10 else "11-20" if rank <= 20 else "21-30",
                    "text": text, "reviewed_candidate_id": candidate_id,
                    "first_draw_raw_record_path": str(root / "first.json"),
                    "first_draw_raw_record_sha256": "a" * 64,
                    "correction_provider_response_path": str(root / "correction.json"),
                    "correction_provider_response_sha256": "b" * 64,
                })
            self.cases[case_id] = {
                "case_id": case_id, "group_id": f"group{index}", "source_id": f"source{index}",
                "device_type": device, "camera_tag": tag, "view_role": role,
                "provenance_map_path": str(root / "provenance.json"),
                "candidates": candidates,
            }
        self.pilot = {
            "status": runner.EXPECTED_PILOT_STATUS, "prompt_count": 120,
            "prompts": self.prompts,
        }
        self.accepted = {
            "status": runner.EXPECTED_PILOT_STATUS,
            "counts": {"accepted_cases": 4, "candidates": 120}, "cases": self.cases,
        }

    def manifest(self, pilot_path: Path, pilot_sha: str, accepted_path: Path, accepted_sha: str):
        return {
            "version": "fixture-v1", "status": "authorized",
            "authorized_at": "2026-10-27T00:00:00Z",
            "scope": {"image_generation_authorized": True, "expected_images": 120},
            "pilot_prompts": {"path": str(pilot_path), "sha256": pilot_sha},
            "accepted_prompt_cases": {"path": str(accepted_path), "sha256": accepted_sha},
            "renders": self.renders,
            "model": {"base_url": runner.BASE_URL, "rewriter_model": "gemini-3.1-pro",
                      "num_inference_steps": 50, "seed": 42, "n": 1},
            "run_dir": str(self.run_dir),
            "s3": {"bucket": runner.EXPECTED_S3_BUCKET, "prefix": runner.EXPECTED_S3_PREFIX},
        }


class RunnerTests(unittest.TestCase):
    def test_builds_exact_120_rows_and_fixed_payload(self):
        with TemporaryDirectory() as directory:
            fixture = Fixture(Path(directory))
            manifest = {"renders": fixture.renders}
            rows = runner.build_rows(manifest, fixture.accepted, fixture.pilot)
            self.assertEqual(len(rows), 120)
            self.assertEqual(len({row["row_id"] for row in rows}), 120)
            payload = runner.build_payload(rows[0], "blob")
            self.assertEqual(payload["seeds"], [42])
            self.assertEqual(payload["n"], 1)
            self.assertEqual(payload["size"], {"width": 2560, "height": 1440})
            self.assertEqual(payload["modelSpecificPayload"], {
                "enablePromptRewrite": True, "rewriterModel": "gemini-3.1-pro",
                "numInferenceSteps": 50,
            })

    def test_load_inputs_pins_exact_artifact_bytes_and_authorization(self):
        with TemporaryDirectory() as directory:
            root = Path(directory); fixture = Fixture(root)
            pilot_path = root / "pilot.json"; pilot_sha = write_json(pilot_path, fixture.pilot)
            accepted_path = root / "accepted.json"; accepted_sha = write_json(accepted_path, fixture.accepted)
            manifest_path = root / "generation.json"
            write_json(manifest_path, fixture.manifest(pilot_path, pilot_sha, accepted_path, accepted_sha))
            patches = (
                mock.patch.object(runner, "MANIFEST_PATH", manifest_path),
                mock.patch.object(runner, "PILOT_PROMPTS_PATH", pilot_path),
                mock.patch.object(runner, "ACCEPTED_PATH", accepted_path),
                mock.patch.object(runner, "EXPECTED_PILOT_SHA256", pilot_sha),
                mock.patch.object(runner, "EXPECTED_ACCEPTED_SHA256", accepted_sha),
                mock.patch.object(runner, "DEFAULT_RUN_DIR", fixture.run_dir),
            )
            for patch in patches: patch.start()
            try:
                values = runner.load_inputs()
                self.assertEqual(values[5], pilot_sha)
                pilot_path.write_text(pilot_path.read_text() + " ")
                with self.assertRaisesRegex(ValueError, "Immutable pilot prompt bytes differ"):
                    runner.load_inputs()
            finally:
                for patch in reversed(patches): patch.stop()

    def test_render_byte_drift_is_rejected(self):
        with TemporaryDirectory() as directory:
            fixture = Fixture(Path(directory)); render = runner.normalized_render(fixture.renders[0])
            runner.validate_render(render)
            Path(render["path"]).write_bytes(Path(render["path"]).read_bytes() + b"drift")
            with self.assertRaisesRegex(ValueError, "Render bytes differ"):
                runner.validate_render(render)

    def test_smoke_progress_keeps_full_120_row_resume_scope(self):
        with TemporaryDirectory() as directory:
            fixture = Fixture(Path(directory)); rows = runner.build_rows({"renders": fixture.renders}, fixture.accepted, fixture.pilot)
            summary = runner.write_progress(
                fixture.run_dir, {"scope": {"expected_images": 120}}, "m" * 64,
                fixture.accepted, "a" * 64, fixture.pilot, "p" * 64, rows, rows[:4],
            )
            self.assertEqual(summary["selected_generation_row_count"], 120)
            self.assertEqual(summary["invocation_generation_row_count"], 4)
            self.assertEqual(summary["selected_missing_record_count"], 120)
            self.assertEqual(summary["invocation_missing_record_count"], 4)

            for row in rows[:4]:
                runner.atomic_write_json(
                    runner.record_path(fixture.run_dir, row["row_id"]),
                    {"row_id": row["row_id"], "status": "done"},
                )
            summary = runner.write_progress(
                fixture.run_dir, {"scope": {"expected_images": 120}}, "m" * 64,
                fixture.accepted, "a" * 64, fixture.pilot, "p" * 64, rows, rows[:4],
            )
            self.assertEqual(summary["selected_missing_record_count"], 116)
            self.assertEqual(summary["invocation_missing_record_count"], 0)
            self.assertEqual(summary["invocation_record_status_counts"], {"done": 4})

    def test_submit_timeout_is_ambiguous_and_never_retried(self):
        class Client:
            def __init__(self, *args, **kwargs): pass
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def post(self, *args, **kwargs):
                raise httpx.ReadTimeout("unknown", request=httpx.Request("POST", runner.GENERATE_URL))
        row = {field: field for field in runner.ROW_IDENTITY_FIELDS}
        with TemporaryDirectory() as directory, mock.patch.object(runner.httpx, "Client", Client):
            job = runner.submit_job(Path(directory), row, {"prompt": "x"}, {"hash": "y"})
        self.assertEqual(job["status"], "submission_ambiguous")
        self.assertEqual(len(job["submission_attempts"]), 1)

    def test_submit_http_5xx_without_job_identity_is_ambiguous_and_never_retried(self):
        class Client:
            calls = 0

            def __init__(self, *args, **kwargs): pass
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def post(self, *args, **kwargs):
                type(self).calls += 1
                return httpx.Response(
                    503,
                    json={"error": "upstream unavailable"},
                    request=httpx.Request("POST", runner.GENERATE_URL),
                )

        row = {field: field for field in runner.ROW_IDENTITY_FIELDS}
        with TemporaryDirectory() as directory, mock.patch.object(runner.httpx, "Client", Client):
            run_dir = Path(directory)
            job = runner.submit_job(run_dir, row, {"prompt": "x"}, {"hash": "y"})
            durable = runner.read_json(runner.job_path(run_dir, row["row_id"]))
        self.assertEqual(Client.calls, 1)
        self.assertEqual(job["status"], "submission_ambiguous")
        self.assertEqual(len(job["submission_attempts"]), 1)
        self.assertEqual(durable["submission_response"], {"error": "upstream unavailable"})

    def test_completed_response_raw_prompt_mismatch_is_terminal_without_download(self):
        row = {field: field for field in runner.ROW_IDENTITY_FIELDS}
        row.update({"render": {}, "candidate": {"text": "frozen"}, "accepted_case": {}})
        payload = {"prompt": "frozen", "size": {"width": 2560, "height": 1440}}
        response = {
            "outputs": [{"image": {"presignedUrl": "https://example.invalid/output.png"}}],
            "debugData": {"rawPrompt": "different", "usedPrompt": "rewritten"},
        }
        job = {
            **{field: row[field] for field in runner.ROW_IDENTITY_FIELDS},
            "status": "completed_response_ready",
            "request_payload": payload,
            "provenance": {"hash": "y"},
            "_transient_final_response": response,
        }
        with TemporaryDirectory() as directory, mock.patch.object(
            runner, "download_generated", side_effect=AssertionError("must not download")
        ):
            run_dir = Path(directory)
            record = runner.materialize_record(
                run_dir, row, payload, {"hash": "y"}, {"blob_id": "blob"}, job
            )
            durable_job = runner.read_json(runner.job_path(run_dir, row["row_id"]))
            raw = runner.read_json(Path(record["raw_response_path"]))
            resumed = runner.materialize_record(
                run_dir, row, payload, {"hash": "y"}, {"blob_id": "blob"}, durable_job
            )
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["failure_class"], "completed_response_raw_prompt_mismatch")
        self.assertEqual(durable_job["status"], "integrity_failed_terminal")
        self.assertEqual(raw["debugData"]["rawPrompt"], "different")
        self.assertEqual(resumed, record)

    def test_completed_response_missing_raw_prompt_is_terminal(self):
        row = {field: field for field in runner.ROW_IDENTITY_FIELDS}
        row.update({"render": {}, "candidate": {"text": "frozen"}, "accepted_case": {}})
        payload = {"prompt": "frozen", "size": {"width": 2560, "height": 1440}}
        job = {
            **{field: row[field] for field in runner.ROW_IDENTITY_FIELDS},
            "status": "completed_response_ready",
            "request_payload": payload,
            "provenance": {"hash": "y"},
            "_transient_final_response": {"debugData": {"usedPrompt": "rewritten"}},
        }
        with TemporaryDirectory() as directory:
            record = runner.materialize_record(
                Path(directory), row, payload, {"hash": "y"}, {"blob_id": "blob"}, job
            )
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["failure_class"], "completed_response_raw_prompt_missing")


if __name__ == "__main__":
    unittest.main()
