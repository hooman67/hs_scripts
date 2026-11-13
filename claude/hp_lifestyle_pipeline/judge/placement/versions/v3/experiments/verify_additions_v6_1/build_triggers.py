#!/usr/bin/env python3
"""Build comment-free verifier triggers from saved two-pass predictions."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


INPUT_KEYS = frozenset(
    {"generated_image", "twin_image", "product_type", "scene_prompt", "image_stage"}
)


def sha256(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def confirmed_material(component: Mapping[str, Any]) -> bool:
    return (
        component.get("visibility") in {"observed", "partial"}
        and component.get("confidence") in {"medium", "high"}
        and isinstance(component.get("severity"), int)
        and component["severity"] >= 2
    )


def baseline_reliable(component: Mapping[str, Any]) -> bool:
    return (
        component.get("visibility") in {"observed", "partial"}
        and component.get("confidence") in {"medium", "high"}
        and isinstance(component.get("severity"), int)
    )


def trigger_components(result: Mapping[str, Any]) -> list[str]:
    baseline = result["stages"]["baseline_v2"]["judgment"]["observation"]["components"]
    compact = result["stages"]["compact_v3"]["judgment"]["observation"]["components"]
    selected = []
    for name, proposal in compact.items():
        original = baseline[name]
        if confirmed_material(proposal) and (
            not baseline_reliable(original) or proposal["severity"] > original["severity"]
        ):
            selected.append(name)
    return selected


def build(source_runs: list[Path]) -> dict[str, Any]:
    records = []
    seen: set[str] = set()
    for source_run in source_runs:
        for result_path in sorted(source_run.glob("*/result.json")):
            result = json.loads(result_path.read_text(encoding="utf-8"))
            names = trigger_components(result)
            if not names:
                continue
            case_id = result["record_id"]
            if case_id in seen:
                raise ValueError(f"Duplicate triggered case: {case_id}")
            seen.add(case_id)
            compact_stage = result["stages"]["compact_v3"]
            request = json.loads(
                Path(compact_stage["artifacts"]["request"]["path"]).read_text(encoding="utf-8")
            )
            runtime_input = request["input"]
            if set(runtime_input) != INPUT_KEYS:
                raise ValueError(f"{case_id}: stage input whitelist changed")
            proposals = {
                name: compact_stage["judgment"]["observation"]["components"][name]
                for name in names
            }
            records.append(
                {
                    "id": case_id,
                    "source_dataset": source_run.name,
                    "runtime_input": runtime_input,
                    "images": request["images"],
                    "proposed_components": proposals,
                    "source_provenance": {
                        "combined_result_path": str(result_path.resolve()),
                        "combined_result_sha256": sha256(result_path),
                        "compact_raw_response": compact_stage["artifacts"]["raw_response"],
                        "compact_result": compact_stage["artifacts"]["result"],
                        "baseline_raw_response": result["stages"]["baseline_v2"]["artifacts"]["raw_response"],
                        "baseline_result": result["stages"]["baseline_v2"]["artifacts"]["result"],
                    },
                }
            )
    return {
        "schema_version": "placement-addition-verifier-triggers-v1",
        "trigger_policy": (
            "compact observed/partial medium/high-confidence severity>=2 and either "
            "baseline unassessable/low-confidence or compact severity above baseline"
        ),
        "source_runs": [str(path.resolve()) for path in source_runs],
        "expected_count": len(records),
        "expected_component_count": sum(len(r["proposed_components"]) for r in records),
        "comments_or_expectations_included": False,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-run", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"Output already exists: {output}")
    value = build([path.resolve() for path in args.source_run])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "cases": value["expected_count"], "components": value["expected_component_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
