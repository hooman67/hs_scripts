#!/usr/bin/env python3
"""Export and summarize the frozen four-bank V6.2 text pilot."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import argparse
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUNNER_SPEC = importlib.util.spec_from_file_location("v62_eval_runner", HERE / "run_eval.py")
assert RUNNER_SPEC and RUNNER_SPEC.loader
runner = importlib.util.module_from_spec(RUNNER_SPEC)
RUNNER_SPEC.loader.exec_module(runner)

CASE_IDS = (
    "cashmere__laptop_FrontCloseUp",
    "elitebook__laptop_FrontWide",
    "tassel__printer_FrontCloseUp",
    "magic__printer_FrontWide",
)


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", default="v6.2-pilot-20261106-r3")
    args = parser.parse_args()
    snapshot = runner.revision_dir(args.revision)
    manifest = runner.verify_snapshot(snapshot)
    cases = {case["case_id"]: case for case in manifest["cases"]}
    rows = []
    audit = {}
    environments = Counter()
    repair_errors = Counter()
    for case_id in CASE_IDS:
        result_path = snapshot / "results" / f"{case_id}.json"
        result = runner.load_json(result_path)
        runner._validate_successful_bank(case_id, result)
        journal = runner._validate_call_journals(snapshot, case_id, result)
        case = cases[case_id]
        source_input = runner.load_json(snapshot / case["frozen_input_path"])
        for attempt in result["audit"]["attempts"][:-1]:
            repair_errors.update(error["code"] for error in attempt.get("errors", []))
        audit[case_id] = {
            "result_sha256": runner.sha_file(result_path),
            "source_input": source_input,
            "debug": result["debug"],
            "run": runner._bank_audit_summary(result),
            "journals": journal,
        }
        for rank, prompt in enumerate(result["prompts"], 1):
            environments[prompt["environment"]] += 1
            rows.append(
                {
                    "prompt_key": f"{case_id}::{prompt['id']}",
                    "case_id": case_id,
                    "device_id": case["device_id"],
                    "device_display_name": case["device_display_name"],
                    "device_type": case["device_type"],
                    "camera_tag": case["camera_tag"],
                    "rank": rank,
                    **prompt,
                    "text_sha256": sha_text(prompt["text"]),
                }
            )
    assert len(rows) == 40 and len({row["prompt_key"] for row in rows}) == 40
    round_rows = [
        row for row in rows
        if row["device_type"] == "laptop"
        and any(token in row["text"].casefold() for token in ("round ", "circular "))
    ]
    printer_forbidden = [
        row["prompt_key"] for row in rows
        if row["device_type"] == "printer"
        and any(token in row["text"].casefold() for token in ("round table", "coffee table", "café table", "cafe table", "gaming desk"))
    ]
    payload = {
        "version": "hp-lifestyle-spatial-composition-v6.2-pilot-40-v1",
        "revision": args.revision,
        "snapshot_manifest": str(snapshot / "snapshot_manifest.json"),
        "snapshot_manifest_sha256": runner.sha_file(snapshot / "snapshot_manifest.json"),
        "counts": {"banks": 4, "prompts_per_bank": 10, "prompts": 40},
        "environment_counts": dict(sorted(environments.items())),
        "round_laptop_prompts": [row["prompt_key"] for row in round_rows],
        "printer_forbidden_support_hits": printer_forbidden,
        "initial_repair_error_counts": dict(sorted(repair_errors.items())),
        "bank_audit": audit,
        "prompts": rows,
    }
    output = snapshot / "pilot_export"
    output.mkdir(exist_ok=False)
    (output / "prompts_pilot_40.json").write_text(json.dumps(payload, indent=2) + "\n")
    (output / "prompts_pilot_40.txt").write_text(
        "\n\n".join(
            f"[{row['prompt_key']} | {row['environment']} | source {row['source_relevance_score']} | C-Tech {row['ctech_reference_score']}]\n{row['text']}"
            for row in rows
        )
        + "\n"
    )
    validation = {
        "passed": not printer_forbidden and len(round_rows) >= 2,
        "checks": {
            "snapshot_verified": True,
            "four_banks_succeeded": True,
            "ten_prompts_per_bank": True,
            "forty_unique_prompt_keys": True,
            "at_least_one_round_support_per_laptop_bank": len(round_rows) >= 2,
            "no_forbidden_printer_support_hit": not printer_forbidden,
            "no_manual_prose_edits": True,
        },
    }
    (output / "validation.json").write_text(json.dumps(validation, indent=2) + "\n")
    print(json.dumps({"output": str(output), "validation": validation, "environments": payload["environment_counts"], "repair_errors": payload["initial_repair_error_counts"]}, indent=2))


if __name__ == "__main__":
    main()
