#!/usr/bin/env python3
"""Upgrade the V4 observation contract with mandatory evidence-first checks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "observation_schema.json"
CHECK_IDS = (
    "rigid_edges_corners",
    "thickness_joints",
    "support_load_paths",
    "room_depth_relations",
    "station_anchoring",
    "device_support_contact",
    "prop_interactions",
    "incidental_prop_geometry",
    "user_access",
)
COMPONENTS = (
    "support_scenario",
    "access_usability",
    "orientation_alignment",
    "scale_perspective",
    "contact_integration",
)


def build() -> dict:
    schema = json.loads(TARGET.read_text(encoding="utf-8"))
    required = schema["required"]
    for field in ("view_class", "context_visibility", "inspection_checks", "defect_inventory", "verification"):
        if field not in required:
            required.insert(required.index("components"), field)

    properties = schema["properties"]
    properties["view_class"] = {"type": "string", "enum": ["close", "medium", "wide"]}
    properties["context_visibility"] = {
        "type": "string",
        "enum": ["adequate", "partial", "minimal"],
    }
    properties["inspection_checks"] = {
        "type": "object",
        "additionalProperties": False,
        "required": list(CHECK_IDS),
        "properties": {check_id: {"$ref": "#/$defs/inspection_check"} for check_id in CHECK_IDS},
    }
    properties["defect_inventory"] = {
        "type": "array",
        "items": {"$ref": "#/$defs/finding"},
    }
    properties["verification"] = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "structural_contradictions_rechecked",
            "severity_zero_evidence_checked",
            "hidden_geometry_not_assumed",
            "creative_advisories_not_scored",
            "corrected_assignments",
            "notes",
        ],
        "properties": {
            "structural_contradictions_rechecked": {"type": "boolean", "const": True},
            "severity_zero_evidence_checked": {"type": "boolean", "const": True},
            "hidden_geometry_not_assumed": {"type": "boolean", "const": True},
            "creative_advisories_not_scored": {"type": "boolean", "const": True},
            "corrected_assignments": {"type": "array", "items": {"type": "string"}},
            "notes": {"type": "string"},
        },
    }

    schema["$defs"]["inspection_check"] = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "visibility",
            "result",
            "evidence",
            "limitation",
            "alternative",
            "alternative_status",
            "finding_ids",
        ],
        "properties": {
            "visibility": {"type": "string", "enum": ["adequate", "partial", "none"]},
            "result": {
                "type": "string",
                "enum": ["consistent", "contradiction", "ambiguous", "unobservable", "not_applicable"],
            },
            "evidence": {"type": "string", "minLength": 1},
            "limitation": {
                "type": "string",
                "enum": ["none", "crop", "occlusion", "resolution", "insufficient_context"],
            },
            "alternative": {
                "type": "string",
                "enum": ["perspective", "crop_occlusion", "pedestal", "cantilever", "other_visible_support", "none"],
            },
            "alternative_status": {
                "type": "string",
                "enum": ["supported", "possible_but_unverified", "contradicted", "not_applicable"],
            },
            "finding_ids": {"type": "array", "items": {"type": "string", "pattern": "^F[1-9][0-9]*$"}},
        },
    }
    schema["$defs"]["finding"] = {
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "defect_type", "image_region", "evidence", "basis", "primary_component", "severity_recommendation"],
        "properties": {
            "id": {"type": "string", "pattern": "^F[1-9][0-9]*$"},
            "defect_type": {"type": "string"},
            "image_region": {"type": "string"},
            "evidence": {"type": "string", "minLength": 1},
            "basis": {"type": "string", "enum": ["physical_geometry", "usability", "station_policy", "incidental_geometry"]},
            "primary_component": {"type": "string", "enum": list(COMPONENTS)},
            "severity_recommendation": {"type": "integer", "minimum": 1, "maximum": 3},
        },
    }

    for component in COMPONENTS:
        definition = schema["$defs"][component]
        for field in ("supporting_check_ids", "finding_ids"):
            if field not in definition["required"]:
                definition["required"].append(field)
        definition["properties"]["supporting_check_ids"] = {
            "type": "array",
            "items": {"type": "string", "enum": list(CHECK_IDS)},
        }
        definition["properties"]["finding_ids"] = {
            "type": "array",
            "items": {"type": "string", "pattern": "^F[1-9][0-9]*$"},
        }
    return schema


if __name__ == "__main__":
    TARGET.write_text(json.dumps(build(), indent=2) + "\n", encoding="utf-8")
