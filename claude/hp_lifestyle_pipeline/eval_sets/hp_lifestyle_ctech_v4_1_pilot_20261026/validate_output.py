#!/usr/bin/env python3
"""Deterministic semantic validator for one V4.1 candidate bank; never repairs output."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import jsonschema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCRIPTS = ROOT / "research/source_messaging_v1_to_v6/versions/v4.1/scripts"
VERSION = SCRIPTS.parent
OUTPUT_SCHEMA = VERSION / "output.schema.json"
EXPECTED_ENVIRONMENTS = ("Home", "Office", "Education", "Gaming", "Café", "Creative Studio")
sys.path.insert(0, str(SCRIPTS))
from camera_profile_resolver import load_registry, resolve_profile  # noqa: E402

DEVICE_RE = re.compile(
    r"\b(?:laptops?|printers?|mini\s*pcs?|minipcs?|desktops?|computers?|monitors?|"
    r"hardware|devices?|skus?|phones?|smartphones?|tablets?|screens?|keyboards?|"
    r"hp|elitebooks?|omnibooks?|laserjets?)\b", re.I
)
CAMERA_RE = re.compile(r"\b(?:camera|lens|render(?:ing)?|zoom|aspect ratio|depth of field|bokeh|pull back|widen the view)\b", re.I)
BLUE_RE = re.compile(r"\bblue\b", re.I)
UNNATURAL_PLACE_RE = re.compile(
    r"\b(?:(?:close|local|tight|compact|small) (?:section|patch|area|portion|piece|stretch|slice) of|shared department records counter|records counter|"
    r"paperwork nook|policy deployment counter|illustration worktop|"
    r"teaching[- ]preparation table|"
    r"(?:records?|policy|deployment|paperwork|illustration|workflow|department|administration|administrative|output check|queue)\s+"
    r"(?:counter|nook|corner|worktop|surface)|"
    r"(?:teaching[- ]preparation|content review|document review|records?|paperwork|workflow|department)\s+"
    r"(?:desk|table|counter|nook|worktop|surface)|workspace feeling|document queue)\b", re.I
)
KSP_RE = re.compile(r"^KSP[1-9][0-9]*$")
SURFACE_DESKTOP_RE = re.compile(
    r"\b(?:wooden|wood|walnut|oak|birch|maple|laminate|veneer|painted|satin|matte|smooth|white|graphite)\s+desktop\b",
    re.I,
)
NONCOMPUTING_SCREEN_RE = re.compile(r"\b(?:privacy|acoustic|folding|divider)\s+screen\b", re.I)
ALLOWED_TEXT_FIELDS = {"headline", "long_message_best_sku", "long_message_safe_to_inherit",
                       "mid_length", "short_message", "ultra_short",
                       "mid_length_safe_to_inherit", "short_message_safe_to_inherit",
                       "ultra_short_safe_to_inherit"}

REFERENCE_LIBRARY = VERSION / "reference_library.json"
_REFERENCE_DOC = json.loads(REFERENCE_LIBRARY.read_text(encoding="utf-8"))
CTECH_REFERENCES = {
    item["id"]: (item["environment"], item["text"])
    for item in _REFERENCE_DOC["references"]
}


def digest_obj(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def _path_value(root: Any, path: str) -> Any:
    cur = root
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(path)
        cur = cur[part]
    return cur


def prohibited_device_term(text: str) -> str | None:
    """Return a device term, excluding established furniture/divider compounds."""

    allowed_spans = [m.span() for m in SURFACE_DESKTOP_RE.finditer(text)]
    allowed_spans.extend(m.span() for m in NONCOMPUTING_SCREEN_RE.finditer(text))
    for match in DEVICE_RE.finditer(text):
        if any(start <= match.start() and match.end() <= end for start, end in allowed_spans):
            continue
        return match.group(0)
    return None


def literal_background_collections(text: str) -> set[str]:
    """Conservative count of named furniture/room collections that cannot be a focal surface."""

    lowered = text.casefold()
    hits = set()
    tests = {
        "simple furniture": r"\bsimple furniture\b",
        "desks": r"\bdesks\b",
        "workstations": r"\b(?:multiple|repeating) workstations\b",
        "work areas": r"\brepeating work areas\b",
        "shelving": r"\b(?:(?<!integrated )shelving|bookshelves|floating shelves|display shelving)\b",
        "wall": r"\b(?:textured\s+)?wall\b(?!\s+art)",
        "couch": r"\bcouch\b",
        "chair": r"\b(?:(?:comfortable|accent|ergonomic)\s+)?chairs?\b",
        "plants": r"\b(?:plants|houseplants)\b",
        "soft textiles": r"\bsoft textiles\b",
        "windows": r"\b(?:large )?windows\b",
        "curtains": r"\b(?:soft|relaxed) curtains\b",
        "artwork": r"\b(?:framed art(?:work)?|wall art|artwork)\b",
        "seating": r"\b(?:comfortable )?seating\b",
        "cabinetry": r"\b(?:white|sleek) cabinetry\b",
        "side cabinet": r"\bside cabinet\b",
        "furnishings": r"\b(?:(?:layered|office|residential|subtle residential|familiar residential)\s+)?furnishings\b",
        "architectural details": r"\barchitectural details\b",
        "workplace decor": r"\b(?:refined )?workplace d[ée]cor\b",
        "organized displays": r"\borganized displays\b",
        "collectibles": r"\bcollectibles\b",
    }
    for label, pattern in tests.items():
        if re.search(pattern, lowered):
            hits.add(label)
    # One explicitly described shelf and its contents occupy one fixture slot.
    # This is the same treatment as books on a bookshelf; independent collections still count.
    if "shelving" in hits and re.search(
            r"\b(?:shelving|shelves)\s+(?:holding|displaying|with)\s+(?:a few |small |curated )?collectibles\b", lowered):
        hits.discard("collectibles")
    return hits


COLLECTION_AS_SURFACE_RE = re.compile(
    r"\b(?:simple furniture|desks|multiple workstations|repeating workstations|"
    r"repeating work areas|couch|accent chair|plants|soft textiles)\b", re.I
)
SINGULAR_SUPPORT_RE = re.compile(r"\b(?:desk|table|tabletop|work surface|workspace surface|shelf unit)\b", re.I)


def validate_output(output: dict[str, Any], raw_input: dict[str, Any], schema: dict[str, Any],
                    registry: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    def err(code: str, detail: str, candidate_id: str | None = None) -> None:
        item = {"code": code, "detail": detail}
        if candidate_id:
            item["candidate_id"] = candidate_id
        errors.append(item)

    try:
        jsonschema.validate(output, schema)
    except jsonschema.ValidationError as exc:
        err("schema_invalid", f"{'/'.join(map(str, exc.absolute_path))}: {exc.message}")
        return {"validator_version": "v4.1-host-validator-r2", "passed": False,
                "error_count": len(errors), "warning_count": 0,
                "errors": errors, "warnings": [], "output_semantic_sha256": digest_obj(output)}

    prompts = output["prompts"]
    debug = output["debug"]
    source = raw_input["source_messaging"]
    expected_ids = [f"p{i}" for i in range(1, 31)]
    ids = [p["id"] for p in prompts]
    if ids != expected_ids:
        err("candidate_id_order", f"expected p1..p30; got {ids}")
    normalized = [" ".join(p["text"].casefold().split()) for p in prompts]
    if len(set(normalized)) != 30:
        err("duplicate_candidate_text", "candidate texts are not unique after whitespace/case normalization")

    prior_rank = (101, 101)
    env_counts = Counter()
    rel_counts = Counter()
    prompt_by_id = {p["id"]: p for p in prompts}
    for p in prompts:
        pid = p["id"]
        components = p["score_components"]
        total = sum(components.values())
        if total != p["source_relevance_score"]:
            err("score_sum", f"components sum {total}, score is {p['source_relevance_score']}", pid)
        current_rank = (p["ctech_reference_score"], p["source_relevance_score"])
        if current_rank > prior_rank:
            err("score_order", "C-Tech score, then source-relevance tie-breaker, are not descending", pid)
        prior_rank = current_rank
        reference_environment, reference_text = CTECH_REFERENCES[p["ctech_reference_id"]]
        relationship = p["ctech_relationship"]
        ctech_score = p["ctech_reference_score"]
        allowed_band = {
            "exact_reference": range(100, 101),
            "minimal_camera_edit": range(80, 100),
            "close_adaptation": range(70, 80),
            "category_extension": range(60, 70),
        }[relationship]
        if ctech_score not in allowed_band:
            err("ctech_score_band", f"{relationship} cannot use score {ctech_score}", pid)
        if ctech_score < 60:
            err("ctech_too_distant", "V4.1 requires a C-Tech reference score of at least 60", pid)
        if relationship == "exact_reference":
            if p["text"] != reference_text or p["environment"] != reference_environment or p["ctech_changes"]:
                err("ctech_exact_mismatch", "exact_reference must exactly match text/environment and have no changes", pid)
        else:
            if not p["ctech_changes"]:
                err("ctech_changes_empty", "non-exact reference use must list material changes", pid)
        if relationship in {"exact_reference", "minimal_camera_edit", "close_adaptation"} and p["environment"] != reference_environment:
            err("ctech_reference_environment", f"{relationship} must preserve {reference_environment}", pid)
        if relationship == "category_extension" and p["environment"] == reference_environment:
            err("ctech_extension_environment", "category_extension must change the reference environment", pid)
        scene_text = p["text"].casefold()
        if p["environment"] == "Gaming" and any(term in scene_text for term in ("café", "cafe", "coffee shop")):
            err("environment_scene_mismatch", "Gaming scene may not use a café or coffee-shop setting", pid)
        if p["environment"] == "Office" and "home workspace" in scene_text:
            err("environment_scene_mismatch", "Office scene may not retain a home-workspace setting", pid)
        if p["environment"] == "Education" and any(term in scene_text for term in
                ("gaming room", "gaming club", "gaming space", "gaming workspace")):
            err("environment_scene_mismatch", "Education scene may not be a gaming room, club, space, or workspace", pid)
        explanation_text = p["ctech_explanation"].casefold()
        if (p["ctech_reference_id"] in {"CT04", "CT10"}
                and any(term in explanation_text for term in
                        ("simplicity", "low-density", "low density", "clear-surface logic", "clear surface logic"))):
            err("ctech_explanation_density", "object-dense reference cannot be credited with surface simplicity", pid)
        if p["relationship"] == "creative_departure" and p["source_relevance_score"] > 59:
            err("departure_score", "creative_departure exceeds 59", pid)
        if not p["evidence_ids"] and (p["source_relevance_score"] != 0 or any(components.values())):
            err("ungrounded_nonzero_score", "nonzero relevance requires relevant source evidence", pid)
        device_term = prohibited_device_term(p["text"])
        if device_term:
            err("device_term", device_term, pid)
        if CAMERA_RE.search(p["text"]):
            err("camera_term", CAMERA_RE.search(p["text"]).group(0), pid)
        if BLUE_RE.search(p["text"]):
            err("blue_policy_term", "blue", pid)
        unnatural = UNNATURAL_PLACE_RE.search(p["text"])
        if unnatural:
            err("unnatural_place_phrase", unnatural.group(0), pid)
        env_counts[p["environment"]] += 1
        rel_counts[p["relationship"]] += 1

    resolution = resolve_profile(registry, raw_input["camera_tag"])
    profile = resolution["effective_profile"]
    expected_camera = {"requested_tag": raw_input["camera_tag"],
                       "resolved_tag": resolution["resolved_tag"],
                       "device_type": resolution["device_type"],
                       "profile_version": resolution["profile_version"],
                       "resolution": resolution["resolution"], **profile}
    if debug["camera"] != expected_camera:
        err("camera_debug", f"expected {expected_camera!r}; got {debug['camera']!r}")
    for p in prompts:
        sig = p["visual_signature"]
        if len(sig["local_props"]) > profile["max_local_props"]:
            err("local_prop_budget", f"{len(sig['local_props'])}>{profile['max_local_props']}", p["id"])
        if len(sig["background_details"]) > profile["max_background_details"]:
            err("background_budget", f"{len(sig['background_details'])}>{profile['max_background_details']}", p["id"])
        if profile["people_policy"] == "omit" and sig["people"]:
            err("people_policy", "people must be empty for omit profile", p["id"])
        if p["ctech_relationship"] != "category_extension" and sig["people"]:
            err("ctech_people_addition", "October reference reuse may add people only in category extensions", p["id"])
        literal_backgrounds = literal_background_collections(p["text"])
        if len(literal_backgrounds) > profile["max_background_details"]:
            err("literal_background_budget",
                f"{len(literal_backgrounds)}>{profile['max_background_details']}: {sorted(literal_backgrounds)}",
                p["id"])
        if len(literal_backgrounds) > len(sig["background_details"]):
            err("background_signature_undercount",
                f"prose names {sorted(literal_backgrounds)} but signature has {len(sig['background_details'])} entries",
                p["id"])
        if COLLECTION_AS_SURFACE_RE.search(sig["surface"]):
            err("collection_used_as_surface", COLLECTION_AS_SURFACE_RE.search(sig["surface"]).group(0), p["id"])
        if sig["surface"] and not SINGULAR_SUPPORT_RE.search(p["text"]):
            err("surface_not_literal", "signature names a focal surface but prose has no singular desk/table/work surface", p["id"])

    evidence_by_id = {}
    for index, ev in enumerate(debug["source_evidence"], 1):
        if ev["id"] != f"e{index}":
            err("evidence_id_order", f"expected e{index}; got {ev['id']}")
        if ev["id"] in evidence_by_id:
            err("duplicate_evidence_id", ev["id"])
        evidence_by_id[ev["id"]] = ev
        parts = ev["path"].split(".")
        if len(parts) < 2 or parts[0] != ev["message_id"] or parts[-1] not in ALLOWED_TEXT_FIELDS:
            err("evidence_path_scope", f"{ev['id']} invalid path/message: {ev['path']}")
            continue
        if not (KSP_RE.match(parts[0]) or parts[0] == "ValueProposition"):
            err("evidence_message_scope", f"{ev['id']} uses {parts[0]}")
            continue
        try:
            field = _path_value(source, ev["path"])
        except KeyError:
            err("evidence_path_missing", f"{ev['id']} path {ev['path']} does not exist")
            continue
        if not isinstance(field, str) or ev["quote"] not in field:
            err("evidence_quote", f"{ev['id']} quote is not verbatim in {ev['path']}")

    used_evidence = set()
    reverse_prompts = defaultdict(set)
    for p in prompts:
        for eid in p["evidence_ids"]:
            if eid not in evidence_by_id:
                err("unknown_evidence", eid, p["id"])
            else:
                used_evidence.add(eid)
                reverse_prompts[evidence_by_id[eid]["message_id"]].add(p["id"])
    unused_evidence = sorted(set(evidence_by_id) - used_evidence)
    if unused_evidence:
        warnings.append({"code": "unused_source_evidence",
                         "detail": f"Unused evidence may support an omission explanation; inspect: {unused_evidence}"})

    ksps = sorted((k for k in source if KSP_RE.match(k)), key=lambda k: int(k[3:]))
    maps = debug["ksp_mappings"]
    if [m["ksp_id"] for m in maps] != ksps:
        err("ksp_mapping_coverage", f"expected {ksps}; got {[m['ksp_id'] for m in maps]}")

    ignored = debug["ignored_fields"]
    if "_chatSession" in source and "_chatSession" not in ignored:
        err("chat_session_not_ignored", "source has _chatSession but debug does not list it")
    if any(x.startswith("_chatSession.") for x in ignored):
        err("chat_session_nested_ignore", "must list only _chatSession as a whole object")
    for path in ignored:
        try:
            _path_value(source, path)
        except KeyError:
            err("ignored_path_missing", path)

    if not debug["diversity_summary"].strip():
        err("diversity_summary_empty", "diversity_summary must briefly describe material limitations/variety")
    if resolution["resolution"] in ("exact", "alias") and set(env_counts) != set(EXPECTED_ENVIRONMENTS):
        err("environment_coverage", f"known profile bank must use all six V4.1 environments: {dict(env_counts)}")

    warnings.append({"code": "human_scene_review_required",
                     "detail": "Prop/background inventories are model self-reports; inspect candidate prose before selection or image launch."})

    derived_reverse = {}
    for mid in [*ksps, "ValueProposition"]:
        evidence_ids = sorted((eid for eid in used_evidence
                               if evidence_by_id[eid]["message_id"] == mid),
                              key=lambda x: int(x[1:]))
        derived_reverse[mid] = {"evidence_ids": evidence_ids,
                                "prompt_ids": sorted(reverse_prompts[mid], key=lambda x: int(x[1:]))}
    derived_audit = {
        "environment_counts": {k: env_counts[k] for k in EXPECTED_ENVIRONMENTS},
        "relationship_counts": {k: rel_counts[k] for k in ("source_grounded", "source_adjacent", "creative_departure")},
        "ctech_relationship_counts": dict(Counter(p["ctech_relationship"] for p in prompts)),
        "ctech_reference_counts": dict(Counter(p["ctech_reference_id"] for p in prompts)),
        "ctech_score_range": [min(p["ctech_reference_score"] for p in prompts),
                              max(p["ctech_reference_score"] for p in prompts)],
        "distinct_subsettings": len({p["subsetting"].casefold().strip() for p in prompts}),
        "evidence_reverse_mappings": derived_reverse,
    }
    return {"validator_version": "v4.1-host-validator-r2", "passed": not errors,
            "error_count": len(errors), "warning_count": len(warnings),
            "errors": errors, "warnings": warnings, "counts": {"prompts": len(prompts),
            "evidence": len(evidence_by_id), "environments": dict(env_counts),
            "relationships": dict(rel_counts)}, "derived_audit": derived_audit,
            "output_semantic_sha256": digest_obj(output)}


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--schema", type=Path, default=OUTPUT_SCHEMA)
    args = parser.parse_args()
    result = validate_output(json.loads(args.output.read_text()), json.loads(args.input.read_text()),
                             json.loads(args.schema.read_text()), load_registry(VERSION / "camera_profiles.json"))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()

