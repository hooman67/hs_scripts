"""One fresh six-case r2 calibration; labels stay outside the model input."""
from __future__ import annotations

import concurrent.futures
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path

import run_judge as runner
from trace_contract import material

ROOT = Path(__file__).resolve().parent


def summarize(case, result, folder):
    observation = result["application_merged_judgment"]["observation"]
    checks = {}
    for dimension, expected in case["expectation"].items():
        component = observation["components"][dimension]
        if expected in {"no_material_defect", "no_new_material_defect"}:
            checks[dimension] = (component["visibility"] in {"observed", "partial"}
                                 and component["severity"] in {0, 1})
        elif expected != "unlabeled":
            code = ("furniture_axis_conflict" if dimension == "orientation_alignment"
                    else "malformed_support_furniture")
            checks[dimension] = (
                material(component) and code in component["issue_codes"]
                and result["final_decision"]["verdict"] == "fail")
    checks["no_retired_chair_code"] = all(
        "chair_alignment_conflict" not in c["issue_codes"]
        for c in observation["components"].values())
    return {
        "id": case["id"], "role": case["role"], "ok": True,
        "verdict": result["final_decision"]["verdict"],
        "score": result["application_merged_judgment"]["natural_placement_score"],
        "expectation": case["expectation"], "checks": checks,
        "components": observation["components"],
        "triggered_components": result["triggered_components"],
        "consensus_resolution": result["consensus_resolution"],
        "result_path": str(folder / "result.json"),
        "result_sha256": runner.sha(folder / "result.json"),
    }


def main():
    execution = json.loads((ROOT / "calibration_execution_freeze.json").read_text())
    for row in execution["files"]:
        if runner.sha(row["path"]) != row["sha256"]:
            raise RuntimeError("Frozen calibration execution dependency changed")
    folder = ROOT / "calibration"
    folder.mkdir(exist_ok=False)
    manifest_path = ROOT / "calibration_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    summary = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_freeze_sha256": runner.verify_freeze(),
        "manifest_sha256": runner.sha(manifest_path),
        "method": "Each of six cases once, each existing role once; no semantic retry or preferred-response selection.",
        "concurrency_cases": 3, "labels_and_prior_outputs_withheld_from_model": True,
        "source_image_stage": "e2e_comparison_output",
        "runtime_stage_adapter": "scene_generation literal for unchanged V3 validator; out-of-domain diagnostic.",
        "packages": {p: importlib.metadata.version(p)
                     for p in ("foundry-aws-gateway", "openai", "jsonschema")},
        "items": [], "status": "in_progress", "full128_started": False,
    }
    summary_path = folder / "results.json"
    runner.write_json(summary_path, summary)

    def run(case):
        target = folder / "runs" / case["id"]
        target.mkdir(parents=True, exist_ok=False)
        runtime = {k: case[k] for k in ("product_type", "scene_prompt")}
        runtime["image_stage"] = "scene_generation"
        for key in ("generated_image", "twin_image"):
            runtime[key] = case[key]["local_path"]
            if runner.sha(runtime[key]) != case[key]["sha256"]:
                raise ValueError("Frozen image bytes changed")
        runner.write_json(target / "input.json", runtime)
        try:
            return summarize(case, runner.judge(runtime, target), target)
        except Exception as exc:
            error = {"id": case["id"], "role": case["role"], "ok": False,
                     "error_type": type(exc).__name__, "checks": {},
                     "expectation": case["expectation"]}
            runner.write_json(target / "error.json", error)
            return error

    items = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(run, case): case for case in manifest["cases"]}
        for future in concurrent.futures.as_completed(futures):
            item = future.result()
            items[item["id"]] = item
            summary["items"] = [items[c["id"]] for c in manifest["cases"] if c["id"] in items]
            runner.write_json(summary_path, summary)
            print(json.dumps({key: item.get(key) for key in
                              ("id", "ok", "verdict", "score", "checks")}), flush=True)
    summary["finished_utc"] = datetime.now(timezone.utc).isoformat()
    summary["complete_count"] = sum(row["ok"] for row in summary["items"])
    summary["all_stated_checks_matched"] = (
        len(items) == 6 and all(item["ok"] and all(item["checks"].values()) for item in items.values()))
    summary["status"] = ("label_gate_matched_pending_evidence_review"
                         if summary["all_stated_checks_matched"] else "calibration_gate_not_met")
    summary["full128_authorized_by_gate"] = False
    summary["evidence_review_required_before_expansion"] = summary["all_stated_checks_matched"]
    runner.write_json(summary_path, summary)


if __name__ == "__main__":
    main()
