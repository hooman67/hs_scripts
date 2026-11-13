"""Evidence-first envelope; original V3 observation/scoring payload is unchanged."""
from __future__ import annotations

import copy

from jsonschema import Draft202012Validator

VERSION = "placement-evidence-envelope-v3.1-r2"
FOCUSED_DIMENSIONS = {"alignment": "orientation_alignment", "construction": "scale_perspective"}
FOCUSED_CODES = {
    "alignment": ["furniture_axis_conflict", "corner_facing"],
    "construction": ["malformed_support_furniture", "conflicting_perspective"],
}


def obj(properties):
    return {"type": "object", "additionalProperties": False,
            "required": list(properties), "properties": properties}


def text():
    return {"type": "string", "minLength": 1}


def choice(values):
    return {"type": "string", "enum": values}


def array(item):
    return {"type": "array", "items": item}


def trace_schema():
    comparison = obj({
        "boundary_refs": array(text()),
        "relationship": choice(["compatible", "different_direction_family", "indeterminate", "not_applicable"]),
        "projective_explanation": text(), "counter_evidence": text(), "visibility_limits": text(),
    })
    findings = {
        focus: obj({
            "conclusion": choice(["material_established", "no_visible_material_defect",
                                  "unresolved", "not_applicable"]),
            "evidence_refs": array(text()), "evidence": text(), "counter_evidence": text(),
            "visibility_limits": text(), "consequence": {"type": "string"},
            "issue_codes": array(choice(codes)),
        }) for focus, codes in FOCUSED_CODES.items()
    }
    return obj({
        "boundary_inventory": array(obj({
            "id": text(), "owner": choice(["product_base", "support_surface"]),
            "role": choice(["width", "depth", "curved_outline", "other"]),
            "visible_location": text(), "visibility": choice(["observed", "partial"]),
            "visibility_limits": text(),
        })),
        "axis_comparisons": obj({"width": comparison, "depth": copy.deepcopy(comparison)}),
        "surface_construction": obj({
            "visible_outline": text(), "thickness_and_joins": text(),
            "visibility_limits": text(), "counter_evidence": text(),
        }),
        "member_connections": array(obj({
            "id": text(), "owner": choice(["support_surface", "associated_seating", "other", "uncertain"]),
            "visible_location": text(), "exposed_connections": text(),
            "termination": choice(["visible_connection", "visible_disconnection",
                                   "occluded", "out_of_frame", "uncertain"]),
            "alternative_interpretation": text(), "visibility_limits": text(),
        })),
        "focused_findings": obj(findings),
    })


def envelope_schema(payload):
    payload = copy.deepcopy(payload)
    definitions = payload.pop("$defs", {})
    payload.pop("$id", None)
    payload.pop("$schema", None)
    schema = obj({
        "schema_version": {"type": "string", "const": VERSION},
        "trace": trace_schema(),
        "observation": payload,
    })
    if definitions:
        schema["$defs"] = definitions
    return schema


def material(component):
    return (component["visibility"] in {"observed", "partial"}
            and component["confidence"] in {"medium", "high"}
            and isinstance(component["severity"], int) and component["severity"] >= 2)


def validate(value, payload_schema):
    """Reject missing/inconsistent evidence; never repair or promote observations."""
    Draft202012Validator(envelope_schema(payload_schema)).validate(value)
    trace, observation = value["trace"], value["observation"]

    def reject_blank(node):
        if isinstance(node, dict):
            for key, child in node.items():
                if isinstance(child, str) and key != "consequence" and not child.strip():
                    raise ValueError(f"Whitespace-only trace field: {key}")
                reject_blank(child)
        elif isinstance(node, list):
            for child in node:
                reject_blank(child)
    reject_blank(trace)
    boundaries = trace["boundary_inventory"]
    members = trace["member_connections"]
    ids = [row["id"] for row in boundaries + members]
    if len(set(ids)) != len(ids) or "surface" in ids:
        raise ValueError("Trace IDs must be unique; surface is reserved")
    boundary_by_id = {row["id"]: row for row in boundaries}
    for axis, comparison in trace["axis_comparisons"].items():
        refs = comparison["boundary_refs"]
        if len(set(refs)) != len(refs) or set(refs) - set(boundary_by_id):
            raise ValueError("Axis comparison references unknown/duplicate boundaries")
        if any(boundary_by_id[ref]["role"] != axis for ref in refs):
            raise ValueError("Corresponding axis references must use that geometric role")
        if comparison["relationship"] in {"compatible", "different_direction_family"}:
            if {boundary_by_id[ref]["owner"] for ref in refs} != {"product_base", "support_surface"}:
                raise ValueError("Axis comparison requires both product and support evidence")
    valid_refs = set(ids) | {"surface"}
    for focus, finding in trace["focused_findings"].items():
        refs = finding["evidence_refs"]
        if len(set(refs)) != len(refs) or set(refs) - valid_refs:
            raise ValueError("Focused finding references unknown/duplicate evidence")
        dim = FOCUSED_DIMENSIONS[focus]
        if dim not in observation["components"]:
            if finding["conclusion"] != "not_applicable" or finding["issue_codes"]:
                raise ValueError("Verifier trace cannot assess an unrequested dimension")
            continue
        if finding["conclusion"] == "material_established":
            component = observation["components"][dim]
            if (not refs or not finding["issue_codes"] or not finding["consequence"].strip()
                    or not material(component)
                    or not set(finding["issue_codes"]).issubset(component["issue_codes"])):
                raise ValueError("Established trace finding must map to a material scored component")
            if focus == "alignment" and not any(
                c["relationship"] == "different_direction_family"
                for c in trace["axis_comparisons"].values()
            ):
                raise ValueError("Material product/support alignment requires a direction-family conflict")
        elif finding["issue_codes"]:
            raise ValueError("Non-material trace finding must not claim material issue codes")
    return observation
