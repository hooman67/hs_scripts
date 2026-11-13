#!/usr/bin/env python3
"""Build a bounded lexical/diversity audit of accepted camera-V2 prompts."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT = Path(__file__).resolve().parents[3]
OUTPUT = PROJECT / "research/diversity_aware_v3/data/v2_diversity_audit.json"
ACCEPTED = PROJECT / "eval_sets/hp_lifestyle_camera_v2_eval_20261022/accepted_prompt_cases.json"
MANIFEST = PROJECT / "eval_sets/hp_lifestyle_camera_v2_eval_20261022/manifest.json"
GUIDANCE_EXTRACT = PROJECT / "research/source_messaging_v1_to_v6/data/october_guidance.json"
WORKBOOK_EXTRACT = PROJECT / "research/source_messaging_v1_to_v6/data/lifestyle_column_a.json"
DOWNSTREAM = PROJECT / "local_data/generation_runs/hp_lifestyle_camera_v2_eval_20261022"


INDICATORS = {
    "office_workplace": r"\boffice\b|shared[- ]workspace|\bworkplace\b|\bcorporate\b",
    "education_library": r"\bschool\b|classroom|education|learning|lesson|student|university|library",
    "home_residential": r"\bhome\b|household|residential|living room|kitchen|bedroom|sunroom",
    "creative_studio": r"creative|studio|design|sketch|storyboard|\bart\b|jewelry|craft",
    "cafe_coffee_shop": r"caf[eé]|coffee shop",
    "customer_site_reception": r"customer[- ]site|client[- ]site|reception",
    "meeting_collaboration": r"meeting|conference|collaborat|\bteam\b",
    "it_operations_policy": r"\bit\b|deployment|operations|policy",
    "outdoor_urban": r"outdoor|sidewalk|plaza|patio|\bcity\b|storefront|\bdeck\b",
    "healthcare": r"clinic|medical|hospital",
    "gaming": r"gaming|\bgame\b|gamer",
    "retail_craft_shop": r"bookstore|\bshop\b|retail|craft shop",
}

SURFACES = {
    "wood_or_wood_species": r"\bwood(?:en)?\b|\boak\b|\bmaple\b",
    "laminate": r"\blaminate\b",
    "stone_or_marble": r"\bstone\b|\bmarble\b",
    "desk": r"\bdesk\b",
    "table_worktable_tabletop": r"\btable\b|tabletop|worktable",
    "counter_credenza": r"counter|credenza",
    "floor_lap_or_soft_seating": r"\bfloor\b|\blap\b|sofa|couch|bench",
}

PROPS = {
    "documents_forms_paper": r"\bforms?\b|\bpapers?\b|documents?|worksheets?|handouts?|reports?|records?|packets?|pages?|schedule|checklist",
    "writing_instrument": r"\bpen\b|pencil|marker",
    "folder_binder_notebook": r"folder|binder|notebook|notepad|sketchpad|planner",
    "drinkware_or_coffee": r"\bmug\b|\bcup\b|\bglass\b|coffee",
    "chair_or_seating": r"chair|seating",
    "storage_shelving_or_tray": r"cabinet|shelf|shelving|cubby|organizer|\btray\b",
    "noticeboard_pinboard": r"notice ?board|bulletin|corkboard|pinboard",
    "plant_or_greenery": r"plant|greenery|succulent",
    "window": r"\bwindows?\b",
    "people": r"\bperson\b|\bpeople\b|professional|student|teacher|\bwoman\b|\bman\b|colleague|coworker|family|\bboy\b|\bgirl\b",
    "secondary_computing_hardware": r"\bphone\b|smartphone|\btablet\b|monitor|\bhardware\b|\bdevice\b|\bscreen\b",
}

STYLE_LANGUAGE = {
    "soft_or_diffuse_daylight": r"soft(?:,)?(?: diffuse)? daylight|diffuse daylight",
    "warm_light_or_atmosphere": r"warm (?:natural )?(?:light|lighting|atmosphere)|warmly lit|warm ambient",
    "plain_or_clean_neutral_backdrop": r"(?:plain|clean|simple) neutral (?:backdrop|background|surround|tone)",
    "softly_blurred": r"softly blurred|softly out of focus|soft-focus",
    "lived_in_authentic_imperfect": r"lived-in|authentic|imperfection|imperfect",
    "layered_or_natural_depth": r"layered|natural depth",
}

DOWNSTREAM_PATTERNS = {
    "soft_cool_daylight": r"soft cool daylight",
    "teal_cyan_color_grade": r"teal-cyan color grade",
    "shallow_depth_of_field": r"shallow depth of field",
    "sitting_flush": r"sits? flush|sitting flush",
    "no_occlusions": r"no occlusions",
    "white_mug": r"white (?:ceramic )?mug",
    "smartphone": r"\bsmartphone\b",
    "window": r"\bwindows?\b",
    "partition": r"partition",
    "chair": r"\bchair\b",
    "plant_or_greenery": r"plant|greenery",
    "notebook_or_notepad": r"notebook|notepad",
    "writing_instrument": r"\bpen\b|pencil|marker",
    "paperwork": r"form|paper|worksheet|document|folder|binder|packet|report",
}

STOPWORDS = {
    "a", "an", "the", "and", "with", "in", "of", "to", "on", "for", "at", "by",
    "as", "is", "it", "its", "this", "that", "from",
}


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pct(count: int, denominator: int) -> float:
    return round(100 * count / denominator, 2) if denominator else 0.0


def tokens(text: str) -> list[str]:
    return re.findall(r"\b[a-z0-9]+\b", text.lower())


def normalized(text: str) -> str:
    return " ".join(tokens(text))


def lexical_counts(texts: list[str], patterns: dict[str, str]) -> dict[str, dict[str, Any]]:
    result = {}
    for name, pattern in patterns.items():
        count = sum(bool(re.search(pattern, text, re.I)) for text in texts)
        result[name] = {"count": count, "percent": pct(count, len(texts))}
    return result


def top_ngrams(rows: list[dict[str, Any]], n: int, limit: int = 20) -> list[dict[str, Any]]:
    occurrences: Counter[tuple[str, ...]] = Counter()
    sources: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for row in rows:
        words = tokens(row["text"])
        seen = {tuple(words[i : i + n]) for i in range(len(words) - n + 1)}
        for gram in seen:
            occurrences[gram] += 1
            sources[gram].add(row["source_id"])
    ranked = sorted(
        occurrences,
        key=lambda gram: (len(sources[gram]), occurrences[gram], gram),
        reverse=True,
    )[:limit]
    return [
        {
            "phrase": " ".join(gram),
            "prompt_count": occurrences[gram],
            "prompt_percent": pct(occurrences[gram], len(rows)),
            "distinct_source_count": len(sources[gram]),
        }
        for gram in ranked
    ]


def jaccard(a: str, b: str) -> float:
    left, right = set(tokens(a)) - STOPWORDS, set(tokens(b)) - STOPWORDS
    return len(left & right) / len(left | right) if left or right else 1.0


def similarity(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[float]] = defaultdict(list)
    for left, right in itertools.combinations(rows, 2):
        score = jaccard(left["text"], right["text"])
        if left["source_id"] == right["source_id"]:
            groups["same_source"].append(score)
        elif left["device_type"] == right["device_type"]:
            groups["different_source_same_device_type"].append(score)
            if left["camera_tag"] == right["camera_tag"]:
                groups["same_camera_tag_different_source_same_device_type"].append(score)
        else:
            groups["different_device_type"].append(score)
    return {
        name: {
            "pair_count": len(values),
            "mean_jaccard": round(statistics.mean(values), 4),
            "median_jaccard": round(statistics.median(values), 4),
        }
        for name, values in groups.items()
    }


def corpus_summary(texts: list[str]) -> dict[str, Any]:
    lengths = [len(tokens(text)) for text in texts]
    normalized_counts = Counter(normalized(text) for text in texts)
    duplicate_groups = [
        {"normalized_text": text, "count": count}
        for text, count in normalized_counts.most_common()
        if count > 1
    ]
    return {
        "prompt_count": len(texts),
        "unique_normalized_prompt_count": len(normalized_counts),
        "exact_normalized_duplicate_group_count": len(duplicate_groups),
        "exact_normalized_duplicate_row_count": sum(x["count"] for x in duplicate_groups),
        "duplicate_groups": duplicate_groups,
        "word_count": {
            "mean": round(statistics.mean(lengths), 2),
            "median": statistics.median(lengths),
            "min": min(lengths),
            "max": max(lengths),
        },
        "subsetting_indicators_overlapping": lexical_counts(texts, INDICATORS),
        "surface_indicators_overlapping": lexical_counts(texts, SURFACES),
        "prop_and_scene_element_indicators_overlapping": lexical_counts(texts, PROPS),
        "style_language_indicators_overlapping": lexical_counts(texts, STYLE_LANGUAGE),
    }


def source_record(
    path: Path,
    role: str,
    source_class: str,
    original_sha: str | None = None,
) -> dict[str, Any]:
    item = {
        "path": str(path),
        "sha256": sha(path),
        "bytes": path.stat().st_size,
        "role": role,
        "source_class": source_class,
        "retrieved_or_inspected_date": "2026-10-23",
    }
    if original_sha:
        item["original_artifact_sha256"] = original_sha
    return item


def camera_family(tag: str) -> str:
    if "CAMReview" in tag:
        return "unknown_review"
    if "CloseUp" in tag:
        return "tight"
    if "Wide" in tag:
        return "wide"
    if "Medium" in tag:
        return "medium"
    return "other"


def downstream_snapshot() -> dict[str, Any]:
    parsed = []
    parse_failures = []
    record_paths = sorted((DOWNSTREAM / "records").glob("*.json"))
    for path in record_paths:
        try:
            record = read(path)
        except Exception as exc:  # evidence remains visible
            parse_failures.append({"path": str(path), "error": str(exc)})
            continue
        if record.get("status") == "done" and record.get("usedPrompt"):
            parsed.append((path, record))

    snapshot_hash = hashlib.sha256()
    for path, _ in parsed:
        snapshot_hash.update(path.name.encode("utf-8"))
        snapshot_hash.update(b"\0")
        snapshot_hash.update(sha(path).encode("ascii"))
        snapshot_hash.update(b"\n")

    pattern_counts = {}
    for name, pattern in DOWNSTREAM_PATTERNS.items():
        raw_count = sum(
            bool(re.search(pattern, row["prompt"]["text"], re.I)) for _, row in parsed
        )
        used_count = sum(bool(re.search(pattern, row["usedPrompt"], re.I)) for _, row in parsed)
        added_count = sum(
            not re.search(pattern, row["prompt"]["text"], re.I)
            and bool(re.search(pattern, row["usedPrompt"], re.I))
            for _, row in parsed
        )
        pattern_counts[name] = {
            "raw_prompt_count": raw_count,
            "raw_prompt_percent": pct(raw_count, len(parsed)),
            "used_prompt_count": used_count,
            "used_prompt_percent": pct(used_count, len(parsed)),
            "used_but_absent_from_raw_count": added_count,
            "used_but_absent_from_raw_percent": pct(added_count, len(parsed)),
        }

    used_rows = [
        {"source_id": row["source_id"], "text": row["usedPrompt"]} for _, row in parsed
    ]
    downstream_ngrams = top_ngrams(used_rows, 4, 15)

    strata: dict[tuple[str, str, str, str], list[tuple[Path, dict[str, Any]]]] = defaultdict(list)
    for path, row in parsed:
        strata[
            (
                row["device_type"],
                camera_family(row["camera_tag"]),
                row["prompt"]["environment"],
                row["source_id"],
            )
        ].append((path, row))
    sample = []
    for stratum, candidates in sorted(strata.items()):
        path, row = min(
            candidates,
            key=lambda item: hashlib.sha256(item[1]["row_id"].encode("utf-8")).hexdigest(),
        )
        stage = (row.get("debugData") or {}).get("stage1Output") or {}
        prompt = stage.get("prompt") or {}
        sample.append(
            {
                "stratum": {
                    "device_type": stratum[0],
                    "camera_family": stratum[1],
                    "environment": stratum[2],
                    "source_id": stratum[3],
                },
                "row_id": row["row_id"],
                "source_id": row["source_id"],
                "camera_tag": row["camera_tag"],
                "record_path": str(path),
                "record_sha256": sha(path),
                "raw_prompt_exact": row["prompt"]["text"],
                "editing_instruction_exact": stage.get("editing_instruction"),
                "entity_labels_exact": [entity.get("label") for entity in prompt.get("entities", [])],
            }
        )

    return {
        "snapshot_generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "records_directory": str(DOWNSTREAM / "records"),
        "all_record_file_count_at_snapshot": len(record_paths),
        "completed_records_with_used_prompt_count": len(parsed),
        "completed_records_snapshot_sha256": snapshot_hash.hexdigest(),
        "parse_failures": parse_failures,
        "device_type_counts": dict(Counter(row["device_type"] for _, row in parsed)),
        "camera_family_counts": {
            f"{device_type}:{family}": count
            for (device_type, family), count in sorted(
                Counter(
                    (row["device_type"], camera_family(row["camera_tag"]))
                    for _, row in parsed
                ).items()
            )
        },
        "distinct_case_count": len({row["case_id"] for _, row in parsed}),
        "distinct_case_prompt_count": len(
            {(row["case_id"], row["prompt_id"]) for _, row in parsed}
        ),
        "raw_to_used_pattern_counts": pattern_counts,
        "common_used_prompt_four_grams": downstream_ngrams,
        "stratified_sample_method": "One deterministic SHA-256-minimum row per available device_type × camera_family × accepted environment × source_id stratum.",
        "stratified_sample_count": len(sample),
        "stratified_sample": sample,
    }


def main() -> None:
    accepted = read(ACCEPTED)
    manifest = read(MANIFEST)
    guidance = read(GUIDANCE_EXTRACT)
    workbook = read(WORKBOOK_EXTRACT)

    v2_rows = []
    for case_id, entry in accepted["cases"].items():
        for prompt in entry["prompts"]:
            v2_rows.append(
                {
                    "case_id": case_id,
                    "source_id": entry["source_id"],
                    "device_type": entry["device_type"],
                    "camera_tag": entry["camera_tag"],
                    "framing": entry["expected_camera"]["framing"],
                    "environment": prompt["environment"],
                    "prompt_id": prompt["prompt_id"],
                    "text": prompt["text"],
                }
            )
    v2_texts = [row["text"] for row in v2_rows]

    guidance_paragraphs = {
        item["paragraph"]: item["text"] for item in guidance["paragraphs"]
    }
    guidance_sample_ids = [6, 7, 8, 10, 11, 12, 14, 15, 17, 18]
    guidance_texts = [guidance_paragraphs[index] for index in guidance_sample_ids]
    workbook_eval = next(sheet for sheet in workbook["sheets"] if sheet["name"] == "Eval Set Prompts")
    workbook_texts = [item["text"] for item in workbook_eval["cells"] if item["cell"] != "A1"]
    theme_sheet = next(sheet for sheet in workbook["sheets"] if sheet["name"] == "Theme Styles")

    by_source = {}
    for source_id in sorted({row["source_id"] for row in v2_rows}):
        subset = [row for row in v2_rows if row["source_id"] == source_id]
        by_source[source_id] = {
            "device_type": subset[0]["device_type"],
            "prompt_count": len(subset),
            "environment_counts": dict(Counter(row["environment"] for row in subset)),
            "subsetting_indicators_overlapping": lexical_counts(
                [row["text"] for row in subset], INDICATORS
            ),
        }

    by_framing = {}
    for framing in sorted({row["framing"] for row in v2_rows}):
        subset = [row for row in v2_rows if row["framing"] == framing]
        by_framing[framing] = {
            "prompt_count": len(subset),
            "environment_counts": dict(Counter(row["environment"] for row in subset)),
            "word_count_mean": round(
                statistics.mean(len(tokens(row["text"])) for row in subset), 2
            ),
            "surface_indicators_overlapping": lexical_counts(
                [row["text"] for row in subset], SURFACES
            ),
            "prop_and_scene_element_indicators_overlapping": lexical_counts(
                [row["text"] for row in subset], PROPS
            ),
        }

    guidance_summary = corpus_summary(guidance_texts)
    workbook_summary = corpus_summary(workbook_texts)
    v2_summary = corpus_summary(v2_texts)
    env_counts = Counter(row["environment"] for row in v2_rows)

    original_guidance = Path(guidance["path"])
    original_workbook = Path(workbook["path"])
    evidence = {
        "version": "v2-diversity-audit-v1",
        "as_of_date": "2026-10-23",
        "scope": {
            "question": "How diverse are accepted camera-V2 environment prompts, how do their recurring settings/surfaces/props/language compare with established October mAIstro guidance and workbook column A, and what additional homogenization is visible in available downstream usedPrompt records?",
            "included": [
                "All 592 accepted prompt texts from 369 final camera-V2 cases.",
                "The 10 scene examples and reusable template in the October mAIstro guidance extraction.",
                "The 58 base scene prompts in column A of the workbook's Eval Set Prompts sheet; the Theme Styles column-A instruction is recorded separately and not counted as a scene.",
                "A bounded snapshot of completed downstream records containing usedPrompt, with a deterministic stratified exact-text sample.",
            ],
            "excluded": [
                "Image-quality judgments and visual annotation.",
                "Any claim that source-message weakness alone caused repetition.",
                "Prompt redesign, generation calls, or edits to camera-V2 artifacts.",
            ],
        },
        "sources": [
            source_record(
                ACCEPTED,
                "final accepted camera-V2 prompts",
                "derived primary evidence",
            ),
            source_record(
                MANIFEST,
                "camera-V2 case/source/camera denominators",
                "derived primary evidence",
            ),
            source_record(
                GUIDANCE_EXTRACT,
                "allowed-content extraction of October mAIstro guidance",
                "derived primary evidence",
                guidance["sha256"],
            ),
            source_record(
                WORKBOOK_EXTRACT,
                "allowed extraction of workbook column A only",
                "derived primary evidence",
                workbook["sha256"],
            ),
            source_record(
                original_guidance,
                "original October mAIstro guidance artifact",
                "user-provided primary work artifact",
            ),
            source_record(
                original_workbook,
                "original workbook; audit reads column A extraction only",
                "user-provided primary work artifact",
            ),
        ],
        "denominators": {
            "v2_case_count": len(accepted["cases"]),
            "v2_prompt_count": len(v2_rows),
            "v2_source_count": len({row["source_id"] for row in v2_rows}),
            "v2_device_type_counts_prompts": dict(
                Counter(row["device_type"] for row in v2_rows)
            ),
            "october_guidance_scene_example_count": len(guidance_texts),
            "workbook_eval_set_column_a_scene_count": len(workbook_texts),
            "workbook_theme_style_column_a_instruction_count": 1,
        },
        "method": {
            "environment": "Exact accepted schema field; mutually exclusive.",
            "subsettings_surfaces_props_style": "Case-insensitive lexical indicators. Categories overlap and are not exhaustive semantic classifications. Regex definitions are preserved below.",
            "similarity": "All-pairs Jaccard similarity over lowercased alphanumeric word sets after listed stopword removal.",
            "ngrams": "Each n-gram counts at most once per prompt; distinct-source coverage is also reported.",
            "downstream": "All parseable completed record files with nonempty usedPrompt at snapshot time; exact raw and structured rewrite fields are read from saved local records.",
            "definitions": {
                "subsetting_indicators": INDICATORS,
                "surface_indicators": SURFACES,
                "prop_indicators": PROPS,
                "style_language_indicators": STYLE_LANGUAGE,
                "similarity_stopwords": sorted(STOPWORDS),
            },
        },
        "v2_accepted_prompt_audit": {
            **v2_summary,
            "environment_counts": {
                name: {"count": count, "percent": pct(count, len(v2_rows))}
                for name, count in env_counts.most_common()
            },
            "by_source": by_source,
            "by_framing": by_framing,
            "common_four_grams_ranked_by_source_coverage_then_frequency": top_ngrams(
                v2_rows, 4, 30
            ),
            "all_pair_similarity": similarity(v2_rows),
        },
        "comparison_corpora": {
            "october_guidance": {
                **guidance_summary,
                "scene_paragraph_ids": guidance_sample_ids,
                "named_scene_families": {
                    "Corporate Office": 3,
                    "Home Workspace": 3,
                    "Coffee Shop": 2,
                    "Creative Studio": 2,
                },
                "reusable_template_exact": guidance_paragraphs[3],
                "representative_exact_snippets": [
                    {"paragraph": 7, "text": guidance_paragraphs[7]},
                    {"paragraph": 11, "text": guidance_paragraphs[11]},
                    {"paragraph": 14, "text": guidance_paragraphs[14]},
                    {"paragraph": 17, "text": guidance_paragraphs[17]},
                ],
            },
            "workbook_column_a": {
                **workbook_summary,
                "sheet": "Eval Set Prompts",
                "included_cells": "A2:A59",
                "theme_style_instruction_exact": theme_sheet["cells"][1]["text"],
                "representative_exact_snippets": [
                    next(item for item in workbook_eval["cells"] if item["cell"] == cell)
                    for cell in ("A9", "A19", "A22", "A34", "A53", "A59")
                ],
            },
        },
        "downstream_used_prompt_snapshot": downstream_snapshot(),
        "findings": [
            {
                "id": "environment_concentration",
                "confidence": "VERIFIED",
                "claim": "Accepted V2 environment labels are concentrated in Office: 493/592 prompts (83.28%); Education is 82/592 (13.85%) and Home is 17/592 (2.87%).",
                "scope": "All final accepted V2 prompt texts.",
            },
            {
                "id": "repeated_scene_materials",
                "confidence": "VERIFIED",
                "claim": "Lexical scene construction repeatedly uses documents/forms/paper (416/592), writing instruments (314/592), wood/species surfaces (308/592), table/worktable/tabletop (284/592), and laminate (155/592).",
                "scope": "Overlapping lexical indicators; a prompt may count in several categories.",
            },
            {
                "id": "cross_source_repetition",
                "confidence": "VERIFIED",
                "claim": "The most repeated four-gram, 'a compact stack of', occurs in 205/592 prompts and all 9 sources. Multiple high-frequency phrases span all 9 sources, and same-camera/different-source mean Jaccard similarity exceeds the overall same-source mean. Repetition therefore is not isolated to one weak source.",
                "scope": "All accepted V2 texts; lexical similarity does not establish causal attribution.",
            },
            {
                "id": "reference_breadth",
                "confidence": "VERIFIED",
                "claim": "The October guidance deliberately demonstrates four named setting families and its template asks for background depth, lived-in signs, imperfections, and lighting. Workbook column A contains additional outdoor/urban, healthcare, gaming, retail/craft, kitchen, bedroom, library, studio, café, and office examples. V2 has some café and creative-studio indicators but no outdoor/urban, healthcare, or gaming indicators in accepted text.",
                "scope": "Lexical indicators over 10 guidance examples, 58 workbook scenes, and 592 V2 prompts; corpora serve different product/task constraints.",
            },
            {
                "id": "reference_element_gap",
                "confidence": "VERIFIED",
                "claim": "Plants/greenery and windows appear in 0/592 accepted V2 prompts, versus 9/10 and 4/10 October examples and 11/58 and 22/58 workbook scenes. This is a measured corpus difference, not by itself a recommendation to add those elements to tight camera prompts.",
                "scope": "Lexical presence only.",
            },
            {
                "id": "downstream_homogenization",
                "confidence": "VERIFIED",
                "claim": "In the bounded downstream snapshot, the rewrite adds a common rendering scaffold to nearly every accessible row: shallow depth of field, flush placement, and no-occlusion language occur in every usedPrompt despite being absent from every raw accepted prompt; soft cool daylight and teal-cyan grading are also frequent additions.",
                "scope": "Incomplete and laptop-heavy downstream snapshot; counts and exact sample are stored in downstream_used_prompt_snapshot.",
            },
        ],
        "design_relevant_evidence_not_prompt_authorship": [
            "Measure diversity at the bank level as well as per prompt; individually valid prompts can still form a repetitive bank.",
            "Keep camera-density constraints stratified in evaluation because tight, medium, and wide prompts have different legitimate scene-detail ceilings.",
            "Track environment/subsetting, surface, prop bundle, lighting phrase, and opening construction separately; changing one dimension does not establish overall diversity.",
            "Evaluate raw writer output separately from downstream usedPrompt because the endpoint adds its own repeated composition, lighting, background, and prop language.",
            "Treat source relevance as a constraint and a stratum, not as a claim that all diversity limitations originate in source messaging.",
        ],
        "caveats": [
            "The lexical taxonomies are transparent indicators, not a human semantic annotation set. They can miss synonyms and count a term used in a negation.",
            "October guidance and workbook scenes are broader creative references. Many include people, target products, secondary hardware, rich backgrounds, or explicit camera/style instructions that camera-V2 intentionally omits or restricts.",
            "The 592-prompt denominator weights each generated prompt, so sources that yielded more prompts contribute more rows. Per-source counts are retained to expose that weighting.",
            "Camera profiles deliberately constrain tight views; corpus-level plant/window absence and prop concentration should not be interpreted without the by-framing evidence.",
            "Downstream generation was still active at snapshot time. The saved sample is strongly laptop-heavy and cannot establish printer rewrite prevalence.",
            "Jaccard similarity is lexical and bag-of-words; it does not measure visual diversity or semantic equivalence.",
            "No image pixels were reviewed in this bounded audit.",
        ],
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)
    print(sha(OUTPUT))


if __name__ == "__main__":
    main()
