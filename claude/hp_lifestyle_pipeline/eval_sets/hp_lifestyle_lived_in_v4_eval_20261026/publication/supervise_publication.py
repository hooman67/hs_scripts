#!/usr/bin/env python3
"""Publish V4 only after the complete candidate bank and selections are approved."""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import importlib.util
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
RUN_ROOT = PROJECT_ROOT / "local_data/generation_runs/hp_lifestyle_lived_in_v4_eval_20261026"
BUILD_SCRIPT = EVAL_ROOT / "build_gallery.py"
PUBLICATION_DIR = EVAL_ROOT / "publication"
PUBLICATION_PATH = PUBLICATION_DIR / "publication.json"
HISTORY_PATH = PUBLICATION_DIR / "snapshots.jsonl"
STATE_PATH = PUBLICATION_DIR / "supervisor_state.json"
PID_PATH = PUBLICATION_DIR / "publisher.pid.json"
LOCK_PATH = PUBLICATION_DIR / "publisher.lock"
LOG_PATH = PUBLICATION_DIR / "publisher.log"
UI_VALIDATION_PATH = PUBLICATION_DIR / "ui_validation.json"
SMOKE_REVIEW_PATHS = (EVAL_ROOT / "smoke_review.json", RUN_ROOT / "smoke_review.json")
PROMPT_EXPORT_PATHS = (EVAL_ROOT / "generation_prompts.json", EVAL_ROOT / "generation_prompts_selected.json")
AWS_ENV_PATH = Path("/home/colligo/.claude/hshariati/aws_creds.env")
AWS_HELPER = Path("/home/colligo/.claude/scripts/foundry_aws_creds.py")
AWS_BROKER = "https://foundry-aws-pluto.adobe.io/iam/credentials/aws"
REGION = "us-west-2"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/generated_v4"
GALLERY_URL = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}/gallery/index.html"
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
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_json(path: Path, default: Any = None) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def load_builder_module():
    spec = importlib.util.spec_from_file_location("v4_gallery_builder", BUILD_SCRIPT)
    if not spec or not spec.loader:
        raise RuntimeError("Unable to load V4 gallery builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
        if key.strip().startswith("AWS_"):
            values = shlex.split(raw_value, posix=True)
            os.environ[key.strip()] = values[0] if values else ""


def refresh_aws_credentials() -> None:
    result = subprocess.run(
        ["uv", "run", "--script", str(AWS_HELPER), "--endpoint", AWS_BROKER],
        cwd=str(PROJECT_ROOT), stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, timeout=120, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"AWS credential broker failed with exit {result.returncode}")
    load_aws_env()


def aws(arguments: list[str], retry: bool = True) -> subprocess.CompletedProcess[str]:
    load_aws_env()
    result = subprocess.run(["aws", *arguments], cwd=str(PROJECT_ROOT), text=True, capture_output=True, check=False)
    if result.returncode == 0:
        return result
    combined = f"{result.stdout}\n{result.stderr}"
    if retry and any(marker in combined for marker in ("ExpiredToken", "Unable to locate credentials", "InvalidClientTokenId", "RequestExpired")):
        refresh_aws_credentials()
        return aws(arguments, retry=False)
    raise RuntimeError(f"AWS CLI failed ({result.returncode}): {result.stderr.strip()[:1000]}")


def object_spec(path: Path, key: str, content_type: str) -> dict[str, Any]:
    return {"path": str(path), "key": key, "bytes": path.stat().st_size, "sha256": sha256_path(path), "content_type": content_type}


def stable_snapshot(path: Path, name: str) -> Path:
    """Freeze a concurrently updated local file before hashing and upload."""
    destination = RUN_ROOT / "publication_inputs" / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
    temporary.write_bytes(path.read_bytes())
    temporary.replace(destination)
    return destination


def content_type(path: Path) -> str:
    return {".png":"image/png", ".jpg":"image/jpeg", ".jpeg":"image/jpeg", ".webp":"image/webp"}.get(path.suffix.lower(), "application/octet-stream")


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
        summary_snapshot = stable_snapshot(summary, "generation_summary.json")
        objects.append(object_spec(summary_snapshot, f"{PREFIX}/generation_summary.json", "application/json"))
    if UI_VALIDATION_PATH.exists():
        objects.append(object_spec(UI_VALIDATION_PATH, f"{PREFIX}/ui_validation.json", "application/json"))
    smoke_reviews = [path for path in SMOKE_REVIEW_PATHS if path.exists()]
    if len(smoke_reviews) > 1 and sha256_path(smoke_reviews[0]) != sha256_path(smoke_reviews[1]):
        raise RuntimeError(f"Conflicting smoke review artifacts: {[str(path) for path in smoke_reviews]}")
    if smoke_reviews:
        objects.append(object_spec(smoke_reviews[0], f"{PREFIX}/smoke_review.json", "application/json"))
    for path in PROMPT_EXPORT_PATHS:
        if path.exists():
            objects.append(object_spec(path, f"{PREFIX}/{path.name}", "application/json"))
    for path in sorted((RUN_ROOT / "assets/references").glob("*.png")):
        objects.append(object_spec(path, f"{PREFIX}/assets/references/{path.name}", "image/png"))
    for path in sorted((RUN_ROOT / "images").glob("*")):
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            objects.append(object_spec(path, f"{PREFIX}/images/{path.name}", content_type(path)))
    return objects


def upload_and_verify(spec: dict[str, Any]) -> None:
    aws(["s3", "cp", spec["path"], f"s3://{BUCKET}/{spec['key']}", "--content-type", spec["content_type"], "--metadata", f"sha256={spec['sha256']}", "--region", REGION, "--only-show-errors"])
    head = json.loads(aws(["s3api", "head-object", "--bucket", BUCKET, "--key", spec["key"], "--region", REGION, "--output", "json"]).stdout)
    if head.get("ContentLength") != spec["bytes"] or head.get("ContentType") != spec["content_type"] or (head.get("Metadata") or {}).get("sha256") != spec["sha256"]:
        raise RuntimeError(f"S3 verification differs for {spec['key']}")


def assert_new_prefix_is_safe(state: dict[str, Any]) -> None:
    if state.get("remote_prefix_initialized"):
        return
    response = json.loads(aws(["s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", f"{PREFIX}/", "--max-keys", "5", "--region", REGION, "--output", "json"]).stdout)
    existing = [item["Key"] for item in response.get("Contents", [])]
    if existing:
        raise RuntimeError(f"New V4 prefix contains unowned objects: {existing}")
    state["remote_prefix_initialized"] = True
    state["remote_prefix_verified_empty_at_utc"] = utc_now()


def input_fingerprint() -> str:
    digest = hashlib.sha256()
    watched = [BUILD_SCRIPT, *(EVAL_ROOT / "gallery").glob("*"), EVAL_ROOT / "manifest.json", EVAL_ROOT / "accepted_prompt_cases.json", EVAL_ROOT / "selection_manifest.json", UI_VALIDATION_PATH, *SMOKE_REVIEW_PATHS, *PROMPT_EXPORT_PATHS]
    for path in watched:
        if path.is_file():
            stat = path.stat(); digest.update(f"{path}:{stat.st_size}:{stat.st_mtime_ns}\n".encode())
    for directory, pattern in ((RUN_ROOT / "records", "*.json"), (RUN_ROOT / "images", "*")):
        for path in sorted(directory.glob(pattern)):
            if path.is_file():
                stat = path.stat(); digest.update(f"{path.name}:{stat.st_size}:{stat.st_mtime_ns}\n".encode())
    summary = RUN_ROOT / "summary.json"
    if summary.exists():
        stat = summary.stat(); digest.update(f"summary:{stat.st_size}:{stat.st_mtime_ns}\n".encode())
    return digest.hexdigest()


def run_builder() -> dict[str, Any]:
    result = subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=str(PROJECT_ROOT), text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"Gallery builder failed ({result.returncode}): {result.stderr[-2000:]}")
    build = read_json(RUN_ROOT / "gallery_build.json")
    statuses = build.get("generation_status_counts", {})
    if not statuses.get("missing", 0) and not statuses.get("pending", 0):
        final_result = subprocess.run([sys.executable, str(BUILD_SCRIPT), "--final"], cwd=str(PROJECT_ROOT), text=True, capture_output=True, check=False)
        if final_result.returncode:
            raise RuntimeError(f"Final gallery validation failed ({final_result.returncode}): {final_result.stderr[-2000:]}")
        build = read_json(RUN_ROOT / "gallery_build.json")
    return build


