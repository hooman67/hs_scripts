#!/usr/bin/env python3
"""Publish and byte-verify the frozen V6.1 distribution/prop report."""
from __future__ import annotations

import hashlib
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
BUILT = HERE / "built"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_v6_1_distribution_prop_audit_20261103"
GATEWAY = "https://foundry-aws-corp.adobe.io/asset"
CACHE_CONTROL = "no-cache, no-store, must-revalidate"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def content_type(path: Path) -> str:
    return {
        ".html": "text/html",
        ".js": "application/javascript",
        ".css": "text/css",
        ".json": "application/json",
        ".csv": "text/csv",
        ".md": "text/markdown; charset=utf-8",
    }.get(path.suffix.lower(), mimetypes.guess_type(path.name)[0] or "application/octet-stream")


def upload_and_verify(client, path: Path, relative: str) -> dict:
    body = path.read_bytes()
    digest = sha256(body)
    key = f"{PREFIX}/{relative}"
    client.put_object(
        Bucket=BUCKET, Key=key, Body=body, ContentType=content_type(path),
        CacheControl=CACHE_CONTROL, Metadata={"sha256": digest}, ServerSideEncryption="AES256",
    )
    remote = client.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    if sha256(remote) != digest:
        raise RuntimeError(f"Remote byte verification failed: s3://{BUCKET}/{key}")
    return {
        "key": key, "bytes": len(body), "sha256": digest, "content_type": content_type(path),
        "remote_verified": True, "cache_control": CACHE_CONTROL,
    }


def main() -> None:
    client = boto3.client("s3", region_name="us-west-2")
    files = {}
    for path in sorted(p for p in BUILT.rglob("*") if p.is_file()):
        relative = path.relative_to(BUILT).as_posix()
        files[relative] = upload_and_verify(client, path, relative)
    analysis = json.loads((BUILT / "downloads/analysis.json").read_text(encoding="utf-8"))
    catalog = analysis["approved_prop_catalog"]
    publication = {
        "version": "hp-lifestyle-v6.1-report-publication-v2",
        "published_at_utc": datetime.now(timezone.utc).isoformat(),
        "bucket": BUCKET, "prefix": PREFIX,
        "gallery_url": f"{GATEWAY}/{BUCKET}/{PREFIX}/gallery/index.html",
        "accepted_prompt_sha256": analysis["inputs"]["accepted_export"]["sha256"],
        "approved_catalog_sha256": catalog["source_sha256"],
        "approved_catalog_entries": catalog["entry_count"],
        "approved_visual_families": catalog["visual_family_count"],
        "files": files,
    }
    HERE.joinpath("publication.json").write_text(
        json.dumps(publication, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    publication_record = upload_and_verify(client, HERE / "publication.json", "publication.json")
    print(json.dumps({"gallery_url": publication["gallery_url"], "built_files": len(files), "publication": publication_record}, indent=2))


if __name__ == "__main__":
    main()
