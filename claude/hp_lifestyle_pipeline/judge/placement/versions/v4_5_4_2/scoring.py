"""Strict V4.5.2 observer validation and deterministic synthesis."""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from codebook import (
    ALL_TESTS,
    COHERENT_SUBTYPES,
    COMPONENT_TESTS,
    DEFECT_SUBTYPES,
    FUNCTIONAL_TESTS,
    GEOMETRY_TESTS,
    ISSUE_BY_SUBTYPE,
    PENALTY_GROUPS,
    SEVERITY_BY_SUBTYPE,
    SEVERITY_PENALTY,
)

ROOT = Path(__file__).resolve().parent
FUNCTIONAL_SCHEMA = json.loads((ROOT / "functional_observer_schema.json").read_text())
GEOMETRY_SCHEMA = json.loads((ROOT / "geometry_observer_schema.json").read_text())
FUNCTIONAL_VALIDATOR = Draft202012Validator(FUNCTIONAL_SCHEMA)
GEOMETRY_VALIDATOR = Draft202012Validator(GEOMETRY_SCHEMA)

class PlacementValidationError(ValueError):
    def __init__(self, errors: list[str] | tuple[str, ...]):
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))

def canonical_sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _schema_errors(value: Any, validator: Draft202012Validator) -> list[str]:
    errors = []
    for error in sorted(validator.iter_errors(value), key=lambda item: tuple(map(str, item.absolute_path))):
        path = "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path)
        errors.append(f"{path}: {error.message}")
    return errors

def _valid_region(region: Mapping[str, Any] | None) -> bool:
    if not region:
        return False
    x0, y0, x1, y1 = region["box"]
    return x1 > x0 and y1 > y0

def _validate_relations(value: Mapping[str, Any], expected: tuple[str, ...], errors: list[str]) -> None:
    relations = value.get("relations") or []
    ids = [item.get("test_id") for item in relations]
    if len(ids) != len(set(ids)) or tuple(ids) != expected:
        errors.append("relations must contain every fixed test exactly once in the prescribed order")
    for index, relation in enumerate(relations):
        test_id = relation.get("test_id")
        if test_id not in ALL_TESTS:
            continue
        state = relation.get("state")
        obs = relation.get("observability")
        subtype = relation.get("subtype")
        if state == "defect":
            if subtype not in DEFECT_SUBTYPES[test_id]:
                allowed = sorted(DEFECT_SUBTYPES[test_id])
                errors.append(f"relations[{index}] {test_id} state=defect got subtype={subtype!r}; allowed={allowed}")
            if obs == "hidden" or not _valid_region(relation.get("region")):
                errors.append(f"relations[{index}] defect requires visible/partial evidence and positive-area region")
        elif state == "coherent":
            if subtype not in COHERENT_SUBTYPES[test_id]:
                allowed = sorted(COHERENT_SUBTYPES[test_id])
                errors.append(f"relations[{index}] {test_id} state=coherent got subtype={subtype!r}; allowed={allowed}")
            if obs == "hidden" or relation.get("region") is not None:
                errors.append(f"relations[{index}] coherent requires visible/partial observability and null region")
        elif state == "unresolved":
            if subtype != "unresolved" or relation.get("region") is not None:
                errors.append(f"relations[{index}] {test_id} state=unresolved got subtype={subtype!r}; allowed=['unresolved']; region must be null")
            if obs not in {"hidden", "partial"}:
                errors.append(f"relations[{index}] unresolved requires hidden or partial observability")

def validate_functional(value: Mapping[str, Any], product_type: str | None = None) -> Mapping[str, Any]:
    errors = _schema_errors(value, FUNCTIONAL_VALIDATOR)
    status = value.get("stage_status")
    if status == "unable":
        if value.get("unable_reason") is None or value.get("product_front") is not None or value.get("visible_user_positions") is not None or value.get("relations") is not None:
            errors.append("unable functional stage requires reason and null observation fields")
    elif status == "assessed":
        if value.get("unable_reason") is not None or value.get("product_front") is None or value.get("visible_user_positions") is None or value.get("relations") is None:
            errors.append("assessed functional stage requires observations and null unable_reason")
        _validate_relations(value, FUNCTIONAL_TESTS, errors)
        front = value.get("product_front") or {}
        if front.get("state") == "hidden" and front.get("region") is not None:
            errors.append("hidden product front requires null region")
        if front.get("state") in {"observed", "partial"} and not _valid_region(front.get("region")):
            errors.append("observed/partial product front requires positive-area region")
        if product_type == "laptop":
            for relation in value.get("relations") or []:
                if relation.get("subtype") == "central_rectangular_home_printer_support_without_shared_use":
                    errors.append("home-printer central-support subtype cannot apply to laptop")
    if errors:
        raise PlacementValidationError(errors)
    return value

