"""Bounded, identity-checked candidate evaluations without target labels."""

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import common
import openai
import p1
import p2
from jsonschema.exceptions import ValidationError


def material(component):
    return (
        component["visibility"] in {"observed", "partial"}
        and component["severity"] is not None
        and component["severity"] >= 2
        and component["confidence"] in {"medium", "high"}
    )


def calibration_checks(case, result):
    components = result["application_merged_judgment"]["observation"]["components"]
    checks = {}
    for name, expectation in case["expectation"].items():
        component = components[name]
        if expectation == "unlabeled":
            continue
        if expectation in ("no_material_defect", "no_new_material_defect"):
            checks[name + ":" + expectation] = not material(component)
        elif expectation.startswith("appearance_"):
            code = {
                "appearance_furniture_axis_conflict": "furniture_axis_conflict",
                "appearance_malformed_support_furniture": "malformed_support_furniture",
            }[expectation]
            checks[name + ":" + expectation] = (
                component["visibility"] in {"observed", "partial"}
                and component["severity"] is not None
                and component["severity"] >= 1
                and code in component["issue_codes"]
                and result["application_merged_judgment"]["natural_placement_score"]
                < 100
            )
        else:
            code = {
                "material_furniture_axis_conflict": "furniture_axis_conflict",
                "material_malformed_support_furniture": "malformed_support_furniture",
            }[expectation]
            checks[name + ":" + expectation] = (
                material(component)
                and code in component["issue_codes"]
                and result["final_decision"]["verdict"] == "fail"
            )
    checks["no_retired_chair_code"] = all(
        "chair_alignment_conflict" not in component["issue_codes"]
        for component in components.values()
    )
    return checks


def assess(case, candidate, root):
    output = root / candidate / case["id"]
    runtime = {name: case[name] for name in ("product_type", "scene_prompt")}
    runtime["image_stage"] = "scene_generation"
    for name in ("generated_image", "twin_image"):
        runtime[name] = case[name]["local_path"]
        if common.sha(runtime[name]) != case[name]["sha256"]:
            raise ValueError(f"Source bytes changed: {case['id']} / {name}")
    common.write_json(output / "input.json", runtime)
    metadata = {
        key: case[key]
        for key in (
            "id",
            "product_type",
            "source_row_id",
            "variant",
            "generated_image",
            "twin_image",
        )
        if key in case
    }
    try:
        result = {"p1": p1, "p2": p2}[candidate].judge(runtime, output)
        row = {
            **metadata,
            "candidate": candidate,
            "status": "complete",
            "verdict": result["final_decision"]["verdict"],
            "score": result["application_merged_judgment"]["natural_placement_score"],
            "observation": result["application_merged_judgment"]["observation"],
            "result_path": str((output / "result.json").resolve()),
            "result_sha256": common.sha(output / "result.json"),
            "checks": calibration_checks(case, result)
            if "expectation" in case
            else None,
        }
    except (ValueError, RuntimeError, openai.APIError, ValidationError) as error:
        row = {
            **metadata,
            "candidate": candidate,
            "status": "error",
            "verdict": None,
            "score": None,
            "observation": None,
            "error_type": type(error).__name__,
            "error": str(error)
            if isinstance(error, ValueError)
            else "See preserved stage error/stream.",
            "checks": None,
        }
    common.write_json(output / "assessment.json", row)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset", choices=("calibration", "historical", "ctech"), required=True
    )
    parser.add_argument("--candidate", choices=("p1", "p2", "both"), default="both")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        raise ValueError("Use1-8 bounded image workers")
    source = (
        common.ROOT / "calibration_manifest.json"
        if args.dataset == "calibration"
        else common.ROOT / "evaluation/ctech/corpus.json"
        if args.dataset == "ctech"
        else common.R1 / "evaluation/inventory.json"
    )
    document = json.loads(source.read_text())
    cases = document["cases" if args.dataset == "calibration" else "records"]
    candidates = ("p1", "p2") if args.candidate == "both" else (args.candidate,)
    root = common.ROOT / "evaluation" / args.dataset
    frozen = common.verify_freeze()
    rows = []
    summary = {
        "source": str(source),
        "source_sha256": common.sha(source),
        "protocol_freeze_sha256": frozen,
        "candidates": candidates,
        "expected": len(cases) * len(candidates),
        "source_stage": "scene_generation"
        if args.dataset == "ctech"
        else "e2e_comparison_output",
        "runtime_stage_adapter": "scene_generation literal; not held-out scene-stage accuracy",
        "target_labels_withheld": True,
        "actual_judge_model": common.MODEL,
        "semantic_samples_per_candidate_revision_case": 1,
        "records": rows,
    }
    common.write_json(root / "summary.json", summary)
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        jobs = {
            executor.submit(assess, case, candidate, root): (case, candidate)
            for case in cases
            for candidate in candidates
        }
        for future in as_completed(jobs):
            row = future.result()
            rows.append(row)
            rows.sort(key=lambda value: (value["id"], value["candidate"]))
            common.write_json(root / "summary.json", summary)
            print(
                json.dumps(
                    {
                        key: row.get(key)
                        for key in (
                            "id",
                            "candidate",
                            "status",
                            "verdict",
                            "score",
                            "checks",
                            "error_type",
                            "error",
                        )
                    }
                ),
                flush=True,
            )
    summary["complete"] = all(row["status"] == "complete" for row in rows)
    summary["all_stated_checks_matched"] = (
        None
        if args.dataset == "ctech"
        else summary["complete"]
        and all(
            all(row["checks"].values()) for row in rows if row["checks"] is not None
        )
    )
    if args.dataset == "ctech":
        summary["ctech_feedback_coverage_audited"] = False
    common.write_json(root / "summary.json", summary)
    if not summary["complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
