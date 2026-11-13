#!/usr/bin/env python3
"""Offline regression checks for the camera-V2 endpoint runner."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import httpx

import run_generation as runner


class RunnerTests(unittest.TestCase):
    @staticmethod
    def minimal_row() -> dict:
        return {
            "row_id": "case__render__p1",
            "case_id": "case",
            "source_id": "source",
            "render_id": "render",
            "prompt_id": "p1",
        }

    def test_regular_reference_uses_exact_16_by_9_output(self) -> None:
        self.assertEqual(runner.exact_ratio_dimensions(1024, 576), (2560, 1440))
        self.assertEqual(1024 * 1440, 576 * 2560)

    def test_nonstandard_ratio_stays_exact_and_multiple_of_16(self) -> None:
        width, height = runner.exact_ratio_dimensions(800, 600)
        self.assertEqual(width * 600, height * 800)
        self.assertEqual(width % 16, 0)
        self.assertEqual(height % 16, 0)

    def test_payload_has_all_fixed_endpoint_settings(self) -> None:
        row = {
            "prompt": {"text": "A test environment"},
            "render": {"output_width": 2560, "output_height": 1440},
        }
        payload = runner.build_payload(row, "blob-123")
        self.assertEqual(payload["size"], {"width": 2560, "height": 1440})
        self.assertEqual(payload["referenceBlobs"], [{"id": "blob-123"}])
        self.assertEqual(payload["seeds"], [42])
        self.assertEqual(payload["n"], 1)
        self.assertEqual(
            payload["modelSpecificPayload"],
            {
                "enablePromptRewrite": True,
                "rewriterModel": "gemini-3.1-pro",
                "numInferenceSteps": 50,
            },
        )

    def test_endpoint_artifact_sanitizer_removes_urls_and_auth(self) -> None:
        value = {
            "presignedUrl": "https://example.test/x?X-Amz-Signature=secret",
            "authorization": "Bearer secret",
            "debugData": {"usedPrompt": "safe"},
            "nested": ["https://example.test/x?X-Amz-Credential=secret"],
        }
        self.assertEqual(
            runner.sanitize_endpoint_value(value),
            {
                "debugData": {"usedPrompt": "safe"},
                "nested": ["[redacted_presigned_url]"],
            },
        )

    def test_binding_hash_ignores_upload_response_transport_fields(self) -> None:
        binding = {field: f"value-{field}" for field in runner.BINDING_PROVENANCE_FIELDS}
        left = runner.canonical_sha256(runner.stable_binding(binding))
        binding["upload_response"] = {"presignedUrl": "secret"}
        right = runner.canonical_sha256(runner.stable_binding(binding))
        self.assertEqual(left, right)

    def test_safe_no_job_responses_retry_three_times_with_journal(self) -> None:
        class Response:
            def __init__(self, status: int, body: dict) -> None:
                self.status_code = status
                self._body = body
                self.headers = {}
                self.text = str(body)

            def json(self) -> dict:
                return self._body

        responses = iter(
            [
                Response(500, {"error_code": "provider_error"}),
                Response(429, {"error_code": "throttled"}),
                Response(
                    202,
                    {
                        "job_id": "job-123",
                        "links": {"result": {"href": "/jobs/result/job-123"}},
                    },
                ),
            ]
        )

        class Client:
            def __init__(self, *args, **kwargs) -> None:
                pass

            def __enter__(self):
                return self

            def __exit__(self, *args) -> None:
                pass

            def post(self, *args, **kwargs):
                return next(responses)

        with TemporaryDirectory() as directory, mock.patch.object(
            runner.httpx, "Client", Client
        ), mock.patch.object(runner.time, "sleep"):
            job = runner.submit_job(
                Path(directory), self.minimal_row(), {"prompt": "x"}, {"hash": "y"}
            )
            self.assertEqual(job["status"], "submitted")
            self.assertEqual(job["job_id"], "job-123")
            self.assertEqual(len(job["submission_attempts"]), 3)
            self.assertEqual(
                [item["status"] for item in job["submission_attempts"]],
                ["confirmed_no_job_http_500", "confirmed_no_job_http_429", "response_received"],
            )

    def test_ambiguous_submit_timeout_is_held_without_retry(self) -> None:
        class Client:
            def __init__(self, *args, **kwargs) -> None:
                pass

            def __enter__(self):
                return self

            def __exit__(self, *args) -> None:
                pass

            def post(self, *args, **kwargs):
                raise httpx.ReadTimeout(
                    "unknown submit outcome",
                    request=httpx.Request("POST", runner.GENERATE_URL),
                )

        with TemporaryDirectory() as directory, mock.patch.object(
            runner.httpx, "Client", Client
        ):
            job = runner.submit_job(
                Path(directory), self.minimal_row(), {"prompt": "x"}, {"hash": "y"}
            )
            self.assertEqual(job["status"], "submission_ambiguous")
            self.assertEqual(job["failure_class"], "submit_timeout_ambiguous_held_no_retry")
            self.assertEqual(len(job["submission_attempts"]), 1)

    def test_total_latency_uses_durable_submit_timestamp(self) -> None:
        self.assertEqual(
            runner.total_latency_ms(
                {"submission_started_at_utc": "2026-10-23T01:00:00+00:00"},
                "2026-10-23T01:02:03.500000+00:00",
            ),
            123500.0,
        )

    def test_current_manifest_has_only_expected_source_images(self) -> None:
        manifest, _, accepted, _ = runner.load_inputs()
        self.assertEqual(len(manifest["renders"]), 202)
        self.assertEqual(
            {render["device_type"] for render in manifest["renders"]},
            {"laptop", "printer"},
        )
        self.assertTrue(
            all(
                (render["width"], render["height"], render["output_width"], render["output_height"])
                == (1024, 576, 2560, 1440)
                for render in manifest["renders"]
            )
        )
        self.assertEqual(accepted["manifest_sha256"], runner.sha256_path(runner.MANIFEST_PATH))


if __name__ == "__main__":
    unittest.main()
