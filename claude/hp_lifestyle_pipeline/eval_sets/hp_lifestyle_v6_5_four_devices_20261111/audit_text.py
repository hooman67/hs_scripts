#!/usr/bin/env python3
"""Independently replay all native V6.5 responses, validation and source ranking."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

import run_text_eval as study


FAILED_BANK = "magic__printer_FrontRightCloseUp"
REVALIDATION = study.SNAPSHOT / "revalidations/fitted-support-recognition-r2"


def freeze_recognition_fix():
    manifest_path = REVALIDATION / "manifest.json"
    if not manifest_path.exists():
        if REVALIDATION.exists():
            raise ValueError("incomplete recognition freeze; inspect rather than overwrite")
        release = study.load(study.RUNTIME / "assets_manifest.json")
        for name, digest in release["files"].items():
            if study.sha(study.RUNTIME / name) != digest:
                raise ValueError(f"corrected runtime asset changed: {name}")
        original = study.SNAPSHOT / "runtime/v6_5"
        changed = {
            name for name in release["files"]
            if not (original / name).is_file()
            or study.sha(original / name) != study.sha(study.RUNTIME / name)
        }
        if changed != {"surfaces.py", "tests/test_surfaces.py", "build_assets.py"}:
            raise ValueError(f"revalidation exceeds the bounded support recognition fix: {changed}")
        shutil.copytree(study.RUNTIME, REVALIDATION / "runtime/v6_5",
                        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc", "*.pyo"))
        study.write(manifest_path, {
            "version": release["version"], "frozen_at_utc": study.now(),
            "original_snapshot_manifest_sha256": study.sha(study.SNAPSHOT / "snapshot_manifest.json"),
            "original_terminal_sha256": study.sha(study.SNAPSHOT / "run_complete.json"),
            "support_recognition_fix": release["support_recognition_fix"],
            "runtime_files": {
                str(path.relative_to(REVALIDATION)): study.sha(path)
                for path in sorted((REVALIDATION / "runtime").rglob("*")) if path.is_file()
            },
            "additional_model_calls": 0, "original_process_outcomes_preserved": True,
        })
    frozen = study.load(manifest_path)
    if (
        frozen["original_snapshot_manifest_sha256"] != study.sha(study.SNAPSHOT / "snapshot_manifest.json")
        or frozen["original_terminal_sha256"] != study.sha(study.SNAPSHOT / "run_complete.json")
    ):
        raise ValueError("original native evidence changed")
    for name, digest in frozen["runtime_files"].items():
        if study.sha(REVALIDATION / name) != digest:
            raise ValueError(f"recognition revalidation runtime changed: {name}")
    return REVALIDATION / "runtime"


def main(revalidate=False):
    manifest = study.verify()
    snapshot = study.SNAPSHOT
    export = snapshot / "exports/prompts_all_160.json"
    if revalidate and export.exists():
        raise FileExistsError("revalidated export already exists; do not rewrite")
    document = {"prompts": []} if revalidate else study.load(export)
    terminal = study.load(snapshot / "run_complete.json")
    if revalidate:
        if (terminal["successful_banks"], terminal["failed_banks"], terminal["pending_banks"]) != (15, 1, 0):
            raise ValueError("revalidation requires the preserved fifteen-success/one-failure native run")
    elif terminal["successful_banks"] != 16 or terminal["failed_banks"]:
        raise ValueError("native text run is not sixteen successful banks")
    runtime_root = freeze_recognition_fix() if revalidate else snapshot / "runtime"
    sys.path.insert(0, str(runtime_root))
    from v6_5.camera import resolve_camera
    from v6_5.catalog import validate_catalog
    from v6_5.runtime import _effective_model_schema, _repair_instruction
    from v6_5.validation import finalize_output, normalize_invalid_evidence, validate_output
    from v6_5 import validation as validation_module

    original_spec = importlib.util.spec_from_file_location(
        "v65_original_supports", snapshot / "runtime/v6_5/surfaces.py",
    )
    if original_spec is None or original_spec.loader is None:
        raise ValueError("original support extractor is unavailable")
    original_supports = importlib.util.module_from_spec(original_spec)
    sys.modules[original_spec.name] = original_supports
    original_spec.loader.exec_module(original_supports)

    runtime = runtime_root / "v6_5"
    catalog = study.load(runtime / study.CATALOGUE)
    validate_catalog(catalog)
    registry = study.load(runtime / "camera_profiles.json")
    references = study.load(runtime / "reference_library.json")
    guidance = study.load(runtime / "prop_guidance.json")["entries"]
    schema = _effective_model_schema(
        study.load(runtime / "model_output.schema.json"),
        [entry["id"] for entry in catalog["entries"]],
    )
    by_slot = {
        (row["device_id"], row["camera_tag"], row["bank_rank"]): row
        for row in document["prompts"]
    }
    if not revalidate and (len(by_slot) != 160 or len(document["prompts"]) != 160):
        raise ValueError("full export does not contain160 unique slots")
    audits = []
    banks = {}
    semantic_calls = transport_calls = repairs = 0
    for case in manifest["cases"]:
        stem = case["case_id"]
        result_path = snapshot / "results" / (stem + ".json")
        result = study.load(result_path)
        process = study.load(snapshot / "call_journals" / (stem + ".process.json"))
        native_failure = revalidate and stem == FAILED_BANK
        if (
            result["status"] != ("error" if native_failure else "ok")
            or process["returncode"] != (2 if native_failure else 0)
            or process["output_sha256"] != study.sha(result_path)
            or terminal["cases"][stem] != process
        ):
            raise ValueError(f"native result/process provenance differs: {stem}")
        source_path = snapshot / case["frozen_input_path"]
        source = study.load(source_path)
        baseline_input = study.BASELINE / case["frozen_input_path"]
        if (
            study.sha(source_path) != case["frozen_input_sha256"]
            or source_path.read_bytes() != baseline_input.read_bytes()
            or result["audit"]["source_input"] != source
        ):
            raise ValueError(f"input not byte-identical to V6.4: {stem}")
        camera = resolve_camera(registry, source["camera_tag"])
        expected_trusted = {
            "camera": camera, "approved_catalogue": catalog["entries"],
            "reference_library": references, "approved_prop_usage_guidance": guidance,
        }
        attempts = result["audit"]["attempts"]
        if len(attempts) not in {1, 2}:
            raise ValueError("semantic limit violated")
        if result["audit"]["semantic_calls"] != len(attempts):
            raise ValueError("semantic accounting differs from raw attempts")
        for number, attempt in enumerate(attempts, 1):
            journal = snapshot / "results" / (stem + ".json.run")
            request_path = journal / f"attempt_{number}.request.json"
            response_path = journal / f"attempt_{number}.response.json"
            request = study.load(request_path)
            reply = study.load(response_path)
            messages = request["messages"]
            if (
                request["schema"] != schema
                or messages[0] != {"role": "system", "content": (runtime / "system_prompt.md").read_text()}
                or messages[1]["role"] != "system"
                or json.loads(messages[1]["content"]) != expected_trusted
                or messages[2]["role"] != "user"
                or json.loads(messages[2]["content"]) != source
            ):
                raise ValueError(f"actual request differs from frozen configuration: {stem}/{number}")
            if number == 2 and (
                len(messages) != 6
                or messages[3] != {"role": "assistant", "content": attempts[0]["raw_content"] or ""}
                or messages[4] != {"role": "developer", "content": _repair_instruction(camera)}
                or json.loads(messages[5]["content"])["validation_diagnostics_data"] != attempts[0]["errors"]
            ):
                raise ValueError("semantic repair is not the exact complete-bank continuation")
            if number == 1 and len(messages) != 3:
                raise ValueError("unexpected initial conversation context")
            if reply["content"] != attempt["raw_content"] or reply["model"] != attempt["provider"]["model"]:
                raise ValueError("native response and application audit disagree")
            if not (reply["model"] == "gpt-5.5" or reply["model"].startswith("gpt-5.5-")):
                raise ValueError("writer model substitution")
            if (
                reply["settings"]["model"] != "gpt-5.5"
                or reply["settings"]["reasoning_effort"] != "medium"
                or reply["settings"]["max_completion_tokens"] != 16000
                or reply["settings"]["timeout"] != 180
                or reply["refusal"] is not None
            ):
                raise ValueError("writer settings/refusal changed")
            if reply["finish_reason"] == "stop":
                parsed = json.loads(reply["content"])
                if parsed != attempt["parsed_output"]:
                    raise ValueError("native parsed output changed")
                normalized, changes = normalize_invalid_evidence(parsed, source)
                if normalized != attempt["normalized_output"] or changes != attempt["normalization_changes"]:
                    raise ValueError("host evidence normalization does not replay")
            elif number == len(attempts) or reply["finish_reason"] != "length":
                raise ValueError("invalid final or unsupported initial finish")
            transport_calls += reply["transport_attempts"]
            if reply["finish_reason"] == "stop":
                corrected_audit_bank = validation_module.audit_bank
                corrected_infer = validation_module.infer_primary_support
                try:
                    validation_module.audit_bank = original_supports.audit_bank
                    validation_module.infer_primary_support = original_supports.infer_primary_support
                    original_validation = validate_output(normalized, source, catalog, camera, references)
                finally:
                    validation_module.audit_bank = corrected_audit_bank
                    validation_module.infer_primary_support = corrected_infer
                if original_validation["errors"] != attempt["errors"]:
                    raise ValueError(f"original diagnostics do not replay: {stem}/{number}")
        final = attempts[-1]["normalized_output"]
        validation = validate_output(final, source, catalog, camera, references)
        if native_failure:
            errors = attempts[-1]["errors"]
            if len(attempts) != 2 or len(errors) != 4 or {
                (error["code"], error["path"]) for error in errors
            } != {
                (code, f"/prompts/{index}/text") for index in (6, 7)
                for code in ("printer_surface_implausible", "undeclared_known_prop")
            }:
                raise ValueError("native failed bank is not the diagnosed fitted-casework false positive")
        if not validation["passed"] or (attempts[-1]["errors"] and not native_failure):
            raise ValueError(f"native final bank fails independent validation: {stem}")
        replayed = finalize_output(copy.deepcopy(final), camera=camera, catalog=catalog)
        def without_support(rows):
            return [{key: value for key, value in row.items() if key != "primary_support"} for row in rows]

        if not native_failure and without_support(replayed["prompts"]) != without_support(result["prompts"]):
            raise ValueError("application-owned scores/ranking/text do not replay")
        if not revalidate and replayed["prompts"] != result["prompts"]:
            raise ValueError("native primary support metadata does not replay")
        journals = study.helpers()._validate_call_journals(snapshot, stem, result)
        if revalidate:
            banks[stem] = {
                "case_metadata": case, "source_input": source,
                "source_input_path": str(source_path), "source_input_sha256": study.sha(source_path),
                "result_path": str(result_path), "result_sha256": study.sha(result_path),
                "run": study.helpers()._bank_audit_summary(result),
                "native_process_returncode": process["returncode"],
                "offline_revalidation": {
                    "passed": True, "original_native_status": result["status"],
                    "manifest_path": str(REVALIDATION / "manifest.json"),
                    "manifest_sha256": study.sha(REVALIDATION / "manifest.json"),
                    "additional_model_calls": 0,
                },
                "debug": replayed["debug"], "journals": journals,
            }
        for rank, candidate in enumerate(replayed["prompts"], 1):
            if revalidate:
                row = {
                    **{key: copy.deepcopy(case[key]) for key in (
                        "device_id", "device_display_name", "device_type", "source_pair", "camera_tag",
                        "source_camera_name", "view_role", "render_gallery_url", "render_lookup",
                    )},
                    "prompt_key": f"{stem}::{candidate['id']}", "bank_rank": rank,
                    **copy.deepcopy(candidate),
                    "text_sha256": hashlib.sha256(candidate["text"].encode()).hexdigest(),
                    "bank_debug_ref": stem,
                }
                document["prompts"].append(row)
                by_slot[(case["device_id"], case["camera_tag"], rank)] = row
            row = by_slot[(case["device_id"], case["camera_tag"], rank)]
            if any(row[key] != value for key, value in candidate.items()):
                raise ValueError("export changes actual candidate fields")
            if row["text_sha256"] != hashlib.sha256(candidate["text"].encode()).hexdigest():
                raise ValueError("exported scene text hash differs")
            if row["source_pair"] != case["source_pair"] or row["render_lookup"] != case["render_lookup"]:
                raise ValueError("exported source/product mapping changed")
        semantic_calls += len(attempts)
        repairs += len(attempts) == 2
        audits.append({
            "case_id": stem, "input_sha256": study.sha(source_path),
            "result_sha256": study.sha(result_path), "actual_prompts": 10,
            "semantic_calls": len(attempts), "final_validation": "passed",
            "original_native_status": result["status"], "original_returncode": process["returncode"],
            "native_response_equality": "passed", "source_score_and_sort_replay": "passed",
        })
    if len(by_slot) != 160 or len({row["text"] for row in document["prompts"]}) != 160:
        raise ValueError("scene texts are not distinct")
    counts = {}
    old = study.load(study.BASELINE / "exports/prompts_all_160.json")["prompts"]
    old_entries = {
        entry["id"]: entry
        for entry in study.load(study.VERSIONS / "v6_4/approved-v6.3-20261109.catalog.json")["entries"]
    }
    new_entries = {entry["id"]: entry for entry in catalog["entries"]}
    for framing in ("tight", "medium", "wide"):
        metrics = {}
        for version, rows, entries in (("v6_4", old, old_entries),
                                       ("v6_5", document["prompts"], new_entries)):
            selected = [row for row in rows if resolve_camera(registry, row["camera_tag"])["framing"] == framing]
            props = [len(row["prop_ids"]) for row in selected]
            background = [
                sum(entries[prop_id]["role"] == "background_furnishing_or_decor" for prop_id in row["prop_ids"])
                for row in selected
            ]
            metrics[version] = {
                "prompts": len(selected), "mean_declared_ids": sum(props) / len(props),
                "min_declared_ids": min(props), "max_declared_ids": max(props),
                "mean_background_ids": sum(background) / len(background),
            }
        counts[framing] = metrics
    if revalidate:
        document.update({
            "version": "hp-lifestyle-v6.5-four-devices-all160-r2-offline-revalidation",
            "snapshot_manifest_path": str(snapshot / "snapshot_manifest.json"),
            "snapshot_manifest_sha256": study.sha(snapshot / "snapshot_manifest.json"),
            "selection_rule": "all ten source/C-Tech-ranked final native candidates per original input; no scene edits or new calls",
            "counts": {"devices": 4, "views_per_device": 4, "banks": 16, "candidates_per_bank": 10, "prompts": 160},
            "device_source_mapping": manifest["device_source_mapping"], "bank_audit": banks,
            "offline_revalidation_manifest_path": str(REVALIDATION / "manifest.json"),
            "offline_revalidation_manifest_sha256": study.sha(REVALIDATION / "manifest.json"),
            "original_native_successful_banks": 15, "original_native_failed_banks": 1,
            "additional_model_calls": 0,
        })
        study.write(export, document)
        plain_text = "\n\n".join(
            study.helpers()._plain_text_block(row) for row in document["prompts"]
        ) + "\n"
        text_export = snapshot / "exports/prompts_all_160.txt"
        with text_export.open("x", encoding="utf-8") as stream:
            stream.write(plain_text)
        if text_export.read_text() != plain_text:
            raise ValueError("persisted plain-text export differs from audited candidates")
        if study.load(export) != document:
            raise ValueError("persisted export differs from audited native candidates")
    study.write(snapshot / "exports/completion_audit.json", {
        "passed": True, "verified_at_utc": study.now(),
        "export_sha256": study.sha(export), "prompts": 160, "banks": 16,
        "plain_text_export_sha256": study.sha(snapshot / "exports/prompts_all_160.txt"),
        "actual_semantic_calls": semantic_calls, "actual_transport_attempts": transport_calls,
        "full_bank_repairs": repairs, "terminal_bank_resampling": False,
        "native_image_calls": 0, "banks_verified": audits,
        "offline_revalidation": revalidate,
        "original_native_successful_banks": terminal["successful_banks"],
        "original_native_failed_banks": terminal["failed_banks"],
        "additional_model_calls": 0,
        "auditor_sha256": study.sha(__file__),
        "declared_inventory_diagnostics": counts,
        "diagnostics_are_not_image_density_or_quality_measurements": True,
    })
    print(json.dumps({
        "verified_prompts": 160, "semantic_calls": semantic_calls,
        "full_bank_repairs": repairs, "inventory_diagnostics": counts,
    }), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revalidate-supported-casework", action="store_true")
    main(parser.parse_args().revalidate_supported_casework)
