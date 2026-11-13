#!/usr/bin/env python3
"""Build a like-for-like distribution comparison for frozen V5 and V6 top-96 sets."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
HERE = Path(__file__).resolve().parent
V5 = (
    PROJECT
    / "eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028/data/prompts_top6_96.json"
)
V6 = (
    PROJECT
    / "eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/revisions/v6-approved-20261029-final-r44/exports/final/prompts_top6_96.json"
)
V6_ALL = (
    PROJECT
    / "eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/revisions/v6-approved-20261029-final-r44/exports/final/prompts_all_160.json"
)
SOURCE_INPUTS = (
    PROJECT
    / "eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/revisions/v6-approved-20261029-final-r44/inputs"
)
V41_ANALYSIS = (
    PROJECT
    / "local_data/reports/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/downloads/analysis.json"
)
V41_HELPERS = (
    PROJECT
    / "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/build_analysis.py"
)
V6_PROP_RECORDS = HERE / "inputs/v6_preview_prop_records.json"
V6_PROP_CATALOG = (
    PROJECT
    / "research/source_messaging_v1_to_v6/versions/v6/approved-20261029-r2.catalog.json"
)
DOWNSTREAM_ADDITIONS = HERE / "downstream_prop_additions_audit.json"
TEMPLATE = HERE / "template"
DEFAULT_OUTPUT = HERE / "built"
VERSIONS = ("V5", "V6")

PROP_FEEDBACK = [
    {"label": "Open notebook", "reported_share": "~30%", "approximate_count": 29},
    {"label": "Stack of papers", "reported_share": "~16%", "approximate_count": 15},
    {"label": "Pencil/pen cup", "reported_share": "~16%", "approximate_count": 15},
]

PROP_SIGNAL_PATTERNS = {
    "Open notebook": re.compile(
        r"\bopen(?:ed)?\b(?:(?![.!?]).){0,35}\b(?:paper|exercise|spiral)?\s*notebooks?\b|"
        r"\bnotebooks?\b(?:(?![.!?]).){0,30}\bopen\b",
        re.IGNORECASE,
    ),
    "Stack of papers": re.compile(
        r"\bstack(?:ed)?\b(?:(?![.!?]).){0,45}\bpapers?\b|"
        r"\bpapers?\b(?:(?![.!?]).){0,35}\bstack(?:ed)?\b",
        re.IGNORECASE,
    ),
    "Pencil/pen cup": re.compile(
        r"\b(?:pen|pencil)\s+cup\b|\bcup\s+of\s+(?:pens|pencils)\b|"
        r"\b(?:pen|pencil)\s+holder\b|\bholder\s+(?:with|of)\s+(?:pens|pencils)\b",
        re.IGNORECASE,
    ),
}


def load_helpers():
    spec = importlib.util.spec_from_file_location(
        "v41_distribution_helpers", V41_HELPERS
    )
    if not spec or not spec.loader:
        raise RuntimeError("Cannot load V4.1 analysis helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


H = load_helpers()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entropy(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    return round(
        -sum(
            (value / total) * math.log2(value / total)
            for value in counts.values()
            if value
        ),
        6,
    )


def histogram(values: list[float], edges: list[float]) -> list[dict[str, Any]]:
    result = []
    for index, low in enumerate(edges[:-1]):
        high = edges[index + 1]
        count = sum(
            low <= value <= high if index == len(edges) - 2 else low <= value < high
            for value in values
        )
        result.append({"label": f"{low:g}-{high:g}", "count": count})
    return result


def document_total(row: dict[str, Any], document: str) -> int:
    return int(
        sum(
            int(value)
            for value in (row.get("score_components") or {}).get(document, {}).values()
        )
    )


def entity_category(label: str) -> str:
    normalized = label.casefold()
    if re.search(r"\b(laptop|printer|computer|device)\b", normalized):
        return "primary_device"
    if re.search(
        r"\b(?:desk|table|worktable|work surface|counter|bench|credenza|console table)\b",
        normalized,
    ) and not re.search(r"\b(?:calendar|chair|lamp|ornament|supplies)\b", normalized):
        return "support_surface"
    if re.search(
        r"\b(?:walls?|windows?|partitions?|meeting rooms?|rooms?|workspaces?)\b",
        normalized,
    ):
        return "architecture_or_setting"
    return "prop_or_furnishing"


def prompt_keys_matching(
    records: list[dict[str, Any]], field: str, pattern: re.Pattern[str]
) -> list[str]:
    return sorted(
        record["prompt_key"] for record in records if pattern.search(record[field])
    )


def build_upstream_prop_usage(
    prompt_rows: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
    *,
    key_field: str,
    prop_field: str,
    text_field: str,
) -> dict[str, Any]:
    total = len(prompt_rows)
    upstream_keys: dict[str, set[str]] = defaultdict(set)
    group_keys: dict[str, set[str]] = defaultdict(set)
    group_ids: dict[str, set[str]] = defaultdict(set)
    for row in prompt_rows:
        prompt_key = row[key_field]
        for prop_id in row[prop_field]:
            entry = catalog.get(prop_id)
            if entry is None:
                raise ValueError(f"Unknown approved prop ID: {prop_id}")
            upstream_keys[prop_id].add(prompt_key)
            for group in entry["repetition_groups"]:
                group_keys[group].add(prompt_key)
                group_ids[group].add(prop_id)

    upstream_props = []
    for prop_id, keys in upstream_keys.items():
        entry = catalog[prop_id]
        upstream_props.append(
            {
                "prop_id": prop_id,
                "name": entry["name"],
                "environment": entry["environment"],
                "role": entry["role"],
                "repetition_groups": entry["repetition_groups"],
                "prompt_count": len(keys),
                "prompt_share": round(len(keys) / total, 6),
                "prompt_keys": sorted(keys),
            }
        )
    upstream_props.sort(
        key=lambda item: (-item["prompt_count"], item["name"], item["prop_id"])
    )

    semantic_groups = [
        {
            "group": group,
            "prompt_count": len(keys),
            "prompt_share": round(len(keys) / total, 6),
            "prop_ids": sorted(group_ids[group]),
            "prompt_keys": sorted(keys),
        }
        for group, keys in group_keys.items()
    ]
    semantic_groups.sort(key=lambda item: (-item["prompt_count"], item["group"]))

    group_signal = {
        "Open notebook": group_keys.get("notebook", set()),
        "Stack of papers": group_keys.get("paper_documents", set()),
        "Pencil/pen cup": set(),
    }
    signals = []
    for label, pattern in PROP_SIGNAL_PATTERNS.items():
        explicit_keys = prompt_keys_matching(prompt_rows, text_field, pattern)
        declared_keys = sorted(group_signal[label])
        signals.append(
            {
                "label": label,
                "declared_group_count": len(declared_keys),
                "declared_group_share": round(len(declared_keys) / total, 6),
                "explicit_input_phrase_count": len(explicit_keys),
                "explicit_input_phrase_share": round(len(explicit_keys) / total, 6),
                "declared_prompt_keys": declared_keys,
                "explicit_input_prompt_keys": explicit_keys,
            }
        )

    return {
        "prompt_count": total,
        "headline": {
            "unique_approved_prop_ids_used": len(upstream_props),
            "approved_prop_assignments": sum(
                len(row[prop_field]) for row in prompt_rows
            ),
            "unique_semantic_groups_used": len(semantic_groups),
        },
        "environment_counts": dict(
            sorted(Counter(row["environment"] for row in prompt_rows).items())
        ),
        "feedback_signals": signals,
        "upstream_props": upstream_props,
        "semantic_groups": semantic_groups,
    }


def build_prop_usage(
    v6_rows: list[dict[str, Any]], v6_all_document: dict[str, Any]
) -> dict[str, Any]:
    snapshot = json.loads(V6_PROP_RECORDS.read_text(encoding="utf-8"))
    records = snapshot["rows"]
    if snapshot["row_count"] != 96 or len(records) != 96:
        raise ValueError("V6 preview prop snapshot must contain 96 rows")
    expected_keys = {row["candidate_key"] for row in v6_rows}
    actual_keys = {row["prompt_key"] for row in records}
    if expected_keys != actual_keys:
        raise ValueError(
            "V6 preview prop snapshot does not match the frozen top-96 prompt keys"
        )

    catalog_document = json.loads(V6_PROP_CATALOG.read_text(encoding="utf-8"))
    catalog = {entry["id"]: entry for entry in catalog_document["entries"]}
    full_rows = v6_all_document["prompts"]
    if len(full_rows) != 160 or len({row["prompt_key"] for row in full_rows}) != 160:
        raise ValueError("Frozen V6 full set must contain 160 unique prompts")
    banks = Counter((row["device_id"], row["camera_tag"]) for row in full_rows)
    if len(banks) != 16 or set(banks.values()) != {10}:
        raise ValueError(
            "Frozen V6 full set must contain 16 banks with ten prompts each"
        )
    full_160 = build_upstream_prop_usage(
        full_rows,
        catalog,
        key_field="prompt_key",
        prop_field="prop_ids",
        text_field="text",
    )
    preview_upstream = build_upstream_prop_usage(
        records,
        catalog,
        key_field="prompt_key",
        prop_field="upstream_prop_ids",
        text_field="raw_prompt",
    )

    downstream_keys: dict[str, set[str]] = defaultdict(set)
    downstream_descriptions: dict[str, set[str]] = defaultdict(set)
    for record in records:
        for entity in record["rewritten_entities"]:
            label = " ".join(entity.get("label", "").split()).casefold()
            if not label:
                continue
            downstream_keys[label].add(record["prompt_key"])
            if entity.get("description"):
                downstream_descriptions[label].add(
                    " ".join(entity["description"].split())
                )
    downstream_entities = [
        {
            "label": label,
            "category": entity_category(label),
            "image_count": len(keys),
            "image_share": round(len(keys) / 96, 6),
            "example_description": (
                sorted(downstream_descriptions[label])[0]
                if downstream_descriptions[label]
                else ""
            ),
            "prompt_keys": sorted(keys),
        }
        for label, keys in downstream_keys.items()
    ]
    downstream_entities.sort(key=lambda item: (-item["image_count"], item["label"]))

    signal_rows = []
    upstream_signals = {
        item["label"]: item for item in preview_upstream["feedback_signals"]
    }
    for feedback in PROP_FEEDBACK:
        label = feedback["label"]
        rewrite_keys = prompt_keys_matching(
            records, "rewritten_search_text", PROP_SIGNAL_PATTERNS[label]
        )
        upstream_signal = upstream_signals[label]
        signal_rows.append(
            {
                **feedback,
                "declared_group_count": upstream_signal["declared_group_count"],
                "declared_group_share": upstream_signal["declared_group_share"],
                "explicit_input_phrase_count": upstream_signal[
                    "explicit_input_phrase_count"
                ],
                "explicit_input_phrase_share": upstream_signal[
                    "explicit_input_phrase_share"
                ],
                "explicit_rewrite_phrase_count": len(rewrite_keys),
                "explicit_rewrite_phrase_share": round(len(rewrite_keys) / 96, 6),
                "declared_prompt_keys": upstream_signal["declared_prompt_keys"],
                "explicit_input_prompt_keys": upstream_signal[
                    "explicit_input_prompt_keys"
                ],
                "explicit_rewrite_prompt_keys": rewrite_keys,
            }
        )

    additions = json.loads(DOWNSTREAM_ADDITIONS.read_text(encoding="utf-8"))
    return {
        "scope": {
            "all_prompt_rows": 160,
            "banks": 16,
            "prompts_per_bank": 10,
            "generated_preview_rows": 96,
            "rows_without_downstream_rewrite": 64,
        },
        "method": {
            "full_160": "Exact approved prop IDs and semantic repetition groups attached to all 160 frozen V6 prompts. Each ID or group counts at most once per prompt.",
            "preview_96": "The selected 96 generated preview rows add exact Gemini 3.1 Pro stage1Output entity labels and the manually audited rewrite-addition trace.",
            "signals": "Input and rewrite phrase counts use sentence-bounded semantic patterns. For example, stack of plain papers and stack of household papers both count as stack-of-papers mentions.",
            "manual_feedback": "Approximate visual-image prevalence supplied by C-Tech feedback; these figures were not independently re-annotated in this report.",
        },
        "full_160": full_160,
        "preview_96": {
            "scope": {
                "image_rows": 96,
                "completed_rows": 96,
                "source_gallery_url": snapshot["source_gallery_url"],
                "source_snapshot_path": str(V6_PROP_RECORDS),
                "source_snapshot_sha256": sha256(V6_PROP_RECORDS),
                "source_results_jsonl": snapshot["source_results_jsonl"],
            },
            "headline": {
                **preview_upstream["headline"],
                "unique_rewriter_entity_labels": len(downstream_entities),
            },
            "feedback_comparison": signal_rows,
            "upstream_props": preview_upstream["upstream_props"],
            "semantic_groups": preview_upstream["semantic_groups"],
            "downstream_entities": downstream_entities,
        },
        "downstream_additions": additions,
    }


def normalize(version: str, source: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in source["prompts"]:
        candidate_key = item["prompt_key"]
        if version == "V5":
            prop_ids = []
            prop_labels = list(
                (item.get("visual_signature") or {}).get("local_props") or []
            )
            source_revision = "v5-reviewed-top6"
        else:
            prop_ids = list(item.get("prop_ids") or [])
            prop_labels = []
            source_revision = item.get("source_revision")
        rows.append(
            {
                "version": version,
                "versioned_key": f"{version}::{candidate_key}",
                "candidate_key": candidate_key,
                "device_id": item["device_id"],
                "device_display_name": item["device_display_name"],
                "device_type": item["device_type"],
                "source_pair": item["source_pair"],
                "camera_tag": item["camera_tag"],
                "source_camera_name": item["source_camera_name"],
                "view_role": item["view_role"],
                "bank_rank": int(item["bank_rank"]),
                "environment": item["environment"],
                "subsetting": item.get("subsetting") or "",
                "text": item["text"],
                "source_relevance_score": int(item["source_relevance_score"]),
                "ctech_reference_score": int(item["ctech_reference_score"]),
                "ctech_reference_id": item["ctech_reference_id"],
                "source_relationship": item.get("relationship") or "",
                "source_explanation": item.get("explanation") or "",
                "ctech_explanation": item.get("ctech_explanation") or "",
                "camera_fit_explanation": item.get("camera_fit_explanation") or "",
                "source_evidence": item.get("evidence")
                or item.get("evidence_ids")
                or [],
                "creative_departures": item.get("creative_departures") or [],
                "camera_omissions": item.get("camera_omissions") or [],
                "score_components": item.get("score_components") or {},
                "smart_brief_support_total": document_total(item, "smart_brief"),
                "source_messaging_support_total": document_total(
                    item, "source_messaging"
                ),
                "prop_ids": prop_ids,
                "prop_labels": prop_labels,
                "prop_count": len(prop_ids) if prop_ids else len(prop_labels),
                "source_revision": source_revision,
                "word_count": len(H.words(item["text"])),
                "sentence_count": len(H.sentences(item["text"])),
            }
        )
    if len(rows) != 96 or len({row["candidate_key"] for row in rows}) != 96:
        raise ValueError(f"{version} must contain 96 unique prompt keys")
    banks = Counter((row["device_id"], row["camera_tag"]) for row in rows)
    if len(banks) != 16 or set(banks.values()) != {6}:
        raise ValueError(f"{version} must contain 16 banks with six prompts each")
    return rows


def summarize(version: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    environments = dict(sorted(Counter(row["environment"] for row in rows).items()))
    devices = dict(sorted(Counter(row["device_id"] for row in rows).items()))
    views = dict(sorted(Counter(row["view_role"] for row in rows).items()))
    source_values = [row["source_relevance_score"] for row in rows]
    ctech_values = [row["ctech_reference_score"] for row in rows]
    measured = [row["measured_ctech_similarity"] for row in rows]
    lexical = H.lexical_audit(
        [{**row, "candidate_key": row["versioned_key"]} for row in rows]
    )
    prop_counts = [row["prop_count"] for row in rows]
    prop_frequency = Counter(
        prop for row in rows for prop in (row["prop_ids"] or row["prop_labels"])
    )
    support = {
        "both_documents_nonzero": sum(
            row["smart_brief_support_total"] > 0
            and row["source_messaging_support_total"] > 0
            for row in rows
        ),
        "smart_brief_only": sum(
            row["smart_brief_support_total"] > 0
            and row["source_messaging_support_total"] == 0
            for row in rows
        ),
        "source_messaging_only": sum(
            row["smart_brief_support_total"] == 0
            and row["source_messaging_support_total"] > 0
            for row in rows
        ),
        "neither_document": sum(
            row["smart_brief_support_total"] == 0
            and row["source_messaging_support_total"] == 0
            for row in rows
        ),
    }
    return {
        "version": version,
        "count": len(rows),
        "distinct_text_count": len({" ".join(row["text"].split()) for row in rows}),
        "exact_duplicate_groups": lexical["exact_duplicate_groups"],
        "canonical_duplicate_groups": lexical["canonical_duplicate_groups"],
        "environment_counts": environments,
        "environment_entropy": entropy(environments),
        "device_counts": devices,
        "view_counts": views,
        "source_score": {
            "mean": round(float(np.mean(source_values)), 3),
            "quantiles": H.quantiles(source_values),
            "histogram": histogram(source_values, list(range(0, 101, 10))),
        },
        "declared_ctech_score": {
            "mean": round(float(np.mean(ctech_values)), 3),
            "quantiles": H.quantiles(ctech_values),
            "histogram": histogram(ctech_values, list(range(0, 101, 10))),
        },
        "measured_ctech_similarity": {
            "mean": round(float(np.mean(measured)), 6),
            "quantiles": H.quantiles(measured),
            "histogram": H.similarity_hist(np.asarray(measured)),
        },
        "word_count": {
            "mean": round(float(np.mean([row["word_count"] for row in rows])), 3),
            "quantiles": H.quantiles([row["word_count"] for row in rows]),
        },
        "sentence_count": {
            "mean": round(float(np.mean([row["sentence_count"] for row in rows])), 3),
            "quantiles": H.quantiles([row["sentence_count"] for row in rows]),
        },
        "prop_count": {
            "mean": round(float(np.mean(prop_counts)), 3),
            "quantiles": H.quantiles(prop_counts),
            "zero_prop_prompts": sum(value == 0 for value in prop_counts),
        },
        "prop_frequency": [
            {"label": key, "count": value}
            for key, value in prop_frequency.most_common(30)
        ],
        "document_support": support,
        "recurring_phrases": lexical["recurring_phrases"][:30],
        "closest_lexical_pairs": lexical["closest_pairs"][:20],
        "similarity_by_environment": H.grouped(
            rows, "environment", "measured_ctech_similarity"
        ),
        "similarity_by_view": H.grouped(rows, "view_role", "measured_ctech_similarity"),
    }


def build(output: Path, cache_dir: Path) -> dict[str, Any]:
    v5_document = json.loads(V5.read_text(encoding="utf-8"))
    v6_document = json.loads(V6.read_text(encoding="utf-8"))
    v6_all_document = json.loads(V6_ALL.read_text(encoding="utf-8"))
    baseline = json.loads(V41_ANALYSIS.read_text(encoding="utf-8"))
    refs = baseline["references"]
    rows = normalize("V5", v5_document) + normalize("V6", v6_document)
    source_pairs: dict[str, dict[str, Any]] = {}
    input_by_bank = {path.stem: path for path in SOURCE_INPUTS.glob("*.json")}
    for row in rows:
        bank = f"{row['device_id']}__{row['camera_tag']}"
        path = input_by_bank.get(bank)
        if path is None:
            raise ValueError(f"Missing frozen dual-source input for {bank}")
        document = json.loads(path.read_text(encoding="utf-8"))
        entry = {
            "smart_brief": document["smart_brief"],
            "source_messaging": document["source_messaging"],
            "input_files": [{"path": str(path), "sha256": sha256(path)}],
        }
        prior = source_pairs.get(row["source_pair"])
        if prior is not None:
            if (prior["smart_brief"], prior["source_messaging"]) != (
                entry["smart_brief"],
                entry["source_messaging"],
            ):
                raise ValueError(
                    f"Source documents differ within source pair {row['source_pair']}"
                )
            if not any(item["path"] == str(path) for item in prior["input_files"]):
                prior["input_files"].append({"path": str(path), "sha256": sha256(path)})
        else:
            source_pairs[row["source_pair"]] = entry
    texts = [row["text"] for row in rows]
    ref_texts = [ref["scope_adjusted_text"] for ref in refs]
    embeddings, model_meta = H.embed(texts + ref_texts, cache_dir)
    prompt_embeddings = embeddings[: len(rows)]
    ref_embeddings = embeddings[len(rows) :]
    similarity = prompt_embeddings @ ref_embeddings.T
    nearest_idx = similarity.argmax(axis=1)
    nearest_value = similarity.max(axis=1)
    pairwise = prompt_embeddings @ prompt_embeddings.T
    np.fill_diagonal(pairwise, -np.inf)
    nearest_prompt_idx = pairwise.argmax(axis=1)
    nearest_prompt_value = pairwise.max(axis=1)
    coordinates, explained = H.pca_2d(np.vstack([prompt_embeddings, ref_embeddings]))

    for index, row in enumerate(rows):
        nearest_ref = refs[int(nearest_idx[index])]
        nearest_prompt = rows[int(nearest_prompt_idx[index])]
        row.update(
            {
                "measured_ctech_similarity": round(float(nearest_value[index]), 6),
                "measured_ctech_reference_id": nearest_ref["reference_id"],
                "declared_reference_similarity": round(
                    float(
                        similarity[
                            index,
                            next(
                                i
                                for i, ref in enumerate(refs)
                                if ref["reference_id"] == row["ctech_reference_id"]
                            ),
                        ]
                    ),
                    6,
                ),
                "nearest_prompt_similarity": round(
                    float(nearest_prompt_value[index]), 6
                ),
                "nearest_prompt_key": nearest_prompt["versioned_key"],
                "map_x": round(float(coordinates[index, 0]), 6),
                "map_y": round(float(coordinates[index, 1]), 6),
            }
        )

    by_version = {
        version: [row for row in rows if row["version"] == version]
        for version in VERSIONS
    }
    summaries = {
        version: summarize(version, by_version[version]) for version in VERSIONS
    }
    prop_usage = build_prop_usage(by_version["V6"], v6_all_document)
    reference_map = [
        {
            **ref,
            "map_x": round(float(coordinates[len(rows) + index, 0]), 6),
            "map_y": round(float(coordinates[len(rows) + index, 1]), 6),
        }
        for index, ref in enumerate(refs)
    ]
    reference_coverage = {}
    for version in VERSIONS:
        version_rows = by_version[version]
        counts = Counter(row["measured_ctech_reference_id"] for row in version_rows)
        declared = Counter(row["ctech_reference_id"] for row in version_rows)
        reference_coverage[version] = [
            {
                "reference_id": ref["reference_id"],
                "group": ref["group"],
                "original_text": ref["original_text"],
                "scope_adjusted_text": ref["scope_adjusted_text"],
                "nearest_count": counts[ref["reference_id"]],
                "declared_count": declared[ref["reference_id"]],
            }
            for ref in refs
        ]

    analysis = {
        "version": "hp-lifestyle-v5-v6-top96-distribution-comparison-v3",
        "as_of": "2026-11-03",
        "status": "frozen_text_comparison_with_full_v6_prompt_and_preview_rewrite_audit",
        "scope": {
            "versions": list(VERSIONS),
            "prompt_count_per_version": 96,
            "total_prompt_rows": 192,
            "banks_per_version": 16,
            "prompts_per_bank": 6,
            "ctech_reference_count": len(refs),
        },
        "inputs": {
            "v5_top96": {"path": str(V5), "sha256": sha256(V5)},
            "v6_top96": {"path": str(V6), "sha256": sha256(V6)},
            "v6_all160": {"path": str(V6_ALL), "sha256": sha256(V6_ALL)},
            "v4_1_reference_analysis": {
                "path": str(V41_ANALYSIS),
                "sha256": sha256(V41_ANALYSIS),
            },
            "v6_preview_prop_records": {
                "path": str(V6_PROP_RECORDS),
                "sha256": sha256(V6_PROP_RECORDS),
            },
            "v6_approved_prop_catalog": {
                "path": str(V6_PROP_CATALOG),
                "sha256": sha256(V6_PROP_CATALOG),
            },
            "v6_downstream_additions_audit": {
                "path": str(DOWNSTREAM_ADDITIONS),
                "sha256": sha256(DOWNSTREAM_ADDITIONS),
            },
        },
        "methods": {
            "semantic_embedding": model_meta,
            "map": {
                "method": "Joint PCA over 192 V5/V6 prompts and 18 C-Tech reference embeddings",
                "explained_variance_ratio_first_two": explained,
            },
            "measured_ctech_similarity": "Maximum cosine similarity to the same 18 normalized C-Tech references used by the established V4.1/V5 analyses.",
            "selection": "Frozen source-ranked top six from each of the same 16 device/camera banks.",
        },
        "summaries": summaries,
        "v6_prop_audit": prop_usage,
        "prop_usage": prop_usage["preview_96"],
        "source_pairs": source_pairs,
        "reference_coverage": reference_coverage,
        "references": reference_map,
        "rows": rows,
        "v4_1": {
            "comparable_96_exists": False,
            "canonical_prompt_count": 120,
            "reason": "V4.1 has four 30-prompt banks and a different ranking contract; a 96-row slice would be arbitrary.",
            "report_url": "https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/gallery/index.html",
        },
        "limitations": [
            "The report compares the frozen selected 96 rows for each version; it does not compare full candidate-bank distributions.",
            "V5 and V6 share the same device/source/camera bank design, but their text generation and review histories differ.",
            "Semantic proximity is descriptive text similarity and is not a calibrated acceptance threshold or an image-quality metric.",
            "V5 prop labels come from visual_signature.local_props; V6 prop identities come from its approved prop IDs, so cross-version prop counts are directional rather than ontology-identical.",
            "Prop-frequency tables count requested or rewritten text entities. They do not use computer vision and therefore do not prove that an object is visibly present in the generated pixels.",
            "The three C-Tech percentages are approximate manual visual feedback supplied after generation and are shown as reported, without independent image re-annotation.",
            "All 160 V6 prompts have approved-prop and input-text data, but only the selected 96 generated previews have downstream Gemini rewrite/debug data. The remaining 64 are never assigned rewrite counts.",
            "Downstream rewrite additions are a manual semantic audit of prompt/debug text, not computer-vision detections in generated images.",
            "No arbitrary 96-row V4.1 subset was created; its canonical 120-prompt report is linked separately.",
        ],
    }

    downloads = output / "downloads"
    gallery = output / "gallery"
    downloads.mkdir(parents=True, exist_ok=True)
    gallery.mkdir(parents=True, exist_ok=True)
    (downloads / "analysis.json").write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (downloads / "v6_prop_usage.json").write_text(
        json.dumps(prop_usage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    shutil.copyfile(V5, downloads / "v5_prompts_top6_96.json")
    shutil.copyfile(V6, downloads / "v6_prompts_top6_96.json")
    shutil.copyfile(V6_ALL, downloads / "v6_prompts_all_160.json")
    shutil.copyfile(
        DOWNSTREAM_ADDITIONS, downloads / "downstream_prop_additions_audit.json"
    )
    with (downloads / "v6_prop_usage.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        fieldnames = [
            "scope",
            "source",
            "item",
            "item_id",
            "environment_or_category",
            "prompt_count",
            "prompt_share",
        ]
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for item in prop_usage["full_160"]["upstream_props"]:
            writer.writerow(
                {
                    "scope": "all_160_v6_prompts",
                    "source": "v6_declared_approved_prop",
                    "item": item["name"],
                    "item_id": item["prop_id"],
                    "environment_or_category": item["environment"],
                    "prompt_count": item["prompt_count"],
                    "prompt_share": item["prompt_share"],
                }
            )
        for item in prop_usage["full_160"]["semantic_groups"]:
            writer.writerow(
                {
                    "scope": "all_160_v6_prompts",
                    "source": "v6_declared_semantic_group",
                    "item": item["group"],
                    "item_id": "|".join(item["prop_ids"]),
                    "environment_or_category": "repetition_group",
                    "prompt_count": item["prompt_count"],
                    "prompt_share": item["prompt_share"],
                }
            )
        for item in prop_usage["preview_96"]["downstream_entities"]:
            writer.writerow(
                {
                    "scope": "generated_preview_96",
                    "source": "gemini_stage1_entity_label",
                    "item": item["label"],
                    "item_id": "",
                    "environment_or_category": item["category"],
                    "prompt_count": item["image_count"],
                    "prompt_share": item["image_share"],
                }
            )
    with (downloads / "candidate_metrics.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        fieldnames = list(rows[0])
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: (
                        json.dumps(value, ensure_ascii=False)
                        if isinstance(value, (dict, list))
                        else value
                    )
                    for key, value in row.items()
                }
            )
    (gallery / "data.js").write_text(
        "const ANALYSIS="
        + json.dumps(analysis, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    for name in ("index.html", "report.js", "style.css", "imsauth.js"):
        shutil.copyfile(TEMPLATE / name, gallery / name)
    manifest = {
        "version": "hp-lifestyle-v5-v6-top96-distribution-build-v3",
        "output": str(output),
        "inputs": analysis["inputs"],
        "counts": analysis["scope"],
        "artifacts": {},
    }
    manifest_path = output / "build_manifest.json"
    for path in sorted(
        item for item in output.rglob("*") if item.is_file() and item != manifest_path
    ):
        manifest["artifacts"][str(path.relative_to(output))] = {
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("/mnt/localssd/hp_lifestyle_pipeline/cache/huggingface"),
    )
    args = parser.parse_args()
    print(json.dumps(build(args.output.resolve(), args.cache_dir.resolve()), indent=2))
