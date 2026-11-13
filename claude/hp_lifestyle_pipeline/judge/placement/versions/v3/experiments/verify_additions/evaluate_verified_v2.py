#!/usr/bin/env python3
"""Reproducibly audit and evaluate a verified-additions V2 development run."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def issue_codes(result: dict) -> set[str]:
    return {
        code
        for component in result["application_merged_judgment"]["observation"]["components"].values()
        for code in component["issue_codes"]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--diagnostic-manifest", type=Path, required=True)
    parser.add_argument("--extended-manifest", type=Path, required=True)
    parser.add_argument("--trigger-manifest", type=Path, default=ROOT / "triggers.json")
    parser.add_argument("--semantic-snapshot", type=Path, default=ROOT / "protocol_snapshots/semantic_v3")
    args = parser.parse_args()
    run = args.run.resolve()
    generated = datetime.now(timezone.utc).isoformat()
    evaluator_hash = digest(Path(__file__))
    trigger = json.loads(args.trigger_manifest.read_text())
    trigger_map = {record["id"]: set(record["proposed_components"]) for record in trigger["records"]}
    results = {path.parent.name: json.loads(path.read_text()) for path in run.glob("*/result.json")}
    if len(results) != 84:
        raise ValueError(f"Expected 84 results, found {len(results)}")
    coverage = {"source_results": 0, "verifier_overlays": 0, "trigger_components": 0}
    for record_id, result in results.items():
        source = Path(result["source_two_pass"]["path"])
        if digest(source) != result["source_two_pass"]["sha256"]:
            raise ValueError(f"{record_id}: source result hash mismatch")
        coverage["source_results"] += 1
        if record_id in trigger_map:
            overlay = result["verifier_overlay"]
            if not overlay or digest(Path(overlay["result_path"])) != overlay["result_sha256"]:
                raise ValueError(f"{record_id}: verifier overlay hash mismatch")
            if set(overlay["result"]["assessment"]["components"]) != trigger_map[record_id]:
                raise ValueError(f"{record_id}: trigger components differ")
            coverage["verifier_overlays"] += 1
            coverage["trigger_components"] += len(trigger_map[record_id])
        elif result["verifier_overlay"] is not None:
            raise ValueError(f"{record_id}: unexpected verifier overlay")
    expected = {"source_results": 84, "verifier_overlays": 6, "trigger_components": 8}
    if coverage != expected:
        raise ValueError(f"Coverage mismatch: {coverage}")

    diagnostic = json.loads(args.diagnostic_manifest.read_text())["records"]
    verdict_checks, diagnostic_issues = [], []
    for record in diagnostic:
        result, expectation = results[record["id"]], record["diagnostic_expectation"]
        if expectation["acceptable_verdicts"]:
            verdict_checks.append(result["final_decision"]["verdict"] in expectation["acceptable_verdicts"])
        if expectation["expected_issue_any"]:
            diagnostic_issues.append(bool(issue_codes(result) & set(expectation["expected_issue_any"])))
    extended = json.loads(args.extended_manifest.read_text())["records"]
    explicit, agreements, extended_issues = [], [], []
    for record in extended:
        result, expectation = results[record["id"]], record["extended_validation_expectation"]
        verdict = result["final_decision"]["verdict"]
        if expectation["expectation_type"] == "explicit_verdict":
            explicit.append(verdict in expectation["explicit_acceptable_verdicts"])
        if expectation["expectation_type"] == "agreement_with_v2":
            agreements.append(verdict == expectation["agreement_with_v2"]["v2_verdict"])
        if expectation["expected_issue_any"]:
            extended_issues.append(bool(issue_codes(result) & set(expectation["expected_issue_any"])))
    evaluation = {
        "schema_version": "placement-verified-additions-evaluation-v2",
        "generated_at_utc": generated,
        "evaluator_path": str(Path(__file__).resolve()),
        "evaluator_sha256": evaluator_hash,
        "development_status": "posthoc_policy_revision_not_untouched_validation",
        "diagnostic_20": {"verdict_checks": {"matched": sum(verdict_checks), "count": len(verdict_checks)}, "issue_checks": {"matched": sum(diagnostic_issues), "count": len(diagnostic_issues)}},
        "extended_64": {"explicit_labels": {"matched": sum(explicit), "count": len(explicit)}, "v2_agreements": {"matched": sum(agreements), "count": len(agreements)}, "issue_checks": {"matched": sum(extended_issues), "count": len(extended_issues)}},
    }
    from collections import Counter
    final_counts = Counter(result["final_decision"]["verdict"] for result in results.values())
    audit = {
        "schema_version": "placement-verified-additions-audit-v2",
        "generated_at_utc": generated,
        "evaluator_path": str(Path(__file__).resolve()),
        "evaluator_sha256": evaluator_hash,
        "development_status": "posthoc_policy_revision_not_untouched_validation",
        "policy_version": "placement-verified-additions-decision-v2",
        "merge_generator": {
            "path": str((ROOT / "merge_verified_v2.py").resolve()),
            "sha256": digest(ROOT / "merge_verified_v2.py"),
        },
        "source_hash_coverage": coverage,
        "expected_coverage": expected,
        "trigger_manifest": {"path": str(args.trigger_manifest.resolve()), "sha256": digest(args.trigger_manifest), "cases": len(trigger_map), "components": sum(map(len, trigger_map.values()))},
        "semantic_verifier_protocol": {"freeze_path": str((args.semantic_snapshot / "freeze.json").resolve()), "freeze_sha256": digest(args.semantic_snapshot / "freeze.json"), "runner_snapshot_sha256": digest(args.semantic_snapshot / "run_verifier.py")},
        "final_verdict_counts": dict(final_counts),
        "evaluation": evaluation,
    }
    write(run / "evaluation.json", evaluation)
    write(run / "audit.json", audit)
    print(json.dumps({"evaluation": str(run / "evaluation.json"), "audit": str(run / "audit.json"), "evaluator_sha256": evaluator_hash, "generated_at_utc": generated}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
