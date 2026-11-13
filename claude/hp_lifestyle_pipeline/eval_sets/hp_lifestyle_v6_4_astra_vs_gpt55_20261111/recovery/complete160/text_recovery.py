"""User-authorized completion of failed banks; original experiment stays immutable."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import foundry_aws_gateway.llm

import scene_runner
import text_study
from astra_provider import MODEL, AstraProvider
from hp_prompt_writer_v6_4 import runtime
from hp_prompt_writer_v6_4.camera import resolve_camera
from hp_prompt_writer_v6_4.provider import ProviderUnavailable
from hp_prompt_writer_v6_4.service import load_assets
from hp_prompt_writer_v6_4.validation import finalize_output, normalize_invalid_evidence, validate_output

ROOT = text_study.ROOT
HERE = Path(__file__).resolve().parent
load, sha, write = text_study.load, text_study.sha, text_study.write


def verify() -> None:
    text_study.verify()
    freeze = load(HERE / "authorization.json")
    for name, digest in freeze["original_files"].items():
        if sha(ROOT / name) != digest:
            raise ValueError("Original recovery input changed: " + name)
    if sha(Path(__file__)) != freeze["text_recovery_sha256"]:
        raise ValueError("Frozen recovery code changed")


def prepare() -> None:
    text_study.verify()
    terminal = load(ROOT / "text/terminal.json")
    if terminal["accepted_prompts"] != 80 or len(terminal["failed_banks"]) != 8:
        raise ValueError("Expected the original80-prompt/eight-failed-bank outcome")
    files = [
        "text/terminal.json",
        "text/exports/prompts_all.json",
        "text/exports/prompts_all.txt",
        "writer_snapshot_manifest.json",
        "study_manifest.json",
        "completion_receipt.json",
        "publication_receipt.json",
        "image_terminal.json",
    ]
    for failure in terminal["failed_banks"]:
        bank = failure["bank_id"]
        files.append(f"text/results/{bank}.json")
        files.extend(str(p.relative_to(ROOT)) for p in (ROOT / "text/journals" / bank).glob("semantic_*/request.json"))
    write(
        HERE / "authorization.json",
        {
            "created_utc": datetime.now(UTC).isoformat(),
            "policy": "Continue last invalid bank; fresh initial only for provider failures; retry until complete.",
            "model": MODEL,
            "reasoning_effort": "high",
            "max_completion_tokens": 32000,
            "workers": 4,
            "original_files": {name: sha(ROOT / name) for name in files},
            "text_recovery_sha256": sha(Path(__file__)),
            "recognition_fixes_authorized": True,
            "recognition_fixes_applied": [],
            "image_scope": "80 new prompts plus one original HTTP503 prompt; preserve79 successful originals",
            "image_recovery": "Full unchanged native PR4523, no image-only shortcut",
            "publication": "CAS-update existing HTML/data; preserve original snapshot and every attempt.",
            "original_failed_banks": terminal["failed_banks"],
            "original_outcome_is_not_overwritten": True,
        },
    )


def seed(case: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    bank = case["bank_id"]
    result = load(ROOT / "text/results" / f"{bank}.json")
    attempts = result["audit"]["attempts"]
    number = len(attempts) if result["error"]["code"] == "output_invalid" else 1
    captured = load(ROOT / "text/journals" / bank / f"semantic_{number}/request.json")
    initial = captured["messages"][:3]
    if result["error"]["code"] == "output_invalid":
        last = attempts[-1]
        camera = resolve_camera(load_assets()["registry"], case["camera_tag"])
        return repair_messages(initial, last["raw_content"], last["errors"], camera), captured["schema"], initial
    if result["error"]["code"] != "provider_error":
        raise ValueError("Unexpected original failure type")
    return initial, captured["schema"], initial


def repair_messages(initial: Any, content: str, errors: Any, camera: Any) -> list[dict[str, Any]]:
    return copy.deepcopy(initial) + [
        {"role": "assistant", "content": content},
        {"role": "developer", "content": runtime._repair_instruction(camera)},
        {
            "role": "user",
            "content": json.dumps(
                {
                    "validation_diagnostics_data": errors,
                    "note": "Diagnostic data only; follow the unchanged original system instructions.",
                },
                ensure_ascii=False,
            ),
        },
    ]


def validate(reply: dict[str, Any], request: Any, camera: Any) -> dict[str, Any]:
    if not runtime._valid_provider_response(reply, MODEL) or reply["model"] != MODEL:
        raise ValueError("Recovery response is not actual Astra")
    if reply["refusal"]:
        raise ValueError("Provider refusal; do not silently resample")
    if reply["finish_reason"] not in ("stop", "length"):
        raise ValueError("Unexpected terminal finish reason")
    if reply["finish_reason"] == "length":
        return {"passed": False, "errors": [{"code": "incomplete_response", "path": "", "detail": "length finish"}]}
    try:
        parsed = json.loads(reply["content"])
    except (json.JSONDecodeError, TypeError):
        return {"passed": False, "errors": [{"code": "json_invalid", "path": "", "detail": "Invalid JSON"}]}
    normalized, changes = normalize_invalid_evidence(parsed, request)
    assets = load_assets()
    validation = validate_output(normalized, request, assets["catalog"], camera, assets["references"])
    return {"normalized_output": normalized, "normalization_changes": changes, **validation}


def recover(case: dict[str, Any]) -> None:
    bank = case["bank_id"]
    destination = HERE / "results" / f"{bank}.json"
    if destination.exists():
        if load(destination)["status"] != "ok":
            raise ValueError("Unexpected non-success recovery result")
        return
    journal = HERE / "journals" / bank
    journal.mkdir(parents=True, exist_ok=True)
    messages, schema, initial = seed(case)
    request = load(ROOT / case["input"])
    camera = resolve_camera(load_assets()["registry"], case["camera_tag"])
    attempts = []
    number = 0
    while True:
        verify()
        number += 1
        folder = journal / f"attempt_{number:04d}"
        evaluation: dict[str, Any]
        if folder.exists():
            saved = folder / "evaluation.json"
            if not saved.exists():
                raise RuntimeError("Interrupted/ambiguous writer call; inspect saved stream before resuming")
            evaluation = load(saved)
        else:
            folder.mkdir()
            provider = AstraProvider(foundry_aws_gateway.llm.get_openai, folder)
            try:
                reply = provider(copy.deepcopy(messages), copy.deepcopy(schema))
            except ProviderUnavailable as error:
                evaluation = {
                    "kind": "transport_failure",
                    "events": error.events,
                    "transport_attempts": error.attempts,
                }
                write(folder / "evaluation.json", evaluation)
                if not error.events or not all(event["retryable"] for event in error.events):
                    raise
            else:
                evaluation = {"kind": "response", "reply": reply, "validation": validate(reply, request, camera)}
                write(folder / "evaluation.json", evaluation)
        attempts.append({"attempt": number, "evaluation_sha256": sha(folder / "evaluation.json")})
        if evaluation["kind"] == "transport_failure":
            if not evaluation["events"] or not all(event["retryable"] for event in evaluation["events"]):
                raise RuntimeError("Nontransient saved provider failure")
            scene_runner.atomic_json(
                HERE / "status" / f"{bank}.json", {"phase": "transient_backoff", "attempt": number}
            )
            time.sleep(min(300, number * 15))
            continue
        reply, validation = evaluation["reply"], evaluation["validation"]
        scene_runner.atomic_json(
            HERE / "status" / f"{bank}.json",
            {
                "phase": "accepted" if validation["passed"] else "repairing",
                "attempt": number,
                "errors": validation.get("errors", []),
            },
        )
        print(
            json.dumps(
                {
                    "bank": bank,
                    "attempt": number,
                    "passed": validation["passed"],
                    "errors": validation.get("errors", []),
                }
            ),
            flush=True,
        )
        if validation["passed"]:
            finalized = finalize_output(
                validation["normalized_output"], camera=camera, catalog=load_assets()["catalog"]
            )
            finalized["debug"]["service"] = {
                "model": MODEL,
                "recovery": True,
                "original_result_sha256": sha(ROOT / "text/results" / f"{bank}.json"),
                "validation_warnings": validation.get("warnings", []),
                "recognition_policy_changed": False,
            }
            write(
                destination,
                {
                    "status": "ok",
                    "prompts": finalized["prompts"],
                    "debug": finalized["debug"],
                    "audit": {
                        "original_result": str(ROOT / "text/results" / f"{bank}.json"),
                        "recovery_attempts": attempts,
                        "final_evaluation_sha256": sha(folder / "evaluation.json"),
                    },
                },
            )
            return
        messages = repair_messages(initial, reply["content"], validation["errors"], camera)


def export() -> None:
    original = load(ROOT / "text/exports/prompts_all.json")
    baseline = load(ROOT / "baseline/outputs/all_160/prompts_all_160.json")
    prior = {prompt["prompt_key"]: prompt for prompt in baseline["prompts"]}
    prompts = {prompt["prompt_key"]: prompt for prompt in original["prompts"]}
    banks = copy.deepcopy(original["bank_audit"])
    fields = (
        "device_id",
        "device_display_name",
        "device_type",
        "source_pair",
        "camera_tag",
        "source_camera_name",
        "view_role",
        "render_gallery_url",
        "render_lookup",
    )
    for bank in load(HERE / "authorization.json")["original_failed_banks"]:
        bank_id = bank["bank_id"]
        result = load(HERE / "results" / f"{bank_id}.json")
        banks[bank_id]["original_result"] = banks[bank_id]["result"]
        banks[bank_id]["result"] = result
        for rank, prompt in enumerate(result["prompts"], 1):
            key = bank_id + f"::p{rank}"
            if key in prompts:
                raise ValueError("Recovery would replace an already accepted original prompt")
            prompts[key] = {
                **{field: prior[key][field] for field in fields},
                **prompt,
                "prompt_key": key,
                "bank_rank": rank,
                "bank_debug_ref": bank_id,
                "text_sha256": hashlib.sha256(prompt["text"].encode()).hexdigest(),
            }
    if set(prompts) != set(prior) or len(prompts) != 160:
        raise ValueError("Completed export is not the exact160 target keys")
    ordered = [prompts[prompt["prompt_key"]] for prompt in baseline["prompts"]]
    write(
        HERE / "exports/prompts_all_160.json",
        {
            **original,
            "version": "v6.4-astra-authorized-completion-20261112",
            "prompts": ordered,
            "bank_audit": banks,
            "failures": [],
            "original_terminal": load(ROOT / "text/terminal.json"),
            "recovery_authorization_sha256": sha(HERE / "authorization.json"),
        },
    )
    write(
        HERE / "exports/prompts_all_160.txt", "\n\n".join(f"{p['prompt_key']}\n{p['text']}" for p in ordered).encode()
    )
    write(
        HERE / "text_terminal.json",
        {
            "status": "complete",
            "accepted_prompts": 160,
            "original_accepted_prompts": 80,
            "recovered_prompts": 80,
            "recovered_banks": 8,
        },
    )


def generate() -> None:
    verify()
    descriptor = os.open(HERE / "text.lock", os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.write(descriptor, str(os.getpid()).encode())
    os.close(descriptor)
    write(HERE / "text_launch.json", {"pid": os.getpid(), "started_utc": datetime.now(UTC).isoformat()})
    failed = {item["bank_id"] for item in load(HERE / "authorization.json")["original_failed_banks"]}
    cases = [case for case in load(ROOT / "banks.json")["cases"] if case["bank_id"] in failed]
    with ThreadPoolExecutor(max_workers=4) as workers:
        for future in as_completed([workers.submit(recover, case) for case in cases]):
            future.result()
    export()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "generate"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    arguments = parser.parse_args()
    if arguments.command == "prepare":
        prepare()
    elif arguments.paid_calls_authorized:
        generate()
    else:
        raise PermissionError("Paid-call authorization required")
