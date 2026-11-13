#!/usr/bin/env python3
"""Sequential, resumable V4.2 batch runner."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from run_judge import judge, atomic_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model", default="gpt-6-astra")
    args = parser.parse_args()
    manifest_path, output = Path(args.manifest), Path(args.output_dir)
    manifest = json.loads(manifest_path.read_text())
    records = manifest["records"]
    runtimes = [r["runtime_input"] for r in records]
    output.mkdir(parents=True, exist_ok=True)
    progress_path = output / "progress.json"
    progress = json.loads(progress_path.read_text()) if progress_path.exists() else {
        "schema_version": "hp-placement-v4.2-batch-progress-v1", "manifest": str(manifest_path.resolve()),
        "model": args.model, "started_at": datetime.now(timezone.utc).isoformat(),
        "records": [{"record_id": r["record_id"], "status": "pending"} for r in records],
    }
    atomic_json(progress_path, progress)
    by_id = {r["record_id"]: r for r in progress["records"]}
    for row in records:
        item = by_id[row["record_id"]]
        if item["status"] == "done":
            continue
        item.update(status="running", started_at=datetime.now(timezone.utc).isoformat())
        atomic_json(progress_path, progress)
        result = judge(row["runtime_input"], output / row["record_id"], model=args.model, exclusion_targets=runtimes)
        item.update(status="done", finished_at=datetime.now(timezone.utc).isoformat(), result_status=result["status"], verdict=(result.get("derived") or {}).get("verdict"))
        atomic_json(progress_path, progress)
    progress["finished_at"] = datetime.now(timezone.utc).isoformat()
    atomic_json(progress_path, progress)


if __name__ == "__main__":
    main()
