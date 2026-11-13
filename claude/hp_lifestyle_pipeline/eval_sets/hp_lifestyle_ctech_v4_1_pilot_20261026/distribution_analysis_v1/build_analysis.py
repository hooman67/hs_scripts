#!/usr/bin/env python3
"""Build the V4.1 120-prompt distribution and C-Tech proximity report."""

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
EVAL = PROJECT / "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026"
PROMPTS = EVAL / "pilot_prompts.json"
ACCEPTED = EVAL / "accepted_prompt_cases.json"
MANIFEST = EVAL / "manifest.json"
BASELINE = PROJECT / "eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/accepted_prompt_cases.json"
RAW_EXTRACTION = PROJECT / "research/diversity_aware_v3/data/october_guidance_raw_extraction.json"
REFERENCE_LIBRARY = PROJECT / "research/source_messaging_v1_to_v6/versions/v4.1/reference_library.json"
USER_REFERENCE_ADDITIONS = PROJECT / "research/source_messaging_v1_to_v6/versions/v4.1/user_reference_additions.json"
FINAL_TEXT_REVIEW = EVAL / "final_text_review.json"
TEMPLATE = EVAL / "distribution_analysis_v1/gallery"
DEFAULT_OUTPUT = PROJECT / "local_data/reports/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1"
MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
EXPECTED_ENVIRONMENTS = ("Home", "Office", "Education", "Gaming", "Café", "Creative Studio")
REFERENCE_PARAGRAPHS = {"CT01": 6, "CT02": 7, "CT03": 8, "CT04": 10, "CT05": 11,
                        "CT06": 12, "CT07": 14, "CT08": 15, "CT09": 17, "CT10": 18}
WORD_RE = re.compile(r"[A-Za-z0-9À-ÖØ-öø-ÿ]+")
UNNATURAL_PLACE_PATTERN_VERSION = "validate_output.py sha256:9f2d986648dab2395b877738855ca7633a6ecdb4ae8dc64569dfb141435164da"
UNNATURAL_PLACE_RE = re.compile(
    r"\b(?:(?:close|local|tight|compact|small) (?:section|patch|area|portion|piece|stretch|slice) of|shared department records counter|records counter|"
    r"paperwork nook|policy deployment counter|illustration worktop|"
    r"teaching[- ]preparation table|"
    r"(?:records?|policy|deployment|paperwork|illustration|workflow|department|administration|administrative|output check|queue)\s+"
    r"(?:counter|nook|corner|worktop|surface)|"
    r"(?:teaching[- ]preparation|content review|document review|records?|paperwork|workflow|department)\s+"
    r"(?:desk|table|counter|nook|worktop|surface)|workspace feeling|document queue)\b", re.I
)
MICROSCOPIC_STORY_RE = re.compile(
    r"\b(?:dog-eared|out of square|set askew|wipe (?:streaks?|marks?|arcs?)|rubbed|scuffs?|"
    r"writing impressions|thumb[- ]smudg\w*|fingertip[- ]smudg\w*|"
    r"softened (?:edges?|corners?)|chipped|frayed|crossed-out|routing notes|"
    r"lowered (?:coffee|tea|water) line)\b", re.I
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]


def quantiles(values: list[float], points=(0, .1, .25, .5, .75, .9, 1)) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    return {f"p{int(point * 100):02d}": round(float(np.quantile(arr, point)), 6) for point in points}


def entropy(counts: dict[str, int]) -> dict[str, float]:
    total = sum(counts.values())
    value = -sum((count / total) * math.log(count / total) for count in counts.values())
    maximum = math.log(len(counts)) if len(counts) > 1 else 0
    return {"shannon_nats": round(value, 6), "normalized_0_to_1": round(value / maximum, 6) if maximum else 0}


def strip_device_prefix(text: str) -> str:
    return re.sub(r"^(?:Laptop|Printer):\s*", "", text).strip()


