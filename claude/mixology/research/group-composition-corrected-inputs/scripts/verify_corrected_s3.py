"""Authenticated full-package S3 byte readback after corrected-input publication."""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
from pathlib import Path

import boto3


RUN = Path("/home/colligo/mixology_data/refraction_research_2026-10-19")
BUCKET = "foundry-tccc-enterprise-adobe-assets"
PREFIX = "mixology/refraction_research_2026-10-19/"
BASELINE = RUN / "_review/corrected_composition_prepublication_2026-10-20/live_s3_manifest.json"


def main() -> None:
    client = boto3.client("s3", region_name="us-west-2")
    paginator = client.get_paginator("list_objects_v2")
    objects = []
    for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX):
        objects.extend(item for item in page.get("Contents", []) if not item["Key"].endswith("/"))
    expected_types = {
        "gallery/index.html": "text/html",
        "gallery/style.css": "text/css",
        "gallery/data.js": "application/javascript",
        "gallery/main.js": "application/javascript",
        "gallery/imsauth.js": "application/javascript",
    }

    def check(item: dict) -> dict:
        relative = item["Key"][len(PREFIX):]
        local = RUN / relative
        if not local.is_file():
            raise AssertionError(f"Live S3 object missing locally: {relative}")
        response = client.get_object(Bucket=BUCKET, Key=item["Key"])
        payload = response["Body"].read()
        remote_hash = hashlib.sha256(payload).hexdigest()
        local_hash = hashlib.sha256(local.read_bytes()).hexdigest()
        if remote_hash != local_hash:
            raise AssertionError(f"S3 byte mismatch: {relative}")
        content_type = response["ContentType"].split(";")[0]
        if relative in expected_types and content_type != expected_types[relative]:
            raise AssertionError((relative, content_type, expected_types[relative]))
        return {
            "path": relative,
            "bytes": len(payload),
            "sha256": remote_hash,
            "content_type": response["ContentType"],
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        files = list(pool.map(check, objects))
    by_path = {item["path"]: item for item in files}
    baseline = json.loads(BASELINE.read_text())
    old_outputs = [item for item in baseline["files"] if item["path"].endswith("/output.png")]
    assert len(old_outputs) == 35
    for item in old_outputs:
        assert by_path[item["path"]]["sha256"] == item["sha256"]
    new_outputs = [
        item for item in files
        if item["path"].startswith("composition-corrected-inputs/runs/")
        and item["path"].endswith("/output.png")
    ]
    assert len(new_outputs) == 9
    result = {
        "verified_at": "2026-10-20",
        "bucket": BUCKET,
        "prefix": PREFIX.removesuffix("/"),
        "all_s3_objects_match_local_bytes": True,
        "file_count": len(files),
        "total_bytes": sum(item["bytes"] for item in files),
        "preexisting_output_hashes_preserved": len(old_outputs),
        "corrected_outputs_verified": len(new_outputs),
        "gallery_mime_types": "pass",
        "authentication": "Authenticated AWS S3 object readback; live signed-in browser session not exercised.",
        "files": sorted(files, key=lambda item: item["path"]),
    }
    destination = RUN / "_review/corrected_composition_s3_verification.json"
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "files"}))


if __name__ == "__main__":
    main()
