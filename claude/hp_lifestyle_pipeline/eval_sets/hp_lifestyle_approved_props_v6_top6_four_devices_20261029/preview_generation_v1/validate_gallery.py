#!/usr/bin/env python3
"""Validate the V6 preview-generation gallery without endpoint or S3 access."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from build_gallery import (
    DEFAULT_RUN_DIR,
    EXPECTED_BANKS,
    EXPECTED_DISPLAY_PER_BANK,
    EXPECTED_DISPLAY_ROWS,
    EXPECTED_GENERATED_PER_BANK,
    EXPECTED_GENERATED_ROWS,
    EXPECTED_RENDERS,
    SENSITIVE_MARKERS,
    assert_sanitized,
    sha256_path,
)


STATIC_FILES = {"index.html", "main.js", "style.css", "imsauth.js", "data.js"}
DOWNLOAD_FILES = {
    "image_generation_manifest.json",
    "prompts_all_160.json",
    "prompts_top6_96.json",
    "results.jsonl",
    "source_inputs_r44.json",
    "recovery_manifest.json",
}
REQUIRED_COLUMNS = (
    "Prompt + scores",
    "Corrected digital twin",
    "Smart Brief + source messaging",
    "Explanation + provenance",
    "Generated output",
    "Rewritten prompt",
    "Full debug / request",
)


def read_data(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    match = re.fullmatch(r"const GENERATION_DATA = (.*);\n?", raw, re.DOTALL)
    if not match:
        raise ValueError("Gallery data.js envelope differs")
    return json.loads(match.group(1))


def validate(run_dir: Path, final: bool = False) -> dict[str, Any]:
    gallery = run_dir / "gallery"
    actual_static = {path.name for path in gallery.iterdir() if path.is_file()}
    if actual_static != STATIC_FILES:
        raise ValueError(f"Gallery static-file inventory differs: {sorted(actual_static)}")
    actual_downloads = {path.name for path in (run_dir / "downloads").iterdir() if path.is_file()}
    if actual_downloads != DOWNLOAD_FILES:
        raise ValueError(f"Gallery download inventory differs: {sorted(actual_downloads)}")
    index = (gallery / "index.html").read_text(encoding="utf-8")
    main = (gallery / "main.js").read_text(encoding="utf-8")
    if not re.search(r"<thead><tr>.*?</tr></thead>", index, flags=re.DOTALL):
        raise ValueError("Column headers are not inside the table head")
    for column in REQUIRED_COLUMNS:
        if column not in index:
            raise ValueError(f"Gallery UI lacks required column: {column}")
    for control in ("searchInput", "environmentFilter", "deviceFilter", "sourcePairFilter", "cameraFilter", "bankFilter", "statusFilter", "prevBank", "nextBank"):
        if control not in index or control not in main:
            raise ValueError(f"Gallery UI lacks required filter behavior: {control}")
    for collapsed in ("View Smart Brief", "View source messaging", "View explanation + score metadata", "View rewritten prompt", "View full debug / request"):
        if collapsed not in main:
            raise ValueError(f"Gallery UI lacks collapsed detail: {collapsed}")

    data = read_data(gallery / "data.js")
    assert_sanitized(data)
    metadata = data.get("metadata") or {}
    rows = data.get("rows") or []
    banks = data.get("banks") or []
    sources = data.get("sources") or {}
    if len(rows) != EXPECTED_DISPLAY_ROWS or metadata.get("row_count") != EXPECTED_DISPLAY_ROWS:
        raise ValueError(f"Gallery must contain {EXPECTED_DISPLAY_ROWS} candidate rows")
    if len({row["row_id"] for row in rows}) != EXPECTED_DISPLAY_ROWS:
        raise ValueError("Gallery row IDs are not unique")
    if len({row["prompt_key"] for row in rows}) != EXPECTED_DISPLAY_ROWS:
        raise ValueError("Gallery prompt keys are not unique")
    bank_counts = {
        bank_id: sum(row["bank_id"] == bank_id for row in rows)
        for bank_id in {row["bank_id"] for row in rows}
    }
    if len(bank_counts) != EXPECTED_BANKS or set(bank_counts.values()) != {EXPECTED_DISPLAY_PER_BANK}:
        raise ValueError(f"Gallery bank inventory differs: {bank_counts}")
    if len(banks) != EXPECTED_BANKS or len({bank["bank_id"] for bank in banks}) != EXPECTED_BANKS:
        raise ValueError("Gallery must contain 16 unique bank descriptors")
    bank_descriptors = {bank["bank_id"]: bank for bank in banks}
    if set(bank_descriptors) != set(bank_counts):
        raise ValueError("Bank descriptors and candidate rows differ")
    for bank_id, bank in bank_descriptors.items():
        if bank.get("candidate_count") != EXPECTED_DISPLAY_PER_BANK:
            raise ValueError(f"Bank candidate count differs for {bank_id}")
        if bank.get("generated_selection_count") != EXPECTED_GENERATED_PER_BANK or bank.get("prompt_only_count") != EXPECTED_DISPLAY_PER_BANK - EXPECTED_GENERATED_PER_BANK:
            raise ValueError(f"Bank generation selection differs for {bank_id}")
        bank_rows = sorted(
            (row for row in rows if row["bank_id"] == bank_id),
            key=lambda row: row["candidate"]["bank_rank"],
        )
        if bank.get("prompt_keys") != [row["prompt_key"] for row in bank_rows]:
            raise ValueError(f"Bank prompt order differs for {bank_id}")
        if [row["candidate"]["bank_rank"] for row in bank_rows] != list(range(1, 11)):
            raise ValueError(f"Bank ranks differ for {bank_id}")
    if len(sources) != EXPECTED_BANKS:
        raise ValueError(f"Gallery must contain {EXPECTED_BANKS} source-document banks")

    downloads = metadata.get("downloads") or []
    if len(downloads) != len(DOWNLOAD_FILES):
        raise ValueError("Gallery must link the manifest, prompts, results, and source inputs")
    for item in downloads:
        path = (gallery / item["path"]).resolve()
        if path.parent != (run_dir / "downloads").resolve():
            raise ValueError(f"Download escapes the gallery run: {path}")
        if not path.is_file() or sha256_path(path) != item["sha256"]:
            raise ValueError(f"Download is missing or changed: {path}")

    statuses = {"done": 0, "pending": 0, "failed": 0, "prompt_only": 0}
    corrected_hashes: dict[str, str] = {}
    generated_paths: set[Path] = set()
    for row in rows:
        status = row.get("status")
        if status not in statuses:
            raise ValueError(f"Unknown row status for {row['row_id']}: {status}")
        statuses[status] += 1
        candidate = row.get("candidate") or {}
        for field in (
            "text",
            "environment",
            "view_role",
            "bank_rank",
            "source_relevance_score",
            "ctech_reference_score",
            "score_components",
            "evidence",
            "explanation",
            "ctech_explanation",
            "camera_fit_explanation",
        ):
            if field not in candidate:
                raise ValueError(f"Candidate metadata lacks {field}: {row['row_id']}")
        source = sources.get(row["bank_id"]) or {}
        if not source.get("smart_brief") or not source.get("source_messaging"):
            raise ValueError(f"Source documents are incomplete for {row['bank_id']}")
        if source.get("camera_tag") != row["camera_tag"]:
            raise ValueError(f"Source camera tag differs for {row['row_id']}")
        source_path = Path(source.get("input_path", ""))
        if not source_path.is_file() or sha256_path(source_path) != source.get("input_sha256"):
            raise ValueError(f"Source input bytes differ for {row['row_id']}")
        render = row.get("corrected_input") or {}
        corrected = run_dir / render.get("gallery_path", "")
        if not corrected.is_file() or corrected.stat().st_size != render.get("bytes"):
            raise ValueError(f"Corrected digital twin is missing for {row['row_id']}")
        if sha256_path(corrected) != render.get("sha256"):
            raise ValueError(f"Corrected digital-twin hash differs for {row['row_id']}")
        corrected_hashes[row["render_id"]] = render["sha256"]
        record = row.get("record")
        if status == "done":
            if not record or "usedPrompt" not in record or "debugData" not in record:
                raise ValueError(f"Done record lacks rewrite/debug data for {row['row_id']}")
            if record.get("request_payload", {}).get("prompt") != candidate["text"]:
                raise ValueError(f"Done request prompt differs for {row['row_id']}")
            output = record.get("generated_image") or {}
            image = (run_dir / output.get("gallery_path", "")).resolve()
            if image.parent != (run_dir / "images").resolve():
                raise ValueError(f"Generated output escapes the V6 run: {row['row_id']}")
            if not image.is_file() or image.stat().st_size != output.get("bytes"):
                raise ValueError(f"Generated output is missing for {row['row_id']}")
            if sha256_path(image) != output.get("sha256"):
                raise ValueError(f"Generated output hash differs for {row['row_id']}")
            generated_paths.add(image)
            if candidate["bank_rank"] > EXPECTED_GENERATED_PER_BANK:
                raise ValueError(f"A rank outside the top six has a generated image: {row['row_id']}")
        elif status == "prompt_only":
            if candidate["bank_rank"] <= EXPECTED_GENERATED_PER_BANK:
                raise ValueError(f"A top-six candidate is incorrectly prompt-only: {row['row_id']}")
            if record is not None:
                raise ValueError(f"Prompt-only row has a generation record: {row['row_id']}")
        elif record and record.get("status") != status:
            raise ValueError(f"Projected and durable status differ for {row['row_id']}")
    if len(corrected_hashes) != EXPECTED_RENDERS:
        raise ValueError(f"Gallery must byte-verify {EXPECTED_RENDERS} corrected digital twins")
    image_inventory = {path.resolve() for path in (run_dir / "images").glob("*") if path.is_file()}
    if final and generated_paths != image_inventory:
        raise ValueError("Generated-image inventory differs from gallery done rows")
    if statuses != metadata.get("status_counts"):
        raise ValueError("Gallery metadata status counts differ from its rows")
    expected_final_statuses = {
        "done": EXPECTED_GENERATED_ROWS,
        "pending": 0,
        "failed": 0,
        "prompt_only": EXPECTED_DISPLAY_ROWS - EXPECTED_GENERATED_ROWS,
    }
    if final and statuses != expected_final_statuses:
        raise ValueError(f"Final gallery requires 96 generated and 64 prompt-only rows: {statuses}")
    encoded = json.dumps(data, ensure_ascii=False).casefold()
    if any(marker in encoded for marker in SENSITIVE_MARKERS):
        raise ValueError("Gallery data contains presigned credential material")
    return {
        "validated": True,
        "mode": "final" if final else "progressive",
        "row_count": len(rows),
        "bank_count": len(bank_counts),
        "prompts_per_bank": sorted(set(bank_counts.values())),
        "status_counts": statuses,
        "corrected_input_count": len(corrected_hashes),
        "source_bank_count": len(sources),
        "generated_image_count": len(generated_paths),
        "download_count": len(downloads),
        "all_corrected_input_hashes_verified": True,
        "all_generated_image_hashes_verified": True,
        "sensitive_material_absent": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate(args.run_dir.resolve(), args.final), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