def scope_adjust_reference(text: str) -> str:
    kept = []
    for sentence in sentences(strip_device_prefix(text)):
        if sentence.lower().startswith("minimal blue"):
            continue
        punctuation = sentence[-1] if sentence[-1:] in ".!?" else ""
        body = sentence[:-1] if punctuation else sentence
        body = re.sub(r",?\s+with no (?:additional )?hardware or devices visible", "", body, flags=re.I)
        body = re.sub(r",?\s+(?:with|and) minimal (?:blue accents|accents of blue|touches of blue).*?$", "", body, flags=re.I)
        body = body.strip().rstrip(",")
        if body:
            kept.append(body + punctuation)
    return " ".join(kept).strip()


def load_references() -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    extraction = json.loads(RAW_EXTRACTION.read_text(encoding="utf-8"))
    by_paragraph = {item["paragraph"]: item for item in extraction["blocks"] if item.get("type") == "paragraph"}
    library = json.loads(REFERENCE_LIBRARY.read_text(encoding="utf-8"))
    user_additions = json.loads(USER_REFERENCE_ADDITIONS.read_text(encoding="utf-8"))
    user_raw_path = Path(user_additions["raw_path"])
    if sha256(user_raw_path) != user_additions["raw_sha256"]:
        raise ValueError("user reference raw source hash mismatch")
    user_raw_by_id = {
        item["reference_id"]: item for item in user_additions["occurrences"]
        if item["reference_id"] in {f"CT{number:02d}" for number in range(11, 19)}
    }
    if set(user_raw_by_id) != {f"CT{number:02d}" for number in range(11, 19)}:
        raise ValueError("expected raw user examples CT11-CT18")
    refs = []
    for item in library["references"]:
        paragraph = REFERENCE_PARAGRAPHS.get(item["id"])
        source = by_paragraph.get(paragraph)
        user_source = user_raw_by_id.get(item["id"])
        raw_text = source["text"] if source else user_source["text"]
        refs.append({
            "reference_id": item["id"], "paragraph": paragraph,
            "location": source["location"] if source else f"Hooman additional C-Tech examples, line {user_source['line']}",
            "group": item["environment"], "source": item["source"],
            "original_text": raw_text,
            "raw_source_kind": "october_guidance" if source else "user_reference_addition",
            "raw_source_sha256": extraction["authority"]["sha256"] if source else user_additions["raw_sha256"],
            "scope_adjusted_text": item["text"],
        })
    return refs, extraction, user_additions


