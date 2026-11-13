# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests"]
# ///
"""Run the frozen addition-verifier trigger manifest."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from run_verifier import FREEZE_PATH, RUNS_ROOT, TRIGGER_PATH, ensure_frozen, verify


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--model", default="gpt-5.5")
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 3:
        raise SystemExit("workers must be between 1 and 3")
    ensure_frozen()
    payload = json.loads(TRIGGER_PATH.read_text(encoding="utf-8"))
    records = payload["records"]
    if len(records) != payload["expected_count"] or sum(len(r["proposed_components"]) for r in records) != payload["expected_component_count"]:
        raise SystemExit("Trigger manifest count mismatch")
    run_dir = RUNS_ROOT / args.run_name
    if run_dir.exists():
        raise SystemExit(f"Run exists: {run_dir}")
    run_dir.mkdir(parents=True)
    statuses = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(verify, record, run_dir / record["id"], args.model): record["id"] for record in records}
        for future in as_completed(futures):
            result = future.result()
            statuses.append(result.get("ok") is True)
            print(json.dumps({"id": futures[future], "ok": result.get("ok")}), flush=True)
    summary = {"schema_version": "placement-addition-verifier-run-v1", "freeze_sha256": __import__("hashlib").sha256(FREEZE_PATH.read_bytes()).hexdigest(), "records": len(records), "components": payload["expected_component_count"], "ok": sum(statuses), "errors": len(statuses)-sum(statuses)}
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))
    return 0 if all(statuses) else 1


if __name__ == "__main__":
    raise SystemExit(main())
