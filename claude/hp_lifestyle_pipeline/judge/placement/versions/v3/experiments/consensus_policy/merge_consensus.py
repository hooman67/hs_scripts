#!/usr/bin/env python3
"""Apply the generic two-verifier consensus policy to saved predictions only."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parent
V3_ROOT = ROOT.parents[1]
TWO_PASS_ROOT = ROOT.parent / "two_pass"
POLICY_PATH = ROOT / "policy.json"
POLICY_VERSION = "placement-consensus-additions-decision-v1"
DEVELOPMENT_STATUS = "posthoc_policy_developed_with_partial_new_image_inspection_not_heldout_validation"
CONFIDENCE_ORDER = {"low": 0, "medium": 1, "high": 2}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCORING = load_module("consensus_v3_scoring", V3_ROOT / "scoring.py")
COMBINE = load_module("consensus_two_pass_combine", TWO_PASS_ROOT / "combine.py")


def sha256(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def confidently_material(component: Mapping[str, Any]) -> bool:
    return (
        component.get("visibility") in {"observed", "partial"}
        and component.get("confidence") in {"medium", "high"}
        and isinstance(component.get("severity"), int)
        and component["severity"] >= 2
    )


def confidently_clear(component: Mapping[str, Any]) -> bool:
    return (
        component.get("visibility") in {"observed", "partial"}
        and component.get("confidence") in {"medium", "high"}
        and isinstance(component.get("severity"), int)
        and component["severity"] <= 1
    )


def uncertain(component: Mapping[str, Any]) -> bool:
    return component.get("visibility") == "unobservable" or component.get("confidence") == "low" or component.get("severity") is None


def quote(label: str, text: str) -> str:
    return f'{label}: "{text.strip()}"'


def resolve_component(name: str, proposal: Mapping[str, Any], independent: Mapping[str, Any], baseline: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    proposal_material = confidently_material(proposal)
    independent_material = confidently_material(independent)
    shared_codes = sorted(set(proposal["issue_codes"]) & set(independent["issue_codes"]))
    if proposal_material and independent_material and shared_codes:
        confidence = min((proposal["confidence"], independent["confidence"]), key=CONFIDENCE_ORDER.get)
        component = {
            "visibility": "partial" if "partial" in {proposal["visibility"], independent["visibility"]} else "observed",
            "severity": min(proposal["severity"], independent["severity"]),
            "confidence": confidence,
            "evidence": " ".join((quote("Proposal-aware verifier", proposal["evidence"]), quote("Names-only independent check", independent["evidence"]))),
            "consequence": " ".join((quote("Proposal-aware consequence", proposal["consequence"]), quote("Names-only consequence", independent["consequence"]))),
            "issue_codes": shared_codes,
        }
        status = "confirmed_consensus"
        selected = "application_derived_consensus_component"
    elif confidently_clear(proposal) or confidently_clear(independent):
        component = copy.deepcopy(baseline)
        status = "rejected_confident_clear_or_minor"
        selected = "baseline_v2_component"
    elif proposal_material and independent_material and not shared_codes:
        component = copy.deepcopy(baseline)
        status = "rejected_disjoint_material_issue_codes"
        selected = "baseline_v2_component"
    else:
        component = copy.deepcopy(baseline)
        status = "unconfirmed_uncertain"
        selected = "baseline_v2_component"
    resolution = {
        "component": name,
        "status": status,
        "selected": selected,
        "shared_issue_codes": shared_codes,
        "proposal_aware": copy.deepcopy(proposal),
        "names_only_independent": copy.deepcopy(independent),
        "baseline_v2": copy.deepcopy(baseline),
        "proposal_aware_confidently_material": proposal_material,
        "names_only_confidently_material": independent_material,
        "proposal_aware_confidently_clear_or_minor": confidently_clear(proposal),
        "names_only_confidently_clear_or_minor": confidently_clear(independent),
        "proposal_aware_uncertain": uncertain(proposal),
        "names_only_uncertain": uncertain(independent),
    }
    return component, resolution


def final_policy(baseline_verdict: str, merged: Mapping[str, Any], resolutions: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    confirmed = sorted(name for name, value in resolutions.items() if value["status"] == "confirmed_consensus")
    rejected = sorted(name for name, value in resolutions.items() if value["status"].startswith("rejected_"))
    unconfirmed = sorted(name for name, value in resolutions.items() if value["status"] == "unconfirmed_uncertain")
    verdict = merged["verdict"]
    reasons = list(merged["verdict_reasons"])
    verdict_override = None
    if unconfirmed and baseline_verdict == "pass" and verdict == "pass":
        verdict = "review"
        reasons = [f"consensus_unconfirmed_component:{name}" for name in unconfirmed]
        verdict_override = "baseline_pass_deferred_to_review_for_unconfirmed_consensus"
    confidence = merged["confidence"]
    confidence_override = None
    if (rejected or unconfirmed) and confidence == "high":
        confidence = "medium"
        confidence_override = "reported_confidence_capped_to_medium_for_consensus_disagreement_or_uncertainty"
    notes = [
        f"The proposal-aware and names-only checks did not reach material consensus for {name}; the baseline V2 component remains selected. See consensus_resolution for both assessments."
        for name in rejected
    ] + [
        f"The independent checks could not confirm or confidently clear the proposed {name} addition; the baseline V2 component remains selected and the addition is unconfirmed."
        for name in unconfirmed
    ]
    return {
        "verdict": verdict,
        "verdict_reasons": reasons,
        "reported_overall_confidence": confidence,
        "verdict_override": verdict_override,
        "confidence_override": confidence_override,
        "uncertainty_notes": notes,
        "confirmed_consensus_components": confirmed,
        "rejected_addition_components": rejected,
        "unconfirmed_addition_components": unconfirmed,
    }


def artifact(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": sha256(path)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-run", type=Path, action="append", required=True)
    parser.add_argument("--proposal-aware-run", type=Path, required=True)
    parser.add_argument("--names-only-run", type=Path, required=True)
    parser.add_argument("--trigger-manifest", type=Path, required=True)
    parser.add_argument("--run-name", required=True)
    args = parser.parse_args()
    output = ROOT / "runs" / args.run_name
    if output.exists():
        raise SystemExit(f"Output exists: {output}")
    trigger_path = args.trigger_manifest.resolve()
    trigger = json.loads(trigger_path.read_text(encoding="utf-8"))
    trigger_map = {record["id"]: set(record["proposed_components"]) for record in trigger["records"]}
    proposal_paths = {path.parent.name: path for path in args.proposal_aware_run.resolve().glob("*/result.json")}
    independent_paths = {path.parent.name: path for path in args.names_only_run.resolve().glob("*/result.json")}
    if not set(trigger_map) <= set(proposal_paths) or not set(trigger_map) <= set(independent_paths):
        raise ValueError("Trigger coverage missing from one or both verifier runs")
    records = []
    resolution_counts = {}
    for source_run in args.source_run:
        for source_path in sorted(source_run.resolve().glob("*/result.json")):
            source = json.loads(source_path.read_text(encoding="utf-8"))
            record_id = source["record_id"]
            baseline = source["stages"]["baseline_v2"]["judgment"]
            compact_original = source["stages"]["compact_v3"]["judgment"]
            compact_obs = copy.deepcopy(compact_original["observation"])
            proposal_overlay = independent_overlay = None
            resolutions = {}
            if record_id in trigger_map:
                proposal_path, independent_path = proposal_paths[record_id], independent_paths[record_id]
                proposal_overlay, independent_overlay = json.loads(proposal_path.read_text()), json.loads(independent_path.read_text())
                if proposal_overlay.get("ok") is not True or independent_overlay.get("ok") is not True:
                    raise ValueError(f"{record_id}: unsuccessful verifier source")
                names = trigger_map[record_id]
                if set(proposal_overlay["assessment"]["components"]) != names or set(independent_overlay["assessment"]["components"]) != names:
                    raise ValueError(f"{record_id}: verifier component coverage mismatch")
                if proposal_overlay["source_provenance"]["combined_result_sha256"] != sha256(source_path):
                    raise ValueError(f"{record_id}: proposal-aware source hash mismatch")
                for name in sorted(names):
                    selected, resolution = resolve_component(name, proposal_overlay["assessment"]["components"][name], independent_overlay["assessment"]["components"][name], baseline["observation"]["components"][name])
                    compact_obs["components"][name] = selected
                    resolutions[name] = resolution
                    resolution_counts[resolution["status"]] = resolution_counts.get(resolution["status"], 0) + 1
            consensus_compact = SCORING.aggregate_observation(compact_obs)
            merged_obs, provenance = COMBINE.merge_observations(baseline["observation"], compact_obs, baseline_verdict=baseline["verdict"], compact_verdict=consensus_compact["verdict"])
            merged = SCORING.aggregate_observation(merged_obs)
            decision = final_policy(baseline["verdict"], merged, resolutions)
            envelope = {
                "schema_version": "placement-consensus-additions-envelope-v1",
                "policy_version": POLICY_VERSION,
                "development_status": DEVELOPMENT_STATUS,
                "policy_developed_on": "prior_comment_checks_and_root_inspection_of_four_new160_trigger_cases",
                "record_id": record_id,
                "policy": {"path": str(POLICY_PATH.resolve()), "sha256": sha256(POLICY_PATH)},
                "merge_generator": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__).resolve())},
                "source_two_pass": {"path": str(source_path.resolve()), "sha256": sha256(source_path), "result": source},
                "trigger_manifest": {"path": str(trigger_path), "sha256": sha256(trigger_path), "requested_components": sorted(trigger_map.get(record_id, set()))},
                "proposal_aware_overlay": None if proposal_overlay is None else {"result": artifact(proposal_paths[record_id]), "raw_response": artifact(proposal_paths[record_id].parent / "response.json"), "assessment": proposal_overlay},
                "names_only_overlay": None if independent_overlay is None else {"result": artifact(independent_paths[record_id]), "raw_response": artifact(independent_paths[record_id].parent / "response.json"), "assessment": independent_overlay},
                "original_compact_judgment": compact_original,
                "consensus_resolution": resolutions,
                "consensus_compact_judgment": consensus_compact,
                "component_provenance": provenance,
                "application_merged_judgment": merged,
                "final_decision": decision,
                "suggested_scene_changes": [],
            }
            case_output = output / record_id
            case_output.mkdir(parents=True)
            atomic_json(case_output / "result.json", envelope)
            records.append({"id": record_id, "verdict": decision["verdict"], "reported_overall_confidence": decision["reported_overall_confidence"], "confirmed": decision["confirmed_consensus_components"], "rejected": decision["rejected_addition_components"], "unconfirmed": decision["unconfirmed_addition_components"]})
    output.mkdir(parents=True, exist_ok=True)
    summary = {
        "schema_version": "placement-consensus-additions-run-v1",
        "policy_version": POLICY_VERSION,
        "development_status": DEVELOPMENT_STATUS,
        "policy_developed_on": "prior_comment_checks_and_root_inspection_of_four_new160_trigger_cases",
        "policy": {"path": str(POLICY_PATH.resolve()), "sha256": sha256(POLICY_PATH)},
        "merge_generator": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__).resolve())},
        "record_count": len(records),
        "trigger_case_count": len(trigger_map),
        "trigger_component_count": sum(map(len, trigger_map.values())),
        "resolution_counts": resolution_counts,
        "records": records,
    }
    atomic_json(output / "summary.json", summary)
    print(json.dumps({"output": str(output), "records": len(records), "resolutions": resolution_counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