def validate_geometry(value: Mapping[str, Any]) -> Mapping[str, Any]:
    errors = _schema_errors(value, GEOMETRY_VALIDATOR)
    status = value.get("stage_status")
    if status == "unable":
        if value.get("unable_reason") is None or value.get("support_inventory") is not None or value.get("edge_observations") is not None or value.get("relations") is not None:
            errors.append("unable geometry stage requires reason and null observation fields")
    elif status == "assessed":
        if value.get("unable_reason") is not None or value.get("support_inventory") is None or value.get("edge_observations") is None or value.get("relations") is None:
            errors.append("assessed geometry stage requires observations and null unable_reason")
        _validate_relations(value, GEOMETRY_TESTS, errors)
        inventory = value.get("support_inventory") or {}
        exposed = inventory.get("exposed_required_regions") or []
        breaks = inventory.get("visible_breaks_or_negative_space") or []
        edges = value.get("edge_observations") or []
        for index, edge in enumerate(edges):
            p0, p1 = edge.get("p0"), edge.get("p1")
            for endpoint_name, endpoint in (("p0", p0), ("p1", p1)):
                if (
                    isinstance(endpoint, list)
                    and len(endpoint) == 2
                    and all(isinstance(coordinate, (int, float)) for coordinate in endpoint)
                    and any(coordinate < 0 or coordinate > 1 for coordinate in endpoint)
                ):
                    errors.append(
                        f"edge_observations[{index}].{endpoint_name} coordinates must be normalized "
                        f"to [0,1]; got {endpoint!r}"
                    )
            if isinstance(p0, list) and isinstance(p1, list) and p0 == p1:
                errors.append(
                    f"edge_observations[{index}] is zero-length because p0==p1; "
                    "emit two distinct normalized [0,1] endpoints traced from the raw image"
                )
            evidence = edge.get("raw_pixel_evidence")
            normalized = evidence.strip().lower() if isinstance(evidence, str) else ""
            if normalized in {
                "placeholder", "generic placeholder", "visible edge", "edge",
                "raw pixel evidence", "n/a", "none", "unknown", "tbd",
            } or "placeholder" in normalized:
                errors.append(
                    f"edge_observations[{index}].raw_pixel_evidence is placeholder/generic; "
                    "replace it with a concrete description of the visible raw-pixel boundary"
                )
        edge_owners = {edge.get("owner") for edge in edges}
        by_id = {r.get("test_id"): r for r in (value.get("relations") or [])}
        if by_id.get("load_path", {}).get("state") == "defect":
            if not any(item.get("connected_support_visible") is False for item in exposed):
                errors.append("load_path defect requires an exposed region with connected_support_visible=false")
            if not any(item.get("kind") in {"gap", "disconnection", "unsupported_span"} for item in breaks):
                errors.append("load_path defect requires a visible gap, disconnection, or unsupported span")
        if by_id.get("support_anatomy", {}).get("state") == "defect" and not any(item.get("kind") in {"disconnection", "impossible_junction", "unsupported_span"} for item in breaks):
            errors.append("support_anatomy defect requires a visible topology break")
        if by_id.get("device_support_axes", {}).get("state") == "defect" and (
            not edge_owners.intersection({"product_front", "product_depth"})
            or not edge_owners.intersection({"support_front", "support_side"})
        ):
            errors.append("device_support_axes defect requires named product and support edges")
        if by_id.get("furniture_room_axes", {}).get("state") == "defect" and (
            not edge_owners.intersection({"support_front", "support_side"})
            or not edge_owners.intersection({"wall", "floor", "cabinet", "neighboring_furniture"})
        ):
            errors.append("furniture_room_axes defect requires named support and room/furniture edges")
        if by_id.get("shared_perspective", {}).get("state") == "defect" and len(edge_owners) < 2:
            errors.append("shared_perspective defect requires at least two named edge-owner families")
    if errors:
        raise PlacementValidationError(errors)
    return value

