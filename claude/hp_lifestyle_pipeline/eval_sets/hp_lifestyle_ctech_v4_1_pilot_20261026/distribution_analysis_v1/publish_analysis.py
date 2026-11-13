#!/usr/bin/env python3
"""One-shot isolated S3 publisher for the V4.1 text-pilot distribution."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import boto3


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
SOURCE = PROJECT / "local_data/reports/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1"
STATE = PROJECT / "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/publication.json"
BROWSER_VALIDATION = PROJECT / "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/browser_validation/browser_validation.json"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1"
REGION = "us-west-2"
FILES = {
    "gallery/index.html": "text/html", "gallery/imsauth.js": "application/javascript",
    "gallery/data.js": "application/javascript", "gallery/report.js": "application/javascript",
    "gallery/style.css": "text/css", "downloads/analysis.json": "application/json",
    "downloads/pilot_prompts.json": "application/json", "downloads/pilot_prompts.txt": "text/plain",
    "downloads/system_prompt.md": "text/markdown",
    "downloads/candidate_metrics.csv": "text/csv", "downloads/reference_prompts.json": "application/json",
    "downloads/lexical_audit.json": "application/json", "source_manifest.json": "application/json",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def list_keys(client) -> list[str]:
    paginator = client.get_paginator("list_objects_v2")
    return sorted(item["Key"] for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX + "/") for item in page.get("Contents", []))


def main() -> None:
    if STATE.exists(): raise SystemExit(f"publication state already exists: {STATE}")
    if not BROWSER_VALIDATION.is_file(): raise SystemExit(f"browser validation is missing: {BROWSER_VALIDATION}")
    browser_validation = json.loads(BROWSER_VALIDATION.read_text(encoding="utf-8"))
    manifest_sha256 = digest((SOURCE / "source_manifest.json").read_bytes())
    if browser_validation.get("status") != "passed": raise SystemExit("browser validation did not pass")
    if browser_validation.get("report_root") != str(SOURCE): raise SystemExit("browser validation used a different report root")
    if browser_validation.get("source_manifest_sha256") != manifest_sha256:
        raise SystemExit("browser validation does not match the current source manifest")
    screenshot = Path(browser_validation["screenshot"])
    if not screenshot.is_file() or screenshot.stat().st_size == 0:
        raise SystemExit(f"browser validation screenshot is missing: {screenshot}")
    s3 = boto3.client("s3", region_name=REGION)
    existing = list_keys(s3)
    if existing: raise SystemExit(f"target prefix is not empty: {len(existing)} objects")
    objects = []
    for relative, content_type in FILES.items():
        path = SOURCE / relative; data = path.read_bytes(); sha = digest(data); key = f"{PREFIX}/{relative}"
        s3.put_object(Bucket=BUCKET, Key=key, Body=data, ContentType=content_type, Metadata={"sha256": sha})
        head = s3.head_object(Bucket=BUCKET, Key=key)
        remote = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
        if head["ContentLength"] != len(data) or head["ContentType"].split(";")[0] != content_type or head["Metadata"].get("sha256") != sha or digest(remote) != sha:
            raise RuntimeError(f"remote verification failed: {key}")
        objects.append({"key": key, "relative_path": relative, "bytes": len(data), "sha256": sha, "content_type": content_type})
    if list_keys(s3) != sorted(item["key"] for item in objects): raise RuntimeError("remote allowlist mismatch")
    record = {"version": "hp-v4.1-distribution-publication-v1", "published_at_utc": datetime.now(timezone.utc).isoformat(),
              "bucket": BUCKET, "prefix": PREFIX,
              "gallery_url": f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}/gallery/index.html",
              "source": str(SOURCE), "active_image_gallery_touched": False, "image_generation_started": False,
              "preflight_prefix_was_empty": True, "remote_object_count": len(objects), "objects": objects,
              "verification": "Each GET matched local SHA-256; HEAD size, content type and sha256 metadata matched; final key list matched the allowlist.",
              "browser_validation": {"status": "passed", "record": str(BROWSER_VALIDATION),
                                     "record_sha256": digest(BROWSER_VALIDATION.read_bytes()),
                                     "source_manifest_sha256": manifest_sha256,
                                     "screenshot": str(screenshot),
                                     "screenshot_sha256": digest(screenshot.read_bytes())}}
    STATE.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
