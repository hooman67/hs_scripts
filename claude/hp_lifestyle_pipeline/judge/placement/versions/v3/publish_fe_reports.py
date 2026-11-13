#!/usr/bin/env python3
"""Plan or publish the V6.1 placement-judge FE reports.

The default mode is a local dry run. ``--execute`` uploads data.json and
viewer.html for printers, laptops, and combined, plus the 16 verified digital
twin assets referenced by those reports. Existing destination objects are a
hard error so prior reports and annotations are never replaced.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence

from build_fe_report import (
    DEFAULT_PUBLISH_BUCKET,
    DEFAULT_PUBLISH_PREFIX,
    GATEWAY,
    REPORT_SCOPES,
    review_query,
    validate_review_query,
)


ROOT = Path(__file__).resolve().parent
DEFAULT_SOURCE = ROOT / "fe_reports/v6_1_20261105"
DEFAULT_BUCKET = DEFAULT_PUBLISH_BUCKET
DEFAULT_PREFIX = DEFAULT_PUBLISH_PREFIX


class S3Client(Protocol):
    def head_object(self, **kwargs: Any) -> Mapping[str, Any]: ...
    def put_object(self, **kwargs: Any) -> Mapping[str, Any]: ...
    def get_object(self, **kwargs: Any) -> Mapping[str, Any]: ...


@dataclass(frozen=True)
class Upload:
    key: str
    body: bytes
    content_type: str
    source: Path

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.body).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha256(path: Path) -> str:
    require(path.is_file(), f"missing file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def content_type(path: Path) -> str:
    if path.suffix == ".html":
        return "text/html; charset=utf-8"
    if path.suffix == ".json":
        return "application/json"
    return mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def gateway_url(bucket: str, key: str) -> str:
    return f"{GATEWAY}/asset/{bucket}/{key}"


def load_build(source_root: Path) -> Mapping[str, Any]:
    path = source_root / "build_manifest.json"
    require(path.is_file(), f"build manifest missing: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid build manifest {path}: {exc}") from exc
    require(isinstance(payload, Mapping), "build manifest must be an object")
    require(payload.get("status") == "local_build_validated_not_published", "build is not validated")
    validation = payload.get("validation")
    require(isinstance(validation, Mapping), "build validation missing")
    required_true = (
        "result_ids_exactly_match_manifest",
        "runtime_inputs_exactly_match_manifest",
        "runtime_input_whitelist_verified",
        "image_prompt_and_result_hashes_verified",
        "protocol_claims_match_every_result",
        "viewer_copied_verbatim",
        "question_wire_round_trip_verified",
    )
    require(all(validation.get(key) is True for key in required_true), "build validation is incomplete")
    require(validation.get("human_labels_invented") is False, "build claims invented human labels")
    return payload


def build_plan(
    source_root: Path, bucket: str, prefix: str
) -> tuple[list[Upload], dict[str, str]]:
    require(bool(bucket.strip()), "bucket must be nonempty")
    prefix = prefix.strip("/")
    require(bool(prefix), "prefix must be nonempty")
    build = load_build(source_root)
    destination = build.get("publish_destination")
    require(isinstance(destination, Mapping), "build publish destination missing")
    require(destination.get("bucket") == bucket, "bucket differs from validated report links")
    require(destination.get("prefix") == prefix, "prefix differs from validated report links")
    report_claims = build.get("reports")
    require(isinstance(report_claims, Mapping), "build report hashes missing")
    uploads: list[Upload] = []
    urls: dict[str, str] = {}
    expected_rows = {"combined": 160, "laptops": 80, "printers": 80}
    for report_name, _ in REPORT_SCOPES:
        report_dir = source_root / report_name
        data_path = report_dir / "data.json"
        viewer_path = report_dir / "viewer.html"
        require(data_path.is_file() and viewer_path.is_file(), f"incomplete report: {report_name}")
        claim = report_claims.get(report_name)
        require(isinstance(claim, Mapping), f"missing build claim: {report_name}")
        require(file_sha256(data_path) == claim.get("data_json_sha256"), f"{report_name}: data hash changed")
        require(file_sha256(viewer_path) == claim.get("viewer_html_sha256"), f"{report_name}: viewer hash changed")
        data = json.loads(data_path.read_text(encoding="utf-8"))
        require(isinstance(data, Mapping) and isinstance(data.get("rows"), list), f"{report_name}: invalid FE data")
        require(len(data["rows"]) == expected_rows[report_name] == claim.get("rows"), f"{report_name}: row count differs")
        ids = [row.get("meta_data", {}).get("evalset_item_id") for row in data["rows"]]
        require(all(isinstance(value, str) and value for value in ids), f"{report_name}: invalid row IDs")
        require(len(ids) == len(set(ids)), f"{report_name}: duplicate row IDs")
        for path in (data_path, viewer_path):
            key = f"{prefix}/{report_name}/{path.name}"
            uploads.append(Upload(key, path.read_bytes(), content_type(path), path.resolve()))
        urls[report_name] = gateway_url(bucket, f"{prefix}/{report_name}/viewer.html")
    twin_assets = build.get("shared_twin_assets")
    require(isinstance(twin_assets, Mapping) and twin_assets, "shared twin assets missing")
    require(len(twin_assets) == 16, f"expected 16 unique twin assets, found {len(twin_assets)}")
    for filename, claim in sorted(twin_assets.items()):
        require(isinstance(filename, str) and filename, "invalid twin filename")
        require(isinstance(claim, Mapping), f"invalid twin claim: {filename}")
        path = Path(str(claim.get("path", ""))).resolve()
        require(path.is_file(), f"missing twin asset: {path}")
        require(
            path.name == claim.get("source_filename"),
            f"twin source filename/path differ: {filename}",
        )
        require(path.stat().st_size == claim.get("bytes"), f"twin byte count changed: {filename}")
        require(file_sha256(path) == claim.get("sha256"), f"twin hash changed: {filename}")
        key = str(claim.get("s3_key", ""))
        require(key == f"{prefix}/assets/twins/{filename}", f"twin destination differs: {filename}")
        uploads.append(Upload(key, path.read_bytes(), content_type(path), path))
    keys = [upload.key for upload in uploads]
    require(len(keys) == len(set(keys)) == 22, "upload plan must contain 22 unique objects")
    return uploads, urls


def is_missing(exc: Exception) -> bool:
    response = getattr(exc, "response", None)
    if not isinstance(response, Mapping):
        return False
    error = response.get("Error")
    return isinstance(error, Mapping) and str(error.get("Code")) in {
        "404",
        "NoSuchKey",
        "NotFound",
    }


def require_destinations_absent(
    client: S3Client, bucket: str, uploads: Sequence[Upload]
) -> None:
    collisions = []
    for upload in uploads:
        try:
            client.head_object(Bucket=bucket, Key=upload.key)
        except Exception as exc:
            if is_missing(exc):
                continue
            raise
        collisions.append(upload.key)
    require(
        not collisions,
        "destination objects already exist; refusing to overwrite:\n"
        + "\n".join(f"  s3://{bucket}/{key}" for key in collisions),
    )


def upload_and_verify(
    client: S3Client, bucket: str, upload: Upload
) -> dict[str, Any]:
    checksum = base64.b64encode(hashlib.sha256(upload.body).digest()).decode("ascii")
    client.put_object(
        Bucket=bucket,
        Key=upload.key,
        Body=upload.body,
        ContentType=upload.content_type,
        Metadata={"sha256": upload.sha256},
        ChecksumSHA256=checksum,
    )
    head = client.head_object(Bucket=bucket, Key=upload.key)
    require(int(head.get("ContentLength", -1)) == len(upload.body), f"length check failed: {upload.key}")
    require(str(head.get("ContentType")) == upload.content_type, f"content type check failed: {upload.key}")
    require((head.get("Metadata") or {}).get("sha256") == upload.sha256, f"metadata hash failed: {upload.key}")
    response = client.get_object(Bucket=bucket, Key=upload.key)
    stream = response["Body"]
    try:
        downloaded = stream.read()
    finally:
        close = getattr(stream, "close", None)
        if close is not None:
            close()
    require(hashlib.sha256(downloaded).hexdigest() == upload.sha256, f"download hash failed: {upload.key}")
    return {
        "key": upload.key,
        "bytes": len(upload.body),
        "content_type": upload.content_type,
        "sha256": upload.sha256,
    }


def summary(
    uploads: Sequence[Upload],
    urls: Mapping[str, str],
    *,
    bucket: str,
    ldap: str,
    mode: str,
) -> dict[str, Any]:
    query = review_query(ldap)
    validate_review_query(query, ldap)
    return {
        "mode": mode,
        "bucket": bucket,
        "object_count": len(uploads),
        "objects": [
            {
                "key": upload.key,
                "bytes": len(upload.body),
                "content_type": upload.content_type,
                "sha256": upload.sha256,
                "source": str(upload.source),
            }
            for upload in uploads
        ],
        "review_urls": {name: url + query for name, url in urls.items()},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--bucket", default=DEFAULT_BUCKET)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--ldap", default="hshariati")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="upload after collision checks; without this flag only print the plan",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        source = args.source_root.expanduser().resolve()
        uploads, urls = build_plan(source, args.bucket, args.prefix)
        payload = summary(
            uploads,
            urls,
            bucket=args.bucket,
            ldap=args.ldap.strip(),
            mode="dry-run",
        )
        if args.execute:
            import boto3

            client = boto3.client("s3", region_name="us-west-2")
            require_destinations_absent(client, args.bucket, uploads)
            payload["mode"] = "executed-and-verified"
            payload["verified_uploads"] = [
                upload_and_verify(client, args.bucket, upload) for upload in uploads
            ]
    except (OSError, ValueError, RuntimeError) as exc:
        raise SystemExit(f"error: {exc}") from exc
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
