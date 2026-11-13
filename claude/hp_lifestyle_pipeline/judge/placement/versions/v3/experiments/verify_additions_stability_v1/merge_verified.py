#!/usr/bin/env python3
"""Create separate verified envelopes without changing two-pass artifacts."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path

from run_verifier import SCORING, atomic_json, sha256, validate_response, response_schema


ROOT = Path(__file__).resolve().parent
TWO_PASS_ROOT = ROOT.parent / "two_pass"


def load_combine():
    spec = importlib.util.spec_from_file_location("verified_two_pass_combine", TWO_PASS_ROOT / "combine.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


COMBINE = load_combine()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-run", type=Path, action="append", required=True)
    parser.add_argument("--verifier-run", type=Path, required=True)
    parser.add_argument("--run-name", required=True)
    args = parser.parse_args()
    output = ROOT / "verified_runs" / args.run_name
    if output.exists(): raise SystemExit(f"Output exists: {output}")
    verifier = {}
    for p in args.verifier_run.resolve().glob("*/result.json"):
        value=json.loads(p.read_text());
        if value.get("ok") is not True: raise ValueError(f"Failed verifier result: {p}")
        verifier[value["record_id"]]=(p,value)
    records=[]
    for source_run in args.source_run:
        for p in sorted(source_run.resolve().glob("*/result.json")):
            original=json.loads(p.read_text()); case_id=original["record_id"]
            baseline=original["stages"]["baseline_v2"]["judgment"]
            compact_original=original["stages"]["compact_v3"]["judgment"]
            compact_obs=copy.deepcopy(compact_original["observation"])
            overlay=None; uncertain=[]
            if case_id in verifier:
                vp,overlay=verifier[case_id]
                source=overlay["source_provenance"]
                if source["combined_result_sha256"] != sha256(p): raise ValueError(f"{case_id}: verifier source hash mismatch")
                names=overlay["proposed_component_names"]
                validate_response(overlay["assessment"], response_schema(names), names)
                for name in names: compact_obs["components"][name]=copy.deepcopy(overlay["assessment"]["components"][name])
                uncertain=[name for name in names if compact_obs["components"][name]["visibility"]=="unobservable" or compact_obs["components"][name]["confidence"]=="low"]
            verified_compact=SCORING.aggregate_observation(compact_obs)
            merged_obs,provenance=COMBINE.merge_observations(baseline["observation"],compact_obs,baseline_verdict=baseline["verdict"],compact_verdict=verified_compact["verdict"])
            merged=SCORING.aggregate_observation(merged_obs)
            final_verdict=merged["verdict"]; reasons=list(merged["verdict_reasons"]); override=None
            if uncertain and baseline["verdict"]=="pass" and final_verdict=="pass":
                final_verdict="review"; reasons=[f"verifier_uncertain:{name}" for name in uncertain]; override="baseline_pass_capped_to_review_for_verifier_uncertainty"
            envelope={"schema_version":"placement-verified-additions-envelope-v1","origin":"application_derived_verified_overlay","record_id":case_id,"source_two_pass":{"path":str(p),"sha256":sha256(p),"result":original},"verifier_overlay":None if overlay is None else {"result_path":str(vp),"result_sha256":sha256(vp),"result":overlay},"verified_compact_judgment":verified_compact,"verified_component_provenance":provenance,"application_merged_judgment":merged,"verification_uncertain_components":uncertain,"final_decision":{"verdict":final_verdict,"verdict_reasons":reasons,"override":override},"suggested_scene_changes":[]}
            case_out=output/case_id; case_out.mkdir(parents=True)
            atomic_json(case_out/"result.json",envelope); records.append({"id":case_id,"verdict":final_verdict,"override":override})
    output.mkdir(parents=True,exist_ok=True); atomic_json(output/"summary.json",{"schema_version":"placement-verified-additions-run-v1","record_count":len(records),"records":records})
    print(json.dumps({"output":str(output),"records":len(records)},indent=2)); return 0


if __name__ == "__main__": raise SystemExit(main())
