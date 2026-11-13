#!/usr/bin/env python3
"""Posthoc development policy V2 for verified-addition envelopes."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
from typing import Any, Mapping

from run_verifier import SCORING, atomic_json, sha256, validate_response, response_schema


ROOT = Path(__file__).resolve().parent
TWO_PASS_ROOT = ROOT.parent / "two_pass"
POLICY_VERSION = "placement-verified-additions-decision-v2"
MERGER_PATH = Path(__file__).resolve()


def load_combine():
    spec = importlib.util.spec_from_file_location("verified_v2_two_pass_combine", TWO_PASS_ROOT / "combine.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


COMBINE = load_combine()


def final_policy(
    baseline_verdict: str,
    merged: Mapping[str, Any],
    verifier_components: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    material_low = sorted(
        name for name, component in verifier_components.items()
        if component.get("visibility") in {"observed", "partial"}
        and component.get("confidence") == "low"
        and isinstance(component.get("severity"), int)
        and component["severity"] >= 2
    )
    unobservable = sorted(
        name for name, component in verifier_components.items()
        if component.get("visibility") == "unobservable"
    )
    verdict = merged["verdict"]
    reasons = list(merged["verdict_reasons"])
    verdict_override = None
    if material_low and baseline_verdict == "pass" and verdict == "pass":
        verdict = "review"
        reasons = [f"verifier_low_confidence_material:{name}" for name in material_low]
        verdict_override = "baseline_pass_capped_to_review_for_low_confidence_material_verification"
    confidence = merged["confidence"]
    confidence_override = None
    uncertainty_notes = []
    if unobservable:
        uncertainty_notes = [
            f"Verifier could not observe the proposed {name} relation; this allegation remains unconfirmed. See component provenance for which observable evidence contributes to the score."
            for name in unobservable
        ]
        if confidence == "high":
            confidence = "medium"
            confidence_override = "reported_confidence_capped_to_medium_for_unobservable_verification_check"
    return {
        "verdict": verdict,
        "verdict_reasons": reasons,
        "reported_overall_confidence": confidence,
        "verdict_override": verdict_override,
        "confidence_override": confidence_override,
        "uncertainty_notes": uncertainty_notes,
        "low_confidence_material_components": material_low,
        "unobservable_verification_components": unobservable,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-run", type=Path, action="append", required=True)
    parser.add_argument("--verifier-run", type=Path, required=True)
    parser.add_argument("--run-name", required=True)
    parser.add_argument(
        "--development-status",
        default="posthoc_policy_revision_not_untouched_validation",
        choices=(
            "posthoc_policy_revision_not_untouched_validation",
            "frozen_protocol_unlabeled_new_image_evaluation",
        ),
    )
    args = parser.parse_args()
    output = ROOT / "verified_runs" / args.run_name
    if output.exists(): raise SystemExit(f"Output exists: {output}")
    merge_generator = {"path": str(MERGER_PATH), "sha256": sha256(MERGER_PATH)}
    verifier = {}
    for p in args.verifier_run.resolve().glob("*/result.json"):
        value=json.loads(p.read_text())
        if value.get("ok") is not True: raise ValueError(f"Failed verifier result: {p}")
        verifier[value["record_id"]]=(p,value)
    records=[]
    for source_run in args.source_run:
        for p in sorted(source_run.resolve().glob("*/result.json")):
            original=json.loads(p.read_text()); case_id=original["record_id"]
            baseline=original["stages"]["baseline_v2"]["judgment"]
            compact_original=original["stages"]["compact_v3"]["judgment"]
            compact_obs=copy.deepcopy(compact_original["observation"])
            overlay=None; verifier_components={}
            if case_id in verifier:
                vp,overlay=verifier[case_id]
                if overlay["source_provenance"]["combined_result_sha256"] != sha256(p): raise ValueError(f"{case_id}: verifier source hash mismatch")
                names=overlay["proposed_component_names"]
                validate_response(overlay["assessment"], response_schema(names), names)
                verifier_components=overlay["assessment"]["components"]
                for name in names: compact_obs["components"][name]=copy.deepcopy(verifier_components[name])
            verified_compact=SCORING.aggregate_observation(compact_obs)
            merged_obs,provenance=COMBINE.merge_observations(baseline["observation"],compact_obs,baseline_verdict=baseline["verdict"],compact_verdict=verified_compact["verdict"])
            merged=SCORING.aggregate_observation(merged_obs)
            decision=final_policy(baseline["verdict"],merged,verifier_components)
            envelope={
                "schema_version":"placement-verified-additions-envelope-v2",
                "policy_version":POLICY_VERSION,
                "development_status":args.development_status,
                "policy_developed_on":"prior_comment_checks",
                "merge_generator":merge_generator,
                "origin":"application_derived_verified_overlay",
                "record_id":case_id,
                "source_two_pass":{"path":str(p.resolve()),"sha256":sha256(p),"result":original},
                "verifier_overlay":None if overlay is None else {"result_path":str(vp.resolve()),"result_sha256":sha256(vp),"raw_response_path":str((vp.parent/"response.json").resolve()),"raw_response_sha256":sha256(vp.parent/"response.json"),"result":overlay},
                "verified_compact_judgment":verified_compact,
                "verified_component_provenance":provenance,
                "application_merged_judgment":merged,
                "final_decision":decision,
                "suggested_scene_changes":[],
            }
            case_out=output/case_id; case_out.mkdir(parents=True); atomic_json(case_out/"result.json",envelope)
            records.append({"id":case_id,"verdict":decision["verdict"],"reported_overall_confidence":decision["reported_overall_confidence"],"verdict_override":decision["verdict_override"],"confidence_override":decision["confidence_override"]})
    output.mkdir(parents=True,exist_ok=True)
    atomic_json(output/"summary.json",{"schema_version":"placement-verified-additions-run-v2","policy_version":POLICY_VERSION,"development_status":args.development_status,"policy_developed_on":"prior_comment_checks","merge_generator":merge_generator,"record_count":len(records),"records":records})
    print(json.dumps({"output":str(output),"records":len(records)},indent=2)); return 0


if __name__ == "__main__": raise SystemExit(main())
