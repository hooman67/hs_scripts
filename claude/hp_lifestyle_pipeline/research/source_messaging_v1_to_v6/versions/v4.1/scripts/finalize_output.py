#!/usr/bin/env python3
"""Transparent deterministic V4.1 score finalizer; never edits scene text."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

from camera_profile_resolver import resolve_profile

PREFIX = "No cited source evidence: scored 0/100 by validation. "
LIMITATION = ("Host finalizer set empty-evidence candidates to zero source relevance, "
              "recomputed source component sums, clamped C-Tech scores to the declared "
              "relationship's fixed rubric band, repaired uniquely verifiable evidence "
              "paths, preserved model-authored reference explanations and edits, and reranked the bank by "
              "C-Tech reference score with source relevance as the tie-breaker.")

CTECH_SCORE_BANDS = {
    "exact_reference": (100, 100),
    "minimal_camera_edit": (80, 99),
    "close_adaptation": (70, 79),
    "category_extension": (60, 69),
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode()


def semantic_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def finalize_output(raw_output: dict[str, Any], *, raw_input: dict[str, Any] | None = None,
                    registry: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    if (raw_input is None) != (registry is None):
        raise ValueError("raw_input and registry must be supplied together")
    normalized = copy.deepcopy(raw_output)
    raw_hash = semantic_sha256(raw_output)
    changes = []
    ctech_change_summaries = []
    ctech_explanation_summaries = []
    original_order = {item["id"]: index for index, item in enumerate(normalized["prompts"])}

    for candidate in normalized["prompts"]:
        old_id = candidate["id"]
        old = {"ctech_reference_score": candidate["ctech_reference_score"],
               "source_relevance_score": candidate["source_relevance_score"],
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
        low, high = CTECH_SCORE_BANDS[candidate["ctech_relationship"]]
        clamped = min(high, max(low, candidate["ctech_reference_score"]))
        if clamped != candidate["ctech_reference_score"]:
            candidate["ctech_reference_score"] = clamped
            reasons.append("ctech_score_clamped_to_declared_relationship_band")
        new = {"ctech_reference_score": candidate["ctech_reference_score"],
               "source_relevance_score": candidate["source_relevance_score"],
               "score_components": copy.deepcopy(candidate["score_components"]),
               "relationship": candidate["relationship"],
               "explanation": candidate["explanation"]}
        if old != new:
            changes.append({"original_id": old_id, "reasons": reasons,
                            "original_fields": old, "normalized_fields": new})

    citation_path_repairs = []
    if raw_input is not None:
        source_messaging = raw_input.get("source_messaging", {})
        for evidence in normalized["debug"]["source_evidence"]:
            message_id = evidence["message_id"]
            message = source_messaging.get(message_id)
            if not isinstance(message, dict):
                continue
            quote = evidence["quote"]
            original_path = evidence["path"]
            leaf = original_path.rsplit(".", 1)[-1]
            matches = [key for key, value in message.items()
                       if isinstance(value, str) and quote in value]
            if leaf in message and isinstance(message[leaf], str) and quote in message[leaf]:
                resolved_leaf = leaf
            elif len(matches) == 1:
                resolved_leaf = matches[0]
            else:
                continue
            expected_path = f"{message_id}.{resolved_leaf}"
            if original_path != expected_path:
                evidence["path"] = expected_path
                citation_path_repairs.append({"evidence_id": evidence["id"],
                    "message_id": message_id, "quote": quote,
                    "original_path": original_path, "normalized_path": expected_path,
                    "reason": "quote_verified_in_declared_message_field"})

    # Python's sort is stable, preserving original order for exact two-score ties.
    normalized["prompts"].sort(
        key=lambda item: (-item["ctech_reference_score"],
                          -item["source_relevance_score"])
    )
    id_map = []
    for rank, candidate in enumerate(normalized["prompts"], 1):
        old_id = candidate["id"]
        new_id = f"p{rank}"
        candidate["id"] = new_id
        id_map.append({"original_id": old_id, "normalized_id": new_id,
                       "original_rank": original_order[old_id] + 1, "normalized_rank": rank})

    if (changes or ctech_change_summaries or ctech_explanation_summaries
            or citation_path_repairs
            or any(row["original_id"] != row["normalized_id"] for row in id_map)):
        limitations = normalized["debug"]["limitations"]
        if LIMITATION not in limitations:
            limitations.append(LIMITATION)

    camera_metadata_repair = None
    if raw_input is not None and registry is not None:
        resolution = resolve_profile(registry, raw_input.get("camera_tag"))
        expected_camera = {"requested_tag": raw_input.get("camera_tag", ""),
            "resolved_tag": resolution["resolved_tag"], "device_type": resolution["device_type"],
            "profile_version": resolution["profile_version"], "resolution": resolution["resolution"],
            **resolution["effective_profile"]}
        original_camera = normalized["debug"]["camera"]
        if original_camera != expected_camera:
            camera_metadata_repair = {"reason": "offline_registry_resolution",
                                      "original_camera": copy.deepcopy(original_camera),
                                      "normalized_camera": copy.deepcopy(expected_camera)}
            normalized["debug"]["camera"] = expected_camera

    normalized_hash = semantic_sha256(normalized)
    log = {"version": "v4.1-deterministic-finalizer-v2",
           "algorithm": {"empty_evidence": "zero all components and total; creative_departure",
                         "all_candidates": "total equals declared component sum",
                         "ctech_score": "clamp to the fixed band for the model-declared C-Tech relationship; never change relationship or text",
                         "ctech_changes": "preserve model-authored change summary",
                         "ctech_explanation": "preserve model-authored explanation",
                         "ranking": "stable descending C-Tech reference score, then source relevance, then p1..p30",
                         "text_edits": "none",
                         "citation_edits": "repair a path only when its quote is verified in the declared source-message field"},
           "raw_output_semantic_sha256": raw_hash,
           "normalized_output_semantic_sha256": normalized_hash,
           "changed_candidate_count": len(changes), "changes": changes,
           "ctech_change_summary_count": len(ctech_change_summaries),
           "ctech_change_summaries": ctech_change_summaries,
           "ctech_explanation_summary_count": len(ctech_explanation_summaries),
           "ctech_explanation_summaries": ctech_explanation_summaries,
           "id_map": id_map}
    if citation_path_repairs:
        log["citation_path_repairs"] = citation_path_repairs
    if camera_metadata_repair is not None:
        log["camera_metadata_repair"] = camera_metadata_repair
    return normalized, log

