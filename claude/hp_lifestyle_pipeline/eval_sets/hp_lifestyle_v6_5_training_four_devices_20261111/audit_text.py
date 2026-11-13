#!/usr/bin/env python3
"""Replay native replacement responses, validation, source ranking and export."""
import copy
import hashlib
import json
import sys

import run_text_eval as study


def main():
    manifest = study.verify()
    snapshot = study.SNAPSHOT
    export = snapshot / "exports/prompts_all_160.json"
    document = study.load(export)
    terminal = study.load(snapshot / "run_complete.json")
    if (terminal["successful_banks"], terminal["failed_banks"], terminal["pending_banks"]) != (16, 0, 0):
        raise ValueError("fresh audit requires sixteen actual successful banks")
    sys.path.insert(0, str(snapshot / "runtime"))
    from v6_5_training.camera import resolve_camera
    from v6_5_training.catalog import validate_catalog
    from v6_5_training.runtime import _effective_model_schema, _repair_instruction
    from v6_5_training.validation import finalize_output, normalize_invalid_evidence, validate_output

    runtime = snapshot / "runtime/v6_5_training"
    catalog = study.load(runtime / study.CATALOGUE)
    validate_catalog(catalog)
    registry = study.load(runtime / "camera_profiles.json")
    references = study.load(runtime / "reference_library.json")
    guidance = study.load(runtime / "prop_guidance.json")["entries"]
    schema = _effective_model_schema(
        study.load(runtime / "model_output.schema.json"), [entry["id"] for entry in catalog["entries"]],
    )
    by_slot = {
        (row["device_id"], row["camera_tag"], row["bank_rank"]): row for row in document["prompts"]
    }
    if len(by_slot) != 160 or len(document["prompts"]) != 160:
        raise ValueError("full export does not contain160 unique slots")
    audits = []
    semantic_calls = transport_calls = repairs = 0
    for case in manifest["cases"]:
        stem = case["case_id"]
        result_path = snapshot / "results" / (stem + ".json")
        result = study.load(result_path)
        process = study.load(snapshot / "call_journals" / (stem + ".process.json"))
        if (
            result["status"] != "ok" or process["returncode"] != 0
            or process["output_sha256"] != study.sha(result_path) or terminal["cases"][stem] != process
        ):
            raise ValueError(f"native result/process provenance differs: {stem}")
        source_path = snapshot / case["frozen_input_path"]
        source = study.load(source_path)
        if (
            study.sha(source_path) != case["frozen_input_sha256"]
            or source_path.read_bytes() != (study.BASELINE / case["frozen_input_path"]).read_bytes()
            or result["audit"]["source_input"] != source
        ):
            raise ValueError(f"input not byte-identical to V6.4: {stem}")
        camera = resolve_camera(registry, source["camera_tag"])
        expected_trusted = {
            "camera": camera, "approved_catalogue": catalog["entries"],
            "reference_library": references, "approved_prop_usage_guidance": guidance,
        }
        attempts = result["audit"]["attempts"]
        if len(attempts) not in {1, 2} or result["audit"]["semantic_calls"] != len(attempts):
            raise ValueError("semantic limit/accounting violated")
        for number, attempt in enumerate(attempts, 1):
            journal = snapshot / "results" / (stem + ".json.run")
            request = study.load(journal / f"attempt_{number}.request.json")
            reply = study.load(journal / f"attempt_{number}.response.json")
            messages = request["messages"]
            if (
                request["schema"] != schema
                or messages[0] != {"role": "system", "content": (runtime / "system_prompt.md").read_text()}
                or messages[1]["role"] != "system" or json.loads(messages[1]["content"]) != expected_trusted
                or messages[2]["role"] != "user" or json.loads(messages[2]["content"]) != source
            ):
                raise ValueError(f"actual request differs from frozen configuration: {stem}/{number}")
            if number == 2 and (
                len(messages) != 6
                or messages[3] != {"role": "assistant", "content": attempts[0]["raw_content"] or ""}
                or messages[4] != {"role": "developer", "content": _repair_instruction(camera)}
                or json.loads(messages[5]["content"])["validation_diagnostics_data"] != attempts[0]["errors"]
            ):
                raise ValueError("repair is not the exact complete-bank continuation")
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
                or reply["settings"]["timeout"] != 180 or reply["refusal"] is not None
            ):
                raise ValueError("writer settings/refusal changed")
            if reply["finish_reason"] == "stop":
                parsed = json.loads(reply["content"])
                if parsed != attempt["parsed_output"]:
                    raise ValueError("native parsed output changed")
                normalized, changes = normalize_invalid_evidence(parsed, source)
                if normalized != attempt["normalized_output"] or changes != attempt["normalization_changes"]:
                    raise ValueError("host evidence normalization does not replay")
                replayed_validation = validate_output(normalized, source, catalog, camera, references)
                if replayed_validation["errors"] != attempt["errors"]:
                    raise ValueError(f"native diagnostics do not replay: {stem}/{number}")
            elif number == len(attempts) or reply["finish_reason"] != "length":
                raise ValueError("invalid final or unsupported initial finish")
            transport_calls += reply["transport_attempts"]
        final = attempts[-1]["normalized_output"]
        if not validate_output(final, source, catalog, camera, references)["passed"] or attempts[-1]["errors"]:
            raise ValueError(f"native final bank fails independent validation: {stem}")
        replayed = finalize_output(copy.deepcopy(final), camera=camera, catalog=catalog)
        if replayed["prompts"] != result["prompts"]:
            raise ValueError("application-owned scores/ranking/text/support do not replay")
        study.helpers()._validate_call_journals(snapshot, stem, result)
        for rank, candidate in enumerate(replayed["prompts"], 1):
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
    if len({row["text"] for row in document["prompts"]}) != 160:
        raise ValueError("scene texts are not distinct")
    plain_text = "\n\n".join(study.helpers()._plain_text_block(row) for row in document["prompts"]) + "\n"
    if (snapshot / "exports/prompts_all_160.txt").read_text() != plain_text:
        raise ValueError("plain-text export differs from actual candidates")
    study.write(snapshot / "exports/completion_audit.json", {
        "passed": True, "verified_at_utc": study.now(), "export_sha256": study.sha(export),
        "prompts": 160, "banks": 16,
        "plain_text_export_sha256": study.sha(snapshot / "exports/prompts_all_160.txt"),
        "actual_semantic_calls": semantic_calls, "actual_transport_attempts": transport_calls,
        "full_bank_repairs": repairs, "terminal_bank_resampling": False,
        "native_image_calls": 0, "banks_verified": audits, "offline_revalidation": False,
        "original_native_successful_banks": 16, "original_native_failed_banks": 0,
        "additional_model_calls_for_audit": 0, "auditor_sha256": study.sha(__file__),
    })
    print(json.dumps({"verified_prompts": 160, "semantic_calls": semantic_calls,
                      "full_bank_repairs": repairs}), flush=True)


if __name__ == "__main__":
    main()
