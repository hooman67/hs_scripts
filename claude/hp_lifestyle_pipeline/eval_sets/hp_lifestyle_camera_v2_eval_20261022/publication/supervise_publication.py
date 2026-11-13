#!/usr/bin/env python3
"""Continuously rebuild and publish the camera-V2 gallery when inputs change."""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
import shlex
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


EVAL_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = EVAL_ROOT.parents[1]
RUN_ROOT = PROJECT_ROOT / "local_data/generation_runs/hp_lifestyle_camera_v2_eval_20261022"
BUILD_SCRIPT = EVAL_ROOT / "build_gallery.py"
ACCEPTED_PATH = EVAL_ROOT / "accepted_prompt_cases.json"
MANIFEST_PATH = EVAL_ROOT / "manifest.json"
PUBLICATION_DIR = EVAL_ROOT / "publication"
PUBLICATION_PATH = PUBLICATION_DIR / "publication.json"
HISTORY_PATH = PUBLICATION_DIR / "snapshots.jsonl"
STATE_PATH = PUBLICATION_DIR / "supervisor_state.json"
PID_PATH = PUBLICATION_DIR / "publisher.pid.json"
LOCK_PATH = PUBLICATION_DIR / "publisher.lock"
AWS_ENV_PATH = Path("/home/colligo/.claude/hshariati/aws_creds.env")
AWS_HELPER = Path("/home/colligo/.claude/scripts/foundry_aws_creds.py")
AWS_BROKER = "https://foundry-aws-pluto.adobe.io/iam/credentials/aws"
REGION = "us-west-2"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_camera_v2_eval_20261022/generated_v2"
GALLERY_URL = (
    "https://foundry-aws-corp.adobe.io/asset/"
    f"{BUCKET}/{PREFIX}/gallery/index.html"
)

STOP = False


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_aws_env() -> None:
    if not AWS_ENV_PATH.exists():
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
        if key.startswith("AWS_"):
            values = shlex.split(raw_value, posix=True)
            os.environ[key] = values[0] if values else ""


