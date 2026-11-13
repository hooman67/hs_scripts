#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml", "tomli", "jsonschema"]
# ///
"""Build normalized sidecars for preserved V4 records without modifying raw bytes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_gpt55 import (HERE, V4, derive_artifacts, load_registry, rebuild_accepted,
                       sha_bytes, sha_obj)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append")
    parser.add_argument("--all-current", action="store_true")
    parser.add_argument("--sample", default="sample_003")
    args = parser.parse_args()
    manifest = json.loads((HERE / "manifest.json").read_text())
    cases = {c["case_id"]: c for c in manifest["cases"]}
    schema = json.loads((V4 / "output.schema.json").read_text())
    registry = load_registry(V4 / "camera_profiles.json")
    settings = {"model": "gpt-5.5", "reasoning_effort": "medium", "max_completion_tokens": 24000}
    results = []
    case_ids = sorted(cases) if args.all_current else (args.case or [])
    if not case_ids:
        parser.error("--case or --all-current is required")
    for case_id in case_ids:
        case = cases[case_id]
        expected_request = sha_obj({"system_sha256": manifest["provenance"]["system_prompt"]["sha256"],
                                    "schema": schema, "settings": settings,
                                    "input_sha256": case["input_sha256"]})
        if args.all_current:
            matches = []
            for candidate in sorted((HERE / "records/attempts" / case_id).glob("sample_[0-9][0-9][0-9].json")):
                value = json.loads(candidate.read_text())
                if value.get("request_sha256") == expected_request and value.get("parsed_output") is not None:
                    matches.append((candidate, value))
            if not matches:
                raise RuntimeError(f"no completed current request: {case_id}")
            path, record = matches[-1]
        else:
            path = HERE / "records/attempts" / case_id / f"{args.sample}.json"
            record = json.loads(path.read_text())
        before = sha_bytes(path.read_bytes())
        if record.get("request_sha256") != expected_request:
            raise RuntimeError(f"request provenance mismatch: {case_id}/{args.sample}")
        result = derive_artifacts(case_id, path, record, json.loads(record["raw_input_json"]),
                                  schema, registry, expected_request)
        after = sha_bytes(path.read_bytes())
        if before != after:
            raise RuntimeError(f"raw record changed: {case_id}/{args.sample}")
        results.append({"case_id": case_id, "sample": path.stem,
                        "raw_record_sha256": before, **result})
    accepted = rebuild_accepted(manifest)
    print(json.dumps({"results": results, "accepted_counts": accepted["counts"]}, indent=2))


if __name__ == "__main__":
    main()

