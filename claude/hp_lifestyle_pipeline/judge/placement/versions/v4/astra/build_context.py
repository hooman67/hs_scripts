#!/usr/bin/env python3
"""Join exact reviewer comments to the frozen V3 report evidence for Astra."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ANNOTATION = HERE / "evidence" / "reviewer_0.json"
REPORT = (
    ROOT
    / "judge/placement/versions/v3/fe_reports/"
    "v6_1_consensus_v2_20261105/combined/data.json"
)
SOURCE_MANIFEST = (
    ROOT
    / "judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json"
)
OUTPUT = HERE / "evidence" / "joined_feedback_context.json"
EXPECTED_ANNOTATION_SHA256 = (
    "d466958fc707f504f70ec0c7273a433dfc84826aa36a1cbb46a0df201b51a1f3"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_embedded(meta: dict, key: str):
    value = meta[key]
    if not isinstance(value, str):
        raise TypeError(f"{key} must be an embedded JSON string")
    return json.loads(value)


def main() -> None:
    annotation_sha = sha256(ANNOTATION)
    if annotation_sha != EXPECTED_ANNOTATION_SHA256:
        raise RuntimeError("The reviewer annotation bytes changed")

    annotation = load_json(ANNOTATION)
    if annotation.get("questions") != []:
        raise RuntimeError("Expected a comment-only review with no questions")
    comments = annotation.get("rows")
    if not isinstance(comments, list) or len(comments) != 15:
        raise RuntimeError("Expected exactly 15 reviewer comments")
    if any(not isinstance(row.get("comment"), str) or not row["comment"].strip() for row in comments):
        raise RuntimeError("Every selected reviewer row must contain a comment")

    report = load_json(REPORT)
    report_rows = {
        row["meta_data"]["evalset_item_id"]: row
        for row in report["rows"]
    }
    source = load_json(SOURCE_MANIFEST)
    source_rows = {row["id"]: row for row in source["records"]}

    joined = []
    for annotation_row in comments:
        row_id = annotation_row["evalset_item_id"]
        report_row = report_rows[row_id]
        source_row = source_rows[row_id]
        meta = report_row["meta_data"]["key_val_informations"]
        images = [item for item in report_row["images"] if item.get("asset_type") == "image"]
        generated = next(item for item in images if item["is_model_input_or_output"] == "model_output")
        twin = next(item for item in images if item["is_model_input_or_output"] == "model_input")
        joined.append(
            {
                "record_id": row_id,
                "annotation_record_exact": annotation_row,
                "input": {
                    "product_type": meta["Product type"],
                    "product": meta["Product"],
                    "camera": meta["Camera"],
                    "environment": meta["Environment"],
                    "scene_prompt": meta["Original scene prompt"],
                    "scene_prompt_sha256": source_row["scene_prompt_sha256"],
                    "generated_image_url": generated["image_src"],
                    "generated_image_sha256": source_row["generated_image"]["sha256"],
                    "twin_image_url": twin["image_src"],
                    "twin_image_sha256": source_row["twin_image"]["sha256"],
                    "image_stage": source_row["image_stage"],
                },
                "current_final": {
                    "predicted_verdict": meta["Judge v3 predicted verdict"],
                    "score": meta["Judge score"],
                    "confidence": meta["Judge confidence"],
                    "coverage": meta["Judge coverage"],
                    "evidence_summary": meta["Judge evidence summary"],
                    "assessment_origin": meta["Assessment origin"],
                },
                "stage_assessments": {
                    "baseline_v2": parse_embedded(meta, "Baseline V2 original assessment"),
                    "compact_v3": parse_embedded(meta, "Compact V3 original assessment"),
                    "application_merge_before_consensus": parse_embedded(
                        meta, "Application merged assessment before consensus decision"
                    ),
                    "consensus_final_decision": parse_embedded(
                        meta, "Consensus final decision"
                    ),
                },
            }
        )

    payload = {
        "schema_version": "hp-placement-astra-feedback-context-v1",
        "annotation_source": {
            "s3_uri": (
                "s3://foundry-hp-enterprise-adobe-assets/"
                "hp_natural_placement_judge_v3_v6_1_20261105/consensus_v2/"
                "combined/annotations/reviewer_0.json"
            ),
            "sha256": annotation_sha,
            "bytes": ANNOTATION.stat().st_size,
            "submitted_at": annotation["submitted_at"],
            "reviewer": annotation["reviewer"],
            "button_values_present": False,
            "interpretation": (
                "Comments are authoritative feedback. Missing rows and missing comments are not passes."
            ),
        },
        "source_hashes": {
            "report_data_sha256": sha256(REPORT),
            "source_manifest_sha256": sha256(SOURCE_MANIFEST),
        },
        "comment_count": len(joined),
        "records": joined,
    }
    encoded = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    temporary = OUTPUT.with_suffix(".tmp")
    temporary.write_text(encoded, encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"output": str(OUTPUT), "sha256": sha256(OUTPUT), "records": len(joined)}))


if __name__ == "__main__":
    main()
