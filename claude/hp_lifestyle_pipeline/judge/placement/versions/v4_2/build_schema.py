#!/usr/bin/env python3
"""Build the strict V4.2 assessment and application envelope schemas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CHECKS = [
    "support_role", "room_use_zone", "device_surface_position", "props_use_relation",
    "operating_access", "user_position", "device_support_axes", "furniture_room_axes",
    "product_scale", "support_anatomy", "shared_perspective", "support_contact",
    "shadows_reflections",
]
TRIGGERS = [
    "support_role", "room_use_zone", "device_surface_position", "props_use_relation",
    "operating_access", "user_position", "device_support_axes", "furniture_room_axes",
    "product_scale", "support_load_path", "support_shape", "shared_perspective",
    "support_contact", "shadows_reflections",
]
INVENTORY_REFS = [
    "support_type", "room_location", "product_footprint", "functional_front",
    "surface_position", "edge_families.longitudinal", "edge_families.depth",
    "visible_corners", "load_path", "room_relations.wall", "room_relations.floor",
    "room_relations.cabinets", "room_relations.nearby_furniture", "operating_approach",
    "associated_chair_or_standing_position", "props_activity",
]
ISSUES = [
    "inappropriate_support", "occupied_workstation", "misplaced_support_furniture",
    "incoherent_use_zone", "unmotivated_device_position", "incoherent_prop_arrangement",
    "blocked_operating_path", "excessive_reach", "no_feasible_user_position",
    "chair_displacement", "device_support_axis_conflict", "furniture_layout_conflict",
    "implausible_scale", "missing_required_support", "malformed_support_furniture",
    "conflicting_perspective", "unsupported_product", "floating",
    "sinking_or_intersection", "inconsistent_shadow", "inconsistent_reflection",
]


def obj(properties, required=None):
    return {
        "type": "object", "additionalProperties": False,
        "required": list(properties) if required is None else required,
        "properties": properties,
    }


text = {"type": "string", "minLength": 1}
string = {"type": "string"}
visibility = {"type": "string", "enum": ["observed", "partial", "unobservable"]}
confidence = {"type": "string", "enum": ["low", "medium", "high"]}
warning = {"type": "string", "enum": ["none", "advisory", "review"]}
point = {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "number", "minimum": 0, "maximum": 1}}
region = obj({
    "image": {"type": "string", "enum": ["generated_scene", "original_twin"]},
    "label": text,
    "box": {"type": "array", "minItems": 4, "maxItems": 4, "items": {"type": "number", "minimum": 0, "maximum": 1}},
})
fact = obj({
    "visibility": visibility,
    "observation": text,
    "regions": {"type": "array", "minItems": 0, "maxItems": 8, "items": region},
    "visibility_limit": string,
})
inventory = obj({
    "scene_extent": {"type": "string", "enum": ["tight", "medium", "wide", "indeterminate"]},
    "support_and_room_landmarks_visible": {"type": "boolean"},
    "support_type": fact,
    "room_location": fact,
    "product_footprint": fact,
    "functional_front": fact,
    "surface_position": fact,
    "edge_families": obj({"longitudinal": fact, "depth": fact}),
    "visible_corners": fact,
    "load_path": fact,
    "room_relations": obj({"wall": fact, "floor": fact, "cabinets": fact, "nearby_furniture": fact}),
    "operating_approach": fact,
    "associated_chair_or_standing_position": fact,
    "props_activity": fact,
})
inventory_ref_array = {
    "type": "array", "minItems": 1, "maxItems": 16, "uniqueItems": True,
    "items": {"type": "string", "enum": INVENTORY_REFS},
}
candidate_id_array = {
    "type": "array", "minItems": 1, "maxItems": 8, "uniqueItems": True,
    "items": {"type": "string", "pattern": "^[a-z][a-z0-9_]{0,63}$"},
}
trigger = obj({
    "answer": {"type": "string", "enum": ["yes", "no", "unknown"]},
    "evidence": text,
    "inventory_refs": inventory_ref_array,
    "candidate_ids": candidate_id_array,
    "visibility_limit": string,
})
triggers = obj({name: trigger for name in TRIGGERS})
structural_test = obj({
    "exposed_required_region": region,
    "required_support_reason": text,
    "positive_break_or_unsupported_span_evidence": text,
    "observed_alternate_load_paths": text,
    "hidden_alternatives_and_limits": text,
})
candidate = obj({
    "id": {"type": "string", "pattern": "^[a-z][a-z0-9_]{0,63}$"},
    "physical_relation": text,
    "hypothesis": text,
    "regions": {"type": "array", "minItems": 0, "maxItems": 8, "items": region},
    "inventory_refs": inventory_ref_array,
    "trigger_ids": {"type": "array", "minItems": 1, "maxItems": 14, "uniqueItems": True, "items": {"type": "string", "enum": TRIGGERS}},
    "owner_check": {"type": "string", "enum": CHECKS},
    "issue_code": {"type": "string", "enum": ISSUES},
    "disposition": {"type": "string", "enum": ["retained", "rejected"]},
    "disposition_evidence": text,
    "benign_alternative": text,
    "alternative_status": {"type": "string", "enum": ["excluded_by_visible_evidence", "remains_substantial", "not_assessable"]},
    "severity": {"type": ["integer", "null"], "minimum": 1, "maximum": 4},
    "confidence": confidence,
    "warning_level": warning,
    "consequence": string,
    "missing_support_test": {"anyOf": [structural_test, {"type": "null"}]},
})
check = obj({
    "visibility": visibility,
    "severity": {"type": ["integer", "null"], "minimum": 0, "maximum": 4},
    "confidence": confidence,
    "warning_level": warning,
    "issue_codes": {"type": "array", "uniqueItems": True, "items": {"type": "string", "enum": ISSUES}},
    "evidence": text,
    "consequence": string,
    "alternative_explanation": string,
    "visibility_limit": string,
    "inventory_refs": inventory_ref_array,
    "candidate_ids": {"type": "array", "minItems": 0, "maxItems": 40, "uniqueItems": True, "items": {"type": "string", "pattern": "^[a-z][a-z0-9_]{0,63}$"}},
})
checks = obj({name: check for name in CHECKS})

assessment = obj({
    "inventory": {"anyOf": [inventory, {"type": "null"}]},
    "triggers": {"anyOf": [triggers, {"type": "null"}]},
    "defect_candidates": {"type": "array", "minItems": 0, "maxItems": 40, "items": candidate},
    "stage_status": {"type": "string", "enum": ["assessed", "unable"]},
    "unable_reason": {"type": ["string", "null"], "enum": [None, "unreadable_image", "target_not_identifiable", "product_type_conflict", "fundamentally_unjudgeable_product_support"]},
    "functional_front": string,
    "context_reading": string,
    "checks": {"anyOf": [checks, {"type": "null"}]},
    "general_artifact_warnings": {"type": "array", "items": obj({"code": {"type": "string", "const": "unrelated_rendering_artifact"}, "evidence": text})},
})
assessment.update({
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://foundry.adobe.com/schemas/hp-natural-placement-v4.2-assessment.json",
    "title": "HP Natural Placement V4.2 evidence-graph assessment",
})

audit_props = {
    "protocol_version": text,
    "model_requested": text,
    "model_returned": {"type": ["string", "null"]},
    "input_fingerprint": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "system_prompt_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "assessment_schema_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "wire_schema_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "scoring_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "crop_algorithm_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "anchor_catalog_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "target_record_id": {"type": ["string", "null"]},
    "selected_anchor_ids": {"type": "array", "minItems": 0, "maxItems": 4, "uniqueItems": True, "items": text},
    "crop_provenance_sha256": {"type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"},
}
result = obj({
    "schema_version": {"type": "string", "const": "hp-natural-placement-v4.2-result-v1"},
    "status": {"type": "string", "enum": ["ok", "error", "unassessable"]},
    "assessment": {"type": ["object", "null"]},
    "derived": {"type": ["object", "null"]},
    "error": {"anyOf": [{"type": "null"}, obj({
        "code": {"type": "string", "enum": ["invalid_input", "transport_failure", "invalid_model_output", "unassessable_input", "audit_failure"]},
        "message": text,
    })]},
    "raw_attempts": {"type": "array", "minItems": 1, "maxItems": 2, "items": obj({
        "attempt": {"type": "integer", "minimum": 1, "maximum": 2},
        "audit_id": text,
        "validation_status": {"type": "string", "enum": ["valid", "invalid", "transport_error"]},
    })},
    "audit": obj(audit_props),
})
result.update({"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://foundry.adobe.com/schemas/hp-natural-placement-v4.2-result.json"})

(ROOT / "assessment_schema.json").write_text(json.dumps(assessment, indent=2) + "\n", encoding="utf-8")
(ROOT / "result_schema.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print("wrote assessment_schema.json and result_schema.json")
