#!/usr/bin/env python3
"""Offline regressions for the isolated lived-in-V4 image runner."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import httpx
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_generation as runner


def write_json(path: Path, value: object) -> str:
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


class ContractFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.sources = []
        for index in range(9):
            device_type = "laptop" if index < 3 else "printer"
            path = root / f"source_{index}.json"
            sha = write_json(path, {"source": index, "device_type": device_type})
            self.sources.append(
                {
                    "source_id": f"source{index}",
                    "device_type": device_type,
                    "source_json_path": str(path),
                    "sha256": sha,
                    "bytes": path.stat().st_size,
                }
            )

        self.renders = []
        for device_type, camera, tag in (
            ("laptop", "Front_Right_CloseUp", "laptop_FrontRightCloseUp"),
            ("laptop", "Front_Right_Wide", "laptop_FrontRightWide"),
            ("printer", "Front_Right_CloseUp", "printer_FrontRightCloseUp"),
            ("printer", "Front_Right_Wide", "printer_FrontRightWide"),
        ):
            render_id = f"{device_type}_{'close' if 'CloseUp' in camera else 'wide'}"
            path = root / f"{render_id}.png"
            Image.new("RGBA", (1024, 576), (100, 120, 140, 255)).save(path)
            self.renders.append(
                {
                    "render_id": render_id,
                    "device_type": device_type,
                    "camera_tag": tag,
                    "source_camera_name": camera,
                    "product_provenance": f"approved-{device_type}",
                    "path": str(path),
                    "sha256": runner.sha256_path(path),
                    "bytes": path.stat().st_size,
                    "width": 1024,
                    "height": 576,
                    "output_width": 2560,
                    "output_height": 1440,
                    "preserve_aspect_ratio": True,
                }
            )

        render_by_tag = {value["camera_tag"]: value for value in self.renders}
        self.cases = []
        self.accepted_cases = {}
        self.selections = []
        selected_ranks = (1, 2, 11, 12, 21, 22)
        for source in self.sources:
            for framing in ("CloseUp", "Wide"):
                tag = f"{source['device_type']}_FrontRight{framing}"
                case_id = f"{source['source_id']}__{tag}"
                group_id = f"{source['source_id']}__{source['device_type']}_FrontRight"
                render_id = render_by_tag[tag]["render_id"]
                input_path = root / f"{case_id}_input.json"
                input_sha = write_json(input_path, {"source_messaging": {}, "camera_tag": tag})
                self.cases.append(
                    {
                        "case_id": case_id,
                        "group_id": group_id,
                        "source_id": source["source_id"],
                        "device_type": source["device_type"],
                        "camera_tag": tag,
                        "view_role": "close_up" if framing == "CloseUp" else "wide",
                        "input_path": str(input_path),
                        "input_sha256": input_sha,
                        "render_id": render_id,
                    }
                )
                record_path = root / f"{case_id}_record.json"
                record_sha = write_json(record_path, {"case_id": case_id, "candidate_count": 30})
                candidates = []
                for rank in range(1, 31):
                    candidate_id = f"candidate_{rank:02d}"
                    text = f"Environment for {case_id}, ranked {rank}."
                    rank_bin = "1-10" if rank <= 10 else "11-20" if rank <= 20 else "21-30"
                    selection_stratum = (
                        "upper_rank_1_10" if rank <= 10
                        else "middle_rank_11_20" if rank <= 20
                        else "lower_rank_21_30"
                    )
                    candidate = {
                        "candidate_key": f"{case_id}::{candidate_id}",
                        "id": candidate_id,
                        "rank": rank,
                        "rank_bin": rank_bin,
                        "text": text,
                        "text_sha256": runner.sha256_bytes(text.encode()),
                        "environment": "Home",
                        "subsetting": "fixture",
                        "source_relevance_score": 80,
                        "relationship": "source_grounded",
                        "score_components": {"setting": 30, "activity": 30, "materials": 10, "use_context": 10},
                        "evidence_ids": [],
                        "explanation": "Fixture score.",
                        "creative_departures": [],
                        "visual_signature": {"surface": "desk", "light": "daylight", "local_props": [], "background_details": [], "people": []},
                        "camera_omissions": [],
                    }
                    candidates.append(candidate)
                    if rank not in selected_ranks:
                        continue
                    self.selections.append(
                        {
                            "selection_key": f"{case_id}::{candidate_id}::selected",
                            "candidate_key": candidate["candidate_key"],
                            "case_id": case_id,
                            "group_id": group_id,
                            "source_id": source["source_id"],
                            "device_type": source["device_type"],
                            "camera_tag": tag,
                            "view_role": "close_up" if framing == "CloseUp" else "wide",
                            "candidate_id": candidate_id,
                            "rank": rank,
                            "rank_bin": rank_bin,
                            "selection_stratum": selection_stratum,
                            "score_total": 80,
                            "selection_reason": "Deterministic fixture selection.",
                            "text": text,
                            "text_sha256": candidate["text_sha256"],
                            "render_id": render_id,
                            "render_path": render_by_tag[tag]["path"],
                            "render_sha256": render_by_tag[tag]["sha256"],
                            "input_sha256": input_sha,
                            "accepted_record_path": str(record_path),
                            "accepted_record_sha256": record_sha,
                            "semantic_review_status": "accepted",
                        }
                    )
                self.accepted_cases[case_id] = {
                    **self.cases[-1],
                    "record_path": str(record_path),
                    "record_sha256": record_sha,
                    "parsed_output_sha256": "a" * 64,
                    "status": "normalized_validator_passed_pending_human_review",
                    "candidates": candidates,
                    "debug": {},
                }

        self.manifest = {
            "version": "fixture-manifest-v1",
            "scope": {
                "source_count": 9,
                "case_count": 18,
                "candidates_per_case": 30,
                "render_count": 4,
                "image_generation_authorized": True,
            },
            "sources": self.sources,
            "renders": self.renders,
            "cases": self.cases,
        }

    def accepted(self, manifest_sha256: str) -> dict:
        return {
            "version": "fixture-accepted-v1",
            "status": "complete_human_review_required",
            "manifest_sha256": manifest_sha256,
            "counts": {"manifest_cases": 18, "accepted_cases": 18, "candidates": 540},
            "cases": self.accepted_cases,
        }

    def approve(self, accepted: dict) -> dict:
        accepted["status"] = "complete"
        for case in accepted["cases"].values():
            case["status"] = "normalized_validator_passed"
            case["human_review_status"] = "accepted"
            case["launchable"] = True
        return accepted

    def selection(self, manifest_sha256: str, accepted_sha256: str = "accepted-hash") -> dict:
        return {
            "version": "fixture-selection-v1",
            "status": "approved_for_image_generation",
            "manifest_sha256": manifest_sha256,
            "accepted_prompt_cases_sha256": accepted_sha256,
            "counts": {"accepted_banks": 18, "selected": 108},
            "selections": self.selections,
        }


class RunnerContractTests(unittest.TestCase):
    @staticmethod
    def minimal_row() -> dict:
        return {
            "row_id": "source__tag__candidate__render",
            "case_id": "source__tag",
            "group_id": "source__tag",
            "selection_key": "source__tag__candidate::selected",
            "source_id": "source",
            "render_id": "render",
            "candidate_id": "candidate",
            "device_type": "laptop",
            "camera_tag": "tag",
        }

    def test_exact_108_rows_one_render_per_group_and_two_per_stratum(self) -> None:
        with TemporaryDirectory() as directory:
            fixture = ContractFixture(Path(directory))
            accepted = fixture.accepted("manifest-hash")
            selection = fixture.selection("manifest-hash")
            rows = runner.build_rows(fixture.manifest, accepted, selection)
            self.assertEqual(len(rows), 108)
            by_case: dict[str, list[dict]] = {}
            for row in rows:
                by_case.setdefault(row["case_id"], []).append(row)
                expected = (
                    f"{row['source_id']}__{row['camera_tag']}__"
                    f"{row['candidate_id']}__{row['render_id']}"
                )
                self.assertEqual(row["row_id"], expected)
            self.assertEqual(set(map(len, by_case.values())), {6})
            self.assertTrue(all(len({row["render_id"] for row in values}) == 1 for values in by_case.values()))

    def test_rejects_cross_tag_reference_render(self) -> None:
        with TemporaryDirectory() as directory:
            fixture = ContractFixture(Path(directory))
            accepted = fixture.accepted("manifest-hash")
            selection = fixture.selection("manifest-hash")
            selection["selections"][0]["render_id"] = "laptop_wide"
            with self.assertRaisesRegex(ValueError, "differs from case for render_id"):
                runner.build_rows(fixture.manifest, accepted, selection)

    def test_rejects_rank_outside_declared_stratum(self) -> None:
        with TemporaryDirectory() as directory:
            fixture = ContractFixture(Path(directory))
            accepted = fixture.accepted("manifest-hash")
            selection = fixture.selection("manifest-hash")
            item = selection["selections"][0]
            item["rank"] = 30
            candidate = next(
                value for value in accepted["cases"][item["case_id"]]["candidates"]
                if value["candidate_key"] == item["candidate_key"]
            )
            rank_30_candidate = next(
                value for value in accepted["cases"][item["case_id"]]["candidates"]
                if value["rank"] == 30
            )
            rank_30_candidate["rank"] = candidate["rank"]
            candidate["rank"] = 30
            with self.assertRaisesRegex(ValueError, "Rank/bin mismatch"):
                runner.build_rows(fixture.manifest, accepted, selection)

    def test_rejects_candidate_text_hash_drift(self) -> None:
        with TemporaryDirectory() as directory:
            fixture = ContractFixture(Path(directory))
            accepted = fixture.accepted("manifest-hash")
            selection = fixture.selection("manifest-hash")
            item = selection["selections"][0]
            item["text"] += " changed"
            candidate = next(
                value for value in accepted["cases"][item["case_id"]]["candidates"]
                if value["candidate_key"] == item["candidate_key"]
            )
            candidate["text"] = item["text"]
            with self.assertRaisesRegex(ValueError, "Candidate text hash mismatch"):
                runner.build_rows(fixture.manifest, accepted, selection)

    def test_load_inputs_binds_selection_to_exact_manifest(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = ContractFixture(root)
            manifest_path = root / "manifest.json"
            manifest_sha = write_json(manifest_path, fixture.manifest)
            accepted_path = root / "accepted_prompt_cases.json"
            accepted_sha = write_json(accepted_path, fixture.accepted(manifest_sha))
            selection_path = root / "selection_manifest.json"
            write_json(selection_path, fixture.selection(manifest_sha, accepted_sha))
            old_manifest, old_accepted, old_selection = (
                runner.MANIFEST_PATH, runner.ACCEPTED_PATH, runner.SELECTION_PATH
            )
            try:
                runner.MANIFEST_PATH = manifest_path
                runner.ACCEPTED_PATH = accepted_path
                runner.SELECTION_PATH = selection_path
                manifest, actual_manifest_sha, accepted, _, selection, _ = runner.load_inputs()
            finally:
                runner.MANIFEST_PATH, runner.ACCEPTED_PATH, runner.SELECTION_PATH = (
                    old_manifest, old_accepted, old_selection
                )
            self.assertEqual(actual_manifest_sha, manifest_sha)
            self.assertEqual(manifest["scope"]["case_count"], 18)
            self.assertEqual(accepted["counts"]["candidates"], 540)
            self.assertEqual(selection["counts"]["selected"], 108)

    def test_fixed_payload_preserves_authorized_settings(self) -> None:
        row = {
            "candidate": {"text": "A bounded environment."},
            "render": {"output_width": 2560, "output_height": 1440},
        }
        self.assertEqual(
            runner.build_payload(row, "blob-id"),
            {
                "prompt": "A bounded environment.",
                "size": {"width": 2560, "height": 1440},
                "referenceBlobs": [{"id": "blob-id"}],
                "seeds": [42],
                "n": 1,
                "modelSpecificPayload": {
                    "enablePromptRewrite": True,
                    "rewriterModel": "gemini-3.1-pro",
                    "numInferenceSteps": 50,
                },
            },
        )

    def test_provenance_uses_final_raw_and_normalized_bank_hashes(self) -> None:
        row = {
            "selected_candidate_sha256": "selected",
            "selection_row_sha256": "selection",
            "selection": {
                "accepted_record_path": "/tmp/raw.json",
                "accepted_record_sha256": "raw-file",
            },
            "accepted_case": {
                "raw_parsed_output_sha256": "raw-semantic",
                "normalized_output_path": "/tmp/normalized.json",
                "normalized_output_file_sha256": "normalized-file",
                "normalized_output_semantic_sha256": "normalized-semantic",
                "normalization_log_path": "/tmp/normalization-log.json",
                "normalization_log_file_sha256": "normalization-log-file",
            },
            "candidate": {"text_sha256": "text"},
            "case": {"input_sha256": "input"},
            "source": {"sha256": "source"},
        }
        value = runner.provenance(
            row,
            {"prompt": "x"},
            {"blob_id": "blob", "render_sha256": "render", "bytes": 1},
            "manifest",
            "accepted",
            "selection",
        )
        self.assertEqual(value["raw_parsed_output_sha256"], "raw-semantic")
        self.assertEqual(
            value["normalized_output_semantic_sha256"], "normalized-semantic"
        )
        self.assertNotIn("parsed_output_sha256", value)

    def test_launch_gate_requires_manifest_and_every_semantic_review(self) -> None:
        approved_case = {
            "status": "normalized_validator_passed",
            "human_review_status": "accepted",
            "launchable": True,
        }
        rows = [
            {
                "selection_key": "s1",
                "case_id": "case1",
                "selection": {"semantic_review_status": "accepted"},
                "accepted_case": dict(approved_case),
            }
            for _ in range(108)
        ]
        manifest = {"scope": {"image_generation_authorized": True}}
        selection = {"status": "approved_for_image_generation"}
        runner.require_launch_authorization(manifest, selection, rows)
        rows[0]["selection"]["semantic_review_status"] = "pending_root_review"
        with self.assertRaisesRegex(ValueError, "outside accepted semantic review"):
            runner.require_launch_authorization(manifest, selection, rows)
        rows[0]["selection"]["semantic_review_status"] = "accepted"
        manifest["scope"]["image_generation_authorized"] = False
        with self.assertRaisesRegex(ValueError, "does not authorize"):
            runner.require_launch_authorization(manifest, selection, rows)

    def test_launch_gate_requires_approved_accepted_bank(self) -> None:
        rows = [
            {
                "selection_key": "s1",
                "case_id": "case1",
                "selection": {"semantic_review_status": "accepted"},
                "accepted_case": {
                    "status": "normalized_validator_passed",
                    "human_review_status": "accepted",
                    "launchable": True,
                },
            }
            for _ in range(108)
        ]
        rows[0]["accepted_case"]["launchable"] = False
        with self.assertRaisesRegex(ValueError, "outside launch approval"):
            runner.require_launch_authorization(
                {"scope": {"image_generation_authorized": True}},
                {"status": "approved_for_image_generation"},
                rows,
            )

    def test_all_approved_renders_preserve_exact_16_by_9(self) -> None:
        self.assertEqual(runner.exact_ratio_dimensions(1024, 576), (2560, 1440))
        self.assertEqual(1024 * 1440, 576 * 2560)

    def test_v4_paths_are_isolated_from_v2_and_publisher_content(self) -> None:
        self.assertIn("hp_lifestyle_lived_in_v4_eval_20261026", str(runner.EVAL_ROOT))
        self.assertIn("hp_lifestyle_lived_in_v4_eval_20261026", str(runner.DEFAULT_RUN_DIR))
        self.assertNotIn("hp_lifestyle_camera_v2_eval_20261022", str(runner.DEFAULT_RUN_DIR))
        self.assertNotIn("/gallery/", str(runner.DEFAULT_RUN_DIR))
        self.assertNotIn("/publication/", str(runner.DEFAULT_RUN_DIR))

    def test_submit_timeout_is_held_without_retry(self) -> None:
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

        with TemporaryDirectory() as directory, mock.patch.object(runner.httpx, "Client", Client):
            job = runner.submit_job(
                Path(directory), self.minimal_row(), {"prompt": "x"}, {"hash": "y"}
            )
        self.assertEqual(job["status"], "submission_ambiguous")
        self.assertEqual(job["failure_class"], "submit_timeout_ambiguous_held_no_retry")
        self.assertEqual(len(job["submission_attempts"]), 1)

    def test_existing_ambiguous_or_terminal_job_is_never_resubmitted(self) -> None:
        row = self.minimal_row()
        payload = {"prompt": "x"}
        provenance = {"hash": "y"}
        for status in ("submission_ambiguous", "failed_terminal"):
            with self.subTest(status=status), TemporaryDirectory() as directory:
                run_dir = Path(directory)
                path = runner.job_path(run_dir, row["row_id"])
                path.parent.mkdir(parents=True)
                write_json(
                    path,
                    {
                        **row,
                        "status": status,
                        "request_payload": payload,
                        "provenance": provenance,
                    },
                )
                with mock.patch.object(runner.httpx, "Client") as client:
                    job = runner.submit_job(run_dir, row, payload, provenance)
                self.assertEqual(job["status"], status)
                client.assert_not_called()

    def test_endpoint_artifact_sanitizer_removes_credentials(self) -> None:
        value = {
            "presignedUrl": "https://example/x?X-Amz-Signature=secret",
            "authorization": "Bearer secret",
            "debugData": {"usedPrompt": "safe"},
        }
        self.assertEqual(
            runner.sanitize_endpoint_value(value),
            {"debugData": {"usedPrompt": "safe"}},
        )


if __name__ == "__main__":
    unittest.main()

