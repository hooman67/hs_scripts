#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""Generate every prompt × compatible digital-twin row through the HP endpoint.

The run is resumable. Each completed row has an atomic JSON record and a locally
downloaded output image. Re-running skips successful rows and retries failures.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[3]
INPUT_DATA_JS = (
    PROJECT_ROOT
    / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/data.js"
)
TWIN_DIR = Path("/mnt/localssd/hp_lifestyle_pipeline/digital_twin_renders_first_column")
TWIN_MANIFEST = PROJECT_ROOT / "digital_twin_assets/first_column_manifest.json"

BASE_URL = "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8000.or2.colligo.dev"
UPLOAD_URL = f"{BASE_URL}/v2/storage/image"
GENERATE_URL = f"{BASE_URL}/v1/image/generate"

WIDTH = 2368
HEIGHT = 1776
REWRITER_MODEL = "gemini-3.1-pro"
NUM_INFERENCE_STEPS = 50
POLL_INTERVAL_SECONDS = 5
JOB_TIMEOUT_SECONDS = 1800

_print_lock = threading.Lock()


def log(message: str) -> None:
    with _print_lock:
        stamp = dt.datetime.now().strftime("%H:%M:%S")
        print(f"[{stamp}] {message}", flush=True)


def load_eval_data() -> dict[str, Any]:
    text = INPUT_DATA_JS.read_text(encoding="utf-8")
    match = re.fullmatch(r"const EVAL_DATA = (.*);\n?", text, re.S)
    if not match:
        raise ValueError(f"Could not parse {INPUT_DATA_JS}")
    return json.loads(match.group(1))


def safe_row_id(row_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "__", row_id)


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def load_twin_manifest(
    data: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], str]:
    raw = TWIN_MANIFEST.read_bytes()
    manifest_sha256 = sha256_bytes(raw)
    manifest = json.loads(raw)
    assets = {asset["evalset_item_id"]: asset for asset in manifest["assets"]}
    twins = {twin["evalset_item_id"]: twin for twin in data["twins"]}
    missing = sorted(set(twins) - set(assets))
    if missing:
        raise ValueError(f"Twin source manifest is missing IDs: {missing}")
    for twin_id, twin in twins.items():
        asset = assets[twin_id]
        for field in ("local_filename", "sha256", "bytes", "width", "height"):
            if twin.get(field) != asset.get(field):
                raise ValueError(
                    f"Eval data and twin source manifest disagree for {twin_id} {field}: "
                    f"{twin.get(field)!r} != {asset.get(field)!r}"
                )
    return assets, manifest_sha256


BINDING_FIELDS = (
    "id",
    "twin_id",
    "local_filename",
    "source_path",
    "source_sha256",
    "source_bytes",
    "width",
    "height",
    "source_manifest_sha256",
    "upload_endpoint",
)


def stable_binding(binding: dict[str, Any]) -> dict[str, Any]:
    return {field: binding.get(field) for field in BINDING_FIELDS}


def validate_binding(
    twin_id: str,
    binding: dict[str, Any],
    asset: dict[str, Any],
    manifest_sha256: str,
) -> None:
    missing = [field for field in BINDING_FIELDS if not binding.get(field)]
    if missing:
        raise ValueError(
            f"Cached reference binding for {twin_id} lacks provenance fields {missing}; "
            "use a new run directory and re-upload from the verified source manifest"
        )
    expected = {
        "twin_id": twin_id,
        "local_filename": asset["local_filename"],
        "source_sha256": asset["sha256"],
        "source_bytes": asset["bytes"],
        "width": asset["width"],
        "height": asset["height"],
        "source_manifest_sha256": manifest_sha256,
        "upload_endpoint": UPLOAD_URL,
    }
    for field, expected_value in expected.items():
        if binding.get(field) != expected_value:
            raise ValueError(
                f"Cached reference binding for {twin_id} has {field}="
                f"{binding.get(field)!r}; expected {expected_value!r}. "
                "Refusing to reuse an unverified blob"
            )


def load_cached_bindings(
    mapping_path: Path,
    twins: dict[str, dict[str, Any]],
    assets: dict[str, dict[str, Any]],
    manifest_sha256: str,
) -> dict[str, dict[str, Any]]:
    if not mapping_path.exists():
        return {}
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    unknown = sorted(set(mapping) - set(twins))
    if unknown:
        raise ValueError(f"Reference-blob cache contains unknown twin IDs: {unknown}")
    for twin_id, binding in mapping.items():
        validate_binding(twin_id, binding, assets[twin_id], manifest_sha256)
    return mapping


