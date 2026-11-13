#!/usr/bin/env python3
"""Build strict local and compact Direct OpenAI schemas for V4.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from codebook import SUBTYPE_ISSUES, TEST_ISSUES

ROOT = Path(__file__).resolve().parent

def obj(properties: dict[str, Any]) -> dict[str, Any]:
    return {"type": "object", "additionalProperties": False, "required": list(properties), "properties": properties}


text = {"type": "string", "minLength": 1, "maxLength": 360}
short_text = {"type": "string", "minLength": 1, "maxLength": 180}
string = {"type": "string", "maxLength": 360}
region = obj({
    "label": text,
    "box": {"type": "array", "minItems": 4, "maxItems": 4, "items": {"type": "number", "minimum": 0, "maximum": 1}},
})
inventory = obj({
    "scene_extent": {"type": "string", "enum": ["tight", "medium", "wide", "indeterminate"]},
    "product_front_and_footprint": text,
    "support_type_and_room_location": text,
    "support_topology_and_edges": text,
    "visible_load_path": text,
    "furniture_wall_floor_perspective": text,
    "operating_and_user_approach": text,
    "props_and_activity_zone": text,
    "contact_scale_shadows": text,
    "support_role_class": {"type": "string", "enum": ["compatible_support", "occupied_personal_workstation", "incompatible_support", "unresolved"]},
    "support_room_class": {"type": "string", "enum": ["coherent", "misplaced_furniture", "incoherent_use_zone", "unresolved"]},
    "operating_access_class": {"type": "string", "enum": ["open", "blocked", "excessive_reach", "unresolved"]},
    "user_position_class": {"type": "string", "enum": ["coherent", "chair_displacement", "no_feasible_user_position", "unresolved"]},
    "support_contact_class": {"type": "string", "enum": ["supported", "unsupported", "floating", "sinking_or_intersection", "unresolved"]},
    "light_transport_class": {"type": "string", "enum": ["coherent", "inconsistent_shadow", "inconsistent_reflection", "unresolved"]},
})


def test_schema() -> dict[str, Any]:
    return obj({
        "test_id": {"type": "string", "enum": list(TEST_ISSUES)},
        "defect": {"type": "string", "enum": ["yes", "no", "unknown"]},
        "severity": {"type": "integer", "minimum": 0, "maximum": 3},
        "visible_test": short_text,
        "direct_evidence": text,
        "counterevidence": string,
        "visibility_limit": string,
        "region": {"anyOf": [{"$ref": "#/$defs/region"}, {"type": "null"}]},
    })


artifact = obj({"code": {"type": "string", "const": "unrelated_rendering_artifact"}, "evidence": text})
scout = obj({
    "stage_status": {"type": "string", "enum": ["assessed", "unable"]},
    "unable_reason": {"type": ["string", "null"], "enum": [None, "unreadable_image", "target_not_identifiable", "product_type_conflict", "fundamentally_unjudgeable_product_support"]},
    "inventory": {"anyOf": [inventory, {"type": "null"}]},
    "tests": {"anyOf": [{"type": "array", "minItems": len(TEST_ISSUES), "maxItems": len(TEST_ISSUES), "items": test_schema()}, {"type": "null"}]},
    "general_artifact_warnings": {"type": "array", "maxItems": 8, "items": artifact},
})
scout.update({
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://foundry.adobe.com/schemas/hp-natural-placement-v4.4-scout.json",
    "title": "HP Natural Placement V4.4 defect scout",
    "$defs": {"region": region},
})

verifier_item = obj({
    "test_id": {"type": "string", "enum": list(TEST_ISSUES)},
    "decision": {"type": "string", "enum": ["confirmed", "rejected", "uncertain"]},
    "severity": {"type": "integer", "minimum": 0, "maximum": 3},
    "observability": {"type": "string", "enum": ["visible", "partial", "hidden"]},
    "observed_subtype": {"type": "string", "enum": ["not_applicable", *sorted({item for mapping in SUBTYPE_ISSUES.values() for item in mapping})]},
    "direct_evidence": text,
    "counterevidence": string,
    "visibility_limit": string,
    "region": {"anyOf": [{"$ref": "#/$defs/region"}, {"type": "null"}]},
})
verifier = obj({
    "stage_status": {"type": "string", "enum": ["verified", "unable"]},
    "unable_reason": {"type": ["string", "null"], "enum": [None, "unreadable_image", "target_not_identifiable", "product_type_conflict", "fundamentally_unjudgeable_product_support"]},
    "results": {"type": "array", "minItems": 0, "maxItems": len(TEST_ISSUES), "items": verifier_item},
})
verifier.update({
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://foundry.adobe.com/schemas/hp-natural-placement-v4.4-verifier.json",
    "title": "HP Natural Placement V4.4 material-defect verifier",
    "$defs": {"region": region},
})


def wire(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: wire(item) for key, item in value.items() if key not in {"$schema", "$id", "title", "uniqueItems", "pattern"}}
    if isinstance(value, list):
        return [wire(item) for item in value]
    return value


def main() -> None:
    for name, schema in (("scout", scout), ("verifier", verifier)):
        (ROOT / f"{name}_schema.json").write_text(json.dumps(schema, indent=2) + "\n")
        (ROOT / f"{name}_wire_schema.json").write_text(json.dumps(wire(schema), indent=2) + "\n")
    print("built", len(TEST_ISSUES), "defect tests")


if __name__ == "__main__":
    main()
