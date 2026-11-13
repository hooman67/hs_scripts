#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests"]
# ///
"""Run the frozen names-only checks for this comparison campaign."""

from __future__ import annotations

import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from run_check import (
    FREEZE_PATH,
    MANIFEST_PATH,
    RUNS_ROOT,
    atomic_json,
    ensure_frozen,
    run,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--model", default="gpt-5.5")
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 3:
        raise SystemExit("workers must be between 1 and 3")
    ensure_frozen()
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    records = payload["records"]
    if len(records) != payload["expected_count"]:
        raise SystemExit("Input manifest count mismatch")
    components = sum(len(record["requested_component_names"]) for record in records)
    if components != payload["expected_component_count"]:
        raise SystemExit("Input manifest component count mismatch")
    run_dir = RUNS_ROOT / args.run_name
    if run_dir.exists():
        raise SystemExit(f"Run exists: {run_dir}")
    run_dir.mkdir(parents=True)
    statuses = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run, record, run_dir / record["id"], args.model): record["id"]
            for record in records
        }
        for future in as_completed(futures):
            result = future.result()
            statuses.append(result.get("ok") is True)
            print(json.dumps({"id": futures[future], "ok": result.get("ok")}), flush=True)
    summary = {
        "schema_version": "placement-independent-component-check-run-v1",
        "freeze_sha256": hashlib.sha256(FREEZE_PATH.read_bytes()).hexdigest(),
        "manifest_sha256": hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
        "records": len(records),
        "components": components,
        "ok": sum(statuses),
        "errors": len(statuses) - sum(statuses),
    }
    atomic_json(run_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    return 0 if all(statuses) else 1


if __name__ == "__main__":
    raise SystemExit(main())
