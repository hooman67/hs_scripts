#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "httpx", "pillow"]
# ///
"""Generate the frozen V6.1 160-prompt set with the HP GPT-Image scene endpoint.

The queue is deliberately interleaved across device and camera banks. Every
completed image is checkpointed locally and uploaded with a refreshed live
gallery, so a reviewer can inspect all product families while the run continues.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import boto3
import httpx
from PIL import Image


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
PROMPTS = (
    PROJECT
    / "eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103"
    / "revisions/v6.1-expanded-20261103-r6/exports/final/prompts_all_160.json"
)
PROMPTS_SHA256 = "adcb9edb2643e45acb0cb882cdc4d65b8c256a52d58ad4a44ddd9c235287b3cd"
BASE_URL = "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev"
EXPECTED_GENERATOR = "GPT Image 2.5 / single reference / no grading"
EXPECTED_COUNT = 160
EXPECTED_SIZE = (2368, 1776)
RUN_DIR = HERE / "run"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_phrase_diversity_v6_1_gpt_image2_scene_20261105"
REGION = "us-west-2"
GATEWAY = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}"
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
    temporary = path.with_suffix(path.suffix + f".{os.getpid()}.{threading.get_ident()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def atomic_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".{os.getpid()}.{threading.get_ident()}.tmp")
    temporary.write_bytes(value)
    os.replace(temporary, path)


def client() -> tuple[httpx.Client, str]:
    existing = getattr(THREAD_LOCAL, "endpoint", None)
    csrf = getattr(THREAD_LOCAL, "csrf", None)
    if existing is None or not csrf:
        existing = httpx.Client(timeout=httpx.Timeout(60.0, connect=30.0), follow_redirects=True)
        response = existing.get(f"{BASE_URL}/api/credentials")
        response.raise_for_status()
        csrf = response.json()["csrfToken"]
        THREAD_LOCAL.endpoint = existing
        THREAD_LOCAL.csrf = csrf
    return existing, csrf


def slug(row_id: str) -> str:
    return row_id.replace("::", "__").replace("/", "_")


def validate_prompt_document(document: dict[str, Any]) -> list[dict[str, Any]]:
    prompts = document.get("prompts")
    if sha256_path(PROMPTS) != PROMPTS_SHA256:
        raise ValueError("Frozen V6.1 prompt export hash changed")
    if not isinstance(prompts, list) or len(prompts) != EXPECTED_COUNT:
        raise ValueError("Expected exactly 160 frozen V6.1 prompts")
    seen: set[str] = set()
    counts: dict[tuple[str, str], int] = {}
    ranks: dict[tuple[str, str], set[int]] = {}
    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        key = prompt["prompt_key"]
        device = prompt["device_id"]
        camera = prompt["source_camera_name"]
        rank = int(prompt["bank_rank"])
        if key in seen or device not in DEVICE_MAP or camera not in VIEW_ORDER[device]:
            raise ValueError(f"Invalid or duplicate prompt mapping: {key}")
        seen.add(key)
        bank = (device, camera)
        counts[bank] = counts.get(bank, 0) + 1
        ranks.setdefault(bank, set()).add(rank)
        rows.append(
            {
                "row_id": key,
                "row_slug": slug(key),
                "prompt": prompt,
                "device_id": device,
                "digital_twin_id": DEVICE_MAP[device],
                "camera_id": camera,
                "rank": rank,
                "prompt_sha256": sha256_bytes(prompt["text"].encode("utf-8")),
                "prompt_record_sha256": canonical_sha256(prompt),
            }
        )
    expected_banks = {(device, camera) for device in DEVICE_ORDER for camera in VIEW_ORDER[device]}
    if set(counts) != expected_banks or any(count != 10 for count in counts.values()):
        raise ValueError("Expected 16 device/view banks with ten prompts each")
    if any(value != set(range(1, 11)) for value in ranks.values()):
        raise ValueError("Every bank must contain ranks 1 through 10")
    return rows


def interleave(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key = {(row["device_id"], row["camera_id"], row["rank"]): row for row in rows}
    ordered: list[dict[str, Any]] = []
    # A Latin-square bank schedule makes each four-task wave contain all devices
    # and all four view positions. Repeat it rank-by-rank for even early coverage.
    for rank in range(1, 11):
        for wave in range(4):
            for device_index, device in enumerate(DEVICE_ORDER):
                camera = VIEW_ORDER[device][(wave + device_index) % 4]
                ordered.append(by_key[(device, camera, rank)])
    if len(ordered) != EXPECTED_COUNT or len({row["row_id"] for row in ordered}) != EXPECTED_COUNT:
        raise ValueError("Interleaved queue is incomplete")
    return ordered


def validate_catalog(catalog: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    if catalog.get("generator") != EXPECTED_GENERATOR:
        raise ValueError(f"Unexpected live generator: {catalog.get('generator')!r}")
    twins = {item["id"]: item for item in catalog.get("digitalTwins", [])}
    for row in rows:
        twin = twins.get(row["digital_twin_id"])
        cameras = {item["id"] for item in (twin or {}).get("cameras", [])}
        if not twin or row["camera_id"] not in cameras:
            raise ValueError(f"Missing live twin/camera mapping for {row['row_id']}")


def record_path(row: dict[str, Any]) -> Path:
    return RUN_DIR / "records" / f"{row['row_slug']}.json"


def job_path(row: dict[str, Any]) -> Path:
    return RUN_DIR / "jobs" / f"{row['row_slug']}.json"


def image_path(row: dict[str, Any]) -> Path:
    return RUN_DIR / "images" / f"{row['row_slug']}.png"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def valid_completed_record(row: dict[str, Any]) -> dict[str, Any] | None:
    path = record_path(row)
    image = image_path(row)
    if not path.is_file() or not image.is_file():
        return None
    record = load_json(path)
    if (
        record.get("status") != "done"
        or record.get("row_id") != row["row_id"]
        or record.get("prompt_sha256") != row["prompt_sha256"]
        or record.get("image_sha256") != sha256_path(image)
    ):
        return None
    return record


def submit(row: dict[str, Any], catalog_sha256: str) -> dict[str, Any]:
    endpoint, csrf = client()
    payload = {
        "digitalTwinId": row["digital_twin_id"],
        "cameraId": row["camera_id"],
        "prompt": row["prompt"]["text"],
    }
    response = endpoint.post(
        f"{BASE_URL}/api/generate",
        json=payload,
        headers={"Origin": BASE_URL, "x-hp12-csrf": csrf},
    )
    response.raise_for_status()
    submitted = response.json()
    job = {
        "schema_version": 1,
        "row_id": row["row_id"],
        "submitted_at_utc": now(),
        "request": payload,
        "request_sha256": canonical_sha256(payload),
        "catalog_sha256": catalog_sha256,
        "submit_response": submitted,
        "status_url": urljoin(BASE_URL, submitted["statusUrl"]),
        "image_url": urljoin(BASE_URL, submitted["imageUrl"]),
    }
    atomic_json(job_path(row), job)
    return job


def process(row: dict[str, Any], catalog_sha256: str, poll_seconds: int) -> dict[str, Any]:
    completed = valid_completed_record(row)
    if completed:
        return completed
    job_file = job_path(row)
    if job_file.is_file():
        job = load_json(job_file)
        if job.get("row_id") != row["row_id"] or job.get("request", {}).get("prompt") != row["prompt"]["text"]:
            raise ValueError(f"Existing job identity mismatch: {row['row_id']}")
    else:
        job = submit(row, catalog_sha256)

    endpoint, _ = client()
    deadline = time.monotonic() + poll_seconds
    poll_count = 0
    final_status: dict[str, Any] | None = None
    while time.monotonic() < deadline:
        poll_count += 1
        try:
            response = endpoint.get(job["status_url"])
            response.raise_for_status()
            status = response.json()
        except (httpx.HTTPError, ValueError):
            time.sleep(5)
            continue
        if status.get("done"):
            final_status = status
            break
        time.sleep(5)
    if final_status is None:
        raise TimeoutError(f"Polling timed out for {row['row_id']}; resume the saved job")

    atomic_json(RUN_DIR / "status" / f"{row['row_slug']}.json", final_status)
    stages = final_status.get("stages", {})
    scene = stages.get("scene", {})
    if scene.get("status") != "done" or not scene.get("has_image"):
        record = {
            "schema_version": 1,
            "row_id": row["row_id"],
            "status": "failed",
            "completed_at_utc": now(),
            "prompt_sha256": row["prompt_sha256"],
            "job_id": final_status.get("jobId"),
            "error": scene.get("error") or "scene stage did not return an image",
            "final_status": final_status,
        }
        atomic_json(record_path(row), record)
        return record
    for skipped in ("ibl", "backplate", "recomposite", "relight"):
        if stages.get(skipped, {}).get("status") != "skipped":
            raise ValueError(f"{row['row_id']} unexpectedly ran downstream stage {skipped}")

    image_response = endpoint.get(job["image_url"], timeout=180.0)
    image_response.raise_for_status()
    atomic_bytes(image_path(row), image_response.content)
    with Image.open(image_path(row)) as generated:
        generated.verify()
    with Image.open(image_path(row)) as generated:
        dimensions = generated.size
        image_format = generated.format
    if dimensions != EXPECTED_SIZE or image_format != "PNG":
        raise ValueError(f"Unexpected image output for {row['row_id']}: {dimensions}, {image_format}")

    record = {
        "schema_version": 1,
        "row_id": row["row_id"],
        "row_slug": row["row_slug"],
        "status": "done",
        "completed_at_utc": now(),
        "queue_position": row["queue_position"],
        "device_id": row["device_id"],
        "digital_twin_id": row["digital_twin_id"],
        "device_type": row["prompt"]["device_type"],
        "camera_id": row["camera_id"],
        "camera_tag": row["prompt"]["camera_tag"],
        "bank_rank": row["rank"],
        "environment": row["prompt"]["environment"],
        "source_relevance_score": row["prompt"]["source_relevance_score"],
        "ctech_reference_score": row["prompt"]["ctech_reference_score"],
        "prompt": row["prompt"]["text"],
        "prompt_sha256": row["prompt_sha256"],
        "prompt_record_sha256": row["prompt_record_sha256"],
        "job_id": final_status.get("jobId"),
        "status_url": job["status_url"],
        "image_source_url": job["image_url"],
        "image_filename": image_path(row).name,
        "image_sha256": sha256_path(image_path(row)),
        "image_bytes": image_path(row).stat().st_size,
        "image_dimensions": {"width": dimensions[0], "height": dimensions[1]},
        "poll_count": poll_count,
        "runtime": final_status.get("params", {}),
        "scene_debug": scene.get("detail", {}),
    }
    atomic_json(record_path(row), record)
    return record


def all_records() -> list[dict[str, Any]]:
    return [load_json(path) for path in sorted((RUN_DIR / "records").glob("*.json"))]


def gallery_document(rows: list[dict[str, Any]], catalog: dict[str, Any]) -> dict[str, Any]:
    records = {record["row_id"]: record for record in all_records()}
    output_rows = []
    for row in rows:
        record = records.get(row["row_id"])
        output_rows.append(
            {
                "row_id": row["row_id"],
                "queue_position": row["queue_position"],
                "device_id": row["device_id"],
                "digital_twin_id": row["digital_twin_id"],
                "device_type": row["prompt"]["device_type"],
                "camera_id": row["camera_id"],
                "camera_tag": row["prompt"]["camera_tag"],
                "bank_rank": row["rank"],
                "environment": row["prompt"]["environment"],
                "source_relevance_score": row["prompt"]["source_relevance_score"],
                "ctech_reference_score": row["prompt"]["ctech_reference_score"],
                "prompt": row["prompt"]["text"],
                "status": record.get("status") if record else "queued",
                "image_url": (
                    f"{GATEWAY}/images/{row['row_slug']}.png"
                    if record and record.get("status") == "done"
                    else None
                ),
                "job_id": record.get("job_id") if record else None,
                "scene_debug": record.get("scene_debug") if record else None,
                "completed_at_utc": record.get("completed_at_utc") if record else None,
            }
        )
    counts: dict[str, int] = {}
    for output in output_rows:
        counts[output["status"]] = counts.get(output["status"], 0) + 1
    return {
        "schema_version": 1,
        "title": "HP Lifestyle V6.1 — GPT Image 2.5 Scene Generations",
        "updated_at_utc": now(),
        "expected_count": EXPECTED_COUNT,
        "status_counts": counts,
        "queue_policy": "Latin-square device/view interleave repeated for ranks 1–10",
        "endpoint": f"{BASE_URL}/api/generate",
        "catalog": {
            "generator": catalog.get("generator"),
            "rewriterVersion": catalog.get("rewriterVersion"),
            "referenceCount": catalog.get("referenceCount"),
        },
        "source": {"path": str(PROMPTS), "sha256": PROMPTS_SHA256},
        "rows": output_rows,
    }


def viewer_html() -> bytes:
    page = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HP Lifestyle V6.1 — GPT Image 2.5</title>
<style>
body{margin:0;font:14px/1.45 system-ui;background:#101319;color:#e7ebf2}header{position:sticky;top:0;z-index:3;padding:14px 20px;background:#171c25;border-bottom:1px solid #343c4b}h1{margin:0 0 7px;font-size:20px}.meta{color:#aeb8c8}.filters{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}select,input{background:#0f131a;color:#e7ebf2;border:1px solid #3a4454;border-radius:6px;padding:7px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:14px;padding:16px}.card{background:#181e27;border:1px solid #323b4a;border-radius:10px;overflow:hidden}.card img{width:100%;aspect-ratio:4/3;object-fit:contain;background:#0b0e13}.waiting{display:grid;place-items:center;aspect-ratio:4/3;background:#0b0e13;color:#718096}.body{padding:12px}.tags{display:flex;gap:6px;flex-wrap:wrap}.tag{background:#273043;border-radius:999px;padding:3px 8px}.prompt{margin:10px 0;white-space:pre-wrap}.scores{color:#aeb8c8}details{border-top:1px solid #303847;padding-top:8px}pre{white-space:pre-wrap;word-break:break-word;font-size:11px}.done{color:#6ee7a2}.failed{color:#ff8a8a}.queued{color:#aeb8c8}
</style></head><body><header><h1 id="title">HP Lifestyle V6.1 — GPT Image 2.5</h1><div id="meta" class="meta">Loading…</div><div class="filters"><select id="device"><option value="">All devices</option></select><select id="camera"><option value="">All views</option></select><select id="status"><option value="done">Completed only</option><option value="">All statuses</option><option value="failed">Failed</option></select><input id="search" placeholder="Search prompts"></div></header><main id="grid" class="grid"></main><script>
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));let data;
function option(id,values){const e=document.getElementById(id);[...new Set(values)].sort().forEach(v=>e.insertAdjacentHTML('beforeend',`<option>${esc(v)}</option>`))}
function render(){const d=document.getElementById('device').value,c=document.getElementById('camera').value,s=document.getElementById('status').value,q=document.getElementById('search').value.toLowerCase();const rows=data.rows.filter(r=>(!d||r.device_id===d)&&(!c||r.camera_id===c)&&(!s||r.status===s)&&(!q||r.prompt.toLowerCase().includes(q)));document.getElementById('grid').innerHTML=rows.map(r=>`<article class="card">${r.image_url?`<a href="${esc(r.image_url)}" target="_blank"><img loading="lazy" src="${esc(r.image_url)}"></a>`:`<div class="waiting ${esc(r.status)}">${esc(r.status)}</div>`}<div class="body"><div class="tags"><span class="tag">#${r.queue_position}</span><span class="tag">${esc(r.device_id)}</span><span class="tag">${esc(r.camera_id)}</span><span class="tag">rank ${r.bank_rank}</span><span class="tag">${esc(r.environment)}</span></div><div class="prompt">${esc(r.prompt)}</div><div class="scores">Source ${r.source_relevance_score} · C-Tech ${r.ctech_reference_score} · <span class="${esc(r.status)}">${esc(r.status)}</span></div>${r.scene_debug?`<details><summary>Pipeline debug</summary><pre>${esc(JSON.stringify(r.scene_debug,null,2))}</pre></details>`:''}</div></article>`).join('');}
async function load(){try{data=await fetch(`data.json?t=${Date.now()}`,{cache:'no-store'}).then(r=>r.json());document.getElementById('title').textContent=data.title;const counts=data.status_counts;document.getElementById('meta').textContent=`${counts.done||0}/${data.expected_count} completed · ${counts.failed||0} failed · updated ${data.updated_at_utc} · ${data.catalog.generator} · auto-refreshes every 30s`;if(!document.getElementById('device').dataset.ready){option('device',data.rows.map(r=>r.device_id));option('camera',data.rows.map(r=>r.camera_id));document.getElementById('device').dataset.ready=1;['device','camera','status','search'].forEach(id=>document.getElementById(id).addEventListener(id==='search'?'input':'change',render));}render();}catch(e){document.getElementById('meta').textContent=`Refresh error: ${e}`}}
load();setInterval(load,30000);
</script></body></html>'''
    return page.encode("utf-8")


def publish(rows: list[dict[str, Any]], catalog: dict[str, Any]) -> None:
    s3 = boto3.client("s3", region_name=REGION)
    records = all_records()
    for record in records:
        if record.get("status") != "done":
            continue
        row = next(item for item in rows if item["row_id"] == record["row_id"])
        key = f"{PREFIX}/images/{row['row_slug']}.png"
        if not record.get("published_image_sha256"):
            image = image_path(row)
            s3.upload_file(
                str(image), BUCKET, key,
                ExtraArgs={"ContentType": "image/png", "Metadata": {"sha256": record["image_sha256"]}},
            )
            record["published_image_sha256"] = record["image_sha256"]
            atomic_json(record_path(row), record)
    document = gallery_document(rows, catalog)
    data = json.dumps(document, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    s3.put_object(Bucket=BUCKET, Key=f"{PREFIX}/gallery/data.json", Body=data, ContentType="application/json", CacheControl="no-store")
    s3.put_object(Bucket=BUCKET, Key=f"{PREFIX}/gallery/index.html", Body=viewer_html(), ContentType="text/html; charset=utf-8", CacheControl="no-store")
    s3.put_object(Bucket=BUCKET, Key=f"{PREFIX}/artifacts/results.json", Body=data, ContentType="application/json", CacheControl="no-store")


def summary(rows: list[dict[str, Any]], catalog: dict[str, Any]) -> dict[str, Any]:
    document = gallery_document(rows, catalog)
    value = {
        "schema_version": 1,
        "updated_at_utc": document["updated_at_utc"],
        "expected_count": EXPECTED_COUNT,
        "status_counts": document["status_counts"],
        "gallery_url": f"{GATEWAY}/gallery/index.html",
        "generator": catalog.get("generator"),
        "rewriterVersion": catalog.get("rewriterVersion"),
        "queue_policy": document["queue_policy"],
    }
    atomic_json(RUN_DIR / "summary.json", value)
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--poll-seconds", type=int, default=2400)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error("--workers must be between 1 and 8")
    if args.limit is not None and not 1 <= args.limit <= EXPECTED_COUNT:
        parser.error("--limit must be between 1 and 160")

    document = json.loads(PROMPTS.read_text(encoding="utf-8"))
    rows = interleave(validate_prompt_document(document))
    for position, row in enumerate(rows, start=1):
        row["queue_position"] = position
    catalog_response = httpx.get(f"{BASE_URL}/api/catalog", timeout=60.0)
    catalog_response.raise_for_status()
    catalog = catalog_response.json()
    validate_catalog(catalog, rows)
    catalog_sha256 = canonical_sha256(catalog)
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    for directory in ("jobs", "records", "status", "images"):
        (RUN_DIR / directory).mkdir(exist_ok=True)
    if not (RUN_DIR / "catalog.json").exists():
        atomic_json(RUN_DIR / "catalog.json", catalog)
    elif canonical_sha256(load_json(RUN_DIR / "catalog.json")) != catalog_sha256:
        raise ValueError("Live endpoint catalog changed after this run began; start a separate run")
    atomic_json(
        RUN_DIR / "run_manifest.json",
        {
            "schema_version": 1,
            "created_at_utc": now(),
            "source_path": str(PROMPTS),
            "source_sha256": PROMPTS_SHA256,
            "endpoint": f"{BASE_URL}/api/generate",
            "expected_generator": EXPECTED_GENERATOR,
            "catalog_sha256": catalog_sha256,
            "rewriterVersion": catalog.get("rewriterVersion"),
            "queue_policy": "Latin-square device/view interleave repeated for ranks 1–10",
            "device_map": DEVICE_MAP,
            "expected_count": EXPECTED_COUNT,
            "s3_uri": f"s3://{BUCKET}/{PREFIX}/",
            "gallery_url": f"{GATEWAY}/gallery/index.html",
        },
    )
    publish(rows, catalog)
    if args.preflight_only:
        print(json.dumps(summary(rows, catalog), indent=2))
        return 0

    selected = rows[: args.limit] if args.limit else rows
    print(f"Starting {len(selected)} rows with {args.workers} workers; gallery={GATEWAY}/gallery/index.html", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(process, row, catalog_sha256, args.poll_seconds): row for row in selected}
        for future in as_completed(futures):
            row = futures[future]
            try:
                record = future.result()
                print(f"{record['status']} #{row['queue_position']} {row['row_id']}", flush=True)
            except Exception as exc:  # noqa: BLE001
                error = {
                    "schema_version": 1,
                    "row_id": row["row_id"],
                    "status": "failed",
                    "completed_at_utc": now(),
                    "prompt_sha256": row["prompt_sha256"],
                    "error": f"{type(exc).__name__}: {exc}",
                }
                atomic_json(record_path(row), error)
                print(f"failed #{row['queue_position']} {row['row_id']}: {error['error']}", file=sys.stderr, flush=True)
            with WRITE_LOCK:
                try:
                    publish(rows, catalog)
                except Exception as exc:  # noqa: BLE001
                    print(f"incremental publish failed: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
                print(json.dumps(summary(rows, catalog), ensure_ascii=False), flush=True)
    publish(rows, catalog)
    print(json.dumps(summary(rows, catalog), indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
