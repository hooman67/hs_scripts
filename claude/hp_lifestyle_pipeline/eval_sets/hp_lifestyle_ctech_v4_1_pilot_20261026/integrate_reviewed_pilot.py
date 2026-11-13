#!/usr/bin/env python3
"""Deterministically integrate reviewed V4.1 repair outputs and explicit editorial patches."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VERSION = ROOT / "research/source_messaging_v1_to_v6/versions/v4.1"
SCRIPTS = VERSION / "scripts"
REPAIR_ROOT = HERE / "repair_pass_01"
REVIEWED_ROOT = HERE / "reviewed_outputs"
PROSE_PATCH_PATH = HERE / "editorial_prose_patch.json"
METADATA_PATCH_PATH = REPAIR_ROOT / "editorial_metadata_patch.json"
QUEUE_PATH = HERE / "repair_review_queue.json"
REPAIR_ACCOUNTING_PATH = REPAIR_ROOT / "accounting.json"
MANIFEST_PATH = HERE / "manifest.json"
ACCEPTED_PATH = HERE / "accepted_prompt_cases.json"
REVIEWED_CASES_PATH = HERE / "reviewed_prompt_cases.json"
ARCHIVE_ROOT = HERE / "first_draw_evaluation"
STATUS = "root_reviewed_after_bounded_model_correction_and_editorial_edits"

sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(HERE))
from camera_profile_resolver import load_registry  # noqa: E402
from finalize_output import finalize_output, semantic_sha256  # noqa: E402
from validate_output import validate_output  # noqa: E402


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode()


def write_bytes_exclusive(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def write_json_exclusive(path: Path, value: Any) -> None:
    write_bytes_exclusive(path, json.dumps(value, ensure_ascii=False, indent=2).encode() + b"\n")


def replace_json(path: Path, value: Any) -> None:
    data = json.dumps(value, ensure_ascii=False, indent=2).encode() + b"\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def get_field(candidate: dict[str, Any], field: str) -> Any:
    value: Any = candidate
    for part in field.split("."):
        value = value[part]
    return value


def set_field(candidate: dict[str, Any], field: str, value: Any) -> None:
    target: Any = candidate
    parts = field.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = copy.deepcopy(value)


def load_patch_rows() -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    prose_doc = json.loads(PROSE_PATCH_PATH.read_text())
    metadata_doc = json.loads(METADATA_PATCH_PATH.read_text())
    rows = []
    for source, items in (("root_editorial_prose_patch", prose_doc["patches"]),
                          ("reference_matrix_metadata_patch", metadata_doc["entries"])):
        for item in items:
            rows.append({"patch_source": source, **copy.deepcopy(item)})
    seen: list[tuple[str, str, str, str]] = []
    for row in rows:
        current = (row["case_id"], row["candidate_id"], row["field"], row["patch_source"])
        for prior in seen:
            same_candidate = current[:2] == prior[:2]
            overlap = (current[2] == prior[2]
                       or current[2].startswith(prior[2] + ".")
                       or prior[2].startswith(current[2] + "."))
            if same_candidate and overlap:
                raise RuntimeError(f"conflicting editorial patch paths: {prior} vs {current}")
        seen.append(current)
    return rows, prose_doc, metadata_doc


def main() -> None:
    if REVIEWED_ROOT.exists() or REVIEWED_CASES_PATH.exists() or ARCHIVE_ROOT.exists():
        raise SystemExit("refusing to reuse reviewed/archive output paths")
    manifest = json.loads(MANIFEST_PATH.read_text())
    queue = json.loads(QUEUE_PATH.read_text())
    repair_accounting = json.loads(REPAIR_ACCOUNTING_PATH.read_text())
    repair_by_case = {row["case_id"]: row for row in repair_accounting["cases"]}
    schema_path = VERSION / "output.schema.json"
    registry_path = VERSION / "camera_profiles.json"
    schema = json.loads(schema_path.read_text())
    registry = load_registry(registry_path)
    patch_rows, prose_doc, metadata_doc = load_patch_rows()
    metadata_sources = {row["case_id"]: row for row in metadata_doc["normalized_sources"]}
    case_patches: dict[str, list[dict[str, Any]]] = {
        case_id: [] for case_id in manifest["authorized_text_case_ids"]
    }
    for row in patch_rows:
        if row["case_id"] not in case_patches:
            raise RuntimeError(f"patch targets unauthorized case: {row['case_id']}")
        case_patches[row["case_id"]].append(row)

    built: dict[str, dict[str, Any]] = {}
    all_scene_edits = set()
    for case in manifest["cases"]:
        case_id = case["case_id"]
        repair_case_dir = REPAIR_ROOT / case_id
        base_path = repair_case_dir / "normalized_output.json"
        source_claim = metadata_sources[case_id]
        if Path(source_claim["path"]) != base_path or source_claim["sha256"] != file_sha(base_path):
            raise RuntimeError(f"metadata patch source mismatch: {case_id}")
        base = json.loads(base_path.read_text())
        patched = copy.deepcopy(base)
        candidates = {candidate["id"]: candidate for candidate in patched["prompts"]}
        applied = []
        for row in case_patches[case_id]:
            candidate_id = row["candidate_id"]
            if candidate_id not in candidates:
                raise RuntimeError(f"unknown patch candidate: {case_id}/{candidate_id}")
            actual = get_field(candidates[candidate_id], row["field"])
            if actual != row["before"]:
                raise RuntimeError(
                    f"editorial before conflict: {case_id}/{candidate_id}/{row['field']}\n"
                    f"expected={row['before']!r}\nactual={actual!r}")
            set_field(candidates[candidate_id], row["field"], row["after"])
            applied.append(copy.deepcopy(row))
            if row["patch_source"] == "root_editorial_prose_patch" and row["field"] == "text":
                all_scene_edits.add((case_id, candidate_id))

        first_draw_record = Path(queue["cases"][case_id]["base_raw_record_path"])
        if file_sha(first_draw_record) != queue["cases"][case_id]["base_raw_sha256"]:
            raise RuntimeError(f"first-draw raw record changed: {case_id}")
        first_draw = json.loads(first_draw_record.read_text())
        raw_input = json.loads(first_draw["raw_input_json"])
        normalized, normalization_log = finalize_output(
            patched, raw_input=raw_input, registry=registry)
        validation = validate_output(normalized, raw_input, schema, registry)
        if not validation["passed"]:
            raise RuntimeError(f"reviewed validation failed: {case_id}: {validation['errors']}")

        repair_normalization_log_path = repair_case_dir / "normalization_log.json"
        repair_normalization_log = json.loads(repair_normalization_log_path.read_text())
        repair_id_inverse = {
            row["normalized_id"]: row["original_id"]
            for row in repair_normalization_log["id_map"]
        }
        proposed_path = repair_case_dir / "proposed_output.json"
        proposed = json.loads(proposed_path.read_text())
        proposed_by_id = {candidate["id"]: candidate for candidate in proposed["prompts"]}
        reviewed_to_old = {
            row["normalized_id"]: row["original_id"]
            for row in normalization_log["id_map"]
        }
        patches_by_old: dict[str, list[dict[str, Any]]] = {}
        for row in applied:
            patches_by_old.setdefault(row["candidate_id"], []).append(row)
        base_by_id = {candidate["id"]: candidate for candidate in base["prompts"]}
        candidate_maps = []
        for reviewed_candidate in normalized["prompts"]:
            reviewed_id = reviewed_candidate["id"]
            old_id = reviewed_to_old[reviewed_id]
            raw_correction_id = repair_id_inverse[old_id]
            raw_correction_candidate = proposed_by_id[raw_correction_id]
            edits = patches_by_old.get(old_id, [])
            candidate_maps.append({
                "repair_normalized_candidate_id": old_id,
                "reviewed_candidate_id": reviewed_id,
                "raw_correction_candidate_id": raw_correction_id,
                "raw_correction_text": raw_correction_candidate["text"],
                "repair_normalized_text": base_by_id[old_id]["text"],
                "reviewed_text": reviewed_candidate["text"],
                "editorially_scene_edited": any(
                    row["patch_source"] == "root_editorial_prose_patch" and row["field"] == "text"
                    for row in edits),
                "editorial_edits": edits,
            })

        correction = repair_by_case[case_id]["correction"]
        provenance_map = {
            "version": "v4.1-reviewed-output-provenance-map-v1",
            "case_id": case_id,
            "status": STATUS,
            "sources": {
                "first_draw_raw_record_path": str(first_draw_record),
                "first_draw_raw_record_sha256": file_sha(first_draw_record),
                "correction_provider_response_path": correction["provider_response_path"],
                "correction_provider_response_sha256": correction["provider_response_sha256"],
                "correction_proposed_output_path": str(proposed_path),
                "correction_proposed_output_sha256": file_sha(proposed_path),
                "correction_repair_normalized_path": str(base_path),
                "correction_repair_normalized_sha256": file_sha(base_path),
                "correction_normalization_log_path": str(repair_normalization_log_path),
                "correction_normalization_log_sha256": file_sha(repair_normalization_log_path),
                "prose_patch_path": str(PROSE_PATCH_PATH),
                "prose_patch_sha256": file_sha(PROSE_PATCH_PATH),
                "metadata_patch_path": str(METADATA_PATCH_PATH),
                "metadata_patch_sha256": file_sha(METADATA_PATCH_PATH),
            },
            "patch_count": len(applied),
            "editorially_scene_edited_count": sum(
                row["editorially_scene_edited"] for row in candidate_maps),
            "candidate_id_map": candidate_maps,
        }
        reviewed_case_dir = REVIEWED_ROOT / case_id
        validation_doc = {
            "version": "v4.1-reviewed-output-validation-v1",
            "case_id": case_id,
            "status": STATUS,
            "normalized_output_semantic_sha256": semantic_sha256(normalized),
            "validation": validation,
        }
        built[case_id] = {
            "case": case,
            "base": base,
            "normalized": normalized,
            "normalization_log": normalization_log,
            "validation_doc": validation_doc,
            "provenance_map": provenance_map,
            "reviewed_case_dir": reviewed_case_dir,
            "patched_semantic_sha256": semantic_sha256(patched),
        }

    if len(all_scene_edits) != prose_doc["scene_changed_candidates"] or len(all_scene_edits) != 8:
        raise RuntimeError(f"expected 8 editorial scene edits, found {len(all_scene_edits)}")

    cases_doc = {}
    for case_id in manifest["authorized_text_case_ids"]:
        item = built[case_id]
        case = item["case"]
        normalized = item["normalized"]
        provenance_map = item["provenance_map"]
        provenance_by_reviewed = {
            row["reviewed_candidate_id"]: row for row in provenance_map["candidate_id_map"]
        }
        candidates = []
        for rank, candidate in enumerate(normalized["prompts"], 1):
            candidate_provenance = provenance_by_reviewed[candidate["id"]]
            candidates.append({
                "candidate_key": f"{case_id}::{candidate['id']}",
                "rank": rank,
                "rank_bin": "1-10" if rank <= 10 else "11-20" if rank <= 20 else "21-30",
                "text_sha256": text_sha(candidate["text"]),
                **candidate,
                "candidate_provenance": candidate_provenance,
            })
        reviewed_case_dir = item["reviewed_case_dir"]
        sources = provenance_map["sources"]
        cases_doc[case_id] = {
            "case_id": case_id,
            "group_id": case["group_id"],
            "source_id": case["source_id"],
            "device_type": case["device_type"],
            "camera_tag": case["camera_tag"],
            "view_role": case["view_role"],
            "input_path": case["input_path"],
            "input_sha256": case["input_sha256"],
            "record_path": sources["first_draw_raw_record_path"],
            "record_sha256": sources["first_draw_raw_record_sha256"],
            "correction_provider_response_path": sources["correction_provider_response_path"],
            "correction_provider_response_sha256": sources["correction_provider_response_sha256"],
            "correction_proposed_output_path": sources["correction_proposed_output_path"],
            "correction_proposed_output_sha256": sources["correction_proposed_output_sha256"],
            "repair_normalized_output_path": sources["correction_repair_normalized_path"],
            "repair_normalized_output_sha256": sources["correction_repair_normalized_sha256"],
            "normalized_output_path": str(reviewed_case_dir / "normalized_output.json"),
            "normalization_log_path": str(reviewed_case_dir / "normalization_log.json"),
            "validation_audit_path": str(reviewed_case_dir / "validation.json"),
            "provenance_map_path": str(reviewed_case_dir / "provenance_map.json"),
            "status": STATUS,
            "human_review_status": STATUS,
            "launchable": False,
            "editorially_scene_edited_count": provenance_map["editorially_scene_edited_count"],
            "editorial_patch_count": provenance_map["patch_count"],
            "candidates": candidates,
            "debug": normalized["debug"],
        }

    reviewed_doc = {
        "version": "v4.1-pilot-reviewed-prompt-cases-v1",
        "status": STATUS,
        "manifest_path": str(MANIFEST_PATH),
        "manifest_sha256": file_sha(MANIFEST_PATH),
        "selection_status": "root_reviewed_all_120_no_image_authorization",
        "review_disclosure": (
            "All 120 candidates derive from one bounded GPT-5.5 correction response per bank. "
            "Eight scene texts were subsequently edited by the root reviewer; this corpus is not "
            "an unedited raw-model-success sample. Explicit metadata and related audit fields were "
            "also corrected through hash-pinned patch files."
        ),
        "provenance": {
            "repair_accounting_path": str(REPAIR_ACCOUNTING_PATH),
            "repair_accounting_sha256": file_sha(REPAIR_ACCOUNTING_PATH),
            "prose_patch_path": str(PROSE_PATCH_PATH),
            "prose_patch_sha256": file_sha(PROSE_PATCH_PATH),
            "metadata_patch_path": str(METADATA_PATCH_PATH),
            "metadata_patch_sha256": file_sha(METADATA_PATCH_PATH),
            "integrator_path": str(Path(__file__).resolve()),
            "integrator_sha256": file_sha(Path(__file__).resolve()),
            "system_prompt": manifest["provenance"]["system_prompt"],
            "output_schema": manifest["provenance"]["output_schema"],
        },
        "counts": {
            "manifest_cases": 4,
            "accepted_cases": 4,
            "status_counts": {STATUS: 4},
            "candidates": 120,
            "editorially_scene_edited_candidates": 8,
            "unedited_scene_candidates": 112,
            "editorial_patch_entries": len(patch_rows),
        },
        "cases": cases_doc,
    }

    # No output mutation occurs before all four replayed banks validate.
    archived_bytes = ACCEPTED_PATH.read_bytes()
    archive_path = ARCHIVE_ROOT / "accepted_prompt_cases.json"
    archive_manifest = {
        "version": "v4.1-first-draw-evaluation-archive-v1",
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(ACCEPTED_PATH),
        "archived_path": str(archive_path),
        "sha256": hashlib.sha256(archived_bytes).hexdigest(),
        "reason": "Preserve the zero-accepted first-draw evaluation map before reviewed compatibility replacement.",
    }
    write_bytes_exclusive(archive_path, archived_bytes)
    write_json_exclusive(ARCHIVE_ROOT / "archive_manifest.json", archive_manifest)
    for case_id in manifest["authorized_text_case_ids"]:
        item = built[case_id]
        case_dir = item["reviewed_case_dir"]
        write_json_exclusive(case_dir / "normalized_output.json", item["normalized"])
        write_json_exclusive(case_dir / "normalization_log.json", item["normalization_log"])
        write_json_exclusive(case_dir / "validation.json", item["validation_doc"])
        write_json_exclusive(case_dir / "provenance_map.json", item["provenance_map"])
    write_json_exclusive(REVIEWED_CASES_PATH, reviewed_doc)
    replace_json(ACCEPTED_PATH, reviewed_doc)
    print(json.dumps({
        "status": STATUS,
        "reviewed_prompt_cases_path": str(REVIEWED_CASES_PATH),
        "reviewed_prompt_cases_sha256": file_sha(REVIEWED_CASES_PATH),
        "accepted_prompt_cases_path": str(ACCEPTED_PATH),
        "accepted_prompt_cases_sha256": file_sha(ACCEPTED_PATH),
        "archived_first_draw_path": str(archive_path),
        "archived_first_draw_sha256": file_sha(archive_path),
        "validator_passed_cases": 4,
        "candidates": 120,
        "editorially_scene_edited_candidates": 8,
        "editorial_patch_entries": len(patch_rows),
    }, indent=2))


if __name__ == "__main__":
    main()
