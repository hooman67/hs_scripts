#!/usr/bin/env python3
"""Build the V4 calibration set from frozen C-Tech comments.

Labels are an explicit interpretation of the comments for the expanded V4
contract: natural placement plus restrained room-composition coherence.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
SOURCE = ROOT / "research/prompt_writer_v6_2/evidence/ctech_joined_evidence.json"
OUT = ROOT / "judge/placement/versions/v4_ctech_20261106/evidence/calibration_cases.json"


EXPECTED = {
    "elitebook__laptop_FrontLeftMedium__p1": ("pass", ["chair_alignment_warning"]),
    "tassel__printer_FrontWide__p1": ("fail", ["malformed_support_furniture", "misplaced_support_furniture"]),
    "cashmere__laptop_FrontLeftMedium__p1": ("pass", ["chair_alignment_warning"]),
    "tassel__printer_FrontCloseUp__p1": ("fail", ["misplaced_support_furniture"]),
    "elitebook__laptop_FrontCloseUp__p1": ("pass", ["user_position_unobservable"]),
    "tassel__printer_FrontRightCloseUp__p1": ("fail", ["conflicting_perspective", "misplaced_support_furniture"]),
    "magic__printer_FrontLeftMedium__p1": ("fail", ["missing_support_structure"]),
    "tassel__printer_FrontLeftMedium__p2": ("fail", ["excessive_wall_clearance"]),
    "elitebook__laptop_FrontLeftMedium__p2": ("fail", ["missing_support_structure"]),
    "elitebook__laptop_FrontWide__p2": ("pass", ["furniture_layout_minor"]),
    "tassel__printer_FrontCloseUp__p2": ("fail", ["furniture_axis_conflict", "random_floor_prop"]),
    "magic__printer_FrontRightCloseUp__p2": ("review", ["malformed_prop"]),
    "tassel__printer_FrontRightCloseUp__p2": ("fail", ["misplaced_support_furniture", "random_floor_prop"]),
    "elitebook__laptop_BackRightCloseUp__p3": ("pass", ["chair_alignment_minor"]),
    "elitebook__laptop_FrontLeftMedium__p3": ("pass", ["chair_alignment_minor"]),
    "cashmere__laptop_FrontCloseUp__p1": ("pass", ["wall_enrichment_optional"]),
    "cashmere__laptop_FrontCloseUp__p2": ("review", ["liquid_crowding"]),
    "cashmere__laptop_FrontCloseUp__p3": ("pass", []),
    "cashmere__laptop_FrontCloseUp__p4": ("pass", ["wall_art_crop_minor"]),
    "cashmere__laptop_FrontCloseUp__p5": ("pass", ["wall_art_crop_minor"]),
    "cashmere__laptop_FrontCloseUp__p6": ("pass", ["style_prop_relevance", "style_wall_unresolved"]),
    "cashmere__laptop_FrontCloseUp__p7": ("fail", ["misplaced_support_furniture"]),
    "cashmere__laptop_FrontCloseUp__p8": ("pass", []),
    "cashmere__laptop_FrontCloseUp__p9": ("pass", ["style_prop_relevance", "style_wall_unresolved"]),
    "cashmere__laptop_FrontCloseUp__p10": ("pass", ["style_wall_unresolved", "style_prop_relevance"]),
    "magic__printer_FrontWide__p1": ("pass", ["style_wall_unresolved"]),
    "magic__printer_FrontWide__p2": ("fail", ["product_prop_collision", "warped_furniture"]),
    "magic__printer_FrontWide__p3": ("fail", ["unrealistic_furniture"]),
    "magic__printer_FrontWide__p4": ("pass", ["style_wall_unresolved"]),
    "magic__printer_FrontWide__p5": ("pass", ["style_wall_unresolved"]),
    "magic__printer_FrontWide__p6": ("fail", ["malformed_support_furniture"]),
    "magic__printer_FrontWide__p7": ("pass", ["style_wall_unresolved"]),
    "magic__printer_FrontWide__p8": ("fail", ["warped_furniture"]),
    "magic__printer_FrontWide__p9": ("fail", ["isolated_staging", "incoherent_prop_selection"]),
    "magic__printer_FrontWide__p10": ("pass", ["style_wall_unresolved"]),
}


def main() -> None:
    source = json.loads(SOURCE.read_text())
    records = source["records"]
    found = {record["evalset_item_id"] for record in records}
    if found != set(EXPECTED):
        missing = sorted(found - set(EXPECTED))
        stale = sorted(set(EXPECTED) - found)
        raise RuntimeError(f"label mismatch: missing={missing}, stale={stale}")

    cases = []
    for record in records:
        verdict, issue_codes = EXPECTED[record["evalset_item_id"]]
        generated = next(
            image["url"]
            for image in record["images"]
            if image["label"].startswith("Generated scene")
        )
        twin = next(
            image["url"]
            for image in record["images"]
            if image["label"].startswith("Digital twin")
        )
        cases.append(
            {
                "id": record["evalset_item_id"],
                "generated_image": generated,
                "twin_image": twin,
                "product_type": record["product_type"],
                "scene_prompt": record["scene_prompt"],
                "image_stage": "scene_generation",
                "v3_verdict": record["v3_verdict"],
                "v3_score": record["v3_score"],
                "ctech_comment": record["ctech_comment"],
                "expected_v4_verdict": verdict,
                "expected_issue_concepts": issue_codes,
            }
        )

    payload = {
        "schema_version": 1,
        "source": str(SOURCE),
        "interpretation_note": (
            "Expected labels follow explicit C-Tech language. Optional wall-art "
            "or chair suggestions can remain pass; coherent but material style/" 
            "composition concerns are review; visible malformed or implausible "
            "furniture, support, or product arrangements are fail."
        ),
        "cases": cases,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
