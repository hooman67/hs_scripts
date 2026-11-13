#!/usr/bin/env python3
"""Assemble unchanged successful banks and revalidate them with a frozen V6 runtime."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

import run_eval


HERE = Path(__file__).resolve().parent


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json_exclusive(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def write_text_exclusive(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(value)
        handle.flush()
        os.fsync(handle.fileno())


def plain_text_block(row: dict[str, Any]) -> str:
    return (
        f"[{row['prompt_key']} | {row['device_display_name']} | "
        f"{row['camera_tag']} | rank {row['bank_rank']} | "
        f"source {row['source_relevance_score']} | "
        f"C-Tech {row['ctech_reference_score']}]\n{row['text']}"
    )


def load_frozen_runtime(snapshot: Path):
    runtime_parent = snapshot / "runtime"
    sys.path.insert(0, str(runtime_parent))
    for name in list(sys.modules):
        if name == "v6" or name.startswith("v6."):
            del sys.modules[name]
    validation = importlib.import_module("v6.validation")
    camera = importlib.import_module("v6.camera")
    return validation, camera


def assemble(revision: str, source_map_path: Path) -> Path:
    snapshot = run_eval.revision_dir(revision)
    manifest = run_eval.verify_snapshot(snapshot)
    destination = snapshot / "exports/final"
    if destination.exists():
        raise FileExistsError(f"composite export already exists: {destination}")

    source_map = load_json(source_map_path)
    if set(source_map) != {
        "version", "purpose", "default_source_revision", "case_overrides"
    }:
        raise ValueError("source map fields are malformed")
    if source_map["version"] != "hp-lifestyle-v6-composite-source-map-v1":
        raise ValueError("source map version is unsupported")
    overrides = source_map["case_overrides"]
    if not isinstance(overrides, dict):
        raise ValueError("case overrides must be an object")
    case_ids = manifest["authorized_text_case_ids"]
    if not set(overrides).issubset(case_ids):
        raise ValueError("source map contains an unknown case")

    validation, camera_module = load_frozen_runtime(snapshot)
    catalog = load_json(snapshot / "runtime/v6/approved_catalog.json")
    registry = load_json(snapshot / "runtime/v6/camera_profiles.json")
    references = load_json(snapshot / "runtime/v6/reference_library.json")
    cases_by_id = {case["case_id"]: case for case in manifest["cases"]}

    all_rows: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []
    bank_audit: dict[str, Any] = {}
    selected_sources: dict[str, str] = {}

    for case_id in case_ids:
        source_revision = overrides.get(case_id, source_map["default_source_revision"])
        source_snapshot = run_eval.revision_dir(source_revision)
        run_eval.verify_snapshot(source_snapshot)
        result_path = source_snapshot / "results" / f"{case_id}.json"
        result = load_json(result_path)
        run_eval._validate_successful_bank(case_id, result)
        journals = run_eval._validate_call_journals(source_snapshot, case_id, result)

        attempt = result["audit"]["attempts"][-1]
        normalized_output = attempt.get("normalized_output")
        request = result["audit"]["source_input"]
        resolved_camera = camera_module.resolve_camera(registry, request["camera_tag"])
        final_validation = validation.validate_output(
            normalized_output, request, catalog, resolved_camera, references
        )
        if not final_validation["passed"]:
            raise ValueError(
                f"selected bank fails frozen final validation: {case_id}: "
                f"{final_validation['errors']}"
            )
        refinalized = validation.finalize_output(
            normalized_output, camera=resolved_camera, catalog=catalog
        )
        if refinalized["prompts"] != result["prompts"]:
            raise ValueError(f"final-code replay changes prompt fields: {case_id}")

        case = cases_by_id[case_id]
        source_input = load_json(snapshot / case["frozen_input_path"])
        if source_input != request:
            raise ValueError(f"source input differs from selected bank: {case_id}")
        selected_sources[case_id] = source_revision
        bank_audit[case_id] = {
            "case_metadata": copy.deepcopy(case),
            "source_input": source_input,
            "source_input_sha256": sha_file(snapshot / case["frozen_input_path"]),
            "selected_source_revision": source_revision,
            "selected_result_path": str(result_path),
            "selected_result_sha256": sha_file(result_path),
            "selected_final_attempt": attempt["number"],
            "selected_normalization_changes": copy.deepcopy(
                attempt.get("normalization_changes", [])
            ),
            "final_runtime_revalidation": copy.deepcopy(final_validation),
            "prompts_byte_identical_after_refinalization": True,
            "debug": copy.deepcopy(result["debug"]),
            "run": run_eval._bank_audit_summary(result),
            "journals": journals,
        }

        for rank, candidate in enumerate(result["prompts"], start=1):
            row = {
                "prompt_key": f"{case_id}::{candidate['id']}",
                "device_id": case["device_id"],
                "device_display_name": case["device_display_name"],
                "device_type": case["device_type"],
                "source_pair": case["source_pair"],
                "camera_tag": case["camera_tag"],
                "source_camera_name": case["source_camera_name"],
                "view_role": case["view_role"],
                "render_gallery_url": case["render_gallery_url"],
                "render_lookup": copy.deepcopy(case["render_lookup"]),
                "bank_rank": rank,
                **copy.deepcopy(candidate),
                "text_sha256": hashlib.sha256(
                    candidate["text"].encode("utf-8")
                ).hexdigest(),
                "bank_debug_ref": case_id,
                "source_revision": source_revision,
            }
            all_rows.append(row)
            if rank <= 6:
                selected_rows.append(copy.deepcopy(row))

    if len(all_rows) != 160 or len(selected_rows) != 96:
        raise ValueError("composite counts are not 160 and 96")
    if len({row["prompt_key"] for row in all_rows}) != 160:
        raise ValueError("composite prompt keys are not unique")
    if len({row["text"] for row in all_rows}) != 160:
        raise ValueError("composite prompt texts are not unique")
    bank_counts = Counter(row["bank_debug_ref"] for row in selected_rows)
    if len(bank_counts) != 16 or set(bank_counts.values()) != {6}:
        raise ValueError("composite does not select six prompts per bank")

    common = {
        "revision": revision,
        "assembly_mode": "unchanged_successful_bank_composite",
        "snapshot_manifest_path": str(snapshot / "snapshot_manifest.json"),
        "snapshot_manifest_sha256": sha_file(snapshot / "snapshot_manifest.json"),
        "source_map_path": str(source_map_path.resolve()),
        "source_map_sha256": sha_file(source_map_path),
        "selected_source_revisions": selected_sources,
        "selection_rule": manifest["scope"]["selection_rule"],
        "device_source_mapping": copy.deepcopy(manifest["device_source_mapping"]),
        "bank_audit": bank_audit,
    }
    all_output = {
        "version": "hp-lifestyle-approved-props-v6-all-four-devices-composite-v1",
        **copy.deepcopy(common),
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16,
                   "candidates_per_bank": 10, "prompts": 160},
        "prompts": all_rows,
    }
    top_output = {
        "version": "hp-lifestyle-approved-props-v6-top6-four-devices-composite-v1",
        **copy.deepcopy(common),
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16,
                   "selected_per_bank": 6, "prompts": 96},
        "prompts": selected_rows,
    }

    export_root = snapshot / "exports"
    export_root.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".final.composite-", dir=export_root))
    try:
        write_json_exclusive(stage / "prompts_all_160.json", all_output)
        write_json_exclusive(stage / "prompts_top6_96.json", top_output)
        write_text_exclusive(
            stage / "prompts_all_160.txt",
            "\n\n".join(plain_text_block(row) for row in all_rows) + "\n",
        )
        write_text_exclusive(
            stage / "prompts_top6_96.txt",
            "\n\n".join(plain_text_block(row) for row in selected_rows) + "\n",
        )
        composite_manifest = {
            "version": "hp-lifestyle-v6-validated-composite-manifest-v1",
            "revision": revision,
            "no_scene_text_edits": True,
            "no_cross_bank_field_repairs": True,
            "all_banks_actual_gpt55_outputs": True,
            "all_banks_pass_frozen_final_runtime": True,
            "selected_sources": selected_sources,
            "assembler_path": str(Path(__file__).resolve()),
            "assembler_sha256": sha_file(Path(__file__)),
        }
        write_json_exclusive(stage / "composite_manifest.json", composite_manifest)
        validation_record = {
            "version": "hp-lifestyle-approved-props-v6-composite-validation-v1",
            "passed": True,
            "checks": {
                "final_runtime_snapshot_integrity_passed": True,
                "all_16_selected_banks_original_status_ok": True,
                "all_16_banks_pass_final_runtime_revalidation": True,
                "all_prompt_fields_byte_identical_after_refinalization": True,
                "all_160_candidates_exported": True,
                "source_rank_top_6_per_bank_exported": True,
                "top_96_prompt_keys_unique": True,
                "source_inputs_debug_and_call_journals_preserved": True,
                "no_scene_text_edits": True,
            },
            "bank_counts": dict(sorted(bank_counts.items())),
            "files": {
                name: {"bytes": (stage / name).stat().st_size,
                       "sha256": sha_file(stage / name)}
                for name in (
                    "prompts_all_160.json", "prompts_all_160.txt",
                    "prompts_top6_96.json", "prompts_top6_96.txt",
                    "composite_manifest.json",
                )
            },
        }
        write_json_exclusive(stage / "validation.json", validation_record)
        stage.rename(destination)
    except Exception:
        import shutil
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--source-map", type=Path, required=True)
    args = parser.parse_args()
    destination = assemble(args.revision, args.source_map.resolve())
    print(json.dumps({"status": "exported", "path": str(destination)}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}), file=sys.stderr)
        raise SystemExit(2)
