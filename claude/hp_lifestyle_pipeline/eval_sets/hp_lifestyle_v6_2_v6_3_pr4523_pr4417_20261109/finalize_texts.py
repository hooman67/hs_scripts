#!/usr/bin/env python3
"""Revalidate only the last actual response per bank; never make provider calls."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("hp_text_eval", HERE / "run_text_eval.py")
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)
SOURCE_REVISION = "v6.3-hp-associations-20261110-r1"
VALIDATION_REVISION = "v6.3-hp-associations-20261110-r2-recognition"


def main():
    source = evaluation.revision_dir(SOURCE_REVISION, HERE)
    original_manifest = evaluation.verify_snapshot(source)
    complete = evaluation.load_json(source / "run_complete.json")
    if complete["case_count"] != 16:
        raise ValueError("the paid sixteen-bank batch is not terminal")
    snapshot = evaluation.revision_dir(VALIDATION_REVISION, HERE)
    if not snapshot.exists():
        evaluation.prepare_revision(VALIDATION_REVISION, evaluation.DEFAULT_CATALOG, eval_root=HERE)
    manifest = evaluation.verify_snapshot(snapshot)
    runtime = snapshot / "runtime/v6_3"
    sys.path.insert(0, str(runtime.parent))
    from v6_3.camera import resolve_camera
    from v6_3.validation import finalize_output, validate_output

    catalog = evaluation.load_json(runtime / "approved_catalog.json")
    references = evaluation.load_json(runtime / "reference_library.json")
    registry = evaluation.load_json(runtime / "camera_profiles.json")
    banks, rows, rejected = {}, [], {}
    for case in original_manifest["cases"]:
        case_id = case["case_id"]
        result_path = source / "results" / f"{case_id}.json"
        result = evaluation.load_json(result_path)
        attempts = result["audit"]["attempts"]
        if not 1 <= len(attempts) <= 2:
            raise ValueError(f"{case_id}: missing bounded actual responses")
        last = attempts[-1]["normalized_output"]
        if not isinstance(last, dict):
            raise ValueError(f"{case_id}: last actual response is not a normalized object")
        raw_input = source / case["frozen_input_path"]
        frozen_input = snapshot / case["frozen_input_path"]
        if raw_input.read_bytes() != frozen_input.read_bytes():
            raise ValueError(f"{case_id}: writer source inputs changed")
        request = evaluation.load_json(raw_input)
        camera = resolve_camera(registry, request["camera_tag"])
        checked = validate_output(last, request, catalog, camera, references)
        evaluation.write_json_exclusive(snapshot / "revalidation" / f"{case_id}.json", {
            "case_id": case_id, "source_result_path": str(result_path),
            "source_result_sha256": evaluation.sha_file(result_path),
            "selected_attempt": len(attempts), "selection": "last actual normalized response only",
            "source_service_status": result["status"], "source_service_error": result.get("error"),
            "selected_normalized_output_sha256": evaluation.canonical_json_hash(last),
            "additional_model_calls": 0, "manual_model_field_edits": False,
            "validation": checked,
        })
        if not checked["passed"]:
            rejected[case_id] = checked["errors"]
            continue
        finalized = finalize_output(last, camera=camera, catalog=catalog)
        journal_audit = evaluation._validate_call_journals(source, case_id, result)
        banks[case_id] = {
            "case_metadata": copy.deepcopy(case), "source_input": request,
            "source_input_path": str(frozen_input), "source_input_sha256": evaluation.sha_file(frozen_input),
            "source_result_path": str(result_path), "source_result_sha256": evaluation.sha_file(result_path),
            "source_service_status": result["status"], "source_service_error": result.get("error"),
            "selected_attempt": len(attempts), "selected_last_actual_response_only": True,
            "selected_normalized_output_sha256": evaluation.canonical_json_hash(last),
            "debug": finalized["debug"], "run": evaluation._bank_audit_summary(result),
            "journals": journal_audit, "revalidation": checked,
            "additional_model_calls": 0, "manual_model_field_edits": False,
        }
        for rank, candidate in enumerate(finalized["prompts"], 1):
            rows.append({
                "prompt_key": f"{case_id}::{candidate['id']}",
                **{field: copy.deepcopy(case[field]) for field in (
                    "device_id", "device_display_name", "device_type", "source_pair", "camera_tag",
                    "source_camera_name", "view_role", "render_gallery_url", "render_lookup",
                )},
                "bank_rank": rank, **copy.deepcopy(candidate),
                "text_sha256": evaluation.sha_bytes(candidate["text"].encode()),
                "bank_debug_ref": case_id,
            })
    evaluation.write_json_exclusive(snapshot / "revalidation_complete.json", {
        "source_revision": SOURCE_REVISION, "validation_revision": VALIDATION_REVISION,
        "source_service_process_successes": complete["process_successes"],
        "source_service_process_failures": complete["process_failures"],
        "validated_banks": len(banks), "rejected_banks": rejected,
        "additional_model_calls": 0, "manual_model_field_edits": False,
    })
    if rejected or len(rows) != 160:
        raise ValueError(f"no complete160 export: {json.dumps(rejected)}")
    document = {
        "version": "hp-lifestyle-v6.3-associations-all-four-devices-v1",
        "revision": VALIDATION_REVISION, "source_revision": SOURCE_REVISION,
        "validation_revision": VALIDATION_REVISION,
        "snapshot_manifest_path": str(snapshot / "snapshot_manifest.json"),
        "snapshot_manifest_sha256": evaluation.sha_file(snapshot / "snapshot_manifest.json"),
        "selection_rule": "all ten source/CTech-ranked prompts in each of sixteen banks; no subset",
        "device_source_mapping": manifest["device_source_mapping"],
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16, "candidates_per_bank": 10, "prompts": 160},
        "bank_audit": banks, "prompts": rows,
        "provenance": {
            "source_snapshot_manifest_path": str(source / "snapshot_manifest.json"),
            "source_snapshot_manifest_sha256": evaluation.sha_file(source / "snapshot_manifest.json"),
            "source_run_complete_sha256": evaluation.sha_file(source / "run_complete.json"),
            "source_service_successes": complete["process_successes"],
            "source_service_failures": complete["process_failures"],
            "recognition_fix": "desk trays/table lamps/desk clocks are accessories, not additional primary-furniture antecedents",
            "no_earlier_attempt_selection": True, "additional_model_calls": 0, "manual_model_field_edits": False,
        },
    }
    export = snapshot / "exports/final"
    evaluation.write_json_exclusive(export / "prompts_all_160.json", document)
    evaluation.write_text_exclusive(export / "prompts_all_160.txt",
                                    "\n\n".join(evaluation._plain_text_block(row) for row in rows) + "\n")
    print(json.dumps({"export": str(export), "prompts": len(rows),
                      "source_service_successes": complete["process_successes"],
                      "source_service_failures": complete["process_failures"], "additional_model_calls": 0}))


if __name__ == "__main__":
    main()
