#!/usr/bin/env python3
"""Back up and replace the comparison viewer, preserving its URL."""

from __future__ import annotations

import base64
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import boto3
from botocore.exceptions import ClientError

HERE = Path(__file__).resolve().parent
BUILT = HERE / "built"
ORIGINAL = HERE / "source/viewer.original.html"
BUILD_MANIFEST = BUILT / "build_manifest.json"
VIEWER = BUILT / "viewer.html"
RESULTS = BUILT / "placement_judge_v3_results.json"
PUBLICATION = BUILT / "publication_manifest.json"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = (
    "hp-data-artifacts/hp-3p-gpt25/"
    "hp16-v6prompt-v156-vs-v164-vs-v166-vs-v166noguide-v2-e2e32-"
    "20261106T181903Z"
)
ALIAS_PREFIX = PREFIX + "-viewer"
REGION = "us-west-2"
GATEWAY = "https://foundry-aws-corp.adobe.io/asset"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def missing(error: ClientError) -> bool:
    return str(error.response.get("Error", {}).get("Code")) in {
        "404",
        "NoSuchKey",
        "NotFound",
    }


def get(client: Any, key: str) -> bytes:
    response = client.get_object(Bucket=BUCKET, Key=key)
    body = response["Body"]
    try:
        value = body.read()
    finally:
        body.close()
    require(len(value) == response["ContentLength"], f"truncated download: {key}")
    return value


def exists(client: Any, key: str) -> bool:
    try:
        client.head_object(Bucket=BUCKET, Key=key)
        return True
    except ClientError as error:
        if missing(error):
            return False
        raise


def put(client: Any, key: str, value: bytes, content_type: str) -> dict[str, Any]:
    digest = sha256_bytes(value)
    client.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=value,
        ContentType=content_type,
        ContentDisposition="inline",
        Metadata={"sha256": digest},
        ChecksumSHA256=base64.b64encode(hashlib.sha256(value).digest()).decode("ascii"),
    )
    head = client.head_object(Bucket=BUCKET, Key=key)
    downloaded = get(client, key)
    require(sha256_bytes(downloaded) == digest, f"remote hash differs: {key}")
    require(int(head["ContentLength"]) == len(value), f"remote length differs: {key}")
    require((head.get("Metadata") or {}).get("sha256") == digest, f"remote metadata differs: {key}")
    return {
        "key": key,
        "bytes": len(value),
        "sha256": digest,
        "content_type": content_type,
    }


def main() -> int:
    build = json.loads(BUILD_MANIFEST.read_text(encoding="utf-8"))
    require(build.get("status") == "validated_local_build_not_published", "local build is not publishable")
    require(build.get("judge_panels") == 128, "judge panel count differs")
    require(sha256(VIEWER) == build["viewer"]["sha256"], "viewer changed after build")
    require(sha256(RESULTS) == build["results"]["sha256"], "results changed after build")
    require(sha256(ORIGINAL) == build["original_viewer_sha256"], "original changed after build")

    client = boto3.client("s3", region_name=REGION)
    actual_key = f"{PREFIX}/viewer.html"
    alias_key = f"{ALIAS_PREFIX}/viewer.html"
    original_bytes = ORIGINAL.read_bytes()
    current = get(client, actual_key)
    require(sha256_bytes(current) == sha256_bytes(original_bytes), "live viewer changed since collection")
    backup_key = f"{PREFIX}/viewer.pre-natural-placement-v3.{sha256_bytes(original_bytes)}.html"
    if exists(client, backup_key):
        require(sha256_bytes(get(client, backup_key)) == sha256_bytes(original_bytes), "existing backup differs")
        backup = {
            "key": backup_key,
            "bytes": len(original_bytes),
            "sha256": sha256_bytes(original_bytes),
            "content_type": "text/html; charset=utf-8",
            "already_present": True,
        }
    else:
        backup = put(client, backup_key, original_bytes, "text/html; charset=utf-8")
        backup["already_present"] = False

    for key in (alias_key, f"{PREFIX}/placement_judge_v3_results.json"):
        require(not exists(client, key), f"refusing unexpected destination collision: {key}")

    uploaded = [
        put(client, f"{PREFIX}/placement_judge_v3_results.json", RESULTS.read_bytes(), "application/json"),
        put(client, actual_key, VIEWER.read_bytes(), "text/html; charset=utf-8"),
        put(client, alias_key, VIEWER.read_bytes(), "text/html; charset=utf-8"),
    ]
    require(sha256_bytes(get(client, actual_key)) == sha256_bytes(get(client, alias_key)), "viewer and alias differ")

    publication = {
        "schema_version": "placement-v3-in-place-publication-v1",
        "published_at_utc": datetime.now(timezone.utc).isoformat(),
        "bucket": BUCKET,
        "actual_prefix": PREFIX,
        "alias_prefix": ALIAS_PREFIX,
        "source_backup": backup,
        "uploads": uploaded,
        "viewer_url": f"{GATEWAY}/{BUCKET}/{actual_key}",
        "user_supplied_alias_url": f"{GATEWAY}/{BUCKET}/{alias_key}",
        "results_url": f"{GATEWAY}/{BUCKET}/{PREFIX}/placement_judge_v3_results.json",
        "verification": {
            "live_original_hash_matched_before_overwrite": True,
            "backup_download_hash_verified": True,
            "all_upload_download_hashes_verified": True,
            "actual_and_alias_viewer_bytes_identical": True,
            "original_report_restorable": True,
        },
    }
    PUBLICATION.write_text(json.dumps(publication, indent=2) + "\n", encoding="utf-8")
    publication_key = f"{PREFIX}/placement_judge_v3_publication.json"
    require(not exists(client, publication_key), f"refusing unexpected destination collision: {publication_key}")
    publication_object = put(
        client, publication_key, PUBLICATION.read_bytes(), "application/json"
    )
    print(json.dumps({**publication, "publication_object": publication_object}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
