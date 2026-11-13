#!/usr/bin/env python3
"""Freeze a small independent calibration catalog from the verified prior-V6 corpus."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "v4" / "validation_corpus" / "manifest.json"
OUT = ROOT / "anchors"
ASSETS = OUT / "assets"
SELECTED = [
    "cashmere__laptop_BackRightCloseUp__p5",
    "cashmere__laptop_FrontLeftMedium__p6",
    "elitebook__laptop_FrontLeftMedium__p5",
    "elitebook__laptop_FrontLeftMedium__p6",
    "magic__printer_FrontCloseUp__p5",
    "magic__printer_FrontWide__p2",
    "magic__printer_FrontCloseUp__p3",
    "tassel__printer_FrontLeftMedium__p6",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixel_sha(path: Path) -> str:
    with Image.open(path) as im:
        arr = ImageOps.exif_transpose(im).convert("RGB").tobytes()
    return hashlib.sha256(arr).hexdigest()


def make_image(source: Path, destination: Path, max_edge: int) -> None:
    with Image.open(source) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
        im.save(destination, "JPEG", quality=88, optimize=True)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    source_doc = json.loads(SOURCE.read_text())
    by_id = {r["id"]: r for r in source_doc["records"]}
    records = []
    for ordinal, record_id in enumerate(SELECTED, 1):
        row = by_id[record_id]
        scene_source = Path(row["assets"]["generated_scene"]["local_path"])
        twin_source = Path(row["assets"]["digital_twin_reference"]["local_path"])
        if not scene_source.is_file() or not twin_source.is_file():
            raise FileNotFoundError(record_id)
        stem = f"a{ordinal:02d}_{record_id}"
        scene_out, twin_out = ASSETS / f"{stem}_scene.jpg", ASSETS / f"{stem}_twin.jpg"
        make_image(scene_source, scene_out, 1536)
        make_image(twin_source, twin_out, 1024)
        h = row["human_evidence"]
        label = h["direct_label"] or {"label": "no human verdict", "qualifier": "issue-only calibration", "trigger_quote": None}
        records.append({
            "anchor_id": f"prior_v6::{record_id}::{row['assets']['generated_scene']['sha256'][:12]}",
            "source_record_id": record_id,
            "source_manifest_sha256": sha(SOURCE),
            "product_type": row["device_type"],
            "device": row["device"],
            "camera": row["camera"]["camera_tag"],
            "prompt_rank": row["candidate_id"],
            "scene_prompt": row["scene_prompt"],
            "prompt_sha256": hashlib.sha256(row["scene_prompt"].encode("utf-8")).hexdigest(),
            "comment_exact": h["comment_exact"],
            "human_label": label,
            "generated": {
                "source_path": str(scene_source), "byte_sha256": sha(scene_source), "pixel_sha256": pixel_sha(scene_source),
                "display_path": str(scene_out), "display_sha256": sha(scene_out),
            },
            "twin": {
                "source_path": str(twin_source), "byte_sha256": sha(twin_source), "pixel_sha256": pixel_sha(twin_source),
                "display_path": str(twin_out), "display_sha256": sha(twin_out),
            },
        })
    catalog = {
        "schema_version": "hp-placement-anchor-catalog-v4.2.1",
        "purpose": "Independent prior-V6 calibration; exact comments and qualified labels preserved.",
        "scope_notice": "Historical comments are calibration data, not universal rules. no human verdict means issue-only evidence.",
        "maximum_selected": 4,
        "records": records,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "anchor_catalog.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
    print(OUT / "anchor_catalog.json")


if __name__ == "__main__":
    main()
