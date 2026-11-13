#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3>=1.34", "requests>=2.31"]
# ///
"""Resumable HP16 runner for the frozen V5 top-96 prompt set."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import stat
import sys
import threading
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import boto3
import requests


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SOURCE = PROJECT / "eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028/data/prompts_top6_96.json"
SOURCE_INPUTS = PROJECT / "eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028/inputs"
EXPECTED_SOURCE_SHA256 = "882f60c772fff18b3a008567e46ff112e42af141001fa22bdc5277716497b804"
BASE_URL = "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev"
S3_BUCKET = "foundry-hp-enterprise-adobe-assets"
S3_PREFIX = "eval_sets/hp_lifestyle_dual_source_v5_hp16_baseline_20261029"
DEVICE_MAP = {
    "cashmere": "cashmere_x",
    "elitebook": "elitebook_13",
    "tassel": "tassel",
    "magic": "adf_printer",
}
ARTIFACTS = (
    "1_hero_white.png",
    "1_hero_mask.png",
    "2_scene.png",
    "3_ibl.exr",
    "3_ibl_preview.png",
    "4_backplate.png",
    "6_relight_3d.png",
)
REQUIRED_STAGES = ("hero", "scene", "ibl", "backplate", "relight")
_WRITE_LOCK = threading.Lock()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_json(path: Path, value: Any, *, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if mode is not None:
        temporary.chmod(mode)
    os.replace(temporary, path)


def safe_slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")


def read_token(path: Path | None) -> str:
    token = os.environ.get("S3D_BEARER_TOKEN", "").strip()
    if not token and path is not None:
        if not path.exists():
            raise RuntimeError(f"S3D token file does not exist: {path}")
        permissions = stat.S_IMODE(path.stat().st_mode)
        if permissions & 0o077:
            raise RuntimeError(f"S3D token file must be mode 600: {path}")
        token = path.read_text(encoding="utf-8").strip()
    if not token:
        raise RuntimeError("S3D_BEARER_TOKEN or --token-file is required")
    return token


def load_tasks() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    raw = SOURCE.read_bytes()
    actual_hash = sha256_bytes(raw)
    if actual_hash != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(f"frozen source hash mismatch: {actual_hash}")
    document = json.loads(raw)
    rows = document.get("prompts")
    if not isinstance(rows, list) or len(rows) != 96:
        raise RuntimeError("frozen source must contain exactly 96 prompts")
    if len({row.get("prompt_key") for row in rows}) != 96:
        raise RuntimeError("prompt keys must be unique")

    tasks: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        device = row.get("device_id")
        camera = row.get("source_camera_name")
        prompt = row.get("text")
        if device not in DEVICE_MAP or not all(isinstance(item, str) and item.strip() for item in (camera, prompt)):
            raise RuntimeError(f"invalid frozen row {index}")
        input_path = SOURCE_INPUTS / f"{device}__{row['camera_tag']}.json"
        if not input_path.exists():
            raise RuntimeError(f"missing source input: {input_path}")
        source_input = json.loads(input_path.read_text(encoding="utf-8"))
        slug = f"{index:03d}__{safe_slug(row['prompt_key'])}"
        tasks.append(
            {
                "index": index,
                "slug": slug,
                "prompt_key": row["prompt_key"],
                "digitalTwinId": DEVICE_MAP[device],
                "cameraId": camera,
                "prompt": prompt,
                "prompt_sha256": sha256_bytes(prompt.encode("utf-8")),
                "v5": row,
                "source_input": source_input,
                "source_input_path": str(input_path),
            }
        )
    return tasks, document


def fetch_catalog() -> dict[str, Any]:
    response = requests.get(f"{BASE_URL}/api/catalog", timeout=90)
    response.raise_for_status()
    return response.json()


def validate_catalog(tasks: list[dict[str, Any]], catalog: dict[str, Any]) -> None:
    twins = catalog.get("digitalTwins")
    if not isinstance(twins, list):
        raise RuntimeError("endpoint catalog has no digitalTwins list")
    cameras = {
        twin.get("id"): {camera.get("id") for camera in twin.get("cameras", [])}
        for twin in twins
        if isinstance(twin, dict)
    }
    missing = sorted(
        {
            (task["digitalTwinId"], task["cameraId"])
            for task in tasks
            if task["digitalTwinId"] not in cameras or task["cameraId"] not in cameras[task["digitalTwinId"]]
        }
    )
    if missing:
        raise RuntimeError(f"endpoint catalog is missing requested mappings: {missing}")


def load_cookies(session: requests.Session, path: Path) -> None:
    if not path.exists():
        return
    for cookie in json.loads(path.read_text(encoding="utf-8")):
        session.cookies.set(
            cookie["name"], cookie["value"], domain=cookie.get("domain"), path=cookie.get("path", "/")
        )


def save_cookies(session: requests.Session, path: Path) -> None:
    values = [
        {"name": c.name, "value": c.value, "domain": c.domain, "path": c.path}
        for c in session.cookies
    ]
    atomic_json(path, values, mode=0o600)


def authenticate(session: requests.Session, token: str, cookie_path: Path) -> str:
    load_cookies(session, cookie_path)
    response = session.get(f"{BASE_URL}/api/credentials", timeout=90)
    response.raise_for_status()
    csrf = response.json()["csrfToken"]
    headers = {"Origin": BASE_URL, "x-hp12-csrf": csrf}
    response = session.post(
        f"{BASE_URL}/api/credentials",
        headers=headers,
        json={"s3dBearerToken": token},
        timeout=90,
    )
    response.raise_for_status()
    state = response.json().get("services", {}).get("s3d", {}).get("state")
    if state != "valid":
        raise RuntimeError(f"S3D credential state is {state!r}, expected 'valid'")
    save_cookies(session, cookie_path)
    return csrf


class Publisher:
    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled
        self.client = boto3.client("s3", region_name="us-west-2") if enabled else None

    def upload(self, path: Path, key: str, content_type: str | None = None) -> dict[str, Any]:
        if not self.enabled:
            return {"uploaded": False, "s3_uri": None}
        extra = {"ContentType": content_type} if content_type else {}
        last_error: Exception | None = None
        for attempt in range(1, 6):
            try:
                assert self.client is not None
                self.client.upload_file(str(path), S3_BUCKET, key, ExtraArgs=extra or None)
                head = self.client.head_object(Bucket=S3_BUCKET, Key=key)
                if head["ContentLength"] != path.stat().st_size:
                    raise RuntimeError("uploaded byte count mismatch")
                return {
                    "uploaded": True,
                    "s3_uri": f"s3://{S3_BUCKET}/{key}",
                    "bytes": head["ContentLength"],
                    "etag": head.get("ETag", "").strip('"'),
                }
            except Exception as exc:  # Keep the final class only; never provider bodies.
                last_error = exc
                if attempt < 5:
                    time.sleep(min(2**attempt, 30))
        raise RuntimeError(f"S3 upload failed after 5 attempts: {type(last_error).__name__}")


def record_path(state_root: Path, task: dict[str, Any]) -> Path:
    return state_root / "records" / f"{task['slug']}.json"


def read_record(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_record(path: Path, value: dict[str, Any]) -> None:
    value["updated_at_utc"] = utc_now()
    atomic_json(path, value)


def stage_success(manifest: dict[str, Any]) -> bool:
    stages = manifest.get("stages", {})
    return all(stages.get(name, {}).get("status") == "done" for name in REQUIRED_STAGES)


def process_task(
    task: dict[str, Any],
    *,
    session: requests.Session,
    headers: dict[str, str],
    state_root: Path,
    artifact_root: Path,
    publisher: Publisher,
    poll_seconds: float,
    timeout_seconds: int,
) -> dict[str, Any]:
    path = record_path(state_root, task)
    record = read_record(path) or {
        "version": "hp16-v5-baseline-record-v1",
        "task": task,
        "request": {
            "digitalTwinId": task["digitalTwinId"],
            "cameraId": task["cameraId"],
            "prompt": task["prompt"],
        },
        "created_at_utc": utc_now(),
        "status": "prepared",
        "job_id": None,
        "manifest": None,
        "artifacts": {},
        "error": None,
    }
    if record.get("status") == "complete":
        valid = all(
            Path(info["local_path"]).is_file()
            and sha256_file(Path(info["local_path"])) == info["sha256"]
            and (not publisher.enabled or info.get("publication", {}).get("uploaded"))
            for info in record.get("artifacts", {}).values()
        )
        if valid and set(record.get("artifacts", {})) == set(ARTIFACTS):
            return record
        record["status"] = "artifact_recovery"
        write_record(path, record)
    if record.get("status") == "submit_ambiguous":
        return record

    job_id = record.get("job_id")
    if not job_id:
        record["status"] = "submitting"
        write_record(path, record)
        try:
            response = session.post(
                f"{BASE_URL}/api/run", headers=headers, json=record["request"], timeout=90
            )
            response.raise_for_status()
            job_id = response.json()["jobId"]
        except requests.RequestException as exc:
            record["status"] = "submit_ambiguous"
            record["error"] = {"code": "submit_ambiguous", "type": type(exc).__name__}
            write_record(path, record)
            return record
        except (KeyError, ValueError) as exc:
            # A successful HTTP response without a usable job ID is still ambiguous:
            # the server may have accepted the request. Never resubmit automatically.
            record["status"] = "submit_ambiguous"
            record["error"] = {"code": "submit_ambiguous_response", "type": type(exc).__name__}
            write_record(path, record)
            return record
        record["job_id"] = job_id
        record["status"] = "submitted"
        record["error"] = None
        write_record(path, record)

    deadline = time.monotonic() + timeout_seconds
    while True:
        try:
            response = session.get(f"{BASE_URL}/api/jobs/{job_id}", headers=headers, timeout=90)
            response.raise_for_status()
            manifest = response.json()
        except (requests.RequestException, ValueError) as exc:
            record["status"] = "poll_interrupted"
            record["error"] = {"code": "poll_interrupted", "type": type(exc).__name__}
            write_record(path, record)
            return record
        record["manifest"] = manifest
        record["status"] = "finished" if manifest.get("done") is True else "running"
        write_record(path, record)
        if manifest.get("done") is True:
            break
        if time.monotonic() >= deadline:
            record["status"] = "poll_timeout"
            record["error"] = {"code": "poll_timeout", "timeout_seconds": timeout_seconds}
            write_record(path, record)
            return record
        time.sleep(poll_seconds)

    if not stage_success(manifest):
        record["status"] = "stage_failure"
        record["error"] = {
            "code": "stage_failure",
            "stages": {
                name: {
                    "status": manifest.get("stages", {}).get(name, {}).get("status"),
                    "error": manifest.get("stages", {}).get(name, {}).get("error"),
                }
                for name in REQUIRED_STAGES
            },
        }
        write_record(path, record)
        return record

    job_dir = artifact_root / task["slug"] / str(job_id)
    job_dir.mkdir(parents=True, exist_ok=True)
    for filename in ARTIFACTS:
        destination = job_dir / filename
        if not destination.exists() or destination.stat().st_size == 0:
            try:
                response = session.get(
                    f"{BASE_URL}/api/jobs/{job_id}/artifacts/{filename}",
                    headers=headers,
                    timeout=180,
                )
                response.raise_for_status()
                temporary = destination.with_suffix(destination.suffix + ".part")
                temporary.write_bytes(response.content)
                if temporary.stat().st_size == 0:
                    raise RuntimeError("empty artifact")
                os.replace(temporary, destination)
            except Exception as exc:
                record["status"] = "artifact_failure"
                record["error"] = {
                    "code": "artifact_failure",
                    "artifact": filename,
                    "type": type(exc).__name__,
                }
                write_record(path, record)
                return record
        if filename.endswith(".png") and destination.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            record["status"] = "artifact_failure"
            record["error"] = {"code": "invalid_png", "artifact": filename}
            write_record(path, record)
            return record
        artifact_info = {
            "local_path": str(destination),
            "bytes": destination.stat().st_size,
            "sha256": sha256_file(destination),
        }
        key = f"{S3_PREFIX}/artifacts/{task['slug']}/{job_id}/{filename}"
        content_type = "image/png" if filename.endswith(".png") else "image/x-exr"
        try:
            artifact_info["publication"] = publisher.upload(destination, key, content_type)
        except RuntimeError as exc:
            record["artifacts"][filename] = artifact_info
            record["status"] = "publication_failure"
            record["error"] = {"code": "publication_failure", "artifact": filename, "detail": str(exc)}
            write_record(path, record)
            return record
        record["artifacts"][filename] = artifact_info
        write_record(path, record)

    record["status"] = "complete"
    record["error"] = None
    record["completed_at_utc"] = utc_now()
    write_record(path, record)
    record_key = f"{S3_PREFIX}/records/{task['slug']}.json"
    if publisher.enabled:
        publisher.upload(path, record_key, "application/json")
    return record


def build_summary(state_root: Path, tasks: list[dict[str, Any]], catalog: dict[str, Any]) -> dict[str, Any]:
    records = [read_record(record_path(state_root, task)) for task in tasks]
    statuses = Counter((record or {}).get("status", "not_started") for record in records)
    return {
        "version": "hp16-v5-baseline-summary-v1",
        "as_of_utc": utc_now(),
        "endpoint": BASE_URL,
        "source_path": str(SOURCE),
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "tasks": len(tasks),
        "status_counts": dict(sorted(statuses.items())),
        "complete": statuses.get("complete", 0) == len(tasks),
        "s3_prefix": f"s3://{S3_BUCKET}/{S3_PREFIX}/",
        "endpoint_catalog": {
            "referenceCount": catalog.get("referenceCount"),
            "rewriterVersion": catalog.get("rewriterVersion"),
            "generator": catalog.get("generator"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--token-file", type=Path, default=Path("/tmp/hp16_s3d_token.txt"))
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--poll-seconds", type=float, default=5)
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    parser.add_argument(
        "--state-root",
        type=Path,
        default=PROJECT / "local_data/generation_runs/hp_lifestyle_dual_source_v5_hp16_baseline_20261029",
    )
    parser.add_argument(
        "--artifact-root",
        type=Path,
        default=Path("/mnt/localssd/hp_lifestyle_pipeline/hp16_v5_baseline_20261029"),
    )
    parser.add_argument("--no-upload", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        raise SystemExit("--workers must be between 1 and 8")
    if args.limit is not None and args.limit < 1:
        raise SystemExit("--limit must be positive")

    tasks, source_document = load_tasks()
    if args.limit is not None:
        tasks = tasks[: args.limit]
    catalog = fetch_catalog()
    validate_catalog(tasks, catalog)
    validation = {
        "as_of_utc": utc_now(),
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "source_version": source_document.get("version"),
        "selected_tasks": len(tasks),
        "device_counts": dict(sorted(Counter(task["digitalTwinId"] for task in tasks).items())),
        "mapping_valid": True,
        "endpoint": BASE_URL,
        "endpoint_catalog": {
            "referenceCount": catalog.get("referenceCount"),
            "rewriterVersion": catalog.get("rewriterVersion"),
            "generator": catalog.get("generator"),
        },
    }
    atomic_json(HERE / "input_validation.json", validation)
    print(json.dumps(validation, indent=2))
    if args.validate_only:
        return 0

    token = read_token(args.token_file)
    args.state_root.mkdir(parents=True, exist_ok=True)
    args.artifact_root.mkdir(parents=True, exist_ok=True)
    publisher = Publisher(not args.no_upload)

    worker_tasks = [[] for _ in range(args.workers)]
    for position, task in enumerate(tasks):
        worker_tasks[position % args.workers].append(task)

    def worker(worker_index: int) -> list[dict[str, Any]]:
        session = requests.Session()
        cookie_path = args.state_root / "sessions" / f"worker_{worker_index}.cookies.json"
        csrf = authenticate(session, token, cookie_path)
        headers = {"Origin": BASE_URL, "x-hp12-csrf": csrf}
        results = []
        for task in worker_tasks[worker_index]:
            result = process_task(
                task,
                session=session,
                headers=headers,
                state_root=args.state_root,
                artifact_root=args.artifact_root,
                publisher=publisher,
                poll_seconds=args.poll_seconds,
                timeout_seconds=args.timeout_seconds,
            )
            results.append(result)
            with _WRITE_LOCK:
                summary = build_summary(args.state_root, tasks, catalog)
                atomic_json(args.state_root / "summary.json", summary)
                atomic_json(HERE / "run_summary.json", summary)
                if publisher.enabled:
                    publisher.upload(args.state_root / "summary.json", f"{S3_PREFIX}/summary.json", "application/json")
        save_cookies(session, cookie_path)
        return results

    failures: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(worker, index): index for index in range(args.workers)}
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                failures.append(f"worker {futures[future]}: {type(exc).__name__}: {exc}")

    summary = build_summary(args.state_root, tasks, catalog)
    summary["worker_errors"] = failures
    atomic_json(args.state_root / "summary.json", summary)
    atomic_json(HERE / "run_summary.json", summary)
    print(json.dumps(summary, indent=2))
    return 0 if summary["complete"] and not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
