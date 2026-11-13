#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml", "tomli", "jsonschema"]
# ///
"""Run one bounded GPT-5.5 correction pass without mutating first-draw evidence."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VERSION = ROOT / "research/source_messaging_v1_to_v6/versions/v4.1"
SCRIPTS = VERSION / "scripts"
PASS_ROOT = HERE / "repair_pass_01"
QUEUE_PATH = HERE / "repair_review_queue.json"
INSTRUCTION_PATH = HERE / "repair_instruction.md"
SYSTEM_PATH = VERSION / "system_prompt.md"
SCHEMA_PATH = VERSION / "output.schema.json"
REGISTRY_PATH = VERSION / "camera_profiles.json"

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(ROOT / "research/source_messaging_v1_to_v6/scripts"))
from record_integrity import write_json_exclusive  # noqa: E402
from probe_gpt55 import client_and_auth_mode  # noqa: E402
from finalize_output import finalize_output, semantic_sha256  # noqa: E402
from camera_profile_resolver import load_registry  # noqa: E402
from validate_output import validate_output  # noqa: E402


_SHARED_RUNNER_PATH = ROOT / "research/source_messaging_v1_to_v6/scripts/run_gpt55.py"
_spec = importlib.util.spec_from_file_location("shared_gpt55_runner", _SHARED_RUNNER_PATH)
_shared = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_shared)
retry_delay, transient = _shared.retry_delay, _shared.transient

METADATA_FIELDS = {
    "ctech_relationship",
    "ctech_reference_score",
    "ctech_changes",
    "ctech_explanation",
}
SETTINGS = {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 24000,
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode()


def sha_obj(value: Any) -> str:
    return sha_bytes(canonical_bytes(value))


def file_sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def changed_top_level_fields(original: dict[str, Any], proposed: dict[str, Any]) -> list[str]:
    return sorted(key for key in set(original) | set(proposed)
                  if original.get(key) != proposed.get(key))


def merge_proposal(base: dict[str, Any], proposed: dict[str, Any], review_case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Apply only queue-authorized candidate fields and retain an exhaustive edit log."""
    base_by_id = {candidate["id"]: candidate for candidate in base["prompts"]}
    proposed_by_id: dict[str, dict[str, Any]] = {}
    duplicate_ids = []
    for candidate in proposed["prompts"]:
        candidate_id = candidate["id"]
        if candidate_id in proposed_by_id:
            duplicate_ids.append(candidate_id)
        proposed_by_id[candidate_id] = candidate
    if duplicate_ids or set(proposed_by_id) != set(base_by_id):
        raise ValueError({
            "duplicate_proposed_ids": sorted(set(duplicate_ids)),
            "missing_proposed_ids": sorted(set(base_by_id) - set(proposed_by_id)),
            "extra_proposed_ids": sorted(set(proposed_by_id) - set(base_by_id)),
        })

    issues = {item["candidate_id"]: item for item in review_case["issues"]}
    if len(issues) != len(review_case["issues"]):
        raise ValueError("duplicate candidate IDs in repair queue")
    if not set(issues) <= set(base_by_id):
        raise ValueError(f"unknown queued candidate IDs: {sorted(set(issues)-set(base_by_id))}")

    merged_by_id: dict[str, dict[str, Any]] = {}
    accepted_changes = []
    discarded_changes = []
    unchanged_candidates = []
    for candidate_id, original in base_by_id.items():
        proposal = proposed_by_id[candidate_id]
        review = issues.get(candidate_id)
        changed_fields = changed_top_level_fields(original, proposal)
        if review is None:
            merged_by_id[candidate_id] = copy.deepcopy(original)
            unchanged_candidates.append(candidate_id)
            for field in changed_fields:
                discarded_changes.append({
                    "candidate_id": candidate_id,
                    "field": field,
                    "reason": "unflagged_candidate_must_remain_entirely_original",
                    "original": copy.deepcopy(original.get(field)),
                    "proposed": copy.deepcopy(proposal.get(field)),
                })
            continue

        if review["scene_edit_allowed"]:
            if review["allowed_fields"] != "all_except_id_and_ctech_reference_id":
                raise ValueError(f"unexpected scene permission for {candidate_id}")
            merged_candidate = copy.deepcopy(proposal)
            for field in ("id", "ctech_reference_id"):
                if proposal.get(field) != original.get(field):
                    discarded_changes.append({
                        "candidate_id": candidate_id,
                        "field": field,
                        "reason": "immutable_scene_candidate_identity",
                        "original": copy.deepcopy(original.get(field)),
                        "proposed": copy.deepcopy(proposal.get(field)),
                    })
                merged_candidate[field] = copy.deepcopy(original[field])
            for field in changed_fields:
                if field not in {"id", "ctech_reference_id"}:
                    accepted_changes.append({
                        "candidate_id": candidate_id,
                        "field": field,
                        "reason": "scene_edit_allowed",
                        "original": copy.deepcopy(original.get(field)),
                        "proposed": copy.deepcopy(proposal.get(field)),
                    })
            merged_by_id[candidate_id] = merged_candidate
            continue

        allowed = set(review["allowed_fields"])
        if allowed != METADATA_FIELDS:
            raise ValueError(f"unexpected metadata permission for {candidate_id}: {sorted(allowed)}")
        merged_candidate = copy.deepcopy(original)
        for field in allowed:
            if proposal[field] != original[field]:
                accepted_changes.append({
                    "candidate_id": candidate_id,
                    "field": field,
                    "reason": "metadata_only_field_allowed",
                    "original": copy.deepcopy(original[field]),
                    "proposed": copy.deepcopy(proposal[field]),
                })
            merged_candidate[field] = copy.deepcopy(proposal[field])
        for field in changed_fields:
            if field not in allowed:
                discarded_changes.append({
                    "candidate_id": candidate_id,
                    "field": field,
                    "reason": "metadata_only_field_not_allowed",
                    "original": copy.deepcopy(original.get(field)),
                    "proposed": copy.deepcopy(proposal.get(field)),
                })
        merged_by_id[candidate_id] = merged_candidate

    merged = copy.deepcopy(base)
    merged["prompts"] = [merged_by_id[item["id"]] for item in base["prompts"]]
    if proposed.get("debug") != base.get("debug"):
        discarded_changes.append({
            "candidate_id": None,
            "field": "debug",
            "reason": "no_quote_correction_authorized_keep_original_debug",
            "original": copy.deepcopy(base.get("debug")),
            "proposed": copy.deepcopy(proposed.get("debug")),
        })
    merged["debug"] = copy.deepcopy(base["debug"])
    log = {
        "version": "v4.1-bounded-repair-merge-v1",
        "policy": {
            "unflagged": "entire candidate copied from base",
            "metadata_only": "copy only ctech_relationship, ctech_reference_score, ctech_changes, ctech_explanation",
            "scene_edit": "copy proposed candidate except preserve base id and ctech_reference_id",
            "debug": "copy base debug; no quote correction was authorized",
        },
        "base_semantic_sha256": semantic_sha256(base),
        "proposed_semantic_sha256": semantic_sha256(proposed),
        "merged_semantic_sha256": semantic_sha256(merged),
        "flagged_candidate_count": len(issues),
        "scene_edit_candidate_count": sum(bool(item["scene_edit_allowed"])
                                          for item in review_case["issues"]),
        "metadata_only_candidate_count": sum(not item["scene_edit_allowed"]
                                             for item in review_case["issues"]),
        "unflagged_candidate_count": len(unchanged_candidates),
        "unflagged_candidate_ids": unchanged_candidates,
        "accepted_field_change_count": len(accepted_changes),
        "accepted_field_changes": accepted_changes,
        "discarded_unauthorized_change_count": len(discarded_changes),
        "discarded_unauthorized_changes": discarded_changes,
    }
    return merged, log


