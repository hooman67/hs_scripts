#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "httpx", "pillow"]
# ///
"""Build, validate, and publish the V5 generation gallery to its isolated prefix."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import mimetypes
from pathlib import Path
from typing import Any

import boto3

from build_gallery import DEFAULT_RUN_DIR, atomic_json, build, read_json, sha256_path
from validate_gallery import validate


GENERATION_DIR = Path(__file__).resolve().parent
PUBLIC_BASE = "https://foundry-aws-corp.adobe.io/asset"


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
    return overrides.get(path.suffix.casefold(), mimetypes.guess_type(path.name)[0] or "application/octet-stream")


def publish(run_dir: Path, final: bool = False) -> dict[str, Any]:
    build_record = build(run_dir, final)
    validation = validate(run_dir, final)
    manifest = read_json(GENERATION_DIR / "image_generation_manifest.json")
    bucket = manifest["s3"]["bucket"]
    prefix = manifest["s3"]["prefix"].rstrip("/")
    client = boto3.client("s3", region_name="us-west-2")
    artifacts = build_record["artifacts"]
    ordered = sorted(artifacts, key=lambda value: (value == "gallery/index.html", value))
    uploaded: list[dict[str, Any]] = []
    for relative in ordered:
        path = run_dir / relative
        key = f"{prefix}/{relative}"
        sha = sha256_path(path)
        client.upload_file(
            str(path),
            bucket,
            key,
            ExtraArgs={
                "ContentType": content_type(path),
                "CacheControl": "no-cache, no-store, must-revalidate" if relative.startswith("gallery/") else "public, max-age=31536000, immutable",
                "Metadata": {"sha256": sha},
            },
        )
        head = client.head_object(Bucket=bucket, Key=key)
        if head["ContentLength"] != path.stat().st_size or head.get("Metadata", {}).get("sha256") != sha:
            raise ValueError(f"Published object verification failed: s3://{bucket}/{key}")
        uploaded.append({"relative_path": relative, "s3_key": key, "bytes": path.stat().st_size, "sha256": sha})
    public_url = f"{PUBLIC_BASE}/{bucket}/{prefix}/gallery/index.html"
    record = {
        "version": "hp-v5-top5-dual-generation-publication-v1",
        "published_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "mode": "final" if final else "progressive",
        "bucket": bucket,
        "prefix": prefix,
        "public_url": public_url,
        "build": build_record,
        "validation": validation,
        "uploaded_object_count": len(uploaded),
        "uploaded": uploaded,
    }
    atomic_json(GENERATION_DIR / "publication.json", record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    print(json.dumps(publish(args.run_dir.resolve(), args.final), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
