#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml", "tomli", "jsonschema"]
# ///
"""Run exactly two isolated GPT-5.5 scoring-contract smoke cases."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import time
import uuid
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PILOT = HERE.parent
ROOT = HERE.parents[2]
VERSION = ROOT / "research/source_messaging_v1_to_v6/versions/v5"
VERSION_SCRIPTS = VERSION / "scripts"
sys.path.insert(0, str(ROOT / "research/source_messaging_v1_to_v6/scripts"))
sys.path.insert(0, str(VERSION_SCRIPTS))
sys.path.insert(0, str(PILOT))

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


_shared_path = ROOT / "research/source_messaging_v1_to_v6/scripts/run_gpt55.py"
_spec = importlib.util.spec_from_file_location("shared_gpt55_runner", _shared_path)
_shared = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_shared)
checkpoint, retry_delay, transient = _shared.checkpoint, _shared.retry_delay, _shared.transient

DOCUMENTS = ("smart_brief", "source_messaging")
COMPONENTS = ("setting", "activity", "materials", "use_context")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    )


def settings(manifest: dict[str, Any]) -> dict[str, Any]:
    model = manifest["model"]
    return {
        "model": model["deployment"],
        "reasoning_effort": model["reasoning_effort"],
        "max_completion_tokens": model["max_completion_tokens"],
    }


def request_hash(case: dict[str, Any], manifest: dict[str, Any], schema: dict[str, Any]) -> str:
    return sha_obj(
        {
            "system_prompt_sha256": manifest["provenance"]["system_prompt"]["sha256"],
            "output_schema": schema,
            "settings": settings(manifest),
            "input_sha256": case["input_sha256"],
        }
    )


def derive(
    case: dict[str, Any],
    attempt_path: Path,
    record: dict[str, Any],
    raw_input: dict[str, Any],
    schema: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    case_id = case["case_id"]
    parsed = record["parsed_output"]
    raw_validation = validate_output(parsed, raw_input, schema, registry)
    normalized, log = finalize_output(parsed, raw_input=raw_input, registry=registry)
    normalized_validation = validate_output(normalized, raw_input, schema, registry)
    paths = {
        "normalized_output": HERE / "normalized_outputs" / f"{case_id}.json",
        "normalization_log": HERE / "normalization_logs" / f"{case_id}.json",
        "raw_validation": HERE / "validation/raw" / f"{case_id}.json",
        "normalized_validation": HERE / "validation/normalized" / f"{case_id}.json",
    }
    for key, value in (
        ("normalized_output", normalized),
        ("normalization_log", log),
        ("raw_validation", raw_validation),
        ("normalized_validation", normalized_validation),
    ):
        paths[key].parent.mkdir(parents=True, exist_ok=True)
        checkpoint(paths[key], value)
    audit = {
        "version": "v5-scoring-contract-smoke-audit-v1",
        "case_id": case_id,
        "request_sha256": record["request_sha256"],
        "attempt_path": str(attempt_path),
        "attempt_sha256": sha_bytes(attempt_path.read_bytes()),
        "raw_validation": raw_validation,
        "normalized_validation": normalized_validation,
        "normalized_output_path": str(paths["normalized_output"]),
        "normalized_output_file_sha256": sha_bytes(paths["normalized_output"].read_bytes()),
        "normalized_output_semantic_sha256": semantic_sha256(normalized),
        "normalization_log_path": str(paths["normalization_log"]),
        "normalization_log_file_sha256": sha_bytes(paths["normalization_log"].read_bytes()),
        "human_review_status": "pending",
        "launchable": False,
    }
    checkpoint(HERE / "validation" / f"{case_id}.json", audit)
    return {
        "status": (
            "normalized_validator_passed_pending_human_review"
            if normalized_validation["passed"]
            else "normalized_validator_rejected"
        ),
        "elapsed_seconds": record.get("elapsed_seconds"),
        "attempt_path": str(attempt_path),
        "attempt_sha256": audit["attempt_sha256"],
    }


def run_case(
    case: dict[str, Any],
    manifest: dict[str, Any],
    client: Any,
    auth_mode: str,
    system: str,
    schema: dict[str, Any],
    registry: dict[str, Any],
) -> tuple[str, dict[str, Any]]:
    case_id = case["case_id"]
    input_path = Path(case["input_path"])
    input_bytes = input_path.read_bytes()
    if sha_bytes(input_bytes) != case["input_sha256"]:
        raise RuntimeError(f"input changed: {case_id}")
    raw_input = json.loads(input_bytes)
    current_request = request_hash(case, manifest, schema)
    attempt_dir = HERE / "records/attempts" / case_id
    prior = newest_matching_attempt(attempt_dir, current_request)
    if prior is not None:
        prior_path, prior_record = prior
        if prior_record.get("parsed_output") is not None:
            return case_id, derive(case, prior_path, prior_record, raw_input, schema, registry)
        return case_id, prior_record
    if distinct_request_hashes(attempt_dir):
        raise RuntimeError(f"semantic attempt already exists under a different request: {case_id}")

    run_id = uuid.uuid4().hex
    request_settings = settings(manifest)
    record: dict[str, Any] = {
        "version": "v5-scoring-contract-smoke-attempt-v1",
        "case_id": case_id,
        "semantic_attempt": 1,
        "run_id": run_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "request_sha256": current_request,
        "input_path": str(input_path),
        "input_sha256": case["input_sha256"],
        "input_semantic_sha256": case["input_semantic_sha256"],
        "raw_input_json": input_bytes.decode("utf-8"),
        "empty_document": case["empty_document"],
        "nonempty_document": case["nonempty_document"],
        "system_prompt_path": manifest["provenance"]["system_prompt"]["path"],
        "system_prompt_sha256": manifest["provenance"]["system_prompt"]["sha256"],
        "input_schema_sha256": manifest["provenance"]["input_schema"]["sha256"],
        "output_schema_sha256": manifest["provenance"]["output_schema"]["sha256"],
        "finalizer_sha256": manifest["provenance"]["finalizer"]["sha256"],
        "validator_sha256": manifest["provenance"]["validator"]["sha256"],
        "settings": request_settings,
        "auth_mode": auth_mode,
        "retry_events": [],
        "human_review_status": "pending",
        "launchable": False,
    }
    started = time.monotonic()
    max_attempts = manifest["scope"]["max_transport_attempts"]
    for transport_attempt in range(1, max_attempts + 1):
        try:
            response = client.chat.completions.create(
                **request_settings,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": input_bytes.decode("utf-8")},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "hp_lifestyle_scoring_contract_smoke",
                        "strict": True,
                        "schema": schema,
                    },
                },
            )
            response_payload = response.model_dump(mode="json")
            provider = {
                "version": "v5-scoring-contract-smoke-provider-response-v1",
                "case_id": case_id,
                "run_id": run_id,
                "request_sha256": current_request,
                "received_at": datetime.now(timezone.utc).isoformat(),
                "response": response_payload,
            }
            provider_path = HERE / "records/provider_responses" / case_id / f"{run_id}.json"
            write_json_exclusive(provider_path, provider)
            record.update(
                {
                    "provider_response_path": str(provider_path),
                    "provider_response_sha256": sha_bytes(provider_path.read_bytes()),
                    "response": response_payload,
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "transport_attempts": transport_attempt,
                }
            )
            if not response.model.startswith("gpt-5.5") or response.choices[0].finish_reason != "stop":
                raise RuntimeError("unexpected model or incomplete response")
            parsed = json.loads(response.choices[0].message.content or "")
            record["parsed_output"] = parsed
            record["parsed_output_sha256"] = sha_obj(parsed)
            record["status"] = "raw_response_preserved_pending_derived_audit"
        except Exception as exc:
            if record.get("response") or not transient(exc) or transport_attempt == max_attempts:
                record["status"] = "failed_preserved"
                record["failure"] = {
                    "type": type(exc).__name__,
                    "status_code": getattr(exc, "status_code", None),
                    "transport_attempt": transport_attempt,
                    "detail": str(exc)[:1200],
                }
                record["elapsed_seconds"] = round(time.monotonic() - started, 3)
                attempt_path = allocate_and_write_attempt(attempt_dir, record)
                return case_id, {**record, "attempt_path": str(attempt_path)}
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
                HERE / "records/transport_retries" / case_id
                / f"{run_id}__transport_{transport_attempt:03d}.json"
            )
            write_json_exclusive(retry_path, record)
            time.sleep(delay)
        else:
            attempt_path = allocate_and_write_attempt(attempt_dir, record)
            return case_id, derive(case, attempt_path, record, raw_input, schema, registry)
    raise AssertionError("unreachable")


def build_contract_analysis(manifest: dict[str, Any]) -> dict[str, Any]:
    case_reports = {}
    for case in manifest["cases"]:
        case_id = case["case_id"]
        output_path = HERE / "normalized_outputs" / f"{case_id}.json"
        audit_path = HERE / "validation" / f"{case_id}.json"
        if not output_path.exists() or not audit_path.exists():
            continue
        output = json.loads(output_path.read_text(encoding="utf-8"))
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        empty = case["empty_document"]
        nonempty = case["nonempty_document"]
        empty_nonzero = []
        arithmetic_errors = []
        for candidate in output["prompts"]:
            if any(candidate["score_components"][empty][name] for name in COMPONENTS):
                empty_nonzero.append(candidate["id"])
            expected = sum(
                max(
                    candidate["score_components"]["smart_brief"][name],
                    candidate["score_components"]["source_messaging"][name],
                )
                for name in COMPONENTS
            )
            if candidate["source_relevance_score"] != expected:
                arithmetic_errors.append(
                    {"id": candidate["id"], "expected": expected, "actual": candidate["source_relevance_score"]}
                )
        evidence_counts = Counter(
            evidence["document"] for evidence in output["debug"]["source_evidence"]
        )
        top = output["prompts"][0]
        case_reports[case_id] = {
            "empty_document": empty,
            "nonempty_document": nonempty,
            "prompt_count": len(output["prompts"]),
            "normalized_validator_passed": audit["normalized_validation"]["passed"],
            "normalized_error_count": audit["normalized_validation"]["error_count"],
            "normalized_warning_count": audit["normalized_validation"]["warning_count"],
            "all_empty_document_components_zero": not empty_nonzero,
            "empty_document_nonzero_candidate_ids": empty_nonzero,
            "all_scores_match_component_max_sum": not arithmetic_errors,
            "arithmetic_errors": arithmetic_errors,
            "top_score": top["source_relevance_score"],
            "top_score_exceeds_50": top["source_relevance_score"] > 50,
            "top_candidate": {
                "id": top["id"],
                "environment": top["environment"],
                "text": top["text"],
                "score_components": top["score_components"],
                "evidence_ids": top["evidence_ids"],
            },
            "source_evidence_counts": {document: evidence_counts[document] for document in DOCUMENTS},
            "empty_document_evidence_count": evidence_counts[empty],
            "nonempty_document_evidence_count": evidence_counts[nonempty],
            "no_missing_document_penalty_observed": (
                not arithmetic_errors and not empty_nonzero and top["source_relevance_score"] > 50
            ),
        }
    report = {
        "version": "v5-scoring-contract-smoke-analysis-v1",
        "manifest_sha256": sha_bytes((HERE / "manifest.json").read_bytes()),
        "separate_from_main_review_set": True,
        "case_count": len(case_reports),
        "all_empty_document_components_zero": bool(case_reports) and all(
            item["all_empty_document_components_zero"] for item in case_reports.values()
        ),
        "all_scores_match_component_max_sum": bool(case_reports) and all(
            item["all_scores_match_component_max_sum"] for item in case_reports.values()
        ),
        "cases": case_reports,
    }
    checkpoint(HERE / "contract_analysis.json", report)
    return report


def rebuild(manifest: dict[str, Any]) -> dict[str, Any]:
    schema = json.loads((VERSION / "output.schema.json").read_text(encoding="utf-8"))
    statuses = {}
    counts: Counter[str] = Counter()
    for case in manifest["cases"]:
        case_id = case["case_id"]
        expected = request_hash(case, manifest, schema)
        prior = newest_matching_attempt(HERE / "records/attempts" / case_id, expected)
        status = "pending"
        if prior is not None:
            path, record = prior
            audit_path = HERE / "validation" / f"{case_id}.json"
            if audit_path.exists() and record.get("parsed_output") is not None:
                audit = json.loads(audit_path.read_text(encoding="utf-8"))
                status = (
                    "normalized_validator_passed_pending_human_review"
                    if audit["normalized_validation"]["passed"]
                    else "normalized_validator_rejected"
                )
            else:
                status = record.get("status", "pending_derived_audit")
        counts[status] += 1
        statuses[case_id] = {
            "case_id": case_id,
            "empty_document": case["empty_document"],
            "nonempty_document": case["nonempty_document"],
            "status": status,
            "human_review_status": "pending",
            "launchable": False,
        }
    inventory = {
        "version": "v5-scoring-contract-smoke-status-v1",
        "manifest_sha256": sha_bytes((HERE / "manifest.json").read_bytes()),
        "counts": {"total": len(manifest["cases"]), **dict(counts)},
        "cases": statuses,
        "human_review_status": "pending",
        "launchable": False,
    }
    checkpoint(HERE / "status_inventory.json", inventory)
    build_contract_analysis(manifest)
    return inventory


def verify_provenance(manifest: dict[str, Any]) -> None:
    for key, item in manifest["provenance"].items():
        path = Path(item["path"])
        if not path.is_file() or sha_bytes(path.read_bytes()) != item["sha256"]:
            raise SystemExit(f"provenance changed: {key}; no calls made")
    for case in manifest["cases"]:
        path = Path(case["input_path"])
        if not path.is_file() or sha_bytes(path.read_bytes()) != case["input_sha256"]:
            raise SystemExit(f"input changed: {case['case_id']}; no calls made")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-authorized", action="store_true")
    parser.add_argument("--rebuild-only", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    verify_provenance(manifest)
    if args.rebuild_only:
        print(json.dumps(rebuild(manifest), indent=2))
        return
    if not args.all_authorized:
        parser.error("--all-authorized is required")
    system = (VERSION / "system_prompt.md").read_text(encoding="utf-8")
    schema = json.loads((VERSION / "output.schema.json").read_text(encoding="utf-8"))
    registry = load_registry(VERSION / "camera_profiles.json")
    client, auth_mode = client_and_auth_mode()
    cases = {case["case_id"]: case for case in manifest["cases"]}
    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {
            pool.submit(
                run_case, case, manifest, client, auth_mode, system, schema, registry
            ): case_id
            for case_id, case in sorted(cases.items())
        }
        for future in as_completed(futures):
            case_id, result = future.result()
            results.append({"case_id": case_id, **result})
            inventory = rebuild(manifest)
            print(json.dumps({"completed": results[-1], "counts": inventory["counts"]}), flush=True)
    passed = all(result.get("status") == "normalized_validator_passed_pending_human_review" for result in results)
    raise SystemExit(0 if passed else 2)


if __name__ == "__main__":
    main()
