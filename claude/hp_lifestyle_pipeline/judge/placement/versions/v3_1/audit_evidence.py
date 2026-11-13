"""Recompute saved model outputs and ensemble decisions without model calls."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import run_judge

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-name", required=True)
    args = parser.parse_args()
    folder = ROOT / "calibration" / args.run_name
    summary = json.loads((folder / "summary.json").read_text())
    if not summary["completed"]:
        raise ValueError("Calibration incomplete")
    manifest = json.loads((ROOT / "sources/manifest.json").read_text())
    expected_ids = {c["id"] for c in manifest["cases"]}
    if {r["id"] for r in summary["items"]} != expected_ids:
        raise ValueError("Anchor coverage differs from frozen manifest")
    cases, calls = [], []
    for item in summary["items"]:
        case_dir = folder / item["id"]
        result = json.loads((case_dir / "result.json").read_text())
        runtime = json.loads((case_dir / "input.json").read_text())
        stages = {}
        for stage, artifact in result["stages"].items():
            path = Path(artifact["path"])
            if run_judge.sha(path) != artifact["sha256"]:
                raise ValueError("Stage result hash changed")
            request = json.loads((path.parent / "request.json").read_text())
            fingerprint = request.pop("fingerprint")
            if run_judge.json_sha(request) != fingerprint:
                raise ValueError("Stage request fingerprint mismatch")
            saved = json.loads(path.read_text())
            raw = json.loads((path.parent / "response.json").read_text())
            if not saved["ok"] or saved["fingerprint"] != fingerprint:
                raise ValueError("Failed or mismatched stage result")
            if request["runtime_input"] != runtime or set(runtime) != run_judge.INPUT_KEYS:
                raise ValueError("Stage inputs not bound to exact five-field target")
            for key, image in request["images"].items():
                if image["path"] != runtime[key] or run_judge.sha(image["path"]) != image["sha256"]:
                    raise ValueError("Stage image bytes changed")
            if request["protocol_freeze_sha256"] != summary["protocol_freeze_sha256"]:
                raise ValueError("Stage protocol binding differs")
            if stage == "independent" and request["proposals"] is not None:
                raise ValueError("Names-only check received accusations")
            choice = raw["choices"][0]
            if not run_judge.identity_matches(raw["model"]) or choice["finish_reason"] != "stop":
                raise ValueError("Unexpected model or incomplete judgment")
            observation = json.loads(choice["message"]["content"])
            if observation != saved["observation"]:
                raise ValueError("Saved model observation was edited")
            if stage in {"baseline", "compact"}:
                run_judge.SCORING.validate_observation(observation)
            else:
                run_judge.validate_components(
                    observation, run_judge.component_schema(request["requested_components"]))
            stages[stage] = observation
            calls.append({"case": item["id"], "stage": stage, "model": raw["model"],
                          "response_sha256": run_judge.sha(path.parent / "response.json")})
        recomputed = run_judge.aggregate_stages(
            stages["baseline"], stages["compact"], stages.get("proposal"), stages.get("independent"))
        for key in recomputed:
            if recomputed[key] != result[key]:
                raise ValueError(f"Deterministic recomputation differs: {key}")
        cases.append({"id": item["id"], "recomputation_matches": True,
                      "verdict": result["final_decision"]["verdict"],
                      "checks": item["checks"]})
    audit = {
        "protocol_freeze_sha256": run_judge.verify_freeze(),
        "case_count": len(cases), "actual_model_response_count": len(calls),
        "model_identities": sorted({r["model"] for r in calls}),
        "cases": cases, "calls": calls,
        "raw_observations_unchanged": True, "deterministic_recomputation_matches": True,
        "scope": "Development anchor evidence audit, not held-out accuracy or visual certification.",
    }
    run_judge.write_json(folder / "audit.json", audit)
    print(json.dumps({k: audit[k] for k in (
        "case_count", "actual_model_response_count", "model_identities",
        "raw_observations_unchanged", "deterministic_recomputation_matches")}))


if __name__ == "__main__":
    main()