def _sentinel(reason: str, warnings: list[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "rules_version": "hp-placement-v4.5.2-deterministic-v1", "score": 0,
        "score_valid": False, "verdict": "review", "reason": reason, "checks": {},
        "components": {}, "confirmed_issues": [], "uncertain_relations": [],
        "advisories": list(warnings or []), "warnings": list(warnings or []),
        "penalty_causes": {}, "owned_issue_codes": [],
        "explanation": "The product/support placement could not be assessed reliably.",
    }

def error_sentinel(message: str) -> dict[str, Any]:
    result = _sentinel("execution_error")
    result["explanation"] = f"Judge execution failed: {message}"
    return result

def synthesize(functional: Mapping[str, Any], geometry: Mapping[str, Any], product_type: str | None = None) -> dict[str, Any]:
    validate_functional(functional, product_type)
    validate_geometry(geometry)
    warnings = list(functional.get("unrelated_artifacts") or []) + list(geometry.get("unrelated_artifacts") or [])
    if functional["stage_status"] == "unable" or geometry["stage_status"] == "unable":
        return _sentinel("unassessable_target", warnings)
    relations = list(functional["relations"]) + list(geometry["relations"])
    by_id = {relation["test_id"]: relation for relation in relations}
    if set(by_id) != set(ALL_TESTS):
        raise PlacementValidationError(["synthesis requires all fourteen disjoint relations"])
    confirmed = []
    uncertain = []
    checks = {}
    for test_id in ALL_TESTS:
        relation = by_id[test_id]
        issue_code = None
        severity = 0
        if relation["state"] == "defect":
            issue_code = ISSUE_BY_SUBTYPE[relation["subtype"]]
            severity = SEVERITY_BY_SUBTYPE[relation["subtype"]]
            confirmed.append({
                "test_id": test_id, "issue_code": issue_code, "subtype": relation["subtype"],
                "severity": severity, "evidence": relation["direct_evidence"], "region": relation["region"],
            })
        elif relation["state"] == "unresolved":
            uncertain.append({"test_id": test_id, "evidence": relation["direct_evidence"], "visibility_limit": relation["visibility_limit"]})
        checks[test_id] = {
            "state": "confirmed" if relation["state"] == "defect" else ("unobservable" if relation["state"] == "unresolved" else "tested_absent"),
            "issue_code": issue_code, "subtype": relation["subtype"], "severity": severity,
            "observability": relation["observability"], "evidence": relation["direct_evidence"],
            "counterevidence": relation["counterevidence"], "visibility_limit": relation["visibility_limit"],
        }
    if all(check["state"] == "unobservable" for check in checks.values()):
        return _sentinel("all_relations_unobservable", warnings)
    penalties = {}
    for group, test_ids in PENALTY_GROUPS.items():
        group_confirmed = [item for item in confirmed if item["test_id"] in test_ids]
        severity = max((item["severity"] for item in group_confirmed), default=0)
        penalties[group] = {
            "severity": severity, "confirmed_tests": [item["test_id"] for item in group_confirmed],
            "penalty": SEVERITY_PENALTY.get(severity, 0),
        }
    raw_score = max(0, 100 - sum(item["penalty"] for item in penalties.values()))
    if any(item["severity"] >= 2 for item in confirmed):
        verdict, score = "fail", min(59, raw_score)
    elif any(item["severity"] == 1 for item in confirmed):
        verdict, score = "review", min(89, max(60, raw_score))
    else:
        verdict, score = "pass", 100
    components = {}
    for component, test_ids in COMPONENT_TESTS.items():
        items = [checks[test_id] for test_id in test_ids]
        state = "fail" if any(item["state"] == "confirmed" and item["severity"] >= 2 for item in items) else ("review" if any(item["state"] == "confirmed" for item in items) else "pass")
        components[component] = {"state": state, "tests": list(test_ids)}
    parts = [f"{item['issue_code']} (severity {item['severity']}): {item['evidence']}" for item in confirmed]
    if not parts:
        parts.append("No placement defect was observed in the assessed visible relations.")
    if uncertain:
        parts.append("Unresolved visible relations: " + "; ".join(f"{item['test_id']}: {item['visibility_limit']}" for item in uncertain))
    if warnings:
        parts.append("Separate zero-penalty rendering warnings: " + "; ".join(item["evidence"] for item in warnings))
    return {
        "rules_version": "hp-placement-v4.5.2-deterministic-v1", "score": score,
        "score_valid": True, "verdict": verdict,
        "reason": "confirmed_material_defect" if verdict == "fail" else ("reviewable_finding" if verdict == "review" else "no_observed_defect"),
        "checks": checks, "components": components, "confirmed_issues": confirmed,
        "uncertain_relations": uncertain, "advisories": warnings, "warnings": warnings,
        "penalty_causes": penalties, "owned_issue_codes": sorted({item["issue_code"] for item in confirmed}),
        "explanation": " ".join(parts),
    }