def load_case_inputs(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    cases = []
    for case in manifest["cases"]:
        path = Path(case["input_path"])
        if sha256(path) != case["input_sha256"]:
            raise ValueError(f"case input hash mismatch: {case['case_id']}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("camera_tag") != case["camera_tag"]:
            raise ValueError(f"case camera mismatch: {case['case_id']}")
        cases.append({
            "case_id": case["case_id"], "source_id": case["source_id"],
            "device_type": case["device_type"], "view_role": case["view_role"],
            "input_sha256": case["input_sha256"],
            "camera_tag": payload["camera_tag"], "expected_camera": case["expected_camera"],
            "source_messaging": payload["source_messaging"],
        })
    return cases


def load_final_review() -> tuple[dict[str, Any], list[str]]:
    generic = "No complete, corpus-bound prompt-run accounting is attached, so this report makes no first-draw or retry reliability claim."
    if not FINAL_TEXT_REVIEW.is_file():
        return {"status": "not_present", "path": str(FINAL_TEXT_REVIEW)}, [generic]
    review = json.loads(FINAL_TEXT_REVIEW.read_text(encoding="utf-8"))
    record = {"status": "loaded", "path": str(FINAL_TEXT_REVIEW),
              "sha256": sha256(FINAL_TEXT_REVIEW), "document": review}
    if review.get("accepted_prompt_cases_sha256") != sha256(ACCEPTED):
        record["status"] = "ignored_accepted_corpus_hash_mismatch"
        return record, [generic]
    candidates = review.get("prompt_run_limitations", review.get("accepted_limitations", []))
    def is_stale(item: Any) -> bool:
        value = str(item).casefold()
        return (("first draw" in value and "all" in value and "four" in value)
                or ("both fields" in value and "replac" in value))

    limitations = [str(item) for item in candidates if not is_stale(item)]
    return record, limitations or [generic]


def load_inputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any],
                           dict[str, Any], list[dict[str, Any]], Path, dict[str, Any], list[str]]:
    doc = json.loads(PROMPTS.read_text(encoding="utf-8"))
    prompts = doc["prompts"]
    if doc["prompt_count"] != 120 or len(prompts) != 120 or len({row["candidate_key"] for row in prompts}) != 120:
        raise ValueError("expected 120 unique V4.1 pilot prompts")
    if doc["provenance"]["accepted_prompt_cases_sha256"] != sha256(ACCEPTED):
        raise ValueError("pilot export is not bound to current accepted cases")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if doc["provenance"]["manifest_sha256"] != sha256(MANIFEST):
        raise ValueError("pilot export is not bound to current manifest")
    if manifest["scope"]["image_generation_authorized"] is not False:
        raise ValueError("distribution gate requires image generation to remain unauthorized")
    if {row["environment"] for row in prompts} != set(EXPECTED_ENVIRONMENTS):
        raise ValueError("pilot does not contain the exact six-category taxonomy")
    baseline_doc = json.loads(BASELINE.read_text(encoding="utf-8"))
    baseline = []
    for case_id in manifest["authorized_text_case_ids"]:
        for candidate in baseline_doc["cases"][case_id]["candidates"]:
            baseline.append({"candidate_key": candidate["candidate_key"], "case_id": case_id,
                             "view_role": baseline_doc["cases"][case_id]["view_role"],
                             "text": candidate["text"]})
    if len(baseline) != 120:
        raise ValueError("expected the same 120 final-V4 comparison prompts")
    refs, extraction, user_additions = load_references()
    case_inputs = load_case_inputs(manifest)
    if {row["case_id"] for row in prompts} != {row["case_id"] for row in case_inputs}:
        raise ValueError("frozen case inputs do not exactly cover pilot prompts")
    system_prompt_record = manifest["provenance"]["system_prompt"]
    system_prompt = Path(system_prompt_record["path"])
    if (sha256(system_prompt) != system_prompt_record["sha256"]
            or system_prompt.stat().st_size != system_prompt_record["bytes"]):
        raise ValueError("manifest system prompt provenance mismatch")
    final_review, run_limitations = load_final_review()
    return (prompts, baseline, refs, extraction, user_additions, case_inputs, system_prompt,
            final_review, run_limitations)


def embed(texts: list[str], cache_dir: Path, batch_size: int = 48) -> tuple[np.ndarray, dict[str, Any]]:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION, cache_dir=cache_dir, local_files_only=True)
    model = AutoModel.from_pretrained(MODEL_ID, revision=MODEL_REVISION, cache_dir=cache_dir, local_files_only=True)
    model.eval()
    batches = []
    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            encoded = tokenizer(texts[start:start + batch_size], padding=True, truncation=True, max_length=256, return_tensors="pt")
            hidden = model(**encoded).last_hidden_state
            mask = encoded["attention_mask"].unsqueeze(-1).expand(hidden.size()).float()
            pooled = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
            batches.append(torch.nn.functional.normalize(pooled, p=2, dim=1).cpu().numpy())
    return np.vstack(batches).astype(np.float64), {
        "model_id": MODEL_ID, "revision": MODEL_REVISION,
        "model_loading": "local_files_only=True; no network resolution",
        "pooling": "attention-mask mean pooling over last_hidden_state, then L2 normalization",
        "similarity": "cosine similarity of L2-normalized embeddings",
        "interpretation": "Descriptive semantic-text proximity, not a calibrated style or image-quality score.",
    }


def tfidf_vectors(texts: list[str]) -> list[dict[str, float]]:
    docs = [Counter(words(text) + [" ".join(words(text)[i:i + 2]) for i in range(max(0, len(words(text)) - 1))]) for text in texts]
    df = Counter(term for doc in docs for term in doc)
    total = len(docs)
    vectors = []
    for doc in docs:
        weighted = {term: (1 + math.log(freq)) * (math.log((1 + total) / (1 + df[term])) + 1) for term, freq in doc.items()}
        norm = math.sqrt(sum(value * value for value in weighted.values())) or 1
        vectors.append({term: value / norm for term, value in weighted.items()})
    return vectors


def sparse_dot(left: dict[str, float], right: dict[str, float]) -> float:
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(term, 0) for term, value in left.items())


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


