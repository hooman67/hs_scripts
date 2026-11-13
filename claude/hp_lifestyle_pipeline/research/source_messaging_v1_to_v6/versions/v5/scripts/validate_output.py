#!/usr/bin/env python3
"""Deterministic semantic validator for one V5 dual-source candidate bank.

The validator is intentionally read-only: it reports contract violations and
derives audit summaries, but never repairs model output.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import jsonschema

try:  # Package import in tests; direct import when invoked as a script.
    from .camera_profile_resolver import load_registry, resolve_profile
except ImportError:  # pragma: no cover - exercised by CLI use
    from camera_profile_resolver import load_registry, resolve_profile


HERE = Path(__file__).resolve().parent
VERSION = HERE.parent
OUTPUT_SCHEMA = VERSION / "output.schema.json"
REFERENCE_LIBRARY = VERSION / "reference_library.json"
EXPECTED_ENVIRONMENTS = (
    "Home", "Office", "Education", "Gaming", "Café", "Creative Studio",
)
DOCUMENTS = ("smart_brief", "source_messaging")
COMPONENTS = ("setting", "activity", "materials", "use_context")
CTECH_SCORE_BANDS = {
    "exact_reference": (100, 100),
    "minimal_camera_edit": (80, 99),
    "close_adaptation": (70, 79),
    "category_extension": (60, 69),
}

DEVICE_RE = re.compile(
    r"\b(?:laptops?|printers?|mini\s*pcs?|minipcs?|desktops?|computers?|monitors?|"
    r"hardware|devices?|skus?|phones?|smartphones?|tablets?|screens?|keyboards?|"
    r"hp|elitebooks?|omnibooks?|laserjets?)\b", re.I,
)
CAMERA_RE = re.compile(
    r"\b(?:camera|lens|render(?:ing)?|zoom|aspect ratio|depth of field|bokeh|"
    r"pull back|widen the view)\b", re.I,
)
BLUE_RE = re.compile(r"\bblue\b", re.I)
UNNATURAL_PLACE_RE = re.compile(
    r"\b(?:(?:close|local|tight|compact|small) "
    r"(?:section|patch|area|portion|piece|stretch|slice) of|"
    r"shared department records counter|records counter|paperwork nook|"
    r"policy deployment counter|illustration worktop|teaching[- ]preparation table|"
    r"(?:records?|policy|deployment|paperwork|illustration|workflow|department|"
    r"administration|administrative|output check|queue)\s+"
    r"(?:counter|nook|corner|worktop|surface)|"
    r"(?:teaching[- ]preparation|content review|document review|records?|paperwork|"
    r"workflow|department)\s+(?:desk|table|counter|nook|worktop|surface)|"
    r"workspace feeling|document queue)\b", re.I,
)
KSP_RE = re.compile(r"^KSP[1-9][0-9]*$")
STRING_KSP_HEADING_RE = re.compile(
    r"(?im)^\s*KSP\s*([1-9][0-9]*)\b(?:\s*[-:].*)?$"
)
STRING_KSP_NUMBER_RE = re.compile(
    r"(?im)^\s*KSP\s+NUMBER\s*:\s*\n\s*([1-9][0-9]*)\s*$"
)
OUTPUT_KSP_PREFIX_RE = re.compile(r"^\s*KSP\s*([1-9][0-9]*)\b", re.I)
SURFACE_DESKTOP_RE = re.compile(
    r"\b(?:wooden|wood|walnut|oak|birch|maple|laminate|veneer|painted|satin|"
    r"matte|smooth|white|graphite)\s+desktop\b", re.I,
)
NONCOMPUTING_SCREEN_RE = re.compile(
    r"\b(?:privacy|acoustic|folding|divider)\s+screen\b", re.I,
)
COLLECTION_AS_SURFACE_RE = re.compile(
    r"\b(?:simple furniture|desks|multiple workstations|repeating workstations|"
    r"repeating work areas|couch|accent chair|plants|soft textiles)\b", re.I,
)
SINGULAR_SUPPORT_RE = re.compile(
    r"\b(?:desk|table|tabletop|work surface|workspace surface|shelf unit)\b", re.I,
)

_REFERENCE_DOC = json.loads(REFERENCE_LIBRARY.read_text(encoding="utf-8"))
CTECH_REFERENCES = {
    item["id"]: (item["environment"], item["text"])
    for item in _REFERENCE_DOC["references"]
}


def digest_obj(value: Any) -> str:
    """Hash canonical JSON semantics rather than source formatting."""

    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _numeric_suffix_key(value: str, prefix: str) -> tuple[int, int | str]:
    """Sort conventional IDs numerically and malformed IDs deterministically."""

    suffix = value[len(prefix):] if value.startswith(prefix) else ""
    if suffix.isdigit():
        return (0, int(suffix))
    return (1, value)


def _string_ksp_ids(value: str) -> list[str]:
    """Extract unique anchored KSP numbers from an exported text document."""

    numbers = {
        int(match.group(1))
        for pattern in (STRING_KSP_HEADING_RE, STRING_KSP_NUMBER_RE)
        for match in pattern.finditer(value)
    }
    return [f"KSP{number}" for number in sorted(numbers)]


def _normalized_output_ksp_id(value: str) -> str | None:
    """Normalize labels such as ``KSP 1: Name`` to their KSP-number prefix."""

    match = OUTPUT_KSP_PREFIX_RE.match(value)
    return f"KSP{int(match.group(1))}" if match else None


def _pointer_value(root: Any, pointer: str) -> Any:
    """Resolve an RFC 6901 JSON Pointer relative to *root*."""

    if pointer == "":
        return root
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise KeyError(pointer)
    current = root
    for encoded in pointer[1:].split("/"):
        # RFC 6901 permits only ~0 and ~1 escape sequences.
        if re.search(r"~(?:[^01]|$)", encoded):
            raise KeyError(pointer)
        token = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and token in current:
            current = current[token]
        elif (isinstance(current, list) and token.isdigit()
              and (token == "0" or not token.startswith("0"))):
            index = int(token)
            if index >= len(current):
                raise KeyError(pointer)
            current = current[index]
        else:
            raise KeyError(pointer)
    return current


def prohibited_device_term(text: str) -> str | None:
    """Return a device term, excluding established furniture compounds."""

    allowed_spans = [match.span() for match in SURFACE_DESKTOP_RE.finditer(text)]
    allowed_spans.extend(match.span() for match in NONCOMPUTING_SCREEN_RE.finditer(text))
    for match in DEVICE_RE.finditer(text):
        if any(start <= match.start() and match.end() <= end
               for start, end in allowed_spans):
            continue
        return match.group(0)
    return None


def literal_background_collections(text: str) -> set[str]:
    """Conservatively count named furniture/room collections in prose."""

    lowered = text.casefold()
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
        "furnishings": r"\b(?:(?:layered|office|residential|subtle residential|"
                       r"familiar residential)\s+)?furnishings\b",
        "architectural details": r"\barchitectural details\b",
        "workplace decor": r"\b(?:refined )?workplace d[ée]cor\b",
        "organized displays": r"\borganized displays\b",
        "collectibles": r"\bcollectibles\b",
    }
    hits = {label for label, pattern in tests.items() if re.search(pattern, lowered)}
    if "shelving" in hits and re.search(
        r"\b(?:shelving|shelves)\s+(?:holding|displaying|with)\s+"
        r"(?:a few |small |curated )?collectibles\b", lowered
    ):
        hits.discard("collectibles")
    return hits


def _camera_debug(raw_input: dict[str, Any], registry: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    resolution = resolve_profile(registry, raw_input.get("camera_tag"))
    profile = resolution["effective_profile"]
    expected = {
        "requested_tag": raw_input.get("camera_tag", ""),
        "resolved_tag": resolution["resolved_tag"],
        "device_type": resolution["device_type"],
        "profile_version": resolution["profile_version"],
        "resolution": resolution["resolution"],
        **profile,
    }
    return expected, profile


def validate_output(
    output: dict[str, Any],
    raw_input: dict[str, Any],
    schema: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    """Validate one V5 response and return a stable machine-readable report."""

    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    def err(code: str, detail: str, candidate_id: str | None = None) -> None:
        item: dict[str, Any] = {"code": code, "detail": detail}
        if candidate_id is not None:
            item["candidate_id"] = candidate_id
        errors.append(item)

    try:
        jsonschema.validate(output, schema)
    except jsonschema.ValidationError as exc:
        err("schema_invalid", f"{'/'.join(map(str, exc.absolute_path))}: {exc.message}")
        return {
            "validator_version": "v5-host-validator-r3",
            "passed": False,
            "error_count": len(errors),
            "warning_count": 0,
            "errors": errors,
            "warnings": [],
            "output_semantic_sha256": digest_obj(output),
        }

    prompts = output["prompts"]
    debug = output["debug"]
    expected_ids = [f"p{i}" for i in range(1, 21)]
    ids = [candidate["id"] for candidate in prompts]
    if ids != expected_ids:
        err("candidate_id_order", f"expected p1..p20; got {ids}")

    normalized_texts = [
        " ".join(candidate["text"].casefold().split()) for candidate in prompts
    ]
    if len(set(normalized_texts)) != 20:
        err("duplicate_candidate_text", "candidate texts are not unique after whitespace/case normalization")

    evidence_by_id: dict[str, dict[str, Any]] = {}
    for index, evidence in enumerate(debug["source_evidence"], 1):
        evidence_id = evidence["id"]
        if evidence_id != f"e{index}":
            err("evidence_id_order", f"expected e{index}; got {evidence_id}")
        if evidence_id in evidence_by_id:
            err("duplicate_evidence_id", evidence_id)
        evidence_by_id[evidence_id] = evidence
        document = evidence["document"]
        pointer = evidence["path"]
        document_value = raw_input[document]
        if isinstance(document_value, str) and pointer != "":
            err("evidence_path_scope", f"{evidence_id} string document requires empty path")
            continue
        if not isinstance(document_value, str) and pointer == "":
            err("evidence_path_scope", f"{evidence_id} object document requires an RFC 6901 path")
            continue
        try:
            field = _pointer_value(document_value, pointer)
        except KeyError:
            err("evidence_path_missing", f"{evidence_id} path {pointer!r} does not exist in {document}")
            continue
        quote = evidence["quote"]
        if not quote:
            err("evidence_quote_empty", f"{evidence_id} quote must be nonempty")
        elif not isinstance(field, str) or quote not in field:
            err("evidence_quote", f"{evidence_id} quote is not verbatim in {document}{pointer}")

    used_evidence: set[str] = set()
    evidence_prompt_ids: dict[str, set[str]] = defaultdict(set)
    env_counts: Counter[str] = Counter()
    rel_counts: Counter[str] = Counter()
    prior_rank = (float("inf"), float("inf"))

    for candidate in prompts:
        candidate_id = candidate["id"]
        evidence_ids = candidate["evidence_ids"]
        if len(evidence_ids) != len(set(evidence_ids)):
            err("duplicate_candidate_evidence", "candidate evidence_ids contain duplicates", candidate_id)
        cited_documents: set[str] = set()
        for evidence_id in evidence_ids:
            evidence = evidence_by_id.get(evidence_id)
            if evidence is None:
                err("unknown_evidence", evidence_id, candidate_id)
            else:
                used_evidence.add(evidence_id)
                cited_documents.add(evidence["document"])
                evidence_prompt_ids[evidence_id].add(candidate_id)

        for document in DOCUMENTS:
            group = candidate["score_components"][document]
            if document not in cited_documents and any(group.values()):
                err(
                    "ungrounded_document_components",
                    f"{document} components must be zero without candidate evidence from that document",
                    candidate_id,
                )
        expected_score = sum(
            max(
                candidate["score_components"]["smart_brief"][name],
                candidate["score_components"]["source_messaging"][name],
            )
            for name in COMPONENTS
        )
        if candidate["source_relevance_score"] != expected_score:
            err(
                "score_component_max_sum",
                (
                    "sum of per-component document maxima is "
                    f"{expected_score:g}, score is {candidate['source_relevance_score']}"
                ),
                candidate_id,
            )
        current_rank = (
            candidate["source_relevance_score"], candidate["ctech_reference_score"]
        )
        if current_rank > prior_rank:
            err(
                "score_order",
                "source relevance, then C-Tech tie-breaker, are not descending",
                candidate_id,
            )
        prior_rank = current_rank

        reference_environment, reference_text = CTECH_REFERENCES[candidate["ctech_reference_id"]]
        relationship = candidate["ctech_relationship"]
        ctech_score = candidate["ctech_reference_score"]
        low, high = CTECH_SCORE_BANDS[relationship]
        if not low <= ctech_score <= high:
            err("ctech_score_band", f"{relationship} cannot use score {ctech_score}", candidate_id)
        if relationship == "exact_reference":
            if (candidate["text"] != reference_text
                    or candidate["environment"] != reference_environment
                    or candidate["ctech_changes"]):
                err(
                    "ctech_exact_mismatch",
                    "exact_reference must exactly match text/environment and have no changes",
                    candidate_id,
                )
        elif not candidate["ctech_changes"]:
            err("ctech_changes_empty", "non-exact reference use must list material changes", candidate_id)
        if (relationship in {"exact_reference", "minimal_camera_edit", "close_adaptation"}
                and candidate["environment"] != reference_environment):
            err(
                "ctech_reference_environment",
                f"{relationship} must preserve {reference_environment}",
                candidate_id,
            )
        if relationship == "category_extension" and candidate["environment"] == reference_environment:
            err(
                "ctech_extension_environment",
                "category_extension must change the reference environment",
                candidate_id,
            )

        scene_text = candidate["text"].casefold()
        if candidate["environment"] == "Gaming" and any(
            term in scene_text for term in ("café", "cafe", "coffee shop")
        ):
            err("environment_scene_mismatch", "Gaming scene may not use a café setting", candidate_id)
        if candidate["environment"] == "Office" and "home workspace" in scene_text:
            err("environment_scene_mismatch", "Office scene may not retain a home workspace", candidate_id)
        if candidate["environment"] == "Education" and any(
            term in scene_text
            for term in ("gaming room", "gaming club", "gaming space", "gaming workspace")
        ):
            err("environment_scene_mismatch", "Education scene may not use a gaming setting", candidate_id)
        explanation_text = candidate["ctech_explanation"].casefold()
        if (candidate["ctech_reference_id"] in {"CT04", "CT10"}
                and any(term in explanation_text for term in (
                    "simplicity", "low-density", "low density",
                    "clear-surface logic", "clear surface logic",
                ))):
            err(
                "ctech_explanation_density",
                "object-dense reference cannot be credited with surface simplicity",
                candidate_id,
            )
        if candidate["relationship"] == "creative_departure" and candidate["source_relevance_score"] > 59:
            err("departure_score", "creative_departure exceeds 59", candidate_id)

        device_term = prohibited_device_term(candidate["text"])
        if device_term:
            err("device_term", device_term, candidate_id)
        camera_match = CAMERA_RE.search(candidate["text"])
        if camera_match:
            err("camera_term", camera_match.group(0), candidate_id)
        if BLUE_RE.search(candidate["text"]):
            err("blue_policy_term", "blue", candidate_id)
        unnatural_match = UNNATURAL_PLACE_RE.search(candidate["text"])
        if unnatural_match:
            err("unnatural_place_phrase", unnatural_match.group(0), candidate_id)

        env_counts[candidate["environment"]] += 1
        rel_counts[candidate["relationship"]] += 1

    expected_camera, profile = _camera_debug(raw_input, registry)
    if debug["camera"] != expected_camera:
        err("camera_debug", f"expected {expected_camera!r}; got {debug['camera']!r}")
    for candidate in prompts:
        candidate_id = candidate["id"]
        signature = candidate["visual_signature"]
        if len(signature["local_props"]) > profile["max_local_props"]:
            err(
                "local_prop_budget",
                f"{len(signature['local_props'])}>{profile['max_local_props']}",
                candidate_id,
            )
        if len(signature["background_details"]) > profile["max_background_details"]:
            err(
                "background_budget",
                f"{len(signature['background_details'])}>{profile['max_background_details']}",
                candidate_id,
            )
        if profile["people_policy"] == "omit" and signature["people"]:
            err("people_policy", "people must be empty for omit profile", candidate_id)
        if candidate["ctech_relationship"] != "category_extension" and signature["people"]:
            err(
                "ctech_people_addition",
                "reference reuse may add people only in category extensions",
                candidate_id,
            )
        literal_backgrounds = literal_background_collections(candidate["text"])
        if len(literal_backgrounds) > profile["max_background_details"]:
            err(
                "literal_background_budget",
                f"{len(literal_backgrounds)}>{profile['max_background_details']}: "
                f"{sorted(literal_backgrounds)}",
                candidate_id,
            )
        if len(literal_backgrounds) > len(signature["background_details"]):
            err(
                "background_signature_undercount",
                f"prose names {sorted(literal_backgrounds)} but signature has "
                f"{len(signature['background_details'])} entries",
                candidate_id,
            )
        surface_collection = COLLECTION_AS_SURFACE_RE.search(signature["surface"])
        if surface_collection:
            err("collection_used_as_surface", surface_collection.group(0), candidate_id)
        if signature["surface"] and not SINGULAR_SUPPORT_RE.search(candidate["text"]):
            err(
                "surface_not_literal",
                "signature names a focal surface but prose has no singular desk/table/work surface",
                candidate_id,
            )

    source_messaging = raw_input["source_messaging"]
    maps = debug["ksp_mappings"]
    if isinstance(source_messaging, dict):
        expected_ksps = sorted(
            (key for key in source_messaging if KSP_RE.match(key)),
            key=lambda key: int(key[3:]),
        )
        observed_ksps = [mapping["ksp_id"] for mapping in maps]
        ambiguous_labels: list[str] = []
    else:
        expected_ksps = _string_ksp_ids(source_messaging)
        observed_ksps = []
        ambiguous_labels = []
        for mapping in maps:
            normalized_id = _normalized_output_ksp_id(mapping["ksp_id"])
            if normalized_id is None:
                ambiguous_labels.append(mapping["ksp_id"])
            else:
                observed_ksps.append(normalized_id)
        if ambiguous_labels:
            warnings.append({
                "code": "ambiguous_ksp_mapping_id",
                "detail": (
                    "Could not normalize KSP-number prefixes from string-input mappings: "
                    f"{ambiguous_labels}"
                ),
            })
    if ambiguous_labels:
        coverage_impossible = (
            (bool(expected_ksps) and len(maps) != len(expected_ksps))
            or len(observed_ksps) != len(set(observed_ksps))
            or any(ksp_id not in expected_ksps for ksp_id in observed_ksps)
        )
    else:
        coverage_impossible = observed_ksps != expected_ksps
    if coverage_impossible:
        err(
            "ksp_mapping_coverage",
            f"expected normalized {expected_ksps}; got {observed_ksps}",
        )

    ignored = debug["ignored_fields"]
    for index, description in enumerate(ignored, 1):
        if not description.strip():
            err("ignored_field_empty", f"ignored_fields entry {index} must be nonempty")

    assessments = [item["document"] for item in debug["document_assessments"]]
    if Counter(assessments) != Counter(DOCUMENTS):
        err("document_assessment_coverage", f"expected one assessment per document; got {assessments}")

    for index, conflict in enumerate(debug["source_conflicts"], 1):
        if len(conflict["evidence_ids"]) != len(set(conflict["evidence_ids"])):
            err("source_conflict_duplicate_evidence", f"conflict {index} repeats evidence IDs")
        unknown = [eid for eid in conflict["evidence_ids"] if eid not in evidence_by_id]
        if unknown:
            err("source_conflict_unknown_evidence", f"conflict {index} uses {unknown}")
        known_evidence = {
            eid
            for eid in conflict["evidence_ids"]
            if eid in evidence_by_id
        }
        used_evidence.update(known_evidence)
        if not known_evidence:
            err("source_conflict_evidence_missing", f"conflict {index} has no valid evidence")

    unused_evidence = sorted(
        set(evidence_by_id) - used_evidence,
        key=lambda value: _numeric_suffix_key(value, "e"),
    )
    if unused_evidence:
        warnings.append({
            "code": "unused_source_evidence",
            "detail": f"Unused evidence may support audit text; inspect: {unused_evidence}",
        })

    if not debug["diversity_summary"].strip():
        err("diversity_summary_empty", "diversity_summary must describe material limitations/variety")
    if expected_camera["resolution"] in {"exact", "alias"} and set(env_counts) != set(EXPECTED_ENVIRONMENTS):
        err(
            "environment_coverage",
            f"known profile bank must use all six V5 environments: {dict(env_counts)}",
        )

    warnings.append({
        "code": "human_scene_review_required",
        "detail": "Prop/background inventories and semantic grounding remain model self-reports; inspect prose before image launch.",
    })

    reverse_by_document: dict[str, dict[str, list[str]]] = {}
    for document in DOCUMENTS:
        document_ids = [
            eid for eid in used_evidence if evidence_by_id[eid]["document"] == document
        ]
        document_ids.sort(key=lambda value: _numeric_suffix_key(value, "e"))
        prompt_ids = sorted(
            {pid for eid in document_ids for pid in evidence_prompt_ids[eid]},
            key=lambda value: _numeric_suffix_key(value, "p"),
        )
        reverse_by_document[document] = {
            "evidence_ids": document_ids,
            "prompt_ids": prompt_ids,
        }
    derived_audit = {
        "environment_counts": {name: env_counts[name] for name in EXPECTED_ENVIRONMENTS},
        "relationship_counts": {
            name: rel_counts[name]
            for name in ("source_grounded", "source_adjacent", "creative_departure")
        },
        "ctech_relationship_counts": dict(Counter(
            candidate["ctech_relationship"] for candidate in prompts
        )),
        "ctech_reference_counts": dict(Counter(
            candidate["ctech_reference_id"] for candidate in prompts
        )),
        "ctech_score_range": [
            min(candidate["ctech_reference_score"] for candidate in prompts),
            max(candidate["ctech_reference_score"] for candidate in prompts),
        ],
        "distinct_subsettings": len({
            candidate["subsetting"].casefold().strip() for candidate in prompts
        }),
        "evidence_reverse_mappings": reverse_by_document,
    }
    return {
        "validator_version": "v5-host-validator-r3",
        "passed": not errors,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "prompts": len(prompts),
            "evidence": len(evidence_by_id),
            "environments": dict(env_counts),
            "relationships": dict(rel_counts),
        },
        "derived_audit": derived_audit,
        "output_semantic_sha256": digest_obj(output),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--schema", type=Path, default=OUTPUT_SCHEMA)
    parser.add_argument("--registry", type=Path, default=VERSION / "camera_profiles.json")
    args = parser.parse_args()
    result = validate_output(
        json.loads(args.output.read_text(encoding="utf-8")),
        json.loads(args.input.read_text(encoding="utf-8")),
        json.loads(args.schema.read_text(encoding="utf-8")),
        load_registry(args.registry),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
