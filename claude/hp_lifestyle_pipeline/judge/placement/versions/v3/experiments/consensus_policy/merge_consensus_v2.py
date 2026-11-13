#!/usr/bin/env python3
"""Apply consensus-v1 with strengthened source binding and coverage validation."""

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
INPUT_KEYS = frozenset({"generated_image", "twin_image", "product_type", "scene_prompt", "image_stage"})
SOURCE_BINDING_VERSION = "placement-consensus-source-binding-v2"


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


def require_exact_ids(label: str, actual: set[str], expected: set[str]) -> None:
    if actual != expected:
        raise ValueError(f"{label} IDs differ: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")


def validate_independent_binding(record_id: str, independent: Mapping[str, Any], source: Mapping[str, Any], trigger_sha256: str) -> dict[str, Any]:
    runtime_input = independent.get("runtime_input")
    if not isinstance(runtime_input, Mapping) or set(runtime_input) != INPUT_KEYS:
        raise ValueError(f"{record_id}: names-only runtime input whitelist mismatch")
    identity = source["input_identity"]
    scene_prompt_sha256 = hashlib.sha256(runtime_input["scene_prompt"].encode("utf-8")).hexdigest()
    actual = {
        "generated_image_sha256": sha256(Path(runtime_input["generated_image"])),
        "twin_image_sha256": sha256(Path(runtime_input["twin_image"])),
        "scene_prompt_sha256": scene_prompt_sha256,
        "product_type": runtime_input["product_type"],
        "image_stage": runtime_input["image_stage"],
    }
    expected = {key: identity[key] for key in actual}
    if actual != expected:
        raise ValueError(f"{record_id}: names-only runtime input does not match two-pass source identity")
    for key in ("generated_image", "twin_image"):
        if independent["images"][key]["sha256"] != actual[f"{key}_sha256"]:
            raise ValueError(f"{record_id}: names-only saved image hash differs from source bytes")
    source_trigger = independent.get("source_trigger")
    if not isinstance(source_trigger, Mapping) or source_trigger.get("sha256") != trigger_sha256:
        raise ValueError(f"{record_id}: names-only result is not bound to this trigger manifest")
    if independent.get("proposal_text_codes_severities_prior_verdicts_comments_passed") is not False:
        raise ValueError(f"{record_id}: names-only contamination exclusion flag changed")
    return {
        "validation_version": SOURCE_BINDING_VERSION,
        "input_whitelist": sorted(INPUT_KEYS),
        "source_input_identity_sha256": identity["input_identity_sha256"],
        "generated_image_sha256": actual["generated_image_sha256"],
        "twin_image_sha256": actual["twin_image_sha256"],
        "scene_prompt_sha256": actual["scene_prompt_sha256"],
        "product_type": actual["product_type"],
        "image_stage": actual["image_stage"],
        "trigger_manifest_sha256": trigger_sha256,
    }


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
    trigger_sha256 = sha256(trigger_path)
    trigger = json.loads(trigger_path.read_text(encoding="utf-8"))
    trigger_map = {record["id"]: set(record["proposed_components"]) for record in trigger["records"]}
    proposal_paths = {path.parent.name: path for path in args.proposal_aware_run.resolve().glob("*/result.json")}
    require_exact_ids("Proposal-aware source", set(proposal_paths), set(trigger_map))
    independent_paths = {}
    for path in args.names_only_run.resolve().glob("*/result.json"):
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("source_trigger", {}).get("sha256") == trigger_sha256:
            independent_paths[path.parent.name] = path
    require_exact_ids("Names-only source bound to this trigger", set(independent_paths), set(trigger_map))
    source_paths = {}
    source_run_coverage = []
    for source_run in args.source_run:
        source_run = source_run.resolve()
        run_paths = {path.parent.name: path for path in source_run.glob("*/result.json")}
        summary = json.loads((source_run / "summary.json").read_text(encoding="utf-8"))
        summary_ids = {item["id"] for item in summary["items"]}
        if summary["record_count"] != len(run_paths) or summary_ids != set(run_paths):
            raise ValueError(f"Source run coverage mismatch: {source_run}")
        duplicate_ids = set(source_paths) & set(run_paths)
        if duplicate_ids:
            raise ValueError(f"Duplicate source IDs across runs: {sorted(duplicate_ids)}")
        source_paths.update(run_paths)
        source_run_coverage.append({"path": str(source_run), "summary_sha256": sha256(source_run / "summary.json"), "record_count": len(run_paths)})
    if not set(trigger_map) <= set(source_paths):
        raise ValueError(f"Triggered source IDs missing from two-pass runs: {sorted(set(trigger_map)-set(source_paths))}")
    records = []
    resolution_counts = {}
    for record_id, source_path in sorted(source_paths.items()):
            source = json.loads(source_path.read_text(encoding="utf-8"))
            if source["record_id"] != record_id:
                raise ValueError(f"{record_id}: source folder/result ID mismatch")
            baseline = source["stages"]["baseline_v2"]["judgment"]
            compact_original = source["stages"]["compact_v3"]["judgment"]
            compact_obs = copy.deepcopy(compact_original["observation"])
            proposal_overlay = independent_overlay = None
            resolutions = {}
            source_binding = None
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
                source_binding = validate_independent_binding(record_id, independent_overlay, source, trigger_sha256)
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
                "schema_version": "placement-consensus-additions-envelope-v2",
                "policy_version": POLICY_VERSION,
                "development_status": DEVELOPMENT_STATUS,
                "policy_developed_on": "prior_comment_checks_and_root_inspection_of_four_new160_trigger_cases",
                "record_id": record_id,
                "policy": {"path": str(POLICY_PATH.resolve()), "sha256": sha256(POLICY_PATH)},
                "merge_generator": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__).resolve())},
                "source_two_pass": {"path": str(source_path.resolve()), "sha256": sha256(source_path), "result": source},
                "trigger_manifest": {"path": str(trigger_path), "sha256": sha256(trigger_path), "requested_components": sorted(trigger_map.get(record_id, set()))},
                "source_binding_validation": source_binding,
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
        "schema_version": "placement-consensus-additions-run-v2",
        "policy_version": POLICY_VERSION,
        "development_status": DEVELOPMENT_STATUS,
        "policy_developed_on": "prior_comment_checks_and_root_inspection_of_four_new160_trigger_cases",
        "policy": {"path": str(POLICY_PATH.resolve()), "sha256": sha256(POLICY_PATH)},
        "merge_generator": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__).resolve())},
        "validator_change": "Strengthened names-only binding to exact two-pass scene/twin bytes, prompt hash, product type, stage, input whitelist, trigger manifest, and exact source-ID coverage; semantic consensus policy unchanged.",
        "source_binding_version": SOURCE_BINDING_VERSION,
        "source_run_coverage": source_run_coverage,
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
