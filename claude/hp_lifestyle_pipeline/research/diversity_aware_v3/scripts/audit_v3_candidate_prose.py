#!/usr/bin/env python3
"""Mechanically audit V3 candidate prose independently of model inventories.

This is a conservative lexical audit, not a semantic quality model. It reads
the actual final prose, extracts explicit prop/background/people terms, checks
device and camera language, compares the extraction with visual_signature, and
flags rows for human review. A visible person or partial activity consumes one
local-prop slot, matching the V2 replacement rule.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
EVAL_ROOT = PROJECT_ROOT / "eval_sets/hp_lifestyle_diversity_v3_eval_20261023"
MANIFEST_PATH = EVAL_ROOT / "manifest.json"
ACCEPTED_PATH = EVAL_ROOT / "accepted_prompt_cases.json"
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "research/diversity_aware_v3/data/v3_camera_prose_review.json"
)

DEVICE_RE = re.compile(
    r"\b(?:hp|laptops?|printers?|mini\s*pcs?|minipcs?|computers?|"
    r"monitors?|hardware|devices?|skus?|phones?|smartphones?|tablets?|"
    r"keyboards?|elitebooks?|omnibooks?|laserjets?|ports?)\b",
    re.I,
)
CAMERA_RE = re.compile(
    r"\b(?:camera|lens|render(?:ing)?|zoom|aspect\s+ratio|depth\s+of\s+field|"
    r"bokeh|pull\s+back|widen\s+the\s+view|viewpoint|perspective|"
    r"overhead\s+(?:view|shot|angle|camera|perspective)|"
    r"top[- ]down|close[- ]up|wide[- ]angle|front\s+view|rear\s+view|"
    r"back\s+view|left[- ]side\s+view|right[- ]side\s+view|from\s+above)\b",
    re.I,
)

# Longest phrases should appear first; overlapping matches are collapsed.
PROP_PATTERNS = (
    ("document_packet", r"\b(?:compact\s+)?(?:packet|bundle)\s+of\s+(?:recurring\s+)?(?:forms?|reports?|documents?)(?:\s+and\s+(?:forms?|reports?|documents?))?\b"),
    ("document_folder", r"\bfolders?\s+of\s+(?:practice\s+)?(?:forms?|records?|documents?)\b"),
    ("document_folder", r"\b(?:forms?|records?|documents?)\s+folders?\b"),
    ("paper_stack", r"\b(?:compact\s+)?(?:stack|bundle)\s+of\s+(?:papers?|forms?|worksheets?)\b"),
    ("material_samples", r"\b(?:loose\s+)?material\s+samples?\b"),
    ("paper_samples", r"\bpaper\s+samples?\b"),
    ("sticky_notes", r"\bsticky\s+notes?\b"),
    ("game_controller", r"\b(?:game|gaming)\s+controllers?\b|\bcontrollers?\b"),
    ("framed_photo", r"\bframed\s+photos?\b"),
    # Bare "paper" is often context (paper supply point/edge/background). Keep
    # concrete paper objects and forms while avoiding those contextual uses.
    ("papers", r"\b(?:loose|construction|blank)\s+papers?\b|\bforms?\b"),
    ("notebook", r"\bpaper\s+notebooks?\b|\bnotebooks?\b"),
    ("planner", r"\bplanners?\b"),
    ("worksheet", r"\bworksheets?\b|\bhandouts?\b"),
    ("sketchbook", r"\bsketchbooks?\b"),
    ("pen", r"\bpens?\b"),
    ("pencil", r"\bpencils?\b"),
    ("cup", r"\b(?:ceramic\s+)?cups?\b|\bmugs?\b"),
    ("plant", r"\b(?:potted\s+|small\s+)?plants?\b|\bsucculents?\b"),
    ("headphones", r"\bheadphones?\b|\bheadsets?\b"),
    ("book", r"\bbooks?\b(?!\s+(?:cart|bin|shelf|case))"),
    ("folder", r"\bfolders?\b"),
    ("envelope", r"\benvelopes?\b"),
    ("clipboard", r"\bclipboards?\b"),
    ("calendar", r"\bcalendars?\b"),
    ("lamp", r"\b(?:desk\s+)?lamps?\b(?!\s+(?:glow|light|lighting))"),
    ("scissors", r"\bscissors\b"),
    ("ruler", r"\brulers?\b"),
    ("photo", r"\bphotos?\b|\bphotographs?\b"),
    ("vase", r"\bvases?\b"),
    ("bowl", r"\bbowls?\b"),
    ("keys", r"(?<!-)\bkeys?\b(?!-)"),
    ("glasses", r"\b(?:eye)?glasses\b|\bspectacles\b"),
)

BACKGROUND_PATTERNS = (
    ("framed_art", r"\bframed\s+(?:art|artwork|print|poster)s?\b"),
    ("wall_art", r"\bwall\s+(?:art|artwork|print|poster)s?\b"),
    ("bulletin_board", r"\bbulletin\s+boards?\b|\bpinboards?\b|\bpegboards?\b"),
    ("shelving", r"\b(?:section\s+of\s+)?shelving\b|\bshelves?\b|\bbookcases?\b"),
    ("window", r"\bwindows?\b"),
    ("curtain", r"\bcurtains?\b|\bdrapes?\b"),
    ("chair", r"\bchairs?\b"),
    ("cabinet", r"\bcabinets?\b"),
    ("artwork", r"\bartwork\b|\bposters?\b"),
    ("stool", r"\bstools?\b"),
    ("rug", r"\brugs?\b"),
    ("sofa", r"\bsofas?\b|\bcouches?\b"),
    ("wall_clock", r"\bwall\s+clocks?\b"),
)

PEOPLE_PATTERNS = (
    ("hand", r"\b(?:cropped|partial|visible)?\s*hands?\b(?![-‑–])"),
    ("sleeve", r"\b(?:cropped|partial|visible)\s+sleeves?\b"),
    ("person", r"\bpersons?\b|\bpeople\b|\bsomeone\b"),
    # Role nouns frequently modify a surface or document ("teacher desk",
    # "client forms", "family command center"). Require visible activity.
    (
        "active_person",
        r"\b(?:a|an|one|the)\s+(?:worker|colleague|staff\s+member|student|pupil|"
        r"learner|teacher|instructor|educator|designer|artist|maker|gamer|player|"
        r"customer|client|parent|child|adult)\s+(?:reaches|sorts|reviews|writes|"
        r"uses|stands|sits|works|holds|places|arranges)\b",
    ),
)

QUANTITY_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def extract_nonoverlapping(text: str, patterns: tuple[tuple[str, str], ...]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    occupied: list[tuple[int, int]] = []
    for label, pattern in patterns:
        for found in re.finditer(pattern, text, re.I):
            span = found.span()
            if any(span[0] < old[1] and old[0] < span[1] for old in occupied):
                continue
            occupied.append(span)
            prefix = text[max(0, span[0] - 16) : span[0]]
            quantity_match = re.search(
                r"\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+$",
                prefix,
                re.I,
            )
            quantity = 1
            if quantity_match:
                raw_quantity = quantity_match.group(1).casefold()
                quantity = QUANTITY_WORDS.get(raw_quantity, int(raw_quantity) if raw_quantity.isdigit() else 1)
            matches.append(
                {
                    "label": label,
                    "text": found.group(0),
                    "quantity": quantity,
                    "start": span[0],
                    "end": span[1],
                }
            )
    return sorted(matches, key=lambda value: value["start"])


def normalized_words(value: str) -> set[str]:
    words = set(re.findall(r"[a-z]+", value.casefold()))
    normalized = set()
    for word in words:
        if word == "tabbed":
            word = "tab"
        elif word == "batches":
            word = "batch"
        if word.endswith("ies") and len(word) > 4:
            word = word[:-3] + "y"
        elif word.endswith("s") and len(word) > 3 and not word.endswith("ss"):
            word = word[:-1]
        normalized.add(word)
    return normalized


def inventory_item_supported_by_text(item: str, text: str) -> bool:
    item_words = normalized_words(item) - {
        "a", "an", "the", "one", "two", "three", "small", "simple",
        "single", "short", "slim", "partial", "cropped", "open", "opened",
        "folded", "capped", "labeled", "marked", "adjusting", "straightening",
    }
    text_words = normalized_words(text)
    return bool(item_words) and item_words <= text_words


def extracted_item_reported(match: dict[str, Any], inventory: list[str]) -> bool:
    match_words = normalized_words(match["text"])
    return any(bool(match_words & normalized_words(item)) for item in inventory)


def inventory_unit_count(inventory: list[str]) -> int:
    total = 0
    for item in inventory:
        match = re.match(
            r"\s*(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\b",
            item,
            re.I,
        )
        if not match:
            total += 1
            continue
        raw_quantity = match.group(1).casefold()
        total += QUANTITY_WORDS.get(raw_quantity, int(raw_quantity) if raw_quantity.isdigit() else 1)
    return total


def remove_lighting_context_backgrounds(
    text: str, matches: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Do not turn a light-source adjective into a physical background item."""
    kept = []
    for match in matches:
        if match["label"] not in {"window", "curtain", "cabinet"}:
            kept.append(match)
            continue
        suffix = text[match["end"] : match["end"] + 24]
        if re.match(
            r"(?:[- ](?:like|filtered|softened))?[- ]*(?:daylight|light|lighting|glow|illumination)\b",
            suffix,
            re.I,
        ):
            continue
        kept.append(match)
    return kept