def build_request(case_id: str, review_case: dict[str, Any], system: str,
                  repair_instruction: str, schema: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    base_path = Path(review_case["base_normalized_output_path"])
    raw_path = Path(review_case["base_raw_record_path"])
    if file_sha(raw_path) != review_case["base_raw_sha256"]:
        raise RuntimeError(f"base raw hash changed: {case_id}")
    base = json.loads(base_path.read_text())
    raw_record = json.loads(raw_path.read_text())
    raw_input = json.loads(raw_record["raw_input_json"])
    input_path = Path(raw_record["input_path"])
    if file_sha(input_path) != raw_record["input_sha256"]:
        raise RuntimeError(f"runtime input hash changed: {case_id}")
    user_payload = {
        "original_runtime_input": raw_input,
        "previous_normalized_output": base,
        "review_case": review_case,
    }
    combined_system = system + "\n\n" + repair_instruction
    api_request = {
        **SETTINGS,
        "messages": [
            {"role": "system", "content": combined_system},
            {"role": "user", "content": canonical_bytes(user_payload).decode()},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "hp_lifestyle_ctech_v4_1_repair",
                "strict": True,
                "schema": schema,
            },
        },
    }
    lineage = {
        "case_id": case_id,
        "base_raw_record_path": str(raw_path),
        "base_raw_record_sha256": file_sha(raw_path),
        "base_raw_request_sha256": raw_record["request_sha256"],
        "base_normalized_output_path": str(base_path),
        "base_normalized_output_file_sha256": file_sha(base_path),
        "base_normalized_output_semantic_sha256": semantic_sha256(base),
        "runtime_input_path": str(input_path),
        "runtime_input_sha256": raw_record["input_sha256"],
        "system_prompt_path": str(SYSTEM_PATH),
        "system_prompt_sha256": file_sha(SYSTEM_PATH),
        "repair_instruction_path": str(INSTRUCTION_PATH),
        "repair_instruction_sha256": file_sha(INSTRUCTION_PATH),
        "combined_system_sha256": sha_bytes(combined_system.encode()),
        "output_schema_path": str(SCHEMA_PATH),
        "output_schema_sha256": file_sha(SCHEMA_PATH),
        "repair_queue_path": str(QUEUE_PATH),
        "repair_queue_sha256": file_sha(QUEUE_PATH),
        "repair_queue_version": json.loads(QUEUE_PATH.read_text())["version"],
    }
    return api_request, lineage


