#!/usr/bin/env python3
"""Export the four accepted V4.1 pilot banks into one immutable review corpus."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    accepted_path = HERE / "accepted_prompt_cases.json"
    manifest_path = HERE / "manifest.json"
    accepted = json.loads(accepted_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    accepted_status = "root_reviewed_after_bounded_model_correction_and_editorial_edits"
    if accepted["status"] != accepted_status:
        raise ValueError(f"unsupported accepted corpus status: {accepted['status']}")
    if accepted["counts"]["accepted_cases"] != 4 or accepted["counts"]["candidates"] != 120:
        raise ValueError("pilot must contain four validator-passing banks and 120 candidates")
    rows = []
    for case_id in manifest["authorized_text_case_ids"]:
        case = accepted["cases"][case_id]
        if case["status"] != accepted_status:
            raise ValueError(f"case is not root-reviewed: {case_id}")
        evidence_by_id = {item["id"]: item for item in case["debug"]["source_evidence"]}
        for candidate in case["candidates"]:
            candidate_provenance = candidate["candidate_provenance"]
            rows.append({
                "candidate_key": candidate["candidate_key"],
                "case_id": case_id,
                "source_id": case["source_id"],
                "device_type": case["device_type"],
                "camera_tag": case["camera_tag"],
                "view_role": case["view_role"],
                "rank": candidate["rank"],
                "rank_bin": candidate["rank_bin"],
                "environment": candidate["environment"],
                "subsetting": candidate["subsetting"],
                "text": candidate["text"],
                "ctech_reference_id": candidate["ctech_reference_id"],
                "ctech_reference_score": candidate["ctech_reference_score"],
                "ctech_relationship": candidate["ctech_relationship"],
                "ctech_changes": candidate["ctech_changes"],
                "ctech_explanation": candidate["ctech_explanation"],
                "source_relevance_score": candidate["source_relevance_score"],
                "source_relationship": candidate["relationship"],
                "source_explanation": candidate["explanation"],
                "evidence_ids": candidate["evidence_ids"],
                "source_evidence": [evidence_by_id[evidence_id]
                                    for evidence_id in candidate["evidence_ids"]],
                "visual_signature": candidate["visual_signature"],
                "camera_omissions": candidate["camera_omissions"],
                "editorially_scene_edited": candidate_provenance["editorially_scene_edited"],
                "editorial_edits": candidate_provenance["editorial_edits"],
                "raw_correction_candidate_id": candidate_provenance["raw_correction_candidate_id"],
                "raw_correction_text": candidate_provenance["raw_correction_text"],
                "repair_normalized_candidate_id": candidate_provenance["repair_normalized_candidate_id"],
                "repair_normalized_text": candidate_provenance["repair_normalized_text"],
                "reviewed_candidate_id": candidate_provenance["reviewed_candidate_id"],
                "first_draw_raw_record_path": case["record_path"],
                "first_draw_raw_record_sha256": case["record_sha256"],
                "correction_provider_response_path": case["correction_provider_response_path"],
                "correction_provider_response_sha256": case["correction_provider_response_sha256"],
            })
    if len(rows) != 120 or len({row["candidate_key"] for row in rows}) != 120:
        raise ValueError("expected 120 unique candidate keys")
    output = {
        "version": "hp-lifestyle-ctech-v4.1-reviewed-pilot-prompts-v1",
        "status": accepted_status,
        "prompt_count": len(rows),
        "review_disclosure": accepted["review_disclosure"],
        "counts": {
            "reviewed_candidates": 120,
            "editorially_scene_edited_candidates": 8,
            "unedited_scene_candidates": 112,
            "raw_model_success_claim": False,
        },
        "provenance": {
            "manifest_path": str(manifest_path),
            "manifest_sha256": sha256(manifest_path),
            "accepted_prompt_cases_path": str(accepted_path),
            "accepted_prompt_cases_sha256": sha256(accepted_path),
            "system_prompt": manifest["provenance"]["system_prompt"],
            "output_schema": manifest["provenance"]["output_schema"],
            "repair_accounting_path": accepted["provenance"]["repair_accounting_path"],
            "repair_accounting_sha256": accepted["provenance"]["repair_accounting_sha256"],
            "prose_patch_path": accepted["provenance"]["prose_patch_path"],
            "prose_patch_sha256": accepted["provenance"]["prose_patch_sha256"],
            "metadata_patch_path": accepted["provenance"]["metadata_patch_path"],
            "metadata_patch_sha256": accepted["provenance"]["metadata_patch_sha256"],
        },
        "prompts": rows,
    }
    path = HERE / "pilot_prompts.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(path), "sha256": sha256(path), "prompts": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
