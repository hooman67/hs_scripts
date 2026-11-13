#!/usr/bin/env python3
"""Freeze the 15 comment-derived development cases without leaking labels to runtime."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[3]
ANNOTATION = ROOT / "astra/evidence/reviewer_0.json"
SOURCE = ROOT.parent / "v3/data/new_v6_1_eval_20261105/manifest.json"
MANIFEST_OUT = ROOT / "data/development_15_manifest.json"
EXPECTATIONS_OUT = ROOT / "data/development_15_expectations.json"
EXPECTED_ANNOTATION_SHA = "d466958fc707f504f70ec0c7273a433dfc84826aa36a1cbb46a0df201b51a1f3"

VERDICTS = {
    "elitebook__laptop_FrontLeftMedium__p1": "review",
    "tassel__printer_FrontWide__p1": "fail",
    "cashmere__laptop_FrontLeftMedium__p1": "review",
    "tassel__printer_FrontCloseUp__p1": "fail",
    "elitebook__laptop_FrontCloseUp__p1": "review",
    "tassel__printer_FrontRightCloseUp__p1": None,
    "magic__printer_FrontLeftMedium__p1": "fail",
    "tassel__printer_FrontLeftMedium__p2": "fail",
    "elitebook__laptop_FrontLeftMedium__p2": "fail",
    "elitebook__laptop_FrontWide__p2": "pass",
    "tassel__printer_FrontCloseUp__p2": "fail",
    "magic__printer_FrontRightCloseUp__p2": "pass",
    "tassel__printer_FrontRightCloseUp__p2": "fail",
    "elitebook__laptop_BackRightCloseUp__p3": None,
    "elitebook__laptop_FrontLeftMedium__p3": "pass",
}

ISSUE_EXPECTATIONS = {
    "elitebook__laptop_FrontLeftMedium__p1": ["chair_displacement"],
    "tassel__printer_FrontWide__p1": ["malformed_support_furniture", "misplaced_support_furniture"],
    "cashmere__laptop_FrontLeftMedium__p1": ["chair_displacement"],
    "tassel__printer_FrontCloseUp__p1": ["misplaced_support_furniture"],
    "elitebook__laptop_FrontCloseUp__p1": [],
    "tassel__printer_FrontRightCloseUp__p1": ["conflicting_perspective"],
    "magic__printer_FrontLeftMedium__p1": ["missing_required_support"],
    "tassel__printer_FrontLeftMedium__p2": ["unmotivated_device_position"],
    "elitebook__laptop_FrontLeftMedium__p2": ["missing_required_support"],
    "elitebook__laptop_FrontWide__p2": ["furniture_layout_conflict"],
    "tassel__printer_FrontCloseUp__p2": ["device_support_axis_conflict", "incoherent_prop_arrangement"],
    "magic__printer_FrontRightCloseUp__p2": ["unrelated_rendering_artifact"],
    "tassel__printer_FrontRightCloseUp__p2": ["misplaced_support_furniture", "incoherent_prop_arrangement"],
    "elitebook__laptop_BackRightCloseUp__p3": [],
    "elitebook__laptop_FrontLeftMedium__p3": [],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    if sha256(ANNOTATION) != EXPECTED_ANNOTATION_SHA:
        raise RuntimeError("Annotation bytes changed")
    annotation = json.loads(ANNOTATION.read_text(encoding="utf-8"))
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    by_id = {record["id"]: record for record in source["records"]}
    runtime_records = []
    expectations = []
    for row in annotation["rows"]:
        record_id = row["evalset_item_id"]
        record = json.loads(json.dumps(by_id[record_id]))
        record["dataset_role"] = "development_target_feedback_withheld"
        record["label_provenance"] = {
            "human_annotations_included": False,
            "diagnostic_expectations_included": False,
            "passed_to_judge": False,
            "withheld_expectations_path": str(EXPECTATIONS_OUT),
        }
        runtime_records.append(record)
        expectations.append(
            {
                "record_id": record_id,
                "human_comment_exact": row["comment"],
                "explicit_verdict": VERDICTS[record_id],
                "verdict_labeled": VERDICTS[record_id] is not None,
                "expected_issue_any": ISSUE_EXPECTATIONS[record_id],
                "interpretation_note": (
                    "No absolute verdict inferred from comment."
                    if VERDICTS[record_id] is None
                    else "Verdict is explicit or directly resolved by the comment."
                ),
            }
        )
    atomic(
        MANIFEST_OUT,
        {
            "schema_version": "placement-v4-development-manifest-v1",
            "expected_count": len(runtime_records),
            "source_manifest": str(SOURCE),
            "source_manifest_sha256": sha256(SOURCE),
            "annotation_sha256_used_only_for_selection": EXPECTED_ANNOTATION_SHA,
            "labels_passed_to_judge": False,
            "records": runtime_records,
        },
    )
    atomic(
        EXPECTATIONS_OUT,
        {
            "schema_version": "placement-v4-development-expectations-v1",
            "annotation_path": str(ANNOTATION),
            "annotation_sha256": EXPECTED_ANNOTATION_SHA,
            "verdict_labeled_count": sum(item["verdict_labeled"] for item in expectations),
            "unlabeled_verdict_record_ids": [item["record_id"] for item in expectations if not item["verdict_labeled"]],
            "records": expectations,
        },
    )
    print(json.dumps({"manifest": str(MANIFEST_OUT), "expectations": str(EXPECTATIONS_OUT), "records": len(runtime_records)}))


if __name__ == "__main__":
    main()
