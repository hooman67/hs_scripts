#!/usr/bin/env python3
"""Reproducible mechanical statistics for the frozen V3 540-prompt export."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_INPUT = (
    PROJECT_ROOT
    / "eval_sets/hp_lifestyle_diversity_v3_eval_20261023/generation_prompts.json"
)
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "research/diversity_aware_v3/data/v3_generation_prompt_stats.json"
)
QUANTILE_PROBABILITIES = (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0)
SIMILARITY_HISTOGRAM_STEP = 0.05


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_text(text: str) -> str:
    """NFKC, casefold, retain Unicode word characters, collapse whitespace."""
    value = unicodedata.normalize("NFKC", text).casefold()
    value = re.sub(r"[^\w]+", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def word_tokens(text: str) -> list[str]:
    value = canonical_text(text)
    return value.split() if value else []


def ngrams(sequence: list[str] | str, n: int) -> set[Any]:
    if len(sequence) < n:
        return set()
    return {tuple(sequence[index : index + n]) for index in range(len(sequence) - n + 1)}


def char_ngrams(text: str, n: int = 3) -> set[str]:
    value = canonical_text(text)
    if len(value) < n:
        return {value} if value else set()
    return {value[index : index + n] for index in range(len(value) - n + 1)}


def jaccard(left: set[Any], right: set[Any]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def type7_quantile(sorted_values: list[float | int], probability: float) -> float:
    """R/NumPy linear quantile: h=(n-1)p, interpolate adjacent order statistics."""
    if not sorted_values:
        raise ValueError("quantile requires at least one value")
    h = (len(sorted_values) - 1) * probability
    lower = math.floor(h)
    upper = math.ceil(h)
    if lower == upper:
        return float(sorted_values[lower])
    fraction = h - lower
    return float(sorted_values[lower] + fraction * (sorted_values[upper] - sorted_values[lower]))


def numeric_summary(values: Iterable[float | int]) -> dict[str, Any]:
    sequence = list(values)
    ordered = sorted(sequence)
    return {
        "count": len(sequence),
        "min": ordered[0],
        "max": ordered[-1],
        "mean": sum(sequence) / len(sequence),
        "quantiles_type7": {
            f"p{round(probability * 100):02d}": type7_quantile(ordered, probability)
            for probability in QUANTILE_PROBABILITIES
        },
    }


def sorted_counts(values: Iterable[Any]) -> dict[str, int]:
    counts = Counter(str(value) for value in values)
    return {key: counts[key] for key in sorted(counts)}


def histogram(values: Iterable[int]) -> dict[str, int]:
    counts = Counter(values)
    return {str(key): counts[key] for key in sorted(counts)}


def similarity_histogram(values: Iterable[float]) -> dict[str, int]:
    bins = Counter()
    final_index = round(1 / SIMILARITY_HISTOGRAM_STEP)
    for value in values:
        index = min(int(value / SIMILARITY_HISTOGRAM_STEP), final_index - 1)
        lower = index * SIMILARITY_HISTOGRAM_STEP
        upper = (index + 1) * SIMILARITY_HISTOGRAM_STEP
        label = f"[{lower:.2f},{upper:.2f})" if upper < 1 else f"[{lower:.2f},1.00]"
        bins[label] += 1
    return {key: bins[key] for key in sorted(bins)}


def duplicate_audit(prompts: list[dict[str, Any]]) -> dict[str, Any]:
    def groups(key_function: Any) -> tuple[list[dict[str, Any]], int]:
        by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for prompt in prompts:
            by_key[key_function(prompt)].append(prompt)
        duplicate_groups = []
        duplicate_pairs = 0
        for key, members in sorted(by_key.items()):
            if len(members) < 2:
                continue
            duplicate_pairs += len(members) * (len(members) - 1) // 2
            duplicate_groups.append(
                {
                    "key": key,
                    "count": len(members),
                    "candidate_keys": sorted(member["candidate_key"] for member in members),
                    "text": members[0]["text"],
                }
            )
        return duplicate_groups, duplicate_pairs

    exact_groups, exact_pairs = groups(lambda prompt: prompt["text"])
    canonical_groups, canonical_pairs = groups(lambda prompt: canonical_text(prompt["text"]))
    return {
        "exact_raw_text": {
            "unique_count": len({prompt["text"] for prompt in prompts}),
            "duplicate_group_count": len(exact_groups),
            "duplicate_prompt_count": sum(group["count"] for group in exact_groups),
            "duplicate_pair_count": exact_pairs,
            "groups": exact_groups,
        },
        "canonical_text": {
            "normalization": "Unicode NFKC, casefold, non-word characters to spaces, whitespace collapsed",
            "unique_count": len({canonical_text(prompt["text"]) for prompt in prompts}),
            "duplicate_group_count": len(canonical_groups),
            "duplicate_prompt_count": sum(group["count"] for group in canonical_groups),
            "duplicate_pair_count": canonical_pairs,
            "groups": canonical_groups,
        },
    }


def pairwise_audit(prompts: list[dict[str, Any]]) -> dict[str, Any]:
    features = {
        prompt["candidate_key"]: {
            "word_bigrams": ngrams(word_tokens(prompt["text"]), 2),
            "char_trigrams": char_ngrams(prompt["text"], 3),
        }
        for prompt in prompts
    }
    by_key = {prompt["candidate_key"]: prompt for prompt in prompts}
    corpus_nearest: dict[str, dict[str, tuple[float, str]]] = defaultdict(dict)
    bank_nearest: dict[str, dict[str, tuple[float, str]]] = defaultdict(dict)
    corpus_values = {"word_bigram_jaccard": [], "char_trigram_jaccard": []}
    bank_values = {"word_bigram_jaccard": [], "char_trigram_jaccard": []}
    bank_pair_values: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: {"word_bigram_jaccard": [], "char_trigram_jaccard": []}
    )
    top_pairs: dict[str, list[tuple[float, str, str]]] = {
        "word_bigram_jaccard": [],
        "char_trigram_jaccard": [],
    }

    def update_nearest(
        target: dict[str, dict[str, tuple[float, str]]],
        key: str,
        metric: str,
        score: float,
        neighbor: str,
    ) -> None:
        existing = target[key].get(metric)
        candidate = (score, neighbor)
        if existing is None or score > existing[0] or (score == existing[0] and neighbor < existing[1]):
            target[key][metric] = candidate

    for left, right in combinations(prompts, 2):
        left_key = left["candidate_key"]
        right_key = right["candidate_key"]
        same_bank = left["case_id"] == right["case_id"]
        for metric, feature_name in (
            ("word_bigram_jaccard", "word_bigrams"),
            ("char_trigram_jaccard", "char_trigrams"),
        ):
            score = jaccard(features[left_key][feature_name], features[right_key][feature_name])
            corpus_values[metric].append(score)
            update_nearest(corpus_nearest, left_key, metric, score, right_key)
            update_nearest(corpus_nearest, right_key, metric, score, left_key)
            top_pairs[metric].append((score, left_key, right_key))
            if same_bank:
                bank_values[metric].append(score)
                bank_pair_values[left["case_id"]][metric].append(score)
                update_nearest(bank_nearest, left_key, metric, score, right_key)
                update_nearest(bank_nearest, right_key, metric, score, left_key)

    def pair_summary(values: dict[str, list[float]]) -> dict[str, Any]:
        return {
            metric: {
                **numeric_summary(scores),
                "histogram_step_0_05": similarity_histogram(scores),
            }
            for metric, scores in values.items()
        }

    nearest_rows = []
    for prompt in sorted(prompts, key=lambda value: value["candidate_key"]):
        key = prompt["candidate_key"]
        row: dict[str, Any] = {
            "candidate_key": key,
            "case_id": prompt["case_id"],
            "source_id": prompt["source_id"],
            "camera_tag": prompt["camera_tag"],
        }
        for scope, nearest in (("corpus", corpus_nearest), ("within_bank", bank_nearest)):
            row[scope] = {}
            for metric in ("word_bigram_jaccard", "char_trigram_jaccard"):
                score, neighbor_key = nearest[key][metric]
                neighbor = by_key[neighbor_key]
                row[scope][metric] = {
                    "similarity": score,
                    "neighbor_candidate_key": neighbor_key,
                    "neighbor_case_id": neighbor["case_id"],
                    "same_bank": prompt["case_id"] == neighbor["case_id"],
                    "same_source": prompt["source_id"] == neighbor["source_id"],
                    "same_camera": prompt["camera_tag"] == neighbor["camera_tag"],
                }
        nearest_rows.append(row)

    nearest_distribution = {}
    for scope, nearest in (("corpus", corpus_nearest), ("within_bank", bank_nearest)):
        nearest_distribution[scope] = {}
        for metric in ("word_bigram_jaccard", "char_trigram_jaccard"):
            scores = [nearest[prompt["candidate_key"]][metric][0] for prompt in prompts]
            nearest_distribution[scope][metric] = {
                **numeric_summary(scores),
                "histogram_step_0_05": similarity_histogram(scores),
            }

    highest_pairs = {}
    for metric, values in top_pairs.items():
        ordered = sorted(values, key=lambda value: (-value[0], value[1], value[2]))[:100]
        highest_pairs[metric] = [
            {
                "similarity": score,
                "left_candidate_key": left,
                "right_candidate_key": right,
                "same_bank": by_key[left]["case_id"] == by_key[right]["case_id"],
                "same_source": by_key[left]["source_id"] == by_key[right]["source_id"],
                "same_camera": by_key[left]["camera_tag"] == by_key[right]["camera_tag"],
            }
            for score, left, right in ordered
        ]

    return {
        "formula": {
            "canonical_text": "Unicode NFKC, casefold, non-word characters to spaces, whitespace collapsed",
            "word_feature": "set of contiguous canonical word bigrams",
            "character_feature": "set of contiguous canonical character trigrams, including collapsed single spaces",
            "similarity": "Jaccard(A,B)=|A intersection B|/|A union B|; empty/empty=1",
            "corpus_pairs": "all unordered prompt pairs",
            "within_bank_pairs": "unordered pairs sharing case_id",
            "nearest_neighbor": "maximum similarity; ties use lexicographically smallest candidate_key",
            "histogram": "left-closed 0.05 bins; final bin includes 1.00",
        },
        "corpus_pair_count": len(prompts) * (len(prompts) - 1) // 2,
        "within_bank_pair_count": sum(
            len(values) * (len(values) - 1) // 2
            for values in defaultdict(list, {
                case_id: [p for p in prompts if p["case_id"] == case_id]
                for case_id in sorted({p["case_id"] for p in prompts})
            }).values()
        ),
        "pairwise": {
            "corpus": pair_summary(corpus_values),
            "within_bank": pair_summary(bank_values),
            "within_each_bank": {
                case_id: pair_summary(values)
                for case_id, values in sorted(bank_pair_values.items())
            },
        },
        "nearest_neighbor_distributions": nearest_distribution,
        "nearest_neighbors": nearest_rows,
        "highest_similarity_pairs_top_100": highest_pairs,
    }


def recurring_phrases(prompts: list[dict[str, Any]]) -> dict[str, Any]:
    prompt_tokens = {prompt["candidate_key"]: word_tokens(prompt["text"]) for prompt in prompts}
    prompt_by_key = {prompt["candidate_key"]: prompt for prompt in prompts}
    results = {}
    flags = []
    for n in (3, 4, 5, 6):
        document_keys: dict[tuple[str, ...], set[str]] = defaultdict(set)
        occurrence_counts: Counter[tuple[str, ...]] = Counter()
        for key, tokens in prompt_tokens.items():
            sequence = [tuple(tokens[index : index + n]) for index in range(len(tokens) - n + 1)]
            occurrence_counts.update(sequence)
            for phrase in set(sequence):
                document_keys[phrase].add(key)
        rows = []
        for phrase, keys in document_keys.items():
            if len(keys) < 2:
                continue
            members = [prompt_by_key[key] for key in keys]
            row = {
                "phrase": " ".join(phrase),
                "n": n,
                "prompt_document_frequency": len(keys),
                "prompt_coverage": len(keys) / len(prompts),
                "total_occurrences": occurrence_counts[phrase],
                "case_count": len({member["case_id"] for member in members}),
                "source_count": len({member["source_id"] for member in members}),
                "camera_count": len({member["camera_tag"] for member in members}),
                "candidate_keys": sorted(keys),
            }
            rows.append(row)
            if len(keys) >= 10:
                flags.append(row)
        rows.sort(key=lambda row: (-row["prompt_document_frequency"], -row["total_occurrences"], row["phrase"]))
        results[f"word_{n}gram"] = {
            "recurring_phrase_count_df_ge_2": len(rows),
            "top_100": rows[:100],
        }
    flags.sort(key=lambda row: (-row["prompt_document_frequency"], -row["n"], row["phrase"]))
    return {
        "formula": "Canonical contiguous word n-grams; document frequency counts each prompt at most once; flagged when frequency >=10/540.",
        "by_ngram_size": results,
        "flagged_recurring_phrases_df_ge_10": flags,
    }


def build_audit(document: dict[str, Any], input_path: Path, input_sha256: str) -> dict[str, Any]:
    prompts = document["prompts"]
    if len(prompts) != 540:
        raise ValueError(f"Expected 540 prompts, found {len(prompts)}")
    candidate_keys = [prompt["candidate_key"] for prompt in prompts]
    if len(set(candidate_keys)) != len(candidate_keys):
        raise ValueError("candidate_key values are not unique")
    for prompt in prompts:
        if sha256_bytes(prompt["text"].encode()) != prompt["text_sha256"]:
            raise ValueError(f"text_sha256 mismatch: {prompt['candidate_key']}")

    character_lengths = [len(prompt["text"]) for prompt in prompts]
    normalized_character_lengths = [len(canonical_text(prompt["text"])) for prompt in prompts]
    word_lengths = [len(word_tokens(prompt["text"])) for prompt in prompts]
    sentence_lengths = [len(re.findall(r"[^.!?]+[.!?]?", prompt["text"])) for prompt in prompts]
    departure_counts = [len(prompt["creative_departures"]) for prompt in prompts]
    departure_strings = [item for prompt in prompts for item in prompt["creative_departures"]]
    scores = [prompt["score"] for prompt in prompts]

    distributions = {
        "environment": sorted_counts(prompt["environment"] for prompt in prompts),
        "subsetting": sorted_counts(prompt["subsetting"] for prompt in prompts),
        "relationship": sorted_counts(prompt["relationship"] for prompt in prompts),
        "source_id": sorted_counts(prompt["source_id"] for prompt in prompts),
        "device_type": sorted_counts(prompt["device_type"] for prompt in prompts),
        "camera_tag": sorted_counts(prompt["camera_tag"] for prompt in prompts),
        "view_role": sorted_counts(prompt["view_role"] for prompt in prompts),
        "rank_bin": sorted_counts(prompt["rank_bin"] for prompt in prompts),
        "rank": histogram(prompt["rank"] for prompt in prompts),
        "selected_for_image_eval": sorted_counts(prompt["selected_for_image_eval"] for prompt in prompts),
        "score": {"histogram": histogram(scores), **numeric_summary(scores)},
        "creative_departures": {
            "prompt_count_with_any": sum(bool(count) for count in departure_counts),
            "prompt_count_without_any": sum(not count for count in departure_counts),
            "departure_count_per_prompt_histogram": histogram(departure_counts),
            "total_departure_statements": len(departure_strings),
            "unique_departure_statements": len(set(departure_strings)),
            "exact_statement_counts": sorted_counts(departure_strings),
        },
        "prompt_length": {
            "characters": {"histogram": histogram(character_lengths), **numeric_summary(character_lengths)},
            "canonical_characters": {
                "histogram": histogram(normalized_character_lengths),
                **numeric_summary(normalized_character_lengths),
            },
            "canonical_words": {"histogram": histogram(word_lengths), **numeric_summary(word_lengths)},
            "sentences_regex": {"histogram": histogram(sentence_lengths), **numeric_summary(sentence_lengths)},
        },
        "score_by_relationship": {
            relationship: numeric_summary(
                prompt["score"] for prompt in prompts if prompt["relationship"] == relationship
            )
            for relationship in sorted({prompt["relationship"] for prompt in prompts})
        },
        "score_by_source": {
            source: numeric_summary(prompt["score"] for prompt in prompts if prompt["source_id"] == source)
            for source in sorted({prompt["source_id"] for prompt in prompts})
        },
        "score_by_camera": {
            camera: numeric_summary(prompt["score"] for prompt in prompts if prompt["camera_tag"] == camera)
            for camera in sorted({prompt["camera_tag"] for prompt in prompts})
        },
    }

    return {
        "version": "v3-generation-prompt-stats-v1",
        "input": {
            "path": str(input_path.resolve()),
            "sha256": input_sha256,
            "bytes": input_path.stat().st_size,
            "export_version": document.get("version"),
            "export_as_of": document.get("as_of"),
            "scope": document.get("scope"),
        },
        "validation": {
            "prompt_count": len(prompts),
            "candidate_keys_unique": True,
            "text_sha256_all_verified": True,
            "case_count": len({prompt["case_id"] for prompt in prompts}),
            "source_count": len({prompt["source_id"] for prompt in prompts}),
            "camera_count": len({prompt["camera_tag"] for prompt in prompts}),
        },
        "formulas": {
            "categorical_distribution": "exact frequency count over 540 prompts",
            "histogram": "exact frequency by observed numeric value",
            "quantiles": "type-7 linear interpolation: h=(n-1)p, interpolate adjacent sorted values",
            "character_length": "Python len() of exported prompt text (Unicode code points)",
            "canonical_word_length": "token count after NFKC/casefold/non-word-to-space normalization",
            "sentence_count": "count of nonempty spans matched by regex [^.!?]+[.!?]?",
            "duplicate_pairs": "sum over duplicate groups of n*(n-1)/2",
        },
        "distributions": distributions,
        "duplicates": duplicate_audit(prompts),
        "similarity": pairwise_audit(prompts),
        "recurring_phrases": recurring_phrases(prompts),
        "limitations": [
            "These are lexical statistics and do not measure semantic or visual diversity.",
            "Jaccard uses sets, so repeated n-grams within one prompt do not add weight.",
            "Character trigrams include normalized spaces and are sensitive to wording and morphology.",
            "Word bigrams ignore word order beyond adjacent pairs and do not use stemming or synonyms.",
            "Nearest-neighbor similarity can be high because prompts share campaign vocabulary; it is not proof of duplication.",
            "Recurring phrases are mechanically flagged by document frequency >=10 and are not judged as good or bad.",
            "The audit reads only generation_prompts.json and does not read or interpret the C-Tech DOCX.",
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
    print(json.dumps({
        "output": str(output_path),
        "prompt_count": audit["validation"]["prompt_count"],
        "exact_duplicate_groups": audit["duplicates"]["exact_raw_text"]["duplicate_group_count"],
        "canonical_duplicate_groups": audit["duplicates"]["canonical_text"]["duplicate_group_count"],
        "corpus_pair_count": audit["similarity"]["corpus_pair_count"],
        "within_bank_pair_count": audit["similarity"]["within_bank_pair_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
