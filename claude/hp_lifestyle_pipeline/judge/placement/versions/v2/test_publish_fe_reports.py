from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import publish_fe_reports as publisher


class FakeS3:
    def __init__(self) -> None:
        self.objects: dict[tuple[str, str], dict[str, object]] = {}

    def put_object(self, **kwargs):
        self.objects[(kwargs["Bucket"], kwargs["Key"])] = {
            "body": bytes(kwargs["Body"]),
            "content_type": kwargs["ContentType"],
            "metadata": dict(kwargs["Metadata"]),
            "checksum": kwargs["ChecksumSHA256"],
        }
        return {}

    def head_object(self, **kwargs):
        item = self.objects[(kwargs["Bucket"], kwargs["Key"])]
        return {
            "ContentLength": len(item["body"]),
            "ContentType": item["content_type"],
            "Metadata": item["metadata"],
        }

    def get_object(self, **kwargs):
        item = self.objects[(kwargs["Bucket"], kwargs["Key"])]
        return {"Body": io.BytesIO(item["body"])}


class CorruptDownloadS3(FakeS3):
    def get_object(self, **kwargs):
        return {"Body": io.BytesIO(b"corrupt")}


class PublishFeReportsTests(unittest.TestCase):
    def _fixture(self, root: Path) -> None:
        for name in publisher.REPORT_NAMES:
            report = root / name
            report.mkdir(parents=True)
            (report / "data.json").write_text(
                json.dumps(
                    {
                        "is_secure": True,
                        "meta_texts": [f"Report {name}"],
                        "rows": [{"meta_data": {}, "images": []}],
                    }
                ),
                encoding="utf-8",
            )
            (report / "viewer.html").write_text(
                "<!doctype html><title>viewer</title>", encoding="utf-8"
            )

    def test_plan_stages_four_reports_and_artifact_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._fixture(root)
            artifact_path = root / "method.md"
            artifact_path.write_text("method", encoding="utf-8")
            uploads, urls = publisher.build_upload_plan(
                source_root=root,
                bucket="test-bucket",
                prefix="test/prefix",
                artifacts=[publisher.Artifact("Method", artifact_path)],
            )
            self.assertEqual(len(uploads), 9)
            self.assertEqual(set(urls), set(publisher.REPORT_NAMES))
            combined = next(
                upload for upload in uploads if upload.key.endswith("combined/data.json")
            )
            staged = json.loads(combined.body)
            self.assertEqual(
                staged["links"],
                [
                    {
                        "label": "Method",
                        "url": (
                            "https://foundry-aws-corp.adobe.io/asset/"
                            "test-bucket/test/prefix/artifacts/method.md"
                        ),
                    }
                ],
            )
            self.assertEqual(combined.content_type, "application/json")
            self.assertEqual(
                next(upload for upload in uploads if upload.key.endswith("viewer.html")).content_type,
                "text/html; charset=utf-8",
            )

    def test_upload_is_verified_by_downloaded_sha(self) -> None:
        client = FakeS3()
        upload = publisher.UploadObject(
            key="prefix/data.json",
            body=b'{"ok":true}\n',
            content_type="application/json",
            source="fixture",
        )
        verified = publisher.upload_and_verify(client, "test-bucket", upload)
        self.assertEqual(verified["sha256"], upload.sha256)
        self.assertEqual(verified["bytes"], len(upload.body))
        stored = client.objects[("test-bucket", "prefix/data.json")]
        self.assertEqual(stored["metadata"], {"sha256": upload.sha256})

    def test_upload_rejects_downloaded_sha_mismatch(self) -> None:
        client = CorruptDownloadS3()
        upload = publisher.UploadObject(
            key="prefix/data.json",
            body=b'{"ok":true}\n',
            content_type="application/json",
            source="fixture",
        )
        with self.assertRaisesRegex(RuntimeError, "byte SHA-256 verification failed"):
            publisher.upload_and_verify(client, "test-bucket", upload)

    def test_plan_rejects_missing_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._fixture(root)
            (root / "printers" / "viewer.html").unlink()
            with self.assertRaisesRegex(ValueError, "Incomplete report printers"):
                publisher.build_upload_plan(
                    source_root=root,
                    bucket="test-bucket",
                    prefix="test/prefix",
                    artifacts=[],
                )


if __name__ == "__main__":
    unittest.main()
