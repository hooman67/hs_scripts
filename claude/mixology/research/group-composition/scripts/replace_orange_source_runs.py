"""Replace the eight completed Mixology runs that used the superseded orange input.

This is deliberately separate from the general fal runner.  It archives the
complete old run folders, preserves every run's system/user prompt, model
settings and arrangement, then performs one source-aware Astra rewrite, one
Sunburst edit and one Astra critique per replacement.  Queue state is handled
by fal_transport, so an uncertain submission is never repeated blindly.
"""
from __future__ import annotations

import argparse
import base64
import concurrent.futures
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests
from PIL import Image

ROOT = Path("/home/colligo/hs_scripts/claude/mixology")
RUN = Path("/home/colligo/mixology_data/refraction_research_2026-10-19")
MODEL_SCRIPTS = ROOT / "research/model-access/scripts"
sys.path.insert(0, str(MODEL_SCRIPTS))
from fal_transport import call  # noqa: E402

IMAGE_ENDPOINT = "openai/gpt-image-2.5/sunburst/edit"
VISION_ENDPOINT = "openrouter/router/vision"
ASTRA = "openai/gpt-6-astra"
OLD_SOURCE_SHA256 = "823e2af02c08738a5dc68733bf7d9349623cb4f4611a0763c72dccf0d13b7cbc"
NEW_SOURCE_SHA256 = "152427247d881087c4e7835408c9f76e28ca40929b0b2dc4e89542137db257da"
NEW_SOURCE = RUN / "assets/ref_inputs/TCCC–Crafted-Sept-2026.png"
ARCHIVE = RUN / "_archive/composition_orange_source_replacement_2026-10-20T185455Z"
AUDIT = RUN / "_review/composition_orange_source_replacement_2026-10-20.json"

