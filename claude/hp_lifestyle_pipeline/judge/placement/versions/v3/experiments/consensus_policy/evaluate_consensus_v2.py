#!/usr/bin/env python3
"""Audit source-bound consensus-v2 and prove semantic identity with consensus-v1."""

from __future__ import annotations

import argparse
import hashlib
import json
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


def issue_codes(envelope: dict) -> set[str]:
    return {code for component in envelope["application_merged_judgment"]["observation"]["components"].values() for code in component["issue_codes"]}


def api_stats(values: list[dict]) -> dict:
    elapsed = [float(value["elapsed_seconds"]) for value in values]
    return {
        "calls": len(values),
        "successful": sum(value.get("ok") is True for value in values),
        "errors": sum(value.get("ok") is not True for value in values),
        "retried_calls": sum(len(value.get("attempts", [])) > 1 for value in values),
        "returned_model_ids": dict(Counter(value.get("model_returned") for value in values)),
        "tokens": {
            key: sum(int((value.get("usage") or {}).get(key, 0)) for value in values)
            for key in ("prompt_tokens", "completion_tokens", "total_tokens")
        },
        "latency_seconds": {"min": min(elapsed), "median": statistics.median(elapsed), "mean": statistics.fmean(elapsed), "max": max(elapsed)},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, required=True)
    parser.add_argument("--trigger-manifest", type=Path, required=True)
    parser.add_argument("--diagnostic-manifest", type=Path)
    parser.add_argument("--extended-manifest", type=Path)
    parser.add_argument("--comparison-run", type=Path, required=True)
    args = parser.parse_args()
    run = args.run.resolve()
    generated = datetime.now(timezone.utc).isoformat()
    script = Path(__file__).resolve()
    trigger_path = args.trigger_manifest.resolve()
    trigger = load(trigger_path)
    trigger_map = {record["id"]: set(record["proposed_components"]) for record in trigger["records"]}
    results = {path.parent.name: (path, load(path)) for path in run.glob("*/result.json")}
    if len(results) != args.expected_count:
        raise ValueError(f"Expected {args.expected_count} results, found {len(results)}")
    resolution_counts = Counter()
    intersection_details = []
    source_hashes = overlay_result_hashes = overlay_raw_hashes = 0
    policy_hashes = set()
    generator_hashes = set()
    api_calls = {"baseline_v2": {}, "compact_v3": {}, "proposal_aware": {}, "names_only": {}}
    source_artifact_hashes_validated = 0
    for record_id, (path, envelope) in results.items():
        source = envelope["source_two_pass"]
        if sha256(Path(source["path"])) != source["sha256"]:
            raise ValueError(f"{record_id}: source two-pass hash mismatch")
        source_hashes += 1
        if envelope.get("schema_version") != "placement-consensus-additions-envelope-v2":
            raise ValueError(f"{record_id}: expected consensus envelope v2")
        for stage_name, call_name in (("baseline_v2", "baseline_v2"), ("compact_v3", "compact_v3")):
            stage = source["result"]["stages"][stage_name]
            for stage_artifact in stage["artifacts"].values():
                if sha256(Path(stage_artifact["path"])) != stage_artifact["sha256"]:
                    raise ValueError(f"{record_id}: {stage_name} artifact hash mismatch")
                source_artifact_hashes_validated += 1
            api_calls[call_name][record_id] = load(Path(stage["artifacts"]["result"]["path"]))
        policy_hashes.add((envelope["policy"]["path"], envelope["policy"]["sha256"]))
        generator_hashes.add((envelope["merge_generator"]["path"], envelope["merge_generator"]["sha256"]))
        expected_names = trigger_map.get(record_id, set())
        if set(envelope["consensus_resolution"]) != expected_names:
            raise ValueError(f"{record_id}: consensus resolution coverage mismatch")
        if expected_names:
            binding = envelope.get("source_binding_validation")
            source_identity = source["result"]["input_identity"]
            if not isinstance(binding, dict) or binding.get("validation_version") != "placement-consensus-source-binding-v2":
                raise ValueError(f"{record_id}: missing source-binding v2 validation")
            for key in ("generated_image_sha256", "twin_image_sha256", "scene_prompt_sha256", "product_type", "image_stage"):
                if binding.get(key) != source_identity[key]:
                    raise ValueError(f"{record_id}: source-binding field mismatch: {key}")
            if binding.get("trigger_manifest_sha256") != sha256(trigger_path):
                raise ValueError(f"{record_id}: source-binding trigger hash mismatch")
            for overlay_name in ("proposal_aware_overlay", "names_only_overlay"):
                overlay = envelope[overlay_name]
                if overlay is None:
                    raise ValueError(f"{record_id}: missing {overlay_name}")
                if sha256(Path(overlay["result"]["path"])) != overlay["result"]["sha256"]:
                    raise ValueError(f"{record_id}: {overlay_name} result hash mismatch")
                if sha256(Path(overlay["raw_response"]["path"])) != overlay["raw_response"]["sha256"]:
                    raise ValueError(f"{record_id}: {overlay_name} raw hash mismatch")
                overlay_result_hashes += 1
                overlay_raw_hashes += 1
            api_calls["proposal_aware"][record_id] = envelope["proposal_aware_overlay"]["assessment"]
            api_calls["names_only"][record_id] = envelope["names_only_overlay"]["assessment"]
            independent = envelope["names_only_overlay"]["assessment"]
            source_identity = source["result"]["input_identity"]
            if independent["images"]["generated_image"]["sha256"] != source_identity["generated_image_sha256"] or independent["images"]["twin_image"]["sha256"] != source_identity["twin_image_sha256"]:
                raise ValueError(f"{record_id}: names-only image identity mismatch")
        elif envelope["proposal_aware_overlay"] is not None or envelope["names_only_overlay"] is not None:
            raise ValueError(f"{record_id}: unexpected overlay")
        elif envelope.get("source_binding_validation") is not None:
            raise ValueError(f"{record_id}: unexpected source-binding validation on nontrigger record")
        for name, resolution in envelope["consensus_resolution"].items():
            resolution_counts[resolution["status"]] += 1
            selected_component = envelope["consensus_compact_judgment"]["observation"]["components"][name]
            if resolution["selected"] == "baseline_v2_component" and selected_component != resolution["baseline_v2"]:
                raise ValueError(f"{record_id}/{name}: rejected or unconfirmed addition did not keep baseline")
            if resolution["status"] == "confirmed_consensus":
                if selected_component["issue_codes"] != resolution["shared_issue_codes"] or not resolution["shared_issue_codes"]:
                    raise ValueError(f"{record_id}/{name}: consensus issue-code intersection mismatch")
            intersection_details.append({
                "id": record_id,
                "component": name,
                "status": resolution["status"],
                "selected": resolution["selected"],
                "proposal_aware_severity": resolution["proposal_aware"]["severity"],
                "proposal_aware_confidence": resolution["proposal_aware"]["confidence"],
                "proposal_aware_issue_codes": resolution["proposal_aware"]["issue_codes"],
                "names_only_severity": resolution["names_only_independent"]["severity"],
                "names_only_confidence": resolution["names_only_independent"]["confidence"],
                "names_only_issue_codes": resolution["names_only_independent"]["issue_codes"],
                "shared_issue_codes": resolution["shared_issue_codes"],
                "selected_severity": selected_component["severity"],
                "selected_confidence": selected_component["confidence"],
                "selected_issue_codes": selected_component["issue_codes"],
            })
    if len(policy_hashes) != 1 or len(generator_hashes) != 1:
        raise ValueError("Run contains multiple policy or generator fingerprints")
    policy_path, policy_hash = next(iter(policy_hashes))
    generator_path, generator_hash = next(iter(generator_hashes))
    if sha256(Path(policy_path)) != policy_hash or sha256(Path(generator_path)) != generator_hash:
        raise ValueError("Live policy or generator hash differs from envelope")
    summary = load(run / "summary.json")
    if summary.get("schema_version") != "placement-consensus-additions-run-v2" or summary.get("source_binding_version") != "placement-consensus-source-binding-v2":
        raise ValueError("Run summary is not source-binding v2")
    if {record["id"] for record in summary["records"]} != set(results) or summary["record_count"] != len(results):
        raise ValueError("Run summary source ID coverage mismatch")
    if summary["resolution_counts"] != dict(resolution_counts):
        raise ValueError("Run summary resolution counts mismatch")

    baseline_verdicts = {record_id: envelope["source_two_pass"]["result"]["stages"]["baseline_v2"]["judgment"]["verdict"] for record_id, (_, envelope) in results.items()}
    two_pass_verdicts = {record_id: envelope["source_two_pass"]["result"]["combined_judgment"]["verdict"] for record_id, (_, envelope) in results.items()}
    consensus_verdicts = {record_id: envelope["final_decision"]["verdict"] for record_id, (_, envelope) in results.items()}
    def transitions(before: dict, after: dict) -> dict:
        changed = sorted(record_id for record_id in before if before[record_id] != after[record_id])
        return {"changed_count": len(changed), "counts": dict(Counter(f"{before[i]}->{after[i]}" for i in changed)), "record_ids": changed}
    scores = [float(envelope["application_merged_judgment"]["natural_placement_score"]) for _, envelope in results.values()]
    evaluation = {
        "schema_version": "placement-consensus-additions-evaluation-v2",
        "generated_at_utc": generated,
        "evaluator": {"path": str(script), "sha256": sha256(script)},
        "development_status": "posthoc_policy_developed_with_partial_new_image_inspection_not_heldout_validation",
        "record_count": len(results),
        "trigger_case_count": len(trigger_map),
        "trigger_component_count": len(intersection_details),
        "resolution_counts": dict(resolution_counts),
        "verdict_counts": {
            "baseline_v2": dict(Counter(baseline_verdicts.values())),
            "original_two_pass": dict(Counter(two_pass_verdicts.values())),
            "consensus": dict(Counter(consensus_verdicts.values())),
        },
        "verdict_transitions": {"baseline_to_consensus": transitions(baseline_verdicts, consensus_verdicts), "original_two_pass_to_consensus": transitions(two_pass_verdicts, consensus_verdicts)},
        "natural_placement_score": {"min": min(scores), "median": statistics.median(scores), "mean": statistics.fmean(scores), "max": max(scores)},
        "component_intersections": sorted(intersection_details, key=lambda value: (value["id"], value["component"])),
        "api_call_summary": {stage: api_stats(list(values.values())) for stage, values in api_calls.items()},
    }
    evaluation["api_call_summary"]["total_calls"] = sum(value["calls"] for value in evaluation["api_call_summary"].values())
    stage_api_stats = [value for value in evaluation["api_call_summary"].values() if isinstance(value, dict) and "calls" in value]
    evaluation["api_call_summary"]["total_successful"] = sum(value["successful"] for value in stage_api_stats)
    evaluation["api_call_summary"]["total_errors"] = sum(value["errors"] for value in stage_api_stats)
    evaluation["api_call_summary"]["total_retried_calls"] = sum(value["retried_calls"] for value in stage_api_stats)
    evaluation["api_call_summary"]["total_tokens"] = {
        key: sum(value["tokens"][key] for value in stage_api_stats)
        for key in ("prompt_tokens", "completion_tokens", "total_tokens")
    }
    returned_models = Counter()
    for value in stage_api_stats:
        returned_models.update(value["returned_model_ids"])
    evaluation["api_call_summary"]["returned_model_ids"] = dict(returned_models)
    comparison_run = args.comparison_run.resolve()
    comparison_results = {path.parent.name: load(path) for path in comparison_run.glob("*/result.json")}
    if set(comparison_results) != set(results):
        raise ValueError("Consensus-v1/v2 result ID coverage differs")
    semantic_fields = ("policy_version", "record_id", "original_compact_judgment", "consensus_resolution", "consensus_compact_judgment", "component_provenance", "application_merged_judgment", "final_decision", "suggested_scene_changes")
    semantic_matches = []
    for record_id, (_, envelope) in results.items():
        semantic_matches.append(all(envelope[field] == comparison_results[record_id][field] for field in semantic_fields))
    if not all(semantic_matches):
        raise ValueError("Consensus-v2 changed semantic decisions from consensus-v1")
    evaluation["consensus_v1_semantic_identity"] = {
        "comparison_run": str(comparison_run),
        "fields": list(semantic_fields),
        "matched": sum(semantic_matches),
        "count": len(semantic_matches),
        "all_matched": all(semantic_matches),
    }
    detail_map = {(value["id"], value["component"]): value for value in intersection_details}
    expected_old_material = {
        ("cashmere__laptop_FrontLeftMedium__p6", "access_usability"),
        ("cashmere__laptop_FrontLeftMedium__p6", "orientation_alignment"),
        ("tassel__printer_FrontLeftMedium__p6", "support_scenario"),
    }
    old_present = expected_old_material & set(detail_map)
    if old_present:
        evaluation["preregistered_selection_checks"] = {
            "old_three_material_components_retained": {
                "matched": sum(detail_map[key]["status"] == "confirmed_consensus" for key in expected_old_material),
                "count": 3,
                "passed": all(detail_map[key]["status"] == "confirmed_consensus" for key in expected_old_material),
            },
            "visitor_chair_additions_not_confirmed": {
                "matched": sum(detail_map[("cashmere__laptop_FrontCloseUp__p5", name)]["status"] != "confirmed_consensus" for name in ("access_usability", "orientation_alignment")),
                "count": 2,
                "passed": all(detail_map[("cashmere__laptop_FrontCloseUp__p5", name)]["status"] != "confirmed_consensus" for name in ("access_usability", "orientation_alignment")),
            },
        }
    elitebook_keys = {
        ("elitebook__laptop_BackRightCloseUp__p7", "orientation_alignment"),
        ("elitebook__laptop_BackRightCloseUp__p9", "access_usability"),
        ("elitebook__laptop_BackRightCloseUp__p9", "orientation_alignment"),
    }
    if elitebook_keys <= set(detail_map):
        evaluation["preregistered_selection_checks"] = {
            "new_elitebook_additions_not_confirmed": {
                "matched": sum(detail_map[key]["status"] != "confirmed_consensus" for key in elitebook_keys),
                "count": 3,
                "passed": all(detail_map[key]["status"] != "confirmed_consensus" for key in elitebook_keys),
            },
            "sole_original_new160_verdict_change_removed": {
                "record_id": "elitebook__laptop_BackRightCloseUp__p9",
                "baseline_verdict": baseline_verdicts["elitebook__laptop_BackRightCloseUp__p9"],
                "original_two_pass_verdict": two_pass_verdicts["elitebook__laptop_BackRightCloseUp__p9"],
                "consensus_verdict": consensus_verdicts["elitebook__laptop_BackRightCloseUp__p9"],
                "passed": consensus_verdicts["elitebook__laptop_BackRightCloseUp__p9"] == baseline_verdicts["elitebook__laptop_BackRightCloseUp__p9"],
            },
        }
    if args.diagnostic_manifest:
        checks = load(args.diagnostic_manifest.resolve())["records"]
        verdict_matches, issue_matches = [], []
        for record in checks:
            envelope = results[record["id"]][1]
            expectation = record["diagnostic_expectation"]
            if expectation["acceptable_verdicts"]:
                verdict_matches.append(envelope["final_decision"]["verdict"] in expectation["acceptable_verdicts"])
            if expectation["expected_issue_any"]:
                issue_matches.append(bool(issue_codes(envelope) & set(expectation["expected_issue_any"])))
        evaluation["diagnostic_20"] = {"verdict_checks": {"matched": sum(verdict_matches), "count": len(verdict_matches)}, "issue_checks": {"matched": sum(issue_matches), "count": len(issue_matches)}}
    if args.extended_manifest:
        checks = load(args.extended_manifest.resolve())["records"]
        explicit, agreements, issues = [], [], []
        for record in checks:
            envelope = results[record["id"]][1]
            expectation = record["extended_validation_expectation"]
            verdict = envelope["final_decision"]["verdict"]
            if expectation["expectation_type"] == "explicit_verdict":
                explicit.append(verdict in expectation["explicit_acceptable_verdicts"])
            if expectation["expectation_type"] == "agreement_with_v2":
                agreements.append(verdict == expectation["agreement_with_v2"]["v2_verdict"])
            if expectation["expected_issue_any"]:
                issues.append(bool(issue_codes(envelope) & set(expectation["expected_issue_any"])))
        evaluation["extended_64"] = {"explicit_labels": {"matched": sum(explicit), "count": len(explicit)}, "v2_agreements": {"matched": sum(agreements), "count": len(agreements)}, "issue_checks": {"matched": sum(issues), "count": len(issues)}}
    audit = {
        "schema_version": "placement-consensus-additions-audit-v2",
        "generated_at_utc": generated,
        "evaluator": evaluation["evaluator"],
        "run": {"path": str(run), "summary_sha256": sha256(run / "summary.json")},
        "trigger_manifest": {"path": str(trigger_path), "sha256": sha256(trigger_path)},
        "policy": {"path": policy_path, "sha256": policy_hash},
        "merge_generator": {"path": generator_path, "sha256": generator_hash},
        "coverage": {"source_results": source_hashes, "trigger_cases": len(trigger_map), "trigger_components": len(intersection_details), "overlay_results": overlay_result_hashes, "overlay_raw_responses": overlay_raw_hashes, "missing": 0},
        "validator_change": "Names-only inputs are bound to exact source scene/twin bytes, scene-prompt hash, product type, image stage, five-field input whitelist, trigger manifest, and exact source-ID coverage. Consensus semantics are unchanged.",
        "source_artifact_hashes_validated": source_artifact_hashes_validated,
        "consensus_v1_semantic_identity": evaluation["consensus_v1_semantic_identity"],
        "api_call_summary": evaluation["api_call_summary"],
        "component_intersections": evaluation["component_intersections"],
    }
    write(run / "evaluation.json", evaluation)
    write(run / "audit.json", audit)
    print(json.dumps({"evaluation": str(run/"evaluation.json"), "audit": str(run/"audit.json"), "summary": evaluation}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
