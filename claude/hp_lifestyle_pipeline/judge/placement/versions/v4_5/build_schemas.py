#!/usr/bin/env python3
"""Build strict local and compact wire schemas for both V4.5 observers."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from codebook import (
    ALL_TESTS,
    COHERENT_SUBTYPES,
    DEFECT_SUBTYPES,
    FUNCTIONAL_TESTS,
    GEOMETRY_TESTS,
)

ROOT = Path(__file__).resolve().parent

def obj(properties: dict[str, Any]) -> dict[str, Any]:
    return {"type": "object", "additionalProperties": False, "required": list(properties), "properties": properties}

text = {"type": "string", "minLength": 1, "maxLength": 360}
maybe_text = {"type": "string", "maxLength": 360}
box = {"type": "array", "minItems": 4, "maxItems": 4, "items": {"type": "number", "minimum": 0, "maximum": 1}}
region = obj({"label": text, "box": box})
maybe_region = {"anyOf": [{"$ref": "#/$defs/region"}, {"type": "null"}]}

ALL_SUBTYPES = sorted({"unresolved", *{s for v in DEFECT_SUBTYPES.values() for s in v}, *{s for v in COHERENT_SUBTYPES.values() for s in v}})

def relation_schema(test_ids: tuple[str, ...]) -> dict[str, Any]:
    return obj({
        "test_id": {"type": "string", "enum": list(test_ids)},
        "observability": {"type": "string", "enum": ["visible", "partial", "hidden"]},
        "state": {"type": "string", "enum": ["coherent", "defect", "unresolved"]},
        "subtype": {"type": "string", "enum": ALL_SUBTYPES},
        "direct_evidence": text,
        "counterevidence": maybe_text,
        "visibility_limit": text,
        "region": maybe_region,
    })

artifact = obj({"region": region, "evidence": text})
functional = obj({
    "stage_status": {"type": "string", "enum": ["assessed", "unable"]},
    "unable_reason": {"type": ["string", "null"], "enum": [None, "unreadable_image", "target_not_identifiable", "product_type_conflict", "fundamentally_unjudgeable_product_support"]},
    "product_front": {"anyOf": [obj({
        "state": {"type": "string", "enum": ["observed", "partial", "hidden"]},
        "region": maybe_region,
        "evidence": text,
    }), {"type": "null"}]},
    "visible_user_positions": {"anyOf": [{"type": "array", "maxItems": 12, "items": obj({
        "kind": {"type": "string", "enum": ["chair", "standing_zone"]}, "region": region,
    })}, {"type": "null"}]},
    "relations": {"anyOf": [{"type": "array", "minItems": len(FUNCTIONAL_TESTS), "maxItems": len(FUNCTIONAL_TESTS), "items": relation_schema(FUNCTIONAL_TESTS)}, {"type": "null"}]},
    "unrelated_artifacts": {"type": "array", "maxItems": 8, "items": artifact},
})
functional.update({"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://foundry.adobe.com/schemas/hp-placement-v4.5-functional.json", "title": "HP Placement V4.5 functional observer", "$defs": {"region": region}})

element = obj({"kind": {"type": "string", "enum": ["top", "leg", "panel", "pedestal", "rail", "bracket", "wall_attachment"]}, "region": region})
required_region = obj({"region": region, "connected_support_visible": {"type": ["boolean", "null"]}})
visible_break = obj({"region": region, "kind": {"type": "string", "enum": ["gap", "disconnection", "unsupported_span", "impossible_junction", "negative_space"]}})
edge = obj({
    "owner": {"type": "string", "enum": ["product_front", "product_depth", "support_front", "support_side", "wall", "floor", "cabinet", "neighboring_furniture"]},
    "p0": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "number", "minimum": 0, "maximum": 1}},
    "p1": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "number", "minimum": 0, "maximum": 1}},
    "raw_pixel_evidence": text,
})
inventory = obj({
    "visible_elements": {"type": "array", "maxItems": 24, "items": element},
    "exposed_required_regions": {"type": "array", "maxItems": 16, "items": required_region},
    "visible_breaks_or_negative_space": {"type": "array", "maxItems": 16, "items": visible_break},
})
geometry = obj({
    "stage_status": {"type": "string", "enum": ["assessed", "unable"]},
    "unable_reason": {"type": ["string", "null"], "enum": [None, "unreadable_image", "target_not_identifiable", "product_type_conflict", "fundamentally_unjudgeable_product_support"]},
    "support_inventory": {"anyOf": [inventory, {"type": "null"}]},
    "edge_observations": {"anyOf": [{"type": "array", "maxItems": 32, "items": edge}, {"type": "null"}]},
    "relations": {"anyOf": [{"type": "array", "minItems": len(GEOMETRY_TESTS), "maxItems": len(GEOMETRY_TESTS), "items": relation_schema(GEOMETRY_TESTS)}, {"type": "null"}]},
    "unrelated_artifacts": {"type": "array", "maxItems": 8, "items": artifact},
})
geometry.update({"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://foundry.adobe.com/schemas/hp-placement-v4.5-geometry.json", "title": "HP Placement V4.5 geometry observer", "$defs": {"region": region}})

def wire(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: wire(v) for k, v in value.items() if k not in {"$schema", "$id", "title", "uniqueItems", "pattern"}}
    if isinstance(value, list):
        return [wire(v) for v in value]
    return value

def main() -> None:
    for name, schema in (("functional_observer", functional), ("geometry_observer", geometry)):
        (ROOT / f"{name}_schema.json").write_text(json.dumps(schema, indent=2) + "\n")
        (ROOT / f"{name}_wire_schema.json").write_text(json.dumps(wire(schema), indent=2) + "\n")
    print(json.dumps({"functional_tests": len(FUNCTIONAL_TESTS), "geometry_tests": len(GEOMETRY_TESTS), "all_tests": len(ALL_TESTS)}))

if __name__ == "__main__":
    main()
