#!/usr/bin/env python3
"""Evaluate two-pass results without passing annotations into either model stage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from combine import atomic_json, manifest_records, sha256_path


def observed_issue_codes(judgment: Mapping[str, Any]) -> set[str]:
    return {
        code
        for component in judgment["observation"]["components"].values()
        for code in component["issue_codes"]
    }


def match_transition(before: bool, after: bool) -> str:
    if not before and after:
        return "gained_match"
    if before and not after:
        return "lost_match"
    return "retained_match" if after else "retained_miss"


def mechanical_comparison(result: Mapping[str, Any]) -> dict[str, Any]:
    baseline = result["stages"]["baseline_v2"]["judgment"]
    compact = result["stages"]["compact_v3"]["judgment"]
    combined = result["combined_judgment"]
    baseline_issues = observed_issue_codes(baseline)
    combined_issues = observed_issue_codes(combined)
    return {
        "baseline_v2_verdict": baseline["verdict"],
        "compact_v3_verdict": compact["verdict"],
        "combined_verdict": combined["verdict"],
        "baseline_to_combined_verdict": f"{baseline['verdict']}->{combined['verdict']}",
        "component_sources": {
            name: value["selected_source"]
            for name, value in result["component_provenance"].items()
        },
        "baseline_v2_issue_codes": sorted(baseline_issues),
        "combined_issue_codes": sorted(combined_issues),
        "issue_codes_added": sorted(combined_issues - baseline_issues),
        "issue_codes_removed": sorted(baseline_issues - combined_issues),
    }


def comparison_summary(results: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    comparisons = {
        record_id: mechanical_comparison(result) for record_id, result in results.items()
    }
    transitions: dict[str, int] = {}
    selected: dict[str, int] = {"baseline_v2": 0, "compact_v3": 0}
    changed = []
    for record_id, comparison in comparisons.items():
        transition = comparison["baseline_to_combined_verdict"]
        transitions[transition] = transitions.get(transition, 0) + 1
        if comparison["baseline_v2_verdict"] != comparison["combined_verdict"]:
            changed.append(record_id)
        for source in comparison["component_sources"].values():
            selected[source] += 1
    return {
        "verdict_transition_counts": dict(sorted(transitions.items())),
        "verdict_changed_count": len(changed),
        "verdict_changed_ids": sorted(changed),
        "selected_component_source_counts": selected,
        "comments_or_expectations_passed_to_models": False,
        "stage_runtime_inputs_verified": 2 * len(results),
        "cases": comparisons,
    }


def evaluate_diagnostic(
    records: list[Mapping[str, Any]], results: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    items = []
    for record in records:
        result = results[record["id"]]
        judgment = result["combined_judgment"]
        expectation = record.get("diagnostic_expectation")
        if not isinstance(expectation, Mapping) or expectation.get("passed_to_judge") is not False:
            raise ValueError(f"{record['id']}: invalid diagnostic expectation separation")
        acceptable = expectation.get("acceptable_verdicts", [])
        expected_issues = expectation.get("expected_issue_any", [])
        actual_issues = observed_issue_codes(judgment)
        verdict_match = judgment["verdict"] in acceptable if acceptable else None
        issue_match = bool(actual_issues.intersection(expected_issues)) if expected_issues else None
        items.append(
            {
                "id": record["id"],
                "combined_verdict": judgment["verdict"],
                "acceptable_verdicts": acceptable,
                "verdict_match": verdict_match,
                "expected_issue_any": expected_issues,
                "observed_issue_codes": sorted(actual_issues),
                "issue_match": issue_match,
                "baseline_v2_verdict": result["stages"]["baseline_v2"]["judgment"]["verdict"],
                "compact_v3_verdict": result["stages"]["compact_v3"]["judgment"]["verdict"],
                "mechanical_comparison": mechanical_comparison(result),
            }
        )
    verdict_checks = [item for item in items if item["verdict_match"] is not None]
    issue_checks = [item for item in items if item["issue_match"] is not None]
    return {
        "dataset_kind": "development_diagnostic_20",
        "record_count": len(items),
        "verdict_checks": {
            "count": len(verdict_checks),
            "matched": sum(item["verdict_match"] is True for item in verdict_checks),
        },
        "issue_checks": {
            "count": len(issue_checks),
            "matched": sum(item["issue_match"] is True for item in issue_checks),
        },
        "items": items,
    }


def evaluate_extended(
    records: list[Mapping[str, Any]], results: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    explicit: list[dict[str, Any]] = []
    agreements: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    for record in records:
        result = results[record["id"]]
        judgment = result["combined_judgment"]
        expectation = record.get("extended_validation_expectation")
        if not isinstance(expectation, Mapping) or expectation.get("passed_to_judge") is not False:
            raise ValueError(f"{record['id']}: invalid extended expectation separation")
        kind = expectation.get("expectation_type")
        if kind == "explicit_verdict":
            acceptable = expectation.get("explicit_acceptable_verdicts", [])
            baseline_verdict = result["stages"]["baseline_v2"]["judgment"]["verdict"]
            baseline_match = baseline_verdict in acceptable
            combined_match = judgment["verdict"] in acceptable
            explicit.append(
                {
                    "id": record["id"],
                    "baseline_v2_verdict": baseline_verdict,
                    "combined_verdict": judgment["verdict"],
                    "acceptable_verdicts": acceptable,
                    "baseline_match": baseline_match,
                    "match": combined_match,
                    "match_transition": match_transition(baseline_match, combined_match),
                }
            )
        elif kind == "agreement_with_v2":
            expected = expectation.get("agreement_with_v2", {}).get("v2_verdict")
            agreements.append(
                {
                    "id": record["id"],
                    "combined_verdict": judgment["verdict"],
                    "frozen_v2_verdict": expected,
                    "match": judgment["verdict"] == expected,
                    "match_transition": (
                        "retained_match"
                        if judgment["verdict"] == expected
                        else "lost_match"
                    ),
                }
            )
        expected_issues = expectation.get("expected_issue_any", [])
        if expected_issues:
            baseline_actual = observed_issue_codes(
                result["stages"]["baseline_v2"]["judgment"]
            )
            actual = observed_issue_codes(judgment)
            baseline_match = bool(baseline_actual.intersection(expected_issues))
            combined_match = bool(actual.intersection(expected_issues))
            issues.append(
                {
                    "id": record["id"],
                    "expectation_type": kind,
                    "expected_issue_any": expected_issues,
                    "baseline_v2_issue_codes": sorted(baseline_actual),
                    "observed_issue_codes": sorted(actual),
                    "baseline_match": baseline_match,
                    "match": combined_match,
                    "match_transition": match_transition(baseline_match, combined_match),
                }
            )
    if (len(explicit), len(agreements), len(issues)) != (2, 56, 6):
        raise ValueError(
            "Extended contract must contain 2 explicit labels, 56 V2 agreements and 6 issue checks"
        )
    return {
        "dataset_kind": "extended_validation_64",
        "record_count": len(records),
        "explicit_labels": {
            "count": 2,
            "matched": sum(item["match"] for item in explicit),
            "items": explicit,
            "match_transitions": {
                value: sum(item["match_transition"] == value for item in explicit)
                for value in ("gained_match", "lost_match", "retained_match", "retained_miss")
            },
        },
        "v2_agreements": {
            "count": 56,
            "matched": sum(item["match"] for item in agreements),
            "items": agreements,
            "match_transitions": {
                "retained_match": sum(item["match"] for item in agreements),
                "lost_match": sum(not item["match"] for item in agreements),
            },
        },
        "issue_checks": {
            "count": 6,
            "matched": sum(item["match"] for item in issues),
            "items": issues,
            "match_transitions": {
                value: sum(item["match_transition"] == value for item in issues)
                for value in ("gained_match", "lost_match", "retained_match", "retained_miss")
            },
        },
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--manifest", type=Path, required=True)
    value.add_argument("--combined-run", type=Path, required=True)
    value.add_argument("--output", type=Path, required=True)
    return value


def main() -> int:
    args = parser().parse_args()
    manifest_path = args.manifest.expanduser().resolve()
    combined_run = args.combined_run.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if output.exists():
        raise SystemExit(f"Output already exists: {output}")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = manifest_records(payload)
    results = {}
    for record in records:
        path = combined_run / record["id"] / "result.json"
        if not path.is_file():
            raise SystemExit(f"Missing combined result: {path}")
        result = json.loads(path.read_text(encoding="utf-8"))
        if result.get("record_id") != record["id"]:
            raise ValueError(f"Combined result id mismatch: {path}")
        results[record["id"]] = result
    if all("diagnostic_expectation" in record for record in records):
        evaluation = evaluate_diagnostic(records, results)
    elif all("extended_validation_expectation" in record for record in records):
        evaluation = evaluate_extended(records, results)
    else:
        raise ValueError("Manifest has no supported uniform evaluation contract")
    output_value = {
        "schema_version": "placement-two-pass-evaluation-v1",
        "manifest": str(manifest_path),
        "manifest_sha256": sha256_path(manifest_path),
        "combined_run": str(combined_run),
        "annotation_inputs_to_models": False,
        "mechanical_v2_to_combined_comparison": comparison_summary(results),
        **evaluation,
    }
    atomic_json(output, output_value)
    print(json.dumps(output_value, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