def append_snapshot(build: dict[str, Any], changed: list[dict[str, Any]]) -> dict[str, Any]:
    snapshot = {
        "published_at_utc": utc_now(), "phase": build["mode"],
        "candidate_count": build["candidate_count"], "selected_count": build["selected_count"],
        "generation_row_count": build["generation_row_count"], "generation_record_count": build["generation_record_count"],
        "generation_status_counts": build["generation_status_counts"], "manifest_sha256": build["manifest_sha256"],
        "accepted_prompt_cases_sha256": build["accepted_prompt_cases_sha256"], "selection_manifest_sha256": build["selection_manifest_sha256"],
        "gallery_artifacts": build["artifacts"],
        "changed_s3_objects": [{k:item[k] for k in ("key","bytes","sha256","content_type")} for item in changed],
        "s3_verification": {"changed_object_count":len(changed), "all_changed_object_sizes_types_and_sha256_metadata_match":True},
        "browser_render_verified": False,
    }
    publication = read_json(PUBLICATION_PATH, {
        "version":"hp-lived-in-v4-publication-v1", "bucket":BUCKET, "prefix":PREFIX,
        "gallery_key":f"{PREFIX}/gallery/index.html", "gallery_url":GALLERY_URL,
        "historical_prefix_overwritten":False, "model_or_image_calls_by_gallery_agent":False,
        "visual_acceptance_recorded_by_publisher":False,
        "snapshots":[],
    })
    publication["status"] = "final" if build["mode"] == "final" else "progressive"
    publication["latest_snapshot"] = snapshot
    publication["snapshots"].append(snapshot)
    atomic_json(PUBLICATION_PATH, publication)
    with HISTORY_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(snapshot, separators=(",", ":")) + "\n"); handle.flush(); os.fsync(handle.fileno())
    return snapshot


