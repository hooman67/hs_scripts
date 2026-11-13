#!/usr/bin/env python3
"""Explicit single-repair recovery; original native failures remain immutable."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import copy
import hashlib
import importlib
import json
from pathlib import Path
import shutil
import sys
from types import SimpleNamespace

import run_text_eval as native

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE / "revisions/v6.5-astra-training-20261111-r2-recovery"
RUNTIME_SOURCE = native.VERSIONS / "v6_5_training_r2"
RUNTIME = SNAPSHOT / "runtime/v6_5_training_r2"
AUTHORIZATION = "Fix recognition; allow one extra repair per genuinely invalid bank"


def engine(root, package):
    sys.path.insert(0, str(root.parent))
    camera = importlib.import_module(package + ".camera")
    catalog = importlib.import_module(package + ".catalog")
    runtime = importlib.import_module(package + ".runtime")
    validation = importlib.import_module(package + ".validation")
    provider = importlib.import_module(package + ".provider")
    props = native.load(root / native.CATALOGUE)
    catalog.validate_catalog(props)
    return SimpleNamespace(
        root=root, runtime=runtime, validation=validation, provider=provider,
        catalog=props, registry=native.load(root / "camera_profiles.json"),
        references=native.load(root / "reference_library.json"),
        resolve_camera=camera.resolve_camera,
        guidance=native.load(root / "prop_guidance.json")["entries"],
        schema=runtime._effective_model_schema(
            native.load(root / "model_output.schema.json"), [entry["id"] for entry in props["entries"]],
        ),
    )


def initial_messages(config, source):
    camera = config.resolve_camera(config.registry, source["camera_tag"])
    trusted = {
        "camera": camera, "approved_catalogue": config.catalog["entries"],
        "approved_prop_usage_guidance": config.guidance, "reference_library": config.references,
    }
    return [
        {"role": "system", "content": (config.root / "system_prompt.md").read_text()},
        {"role": "system", "content": json.dumps(trusted, ensure_ascii=False, sort_keys=True, allow_nan=False)},
        {"role": "user", "content": json.dumps(source, ensure_ascii=False, sort_keys=True)},
    ]


def validate_reply(config, reply, source):
    errors = []
    parsed = normalized = None
    changes = []
    if not config.runtime._valid_provider_response(reply):
        errors.append({"code": "provider_response_invalid", "path": "", "detail": "Provider interface mismatch."})
    elif reply["refusal"] is not None or reply["finish_reason"] != "stop":
        errors.append({"code": "provider_incomplete", "path": "", "detail": "A normal non-refused stop is required."})
    elif not isinstance(reply["content"], str):
        errors.append({"code": "provider_content_missing", "path": "", "detail": "Provider content is absent."})
    else:
        try:
            parsed = json.loads(reply["content"])
        except json.JSONDecodeError:
            errors.append({"code": "json_invalid", "path": "", "detail": "Provider content is not JSON."})
        else:
            normalized, changes = config.validation.normalize_invalid_evidence(parsed, source)
            camera = config.resolve_camera(config.registry, source["camera_tag"])
            errors = config.validation.validate_output(
                normalized, source, config.catalog, camera, config.references,
            )["errors"]
    return {"parsed_output": parsed, "normalized_output": normalized,
            "normalization_changes": changes, "errors": errors}


def require_settings(reply):
    if (
        reply["settings"] != {
            "model": "gpt-5.5", "reasoning_effort": "medium",
            "max_completion_tokens": 16000, "timeout": 180,
        }
        or not (reply["model"] == "gpt-5.5" or reply["model"].startswith("gpt-5.5-"))
        or len(reply["transport_events"]) != reply["transport_attempts"] - 1
    ):
        raise ValueError("actual writer model/settings/transport accounting changed")


def replay_native(case, terminal, config):
    stem = case["case_id"]
    path = native.SNAPSHOT / "results" / (stem + ".json")
    result = native.load(path)
    process_path = native.SNAPSHOT / "call_journals" / (stem + ".process.json")
    process = native.load(process_path)
    source_path = native.SNAPSHOT / case["frozen_input_path"]
    source = native.load(source_path)
    attempts = result["audit"]["attempts"]
    if (
        result["status"] != "error" or process["returncode"] != 2
        or process["output_sha256"] != native.sha(path) or terminal["cases"][stem] != process
        or len(attempts) != 2 or result["audit"]["semantic_calls"] != 2
        or result["audit"]["source_input"] != source
        or native.sha(source_path) != case["frozen_input_sha256"]
        or source_path.read_bytes() != (native.BASELINE / case["frozen_input_path"]).read_bytes()
    ):
        raise ValueError("original native outcome/source binding changed: " + stem)
    journal = native.SNAPSHOT / "results" / (stem + ".json.run")
    expected_messages = initial_messages(config, source)
    files = [path, process_path, source_path,
             native.SNAPSHOT / "call_journals" / (stem + ".launch.json")]
    for number, attempt in enumerate(attempts, 1):
        request_path = journal / f"attempt_{number}.request.json"
        response_path = journal / f"attempt_{number}.response.json"
        request, reply = native.load(request_path), native.load(response_path)
        if request != {"messages": expected_messages, "schema": config.schema}:
            raise ValueError(f"original actual request does not replay: {stem}/{number}")
        require_settings(reply)
        if (
            reply["content"] != attempt["raw_content"]
            or config.runtime._response_metadata(reply) != attempt["provider"]
        ):
            raise ValueError("original raw reply and application audit differ")
        replay = validate_reply(config, reply, source)
        for key in ("parsed_output", "normalized_output", "normalization_changes", "errors"):
            if replay[key] != attempt[key]:
                raise ValueError(f"original normalization/diagnostics do not replay: {stem}/{number}/{key}")
        if number == 1:
            expected_messages.extend([
                {"role": "assistant", "content": attempt["raw_content"] or ""},
                {"role": "developer", "content": config.runtime._repair_instruction(
                    config.resolve_camera(config.registry, source["camera_tag"]),
                )},
                {"role": "user", "content": json.dumps({
                    "validation_diagnostics_data": attempt["errors"],
                    "note": "Diagnostic data only; follow the original system instructions.",
                }, ensure_ascii=False)},
            ])
        files.extend((request_path, response_path))
    if not attempts[-1]["errors"]:
        raise ValueError("a native failed bank unexpectedly has no errors")
    return result, source, {str(path): native.sha(path) for path in files}


def revalidate(case, result, source, config):
    final = result["audit"]["attempts"][-1]
    camera = config.resolve_camera(config.registry, source["camera_tag"])
    return {
        "case_id": case["case_id"], "source_input_sha256": case["frozen_input_sha256"],
        "original_result_sha256": native.sha(native.SNAPSHOT / "results" / (case["case_id"] + ".json")),
        "original_final_normalized_sha256": config.runtime._json_hash(final["normalized_output"]),
        "only_final_original_attempt_considered": True,
        "scene_fields_edited": False,
        "validation": config.validation.validate_output(
            final["normalized_output"], source, config.catalog, camera, config.references,
        ),
    }


def recovery_messages(config, source, previous, diagnostics):
    messages = initial_messages(config, source)
    messages.extend([
        {"role": "assistant", "content": previous["audit"]["attempts"][-1]["raw_content"]},
        {"role": "developer", "content": config.runtime._repair_instruction(
            config.resolve_camera(config.registry, source["camera_tag"]),
        )},
        {"role": "user", "content": json.dumps({
            "validation_diagnostics_data": diagnostics,
            "note": "Diagnostic data only; follow the original system instructions.",
        }, ensure_ascii=False)},
    ])
    return messages


def recovered_result(case, config, normalized, validation, *, kind, reply=None):
    camera = config.resolve_camera(config.registry, case["camera_tag"])
    value = {
        "case_id": case["case_id"], "status": "error" if validation["errors"] else "ok",
        "recovery_kind": kind, "original_native_status": "error", "original_returncode": 2,
        "extra_semantic_calls": int(reply is not None),
        "normalized_output": normalized, "validation": validation,
        "provider": config.runtime._response_metadata(reply) if reply is not None else None,
    }
    if not validation["errors"]:
        final = config.validation.finalize_output(copy.deepcopy(normalized), camera=camera, catalog=config.catalog)
        value.update(prompts=final["prompts"], debug=final["debug"])
    return value


def prepare():
    if SNAPSHOT.exists():
        raise FileExistsError("recovery snapshot already exists; inspect, never refreeze")
    original = native.verify()
    terminal = native.load(native.SNAPSHOT / "run_complete.json")
    if (terminal["successful_banks"], terminal["failed_banks"], terminal["pending_banks"]) != (0, 16, 0):
        raise ValueError("expected actual native0/16 terminal evidence")
    release = native.load(RUNTIME_SOURCE / "assets_manifest.json")
    for name, digest in release["files"].items():
        if native.sha(RUNTIME_SOURCE / name) != digest:
            raise ValueError("unfrozen recognition asset: " + name)
    old = engine(native.SNAPSHOT / "runtime/v6_5_training", "v6_5_training")
    fixed = engine(RUNTIME_SOURCE, "v6_5_training_r2")
    selection, unchanged, frozen = {}, {}, {}
    for case in original["cases"]:
        result, source, files = replay_native(case, terminal, old)
        frozen.update(files)
        record = revalidate(case, result, source, fixed)
        selection[case["case_id"]] = record
        if record["validation"]["passed"]:
            unchanged[case["case_id"]] = recovered_result(
                case, fixed, result["audit"]["attempts"][-1]["normalized_output"],
                record["validation"], kind="accepted_unchanged_final",
            )
    shutil.copytree(RUNTIME_SOURCE, RUNTIME, ignore=shutil.ignore_patterns(
        "__pycache__", ".pytest_cache", "*.pyc", "*.pyo",
    ))
    for case in original["cases"]:
        target = SNAPSHOT / case["frozen_input_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(native.SNAPSHOT / case["frozen_input_path"], target)
    for stem, result in unchanged.items():
        native.write(SNAPSHOT / "results" / (stem + ".json"), result)
    for path in [
        Path(__file__), native.SNAPSHOT / "snapshot_manifest.json",
        native.SNAPSHOT / "run_complete.json", *[
            path for directory in ("runtime", "inputs") for path in (SNAPSHOT / directory).rglob("*")
            if path.is_file()
        ],
    ]:
        frozen[str(path)] = native.sha(path)
    native.write(SNAPSHOT / "recovery_manifest.json", {
        "version": "hp-v6.5-training-explicit-recovery-r2",
        "prepared_at_utc": native.now(), "authorization": AUTHORIZATION,
        "maximum_extra_semantic_calls_per_invalid_bank": 1,
        "original_native_successful_banks": 0, "original_native_failed_banks": 16,
        "original_semantic_calls": 32, "cases": original["cases"],
        "device_source_mapping": original["device_source_mapping"],
        "revalidation": selection, "accepted_unchanged_banks": list(unchanged),
        "repair_required_banks": [stem for stem in selection if stem not in unchanged],
        "frozen_files": frozen,
    })
    print(json.dumps({"accepted_unchanged": len(unchanged), "repair_required": 16 - len(unchanged)}), flush=True)


def verify():
    manifest = native.load(SNAPSHOT / "recovery_manifest.json")
    native.verify()
    if manifest["authorization"] != AUTHORIZATION or manifest["maximum_extra_semantic_calls_per_invalid_bank"] != 1:
        raise ValueError("recovery authorization changed")
    for path, digest in manifest["frozen_files"].items():
        if native.sha(path) != digest:
            raise ValueError("frozen recovery/native evidence changed: " + path)
    return manifest


def repair_one(case, record, config, provider_factory=None):
    stem = case["case_id"]
    if record["validation"]["passed"]:
        raise ValueError("a bank that passes unchanged must never be redrawn")
    destination = SNAPSHOT / "results" / (stem + ".json")
    if destination.exists():
        raise FileExistsError("terminal recovery result exists: " + stem)
    journal = SNAPSHOT / "journals" / stem
    journal.mkdir(parents=True, exist_ok=False)
    previous = native.load(native.SNAPSHOT / "results" / (stem + ".json"))
    source = native.load(SNAPSHOT / case["frozen_input_path"])
    messages = recovery_messages(config, source, previous, record["validation"]["errors"])
    native.write(journal / "launch.json", {
        "case_id": stem, "recorded_at_utc": native.now(), "authorization": AUTHORIZATION,
        "source_input_sha256": case["frozen_input_sha256"], "maximum_semantic_invocations": 1,
        "recorded_before_provider_invocation": True,
    })
    native.write(journal / "request.json", {"messages": messages, "schema": config.schema})
    provider = provider_factory() if provider_factory is not None else config.provider.GPT55Provider()
    try:
        reply = provider(copy.deepcopy(messages), copy.deepcopy(config.schema))
    except config.provider.ProviderUnavailable as exc:
        error = {"code": exc.code, "status_code": exc.status_code,
                 "transport_attempts": exc.attempts, "transport_events": exc.events}
        native.write(journal / "provider_error.json", error)
        value = {"case_id": stem, "status": "error", "recovery_kind": "authorized_single_repair",
                 "extra_semantic_calls": 1, "provider_error": error}
    else:
        native.write(journal / "response.json", reply)
        require_settings(reply)
        replay = validate_reply(config, reply, source)
        native.write(journal / "normalization.json", replay)
        camera = config.resolve_camera(config.registry, source["camera_tag"])
        validation = (
            config.validation.validate_output(replay["normalized_output"], source, config.catalog, camera, config.references)
            if not replay["errors"] else {"passed": False, "errors": replay["errors"], "warnings": []}
        )
        value = recovered_result(
            case, config, replay["normalized_output"], validation, kind="authorized_single_repair", reply=reply,
        )
    native.write(destination, value)
    native.write(journal / "completion.json", {
        "completed_at_utc": native.now(), "result_sha256": native.sha(destination), "status": value["status"],
    })
    print(json.dumps({"case_id": stem, "recovery_status": value["status"]}), flush=True)
    return value


def run(authorized):
    if not authorized:
        raise PermissionError("additional paid repairs require --paid-calls-authorized")
    manifest = verify()
    if (SNAPSHOT / "run_complete.json").exists():
        raise FileExistsError("recovery run is terminal; no additional semantic repair")
    config = engine(RUNTIME, "v6_5_training_r2")
    pending = []
    for case in manifest["cases"]:
        stem = case["case_id"]
        if stem not in manifest["repair_required_banks"]:
            continue
        result = SNAPSHOT / "results" / (stem + ".json")
        journal = SNAPSHOT / "journals" / stem
        if result.exists():
            completion = native.load(journal / "completion.json")
            if completion["result_sha256"] != native.sha(result):
                raise ValueError("terminal recovery result changed: " + stem)
        elif journal.exists():
            raise FileExistsError("ambiguous/interrupted single repair; inspect, never retry: " + stem)
        else:
            pending.append(case)
    with ThreadPoolExecutor(max_workers=2) as executor:
        for future in as_completed([
            executor.submit(repair_one, case, manifest["revalidation"][case["case_id"]], config)
            for case in pending
        ]):
            future.result()
    results = {
        case["case_id"]: native.load(SNAPSHOT / "results" / (case["case_id"] + ".json"))
        for case in manifest["cases"]
    }
    receipt = {
        "completed_at_utc": native.now(), "original_native_successful_banks": 0,
        "original_native_failed_banks": 16, "original_semantic_calls": 32,
        "accepted_unchanged_banks": len(manifest["accepted_unchanged_banks"]),
        "additional_semantic_calls": sum(result["extra_semantic_calls"] for result in results.values()),
        "successful_banks": sum(result["status"] == "ok" for result in results.values()),
        "failed_banks": sum(result["status"] != "ok" for result in results.values()), "pending_banks": 0,
        "result_files": {
            stem: native.sha(SNAPSHOT / "results" / (stem + ".json")) for stem in results
        },
    }
    native.write(SNAPSHOT / "run_complete.json", receipt)
    print(json.dumps(receipt), flush=True)
    return 2 if receipt["failed_banks"] else 0


def audit_export():
    manifest = verify()
    terminal = native.load(SNAPSHOT / "run_complete.json")
    if (terminal["successful_banks"], terminal["failed_banks"], terminal["pending_banks"]) != (16, 0, 0):
        raise ValueError("recovered export requires sixteen genuinely valid complete banks")
    old = engine(native.SNAPSHOT / "runtime/v6_5_training", "v6_5_training")
    config = engine(RUNTIME, "v6_5_training_r2")
    native_terminal = native.load(native.SNAPSHOT / "run_complete.json")
    rows, banks, audits = [], {}, []
    extra_calls = native_transport = extra_transport = 0
    for case in manifest["cases"]:
        stem = case["case_id"]
        previous, source, _ = replay_native(case, native_terminal, old)
        record = revalidate(case, previous, source, config)
        if record != manifest["revalidation"][stem]:
            raise ValueError("unchanged-final revalidation does not replay: " + stem)
        result_path = SNAPSHOT / "results" / (stem + ".json")
        result = native.load(result_path)
        if native.sha(result_path) != terminal["result_files"][stem] or result["status"] != "ok":
            raise ValueError("recovery terminal result changed: " + stem)
        native_transport += sum(attempt["provider"]["transport_attempts"] for attempt in previous["audit"]["attempts"])
        journal = SNAPSHOT / "journals" / stem
        if record["validation"]["passed"]:
            if journal.exists() or result["extra_semantic_calls"] != 0:
                raise ValueError("a valid unchanged bank was redrawn")
            normalized, validation, reply = previous["audit"]["attempts"][-1]["normalized_output"], record["validation"], None
            kind = "accepted_unchanged_final"
        else:
            request = native.load(journal / "request.json")
            if request != {"messages": recovery_messages(config, source, previous, record["validation"]["errors"]),
                           "schema": config.schema}:
                raise ValueError("single repair actual request/configuration does not replay")
            launch = native.load(journal / "launch.json")
            if launch["maximum_semantic_invocations"] != 1 or launch["authorization"] != AUTHORIZATION:
                raise ValueError("single repair launch provenance changed")
            reply = native.load(journal / "response.json")
            require_settings(reply)
            replay = validate_reply(config, reply, source)
            if replay != native.load(journal / "normalization.json") or replay["errors"]:
                raise ValueError("single repair raw-response validation does not replay")
            normalized = replay["normalized_output"]
            camera = config.resolve_camera(config.registry, source["camera_tag"])
            validation = config.validation.validate_output(normalized, source, config.catalog, camera, config.references)
            completion = native.load(journal / "completion.json")
            if completion["result_sha256"] != native.sha(result_path) or completion["status"] != "ok":
                raise ValueError("single repair completion provenance changed")
            kind = "authorized_single_repair"
            extra_calls += 1
            extra_transport += reply["transport_attempts"]
        expected = recovered_result(case, config, normalized, validation, kind=kind, reply=reply)
        if result != expected or not validation["passed"]:
            raise ValueError("recovered prose/host ranking/support/debug does not replay: " + stem)
        for rank, candidate in enumerate(result["prompts"], 1):
            if candidate["text"] != next(row["text"] for row in normalized["prompts"] if row["id"] == candidate["id"]):
                raise ValueError("finalizer altered actual scene text")
            rows.append({
                **{key: copy.deepcopy(case[key]) for key in (
                    "device_id", "device_display_name", "device_type", "source_pair", "camera_tag",
                    "source_camera_name", "view_role", "render_gallery_url", "render_lookup",
                )},
                "prompt_key": f"{stem}::{candidate['id']}", "bank_rank": rank, **copy.deepcopy(candidate),
                "text_sha256": hashlib.sha256(candidate["text"].encode()).hexdigest(), "bank_debug_ref": stem,
            })
        banks[stem] = {
            "case_metadata": case, "source_input": source,
            "source_input_path": str(SNAPSHOT / case["frozen_input_path"]),
            "source_input_sha256": case["frozen_input_sha256"],
            "result_path": str(result_path), "result_sha256": native.sha(result_path), "debug": result["debug"],
            "run": {
                "status": "ok", "original_native_status": "error", "original_returncode": 2,
                "native_semantic_calls": 2, "extra_semantic_calls": result["extra_semantic_calls"],
                "semantic_calls": 2 + result["extra_semantic_calls"], "recovery_kind": kind,
                "final_validation_errors": [],
            },
            "revalidation": record,
            "recovery_journal_path": str(journal) if journal.exists() else None,
        }
        audits.append({"case_id": stem, "recovery_kind": kind, "prompts": 10,
                       "actual_response_equality": True, "source_score_sort_support_replay": True,
                       "original_native_status": "error", "original_returncode": 2})
    if (
        len(rows) != 160 or len({row["prompt_key"] for row in rows}) != 160
        or len({row["text"] for row in rows}) != 160
        or extra_calls != terminal["additional_semantic_calls"]
        or extra_calls != len(manifest["repair_required_banks"])
    ):
        raise ValueError("recovery export/count/repair-limit discrepancy")
    destination = SNAPSHOT / "exports"
    native.write(destination / "prompts_all_160.json", {
        "version": "hp-lifestyle-v6.5-training-recovered-all160-v1",
        "snapshot_manifest_path": str(SNAPSHOT / "recovery_manifest.json"),
        "snapshot_manifest_sha256": native.sha(SNAPSHOT / "recovery_manifest.json"),
        "selection_rule": "all ten source/C-Tech-ranked candidates in the same sixteen original V6.4 input banks",
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16, "candidates_per_bank": 10, "prompts": 160},
        "device_source_mapping": manifest["device_source_mapping"], "bank_audit": banks, "prompts": rows,
        "original_native_successful_banks": 0, "original_native_failed_banks": 16,
        "accepted_unchanged_banks": len(manifest["accepted_unchanged_banks"]), "additional_semantic_calls": extra_calls,
    })
    text = "\n\n".join(native.helpers()._plain_text_block(row) for row in rows) + "\n"
    native.write(destination / "prompts_all_160.txt", text)
    native.write(destination / "completion_audit.json", {
        "passed": True, "verified_at_utc": native.now(), "prompts": 160, "banks": 16,
        "export_sha256": native.sha(destination / "prompts_all_160.json"),
        "plain_text_export_sha256": native.sha(destination / "prompts_all_160.txt"),
        "actual_semantic_calls": 32 + extra_calls, "actual_transport_attempts": native_transport + extra_transport,
        "full_bank_repairs": 16 + extra_calls, "original_native_successful_banks": 0, "original_native_failed_banks": 16,
        "accepted_unchanged_banks": len(manifest["accepted_unchanged_banks"]),
        "additional_semantic_calls": extra_calls, "additional_transport_attempts": extra_transport,
        "offline_revalidation": True, "explicit_additional_repair_authorization": AUTHORIZATION,
        "additional_model_calls_for_audit": 0, "native_image_calls": 0,
        "banks_verified": audits, "auditor_sha256": native.sha(__file__),
    })
    print(json.dumps({"verified_prompts": 160, "additional_semantic_calls": extra_calls}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "verify", "run", "audit-export"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "verify":
        print(json.dumps({"verified_banks": len(verify()["cases"])}))
    elif args.command == "run":
        raise SystemExit(run(args.paid_calls_authorized))
    else:
        audit_export()
