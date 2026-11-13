#!/usr/bin/env python3
"""Build the Direct OpenAI wire schema; full constraints remain local."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
INVENTORY_REFS = [
    "support_type", "room_location", "product_footprint", "functional_front",
    "surface_position", "edge_families.longitudinal", "edge_families.depth",
    "visible_corners", "load_path", "room_relations.wall", "room_relations.floor",
    "room_relations.cabinets", "room_relations.nearby_furniture", "operating_approach",
    "associated_chair_or_standing_position", "props_activity",
]


def transform(value: Any) -> Any:
    if isinstance(value, dict):
        out = {}
        for key, child in value.items():
            if key in {"$schema", "$id", "title", "uniqueItems", "minLength", "pattern"}:
                continue
            # The same 16-value inventory-reference enum is expanded once per
            # trigger/check in the inline strict schema, breaching the API's
            # 1000-enum-value limit. The full local validator retains it.
            if key == "enum" and child == INVENTORY_REFS:
                continue
            out[key] = transform(child)
        return out
    if isinstance(value, list):
        return [transform(child) for child in value]
    return value


def enum_value_count(value: Any) -> int:
    if isinstance(value, dict):
        return (len(value.get("enum", [])) if isinstance(value.get("enum"), list) else 0) + sum(enum_value_count(v) for v in value.values())
    if isinstance(value, list):
        return sum(enum_value_count(v) for v in value)
    return 0


def main() -> None:
    full = json.loads((ROOT / "assessment_schema.json").read_text())
    wire = transform(full)
    count = enum_value_count(wire)
    if count >= 1000:
        raise RuntimeError(f"wire enum value count {count} still exceeds API limit")
    (ROOT / "wire_schema.json").write_text(json.dumps(wire, indent=2) + "\n")
    print(f"wire enum values: {count}")


if __name__ == "__main__":
    main()
