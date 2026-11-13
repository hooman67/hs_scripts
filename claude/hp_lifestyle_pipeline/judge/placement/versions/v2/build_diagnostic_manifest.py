#!/usr/bin/env python3
"""Build three previously reviewed V14 cases for a small judge diagnostic."""

from __future__ import annotations

import hashlib
import json
import struct
from datetime import datetime, timezone
from pathlib import Path


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
ASSETS = PROJECT / "judge/placement/data/assets.json"
LABELS = PROJECT / "judge/placement/data/pilot_labels.json"
STAGE_PROVENANCE = PROJECT / "judge/placement/data/stage_provenance.json"
OUTPUT = (
    PROJECT
    / "judge/placement/versions/v2/data/diagnostic_reviewed_cases.json"
)
GATEWAY = "https://foundry-aws-corp.adobe.io/asset"
REPORT_ID = "hp-v13-v14-laptop-printer30-20261103T015107Z-viewer"

CASES = (
    {"row": 2, "id": "diagnostic-reviewed-row02-v14"},
    {"row": 8, "id": "diagnostic-reviewed-row08-v14"},
    {"row": 13, "id": "diagnostic-reviewed-row13-v14"},
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if (
        len(header) != 24
        or header[:8] != b"\x89PNG\r\n\x1a\n"
        or header[12:16] != b"IHDR"
    ):
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", header[16:24])


def public_url(s3_uri: str) -> str:
    if not s3_uri.startswith("s3://"):
        raise ValueError(f"not an S3 URI: {s3_uri}")
    return f"{GATEWAY}/{s3_uri[5:]}"


def image_payload(asset: dict, *, twin: bool) -> dict:
    path = Path(asset["local_path"])
    if not path.is_file():
        raise FileNotFoundError(path)
    actual_hash = sha256(path)
    width, height = png_dimensions(path)
    if actual_hash != asset["sha256"]:
        raise ValueError(f"hash mismatch: {asset['id']}")
    if path.stat().st_size != asset["bytes"]:
        raise ValueError(f"byte-size mismatch: {asset['id']}")
    if (width, height) != (asset["width"], asset["height"]):
        raise ValueError(f"dimension mismatch: {asset['id']}")
    common = {
        "filename": path.name,
        "local_path": str(path),
        "sha256": actual_hash,
        "bytes": path.stat().st_size,
        "width": width,
        "height": height,
        "s3_etag": None,
        "s3_last_modified": None,
    }
    if twin:
        return {
            "render_id": asset["id"],
            **common,
            "source_s3_uri": asset["s3_url"],
            "source_public_url": public_url(asset["s3_url"]),
            "preview_s3_uri": asset["s3_url"],
            "preview_public_url": public_url(asset["s3_url"]),
        }
    return {
        **common,
        "s3_uri": asset["s3_url"],
        "public_url": public_url(asset["s3_url"]),
    }


def main() -> None:
    asset_payload = json.loads(ASSETS.read_text(encoding="utf-8"))
    label_payload = json.loads(LABELS.read_text(encoding="utf-8"))
    stage_payload = json.loads(STAGE_PROVENANCE.read_text(encoding="utf-8"))
    by_asset_id = {asset["id"]: asset for asset in asset_payload["assets"]}
    by_row = {label["row"]: label for label in label_payload["labels"]}
    report = asset_payload["comparison_report"]
    v14_stage = stage_payload["conclusions"]["v14_final"]
    if report["report_id"] != REPORT_ID:
        raise ValueError("comparison report changed")
    if v14_stage["classification"] != "provisional_scene_generation_output":
        raise ValueError("V14 stage classification changed")

    records = []
    for case in CASES:
        row = case["row"]
        generated_asset = by_asset_id[f"comparison-row-{row:02d}-v14"]
        twin_asset = by_asset_id[f"comparison-row-{row:02d}-product_input"]
        label = by_row[row]
        if generated_asset["case_id"] != twin_asset["case_id"]:
            raise ValueError(f"row {row}: candidate/twin case mismatch")
        if generated_asset["original_prompt"] != twin_asset["original_prompt"]:
            raise ValueError(f"row {row}: candidate/twin prompt mismatch")
        if generated_asset["type"] != "generated_final":
            raise ValueError(f"row {row}: unexpected candidate type")
        if twin_asset["type"] != "product_input":
            raise ValueError(f"row {row}: unexpected twin type")
        if label["target_variant_labels"] != ["V14 final"]:
            raise ValueError(f"row {row}: label does not target V14 exactly")

        generated = image_payload(generated_asset, twin=False)
        twin = image_payload(twin_asset, twin=True)
        prompt = generated_asset["original_prompt"]
        prompt_hash = text_sha256(prompt)
        device_type = generated_asset["device"].lower()
        if device_type not in {"laptop", "printer"}:
            raise ValueError(f"row {row}: unsupported device type")

        records.append(
            {
                "id": case["id"],
                "source_case_id": generated_asset["case_id"],
                "source_asset_id": generated_asset["id"],
                "product": generated_asset["device"],
                "device": f"comparison-row-{row:02d}",
                "device_type": device_type,
                "view": {
                    "camera_tag": "unknown_legacy_report_view",
                    "source_camera_name": "unknown",
                    "view_role": "unknown",
                },
                "image_stage": "scene_generation",
                "stage_provenance": {
                    "classification": v14_stage["classification"],
                    "runtime_stage_value": "scene_generation",
                    "basis": v14_stage["basis"],
                    "reason_provisional": v14_stage["reason_provisional"],
                    "source_file": str(STAGE_PROVENANCE),
                    "source_file_sha256": sha256(STAGE_PROVENANCE),
                },
                "candidate_id": "v14",
                "scene_prompt": prompt,
                "scene_prompt_sha256": prompt_hash,
                "scene_prompt_source": {
                    "kind": "original_report_prompt",
                    "prompt_key": generated_asset["case_id"],
                    "source_revision": REPORT_ID,
                    "bank_rank": None,
                    "environment": None,
                    "rewritten_prompt_included": False,
                },
                "generated_image": generated,
                "twin_image": twin,
                "hashes": {
                    "generated_image_sha256": generated["sha256"],
                    "twin_image_sha256": twin["sha256"],
                    "scene_prompt_sha256": prompt_hash,
                },
                "dimensions": {
                    "generated_image": {
                        "width": generated["width"],
                        "height": generated["height"],
                    },
                    "twin_image": {
                        "width": twin["width"],
                        "height": twin["height"],
                    },
                },
                "original_public_urls": {
                    "generated_image": generated["public_url"],
                    "twin_image": twin["source_public_url"],
                },
                "evaluation_role": "reviewed_training_diagnostic_not_holdout",
                "holdout": False,
                "report_case_provenance": {
                    "report_id": REPORT_ID,
                    "report_s3_prefix": report["s3_prefix"],
                    "report_data_file": report["data_file"],
                    "reviewer": "zperkins",
                    "report_record": label["record"],
                    "source_row": row,
                    "source_case_id": generated_asset["case_id"],
                    "target_variant": "V14 final",
                    "target_basis": label["target_basis"],
                    "prior_dataset_split": label["split"],
                    "current_evaluation_role": "reviewed_training_diagnostic_not_holdout",
                    "source_asset_id": generated_asset["id"],
                    "source_twin_asset_id": twin_asset["id"],
                    "generated_s3_uri": generated_asset["s3_url"],
                    "twin_s3_uri": twin_asset["s3_url"],
                    "label_source_file": str(LABELS),
                    "label_source_file_sha256": sha256(LABELS),
                },
                "diagnostic_expectation": {
                    "exact_human_quote": label["exact_quote"],
                    "expected_issue_codes": label["expected_issue_codes"],
                    "acceptable_placement_dimensions": label[
                        "acceptable_components"
                    ],
                    "target_basis": label["target_basis"],
                    "mapping_notes": label["mapping_notes"],
                    "numeric_gold_score": None,
                    "numeric_gold_status": "not_defined",
                    "passed_to_judge": False,
                },
            }
        )

    payload = {
        "schema_version": "hp-placement-v2-reviewed-diagnostic-assets-v1",
        "expected_count": len(records),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "evaluation_role": "reviewed_training_diagnostic_not_holdout",
        "input_contract": {
            "image_stage": "scene_generation",
            "judge_inputs": [
                "generated_image",
                "twin_image",
                "device_type",
                "scene_prompt",
            ],
            "scene_prompt_policy": (
                "Use the original report prompt; no rewritten prompt is included."
            ),
            "expectation_policy": (
                "Exact reviewer quotes and interpreted issue dimensions are report-only "
                "diagnostic metadata, are not passed to the judge, and do not define "
                "a gold 0-100 score."
            ),
        },
        "source": {
            "verification_status": "VERIFIED_LOCAL_FROZEN_ASSETS",
            "assets_manifest": str(ASSETS),
            "assets_manifest_sha256": sha256(ASSETS),
            "labels_manifest": str(LABELS),
            "labels_manifest_sha256": sha256(LABELS),
            "stage_provenance": str(STAGE_PROVENANCE),
            "stage_provenance_sha256": sha256(STAGE_PROVENANCE),
            "source_report": REPORT_ID,
            "source_report_s3_prefix": report["s3_prefix"],
        },
        "counts": {
            "records": len(records),
            "by_device_type": {
                device_type: sum(
                    record["device_type"] == device_type for record in records
                )
                for device_type in sorted(
                    {record["device_type"] for record in records}
                )
            },
        },
        "validation": {
            "all_local_files_present": True,
            "all_local_sha256_match_source_records": True,
            "all_png_dimensions_match_source_records": True,
            "all_scene_prompts_match_source_records": True,
            "all_labels_target_v14_exactly": True,
            "all_cases_previously_reviewed": True,
            "all_cases_marked_not_holdout": True,
            "numeric_gold_scores_defined": False,
            "rewritten_prompt_fields_present_in_records": False,
            "diagnostic_expectations_passed_to_judge": False,
            "v14_stage_lineage_status": v14_stage["classification"],
            "mismatches": [],
        },
        "records": records,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "records": len(records),
                "ids": [record["id"] for record in records],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