RUN_SPECS = {
    "v1small_trio_lineup": ("composition", "Image 1 red, Image 2 orange, Image 3 amber; one row left to right."),
    "v1small_trio_orange_front": ("composition", "Image 2 orange front-center; Image 1 red back-left; Image 3 amber back-right."),
    "v1small_trio_amber_front": ("composition", "Image 2 amber front-center; Image 1 red back-left; Image 3 orange back-right."),
    "v1fal_side_by_side": ("composition", "Images 1, 2, 3, 4 and 5 in one row from left to right."),
    "v1fal_staggered": ("composition", "Back row: Images 1, 3, 2. Front row: Images 4, 5."),
    "v2fal_side_by_side": ("composition", "Images 1, 2, 3, 4 and 5 in one row from left to right."),
    "v2fal_staggered": ("composition", "Back row: Images 1, 3, 5. Front row: Images 2, 4."),
    "v3fal_new_orange_ribbon": ("refraction", "One Image 1 drink only; preserve its camera, crop, cup and placement."),
}


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def save(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def load(path: Path) -> object:
    return json.loads(path.read_text())


def run_folder(kind: str, run_id: str) -> Path:
    return RUN / ("composition/runs" if kind == "composition" else "runs") / run_id


def archived_folder(kind: str, run_id: str) -> Path:
    return ARCHIVE / "old_runs" / kind / run_id


def image_record(path: Path, role: str, index: int) -> dict:
    with Image.open(path) as image:
        image.load()
        dimensions = list(image.size)
    return {
        "path": str(path),
        "role": role,
        "image_index": index,
        "sha256": digest(path),
        "dimensions": dimensions,
    }


def data_uri(path: Path | str) -> str:
    path = Path(path)
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def manifest_for(folders: dict[str, Path]) -> list[dict]:
    entries = []
    for run_id, folder in folders.items():
        for path in sorted(folder.rglob("*")):
            if path.is_symlink():
                raise RuntimeError(f"Archive source contains a symlink: {path}")
            if path.is_file():
                entries.append({
                    "run_id": run_id,
                    "relative_path": str(path.relative_to(folder)),
                    "bytes": path.stat().st_size,
                    "sha256": digest(path),
                })
    return entries


def validate_old_run(kind: str, run_id: str, folder: Path) -> dict:
    if not folder.is_dir():
        raise RuntimeError(f"Missing canonical old run folder: {folder}")
    record_path = folder / "record.json"
    output = folder / "output.png"
    judge = folder / "judge.json"
    if not record_path.is_file() or not output.is_file() or not judge.is_file():
        raise RuntimeError(f"Old run is not complete: {run_id}")
    record = load(record_path)
    if record["id"] != run_id or record["kind"] != kind or record["status"] != "complete":
        raise RuntimeError(f"Unexpected old record identity/status: {run_id}")
    if record["output_sha256"] != digest(output):
        raise RuntimeError(f"Old output hash mismatch: {run_id}")
    matches = [item for item in record["input_images"] if item["sha256"] == OLD_SOURCE_SHA256]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one superseded source in {run_id}")
    if digest(Path(matches[0]["path"])) != OLD_SOURCE_SHA256:
        raise RuntimeError(f"Superseded source bytes are unavailable for {run_id}")
    return record


def prepare_archive() -> None:
    if digest(NEW_SOURCE) != NEW_SOURCE_SHA256:
        raise RuntimeError("Durable new source is missing or has the wrong hash")
    if AUDIT.exists():
        audit = load(AUDIT)
        if audit.get("archive", {}).get("verified") is True:
            print(f"SKIP verified archive {ARCHIVE}")
            return
        raise RuntimeError(f"Incomplete prior archive attempt requires inspection: {AUDIT}")
    if ARCHIVE.exists():
        raise RuntimeError(f"Archive target already exists: {ARCHIVE}")

    canonical = {}
    old_records = {}
    for run_id, (kind, _) in RUN_SPECS.items():
        folder = run_folder(kind, run_id)
        canonical[run_id] = folder
        old_records[run_id] = validate_old_run(kind, run_id, folder)
    before = manifest_for(canonical)
    if not before:
        raise RuntimeError("Refusing to archive an empty replacement set")

    archive_map = {
        run_id: {
            "kind": RUN_SPECS[run_id][0],
            "canonical_path": str(canonical[run_id]),
            "archive_path": str(archived_folder(RUN_SPECS[run_id][0], run_id)),
            "old_record_sha256": digest(canonical[run_id] / "record.json"),
            "old_output_sha256": old_records[run_id]["output_sha256"],
        }
        for run_id in RUN_SPECS
    }
    audit = {
        "as_of": utc(),
        "status": "archiving",
        "scope": "Replace eight published results that used the superseded leaned-back orange source.",
        "old_source": {"sha256": OLD_SOURCE_SHA256},
        "new_source": {
            "path": str(NEW_SOURCE),
            "sha256": NEW_SOURCE_SHA256,
            "bytes": NEW_SOURCE.stat().st_size,
        },
        "run_ids": list(RUN_SPECS),
        "archive": {
            "root": str(ARCHIVE),
            "mapping": archive_map,
            "pre_move_file_count": len(before),
            "pre_move_total_bytes": sum(item["bytes"] for item in before),
            "pre_move_manifest_sha256": json_digest(before),
            "verified": False,
        },
        "unpublished_old_source_dependencies_not_replaced": [
            str(RUN / "composition/runs/v1_side_by_side"),
            str(RUN / "composition/runs/v1_staggered"),
        ],
    }
    ARCHIVE.mkdir(parents=True)
    save(ARCHIVE / "pre_move_manifest.json", before)
    save(AUDIT, audit)

    for run_id, (kind, _) in RUN_SPECS.items():
        destination = archived_folder(kind, run_id)
        destination.parent.mkdir(parents=True, exist_ok=True)
        canonical[run_id].rename(destination)

    moved = {run_id: archived_folder(RUN_SPECS[run_id][0], run_id) for run_id in RUN_SPECS}
    after = manifest_for(moved)
    if after != before:
        raise RuntimeError("Post-move archive manifest differs from the pre-move manifest")
    for run_id, (kind, _) in RUN_SPECS.items():
        if run_folder(kind, run_id).exists():
            raise RuntimeError(f"Canonical folder still exists after archive: {run_id}")
    save(ARCHIVE / "verified_manifest.json", after)
    audit["archive"].update({
        "verified": True,
        "verified_at": utc(),
        "verified_manifest": str(ARCHIVE / "verified_manifest.json"),
        "verified_manifest_sha256": json_digest(after),
    })
    audit["status"] = "archived"
    save(AUDIT, audit)
    print(f"ARCHIVED {len(RUN_SPECS)} runs, {len(after)} files")


def replacement_record(kind: str, run_id: str) -> tuple[Path, dict, dict]:
    archive = archived_folder(kind, run_id)
    old_record = load(archive / "record.json")
    new_folder = run_folder(kind, run_id)
    inputs = []
    replacements = 0
    for item in old_record["input_images"]:
        if item["sha256"] == OLD_SOURCE_SHA256:
            inputs.append(image_record(NEW_SOURCE, item["role"], item["image_index"]))
            replacements += 1
        else:
            path = Path(item["path"])
            current = image_record(path, item["role"], item["image_index"])
            if current != item:
                raise RuntimeError(f"Unchanged input drifted for {run_id}: {path}")
            inputs.append(current)
    if replacements != 1:
        raise RuntimeError(f"Expected one input replacement for {run_id}")

    keep = [
        "id", "version", "kind", "case_id", "case", "system_version", "system_prompt",
        "user_prompt", "provider", "fal_endpoint", "rewriter_model", "rewriter_endpoint",
        "rewriter_requested_model", "image_model", "quality", "size_requested", "output_format",
        "generation_mode", "provider_limitations",
    ]
    record = {field: old_record[field] for field in keep}
    if kind == "refraction":
        record["case"] = dict(record["case"])
        record["case"]["input"] = "ref_inputs/TCCC–Crafted-Sept-2026.png"
    record.update({
        "input_images": inputs,
        "status": "prepared",
        "prepared_at": utc(),
        "script_sha256": digest(__file__),
        "output": str(new_folder / "output.png"),
        "visual_review": None,
        "replacement": {
            "reason": "User replaced the leaned-back orange source with the upright source.",
            "archive_folder": str(archive),
            "old_record_sha256": digest(archive / "record.json"),
            "old_output_sha256": old_record["output_sha256"],
            "old_source_sha256": OLD_SOURCE_SHA256,
            "new_source_sha256": NEW_SOURCE_SHA256,
            "arrangement_lock": RUN_SPECS[run_id][1],
            "system_user_and_settings_preserved": True,
        },
    })
    return new_folder, record, old_record


def vision(system: str, prompt: str, images: list[dict], folder: Path, stage: str,
           max_tokens: int = 3000) -> dict:
    return call(VISION_ENDPOINT, {
        "model": ASTRA,
        "system_prompt": system,
        "prompt": prompt,
        "image_urls": [data_uri(item["path"]) for item in images],
        "max_tokens": max_tokens,
        "reasoning": True,
        "enable_web_search": False,
    }, folder, stage)


def rewrite_one(run_id: str) -> None:
    kind, arrangement = RUN_SPECS[run_id]
    folder, fresh, old = replacement_record(kind, run_id)
    folder.mkdir(parents=True, exist_ok=True)
    record_path = folder / "record.json"
    if record_path.exists():
        record = load(record_path)
        for field in ("system_prompt", "user_prompt", "input_images", "quality", "size_requested"):
            if record[field] != fresh[field]:
                raise RuntimeError(f"Existing replacement inputs/settings differ for {run_id}")
        if record["status"] in ("rewrite_complete", "image_running", "complete"):
            print(f"SKIP rewritten {run_id}")
            return
    else:
        record = fresh
        save(record_path, record)
        (folder / "system_prompt.md").write_text(record["system_prompt"])
        (folder / "user_prompt.txt").write_text(record["user_prompt"] + "\n")

    request = (
        record["user_prompt"]
        + "\n\nThis is a source replacement, not a new arrangement experiment. Preserve this exact arrangement: "
        + arrangement
        + "\nRewrite the prior image-editor prompt only as needed to describe the newly supplied orange source; "
          "keep its treatment, constraints and all unaffected drink mappings unchanged.\n\n"
        + "Prior image-editor prompt:\n"
        + old["image_prompt"]
        + "\n\nImages are supplied in this exact order:\n"
        + "\n".join(f'Image {index}: {item["role"]}.' for index, item in enumerate(record["input_images"], 1))
    )
    record.update(status="rewrite_running", started_at=record.get("started_at", utc()))
    save(record_path, record)
    started = time.monotonic()
    reply = vision(record["system_prompt"], request, record["input_images"], folder, "rewriter")
    prompt = reply["output"].strip()
    if not prompt or len(prompt) > 32000:
        raise RuntimeError(f"Empty or over-limit replacement prompt for {run_id}")
    if kind == "refraction" and not prompt.lower().startswith("relight image 1"):
        raise RuntimeError("V3 replacement rewrite violated its response contract")
    missing = [index for index in range(1, len(record["input_images"]) + 1)
               if f"Image {index}" not in prompt]
    if missing:
        raise RuntimeError(f"Replacement prompt omitted indexed inputs for {run_id}: {missing}")
    record.update({
        "status": "rewrite_complete",
        "image_prompt": prompt,
        "rewriter": {
            "requested_model": ASTRA,
            "returned_model": None,
            "provider": "fal.ai via OpenRouter",
            "request_prompt": request,
            "reasoning_effort": None,
            "reasoning_field": True,
            "seconds": round(time.monotonic() - started, 2),
            "usage": reply.get("usage"),
            "queue_record": str(folder / "rewriter_queue.json"),
        },
    })
    (folder / "image_prompt.txt").write_text(prompt + "\n")
    save(record_path, record)
    print(f"REWRITTEN {run_id}: {len(prompt.split())} words")


def generate_one(run_id: str) -> None:
    kind, _ = RUN_SPECS[run_id]
    folder = run_folder(kind, run_id)
    record_path = folder / "record.json"
    record = load(record_path)
    if record["status"] == "complete":
        print(f"SKIP complete {run_id}")
        return
    if record["status"] not in ("rewrite_complete", "image_running", "failed"):
        raise RuntimeError(f"Run is not ready for image generation: {run_id} ({record['status']})")
    record["status"] = "image_running"
    save(record_path, record)
    size = "auto" if record["size_requested"] == "auto" else {"width": 1536, "height": 1024}
    started = time.monotonic()
    try:
        result = call(IMAGE_ENDPOINT, {
            "prompt": record["image_prompt"],
            "image_urls": [data_uri(item["path"]) for item in record["input_images"]],
            "quality": record["quality"],
            "image_size": size,
            "num_images": 1,
            "output_format": record["output_format"],
            "enable_safety_checker": True,
        }, folder, "image")
        if len(result.get("images", [])) != 1:
            raise RuntimeError(f"Expected one replacement output for {run_id}")
        output = folder / "output.png"
        if not output.exists():
            url = result["images"][0]["url"]
            parsed = urlsplit(url)
            if parsed.scheme != "https" or not (parsed.hostname or "").endswith(".fal.media"):
                raise RuntimeError("Unexpected generated-image host")
            response = requests.get(url, timeout=(15, 120))
            response.raise_for_status()
            with output.open("xb") as stream:
                stream.write(response.content)
        with Image.open(output) as image:
            image.load()
            if image.format != "PNG":
                raise RuntimeError("Expected original PNG bytes")
            dimensions, mode = list(image.size), image.mode
        record.update({
            "status": "complete",
            "image_seconds": round(time.monotonic() - started, 2),
            "output_dimensions": dimensions,
            "output_mode": mode,
            "output_sha256": digest(output),
            "completed_at": utc(),
            "total_seconds": round(time.monotonic() - started, 2),
        })
        save(record_path, record)
        print(f"DONE {run_id}: {dimensions}")
    except Exception as error:
        record.update({
            "status": "failed",
            "error_type": type(error).__name__,
            "error_status": getattr(error, "status_code", None),
            "failed_at": utc(),
        })
        save(record_path, record)
        raise


def judge_one(run_id: str) -> None:
    kind, _ = RUN_SPECS[run_id]
    folder = run_folder(kind, run_id)
    record = load(folder / "record.json")
    if record["status"] != "complete":
        raise RuntimeError(f"Cannot critique incomplete replacement: {run_id}")
    judge_path = folder / "judge.json"
    if judge_path.exists():
        print(f"SKIP judged {run_id}")
        return
    old_judge = load(archived_folder(kind, run_id) / "judge.json")
    system = old_judge["_meta"]["system_prompt"]
    output_item = image_record(folder / "output.png", "candidate output", len(record["input_images"]) + 1)
    if kind == "composition":
        images = record["input_images"] + [output_item]
    else:
        images = [
            record["input_images"][0],
            image_record(folder / "output.png", "candidate output", 2),
            image_record(RUN / "assets" / record["case"]["positive"],
                         "approved lighting STYLE, different drink", 3),
            image_record(RUN / "assets/image_015_p06_xref590.jpg",
                         "rejected vein-like lighting style", 4),
        ]
    prompt = (
        "Evaluate the candidate and return JSON. User arrangement/request: "
        + record["user_prompt"]
        + "\n"
        + "\n".join(f'Image {index}: {item["role"]}' for index, item in enumerate(images, 1))
    )
    reply = vision(system, prompt, images, folder, "critic", max_tokens=3500)
    raw = reply["output"].strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    result = json.loads(raw)
    result["_meta"] = {
        "requested_model": ASTRA,
        "returned_model": None,
        "provider": "fal.ai via OpenRouter",
        "system_prompt": system,
        "request_prompt": prompt,
        "input_images": images,
        "usage": reply.get("usage"),
        "time": utc(),
        "reasoning_effort": None,
    }
    save(judge_path, result)
    print(f"JUDGED {run_id}: {result.get('verdict')}")


def run_parallel(function, workers: int) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(function, run_id) for run_id in RUN_SPECS]
        for future in concurrent.futures.as_completed(futures):
            future.result()


