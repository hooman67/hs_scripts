#!/usr/bin/env python3
"""Build the V5 dual-source report in the established V4.1 report format."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
EVAL = PROJECT / "eval_sets/hp_lifestyle_dual_source_v5_pilot_20261027"
REVIEW_DATA = EVAL / "data/review_data.json"
REVIEWED_CASES = EVAL / "reviewed_prompt_cases.json"
SCORING_POLICY = EVAL / "review_scoring_policy.json"
SYSTEM_PROMPT = EVAL / "runtime/system_prompt.md"
V41_ANALYSIS = PROJECT / "local_data/reports/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/downloads/analysis.json"
V41_HELPERS = PROJECT / "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/build_analysis.py"
TEMPLATE = EVAL / "distribution_analysis_v1/gallery"
DEFAULT_OUTPUT = EVAL / "distribution_analysis_v1/built"


def load_helpers():
    spec = importlib.util.spec_from_file_location("v41_analysis_helpers", V41_HELPERS)
    if not spec or not spec.loader:
        raise RuntimeError("could not load V4.1 analysis helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


H = load_helpers()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def histogram_0_100(values: list[int]) -> list[dict[str, Any]]:
    rows = []
    for low in range(0, 100, 10):
        high = 100 if low == 90 else low + 10
        rows.append({"label": f"{low}-{high}", "count": sum(low <= value <= high if low == 90 else low <= value < high for value in values)})
    return rows


def support_total(components: dict[str, Any], document: str) -> int:
    return int(sum(int(value) for value in components.get(document, {}).values()))


def combined_component_total(components: dict[str, Any]) -> int:
    left = components.get("smart_brief", {})
    right = components.get("source_messaging", {})
    return int(sum(max(int(left.get(key, 0)), int(right.get(key, 0))) for key in ("setting", "activity", "materials", "use_context")))


def comparison_row(label: str, current: list[float], baseline: list[float]) -> dict[str, Any]:
    current_median = float(np.median(current))
    baseline_median = float(np.median(baseline))
    return {
        "label": label,
        "v5_count": len(current),
        "v4_1_count": len(baseline),
        "v5_median": round(current_median, 6),
        "v4_1_median": round(baseline_median, 6),
        "median_delta": round(current_median - baseline_median, 6),
        "v5_mean": round(float(np.mean(current)), 6),
        "v4_1_mean": round(float(np.mean(baseline)), 6),
    }


def render_text(rows: list[dict[str, Any]]) -> str:
    lines = ["HP V5 dual-source text pilot", f"Prompt count: {len(rows)}", ""]
    for row in rows:
        lines.extend([
            f"[{row['candidate_key']}]",
            f"Case: {row['case_id']}",
            f"Camera: {row['camera_tag']} ({row['view_role']})",
            f"Environment: {row['environment']} · {row['subsetting']}",
            f"Source score: {row['source_relevance_score']} · C-Tech score: {row['ctech_reference_score']}",
            row["text"],
            "",
        ])
    return "\n".join(lines)


def build(output: Path, cache_dir: Path) -> dict[str, Any]:
    if not V41_ANALYSIS.is_file():
        H.build(V41_ANALYSIS.parents[1], cache_dir)
    review = json.loads(REVIEW_DATA.read_text(encoding="utf-8"))
    reviewed_cases = json.loads(REVIEWED_CASES.read_text(encoding="utf-8"))
    policy = json.loads(SCORING_POLICY.read_text(encoding="utf-8"))
    baseline_analysis = json.loads(V41_ANALYSIS.read_text(encoding="utf-8"))
    prompts = review["rows"]
    if len(prompts) != 160 or len({row["candidate_key"] for row in prompts}) != 160:
        raise ValueError("expected 160 unique reviewed V5 prompts")
    if set(row["environment"] for row in prompts) != set(H.EXPECTED_ENVIRONMENTS):
        raise ValueError("V5 pilot must use the established six-environment taxonomy")
    if any(combined_component_total(row["source_score_components"]) != row["source_relevance_score"] for row in prompts):
        raise ValueError("source relevance does not match the equal-authority component-max rule")

    refs = baseline_analysis["references"]
    ref_by_id = {row["reference_id"]: row for row in refs}
    texts = [row["text"] for row in prompts]
    ref_texts = [row["scope_adjusted_text"] for row in refs]
    embeddings, model_meta = H.embed(texts + ref_texts, cache_dir)
    n = len(prompts)
    prompt_emb = embeddings[:n]
    ref_emb = embeddings[n:]
    similarity = prompt_emb @ ref_emb.T
    nearest_idx = similarity.argmax(axis=1)
    nearest_value = similarity.max(axis=1)
    declared_idx = np.asarray([next(i for i, ref in enumerate(refs) if ref["reference_id"] == row["ctech_reference_id"]) for row in prompts])
    declared_similarity = similarity[np.arange(n), declared_idx]
    pairwise = prompt_emb @ prompt_emb.T
    np.fill_diagonal(pairwise, -np.inf)
    nearest_candidate_idx = pairwise.argmax(axis=1)
    nearest_candidate_value = pairwise.max(axis=1)
    finite_pairs = pairwise[np.triu_indices(n, 1)]
    lexical_vectors = H.tfidf_vectors(texts + ref_texts)
    lexical_similarity = np.asarray([[H.sparse_dot(lexical_vectors[i], lexical_vectors[n + j]) for j in range(len(refs))] for i in range(n)])
    coords, explained = H.pca_2d(np.vstack([prompt_emb, ref_emb]))
    lexical = H.lexical_audit(prompts)

    rows = []
    for index, item in enumerate(prompts):
        nearest_ref = refs[int(nearest_idx[index])]
        nearest_candidate = prompts[int(nearest_candidate_idx[index])]
        rank = int(item["bank_rank_by_source"])
        components = item["source_score_components"]
        rows.append({
            **item,
            "rank": rank,
            "rank_bin": "1-6 (top selection)" if rank <= 6 else "7-10" if rank <= 10 else "11-15" if rank <= 15 else "16-20",
            "display_environment": item["environment"],
            "display_environment_rule": "native_v5_environment",
            "relationship": item["ctech_relationship"],
            "score": item["ctech_reference_score"],
            "selected": bool(item["top6_by_source_in_bank"]),
            "editorially_scene_edited": bool(item["review_text_changed"]),
            "raw_correction_candidate_id": item["review_original_r3_id"],
            "repair_normalized_candidate_id": item["review_original_r3_id"],
            "reviewed_candidate_id": item["candidate_id"],
            "raw_correction_text": item["review_original_r3_text"],
            "repair_normalized_text": item["review_original_r3_text"],
            "editorial_edits": item["review_field_edits"],
            "smart_brief_support_total": support_total(components, "smart_brief"),
            "source_messaging_support_total": support_total(components, "source_messaging"),
            "word_count": len(H.words(item["text"])),
            "sentence_count": len(H.sentences(item["text"])),
            "semantic_nearest_candidate_similarity": round(float(nearest_candidate_value[index]), 6),
            "semantic_nearest_candidate_key": nearest_candidate["candidate_key"],
            "semantic_nearest_reference_similarity_scope_adjusted": round(float(nearest_value[index]), 6),
            "semantic_nearest_reference_id_scope_adjusted": nearest_ref["reference_id"],
            "semantic_declared_reference_similarity": round(float(declared_similarity[index]), 6),
            "declared_reference_is_semantic_nearest": bool(declared_idx[index] == nearest_idx[index]),
            "lexical_nearest_reference_similarity_scope_adjusted": round(float(lexical_similarity[index].max()), 6),
            "lexical_nearest_reference_id_scope_adjusted": refs[int(lexical_similarity[index].argmax())]["reference_id"],
            "map_x": round(float(coords[index, 0]), 6),
            "map_y": round(float(coords[index, 1]), 6),
        })

    environment_counts = dict(sorted(Counter(row["environment"] for row in rows).items()))
    relationship_counts = dict(sorted(Counter(row["ctech_relationship"] for row in rows).items()))
    source_relationship_counts = dict(sorted(Counter(row["source_relationship"] for row in rows).items()))
    declared_counts = Counter(row["ctech_reference_id"] for row in rows)
    reference_coverage = []
    for index, ref in enumerate(refs):
        assigned = np.where(nearest_idx == index)[0]
        reference_coverage.append({
            **ref,
            "assigned_prompt_count": int(len(assigned)),
            "declared_prompt_count": declared_counts[ref["reference_id"]],
            "mean_assigned_similarity": round(float(np.mean(nearest_value[assigned])), 6) if len(assigned) else None,
            "maximum_similarity": round(float(similarity[:, index].max()), 6),
            "map_x": round(float(coords[n + index, 0]), 6),
            "map_y": round(float(coords[n + index, 1]), 6),
        })

    baseline_points = baseline_analysis["points"]
    comparison = []
    for label in ("all", "close_up", "wide"):
        current_values = [row["semantic_nearest_reference_similarity_scope_adjusted"] for row in rows if label == "all" or row["view_role"] == label]
        baseline_values = [row["semantic_nearest_reference_similarity_scope_adjusted"] for row in baseline_points if label == "all" or row["view_role"] == label]
        comparison.append(comparison_row(label, current_values, baseline_values))

    feedback_audits = {
        "v4_1": H.feedback_pattern_audit(baseline_points, "frozen_v4.1_pilot"),
        "v5": H.feedback_pattern_audit(rows, "reviewed_v5_dual_source_pilot"),
    }
    feedback_rows = [{
        "indicator": indicator,
        "v4_1_affected_prompt_count": feedback_audits["v4_1"]["categories"][indicator]["affected_prompt_count"],
        "v5_affected_prompt_count": feedback_audits["v5"]["categories"][indicator]["affected_prompt_count"],
    } for indicator in ("unnatural_framing_or_place_phrase", "microscopic_wear_or_story_marker")]

    case_inputs = []
    by_case = reviewed_cases["cases"]
    for case_id in sorted(by_case):
        case = by_case[case_id]
        first = next(row for row in rows if row["case_id"] == case_id)
        case_inputs.append({
            "case_id": case_id,
            "pair_id": case["pair_id"],
            "device_type": case["device_type"],
            "view_role": case["view_role"],
            "input_sha256": case["input_sha256"],
            "camera_tag": case["camera_tag"],
            "expected_camera": case["expected_camera"],
            "smart_brief": first["smart_brief"],
            "source_messaging": first["source_messaging"],
            "source_evidence": first["case_debug"].get("source_evidence", []),
            "document_assessments": first["case_debug"].get("document_assessments", []),
            "source_conflicts": first["case_debug"].get("source_conflicts", []),
        })

    # The complete dual-source inputs and case-level debug data are stored once per
    # case above. Keeping duplicate copies on all 20 points in each bank makes the
    # browser payload unnecessarily large without adding review information.
    for row in rows:
        for duplicate_field in ("smart_brief", "source_messaging", "case_debug", "candidate_debug"):
            row.pop(duplicate_field, None)

    top_rows = [row for row in rows if row["selected"]]
    all_source = [row["source_relevance_score"] for row in rows]
    top_source = [row["source_relevance_score"] for row in top_rows]
    all_ctech = [row["ctech_reference_score"] for row in rows]
    top_ctech = [row["ctech_reference_score"] for row in top_rows]
    document_support = {
        "smart_brief_mean": round(float(np.mean([row["smart_brief_support_total"] for row in rows])), 3),
        "source_messaging_mean": round(float(np.mean([row["source_messaging_support_total"] for row in rows])), 3),
        "both_documents_nonzero_count": sum(row["smart_brief_support_total"] > 0 and row["source_messaging_support_total"] > 0 for row in rows),
        "smart_brief_only_count": sum(row["smart_brief_support_total"] > 0 and row["source_messaging_support_total"] == 0 for row in rows),
        "source_messaging_only_count": sum(row["smart_brief_support_total"] == 0 and row["source_messaging_support_total"] > 0 for row in rows),
        "neither_document_count": sum(row["smart_brief_support_total"] == 0 and row["source_messaging_support_total"] == 0 for row in rows),
    }

    analysis = {
        "version": "hp-v5-dual-source-distribution-analysis-v2",
        "as_of": "2026-10-27",
        "status": "root_reviewed_text_pilot_no_v5_images_generated",
        "scope": {"prompt_count": n, "case_count": len(case_inputs), "source_pair_count": len({row["pair_id"] for row in rows}), "reference_prompt_count": len(refs), "baseline_prompt_count": len(baseline_points)},
        "inputs": {
            "review_data": {"path": str(REVIEW_DATA), "sha256": sha256(REVIEW_DATA)},
            "reviewed_prompt_cases": {"path": str(REVIEWED_CASES), "sha256": sha256(REVIEWED_CASES)},
            "scoring_policy": {"path": str(SCORING_POLICY), "sha256": sha256(SCORING_POLICY)},
            "system_prompt": {"path": str(SYSTEM_PROMPT), "sha256": sha256(SYSTEM_PROMPT)},
            "v4_1_baseline_analysis": {"path": str(V41_ANALYSIS), "sha256": sha256(V41_ANALYSIS)},
        },
        "methods": {
            "semantic_embedding": model_meta,
            "reference_normalization": baseline_analysis["methods"]["reference_normalization"],
            "lexical_reference_similarity": baseline_analysis["methods"]["lexical_reference_similarity"],
            "map": {"method": f"PCA of {n} reviewed V5 prompts plus {len(refs)} normalized C-Tech reference embeddings", "explained_variance_ratio_first_two": explained},
            "source_score": policy,
        },
        "headline": {
            "exact_duplicate_prompt_groups": len(lexical["exact_duplicate_groups"]),
            "canonical_duplicate_prompt_groups": len(lexical["canonical_duplicate_groups"]),
            "exact_normalized_ctech_reference_matches": sum(row["text"] == ref_by_id[row["ctech_reference_id"]]["scope_adjusted_text"] for row in rows),
            "display_environment_counts": environment_counts,
            "display_environment_entropy": H.entropy(environment_counts),
            "relationship_counts": relationship_counts,
            "source_relationship_counts": source_relationship_counts,
            "semantic_pairwise_similarity_quantiles": H.quantiles(finite_pairs.tolist()),
            "semantic_nearest_neighbor_similarity_quantiles": H.quantiles(nearest_candidate_value.tolist()),
            "semantic_nearest_reference_scope_adjusted_quantiles": H.quantiles(nearest_value.tolist()),
            "semantic_declared_reference_similarity_quantiles": H.quantiles(declared_similarity.tolist()),
            "lexical_nearest_reference_scope_adjusted_quantiles": H.quantiles(lexical_similarity.max(axis=1).tolist()),
            "declared_reference_is_semantic_nearest_count": int(np.sum(declared_idx == nearest_idx)),
            "declared_reference_is_semantic_nearest_rate": round(float(np.mean(declared_idx == nearest_idx)), 6),
            "prompt_word_count_quantiles": H.quantiles([len(H.words(text)) for text in texts]),
            "source_relevance_mean": round(float(np.mean(all_source)), 3),
            "ctech_reference_score_mean": round(float(np.mean(all_ctech)), 3),
        },
        "distributions": {
            "display_environment": environment_counts,
            "canonical_environment": environment_counts,
            "relationship": relationship_counts,
            "source_relationship": source_relationship_counts,
            "score_histogram": histogram_0_100(all_ctech),
            "source_score_histogram": histogram_0_100(all_source),
            "reference_similarity_histogram_scope_adjusted": H.similarity_hist(nearest_value),
            "reference_similarity_by_display_environment": H.grouped(rows, "display_environment", "semantic_nearest_reference_similarity_scope_adjusted"),
            "reference_similarity_by_relationship": H.grouped(rows, "ctech_relationship", "semantic_nearest_reference_similarity_scope_adjusted"),
            "reference_similarity_by_view": H.grouped(rows, "view_role", "semantic_nearest_reference_similarity_scope_adjusted"),
            "reference_similarity_by_rank_bin": H.grouped(rows, "rank_bin", "semantic_nearest_reference_similarity_scope_adjusted"),
            "declared_reference": dict(sorted(declared_counts.items())),
        },
        "selection_analysis": {
            "full": {"count": n, "source_mean": round(float(np.mean(all_source)), 3), "ctech_mean": round(float(np.mean(all_ctech)), 3), "measured_ctech_mean": round(float(np.mean(nearest_value)), 6)},
            "top6": {"count": len(top_rows), "source_mean": round(float(np.mean(top_source)), 3), "ctech_mean": round(float(np.mean(top_ctech)), 3), "measured_ctech_mean": round(float(np.mean([row["semantic_nearest_reference_similarity_scope_adjusted"] for row in top_rows])), 6)},
            "document_support": document_support,
        },
        "v4_1_baseline_comparison": comparison,
        "review_accounting": {
            "pilot_status": "root_reviewed_editorial_pilot_not_raw_model_success",
            "review_disclosure": review["review_disclosure"],
            "reviewed_candidate_count": n,
            "editorially_scene_edited_candidate_count": review["review_counts"]["scene_texts_edited"],
            "field_edit_count": review["review_counts"]["field_edits"],
            "model_normalized_validation_passes": review["review_counts"]["model_normalized_validation_passes"],
            "reviewed_validation_passes": review["review_counts"]["reviewed_validation_passes"],
            "bank_count": review["bank_count"],
        },
        "feedback_pattern_comparison": {"interpretation": "Lexical indicators, not a complete style judgment.", "counting_unit": "Affected prompts, not occurrences.", "comparison_rows": feedback_rows, "corpora": feedback_audits},
        "case_inputs": case_inputs,
        "reference_coverage": reference_coverage,
        "recurring_phrases_top_30": lexical["recurring_phrases"][:30],
        "lexically_closest_prompt_pairs_top_20": lexical["closest_pairs"][:20],
        "closest_to_reference_top_20": sorted(rows, key=lambda row: row["semantic_nearest_reference_similarity_scope_adjusted"], reverse=True)[:20],
        "farthest_from_reference_top_20": sorted(rows, key=lambda row: row["semantic_nearest_reference_similarity_scope_adjusted"])[:20],
        "references": refs,
        "points": rows,
        "limitations": [
            "This is a reviewed 160-text pilot over four smart-brief/source-messaging pairs and eight close/wide banks, not a raw single-call reliability sample.",
            "The V4.1 comparison is descriptive only: V5 uses different source documents and a different case inventory.",
            "The source score gives equal authority to both documents and credits the strongest useful support per rubric component; per-document totals are diagnostic and are not averaged 50/50.",
            "Text similarity measures semantic proximity to normalized C-Tech wording; it is not a calibrated acceptance threshold and does not measure generated images.",
            "No V5 images were generated for this report.",
            "The top-six analysis describes the candidates selected by source-score ordering in each bank; it does not establish downstream image quality.",
        ],
    }

    downloads = output / "downloads"
    gallery = output / "gallery"
    downloads.mkdir(parents=True, exist_ok=True)
    gallery.mkdir(parents=True, exist_ok=True)
    (downloads / "analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (downloads / "pilot_prompts.json").write_text(json.dumps({"version": analysis["version"], "prompt_count": n, "prompts": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (downloads / "pilot_prompts.txt").write_text(render_text(rows), encoding="utf-8")
    (downloads / "reference_prompts.json").write_text(json.dumps({"references": refs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (downloads / "lexical_audit.json").write_text(json.dumps(lexical, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(SYSTEM_PROMPT, downloads / "system_prompt.md")
    with (downloads / "candidate_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        fieldnames = list(rows[0])
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value for key, value in row.items()})
    (gallery / "data.js").write_text("const ANALYSIS = " + json.dumps(analysis, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    for filename in ("index.html", "report.js", "style.css", "imsauth.js"):
        shutil.copyfile(TEMPLATE / filename, gallery / filename)
    manifest = {"version": "hp-v5-dual-source-distribution-build-v2", "output": str(output), "inputs": analysis["inputs"], "counts": {"prompts": n, "cases": len(case_inputs), "references": len(refs), "top6": len(top_rows)}, "artifacts": {}}
    for path in sorted(path for path in output.rglob("*") if path.is_file() and path.name != "source_manifest.json"):
        manifest["artifacts"][str(path.relative_to(output))] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
    (output / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--cache-dir", type=Path, default=Path("/mnt/localssd/hp_lifestyle_pipeline/cache/huggingface"))
    args = parser.parse_args()
    print(json.dumps(build(args.output.resolve(), args.cache_dir.resolve()), indent=2))


if __name__ == "__main__":
    main()