def grouped(rows: list[dict[str, Any]], key: str, metric: str) -> list[dict[str, Any]]:
    groups: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        groups[str(row[key])].append(float(row[metric]))
    return [{"label": label, "count": len(values), "mean": round(float(np.mean(values)), 6),
             "quantiles": quantiles(values)} for label, values in sorted(groups.items())]


def jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a | b else 1.0


def lexical_audit(prompts: list[dict[str, Any]]) -> dict[str, Any]:
    exact = defaultdict(list); canonical = defaultdict(list)
    phrase_df = Counter(); word_bigrams = {}; char_trigrams = {}
    for row in prompts:
        text = row["text"]
        exact[" ".join(text.casefold().split())].append(row["candidate_key"])
        canonical[" ".join(words(text))].append(row["candidate_key"])
        tokens = words(text)
        seen = set()
        for n in range(3, 6):
            seen.update(" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1))
        phrase_df.update(seen)
        word_bigrams[row["candidate_key"]] = {" ".join(tokens[i:i + 2]) for i in range(len(tokens) - 1)}
        chars = re.sub(r"\s+", " ", text.casefold()).strip()
        char_trigrams[row["candidate_key"]] = {chars[i:i + 3] for i in range(max(0, len(chars) - 2))}
    pairs = []
    keys = [row["candidate_key"] for row in prompts]
    for i, left in enumerate(keys):
        for right in keys[i + 1:]:
            pairs.append({"left_candidate_key": left, "right_candidate_key": right,
                          "word_bigram_jaccard": round(jaccard(word_bigrams[left], word_bigrams[right]), 6),
                          "char_trigram_jaccard": round(jaccard(char_trigrams[left], char_trigrams[right]), 6)})
    pairs.sort(key=lambda row: (row["word_bigram_jaccard"], row["char_trigram_jaccard"]), reverse=True)
    phrases = [{"phrase": phrase, "prompt_document_frequency": count}
               for phrase, count in sorted(phrase_df.items(), key=lambda item: (-item[1], item[0])) if count >= 2]
    return {
        "exact_duplicate_groups": [value for value in exact.values() if len(value) > 1],
        "canonical_duplicate_groups": [value for value in canonical.values() if len(value) > 1],
        "recurring_phrases": phrases[:100], "closest_pairs": pairs[:100],
    }


def feedback_pattern_audit(rows: list[dict[str, Any]], corpus: str) -> dict[str, Any]:
    patterns = {
        "unnatural_framing_or_place_phrase": UNNATURAL_PLACE_RE,
        "microscopic_wear_or_story_marker": MICROSCOPIC_STORY_RE,
    }
    categories = {}
    for indicator, pattern in patterns.items():
        findings = []
        for row in rows:
            matches = [{"matched_span": match.group(0), "start": match.start(), "end": match.end()}
                       for match in pattern.finditer(row["text"])]
            if matches:
                findings.append({"candidate_key": row["candidate_key"], "case_id": row["case_id"],
                                 "text": row["text"], "matches": matches})
        categories[indicator] = {
            "affected_prompt_count": len(findings),
            "affected_prompt_rate": round(len(findings) / len(rows), 6),
            "findings": findings,
        }
    return {"corpus": corpus, "prompt_count": len(rows), "categories": categories}


def render_plain_text_prompts(document: dict[str, Any]) -> str:
    lines = [
        "HP V4.1 C-Tech pilot prompts",
        f"Version: {document['version']}",
        f"Status: {document['status']}",
        f"Prompt count: {document['prompt_count']}",
        "",
    ]
    for row in document["prompts"]:
        lines.extend([
            f"[{row['candidate_key']}]",
            f"Case: {row['case_id']}",
            f"Camera: {row['camera_tag']} ({row['view_role']})",
            f"Environment: {row['environment']} · {row['subsetting']}",
            row["text"],
            "",
        ])
    return "\n".join(lines)


def score_hist(values: list[int]) -> list[dict[str, Any]]:
    labels = ((60, 69), (70, 79), (80, 89), (90, 99), (100, 100))
    return [{"label": str(low) if low == high else f"{low}-{high}",
             "count": sum(low <= value <= high for value in values)} for low, high in labels]


def similarity_hist(values: np.ndarray) -> list[dict[str, Any]]:
    buckets = Counter(min(9, max(0, int(value * 10))) for value in values)
    return [{"label": f"{bucket / 10:.1f}-{(bucket + 1) / 10:.1f}", "count": buckets[bucket]} for bucket in range(10)]


def build(output: Path, cache_dir: Path) -> dict[str, Any]:
    (prompts, baseline, refs, extraction, user_additions, case_inputs, system_prompt,
     final_review, run_limitations) = load_inputs()
    texts = [row["text"] for row in prompts]
    baseline_texts = [row["text"] for row in baseline]
    ref_texts = [row["scope_adjusted_text"] for row in refs]
    embeddings, model_meta = embed(texts + baseline_texts + ref_texts, cache_dir)
    n = len(texts); b = len(baseline_texts); r = len(refs)
    prompt_emb = embeddings[:n]; baseline_emb = embeddings[n:n + b]; ref_emb = embeddings[n + b:n + b + r]
    similarity = prompt_emb @ ref_emb.T
    baseline_similarity = baseline_emb @ ref_emb.T
    nearest_idx = similarity.argmax(axis=1); nearest_value = similarity.max(axis=1)
    baseline_nearest = baseline_similarity.max(axis=1)
    declared_idx = np.asarray([int(row["ctech_reference_id"][2:]) - 1 for row in prompts])
    declared_similarity = similarity[np.arange(n), declared_idx]
    pairwise = prompt_emb @ prompt_emb.T; np.fill_diagonal(pairwise, -np.inf)
    nearest_candidate_idx = pairwise.argmax(axis=1); nearest_candidate_value = pairwise.max(axis=1)
    finite_pairs = pairwise[np.triu_indices(n, 1)]
    lexical_vectors = tfidf_vectors(texts + ref_texts)
    lexical_similarity = np.asarray([[sparse_dot(lexical_vectors[i], lexical_vectors[n + j]) for j in range(r)] for i in range(n)])
    coords, explained = pca_2d(np.vstack([prompt_emb, ref_emb]))
    lexical = lexical_audit(prompts)
    pilot_document = json.loads(PROMPTS.read_text(encoding="utf-8"))
    edited_rows = [row for row in prompts if row.get("editorially_scene_edited") is True]
    expected_edited_count = pilot_document.get("counts", {}).get("editorially_scene_edited_candidates")
    if expected_edited_count != len(edited_rows):
        raise ValueError("pilot editorial scene-edit count does not match row metadata")
    if any(not row.get("raw_correction_text") or not row.get("repair_normalized_text") for row in prompts):
        raise ValueError("pilot rows must preserve raw and normalized correction text")
    review_document = final_review.get("document", {}) if final_review.get("status") == "loaded" else {}
    review_scope = review_document.get("review_scope", {})
    if review_scope and review_scope.get("editorially_edited_scene_count") != len(edited_rows):
        raise ValueError("final review editorial scene-edit count does not match pilot rows")
    correction_calls = review_document.get("correction_calls")
    correction_banks = review_document.get("bounded_model_correction_bank_passes")
    review_accounting = {
        "pilot_status": pilot_document["status"],
        "review_disclosure": pilot_document.get("review_disclosure"),
        "reviewed_candidate_count": len(prompts),
        "editorially_scene_edited_candidate_count": len(edited_rows),
        "editorially_scene_edited_candidate_keys": [row["candidate_key"] for row in edited_rows],
        "bounded_model_correction": {
            "banks": review_document.get("first_draw_banks"),
            "correction_calls": correction_calls,
            "bank_passes_after_correction": correction_banks,
            "semantic_retries": review_document.get("correction_semantic_retries"),
            "description": (
                "Each of four banks received one bounded GPT-5.5 correction pass; "
                "the reviewed corpus is not evidence of single-call production reliability."
                if correction_calls == correction_banks == 4 else
                "See the corpus-bound final review for correction accounting; no single-call reliability claim is made."
            ),
        },
    }
    feedback_audits = {
        "v4": feedback_pattern_audit(baseline, "same_case_final_v4"),
        "v4_1": feedback_pattern_audit(prompts, "v4.1_pilot"),
    }
    feedback_rows = []
    for indicator in ("unnatural_framing_or_place_phrase", "microscopic_wear_or_story_marker"):
        feedback_rows.append({
            "indicator": indicator,
            "v4_affected_prompt_count": feedback_audits["v4"]["categories"][indicator]["affected_prompt_count"],
            "v4_1_affected_prompt_count": feedback_audits["v4_1"]["categories"][indicator]["affected_prompt_count"],
        })

    rows = []
    for i, item in enumerate(prompts):
        nearest_ref = refs[int(nearest_idx[i])]
        nearest_candidate = prompts[int(nearest_candidate_idx[i])]
        row = {**item,
               "display_environment": item["environment"], "display_environment_rule": "native_v4.1_environment",
               "relationship": item["ctech_relationship"], "score": item["ctech_reference_score"], "selected": False,
               "word_count": len(words(item["text"])), "sentence_count": len(sentences(item["text"])),
               "semantic_nearest_candidate_similarity": round(float(nearest_candidate_value[i]), 6),
               "semantic_nearest_candidate_key": nearest_candidate["candidate_key"],
               "semantic_nearest_reference_similarity_scope_adjusted": round(float(nearest_value[i]), 6),
               "semantic_nearest_reference_id_scope_adjusted": nearest_ref["reference_id"],
               "semantic_declared_reference_similarity": round(float(declared_similarity[i]), 6),
               "declared_reference_is_semantic_nearest": bool(declared_idx[i] == nearest_idx[i]),
               "lexical_nearest_reference_similarity_scope_adjusted": round(float(lexical_similarity[i].max()), 6),
               "lexical_nearest_reference_id_scope_adjusted": refs[int(lexical_similarity[i].argmax())]["reference_id"],
               "map_x": round(float(coords[i, 0]), 6), "map_y": round(float(coords[i, 1]), 6)}
        rows.append(row)

    environment_counts = dict(sorted(Counter(row["environment"] for row in prompts).items()))
    ctech_relationship_counts = dict(sorted(Counter(row["ctech_relationship"] for row in prompts).items()))
    source_relationship_counts = dict(sorted(Counter(row["source_relationship"] for row in prompts).items()))
    declared_reference_counts = Counter(row["ctech_reference_id"] for row in prompts)
    reference_coverage = []
    for j, ref in enumerate(refs):
        assigned = np.where(nearest_idx == j)[0]
        reference_coverage.append({**ref,
            "assigned_prompt_count": int(len(assigned)), "declared_prompt_count": declared_reference_counts[ref["reference_id"]],
            "mean_assigned_similarity": round(float(np.mean(nearest_value[assigned])), 6) if len(assigned) else None,
            "maximum_similarity": round(float(similarity[:, j].max()), 6),
            "map_x": round(float(coords[n + j, 0]), 6), "map_y": round(float(coords[n + j, 1]), 6)})

    comparison = []
    for label in ("all", "close_up", "wide"):
        pi = [i for i, row in enumerate(prompts) if label == "all" or row["view_role"] == label]
        bi = [i for i, row in enumerate(baseline) if label == "all" or row["view_role"] == label]
        pmed = float(np.median(nearest_value[pi])); bmed = float(np.median(baseline_nearest[bi]))
        comparison.append({"label": label, "v4_1_count": len(pi), "v4_count": len(bi),
                           "v4_1_median": round(pmed, 6), "v4_median": round(bmed, 6),
                           "median_delta": round(pmed - bmed, 6),
                           "v4_1_mean": round(float(np.mean(nearest_value[pi])), 6),
                           "v4_mean": round(float(np.mean(baseline_nearest[bi])), 6)})

    exact_reference_matches = sum(row["text"] == refs[int(row["ctech_reference_id"][2:]) - 1]["scope_adjusted_text"] for row in prompts)
    analysis = {
        "version": "hp-v4.1-ctech-pilot-distribution-analysis-v1",
        "as_of": "2026-10-26",
        "status": "text_review_only_no_image_generation_authorized",
        "scope": {"prompt_count": n, "case_count": 4, "source_count": 2, "reference_prompt_count": r,
                  "baseline_prompt_count": b, "reference_ids": [ref["reference_id"] for ref in refs]},
        "inputs": {
            "pilot_prompts": {"path": str(PROMPTS), "sha256": sha256(PROMPTS), "bytes": PROMPTS.stat().st_size},
            "accepted_prompt_cases": {"path": str(ACCEPTED), "sha256": sha256(ACCEPTED)},
            "manifest": {"path": str(MANIFEST), "sha256": sha256(MANIFEST)},
            "v4_baseline": {"path": str(BASELINE), "sha256": sha256(BASELINE)},
            "reference_extraction": {"path": str(RAW_EXTRACTION), "sha256": sha256(RAW_EXTRACTION)},
            "reference_library": {"path": str(REFERENCE_LIBRARY), "sha256": sha256(REFERENCE_LIBRARY)},
            "user_reference_additions": {"path": str(USER_REFERENCE_ADDITIONS),
                                         "sha256": sha256(USER_REFERENCE_ADDITIONS),
                                         "raw_path": user_additions["raw_path"],
                                         "raw_sha256": user_additions["raw_sha256"]},
            "system_prompt": {"path": str(system_prompt), "sha256": sha256(system_prompt),
                              "bytes": system_prompt.stat().st_size},
            "final_text_review": final_review,
            "october_docx": extraction["authority"],
        },
        "methods": {
            "semantic_embedding": model_meta,
            "reference_normalization": "Removed only target-device prefixes, explicit no-hardware clauses, and blue-control clauses outside the approved environment-writer contract.",
            "lexical_reference_similarity": "Cosine similarity over corpus TF-IDF word unigrams and bigrams.",
            "map": {"method": f"PCA of 120 V4.1 prompt plus {r} normalized C-Tech reference embeddings",
                    "explained_variance_ratio_first_two": explained},
            "display_environment": {"derivation": "Direct V4.1 environment field; no post-hoc relabeling."},
        },
        "headline": {
            "exact_duplicate_prompt_groups": len(lexical["exact_duplicate_groups"]),
            "canonical_duplicate_prompt_groups": len(lexical["canonical_duplicate_groups"]),
            "exact_normalized_ctech_reference_matches": exact_reference_matches,
            "display_environment_counts": environment_counts,
            "display_environment_entropy": entropy(environment_counts),
            "relationship_counts": ctech_relationship_counts,
            "source_relationship_counts": source_relationship_counts,
            "semantic_pairwise_similarity_quantiles": quantiles(finite_pairs.tolist()),
            "semantic_nearest_neighbor_similarity_quantiles": quantiles(nearest_candidate_value.tolist()),
            "semantic_nearest_reference_scope_adjusted_quantiles": quantiles(nearest_value.tolist()),
            "semantic_declared_reference_similarity_quantiles": quantiles(declared_similarity.tolist()),
            "lexical_nearest_reference_scope_adjusted_quantiles": quantiles(lexical_similarity.max(axis=1).tolist()),
            "declared_reference_is_semantic_nearest_count": int(np.sum(declared_idx == nearest_idx)),
            "declared_reference_is_semantic_nearest_rate": round(float(np.mean(declared_idx == nearest_idx)), 6),
            "prompt_word_count_quantiles": quantiles([len(words(text)) for text in texts]),
            "v4_baseline_nearest_reference_quantiles": quantiles(baseline_nearest.tolist()),
        },
        "distributions": {
            "display_environment": environment_counts,
            "canonical_environment": environment_counts,
            "relationship": ctech_relationship_counts,
            "source_relationship": source_relationship_counts,
            "score_histogram": score_hist([row["ctech_reference_score"] for row in prompts]),
            "reference_similarity_histogram_scope_adjusted": similarity_hist(nearest_value),
            "reference_similarity_by_display_environment": grouped(rows, "display_environment", "semantic_nearest_reference_similarity_scope_adjusted"),
            "reference_similarity_by_relationship": grouped(rows, "ctech_relationship", "semantic_nearest_reference_similarity_scope_adjusted"),
            "reference_similarity_by_view": grouped(rows, "view_role", "semantic_nearest_reference_similarity_scope_adjusted"),
            "reference_similarity_by_rank_bin": grouped(rows, "rank_bin", "semantic_nearest_reference_similarity_scope_adjusted"),
            "declared_reference": dict(sorted(declared_reference_counts.items())),
        },
        "v4_baseline_comparison": comparison,
        "review_accounting": review_accounting,
        "feedback_pattern_comparison": {
            "interpretation": "Lexical indicators, not a complete style judgment.",
            "counting_unit": "Affected prompts, not match occurrences; each prompt counts at most once per indicator.",
            "methods": {
                "unnatural_framing_or_place_phrase": {
                    "pattern": UNNATURAL_PLACE_RE.pattern,
                    "flags": "IGNORECASE",
                    "copied_from": str(EVAL / "validate_output.py"),
                    "copied_pattern_version": UNNATURAL_PLACE_PATTERN_VERSION,
                },
                "microscopic_wear_or_story_marker": {
                    "pattern": MICROSCOPIC_STORY_RE.pattern,
                    "flags": "IGNORECASE",
                    "requested_exclusions": [
                        "pastry crumbs", "half-finished coffee", "overgrown plants",
                        "lived-in and authentic with subtle imperfections",
                    ],
                },
            },
            "comparison_rows": feedback_rows,
            "corpora": feedback_audits,
        },
        "case_inputs": case_inputs,
        "reference_coverage": reference_coverage,
        "recurring_phrases_top_30": lexical["recurring_phrases"][:30],
        "lexically_closest_prompt_pairs_top_20": lexical["closest_pairs"][:20],
        "closest_to_reference_top_20": sorted(rows, key=lambda row: row["semantic_nearest_reference_similarity_scope_adjusted"], reverse=True)[:20],
        "farthest_from_reference_top_20": sorted(rows, key=lambda row: row["semantic_nearest_reference_similarity_scope_adjusted"])[:20],
        "references": refs, "points": rows,
        "limitations": [
            "This is a 120-text pilot over two source messages and four close/wide banks, not the final nine-source distribution.",
            "Text similarity is descriptive: it does not require every pilot scene to reproduce a reference exactly and does not measure generated images.",
            "Education has no direct reference and therefore requires category extensions. Gaming now has two direct references; Gaming candidates based on other categories remain extensions.",
            "Close-up profiles necessarily delete room, object, and background details and are not directly comparable with wide prompts.",
            *run_limitations,
            "Embedding and TF-IDF similarity measure text proximity, not downstream image quality. No V4.1 image generation is authorized by this report.",
            "The V4 comparison uses the final accepted prompts for the same four source/camera cases; it is descriptive because V4.1 also changes ordering and reference-lineage fields.",
        ],
    }

    output.mkdir(parents=True, exist_ok=True)
    downloads = output / "downloads"; downloads.mkdir(exist_ok=True)
    gallery = output / "gallery"; gallery.mkdir(exist_ok=True)
    (downloads / "analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (downloads / "reference_prompts.json").write_text(json.dumps({"references": refs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (downloads / "lexical_audit.json").write_text(json.dumps(lexical, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(PROMPTS, downloads / "pilot_prompts.json")
    prompt_document = json.loads(PROMPTS.read_text(encoding="utf-8"))
    (downloads / "pilot_prompts.txt").write_text(render_plain_text_prompts(prompt_document), encoding="utf-8")
    shutil.copyfile(system_prompt, downloads / "system_prompt.md")
    fields = list(rows[0])
    with (downloads / "candidate_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    (gallery / "data.js").write_text("const ANALYSIS = " + json.dumps(analysis, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    for filename in ("index.html", "report.js", "style.css"):
        shutil.copyfile(TEMPLATE / filename, gallery / filename)
    shutil.copyfile(PROJECT / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/imsauth.js", gallery / "imsauth.js")
    manifest = {"version": "hp-v4.1-ctech-pilot-distribution-build-v1", "output": str(output),
                "inputs": analysis["inputs"], "artifacts": {},
                "counts": {"prompts": n, "references": r, "baseline_prompts": b, "candidate_csv_rows": len(rows)}}
    for path in sorted(p for p in output.rglob("*") if p.is_file() and p.name != "source_manifest.json"):
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
