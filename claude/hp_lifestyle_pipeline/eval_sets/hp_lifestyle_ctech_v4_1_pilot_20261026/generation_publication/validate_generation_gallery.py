#!/usr/bin/env python3
"""Validate the isolated V4.1 generation gallery without network access."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RUN_DIR = PROJECT_ROOT / "local_data/generation_runs/hp_lifestyle_ctech_v4_1_pilot_20261026_corrected_twins_20261027"
SHARED_IMS = PROJECT_ROOT / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/imsauth.js"
STATIC_FILES = {"index.html", "main.js", "style.css", "imsauth.js", "data.js"}
DOWNLOAD_FILES = {"pilot_prompts.json", "system_prompt.md", "image_generation_manifest.json", "source_inputs.json"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_data(path: Path) -> dict[str, Any]:
    match = re.fullmatch(r"const GENERATION_DATA = (.*);\n?", path.read_text(encoding="utf-8"), re.S)
    if not match:
        raise ValueError(f"Unable to parse gallery data: {path}")
    return json.loads(match.group(1))


def validate(run_dir: Path, require_final: bool) -> dict[str, Any]:
    gallery = run_dir / "gallery"
    actual_static = {path.name for path in gallery.iterdir() if path.is_file()}
    if actual_static != STATIC_FILES:
        raise ValueError(f"Gallery top-level whitelist differs: {sorted(actual_static)}")
    actual_downloads = {path.name for path in (gallery / "downloads").iterdir() if path.is_file()}
    if actual_downloads != DOWNLOAD_FILES:
        raise ValueError(f"Gallery download whitelist differs: {sorted(actual_downloads)}")
    if (gallery / "imsauth.js").read_bytes() != SHARED_IMS.read_bytes():
        raise ValueError("IMS authentication script differs from the shared tested bytes")
    data = load_data(gallery / "data.js")
    meta, rows = data["metadata"], data["rows"]
    if len(rows) != 120 or meta.get("row_count") != 120:
        raise ValueError("Gallery must contain exactly 120 rows")
    if len(meta.get("environments") or []) != 6:
        raise ValueError("Gallery must expose the same six environment filters")
    if len(meta.get("downloads") or []) != len(DOWNLOAD_FILES):
        raise ValueError("Gallery metadata must link all four downloadable inputs")
    for item in meta["downloads"]:
        path = gallery / item["path"]
        if not path.is_file() or sha256(path) != item["sha256"]:
            raise ValueError(f"Download differs: {path}")
    row_ids: set[str] = set()
    status_counts = {"done": 0, "pending": 0, "failed": 0}
    for row in rows:
        row_id = row["row_id"]
        if row_id in row_ids:
            raise ValueError(f"Duplicate row: {row_id}")
        row_ids.add(row_id)
        status = row["status"]
        if status not in status_counts:
            raise ValueError(f"Invalid status for {row_id}: {status}")
        status_counts[status] += 1
        candidate = row.get("candidate") or {}
        if not candidate.get("text") or not candidate.get("environment"):
            raise ValueError(f"Incomplete prompt for {row_id}")
        source = row.get("source_input") or {}
        if "source_messaging" not in source or source.get("camera_tag") != row["camera_tag"]:
            raise ValueError(f"Incomplete source messaging/camera for {row_id}")
        corrected = row.get("corrected_input") or {}
        corrected_path = run_dir / corrected.get("gallery_path", "")
        if not corrected_path.is_file() or sha256(corrected_path) != corrected.get("sha256"):
            raise ValueError(f"Corrected input differs for {row_id}")
        record = row.get("record")
        if status == "done":
            if not record or "usedPrompt" not in record or "debugData" not in record or "request_payload" not in record:
                raise ValueError(f"Done record is incomplete for {row_id}")
            image = record.get("generated_image") or {}
            image_path = run_dir / image.get("gallery_path", "")
            if not image_path.is_file() or sha256(image_path) != image.get("sha256"):
                raise ValueError(f"Generated image differs for {row_id}")
        elif record and record.get("status") != status:
            raise ValueError(f"Projected and durable status differ for {row_id}")
    if status_counts != meta.get("status_counts"):
        raise ValueError(f"Metadata status counts differ: {meta.get('status_counts')} != {status_counts}")
    if require_final and status_counts != {"done": 120, "pending": 0, "failed": 0}:
        raise ValueError(f"Final validation requires 120 done rows: {status_counts}")
    html = (gallery / "index.html").read_text(encoding="utf-8")
    js = (gallery / "main.js").read_text(encoding="utf-8")
    for heading in ("Prompt", "Corrected input image", "Source messaging", "Explanation + C-Tech / provenance", "Output image", "Rewritten prompt", "Full debug / request"):
        if heading not in html:
            raise ValueError(f"Required gallery column absent: {heading}")
    for control in ("environmentFilter", "deviceFilter", "viewFilter", "statusFilter"):
        if control not in html or control not in js:
            raise ValueError(f"Required gallery control absent: {control}")
    return {
        "valid": True,
        "mode": "final" if require_final else "progressive",
        "row_count": len(rows),
        "status_counts": status_counts,
        "environment_count": len(meta["environments"]),
        "download_count": len(meta["downloads"]),
        "ims_auth_unchanged": True,
        "all_done_images_hash_verified": True,
        "all_corrected_input_hashes_verified": True,
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
