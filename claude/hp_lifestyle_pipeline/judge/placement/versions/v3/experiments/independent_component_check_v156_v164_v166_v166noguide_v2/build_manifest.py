#!/usr/bin/env python3
"""Build a names-only component-check manifest from one frozen trigger set."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

INPUT_KEYS = frozenset(
    {"generated_image", "twin_image", "product_type", "scene_prompt", "image_stage"}
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triggers", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.triggers.resolve()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"Output exists: {output}")
    payload = json.loads(source.read_text(encoding="utf-8"))
    records = []
    for trigger in payload["records"]:
        runtime_input = trigger["runtime_input"]
        if set(runtime_input) != INPUT_KEYS:
            raise ValueError(f"{trigger['id']}: runtime input whitelist changed")
        names = sorted(trigger["proposed_components"])
        if not names:
            raise ValueError(f"{trigger['id']}: no requested components")
        images = {}
        for key in ("generated_image", "twin_image"):
            path = Path(runtime_input[key]).resolve()
            expected = trigger["images"][key]["sha256"]
            actual = sha256(path)
            if actual != expected:
                raise ValueError(f"{trigger['id']}: {key} hash mismatch")
            images[key] = {"path": str(path), "sha256": actual}
        records.append(
            {
                "id": trigger["id"],
                "cohort": "requested_e2e_comparison_diagnostic",
                "evaluation_status": "out_of_domain_e2e_diagnostic",
                "runtime_input": runtime_input,
                "requested_component_names": names,
                "images": images,
                "source_trigger": {"path": str(source), "sha256": sha256(source)},
            }
        )
    expected = payload["expected_count"]
    if len(records) != expected:
        raise ValueError(f"expected {expected} records, found {len(records)}")
    value = {
        "schema_version": "placement-independent-component-check-input-v1",
        "protocol_version": "placement-independent-component-check-v1",
        "input_whitelist": sorted(INPUT_KEYS),
        "comments_proposals_codes_severities_or_prior_verdicts_included": False,
        "expected_count": len(records),
        "expected_component_count": sum(
            len(record["requested_component_names"]) for record in records
        ),
        "source_trigger": {"path": str(source), "sha256": sha256(source)},
        "records": records,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output),
                "cases": len(records),
                "components": value["expected_component_count"],
                "sha256": sha256(output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