def remove_setting_label_props(
    text: str, matches: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Exclude nouns used to name a setting rather than a visible object."""
    kept = []
    for match in matches:
        suffix = text[match["end"] : match["end"] + 40]
        if re.match(
            r"(?:\s+[a-z'-]+){0,2}\s+(?:workstation|surface|table|desk|counter|"
            r"nook|station|area|point)\b",
            suffix,
            re.I,
        ):
            continue
        kept.append(match)
    return kept


def issue(code: str, detail: str, severity: str = "error") -> dict[str, str]:
    return {"code": code, "severity": severity, "detail": detail}


def camera_instruction_match(text: str) -> re.Match[str] | None:
    """Return camera language, excluding explicit illumination direction."""
    for match in CAMERA_RE.finditer(text):
        if match.group(0).casefold() == "from above":
            prefix = text[max(0, match.start() - 28) : match.start()]
            if re.search(r"(?:illuminat\w*|lit|light(?:ed|ing)?)\s*$", prefix, re.I):
                continue
        return match
    return None


def lexical_resolution_evidence(text: str) -> list[dict[str, Any]]:
    """Record context-sensitive terms considered and cleared during triage."""
    rules = (
        (
            "light_source_phrase_is_not_physical_background",
            r"\b(?:window|curtain)(?:[- ](?:like|filtered|softened))?[- ]*"
            r"(?:daylight|light|lighting|glow|illumination)\b",
        ),
        (
            "illumination_from_above_is_not_camera_angle",
            r"\b(?:illuminat\w*|lit|light(?:ed|ing)?)\s+from\s+above\b",
        ),
        (
            "hand_drawn_is_adjective_not_visible_person",
            r"\bhand[-‑–]drawn\b",
        ),
        (
            "role_noun_modifies_setting_or_material_not_visible_person",
            r"\b(?:teacher|student|client|customer|family)\s+"
            r"(?:planning\s+)?(?:desk|table|counter|surface|workstation|forms?|"
            r"records?|command\s+center|project\s+table)\b",
        ),
        (
            "material_noun_names_setting_not_additional_prop",
            r"\b(?:forms?|handouts?|worksheets?|papers?)(?:\s+[a-z'-]+){0,2}\s+"
            r"(?:workstation|surface|table|desk|counter|nook|station|area|point)\b",
        ),
        (
            "compound_document_folder_is_one_prop",
            r"\b(?:forms?|records?|documents?)\s+folders?\b",
        ),
    )
    evidence = []
    for rule, pattern in rules:
        for match in re.finditer(pattern, text, re.I):
            evidence.append(
                {
                    "rule": rule,
                    "decision": "harmless_context_nonissue",
                    "evidence": match.group(0),
                }
            )
    return evidence


def audit_candidate(candidate: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    text = candidate["text"]
    signature = candidate["visual_signature"]
    props = remove_setting_label_props(
        text, extract_nonoverlapping(text, PROP_PATTERNS)
    )
    backgrounds = remove_lighting_context_backgrounds(
        text, extract_nonoverlapping(text, BACKGROUND_PATTERNS)
    )
    people = extract_nonoverlapping(text, PEOPLE_PATTERNS)
    # Lexical type alone cannot decide depth. Honor an explicitly disclosed
    # opposite inventory when the text and self report agree on the object
    # (for example, "blank paper" in a background tray or a wall calendar).
    props = [
        match for match in props
        if not (
            extracted_item_reported(match, signature["background_details"])
            and not extracted_item_reported(match, signature["local_props"])
        )
    ]
    backgrounds = [
        match for match in backgrounds
        if not (
            extracted_item_reported(match, signature["local_props"])
            and not extracted_item_reported(match, signature["background_details"])
        )
    ]
    findings: list[dict[str, str]] = []
    device_match = DEVICE_RE.search(text)
    camera_match = camera_instruction_match(text)
    if device_match:
        findings.append(issue("device_term_in_actual_text", device_match.group(0)))
    if camera_match:
        findings.append(issue("camera_or_angle_term_in_actual_text", camera_match.group(0)))

    for field_name, inventory in (
        ("local_props", signature["local_props"]),
        ("background_details", signature["background_details"]),
        ("people", signature["people"]),
    ):
        unsupported = [item for item in inventory if not inventory_item_supported_by_text(item, text)]
        if field_name == "people" and people:
            unsupported = [
                item for item in unsupported
                if not any(extracted_item_reported(match, [item]) for match in people)
            ]
        if unsupported:
            findings.append(
                issue(
                    f"self_report_not_supported_by_actual_text_{field_name}",
                    repr(unsupported),
                    "warning",
                )
            )

    # Classification between prop/background is conservative. A calendar or
    # book cart reported in either inventory is still disclosed, so it is not
    # an inventory omission even if the lexical class differs.
    disclosed_objects = [
        *signature["local_props"],
        *signature["background_details"],
    ]
    unreported_props = [
        match["text"] for match in props
        if not extracted_item_reported(match, disclosed_objects)
    ]
    unreported_backgrounds = [
        match["text"] for match in backgrounds
        if not extracted_item_reported(match, disclosed_objects)
    ]
    unreported_people = [match["text"] for match in people if not extracted_item_reported(match, signature["people"])]
    if unreported_props:
        findings.append(issue("actual_text_prop_missing_from_self_report", repr(unreported_props)))
    if unreported_backgrounds:
        findings.append(issue("actual_text_background_missing_from_self_report", repr(unreported_backgrounds)))
    if unreported_people:
        findings.append(issue("actual_text_people_missing_from_self_report", repr(unreported_people)))

    actual_prop_floor = sum(match["quantity"] for match in props)
    actual_background_floor = sum(match["quantity"] for match in backgrounds)
    people_present = bool(people)
    reported_prop_units = inventory_unit_count(signature["local_props"])
    reported_background_units = inventory_unit_count(signature["background_details"])
    effective_prop_count = max(actual_prop_floor, reported_prop_units)
    effective_background_count = max(actual_background_floor, reported_background_units)
    people_slot = 1 if people_present else 0
    if reported_prop_units > len(signature["local_props"]):
        findings.append(
            issue(
                "self_report_list_length_undercounts_prop_units",
                f"list_items={len(signature['local_props'])}, counted_units={reported_prop_units}",
                "warning",
            )
        )
    if effective_prop_count > profile["max_local_props"]:
        findings.append(
            issue(
                "actual_or_reported_prop_budget_exceeded",
                f"count={effective_prop_count} max={profile['max_local_props']}",
            )
        )
    if effective_background_count > profile["max_background_details"]:
        findings.append(
            issue(
                "actual_or_reported_background_budget_exceeded",
                f"count={effective_background_count} max={profile['max_background_details']}",
            )
        )
    if people_present and profile["people_policy"] == "omit":
        findings.append(issue("actual_text_people_violate_omit_policy", repr([m["text"] for m in people])))
    if people_slot and effective_prop_count + people_slot > profile["max_local_props"]:
        findings.append(
            issue(
                "people_activity_does_not_replace_a_prop",
                f"explicit_prop_count={effective_prop_count}, people_slot=1, max_local_props={profile['max_local_props']}",
            )
        )

    return {
        "candidate_id": candidate["id"],
        "candidate_key": candidate.get("candidate_key"),
        "rank": candidate.get("rank"),
        "text": text,
        "text_sha256": candidate.get("text_sha256") or hashlib.sha256(text.encode()).hexdigest(),
        "profile": profile,
        "self_report": signature,
        "actual_text_extraction": {
            "props": props,
            "background_details": backgrounds,
            "people": people,
            "device_term": device_match.group(0) if device_match else None,
            "camera_or_angle_term": camera_match.group(0) if camera_match else None,
            "actual_prop_floor": actual_prop_floor,
            "actual_background_floor": actual_background_floor,
            "reported_prop_units": reported_prop_units,
            "reported_background_units": reported_background_units,
            "people_slot": people_slot,
            "effective_prop_count": effective_prop_count,
            "effective_prop_plus_people_count": effective_prop_count + people_slot,
            "effective_background_count": effective_background_count,
        },
        "findings": findings,
        "requires_human_review": bool(findings),
    }


def build_audit(
    manifest: dict[str, Any],
    accepted: dict[str, Any],
    allow_partial: bool,
    manifest_path: Path = MANIFEST_PATH,
    accepted_path: Path = ACCEPTED_PATH,
) -> dict[str, Any]:
    cases = {case["case_id"]: case for case in manifest["cases"]}
    accepted_cases = accepted.get("cases", {})
    if not allow_partial and (
        len(accepted_cases) != 18
        or accepted.get("counts", {}).get("candidates") != 540
    ):
        raise ValueError("Final prose audit requires complete 18-case/540-candidate accepted bank")
    case_reviews = []
    rows = []
    for case_id in sorted(accepted_cases):
        if case_id not in cases:
            raise ValueError(f"Accepted map contains unknown case: {case_id}")
        case = cases[case_id]
        bank = accepted_cases[case_id]
        if len(bank.get("candidates", [])) != 30:
            raise ValueError(f"Accepted case is incomplete: {case_id}")
        profile = case["expected_camera"]
        raw_record_path = Path(bank["record_path"])
        normalized_path = Path(bank["normalized_output_path"])
        normalization_log_path = Path(bank["normalization_log_path"])
        validation_audit_path = Path(bank["validation_audit_path"])
        expected_file_hashes = (
            (raw_record_path, bank["record_sha256"], "raw record"),
            (normalized_path, bank["normalized_output_file_sha256"], "normalized output"),
            (normalization_log_path, bank["normalization_log_file_sha256"], "normalization log"),
        )
        for path, expected_hash, label in expected_file_hashes:
            if not path.is_file() or sha256_path(path) != expected_hash:
                raise ValueError(f"{label} hash mismatch for {case_id}: {path}")
        if not validation_audit_path.is_file():
            raise FileNotFoundError(validation_audit_path)
        raw_record = json.loads(raw_record_path.read_text(encoding="utf-8"))
        raw_output = raw_record["parsed_output"]
        normalized_output = json.loads(normalized_path.read_text(encoding="utf-8"))
        normalization_log = json.loads(normalization_log_path.read_text(encoding="utf-8"))
        if canonical_sha256(raw_output) != bank["raw_parsed_output_sha256"]:
            raise ValueError(f"Raw parsed semantic hash mismatch: {case_id}")
        if canonical_sha256(normalized_output) != bank["normalized_output_semantic_sha256"]:
            raise ValueError(f"Normalized semantic hash mismatch: {case_id}")
        if normalization_log["raw_output_semantic_sha256"] != bank["raw_parsed_output_sha256"]:
            raise ValueError(f"Normalization log raw hash mismatch: {case_id}")
        if normalization_log["normalized_output_semantic_sha256"] != bank["normalized_output_semantic_sha256"]:
            raise ValueError(f"Normalization log normalized hash mismatch: {case_id}")

        raw_by_id = {candidate["id"]: candidate for candidate in raw_output["prompts"]}
        normalized_by_id = {candidate["id"]: candidate for candidate in normalized_output["prompts"]}
        accepted_by_id = {candidate["id"]: candidate for candidate in bank["candidates"]}
        id_map = {
            item["normalized_id"]: item["original_id"]
            for item in normalization_log["id_map"]
        }
        if set(id_map) != set(normalized_by_id) or set(id_map.values()) != set(raw_by_id):
            raise ValueError(f"Normalization ID map is not bijective: {case_id}")

        candidate_reviews = []
        for rank, normalized_candidate in enumerate(normalized_output["prompts"], 1):
            normalized_id = normalized_candidate["id"]
            original_id = id_map[normalized_id]
            raw_candidate = raw_by_id[original_id]
            accepted_candidate = accepted_by_id[normalized_id]
            expected_candidate_key = f"{case_id}::{normalized_id}"
            expected_enriched = {
                "candidate_key": expected_candidate_key,
                "rank": rank,
                "rank_bin": "1-10" if rank <= 10 else "11-20" if rank <= 20 else "21-30",
                "text_sha256": hashlib.sha256(normalized_candidate["text"].encode()).hexdigest(),
                **normalized_candidate,
            }
            projection_matches = accepted_candidate == expected_enriched
            if not projection_matches:
                raise ValueError(f"Accepted normalized projection mismatch: {case_id}/{normalized_id}")

            raw_enriched = {
                "candidate_key": f"{case_id}::raw::{original_id}",
                "rank": next(
                    item["original_rank"]
                    for item in normalization_log["id_map"]
                    if item["original_id"] == original_id
                ),
                "text_sha256": hashlib.sha256(raw_candidate["text"].encode()).hexdigest(),
                **raw_candidate,
            }
            raw_review = audit_candidate(raw_enriched, profile)
            normalized_review = audit_candidate(accepted_candidate, profile)
            cross_version_findings = []
            if raw_candidate["text"] != normalized_candidate["text"]:
                cross_version_findings.append(
                    issue("hidden_normalization_text_rewrite", "Raw and normalized prose differ")
                )
            if raw_candidate["visual_signature"] != normalized_candidate["visual_signature"]:
                cross_version_findings.append(
                    issue("hidden_normalization_inventory_rewrite", "Raw and normalized visual_signature differ")
                )
            immutable_fields = (
                "environment", "subsetting", "text", "evidence_ids", "creative_departures",
                "visual_signature", "camera_omissions",
            )
            changed_immutable_fields = [
                field for field in immutable_fields
                if raw_candidate[field] != normalized_candidate[field]
            ]
            if changed_immutable_fields:
                cross_version_findings.append(
                    issue(
                        "normalizer_changed_prohibited_fields",
                        repr(changed_immutable_fields),
                    )
                )

            text = normalized_candidate["text"]
            manual_resolution_evidence = lexical_resolution_evidence(text)
            if re.search(r"\boverhead\s+(?:light|lighting|diffusion)\b", text, re.I):
                manual_resolution_evidence.append(
                    {
                        "rule": "overhead_light_is_lighting_not_camera_instruction",
                        "decision": "harmless_nonissue",
                        "evidence": re.search(
                            r"\boverhead\s+(?:light|lighting|diffusion)\b", text, re.I
                        ).group(0),
                    }
                )
            surface_text = normalized_candidate["visual_signature"]["surface"]
            if re.search(r"\b(?:table|desk|counter|worktop|surface|ledge)\b", surface_text, re.I):
                manual_resolution_evidence.append(
                    {
                        "rule": "named_support_surface_is_context_not_prop_or_full_surface_request",
                        "decision": "harmless_nonissue",
                        "evidence": surface_text,
                    }
                )
            if (
                case_id == "ee810cf51bb82bb4__printer_FrontRightWide"
                and normalized_id == "p25"
            ):
                extraction = normalized_review["actual_text_extraction"]
                manual_resolution_evidence.append(
                    {
                        "rule": "root_review_numbered_prop_units",
                        "decision": "three_local_props_at_limit_not_two",
                        "evidence": {
                            "quoted_text": "a sketchbook and two paper samples",
                            "sketchbook_units": 1,
                            "paper_sample_units": 2,
                            "total_local_prop_units": extraction["effective_prop_count"],
                            "profile_max_local_props": profile["max_local_props"],
                            "people_slot": extraction["people_slot"],
                        },
                    }
                )

            combined_findings = [
                *raw_review["findings"],
                *normalized_review["findings"],
                *cross_version_findings,
            ]
            # Raw and normalized reviews commonly produce the same finding.
            # Preserve each source review above, but count the identical
            # candidate-level concern once.
            unique_findings = []
            seen_findings = set()
            for finding in combined_findings:
                key = canonical_sha256(finding)
                if key in seen_findings:
                    continue
                seen_findings.add(key)
                unique_findings.append(finding)
            resolved_codes = set()
            normalized_extraction = normalized_review["actual_text_extraction"]
            normalized_signature = normalized_candidate["visual_signature"]
            if normalized_extraction["reported_prop_units"] > len(
                normalized_signature["local_props"]
            ):
                manual_resolution_evidence.append(
                    {
                        "rule": "numbered_local_props_count_as_individual_units",
                        "decision": (
                            "within_profile_limit"
                            if normalized_extraction["effective_prop_count"]
                            <= profile["max_local_props"]
                            else "profile_limit_exceeded"
                        ),
                        "evidence": {
                            "inventory": normalized_signature["local_props"],
                            "list_items": len(normalized_signature["local_props"]),
                            "counted_units": normalized_extraction["reported_prop_units"],
                            "profile_max_local_props": profile["max_local_props"],
                        },
                    }
                )
                # This warning identifies the counting correction. Any actual
                # limit breach remains separately unresolved as an error.
                resolved_codes.add("self_report_list_length_undercounts_prop_units")
            if (
                case_id == "ee810cf51bb82bb4__printer_FrontRightWide"
                and normalized_id == "p25"
                and normalized_review["actual_text_extraction"]["effective_prop_count"]
                <= profile["max_local_props"]
                and normalized_review["actual_text_extraction"]["people_slot"] == 0
            ):
                resolved_codes.add("self_report_list_length_undercounts_prop_units")
            unresolved = [
                finding for finding in unique_findings
                if finding["code"] not in resolved_codes
            ]
            review = {
                "normalized_candidate_id": normalized_id,
                "normalized_candidate_key": expected_candidate_key,
                "normalized_rank": rank,
                "raw_candidate_id": original_id,
                "raw_prose_review": raw_review,
                "normalized_prose_review": normalized_review,
                "cross_version_findings": cross_version_findings,
                "accepted_projection_matches_normalized_output": projection_matches,
                "normalization_changed_fields": [
                    change
                    for change in normalization_log["changes"]
                    if change["original_id"] == original_id
                ],
                "manual_resolution_evidence": manual_resolution_evidence,
                "resolved_finding_codes": sorted(resolved_codes),
                "unresolved_findings": unresolved,
                "manual_resolution_status": (
                    "pending_root_review" if unresolved else "mechanically_clear_or_resolved"
                ),
            }
            candidate_reviews.append(review)
            rows.append({"case_id": case_id, **review})

        case_reviews.append(
            {
                "case_id": case_id,
                "source_id": case["source_id"],
                "device_type": case["device_type"],
                "camera_tag": case["camera_tag"],
                "view_role": case["view_role"],
                "profile": profile,
                "accepted_status": bank["status"],
                "human_review_status": bank["human_review_status"],
                "launchable": bank["launchable"],
                "raw_record": {
                    "path": str(raw_record_path.resolve()),
                    "file_sha256": bank["record_sha256"],
                    "parsed_output_semantic_sha256": bank["raw_parsed_output_sha256"],
                    "status": bank["raw_record_status"],
                },
                "normalized_output": {
                    "path": str(normalized_path.resolve()),
                    "file_sha256": bank["normalized_output_file_sha256"],
                    "semantic_sha256": bank["normalized_output_semantic_sha256"],
                },
                "normalization_log": {
                    "path": str(normalization_log_path.resolve()),
                    "file_sha256": bank["normalization_log_file_sha256"],
                    "changed_candidate_count": normalization_log["changed_candidate_count"],
                    "algorithm": normalization_log["algorithm"],
                },
                "validation_audit": {
                    "path": str(validation_audit_path.resolve()),
                    "file_sha256": sha256_path(validation_audit_path),
                },
                "candidate_count": len(candidate_reviews),
                "unresolved_candidate_count": sum(
                    bool(review["unresolved_findings"]) for review in candidate_reviews
                ),
                "candidates": candidate_reviews,
            }
        )
    code_counts: dict[str, int] = {}
    for row in rows:
        for finding in row["unresolved_findings"]:
            code_counts[finding["code"]] = code_counts.get(finding["code"], 0) + 1
    complete = len(accepted_cases) == 18 and len(rows) == 540
    return {
        "version": "v3-camera-prose-review-v2",
        "status": "complete_540_candidate_review" if complete else "progressive_incomplete",
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "method": {
            "claim_status": "MECHANICAL_LEXICAL_AUDIT_REQUIRES_HUMAN_REVIEW",
            "actual_prose_read": True,
            "self_report_used_only_for_comparison_and_conservative_max_count": True,
            "people_slot_rule": "Any explicit person/hand/activity subject consumes one local-prop slot; it must replace rather than add to the allowed props.",
            "normalization_boundary": "Both immutable raw parsed output and normalized output are hash-verified and audited; any prose or visual_signature rewrite is a critical flag.",
            "harmless_context_rules": [
                "Overhead light, overhead lighting, and overhead diffusion are illumination, not camera instructions.",
                "A named desk/table/counter/worktop/ledge is the focal support surface and does not require a full surface or consume a prop slot.",
            ],
            "limitation": "The fixed lexical inventory can miss novel noun phrases and can flag polysemy; a clean result is not proof of semantic correctness.",
        },
        "provenance": {
            "manifest_path": str(manifest_path.resolve()),
            "manifest_sha256": sha256_path(manifest_path),
            "accepted_prompt_cases_path": str(accepted_path.resolve()),
            "accepted_prompt_cases_sha256": sha256_path(accepted_path),
            "accepted_map_canonical_sha256": canonical_sha256(accepted),
        },
        "counts": {
            "accepted_cases_audited": len(accepted_cases),
            "candidate_rows_audited": len(rows),
            "raw_and_normalized_prose_documents_audited": len(rows) * 2,
            "rows_requiring_human_review": sum(bool(row["unresolved_findings"]) for row in rows),
            "unresolved_finding_count": sum(len(row["unresolved_findings"]) for row in rows),
            "finding_code_counts": dict(sorted(code_counts.items())),
            "complete_expected_case_count": 18,
            "complete_expected_candidate_count": 540,
            "is_complete": complete,
        },
        "cases": case_reviews,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--accepted", type=Path, default=ACCEPTED_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    accepted_path = args.accepted.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    accepted = json.loads(accepted_path.read_text(encoding="utf-8"))
    audit = build_audit(
        manifest, accepted, args.allow_partial, manifest_path, accepted_path
    )
    atomic_json(args.output.resolve(), audit)
    print(json.dumps(audit["counts"], indent=2))


if __name__ == "__main__":
    main()
