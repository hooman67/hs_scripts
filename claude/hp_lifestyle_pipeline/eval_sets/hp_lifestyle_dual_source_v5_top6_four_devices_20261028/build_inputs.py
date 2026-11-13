#!/usr/bin/env python3
"""Build 16 frozen V5 inputs for four named products and four camera views."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
V5_VERSION = ROOT / "research/source_messaging_v1_to_v6/versions/v5"
V5_PILOT = ROOT / "eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027"
sys.path.insert(0, str(V5_VERSION / "scripts"))

from camera_profile_resolver import load_registry, resolve_profile  # noqa: E402


FOUR_SKU_GALLERY = (
    "https://foundry-aws-corp.adobe.io/asset/"
    "foundry-hp-enterprise-adobe-assets/weifengc/"
    "four_sku_40cam_studio05_20261028T1839Z/viewer.html"
)
MAGIC_GALLERY = (
    "https://foundry-aws-corp.adobe.io/asset/"
    "foundry-hp-enterprise-adobe-assets/training_logs/"
    "camera_printer_native_lighting_minus1EV_all_20261026/"
    "white_gallery_20261026T232039Z/viewer.html"
)

DEVICES = (
    {
        "device_id": "cashmere",
        "display_name": "Cashmere",
        "device_type": "laptop",
        "source_pair": "cashmere",
        "render_gallery_url": FOUR_SKU_GALLERY,
    },
    {
        "device_id": "elitebook",
        "display_name": "EliteBook",
        "device_type": "laptop",
        "source_pair": "elitebook",
        "render_gallery_url": FOUR_SKU_GALLERY,
    },
    {
        "device_id": "tassel",
        "display_name": "Tassel",
        "device_type": "printer",
        "source_pair": "deskjet_2955",
        "render_gallery_url": FOUR_SKU_GALLERY,
    },
    {
        "device_id": "magic",
        "display_name": "Magic",
        "device_type": "printer",
        "source_pair": "laserjet",
        "render_gallery_url": MAGIC_GALLERY,
    },
)

VIEWS = {
    "laptop": (
        ("FrontCloseUp", "Front_CloseUp"),
        ("BackRightCloseUp", "Back_Right_CloseUp"),
        ("FrontLeftMedium", "Front_Left_Medium"),
        ("FrontWide", "Front_Wide"),
    ),
    "printer": (
        ("FrontCloseUp", "Front_CloseUp"),
        ("FrontRightCloseUp", "Front_Right_CloseUp"),
        ("FrontLeftMedium", "Front_Left_Medium"),
        ("FrontWide", "Front_Wide"),
    ),
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(payload, encoding="utf-8")
    temporary.replace(path)


def source_input(pair_id: str) -> tuple[Path, dict[str, str]]:
    path = V5_PILOT / "inputs" / f"{pair_id}__{'laptop' if pair_id in {'cashmere', 'elitebook'} else 'printer'}_FrontRightCloseUp.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if set(payload) != {"smart_brief", "source_messaging", "camera_tag"}:
        raise ValueError(f"unexpected frozen V5 input contract: {path}")
    return path, {
        "smart_brief": payload["smart_brief"],
        "source_messaging": payload["source_messaging"],
    }


def main() -> None:
    registry_path = V5_VERSION / "camera_profiles.json"
    registry = load_registry(registry_path)
    source_cache = {device["source_pair"]: source_input(device["source_pair"]) for device in DEVICES}
    cases: list[dict[str, Any]] = []

    for device in DEVICES:
        source_path, source = source_cache[device["source_pair"]]
        for camera_name, source_camera_name in VIEWS[device["device_type"]]:
            camera_tag = f"{device['device_type']}_{camera_name}"
            resolution = resolve_profile(registry, camera_tag)
            if resolution["resolution"] != "exact" or resolution["resolved_tag"] != camera_tag:
                raise ValueError(f"camera tag must resolve exactly: {camera_tag}")
            case_id = f"{device['device_id']}__{camera_tag}"
            payload = {
                "smart_brief": source["smart_brief"],
                "source_messaging": source["source_messaging"],
                "camera_tag": camera_tag,
            }
            input_path = HERE / "inputs" / f"{case_id}.json"
            write_json(input_path, payload)
            cases.append(
                {
                    "case_id": case_id,
                    "group_id": f"{device['device_id']}__{device['device_type']}",
                    "pair_id": device["source_pair"],
                    "device_id": device["device_id"],
                    "device_display_name": device["display_name"],
                    "device_type": device["device_type"],
                    "camera_tag": camera_tag,
                    "source_camera_name": source_camera_name,
                    "view_role": resolution["effective_profile"]["framing"],
                    "render_gallery_url": device["render_gallery_url"],
                    "render_lookup": {
                        "device_name": device["display_name"],
                        "camera_name": source_camera_name,
                    },
                    "source_pair": device["source_pair"],
                    "product_identity_conflict": device["source_pair"] == "cashmere",
                    "source_input_path": str(source_path),
                    "source_input_sha256": sha_file(source_path),
                    "input_path": str(input_path),
                    "input_sha256": sha_file(input_path),
                    "input_semantic_sha256": sha_bytes(canonical_bytes(payload)),
                    "expected_camera": {
                        "requested_tag": camera_tag,
                        "resolved_tag": resolution["resolved_tag"],
                        "device_type": resolution["device_type"],
                        "profile_version": resolution["profile_version"],
                        "resolution": resolution["resolution"],
                        **resolution["effective_profile"],
                    },
                    "human_review_status": "pending",
                    "launchable": False,
                }
            )

    provenance_paths = {
        "system_prompt": V5_VERSION / "system_prompt.md",
        "input_schema": V5_VERSION / "input.schema.json",
        "output_schema": V5_VERSION / "output.schema.json",
        "camera_profiles": registry_path,
        "reference_library": V5_VERSION / "reference_library.json",
    }
    manifest = {
        "version": "hp-lifestyle-dual-source-v5-top6-four-devices-v1",
        "as_of": "2026-10-28",
        "status": "authorized_for_gpt5_5_text_generation",
        "scope": {
            "device_count": 4,
            "views_per_device": 4,
            "case_count": 16,
            "candidates_per_case": 20,
            "selected_per_case": 6,
            "generated_candidate_count": 320,
            "selected_prompt_count": 96,
            "selection_rule": "first six candidates after V5 descending combined-source relevance and C-Tech tie-break ordering",
            "runtime_input_fields": ["smart_brief", "source_messaging", "camera_tag"],
            "image_generation_authorized": False,
        },
        "device_source_mapping": [
            {
                "device_id": item["device_id"],
                "device_display_name": item["display_name"],
                "device_type": item["device_type"],
                "source_pair": item["source_pair"],
                "render_gallery_url": item["render_gallery_url"],
            }
            for item in DEVICES
        ],
        "model": {
            "deployment": "gpt-5.5",
            "reasoning_effort": "medium",
            "max_completion_tokens": 24000,
            "temperature": None,
            "strict_output_schema": True,
            "max_concurrency": 2,
            "max_transport_attempts": 100,
            "semantic_attempts_per_case": 1,
        },
        "provenance": {
            name: {"path": str(path), "bytes": path.stat().st_size, "sha256": sha_file(path)}
            for name, path in provenance_paths.items()
        },
        "authorized_text_case_ids": [case["case_id"] for case in cases],
        "cases": cases,
    }
    write_json(HERE / "manifest.json", manifest)
    print(json.dumps({"cases": len(cases), "selected_prompts": len(cases) * 6}, indent=2))


if __name__ == "__main__":
    main()
