"""Strict semantic validation and deterministic scoring for placement judge V4.2."""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
ASSESSMENT_SCHEMA = json.loads((ROOT / "assessment_schema.json").read_text())
RESULT_SCHEMA = json.loads((ROOT / "result_schema.json").read_text())
Draft202012Validator.check_schema(ASSESSMENT_SCHEMA)
Draft202012Validator.check_schema(RESULT_SCHEMA)
ASSESSMENT_VALIDATOR = Draft202012Validator(ASSESSMENT_SCHEMA)
RESULT_VALIDATOR = Draft202012Validator(RESULT_SCHEMA)

RULES_VERSION = "placement-scoring-v4.2"
COMPONENT_WEIGHTS = {
    "support_scenario": 20, "access_usability": 30, "orientation_alignment": 20,
    "scale_perspective": 15, "contact_integration": 15,
}
COMPONENT_CHECKS = {
    "support_scenario": ("support_role", "room_use_zone", "device_surface_position", "props_use_relation"),
    "access_usability": ("operating_access", "user_position"),
    "orientation_alignment": ("device_support_axes", "furniture_room_axes"),
    "scale_perspective": ("product_scale", "support_anatomy", "shared_perspective"),
    "contact_integration": ("support_contact", "shadows_reflections"),
}
VISIBILITY = {"observed": 1.0, "partial": 0.5, "unobservable": 0.0}
CONFIDENCE = {"high": 1.0, "medium": 0.5, "low": 0.0}
ISSUE_OWNERS = {
    "support_role": {"inappropriate_support", "occupied_workstation"},
    "room_use_zone": {"misplaced_support_furniture", "incoherent_use_zone"},
    "device_surface_position": {"unmotivated_device_position"},
    "props_use_relation": {"incoherent_prop_arrangement"},
    "operating_access": {"blocked_operating_path", "excessive_reach"},
    "user_position": {"no_feasible_user_position", "chair_displacement"},
    "device_support_axes": {"device_support_axis_conflict"},
    "furniture_room_axes": {"furniture_layout_conflict"},
    "product_scale": {"implausible_scale"},
    "support_anatomy": {"missing_required_support", "malformed_support_furniture"},
    "shared_perspective": {"conflicting_perspective"},
    "support_contact": {"unsupported_product", "floating", "sinking_or_intersection"},
    "shadows_reflections": {"inconsistent_shadow", "inconsistent_reflection"},
}
TRIGGER_NAMES = (
    "support_role", "room_use_zone", "device_surface_position", "props_use_relation",
    "operating_access", "user_position", "device_support_axes", "furniture_room_axes",
    "product_scale", "support_load_path", "support_shape", "shared_perspective",
    "support_contact", "shadows_reflections",
)
INPUT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object",
    "additionalProperties": False,
    "required": ["generated_image", "twin_image", "product_type", "scene_prompt"],
    "properties": {
        "generated_image": {"type": "string", "minLength": 1},
        "twin_image": {"type": "string", "minLength": 1},
        "product_type": {"enum": ["laptop", "printer"]},
        "scene_prompt": {"type": "string"},
        "target_record_id": {"type": "string", "minLength": 1},
        "device": {"type": "string", "minLength": 1},
        "camera": {"type": "string", "minLength": 1},
        "prompt_rank": {"type": ["string", "integer"]},
    },
}
INPUT_VALIDATOR = Draft202012Validator(INPUT_SCHEMA)


