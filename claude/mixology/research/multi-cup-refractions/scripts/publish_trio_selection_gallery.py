#!/usr/bin/env python3
"""Publish and byte-verify the standalone trio selection gallery without deletions."""

from __future__ import annotations

import hashlib
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path

import boto3


ROOT = Path("/home/colligo/mixology_data/refraction_research_2026-10-19/trio-two-stage-selection")
REVIEW = ROOT / "_review"
BUCKET = "foundry-tccc-enterprise-adobe-assets"
PREFIX = "mixology/refraction_research_2026-10-19/trio-two-stage-selection"
URL = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}/gallery/index.html"


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def content_type(path: Path) -> str:
    overrides = {
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".md": "text/markdown; charset=utf-8",
        ".txt": "text/plain; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".html": "text/html; charset=utf-8",
    }
    return overrides.get(path.suffix.lower()) or mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def local_files() -> list[Path]:
    return sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and "_review" not in path.relative_to(ROOT).parts
    )


def main() -> None:
    s3 = boto3.client("s3", region_name="us-west-2")
    existing = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX.rstrip("/") + "/")
    existing_keys = [item["Key"] for item in existing.get("Contents", [])]
    if existing_keys:
        raise RuntimeError(f"Refusing first publication into non-empty prefix ({len(existing_keys)} objects)")

    files = local_files()
    if not files:
        raise RuntimeError("No files selected for publication")
    uploaded: list[dict] = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        key = f"{PREFIX}/{relative}"
        payload = path.read_bytes()
        cache = (
            "no-cache, no-store, must-revalidate"
            if relative.startswith("gallery/")
            else "private, max-age=31536000, immutable"
        )
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=payload,
            ContentType=content_type(path),
            ContentDisposition="inline",
            CacheControl=cache,
        )
        uploaded.append(
            {
                "path": relative,
                "key": key,
                "bytes": len(payload),
                "sha256": digest_bytes(payload),
                "content_type": content_type(path),
            }
        )

    remote = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX.rstrip("/") + "/")
    remote_keys = {item["Key"] for item in remote.get("Contents", [])}
    expected_keys = {item["key"] for item in uploaded}
    if remote_keys != expected_keys:
        raise RuntimeError(
            f"Remote key mismatch: missing={sorted(expected_keys - remote_keys)}, "
            f"extra={sorted(remote_keys - expected_keys)}"
        )
    for item in uploaded:
        response = s3.get_object(Bucket=BUCKET, Key=item["key"])
        payload = response["Body"].read()
        if len(payload) != item["bytes"] or digest_bytes(payload) != item["sha256"]:
            raise RuntimeError(f"Remote byte mismatch: {item['key']}")
        if response["ContentType"] != item["content_type"]:
            raise RuntimeError(f"Remote MIME mismatch: {item['key']}: {response['ContentType']}")

    record = {
        "published_at": datetime.now(timezone.utc).isoformat(),
        "bucket": BUCKET,
        "prefix": PREFIX,
        "url": URL,
        "preexisting_objects": len(existing_keys),
        "published_objects": len(uploaded),
        "published_bytes": sum(item["bytes"] for item in uploaded),
        "remote_readback": "every object byte-for-byte SHA-256 verified",
        "objects": uploaded,
    }
    REVIEW.mkdir(parents=True, exist_ok=True)
    (REVIEW / "publication.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: record[key] for key in (
        "url", "preexisting_objects", "published_objects", "published_bytes", "remote_readback"
    )}, indent=2))


if __name__ == "__main__":
    main()
