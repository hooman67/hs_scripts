#!/usr/bin/env python3
"""Publish the four judge-v2 fe-html reports with verified S3 uploads.

The command is a dry run unless ``--execute`` is supplied. Credentials are
never read from project files; boto3 uses its normal external credential chain.
Local report files are not modified. Supporting artifacts are uploaded once
under ``artifacts/`` and linked from staged copies of each report's data.json.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol, Sequence

from build_fe_report import GATEWAY, review_query, validate_review_query


ROOT = Path(__file__).resolve().parent
DEFAULT_SOURCE_ROOT = ROOT / "fe_reports"
DEFAULT_BUCKET = "foundry-hp-enterprise-adobe-assets"
DEFAULT_PREFIX = "eval_sets/hp_natural_placement_judge_v2_v6_20261104"
REPORT_NAMES = ("combined", "laptops", "printers", "user_feedback_regressions")
DEFAULT_ARTIFACTS = (
    ("Method summary", ROOT / "SUMMARY.md"),
    ("Judge system prompt", ROOT / "system_prompt.md"),
    ("Observation schema", ROOT / "observation_schema.json"),
    ("Visual-anchor manifest", ROOT / "data" / "visual_anchors.json"),
    ("Browser verification", ROOT / "data" / "browser_verification.json"),
)


class S3Client(Protocol):
    def head_object(self, **kwargs: Any) -> Mapping[str, Any]: ...
    def put_object(self, **kwargs: Any) -> Mapping[str, Any]: ...
    def get_object(self, **kwargs: Any) -> Mapping[str, Any]: ...


@dataclass(frozen=True)
class Artifact:
    label: str
    path: Path


@dataclass(frozen=True)
class UploadObject:
    key: str
    body: bytes
    content_type: str
    source: str

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.body).hexdigest()


def content_type(path: Path) -> str:
    overrides = {
        ".html": "text/html; charset=utf-8",
        ".json": "application/json",
        ".md": "text/markdown; charset=utf-8",
        ".py": "text/x-python; charset=utf-8",
        ".txt": "text/plain; charset=utf-8",
    }
    return overrides.get(
        path.suffix.lower(),
        mimetypes.guess_type(path.name)[0] or "application/octet-stream",
    )


def gateway_url(bucket: str, key: str) -> str:
    return f"{GATEWAY}/asset/{bucket}/{key}"


def _normalize_prefix(prefix: str) -> str:
    value = prefix.strip("/")
    if not value:
        raise ValueError("S3 prefix must be nonempty")
    return value


def _parse_artifact(value: str) -> Artifact:
    label, separator, path = value.partition("=")
    if not separator or not label.strip() or not path.strip():
        raise argparse.ArgumentTypeError("artifact must use LABEL=/absolute/or/relative/path")
    return Artifact(label.strip(), Path(path).expanduser().resolve())


def _as_link_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, Mapping):
        return [{"label": str(label), "url": url} for label, url in value.items()]
    return [value]


def build_upload_plan(
    *,
    source_root: Path,
    bucket: str,
    prefix: str,
    artifacts: Sequence[Artifact],
) -> tuple[list[UploadObject], dict[str, str]]:
    """Validate all inputs and build the exact bytes that would be uploaded."""
    prefix = _normalize_prefix(prefix)
    if not bucket.strip():
        raise ValueError("S3 bucket must be nonempty")

    seen_filenames: dict[str, Path] = {}
    artifact_links: list[dict[str, str]] = []
    uploads: list[UploadObject] = []
    for artifact in artifacts:
        path = artifact.path.resolve()
        if not artifact.label.strip():
            raise ValueError(f"Artifact label must be nonempty: {path}")
        if not path.is_file():
            raise ValueError(f"Missing supporting artifact: {path}")
        previous = seen_filenames.get(path.name)
        if previous is not None and previous != path:
            raise ValueError(
                f"Artifact filename collision for {path.name}: {previous} and {path}"
            )
        seen_filenames[path.name] = path
        key = f"{prefix}/artifacts/{path.name}"
        artifact_links.append(
            {"label": artifact.label.strip(), "url": gateway_url(bucket, key)}
        )
        uploads.append(
            UploadObject(key, path.read_bytes(), content_type(path), str(path))
        )

    report_urls: dict[str, str] = {}
    for name in REPORT_NAMES:
        report_dir = source_root.resolve() / name
        data_path = report_dir / "data.json"
        viewer_path = report_dir / "viewer.html"
        if not data_path.is_file() or not viewer_path.is_file():
            raise ValueError(
                f"Incomplete report {name}: expected {data_path} and {viewer_path}"
            )
        try:
            data = json.loads(data_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid report JSON in {data_path}: {exc}") from exc
        if not isinstance(data, dict) or not isinstance(data.get("rows"), list):
            raise ValueError(f"Report data must contain a rows list: {data_path}")
        if artifact_links:
            data["links"] = _as_link_list(data.get("links")) + artifact_links
        staged_data = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode(
            "utf-8"
        )
        data_key = f"{prefix}/{name}/data.json"
        viewer_key = f"{prefix}/{name}/viewer.html"
        uploads.extend(
            (
                UploadObject(
                    data_key,
                    staged_data,
                    "application/json",
                    f"{data_path} (staged with supporting links)",
                ),
                UploadObject(
                    viewer_key,
                    viewer_path.read_bytes(),
                    "text/html; charset=utf-8",
                    str(viewer_path),
                ),
            )
        )
        report_urls[name] = gateway_url(bucket, viewer_key)

    keys = [upload.key for upload in uploads]
    if len(keys) != len(set(keys)):
        raise ValueError("Upload plan contains duplicate S3 object keys")
    return uploads, report_urls


def _is_missing(exc: Exception) -> bool:
    response = getattr(exc, "response", None)
    if not isinstance(response, Mapping):
        return False
    error = response.get("Error")
    if not isinstance(error, Mapping):
        return False
    return str(error.get("Code")) in {"404", "NoSuchKey", "NotFound"}


def ensure_destinations_absent(
    client: S3Client, bucket: str, uploads: Iterable[UploadObject]
) -> None:
    collisions: list[str] = []
    for upload in uploads:
        try:
            client.head_object(Bucket=bucket, Key=upload.key)
        except Exception as exc:
            if _is_missing(exc):
                continue
            raise
        collisions.append(upload.key)
    if collisions:
        preview = "\n".join(f"  s3://{bucket}/{key}" for key in collisions)
        raise ValueError(
            "Destination objects already exist; pass --allow-overwrite to replace them:\n"
            + preview
        )


def upload_and_verify(
    client: S3Client, bucket: str, upload: UploadObject
) -> dict[str, Any]:
    """Upload one object and verify its metadata plus downloaded bytes."""
    digest = upload.sha256
    checksum = base64.b64encode(hashlib.sha256(upload.body).digest()).decode("ascii")
    client.put_object(
        Bucket=bucket,
        Key=upload.key,
        Body=upload.body,
        ContentType=upload.content_type,
        Metadata={"sha256": digest},
        ChecksumSHA256=checksum,
    )
    head = client.head_object(Bucket=bucket, Key=upload.key)
    if int(head.get("ContentLength", -1)) != len(upload.body):
        raise RuntimeError(f"S3 length verification failed for s3://{bucket}/{upload.key}")
    if str(head.get("ContentType", "")) != upload.content_type:
        raise RuntimeError(
            f"S3 content-type verification failed for s3://{bucket}/{upload.key}"
        )
    metadata = head.get("Metadata") or {}
    if metadata.get("sha256") != digest:
        raise RuntimeError(f"S3 SHA metadata verification failed for {upload.key}")
    response = client.get_object(Bucket=bucket, Key=upload.key)
    stream = response["Body"]
    try:
        downloaded = stream.read()
    finally:
        close = getattr(stream, "close", None)
        if close is not None:
            close()
    downloaded_sha = hashlib.sha256(downloaded).hexdigest()
    if downloaded_sha != digest:
        raise RuntimeError(f"S3 byte SHA-256 verification failed for {upload.key}")
    return {
        "key": upload.key,
        "bytes": len(upload.body),
        "content_type": upload.content_type,
        "sha256": digest,
    }


def plan_summary(
    uploads: Sequence[UploadObject],
    report_urls: Mapping[str, str],
    *,
    bucket: str,
    ldap: str,
) -> dict[str, Any]:
    query = review_query(ldap)
    validate_review_query(query, ldap)
    return {
        "mode": "dry-run",
        "bucket": bucket,
        "object_count": len(uploads),
        "total_bytes": sum(len(upload.body) for upload in uploads),
        "objects": [
            {
                "key": upload.key,
                "bytes": len(upload.body),
                "content_type": upload.content_type,
                "sha256": upload.sha256,
                "source": upload.source,
            }
            for upload in uploads
        ],
        "review_urls": {
            name: url + query for name, url in report_urls.items()
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--bucket", default=DEFAULT_BUCKET)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--ldap", default="hshariati")
    parser.add_argument(
        "--artifact",
        type=_parse_artifact,
        action="append",
        default=[],
        help="additional supporting link and upload in LABEL=PATH form; repeatable",
    )
    parser.add_argument(
        "--no-default-artifacts",
        action="store_true",
        help="omit the standard summary, prompt, schema, anchors, and browser verification",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="perform uploads; without this flag the command only prints the exact plan",
    )
    parser.add_argument(
        "--allow-overwrite",
        action="store_true",
        help="allow replacing objects already present under the destination prefix",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.allow_overwrite and not args.execute:
        raise SystemExit("--allow-overwrite only applies with --execute")
    artifacts = list(args.artifact)
    if not args.no_default_artifacts:
        artifacts = [
            Artifact(label, path.resolve()) for label, path in DEFAULT_ARTIFACTS
        ] + artifacts
    try:
        uploads, report_urls = build_upload_plan(
            source_root=args.source_root,
            bucket=args.bucket,
            prefix=args.prefix,
            artifacts=artifacts,
        )
        summary = plan_summary(
            uploads, report_urls, bucket=args.bucket, ldap=args.ldap.strip()
        )
        if not args.execute:
            print(json.dumps(summary, indent=2))
            return

        import boto3

        client = boto3.client("s3")
        if not args.allow_overwrite:
            ensure_destinations_absent(client, args.bucket, uploads)
        verified = [upload_and_verify(client, args.bucket, upload) for upload in uploads]
        summary["mode"] = "executed-and-verified"
        summary["verified_uploads"] = verified
        print(json.dumps(summary, indent=2))
    except (OSError, ValueError, RuntimeError) as exc:
        raise SystemExit(f"error: {exc}") from exc


if __name__ == "__main__":
    main()