class PlacementValidationError(ValueError):
    def __init__(self, errors: list[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(errors))


def _schema_errors(value: Any, validator: Draft202012Validator) -> list[str]:
    out = []
    for error in sorted(validator.iter_errors(value), key=lambda e: tuple(map(str, e.absolute_path))):
        path = "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in error.absolute_path)
        out.append(f"{path}: {error.message}")
    return out


def validate_runtime_input(value: Any) -> Mapping[str, Any]:
    errors = _schema_errors(value, INPUT_VALIDATOR)
    if errors:
        raise PlacementValidationError(errors)
    return value


def _fact_items(inventory: Mapping[str, Any]):
    direct = ["support_type", "room_location", "product_footprint", "functional_front", "surface_position",
              "visible_corners", "load_path", "operating_approach", "associated_chair_or_standing_position", "props_activity"]
    for name in direct:
        yield name, inventory[name]
    for name in ("longitudinal", "depth"):
        yield f"edge_families.{name}", inventory["edge_families"][name]
    for name in ("wall", "floor", "cabinets", "nearby_furniture"):
        yield f"room_relations.{name}", inventory["room_relations"][name]


def _positive_scene_region(regions: list[Mapping[str, Any]]) -> bool:
    return any(r["image"] == "generated_scene" and r["box"][2] > r["box"][0] and r["box"][3] > r["box"][1] for r in regions)


def validate_assessment(value: Any) -> Mapping[str, Any]:
    errors = _schema_errors(value, ASSESSMENT_VALIDATOR)
    if errors:
        raise PlacementValidationError(errors)
    if value["stage_status"] == "unable":
        if value["unable_reason"] is None or value["inventory"] is not None or value["triggers"] is not None or value["checks"] is not None or value["defect_candidates"]:
            errors.append("unable requires reason, null inventory/triggers/checks, and no candidates")
        if errors:
            raise PlacementValidationError(errors)
        return value
    if value["unable_reason"] is not None or value["inventory"] is None or value["triggers"] is None or value["checks"] is None:
        errors.append("assessed requires inventory, triggers, checks and unable_reason=null")
        raise PlacementValidationError(errors)
    if not value["defect_candidates"]:
        errors.append("assessed requires at least one tested candidate")

    inventory = value["inventory"]
    facts = dict(_fact_items(inventory))
    for name, fact in facts.items():
        prefix = f"$.inventory.{name}"
        if not fact["observation"].strip():
            errors.append(f"{prefix}.observation blank")
        if fact["visibility"] == "unobservable":
            if not fact["visibility_limit"].strip():
                errors.append(f"{prefix}.visibility_limit required")
        else:
            if not _positive_scene_region(fact["regions"]) and name != "functional_front":
                errors.append(f"{prefix} requires positive generated-scene region")
            if name == "functional_front" and not any(r["box"][2] > r["box"][0] and r["box"][3] > r["box"][1] for r in fact["regions"]):
                errors.append(f"{prefix} requires positive region")
            if fact["visibility"] == "partial" and not fact["visibility_limit"].strip():
                errors.append(f"{prefix}.visibility_limit required when partial")

    candidates = value["defect_candidates"]
    by_id: dict[str, Mapping[str, Any]] = {}
    for index, candidate in enumerate(candidates):
        prefix = f"$.defect_candidates[{index}]"
        cid = candidate["id"]
        if cid in by_id:
            errors.append(f"{prefix}.id duplicate: {cid}")
        by_id[cid] = candidate
        if candidate["issue_code"] not in ISSUE_OWNERS[candidate["owner_check"]]:
            errors.append(f"{prefix} illegal issue owner")
        retained = candidate["disposition"] == "retained"
        if retained:
            if candidate["severity"] is None or not candidate["consequence"].strip() or not _positive_scene_region(candidate["regions"]):
                errors.append(f"{prefix} retained candidate lacks severity/consequence/scene region")
            if candidate["severity"] == 1 and candidate["warning_level"] not in {"advisory", "review"}:
                errors.append(f"{prefix} severity 1 requires advisory/review")
            if candidate["severity"] and candidate["severity"] >= 2 and candidate["warning_level"] != "none":
                errors.append(f"{prefix} material severity requires warning none")
            if candidate["confidence"] == "high" and candidate["alternative_status"] != "excluded_by_visible_evidence":
                errors.append(f"{prefix} high confidence requires excluded alternative")
        elif candidate["severity"] is not None or candidate["warning_level"] != "none":
            errors.append(f"{prefix} rejected candidate requires null severity/warning none")
        if candidate["issue_code"] == "chair_displacement" and retained and candidate["severity"] != 1:
            errors.append(f"{prefix} chair_displacement must be severity 1")
        mst = candidate["missing_support_test"]
        if candidate["issue_code"] == "missing_required_support" and retained:
            if mst is None:
                errors.append(f"{prefix} retained missing support requires structural test")
            else:
                r = mst["exposed_required_region"]
                if r["image"] != "generated_scene" or r["box"][2] <= r["box"][0] or r["box"][3] <= r["box"][1]:
                    errors.append(f"{prefix} invalid exposed required region")
                if candidate["confidence"] == "high" and candidate["alternative_status"] != "excluded_by_visible_evidence":
                    errors.append(f"{prefix} hidden support alternative precludes high confidence")
        elif mst is not None:
            errors.append(f"{prefix} structural test only allowed for retained missing support")

    # Trigger-candidate reciprocal graph and answer invariants.
    retained_ids = {c["id"] for c in candidates if c["disposition"] == "retained"}
    for name in TRIGGER_NAMES:
        trigger = value["triggers"][name]
        ids = trigger["candidate_ids"]
        missing = [cid for cid in ids if cid not in by_id]
        if missing:
            errors.append(f"$.triggers.{name} dangling candidate IDs: {missing}")
            continue
        linked_retained = [cid for cid in ids if cid in retained_ids]
        if trigger["answer"] == "no" and len(linked_retained) != 1:
            errors.append(f"$.triggers.{name}: no requires exactly one retained candidate")
        if trigger["answer"] != "no" and linked_retained:
            errors.append(f"$.triggers.{name}: yes/unknown cannot link retained candidate")
        if trigger["answer"] == "unknown" and not trigger["visibility_limit"].strip():
            errors.append(f"$.triggers.{name}: unknown requires visibility limit")
        for cid in ids:
            if cid in by_id and name not in by_id[cid]["trigger_ids"]:
                errors.append(f"$.triggers.{name}<->{cid} not reciprocal")
    for cid, candidate in by_id.items():
        for trigger_name in candidate["trigger_ids"]:
            if cid not in value["triggers"][trigger_name]["candidate_ids"]:
                errors.append(f"$.defect_candidates.{cid}<->{trigger_name} not reciprocal")
        if candidate["disposition"] == "retained" and not any(value["triggers"][t]["answer"] == "no" for t in candidate["trigger_ids"]):
            errors.append(f"$.defect_candidates.{cid}: retained candidate lacks no trigger")

    # Prevent exact duplicate defect tuples.
    seen = set()
    for candidate in candidates:
        norm_relation = " ".join(candidate["physical_relation"].lower().split())
        regions = json.dumps(candidate["regions"], sort_keys=True, separators=(",", ":"))
        key = (norm_relation, regions, candidate["issue_code"])
        if key in seen:
            errors.append(f"duplicate physical candidate tuple: {candidate['id']}")
        seen.add(key)

    # Checks are a strict projection of retained candidates.
    check_membership: dict[str, int] = {cid: 0 for cid in retained_ids}
    for name, check in value["checks"].items():
        prefix = f"$.checks.{name}"
        ids = check["candidate_ids"]
        unknown = [cid for cid in ids if cid not in by_id]
        if unknown:
            errors.append(f"{prefix} dangling candidates: {unknown}")
            continue
        if any(by_id[cid]["disposition"] != "retained" or by_id[cid]["owner_check"] != name for cid in ids):
            errors.append(f"{prefix} contains rejected or wrong-owner candidate")
        for cid in ids:
            check_membership[cid] = check_membership.get(cid, 0) + 1
        expected_codes = sorted({by_id[cid]["issue_code"] for cid in ids})
        if sorted(check["issue_codes"]) != expected_codes:
            errors.append(f"{prefix}.issue_codes not projected from candidates")
        if check["visibility"] == "unobservable":
            if ids or check["severity"] is not None or check["confidence"] != "low" or check["warning_level"] != "none" or check["issue_codes"]:
                errors.append(f"{prefix} unobservable invariant violated")
            if not check["visibility_limit"].strip():
                errors.append(f"{prefix} unobservable requires visibility limit")
        else:
            if check["severity"] is None:
                errors.append(f"{prefix} assessable requires severity")
            if check["visibility"] == "partial" and not check["visibility_limit"].strip():
                errors.append(f"{prefix} partial requires visibility limit")
            if not ids:
                if check["severity"] != 0 or check["issue_codes"] or check["warning_level"] != "none":
                    errors.append(f"{prefix} candidate-free check must be severity 0")
            else:
                max_severity = max(by_id[cid]["severity"] for cid in ids)
                expected_conf = max((by_id[cid]["confidence"] for cid in ids if by_id[cid]["severity"] == max_severity), key=lambda x: CONFIDENCE[x])
                expected_warning = "none"
                if max_severity == 1:
                    expected_warning = "review" if any(by_id[cid]["warning_level"] == "review" for cid in ids) else "advisory"
                if check["severity"] != max_severity or check["confidence"] != expected_conf or check["warning_level"] != expected_warning:
                    errors.append(f"{prefix} aggregation inconsistent with candidates")
    if any(count != 1 for count in check_membership.values()):
        errors.append(f"retained candidate membership must be exactly once: {check_membership}")

    if inventory["support_and_room_landmarks_visible"]:
        for name in ("room_use_zone", "furniture_room_axes", "shared_perspective"):
            if value["checks"][name]["visibility"] == "unobservable":
                errors.append(f"$.checks.{name} cannot be unobservable with support+room landmarks")
    if any(facts[name]["visibility"] != "unobservable" for name in ("edge_families.longitudinal", "edge_families.depth", "visible_corners")):
        if value["checks"]["support_anatomy"]["visibility"] == "unobservable":
            errors.append("support_anatomy cannot be unobservable when edges/corners visible")
    if errors:
        raise PlacementValidationError(errors)
    return value


def _round_half_up(value: float) -> int:
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def aggregate_assessment(assessment: Any) -> dict[str, Any]:
    validate_assessment(assessment)
    if assessment["stage_status"] != "assessed":
        raise PlacementValidationError(["unable assessment has no score"])
    checks = assessment["checks"]
    retained = [c for c in assessment["defect_candidates"] if c["disposition"] == "retained"]
    confirmed = [c for c in retained if c["severity"] >= 2 and c["confidence"] == "high"]
    uncertain = [c for c in retained if c["severity"] >= 2 and c["confidence"] != "high"]
    review = [c for c in retained if c["severity"] == 1 and c["warning_level"] == "review"]
    advisories = [c for c in retained if c["severity"] == 1 and c["warning_level"] == "advisory"]
    components = {}
    total_weight = weighted_score = confidence_numerator = 0.0
    for component, names in COMPONENT_CHECKS.items():
        visibility_sum = sum(VISIBILITY[checks[n]["visibility"]] for n in names)
        coverage = visibility_sum / len(names)
        effective_weight = COMPONENT_WEIGHTS[component] * coverage
        severities = []
        for name in names:
            check = checks[name]
            vis = VISIBILITY[check["visibility"]]
            if vis:
                sev = check["severity"]
                severities.append(1 if sev >= 2 and check["confidence"] != "high" else sev)
                confidence_numerator += COMPONENT_WEIGHTS[component] * vis / len(names) * CONFIDENCE[check["confidence"]]
        component_score = 100 - 25 * max(severities) if severities else None
        if component_score is not None:
            weighted_score += effective_weight * component_score
            total_weight += effective_weight
        components[component] = {"coverage": round(coverage, 3), "score": component_score, "effective_weight": round(effective_weight, 3)}
    if total_weight == 0:
        raise PlacementValidationError(["no observable placement evidence"])
    cap = None
    if confirmed:
        cap = {2: 59, 3: 39, 4: 19}[max(c["severity"] for c in confirmed)]
    elif uncertain:
        cap = 79
    base = weighted_score / total_weight
    score = _round_half_up(min(base, cap) if cap is not None else base)
    coverage = total_weight / 100
    q = confidence_numerator / total_weight
    aggregate_confidence = "high" if coverage >= .85 and q >= .85 and not uncertain else "medium" if coverage >= .60 and q >= .60 else "low"
    verdict = "fail" if confirmed else "review" if (uncertain or review) else "pass"
    reasons = []
    if confirmed: reasons.append("confirmed_material_defect")
    if uncertain: reasons.append("uncertain_material_defect")
    if review: reasons.append("placement_review_warning")
    if advisories: reasons.append("placement_advisory")
    if assessment["general_artifact_warnings"]: reasons.append("general_artifact_warning")
    finding_rows = []
    for c in sorted(retained, key=lambda x: (list(ISSUE_OWNERS).index(x["owner_check"]), x["id"])):
        category = "confirmed_material_defect" if c in confirmed else "uncertain_material_defect" if c in uncertain else "placement_review_warning" if c in review else "placement_advisory"
        finding_rows.append({"category": category, "candidate_id": c["id"], "owner_check": c["owner_check"], "issue_code": c["issue_code"], "severity": c["severity"], "confidence": c["confidence"], "evidence": c["disposition_evidence"], "consequence": c["consequence"]})
    explanation_parts = [f"{verdict.capitalize()}: {r['issue_code']} — {r['evidence']} Consequence: {r['consequence']} Confidence: {r['confidence']}. Owned by {r['owner_check']}." for r in finding_rows]
    if not explanation_parts:
        explanation_parts.append("Pass: no visible placement defect was retained on observable evidence.")
    for name, trigger in assessment["triggers"].items():
        if trigger["answer"] == "unknown":
            explanation_parts.append(f"Not established: {name} — {trigger['visibility_limit']} This limits evidence but does not lower the verdict.")
    return {
        "rules_version": RULES_VERSION, "score": score, "score_label": "100 on observable evidence" if score == 100 else str(score),
        "verdict": verdict, "confidence": aggregate_confidence, "coverage": round(coverage, 3),
        "components": components, "verdict_reasons": reasons, "findings": finding_rows,
        "owned_issue_codes": sorted({c["issue_code"] for c in retained}),
        "explanation": " ".join(explanation_parts),
    }


def validate_result(value: Any) -> Mapping[str, Any]:
    errors = _schema_errors(value, RESULT_VALIDATOR)
    if errors:
        raise PlacementValidationError(errors)
    status = value["status"]
    if status == "ok":
        if value["assessment"] is None or value["derived"] is None or value["error"] is not None:
            errors.append("ok requires assessment+derived and no error")
        else:
            validate_assessment(value["assessment"])
    elif status == "unassessable":
        if value["assessment"] is None or value["assessment"].get("stage_status") != "unable" or value["derived"] is not None or value["error"] is not None:
            errors.append("unassessable requires unable assessment and no derived/error")
        else:
            validate_assessment(value["assessment"])
    elif value["derived"] is not None or value["error"] is None:
        errors.append("error requires derived=null and error")
    if errors:
        raise PlacementValidationError(errors)
    return value


def canonical_json_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