def refresh_aws_credentials() -> None:
    token = os.environ.get("PLUTO_AUTH_TOKEN")
    if not token:
        raise RuntimeError("PLUTO_AUTH_TOKEN is unavailable for AWS credential refresh")
    env = os.environ.copy()
    env["PLUTO_TOKEN"] = token
    result = subprocess.run(
        [sys.executable, str(AWS_HELPER), "--endpoint", AWS_BROKER],
        cwd=str(PROJECT_ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=120,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"AWS credential broker failed with exit {result.returncode}")
    load_aws_env()


def aws(arguments: list[str], *, retry: bool = True) -> subprocess.CompletedProcess[str]:
    load_aws_env()
    result = subprocess.run(
        ["aws", *arguments],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return result
    combined = f"{result.stdout}\n{result.stderr}"
    expired = any(
        marker in combined
        for marker in (
            "ExpiredToken",
            "Unable to locate credentials",
            "InvalidClientTokenId",
            "RequestExpired",
        )
    )
    if retry and expired:
        refresh_aws_credentials()
        return aws(arguments, retry=False)
    safe_message = result.stderr.strip().replace(os.environ.get("PLUTO_AUTH_TOKEN", ""), "[redacted]")
    raise RuntimeError(f"AWS CLI failed ({result.returncode}): {safe_message[:1000]}")


def object_spec(path: Path, key: str, content_type: str) -> dict[str, Any]:
    return {
        "path": str(path),
        "key": key,
        "bytes": path.stat().st_size,
        "sha256": sha256_path(path),
        "content_type": content_type,
    }


def gather_objects() -> list[dict[str, Any]]:
    gallery = RUN_ROOT / "gallery"
    objects = [
        object_spec(gallery / "index.html", f"{PREFIX}/gallery/index.html", "text/html"),
        object_spec(gallery / "data.js", f"{PREFIX}/gallery/data.js", "application/javascript"),
        object_spec(gallery / "main.js", f"{PREFIX}/gallery/main.js", "application/javascript"),
        object_spec(gallery / "imsauth.js", f"{PREFIX}/gallery/imsauth.js", "application/javascript"),
        object_spec(gallery / "style.css", f"{PREFIX}/gallery/style.css", "text/css"),
        object_spec(RUN_ROOT / "gallery_build.json", f"{PREFIX}/gallery_build.json", "application/json"),
        object_spec(RUN_ROOT / "reference_assets.json", f"{PREFIX}/reference_assets.json", "application/json"),
    ]
    summary = RUN_ROOT / "summary.json"
    if summary.exists():
        objects.append(object_spec(summary, f"{PREFIX}/generation_summary.json", "application/json"))
    for path in sorted((RUN_ROOT / "images").glob("*.png")):
        objects.append(object_spec(path, f"{PREFIX}/images/{path.name}", "image/png"))
    return objects


def upload_and_verify(spec: dict[str, Any]) -> None:
    uri = f"s3://{BUCKET}/{spec['key']}"
    aws(
        [
            "s3",
            "cp",
            spec["path"],
            uri,
            "--content-type",
            spec["content_type"],
            "--metadata",
            f"sha256={spec['sha256']}",
            "--checksum-algorithm",
            "SHA256",
            "--region",
            REGION,
            "--only-show-errors",
        ]
    )
    result = aws(
        [
            "s3api",
            "head-object",
            "--bucket",
            BUCKET,
            "--key",
            spec["key"],
            "--region",
            REGION,
            "--output",
            "json",
        ]
    )
    head = json.loads(result.stdout)
    if head.get("ContentLength") != spec["bytes"]:
        raise RuntimeError(f"Uploaded byte count mismatch: {spec['key']}")
    if head.get("ContentType") != spec["content_type"]:
        raise RuntimeError(f"Uploaded content type mismatch: {spec['key']}")
    if (head.get("Metadata") or {}).get("sha256") != spec["sha256"]:
        raise RuntimeError(f"Uploaded SHA-256 metadata mismatch: {spec['key']}")


def input_fingerprint() -> str:
    digest = hashlib.sha256()
    for path in [MANIFEST_PATH, ACCEPTED_PATH, BUILD_SCRIPT, *(EVAL_ROOT / "gallery").glob("*")]:
        if path.is_file():
            stat = path.stat()
            digest.update(f"{path}:{stat.st_size}:{stat.st_mtime_ns}\n".encode())
    for directory, pattern in ((RUN_ROOT / "records", "*.json"), (RUN_ROOT / "images", "*.png")):
        for path in sorted(directory.glob(pattern)):
            stat = path.stat()
            digest.update(f"{path.name}:{stat.st_size}:{stat.st_mtime_ns}\n".encode())
    summary = RUN_ROOT / "summary.json"
    if summary.exists():
        stat = summary.stat()
        digest.update(f"summary:{stat.st_size}:{stat.st_mtime_ns}\n".encode())
    return digest.hexdigest()


def run_builder() -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"Gallery builder failed ({result.returncode}): {result.stderr[-2000:]}")
    build = read_json(RUN_ROOT / "gallery_build.json")
    pending = build.get("status_counts", {}).get("generation_pending", 0) + build.get("status_counts", {}).get("prompt_pending", 0)
    if build.get("prompt_case_set_complete") and pending == 0:
        final_result = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT), "--final"],
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if final_result.returncode:
            raise RuntimeError(f"Final gallery validation failed ({final_result.returncode}): {final_result.stderr[-2000:]}")
        build = read_json(RUN_ROOT / "gallery_build.json")
    return build


def append_snapshot(build: dict[str, Any], changed: list[dict[str, Any]]) -> dict[str, Any]:
    snapshot = {
        "published_at_utc": utc_now(),
        "phase": "final" if build.get("mode") == "final" else "progressive_automated",
        "accepted_case_count": build["accepted_case_count"],
        "manifest_case_count": build["manifest_case_count"],
        "planned_generation_row_count": build["planned_generation_row_count"],
        "placeholder_row_count": build["placeholder_row_count"],
        "generation_record_count": build["generation_record_count"],
        "status_counts": build["status_counts"],
        "manifest_sha256": build["manifest_sha256"],
        "accepted_prompt_cases_sha256": build["accepted_prompt_cases_sha256"],
        "gallery_artifacts": build["artifacts"],
        "changed_s3_objects": [
            {k: item[k] for k in ("key", "bytes", "sha256", "content_type")}
            for item in changed
        ],
        "s3_verification": {
            "changed_object_count": len(changed),
            "all_changed_object_sizes_types_and_sha256_metadata_match": True,
        },
        "browser_render_verified": False,
    }
    publication = read_json(PUBLICATION_PATH, {})
    publication["status"] = "final" if build.get("mode") == "final" else "progressive"
    publication["latest_snapshot"] = snapshot
    publication.setdefault("snapshots", []).append(snapshot)
    atomic_json(PUBLICATION_PATH, publication)
    with HISTORY_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(snapshot, separators=(",", ":")) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return snapshot