def publish_once(state: dict[str, Any], fingerprint: str) -> dict[str, Any]:
    assert_new_prefix_is_safe(state)
    build = run_builder()
    uploaded = state.setdefault("uploaded_objects", {})
    objects = gather_objects()
    changed = [item for item in objects if uploaded.get(item["key"], {}).get("sha256") != item["sha256"]]
    for item in changed:
        upload_and_verify(item); uploaded[item["key"]] = {k:item[k] for k in ("bytes","sha256","content_type")}
    snapshot = append_snapshot(build, changed)
    publication_spec = object_spec(PUBLICATION_PATH, f"{PREFIX}/publication.json", "application/json")
    upload_and_verify(publication_spec)
    uploaded[publication_spec["key"]] = {k:publication_spec[k] for k in ("bytes","sha256","content_type")}
    state.update({"status":"complete" if snapshot["phase"] == "final" else "running", "last_input_fingerprint":fingerprint, "last_success_at_utc":snapshot["published_at_utc"], "last_error":None, "publish_count":state.get("publish_count",0)+1, "latest_snapshot":snapshot})
    if snapshot["phase"] == "final":
        state["completed_at_utc"] = snapshot["published_at_utc"]
    return state


def handle_signal(_signum: int, _frame: Any) -> None:
    global STOP
    STOP = True


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--poll-seconds", type=int, default=120); parser.add_argument("--once", action="store_true"); args = parser.parse_args()
    if args.poll_seconds < 30: parser.error("--poll-seconds must be at least 30")
    PUBLICATION_DIR.mkdir(parents=True, exist_ok=True)
    lock = LOCK_PATH.open("a+")
    try: fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError: print("Another V4 publisher already holds the lock", flush=True); return 2
    signal.signal(signal.SIGTERM, handle_signal); signal.signal(signal.SIGINT, handle_signal)
    started = utc_now(); pid_record = {"pid":os.getpid(), "status":"running", "started_at_utc":started, "poll_seconds":args.poll_seconds, "state_path":str(STATE_PATH), "log_path":str(LOG_PATH), "gallery_url":GALLERY_URL}; atomic_json(PID_PATH,pid_record)
    state = read_json(STATE_PATH, {"version":"hp-lived-in-v4-publisher-state-v1", "publish_count":0, "uploaded_objects":{}})
    if state.get("status") == "complete" and state.get("latest_snapshot", {}).get("phase") == "final":
        pid_record.update({"status":"complete", "completed_at_utc":state.get("completed_at_utc")}); atomic_json(PID_PATH,pid_record)
        print(f"[{utc_now()}] V4 publisher already complete; no work remains", flush=True)
        return 0
    state.pop("stopped_at_utc", None)
    state.pop("completed_at_utc", None)
    state.update({"status":"waiting_for_validated_candidates", "publisher_pid":os.getpid(), "publisher_started_at_utc":started, "poll_seconds":args.poll_seconds, "bucket":BUCKET, "prefix":PREFIX, "gallery_url":GALLERY_URL}); atomic_json(STATE_PATH,state)
    builder = load_builder_module()
    print(f"[{utc_now()}] V4 publisher started pid={os.getpid()} poll={args.poll_seconds}s", flush=True)
    while not STOP:
        try:
            gate = builder.readiness(); state["last_readiness_check_at_utc"] = utc_now(); state["readiness"] = gate
            if not gate["ready"]:
                state["status"] = "waiting_for_validated_candidates"; state["last_error"] = None; atomic_json(STATE_PATH,state)
            else:
                fingerprint = input_fingerprint()
                if fingerprint != state.get("last_input_fingerprint"):
                    state = publish_once(state, fingerprint); atomic_json(STATE_PATH,state)
                    latest=state["latest_snapshot"]; print(f"[{utc_now()}] published candidates={latest['candidate_count']} selected={latest['selected_count']} statuses={latest['generation_status_counts']} changed={latest['s3_verification']['changed_object_count']}", flush=True)
                    if latest["phase"] == "final":
                        break
                else:
                    state.update({"status":"running", "last_error":None}); atomic_json(STATE_PATH,state)
        except Exception as exc:
            state.update({"status":"retrying_after_error", "last_error":{"at_utc":utc_now(),"type":type(exc).__name__,"message":str(exc)[:2000]}, "error_count":state.get("error_count",0)+1}); atomic_json(STATE_PATH,state); print(f"[{utc_now()}] publish error: {type(exc).__name__}: {str(exc)[:2000]}", flush=True)
        if args.once: break
        deadline=time.monotonic()+args.poll_seconds
        while not STOP and time.monotonic()<deadline: time.sleep(min(1,deadline-time.monotonic()))
    if state.get("status") == "complete":
        atomic_json(STATE_PATH,state); pid_record["status"]="complete"; pid_record["completed_at_utc"]=state["completed_at_utc"]; atomic_json(PID_PATH,pid_record); print(f"[{utc_now()}] V4 publisher completed final 108-row publication",flush=True)
    else:
        state["status"]="stopped"; state["stopped_at_utc"]=utc_now(); atomic_json(STATE_PATH,state); pid_record["status"]="stopped"; pid_record["stopped_at_utc"]=state["stopped_at_utc"]; atomic_json(PID_PATH,pid_record); print(f"[{utc_now()}] V4 publisher stopped",flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

