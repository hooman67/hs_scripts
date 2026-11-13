#!/usr/bin/env python3
"""Build the authorized V6 preview-generation manifest from frozen prompts and renders."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

from PIL import Image


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
HERE = Path(__file__).resolve().parent
PROMPTS = (
    HERE.parent
    / "revisions/v6-approved-20261029-final-r44/exports/final/prompts_top6_96.json"
)
RUN_DIR = (
    PROJECT
    / "local_data/generation_runs/hp_lifestyle_approved_props_v6_top6_four_devices_20261029_preview"
)
ASSET_ROOT = RUN_DIR / "assets/references"
BASE_URL = "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8000.or2.colligo.dev"
BUCKET = "foundry-hp-enterprise-adobe-assets"
FOUR_SKU_PREFIX = "weifengc/four_sku_40cam_studio05_20261028T1839Z"
MAGIC_PREFIX = (
    "training_logs/camera_printer_native_lighting_minus1EV_all_20261026/"
    "white_gallery_20261026T232039Z"
)


RENDERS = {
    ("cashmere", "Front_CloseUp"): ("cashmere_x/Front_CloseUp/product_white.png", "laptop_FrontCloseUp"),
    ("cashmere", "Back_Right_CloseUp"): ("cashmere_x/Back_Right_CloseUp/product_white.png", "laptop_BackRightCloseUp"),
    ("cashmere", "Front_Left_Medium"): ("cashmere_x/Front_Left_Medium/product_white.png", "laptop_FrontLeftMedium"),
    ("cashmere", "Front_Wide"): ("cashmere_x/Front_Wide/product_white.png", "laptop_FrontWide"),
    ("elitebook", "Front_CloseUp"): ("elitebook_13/Front_CloseUp/product_white.png", "laptop_FrontCloseUp"),
    ("elitebook", "Back_Right_CloseUp"): ("elitebook_13/Back_Right_CloseUp/product_white.png", "laptop_BackRightCloseUp"),
    ("elitebook", "Front_Left_Medium"): ("elitebook_13/Front_Left_Medium/product_white.png", "laptop_FrontLeftMedium"),
    ("elitebook", "Front_Wide"): ("elitebook_13/Front_Wide/product_white.png", "laptop_FrontWide"),
    ("tassel", "Front_CloseUp"): ("tassel/Front_CloseUp/product_white.png", "printer_FrontCloseUp"),
    ("tassel", "Front_Right_CloseUp"): ("tassel/Front_Right_CloseUp/product_white.png", "printer_FrontRightCloseUp"),
    ("tassel", "Front_Left_Medium"): ("tassel/Front_Left_Medium/product_white.png", "printer_FrontLeftMedium"),
    ("tassel", "Front_Wide"): ("tassel/Front_Wide/product_white.png", "printer_FrontWide"),
    ("magic", "Front_CloseUp"): ("01_Front_CloseUp_white.png", "printer_FrontCloseUp"),
    ("magic", "Front_Right_CloseUp"): ("34_Front-Right_CloseUp_white.png", "printer_FrontRightCloseUp"),
    ("magic", "Front_Left_Medium"): ("28_Front-Left_Medium_white.png", "printer_FrontLeftMedium"),
    ("magic", "Front_Wide"): ("15_Front_Wide_white.png", "printer_FrontWide"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict:
    prompt_document = json.loads(PROMPTS.read_text(encoding="utf-8"))
    prompts = prompt_document["prompts"]
    if len(prompts) != 96 or len({row["prompt_key"] for row in prompts}) != 96:
        raise ValueError("Frozen V6 prompt input must contain 96 unique rows")
    expected_pairs = {(row["device_id"], row["source_camera_name"]) for row in prompts}
    if expected_pairs != set(RENDERS):
        raise ValueError(f"Prompt/render inventory mismatch: {sorted(expected_pairs ^ set(RENDERS))}")

    render_rows = []
    for (device_id, camera_name), (suffix, camera_tag) in sorted(RENDERS.items()):
        is_magic = device_id == "magic"
        key = f"{MAGIC_PREFIX}/{suffix}" if is_magic else f"{FOUR_SKU_PREFIX}/{suffix}"
        local_path = ASSET_ROOT / device_id / f"{camera_name}.png"
        if not local_path.is_file():
            raise FileNotFoundError(local_path)
        with Image.open(local_path) as image:
            size = image.size
            fmt = image.format
        if size != (2368, 1776) or fmt != "PNG":
            raise ValueError(f"Unexpected render metadata for {local_path}: {size} {fmt}")
        device_type = "laptop" if device_id in {"cashmere", "elitebook"} else "printer"
        render_rows.append(
            {
                "render_id": f"{device_id}__{camera_name}",
                "device_id": device_id,
                "device_type": device_type,
                "camera_name": camera_name,
                "camera_tag": camera_tag,
                "role": camera_name,
                "path": str(local_path),
                "sha256": sha256(local_path),
                "bytes": local_path.stat().st_size,
                "width": size[0],
                "height": size[1],
                "format": fmt,
                "output_width": 2368,
                "output_height": 1776,
                "preserve_aspect_ratio": True,
                "source_s3_uri": f"s3://{BUCKET}/{key}",
                "source_gallery_url": (
                    "https://foundry-aws-corp.adobe.io/asset/"
                    f"{BUCKET}/{key}"
                ),
            }
        )

    runner = (
        PROJECT
        / "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/generation/run_generation.py"
    )
    manifest = {
        "version": "hp-lifestyle-v6-preview-generation-manifest-v1",
        "status": "authorized",
        "authorized_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "authorization": (
            "Hooman authorized generation of the frozen V6 96-prompt set with the "
            "same preview model/request used for V4.1 and V5 on 2026-10-30."
        ),
        "scope": {
            "image_generation_authorized": True,
            "expected_images": 96,
            "device_count": 4,
            "views_per_device": 4,
            "bank_count": 16,
            "prompts_per_bank": 6,
            "render_count": 16,
            "candidate_texts_unchanged": True,
        },
        "prompts": {
            "path": str(PROMPTS),
            "sha256": sha256(PROMPTS),
            "version": prompt_document["version"],
            "revision": prompt_document["revision"],
        },
        "runner_dependency": {
            "path": str(runner),
            "sha256": sha256(runner),
            "purpose": "Frozen V4.1 submit, poll, materialize and integrity engine.",
        },
        "model": {
            "base_url": BASE_URL,
            "model_id": "hp-image",
            "rewriter_model": "gemini-3.1-pro",
            "num_inference_steps": 50,
            "seed": 42,
            "n": 1,
            "width": 2368,
            "height": 1776,
            "enable_prompt_rewrite": True,
        },
        "renders": render_rows,
        "run_dir": str(RUN_DIR),
        "s3": {
            "bucket": BUCKET,
            "prefix": (
                "eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/"
                "generated_preview_v1"
            ),
        },
        "interpretation_limits": [
            "This run uses the preview image model/request frozen for V4.1 and V5, not the 8016 E2E pipeline.",
            "Every prompt is used unchanged from the accepted V6 top-six export.",
            "Each row is bound to one product-specific corrected 2368x1776 white-background render.",
        ],
    }
    (HERE / "image_generation_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
