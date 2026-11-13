#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "httpx", "pillow"]
# ///
"""Frozen-input, resumable runner for the HP V6.2 surface-diversity set.

The endpoint contract intentionally matches the validated V6.2 generation run:
POST /api/generate with only digitalTwinId, cameraId, and prompt.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlsplit

import boto3
import httpx
from PIL import Image


BASE_URL = "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev"
EXPECTED_GENERATOR = "GPT Image 2.5 / single reference / no grading"
EXPECTED_REWRITER = (
    "Adobe-Firefly/foundry#4349 / 8c358bc7989c / "
    "unified-blue-scale-v20-text-blue-stage-b-placement-twin-camera-guide-only-no-mask"
)
EXPECTED_PIPELINE_VERSION = "unified-blue-scale-v20-text-blue-stage-b-placement-twin-camera-guide-only-no-mask"
EXPECTED_SCENE_CONTRACT = {
    "textModel": "gpt-6-astra",
    "imageModel": "gpt-image-2.5-sunburst-2026-09-08",
    "size": "2368x1776",
    "refCount": 1,
    "imageCalls": 1,
    "graded": False,
    "imageMaskApplied": False,
    "imageInputOrder": ["hp16_geometry_guide.png"],
}
EXPECTED_COUNT = 160
EXPECTED_SIZE = (2368, 1776)
BUCKET = "foundry-hp-enterprise-adobe-assets"
REGION = "us-west-2"
DEFAULT_PREFIX = "eval_sets/hp_lifestyle_surface_diversity_v6_2_gpt_image2_scene_20261108"
DEFAULT_TWIN_DIR = Path(__file__).resolve().parents[2] / "judge/local_runs/v6_1_placement_assets/twins"
DEVICE_MAP = {
    "cashmere": "cashmere_x",
    "elitebook": "elitebook_13",
    "tassel": "tassel",
    "magic": "adf_printer",
}
DEVICE_ORDER = ("cashmere", "elitebook", "tassel", "magic")
VIEW_ORDER = {
    "cashmere": ("Front_CloseUp", "Back_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
    "elitebook": ("Front_CloseUp", "Back_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
    "tassel": ("Front_CloseUp", "Front_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
    "magic": ("Front_CloseUp", "Front_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
}
THREAD_LOCAL = threading.local()
WRITE_LOCK = threading.Lock()
POLL_SECONDS_MIN = 60
POLL_SECONDS_MAX = 7200
PUBLIC_ROOT_FILES = {
    "catalog.json", "queue_manifest.json", "run_manifest.json", "run_started.json", "summary.json", "twin_manifest.json",
    "final_validation.json", "completion_report.md",
}
PUBLIC_DIRECTORIES = {"images", "jobs", "records", "report", "source", "status", "twins"}
PUBLIC_SUFFIXES = {
    ".css", ".csv", ".html", ".jpeg", ".jpg", ".js", ".json", ".md", ".png", ".svg", ".txt", ".webp",
}
PRIVATE_NAME = re.compile(r"(?:^|[._-])(credential|credentials|creds|private[_-]?key|secret|token)(?:[._-]|$)", re.I)


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(raw.encode("utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def atomic_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    temporary.write_bytes(value)
    os.replace(temporary, path)


def append_journal(run_dir: Path, event: dict[str, Any]) -> None:
    event = {"at_utc": now(), **event}
    with WRITE_LOCK:
        path = run_dir / "journals/events.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())


def slug(row_id: str) -> str:
    return row_id.replace("::", "__").replace("/", "_")


def validate_prompt_document(document: dict[str, Any], prompts_path: Path, expected_sha256: str) -> list[dict[str, Any]]:
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise ValueError("--prompts-sha256 must be a lowercase SHA-256 digest")
    actual_sha = sha256_path(prompts_path)
    if actual_sha != expected_sha256:
        raise ValueError(f"frozen prompt hash mismatch: expected {expected_sha256}, got {actual_sha}")
    prompts = document.get("prompts")
    if not isinstance(prompts, list) or len(prompts) != EXPECTED_COUNT:
        raise ValueError("expected exactly 160 frozen prompts")
    seen: set[str] = set()
    counts: dict[tuple[str, str], int] = {}
    ranks: dict[tuple[str, str], set[int]] = {}
    case_ids: dict[tuple[str, str], set[str]] = {}
    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        key = prompt.get("prompt_key")
        device = prompt.get("device_id")
        camera = prompt.get("source_camera_name")
        raw_rank = prompt.get("bank_rank")
        if isinstance(raw_rank, bool) or not isinstance(raw_rank, int):
            raise ValueError(f"bank_rank must be an integer for {key!r}")
        rank = raw_rank
        text = prompt.get("text")
        case_id = prompt.get("bank_debug_ref")
        if not isinstance(key, str) or key in seen or device not in DEVICE_MAP:
            raise ValueError(f"invalid or duplicate prompt mapping: {key!r}")
        if camera not in VIEW_ORDER[device] or not isinstance(text, str) or not text.strip():
            raise ValueError(f"invalid prompt/camera mapping: {key}")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"missing bank_debug_ref for {key}")
        seen.add(key)
        bank = (device, camera)
        counts[bank] = counts.get(bank, 0) + 1
        ranks.setdefault(bank, set()).add(rank)
        case_ids.setdefault(bank, set()).add(case_id)
        rows.append({
            "row_id": key,
            "row_slug": slug(key),
            "prompt": prompt,
            "device_id": device,
            "digital_twin_id": DEVICE_MAP[device],
            "camera_id": camera,
            "bank_id": case_id,
            "rank": rank,
            "prompt_sha256": sha256_bytes(text.encode("utf-8")),
            "prompt_record_sha256": canonical_sha256(prompt),
        })
    expected_banks = {(device, camera) for device in DEVICE_ORDER for camera in VIEW_ORDER[device]}
    if set(counts) != expected_banks or set(counts.values()) != {10}:
        raise ValueError("expected 16 device/view banks with ten prompts each")
    if any(value != set(range(1, 11)) for value in ranks.values()):
        raise ValueError("every bank must contain ranks 1 through 10")
    if any(len(value) != 1 for value in case_ids.values()) or len({next(iter(value)) for value in case_ids.values()}) != 16:
        raise ValueError("every device/view bank must map to one unique bank_debug_ref")
    return rows


def interleave(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key = {(row["device_id"], row["camera_id"], row["rank"]): row for row in rows}
    ordered: list[dict[str, Any]] = []
    for rank in range(1, 11):
        for wave in range(4):
            for device_index, device in enumerate(DEVICE_ORDER):
                camera = VIEW_ORDER[device][(wave + device_index) % 4]
                ordered.append(by_key[(device, camera, rank)])
    if len(ordered) != EXPECTED_COUNT or len({row["row_id"] for row in ordered}) != EXPECTED_COUNT:
        raise ValueError("Latin-square interleave is incomplete")
    return ordered


def normalize_base_url(value: str) -> str:
    result = value.rstrip("/")
    parsed = urlsplit(result)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.path not in {"", "/"}:
        raise ValueError(f"endpoint base URL must be an HTTP(S) origin: {value!r}")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("endpoint base URL must not contain credentials, a query, or a fragment")
    return result


def validate_digest(value: str | None, label: str) -> None:
    if value is not None and not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError(f"{label} must be a lowercase SHA-256 digest")


def lineage_from_args(args: argparse.Namespace) -> dict[str, Any]:
    base_url = normalize_base_url(args.endpoint_base_url)
    if (not args.expected_generator.strip() or not args.expected_rewriter.strip()
            or not args.expected_pipeline_version.strip() or not args.lineage_label.strip()):
        raise ValueError("generator, rewriter, pipeline version, and lineage label must be non-empty")
    for name in (
        "lineage_patch_sha256", "lineage_runtime_tree_sha256", "lineage_source_manifest_sha256",
        "lineage_deployment_manifest_sha256", "lineage_candidate_config_sha256",
    ):
        validate_digest(getattr(args, name), f"--{name.replace('_', '-')}")
    source_commit = args.lineage_source_commit
    if source_commit is not None and not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("--lineage-source-commit must be a lowercase 40-character Git commit")
    return {
        "label": args.lineage_label,
        "endpoint_base_url": base_url,
        "endpoint": f"{base_url}/api/generate",
        "generator": args.expected_generator,
        "rewriterVersion": args.expected_rewriter,
        "pipelineVersion": args.expected_pipeline_version,
        "source_commit": source_commit,
        "patch_sha256": args.lineage_patch_sha256,
        "runtime_tree_sha256": args.lineage_runtime_tree_sha256,
        "source_manifest_sha256": args.lineage_source_manifest_sha256,
        "deployment_manifest_sha256": args.lineage_deployment_manifest_sha256,
        "candidate_config_sha256": args.lineage_candidate_config_sha256,
        "scene_contract": EXPECTED_SCENE_CONTRACT,
    }


def validate_catalog(
    catalog: dict[str, Any], rows: list[dict[str, Any]],
    expected_generator: str = EXPECTED_GENERATOR, expected_rewriter: str = EXPECTED_REWRITER,
    expected_lineage: dict[str, Any] | None = None,
) -> None:
    if catalog.get("generator") != expected_generator:
        raise ValueError(f"unexpected generator: {catalog.get('generator')!r}")
    if catalog.get("rewriterVersion") != expected_rewriter:
        raise ValueError(f"unexpected rewriterVersion: {catalog.get('rewriterVersion')!r}")
    if expected_lineage and expected_lineage.get("deployment_manifest_sha256"):
        actual = catalog.get("candidateLineage")
        if not isinstance(actual, dict):
            raise ValueError("candidate catalog has no candidateLineage")
        contract = expected_lineage["scene_contract"]
        expected = {
            "candidateId": expected_lineage["label"],
            "sourceCommit": expected_lineage["source_commit"],
            "patchSha256": expected_lineage["patch_sha256"],
            "codeTreeSha256": expected_lineage["runtime_tree_sha256"],
            "candidateManifestSha256": expected_lineage["source_manifest_sha256"],
            "configSha256": expected_lineage["candidate_config_sha256"],
            "deploymentManifestSha256": expected_lineage["deployment_manifest_sha256"],
            "pipelineVersion": expected_lineage["pipelineVersion"],
            "generator": expected_lineage["generator"],
            "rewriterVersion": expected_lineage["rewriterVersion"],
            "textModel": contract["textModel"],
            "imageModel": contract["imageModel"],
        }
        mismatches = {key: {"expected": value, "actual": actual.get(key)}
                      for key, value in expected.items() if actual.get(key) != value}
        image_settings = actual.get("imageSettings") or {}
        settings_expected = {"operation": "images.edit", "count": 1, "size": contract["size"],
                             "inputs": "one generated geometry guide", "mask": False}
        for key, value in settings_expected.items():
            if image_settings.get(key) != value:
                mismatches[f"imageSettings.{key}"] = {"expected": value, "actual": image_settings.get(key)}
        if mismatches:
            raise ValueError(f"candidate catalog lineage mismatch: {json.dumps(mismatches, sort_keys=True)}")
    twins = {item["id"]: item for item in catalog.get("digitalTwins", [])}
    for row in rows:
        twin = twins.get(row["digital_twin_id"])
        cameras = {item["id"] for item in (twin or {}).get("cameras", [])}
        if not twin or row["camera_id"] not in cameras:
            raise ValueError(f"missing live twin/camera mapping for {row['row_id']}")


def endpoint_client(base_url: str = BASE_URL) -> tuple[httpx.Client, str]:
    base_url = normalize_base_url(base_url)
    existing = getattr(THREAD_LOCAL, "endpoint", None)
    csrf = getattr(THREAD_LOCAL, "csrf", None)
    existing_base_url = getattr(THREAD_LOCAL, "endpoint_base_url", None)
    if existing is None or not csrf or existing_base_url != base_url:
        if existing is not None:
            existing.close()
        existing = httpx.Client(timeout=httpx.Timeout(60.0, connect=30.0), follow_redirects=True)
        response = existing.get(f"{base_url}/api/credentials")
        response.raise_for_status()
        csrf = response.json()["csrfToken"]
        THREAD_LOCAL.endpoint = existing
        THREAD_LOCAL.csrf = csrf
        THREAD_LOCAL.endpoint_base_url = base_url
    return existing, csrf


def endpoint_url(value: Any, label: str, base_url: str = BASE_URL) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"endpoint response has no {label}")
    base_url = normalize_base_url(base_url)
    resolved = urljoin(f"{base_url}/", value)
    expected, actual = urlsplit(base_url), urlsplit(resolved)
    if (actual.scheme, actual.netloc) != (expected.scheme, expected.netloc):
        raise ValueError(f"endpoint response returned a cross-origin {label}")
    return resolved


def validate_scene_detail(
    detail: dict[str, Any], row: dict[str, Any], lineage: dict[str, Any],
    image_input_order_evidence: dict[str, Any] | None = None,
) -> None:
    expected = {
        "rewriterVersion": lineage["rewriterVersion"],
        "pipelineVersion": lineage["pipelineVersion"],
        "originalPrompt": row["prompt"]["text"],
        **lineage["scene_contract"],
    }
    mismatches: dict[str, Any] = {}
    for key, value in expected.items():
        actual = detail.get(key)
        if actual == value:
            continue
        if (key == "imageInputOrder" and key not in detail
                and (image_input_order_evidence or {}).get("proven_order") == value):
            continue
        mismatches[key] = {"expected": value, "actual": actual}
    if mismatches:
        raise ValueError(f"scene provenance mismatch for {row['row_id']}: {json.dumps(mismatches, sort_keys=True)}")


DEBUG_IMAGE_CALL_KEYS = {
    "kind", "model", "size", "quality", "outputFormat", "background", "count", "mask",
    "promptSha256", "guideSha256", "outputSha256",
}


def validate_debug_image_input_evidence(
    debug: dict[str, Any], guide_sha256: str, row: dict[str, Any], job: dict[str, Any],
    final_status: dict[str, Any], lineage: dict[str, Any],
) -> dict[str, Any]:
    """Prove guide-only image input when an older scene summary omits imageInputOrder."""
    expected_request = {
        "digitalTwinId": row["digital_twin_id"], "cameraId": row["camera_id"],
        "prompt": row["prompt"]["text"],
    }
    debug_job = debug.get("job") or {}
    debug_status = debug.get("status") or {}
    expected_job_id = str(job.get("submit_response", {}).get("jobId"))
    identity_mismatches = {}
    for label, actual in (
        ("job.jobId", debug_job.get("jobId")),
        ("status.jobId", debug_status.get("jobId")),
        ("final_status.jobId", final_status.get("jobId")),
    ):
        if str(actual) != expected_job_id:
            identity_mismatches[label] = {"expected": expected_job_id, "actual": actual}
    if debug_job.get("request") != expected_request:
        identity_mismatches["job.request"] = {"expected": expected_request, "actual": debug_job.get("request")}
    expected_request_sha = canonical_sha256(expected_request)
    if debug_job.get("requestSha256") != expected_request_sha:
        identity_mismatches["job.requestSha256"] = {
            "expected": expected_request_sha, "actual": debug_job.get("requestSha256")}
    if identity_mismatches:
        raise ValueError(
            f"debug image-input identity mismatch for {row['row_id']}: "
            f"{json.dumps(identity_mismatches, sort_keys=True)}"
        )

    calls = debug.get("calls")
    if not isinstance(calls, list):
        raise ValueError(f"debug image-input evidence has no calls list for {row['row_id']}")
    image_calls = [call for call in calls if isinstance(call, dict) and call.get("kind") == "image_edit"]
    if len(image_calls) != 1:
        raise ValueError(f"debug image-input evidence expected exactly one image_edit for {row['row_id']}")
    call = image_calls[0]
    if set(call) != DEBUG_IMAGE_CALL_KEYS:
        raise ValueError(
            f"debug image-input call fields mismatch for {row['row_id']}: "
            f"expected={sorted(DEBUG_IMAGE_CALL_KEYS)} actual={sorted(call)}"
        )
    contract = lineage["scene_contract"]
    expected_call = {
        "model": contract["imageModel"], "size": contract["size"], "quality": "high",
        "outputFormat": "png", "background": "opaque", "count": 1, "mask": False,
        "guideSha256": guide_sha256, "outputSha256": final_status.get("imageSha256"),
    }
    call_mismatches = {
        key: {"expected": value, "actual": call.get(key)}
        for key, value in expected_call.items() if call.get(key) != value
    }
    if not re.fullmatch(r"[0-9a-f]{64}", str(call.get("promptSha256", ""))):
        call_mismatches["promptSha256"] = {"expected": "lowercase SHA-256", "actual": call.get("promptSha256")}
    if call_mismatches:
        raise ValueError(
            f"debug image-input call mismatch for {row['row_id']}: "
            f"{json.dumps(call_mismatches, sort_keys=True)}"
        )
    return {
        "method": "endpoint_debug_exact_single_image_edit_and_fetched_guide_hash",
        "proven_order": contract["imageInputOrder"],
        "guide_sha256": guide_sha256,
        "output_sha256": call["outputSha256"],
        "image_call": call,
    }


def paths(run_dir: Path, row: dict[str, Any]) -> dict[str, Path]:
    name = row["row_slug"]
    return {
        "job": run_dir / "jobs" / f"{name}.json",
        "record": run_dir / "records" / f"{name}.json",
        "status": run_dir / "status" / f"{name}.json",
        "image": run_dir / "images" / f"{name}.png",
        "debug": run_dir / "status" / f"{name}.debug.json",
        "calls": run_dir / "status" / f"{name}.calls.json",
        "guide": run_dir / "status" / f"{name}.geometry_guide.png",
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def valid_completed_record(run_dir: Path, row: dict[str, Any]) -> dict[str, Any] | None:
    item = paths(run_dir, row)
    if not item["record"].is_file() or not item["image"].is_file():
        return None
    record = load_json(item["record"])
    if (record.get("status") != "done" or record.get("row_id") != row["row_id"]
            or record.get("prompt_sha256") != row["prompt_sha256"]
            or record.get("image_sha256") != sha256_path(item["image"])):
        return None
    manifest_path = run_dir / "run_manifest.json"
    if manifest_path.is_file():
        manifest = load_json(manifest_path)
        if manifest.get("schema_version", 0) >= 3 and (
            record.get("run_sha256") != manifest.get("run_sha256")
            or record.get("catalog_sha256") != manifest.get("catalog_sha256")
            or record.get("lineage") != manifest.get("lineage")
        ):
            return None
    return record


def submit(
    run_dir: Path, row: dict[str, Any], catalog_sha256: str, run_sha256: str,
    lineage: dict[str, Any],
) -> dict[str, Any]:
    base_url = lineage["endpoint_base_url"]
    endpoint, csrf = endpoint_client(base_url)
    payload = {"digitalTwinId": row["digital_twin_id"], "cameraId": row["camera_id"], "prompt": row["prompt"]["text"]}
    append_journal(run_dir, {"event": "submit_started", "row_id": row["row_id"], "request_sha256": canonical_sha256(payload)})
    response = endpoint.post(f"{base_url}/api/generate", json=payload, headers={"Origin": base_url, "x-hp12-csrf": csrf})
    response.raise_for_status()
    submitted = response.json()
    if not isinstance(submitted.get("jobId"), (str, int)):
        raise ValueError("endpoint response has no jobId")
    job = {
        "schema_version": 3, "row_id": row["row_id"], "submitted_at_utc": now(), "request": payload,
        "request_sha256": canonical_sha256(payload), "catalog_sha256": catalog_sha256,
        "run_sha256": run_sha256, "lineage": lineage,
        "submit_response": submitted, "status_url": endpoint_url(submitted.get("statusUrl"), "statusUrl", base_url),
        "image_url": endpoint_url(submitted.get("imageUrl"), "imageUrl", base_url),
    }
    atomic_json(paths(run_dir, row)["job"], job)
    append_journal(run_dir, {"event": "submit_saved", "row_id": row["row_id"], "job_id": submitted.get("jobId")})
    return job


def process(
    run_dir: Path, row: dict[str, Any], catalog_sha256: str, poll_seconds: int,
    run_sha256: str, lineage: dict[str, Any],
) -> dict[str, Any]:
    completed = valid_completed_record(run_dir, row)
    if completed:
        append_journal(run_dir, {"event": "resume_completed", "row_id": row["row_id"]})
        return completed
    item = paths(run_dir, row)
    if item["job"].is_file():
        job = load_json(item["job"])
        expected_request = {"digitalTwinId": row["digital_twin_id"], "cameraId": row["camera_id"], "prompt": row["prompt"]["text"]}
        if (job.get("row_id") != row["row_id"] or job.get("request") != expected_request
                or job.get("request_sha256") != canonical_sha256(expected_request)
                or job.get("catalog_sha256") != catalog_sha256 or job.get("run_sha256") != run_sha256
                or job.get("lineage") != lineage):
            raise ValueError(f"saved job identity mismatch: {row['row_id']}")
        endpoint_url(job.get("status_url"), "saved status_url", lineage["endpoint_base_url"])
        endpoint_url(job.get("image_url"), "saved image_url", lineage["endpoint_base_url"])
        append_journal(run_dir, {"event": "resume_job", "row_id": row["row_id"]})
    else:
        job = submit(run_dir, row, catalog_sha256, run_sha256, lineage)
    endpoint, _ = endpoint_client(lineage["endpoint_base_url"])
    deadline = time.monotonic() + poll_seconds
    poll_count = 0
    final_status: dict[str, Any] | None = None
    while time.monotonic() < deadline:
        poll_count += 1
        try:
            remaining = deadline - time.monotonic()
            response = endpoint.get(job["status_url"], timeout=max(1.0, min(60.0, remaining)))
            response.raise_for_status()
            status = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            append_journal(run_dir, {"event": "poll_retry", "row_id": row["row_id"], "poll": poll_count, "error": f"{type(exc).__name__}: {exc}"})
            time.sleep(max(0.0, min(5.0, deadline - time.monotonic())))
            continue
        if status.get("done"):
            final_status = status
            break
        time.sleep(max(0.0, min(5.0, deadline - time.monotonic())))
    if final_status is None:
        raise TimeoutError(f"polling timed out for {row['row_id']}; resume the saved job")
    atomic_json(item["status"], final_status)
    stages = final_status.get("stages", {})
    scene = stages.get("scene", {})
    if scene.get("status") != "done" or not scene.get("has_image"):
        record = {"schema_version": 3, "row_id": row["row_id"], "status": "failed", "completed_at_utc": now(),
                  "prompt_sha256": row["prompt_sha256"], "job_id": final_status.get("jobId"),
                  "error": scene.get("error") or "scene stage did not return an image", "final_status": final_status,
                  "run_sha256": run_sha256, "catalog_sha256": catalog_sha256, "lineage": lineage}
        atomic_json(item["record"], record)
        return record
    for skipped in ("ibl", "backplate", "recomposite", "relight"):
        if stages.get(skipped, {}).get("status") != "skipped":
            raise ValueError(f"{row['row_id']} unexpectedly ran downstream stage {skipped}")
    detail = scene.get("detail", {})
    image_input_order_evidence = None
    if "imageInputOrder" not in detail:
        debug_url = endpoint_url(
            job.get("submit_response", {}).get("debugUrl"), "debugUrl", lineage["endpoint_base_url"])
        debug_response = endpoint.get(debug_url, timeout=60.0)
        debug_response.raise_for_status()
        try:
            debug = debug_response.json()
        except ValueError as exc:
            raise ValueError(f"debug endpoint returned invalid JSON for {row['row_id']}") from exc
        if not isinstance(debug, dict):
            raise ValueError(f"debug endpoint returned a non-object for {row['row_id']}")
        atomic_bytes(item["debug"], debug_response.content)
        calls = debug.get("calls")
        atomic_json(item["calls"], {"schema_version": 1, "row_id": row["row_id"], "calls": calls})
        guide_url = endpoint_url(
            f"/api/jobs/{job['submit_response']['jobId']}/artifacts/hp16_geometry_guide.png",
            "geometry guide URL", lineage["endpoint_base_url"],
        )
        guide_response = endpoint.get(guide_url, timeout=180.0)
        guide_response.raise_for_status()
        atomic_bytes(item["guide"], guide_response.content)
        with Image.open(item["guide"]) as guide_image:
            guide_image.verify()
        image_input_order_evidence = validate_debug_image_input_evidence(
            debug, sha256_path(item["guide"]), row, job, final_status, lineage)
        image_input_order_evidence.update({
            "debug_url": debug_url, "debug_response_sha256": sha256_path(item["debug"]),
            "debug_response_bytes": item["debug"].stat().st_size,
            "calls_evidence_sha256": sha256_path(item["calls"]),
            "calls_evidence_bytes": item["calls"].stat().st_size,
            "geometry_guide_filename": item["guide"].name,
            "geometry_guide_bytes": item["guide"].stat().st_size,
        })
    validate_scene_detail(detail, row, lineage, image_input_order_evidence)
    image_response = endpoint.get(job["image_url"], timeout=180.0)
    image_response.raise_for_status()
    atomic_bytes(item["image"], image_response.content)
    if (image_input_order_evidence is not None
            and sha256_path(item["image"]) != image_input_order_evidence["output_sha256"]):
        raise ValueError(f"downloaded output hash differs from debug image call for {row['row_id']}")
    with Image.open(item["image"]) as generated:
        generated.verify()
    with Image.open(item["image"]) as generated:
        dimensions, image_format = generated.size, generated.format
    if dimensions != EXPECTED_SIZE or image_format != "PNG":
        raise ValueError(f"unexpected image output for {row['row_id']}: {dimensions}, {image_format}")
    previous_failed_record = None
    if item["record"].is_file():
        previous_bytes = item["record"].read_bytes()
        try:
            previous = json.loads(previous_bytes)
        except ValueError:
            previous = None
        if isinstance(previous, dict) and previous.get("status") == "failed":
            previous_sha256 = sha256_bytes(previous_bytes)
            audit_path = run_dir / "records/audit" / f"{row['row_slug']}.{previous_sha256[:12]}.failed.json"
            if audit_path.exists() and audit_path.read_bytes() != previous_bytes:
                raise ValueError(f"failed-record audit collision for {row['row_id']}")
            if not audit_path.exists():
                atomic_bytes(audit_path, previous_bytes)
            previous_failed_record = {
                "path": str(audit_path.relative_to(run_dir)), "sha256": previous_sha256,
                "bytes": len(previous_bytes),
            }
    record = {
        "schema_version": 3, "row_id": row["row_id"], "row_slug": row["row_slug"], "status": "done",
        "completed_at_utc": now(), "queue_position": row["queue_position"], "device_id": row["device_id"],
        "digital_twin_id": row["digital_twin_id"], "device_type": row["prompt"].get("device_type"),
        "camera_id": row["camera_id"], "camera_tag": row["prompt"].get("camera_tag"), "bank_rank": row["rank"],
        "environment": row["prompt"].get("environment"), "prompt": row["prompt"]["text"],
        "prompt_sha256": row["prompt_sha256"], "prompt_record_sha256": row["prompt_record_sha256"],
        "job_id": final_status.get("jobId"), "status_url": job["status_url"], "image_source_url": job["image_url"],
        "image_filename": item["image"].name, "image_sha256": sha256_path(item["image"]),
        "image_bytes": item["image"].stat().st_size, "image_dimensions": {"width": dimensions[0], "height": dimensions[1]},
        "poll_count": poll_count, "runtime": final_status.get("params", {}), "scene_debug": detail,
        "image_input_order_evidence": image_input_order_evidence,
        "previous_failed_record": previous_failed_record,
        "stage_statuses": {name: value.get("status") for name, value in stages.items()},
        "run_sha256": run_sha256, "catalog_sha256": catalog_sha256, "lineage": lineage,
    }
    atomic_json(item["record"], record)
    append_journal(run_dir, {"event": "record_done", "row_id": row["row_id"], "image_sha256": record["image_sha256"]})
    return record


def materialize_twins(run_dir: Path, rows: list[dict[str, Any]], twin_dir: Path) -> dict[str, Any]:
    assets: dict[str, Any] = {}
    for row in rows:
        name = f"{row['device_id']}__{row['camera_id']}.png"
        source = twin_dir / name
        if not source.is_file():
            raise FileNotFoundError(f"missing frozen twin: {source}")
        destination = run_dir / "twins" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            shutil.copy2(source, destination)
        elif sha256_path(destination) != sha256_path(source):
            raise ValueError(f"materialized twin changed: {destination}")
        assets[name] = {"source_path": str(source.resolve()), "sha256": sha256_path(destination), "bytes": destination.stat().st_size}
    atomic_json(run_dir / "twin_manifest.json", {"schema_version": 1, "assets": assets})
    return assets


def materialize_bank_inputs(run_dir: Path, document: dict[str, Any], rows: list[dict[str, Any]], source_root: Path) -> dict[str, Any]:
    bank_audit = document.get("bank_audit") or {}
    expected_cases = {row["bank_id"] for row in rows}
    if set(bank_audit) != expected_cases:
        missing, extra = sorted(expected_cases - set(bank_audit)), sorted(set(bank_audit) - expected_cases)
        raise ValueError(f"bank_audit must exactly match the 16 prompt banks; missing={missing}, extra={extra}")
    assets: dict[str, Any] = {}
    for case_id, audit in sorted(bank_audit.items()):
        source_value = audit.get("source_input_path")
        expected_sha = audit.get("source_input_sha256")
        if not source_value or not expected_sha:
            raise ValueError(f"bank {case_id} lacks source_input_path/source_input_sha256")
        source = Path(source_value)
        if not source.is_absolute():
            source = source_root / source
        if not source.is_file():
            raise FileNotFoundError(f"missing bank source input: {source}")
        if sha256_path(source) != expected_sha:
            raise ValueError(f"bank source input hash changed: {source}")
        destination = run_dir / "source/bank_inputs" / f"{slug(case_id)}.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            shutil.copy2(source, destination)
        if sha256_path(destination) != expected_sha:
            raise ValueError(f"materialized bank source input changed: {destination}")
        assets[case_id] = {"original_path": str(source.resolve()), "materialized_path": str(destination),
                           "sha256": expected_sha, "bytes": destination.stat().st_size}
    if len(assets) != 16:
        raise ValueError(f"expected 16 hash-verified bank source inputs, found {len(assets)}")
    atomic_json(run_dir / "source/bank_inputs_manifest.json", {"schema_version": 1, "assets": assets})
    return assets


def fallback_credentials(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("export "):
            line = line[7:]
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip("'\"")
        if key in {"AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN", "AWS_REGION", "AWS_DEFAULT_REGION"}:
            values[key] = value
    return values


def s3_client(bucket: str, fallback_path: Path) -> Any:
    try:
        import foundry_aws_gateway
        values = foundry_aws_gateway.maybe_s3_env_vars(bucket)
    except Exception:  # Gateway unavailability is why the explicit private fallback exists.
        values = {}
    if not values:
        values = fallback_credentials(fallback_path)
    if values:
        required = {"AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"}
        if not required.issubset(values):
            raise ValueError(f"AWS credential environment is missing {sorted(required - set(values))}")
        return boto3.client("s3", region_name=values.get("AWS_REGION") or values.get("AWS_DEFAULT_REGION") or REGION,
            aws_access_key_id=values["AWS_ACCESS_KEY_ID"], aws_secret_access_key=values["AWS_SECRET_ACCESS_KEY"],
            aws_session_token=values["AWS_SESSION_TOKEN"])
    return boto3.client("s3", region_name=REGION)


def content_type(path: Path) -> str:
    return {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
            ".svg": "image/svg+xml", ".json": "application/json", ".html": "text/html; charset=utf-8",
            ".md": "text/markdown; charset=utf-8", ".txt": "text/plain; charset=utf-8",
            ".csv": "text/csv; charset=utf-8", ".js": "text/javascript; charset=utf-8",
            ".css": "text/css; charset=utf-8"}.get(path.suffix.lower(), "application/octet-stream")


def publishable_paths(run_dir: Path) -> list[Path]:
    selected: list[Path] = []
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(run_dir)
        parts = relative.parts
        lowered = relative.as_posix().lower()
        if any(part.startswith(".") or part == "__pycache__" for part in parts):
            continue
        if PRIVATE_NAME.search(lowered) or path.suffix.lower() in {".env", ".key", ".log", ".pem"}:
            continue
        if len(parts) == 1:
            if parts[0] in PUBLIC_ROOT_FILES:
                selected.append(path)
            continue
        if parts[0] == "journals":
            continue
        if parts[0] in PUBLIC_DIRECTORIES:
            if path.suffix.lower() not in PUBLIC_SUFFIXES:
                raise ValueError(f"refusing to silently omit unknown public artifact type: {relative}")
            selected.append(path)
    return selected


def publish_tree(run_dir: Path, bucket: str, prefix: str, fallback_path: Path) -> int:
    if not (run_dir / "run_manifest.json").is_file():
        raise FileNotFoundError(f"missing immutable run manifest: {run_dir / 'run_manifest.json'}")
    append_journal(run_dir, {"event": "publish_started", "bucket": bucket, "prefix": prefix})
    upload_paths = publishable_paths(run_dir)
    client = s3_client(bucket, fallback_path)
    count = 0
    for path in upload_paths:
        relative = path.relative_to(run_dir).as_posix()
        client.upload_file(str(path), bucket, f"{prefix.rstrip('/')}/{relative}", ExtraArgs={"ContentType": content_type(path)})
        count += 1
    append_journal(run_dir, {"event": "publish_complete", "bucket": bucket, "prefix": prefix, "files": count})
    return count


def summarize(run_dir: Path, rows: list[dict[str, Any]], bucket: str, prefix: str) -> dict[str, Any]:
    by_id = {row["row_id"]: row for row in rows}
    records: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / "records").glob("*.json")):
        record = load_json(path)
        row_id = record.get("row_id")
        if row_id not in by_id or row_id in records or record.get("prompt_sha256") != by_id[row_id]["prompt_sha256"]:
            raise ValueError(f"stale, duplicate, or mismatched run record: {path}")
        records[row_id] = record
    counts: dict[str, int] = {"queued": EXPECTED_COUNT - len(records)}
    for row_id, record in records.items():
        status = record.get("status", "unknown")
        if status == "done" and valid_completed_record(run_dir, by_id[row_id]) is None:
            status = "invalid_done_artifact"
        counts[status] = counts.get(status, 0) + 1
    value = {"schema_version": 2, "updated_at_utc": now(), "expected_count": EXPECTED_COUNT,
             "status_counts": counts, "queue_policy": "Latin-square device/view interleave repeated for ranks 1-10",
             "s3_uri": f"s3://{bucket}/{prefix.rstrip('/')}/",
             "viewer_url": f"https://foundry-aws-corp.adobe.io/asset/{bucket}/{prefix.rstrip('/')}/report/viewer.html"}
    atomic_json(run_dir / "summary.json", value)
    return value


def queue_document(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if len(rows) != EXPECTED_COUNT or {row["queue_position"] for row in rows} != set(range(1, EXPECTED_COUNT + 1)):
        raise ValueError("full queue must contain positions 1 through 160")
    return {
        "schema_version": 1,
        "expected_count": EXPECTED_COUNT,
        "queue_policy": "Latin-square device/view interleave repeated for ranks 1-10",
        "rows": [
            {
                "queue_position": row["queue_position"], "row_id": row["row_id"],
                "device_id": row["device_id"], "digital_twin_id": row["digital_twin_id"],
                "camera_id": row["camera_id"], "bank_id": row["bank_id"], "rank": row["rank"],
                "prompt_sha256": row["prompt_sha256"], "prompt_record_sha256": row["prompt_record_sha256"],
            }
            for row in rows
        ],
    }


def select_rows(rows: list[dict[str, Any]], requested: list[str] | None) -> list[dict[str, Any]]:
    if not requested:
        return rows
    flattened: list[str] = []
    for value in requested:
        flattened.extend(part.strip() for part in value.split(",") if part.strip())
    if not flattened:
        raise ValueError("--row-ids selected no rows")
    if len(flattened) != len(set(flattened)):
        raise ValueError("--row-ids contains duplicate row IDs")
    by_id = {row["row_id"]: row for row in rows}
    unknown = sorted(set(flattened) - set(by_id))
    if unknown:
        raise ValueError(f"--row-ids contains unknown rows: {unknown}")
    selected = set(flattened)
    return [row for row in rows if row["row_id"] in selected]


def load_selection_file(
    path: Path, document: dict[str, Any], expected_prompts_sha256: str,
) -> tuple[list[str], dict[str, Any]]:
    resolved = path.resolve()
    selection = load_json(resolved)
    if selection.get("source_prompts_sha256") != expected_prompts_sha256:
        raise ValueError("selection file source_prompts_sha256 differs from the frozen prompts")
    row_ids = selection.get("row_ids")
    if not isinstance(row_ids, list) or not row_ids or not all(isinstance(value, str) and value for value in row_ids):
        raise ValueError("selection file row_ids must be a non-empty string list")
    embedded = selection.get("rows")
    if embedded is not None:
        if not isinstance(embedded, list) or [item.get("prompt_key") for item in embedded] != row_ids:
            raise ValueError("selection file embedded rows must match row_ids in order")
        prompts = {item.get("prompt_key"): item for item in document.get("prompts") or []}
        for item in embedded:
            if item != prompts.get(item.get("prompt_key")):
                raise ValueError(f"selection file embedded row differs from frozen prompt: {item.get('prompt_key')!r}")
    provenance = {"path": str(resolved), "sha256": sha256_path(resolved), "row_count": len(row_ids)}
    return row_ids, provenance


def initialize_run(
    args: argparse.Namespace, document: dict[str, Any], rows: list[dict[str, Any]], catalog: dict[str, Any],
    lineage: dict[str, Any] | None = None,
) -> dict[str, Any]:
    run_dir = args.run_dir.resolve()
    for name in ("jobs", "records", "status", "images", "twins", "journals"):
        (run_dir / name).mkdir(parents=True, exist_ok=True)
    catalog_sha = canonical_sha256(catalog)
    if lineage is None:
        lineage = {
            "label": "baseline-pr4349-8c358bc7989c", "endpoint_base_url": BASE_URL,
            "endpoint": f"{BASE_URL}/api/generate", "generator": EXPECTED_GENERATOR,
            "rewriterVersion": EXPECTED_REWRITER, "pipelineVersion": EXPECTED_PIPELINE_VERSION,
            "source_commit": None, "patch_sha256": None, "runtime_tree_sha256": None,
            "source_manifest_sha256": None, "deployment_manifest_sha256": None,
            "candidate_config_sha256": None,
            "scene_contract": EXPECTED_SCENE_CONTRACT,
        }
    queue = queue_document(rows)
    queue_sha = canonical_sha256(queue)
    identity = {
        "schema_version": 3, "prompts_path": str(args.prompts.resolve()), "prompts_sha256": args.prompts_sha256,
        "endpoint": lineage["endpoint"], "catalog_sha256": catalog_sha,
        "generator": lineage["generator"], "rewriterVersion": lineage["rewriterVersion"], "lineage": lineage,
        "expected_count": EXPECTED_COUNT, "bucket": args.bucket, "prefix": args.prefix,
        "queue_policy": "Latin-square device/view interleave repeated for ranks 1-10",
        "queue_manifest_sha256": queue_sha,
    }
    identity["run_sha256"] = canonical_sha256(identity)
    manifest_path = run_dir / "run_manifest.json"
    if manifest_path.is_file():
        if load_json(manifest_path) != identity:
            raise ValueError("run identity differs from the immutable existing run_manifest.json")
    else:
        atomic_json(manifest_path, identity)
        atomic_json(run_dir / "run_started.json", {"created_at_utc": now(), "run_sha256": identity["run_sha256"]})
    queue_path = run_dir / "queue_manifest.json"
    if queue_path.is_file() and load_json(queue_path) != queue:
        raise ValueError("full queue differs from the immutable existing queue_manifest.json")
    if not queue_path.exists():
        atomic_json(queue_path, queue)
    if canonical_sha256(load_json(queue_path)) != identity["queue_manifest_sha256"]:
        raise ValueError("queue manifest hash differs from immutable run identity")
    frozen_copy = run_dir / "source/prompts_all_160.json"
    frozen_copy.parent.mkdir(parents=True, exist_ok=True)
    if not frozen_copy.exists():
        shutil.copy2(args.prompts.resolve(), frozen_copy)
    if sha256_path(frozen_copy) != args.prompts_sha256:
        raise ValueError("materialized frozen prompt document does not match --prompts-sha256")
    atomic_json(run_dir / "source/source_manifest.json", {
        "schema_version": 1,
        "original_path": str(args.prompts.resolve()),
        "materialized_path": str(frozen_copy),
        "sha256": args.prompts_sha256,
        "bytes": frozen_copy.stat().st_size,
    })
    materialize_bank_inputs(run_dir, document, rows, args.prompts.resolve().parent)
    catalog_path = run_dir / "catalog.json"
    if catalog_path.is_file() and canonical_sha256(load_json(catalog_path)) != catalog_sha:
        raise ValueError("live catalog changed after this run began; use a separate run directory")
    if not catalog_path.exists():
        atomic_json(catalog_path, catalog)
    materialize_twins(run_dir, rows, args.twin_dir.resolve())
    return identity


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--prompts-sha256", required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--twin-dir", type=Path, default=DEFAULT_TWIN_DIR)
    parser.add_argument("--bucket", default=BUCKET)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--endpoint-base-url", default=BASE_URL)
    parser.add_argument("--expected-generator", default=EXPECTED_GENERATOR)
    parser.add_argument("--expected-rewriter", default=EXPECTED_REWRITER)
    parser.add_argument("--expected-pipeline-version", default=EXPECTED_PIPELINE_VERSION)
    parser.add_argument("--lineage-label", default="baseline-pr4349-8c358bc7989c")
    parser.add_argument("--lineage-source-commit")
    parser.add_argument("--lineage-patch-sha256")
    parser.add_argument("--lineage-runtime-tree-sha256")
    parser.add_argument("--lineage-source-manifest-sha256")
    parser.add_argument("--lineage-deployment-manifest-sha256")
    parser.add_argument("--lineage-candidate-config-sha256")
    parser.add_argument("--row-ids", nargs="+", help="bounded subset of frozen row IDs; comma-separated values are also accepted")
    parser.add_argument("--selection-file", type=Path, help="JSON with source_prompts_sha256 and bounded row_ids")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--poll-seconds", type=int, default=2400)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--publish-only", action="store_true")
    parser.add_argument("--no-publish", action="store_true")
    parser.add_argument("--existing-jobs-only", action="store_true",
                        help="refuse to submit; every selected row must already have a saved job")
    parser.add_argument("--fallback-creds", type=Path, default=Path.home() / ".claude/hshariati/aws_creds.env")
    parser.add_argument("--catalog-json", type=Path, help="offline testing only; normal runs fetch /api/catalog")
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error("--workers must be between 1 and 8")
    if not POLL_SECONDS_MIN <= args.poll_seconds <= POLL_SECONDS_MAX:
        parser.error(f"--poll-seconds must be between {POLL_SECONDS_MIN} and {POLL_SECONDS_MAX}")
    if args.preflight_only and args.publish_only:
        parser.error("--preflight-only and --publish-only are mutually exclusive")
    if args.row_ids and args.selection_file:
        parser.error("--row-ids and --selection-file are mutually exclusive")
    if args.publish_only and (args.row_ids or args.selection_file):
        parser.error("selection cannot be used with --publish-only")
    if args.existing_jobs_only and (args.preflight_only or args.publish_only):
        parser.error("--existing-jobs-only requires a generation/resume invocation")
    return args


def main() -> int:
    args = parse_args()
    lineage = lineage_from_args(args)
    document = json.loads(args.prompts.resolve().read_text(encoding="utf-8"))
    rows = interleave(validate_prompt_document(document, args.prompts.resolve(), args.prompts_sha256))
    for position, row in enumerate(rows, start=1):
        row["queue_position"] = position
    selection_provenance = None
    requested = args.row_ids
    if args.selection_file:
        requested, selection_provenance = load_selection_file(args.selection_file, document, args.prompts_sha256)
    selected = select_rows(rows, requested)
    if args.publish_only:
        manifest = load_json(args.run_dir.resolve() / "run_manifest.json")
        if (manifest.get("prompts_sha256") != args.prompts_sha256 or manifest.get("bucket") != args.bucket
                or manifest.get("prefix") != args.prefix or manifest.get("lineage") != lineage):
            raise ValueError("publish target, frozen prompt hash, or lineage differs from the immutable run manifest")
        print(json.dumps({"published_files": publish_tree(args.run_dir.resolve(), args.bucket, args.prefix, args.fallback_creds)}, indent=2))
        return 0
    if args.catalog_json:
        catalog = load_json(args.catalog_json.resolve())
    else:
        response = httpx.get(f"{lineage['endpoint_base_url']}/api/catalog", timeout=60.0)
        response.raise_for_status()
        catalog = response.json()
    validate_catalog(catalog, rows, lineage["generator"], lineage["rewriterVersion"], lineage)
    run_identity = initialize_run(args, document, rows, catalog, lineage)
    print(json.dumps(summarize(args.run_dir.resolve(), rows, args.bucket, args.prefix), indent=2), flush=True)
    if args.preflight_only:
        return 0
    if args.existing_jobs_only:
        missing_jobs = [row["row_id"] for row in selected if not paths(args.run_dir.resolve(), row)["job"].is_file()]
        if missing_jobs:
            raise ValueError(f"--existing-jobs-only refuses rows without saved jobs: {missing_jobs}")
    append_journal(args.run_dir.resolve(), {
        "event": "generation_invocation", "selected_count": len(selected),
        "selected_row_ids": [row["row_id"] for row in selected], "full_queue_count": EXPECTED_COUNT,
        "workers": args.workers, "run_sha256": run_identity["run_sha256"],
        "selection_file": selection_provenance,
    })
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(process, args.run_dir.resolve(), row, canonical_sha256(catalog), args.poll_seconds,
                        run_identity["run_sha256"], lineage): row
            for row in selected
        }
        for future in as_completed(futures):
            row = futures[future]
            try:
                record = future.result()
                print(f"{record['status']} #{row['queue_position']} {row['row_id']}", flush=True)
            except Exception as exc:  # noqa: BLE001
                error = {"schema_version": 3, "row_id": row["row_id"], "status": "failed", "completed_at_utc": now(),
                         "prompt_sha256": row["prompt_sha256"], "error": f"{type(exc).__name__}: {exc}",
                         "run_sha256": run_identity["run_sha256"], "catalog_sha256": canonical_sha256(catalog),
                         "lineage": lineage}
                atomic_json(paths(args.run_dir.resolve(), row)["record"], error)
                append_journal(args.run_dir.resolve(), {"event": "row_failed", "row_id": row["row_id"], "error": error["error"]})
                print(f"failed #{row['queue_position']} {row['row_id']}: {error['error']}", file=sys.stderr, flush=True)
            print(json.dumps(summarize(args.run_dir.resolve(), rows, args.bucket, args.prefix), ensure_ascii=False), flush=True)
    if not args.no_publish:
        publish_tree(args.run_dir.resolve(), args.bucket, args.prefix, args.fallback_creds)
    print(json.dumps(summarize(args.run_dir.resolve(), rows, args.bucket, args.prefix), indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
