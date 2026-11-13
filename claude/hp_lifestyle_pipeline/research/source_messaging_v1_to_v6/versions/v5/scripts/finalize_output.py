#!/usr/bin/env python3
"""Narrow deterministic V5 finalizer; never edits scene prose or evidence."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

try:  # Package import in tests; direct import when invoked as a script.
    from .camera_profile_resolver import resolve_profile
except ImportError:  # pragma: no cover - exercised by CLI use
    from camera_profile_resolver import resolve_profile


DOCUMENTS = ("smart_brief", "source_messaging")
COMPONENTS = ("setting", "activity", "materials", "use_context")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def semantic_sha256(value: Any) -> str:
    """Return a SHA-256 over canonical JSON semantics."""

    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _expected_camera(raw_input: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    resolution = resolve_profile(registry, raw_input.get("camera_tag"))
    return {
        "requested_tag": raw_input.get("camera_tag", ""),
        "resolved_tag": resolution["resolved_tag"],
        "device_type": resolution["device_type"],
        "profile_version": resolution["profile_version"],
        "resolution": resolution["resolution"],
        **resolution["effective_profile"],
    }


def finalize_output(
    output: dict[str, Any],
    raw_input: dict[str, Any] | None = None,
    registry: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Apply only deterministic V5 host-owned normalization.

    Repairs are limited to unsupported-document zeroing, exact per-component
    source aggregation, camera debug metadata, ranking, and p1..p20 IDs. Candidate
    prose, evidence, reference declarations, relationships, and explanations
    are preserved byte-for-byte at the string level.
    """

    if (raw_input is None) != (registry is None):
        raise ValueError("raw_input and registry must be supplied together")

    normalized = copy.deepcopy(output)
    raw_hash = semantic_sha256(output)
    evidence_by_id = {
        evidence.get("id"): evidence
        for evidence in normalized.get("debug", {}).get("source_evidence", [])
        if isinstance(evidence, dict)
    }
    candidate_changes: list[dict[str, Any]] = []

    indexed_prompts = list(enumerate(normalized["prompts"]))
    for original_index, candidate in indexed_prompts:
        original_components = copy.deepcopy(candidate["score_components"])
        original_score = candidate["source_relevance_score"]
        cited_documents = {
            evidence_by_id[evidence_id].get("document")
            for evidence_id in candidate.get("evidence_ids", [])
            if evidence_id in evidence_by_id
        }
        reasons: list[str] = []
        zeroed_documents: list[str] = []
        for document in DOCUMENTS:
            group = candidate["score_components"][document]
            if document not in cited_documents and any(group.values()):
                candidate["score_components"][document] = {
                    name: 0 for name in COMPONENTS
                }
                zeroed_documents.append(document)
        if zeroed_documents:
            reasons.append("unsupported_document_components_zeroed")

        expected_score = sum(
            max(
                candidate["score_components"]["smart_brief"][name],
                candidate["score_components"]["source_messaging"][name],
            )
            for name in COMPONENTS
        )
        if candidate["source_relevance_score"] != expected_score:
            candidate["source_relevance_score"] = expected_score
            reasons.append("source_relevance_recomputed_as_component_max_sum")

        if reasons:
            candidate_changes.append({
                "original_index": original_index,
                "original_id": candidate["id"],
                "reasons": reasons,
                "zeroed_documents": zeroed_documents,
                "original_fields": {
                    "score_components": original_components,
                    "source_relevance_score": original_score,
                },
                "normalized_fields": {
                    "score_components": copy.deepcopy(candidate["score_components"]),
                    "source_relevance_score": candidate["source_relevance_score"],
                },
            })

    # Python's stable sort preserves model order for exact two-score ties.
    ranked = sorted(
        indexed_prompts,
        key=lambda pair: (
            -pair[1]["source_relevance_score"],
            -pair[1]["ctech_reference_score"],
        ),
    )
    normalized["prompts"] = [candidate for _, candidate in ranked]

    id_map: list[dict[str, Any]] = []
    order_changed = False
    for normalized_index, (original_index, candidate) in enumerate(ranked):
        original_id = candidate["id"]
        normalized_id = f"p{normalized_index + 1}"
        if original_index != normalized_index or original_id != normalized_id:
            order_changed = True
        candidate["id"] = normalized_id
        id_map.append({
            "original_index": original_index,
            "original_rank": original_index + 1,
            "original_id": original_id,
            "normalized_rank": normalized_index + 1,
            "normalized_id": normalized_id,
        })

    camera_metadata_repair = None
    if raw_input is not None and registry is not None:
        expected_camera = _expected_camera(raw_input, registry)
        original_camera = normalized["debug"]["camera"]
        if original_camera != expected_camera:
            camera_metadata_repair = {
                "reason": "offline_registry_resolution",
                "original_camera": copy.deepcopy(original_camera),
                "normalized_camera": copy.deepcopy(expected_camera),
            }
            normalized["debug"]["camera"] = expected_camera

    normalized_hash = semantic_sha256(normalized)
    log: dict[str, Any] = {
        "version": "v5-deterministic-finalizer-r2",
        "algorithm": {
            "unsupported_document_components": (
                "zero one document's four components when the candidate cites no "
                "evidence from that document"
            ),
            "source_relevance": (
                "sum of the smart_brief/source_messaging maximum for each of "
                "setting, activity, materials, and use_context"
            ),
            "camera": "replace debug.camera from the offline registry when inputs are supplied",
            "ranking": (
                "stable descending source relevance, then C-Tech reference score, "
                "then p1..p20"
            ),
            "scene_text_edits": "none",
            "evidence_edits": "none",
            "relationship_edits": "none",
            "ctech_declaration_edits": "none",
        },
        "raw_output_semantic_sha256": raw_hash,
        "normalized_output_semantic_sha256": normalized_hash,
        "changed_candidate_count": len(candidate_changes),
        "changes": candidate_changes,
        "order_or_id_changed": order_changed,
        "id_map": id_map,
    }
    if camera_metadata_repair is not None:
        log["camera_metadata_repair"] = camera_metadata_repair
    return normalized, log

