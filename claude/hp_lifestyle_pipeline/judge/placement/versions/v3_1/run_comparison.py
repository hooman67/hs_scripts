"""Fresh, resumable V3/V3.1 evaluation of every output in the supplied historical viewer."""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import threading
from datetime import datetime, timezone
from pathlib import Path

import run_judge as updated
import frozen_v3

ROOT = Path(__file__).resolve().parent
ANCHORS = {"07_cashmere_x_Front_Wide_1", "07_cashmere_x_Front_Wide_4",
           "13_elitebook_13_Front_Left_Medium_4"}
WRITE_LOCK = threading.Lock()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers-per-version", type=int, default=4, choices=range(1, 5))
    args = parser.parse_args()
    folder = ROOT / "evaluation"
    inventory = json.loads((folder / "inventory.json").read_text())
    records = sorted(inventory["records"], key=lambda r: (r["id"] not in ANCHORS, r["id"]))
    status_path = folder / "progress.json"
    if status_path.exists():
        progress = json.loads(status_path.read_text())
        if progress["protocol_freeze_sha256"] != updated.verify_freeze():
            raise RuntimeError("Resume protocol mismatch")
        # Completed and failed cases are both terminal. No resampling failed model judgments.
        completed = {(r["version"], r["id"]) for r in progress["items"]}
    else:
        progress = {
            "started_utc": datetime.now(timezone.utc).isoformat(),
            "protocol_freeze_sha256": updated.verify_freeze(),
            "inventory_sha256": updated.sha(folder / "inventory.json"),
            "scope": "User-authorized fresh V3 and V3.1 on historical supplied viewer only.",
            "workers_per_version": args.workers_per_version,
            "expected_output_count_per_version": len(records), "items": [],
        }
        completed = set()
        updated.write_json(status_path, progress)

    def run(version, record):
        case_dir = folder / "runs" / version / record["id"]
        case_dir.mkdir(parents=True, exist_ok=True)
        runtime = {k: record[k] for k in ("product_type", "scene_prompt")}
        runtime["image_stage"] = "scene_generation"
        for key in ("generated_image", "twin_image"):
            runtime[key] = record[key]["local_path"]
            if updated.sha(runtime[key]) != record[key]["sha256"]:
                raise ValueError("Frozen comparison image bytes changed")
        updated.write_json(case_dir / "input.json", runtime)
        try:
            result_path = case_dir / "result.json"
            if result_path.exists():
                # Resume a saved success, never request a replacement judgment.
                result = json.loads(result_path.read_text())
                if (not result["ok"] or result["runtime_input"] != runtime
                        or result["protocol_freeze_sha256"] != updated.verify_freeze()):
                    raise ValueError("Incompatible preserved ensemble")
            elif (case_dir / "error.json").exists():
                raise RuntimeError("Preserved terminal failure; not resampling")
            elif version == "v3":
                result = frozen_v3.judge(runtime, case_dir)
            else:
                result = updated.judge(runtime, case_dir)
            item = {"version": version, "id": record["id"], "ok": True,
                    "verdict": result["final_decision"]["verdict"],
                    "score": result["application_merged_judgment"]["natural_placement_score"],
                    "result_path": str(result_path), "result_sha256": updated.sha(result_path)}
        except Exception as exc:
            item = {"version": version, "id": record["id"], "ok": False,
                    "error_type": type(exc).__name__, "status_code": getattr(exc, "status_code", None),
                    "case_directory": str(case_dir)}
            updated.write_json(case_dir / "error.json", item)
        with WRITE_LOCK:
            progress["items"].append(item)
            updated.write_json(status_path, progress)
            print(json.dumps({**item, "completed": len(progress["items"]),
                              "expected": len(records) * 2}), flush=True)

    # Separate pools keep each version within V3's maximum four case workers.
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers_per_version) as v3_pool, \
            concurrent.futures.ThreadPoolExecutor(max_workers=args.workers_per_version) as v31_pool:
        futures = []
        for record in records:
            for version, pool in (("v3", v3_pool), ("v3_1", v31_pool)):
                if (version, record["id"]) not in completed:
                    futures.append(pool.submit(run, version, record))
        for future in concurrent.futures.as_completed(futures):
            future.result()
    progress["finished_utc"] = datetime.now(timezone.utc).isoformat()
    progress["completed"] = len(progress["items"]) == len(records) * 2
    progress["errors"] = sum(not r["ok"] for r in progress["items"])
    updated.write_json(status_path, progress)
    if progress["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
