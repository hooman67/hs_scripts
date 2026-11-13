#!/usr/bin/env python3
"""Replay the bounded paid recovery, then revalidate its same final texts offline."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil

import recover_text_r3 as bounded

native = bounded.native
HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE / "revisions/v6.5-astra-training-20261111-r4-revalidation"
RUNTIME_SOURCE = native.VERSIONS / "v6_5_training_r4"


def inspect():
    manifest = bounded.verify()
    terminal = native.load(bounded.SNAPSHOT / "run_complete.json")
    if (
        terminal["successful_banks"], terminal["failed_banks"],
        terminal["additional_semantic_calls"], terminal["accepted_unchanged_banks"],
    ) != (14, 2, 15, 1):
        raise ValueError("actual bounded paid-recovery outcome changed")
    original_terminal = native.load(native.SNAPSHOT / "run_complete.json")
    original = bounded.engine(native.SNAPSHOT / "runtime/v6_5_training", "v6_5_training")
    paid = bounded.engine(bounded.RUNTIME, "v6_5_training_r3")
    corrected = bounded.engine(RUNTIME_SOURCE, "v6_5_training_r4")
    banks, frozen = {}, dict(manifest["frozen_files"])
    extra_calls = native_transport = extra_transport = 0
    for path in [Path(__file__), bounded.SNAPSHOT / "recovery_manifest.json", bounded.SNAPSHOT / "run_complete.json"]:
        frozen[str(path)] = native.sha(path)
    for case in manifest["cases"]:
        stem = case["case_id"]
        previous, source, files = bounded.replay_native(case, original_terminal, original)
        frozen.update(files)
        record = bounded.revalidate(case, previous, source, paid)
        if record != manifest["revalidation"][stem]:
            raise ValueError("original-final r3 revalidation does not replay")
        result_path = bounded.SNAPSHOT / "results" / (stem + ".json")
        result = native.load(result_path)
        if native.sha(result_path) != terminal["result_files"][stem]:
            raise ValueError("actual bounded terminal result changed")
        frozen[str(result_path)] = native.sha(result_path)
        native_transport += sum(attempt["provider"]["transport_attempts"] for attempt in previous["audit"]["attempts"])
        journal = bounded.SNAPSHOT / "journals" / stem
        if record["validation"]["passed"]:
            if journal.exists() or result["extra_semantic_calls"] != 0:
                raise ValueError("unchanged valid bank was redrawn")
            normalized = previous["audit"]["attempts"][-1]["normalized_output"]
            validation, reply, kind = record["validation"], None, "accepted_unchanged_final"
        else:
            request = native.load(journal / "request.json")
            expected_request = {
                "messages": bounded.recovery_messages(paid, source, previous, record["validation"]["errors"]),
                "schema": paid.schema,
            }
            if request != expected_request:
                raise ValueError("actual single repair differs from its frozen r3 configuration")
            launch = native.load(journal / "launch.json")
            if launch["maximum_semantic_invocations"] != 1 or launch["authorization"] != bounded.AUTHORIZATION:
                raise ValueError("single-repair launch authorization changed")
            reply = native.load(journal / "response.json")
            bounded.require_settings(reply)
            replay = bounded.validate_reply(paid, reply, source)
            if replay != native.load(journal / "normalization.json"):
                raise ValueError("actual extra reply normalization/diagnostics do not replay")
            normalized = replay["normalized_output"]
            camera = paid.resolve_camera(paid.registry, source["camera_tag"])
            validation = (
                paid.validation.validate_output(normalized, source, paid.catalog, camera, paid.references)
                if not replay["errors"] else {"passed": False, "errors": replay["errors"], "warnings": []}
            )
            completion = native.load(journal / "completion.json")
            if completion["result_sha256"] != native.sha(result_path) or completion["status"] != result["status"]:
                raise ValueError("actual bounded completion/result disagreement")
            kind = "authorized_single_repair"
            extra_calls += 1
            extra_transport += reply["transport_attempts"]
            if {path.name for path in journal.iterdir()} != {
                "launch.json", "request.json", "response.json", "normalization.json", "completion.json",
            }:
                raise ValueError("unexpected extra request or incomplete repair journal")
            frozen.update({str(path): native.sha(path) for path in journal.iterdir()})
        expected = bounded.recovered_result(case, paid, normalized, validation, kind=kind, reply=reply)
        if result != expected:
            raise ValueError("actual r3 result/prose/rank/diagnostics do not replay: " + stem)
        camera = corrected.resolve_camera(corrected.registry, source["camera_tag"])
        offline = corrected.validation.validate_output(
            normalized, source, corrected.catalog, camera, corrected.references,
        )
        if not offline["passed"]:
            raise ValueError("same final text remains genuinely invalid: " + stem + " " + json.dumps(offline["errors"]))
        final = corrected.validation.finalize_output(
            copy.deepcopy(normalized), camera=camera, catalog=corrected.catalog,
        )
        raw_by_text = {row["text"]: row for row in normalized["prompts"]}
        for candidate in final["prompts"]:
            raw = raw_by_text.get(candidate["text"])
            if raw is None or any(candidate[key] != value for key, value in raw.items()):
                raise ValueError("offline finalization edited actual candidate fields")
        banks[stem] = {
            "case": case, "source": source, "normalized_output": normalized, "final": final,
            "bounded_recovery_status": result["status"], "recovery_kind": kind,
            "extra_semantic_calls": result["extra_semantic_calls"],
            "r3_validation": validation, "r4_validation": offline,
            "actual_bounded_result_path": str(result_path), "actual_bounded_result_sha256": native.sha(result_path),
        }
    if extra_calls != 15 or len(banks) != 16:
        raise ValueError("bounded recovery semantic call limit/count mismatch")
    return manifest, banks, frozen, native_transport + extra_transport, extra_transport


def prepare_export():
    if SNAPSHOT.exists():
        raise FileExistsError("offline successor already exists; preserve it rather than refreeze")
    manifest, banks, frozen, transport, extra_transport = inspect()
    release = native.load(RUNTIME_SOURCE / "assets_manifest.json")
    for name, digest in release["files"].items():
        if native.sha(RUNTIME_SOURCE / name) != digest:
            raise ValueError("unfrozen offline recognition asset: " + name)
    runtime = SNAPSHOT / "runtime/v6_5_training_r4"
    shutil.copytree(RUNTIME_SOURCE, runtime, ignore=shutil.ignore_patterns(
        "__pycache__", ".pytest_cache", "*.pyc", "*.pyo",
    ))
    rows, audit = [], {}
    for stem, bank in banks.items():
        case, source, final = bank["case"], bank["source"], bank["final"]
        source_path = SNAPSHOT / case["frozen_input_path"]
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_bytes((native.SNAPSHOT / case["frozen_input_path"]).read_bytes())
        if native.sha(source_path) != case["frozen_input_sha256"] or native.load(source_path) != source:
            raise ValueError("offline successor source bytes changed")
        result_path = SNAPSHOT / "results" / (stem + ".json")
        native.write(result_path, {
            "status": "ok", "prompts": final["prompts"], "debug": final["debug"],
            "actual_bounded_result_path": bank["actual_bounded_result_path"],
            "actual_bounded_result_sha256": bank["actual_bounded_result_sha256"],
            "actual_bounded_status": bank["bounded_recovery_status"],
            "offline_revalidation": bank["r4_validation"], "additional_model_calls_for_revalidation": 0,
            "original_native_status": "error", "original_returncode": 2,
        })
        audit[stem] = {
            "case_metadata": case, "source_input": source, "source_input_path": str(source_path),
            "source_input_sha256": case["frozen_input_sha256"], "result_path": str(result_path),
            "result_sha256": native.sha(result_path), "debug": final["debug"],
            "run": {
                "status": "ok", "original_native_status": "error", "original_returncode": 2,
                "native_semantic_calls": 2, "extra_semantic_calls": bank["extra_semantic_calls"],
                "semantic_calls": 2 + bank["extra_semantic_calls"], "recovery_kind": bank["recovery_kind"],
                "bounded_recovery_status": bank["bounded_recovery_status"], "final_validation_errors": [],
                "offline_recognition_revalidation": True, "extra_calls_for_revalidation": 0,
            },
            "native_final_revalidation": manifest["revalidation"][stem],
            "bounded_recovery_validation": bank["r3_validation"], "offline_validation": bank["r4_validation"],
            "actual_bounded_result_path": bank["actual_bounded_result_path"],
            "actual_bounded_result_sha256": bank["actual_bounded_result_sha256"],
        }
        for rank, candidate in enumerate(final["prompts"], 1):
            rows.append({
                **{key: copy.deepcopy(case[key]) for key in (
                    "device_id", "device_display_name", "device_type", "source_pair", "camera_tag",
                    "source_camera_name", "view_role", "render_gallery_url", "render_lookup",
                )},
                "prompt_key": f"{stem}::{candidate['id']}", "bank_rank": rank, **copy.deepcopy(candidate),
                "text_sha256": hashlib.sha256(candidate["text"].encode()).hexdigest(), "bank_debug_ref": stem,
            })
    if len(rows) != 160 or len({row["text"] for row in rows}) != 160 or len({row["prompt_key"] for row in rows}) != 160:
        raise ValueError("expected160 distinct unchanged actual scene texts/slots")
    for path in [path for folder in ("runtime", "inputs", "results") for path in (SNAPSHOT / folder).rglob("*")
                 if path.is_file()]:
        frozen[str(path)] = native.sha(path)
    native.write(SNAPSHOT / "revalidation_manifest.json", {
        "version": "hp-v6.5-training-r4-offline-recognition-revalidation",
        "prepared_at_utc": native.now(), "cases": manifest["cases"], "frozen_files": frozen,
        "authorization": bounded.AUTHORIZATION, "maximum_extra_calls_per_original_invalid_bank": 1,
        "original_native_successful_banks": 0, "original_native_failed_banks": 16,
        "actual_bounded_successful_banks": 14, "actual_bounded_failed_banks": 2,
        "accepted_unchanged_native_banks": 1, "extra_semantic_calls": 15,
        "extra_model_calls_for_r4": 0, "scene_fields_edited": False,
    })
    native.write(SNAPSHOT / "run_complete.json", {
        "successful_banks": 16, "failed_banks": 0, "pending_banks": 0,
        "outcome_type": "offline final-response recognition revalidation, not a native trial",
        "original_native_successful_banks": 0, "original_native_failed_banks": 16,
        "actual_bounded_successful_banks": 14, "actual_bounded_failed_banks": 2,
        "additional_model_calls_for_revalidation": 0,
    })
    destination = SNAPSHOT / "exports"
    native.write(destination / "prompts_all_160.json", {
        "version": "hp-lifestyle-v6.5-training-recovered-revalidated-all160-v1",
        "snapshot_manifest_path": str(SNAPSHOT / "revalidation_manifest.json"),
        "snapshot_manifest_sha256": native.sha(SNAPSHOT / "revalidation_manifest.json"),
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16, "candidates_per_bank": 10, "prompts": 160},
        "selection_rule": "all ten source/C-Tech-ranked candidates in the same sixteen original V6.4 input banks",
        "device_source_mapping": manifest["device_source_mapping"], "bank_audit": audit, "prompts": rows,
        "original_native_successful_banks": 0, "original_native_failed_banks": 16,
        "bounded_recovery_successful_banks": 14, "bounded_recovery_failed_banks": 2,
        "accepted_unchanged_banks": 1, "additional_semantic_calls": 15, "extra_model_calls_for_r4": 0,
    })
    native.write(destination / "prompts_all_160.txt",
                 "\n\n".join(native.helpers()._plain_text_block(row) for row in rows) + "\n")
    native.write(destination / "completion_audit.json", {
        "passed": True, "verified_at_utc": native.now(), "prompts": 160, "banks": 16,
        "export_sha256": native.sha(destination / "prompts_all_160.json"),
        "plain_text_export_sha256": native.sha(destination / "prompts_all_160.txt"),
        "actual_semantic_calls": 47, "actual_transport_attempts": transport,
        "full_bank_repairs": 31, "original_native_successful_banks": 0, "original_native_failed_banks": 16,
        "bounded_recovery_successful_banks": 14, "bounded_recovery_failed_banks": 2,
        "accepted_unchanged_banks": 1, "extra_replies_offline_revalidated": 2,
        "additional_semantic_calls": 15, "additional_transport_attempts": extra_transport,
        "offline_revalidation": True, "explicit_additional_repair_authorization": bounded.AUTHORIZATION,
        "additional_model_calls_for_audit": 0, "native_image_calls": 0,
        "all_actual_requests_replies_normalizations_diagnostics_replayed": True,
        "scene_text_and_host_score_rank_support_replay": True,
        "frozen_manifest_sha256": native.sha(SNAPSHOT / "revalidation_manifest.json"),
        "auditor_sha256": native.sha(__file__),
    })
    print(json.dumps({"verified_prompts": 160, "actual_writer_semantic_calls": 47,
                      "new_calls_for_offline_revalidation": 0}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("inspect", "prepare-export"))
    args = parser.parse_args()
    if args.command == "inspect":
        _, banks, _, _, _ = inspect()
        print(json.dumps({"unchanged_final_banks_valid": len(banks), "new_model_calls": 0}))
    else:
        prepare_export()
