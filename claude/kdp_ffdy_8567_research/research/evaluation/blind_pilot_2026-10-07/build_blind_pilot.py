#!/usr/bin/env python3
"""Build normalized opaque candidates, a private truth map, and fe-html parquet input."""

from __future__ import annotations

import csv
import hashlib
import json
import random
from pathlib import Path

import pandas as pd
from PIL import Image, ImageOps

PROJECT = Path("/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research")
ROOT = PROJECT / "research/evaluation/blind_pilot_2026-10-07"
ASSETS = ROOT / "staging/assets"
PRIVATE = ROOT / "private"
PARQUET = ROOT / "report_input.parquet"
SEED = 856720261007
BUCKET = "foundry-kdp-enterprise-adobe-assets"
S3_ROOT = "scraped_from_kdp_website/kdp_poc/blind_real_vs_generated_pilot_2026-10-07"
ASSET_S3 = f"s3://{BUCKET}/{S3_ROOT}/assets"


def local(path: str) -> Path:
    return PROJECT / path


REFS = {
    "k_express_black": [
        "s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/3_pairs/K-Express-Single-Serve-Coffee-Maker__Black/ref__K-Express-Single-Serve-Coffee-Maker_5000358267.jpg",
        "s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/3_pairs/K-Express-Single-Serve-Coffee-Maker__Black/ref__K-Express-Single-Serve-Coffee-Maker_en_general.jpg",
    ],
    "mini_mate_warm_stone": [
        "s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/3_pairs/Keurig-Mini-Mate-Plus__Warm_Stone/ref__Keurig-Mini-Mate-Plus_5000390177.jpg",
    ],
    "mini_mate_matte_black": [
        "s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/3_pairs/Keurig-Mini-Mate-Plus__Matte_Black/ref__Keurig-Mini-Mate-Plus_en_general.jpg",
    ],
    "k_supreme_gen2_black": [
        "s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/focus_skus/02_K-Supreme-Gen2_Black_5000393168/reference/00_Keurig-K-Supreme-Gen2_5000393168.jpg",
        "s3://foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/focus_skus/02_K-Supreme-Gen2_Black_5000393168/reference/01_Keurig-K-Supreme-Gen2_5000393168_alt1.jpg",
    ],
}


ITEMS = [
    # K-Express: two exact-SKU real lifestyles and two kitchen generations.
    {"truth": "real", "sku": "k_express_black", "scenario": "kitchen_carousel", "path": "research/dataset/data/pairs/K-Express-Single-Serve-Coffee-Maker__Black/life_H__K-Express_Alt_7.jpg", "overlap": False},
    {"truth": "real", "sku": "k_express_black", "scenario": "kitchen_wood_counter", "path": "research/dataset/data/pairs/K-Express-Single-Serve-Coffee-Maker__Black/life_H__K-Express_Alt_8.jpg", "overlap": False},
    {"truth": "generated", "sku": "k_express_black", "scenario": "kitchen_morning", "path": "research/generation/smoke_2026-10-07/outputs/k_express_lifestyle_sunburst_high_v1.png", "overlap": False},
    {"truth": "generated", "sku": "k_express_black", "scenario": "apartment_breakfast", "path": "research/generation/smoke_2026-10-07/outputs/k_express_window_breakfast_sunburst_high_v3.png", "overlap": False},

    # Warm Stone: one exact-SKU real and one human-interaction generation.
    {"truth": "real", "sku": "mini_mate_warm_stone", "scenario": "human_library", "path": "research/dataset/data/pairs/Keurig-Mini-Mate-Plus__Warm_Stone/life_H__3000x3000_warm_stone_library.jpg", "overlap": False},
    {"truth": "generated", "sku": "mini_mate_warm_stone", "scenario": "human_place_mug", "path": "research/generation/smoke_2026-10-07/outputs/mini_mate_warm_stone_human_place_mug_sunburst_high_v1.png", "overlap": False},

    # Matte Black: two exact-SKU styles and their text-only scene matches.
    {"truth": "real", "sku": "mini_mate_matte_black", "scenario": "lavender_studio", "path": "research/dataset/data/pairs/Keurig-Mini-Mate-Plus__Matte_Black/life_H__matteblack-afterhero.jpg", "overlap": True},
    {"truth": "real", "sku": "mini_mate_matte_black", "scenario": "yellow_blue_tabletop", "path": "research/dataset/data/pairs/Keurig-Mini-Mate-Plus__Matte_Black/life_H__matteblackpoolside.jpg", "overlap": True},
    {"truth": "generated", "sku": "mini_mate_matte_black", "scenario": "lavender_studio", "path": "research/generation/smoke_2026-10-07/outputs/mini_mate_matte_black_lavender_pop_studio_sunburst_high_v2.png", "overlap": True},
    {"truth": "generated", "sku": "mini_mate_matte_black", "scenario": "yellow_blue_tabletop", "path": "research/generation/smoke_2026-10-07/outputs/mini_mate_matte_black_yellow_blue_tabletop_sunburst_high_v3.png", "overlap": True},

    # K-Supreme: two product-present real studio scenes and two text-only scene matches.
    {"truth": "real", "sku": "k_supreme_gen2_black", "scenario": "red_pink_studio", "path": "research/dataset/data/focus_skus/02_K-Supreme-Gen2_Black_5000393168/lifestyle_studio/10_Hero_Silo_or_Lifestyle.jpg", "overlap": True},
    {"truth": "real", "sku": "k_supreme_gen2_black", "scenario": "coral_plinth", "path": "research/dataset/data/focus_skus/02_K-Supreme-Gen2_Black_5000393168/lifestyle_studio/13_Hero_Silo_or_Lifestyle_5.jpg", "overlap": True},
    {"truth": "generated", "sku": "k_supreme_gen2_black", "scenario": "red_pink_seamless", "path": "research/generation/smoke_2026-10-07/outputs/k_supreme_gen2_red_pink_seamless_sunburst_high_v2.png", "overlap": True},
    {"truth": "generated", "sku": "k_supreme_gen2_black", "scenario": "red_pink_editorial", "path": "research/generation/smoke_2026-10-07/outputs/k_supreme_gen2_red_pink_editorial_sunburst_high_v3.png", "overlap": True},
]


