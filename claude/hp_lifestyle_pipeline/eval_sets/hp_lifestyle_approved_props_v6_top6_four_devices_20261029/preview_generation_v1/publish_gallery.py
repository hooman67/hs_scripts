#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "httpx", "pillow"]
# ///
"""Build, validate, and publish the V6 gallery to its isolated S3 prefix."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import mimetypes
from pathlib import Path
from typing import Any

import boto3

from build_gallery import (
    DEFAULT_RUN_DIR,
    MANIFEST_PATH,
    assert_sanitized,
    atomic_json,
    build,
    read_json,
    sha256_path,
)
from validate_gallery import validate


HERE = Path(__file__).resolve().parent
PUBLICATION_PATH = HERE / "publication.json"
PUBLIC_BASE = "https://foundry-aws-corp.adobe.io/asset"
AWS_REGION = "us-west-2"
EXPECTED_BUCKET = "foundry-hp-enterprise-adobe-assets"
EXPECTED_PREFIX = (
    "eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/"
    "generated_preview_v1"
)
INDEX_RELATIVE_PATH = "gallery/index.html"
GALLERY_CACHE_CONTROL = "no-cache, no-store, must-revalidate"
IMMUTABLE_CACHE_CONTROL = "public, max-age=31536000, immutable"


def content_type(path: Path) -> str:
    overrides = {
        ".html": "text/html; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".jsonl": "application/x-ndjson; charset=utf-8",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    return overrides.get(
        path.suffix.casefold(),
        mimetypes.guess_type(path.name)[0] or "application/octet-stream",
    )


def cache_control(relative_path: str) -> str:
    return (
        GALLERY_CACHE_CONTROL
        if relative_path.startswith("gallery/")
        else IMMUTABLE_CACHE_CONTROL
    )


def artifact_plan(
    run_dir: Path,
    artifacts: dict[str, dict[str, Any]],
    prefix: str,
) -> list[dict[str, Any]]:
    """Resolve and re-verify the exact local artifact inventory before S3 access."""
    if INDEX_RELATIVE_PATH not in artifacts:
        raise ValueError("Publication artifact inventory lacks gallery/index.html")
    run_root = run_dir.resolve()
    plan: list[dict[str, Any]] = []
    for relative in sorted(artifacts, key=lambda value: (value == INDEX_RELATIVE_PATH, value)):
        relative_path = Path(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"Unsafe publication artifact path: {relative}")
        path = (run_root / relative_path).resolve()
        if not path.is_relative_to(run_root) or not path.is_file():
            raise ValueError(f"Publication artifact is missing or outside the run: {relative}")
        expected = artifacts[relative]
        actual_bytes = path.stat().st_size
        actual_sha = sha256_path(path)
        if actual_bytes != expected.get("bytes") or actual_sha != expected.get("sha256"):
            raise ValueError(f"Publication artifact changed after gallery build: {relative}")
        plan.append(
            {
                "relative_path": relative,
                "path": str(path),
                "s3_key": f"{prefix}/{relative}",
                "bytes": actual_bytes,
                "sha256": actual_sha,
                "content_type": content_type(path),
                "cache_control": cache_control(relative),
            }
        )
    if plan[-1]["relative_path"] != INDEX_RELATIVE_PATH:
        raise AssertionError("Gallery index must be the final publication object")
    return plan


def upload_verified(client: Any, bucket: str, item: dict[str, Any]) -> dict[str, Any]:
    """Upload one artifact and verify bytes, SHA metadata, and HTTP metadata."""
    extra = {
        "ContentType": item["content_type"],
        "CacheControl": item["cache_control"],
        "Metadata": {"sha256": item["sha256"]},
    }
    client.upload_file(item["path"], bucket, item["s3_key"], ExtraArgs=extra)
    head = client.head_object(Bucket=bucket, Key=item["s3_key"])
    if head.get("ContentLength") != item["bytes"]:
        raise ValueError(f"Published byte count differs: s3://{bucket}/{item['s3_key']}")
    if (head.get("Metadata") or {}).get("sha256") != item["sha256"]:
        raise ValueError(f"Published SHA metadata differs: s3://{bucket}/{item['s3_key']}")
    if head.get("ContentType") != item["content_type"]:
        raise ValueError(f"Published content type differs: s3://{bucket}/{item['s3_key']}")
    if head.get("CacheControl") != item["cache_control"]:
        raise ValueError(f"Published cache control differs: s3://{bucket}/{item['s3_key']}")
    return {key: value for key, value in item.items() if key != "path"}


def publish(
    run_dir: Path,
    final: bool = False,
    *,
    s3_client: Any | None = None,
    publication_path: Path = PUBLICATION_PATH,
) -> dict[str, Any]:
    """Build and validate locally, then publish only the verified artifact inventory."""
    run_dir = run_dir.resolve()
    build_record = build(run_dir, final)
    validation = validate(run_dir, final)
    expected_mode = "final" if final else "progressive"
    if build_record.get("mode") != expected_mode or validation.get("mode") != expected_mode:
        raise ValueError("Build/validation mode differs from requested publication mode")
    if validation.get("validated") is not True:
        raise ValueError("Gallery validation did not succeed")

    manifest = read_json(MANIFEST_PATH)
    bucket = manifest.get("s3", {}).get("bucket")
    prefix = str(manifest.get("s3", {}).get("prefix", "")).rstrip("/")
    if bucket != EXPECTED_BUCKET or prefix != EXPECTED_PREFIX:
        raise ValueError("V6 manifest S3 destination differs from the isolated preview prefix")
    if run_dir != DEFAULT_RUN_DIR.resolve() or run_dir != Path(manifest["run_dir"]).resolve():
        raise ValueError("Publication run directory differs from the isolated V6 preview run")

    plan = artifact_plan(run_dir, build_record["artifacts"], prefix)
    client = s3_client or boto3.client("s3", region_name=AWS_REGION)
    uploaded = [upload_verified(client, bucket, item) for item in plan]
    public_url = f"{PUBLIC_BASE}/{bucket}/{prefix}/{INDEX_RELATIVE_PATH}"
    record = {
        "version": "hp-v6-preview-generation-publication-v1",
        "published_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "mode": expected_mode,
        "bucket": bucket,
        "prefix": prefix,
        "public_url": public_url,
        "build": build_record,
        "validation": validation,
        "uploaded_object_count": len(uploaded),
        "gallery_index_uploaded_last": True,
        "remote_bytes_and_sha_metadata_verified": True,
        "remote_content_type_and_cache_control_verified": True,
        "credentials_persisted": False,
        "uploaded": uploaded,
    }
    assert_sanitized(record, "publication")
    atomic_json(publication_path, record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    print(json.dumps(publish(args.run_dir, args.final), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