def run_case(case_id: str, review_case: dict[str, Any], client: Any, auth_mode: str,
             system: str, repair_instruction: str, schema: dict[str, Any],
             registry: dict[str, Any], max_transient_attempts: int) -> dict[str, Any]:
    case_dir = PASS_ROOT / case_id
    case_dir.mkdir(parents=True, exist_ok=False)
    api_request, lineage = build_request(
        case_id, review_case, system, repair_instruction, schema)
    request_doc = {
        "version": "v4.1-bounded-repair-request-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "request_sha256": sha_obj(api_request),
        "api_request_without_credentials": api_request,
        "lineage": lineage,
    }
    write_json_exclusive(case_dir / "request.json", request_doc)
    started_at = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    retry_events = []
    for transport_attempt in range(1, max_transient_attempts + 1):
        try:
            response = client.chat.completions.create(**api_request)
        except Exception as exc:
            if not transient(exc) or transport_attempt == max_transient_attempts:
                failure = {
                    "version": "v4.1-bounded-repair-failure-v1",
                    "case_id": case_id,
                    "request_sha256": request_doc["request_sha256"],
                    "started_at": started_at,
                    "failed_at": datetime.now(timezone.utc).isoformat(),
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "transport_attempts": transport_attempt,
                    "retry_events": retry_events,
                    "failure": {
                        "type": type(exc).__name__,
                        "status_code": getattr(exc, "status_code", None),
                        "detail": str(exc)[:1200],
                    },
                }
                write_json_exclusive(case_dir / "failure.json", failure)
                return {"case_id": case_id, "status": "transport_failed", **failure}
            delay = retry_delay(exc, transport_attempt)
            event = {
                "transport_attempt": transport_attempt,
                "type": type(exc).__name__,
                "status_code": getattr(exc, "status_code", None),
                "wait_seconds": delay,
            }
            retry_events.append(event)
            write_json_exclusive(case_dir / f"transport_retry_{transport_attempt:03d}.json", event)
            time.sleep(delay)
            continue

        response_payload = response.model_dump(mode="json")
        provider_doc = {
            "version": "v4.1-bounded-repair-provider-response-v1",
            "case_id": case_id,
            "request_sha256": request_doc["request_sha256"],
            "received_at": datetime.now(timezone.utc).isoformat(),
            "transport_attempt": transport_attempt,
            "response": response_payload,
        }
        provider_path = case_dir / "provider_response.json"
        write_json_exclusive(provider_path, provider_doc)
        response_record = {
            "version": "v4.1-bounded-repair-response-record-v1",
            "case_id": case_id,
            "request_sha256": request_doc["request_sha256"],
            "request_path": str(case_dir / "request.json"),
            "request_file_sha256": file_sha(case_dir / "request.json"),
            "provider_response_path": str(provider_path),
            "provider_response_sha256": file_sha(provider_path),
            "auth_mode": auth_mode,
            "started_at": started_at,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "transport_attempts": transport_attempt,
            "retry_events": retry_events,
            "model": response.model,
            "finish_reason": response.choices[0].finish_reason,
        }
        if not response.model.startswith("gpt-5.5") or response.choices[0].finish_reason != "stop":
            response_record["status"] = "unexpected_or_incomplete_response_preserved"
            write_json_exclusive(case_dir / "response_record.json", response_record)
            return response_record
        try:
            proposed = json.loads(response.choices[0].message.content or "")
            write_json_exclusive(case_dir / "proposed_output.json", proposed)
            base = json.loads(Path(review_case["base_normalized_output_path"]).read_text())
            merged, edit_log = merge_proposal(base, proposed, review_case)
            write_json_exclusive(case_dir / "merged_before_finalizer.json", merged)
            write_json_exclusive(case_dir / "edit_log.json", edit_log)
            raw_record = json.loads(Path(review_case["base_raw_record_path"]).read_text())
            raw_input = json.loads(raw_record["raw_input_json"])
            normalized, normalization_log = finalize_output(
                merged, raw_input=raw_input, registry=registry)
            write_json_exclusive(case_dir / "normalized_output.json", normalized)
            write_json_exclusive(case_dir / "normalization_log.json", normalization_log)
            merged_validation = validate_output(merged, raw_input, schema, registry)
            normalized_validation = validate_output(normalized, raw_input, schema, registry)
            validation = {
                "version": "v4.1-bounded-repair-validation-v1",
                "case_id": case_id,
                "request_sha256": request_doc["request_sha256"],
                "base_raw_record_path": review_case["base_raw_record_path"],
                "base_raw_record_sha256": review_case["base_raw_sha256"],
                "proposed_output_path": str(case_dir / "proposed_output.json"),
                "proposed_output_file_sha256": file_sha(case_dir / "proposed_output.json"),
                "proposed_output_semantic_sha256": semantic_sha256(proposed),
                "merged_before_finalizer_path": str(case_dir / "merged_before_finalizer.json"),
                "merged_before_finalizer_file_sha256": file_sha(case_dir / "merged_before_finalizer.json"),
                "merged_before_finalizer_semantic_sha256": semantic_sha256(merged),
                "normalized_output_path": str(case_dir / "normalized_output.json"),
                "normalized_output_file_sha256": file_sha(case_dir / "normalized_output.json"),
                "normalized_output_semantic_sha256": semantic_sha256(normalized),
                "merged_validation": merged_validation,
                "normalized_validation": normalized_validation,
            }
            write_json_exclusive(case_dir / "validation.json", validation)
            response_record.update({
                "status": ("normalized_validator_passed_pending_human_review"
                           if normalized_validation["passed"]
                           else "normalized_validator_rejected"),
                "proposed_output_sha256": file_sha(case_dir / "proposed_output.json"),
                "merged_before_finalizer_sha256": file_sha(case_dir / "merged_before_finalizer.json"),
                "normalized_output_sha256": file_sha(case_dir / "normalized_output.json"),
                "validation_sha256": file_sha(case_dir / "validation.json"),
                "edit_log_sha256": file_sha(case_dir / "edit_log.json"),
                "normalized_error_count": normalized_validation["error_count"],
                "normalized_warning_count": normalized_validation["warning_count"],
            })
            write_json_exclusive(case_dir / "response_record.json", response_record)
            return response_record
        except Exception as exc:
            processing_failure = {
                "version": "v4.1-bounded-repair-processing-failure-v1",
                "case_id": case_id,
                "request_sha256": request_doc["request_sha256"],
                "provider_response_path": str(provider_path),
                "provider_response_sha256": file_sha(provider_path),
                "failure": {"type": type(exc).__name__, "detail": str(exc)[:4000]},
            }
            write_json_exclusive(case_dir / "processing_failure.json", processing_failure)
            response_record["status"] = "response_preserved_processing_failed"
            response_record["processing_failure"] = processing_failure["failure"]
            write_json_exclusive(case_dir / "response_record.json", response_record)
            return response_record
    raise AssertionError("unreachable")