def finalize_audit() -> None:
    audit = load(AUDIT)
    if audit["archive"]["verified"] is not True:
        raise RuntimeError("Archive verification is incomplete")
    replacements = []
    output_hashes = set()
    for run_id, (kind, arrangement) in RUN_SPECS.items():
        old_record = load(archived_folder(kind, run_id) / "record.json")
        folder = run_folder(kind, run_id)
        record = load(folder / "record.json")
        judge = load(folder / "judge.json")
        if record["status"] != "complete" or record["output_sha256"] != digest(folder / "output.png"):
            raise RuntimeError(f"Replacement is incomplete or corrupt: {run_id}")
        if not record.get("visual_review"):
            raise RuntimeError(f"Direct visual review has not been recorded: {run_id}")
        for field in ("id", "version", "kind", "case_id", "system_version", "system_prompt",
                      "user_prompt", "quality", "size_requested", "output_format", "fal_endpoint",
                      "rewriter_requested_model", "image_model"):
            if record[field] != old_record[field]:
                raise RuntimeError(f"Preserved field changed for {run_id}: {field}")
        if len(record["input_images"]) != len(old_record["input_images"]):
            raise RuntimeError(f"Input count changed for {run_id}")
        changed = []
        for old_input, new_input in zip(old_record["input_images"], record["input_images"], strict=True):
            if old_input["image_index"] != new_input["image_index"] or old_input["role"] != new_input["role"]:
                raise RuntimeError(f"Input order/role changed for {run_id}")
            if old_input["sha256"] != new_input["sha256"]:
                changed.append((old_input["sha256"], new_input["sha256"]))
            elif old_input != new_input:
                raise RuntimeError(f"Unchanged input metadata drifted for {run_id}")
        if changed != [(OLD_SOURCE_SHA256, NEW_SOURCE_SHA256)]:
            raise RuntimeError(f"Unexpected source changes for {run_id}: {changed}")
        if record["output_sha256"] in output_hashes:
            raise RuntimeError(f"Duplicate replacement output bytes: {run_id}")
        output_hashes.add(record["output_sha256"])
        queues = {}
        for stage in ("rewriter", "image", "critic"):
            queues[stage] = load(folder / f"{stage}_queue.json")["request_id"]
        replacements.append({
            "run_id": run_id,
            "kind": kind,
            "canonical_folder": str(folder),
            "archive_folder": str(archived_folder(kind, run_id)),
            "arrangement_lock": arrangement,
            "system_version": record["system_version"],
            "user_prompt": record["user_prompt"],
            "input_images": record["input_images"],
            "image_prompt": record["image_prompt"],
            "image_prompt_sha256": hashlib.sha256(record["image_prompt"].encode()).hexdigest(),
            "settings": {
                "image_model": record["image_model"],
                "quality": record["quality"],
                "size_requested": record["size_requested"],
                "output_format": record["output_format"],
            },
            "queue_ids": queues,
            "old_output_sha256": old_record["output_sha256"],
            "new_output_sha256": record["output_sha256"],
            "output_dimensions": record["output_dimensions"],
            "judge_sha256": digest(folder / "judge.json"),
            "judge_verdict": judge.get("verdict"),
            "judge_dominant_failure": judge.get("dominant_failure"),
            "visual_review": record["visual_review"],
        })
    if len(replacements) != 8 or len(output_hashes) != 8:
        raise RuntimeError("Expected exactly eight distinct completed replacement outputs")
    audit.update({
        "status": "complete",
        "completed_at": utc(),
        "replacement_count": 8,
        "critique_count": 8,
        "replacements": replacements,
        "limitations": [
            "One sample per run; no repeatability or customer-acceptance claim.",
            "Astra and Sunburst backend snapshots are not exposed by the fal response schemas.",
            "Critique scores are advisory; direct visual reviews remain qualitative.",
            "No postprocessing or speculative revision was performed.",
        ],
    })
    save(AUDIT, audit)
    print(f"FINALIZED {AUDIT}")


def main() -> None:
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "rewrite", "generate", "judge", "finalize"))
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.workers <= 4:
        parser.error("--workers must be between 1 and 4")
    if args.action == "prepare":
        prepare_archive()
    elif args.action == "rewrite":
        run_parallel(rewrite_one, args.workers)
    elif args.action == "generate":
        run_parallel(generate_one, args.workers)
    elif args.action == "judge":
        run_parallel(judge_one, args.workers)
    else:
        finalize_audit()


if __name__ == "__main__":
    main()
