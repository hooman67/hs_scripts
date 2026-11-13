#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema"]
# ///
"""Verify an immutable accepted-sample selection and rebuild its derived artifacts.

This script never chooses or changes an accepted attempt.  The selection file is the
decision record; all selected and rejected response records are verified and audited
before the two derived accepted artifacts are reproduced.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from citation_path_guard import normalize_citation_paths
from validate_camera_eval import V2_ROOT, load_registry, validate_case


EVAL_ROOT = V2_ROOT / "eval/current"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def confined_file(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise RuntimeError(f"Record path escapes eval root: {relative}") from exc
    if not path.is_file():
        raise RuntimeError(f"Record does not exist: {relative}")
    return path


def audit_record(
    record: dict[str, Any],
    case: dict[str, Any],
    schema: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    identity_failures: list[str] = []
    if record.get("case_id") != case["case_id"]:
        identity_failures.append("Record case_id does not match manifest")
    if record.get("case") != case:
        identity_failures.append("Recorded case metadata does not match manifest")

    raw_result = validate_case(record, schema, registry)
    raw_failures = identity_failures + raw_result["failures"]
    guard = normalize_citation_paths(
        record["parsed_output"], record["request_input"]["source_messaging"]
    )
    normalized_record = copy.deepcopy(record)
    normalized_record["parsed_output"] = guard["validated_output"]
    validated_result = validate_case(normalized_record, schema, registry)
    guard_failures = [
        "Citation path guard failure at "
        f"{item['json_pointer']}: {item['reason']}"
        for item in guard["failures"]
    ]
    validated_failures = (
        identity_failures + validated_result["failures"] + guard_failures
    )
    return {
        "raw_failures": raw_failures,
        "validated_failures": validated_failures,
        "citation_repairs": guard["citation_repairs"],
        "validated_output": guard["validated_output"],
    }


def check_equal(label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        raise RuntimeError(f"{label} differs: {actual!r} != {expected!r}")


def record_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    count = len(records)
    latency = sum(float(record["latency_seconds"]) for record in records)
    prompt_tokens = sum(int(record["usage"]["prompt_tokens"]) for record in records)
    completion_tokens = sum(
        int(record["usage"]["completion_tokens"]) for record in records
    )
    total_tokens = sum(int(record["usage"]["total_tokens"]) for record in records)
    return {
        "successful_response_count": count,
        "latency_seconds_sum": round(latency, 3),
        "latency_seconds_mean": round(latency / count, 6),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "output_prompt_count": sum(
            len(record["parsed_output"]["prompts"]) for record in records
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--selection", type=Path, default=EVAL_ROOT / "accepted_samples.json"
    )
    parser.add_argument(
        "--accepted-outputs",
        type=Path,
        default=EVAL_ROOT / "accepted_validated_outputs.json",
    )
    parser.add_argument(
        "--validation-output",
        type=Path,
        default=EVAL_ROOT / "accepted_validation.json",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify derived files byte-for-byte without writing them.",
    )
    args = parser.parse_args()

    selection_path = args.selection.resolve()
    eval_root = selection_path.parent
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    manifest_path = confined_file(eval_root, selection["canonical_manifest_path"])
    check_equal(
        "Canonical manifest SHA-256",
        file_sha256(manifest_path),
        selection["canonical_manifest_sha256"],
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema_path = V2_ROOT / "output.schema.json"
    registry_path = V2_ROOT / "camera_profiles.json"
    system_path = V2_ROOT / "system_prompt.md"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    registry = load_registry(registry_path)
    actual_provenance = {
        "system_prompt_sha256": file_sha256(system_path),
        "input_schema_sha256": file_sha256(V2_ROOT / "input.schema.json"),
        "output_schema_sha256": file_sha256(schema_path),
        "camera_profiles_sha256": file_sha256(registry_path),
        "manifest_sha256": file_sha256(manifest_path),
    }
    check_equal(
        "Selection system prompt SHA-256",
        actual_provenance["system_prompt_sha256"],
        selection["system_prompt_sha256"],
    )

    manifest_cases = {case["case_id"]: case for case in manifest["cases"]}
    selected_outputs: dict[str, Any] = {}
    selected_records: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    seen_case_ids: set[str] = set()
    seen_record_paths: set[Path] = set()
    rejected_count = 0

    for item in selection["cases"]:
        case_id = item["case_id"]
        if case_id in seen_case_ids:
            raise RuntimeError(f"Duplicate selection case_id: {case_id}")
        seen_case_ids.add(case_id)
        if case_id not in manifest_cases:
            raise RuntimeError(f"Selection case is absent from manifest: {case_id}")
        case = manifest_cases[case_id]

        accepted_path = confined_file(eval_root, item["accepted_record_path"])
        if accepted_path in seen_record_paths:
            raise RuntimeError(f"Response record selected twice: {accepted_path}")
        seen_record_paths.add(accepted_path)
        check_equal(
            f"Accepted record hash for {case_id}",
            file_sha256(accepted_path),
            item["accepted_record_sha256"],
        )
        accepted_record = json.loads(accepted_path.read_text(encoding="utf-8"))
        for field, expected in actual_provenance.items():
            check_equal(
                f"Accepted record {case_id} {field}",
                accepted_record.get(field),
                expected,
            )
        check_equal(
            f"Embedded system prompt hash for {case_id}",
            sha256_bytes(accepted_record["system_prompt"].encode("utf-8")),
            selection["system_prompt_sha256"],
        )
        accepted_audit = audit_record(accepted_record, case, schema, registry)
        recorded_accepted_audit = item["accepted_automated_audit"]
        for field in ("raw_failures", "validated_failures", "citation_repairs"):
            check_equal(
                f"Accepted {field} for {case_id}",
                accepted_audit[field],
                recorded_accepted_audit[field],
            )
        if accepted_audit["raw_failures"] or accepted_audit["validated_failures"]:
            raise RuntimeError(f"Selected attempt no longer passes: {case_id}")
        selected_outputs[case_id] = accepted_audit["validated_output"]
        selected_records.append(accepted_record)
        all_records.append(accepted_record)

        for rejected in item["rejected_attempts"]:
            rejected_count += 1
            rejected_path = confined_file(eval_root, rejected["record_path"])
            if rejected_path in seen_record_paths:
                raise RuntimeError(f"Response record referenced twice: {rejected_path}")
            seen_record_paths.add(rejected_path)
            check_equal(
                f"Rejected record hash for {case_id}",
                file_sha256(rejected_path),
                rejected["record_sha256"],
            )
            rejected_record = json.loads(rejected_path.read_text(encoding="utf-8"))
            for field, expected in actual_provenance.items():
                check_equal(
                    f"Rejected record {case_id} {field}",
                    rejected_record.get(field),
                    expected,
                )
            rejected_audit = audit_record(rejected_record, case, schema, registry)
            for field in ("raw_failures", "validated_failures", "citation_repairs"):
                check_equal(
                    f"Rejected {field} for {case_id}",
                    rejected_audit[field],
                    rejected[field],
                )
            if not rejected.get("reason", {}).get("code"):
                raise RuntimeError(f"Rejected attempt lacks a decision reason: {case_id}")
            all_records.append(rejected_record)

    check_equal("Selection case IDs", seen_case_ids, set(manifest_cases))
    check_equal("Selection case_count", selection["case_count"], len(manifest_cases))
    check_equal(
        "Selection accepted_case_count",
        selection["accepted_case_count"],
        len(selected_records),
    )
    check_equal(
        "Selection successful_sample_attempt_count",
        selection["successful_sample_attempt_count"],
        len(all_records),
    )
    check_equal(
        "Selection rejected_successful_sample_count",
        selection["rejected_successful_sample_count"],
        rejected_count,
    )
    check_equal(
        "Selection API transport attempt count",
        selection["api_transport_attempt_count"],
        sum(int(record["attempt"]) for record in all_records),
    )
    check_equal(
        "Selection transient retry event count",
        selection["transient_retry_event_count"],
        sum(len(record.get("retry_events", [])) for record in all_records),
    )

    accepted_outputs = {
        "version": "accepted-validated-outputs-v1",
        "case_count": len(selected_outputs),
        "outputs": selected_outputs,
    }
    validation = {
        "version": "accepted-sample-validation-v1",
        "case_count": len(selected_records),
        "raw_record_count": len(selected_records),
        "raw_automated_passed": len(selected_records),
        "validated_passed": len(selected_records),
        "citation_repair_count": sum(
            len(item["accepted_automated_audit"]["citation_repairs"])
            for item in selection["cases"]
        ),
        "rejected_attempt_count": rejected_count,
        "accepted_samples_path": selection_path.name,
        "accepted_validated_outputs_path": args.accepted_outputs.name,
    }
    output_bytes = (
        json.dumps(accepted_outputs, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")
    validation_bytes = (json.dumps(validation, indent=2) + "\n").encode("utf-8")

    if args.check:
        check_equal(
            "Accepted validated outputs",
            args.accepted_outputs.read_bytes(),
            output_bytes,
        )
        check_equal(
            "Accepted validation report",
            args.validation_output.read_bytes(),
            validation_bytes,
        )
    else:
        args.accepted_outputs.write_bytes(output_bytes)
        args.validation_output.write_bytes(validation_bytes)

    selected_metrics = record_metrics(selected_records)
    all_metrics = record_metrics(all_records)
    report = {
        "status": "ok",
        "mode": "check" if args.check else "rebuild",
        "selection_decisions_changed": False,
        "selected_record_hashes_verified": len(selected_records),
        "rejected_record_hashes_verified": rejected_count,
        "provenance_verified": actual_provenance,
        "accepted_validated_outputs_sha256": sha256_bytes(output_bytes),
        "accepted_validation_sha256": sha256_bytes(validation_bytes),
        "selected_24": selected_metrics,
        "all_26_successful_responses": all_metrics,
        "selected_successful_response_proportion": round(
            len(selected_records) / len(all_records), 6
        ),
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
