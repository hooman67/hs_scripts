#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml", "tomli", "jsonschema"]
# ///
"""Run the bounded V5 dual-source GPT-5.5 text pilot.

Importing this module never calls the provider.  A case gets one semantic
response only; retries are limited to pre-response transient transport errors.
Successful provider payloads and attempt records are exclusive-write artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VERSION = ROOT / "research/source_messaging_v1_to_v6/versions/v5"
VERSION_SCRIPTS = VERSION / "scripts"
sys.path.insert(0, str(ROOT / "research/source_messaging_v1_to_v6/scripts"))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(VERSION_SCRIPTS))

from probe_gpt55 import client_and_auth_mode  # noqa: E402
from camera_profile_resolver import load_registry  # noqa: E402
from finalize_output import finalize_output, semantic_sha256  # noqa: E402
from record_integrity import (  # noqa: E402
    allocate_and_write_attempt,
    distinct_request_hashes,
    newest_matching_attempt,
    write_json_exclusive,
)
from validate_output import validate_output  # noqa: E402


_SHARED_RUNNER_PATH = ROOT / "research/source_messaging_v1_to_v6/scripts/run_gpt55.py"
_spec = importlib.util.spec_from_file_location("shared_gpt55_runner", _SHARED_RUNNER_PATH)
_shared = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_shared)
checkpoint, retry_delay, transient = _shared.checkpoint, _shared.retry_delay, _shared.transient


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(
        json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    )


def settings_from_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    model = manifest["model"]
    return {
        "model": model["deployment"],
        "reasoning_effort": model["reasoning_effort"],
        "max_completion_tokens": model["max_completion_tokens"],
    }


def request_sha256(
    case: dict[str, Any], manifest: dict[str, Any], schema: dict[str, Any]
) -> str:
    return sha_obj(
        {
            "system_sha256": manifest["provenance"]["system_prompt"]["sha256"],
            "input_schema_sha256": manifest["provenance"]["input_schema"]["sha256"],
            "output_schema": schema,
            "settings": settings_from_manifest(manifest),
            "input_sha256": case["input_sha256"],
        }
    )


def derive_artifacts(
    case: dict[str, Any],
    target: Path,
    record: dict[str, Any],
    raw_input: dict[str, Any],
    schema: dict[str, Any],
    registry: dict[str, Any],
    request_hash: str,
) -> dict[str, Any]:
    """Build reproducible sidecars without changing immutable raw bytes."""
    case_id = case["case_id"]
    parsed = record["parsed_output"]
    raw_record_sha256 = sha_bytes(target.read_bytes())
    sample_name = target.stem
    raw_validation = validate_output(parsed, raw_input, schema, registry)
    normalized, normalization_log = finalize_output(parsed, raw_input=raw_input, registry=registry)
    normalized_validation = validate_output(normalized, raw_input, schema, registry)
    artifact_stem = f"{case_id}__{sample_name}"
    normalized_path = HERE / "normalized_outputs" / f"{artifact_stem}.json"
    log_path = HERE / "normalization_logs" / f"{artifact_stem}.json"
    raw_validation_path = HERE / "validation/raw" / f"{artifact_stem}.json"
    normalized_validation_path = HERE / "validation/normalized" / f"{artifact_stem}.json"
    for path, value in (
        (normalized_path, normalized),
        (log_path, normalization_log),
        (raw_validation_path, raw_validation),
        (normalized_validation_path, normalized_validation),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        checkpoint(path, value)
    audit = {
        "version": "v5-raw-normalized-audit-v1",
        "case_id": case_id,
        "request_sha256": request_hash,
        "record_path": str(target),
        "raw_record_sha256": raw_record_sha256,
        "raw_validation": raw_validation,
        "normalized_validation": normalized_validation,
        "normalized_output_path": str(normalized_path),
        "normalized_output_file_sha256": sha_bytes(normalized_path.read_bytes()),
        "normalized_output_semantic_sha256": semantic_sha256(normalized),
        "normalization_log_path": str(log_path),
        "normalization_log_file_sha256": sha_bytes(log_path.read_bytes()),
        "human_review_status": "pending",
        "launchable": False,
    }
    checkpoint(HERE / "validation" / f"{case_id}.json", audit)
    status = (
        "normalized_validator_passed_pending_human_review"
        if normalized_validation["passed"]
        else "normalized_validator_rejected"
    )
    return {
        "status": status,
        "elapsed_seconds": record.get("elapsed_seconds"),
        "record_path": str(target),
        "raw_record_sha256": raw_record_sha256,
        "human_review_status": "pending",
        "launchable": False,
    }


def run_case(
    case: dict[str, Any],
    manifest: dict[str, Any],
    client: Any,
    auth_mode: str,
    system: str,
    schema: dict[str, Any],
    registry: dict[str, Any],
    max_transport_attempts: int,
    new_request_revision: bool,
) -> tuple[str, dict[str, Any]]:
    case_id = case["case_id"]
    input_path = Path(case["input_path"])
    raw_input_bytes = input_path.read_bytes()
    if sha_bytes(raw_input_bytes) != case["input_sha256"]:
        raise RuntimeError(f"input hash changed: {case_id}")
    raw_input = json.loads(raw_input_bytes)
    if set(raw_input) != {"smart_brief", "source_messaging", "camera_tag"}:
        raise RuntimeError(f"runtime input contract changed: {case_id}")
    settings = settings_from_manifest(manifest)
    request_hash = request_sha256(case, manifest, schema)
    attempt_dir = HERE / "records/attempts" / case_id
    attempt_dir.mkdir(parents=True, exist_ok=True)

    # Any terminal record for this exact request consumes the case's one semantic
    # attempt.  A failure is never converted into an opportunistic second call.
    newest = newest_matching_attempt(attempt_dir, request_hash)
    if newest is not None:
        prior_path, prior = newest
        if prior.get("parsed_output") is not None:
            return case_id, derive_artifacts(
                case, prior_path, prior, raw_input, schema, registry, request_hash
            )
        return case_id, prior

    prior_request_hashes = distinct_request_hashes(attempt_dir)
    if prior_request_hashes and not new_request_revision:
        raise RuntimeError(
            f"{case_id} has a preserved earlier request revision; "
            "pass --new-request-revision to authorize exactly one response for the new request hash"
        )

    run_id = uuid.uuid4().hex
    record: dict[str, Any] = {
        "version": "v5-gpt55-attempt-v1",
        "case_id": case_id,
        "group_id": case["group_id"],
        "pair_id": case["pair_id"],
        "semantic_attempt": 1,
        "request_revision_number": len(prior_request_hashes) + 1,
        "prior_request_sha256s": prior_request_hashes,
        "new_request_revision_authorized": bool(prior_request_hashes and new_request_revision),
        "run_id": run_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "request_sha256": request_hash,
        "input_path": str(input_path),
        "input_sha256": case["input_sha256"],
        "input_semantic_sha256": case["input_semantic_sha256"],
        "raw_input_json": raw_input_bytes.decode("utf-8"),
        "system_prompt_path": manifest["provenance"]["system_prompt"]["path"],
        "system_prompt_sha256": manifest["provenance"]["system_prompt"]["sha256"],
        "input_schema_path": manifest["provenance"]["input_schema"]["path"],
        "input_schema_sha256": manifest["provenance"]["input_schema"]["sha256"],
        "output_schema_path": manifest["provenance"]["output_schema"]["path"],
        "output_schema_sha256": manifest["provenance"]["output_schema"]["sha256"],
        "settings": settings,
        "auth_mode": auth_mode,
        "retry_events": [],
        "human_review_status": "pending",
        "launchable": False,
    }
    started = time.monotonic()
    for transport_attempt in range(1, max_transport_attempts + 1):
        try:
            response = client.chat.completions.create(
                **settings,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": raw_input_bytes.decode("utf-8")},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "hp_lifestyle_dual_source_v5",
                        "strict": True,
                        "schema": schema,
                    },
                },
            )
            response_payload = response.model_dump(mode="json")
            provider_record = {
                "version": "v5-gpt55-provider-response-v1",
                "run_id": run_id,
                "case_id": case_id,
                "request_sha256": request_hash,
                "received_at": datetime.now(timezone.utc).isoformat(),
                "response": response_payload,
            }
            provider_path = HERE / "records/provider_responses" / case_id / f"{run_id}.json"
            write_json_exclusive(provider_path, provider_record)
            record["provider_response_path"] = str(provider_path)
            record["provider_response_sha256"] = sha_bytes(provider_path.read_bytes())
            record["response"] = response_payload
            record["completed_at"] = datetime.now(timezone.utc).isoformat()
            record["elapsed_seconds"] = round(time.monotonic() - started, 3)
            record["transport_attempts"] = transport_attempt
            if not response.model.startswith("gpt-5.5") or response.choices[0].finish_reason != "stop":
                raise RuntimeError("unexpected model or incomplete successful response")
            parsed = json.loads(response.choices[0].message.content or "")
            record["parsed_output"] = parsed
            record["parsed_output_sha256"] = sha_obj(parsed)
            record["status"] = "raw_response_preserved_pending_derived_audit"
        except Exception as exc:
            if record.get("response") or not transient(exc) or transport_attempt == max_transport_attempts:
                record["status"] = "failed_preserved"
                record["failure"] = {
                    "type": type(exc).__name__,
                    "status_code": getattr(exc, "status_code", None),
                    "transport_attempt": transport_attempt,
                    "detail": str(exc)[:1200],
                }
                record["elapsed_seconds"] = round(time.monotonic() - started, 3)
                allocate_and_write_attempt(attempt_dir, record)
                return case_id, record
            delay = retry_delay(exc, transport_attempt)
            record["retry_events"].append(
                {
                    "transport_attempt": transport_attempt,
                    "type": type(exc).__name__,
                    "status_code": getattr(exc, "status_code", None),
                    "wait_seconds": delay,
                }
            )
            retry_path = (
                HERE
                / "records/transport_retries"
                / case_id
                / f"{run_id}__transport_{transport_attempt:03d}.json"
            )
            write_json_exclusive(retry_path, record)
            time.sleep(delay)
        else:
            target = allocate_and_write_attempt(attempt_dir, record)
            return case_id, derive_artifacts(
                case, target, record, raw_input, schema, registry, request_hash
            )
    raise AssertionError("unreachable")


def rebuild_accepted(manifest: dict[str, Any]) -> dict[str, Any]:
    schema = json.loads((VERSION / "output.schema.json").read_text(encoding="utf-8"))
    registry = load_registry(VERSION / "camera_profiles.json")
    accepted_cases: dict[str, Any] = {}
    statuses: dict[str, Any] = {}
    status_counts: dict[str, int] = {}

    for case in manifest["cases"]:
        case_id = case["case_id"]
        raw_input = json.loads(Path(case["input_path"]).read_text(encoding="utf-8"))
        expected_request = request_sha256(case, manifest, schema)
        newest = newest_matching_attempt(HERE / "records/attempts" / case_id, expected_request)
        status = "pending"
        if newest is not None:
            record_path, record = newest
            record_hash = sha_bytes(record_path.read_bytes())
            audit_path = HERE / "validation" / f"{case_id}.json"
            audit = json.loads(audit_path.read_text(encoding="utf-8")) if audit_path.exists() else {}
            eligible = bool(
                record.get("parsed_output") is not None
                and record.get("input_sha256") == case["input_sha256"]
                and record.get("system_prompt_sha256")
                == manifest["provenance"]["system_prompt"]["sha256"]
                and record.get("input_schema_sha256")
                == manifest["provenance"]["input_schema"]["sha256"]
                and record.get("output_schema_sha256")
                == manifest["provenance"]["output_schema"]["sha256"]
                and record.get("parsed_output_sha256") == sha_obj(record["parsed_output"])
                and audit.get("record_path") == str(record_path)
                and audit.get("raw_record_sha256") == record_hash
            )
            if eligible:
                normalized_path = Path(audit["normalized_output_path"])
                log_path = Path(audit["normalization_log_path"])
                eligible = normalized_path.exists() and log_path.exists()
            if eligible:
                output = json.loads(normalized_path.read_text(encoding="utf-8"))
                log = json.loads(log_path.read_text(encoding="utf-8"))
                rebuilt, rebuilt_log = finalize_output(
                    record["parsed_output"], raw_input=raw_input, registry=registry
                )
                current_validation = validate_output(output, raw_input, schema, registry)
                eligible = bool(
                    output == rebuilt
                    and log == rebuilt_log
                    and audit.get("normalized_output_file_sha256")
                    == sha_bytes(normalized_path.read_bytes())
                    and audit.get("normalization_log_file_sha256") == sha_bytes(log_path.read_bytes())
                    and audit.get("normalized_output_semantic_sha256") == semantic_sha256(output)
                    and current_validation["passed"]
                    and len(output.get("prompts", [])) == 20
                )
            if eligible:
                status = "normalized_validator_passed_pending_human_review"
                candidates = []
                for rank, candidate in enumerate(output["prompts"], 1):
                    candidates.append(
                        {
                            "candidate_key": f"{case_id}::{candidate['id']}",
                            "rank": rank,
                            "text_sha256": sha_bytes(candidate["text"].encode("utf-8")),
                            **candidate,
                        }
                    )
                accepted_cases[case_id] = {
                    **{key: case[key] for key in (
                        "case_id", "group_id", "pair_id", "device_type", "camera_tag",
                        "view_role", "product_identity_conflict", "input_path", "input_sha256"
                    )},
                    "record_path": str(record_path),
                    "record_sha256": record_hash,
                    "raw_parsed_output_sha256": record["parsed_output_sha256"],
                    "normalized_output_path": str(normalized_path),
                    "normalized_output_file_sha256": sha_bytes(normalized_path.read_bytes()),
                    "normalized_output_semantic_sha256": semantic_sha256(output),
                    "normalization_log_path": str(log_path),
                    "normalization_log_file_sha256": sha_bytes(log_path.read_bytes()),
                    "validation_audit_path": str(audit_path),
                    "raw_record_status": record.get("status"),
                    "status": status,
                    "human_review_status": "pending",
                    "launchable": False,
                    "candidates": candidates,
                    "debug": output["debug"],
                }
            elif (
                audit.get("record_path") == str(record_path)
                and audit.get("raw_record_sha256") == record_hash
                and audit.get("normalized_validation", {}).get("passed") is False
            ):
                status = "normalized_validator_rejected"
            else:
                status = record.get("status", "pending_derived_audit")

        status_counts[status] = status_counts.get(status, 0) + 1
        statuses[case_id] = {
            "case_id": case_id,
            "group_id": case["group_id"],
            "pair_id": case["pair_id"],
            "camera_tag": case["camera_tag"],
            "view_role": case["view_role"],
            "status": status,
            "human_review_status": "pending",
            "launchable": False,
        }

    accepted = {
        "version": "v5-pilot-accepted-prompt-cases-v1-normalized",
        "status": "human_review_required",
        "manifest_path": str(HERE / "manifest.json"),
        "manifest_sha256": sha_bytes((HERE / "manifest.json").read_bytes()),
        "selection_status": "not_yet_performed",
        "human_review_status": "pending",
        "launchable": False,
        "counts": {
            "manifest_cases": len(manifest["cases"]),
            "accepted_cases": len(accepted_cases),
            "status_counts": status_counts,
            "candidates": sum(len(case["candidates"]) for case in accepted_cases.values()),
        },
        "cases": accepted_cases,
    }
    checkpoint(HERE / "accepted_prompt_cases.json", accepted)
    checkpoint(
        HERE / "status_inventory.json",
        {
            "version": "v5-pilot-status-inventory-v1",
            "manifest_sha256": sha_bytes((HERE / "manifest.json").read_bytes()),
            "human_review_status": "pending",
            "launchable": False,
            "counts": {"total": len(manifest["cases"]), **status_counts},
            "cases": statuses,
        },
    )
    return accepted


def verify_frozen_provenance(manifest: dict[str, Any]) -> None:
    for key, item in manifest["provenance"].items():
        path = Path(item["path"])
        if not path.is_file() or sha_bytes(path.read_bytes()) != item["sha256"]:
            raise SystemExit(f"provenance changed: {key}; rebuild inputs before any call")
    for case in manifest["cases"]:
        path = Path(case["input_path"])
        if not path.is_file() or sha_bytes(path.read_bytes()) != case["input_sha256"]:
            raise SystemExit(f"input changed: {case['case_id']}; rebuild inputs before any call")


def verify_request_revision_authorization(
    requested: set[str],
    cases_by_id: dict[str, dict[str, Any]],
    manifest: dict[str, Any],
    schema: dict[str, Any],
    new_request_revision: bool,
) -> None:
    """Refuse changed-hash calls before client/auth setup unless explicitly gated."""
    blocked: dict[str, list[str]] = {}
    for case_id in sorted(requested):
        case = cases_by_id[case_id]
        current_hash = request_sha256(case, manifest, schema)
        attempt_dir = HERE / "records/attempts" / case_id
        if newest_matching_attempt(attempt_dir, current_hash) is not None:
            continue
        prior_hashes = distinct_request_hashes(attempt_dir)
        if prior_hashes and not new_request_revision:
            blocked[case_id] = prior_hashes
    if blocked:
        details = ", ".join(
            f"{case_id} ({len(hashes)} preserved prior request hash(es))"
            for case_id, hashes in blocked.items()
        )
        raise SystemExit(
            "changed request revision requires --new-request-revision; no calls made: " + details
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append")
    parser.add_argument("--all-authorized", action="store_true")
    parser.add_argument(
        "--new-request-revision",
        action="store_true",
        help=(
            "Authorize one semantic response for a new exact request hash when the case already "
            "has an immutable attempt for an earlier request revision"
        ),
    )
    parser.add_argument("--rebuild-only", action="store_true")
    parser.add_argument("--maxconcurrency", "--max-concurrency", dest="maxconcurrency", type=int, default=2)
    parser.add_argument("--max-transport-attempts", type=int, default=100)
    args = parser.parse_args()
    if not 1 <= args.maxconcurrency <= 2:
        parser.error("--maxconcurrency must be 1 or 2")
    if not 1 <= args.max_transport_attempts <= 100:
        parser.error("--max-transport-attempts must be between 1 and 100")

    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    verify_frozen_provenance(manifest)
    if args.rebuild_only:
        print(json.dumps(rebuild_accepted(manifest)["counts"], indent=2))
        return

    allowed = set(manifest["authorized_text_case_ids"])
    requested = allowed if args.all_authorized else set(args.case or [])
    if not requested:
        parser.error("--case or --all-authorized is required unless --rebuild-only is used")
    if not requested <= allowed:
        raise SystemExit(f"only authorized text cases may run; rejected: {sorted(requested - allowed)}")

    cases_by_id = {case["case_id"]: case for case in manifest["cases"]}
    system = (VERSION / "system_prompt.md").read_text(encoding="utf-8")
    schema = json.loads((VERSION / "output.schema.json").read_text(encoding="utf-8"))
    registry = load_registry(VERSION / "camera_profiles.json")
    verify_request_revision_authorization(
        requested, cases_by_id, manifest, schema, args.new_request_revision
    )
    client, auth_mode = client_and_auth_mode()
    results = []
    with ThreadPoolExecutor(max_workers=args.maxconcurrency) as pool:
        futures = {
            pool.submit(
                run_case,
                cases_by_id[case_id],
                manifest,
                client,
                auth_mode,
                system,
                schema,
                registry,
                args.max_transport_attempts,
                args.new_request_revision,
            ): case_id
            for case_id in sorted(requested)
        }
        for future in as_completed(futures):
            case_id, result = future.result()
            results.append(
                {
                    "case_id": case_id,
                    "status": result.get("status"),
                    "elapsed_seconds": result.get("elapsed_seconds"),
                    "human_review_status": "pending",
                    "launchable": False,
                }
            )
            accepted = rebuild_accepted(manifest)
            print(
                json.dumps(
                    {
                        "completed": results[-1],
                        "accepted_count": accepted["counts"]["accepted_cases"],
                    }
                ),
                flush=True,
            )
    passed = all(
        result["status"] == "normalized_validator_passed_pending_human_review"
        for result in results
    )
    raise SystemExit(0 if passed else 2)


if __name__ == "__main__":
    main()
