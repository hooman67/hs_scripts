#!/usr/bin/env python3
"""Build the four-case user-failure regression manifest from frozen V1 assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from datetime import datetime, timezone
from pathlib import Path


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
SOURCE = PROJECT / "judge/placement/data/assets.json"
OUTPUT = PROJECT / "judge/placement/versions/v2/data/regression_user_failures.json"
GATEWAY = "https://foundry-aws-corp.adobe.io/asset"

CASES = (
    {
        "id": "regression-userfail-row25-v14",
        "row": 25,
        "variant": "v14",
        "human_comment": "This one the edge of the printer is not aligned with edge of the tables.",
        "older_report_comment": "Product angle does not align with table angle.",
        "expected_issue_codes": ["furniture_axis_conflict"],
    },
    {
        "id": "regression-userfail-row12-v13",
        "row": 12,
        "variant": "v13",
        "human_comment": "Because a human would put this flush against the wall. And also not in the middle of the table it would be to a side. The placement is not natural.",
        "older_report_comment": "scene alignment should match product angle",
        "older_expected_issue_codes": ["furniture_axis_conflict"],
        "expected_issue_codes": ["unmotivated_position"],
    },
    {
        "id": "regression-userfail-row09-v14",
        "row": 9,
        "variant": "v14",
        "human_comment": "Laptop is at the centre of the desk. no one leaves their laptop there just like that. It would be closer to the chair to look like they are using the laptop. Also objects wouldn't get between the laptop and the chair (where a person would sit). Same with printers nothing can be in front of them (since people will be blocked from using them).",
        "older_report_comment": "Product needs to be closer to the table edge.",
        "expected_issue_codes": ["excessive_reach"],
    },
    {
        "id": "regression-userfail-row29-v13",
        "row": 29,
        "variant": "v13",
        "human_comment": "laptop should be closer to the chair. But I like the narrative here. In general our images should have a logical narrative explanining the things we see in the scene. This is what makes images natural / blievable. This is the composition we are looking for.",
        "older_report_comment": "v13 - product too far from the table edge closer to the chair.",
        "expected_issue_codes": ["excessive_reach"],
    },
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
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", header[16:24])


def public_url(s3_uri: str) -> str:
    if not s3_uri.startswith("s3://"):
        raise ValueError(f"not an S3 URI: {s3_uri}")
    return f"{GATEWAY}/{s3_uri[5:]}"


def image_payload(asset: dict, *, twin: bool) -> dict:
    path = Path(asset["local_path"])
    assert path.is_file()
    actual_hash = sha256(path)
    width, height = png_dimensions(path)
    assert actual_hash == asset["sha256"]
    assert path.stat().st_size == asset["bytes"]
    assert width == asset["width"]
    assert height == asset["height"]
    if twin:
        return {
            "render_id": asset["id"],
            "filename": path.name,
            "local_path": str(path),
            "sha256": actual_hash,
            "bytes": path.stat().st_size,
            "width": width,
            "height": height,
            "source_s3_uri": asset["s3_url"],
            "source_public_url": public_url(asset["s3_url"]),
            "preview_s3_uri": asset["s3_url"],
            "preview_public_url": public_url(asset["s3_url"]),
            "s3_etag": None,
            "s3_last_modified": None,
        }
    return {
        "filename": path.name,
        "local_path": str(path),
        "sha256": actual_hash,
        "bytes": path.stat().st_size,
        "width": width,
        "height": height,
        "s3_uri": asset["s3_url"],
        "public_url": public_url(asset["s3_url"]),
        "s3_etag": None,
        "s3_last_modified": None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.output.resolve() == OUTPUT.with_name("regression_user_failures_input_snapshot_v1.json").resolve():
        parser.error("The historical input snapshot must not be overwritten.")
    source_payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    by_id = {asset["id"]: asset for asset in source_payload["assets"]}
    records = []
    for case in CASES:
        row = case["row"]
        variant = case["variant"]
        generated_asset = by_id[f"comparison-row-{row:02d}-{variant}"]
        twin_asset = by_id[f"comparison-row-{row:02d}-product_input"]
        assert generated_asset["case_id"] == twin_asset["case_id"]
        assert generated_asset["original_prompt"] == twin_asset["original_prompt"]
        assert generated_asset["type"] == "generated_final"
        assert twin_asset["type"] == "product_input"

        generated = image_payload(generated_asset, twin=False)
        twin = image_payload(twin_asset, twin=True)
        prompt = generated_asset["original_prompt"]
        prompt_hash = text_sha256(prompt)
        device_type = generated_asset["device"].lower()
        assert device_type in {"laptop", "printer"}

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
                "candidate_id": variant,
                "scene_prompt": prompt,
                "scene_prompt_sha256": prompt_hash,
                "scene_prompt_source": {
                    "kind": "original_report_prompt",
                    "prompt_key": generated_asset["case_id"],
                    "source_revision": generated_asset["source_report"],
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
                    "twin_image": {"width": twin["width"], "height": twin["height"]},
                },
                "original_public_urls": {
                    "generated_image": generated["public_url"],
                    "twin_image": twin["source_public_url"],
                },
                "expected_verdict": "fail",
                "human_feedback": case["human_comment"],
                "human_feedback_source": "Hooman, current feedback message, 2026-11-04; verbatim excerpt",
                "older_report_comment": case["older_report_comment"],
                "older_expected_issue_codes": case.get("older_expected_issue_codes", case["expected_issue_codes"]),
                "expected_issue_codes": case["expected_issue_codes"],
                "regression_expectation": {
                    "human_verdict": "fail",
                    "human_comment": case["human_comment"],
                    "expected_issue_codes": case["expected_issue_codes"],
                    "passed_to_judge": False,
                },
            }
        )

    payload = {
        "schema_version": "hp-placement-v2-regression-assets-v1",
        "expected_count": len(records),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "annotation_metadata_correction": "Human feedback and expected issue codes reflect the latest user adjudication rather than the older report comment. Judge images and scene prompts unchanged. Original manifest preserved as regression_user_failures_input_snapshot_v1.json; completed historical run ledgers retain its hash.",
        "input_contract": {
            "image_stage": "scene_generation",
            "judge_inputs": [
                "generated_image",
                "twin_image",
                "device_type",
                "scene_prompt",
            ],
            "scene_prompt_policy": "Use the original report prompt; no rewritten prompt is included.",
            "annotation_policy": "Regression labels are evaluation metadata and are never passed to the judge.",
        },
        "source": {
            "verification_status": "VERIFIED",
            "source_manifest": str(SOURCE),
            "source_manifest_sha256": sha256(SOURCE),
            "source_report": "hp-v13-v14-laptop-printer30-20261103T015107Z-viewer",
        },
        "counts": {
            "records": len(records),
            "by_device_type": {
                device_type: sum(
                    record["device_type"] == device_type for record in records
                )
                for device_type in sorted({record["device_type"] for record in records})
            },
        },
        "validation": {
            "all_local_files_present": True,
            "all_local_sha256_match_source_records": True,
            "all_png_dimensions_match_source_records": True,
            "all_scene_prompts_match_source_records": True,
            "rewritten_prompt_fields_present_in_records": False,
            "annotations_passed_to_judge": False,
            "mismatches": [],
        },
        "records": records,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "records": len(records),
                "ids": [record["id"] for record in records],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
