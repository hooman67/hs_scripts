"""Strict validation and deterministic scoring for anchored placement judge V4.1."""

from __future__ import annotations

import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent
ASSESSMENT_SCHEMA = json.loads((ROOT / "assessment_schema.json").read_text(encoding="utf-8"))
RESULT_SCHEMA = json.loads((ROOT / "result_schema.json").read_text(encoding="utf-8"))
Draft202012Validator.check_schema(ASSESSMENT_SCHEMA)
Draft202012Validator.check_schema(RESULT_SCHEMA)
ASSESSMENT_VALIDATOR = Draft202012Validator(ASSESSMENT_SCHEMA)
RESULT_VALIDATOR = Draft202012Validator(RESULT_SCHEMA)

RULES_VERSION = "placement-scoring-v4.1"
COMPONENT_WEIGHTS = {
    "support_scenario": 20,
    "access_usability": 30,
    "orientation_alignment": 20,
    "scale_perspective": 15,
    "contact_integration": 15,
}
COMPONENT_CHECKS = {
    "support_scenario": ("support_role", "room_use_zone", "device_surface_position", "props_use_relation"),
    "access_usability": ("operating_access", "user_position"),
    "orientation_alignment": ("device_support_axes", "furniture_room_axes"),
    "scale_perspective": ("product_scale", "support_anatomy", "shared_perspective"),
    "contact_integration": ("support_contact", "shadows_reflections"),
}
CHECK_COMPONENT = {
    check: component for component, checks in COMPONENT_CHECKS.items() for check in checks
}
VISIBILITY = {"observed": 1.0, "partial": 0.5, "unobservable": 0.0}
CONFIDENCE = {"high": 1.0, "medium": 0.5, "low": 0.0}
CRITICAL_CHECKS = {"operating_access", "user_position", "support_contact"}
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
INPUT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["generated_image", "twin_image", "product_type", "scene_prompt", "image_stage"],
    "properties": {
        "generated_image": {"type": "string", "minLength": 1},
        "twin_image": {"type": "string", "minLength": 1},
        "product_type": {"enum": ["laptop", "printer"]},
        "scene_prompt": {"type": "string"},
        "image_stage": {"const": "scene_generation"},
    },
}
INPUT_VALIDATOR = Draft202012Validator(INPUT_SCHEMA)


