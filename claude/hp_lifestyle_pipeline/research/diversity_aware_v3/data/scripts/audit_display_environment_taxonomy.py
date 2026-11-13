#!/usr/bin/env python3
"""Audit a proposed display-only Café/Creative Studio taxonomy for V3 prompts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_INPUT = (
    PROJECT_ROOT
    / "eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation_prompts.json"
)
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "research/diversity_aware_v3/data/v3_display_environment_taxonomy_audit.json"
)

CAFE_RE = re.compile(r"(?<![\w])caf(?:é|e)(?![\w])", re.I)
STUDIO_RE = re.compile(r"(?<![\w])studio(?![\w])", re.I)
PHYSICAL_STUDIO_TEXT_RE = re.compile(
    r"(?<![\w])(?:creative\s+|content\s+|maker\s+|design\s+)?studio"
    r"(?:[- ]+[a-z]+){0,2}[- ]+"
    r"(?:tabletop|table|worktable|worktop|desk|surface|counter|workspace|corner|area)\b",
    re.I,
)
COWORKING_RE = re.compile(r"\b(?:co[- ]?working|coworking)\b", re.I)
DESIGN_RE = re.compile(r"\bdesign\b", re.I)
CONTENT_RE = re.compile(r"\bcontent\b", re.I)
MAKER_RE = re.compile(r"\bmaker\b", re.I)
CRAFT_RE = re.compile(r"\bcraft(?:ing)?\b", re.I)
ART_CLASSROOM_RE = re.compile(r"\bart\s+(?:classroom|room)\b|\bdesign\s+critique\b", re.I)
COFFEE_RE = re.compile(r"\bcoffee\b", re.I)
STUDIO_LIGHTING_DEPTH_RE = re.compile(
    r"\bstudio\s+(?:daylight|light|lighting|depth)\b", re.I
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def matches(pattern: re.Pattern[str], value: str) -> list[str]:
    return [match.group(0) for match in pattern.finditer(value)]


def match_record(
    prompt: dict[str, Any], display_environment: str, rule_id: str, triggers: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "candidate_key": prompt["candidate_key"],
        "case_id": prompt["case_id"],
        "source_id": prompt["source_id"],
        "camera_tag": prompt["camera_tag"],
        "rank": prompt["rank"],
        "canonical_environment": prompt["environment"],
        "display_environment": display_environment,
        "subsetting": prompt["subsetting"],
        "text": prompt["text"],
        "rule_id": rule_id,
        "triggers": triggers,
    }


def classify(prompt: dict[str, Any]) -> dict[str, Any]:
    """Apply ordered, conservative display rules without changing environment."""
    canonical = prompt["environment"]
    subsetting = prompt["subsetting"]
    text = prompt["text"]
    if canonical != "Office":
        return match_record(prompt, canonical, "preserve_non_office", [])

    cafe_subsetting = matches(CAFE_RE, subsetting)
    cafe_text = matches(CAFE_RE, text)
    if cafe_subsetting or cafe_text:
        triggers = []
        if cafe_subsetting:
            triggers.append({"field": "subsetting", "terms": cafe_subsetting})
        if cafe_text:
            triggers.append({"field": "text", "terms": cafe_text})
        return match_record(prompt, "Café", "office_explicit_cafe", triggers)

    studio_subsetting = matches(STUDIO_RE, subsetting)
    if studio_subsetting:
        return match_record(
            prompt,
            "Creative Studio",
            "office_explicit_studio_subsetting",
            [{"field": "subsetting", "terms": studio_subsetting}],
        )

    physical_studio_text = matches(PHYSICAL_STUDIO_TEXT_RE, text)
    if physical_studio_text:
        return match_record(
            prompt,
            "Creative Studio",
            "office_physical_studio_setting_in_text",
            [{"field": "text", "terms": physical_studio_text}],
        )

    return match_record(prompt, "Office", "preserve_office_no_explicit_setting", [])


def compact_prompt(prompt: dict[str, Any], triggers: list[dict[str, Any]], reason: str) -> dict[str, Any]:
    return {
        "candidate_key": prompt["candidate_key"],
        "case_id": prompt["case_id"],
        "canonical_environment": prompt["environment"],
        "subsetting": prompt["subsetting"],
        "text": prompt["text"],
        "triggers": triggers,
        "reason": reason,
    }


def ambiguity_audit(
    prompts: list[dict[str, Any]], classifications: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {
        "office_coworking_preserved_as_office": [],
        "office_design_without_explicit_studio_setting": [],
        "office_content_without_explicit_studio_setting": [],
        "office_studio_lighting_or_depth_only": [],
        "non_office_art_classroom_or_design_critique_preserved": [],
        "non_office_craft_preserved": [],
        "non_cafe_literal_coffee_mentions": [],
        "maker_studio_classified_creative_studio": [],
        "content_studio_classified_creative_studio": [],
    }
    for prompt in prompts:
        classification = classifications[prompt["candidate_key"]]
        combined = f"{prompt['subsetting']} {prompt['text']}"
        display = classification["display_environment"]

        coworking = matches(COWORKING_RE, combined)
        if prompt["environment"] == "Office" and display == "Office" and coworking:
            groups["office_coworking_preserved_as_office"].append(
                compact_prompt(
                    prompt,
                    [{"field": "subsetting_and_text", "terms": coworking}],
                    "Coworking is a shared-work arrangement, not explicit evidence of a café or creative studio.",
                )
            )

        design = matches(DESIGN_RE, combined)
        if prompt["environment"] == "Office" and display == "Office" and design:
            groups["office_design_without_explicit_studio_setting"].append(
                compact_prompt(
                    prompt,
                    [{"field": "subsetting_and_text", "terms": design}],
                    "Design vocabulary alone does not establish a studio setting; studio light/depth is treated as description.",
                )
            )

        content = matches(CONTENT_RE, combined)
        if prompt["environment"] == "Office" and display == "Office" and content:
            groups["office_content_without_explicit_studio_setting"].append(
                compact_prompt(
                    prompt,
                    [{"field": "subsetting_and_text", "terms": content}],
                    "Content-work vocabulary alone does not establish a studio setting.",
                )
            )

        studio_lighting = matches(STUDIO_LIGHTING_DEPTH_RE, prompt["text"])
        if prompt["environment"] == "Office" and display == "Office" and studio_lighting:
            groups["office_studio_lighting_or_depth_only"].append(
                compact_prompt(
                    prompt,
                    [{"field": "text", "terms": studio_lighting}],
                    "Studio modifies lighting or depth, rather than naming the physical setting.",
                )
            )

        art_classroom = matches(ART_CLASSROOM_RE, combined)
        if prompt["environment"] != "Office" and art_classroom:
            groups["non_office_art_classroom_or_design_critique_preserved"].append(
                compact_prompt(
                    prompt,
                    [{"field": "subsetting_and_text", "terms": art_classroom}],
                    "The canonical non-Office environment gate takes precedence; art classroom remains Education.",
                )
            )

        craft = matches(CRAFT_RE, combined)
        if prompt["environment"] != "Office" and craft:
            groups["non_office_craft_preserved"].append(
                compact_prompt(
                    prompt,
                    [{"field": "subsetting_and_text", "terms": craft}],
                    "The canonical non-Office environment gate takes precedence; home craft remains Home.",
                )
            )

        coffee = matches(COFFEE_RE, combined)
        if display != "Café" and coffee:
            groups["non_cafe_literal_coffee_mentions"].append(
                compact_prompt(
                    prompt,
                    [{"field": "subsetting_and_text", "terms": coffee}],
                    "A coffee mention alone is not a café-setting trigger.",
                )
            )

        maker = matches(MAKER_RE, combined)
        if display == "Creative Studio" and maker:
            groups["maker_studio_classified_creative_studio"].append(
                compact_prompt(
                    prompt,
                    [{"field": "subsetting_and_text", "terms": maker}],
                    "Explicit maker studio is included in the Creative Studio display family.",
                )
            )

        content = matches(CONTENT_RE, combined)
        if display == "Creative Studio" and content:
            groups["content_studio_classified_creative_studio"].append(
                compact_prompt(
                    prompt,
                    [{"field": "subsetting_and_text", "terms": content}],
                    "Content work is classified as Creative Studio only when an explicit physical studio setting also matches.",
                )
            )

    return {
        key: {"count": len(values), "candidates": sorted(values, key=lambda row: row["candidate_key"])}
        for key, values in groups.items()
    }


def build_audit(document: dict[str, Any], input_path: Path, input_sha256: str) -> dict[str, Any]:
    prompts = document["prompts"]
    if len(prompts) != 540:
        raise ValueError(f"Expected 540 prompts, found {len(prompts)}")
    classifications = {prompt["candidate_key"]: classify(prompt) for prompt in prompts}
    if len(classifications) != 540:
        raise ValueError("candidate_key values are not unique")
    matched = {
        label: sorted(
            [row for row in classifications.values() if row["display_environment"] == label],
            key=lambda row: row["candidate_key"],
        )
        for label in ("Café", "Creative Studio")
    }
    all_rows = sorted(classifications.values(), key=lambda row: row["candidate_key"])
    display_counts = Counter(row["display_environment"] for row in all_rows)
    canonical_counts = Counter(row["canonical_environment"] for row in all_rows)
    rule_counts = Counter(row["rule_id"] for row in all_rows)
    changed_rows = [
        row for row in all_rows if row["canonical_environment"] != row["display_environment"]
    ]
    return {
        "version": "v3-display-environment-taxonomy-audit-v1",
        "input": {
            "path": str(input_path.resolve()),
            "sha256": input_sha256,
            "bytes": input_path.stat().st_size,
            "export_version": document.get("version"),
            "scope": document.get("scope"),
        },
        "recommendation": {
            "new_field": "display_environment",
            "canonical_environment_preserved": True,
            "ordered_rules": [
                {
                    "order": 1,
                    "rule_id": "preserve_non_office",
                    "condition": "environment != 'Office'",
                    "result": "display_environment = environment",
                },
                {
                    "order": 2,
                    "rule_id": "office_explicit_cafe",
                    "condition": "environment == 'Office' and standalone /caf(?:é|e)/ appears in subsetting or text",
                    "result": "display_environment = 'Café'",
                },
                {
                    "order": 3,
                    "rule_id": "office_explicit_studio_subsetting",
                    "condition": "environment == 'Office' and standalone /studio/ appears in subsetting",
                    "result": "display_environment = 'Creative Studio'",
                },
                {
                    "order": 4,
                    "rule_id": "office_physical_studio_setting_in_text",
                    "condition": (
                        "environment == 'Office' and text matches optional creative/content/maker/design + "
                        "studio + up to two modifiers + physical setting noun "
                        "(tabletop/table/worktable/worktop/desk/surface/counter/workspace/corner/area)"
                    ),
                    "result": "display_environment = 'Creative Studio'",
                },
                {
                    "order": 5,
                    "rule_id": "preserve_office_no_explicit_setting",
                    "condition": "remaining environment == 'Office' rows",
                    "result": "display_environment = 'Office'",
                },
            ],
            "rationale": (
                "Use explicit setting nouns conservatively. Coworking, design/content vocabulary, "
                "studio lighting/depth, coffee, cups, and craft/art activity do not independently relabel a setting."
            ),
        },
        "counts": {
            "total_prompts": len(prompts),
            "canonical_environment": {key: canonical_counts[key] for key in sorted(canonical_counts)},
            "display_environment": {key: display_counts[key] for key in sorted(display_counts)},
            "rule_id": {key: rule_counts[key] for key in sorted(rule_counts)},
            "changed_from_canonical": len(changed_rows),
            "unchanged_from_canonical": len(prompts) - len(changed_rows),
        },
        "matched_candidates": {
            "Café": {"count": len(matched["Café"]), "candidates": matched["Café"]},
            "Creative Studio": {
                "count": len(matched["Creative Studio"]),
                "candidates": matched["Creative Studio"],
            },
        },
        "ambiguous_and_borderline": ambiguity_audit(prompts, classifications),
        "all_prompt_mappings": all_rows,
        "limitations": [
            "This is a deterministic lexical display taxonomy, not a semantic classifier.",
            "Only canonical Office rows are eligible for Café or Creative Studio; all other canonical environments are preserved.",
            "The conservative rule intentionally leaves coworking, design/content work without a physical studio noun, and studio lighting/depth as Office.",
            "Literal coffee mentions alone do not trigger Café; this frozen export contains zero such non-Café mentions.",
            "The proposed field is display_environment; the canonical environment value is never modified.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    input_path = args.input.resolve()
    output_path = args.output.resolve()
    raw = input_path.read_bytes()
    document = json.loads(raw)
    audit = build_audit(document, input_path, sha256_bytes(raw))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_name(f".{output_path.name}.tmp")
    temporary.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(output_path)
    print(
        json.dumps(
            {
                "output": str(output_path),
                "display_environment_counts": audit["counts"]["display_environment"],
                "changed_from_canonical": audit["counts"]["changed_from_canonical"],
                "cafe_candidate_count": audit["matched_candidates"]["Café"]["count"],
                "creative_studio_candidate_count": audit["matched_candidates"]["Creative Studio"]["count"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
