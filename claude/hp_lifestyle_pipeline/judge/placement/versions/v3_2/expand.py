"""Expand frozen candidates, reusing exact calibration results without resampling."""

import argparse
import fcntl
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from importlib.metadata import version as package_version
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version-root", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    version = args.version_root.resolve()
    if (
        version.parent != Path(__file__).resolve().parent.parent
        or not 1 <= args.workers <= 8
    ):
        raise ValueError("Use a sibling frozen version and1-8 bounded workers")
    sys.path[0] = str(version)
    import common
    import evaluate

    frozen = common.verify_freeze()
    lock = (version / "evaluation/expansion.lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    common.write_json(
        version / "evaluation/expansion_run.json",
        {
            "started_utc": datetime.now(UTC).isoformat(),
            "runner_sha256": common.sha(__file__),
            "version_root": str(version),
            "protocol_freeze_sha256": frozen,
            "workers": args.workers,
            "actual_judge_model": common.MODEL,
            "packages": {
                name: package_version(name)
                for name in ("openai", "foundry-aws-gateway", "jsonschema")
            },
            "exact_calibration_reuse": True,
        },
    )
    calibration = json.loads(
        (version / "evaluation/calibration/summary.json").read_text()
    )
    if len(calibration["records"]) != 12:
        raise ValueError("Finish both six-case calibrations before expanding")
    inventory = json.loads((common.R1 / "evaluation/inventory.json").read_text())
    corpus = json.loads((version / "evaluation/refiner/corpus.json").read_text())
    sources = {"historical": inventory["records"], "refiner": corpus["records"]}
    summaries = {
        dataset: {
            "expected": len(cases) * 2,
            "records": [],
            "actual_judge_model": common.MODEL,
            "protocol_freeze_sha256": frozen,
            "development_only": True,
            "target_labels_withheld": True,
            "semantic_samples_per_candidate_revision_case": 1,
            "source_stage": (
                "e2e_comparison_output"
                if dataset == "historical"
                else "64 scene-generation baselines +17 refiner edits; passthroughs deduplicated"
            ),
            "source_manifest_sha256": common.sha(
                common.R1 / "evaluation/inventory.json"
                if dataset == "historical"
                else version / "evaluation/refiner/corpus.json"
            ),
        }
        for dataset, cases in sources.items()
    }
    for dataset, summary in summaries.items():
        common.write_json(version / "evaluation" / dataset / "summary.json", summary)
    print(
        json.dumps(
            {
                "started": True,
                "version": version.name,
                "model": common.MODEL,
                "workers": args.workers,
                "expected": sum(item["expected"] for item in summaries.values()),
                "exact_calibration_results_will_be_reused": True,
            }
        ),
        flush=True,
    )

    def job(dataset, case, candidate):
        root = version / "evaluation" / dataset
        expected_runtime = {
            "generated_image": case["generated_image"]["local_path"],
            "twin_image": case["twin_image"]["local_path"],
            "scene_prompt": case["scene_prompt"],
            "product_type": case["product_type"],
            "image_stage": "scene_generation",
        }
        paths = [root / candidate / case["id"] / "assessment.json"]
        if dataset == "historical":
            paths.append(
                version
                / "evaluation/calibration"
                / candidate
                / case["id"]
                / "assessment.json"
            )
        for path in paths:
            if not path.exists():
                continue
            row = json.loads(path.read_text())
            if (
                row["id"] != case["id"]
                or row["candidate"] != candidate
                or any(
                    row[role]["sha256"] != case[role]["sha256"]
                    for role in ("generated_image", "twin_image")
                )
            ):
                raise ValueError("Prior assessment belongs to another case/candidate")
            if json.loads((path.parent / "input.json").read_text()) != expected_runtime:
                raise ValueError(
                    "Prior calibration context differs from expanded input"
                )
            if row["status"] == "complete":
                if common.sha(row["result_path"]) != row["result_sha256"]:
                    raise ValueError("Prior immutable result changed")
                result = json.loads(Path(row["result_path"]).read_text())
                if result["protocol_freeze_sha256"] != frozen:
                    raise ValueError("Prior result belongs to another protocol")
            elif row["status"] != "error":
                raise ValueError("Existing assessment is non-terminal")
            return {**row, "reused_from": str(path.resolve())}
        return evaluate.assess(case, candidate, root)

    completed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(job, dataset, case, candidate): dataset
            for dataset, cases in sources.items()
            for case in cases
            for candidate in ("p1", "p2")
        }
        for future in as_completed(futures):
            dataset = futures[future]
            row = future.result()
            summary = summaries[dataset]
            summary["records"].append(row)
            summary["records"].sort(key=lambda value: (value["id"], value["candidate"]))
            common.write_json(
                version / "evaluation" / dataset / "summary.json", summary
            )
            completed += 1
            if completed % 10 == 0 or row["status"] == "error":
                print(
                    json.dumps(
                        {
                            "completed": completed,
                            "expected": sum(
                                item["expected"] for item in summaries.values()
                            ),
                            "dataset": dataset,
                            "id": row["id"],
                            "candidate": row["candidate"],
                            "status": row["status"],
                            "verdict": row["verdict"],
                        }
                    ),
                    flush=True,
                )
    for dataset, summary in summaries.items():
        summary["complete"] = all(
            row["status"] == "complete" for row in summary["records"]
        )
        summary["terminal"] = len(summary["records"]) == summary["expected"]
        common.write_json(version / "evaluation" / dataset / "summary.json", summary)
    print(
        json.dumps(
            {
                dataset: {
                    "terminal": item["terminal"],
                    "complete": item["complete"],
                    "completed": len(item["records"]),
                }
                for dataset, item in summaries.items()
            }
        ),
        flush=True,
    )
    lock.close()


if __name__ == "__main__":
    main()
