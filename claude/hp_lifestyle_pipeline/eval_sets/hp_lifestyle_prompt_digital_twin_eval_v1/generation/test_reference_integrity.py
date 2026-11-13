#!/usr/bin/env python3
"""Local regressions for reference upload, smoke import, and resume provenance."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).with_name("run_generation.py")
SPEC = importlib.util.spec_from_file_location("hp_run_generation", MODULE_PATH)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class ReferenceIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.twin_dir = self.root / "twins"
        self.run_dir = self.root / "run"
        self.twin_dir.mkdir()
        self.run_dir.mkdir()

        self.bytes_a = b"verified laptop bytes"
        self.bytes_b = b"verified printer bytes"
        self.path_a = self.twin_dir / "00_twin-a.jpg"
        self.path_b = self.twin_dir / "01_twin-b.jpg"
        self.path_a.write_bytes(self.bytes_a)
        self.path_b.write_bytes(self.bytes_b)
        self.assets = [
            self._asset("twin-a", self.path_a.name, self.bytes_a),
            self._asset("twin-b", self.path_b.name, self.bytes_b),
        ]
        self.manifest_path = self.root / "first_column_manifest.json"
        self._write_manifest()
        self.data = {
            "twins": [dict(asset) for asset in self.assets],
            "prompts": [{"key": "prompt-1", "text": "A grounded office scene."}],
            "rows": [
                {
                    "row_id": "row-b",
                    "prompt_key": "prompt-1",
                    "twin_id": "twin-b",
                    "twin_file": "do-not-trust-row-filename.jpg",
                    "device_category": "Printer",
                }
            ],
        }
        self.patch_twin_dir = mock.patch.object(runner, "TWIN_DIR", self.twin_dir)
        self.patch_manifest = mock.patch.object(
            runner, "TWIN_MANIFEST", self.manifest_path
        )
        self.patch_twin_dir.start()
        self.patch_manifest.start()
        self.addCleanup(self.patch_twin_dir.stop)
        self.addCleanup(self.patch_manifest.stop)

    def _asset(self, twin_id: str, filename: str, content: bytes) -> dict[str, object]:
        return {
            "evalset_item_id": twin_id,
            "local_filename": filename,
            "bytes": len(content),
            "sha256": runner.sha256_bytes(content),
            "width": 2368,
            "height": 1776,
        }

    def _write_manifest(self) -> None:
        self.manifest_path.write_text(
            json.dumps({"assets": self.assets}, indent=2) + "\n", encoding="utf-8"
        )

    def _write_smoke_artifacts(self, blob_id: str = "blob-b") -> tuple[Path, Path, Path]:
        request_path = self.root / "smoke_request.json"
        response_path = self.root / "smoke_response.json"
        blob_path = self.root / "smoke_blob.json"
        request_path.write_text(
            json.dumps(
                {
                    "row_id": "row-b",
                    "payload": runner.build_payload(
                        self.data["prompts"][0]["text"], blob_id
                    ),
                }
            ),
            encoding="utf-8",
        )
        response_path.write_text(
            json.dumps(
                {
                    "outputs": [
                        {
                            "seed": 42,
                            "image": {
                                "id": "output-1",
                                "presignedUrl": "https://example.invalid/output.png",
                            },
                        }
                    ],
                    "debugData": {},
                }
            ),
            encoding="utf-8",
        )
        blob_path.write_text(
            json.dumps(
                {
                    "images": [{"id": blob_id}],
                    "upload_provenance": {
                        "twin_id": "twin-b",
                        "local_filename": self.path_b.name,
                        "source_path": str(self.path_b.resolve()),
                        "source_sha256": runner.sha256_bytes(self.bytes_b),
                        "source_bytes": len(self.bytes_b),
                        "width": 2368,
                        "height": 1776,
                        "source_manifest_sha256": runner.sha256_bytes(
                            self.manifest_path.read_bytes()
                        ),
                        "upload_endpoint": runner.UPLOAD_URL,
                    },
                }
            ),
            encoding="utf-8",
        )
        return request_path, response_path, blob_path

    def test_upload_hashes_the_exact_bytes_sent_and_reuses_verified_cache(self) -> None:
        with mock.patch.object(
            runner, "post_image", side_effect=[{"id": "blob-a"}, {"id": "blob-b"}]
        ) as post:
            mapping, manifest_sha256 = runner.upload_missing_twins(
                self.data, self.run_dir, workers=1
            )

        sent = [call.args[0] for call in post.call_args_list]
        self.assertEqual(sent, [self.bytes_a, self.bytes_b])
        self.assertEqual(mapping["twin-b"]["source_sha256"], self.assets[1]["sha256"])
        self.assertEqual(mapping["twin-b"]["source_bytes"], len(self.bytes_b))
        self.assertEqual(mapping["twin-b"]["source_manifest_sha256"], manifest_sha256)
        self.assertEqual(mapping["twin-b"]["upload_endpoint"], runner.UPLOAD_URL)

        with mock.patch.object(runner, "post_image") as post_again:
            cached, cached_manifest_sha256 = runner.upload_missing_twins(
                self.data, self.run_dir, workers=1
            )
        post_again.assert_not_called()
        self.assertEqual(cached, mapping)
        self.assertEqual(cached_manifest_sha256, manifest_sha256)

    def test_legacy_or_different_manifest_cache_is_rejected(self) -> None:
        legacy = {
            "twin-a": {"id": "legacy-blob", "local_filename": self.path_a.name}
        }
        (self.run_dir / "blob_ids.json").write_text(json.dumps(legacy), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "lacks provenance"):
            runner.upload_missing_twins(self.data, self.run_dir, workers=1)

        (self.run_dir / "blob_ids.json").unlink()
        with mock.patch.object(
            runner, "post_image", side_effect=[{"id": "blob-a"}, {"id": "blob-b"}]
        ):
            runner.upload_missing_twins(self.data, self.run_dir, workers=1)
        self.manifest_path.write_text(
            json.dumps({"assets": self.assets}, separators=(",", ":")), encoding="utf-8"
        )
        with self.assertRaisesRegex(ValueError, "source_manifest_sha256"):
            runner.upload_missing_twins(self.data, self.run_dir, workers=1)

    def test_smoke_import_rejects_wrong_source_file_for_row_twin(self) -> None:
        request_path, response_path, blob_path = self._write_smoke_artifacts()
        with self.assertRaisesRegex(ValueError, "does not match manifest identity twin-b"):
            runner.import_smoke(
                self.data,
                self.run_dir,
                request_path,
                response_path,
                blob_path,
                "twin-b",
                self.path_a,
                runner.sha256_bytes(self.bytes_a),
            )
        self.assertFalse((self.run_dir / "blob_ids.json").exists())

    def test_smoke_import_rejects_legacy_blob_response_without_provenance(self) -> None:
        request_path, response_path, blob_path = self._write_smoke_artifacts()
        blob_path.write_text(
            json.dumps({"images": [{"id": "blob-b"}]}), encoding="utf-8"
        )
        with self.assertRaisesRegex(ValueError, "lacks upload_provenance"):
            runner.import_smoke(
                self.data,
                self.run_dir,
                request_path,
                response_path,
                blob_path,
                "twin-b",
                self.path_b,
                runner.sha256_bytes(self.bytes_b),
            )

    def test_smoke_import_accepts_explicit_manifest_verified_source(self) -> None:
        request_path, response_path, blob_path = self._write_smoke_artifacts()
        downloaded = self.run_dir / "images" / "row-b.png"
        with mock.patch.object(runner, "download_output", return_value=downloaded):
            runner.import_smoke(
                self.data,
                self.run_dir,
                request_path,
                response_path,
                blob_path,
                "twin-b",
                self.path_b,
                runner.sha256_bytes(self.bytes_b),
            )
        mapping = json.loads((self.run_dir / "blob_ids.json").read_text())
        record = json.loads(
            (self.run_dir / "records" / "row-b.json").read_text()
        )
        self.assertEqual(mapping["twin-b"]["local_filename"], self.path_b.name)
        self.assertEqual(mapping["twin-b"]["source_sha256"], self.assets[1]["sha256"])
        self.assertEqual(
            record["provenance"]["reference_binding"]["twin_id"], "twin-b"
        )

    def test_completed_record_resume_requires_exact_provenance(self) -> None:
        with mock.patch.object(
            runner, "post_image", side_effect=[{"id": "blob-a"}, {"id": "blob-b"}]
        ):
            bindings, manifest_sha256 = runner.upload_missing_twins(
                self.data, self.run_dir, workers=1
            )
        row = self.data["rows"][0]
        prompt = self.data["prompts"][0]
        binding = bindings["twin-b"]
        payload = runner.build_payload(prompt["text"], binding["id"])
        record = {
            "row_id": row["row_id"],
            "prompt_key": row["prompt_key"],
            "twin_id": row["twin_id"],
            "status": "done",
            "request_payload": payload,
            "provenance": runner.generation_provenance(
                prompt["text"], payload, binding, manifest_sha256
            ),
        }
        runner.validate_completed_record(
            row, record, prompt, binding, manifest_sha256
        )

        no_provenance = copy.deepcopy(record)
        no_provenance.pop("provenance")
        with self.assertRaisesRegex(ValueError, "lacks provenance"):
            runner.validate_completed_record(
                row, no_provenance, prompt, binding, manifest_sha256
            )

        changed_payload_hash = copy.deepcopy(record)
        changed_payload_hash["provenance"]["request_payload_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "request_payload_sha256"):
            runner.validate_completed_record(
                row, changed_payload_hash, prompt, binding, manifest_sha256
            )

        changed_payload = copy.deepcopy(record)
        changed_payload["request_payload"]["prompt"] = "Different prompt."
        with self.assertRaisesRegex(ValueError, "request payload differs"):
            runner.validate_completed_record(
                row, changed_payload, prompt, binding, manifest_sha256
            )

        with self.assertRaisesRegex(ValueError, "reference_manifest_sha256"):
            runner.validate_completed_record(row, record, prompt, binding, "f" * 64)


if __name__ == "__main__":
    unittest.main()
