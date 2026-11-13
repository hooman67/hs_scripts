# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema"]
# ///
"""Build the bounded camera-aware GPT-5.5 text-evaluation inputs and manifest."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import jsonschema


V2_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(__file__).resolve().parents[3]
INPUT_DIR = V2_ROOT / "eval/inputs"
MANIFEST_PATH = V2_ROOT / "eval/manifest.json"
INPUT_SCHEMA_PATH = V2_ROOT / "input.schema.json"
CAMERA_PROFILES_PATH = V2_ROOT / "camera_profiles.json"
SOURCE_MANIFEST_PATH = SOURCE_ROOT / "data/source_manifest.json"
EDGE_MANIFEST_PATH = SOURCE_ROOT / "data/edge_manifest.json"
sys.path.insert(0, str(V2_ROOT))

from camera_profile_resolver import resolve_profile  # noqa: E402


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def bytes_sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_sources() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    source_manifest = json.loads(SOURCE_MANIFEST_PATH.read_text(encoding="utf-8"))
    edge_manifest = json.loads(EDGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    sources: dict[str, dict[str, Any]] = {}
    for kind, manifest in (("actual", source_manifest), ("synthetic", edge_manifest)):
        for semantic_sha256, entry in manifest["unique_inputs"].items():
            value = json.loads(Path(entry["input_path"]).read_text(encoding="utf-8"))
            sources[semantic_sha256[:16]] = {
                "kind": kind,
                "semantic_sha256": semantic_sha256,
                "entry": entry,
                "value": value,
            }
    return source_manifest, sources


def resolve_camera(
    registry: dict[str, Any], product_name: str, camera_tag: str
) -> dict[str, Any]:
    resolved = resolve_profile(registry, camera_tag, product_name)
    return {
        "requested_tag": resolved["requested_tag"],
        "resolved_tag": resolved["resolved_tag"],
        "profile_version": resolved["profile_version"],
        "resolution": resolved["resolution"],
        "framing": resolved["effective_profile"]["framing"],
        "elevation": resolved["effective_profile"]["elevation"],
        "requested_product": resolved["requested_product"],
        "resolved_product": resolved["resolved_product"],
        "product_resolution": resolved["product_resolution"],
    }


def case_specs() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "01_rich_printer_magic_back_closeup",
            "source_id": "ee810cf51bb82bb4",
            "product_name": "Magic",
            "camera_tag": "Printer_Back_CloseUp",
            "purpose": "Rich actual printer messaging under a tight level view.",
        },
        {
            "case_id": "02_rich_printer_messi_back_closeup",
            "source_id": "ee810cf51bb82bb4",
            "product_name": "Messi",
            "camera_tag": "Printer_Back_CloseUp",
            "purpose": "Same source and camera as case 01; exercise the Messi close-view override.",
        },
        {
            "case_id": "03_rich_printer_magic_front_right_medium",
            "source_id": "ee810cf51bb82bb4",
            "product_name": "Magic",
            "camera_tag": "Printer_Front_Right_Medium",
            "purpose": "Same rich source under a medium oblique view.",
        },
        {
            "case_id": "04_rich_printer_magic_front_right_wide",
            "source_id": "ee810cf51bb82bb4",
            "product_name": "Magic",
            "camera_tag": "Printer_Front_Right_Wide",
            "purpose": "Same rich source under a wide oblique view.",
        },
        {
            "case_id": "05_rich_printer_magic_top_front_closeup",
            "source_id": "ee810cf51bb82bb4",
            "product_name": "Magic",
            "camera_tag": "Printer_Top_Front_CloseUp",
            "purpose": "Same rich source under a tight top-oblique view.",
        },
        {
            "case_id": "06_actual_laptop_koki_front_closeup",
            "source_id": "22fdbf19f03d1a31",
            "product_name": "Koki",
            "camera_tag": "Laptop_Front_CloseUp",
            "purpose": "Actual mobile-work and meeting cues under a tight level view.",
        },
        {
            "case_id": "07_actual_laptop_koki_front_right_medium",
            "source_id": "22fdbf19f03d1a31",
            "product_name": "Koki",
            "camera_tag": "Laptop_Front_Right_Medium",
            "purpose": "Same actual laptop source under a medium oblique view.",
        },
        {
            "case_id": "08_actual_laptop_koki_front_right_wide",
            "source_id": "22fdbf19f03d1a31",
            "product_name": "Koki",
            "camera_tag": "Laptop_Front_Right_Wide",
            "purpose": "Same actual laptop source under a wide oblique view.",
        },
        {
            "case_id": "09_actual_laptop_koki_top_front_medium",
            "source_id": "22fdbf19f03d1a31",
            "product_name": "Koki",
            "camera_tag": "Laptop_Top_Front_Medium",
            "purpose": "Same actual laptop source under a medium top-oblique view.",
        },
        {
            "case_id": "10_actual_laptop_viktor_front_right_closeup",
            "source_id": "22fdbf19f03d1a31",
            "product_name": "Viktor",
            "camera_tag": "Laptop_Front_Right_CloseUp",
            "purpose": "Actual laptop source under the especially tight Viktor override.",
        },
        {
            "case_id": "11_actual_printer_tassel_front_closeup",
            "source_id": "160db92655412f4d",
            "product_name": "Tassel",
            "camera_tag": "Printer_Front_CloseUp",
            "purpose": "Second actual printer source with the PDF-only Tassel registry entry.",
        },
        {
            "case_id": "12_synthetic_gaming_cheddar_front_right_wide",
            "source_id": "048217039fd093b2",
            "product_name": "Cheddar",
            "camera_tag": "Laptop_Front_Right_Wide",
            "purpose": "Synthetic grounded Gaming cues under a known wide laptop view.",
        },
        {
            "case_id": "13_empty_source_unknown_camera",
            "source_id": "44136fa355b3678a",
            "product_name": "Magic",
            "camera_tag": "Printer_Unregistered_View",
            "purpose": "Empty source plus unknown camera must use the conservative minimal fallback.",
        },
        {
            "case_id": "14_technical_only_known_tight_camera",
            "source_id": "49aa979045b3b3d6",
            "product_name": "Koki",
            "camera_tag": "Laptop_Back_CloseUp",
            "purpose": "Technical-only source under a known tight camera must not invent a technical scene.",
        },
        {
            "case_id": "15_known_type_conflict_magic_laptop_camera",
            "source_id": "ee810cf51bb82bb4",
            "product_name": "Magic",
            "camera_tag": "Laptop_Back_CloseUp",
            "purpose": "Known printer product with a known laptop camera must resolve as incompatible.",
        },
        {
            "case_id": "16_unknown_product_known_printer_camera",
            "source_id": "ee810cf51bb82bb4",
            "product_name": "Unregistered_Product",
            "camera_tag": "Printer_Back_CloseUp",
            "purpose": "Unknown product with a known camera must use the conservative camera base.",
        },
        {
            "case_id": "17_actual_laptop_cashmere_front_right_medium",
            "source_id": "d60e13e4457fd44c",
            "product_name": "Cashmere",
            "camera_tag": "Laptop_Front_Right_Medium",
            "purpose": "Previously uncovered actual convertible-laptop source under a medium oblique view.",
        },
        {
            "case_id": "18_actual_laptop_cheddar_front_right_medium",
            "source_id": "fecec52a5c57c7bb",
            "product_name": "Cheddar",
            "camera_tag": "Laptop_Front_Right_Medium",
            "purpose": "Previously uncovered actual mobile-work laptop source under a medium oblique view.",
        },
        {
            "case_id": "19_actual_printer_magic_front_right_medium",
            "source_id": "8bbf8af1d8cbf4b2",
            "product_name": "Magic",
            "camera_tag": "Printer_Front_Right_Medium",
            "purpose": "Previously uncovered actual ink-tank printer source under a medium oblique view.",
        },
        {
            "case_id": "20_actual_printer_messi_front_right_medium",
            "source_id": "8189f3ad5af37a81",
            "product_name": "Messi",
            "camera_tag": "Printer_Front_Right_Medium",
            "purpose": "Previously uncovered actual shared-space printer source under a medium oblique view.",
        },
        {
            "case_id": "21_actual_printer_magic_enterprise_front_right_medium",
            "source_id": "324b14a617dfedba",
            "product_name": "Magic",
            "camera_tag": "Printer_Front_Right_Medium",
            "purpose": "Previously uncovered actual enterprise-printer source under a medium oblique view.",
        },
        {
            "case_id": "22_actual_printer_messi_ink_tank_front_right_medium",
            "source_id": "943faef0af11484f",
            "product_name": "Messi",
            "camera_tag": "Printer_Front_Right_Medium",
            "purpose": "Previously uncovered actual ink-tank all-in-one source under a medium oblique view.",
        },
    ]


def main() -> None:
    _, sources = load_sources()
    registry_bytes = CAMERA_PROFILES_PATH.read_bytes()
    registry = json.loads(registry_bytes)
    input_schema_bytes = INPUT_SCHEMA_PATH.read_bytes()
    input_schema = json.loads(input_schema_bytes)
    jsonschema.Draft202012Validator.check_schema(input_schema)
    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    cases = []
    expected_names = set()
    for spec in case_specs():
        source = sources[spec["source_id"]]
        request = {
            "source_messaging": source["value"],
            "product_name": spec["product_name"],
            "camera_tag": spec["camera_tag"],
        }
        jsonschema.validate(request, input_schema)
        target = INPUT_DIR / f"{spec['case_id']}.json"
        raw = (json.dumps(request, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        target.write_bytes(raw)
        expected_names.add(target.name)
        cases.append(
            {
                **spec,
                "input_path": f"inputs/{target.name}",
                "input_raw_sha256": bytes_sha256(raw),
                "input_semantic_sha256": canonical_sha256(request),
                "source_kind": source["kind"],
                "source_semantic_sha256": source["semantic_sha256"],
                "source_input_path": source["entry"]["input_path"],
                "source_origins": source["entry"]["origins"],
                "expected_camera": resolve_camera(
                    registry, spec["product_name"], spec["camera_tag"]
                ),
            }
        )

    unexpected = sorted(
        path.name for path in INPUT_DIR.glob("*.json") if path.name not in expected_names
    )
    if unexpected:
        raise RuntimeError(f"Refusing to leave unexpected eval inputs in place: {unexpected}")

    manifest = {
        "version": "camera-aware-v2-bounded-text-eval-2026-10-22",
        "case_count": len(cases),
        "model": "gpt-5.5",
        "settings": {
            "reasoning_effort": "medium",
            "max_completion_tokens": 8000,
            "temperature": "omitted",
            "strict_json_schema": True,
        },
        "image_generation": False,
        "input_schema_path": str(INPUT_SCHEMA_PATH),
        "input_schema_sha256": bytes_sha256(input_schema_bytes),
        "camera_profiles_path": str(CAMERA_PROFILES_PATH),
        "camera_profiles_sha256": bytes_sha256(registry_bytes),
        "source_manifest_path": str(SOURCE_MANIFEST_PATH),
        "edge_manifest_path": str(EDGE_MANIFEST_PATH),
        "laptop_source_selection": {
            "source_id": "22fdbf19f03d1a31",
            "rationale": "Actual source contains concrete mobile-work and meeting cues suitable for comparing tight, medium, wide, and top-oblique behavior.",
        },
        "cases": cases,
    }
    if manifest["case_count"] <= 0 or manifest["case_count"] != len(manifest["cases"]):
        raise RuntimeError("Bounded eval manifest must contain a positive, consistent case count")
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {len(cases)} inputs and {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
