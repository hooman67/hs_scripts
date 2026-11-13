#!/usr/bin/env python3
"""Build the ten-case, names-only independent component-check manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


INPUT_KEYS = frozenset({"generated_image", "twin_image", "product_type", "scene_prompt", "image_stage"})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--development-triggers", type=Path, required=True)
    parser.add_argument("--new160-triggers", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Output exists: {args.output}")
    sources = [
        ("prior_development_trigger", args.development_triggers.resolve()),
        ("root_inspected_development_probe_not_heldout", args.new160_triggers.resolve()),
    ]
    records = []
    seen = set()
    for cohort, source_path in sources:
        source = json.loads(source_path.read_text(encoding="utf-8"))
        for record in source["records"]:
            record_id = record["id"]
            if record_id in seen:
                raise ValueError(f"Duplicate case across cohorts: {record_id}")
            seen.add(record_id)
            runtime_input = record["runtime_input"]
            if set(runtime_input) != INPUT_KEYS:
                raise ValueError(f"{record_id}: runtime input whitelist changed")
            names = list(record["proposed_components"])
            if not names or len(names) != len(set(names)):
                raise ValueError(f"{record_id}: invalid requested component names")
            images = {}
            for key in ("generated_image", "twin_image"):
                path = Path(runtime_input[key]).resolve()
                expected = record["images"][key]["sha256"]
                actual = sha256(path)
                if actual != expected:
                    raise ValueError(f"{record_id}: {key} hash mismatch")
                images[key] = {"path": str(path), "sha256": actual}
            records.append({
                "id": record_id,
                "cohort": cohort,
                "evaluation_status": "development_probe_not_heldout" if cohort.startswith("root_inspected") else "prior_development_probe",
                "runtime_input": runtime_input,
                "requested_component_names": names,
                "images": images,
                "source_trigger": {"path": str(source_path), "sha256": sha256(source_path)},
            })
    if len(records) != 10:
        raise ValueError(f"Expected exactly 10 cases, found {len(records)}")
    value = {
        "schema_version": "placement-independent-component-check-input-v1",
        "protocol_version": "placement-independent-component-check-v1",
        "input_whitelist": sorted(INPUT_KEYS),
        "comments_proposals_codes_severities_or_prior_verdicts_included": False,
        "expected_count": 10,
        "expected_component_count": sum(len(record["requested_component_names"]) for record in records),
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output.resolve()), "cases": len(records), "components": value["expected_component_count"], "sha256": sha256(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
