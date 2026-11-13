#!/usr/bin/env python3
"""Build a reproducible diversity and October-reference similarity report."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer


PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
EVAL = PROJECT / "eval_sets/hp_lifestyle_lived_in_v4_eval_20261026"
PROMPTS = EVAL / "generation_prompts.json"
ACCEPTED = EVAL / "accepted_prompt_cases.json"
SELECTION = EVAL / "selection_manifest.json"
REFERENCES = PROJECT / "research/diversity_aware_v3/data/october_guidance_raw_extraction.json"
LEXICAL_AUDIT = PROJECT / "research/lived_in_v4/data/v4_generation_prompt_stats.json"
TEMPLATE = EVAL / "diversity_analysis_v1/gallery"
DEFAULT_OUTPUT = PROJECT / "local_data/reports/hp_lifestyle_lived_in_v4_eval_20261026/diversity_analysis_v1"
MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
EXPECTED_ENVIRONMENTS = ("Home", "Office", "Education", "Gaming", "Café", "Creative Studio")
REFERENCE_PARAGRAPHS = (6, 7, 8, 10, 11, 12, 14, 15, 17, 18)
REFERENCE_GROUP = {
    6: "Corporate Office", 7: "Corporate Office", 8: "Corporate Office",
    10: "Home Workspace", 11: "Home Workspace", 12: "Home Workspace",
    14: "Coffee Shop", 15: "Coffee Shop",
    17: "Creative Studio", 18: "Creative Studio",
}
WORD_RE = re.compile(r"[A-Za-z0-9À-ÖØ-öø-ÿ]+")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def q(values: list[float], points=(0, .1, .25, .5, .75, .9, 1)) -> dict[str, float]:
    array = np.asarray(values, dtype=float)
    return {f"p{int(point * 100):02d}": round(float(np.quantile(array, point)), 6) for point in points}


def words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]


def strip_device_prefix(text: str) -> str:
    return re.sub(r"^(?:Laptop|Printer):\s*", "", text).strip()


def scope_adjust_reference(text: str) -> str:
    kept = []
    for sentence in sentences(strip_device_prefix(text)):
        if sentence.lower().startswith("minimal blue"):
            continue
        punctuation = sentence[-1] if sentence[-1:] in ".!?" else ""
        body = sentence[:-1] if punctuation else sentence
        body = re.sub(r",?\s+with no (?:additional )?hardware or devices visible", "", body, flags=re.IGNORECASE)
        body = re.sub(r",?\s+(?:with|and) minimal (?:blue accents|accents of blue|touches of blue).*?$", "", body, flags=re.IGNORECASE)
        body = body.strip().rstrip(",")
        if body:
            kept.append(body + punctuation)
    return " ".join(kept).strip()


def load_inputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    prompt_doc = json.loads(PROMPTS.read_text())
    prompts = [dict(item) for item in prompt_doc["prompts"]]
    prompt_sha256 = sha256(PROMPTS)
    prompt_by_key = {item["candidate_key"]: item for item in prompts}
    if len(prompts) != 540 or len(prompt_by_key) != 540:
        raise ValueError("expected 540 unique prompt candidate keys")
    accepted_sha = sha256(ACCEPTED)
    selection_sha = sha256(SELECTION)
    provenance = prompt_doc.get("provenance") or {}
    if provenance.get("accepted_prompt_cases_sha256") != accepted_sha:
        raise ValueError("prompt export is not bound to the current accepted V4 map")
    if provenance.get("selection_manifest_sha256") != selection_sha:
        raise ValueError("prompt export is not bound to the current approved V4 selection")
    accepted = json.loads(ACCEPTED.read_text())
    selection = json.loads(SELECTION.read_text())
    if accepted.get("status") != "complete" or accepted.get("counts", {}).get("candidates") != 540:
        raise ValueError("accepted V4 map is not complete at 540 candidates")
    if selection.get("status") != "approved_for_image_generation" or selection.get("counts", {}).get("selected") != 108:
        raise ValueError("V4 selection is not the approved 108-row set")
    native_values = {item["environment"] for item in prompts}
    if native_values != set(EXPECTED_ENVIRONMENTS):
        raise ValueError(f"V4 prompt export does not contain the exact native six-category taxonomy: {native_values}")
    for prompt in prompts:
        prompt["display_environment"] = prompt["environment"]
        prompt["display_environment_rule"] = "native_v4_environment"
    derived_display_counts = dict(sorted(Counter(item["display_environment"] for item in prompts).items()))
    extracted = json.loads(REFERENCES.read_text())
    by_paragraph = {item["paragraph"]: item for item in extracted["blocks"] if item.get("type") == "paragraph"}
    refs = []
    for index, paragraph in enumerate(REFERENCE_PARAGRAPHS, 1):
        source = by_paragraph[paragraph]
        full = strip_device_prefix(source["text"])
        adjusted = scope_adjust_reference(source["text"])
        refs.append({
            "reference_id": f"ref_{index:02d}",
            "paragraph": paragraph,
            "location": source["location"],
            "group": REFERENCE_GROUP[paragraph],
            "original_text": source["text"],
            "full_text_device_prefix_removed": full,
            "scope_adjusted_text": adjusted,
            "scope_adjustments": [
                "Removed the Laptop:/Printer: prefix to respect the approved environment-only device boundary.",
                "Removed only blue-control sentences or trailing clauses because color control is outside the V4 environment-writer contract.",
                "Removed only explicit no-hardware/no-device clauses because that boilerplate is outside the V4 environment-writer contract.",
            ],
        })
    native_taxonomy = {
        "field": "environment",
        "categories": list(EXPECTED_ENVIRONMENTS),
        "counts": derived_display_counts,
        "derivation": (
            "Direct frequency count of the model-authored V4 environment field. No lexical display relabeling, "
            "classifier, inference, or post-hoc environment mapping was applied."
        ),
        "generation_prompts_sha256": prompt_sha256,
        "accepted_prompt_cases_sha256": accepted_sha,
        "selection_manifest_sha256": selection_sha,
    }
    return prompts, refs, extracted, native_taxonomy


def embed(texts: list[str], cache_dir: Path, batch_size: int = 48) -> tuple[np.ndarray, dict[str, Any]]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, revision=MODEL_REVISION, cache_dir=cache_dir, local_files_only=True
    )
    model = AutoModel.from_pretrained(
        MODEL_ID, revision=MODEL_REVISION, cache_dir=cache_dir, local_files_only=True
    )
    model.eval()
    batches = []
    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            encoded = tokenizer(texts[start:start + batch_size], padding=True, truncation=True, max_length=256, return_tensors="pt")
            output = model(**encoded).last_hidden_state
            mask = encoded["attention_mask"].unsqueeze(-1).expand(output.size()).float()
            pooled = (output * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
            pooled = torch.nn.functional.normalize(pooled, p=2, dim=1)
            batches.append(pooled.cpu().numpy())
    matrix = np.vstack(batches).astype(np.float64)
    return matrix, {
        "model_id": MODEL_ID,
        "revision": MODEL_REVISION,
        "model_loading": "local_files_only=True; no network resolution",
        "pooling": "attention-mask mean pooling over last_hidden_state, then L2 normalization",
        "max_tokens": 256,
        "similarity": "cosine similarity (dot product of L2-normalized embeddings)",
        "interpretation": "Descriptive semantic-text proximity, not an image-quality or style-acceptance score.",
    }


def ngrams(text: str) -> list[str]:
    tokens = words(text)
    return tokens + [tokens[i] + " " + tokens[i + 1] for i in range(len(tokens) - 1)]


def tfidf_vectors(texts: list[str]) -> list[dict[str, float]]:
    docs = [Counter(ngrams(text)) for text in texts]
    df = Counter(term for doc in docs for term in doc)
    count = len(docs)
    vectors = []
    for doc in docs:
        weighted = {term: (1 + math.log(freq)) * (math.log((1 + count) / (1 + df[term])) + 1) for term, freq in doc.items()}
        norm = math.sqrt(sum(value * value for value in weighted.values())) or 1.0
        vectors.append({term: value / norm for term, value in weighted.items()})
    return vectors


def sparse_dot(left: dict[str, float], right: dict[str, float]) -> float:
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(term, 0.0) for term, value in left.items())


def pca_2d(matrix: np.ndarray) -> tuple[np.ndarray, list[float]]:
    centered = matrix - matrix.mean(axis=0, keepdims=True)
    _, singular, vt = np.linalg.svd(centered, full_matrices=False)
    components = vt[:2].copy()
    for axis in range(2):
        anchor = int(np.argmax(np.abs(components[axis])))
        if components[axis, anchor] < 0:
            components[axis] *= -1
    coords = centered @ components.T
    explained = (singular * singular) / np.sum(singular * singular)
    return coords, [round(float(explained[0]), 6), round(float(explained[1]), 6)]


def grouped_metrics(rows: list[dict[str, Any]], key: str, metric: str) -> list[dict[str, Any]]:
    groups: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        groups[str(row[key])].append(float(row[metric]))
    return [{"label": label, "count": len(values), "mean": round(float(np.mean(values)), 6), "quantiles": q(values)} for label, values in sorted(groups.items())]


def entropy(counts: dict[str, int]) -> dict[str, float]:
    total = sum(counts.values())
    value = -sum((count / total) * math.log(count / total) for count in counts.values())
    maximum = math.log(len(counts)) if len(counts) > 1 else 0
    return {"shannon_nats": round(value, 6), "normalized_0_to_1": round(value / maximum, 6) if maximum else 0}


def build(output: Path, cache_dir: Path) -> dict[str, Any]:
    prompts, refs, extraction, taxonomy = load_inputs()
    lexical_audit = json.loads(LEXICAL_AUDIT.read_text())
    lexical_input = lexical_audit.get("input") or {}
    if lexical_input.get("sha256") != sha256(PROMPTS) or lexical_input.get("bytes") != PROMPTS.stat().st_size:
        raise ValueError("durable V4 lexical audit targets different generation prompt bytes")
    if lexical_audit.get("validation", {}).get("prompt_count") != 540:
        raise ValueError("durable V4 lexical audit does not cover exactly 540 prompts")
    texts = [item["text"] for item in prompts]
    ref_full = [item["full_text_device_prefix_removed"] for item in refs]
    ref_adjusted = [item["scope_adjusted_text"] for item in refs]
    embeddings, model_meta = embed(texts + ref_full + ref_adjusted, cache_dir)
    n = len(texts); r = len(refs)
    prompt_emb = embeddings[:n]
    full_ref_emb = embeddings[n:n + r]
    adjusted_ref_emb = embeddings[n + r:n + 2 * r]
    adjusted_similarity = prompt_emb @ adjusted_ref_emb.T
    full_similarity = prompt_emb @ full_ref_emb.T
    lexical = tfidf_vectors(texts + ref_adjusted)
    lexical_similarity = np.asarray([[sparse_dot(lexical[i], lexical[n + j]) for j in range(r)] for i in range(n)])

    prompt_pairwise = prompt_emb @ prompt_emb.T
    np.fill_diagonal(prompt_pairwise, -np.inf)
    nearest_indices = np.argmax(prompt_pairwise, axis=1)
    nearest_values = prompt_pairwise[np.arange(n), nearest_indices]
    finite_pairs = prompt_pairwise[np.triu_indices(n, 1)]

    combined_for_map = np.vstack([prompt_emb, adjusted_ref_emb])
    coordinates, explained = pca_2d(combined_for_map)
    max_adjusted = adjusted_similarity.max(axis=1)
    nearest_adjusted = adjusted_similarity.argmax(axis=1)
    max_full = full_similarity.max(axis=1)
    max_lexical = lexical_similarity.max(axis=1)
    nearest_lexical = lexical_similarity.argmax(axis=1)

    rows = []
    for i, item in enumerate(prompts):
        nearest = prompts[int(nearest_indices[i])]
        ref = refs[int(nearest_adjusted[i])]
        row = {
            "candidate_key": item["candidate_key"], "source_id": item["source_id"], "case_id": item["case_id"],
            "device_type": item["device_type"], "camera_tag": item["camera_tag"], "view_role": item["view_role"],
            "rank": item["rank"], "rank_bin": item["rank_bin"], "environment": item["environment"],
            "display_environment": item["display_environment"],
            "display_environment_rule": item["display_environment_rule"],
            "subsetting": item["subsetting"], "relationship": item["relationship"], "score": item["score"],
            "selected": item["selected_for_image_eval"], "text": item["text"], "word_count": len(words(item["text"])),
            "sentence_count": len(sentences(item["text"])),
            "semantic_nearest_candidate_similarity": round(float(nearest_values[i]), 6),
            "semantic_nearest_candidate_key": nearest["candidate_key"],
            "semantic_nearest_reference_similarity_scope_adjusted": round(float(max_adjusted[i]), 6),
            "semantic_nearest_reference_id_scope_adjusted": ref["reference_id"],
            "semantic_nearest_reference_similarity_full": round(float(max_full[i]), 6),
            "lexical_nearest_reference_similarity_scope_adjusted": round(float(max_lexical[i]), 6),
            "lexical_nearest_reference_id_scope_adjusted": refs[int(nearest_lexical[i])]["reference_id"],
            "map_x": round(float(coordinates[i, 0]), 6), "map_y": round(float(coordinates[i, 1]), 6),
        }
        rows.append(row)

    canonical_environment_counts = dict(sorted(Counter(item["environment"] for item in prompts).items()))
    display_environment_counts = dict(sorted(Counter(item["display_environment"] for item in prompts).items()))
    display_environment_rule_counts = dict(sorted(Counter(item["display_environment_rule"] for item in prompts).items()))
    relationship_counts = dict(sorted(Counter(item["relationship"] for item in prompts).items()))
    score_hist = Counter((int(item["score"]) // 10) * 10 if int(item["score"]) < 100 else 100 for item in prompts)
    similarity_hist = Counter(min(9, int(max(0, value) * 10)) for value in max_adjusted)
    reference_coverage = []
    for j, ref in enumerate(refs):
        assigned = np.where(nearest_adjusted == j)[0]
        reference_coverage.append({
            **ref,
            "assigned_prompt_count": int(len(assigned)),
            "mean_assigned_similarity": round(float(np.mean(max_adjusted[assigned])), 6) if len(assigned) else None,
            "maximum_similarity": round(float(adjusted_similarity[:, j].max()), 6),
            "map_x": round(float(coordinates[n + j, 0]), 6), "map_y": round(float(coordinates[n + j, 1]), 6),
        })

    ref_word_counts = [len(words(text)) for text in ref_adjusted]
    ref_sentence_counts = [len(sentences(text)) for text in ref_adjusted]
    prompt_word_counts = [row["word_count"] for row in rows]
    prompt_sentence_counts = [row["sentence_count"] for row in rows]
    top_phrases = lexical_audit["recurring_phrases"]["flagged_recurring_phrases_df_ge_10"][:30]
    pair_lists = lexical_audit["similarity"]["highest_similarity_pairs_top_100"]
    char_by_pair = {
        tuple(sorted((item["left_candidate_key"], item["right_candidate_key"]))): item["similarity"]
        for item in pair_lists["char_trigram_jaccard"]
    }
    duplicate_pairs = []
    for item in pair_lists["word_bigram_jaccard"][:20]:
        pair = tuple(sorted((item["left_candidate_key"], item["right_candidate_key"])))
        duplicate_pairs.append({**item, "word_bigram_jaccard": item["similarity"], "char_trigram_jaccard": char_by_pair.get(pair)})
    top_reference = sorted(rows, key=lambda item: item["semantic_nearest_reference_similarity_scope_adjusted"], reverse=True)[:20]
    bottom_reference = sorted(rows, key=lambda item: item["semantic_nearest_reference_similarity_scope_adjusted"])[:20]

    analysis = {
        "version": "hp-v4-diversity-analysis-v1-native-environment",
        "as_of": "2026-10-26",
        "scope": {
            "prompt_count": n,
            "reference_prompt_count": r,
            "reference_paragraphs": list(REFERENCE_PARAGRAPHS),
            "display_environment_count": len(display_environment_counts),
            "canonical_environment_count": len(canonical_environment_counts),
        },
        "inputs": {
            "generation_prompts": {"path": str(PROMPTS), "sha256": sha256(PROMPTS), "bytes": PROMPTS.stat().st_size},
            "october_docx": extraction["authority"],
            "reference_extraction": {"path": str(REFERENCES), "sha256": sha256(REFERENCES)},
            "lexical_audit": {"path": str(LEXICAL_AUDIT), "sha256": sha256(LEXICAL_AUDIT)},
            "accepted_prompt_cases": {"path": str(ACCEPTED), "sha256": sha256(ACCEPTED), "bytes": ACCEPTED.stat().st_size},
            "selection_manifest": {"path": str(SELECTION), "sha256": sha256(SELECTION), "bytes": SELECTION.stat().st_size},
        },
        "methods": {
            "semantic_embedding": model_meta,
            "reference_normalization": refs[0]["scope_adjustments"],
            "lexical_reference_similarity": "Cosine similarity over corpus TF-IDF word unigrams+bigrams; log-scaled term frequency; smoothed IDF.",
            "map": {"method": "PCA of the combined 540 prompt + 10 scope-adjusted reference embeddings", "explained_variance_ratio_first_two": explained},
            "display_environment": {
                "field": "display_environment",
                "canonical_field": "environment",
                "alias_rule": "display_environment equals environment for every row",
                "derivation": taxonomy["derivation"],
                "categories": taxonomy["categories"],
            },
            "diversity_warning": "No single number establishes visual diversity. Category counts, lexical repetition, semantic proximity and images answer different questions.",
        },
        "headline": {
            "exact_duplicate_prompt_groups": lexical_audit["duplicates"]["exact_raw_text"]["duplicate_group_count"],
            "canonical_duplicate_prompt_groups": lexical_audit["duplicates"]["canonical_text"]["duplicate_group_count"],
            "display_environment_counts": display_environment_counts,
            "display_environment_entropy": entropy(display_environment_counts),
            "canonical_environment_counts": canonical_environment_counts,
            "canonical_environment_entropy": entropy(canonical_environment_counts),
            "display_environment_rule_counts": display_environment_rule_counts,
            "relationship_counts": relationship_counts,
            "semantic_pairwise_similarity_quantiles": q(finite_pairs.tolist()),
            "semantic_nearest_neighbor_similarity_quantiles": q(nearest_values.tolist()),
            "semantic_nearest_reference_scope_adjusted_quantiles": q(max_adjusted.tolist()),
            "semantic_nearest_reference_full_quantiles": q(max_full.tolist()),
            "lexical_nearest_reference_scope_adjusted_quantiles": q(max_lexical.tolist()),
            "prompt_word_count_quantiles": q(prompt_word_counts),
            "reference_word_count_quantiles_scope_adjusted": q(ref_word_counts),
            "prompts_inside_reference_word_count_range": sum(min(ref_word_counts) <= value <= max(ref_word_counts) for value in prompt_word_counts),
            "prompts_inside_reference_sentence_count_range": sum(min(ref_sentence_counts) <= value <= max(ref_sentence_counts) for value in prompt_sentence_counts),
        },
        "distributions": {
            "display_environment": display_environment_counts,
            "canonical_environment": canonical_environment_counts,
            "display_environment_rule": display_environment_rule_counts,
            "relationship": relationship_counts,
            "score_histogram": [{"label": "100" if bucket == 100 else f"{bucket}-{bucket+9}", "count": score_hist[bucket]} for bucket in range(0, 101, 10)],
            "reference_similarity_histogram_scope_adjusted": [{"label": f"{bucket/10:.1f}-{(bucket+1)/10:.1f}", "count": similarity_hist[bucket]} for bucket in range(10)],
            "reference_similarity_by_display_environment": grouped_metrics(rows, "display_environment", "semantic_nearest_reference_similarity_scope_adjusted"),
            "reference_similarity_by_canonical_environment": grouped_metrics(rows, "environment", "semantic_nearest_reference_similarity_scope_adjusted"),
            "reference_similarity_by_relationship": grouped_metrics(rows, "relationship", "semantic_nearest_reference_similarity_scope_adjusted"),
            "reference_similarity_by_view": grouped_metrics(rows, "view_role", "semantic_nearest_reference_similarity_scope_adjusted"),
            "reference_similarity_by_rank_bin": grouped_metrics(rows, "rank_bin", "semantic_nearest_reference_similarity_scope_adjusted"),
        },
        "reference_coverage": reference_coverage,
        "recurring_phrases_top_30": top_phrases,
        "lexically_closest_prompt_pairs_top_20": duplicate_pairs,
        "closest_to_reference_top_20": top_reference,
        "farthest_from_reference_top_20": bottom_reference,
        "references": refs,
        "points": rows,
        "limitations": [
            "The ten October reference prompts cover Corporate Office, Home Workspace, Coffee Shop and Creative Studio; they contain no Education or Gaming examples. Lower similarity for those V4 families can reflect intentional breadth.",
            "The October examples are mostly room-level prompts. V4 close-up camera profiles intentionally request shorter, local surface/light descriptions; length and similarity are therefore camera-confounded.",
            "Semantic embedding cosine measures text meaning, not exact photographic style, prompt quality or downstream image quality. Thresholds are descriptive and not calibrated pass/fail gates.",
            "TF-IDF cosine rewards shared literal words and penalizes synonyms; it is reported alongside semantic similarity rather than treated as ground truth.",
            "PCA is a two-dimensional projection; overlap or distance in the map can distort relationships present in the full embedding space.",
            "Zero exact duplicates does not mean zero visual repetition. The bounded 108-image eval is the appropriate evidence for visible diversity.",
            "The six environment categories are native V4 output values. The report aliases them as display_environment only to retain the established V3 gallery data contract; no row is relabeled.",
        ],
    }

    output.mkdir(parents=True, exist_ok=True)
    downloads = output / "downloads"; downloads.mkdir(exist_ok=True)
    gallery = output / "gallery"; gallery.mkdir(exist_ok=True)
    (downloads / "analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n")
    (downloads / "reference_prompts.json").write_text(json.dumps({"references": refs}, ensure_ascii=False, indent=2) + "\n")
    shutil.copyfile(LEXICAL_AUDIT, downloads / "lexical_audit.json")
    fields = list(rows[0])
    with (downloads / "candidate_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    public_data = dict(analysis)
    (gallery / "data.js").write_text("const ANALYSIS = " + json.dumps(public_data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    for filename in ("index.html", "report.js", "style.css"):
        shutil.copyfile(TEMPLATE / filename, gallery / filename)
    shutil.copyfile(PROJECT / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/imsauth.js", gallery / "imsauth.js")
    manifest = {
        "version": "hp-v4-diversity-analysis-build-v1-native-environment",
        "output": str(output),
        "inputs": analysis["inputs"],
        "artifacts": {},
        "counts": {"prompts": n, "references": r, "candidate_csv_rows": len(rows)},
    }
    for path in sorted(p for p in output.rglob("*") if p.is_file() and p.name != "source_manifest.json"):
        manifest["artifacts"][str(path.relative_to(output))] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
    (output / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--cache-dir", type=Path, default=Path("/mnt/localssd/hp_lifestyle_pipeline/cache/huggingface"))
    args = parser.parse_args()
    manifest = build(args.output.resolve(), args.cache_dir.resolve())
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
