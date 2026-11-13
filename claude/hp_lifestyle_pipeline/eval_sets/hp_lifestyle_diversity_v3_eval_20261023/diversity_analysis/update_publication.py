#!/usr/bin/env python3
"""Safely update the already-owned V3 diversity-analysis S3 prefix.

The original publisher is intentionally one-shot. This updater only accepts
remote bytes that match either the prior local publication record or the new
local build, which also makes an interrupted update resumable.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import boto3


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
SOURCE = PROJECT / "local_data/reports/hp_lifestyle_diversity_v3_eval_20261023/diversity_analysis_v1"
STATE = PROJECT / "eval_sets/hp_lifestyle_diversity_v3_eval_20261023/diversity_analysis/publication.json"
HISTORY = PROJECT / "eval_sets/hp_lifestyle_diversity_v3_eval_20261023/diversity_analysis/publication_history.jsonl"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_diversity_v3_eval_20261023/diversity_analysis_v1"
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
    "downloads/display_environment_taxonomy.json": "application/json",
    "source_manifest.json": "application/json",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def list_keys(client: Any) -> list[str]:
    paginator = client.get_paginator("list_objects_v2")
    return sorted(
        item["Key"]
        for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX + "/")
        for item in page.get("Contents", [])
    )


def remote_bytes(client: Any, key: str) -> bytes:
    return client.get_object(Bucket=BUCKET, Key=key)["Body"].read()


def atomic_json(path: Path, value: Any) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    previous = json.loads(STATE.read_text(encoding="utf-8"))
    if previous.get("bucket") != BUCKET or previous.get("prefix") != PREFIX:
        raise RuntimeError("Prior publication record does not own the requested target")
    previous_by_key = {item["key"]: item for item in previous.get("objects", [])}
    if len(previous_by_key) != len(previous.get("objects", [])):
        raise RuntimeError("Prior publication record contains duplicate keys")

    targets = []
    for relative, content_type in FILES.items():
        path = SOURCE / relative
        data = path.read_bytes()
        targets.append(
            {
                "key": f"{PREFIX}/{relative}",
                "relative_path": relative,
                "bytes": len(data),
                "sha256": digest(data),
                "content_type": content_type,
                "data": data,
            }
        )
    target_by_key = {item["key"]: item for item in targets}
    if len(target_by_key) != len(FILES):
        raise RuntimeError("Target allowlist contains duplicate keys")

    s3 = boto3.client("s3", region_name=REGION)
    existing = list_keys(s3)
    unexpected = sorted(set(existing) - set(target_by_key))
    missing_previous = sorted(set(previous_by_key) - set(existing))
    if unexpected or missing_previous:
        raise RuntimeError(
            f"Remote allowlist preflight failed: unexpected={unexpected}, missing_previous={missing_previous}"
        )

    # Every existing object must be the last recorded revision or this exact
    # target revision. The latter permits safe recovery after interruption.
    remote_sha: dict[str, str] = {}
    for key in existing:
        sha = digest(remote_bytes(s3, key))
        allowed = {target_by_key[key]["sha256"]}
        if key in previous_by_key:
            allowed.add(previous_by_key[key]["sha256"])
        if sha not in allowed:
            raise RuntimeError(f"Remote object is neither prior nor target revision: {key}")
        remote_sha[key] = sha

    changed = []
    for item in targets:
        if remote_sha.get(item["key"]) == item["sha256"]:
            continue
        s3.put_object(
            Bucket=BUCKET,
            Key=item["key"],
            Body=item["data"],
            ContentType=item["content_type"],
            Metadata={"sha256": item["sha256"]},
        )
        changed.append(item)

    objects = []
    for item in targets:
        head = s3.head_object(Bucket=BUCKET, Key=item["key"])
        remote = remote_bytes(s3, item["key"])
        if (
            head["ContentLength"] != item["bytes"]
            or head["ContentType"].split(";")[0] != item["content_type"]
            or head["Metadata"].get("sha256") != item["sha256"]
            or digest(remote) != item["sha256"]
        ):
            raise RuntimeError(f"Remote verification failed for {item['key']}")
        objects.append({key: item[key] for key in ("key", "relative_path", "bytes", "sha256", "content_type")})

    expected = sorted(item["key"] for item in targets)
    if list_keys(s3) != expected:
        raise RuntimeError("Final remote key list differs from the explicit target allowlist")

    if not changed and previous.get("version") == "hp-v3-diversity-analysis-publication-v2":
        print(json.dumps(previous, ensure_ascii=False, indent=2))
        return

    prior_revision = int(previous.get("revision", 1))
    record = {
        "version": "hp-v3-diversity-analysis-publication-v2",
        "revision": prior_revision + 1,
        "published_at_utc": datetime.now(timezone.utc).isoformat(),
        "bucket": BUCKET,
        "prefix": PREFIX,
        "gallery_url": f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}/gallery/index.html",
        "source": str(SOURCE),
        "active_image_gallery_touched": False,
        "updated_existing_owned_prefix": True,
        "previous_publication_version": previous.get("version"),
        "previous_published_at_utc": previous.get("published_at_utc"),
        "remote_object_count": len(objects),
        "changed_object_count": len(changed),
        "objects": objects,
        "verification": (
            "Preflight GET matched the prior or target SHA-256 for every existing allowlisted object; "
            "final GET/HEAD matched local bytes, type and sha256 metadata; final keys matched the allowlist."
        ),
        "browser_validation": "not_performed_on_this_host",
    }
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(previous, ensure_ascii=False, separators=(",", ":")) + "\n")
    atomic_json(STATE, record)
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
