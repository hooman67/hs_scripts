#!/usr/bin/env python3
"""Verify the completed prompt eval and write deterministic aggregate accounting."""

from __future__ import annotations

import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[1]
V2_SCRIPTS = PROJECT_ROOT / "research/source_messaging_v1_to_v6/versions/v2/scripts"
sys.path.insert(0, str(V2_SCRIPTS))

from citation_path_guard import normalize_citation_paths  # noqa: E402


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def usage_totals(records: list[dict[str, Any]]) -> dict[str, Any]:
    latencies = [float(record["latency_seconds"]) for record in records]
    usage = [record["usage"] for record in records]
    return {
        "response_count": len(records),
        "latency_seconds_sum": round(sum(latencies), 3),
        "latency_seconds_mean": round(statistics.mean(latencies), 6),
        "latency_seconds_median": round(statistics.median(latencies), 3),
        "latency_seconds_min": min(latencies),
        "latency_seconds_max": max(latencies),
        "prompt_tokens": sum(int(item.get("prompt_tokens") or 0) for item in usage),
        "completion_tokens": sum(
            int(item.get("completion_tokens") or 0) for item in usage
        ),
        "total_tokens": sum(int(item.get("total_tokens") or 0) for item in usage),
        "reasoning_tokens": sum(
            int(
                (item.get("completion_tokens_details") or {}).get(
                    "reasoning_tokens"
                )
                or 0
            )
            for item in usage
        ),
        "cached_prompt_tokens": sum(
            int(
                (item.get("prompt_tokens_details") or {}).get("cached_tokens")
                or 0
            )
            for item in usage
        ),
    }


