#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3>=1.34"]
# ///
"""Dry-run or immutably publish a validated grouped FE report."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def is_missing(exc: Exception) -> bool:
    response = getattr(exc, "response", None)
    if not isinstance(response, Mapping):
        return False
    error = response.get("Error")
    return isinstance(error, Mapping) and str(error.get("Code")) in {"404", "NoSuchKey", "NotFound"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    source = args.source_root.expanduser().resolve()
    prefix = args.prefix.strip("/")
    manifest_path = source / "build_manifest.json"
    require(manifest_path.is_file(), f"missing build manifest: {manifest_path}")
    build = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(build.get("status") == "local_build_validated_not_published", "build status is not publishable")
    require(build.get("bucket") == args.bucket and build.get("prefix") == prefix, "destination differs from build")
    groups = build.get("groups")
    require(isinstance(groups, list) and len(groups) == 16, "build must contain 16 groups")

    claims: list[tuple[Path, str, str]] = [
        (source / "data.json", f"{prefix}/data.json", build["root_data_json_sha256"]),
        (source / "viewer.html", f"{prefix}/viewer.html", build["root_viewer_sha256"]),
    ]
    for group in groups:
        group_dir = source / "groups" / group["slug"]
        claims.extend([
            (group_dir / "data.json", f"{prefix}/groups/{group['slug']}/data.json", group["data_json_sha256"]),
            (group_dir / "viewer.html", f"{prefix}/groups/{group['slug']}/viewer.html", group["viewer_sha256"]),
        ])
    require(len(claims) == 34, "publication must contain exactly 34 FE objects")

    uploads = []
    for path, key, expected_hash in claims:
        require(path.is_file(), f"missing source file: {path}")
        body = path.read_bytes()
        actual_hash = sha256_bytes(body)
        require(actual_hash == expected_hash, f"hash differs: {path}")
        uploads.append({"path": path, "key": key, "body": body, "sha256": actual_hash, "content_type": "application/json" if path.suffix == ".json" else "text/html; charset=utf-8"})

    output: dict[str, Any] = {
        "mode": "dry-run",
        "bucket": args.bucket,
        "prefix": prefix,
        "object_count": len(uploads),
        "objects": [{"key": item["key"], "bytes": len(item["body"]), "sha256": item["sha256"]} for item in uploads],
        "viewer_url": f"https://foundry-aws-corp.adobe.io/asset/{args.bucket}/{prefix}/viewer.html",
    }
    if args.execute:
        import boto3

        client = boto3.client("s3", region_name="us-west-2")
        collisions = []
        for item in uploads:
            try:
                client.head_object(Bucket=args.bucket, Key=item["key"])
            except Exception as exc:
                if is_missing(exc):
                    continue
                raise
            collisions.append(item["key"])
        require(not collisions, "destination objects already exist; refusing to overwrite:\n" + "\n".join(collisions))
        verified = []
        for item in uploads:
            checksum = base64.b64encode(hashlib.sha256(item["body"]).digest()).decode("ascii")
            client.put_object(Bucket=args.bucket, Key=item["key"], Body=item["body"], ContentType=item["content_type"], Metadata={"sha256": item["sha256"]}, ChecksumSHA256=checksum)
            response = client.get_object(Bucket=args.bucket, Key=item["key"])
            downloaded = response["Body"].read()
            require(sha256_bytes(downloaded) == item["sha256"], f"download verification failed: {item['key']}")
            verified.append({"key": item["key"], "sha256": item["sha256"], "bytes": len(downloaded)})
        output["mode"] = "executed_and_download_verified"
        output["verified_uploads"] = verified

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