class PlacementValidationError(ValueError):
    def __init__(self, errors: list[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(errors))


def _schema_errors(value: Any, validator: Draft202012Validator) -> list[str]:
    errors = sorted(validator.iter_errors(value), key=lambda error: tuple(map(str, error.absolute_path)))
    formatted = []
    for error in errors:
        path = "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path)
        formatted.append(f"{path}: {error.message}")
    return formatted


def validate_runtime_input(value: Any) -> Mapping[str, Any]:
    errors = _schema_errors(value, INPUT_VALIDATOR)
    if errors:
        raise PlacementValidationError(errors)
    return value


def validate_assessment(value: Any) -> Mapping[str, Any]:
    errors = _schema_errors(value, ASSESSMENT_VALIDATOR)
    if errors:
        raise PlacementValidationError(errors)
    if value["stage_status"] == "unable":
        if value["unable_reason"] is None or value["checks"] is not None:
            errors.append("unable assessment requires unable_reason and checks=null")
    else:
        if value["unable_reason"] is not None or not isinstance(value["checks"], Mapping):
            errors.append("assessed result requires unable_reason=null and checks object")
        if not value["functional_front"].strip() or not value["context_reading"].strip():
            errors.append("assessed result requires nonblank functional_front and context_reading")

    if isinstance(value.get("checks"), Mapping):
        for name, check in value["checks"].items():
            prefix = f"$.checks.{name}"
            visibility = check["visibility"]
            severity = check["severity"]
            confidence = check["confidence"]
            warning = check["warning_level"]
            codes = check["issue_codes"]
            if not check["evidence"].strip():
                errors.append(f"{prefix}.evidence must be nonblank")
            invalid = sorted(set(codes) - ISSUE_OWNERS[name])
            if invalid:
                errors.append(f"{prefix}.issue_codes invalid ownership: {invalid}")
            if visibility == "unobservable":
                if severity is not None or confidence != "low" or warning != "none" or codes:
                    errors.append(f"{prefix}: unobservable invariant violated")
                if not check["visibility_limit"].strip():
                    errors.append(f"{prefix}.visibility_limit must be nonblank when unobservable")
            else:
                if severity is None:
                    errors.append(f"{prefix}.severity must be integer when assessable")
                if visibility == "partial" and not check["visibility_limit"].strip():
                    errors.append(f"{prefix}.visibility_limit must be nonblank when partial")
            if severity == 0 and (codes or warning != "none"):
                errors.append(f"{prefix}: severity 0 requires no codes and warning none")
            elif severity == 1 and (not codes or warning not in {"advisory", "review"}):
                errors.append(f"{prefix}: severity 1 requires codes and advisory/review warning")
            elif isinstance(severity, int) and severity >= 2:
                if not codes or warning != "none":
                    errors.append(f"{prefix}: severity 2-4 requires codes and warning none")
                if not check["consequence"].strip() or not check["alternative_explanation"].strip():
                    errors.append(f"{prefix}: material finding requires consequence and alternative")
            if "chair_displacement" in codes and severity != 1:
                errors.append(f"{prefix}: chair_displacement must have severity 1")
    if errors:
        raise PlacementValidationError(errors)
    return value


def validate_result(value: Any) -> Mapping[str, Any]:
    errors = _schema_errors(value, RESULT_VALIDATOR)
    if errors:
        raise PlacementValidationError(errors)
    if value["status"] == "ok":
        if value["assessment"] is None or value["derived"] is None or value["error"] is not None:
            errors.append("ok envelope requires assessment+derived and error=null")
        else:
            validate_assessment(value["assessment"])
        if not value["audit"]["target_record_id"] or not value["audit"]["selected_anchor_ids"]:
            errors.append("ok anchored envelope requires target_record_id and selected anchors")
    else:
        if value["derived"] is not None or value["error"] is None:
            errors.append("error envelope requires derived=null and error object")
    if errors:
        raise PlacementValidationError(errors)
    return value


def _round_half_up(value: float) -> int:
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def aggregate_assessment(assessment: Any) -> dict[str, Any]:
    validate_assessment(assessment)
    if assessment["stage_status"] != "assessed":
        raise PlacementValidationError(["unable assessment has no placement score"])
    checks = assessment["checks"]
    components = {}
    total_effective_weight = 0.0
    weighted_score = 0.0
    confidence_numerator = 0.0
    confirmed_material = []
    uncertain_material = []
    review_warnings = []
    advisories = []
    critical_unobservable = []

    for name, check in checks.items():
        severity = check["severity"]
        if isinstance(severity, int) and severity >= 2:
            (confirmed_material if check["confidence"] == "high" else uncertain_material).append((name, severity))
        if severity == 1:
            (review_warnings if check["warning_level"] == "review" else advisories).append(name)
        if name in CRITICAL_CHECKS and check["visibility"] == "unobservable":
            critical_unobservable.append(name)

    for component, component_checks in COMPONENT_CHECKS.items():
        visibility_sum = sum(VISIBILITY[checks[name]["visibility"]] for name in component_checks)
        coverage = visibility_sum / len(component_checks)
        effective_weight = COMPONENT_WEIGHTS[component] * coverage
        observable_effective_severities = []
        for name in component_checks:
            check = checks[name]
            vis = VISIBILITY[check["visibility"]]
            if vis:
                severity = check["severity"]
                effective_severity = 1 if severity >= 2 and check["confidence"] != "high" else severity
                observable_effective_severities.append(effective_severity)
                confidence_numerator += (
                    COMPONENT_WEIGHTS[component] * vis / len(component_checks) * CONFIDENCE[check["confidence"]]
                )
        component_score = None
        if observable_effective_severities:
            component_score = 100 - 25 * max(observable_effective_severities)
            weighted_score += effective_weight * component_score
            total_effective_weight += effective_weight
        components[component] = {
            "coverage": round(coverage, 3),
            "score": component_score,
            "effective_weight": round(effective_weight, 3),
        }

    if total_effective_weight == 0:
        raise PlacementValidationError(["no observable placement evidence"])
    overall_coverage = total_effective_weight / 100
    base_score = weighted_score / total_effective_weight
    cap = None
    if confirmed_material:
        worst = max(severity for _, severity in confirmed_material)
        cap = {2: 59, 3: 39, 4: 19}[worst]
    elif uncertain_material:
        cap = 79
    score = _round_half_up(min(base_score, cap) if cap is not None else base_score)
    q = confidence_numerator / total_effective_weight
    if overall_coverage >= 0.85 and q >= 0.85 and not uncertain_material and not critical_unobservable:
        confidence = "high"
    elif overall_coverage >= 0.60 and q >= 0.60:
        confidence = "medium"
    else:
        confidence = "low"

    reasons = []
    if confirmed_material:
        verdict = "fail"
        reasons.append("confirmed_material_defect")
    else:
        # Coverage and evidence confidence describe epistemic limits; they are not
        # placement defects. Hidden chair/user/contact relations in tight crops can
        # therefore pass. Only a material-but-uncertain finding or an explicit
        # severity-1 review warning withholds an automatic pass.
        if uncertain_material:
            reasons.append("uncertain_material_defect")
        if review_warnings:
            reasons.append("placement_review_warning")
        verdict = "review" if (uncertain_material or review_warnings) else "pass"
    if advisories:
        reasons.append("placement_advisory")
    if assessment["general_artifact_warnings"]:
        reasons.append("general_artifact_warning")

    return {
        "rules_version": RULES_VERSION,
        "score": score,
        "score_basis": "observable_evidence_only",
        "coverage": round(overall_coverage, 3),
        "confidence": confidence,
        "verdict": verdict,
        "reason_codes": list(dict.fromkeys(reasons)),
        "components": components,
        "confirmed_material_checks": [name for name, _ in confirmed_material],
        "uncertain_material_checks": [name for name, _ in uncertain_material],
        "review_warning_checks": review_warnings,
        "advisory_checks": advisories,
        "critical_unobservable_checks": critical_unobservable,
        "base_score_before_cap": round(base_score, 3),
        "applied_score_cap": cap,
    }