def build_accounting(results: list[dict[str, Any]], queue: dict[str, Any]) -> dict[str, Any]:
    by_case = {result["case_id"]: result for result in results}
    cases = []
    for case_id, review_case in queue["cases"].items():
        result = by_case[case_id]
        base_validation_path = HERE / "validation" / f"{case_id}.json"
        base_validation = json.loads(base_validation_path.read_text())
        case_dir = PASS_ROOT / case_id
        row = {
            "case_id": case_id,
            "status": result["status"],
            "base": {
                "raw_record_path": review_case["base_raw_record_path"],
                "raw_record_sha256": review_case["base_raw_sha256"],
                "normalized_output_path": review_case["base_normalized_output_path"],
                "normalized_output_file_sha256": file_sha(Path(review_case["base_normalized_output_path"])),
                "validation_path": str(base_validation_path),
                "validation_file_sha256": file_sha(base_validation_path),
                "normalized_validation_passed": base_validation["normalized_validation"]["passed"],
                "normalized_error_count": base_validation["normalized_validation"]["error_count"],
                "normalized_errors": base_validation["normalized_validation"]["errors"],
            },
            "correction": {
                "request_path": str(case_dir / "request.json"),
                "request_file_sha256": file_sha(case_dir / "request.json"),
                "request_sha256": json.loads((case_dir / "request.json").read_text())["request_sha256"],
                "response_record_path": str(case_dir / "response_record.json") if (case_dir / "response_record.json").exists() else None,
                "response_record_file_sha256": file_sha(case_dir / "response_record.json") if (case_dir / "response_record.json").exists() else None,
                "transport_attempts": result.get("transport_attempts"),
                "retry_events": result.get("retry_events", []),
                "model": result.get("model"),
                "finish_reason": result.get("finish_reason"),
            },
        }
        validation_path = case_dir / "validation.json"
        if validation_path.exists():
            validation = json.loads(validation_path.read_text())
            normalized_validation = validation["normalized_validation"]
            edit_log = json.loads((case_dir / "edit_log.json").read_text())
            row["correction"].update({
                "provider_response_path": result["provider_response_path"],
                "provider_response_sha256": result["provider_response_sha256"],
                "proposed_output_path": validation["proposed_output_path"],
                "proposed_output_file_sha256": validation["proposed_output_file_sha256"],
                "merged_before_finalizer_path": validation["merged_before_finalizer_path"],
                "merged_before_finalizer_file_sha256": validation["merged_before_finalizer_file_sha256"],
                "normalized_output_path": validation["normalized_output_path"],
                "normalized_output_file_sha256": validation["normalized_output_file_sha256"],
                "validation_path": str(validation_path),
                "validation_file_sha256": file_sha(validation_path),
                "normalized_validation_passed": normalized_validation["passed"],
                "normalized_error_count": normalized_validation["error_count"],
                "normalized_errors": normalized_validation["errors"],
                "normalized_warning_count": normalized_validation["warning_count"],
                "normalized_warnings": normalized_validation["warnings"],
                "accepted_field_change_count": edit_log["accepted_field_change_count"],
                "discarded_unauthorized_change_count": edit_log["discarded_unauthorized_change_count"],
            })
        cases.append(row)
    return {
        "version": "v4.1-bounded-repair-accounting-v1",
        "status": "complete",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "requested_cases": len(queue["cases"]),
            "successful_completion_responses": sum(
                result.get("finish_reason") == "stop" for result in results),
            "semantic_retries": 0,
            "transport_attempts": sum(result.get("transport_attempts", 0) for result in results),
            "transport_retries": sum(len(result.get("retry_events", [])) for result in results),
        },
        "provenance": {
            "system_prompt_path": str(SYSTEM_PATH),
            "system_prompt_sha256": file_sha(SYSTEM_PATH),
            "repair_instruction_path": str(INSTRUCTION_PATH),
            "repair_instruction_sha256": file_sha(INSTRUCTION_PATH),
            "repair_queue_path": str(QUEUE_PATH),
            "repair_queue_sha256": file_sha(QUEUE_PATH),
            "output_schema_path": str(SCHEMA_PATH),
            "output_schema_sha256": file_sha(SCHEMA_PATH),
        },
        "counts": {
            "normalized_validator_passed": sum(
                result["status"] == "normalized_validator_passed_pending_human_review"
                for result in results),
            "normalized_validator_rejected": sum(
                result["status"] == "normalized_validator_rejected" for result in results),
            "processing_or_transport_failures": sum(
                result["status"] not in {
                    "normalized_validator_passed_pending_human_review",
                    "normalized_validator_rejected",
                } for result in results),
        },
        "cases": cases,
    }