def main() -> None:
    manifest_path = ROOT / "manifest.json"
    accepted_path = ROOT / "accepted_prompt_cases.json"
    inventory_path = ROOT / "status_inventory.json"
    manifest = load(manifest_path)
    accepted = load(accepted_path)
    inventory = load(inventory_path)

    manifest_cases = {case["case_id"]: case for case in manifest["cases"]}
    accepted_cases = accepted["cases"]
    if set(accepted_cases) != set(manifest_cases):
        raise RuntimeError("Accepted case IDs do not exactly match manifest case IDs")
    if inventory != {
        "version": "camera-v2-prompt-status-v1",
        "manifest_case_count": 369,
        "manifest_source_render_pair_count": 729,
        "accepted_case_count": 369,
        "manual_review_case_count": 0,
        "rejected_case_count": 0,
        "unprocessed_case_count": 0,
        "accepted_prompt_count": 592,
        "launchable_generation_row_count": 1318,
        "accepted_origin_counts": {"api": 355, "reused_exact": 14},
    }:
        raise RuntimeError("Final status inventory does not match the completed contract")

    final_api_records: list[dict[str, Any]] = []
    origin_counts: Counter[str] = Counter()
    repair_cases: list[str] = []
    unknown_fallback_cases: list[str] = []
    for case_id, case in manifest_cases.items():
        entry = accepted_cases[case_id]
        for field in (
            "case_id",
            "source_id",
            "device_type",
            "camera_tag",
            "input_path",
            "input_sha256",
            "render_ids",
            "expected_camera",
        ):
            if entry[field] != case[field]:
                raise RuntimeError(f"Accepted entry mismatch for {case_id}: {field}")
        if entry["status"] != "accepted" or entry["launchable"] is not True:
            raise RuntimeError(f"Case is not launchable and accepted: {case_id}")
        if entry["validated_failures"] or entry["citation_guard_failures"]:
            raise RuntimeError(f"Accepted case retains a validation failure: {case_id}")
        record_path = Path(entry["accepted_record_path"])
        if file_sha256(record_path) != entry["accepted_record_sha256"]:
            raise RuntimeError(f"Accepted record hash mismatch: {case_id}")
        record = load(record_path)
        guard = normalize_citation_paths(
            record["parsed_output"], record["request_input"]["source_messaging"]
        )
        if guard["failures"]:
            raise RuntimeError(f"Citation guard failed on accepted case: {case_id}")
        output = guard["validated_output"]
        if canonical_sha256(output) != entry["validated_output_sha256"]:
            raise RuntimeError(f"Validated output hash mismatch: {case_id}")
        expected_prompts = [
            {
                "prompt_id": prompt["id"],
                "environment": prompt["environment"],
                "text": prompt["text"],
                "text_sha256": sha256_bytes(prompt["text"].encode("utf-8")),
            }
            for prompt in output["prompts"]
        ]
        if entry["prompts"] != expected_prompts or entry["debug"] != output["debug"]:
            raise RuntimeError(f"Accepted prompt/debug projection mismatch: {case_id}")
        validation = load(ROOT / "validation/cases" / f"{case_id}.json")
        if validation["status"] != "accepted":
            raise RuntimeError(f"Final validation is not accepted: {case_id}")
        if validation.get("validated_failures") or validation.get(
            "manual_density_flags"
        ):
            raise RuntimeError(f"Final validation retains a hold: {case_id}")
        origin_counts[record["origin"]] += 1
        if record["origin"] == "api":
            final_api_records.append(record)
        if entry["citation_repairs"]:
            repair_cases.append(case_id)
        if case["unknown_camera_fallback"]:
            unknown_fallback_cases.append(case_id)

    successful_paths = sorted((ROOT / "records/attempts").glob("*/*.json"))
    successful_records = [load(path) for path in successful_paths]
    if len(successful_records) != 367:
        raise RuntimeError("Unexpected successful API response count")
    attempt_reports = [
        load(path) for path in sorted((ROOT / "validation/attempts").glob("*/*.json"))
    ]
    rejected_reports = [item for item in attempt_reports if item["status"] == "rejected"]
    if len(rejected_reports) != 12:
        raise RuntimeError("Unexpected rejected successful response count")
    retry_events = sum(len(record.get("retry_events", [])) for record in successful_records)
    if retry_events != 1:
        raise RuntimeError("Unexpected transient retry count")

    all_usage = usage_totals(successful_records)
    selected_usage = usage_totals(final_api_records)
    rejected_records = [load(Path(report["record_path"])) for report in rejected_reports]
    rejected_usage = usage_totals(rejected_records)
    for additive_key in (
        "response_count",
        "latency_seconds_sum",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "reasoning_tokens",
        "cached_prompt_tokens",
    ):
        if abs(
            all_usage[additive_key]
            - selected_usage[additive_key]
            - rejected_usage[additive_key]
        ) > 0.001:
            raise RuntimeError(f"API accounting does not balance: {additive_key}")
    interruptions_path = ROOT / "run_interruptions.json"
    interruptions = load(interruptions_path)
    possible_unrecorded = sum(
        event["possible_unrecorded_transport_attempt_count_upper_bound"]
        for event in interruptions["events"]
    )
    failure_reasons = Counter(
        reason for report in rejected_reports for reason in report["validated_failures"]
    )

    batch_files = sorted((ROOT / "batches").glob("prompt_batch_*.json"))
    summary = {
        "version": "camera-v2-final-prompt-summary-v1",
        "provenance": {
            "manifest_path": str(manifest_path),
            "manifest_sha256": file_sha256(manifest_path),
            "accepted_prompt_cases_path": str(accepted_path),
            "accepted_prompt_cases_sha256": file_sha256(accepted_path),
            "status_inventory_path": str(inventory_path),
            "status_inventory_sha256": file_sha256(inventory_path),
            "system_prompt_sha256": accepted["system_prompt_sha256"],
            "input_schema_sha256": accepted["input_schema_sha256"],
            "output_schema_sha256": accepted["output_schema_sha256"],
            "model": accepted["model"],
        },
        "final_status": inventory,
        "verified": {
            "exact_manifest_case_join": True,
            "accepted_record_hashes": 369,
            "validated_output_hashes": 369,
            "prompt_and_debug_projections": 369,
            "final_validation_reports_accepted": 369,
            "source_quote_camera_schema_props_and_device_boundary_failures": 0,
            "origin_counts": dict(origin_counts),
            "unknown_camera_fallback_case_ids": unknown_fallback_cases,
            "citation_repair_case_ids": repair_cases,
        },
        "api_accounting": {
            "successful_response_attempts": all_usage,
            "selected_new_api_responses": selected_usage,
            "rejected_successful_responses": rejected_usage,
            "rejected_response_count": len(rejected_reports),
            "rejected_case_count": len(
                {report["case_id"] for report in rejected_reports}
            ),
            "rejection_reason_counts": dict(sorted(failure_reasons.items())),
            "recorded_transient_failed_transport_attempts": retry_events,
            "recorded_transport_attempt_count": len(successful_records) + retry_events,
            "possible_unrecorded_interrupted_transport_attempts_upper_bound": possible_unrecorded,
            "transport_attempt_count_range_including_interruption_uncertainty": [
                len(successful_records) + retry_events,
                len(successful_records) + retry_events + possible_unrecorded,
            ],
            "interruption_audit_path": str(interruptions_path),
            "interruption_audit_sha256": file_sha256(interruptions_path),
        },
        "review_batches": [
            {
                "path": str(path),
                "sha256": file_sha256(path),
                "case_count": load(path)["case_count"],
            }
            for path in batch_files
        ],
        "limitations": [
            "The transport-attempt total has a +0..2 uncertainty because two requests may have been in flight during the documented controlled interruption; no response files exist for them.",
            "The deterministic density audit is a conservative heuristic. Root review accepted all reviewed scene scopes, including the recorded FrontCloseUpHigh ambiguity advisory.",
            "The three laptop_CAMReview cases intentionally use the conservative unknown-camera fallback because the tag is unregistered; no profile was invented.",
        ],
    }
    output_path = ROOT / "validation/final_prompt_summary.json"
    output_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(output_path)
    print(file_sha256(output_path))


if __name__ == "__main__":
    main()
