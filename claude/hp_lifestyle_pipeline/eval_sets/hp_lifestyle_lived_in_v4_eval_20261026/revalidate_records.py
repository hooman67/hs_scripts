#!/usr/bin/env python3
"""Revalidate preserved parsed outputs offline without modifying raw attempt records."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
V4 = ROOT / "research/source_messaging_v1_to_v6/versions/v4"
sys.path.insert(0, str(V4 / "scripts"))
from camera_profile_resolver import load_registry  # noqa: E402
from validate_output import validate_output  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append")
    args = parser.parse_args()
    schema_path = V4 / "output.schema.json"
    schema = json.loads(schema_path.read_text())
    registry = load_registry(V4 / "camera_profiles.json")
    output_dir = HERE / "validation/revalidation"
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = []
    for record_path in sorted((HERE / "records/attempts").glob("*/sample_[0-9][0-9][0-9].json")):
        case_id = record_path.parent.name
        if args.case and case_id not in args.case:
            continue
        record = json.loads(record_path.read_text())
        if "parsed_output" not in record:
            continue
        result = validate_output(record["parsed_output"], json.loads(record["raw_input_json"]), schema, registry)
        result.update({"version": "v4-offline-validator-2026-10-26-v1",
                       "case_id": case_id, "record_path": str(record_path),
                       "record_sha256": sha(record_path), "raw_record_unchanged": True,
                       "output_schema_sha256": sha(schema_path)})
        target = output_dir / f"{case_id}__{record_path.stem}.json"
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        summary.append({"case_id": case_id, "sample": record_path.stem,
                        "passed": result["passed"], "errors": result["error_count"],
                        "warnings": result["warning_count"], "path": str(target)})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

