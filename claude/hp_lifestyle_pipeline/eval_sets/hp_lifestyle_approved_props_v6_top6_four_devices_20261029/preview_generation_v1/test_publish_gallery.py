"""Offline unit tests for the V6 S3 gallery publisher."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import publish_gallery


class FakeS3Client:
    def __init__(self, bad_sha: bool = False) -> None:
        self.bad_sha = bad_sha
        self.uploads: list[dict] = []
        self.objects: dict[tuple[str, str], dict] = {}

    def upload_file(self, path: str, bucket: str, key: str, ExtraArgs: dict) -> None:
        raw = Path(path).read_bytes()
        self.uploads.append(
            {"path": path, "bucket": bucket, "key": key, "extra": ExtraArgs}
        )
        metadata = dict(ExtraArgs["Metadata"])
        if self.bad_sha:
            metadata["sha256"] = "0" * 64
        self.objects[(bucket, key)] = {
            "ContentLength": len(raw),
            "Metadata": metadata,
            "ContentType": ExtraArgs["ContentType"],
            "CacheControl": ExtraArgs["CacheControl"],
        }

    def head_object(self, Bucket: str, Key: str) -> dict:
        return self.objects[(Bucket, Key)]


class V6PublishGalleryTest(unittest.TestCase):
    def make_artifacts(self, root: Path) -> dict[str, dict]:
        values = {
            "gallery/index.html": b"<html>index</html>\n",
            "gallery/data.js": b"const GENERATION_DATA = {};\n",
            "assets/corrected_inputs/reference.png": b"png bytes",
        }
        artifacts = {}
        for relative, raw in values.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            artifacts[relative] = {
                "bytes": len(raw),
                "sha256": publish_gallery.sha256_path(path),
            }
        return artifacts

    def test_publish_builds_validates_uploads_index_last_and_writes_sanitized_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary).resolve()
            artifacts = self.make_artifacts(run_dir)
            build_record = {
                "version": "test-build",
                "mode": "progressive",
                "artifacts": artifacts,
            }
            validation = {"validated": True, "mode": "progressive", "row_count": 96}
            manifest = {
                "run_dir": str(run_dir),
                "s3": {
                    "bucket": publish_gallery.EXPECTED_BUCKET,
                    "prefix": publish_gallery.EXPECTED_PREFIX,
                },
            }
            client = FakeS3Client()
            publication_path = run_dir / "publication.json"
            with (
                mock.patch.object(publish_gallery, "DEFAULT_RUN_DIR", run_dir),
                mock.patch.object(publish_gallery, "build", return_value=build_record) as build_mock,
                mock.patch.object(publish_gallery, "validate", return_value=validation) as validate_mock,
                mock.patch.object(publish_gallery, "read_json", return_value=manifest),
            ):
                record = publish_gallery.publish(
                    run_dir,
                    final=False,
                    s3_client=client,
                    publication_path=publication_path,
                )
            build_mock.assert_called_once_with(run_dir, False)
            validate_mock.assert_called_once_with(run_dir, False)
            self.assertEqual(client.uploads[-1]["key"], f"{publish_gallery.EXPECTED_PREFIX}/gallery/index.html")
            self.assertEqual(
                client.uploads[-1]["extra"]["CacheControl"],
                publish_gallery.GALLERY_CACHE_CONTROL,
            )
            image_upload = next(item for item in client.uploads if item["key"].endswith("reference.png"))
            self.assertEqual(image_upload["extra"]["ContentType"], "image/png")
            self.assertEqual(
                image_upload["extra"]["CacheControl"],
                publish_gallery.IMMUTABLE_CACHE_CONTROL,
            )
            self.assertTrue(record["gallery_index_uploaded_last"])
            self.assertTrue(record["remote_bytes_and_sha_metadata_verified"])
            self.assertFalse(record["credentials_persisted"])
            stored = json.loads(publication_path.read_text(encoding="utf-8"))
            self.assertEqual(stored["uploaded_object_count"], 3)
            publish_gallery.assert_sanitized(stored, "test_publication")

    def test_remote_sha_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifacts = self.make_artifacts(root)
            item = publish_gallery.artifact_plan(
                root, artifacts, publish_gallery.EXPECTED_PREFIX
            )[0]
            with self.assertRaisesRegex(ValueError, "Published SHA metadata differs"):
                publish_gallery.upload_verified(
                    FakeS3Client(bad_sha=True), publish_gallery.EXPECTED_BUCKET, item
                )

    def test_manifest_destination_drift_is_rejected_without_upload(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary).resolve()
            client = FakeS3Client()
            build_record = {
                "mode": "progressive",
                "artifacts": self.make_artifacts(run_dir),
            }
            validation = {"validated": True, "mode": "progressive"}
            drifted_manifest = {
                "run_dir": str(run_dir),
                "s3": {
                    "bucket": publish_gallery.EXPECTED_BUCKET,
                    "prefix": "eval_sets/wrong-prefix",
                },
            }
            with (
                mock.patch.object(publish_gallery, "DEFAULT_RUN_DIR", run_dir),
                mock.patch.object(publish_gallery, "build", return_value=build_record),
                mock.patch.object(publish_gallery, "validate", return_value=validation),
                mock.patch.object(publish_gallery, "read_json", return_value=drifted_manifest),
            ):
                with self.assertRaisesRegex(ValueError, "isolated preview prefix"):
                    publish_gallery.publish(run_dir, s3_client=client)
            self.assertEqual(client.uploads, [])

    def test_local_drift_is_rejected_before_upload(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifacts = self.make_artifacts(root)
            (root / "gallery/data.js").write_text("changed", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "changed after gallery build"):
                publish_gallery.artifact_plan(
                    root, artifacts, publish_gallery.EXPECTED_PREFIX
                )


if __name__ == "__main__":
    unittest.main()