def publish_once(state: dict[str, Any], fingerprint: str) -> dict[str, Any]:
    build = run_builder()
    objects = gather_objects()
    uploaded = state.setdefault("uploaded_objects", {})
    changed = [item for item in objects if uploaded.get(item["key"], {}).get("sha256") != item["sha256"]]
    for item in changed:
        upload_and_verify(item)
        uploaded[item["key"]] = {k: item[k] for k in ("bytes", "sha256", "content_type")}
    snapshot = append_snapshot(build, changed)
    publication_spec = object_spec(PUBLICATION_PATH, f"{PREFIX}/publication.json", "application/json")
    upload_and_verify(publication_spec)
    uploaded[publication_spec["key"]] = {
        k: publication_spec[k] for k in ("bytes", "sha256", "content_type")
    }
    state.update(
        {
            "version": "camera-v2-gallery-publisher-state-v1",
            "status": "running",
            "bucket": BUCKET,
            "prefix": PREFIX,
            "gallery_url": GALLERY_URL,
            "poll_seconds": state.get("poll_seconds"),
            "last_input_fingerprint": fingerprint,
            "last_success_at_utc": snapshot["published_at_utc"],
            "last_error": None,
            "publish_count": state.get("publish_count", 0) + 1,
            "latest_snapshot": snapshot,
        }
    )
    return state


def handle_signal(_signum: int, _frame: Any) -> None:
    global STOP
    STOP = True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--poll-seconds", type=int, default=120)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    if args.poll_seconds < 30:
        parser.error("--poll-seconds must be at least 30")

    PUBLICATION_DIR.mkdir(parents=True, exist_ok=True)
    lock_handle = LOCK_PATH.open("a+")
    try:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("Another publisher already holds the lock", flush=True)
        return 2

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    started = utc_now()
    atomic_json(
        PID_PATH,
        {
            "pid": os.getpid(),
            "status": "running",
            "started_at_utc": started,
            "poll_seconds": args.poll_seconds,
            "state_path": str(STATE_PATH),
            "log_path": str(PUBLICATION_DIR / "publisher.log"),
            "gallery_url": GALLERY_URL,
        },
    )
    state = read_json(STATE_PATH, {})
    state["poll_seconds"] = args.poll_seconds
    state["status"] = "running"
    state["publisher_pid"] = os.getpid()
    state["publisher_started_at_utc"] = started
    atomic_json(STATE_PATH, state)
    print(f"[{utc_now()}] publisher started pid={os.getpid()} poll={args.poll_seconds}s", flush=True)

    while not STOP:
        try:
            fingerprint = input_fingerprint()
            if fingerprint != state.get("last_input_fingerprint"):
                state = publish_once(state, fingerprint)
                atomic_json(STATE_PATH, state)
                latest = state["latest_snapshot"]
                print(
                    f"[{utc_now()}] published accepted={latest['accepted_case_count']} "
                    f"records={latest['generation_record_count']} statuses={latest['status_counts']} "
                    f"changed={latest['s3_verification']['changed_object_count']}",
                    flush=True,
                )
        except Exception as exc:
            state.update(
                {
                    "version": "camera-v2-gallery-publisher-state-v1",
                    "status": "retrying_after_error",
                    "last_error": {"at_utc": utc_now(), "type": type(exc).__name__, "message": str(exc)[:2000]},
                    "error_count": state.get("error_count", 0) + 1,
                }
            )
            atomic_json(STATE_PATH, state)
            print(f"[{utc_now()}] publish error: {type(exc).__name__}: {str(exc)[:2000]}", flush=True)
        if args.once:
            break
        deadline = time.monotonic() + args.poll_seconds
        while not STOP and time.monotonic() < deadline:
            time.sleep(min(1, deadline - time.monotonic()))

    state["status"] = "stopped"
    state["stopped_at_utc"] = utc_now()
    atomic_json(STATE_PATH, state)
    pid_record = read_json(PID_PATH, {})
    pid_record["status"] = "stopped"
    pid_record["stopped_at_utc"] = state["stopped_at_utc"]
    atomic_json(PID_PATH, pid_record)
    print(f"[{utc_now()}] publisher stopped", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