def main() -> None:
    if PASS_ROOT.exists():
        raise SystemExit(f"refusing to reuse repair pass directory: {PASS_ROOT}")
    queue = json.loads(QUEUE_PATH.read_text())
    if len(queue.get("cases", {})) != 4:
        raise SystemExit("repair queue must contain exactly four cases")
    system = SYSTEM_PATH.read_text()
    repair_instruction = INSTRUCTION_PATH.read_text()
    schema = json.loads(SCHEMA_PATH.read_text())
    registry = load_registry(REGISTRY_PATH)
    client, auth_mode = client_and_auth_mode()
    PASS_ROOT.mkdir(parents=True, exist_ok=False)
    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {
            pool.submit(run_case, case_id, review_case, client, auth_mode, system,
                        repair_instruction, schema, registry, 100): case_id
            for case_id, review_case in queue["cases"].items()
        }
        for future in as_completed(futures):
            case_id = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                result = {
                    "case_id": case_id,
                    "status": "unhandled_runner_failure",
                    "failure": {"type": type(exc).__name__, "detail": str(exc)[:4000]},
                }
                write_json_exclusive(PASS_ROOT / case_id / "unhandled_runner_failure.json", result)
            results.append(result)
            print(json.dumps({"completed": case_id, "status": result["status"]}), flush=True)
    accounting = build_accounting(results, queue)
    write_json_exclusive(PASS_ROOT / "accounting.json", accounting)
    print(json.dumps(accounting["counts"], indent=2), flush=True)
    raise SystemExit(0 if accounting["counts"]["processing_or_transport_failures"] == 0 else 2)


if __name__ == "__main__":
    main()
