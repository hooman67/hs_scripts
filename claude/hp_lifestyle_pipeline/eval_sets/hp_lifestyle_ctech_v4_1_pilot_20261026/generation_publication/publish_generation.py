#!/usr/bin/env python3
"""One-shot publisher for the complete V4.1 corrected-input generation gallery.

This script never invokes a model or persists credentials in publication
artifacts. It loads short-lived AWS credentials from the standard local env
file and refreshes them through the proven Pluto broker if authentication has
expired.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import mimetypes
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
EVAL_ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = PROJECT_ROOT / "local_data/generation_runs/hp_lifestyle_ctech_v4_1_pilot_20261026_corrected_twins_20261027"
BUILD_SCRIPT = EVAL_ROOT / "build_generation_gallery.py"
VALIDATOR = Path(__file__).resolve().with_name("validate_generation_gallery.py")
STATE_PATH = Path(__file__).resolve().with_name("publication.json")
ATTEMPT_PATH = Path(__file__).resolve().with_name("publication_attempt.json")
BUCKET = "foundry-hp-enterprise-adobe-assets"
REGION = "us-west-2"
PREFIX = "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/generated_v4_1"
GALLERY_URL = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}/gallery/index.html"
AWS_ENV_PATH = Path("/home/colligo/.claude/hshariati/aws_creds.env")
AWS_HELPER = Path("/home/colligo/.claude/scripts/foundry_aws_creds.py")
AWS_BROKER = "https://foundry-aws-pluto.adobe.io/iam/credentials/aws"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_json(path: Path, default: Any = None) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def content_type(path: Path) -> str:
    fixed = {".js": "application/javascript", ".json": "application/json", ".md": "text/markdown", ".html": "text/html", ".css": "text/css", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    return fixed.get(path.suffix.lower(), mimetypes.guess_type(path.name)[0] or "application/octet-stream")


def run_build() -> tuple[dict[str, Any], dict[str, Any]]:
    build = subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=PROJECT_ROOT, text=True, capture_output=True, check=False)
    if build.returncode:
        raise RuntimeError(f"Gallery build failed ({build.returncode}): {build.stderr[-3000:]}")
    build_record = read_json(RUN_DIR / "generation_gallery_build.json")
    final = build_record.get("status_counts") == {"done": 120, "pending": 0, "failed": 0}
    if final:
        build = subprocess.run([sys.executable, str(BUILD_SCRIPT), "--final"], cwd=PROJECT_ROOT, text=True, capture_output=True, check=False)
        if build.returncode:
            raise RuntimeError(f"Final gallery build failed ({build.returncode}): {build.stderr[-3000:]}")
        build_record = read_json(RUN_DIR / "generation_gallery_build.json")
    validator_command = [sys.executable, str(VALIDATOR)] + (["--final"] if final else [])
    checked = subprocess.run(validator_command, cwd=PROJECT_ROOT, text=True, capture_output=True, check=False)
    if checked.returncode:
        raise RuntimeError(f"Gallery validation failed ({checked.returncode}): {checked.stderr[-3000:]}")
    return build_record, json.loads(checked.stdout)


def gallery_data() -> dict[str, Any]:
    text = (RUN_DIR / "gallery/data.js").read_text(encoding="utf-8")
    match = re.fullmatch(r"const GENERATION_DATA = (.*);\n?", text, re.S)
    if not match:
        raise ValueError("Unable to parse generation gallery data")
    return json.loads(match.group(1))


def object_specs(expected_done: int) -> list[dict[str, Any]]:
    paths: list[tuple[Path, str]] = []
    gallery = RUN_DIR / "gallery"
    for path in sorted(gallery.rglob("*")):
        if path.is_file():
            paths.append((path, f"{PREFIX}/gallery/{path.relative_to(gallery).as_posix()}"))
    for path in sorted((RUN_DIR / "assets/corrected_inputs").glob("*.png")):
        paths.append((path, f"{PREFIX}/assets/corrected_inputs/{path.name}"))
    done_images = []
    for row in gallery_data()["rows"]:
        if row["status"] == "done":
            done_images.append(RUN_DIR / row["record"]["generated_image"]["gallery_path"])
    if len(done_images) != expected_done or len({path.name for path in done_images}) != expected_done:
        raise ValueError("Done-image publication inventory differs from validated gallery counts")
    for path in sorted(done_images):
        paths.append((path, f"{PREFIX}/images/{path.name}"))
    paths.append((RUN_DIR / "generation_gallery_build.json", f"{PREFIX}/generation_gallery_build.json"))
    specs = [{"path": str(path), "key": key, "bytes": path.stat().st_size, "sha256": sha256(path), "content_type": content_type(path)} for path, key in paths]
    if len([item for item in specs if "/images/" in item["key"]]) != expected_done:
        raise ValueError("Publication whitelist differs from validated done-image count")
    if len([item for item in specs if "/assets/corrected_inputs/" in item["key"]]) != 4:
        raise ValueError("Publication whitelist requires exactly four corrected inputs")
    if len({item["key"] for item in specs}) != len(specs):
        raise ValueError("Publication whitelist contains duplicate keys")
    return specs


def load_aws_env() -> None:
    if not AWS_ENV_PATH.is_file():
        return
    for raw_line in AWS_ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip()
        if not key.startswith("AWS_"):
            continue
        values = shlex.split(raw_value, posix=True)
        os.environ[key] = values[0] if values else ""


def refresh_aws_credentials() -> None:
    helper_env = os.environ.copy()
    if not helper_env.get("PLUTO_TOKEN") and helper_env.get("PLUTO_AUTH_TOKEN"):
        helper_env["PLUTO_TOKEN"] = helper_env["PLUTO_AUTH_TOKEN"]
    result = subprocess.run(
        ["uv", "run", "--script", str(AWS_HELPER), "--endpoint", AWS_BROKER],
        cwd=PROJECT_ROOT,
        env=helper_env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=120,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"AWS Pluto credential broker failed with exit {result.returncode}")
    load_aws_env()


def make_s3_client():
    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError("boto3 is required; use an environment that provides it") from exc
    load_aws_env()
    return boto3.client("s3", region_name=REGION)


def is_auth_error(exc: BaseException) -> bool:
    response = getattr(exc, "response", {}) or {}
    code = str((response.get("Error") or {}).get("Code") or "")
    return code in {"ExpiredToken", "InvalidClientTokenId", "RequestExpired", "NoCredentialsError"} or any(
        marker in str(exc) for marker in ("ExpiredToken", "Unable to locate credentials", "InvalidClientTokenId", "RequestExpired")
    )


class RefreshingS3:
    def __init__(self) -> None:
        self.client = make_s3_client()

    def __getattr__(self, name: str):
        method = getattr(self.client, name)

        def call(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except Exception as exc:
                if not is_auth_error(exc):
                    raise
                refresh_aws_credentials()
                self.client = make_s3_client()
                return getattr(self.client, name)(*args, **kwargs)

        return call


def list_remote(client: Any) -> list[str]:
    keys: list[str] = []
    token = None
    while True:
        request: dict[str, Any] = {"Bucket": BUCKET, "Prefix": f"{PREFIX}/"}
        if token:
            request["ContinuationToken"] = token
        response = client.list_objects_v2(**request)
        keys.extend(item["Key"] for item in response.get("Contents", []))
        if not response.get("IsTruncated"):
            return sorted(keys)
        token = response["NextContinuationToken"]


def upload_verified(client: Any, spec: dict[str, Any]) -> None:
    with Path(spec["path"]).open("rb") as handle:
        client.put_object(Bucket=BUCKET, Key=spec["key"], Body=handle, ContentType=spec["content_type"], Metadata={"sha256": spec["sha256"]})
    head = client.head_object(Bucket=BUCKET, Key=spec["key"])
    if head.get("ContentLength") != spec["bytes"] or head.get("ContentType") != spec["content_type"] or (head.get("Metadata") or {}).get("sha256") != spec["sha256"]:
        raise RuntimeError(f"S3 HEAD verification differs for {spec['key']}")
    body = client.get_object(Bucket=BUCKET, Key=spec["key"])["Body"]
    digest = hashlib.sha256()
    for block in iter(lambda: body.read(1024 * 1024), b""):
        digest.update(block)
    if digest.hexdigest() != spec["sha256"]:
        raise RuntimeError(f"S3 GET hash verification differs for {spec['key']}")


def publish() -> dict[str, Any]:
    previous_attempt = read_json(ATTEMPT_PATH)
    existing_state = read_json(STATE_PATH)
    if existing_state and existing_state.get("status") in {"final", "terminal_failures"}:
        return existing_state
    build, validation = run_build()
    done_count = int(build["status_counts"]["done"])
    terminal = int(build["status_counts"]["pending"]) == 0
    immutable_inputs = {
        "image_generation_manifest_sha256": build["image_generation_manifest_sha256"],
        "pilot_prompts_sha256": build["pilot_prompts_sha256"],
        "accepted_prompt_cases_sha256": build["accepted_prompt_cases_sha256"],
        "corrected_input_hashes": build["corrected_input_hashes"],
    }
    specs = object_specs(done_count)
    expected = {item["key"]: item for item in specs}
    client = RefreshingS3()
    attempt = previous_attempt
    remote = list_remote(client)
    if attempt is None:
        if remote:
            raise RuntimeError(f"Isolated publication prefix is not empty: {remote[:10]}")
        attempt = {"version": "hp-ctech-v4.1-generation-publication-attempt-v1", "status": "progressive", "started_at_utc": utc_now(), "bucket": BUCKET, "prefix": PREFIX, "prefix_verified_empty": True, "immutable_inputs": immutable_inputs, "uploaded_objects": {}}
        atomic_json(ATTEMPT_PATH, attempt)
    else:
        if attempt.get("immutable_inputs") != immutable_inputs:
            raise RuntimeError("Immutable generation inputs changed after progressive publication began")
        publication_key = f"{PREFIX}/publication.json"
        if not set(remote).issubset(set(expected) | {publication_key}):
            raise RuntimeError(f"Remote prefix contains unowned keys: {sorted(set(remote) - set(expected) - {publication_key})}")
        for key in remote:
            if key == publication_key:
                if not STATE_PATH.exists():
                    raise RuntimeError("Partial publication object exists without its local one-shot state")
                publication_sha = sha256(STATE_PATH)
                head = client.head_object(Bucket=BUCKET, Key=key)
                if head.get("ContentLength") != STATE_PATH.stat().st_size or (head.get("Metadata") or {}).get("sha256") != publication_sha:
                    raise RuntimeError("Existing partial publication object differs from local state")
                continue
            prior = (attempt.get("uploaded_objects") or {}).get(key)
            if not prior:
                raise RuntimeError(f"Remote object has no durable publisher ownership record: {key}")
            head = client.head_object(Bucket=BUCKET, Key=key)
            if head.get("ContentLength") != prior["bytes"] or (head.get("Metadata") or {}).get("sha256") != prior["sha256"]:
                raise RuntimeError(f"Existing partial object differs during resume: {key}")
    uploaded = attempt.setdefault("uploaded_objects", {})
    changed: list[dict[str, Any]] = []
    for spec in specs:
        if uploaded.get(spec["key"], {}).get("sha256") != spec["sha256"]:
            upload_verified(client, spec)
            uploaded[spec["key"]] = {key: spec[key] for key in ("bytes", "sha256", "content_type")}
            changed.append(spec)
            attempt["updated_at_utc"] = utc_now()
            atomic_json(ATTEMPT_PATH, attempt)
    published_at = utc_now()
    snapshot = {
        "published_at_utc": published_at,
        "mode": build["mode"],
        "status_counts": build["status_counts"],
        "missing_record_count": build["missing_record_count"],
        "content_object_count": len(specs),
        "changed_object_count": len(changed),
        "gallery_data_sha256": next(item["sha256"] for item in specs if item["key"].endswith("/gallery/data.js")),
        "all_uploaded_objects_head_and_get_verified": True,
    }
    prior_snapshots = list((existing_state or {}).get("snapshots") or [])
    state = {
        "version": "hp-ctech-v4.1-generation-publication-v1",
        "status": "final" if build["mode"] == "final" else "terminal_failures" if terminal else "progressive",
        "published_at_utc": published_at,
        "bucket": BUCKET,
        "prefix": PREFIX,
        "gallery_url": GALLERY_URL,
        "prefix_verified_empty_before_first_upload": True,
        "object_count": len(specs) + 1,
        "content_object_count": len(specs),
        "validation": validation,
        "immutable_inputs": immutable_inputs,
        "latest_snapshot": snapshot,
        "snapshots": prior_snapshots + [snapshot],
        "objects": specs,
        "model_or_endpoint_calls_by_publisher": False,
        "credentials_in_publication_artifacts": False,
    }
    atomic_json(STATE_PATH, state)
    publication_spec = {"path": str(STATE_PATH), "key": f"{PREFIX}/publication.json", "bytes": STATE_PATH.stat().st_size, "sha256": sha256(STATE_PATH), "content_type": "application/json"}
    upload_verified(client, publication_spec)
    expected_keys = sorted([*expected, publication_spec["key"]])
    actual_keys = list_remote(client)
    if actual_keys != expected_keys:
        raise RuntimeError(f"Final remote whitelist differs: expected {len(expected_keys)}, found {len(actual_keys)}")
    attempt.update({
        "status": state["status"],
        "updated_at_utc": state["published_at_utc"],
        "publication_sha256": publication_spec["sha256"],
        "expected_objects": specs,
    })
    if state["status"] in {"final", "terminal_failures"}:
        attempt["completed_at_utc"] = state["published_at_utc"]
    atomic_json(ATTEMPT_PATH, attempt)
    return state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Perform the authorized one-shot S3 publication")
    args = parser.parse_args()
    if not args.publish:
        parser.error("Publication is disabled unless --publish is supplied after explicit authorization")
    print(json.dumps(publish(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
