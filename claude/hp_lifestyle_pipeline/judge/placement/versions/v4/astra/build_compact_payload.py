#!/usr/bin/env python3
"""Build bounded Astra evidence while preserving all 15 comments verbatim."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "evidence" / "joined_feedback_context.json"
OUTPUT = HERE / "evidence" / "compact_feedback_context.json"

RELEVANT_COMPONENTS = {
    "elitebook__laptop_FrontLeftMedium__p1": ["access_usability", "orientation_alignment"],
    "tassel__printer_FrontWide__p1": ["support_scenario", "orientation_alignment", "scale_perspective"],
    "cashmere__laptop_FrontLeftMedium__p1": ["access_usability", "orientation_alignment"],
    "tassel__printer_FrontCloseUp__p1": ["support_scenario", "scale_perspective"],
    "elitebook__laptop_FrontCloseUp__p1": ["access_usability", "orientation_alignment"],
    "tassel__printer_FrontRightCloseUp__p1": ["support_scenario", "orientation_alignment", "scale_perspective"],
    "magic__printer_FrontLeftMedium__p1": ["support_scenario", "scale_perspective"],
    "tassel__printer_FrontLeftMedium__p2": ["support_scenario", "scale_perspective"],
    "elitebook__laptop_FrontLeftMedium__p2": ["access_usability", "orientation_alignment", "scale_perspective"],
    "elitebook__laptop_FrontWide__p2": ["support_scenario", "access_usability", "orientation_alignment"],
    "tassel__printer_FrontCloseUp__p2": ["support_scenario", "orientation_alignment", "scale_perspective"],
    "magic__printer_FrontRightCloseUp__p2": ["support_scenario", "scale_perspective"],
    "tassel__printer_FrontRightCloseUp__p2": ["support_scenario", "scale_perspective"],
    "elitebook__laptop_BackRightCloseUp__p3": ["access_usability", "orientation_alignment"],
    "elitebook__laptop_FrontLeftMedium__p3": ["access_usability", "orientation_alignment"],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage_excerpt(stage: dict, components: list[str]) -> dict:
    observation = stage["observation"]
    selected = {}
    for name in components:
        component = observation["components"][name]
        selected[name] = {
            "visibility": component["visibility"],
            "severity": component["severity"],
            "confidence": component["confidence"],
            "evidence": component["evidence"],
            "issue_codes": component["issue_codes"],
        }
    return {
        "verdict": stage["verdict"],
        "selected_component_evidence": selected,
    }


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    records = []
    for row in source["records"]:
        record_id = row["record_id"]
        components = RELEVANT_COMPONENTS[record_id]
        stages = row["stage_assessments"]
        records.append(
            {
                "record_id": record_id,
                "human_comment_exact": row["annotation_record_exact"]["comment"],
                "input": {
                    "product_type": row["input"]["product_type"],
                    "product": row["input"]["product"],
                    "camera": row["input"]["camera"],
                    "environment": row["input"]["environment"],
                    "scene_prompt": row["input"]["scene_prompt"],
                    "generated_image_sha256": row["input"]["generated_image_sha256"],
                    "twin_image_sha256": row["input"]["twin_image_sha256"],
                },
                "current_final": {
                    "predicted_verdict": row["current_final"]["predicted_verdict"],
                    "summary": row["current_final"]["evidence_summary"],
                },
                "relevant_components_selected_for_context": components,
                "baseline_v2_excerpt": stage_excerpt(stages["baseline_v2"], components),
                "compact_v3_excerpt": stage_excerpt(stages["compact_v3"], components),
            }
        )
    payload = {
        "schema_version": "hp-placement-astra-compact-feedback-context-v1",
        "source_joined_evidence_sha256": sha256(SOURCE),
        "interpretation": (
            "All 15 exact comments are development evidence. Unreviewed rows are not passes. "
            "Stage excerpts are fallible model evidence, not labels."
        ),
        "record_count": len(records),
        "records": records,
    }
    encoded = json.dumps(
        payload, ensure_ascii=False, separators=(",", ":")
    ) + "\n"
    if len(encoded.encode("utf-8")) >= 50_000:
        raise RuntimeError(
            f"Compact context exceeded the 50KB evidence target: {len(encoded.encode('utf-8'))} bytes"
        )
    temporary = OUTPUT.with_suffix(".tmp")
    temporary.write_text(encoded, encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"output": str(OUTPUT), "bytes": OUTPUT.stat().st_size, "sha256": sha256(OUTPUT)}))


if __name__ == "__main__":
    main()
