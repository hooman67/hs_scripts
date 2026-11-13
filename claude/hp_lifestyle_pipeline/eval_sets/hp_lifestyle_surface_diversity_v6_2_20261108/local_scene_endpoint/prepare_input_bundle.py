#!/usr/bin/env python3
"""Materialize the 16 audited V6.1 digital-twin views for the local endpoint."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
RECORDS = (
    PROJECT
    / "eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103"
    / "generation_gpt_image2_scene_v1/run/records"
)
PRODUCTS = PROJECT / "judge/prop_detail_experiment/pr4403_full160_20261106/run/inputs"
OUTPUT = HERE / "input_bundle"

TWINS = {
    "cashmere_x": {
        "name": "Cashmere / EliteBook X",
        "device": "cashmere",
        "kind": "laptop",
        "lighting": "Approved original USDZ lighting",
        "cameras": ("Front_CloseUp", "Back_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
    },
    "elitebook_13": {
        "name": "EliteBook 13 / Cheddar",
        "device": "elitebook",
        "kind": "laptop",
        "lighting": "Studio White Soft Light 05; exposure 0; rotation 0",
        "cameras": ("Front_CloseUp", "Back_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
    },
    "tassel": {
        "name": "Tassel",
        "device": "tassel",
        "kind": "printer",
        "lighting": "Studio White Soft Light 05; exposure 0; rotation 0",
        "cameras": ("Front_CloseUp", "Front_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
    },
    "adf_printer": {
        "name": "ADF Printer",
        "device": "magic",
        "kind": "printer",
        "lighting": "Approved original USDZ lighting; native texture gain 0.5 (-1 EV)",
        "cameras": ("Front_CloseUp", "Front_Right_CloseUp", "Front_Left_Medium", "Front_Wide"),
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def compact_camera(camera_id: str) -> str:
    return camera_id.replace("_", "")


def main() -> None:
    images = OUTPUT / "twins"
    images.mkdir(parents=True, exist_ok=True)
    entries: list[dict] = []
    for twin_id, twin in TWINS.items():
        for camera_id in twin["cameras"]:
            row_slug = f"{twin['device']}__{twin['kind']}_{compact_camera(camera_id)}__p1"
            record_path = RECORDS / f"{row_slug}.json"
            product_path = PRODUCTS / row_slug / "product.png"
            if not record_path.is_file() or not product_path.is_file():
                raise FileNotFoundError(f"missing frozen source for {row_slug}")
            record = json.loads(record_path.read_text(encoding="utf-8"))
            debug = record["scene_debug"]
            if debug["originalPrompt"] != record["prompt"]:
                raise ValueError(f"control prompt mismatch for {row_slug}")
            if debug["size"] != "2368x1776":
                raise ValueError(f"control size mismatch for {row_slug}")
            with Image.open(product_path) as image:
                if image.size != (2368, 1776) or image.format != "PNG":
                    raise ValueError(f"invalid product render for {row_slug}: {image.size}, {image.format}")
            destination = images / f"{twin_id}__{camera_id}.png"
            shutil.copyfile(product_path, destination)
            if sha256(destination) != sha256(product_path):
                raise ValueError(f"copy hash mismatch for {row_slug}")
            entries.append(
                {
                    "digital_twin_id": twin_id,
                    "digital_twin_name": twin["name"],
                    "lighting": twin["lighting"],
                    "camera_id": camera_id,
                    "camera_path": debug["twinCamera"]["cameraPrim"],
                    "product_version": record["runtime"].get("productVersion"),
                    "product_path": destination.relative_to(OUTPUT).as_posix(),
                    "product_sha256": sha256(destination),
                    "product_bytes": destination.stat().st_size,
                    "camera": debug["twinCamera"],
                    "control_job_id": record["job_id"],
                    "control_record_path": str(record_path.resolve()),
                    "control_record_sha256": sha256(record_path),
                    "source_product_path": str(product_path.resolve()),
                }
            )
    if len(entries) != 16:
        raise ValueError(f"expected 16 fixed twin views, found {len(entries)}")
    manifest = {
        "schema_version": 1,
        "purpose": "fixed V6.1 product renders and digital-twin cameras for shape-aware V6.2 endpoint",
        "canvas": {"width": 2368, "height": 1776},
        "entries": entries,
    }
    data = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    (OUTPUT / "manifest.json").write_text(data, encoding="utf-8")
    print(f"materialized {len(entries)} fixed twin views")
    print(f"manifest_sha256={hashlib.sha256(data.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
