#!/usr/bin/env python3
"""Sequential, resumable V4.3.1 runner for the five cases after the frozen canary."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from run_judge import atomic_json, judge

CANARY_RECORD_ID = "elitebook__laptop_FrontLeftMedium__p1"


def load_plan(manifest_path: Path) -> tuple[list[dict], list[dict]]:
    manifest = json.loads(manifest_path.read_text())
    all_records = manifest["records"]
    if [row["record_id"] for row in all_records].count(CANARY_RECORD_ID) != 1:
        raise ValueError("full six-case manifest must contain the frozen canary exactly once")
    remaining = [row for row in all_records if row["record_id"] != CANARY_RECORD_ID]
    if len(all_records) != 6 or len(remaining) != 5:
        raise ValueError("expected six original records and five remaining records")
    # All original six targets participate in anchor exclusion for every remaining call.
    exclusion_targets = [row["runtime_input"] for row in all_records]
    return remaining, exclusion_targets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model", default="gpt-5.5")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    output = Path(args.output_dir)
    records, exclusion_targets = load_plan(manifest_path)
    output.mkdir(parents=True, exist_ok=True)
    progress_path = output / "progress.json"
    progress = json.loads(progress_path.read_text()) if progress_path.exists() else {
        "schema_version": "hp-placement-v4.3.1-remaining-five-progress-v1",
        "manifest": str(manifest_path.resolve()),
        "model": args.model,
        "canary_record_id": CANARY_RECORD_ID,
        "anchor_exclusion_record_ids": [row.get("target_record_id") for row in exclusion_targets],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "records": [{"record_id": row["record_id"], "status": "pending"} for row in records],
    }
    atomic_json(progress_path, progress)
    by_id = {row["record_id"]: row for row in progress["records"]}

    for row in records:
        item = by_id[row["record_id"]]
        if item["status"] == "done":
            continue
        item.update(status="running", started_at=datetime.now(timezone.utc).isoformat())
        atomic_json(progress_path, progress)
        result = judge(
            row["runtime_input"],
            output / row["record_id"],
            model=args.model,
            exclusion_targets=exclusion_targets,
        )
        item.update(
            status="done",
            finished_at=datetime.now(timezone.utc).isoformat(),
            result_status=result["status"],
            verdict=(result.get("derived") or {}).get("verdict"),
        )
        atomic_json(progress_path, progress)

    progress["finished_at"] = datetime.now(timezone.utc).isoformat()
    atomic_json(progress_path, progress)


if __name__ == "__main__":
    main()
