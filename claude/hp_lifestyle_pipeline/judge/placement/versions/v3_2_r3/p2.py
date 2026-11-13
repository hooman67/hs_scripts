"""Independent P2 discovery specialists followed by one image-based reconciliation.

Only the reconciler's placement-observations-v3 output enters the unchanged
legacy deterministic scorer; specialist findings are evidence, not votes.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import common
from jsonschema import Draft202012Validator

PROTOCOL_VERSION = "placement-v3.2-p2-r3"
GEOMETRY_CODES = {
    "support_construction": ("malformed_support_furniture",),
    "rigid_alignment": ("furniture_axis_conflict", "corner_facing"),
    "relative_scale_perspective": ("implausible_scale", "conflicting_perspective"),
    "product_contact": (
        "floating",
        "sinking_or_intersection",
        "inconsistent_shadow",
        "inconsistent_reflection",
    ),
}
USE_CODES = {
    "support_scenario": (
        "inappropriate_support",
        "occupied_workstation",
        "implausible_scenario",
        "unsupported_base",
        "unmotivated_position",
        "incoherent_use_arrangement",
        "misplaced_support_furniture",
        "unpopulated_storage",
        "bare_staged_setting",
    ),
    "access_usability": (
        "excessive_reach",
        "precarious_edge",
        "blocked_operating_side",
        "no_user_position",
        "furniture_collision",
        "blocked_paper_or_lid_path",
        "blocked_user_workspace",
    ),
    "layout_orientation": (
        "furniture_axis_conflict",
        "furniture_layout_conflict",
        "ancillary_axis_conflict",
    ),
}


def _discovery_schema(version, codes):
    findings = {}
    for name, allowed in codes.items():
        properties = {
            "visibility": {
                "type": "string",
                "enum": ["observed", "partial", "unobservable"],
            },
            "severity": {"type": ["integer", "null"], "minimum": 0, "maximum": 4},
            "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
            "evidence": {"type": "string", "minLength": 1},
            "counter_evidence": {"type": "string"},
            "limit": {"type": "string"},
            "consequence": {"type": "string"},
            "issue_codes": {
                "type": "array",
                "uniqueItems": True,
                "items": {"type": "string", "enum": list(allowed)},
            },
        }
        findings[name] = {
            "type": "object",
            "additionalProperties": False,
            "required": list(properties),
            "properties": properties,
        }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "product_match",
            "product_match_note",
            "findings",
        ],
        "properties": {
            "schema_version": {"type": "string", "const": version},
            "product_match": {
                "type": "string",
                "enum": ["match", "uncertain", "mismatch"],
            },
            "product_match_note": {"type": "string"},
            "findings": {
                "type": "object",
                "additionalProperties": False,
                "required": list(findings),
                "properties": findings,
            },
        },
    }


GEOMETRY_SCHEMA = _discovery_schema("placement-geometry-discovery-v1", GEOMETRY_CODES)
USE_SCHEMA = _discovery_schema("placement-use-discovery-v1", USE_CODES)
Draft202012Validator.check_schema(GEOMETRY_SCHEMA)
Draft202012Validator.check_schema(USE_SCHEMA)
_GEOMETRY_VALIDATOR = Draft202012Validator(GEOMETRY_SCHEMA)
_USE_VALIDATOR = Draft202012Validator(USE_SCHEMA)


def geometry_schema():
    return copy.deepcopy(GEOMETRY_SCHEMA)


def use_schema():
    return copy.deepcopy(USE_SCHEMA)


def _validate_discovery(value, validator):
    validator.validate(value)
    errors = []
    for name, finding in value["findings"].items():
        prefix = f"$.findings.{name}"
        severity = finding["severity"]
        codes = finding["issue_codes"]
        if not finding["evidence"].strip():
            errors.append(f"{prefix}.evidence: must contain non-whitespace evidence")
        if finding["visibility"] == "unobservable":
            if severity is not None:
                errors.append(f"{prefix}.severity: must be null when unobservable")
            if finding["confidence"] != "low":
                errors.append(f"{prefix}.confidence: must be low when unobservable")
            if codes:
                errors.append(f"{prefix}.issue_codes: must be empty when unobservable")
        elif type(severity) is not int:
            errors.append(f"{prefix}.severity: must be an integer when assessable")
        if severity == 0 and codes:
            errors.append(f"{prefix}.issue_codes: must be empty when severity is 0")
        elif severity is not None and severity > 0 and not codes:
            errors.append(
                f"{prefix}.issue_codes: positive severity requires a supported code"
            )
    if errors:
        raise ValueError("; ".join(errors))
    return value


def validate_geometry(value):
    return _validate_discovery(value, _GEOMETRY_VALIDATOR)


def validate_use(value):
    return _validate_discovery(value, _USE_VALIDATOR)


def judge(runtime_input, output, client=None):
    common.LEGACY.SCORING.validate_runtime_input(runtime_input)
    freeze = common.verify_freeze()
    output = Path(output)
    geometry = common.call_stage(
        runtime_input,
        "p2_geometry",
        output / "p2_geometry",
        GEOMETRY_SCHEMA,
        validate_geometry,
        cap=12000,
        client=client,
    )
    use_location = common.call_stage(
        runtime_input,
        "p2_use",
        output / "p2_use",
        USE_SCHEMA,
        validate_use,
        cap=12000,
        client=client,
    )
    reconciled = common.call_stage(
        runtime_input,
        "p2_reconcile",
        output / "p2_reconcile",
        common.OBSERVATION_SCHEMA,
        common.LEGACY.validate_new_observation,
        reports={
            "geometry": geometry["observation"],
            "use_location": use_location["observation"],
        },
        cap=12000,
        client=client,
    )
    score = common.LEGACY.SCORING.aggregate_observation(reconciled["observation"])
    stages = ("p2_geometry", "p2_use", "p2_reconcile")
    envelope = {
        "protocol_version": PROTOCOL_VERSION,
        "ok": True,
        "runtime_input": runtime_input,
        "protocol_freeze_sha256": freeze,
        "stages": {
            stage: {
                "path": str((output / stage / "result.json").resolve()),
                "sha256": common.sha(output / stage / "result.json"),
            }
            for stage in stages
        },
        "application_merged_judgment": score,
        "final_decision": {"verdict": score["verdict"]},
        "candidate": "p2",
    }
    result_path = output / "result.json"
    if result_path.exists() and json.loads(result_path.read_text()) != envelope:
        raise RuntimeError("Existing P2 result differs from reproducible recomputation")
    common.write_json(result_path, envelope)
    return envelope


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = judge(json.loads(args.input.read_text()), args.output)
    print(
        json.dumps(
            {
                "verdict": result["final_decision"]["verdict"],
                "score": result["application_merged_judgment"][
                    "natural_placement_score"
                ],
            }
        )
    )


if __name__ == "__main__":
    main()
