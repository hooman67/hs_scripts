#!/usr/bin/env python3
"""Build the deterministic eight-case V5 dual-source text pilot.

The runtime input contract stays deliberately small.  All source provenance,
DOCX paragraph coordinates, and the known Cashmere identity conflict remain in
the manifests and never enter the model input.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DUAL_SOURCE = ROOT / "research/dual_source_v5"
NORMALIZED = DUAL_SOURCE / "inputs/normalized"
VERSION = ROOT / "research/source_messaging_v1_to_v6/versions/v5"
VERSION_SCRIPTS = VERSION / "scripts"
sys.path.insert(0, str(VERSION_SCRIPTS))

from camera_profile_resolver import load_registry, resolve_profile  # noqa: E402


PAIR_DEVICE = (
    ("elitebook", "laptop"),
    ("deskjet_2955", "printer"),
    ("laserjet", "printer"),
    ("cashmere", "laptop"),
)
CAMERA_NAMES = (("FrontRightCloseUp", "close_up"), ("FrontRightWide", "wide"))
RUNTIME_FIELDS = ("smart_brief", "source_messaging", "camera_tag")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def file_record(path: Path) -> dict[str, Any]:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha_file(path)}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(payload, encoding="utf-8")
    temporary.replace(path)


def project_txt(normalized: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    text = normalized["raw_text"]
    if len(text) != normalized["decoded_character_count"]:
        raise ValueError("TXT decoded_character_count does not match raw_text")
    line_text = "".join(item["text"] + item["line_ending"] for item in normalized["lines"])
    if line_text != text:
        raise ValueError("TXT line projection does not reconstruct raw_text exactly")
    return text, {
        "format": "txt",
        "normalized_text_field": "raw_text",
        "source_character_count": len(text),
        "projected_character_count": len(text),
        "source_text_sha256": sha_bytes(text.encode("utf-8")),
        "projected_text_sha256": sha_bytes(text.encode("utf-8")),
        "line_count": len(normalized["lines"]),
        "verification": {
            "raw_text_length_matches_normalized_count": True,
            "line_records_reconstruct_raw_text_exactly": True,
            "no_text_loss_or_duplication": True,
        },
    }


def project_docx(normalized: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    paragraphs: list[dict[str, Any]] = []
    source_texts: list[str] = []
    for story_index, story in enumerate(normalized["stories"], 1):
        story_paragraphs = story["all_paragraphs_xml_order"]
        if len(story_paragraphs) != story["paragraph_count"]:
            raise ValueError(f"DOCX story count mismatch: {story['story_part']}")
        for story_paragraph_index, paragraph in enumerate(story_paragraphs, 1):
            segment_text = "".join(segment.get("text", "") for segment in paragraph["segments"])
            if segment_text != paragraph["text"]:
                raise ValueError(f"DOCX segment mismatch: {paragraph['provenance']}")
            source_texts.append(paragraph["text"])
            paragraphs.append(
                {
                    "paragraph_index": len(paragraphs) + 1,
                    "story_index": story_index,
                    "story_part": story["story_part"],
                    "story_paragraph_index": story_paragraph_index,
                    "provenance": paragraph["provenance"],
                    "style": paragraph.get("style"),
                    "source_text_character_count": len(paragraph["text"]),
                    "source_text_sha256": sha_bytes(paragraph["text"].encode("utf-8")),
                }
            )

    if len(source_texts) != normalized["paragraph_count"]:
        raise ValueError("DOCX aggregate paragraph_count mismatch")

    text = "\n".join(source_texts)
    cursor = 0
    reconstructed: list[str] = []
    for index, (entry, source_text) in enumerate(zip(paragraphs, source_texts, strict=True)):
        if index:
            if text[cursor : cursor + 1] != "\n":
                raise AssertionError("missing paragraph separator")
            cursor += 1
        start = cursor
        cursor += len(source_text)
        entry["projected_text_start"] = start
        entry["projected_text_end"] = cursor
        projected = text[start:cursor]
        if projected != source_text:
            raise AssertionError(f"paragraph projection mismatch: {entry['provenance']}")
        reconstructed.append(projected)
    if cursor != len(text) or reconstructed != source_texts:
        raise AssertionError("DOCX projection did not preserve the paragraph sequence")

    sequence_sha = sha_bytes(canonical_bytes(source_texts))
    projected_sequence_sha = sha_bytes(canonical_bytes(reconstructed))
    if sequence_sha != projected_sequence_sha:
        raise AssertionError("DOCX paragraph sequence hash mismatch")
    return text, {
        "format": "docx",
        "flattening": "stories in normalized order; all_paragraphs_xml_order within each story; one newline separator between paragraphs",
        "story_count": len(normalized["stories"]),
        "source_paragraph_count": normalized["paragraph_count"],
        "projected_paragraph_count": len(paragraphs),
        "source_paragraph_text_character_count": sum(map(len, source_texts)),
        "projected_text_character_count_including_separators": len(text),
        "source_paragraph_sequence_sha256": sequence_sha,
        "projected_paragraph_sequence_sha256": projected_sequence_sha,
        "projected_text_sha256": sha_bytes(text.encode("utf-8")),
        "paragraphs": paragraphs,
        "verification": {
            "all_stories_included": True,
            "segment_text_matches_each_normalized_paragraph": True,
            "paragraph_count_matches_normalized_source": True,
            "every_projection_range_matches_source_paragraph": True,
            "paragraph_sequence_hash_matches": True,
            "no_text_loss_or_duplication": True,
        },
    }


def project_file(path: Path, expected: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    normalized = json.loads(path.read_text(encoding="utf-8"))
    source_file = normalized["source_file"]
    for key in ("file_id", "role", "filename", "sha256"):
        if source_file[key] != expected[key]:
            raise ValueError(f"pair/normalized metadata mismatch for {key}: {path}")
    if normalized["format"] == "txt":
        text, projection = project_txt(normalized)
    elif normalized["format"] == "docx":
        text, projection = project_docx(normalized)
    else:
        raise ValueError(f"unsupported selected format: {normalized['format']}")
    projection.update(
        {
            "role": expected["role"],
            "file_id": expected["file_id"],
            "filename": expected["filename"],
            "source_sha256": expected["sha256"],
            "normalized_path": str(path),
            "normalized_sha256": sha_file(path),
            "durable_original": source_file["durable_original"],
        }
    )
    return text, projection


def validate_runtime_input(payload: dict[str, Any], tag: str) -> None:
    if tuple(payload) != RUNTIME_FIELDS or set(payload) != set(RUNTIME_FIELDS):
        raise ValueError("runtime input must contain exactly smart_brief, source_messaging, camera_tag")
    if not all(isinstance(payload[key], str) for key in RUNTIME_FIELDS):
        raise ValueError("all V5 pilot runtime fields must be strings")
    if payload["camera_tag"] != tag:
        raise ValueError("camera tag mismatch")


def main() -> None:
    input_schema = json.loads((VERSION / "input.schema.json").read_text(encoding="utf-8"))
    if set(input_schema.get("required", [])) != set(RUNTIME_FIELDS) or input_schema.get("additionalProperties") is not False:
        raise ValueError("V5 input schema does not match the frozen runtime contract")
    registry = load_registry(VERSION / "camera_profiles.json")
    projections: dict[str, dict[str, Any]] = {}
    pair_payloads: dict[str, dict[str, str]] = {}

    for pair_id, _device_type in PAIR_DEVICE:
        pair_path = NORMALIZED / "pairs" / f"{pair_id}.json"
        pair = json.loads(pair_path.read_text(encoding="utf-8"))
        if pair["pair_id"] != pair_id or len(pair["files"]) != 2:
            raise ValueError(f"unexpected normalized pair: {pair_id}")
        role_map = {item["role"]: item for item in pair["files"]}
        if set(role_map) != {"smart_brief", "source_messaging"}:
            raise ValueError(f"pair does not have exactly the two required roles: {pair_id}")
        pair_payloads[pair_id] = {}
        projections[pair_id] = {
            "pair_id": pair_id,
            "pair_path": str(pair_path),
            "pair_sha256": sha_file(pair_path),
            "files": {},
        }
        for role in ("smart_brief", "source_messaging"):
            expected = role_map[role]
            normalized_path = DUAL_SOURCE / expected["normalized_path"]
            text, projection = project_file(normalized_path, expected)
            pair_payloads[pair_id][role] = text
            projections[pair_id]["files"][role] = projection

    projection_manifest = {
        "version": "hp-lifestyle-dual-source-v5-input-projection-v1",
        "as_of": "2026-10-27",
        "runtime_fields": list(RUNTIME_FIELDS),
        "selected_pairs": [pair_id for pair_id, _ in PAIR_DEVICE],
        "excluded_pairs": ["modric"],
        "projection_rule": "TXT uses normalized raw_text exactly; DOCX uses every normalized story and every paragraph in XML order exactly once",
        "pairs": projections,
        "verification": {
            "selected_pair_count": len(projections),
            "selected_file_count": sum(len(item["files"]) for item in projections.values()),
            "all_projections_no_text_loss_or_duplication": all(
                file_projection["verification"]["no_text_loss_or_duplication"]
                for pair in projections.values()
                for file_projection in pair["files"].values()
            ),
        },
    }
    projection_path = HERE / "input_projection_manifest.json"
    write_json(projection_path, projection_manifest)

    cases: list[dict[str, Any]] = []
    for pair_id, device_type in PAIR_DEVICE:
        for camera_name, view_role in CAMERA_NAMES:
            tag = f"{device_type}_{camera_name}"
            case_id = f"{pair_id}__{tag}"
            payload = {
                "smart_brief": pair_payloads[pair_id]["smart_brief"],
                "source_messaging": pair_payloads[pair_id]["source_messaging"],
                "camera_tag": tag,
            }
            validate_runtime_input(payload, tag)
            input_path = HERE / "inputs" / f"{case_id}.json"
            write_json(input_path, payload)
            resolution = resolve_profile(registry, tag)
            if resolution["resolution"] != "exact" or resolution["device_type"] != device_type:
                raise ValueError(f"camera profile mismatch: {case_id}")
            cases.append(
                {
                    "case_id": case_id,
                    "group_id": f"{pair_id}__{device_type}_FrontRight",
                    "pair_id": pair_id,
                    "device_type": device_type,
                    "camera_tag": tag,
                    "view_role": view_role,
                    "product_identity_conflict": pair_id == "cashmere",
                    "input_path": str(input_path),
                    "input_sha256": sha_file(input_path),
                    "input_semantic_sha256": sha_bytes(canonical_bytes(payload)),
                    "human_review_status": "pending",
                    "launchable": False,
                    "expected_camera": {
                        "requested_tag": tag,
                        "resolved_tag": resolution["resolved_tag"],
                        "device_type": resolution["device_type"],
                        "profile_version": resolution["profile_version"],
                        "resolution": resolution["resolution"],
                        **resolution["effective_profile"],
                    },
                }
            )

    manifest = {
        "version": "hp-lifestyle-dual-source-v5-text-pilot-v1",
        "as_of": "2026-10-27",
        "status": "ready_for_bounded_actual_gpt5_5_text_pilot_human_review_pending",
        "launchable": False,
        "scope": {
            "pair_count": len(PAIR_DEVICE),
            "case_count": len(cases),
            "candidates_per_case": 20,
            "candidate_count": len(cases) * 20,
            "runtime_input_fields": list(RUNTIME_FIELDS),
            "included_pairs": [pair_id for pair_id, _ in PAIR_DEVICE],
            "excluded_pairs": ["modric"],
            "cashmere_product_identity_conflict": True,
            "text_generation_authorized": True,
            "image_generation_authorized": False,
            "human_review_status": "pending",
        },
        "model": {
            "deployment": "gpt-5.5",
            "reasoning_effort": "medium",
            "max_completion_tokens": 24000,
            "temperature": None,
            "strict_output_schema": True,
            "max_concurrency": 2,
            "max_transport_attempts": 100,
            "semantic_attempts_per_case": 1,
        },
        "provenance": {
            "system_prompt": file_record(VERSION / "system_prompt.md"),
            "input_schema": file_record(VERSION / "input.schema.json"),
            "output_schema": file_record(VERSION / "output.schema.json"),
            "camera_profiles": file_record(VERSION / "camera_profiles.json"),
            "reference_library": file_record(VERSION / "reference_library.json"),
            "normalized_extraction_manifest": file_record(NORMALIZED / "extraction_manifest.json"),
            "input_projection_manifest": file_record(projection_path),
        },
        "authorized_text_case_ids": [case["case_id"] for case in cases],
        "cases": cases,
    }
    manifest_path = HERE / "manifest.json"
    write_json(manifest_path, manifest)
    print(
        json.dumps(
            {
                "manifest": str(manifest_path),
                "manifest_sha256": sha_file(manifest_path),
                "projection_manifest": str(projection_path),
                "projection_manifest_sha256": sha_file(projection_path),
                "cases": len(cases),
                "candidate_count": len(cases) * 20,
                "projection_verified": projection_manifest["verification"]["all_projections_no_text_loss_or_duplication"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
