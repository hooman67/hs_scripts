#!/usr/bin/env python3
"""Validate the progressive/final V5 generation gallery without a browser."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from build_gallery import DEFAULT_RUN_DIR, EXPECTED_ROWS, SENSITIVE_MARKERS, assert_sanitized, sha256_path


def read_data(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    prefix = "const GENERATION_DATA = "
    if not raw.startswith(prefix) or not raw.endswith(";\n"):
        raise ValueError("Gallery data.js envelope differs")
    return json.loads(raw[len(prefix) : -2])


def validate(run_dir: Path, final: bool = False) -> dict[str, Any]:
    gallery = run_dir / "gallery"
    required = {"index.html", "main.js", "style.css", "imsauth.js", "data.js"}
    if not all((gallery / name).is_file() for name in required):
        raise FileNotFoundError("Gallery is missing a required file")
    index = (gallery / "index.html").read_text(encoding="utf-8")
    main = (gallery / "main.js").read_text(encoding="utf-8")
    for value in ("selectionFilter", "Prompt + scores", "Corrected input image", "Output image", "Rewritten prompt", "Full debug / request"):
        if value not in index and value not in main:
            raise ValueError(f"Gallery UI lacks required element: {value}")
    if not re.search(r'<thead><tr>.*?</tr></thead>', index, flags=re.DOTALL):
        raise ValueError("Column headers are not inside the table head")
    data = read_data(gallery / "data.js")
    assert_sanitized(data)
    rows = data.get("rows") or []
    if len(rows) != EXPECTED_ROWS:
        raise ValueError(f"Gallery must contain {EXPECTED_ROWS} rows")
    if len({row["row_id"] for row in rows}) != EXPECTED_ROWS:
        raise ValueError("Gallery row IDs are not unique")
    if len({row["candidate_key"] for row in rows}) != EXPECTED_ROWS:
        raise ValueError("Gallery candidate keys are not unique across selections")
    selection_counts = {
        name: sum(row["selection_type"] == name for row in rows)
        for name in ("ctech", "smart_brief")
    }
    if selection_counts != {"ctech": 40, "smart_brief": 40}:
        raise ValueError(f"Selection counts differ: {selection_counts}")
    statuses = {"done": 0, "pending": 0, "failed": 0}
    for row in rows:
        statuses[row["status"]] += 1
        render = row["corrected_input"]
        corrected = run_dir / render["gallery_path"]
        if not corrected.is_file() or sha256_path(corrected) != render["sha256"]:
            raise ValueError(f"Corrected input missing or changed: {row['row_id']}")
        candidate = row["candidate"]
        for field in (
            "smart_brief_support_score",
            "combined_source_relevance_score",
            "ctech_similarity_score",
            "smart_brief_score_components",
            "source_messaging_score_components",
            "source_explanation",
            "ctech_explanation",
        ):
            if field not in candidate:
                raise ValueError(f"Candidate score metadata missing {field}: {row['row_id']}")
        if row["status"] == "done":
            record = row.get("record") or {}
            output = record.get("generated_image") or {}
            image = run_dir / output.get("gallery_path", "")
            if not image.is_file() or sha256_path(image) != output.get("sha256"):
                raise ValueError(f"Done output missing or changed: {row['row_id']}")
            if record.get("request_payload", {}).get("prompt") != candidate["text"]:
                raise ValueError(f"Done request prompt differs: {row['row_id']}")
            if "usedPrompt" not in record or "debugData" not in record:
                raise ValueError(f"Done record lacks rewrite/debug: {row['row_id']}")
    if statuses != data["metadata"]["status_counts"]:
        raise ValueError("Gallery metadata status counts differ from rows")
    if final and statuses != {"done": 80, "pending": 0, "failed": 0}:
        raise ValueError(f"Final gallery requires 80 done rows: {statuses}")
    encoded = json.dumps(data, ensure_ascii=False).casefold()
    if any(marker in encoded for marker in SENSITIVE_MARKERS):
        raise ValueError("Gallery contains presigned credential material")
    return {
        "validated": True,
        "mode": "final" if final else "progressive",
        "row_count": len(rows),
        "selection_counts": selection_counts,
        "status_counts": statuses,
        "corrected_input_count": len({row["render_id"] for row in rows}),
        "source_bank_count": len(data.get("sources") or {}),
        "selection_filter_present": True,
        "full_debug_request_present_for_done_rows": True,
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
