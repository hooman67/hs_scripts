#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "httpx", "pillow"]
# ///
"""Rebuild and publish a generation report only when record/status files change."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import run_generation as generation


ROOT = Path(__file__).resolve().parent


def snapshot(run_dir: Path) -> dict[str, Any]:
    assets: dict[str, Any] = {}
    for directory in ("records", "status"):
        for path in sorted((run_dir / directory).glob("*.json")):
            assets[str(path.relative_to(run_dir))] = {
                "bytes": path.stat().st_size,
                "sha256": generation.sha256_path(path),
            }
    return {"assets": assets, "sha256": generation.canonical_sha256(assets)}


def load_records(run_dir: Path) -> list[dict[str, Any]]:
    return [generation.load_json(path) for path in sorted((run_dir / "records").glob("*.json"))]


def valid_done_count(run_dir: Path) -> int:
    count = 0
    for record in load_records(run_dir):
        if record.get("status") != "done" or not record.get("image_filename") or not record.get("image_sha256"):
            continue
        image = run_dir / "images" / record["image_filename"]
        if image.is_file() and generation.sha256_path(image) == record["image_sha256"]:
            count += 1
    return count


def build_report(args: argparse.Namespace, manifest: dict[str, Any]) -> None:
    command = [
        sys.executable, str(ROOT / "build_grouped_report.py"),
        "--prompts", str(args.prompts.resolve()),
        "--prompts-sha256", manifest["prompts_sha256"],
        "--prompts-txt", str(args.prompts_txt.resolve()),
        "--run-dir", str(args.run_dir.resolve()),
        "--output", str(args.run_dir.resolve() / "report"),
        "--catalog", str(args.catalog.resolve()),
        "--title", args.title,
        "--bucket", manifest["bucket"],
        "--prefix", manifest["prefix"],
    ]
    subprocess.run(command, check=True)


def verify_published(
    run_dir: Path, manifest: dict[str, Any], fallback_creds: Path,
    previous: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    client = generation.s3_client(manifest["bucket"], fallback_creds)
    relative_paths = [
        *sorted(path.relative_to(run_dir) for path in (run_dir / "report").rglob("*") if path.is_file()),
        *sorted(path.relative_to(run_dir) for path in (run_dir / "twins").glob("*.png")),
        *sorted(path.relative_to(run_dir) for path in (run_dir / "images").glob("*.png")),
    ]
    previous = previous or {}
    objects: dict[str, Any] = {}
    remote_get_count = 0
    for relative in relative_paths:
        local = run_dir / relative
        if not local.is_file():
            raise FileNotFoundError(f"required published artifact is missing locally: {local}")
        key = f"{manifest['prefix'].rstrip('/')}/{relative.as_posix()}"
        remote = client.head_object(Bucket=manifest["bucket"], Key=key)
        if remote["ContentLength"] != local.stat().st_size:
            raise ValueError(f"published object size differs: s3://{manifest['bucket']}/{key}")
        name = relative.as_posix()
        local_sha = generation.sha256_path(local)
        etag = str(remote.get("ETag") or "").strip('"')
        prior = previous.get(name) or {}
        cache_matches = (
            prior.get("bytes") == local.stat().st_size and prior.get("sha256") == local_sha
            and prior.get("etag") == etag and prior.get("remote_sha256") == local_sha
        )
        if cache_matches:
            remote_sha = prior["remote_sha256"]
            verification = "cached_remote_get_sha256_plus_current_head"
        else:
            response = client.get_object(Bucket=manifest["bucket"], Key=key)
            digest = hashlib.sha256()
            streamed = 0
            for chunk in response["Body"].iter_chunks(chunk_size=8 * 1024 * 1024):
                if chunk:
                    digest.update(chunk)
                    streamed += len(chunk)
            remote_sha = digest.hexdigest()
            if streamed != local.stat().st_size or remote_sha != local_sha:
                raise ValueError(f"published object content differs: s3://{manifest['bucket']}/{key}")
            remote_get_count += 1
            verification = "remote_get_sha256"
        objects[name] = {
            "bytes": local.stat().st_size, "sha256": local_sha, "etag": etag,
            "remote_sha256": remote_sha, "verification": verification,
        }
    return {"count": len(objects), "remote_get_count": remote_get_count, "objects": objects}


def local_public_manifest(run_dir: Path) -> dict[str, dict[str, Any]]:
    return {
        path.relative_to(run_dir).as_posix(): {
            "bytes": path.stat().st_size, "sha256": generation.sha256_path(path),
        }
        for path in generation.publishable_paths(run_dir)
    }


def publish_changed_tree(
    run_dir: Path, manifest: dict[str, Any], fallback_creds: Path,
    previous_assets: dict[str, dict[str, Any]],
) -> tuple[int, dict[str, dict[str, Any]]]:
    current = local_public_manifest(run_dir)
    changed = [relative for relative, value in current.items() if previous_assets.get(relative) != value]
    client = generation.s3_client(manifest["bucket"], fallback_creds)
    generation.append_journal(run_dir, {
        "event": "progressive_publish_started", "changed_files": len(changed),
        "public_files": len(current), "bucket": manifest["bucket"], "prefix": manifest["prefix"],
    })
    published = {relative: value for relative, value in previous_assets.items() if current.get(relative) == value}
    for relative in changed:
        path = run_dir / relative
        before = current[relative]
        key = f"{manifest['prefix'].rstrip('/')}/{relative}"
        client.upload_file(str(path), manifest["bucket"], key,
                           ExtraArgs={"ContentType": generation.content_type(path)})
        if path.is_file():
            after = {"bytes": path.stat().st_size, "sha256": generation.sha256_path(path)}
            if after == before:
                published[relative] = before
    generation.append_journal(run_dir, {
        "event": "progressive_publish_complete", "changed_files": len(changed),
        "stable_published_files": len(published),
    })
    return len(changed), published


def publish_once(
    args: argparse.Namespace, observed: dict[str, Any], previous: dict[str, Any],
) -> dict[str, Any]:
    run_dir = args.run_dir.resolve()
    manifest = generation.load_json(run_dir / "run_manifest.json")
    if manifest.get("prompts_sha256") != generation.sha256_path(args.prompts.resolve()):
        raise ValueError("publisher prompt file differs from immutable run manifest")
    build_report(args, manifest)
    document = generation.load_json(args.prompts.resolve())
    rows = generation.interleave(generation.validate_prompt_document(
        document, args.prompts.resolve(), manifest["prompts_sha256"],
    ))
    for position, row in enumerate(rows, 1):
        row["queue_position"] = position
    summary = generation.summarize(run_dir, rows, manifest["bucket"], manifest["prefix"])
    uploaded, published_assets = publish_changed_tree(
        run_dir, manifest, args.fallback_creds.resolve(), previous.get("published_artifacts") or {},
    )
    verified = verify_published(
        run_dir, manifest, args.fallback_creds.resolve(), previous.get("verified_objects") or {},
    )
    records = load_records(run_dir)
    statuses = Counter(str(record.get("status") or "unknown") for record in records)
    done = sorted(
        (record for record in records if record.get("status") == "done"),
        key=lambda record: (record.get("completed_at_utc") or "", record.get("row_id") or ""),
    )
    base = f"https://foundry-aws-corp.adobe.io/asset/{manifest['bucket']}/{manifest['prefix'].rstrip('/')}"
    return {
        "schema_version": 1,
        "updated_at_utc": generation.now(),
        "watch_snapshot": observed,
        "run_sha256": manifest["run_sha256"],
        "status_counts": dict(sorted(statuses.items())),
        "summary_status_counts": summary["status_counts"],
        "uploaded_file_count": uploaded,
        "published_artifact_count": len(published_assets),
        "published_artifacts": published_assets,
        "verified_object_count": verified["count"],
        "remote_get_verified_count": verified["remote_get_count"],
        "verified_objects": verified["objects"],
        "viewer_url": f"{base}/report/viewer.html",
        "distribution_url": f"{base}/report/distribution/index.html",
        "first_done": ({
            "row_id": done[0]["row_id"], "completed_at_utc": done[0].get("completed_at_utc"),
            "image_sha256": done[0].get("image_sha256"),
            "image_url": f"{base}/images/{done[0]['row_slug']}.png",
        } if done else None),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--prompts-txt", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--interval-seconds", type=int, default=60)
    parser.add_argument("--minimum-done", type=int, default=0, help="defer first publication until this many valid images exist")
    parser.add_argument("--fallback-creds", type=Path, default=Path.home() / ".claude/hshariati/aws_creds.env")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    if not 15 <= args.interval_seconds <= 3600:
        parser.error("--interval-seconds must be between 15 and 3600")
    if not 0 <= args.minimum_done <= generation.EXPECTED_COUNT:
        parser.error(f"--minimum-done must be between 0 and {generation.EXPECTED_COUNT}")
    return args


def main() -> int:
    args = parse_args()
    state_path = args.run_dir.resolve() / "journals/publisher_state.json"
    error_path = args.run_dir.resolve() / "journals/publisher_error.json"
    while True:
        observed = snapshot(args.run_dir.resolve())
        previous = generation.load_json(state_path) if state_path.is_file() else {}
        if previous.get("watch_snapshot", {}).get("sha256") != observed["sha256"]:
            completed = valid_done_count(args.run_dir.resolve())
            if completed < args.minimum_done:
                state = {
                    "schema_version": 1, "updated_at_utc": generation.now(), "status": "waiting_for_valid_images",
                    "minimum_done": args.minimum_done, "valid_done_count": completed, "watch_snapshot": observed,
                }
                generation.atomic_json(state_path, state)
                print(json.dumps(state, ensure_ascii=False), flush=True)
                if args.once:
                    return 0
                time.sleep(args.interval_seconds)
                continue
            try:
                state = publish_once(args, observed, previous)
                generation.atomic_json(state_path, state)
                if error_path.exists():
                    error_path.unlink()
                print(json.dumps({
                    "published_at_utc": state["updated_at_utc"], "status_counts": state["status_counts"],
                    "viewer_url": state["viewer_url"], "first_done": state["first_done"],
                }, ensure_ascii=False), flush=True)
            except Exception as exc:  # noqa: BLE001
                error = {"at_utc": generation.now(), "type": type(exc).__name__, "error": str(exc),
                         "watch_snapshot": observed}
                generation.atomic_json(error_path, error)
                print(json.dumps(error, ensure_ascii=False), file=sys.stderr, flush=True)
        if args.once:
            return 0 if state_path.is_file() and not error_path.exists() else 1
        time.sleep(args.interval_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
