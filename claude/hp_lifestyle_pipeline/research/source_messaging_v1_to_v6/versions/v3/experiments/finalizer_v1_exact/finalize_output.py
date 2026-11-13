#!/usr/bin/env python3
"""Transparent deterministic V3 score finalizer; never edits raw model output."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

PREFIX = "No cited source evidence: scored 0/100 by validation. "
LIMITATION = ("Host finalizer set empty-evidence candidates to zero relevance, "
              "recomputed component sums, and reranked the bank deterministically.")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode()


def semantic_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def finalize_output(raw_output: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    normalized = copy.deepcopy(raw_output)
    raw_hash = semantic_sha256(raw_output)
    changes = []
    original_order = {item["id"]: index for index, item in enumerate(normalized["prompts"])}

    for candidate in normalized["prompts"]:
        old_id = candidate["id"]
        old = {"source_relevance_score": candidate["source_relevance_score"],
               "score_components": copy.deepcopy(candidate["score_components"]),
               "relationship": candidate["relationship"],
               "explanation": candidate["explanation"]}
        reasons = []
        empty_evidence_needs_correction = (not candidate["evidence_ids"] and
            (candidate["source_relevance_score"] != 0
             or any(candidate["score_components"].values())
             or candidate["relationship"] != "creative_departure"))
        if empty_evidence_needs_correction:
            candidate["score_components"] = {"setting": 0, "activity": 0,
                                               "materials": 0, "use_context": 0}
            candidate["source_relevance_score"] = 0
            candidate["relationship"] = "creative_departure"
            if not candidate["explanation"].startswith(PREFIX):
                candidate["explanation"] = PREFIX + candidate["explanation"]
            reasons.append("empty_evidence_forced_zero")
        component_sum = sum(candidate["score_components"].values())
        if candidate["source_relevance_score"] != component_sum:
            candidate["source_relevance_score"] = component_sum
            reasons.append("score_recomputed_from_components")
        new = {"source_relevance_score": candidate["source_relevance_score"],
               "score_components": copy.deepcopy(candidate["score_components"]),
               "relationship": candidate["relationship"],
               "explanation": candidate["explanation"]}
        if old != new:
            changes.append({"original_id": old_id, "reasons": reasons,
                            "original_fields": old, "normalized_fields": new})

    # Python's sort is stable, preserving original order for exact score ties.
    normalized["prompts"].sort(key=lambda item: -item["source_relevance_score"])
    id_map = []
    for rank, candidate in enumerate(normalized["prompts"], 1):
        old_id = candidate["id"]
        new_id = f"p{rank}"
        candidate["id"] = new_id
        id_map.append({"original_id": old_id, "normalized_id": new_id,
                       "original_rank": original_order[old_id] + 1, "normalized_rank": rank})

    if changes or any(row["original_id"] != row["normalized_id"] for row in id_map):
        limitations = normalized["debug"]["limitations"]
        if LIMITATION not in limitations:
            limitations.append(LIMITATION)

    normalized_hash = semantic_sha256(normalized)
    log = {"version": "v3-deterministic-finalizer-v1",
           "algorithm": {"empty_evidence": "zero all components and total; creative_departure",
                         "all_candidates": "total equals declared component sum",
                         "ranking": "stable descending total, then p1..p30",
                         "text_edits": "none",
                         "citation_edits": "none"},
           "raw_output_semantic_sha256": raw_hash,
           "normalized_output_semantic_sha256": normalized_hash,
           "changed_candidate_count": len(changes), "changes": changes,
           "id_map": id_map}
    return normalized, log

