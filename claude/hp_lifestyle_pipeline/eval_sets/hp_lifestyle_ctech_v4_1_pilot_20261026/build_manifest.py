#!/usr/bin/env python3
"""Build the frozen four-bank V4.1 text-pilot manifest."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VERSION = ROOT / "research/source_messaging_v1_to_v6/versions/v4.1"
SCRIPTS = VERSION / "scripts"
sys.path.insert(0, str(SCRIPTS))

from camera_profile_resolver import load_registry, resolve_profile  # noqa: E402


CASES = (
    ("22fdbf19f03d1a31", "laptop", "FrontRightCloseUp", "close_up"),
    ("22fdbf19f03d1a31", "laptop", "FrontRightWide", "wide"),
    ("ee810cf51bb82bb4", "printer", "FrontRightCloseUp", "close_up"),
    ("ee810cf51bb82bb4", "printer", "FrontRightWide", "wide"),
)
REFERENCE_DOCX = ROOT / "input_output_hp_rewriter_10_03_26/example_prompts/HP - mAIstro Prompt Guidance (Oct 2026).docx"
REFERENCE_XLSX = ROOT / "input_output_hp_rewriter_10_03_26/example_prompts/Eval-Set_Lifestyle-Photography_wSKUs.xlsx"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}


def main() -> None:
    registry_path = VERSION / "camera_profiles.json"
    registry = load_registry(registry_path)
    cases = []
    for source_id, device_type, camera_name, view_role in CASES:
        tag = f"{device_type}_{camera_name}"
        case_id = f"{source_id}__{tag}"
        input_path = HERE / "inputs" / f"{case_id}.json"
        payload = json.loads(input_path.read_text(encoding="utf-8"))
        if set(payload) != {"source_messaging", "camera_tag"} or payload["camera_tag"] != tag:
            raise ValueError(f"invalid frozen input contract: {case_id}")
        resolution = resolve_profile(registry, tag)
        if resolution["resolution"] != "exact" or resolution["device_type"] != device_type:
            raise ValueError(f"unexpected camera resolution: {case_id}: {resolution}")
        cases.append({
            "case_id": case_id,
            "group_id": f"{source_id}__{device_type}_FrontRight",
            "source_id": source_id,
            "device_type": device_type,
            "view_role": view_role,
            "camera_tag": tag,
            "input_path": str(input_path),
            "input_sha256": sha256(input_path),
            "expected_camera": {
                "requested_tag": tag,
                "resolved_tag": resolution["resolved_tag"],
                "device_type": resolution["device_type"],
                "profile_version": resolution["profile_version"],
                "resolution": resolution["resolution"],
                **resolution["effective_profile"],
            },
        })

    manifest = {
        "version": "hp-lifestyle-ctech-v4.1-text-pilot-v1",
        "as_of": "2026-10-26",
        "status": "authorized_text_pilot_only",
        "scope": {
            "source_count": 2,
            "case_count": 4,
            "candidate_count": 120,
            "candidates_per_case": 30,
            "runtime_input_fields": ["source_messaging", "camera_tag"],
            "environments": ["Home", "Office", "Education", "Gaming", "Café", "Creative Studio"],
            "ranking": "descending_ctech_reference_score_then_source_relevance",
            "text_generation_authorized": True,
            "image_generation_authorized": False,
            "image_generation_gate": "Hooman must review and approve the V4.1 text distribution report first",
        },
        "model": {
            "deployment": "gpt-5.5",
            "reasoning_effort": "medium",
            "max_completion_tokens": 24000,
            "temperature": None,
            "strict_output_schema": True,
            "max_concurrency": 2,
            "max_transient_attempts": 100,
        },
        "provenance": {
            "system_prompt": record(VERSION / "system_prompt.md"),
            "input_schema": record(VERSION / "input.schema.json"),
            "output_schema": record(VERSION / "output.schema.json"),
            "camera_profiles": record(registry_path),
            "reference_library": record(VERSION / "reference_library.json"),
            "october_ctech_docx": record(REFERENCE_DOCX),
            "lifestyle_workbook": record(REFERENCE_XLSX),
            "parent_v4_system_prompt": record(ROOT / "research/source_messaging_v1_to_v6/versions/v4/system_prompt.md"),
        },
        "authorized_text_case_ids": [case["case_id"] for case in cases],
        "cases": cases,
    }
    path = HERE / "manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(path), "sha256": sha256(path), "cases": len(cases)}, indent=2))


if __name__ == "__main__":
    main()
