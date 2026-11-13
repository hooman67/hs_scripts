"""One bounded, label-withheld assessment of each supplied C-Tech anchor."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path

import run_judge

ROOT = Path(__file__).resolve().parent


def material(component):
    return (component["severity"] is not None and component["severity"] >= 2
            and component["confidence"] in {"medium", "high"}
            and component["visibility"] in {"observed", "partial"})


def summarize(case, result):
    judgment = result["application_merged_judgment"]
    components = judgment["observation"]["components"]
    orientation = components["orientation_alignment"]
    geometry = components["scale_perspective"]
    checks = {
        "no_retired_chair_alignment_code": all(
            "chair_alignment_conflict" not in c["issue_codes"] for c in components.values()),
    }
    if case["id"] == "07_cashmere_x_Front_Wide_4":
        checks["required_laptop_table_alignment_failure"] = (
            result["final_decision"]["verdict"] == "fail" and material(orientation)
            and bool(set(orientation["issue_codes"]) & {"furniture_axis_conflict", "corner_facing"}))
    else:
        # This is not a global positive label; unrelated component findings remain intact.
        checks["no_material_orientation_failure"] = not material(orientation)
        checks["no_material_access_failure"] = not material(components["access_usability"])
        checks["no_material_support_scenario_failure"] = not material(components["support_scenario"])
    if case["id"] == "13_elitebook_13_Front_Left_Medium_4":
        checks["required_table_geometry_failure"] = (
            result["final_decision"]["verdict"] == "fail" and material(geometry)
            and "malformed_support_furniture" in geometry["issue_codes"])
    return {
        "id": case["id"], "variant": case["variant"],
        "source_url": case["generated_image"]["url"],
        "verdict": result["final_decision"]["verdict"],
        "score": judgment["natural_placement_score"],
        "checks": checks, "components": components,
        "triggered_components": result["triggered_components"],
        "consensus_resolution": result["consensus_resolution"],
        "label_scope": "User-provided dimension labels, not global positives or held-out accuracy.",
        "assessment_scope_caveat": (
            "Absence-of-material placement checks are conservative diagnostics. Inspect evidence "
            "before attributing any unrelated support/access finding specifically to chair pose."),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-name", required=True)
    args = parser.parse_args()
    if not args.run_name.replace("_", "").replace("-", "").isalnum():
        raise ValueError("Invalid run name")
    output = ROOT / "calibration" / args.run_name
    output.mkdir(parents=True, exist_ok=False)
    manifest_path = ROOT / "sources/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    items = []
    summary = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "method": "Each of three supplied anchors once; no semantic retry or preferred-response selection.",
        "development_only": True, "target_labels_withheld": True,
        "source_stage": "e2e_comparison_output",
        "runtime_stage_adapter": "scene_generation literal for unchanged V3 validator; out-of-domain diagnostic.",
        "protocol_freeze_sha256": run_judge.verify_freeze(),
        "manifest_sha256": run_judge.sha(manifest_path),
        "packages": {p: importlib.metadata.version(p)
                     for p in ("foundry-aws-gateway", "openai", "jsonschema")},
        "items": items,
    }
    run_judge.write_json(output / "summary.json", summary)
    for case in manifest["cases"]:
        case_dir = output / case["id"]
        case_dir.mkdir()
        runtime = {k: case[k] for k in ("product_type", "scene_prompt")}
        runtime["image_stage"] = "scene_generation"
        for key in ("generated_image", "twin_image"):
            runtime[key] = case[key]["local_path"]
            if run_judge.sha(runtime[key]) != case[key]["sha256"]:
                raise ValueError("Source anchor bytes changed")
        run_judge.write_json(case_dir / "input.json", runtime)
        try:
            result = run_judge.judge(runtime, case_dir)
            item = {"ok": True, **summarize(case, result),
                    "result_path": str(case_dir / "result.json"),
                    "result_sha256": run_judge.sha(case_dir / "result.json")}
        except Exception as exc:
            item = {"id": case["id"], "ok": False, "error_type": type(exc).__name__}
            run_judge.write_json(case_dir / "error.json", item)
        items.append(item)
        run_judge.write_json(output / "summary.json", summary)
        print(json.dumps({k: item.get(k) for k in ("id", "ok", "verdict", "score", "checks")}), flush=True)
    summary["finished_utc"] = datetime.now(timezone.utc).isoformat()
    summary["completed"] = all(i["ok"] for i in items)
    summary["all_stated_checks_matched"] = summary["completed"] and all(
        all(i["checks"].values()) for i in items)
    run_judge.write_json(output / "summary.json", summary)
    if not summary["completed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
