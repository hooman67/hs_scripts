#!/usr/bin/env python3
"""Audit and summarize the frozen-protocol unlabeled NEW160 evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def api_stats(results: list[dict]) -> dict:
    elapsed = [float(value["elapsed_seconds"]) for value in results]
    attempts = [attempt for value in results for attempt in value["attempts"]]
    usage = [value.get("usage") or {} for value in results]
    return {
        "records": len(results),
        "successful_results": sum(value.get("ok") is True for value in results),
        "failed_results": sum(value.get("ok") is not True for value in results),
        "successful_attempts": sum(attempt.get("status") == "ok" for attempt in attempts),
        "failed_attempts": sum(attempt.get("status") != "ok" for attempt in attempts),
        "retried_records": sum(len(value["attempts"]) > 1 for value in results),
        "returned_models": dict(Counter(value.get("model_returned") for value in results)),
        "latency_seconds": {
            "min": min(elapsed),
            "median": statistics.median(elapsed),
            "mean": statistics.fmean(elapsed),
            "p95": percentile(elapsed, 0.95),
            "max": max(elapsed),
        },
        "tokens": {
            key: sum(int(item.get(key, 0)) for item in usage)
            for key in ("prompt_tokens", "completion_tokens", "total_tokens")
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--baseline-run", type=Path, required=True)
    parser.add_argument("--compact-run", type=Path, required=True)
    parser.add_argument("--two-pass-run", type=Path, required=True)
    parser.add_argument("--trigger-manifest", type=Path, required=True)
    parser.add_argument("--verifier-run", type=Path, required=True)
    parser.add_argument("--verified-run", type=Path, required=True)
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--selected-protocol", type=Path, required=True)
    args = parser.parse_args()
    generated = datetime.now(timezone.utc).isoformat()
    evaluator = Path(__file__).resolve()
    manifest = load(args.manifest.resolve())
    ids = [record["id"] for record in manifest["records"]]
    if len(ids) != 160 or len(set(ids)) != 160:
        raise ValueError("Manifest must contain 160 unique records")

    def result_map(run: Path) -> dict[str, tuple[Path, dict]]:
        values = {}
        for path in run.resolve().glob("*/result.json"):
            value = load(path)
            record_id = value.get("record_id") or value.get("input", {}).get("id") or path.parent.name
            values[record_id] = (path, value)
        return values

    baseline = result_map(args.baseline_run)
    compact = result_map(args.compact_run)
    two_pass = result_map(args.two_pass_run)
    verifier = result_map(args.verifier_run)
    verified = result_map(args.verified_run)
    for name, values, expected in (
        ("baseline", baseline, set(ids)), ("compact", compact, set(ids)),
        ("two_pass", two_pass, set(ids)), ("verified", verified, set(ids)),
    ):
        if set(values) != expected:
            raise ValueError(f"{name} coverage mismatch: missing={sorted(expected-set(values))}, extra={sorted(set(values)-expected)}")

    trigger = load(args.trigger_manifest.resolve())
    trigger_map = {record["id"]: set(record["proposed_components"]) for record in trigger["records"]}
    if set(verifier) != set(trigger_map):
        raise ValueError("Verifier result IDs do not exactly equal trigger IDs")
    if trigger["comments_or_expectations_included"] is not False:
        raise ValueError("Trigger manifest does not affirm comment/expectation exclusion")
    component_count = sum(map(len, trigger_map.values()))
    if len(trigger_map) != trigger["expected_count"] or component_count != trigger["expected_component_count"]:
        raise ValueError("Trigger counts changed")

    merge_generators = set()
    overlays = 0
    overlay_components = 0
    artifact_hashes_validated = 0
    stage_fingerprints = {"baseline_v2": {}, "compact_v3": {}}
    for record_id in ids:
        source_path, source = two_pass[record_id]
        _, envelope = verified[record_id]
        if envelope["source_two_pass"]["sha256"] != sha256(source_path):
            raise ValueError(f"{record_id}: source two-pass hash mismatch")
        merge_generators.add((envelope["merge_generator"]["path"], envelope["merge_generator"]["sha256"]))
        for stage_name in ("baseline_v2", "compact_v3"):
            stage = source["stages"][stage_name]
            fingerprint = stage["protocol_fingerprint"]
            stage_fingerprints[stage_name][record_id] = fingerprint
            for artifact in stage["artifacts"].values():
                if sha256(Path(artifact["path"])) != artifact["sha256"]:
                    raise ValueError(f"{record_id}: {stage_name} artifact hash mismatch")
                artifact_hashes_validated += 1
        overlay = envelope["verifier_overlay"]
        if record_id in trigger_map:
            if overlay is None:
                raise ValueError(f"{record_id}: missing verifier overlay")
            verifier_path, verifier_value = verifier[record_id]
            if overlay["result_sha256"] != sha256(verifier_path):
                raise ValueError(f"{record_id}: verifier result hash mismatch")
            if overlay["raw_response_sha256"] != sha256(Path(overlay["raw_response_path"])):
                raise ValueError(f"{record_id}: verifier raw response hash mismatch")
            if set(verifier_value["assessment"]["components"]) != trigger_map[record_id]:
                raise ValueError(f"{record_id}: verifier dropped or added a component")
            overlays += 1
            overlay_components += len(trigger_map[record_id])
        elif overlay is not None:
            raise ValueError(f"{record_id}: unexpected verifier overlay")
    if len(merge_generators) != 1:
        raise ValueError(f"Expected one merge generator, got {merge_generators}")
    merge_path, merge_hash = next(iter(merge_generators))
    if sha256(Path(merge_path)) != merge_hash:
        raise ValueError("Merge generator hash mismatch")

    baseline_values = [baseline[record_id][1] for record_id in ids]
    compact_values = [compact[record_id][1] for record_id in ids]
    verifier_values = [verifier[record_id][1] for record_id in trigger_map]
    if any(value.get("ok") is not True for value in baseline_values + compact_values + verifier_values):
        raise ValueError("At least one API result is not successful")

    def verdicts(stage: str) -> dict[str, str]:
        if stage == "baseline": return {key: value[1]["stages"]["baseline_v2"]["judgment"]["verdict"] for key, value in two_pass.items()}
        if stage == "compact": return {key: value[1]["stages"]["compact_v3"]["judgment"]["verdict"] for key, value in two_pass.items()}
        if stage == "two_pass": return {key: value[1]["combined_judgment"]["verdict"] for key, value in two_pass.items()}
        return {key: value[1]["final_decision"]["verdict"] for key, value in verified.items()}

    stage_verdicts = {stage: verdicts(stage) for stage in ("baseline", "compact", "two_pass", "verified")}
    transitions = {}
    for before, after in (("baseline", "two_pass"), ("two_pass", "verified"), ("baseline", "verified")):
        changed = [record_id for record_id in ids if stage_verdicts[before][record_id] != stage_verdicts[after][record_id]]
        transitions[f"{before}_to_{after}"] = {
            "changed_count": len(changed),
            "transitions": dict(Counter(f"{stage_verdicts[before][i]}->{stage_verdicts[after][i]}" for i in changed)),
            "record_ids": changed,
        }

    verifier_assessments = []
    for record_id in sorted(trigger_map):
        value = verifier[record_id][1]
        for component, assessment in value["assessment"]["components"].items():
            verifier_assessments.append({"id": record_id, "component": component, "visibility": assessment["visibility"], "severity": assessment["severity"], "confidence": assessment["confidence"], "issue_codes": assessment["issue_codes"]})
    scores = [float(value[1]["application_merged_judgment"]["natural_placement_score"]) for value in verified.values()]
    evaluation = {
        "schema_version": "placement-verified-additions-new160-evaluation-v1",
        "generated_at_utc": generated,
        "evaluator": {"path": str(evaluator), "sha256": sha256(evaluator)},
        "development_status": "frozen_protocol_unlabeled_new_image_evaluation",
        "policy_developed_on": "prior_comment_checks",
        "labeled_accuracy_metrics": None,
        "coverage": {"manifest_records": len(ids), "baseline_results": len(baseline), "compact_results": len(compact), "two_pass_results": len(two_pass), "verified_results": len(verified), "trigger_cases": len(trigger_map), "trigger_components": component_count, "verifier_overlays": overlays, "verified_overlay_components": overlay_components, "stage_artifact_hashes_validated": artifact_hashes_validated, "missing_records": 0},
        "api": {"baseline_v2": api_stats(baseline_values), "compact_v3": api_stats(compact_values), "verifier": api_stats(verifier_values)},
        "verdict_counts": {stage: dict(Counter(values.values())) for stage, values in stage_verdicts.items()},
        "verdict_transitions": transitions,
        "verified_score": {"min": min(scores), "median": statistics.median(scores), "mean": statistics.fmean(scores), "max": max(scores)},
        "verifier_assessments": verifier_assessments,
        "final_override_counts": dict(Counter((value[1]["final_decision"]["verdict_override"] or "none") for value in verified.values())),
        "final_confidence_override_counts": dict(Counter((value[1]["final_decision"]["confidence_override"] or "none") for value in verified.values())),
    }
    audit = {
        "schema_version": "placement-verified-additions-new160-audit-v1",
        "generated_at_utc": generated,
        "evaluator": evaluation["evaluator"],
        "manifest": {"path": str(args.manifest.resolve()), "sha256": sha256(args.manifest.resolve())},
        "runs": {
            "baseline_v2": {"path": str(args.baseline_run.resolve()), "progress_sha256": sha256(args.baseline_run.resolve()/"progress.json")},
            "compact_v3": {"path": str(args.compact_run.resolve()), "progress_sha256": sha256(args.compact_run.resolve()/"progress.json")},
            "two_pass": {"path": str(args.two_pass_run.resolve()), "summary_sha256": sha256(args.two_pass_run.resolve()/"summary.json")},
            "verifier": {"path": str(args.verifier_run.resolve()), "summary_sha256": sha256(args.verifier_run.resolve()/"summary.json")},
            "verified": {"path": str(args.verified_run.resolve()), "summary_sha256": sha256(args.verified_run.resolve()/"summary.json")},
        },
        "trigger_manifest": {"path": str(args.trigger_manifest.resolve()), "sha256": sha256(args.trigger_manifest.resolve())},
        "protocol_freeze": {"path": str(args.freeze.resolve()), "sha256": sha256(args.freeze.resolve())},
        "selected_protocol": {"path": str(args.selected_protocol.resolve()), "sha256": sha256(args.selected_protocol.resolve())},
        "merge_generator": {"path": merge_path, "sha256": merge_hash},
        "stage_protocol_fingerprints": {
            stage: {
                "records": len(values),
                "unique_full_fingerprints": len({value["fingerprint"] for value in values.values()}),
                "protocol_versions": sorted({value["protocol_version"] for value in values.values()}),
                "runner_sha256": sorted({value["runner_sha256"] for value in values.values()}),
                "system_prompt_sha256": sorted({value["system_prompt_sha256"] for value in values.values()}),
                "schema_sha256": sorted({value["schema_sha256"] for value in values.values()}),
                "scoring_sha256": sorted({value["scoring_sha256"] for value in values.values()}),
            }
            for stage, values in stage_fingerprints.items()
        },
        "coverage_validated": evaluation["coverage"],
    }
    write(args.verified_run.resolve()/"evaluation.json", evaluation)
    write(args.verified_run.resolve()/"audit.json", audit)
    print(json.dumps({"evaluation": str(args.verified_run.resolve()/"evaluation.json"), "audit": str(args.verified_run.resolve()/"audit.json"), "summary": evaluation}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
