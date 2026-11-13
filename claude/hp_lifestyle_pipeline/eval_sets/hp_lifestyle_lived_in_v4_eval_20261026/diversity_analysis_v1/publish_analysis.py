#!/usr/bin/env python3
"""One-shot isolated S3 publisher for the V4 distribution analysis."""

from __future__ import annotations

import hashlib
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path

import boto3


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
SOURCE = PROJECT / "local_data/reports/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1"
STATE = PROJECT / "eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1/publication.json"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1"
REGION = "us-west-2"
FILES = {
    "gallery/index.html": "text/html",
    "gallery/imsauth.js": "application/javascript",
    "gallery/data.js": "application/javascript",
    "gallery/report.js": "application/javascript",
    "gallery/style.css": "text/css",
    "downloads/analysis.json": "application/json",
    "downloads/candidate_metrics.csv": "text/csv",
    "downloads/reference_prompts.json": "application/json",
    "downloads/lexical_audit.json": "application/json",
    "source_manifest.json": "application/json",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def list_keys(client) -> list[str]:
    paginator = client.get_paginator("list_objects_v2")
    return sorted(item["Key"] for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX + "/") for item in page.get("Contents", []))


def main() -> None:
    if STATE.exists():
        raise SystemExit(f"Publication state already exists; refusing to overwrite one-shot record: {STATE}")
    s3 = boto3.client("s3", region_name=REGION)
    existing = list_keys(s3)
    if existing:
        raise SystemExit(f"Target prefix is not empty; refusing to overwrite {len(existing)} objects")
    objects = []
    for relative, content_type in FILES.items():
        path = SOURCE / relative
        data = path.read_bytes()
        sha = digest(data)
        key = f"{PREFIX}/{relative}"
        s3.put_object(Bucket=BUCKET, Key=key, Body=data, ContentType=content_type, Metadata={"sha256": sha})
        head = s3.head_object(Bucket=BUCKET, Key=key)
        remote = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
        if head["ContentLength"] != len(data) or head["ContentType"].split(";")[0] != content_type or head["Metadata"].get("sha256") != sha or digest(remote) != sha:
            raise RuntimeError(f"Remote verification failed for {key}")
        objects.append({"key": key, "relative_path": relative, "bytes": len(data), "sha256": sha, "content_type": content_type})
    final_keys = list_keys(s3)
    expected = sorted(item["key"] for item in objects)
    if final_keys != expected:
        raise RuntimeError(f"Remote allowlist mismatch: expected {len(expected)}, got {len(final_keys)}")
    record = {
        "version": "hp-v4-diversity-analysis-publication-v1",
        "published_at_utc": datetime.now(timezone.utc).isoformat(),
        "bucket": BUCKET,
        "prefix": PREFIX,
        "gallery_url": f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}/gallery/index.html",
        "source": str(SOURCE),
        "active_image_gallery_touched": False,
        "preflight_prefix_was_empty": True,
        "remote_object_count": len(objects),
        "objects": objects,
        "verification": "Each object GET matched local SHA-256; HEAD size, content type and sha256 metadata matched; final key list matched the explicit allowlist.",
        "browser_validation": "not_performed_on_this_host",
    }
    STATE.parent.mkdir(parents=True, exist_ok=True)
    temporary = STATE.with_suffix(".tmp")
    temporary.write_text(json.dumps(record, indent=2) + "\n")
    temporary.replace(STATE)
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
