#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3>=1.34", "httpx>=0.27", "pillow>=10"]
# ///
"""Collect the unlabeled V6.2 placement target from the frozen local endpoint run."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from PIL import Image


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[5]
ASSET_ROOT = PROJECT / "judge/local_runs/v6_2_placement_assets"
GENERATED_ROOT = ASSET_ROOT / "generated"
TWIN_ROOT = ASSET_ROOT / "twins"
SOURCE_ROOT = HERE / "source"
MANIFEST_PATH = HERE / "manifest.json"

BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_spatial_composition_v6_2_gpt_image2_scene_20261107"
REGION = "us-west-2"
GATEWAY = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}"
GALLERY_URL = f"{GATEWAY}/gallery/index.html"
ENDPOINT = "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev"
PROMPT_SOURCE = (
    PROJECT
    / "eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106"
    / "revisions/v6.2-full160-20261107-r5-validated-composite/exports/final/prompts_all_160.json"
)
PROMPT_SOURCE_SHA256 = "d23da34ab0c8442f60e497866e79a05d42b25d74b6709ed4c34af0c67169ae84"
GENERATION_RUN = (
    PROJECT
    / "eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106"
    / "generation_gpt_image2_scene_v1/run"
)
EXPECTED_COUNT = 160
EXPECTED_SIZE = (2368, 1776)
EXPECTED_GENERATOR = "GPT Image 2.5 / single reference / no grading"
DOWNSTREAM_STAGES = ("ibl", "backplate", "recomposite", "relight")
PRODUCT_NAMES = {
    "cashmere": "Cashmere",
    "elitebook": "EliteBook",
    "tassel": "Tassel",
    "magic": "Magic",
}
SHA256_RE = re.compile(r"[0-9a-f]{64}")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256_bytes(raw.encode("utf-8"))


def atomic_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(value)
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_bytes(
        path,
        (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8"),
    )


def image_properties(value: bytes) -> tuple[str, int, int]:
    with Image.open(io.BytesIO(value)) as image:
        image.verify()
    with Image.open(io.BytesIO(value)) as image:
        return image.format or "", image.width, image.height


def object_record(response: dict[str, Any], key: str, value: bytes) -> dict[str, Any]:
    return {
        "s3_uri": f"s3://{BUCKET}/{key}",
        "public_url": f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{key}",
        "sha256": sha256_bytes(value),
        "bytes": len(value),
        "etag": response["ETag"].strip('"'),
        "last_modified": response["LastModified"].astimezone(timezone.utc).isoformat(),
        "content_type": response.get("ContentType"),
        "metadata": response.get("Metadata", {}),
    }


def s3_get(client: Any, key: str) -> tuple[bytes, dict[str, Any]]:
    response = client.get_object(Bucket=BUCKET, Key=key)
    value = response["Body"].read()
    if response["ContentLength"] != len(value):
        raise ValueError(f"Truncated S3 object: {key}")
    return value, object_record(response, key, value)


def published_key(image_url: str) -> str:
    path = urlparse(image_url).path
    marker = f"/asset/{BUCKET}/"
    if marker not in path:
        raise ValueError(f"Unexpected published image URL: {image_url}")
    return path.split(marker, 1)[1]


def load_prompts() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    if sha256_path(PROMPT_SOURCE) != PROMPT_SOURCE_SHA256:
        raise ValueError("Frozen V6.2 prompt source hash changed")
    document = json.loads(PROMPT_SOURCE.read_text(encoding="utf-8"))
    prompts = document.get("prompts")
    if not isinstance(prompts, list) or len(prompts) != EXPECTED_COUNT:
        raise ValueError("Frozen prompt source must contain exactly 160 prompts")
    by_key = {row["prompt_key"]: row for row in prompts}
    if len(by_key) != EXPECTED_COUNT:
        raise ValueError("Frozen prompt source contains duplicate prompt keys")
    return by_key, document


def fetch_job(row: dict[str, Any]) -> dict[str, Any]:
    job_id = row["job_id"]
    status_url = f"{ENDPOINT}/api/jobs/{job_id}"
    twin_url = f"{status_url}/artifacts/1_hero_white.png"
    with httpx.Client(timeout=httpx.Timeout(120.0, connect=30.0)) as client:
        status_response = client.get(status_url)
        status_response.raise_for_status()
        status = status_response.json()
        twin_response = client.get(twin_url)
        twin_response.raise_for_status()
    twin = twin_response.content
    twin_format, twin_width, twin_height = image_properties(twin)
    if twin_format != "PNG" or (twin_width, twin_height) != EXPECTED_SIZE:
        raise ValueError(f"Unexpected actual twin artifact for {row['row_id']}")

    params = status.get("params", {})
    stages = status.get("stages", {})
    hero = stages.get("hero", {})
    scene = stages.get("scene", {})
    if status.get("jobId") != job_id or status.get("done") is not True:
        raise ValueError(f"Incomplete or mismatched endpoint job: {row['row_id']}")
    if (
        params.get("prompt") != row["prompt"]
        or params.get("digitalTwinId") != row["digital_twin_id"]
        or params.get("cameraId") != row["camera_id"]
        or params.get("generationMode") != "sceneOnly"
    ):
        raise ValueError(f"Endpoint parameters disagree with gallery row: {row['row_id']}")
    if hero.get("status") != "done" or hero.get("has_image") is not True:
        raise ValueError(f"Hero stage is not complete: {row['row_id']}")
    if scene.get("status") != "done" or scene.get("has_image") is not True:
        raise ValueError(f"Scene stage is not complete: {row['row_id']}")
    if any(
        stages.get(name, {}).get("status") != "skipped"
        or stages.get(name, {}).get("has_image") is not False
        for name in DOWNSTREAM_STAGES
    ):
        raise ValueError(f"A downstream stage was not skipped: {row['row_id']}")
    detail = scene.get("detail", {})
    if (
        detail.get("originalPrompt") != row["prompt"]
        or detail.get("baselinePromptUsed") is not False
        or detail.get("imageCalls") != 1
        or detail.get("size") != "2368x1776"
    ):
        raise ValueError(f"Scene provenance disagrees with gallery row: {row['row_id']}")
    if canonical_sha256(detail) != canonical_sha256(row["scene_debug"]):
        raise ValueError(f"Published and live scene debug differ: {row['row_id']}")
    return {
        "row_id": row["row_id"],
        "job_id": job_id,
        "status_url": status_url,
        "status_sha256": canonical_sha256(status),
        "twin_url": twin_url,
        "twin": twin,
        "twin_sha256": sha256_bytes(twin),
        "twin_bytes": len(twin),
        "twin_width": twin_width,
        "twin_height": twin_height,
        "product_version": params.get("productVersion"),
        "hero_detail": hero.get("detail", {}),
        "scene_evidence": {
            "generation_mode": params["generationMode"],
            "hero_status": hero["status"],
            "scene_status": scene["status"],
            "scene_has_image": scene["has_image"],
            "output_artifact": "2_scene.png",
            "baseline_prompt_used": detail["baselinePromptUsed"],
            "original_prompt_matches": True,
            "image_model": detail.get("imageModel"),
            "text_model": detail.get("textModel"),
            "downstream_stage_statuses": {
                name: stages[name]["status"] for name in DOWNSTREAM_STAGES
            },
        },
    }


def load_generated(row: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    local_path = GENERATION_RUN / "images" / row["image_filename"]
    if not local_path.is_file():
        raise ValueError(f"Missing local generated PNG: {row['row_id']}")
    value = local_path.read_bytes()
    image_format, width, height = image_properties(value)
    if image_format != "PNG" or (width, height) != EXPECTED_SIZE:
        raise ValueError(f"Unexpected local generated PNG: {row['row_id']}")
    digest = sha256_bytes(value)
    if digest != row["image_sha256"]:
        raise ValueError(f"Local generated hash mismatch: {row['row_id']}")
    copied = GENERATED_ROOT / local_path.name
    if copied.exists() and sha256_path(copied) != digest:
        raise ValueError(f"Existing generated file differs: {copied}")
    atomic_bytes(copied, value)
    source = {
        "source_artifact_url": row["image_source_url"],
        "future_s3_uri": f"s3://{BUCKET}/{PREFIX}/images/{local_path.name}",
        "future_public_url": f"{GATEWAY}/images/{local_path.name}",
        "sha256": digest,
        "bytes": len(value),
        "filename": copied.name,
        "local_path": str(copied.resolve()),
        "width": width,
        "height": height,
    }
    return row["row_id"], source


def list_published_objects(s3: Any) -> list[dict[str, Any]]:
    paginator = s3.get_paginator("list_objects_v2")
    objects: list[dict[str, Any]] = []
    for page in paginator.paginate(Bucket=BUCKET, Prefix=f"{PREFIX}/"):
        objects.extend(page.get("Contents", []))
    return objects


def validate_existing() -> dict[str, Any]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    records = manifest.get("records")
    if manifest.get("expected_count") != EXPECTED_COUNT or not isinstance(records, list):
        raise ValueError("Existing manifest count contract is invalid")
    if len(records) != EXPECTED_COUNT:
        raise ValueError("Existing manifest record count is invalid")
    for record in records:
        for key in ("generated_image", "twin_image"):
            image = record[key]
            path = Path(image["local_path"])
            if not path.is_file() or sha256_path(path) != image["sha256"]:
                raise ValueError(f"Existing {key} bytes differ for {record['id']}")
        if record.get("human_feedback") is not None or "diagnostic_expectation" in record:
            raise ValueError("Target manifest contains training/evaluation labels")
    for source in manifest["source_snapshot"].values():
        path = Path(source["local_path"])
        if not path.is_file() or sha256_path(path) != source["sha256"]:
            raise ValueError(f"Source snapshot differs: {path}")
    return {
        "manifest": str(MANIFEST_PATH),
        "records": len(records),
        "generated_images": len({row["generated_image"]["sha256"] for row in records}),
        "actual_twins": len({row["twin_image"]["sha256"] for row in records}),
        "model_calls": 0,
    }


def collect(workers: int) -> dict[str, Any]:
    prompts, _ = load_prompts()
    record_paths = sorted((GENERATION_RUN / "records").glob("*.json"))
    rows = [json.loads(path.read_text(encoding="utf-8")) for path in record_paths]
    rows.sort(key=lambda row: row.get("queue_position", 10**9))
    if len(rows) != EXPECTED_COUNT or any(row.get("status") != "done" for row in rows):
        raise ValueError("Local generation run must contain exactly 160 completed records")
    if len({row.get("row_id") for row in rows}) != EXPECTED_COUNT:
        raise ValueError("Local generation row IDs are not unique")

    run_manifest_path = GENERATION_RUN / "run_manifest.json"
    catalog_path = GENERATION_RUN / "catalog.json"
    run_manifest = json.loads(run_manifest_path.read_text(encoding="utf-8"))
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    if (
        run_manifest.get("expected_count") != EXPECTED_COUNT
        or run_manifest.get("source_sha256") != PROMPT_SOURCE_SHA256
        or run_manifest.get("expected_generator") != EXPECTED_GENERATOR
        or catalog.get("generator") != EXPECTED_GENERATOR
    ):
        raise ValueError("Frozen local run manifest or catalog is incompatible")

    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    source_records: dict[str, dict[str, Any]] = {}
    for name, original in (("run_manifest", run_manifest_path), ("catalog", catalog_path)):
        copied = SOURCE_ROOT / original.name
        value = original.read_bytes()
        if copied.exists() and sha256_path(copied) != sha256_bytes(value):
            raise ValueError(f"Existing source snapshot differs: {copied}")
        atomic_bytes(copied, value)
        source_records[name] = {
            "source_path": str(original.resolve()),
            "local_path": str(copied.resolve()),
            "sha256": sha256_bytes(value),
            "bytes": len(value),
        }

    for row in rows:
        source_prompt = prompts.get(row["row_id"])
        if source_prompt is None or source_prompt.get("text") != row.get("prompt"):
            raise ValueError(f"Local prompt differs from frozen source: {row['row_id']}")
        if (
            source_prompt.get("device_id") != row.get("device_id")
            or source_prompt.get("device_type") != row.get("device_type")
            or source_prompt.get("source_camera_name") != row.get("camera_id")
            or source_prompt.get("camera_tag") != row.get("camera_tag")
            or int(source_prompt.get("bank_rank")) != row.get("bank_rank")
        ):
            raise ValueError(f"Local row mapping differs from source: {row['row_id']}")

    with ThreadPoolExecutor(max_workers=workers) as pool:
        generated_pairs = list(pool.map(load_generated, rows))
        job_results = list(pool.map(fetch_job, rows))
    generated = dict(generated_pairs)
    jobs = {item["row_id"]: item for item in job_results}

    twin_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        twin_groups[(row["device_id"], row["camera_id"])].append(jobs[row["row_id"]])
    if len(twin_groups) != 16 or any(len(items) != 10 for items in twin_groups.values()):
        raise ValueError("Expected sixteen ten-row device/camera twin groups")
    twins: dict[tuple[str, str], dict[str, Any]] = {}
    for (device, camera), items in sorted(twin_groups.items()):
        hashes = {item["twin_sha256"] for item in items}
        versions = {item["product_version"] for item in items}
        if len(hashes) != 1 or len(versions) != 1:
            raise ValueError(f"Actual twin changed within bank: {device}/{camera}")
        exemplar = items[0]
        local_path = TWIN_ROOT / f"{device}__{camera}.png"
        if local_path.exists() and sha256_path(local_path) != exemplar["twin_sha256"]:
            raise ValueError(f"Existing actual twin differs: {local_path}")
        atomic_bytes(local_path, exemplar["twin"])
        twins[(device, camera)] = {
            "render_id": f"{device}__{camera}",
            "filename": local_path.name,
            "local_path": str(local_path.resolve()),
            "sha256": exemplar["twin_sha256"],
            "bytes": exemplar["twin_bytes"],
            "width": exemplar["twin_width"],
            "height": exemplar["twin_height"],
            "source_artifact_url": exemplar["twin_url"],
            "source_artifact_name": "1_hero_white.png",
            "product_version": exemplar["product_version"],
            "verified_job_count": len(items),
            "all_job_artifact_hashes_identical": True,
        }

    records: list[dict[str, Any]] = []
    for row in rows:
        prompt = prompts[row["row_id"]]
        job = jobs[row["row_id"]]
        generated_image = generated[row["row_id"]]
        twin_image = twins[(row["device_id"], row["camera_id"])]
        candidate = row["row_id"].rsplit("::", 1)[1]
        records.append(
            {
                "id": row["row_id"].replace("::", "__"),
                "dataset_role": "evaluation_target_unlabeled",
                "product": PRODUCT_NAMES[row["device_id"]],
                "device": row["device_id"],
                "device_type": row["device_type"],
                "digital_twin_id": row["digital_twin_id"],
                "view": {
                    "camera_tag": row["camera_tag"],
                    "source_camera_name": row["camera_id"],
                },
                "image_stage": "scene_generation",
                "candidate_id": candidate,
                "scene_prompt": row["prompt"],
                "scene_prompt_sha256": sha256_bytes(row["prompt"].encode("utf-8")),
                "scene_prompt_source": {
                    "kind": "original_v6_2_prompt",
                    "prompt_key": row["row_id"],
                    "source_path": str(PROMPT_SOURCE),
                    "source_document_sha256": PROMPT_SOURCE_SHA256,
                    "prompt_record_sha256": canonical_sha256(prompt),
                    "bank_rank": row["bank_rank"],
                    "environment": row["environment"],
                    "rewritten_prompt_included": False,
                },
                "generated_image": generated_image,
                "twin_image": twin_image,
                "hashes": {
                    "generated_image_sha256": generated_image["sha256"],
                    "twin_image_sha256": twin_image["sha256"],
                    "scene_prompt_sha256": sha256_bytes(row["prompt"].encode("utf-8")),
                },
                "dimensions": {
                    "generated_image": {
                        "width": generated_image["width"],
                        "height": generated_image["height"],
                    },
                    "twin_image": {
                        "width": twin_image["width"],
                        "height": twin_image["height"],
                    },
                },
                "generation_provenance": {
                    "job_id": row["job_id"],
                    "status_url": job["status_url"],
                    "status_response_sha256": job["status_sha256"],
                    "endpoint_completed_at_utc": row["completed_at_utc"],
                    "product_version": job["product_version"],
                    "hero_detail": job["hero_detail"],
                },
                "stage_provenance": job["scene_evidence"],
                "label_provenance": {
                    "human_annotations_included": False,
                    "diagnostic_expectations_included": False,
                    "passed_to_judge": False,
                },
            }
        )

    type_counts = Counter(row["device_type"] for row in rows)
    device_counts = Counter(row["device_id"] for row in rows)
    manifest = {
        "schema_version": "placement-v3-evaluation-target-v1",
        "generated_at_utc": utc_now(),
        "expected_count": EXPECTED_COUNT,
        "dataset_role": "evaluation_target_unlabeled",
        "status": "collected_not_judged",
        "source_gallery_url": GALLERY_URL,
        "source_s3_prefix": f"s3://{BUCKET}/{PREFIX}/",
        "source_snapshot": source_records,
        "source_equivalence": {
            "local_generation_records_match_frozen_prompt_export": True,
            "endpoint_status_and_actual_twin_reverified": True,
        },
        "prompt_source": {
            "path": str(PROMPT_SOURCE),
            "sha256": PROMPT_SOURCE_SHA256,
        },
        "input_contract": {
            "runtime_fields": [
                "generated_image",
                "twin_image",
                "device_type",
                "scene_prompt",
                "image_stage",
            ],
            "image_stage": "scene_generation",
            "human_annotations_in_runtime": False,
            "rewritten_prompt_in_runtime": False,
        },
        "separation_from_training": {
            "target_contains_human_feedback": False,
            "target_contains_diagnostic_expectations": False,
            "user_feedback_training_manifests_are_not_sources": True,
            "visual_anchor_manifest_is_not_a_source": True,
        },
        "counts": {
            "records": len(records),
            "generated_images": len({row["generated_image"]["sha256"] for row in records}),
            "actual_twin_images": len({row["twin_image"]["sha256"] for row in records}),
            "device_types": dict(sorted(type_counts.items())),
            "devices": dict(sorted(device_counts.items())),
            "device_camera_banks": len(twin_groups),
            "local_generation_records": len(rows),
        },
        "validation": {
            "all_local_generation_rows_done": True,
            "all_local_generated_hashes_match_records": True,
            "all_prompts_match_frozen_v6_2_source": True,
            "all_endpoint_params_match_local_rows": True,
            "all_hero_and_scene_stages_done": True,
            "all_downstream_stages_skipped": True,
            "all_original_prompts_match_scene_debug": True,
            "all_actual_twins_verified_across_ten_jobs_per_bank": True,
            "missing_mappings": [],
        },
        "records": records,
    }
    atomic_json(MANIFEST_PATH, manifest)
    return validate_existing()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error("--workers must be between 1 and 16")
    result = validate_existing() if args.validate_only else collect(args.workers)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