def post_image(image_bytes: bytes, source_label: str, retries: int = 4) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(1, retries + 2):
        try:
            with httpx.Client(timeout=httpx.Timeout(120, connect=20)) as client:
                response = client.post(
                    UPLOAD_URL,
                    content=image_bytes,
                    headers={"content-type": "image/jpeg", "accept": "application/json"},
                )
                response.raise_for_status()
                image = response.json()["images"][0]
                if not image.get("id"):
                    raise ValueError(f"Upload response had no image ID: {response.text[:500]}")
                return image
        except Exception as exc:
            last_error = exc
            if attempt <= retries:
                time.sleep(min(30, 3 * attempt))
    raise RuntimeError(f"Failed to upload {source_label}: {last_error}")


def upload_missing_twins(
    data: dict[str, Any], run_dir: Path, workers: int
) -> tuple[dict[str, dict[str, Any]], str]:
    mapping_path = run_dir / "blob_ids.json"
    twins = {twin["evalset_item_id"]: twin for twin in data["twins"]}
    assets, manifest_sha256 = load_twin_manifest(data)
    mapping = load_cached_bindings(
        mapping_path, twins, assets, manifest_sha256
    )
    missing = [twin for twin_id, twin in twins.items() if twin_id not in mapping]
    log(f"reference blobs: {len(mapping)} cached, {len(missing)} to upload")

    def upload(twin: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        twin_id = twin["evalset_item_id"]
        asset = assets[twin_id]
        path = TWIN_DIR / asset["local_filename"]
        if not path.is_file():
            raise FileNotFoundError(path)
        image_bytes = path.read_bytes()
        actual_sha256 = sha256_bytes(image_bytes)
        if len(image_bytes) != asset["bytes"] or actual_sha256 != asset["sha256"]:
            raise ValueError(
                f"Local twin bytes do not match source manifest for {twin_id}: "
                f"bytes={len(image_bytes)}, sha256={actual_sha256}"
            )
        uploaded = post_image(image_bytes, str(path))
        return twin_id, {
            "id": uploaded["id"],
            "twin_id": twin_id,
            "local_filename": asset["local_filename"],
            "source_path": str(path),
            "source_sha256": actual_sha256,
            "source_bytes": len(image_bytes),
            "width": asset["width"],
            "height": asset["height"],
            "source_manifest_sha256": manifest_sha256,
            "upload_endpoint": UPLOAD_URL,
            "uploaded_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        }

    if missing:
        with ThreadPoolExecutor(max_workers=min(workers, len(missing))) as pool:
            futures = {pool.submit(upload, twin): twin for twin in missing}
            for future in as_completed(futures):
                twin_id, record = future.result()
                mapping[twin_id] = record
                atomic_write_json(mapping_path, dict(sorted(mapping.items())))
                log(f"uploaded reference {twin_id} ({len(mapping)}/{len(twins)})")

    if set(mapping) != set(twins):
        raise ValueError("Reference-blob mapping does not cover every used twin")
    return mapping, manifest_sha256


def prompt_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {prompt["key"]: prompt for prompt in data["prompts"]}


def build_payload(prompt_text: str, blob_id: str) -> dict[str, Any]:
    return {
        "prompt": prompt_text,
        "size": {"width": WIDTH, "height": HEIGHT},
        "referenceBlobs": [{"id": blob_id}],
        "n": 1,
        "modelSpecificPayload": {
            "enablePromptRewrite": True,
            "rewriterModel": REWRITER_MODEL,
            "numInferenceSteps": NUM_INFERENCE_STEPS,
        },
    }


def generation_provenance(
    prompt_text: str,
    payload: dict[str, Any],
    binding: dict[str, Any],
    manifest_sha256: str,
) -> dict[str, Any]:
    return {
        "prompt_sha256": sha256_bytes(prompt_text.encode("utf-8")),
        "request_payload_sha256": canonical_json_sha256(payload),
        "reference_manifest_sha256": manifest_sha256,
        "reference_binding": stable_binding(binding),
    }


def validate_completed_record(
    row: dict[str, Any],
    record: dict[str, Any],
    prompt: dict[str, Any],
    binding: dict[str, Any],
    manifest_sha256: str,
) -> None:
    payload = build_payload(prompt["text"], binding["id"])
    expected = generation_provenance(
        prompt["text"], payload, binding, manifest_sha256
    )
    if not record.get("provenance"):
        raise ValueError(
            f"Completed record {row['row_id']} lacks provenance; refusing to resume "
            "or silently trust a legacy result"
        )
    identity = {
        "row_id": row["row_id"],
        "prompt_key": row["prompt_key"],
        "twin_id": row["twin_id"],
    }
    for field, expected_value in identity.items():
        if record.get(field) != expected_value:
            raise ValueError(
                f"Completed record {row['row_id']} has {field}={record.get(field)!r}; "
                f"expected {expected_value!r}"
            )
    if record.get("request_payload") != payload:
        raise ValueError(
            f"Completed record {row['row_id']} request payload differs from the "
            "current prompt/reference payload"
        )
    for field, expected_value in expected.items():
        if record["provenance"].get(field) != expected_value:
            raise ValueError(
                f"Completed record {row['row_id']} provenance mismatch for {field}; "
                "refusing to resume"
            )


def validate_completed_records(
    data: dict[str, Any],
    records: dict[str, dict[str, Any]],
    prompts: dict[str, dict[str, Any]],
    bindings: dict[str, dict[str, Any]],
    manifest_sha256: str,
) -> None:
    preflight_completed_records(data, records)
    rows = {row["row_id"]: row for row in data["rows"]}
    for row_id, record in records.items():
        if record.get("status") == "done":
            row = rows[row_id]
            validate_completed_record(
                row,
                record,
                prompts[row["prompt_key"]],
                bindings[row["twin_id"]],
                manifest_sha256,
            )


def preflight_completed_records(
    data: dict[str, Any], records: dict[str, dict[str, Any]]
) -> None:
    rows = {row["row_id"]: row for row in data["rows"]}
    unknown = sorted(set(records) - set(rows))
    if unknown:
        raise ValueError(f"Run directory contains records for unknown rows: {unknown}")
    for row_id, record in records.items():
        if record.get("status") == "done" and not record.get("provenance"):
            raise ValueError(
                f"Completed record {row_id} lacks provenance; use a new run directory. "
                "No uploads or generations were attempted"
            )


def is_final_response(body: dict[str, Any], task_status: str) -> bool:
    status = str(body.get("status") or task_status or "").upper()
    if status in {"COMPLETED", "SUCCEEDED", "FAILED", "TIMEOUT", "CANCELLED"}:
        return True
    return bool(body.get("outputs") or body.get("error_code") or body.get("error"))


def response_failed(body: dict[str, Any], task_status: str) -> bool:
    status = str(body.get("status") or task_status or "").upper()
    return status in {"FAILED", "TIMEOUT", "CANCELLED"} or bool(
        body.get("error_code") or body.get("error")
    )


def submit_and_wait(payload: dict[str, Any]) -> tuple[str, dict[str, Any], float]:
    started = time.monotonic()
    with httpx.Client(timeout=httpx.Timeout(120, connect=20)) as client:
        response = client.post(
            GENERATE_URL,
            json=payload,
            headers={"content-type": "application/json", "accept": "application/json"},
        )
        response.raise_for_status()
        body = response.json()
        task_status = response.headers.get("x-task-status", "")

        if response.status_code != 202 and is_final_response(body, task_status):
            return "", body, (time.monotonic() - started) * 1000

        job_id = body.get("job_id", "")
        result_href = ((body.get("links") or {}).get("result") or {}).get("href")
        if not result_href:
            raise ValueError(f"Async response has no result link: {body}")
        result_url = result_href if result_href.startswith("http") else BASE_URL + result_href

        while True:
            if time.monotonic() - started > JOB_TIMEOUT_SECONDS:
                raise TimeoutError(f"Job {job_id} exceeded {JOB_TIMEOUT_SECONDS}s")
            time.sleep(POLL_INTERVAL_SECONDS)
            result = client.get(result_url, headers={"accept": "application/json"})
            result.raise_for_status()
            final_body = result.json()
            task_status = result.headers.get("x-task-status", "")
            if is_final_response(final_body, task_status):
                if response_failed(final_body, task_status):
                    raise RuntimeError(
                        f"Job {job_id} failed: "
                        + json.dumps(final_body, ensure_ascii=False)[:1500]
                    )
                return job_id, final_body, (time.monotonic() - started) * 1000


def output_extension(content_type: str) -> str:
    clean = content_type.split(";", 1)[0].strip().lower()
    return {"image/jpeg": ".jpg", "image/jpg": ".jpg", "image/webp": ".webp"}.get(
        clean, ".png"
    )


def download_output(presigned_url: str, base_path: Path) -> Path:
    with httpx.Client(timeout=httpx.Timeout(180, connect=20)) as client:
        with client.stream("GET", presigned_url, headers={"user-agent": "Mozilla/5.0"}) as response:
            response.raise_for_status()
            destination = base_path.with_suffix(output_extension(response.headers.get("content-type", "")))
            temporary = destination.with_name(f".{destination.name}.download")
            with temporary.open("wb") as handle:
                for chunk in response.iter_bytes(256 * 1024):
                    handle.write(chunk)
            temporary.replace(destination)
    return destination


def sanitize_response(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: sanitize_response(child)
            for key, child in value.items()
            if key != "presignedUrl"
        }
    if isinstance(value, list):
        return [sanitize_response(child) for child in value]
    return value


def generate_row(
    row: dict[str, Any],
    prompts: dict[str, dict[str, Any]],
    blobs: dict[str, dict[str, Any]],
    manifest_sha256: str,
    run_dir: Path,
    retries: int,
) -> dict[str, Any]:
    prompt = prompts[row["prompt_key"]]
    binding = blobs[row["twin_id"]]
    payload = build_payload(prompt["text"], binding["id"])
    provenance = generation_provenance(
        prompt["text"], payload, binding, manifest_sha256
    )
    record_path = run_dir / "records" / f"{safe_row_id(row['row_id'])}.json"
    image_base = run_dir / "images" / safe_row_id(row["row_id"])
    last_error = ""

    for attempt in range(1, retries + 2):
        try:
            job_id, final_response, latency_ms = submit_and_wait(payload)
            outputs = final_response.get("outputs") or []
            if not outputs:
                raise ValueError("Completed response has no outputs")
            image = outputs[0].get("image") or {}
            presigned_url = image.get("presignedUrl")
            if not presigned_url:
                raise ValueError("Completed response has no output presigned URL")
            image_path = download_output(presigned_url, image_base)
            record = {
                "row_id": row["row_id"],
                "prompt_key": row["prompt_key"],
                "twin_id": row["twin_id"],
                "device_category": row["device_category"],
                "status": "done",
                "attempt": attempt,
                "job_id": job_id,
                "request_payload": payload,
                "provenance": provenance,
                "total_latency_ms": latency_ms,
                "output_image_id": image.get("id", ""),
                "output_image_filename": image_path.name,
                "output_seed": outputs[0].get("seed"),
                "debugData": final_response.get("debugData") or {},
                "response": sanitize_response(final_response),
                "completed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
            atomic_write_json(record_path, record)
            return record
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt <= retries:
                time.sleep(min(60, 10 * attempt))

    failed = {
        "row_id": row["row_id"],
        "prompt_key": row["prompt_key"],
        "twin_id": row["twin_id"],
        "device_category": row["device_category"],
        "status": "failed",
        "attempt": retries + 1,
        "request_payload": payload,
        "provenance": provenance,
        "error": last_error,
        "completed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    atomic_write_json(record_path, failed)
    return failed


def load_records(run_dir: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / "records").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        records[record["row_id"]] = record
    return records


def import_smoke(
    data: dict[str, Any],
    run_dir: Path,
    request_path: Path,
    response_path: Path,
    blob_path: Path,
    smoke_twin_id: str,
    smoke_source_path: Path,
    smoke_source_sha256: str,
) -> None:
    request_wrapper = json.loads(request_path.read_text(encoding="utf-8"))
    final_response = json.loads(response_path.read_text(encoding="utf-8"))
    blob_wrapper = json.loads(blob_path.read_text(encoding="utf-8"))
    uploaded = blob_wrapper["images"][0]
    upload_provenance = blob_wrapper.get("upload_provenance")
    if not upload_provenance:
        raise ValueError(
            "Smoke blob artifact lacks upload_provenance and cannot prove which "
            "source bytes produced the blob; raw legacy upload responses are not importable"
        )
    row_id = request_wrapper["row_id"]
    rows = {row["row_id"]: row for row in data["rows"]}
    if row_id not in rows:
        raise ValueError(f"Smoke request names unknown row {row_id}")
    row = rows[row_id]
    if row["twin_id"] != smoke_twin_id:
        raise ValueError(
            f"Smoke row {row_id} requires twin {row['twin_id']}, but explicit "
            f"smoke identity is {smoke_twin_id}"
        )

    assets, manifest_sha256 = load_twin_manifest(data)
    if smoke_twin_id not in assets:
        raise ValueError(f"Smoke twin {smoke_twin_id} is absent from source manifest")
    asset = assets[smoke_twin_id]
    source_bytes = smoke_source_path.read_bytes()
    actual_sha256 = sha256_bytes(source_bytes)
    if smoke_source_sha256 != actual_sha256:
        raise ValueError(
            "Explicit smoke source SHA-256 does not match the supplied source file: "
            f"{smoke_source_sha256} != {actual_sha256}"
        )
    if actual_sha256 != asset["sha256"] or len(source_bytes) != asset["bytes"]:
        raise ValueError(
            f"Smoke source does not match manifest identity {smoke_twin_id}: "
            f"expected bytes={asset['bytes']}, sha256={asset['sha256']}; "
            f"got bytes={len(source_bytes)}, sha256={actual_sha256}"
        )
    expected_upload_provenance = {
        "twin_id": smoke_twin_id,
        "local_filename": asset["local_filename"],
        "source_path": str(smoke_source_path.resolve()),
        "source_sha256": actual_sha256,
        "source_bytes": len(source_bytes),
        "width": asset["width"],
        "height": asset["height"],
        "source_manifest_sha256": manifest_sha256,
        "upload_endpoint": UPLOAD_URL,
    }
    for field, expected_value in expected_upload_provenance.items():
        if upload_provenance.get(field) != expected_value:
            raise ValueError(
                f"Smoke upload provenance mismatch for {field}: "
                f"{upload_provenance.get(field)!r} != {expected_value!r}"
            )
    if not uploaded.get("id"):
        raise ValueError("Smoke blob response contains no image ID")

    expected_payload = build_payload(
        prompt_map(data)[row["prompt_key"]]["text"], uploaded["id"]
    )
    if request_wrapper.get("payload") != expected_payload:
        raise ValueError(
            f"Smoke request payload for {row_id} does not match the current prompt, "
            "settings, and uploaded blob ID"
        )

    mapping_path = run_dir / "blob_ids.json"
    twins = {twin["evalset_item_id"]: twin for twin in data["twins"]}
    mapping = load_cached_bindings(
        mapping_path, twins, assets, manifest_sha256
    )
    binding = {
        "id": uploaded["id"],
        "twin_id": smoke_twin_id,
        "local_filename": asset["local_filename"],
        "source_path": str(smoke_source_path.resolve()),
        "source_sha256": actual_sha256,
        "source_bytes": len(source_bytes),
        "width": asset["width"],
        "height": asset["height"],
        "source_manifest_sha256": manifest_sha256,
        "upload_endpoint": UPLOAD_URL,
        "uploaded_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "imported_from_smoke": True,
    }
    mapping[smoke_twin_id] = binding
    atomic_write_json(mapping_path, dict(sorted(mapping.items())))

    outputs = final_response["outputs"]
    image = outputs[0]["image"]
    image_path = download_output(
        image["presignedUrl"], run_dir / "images" / safe_row_id(row_id)
    )
    record = {
        "row_id": row_id,
        "prompt_key": row["prompt_key"],
        "twin_id": row["twin_id"],
        "device_category": row["device_category"],
        "status": "done",
        "attempt": 1,
        "job_id": request_wrapper.get("job_id", ""),
        "request_payload": expected_payload,
        "provenance": generation_provenance(
            prompt_map(data)[row["prompt_key"]]["text"],
            expected_payload,
            binding,
            manifest_sha256,
        ),
        "total_latency_ms": None,
        "output_image_id": image.get("id", ""),
        "output_image_filename": image_path.name,
        "output_seed": outputs[0].get("seed"),
        "debugData": final_response.get("debugData") or {},
        "response": sanitize_response(final_response),
        "completed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "imported_from_smoke": True,
    }
    atomic_write_json(
        run_dir / "records" / f"{safe_row_id(row_id)}.json", record
    )
    log(f"imported successful smoke row {row_id}")


def write_summary(run_dir: Path, data: dict[str, Any]) -> dict[str, Any]:
    records = load_records(run_dir)
    done = [record for record in records.values() if record["status"] == "done"]
    failed = [record for record in records.values() if record["status"] != "done"]
    summary = {
        "updated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "endpoint": GENERATE_URL,
        "upload_endpoint": UPLOAD_URL,
        "settings": {
            "width": WIDTH,
            "height": HEIGHT,
            "n": 1,
            "enablePromptRewrite": True,
            "rewriterModel": REWRITER_MODEL,
            "numInferenceSteps": NUM_INFERENCE_STEPS,
        },
        "expected_rows": len(data["rows"]),
        "record_count": len(records),
        "done_count": len(done),
        "failed_count": len(failed),
        "missing_count": len(data["rows"]) - len(records),
        "failed_row_ids": [record["row_id"] for record in failed],
    }
    atomic_write_json(run_dir / "summary.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--import-smoke", action="store_true")
    parser.add_argument(
        "--smoke-request-path",
        type=Path,
        default=Path("/tmp/hp_generation_smoke_request.json"),
    )
    parser.add_argument(
        "--smoke-response-path",
        type=Path,
        default=Path("/tmp/hp_generation_smoke_final.json"),
    )
    parser.add_argument(
        "--smoke-blob-path", type=Path, default=Path("/tmp/hp_blob_probe.json")
    )
    parser.add_argument("--smoke-twin-id")
    parser.add_argument("--smoke-source-path", type=Path)
    parser.add_argument("--smoke-source-sha256")
    args = parser.parse_args()

    args.run_dir.mkdir(parents=True, exist_ok=True)
    (args.run_dir / "images").mkdir(exist_ok=True)
    (args.run_dir / "records").mkdir(exist_ok=True)
    data = load_eval_data()
    records = load_records(args.run_dir)
    preflight_completed_records(data, records)

    if args.import_smoke:
        missing_smoke_args = [
            name
            for name, value in (
                ("--smoke-twin-id", args.smoke_twin_id),
                ("--smoke-source-path", args.smoke_source_path),
                ("--smoke-source-sha256", args.smoke_source_sha256),
            )
            if not value
        ]
        if missing_smoke_args:
            parser.error(
                "--import-smoke requires explicit verifiable source identity: "
                + ", ".join(missing_smoke_args)
            )
        import_smoke(
            data,
            args.run_dir,
            args.smoke_request_path,
            args.smoke_response_path,
            args.smoke_blob_path,
            args.smoke_twin_id,
            args.smoke_source_path,
            args.smoke_source_sha256,
        )

    blobs, manifest_sha256 = upload_missing_twins(data, args.run_dir, args.workers)
    prompts = prompt_map(data)
    records = load_records(args.run_dir)
    validate_completed_records(data, records, prompts, blobs, manifest_sha256)
    pending = [
        row
        for row in data["rows"]
        if records.get(row["row_id"], {}).get("status") != "done"
    ]
    if args.limit:
        pending = pending[: args.limit]

    log(
        f"generation rows: {len(data['rows'])} expected, "
        f"{sum(r.get('status') == 'done' for r in records.values())} complete, "
        f"{len(pending)} pending this invocation; workers={args.workers}, retries={args.retries}"
    )
    completed_this_run = 0
    failed_this_run = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                generate_row,
                row,
                prompts,
                blobs,
                manifest_sha256,
                args.run_dir,
                args.retries,
            ): row
            for row in pending
        }
        for future in as_completed(futures):
            record = future.result()
            if record["status"] == "done":
                completed_this_run += 1
                latency = record.get("total_latency_ms")
                latency_text = f"{latency / 1000:.1f}s" if latency else "imported"
                log(
                    f"done {record['row_id']} ({completed_this_run + failed_this_run}/{len(pending)}, {latency_text})"
                )
            else:
                failed_this_run += 1
                log(
                    f"FAILED {record['row_id']} ({completed_this_run + failed_this_run}/{len(pending)}): "
                    f"{record.get('error', '')[:300]}"
                )

    summary = write_summary(args.run_dir, data)
    log("summary: " + json.dumps(summary, ensure_ascii=False))
    if summary["failed_count"] or summary["missing_count"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