def normalize(src: Path, dest: Path) -> None:
    """Center-crop every candidate to the same square RGB PNG and strip metadata."""
    with Image.open(src) as im:
        normalized = ImageOps.fit(im.convert("RGB"), (1024, 1024), method=Image.Resampling.LANCZOS)
        normalized.save(dest, format="PNG", optimize=True)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    PRIVATE.mkdir(parents=True, exist_ok=True)
    rows = list(ITEMS)
    random.Random(SEED).shuffle(rows)
    public_rows = []
    truth_rows = []
    for order, row in enumerate(rows, start=1):
        src = local(row["path"])
        if not src.is_file():
            raise FileNotFoundError(src)
        token = hashlib.sha256(f"{SEED}:{order}:{src}".encode()).hexdigest()[:12]
        item_id = f"item_{token}"
        filename = f"candidate_{token}.png"
        dest = ASSETS / filename
        normalize(src, dest)
        refs = REFS[row["sku"]]
        public_rows.append({
            "Candidate": f"{ASSET_S3}/{filename}",
            "Reference 1": refs[0],
            "Reference 2": refs[1] if len(refs) > 1 else None,
            "item_id": item_id,
        })
        truth_rows.append({
            "display_order": order,
            "item_id": item_id,
            "opaque_filename": filename,
            "truth": row["truth"],
            "sku": row["sku"],
            "scenario": row["scenario"],
            "prompt_development_overlap": row["overlap"],
            "source_path": str(src),
            "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
        })

    pd.DataFrame(public_rows, columns=["Candidate", "Reference 1", "Reference 2", "item_id"]).to_parquet(PARQUET, index=False)
    truth_path = PRIVATE / "truth_map.csv"
    with truth_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(truth_rows[0]))
        writer.writeheader()
        writer.writerows(truth_rows)
    (PRIVATE / "build_metadata.json").write_text(json.dumps({
        "seed": SEED,
        "candidate_count": len(rows),
        "real_count": sum(r["truth"] == "real" for r in rows),
        "generated_count": sum(r["truth"] == "generated" for r in rows),
        "normalization": "RGB PNG; center crop; 1024x1024; Pillow LANCZOS; metadata stripped",
        "candidate_s3_prefix": ASSET_S3,
        "report_s3_prefix": f"s3://{BUCKET}/{S3_ROOT}/report",
    }, indent=2) + "\n")
    print(json.dumps({"rows": len(rows), "parquet": str(PARQUET), "truth_map": str(truth_path), "assets": str(ASSETS)}, indent=2))


if __name__ == "__main__":
    main()
