#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas", "pyarrow"]
# ///
"""Build the parquet input for the Foundry annotation-viewer report."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
INPUT_DATA_JS = (
    PROJECT_ROOT
    / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/data.js"
)
BUCKET = "foundry-hp-enterprise-adobe-assets"
EVAL_PREFIX = "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1"


def load_eval_data() -> dict[str, Any]:
    text = INPUT_DATA_JS.read_text(encoding="utf-8")
    match = re.fullmatch(r"const EVAL_DATA = (.*);\n?", text, re.S)
    if not match:
        raise ValueError(f"Could not parse {INPUT_DATA_JS}")
    return json.loads(match.group(1))


def load_records(run_dir: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / "records").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        records[record["row_id"]] = record
    return records


def pretty(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    data = load_eval_data()
    prompts = {prompt["key"]: prompt for prompt in data["prompts"]}
    twins = {twin["evalset_item_id"]: twin for twin in data["twins"]}
    records = load_records(args.run_dir)

    rows: list[dict[str, Any]] = []
    for source_row in data["rows"]:
        row_id = source_row["row_id"]
        if row_id not in records:
            raise ValueError(f"Missing generation record for {row_id}")
        record = records[row_id]
        if record.get("status") != "done":
            raise ValueError(f"Generation did not succeed for {row_id}")
        prompt = prompts[source_row["prompt_key"]]
        twin = twins[source_row["twin_id"]]
        debug = record["debugData"]

        rows.append(
            {
                "row_id": row_id,
                "prompt": prompt["text"],
                "digital_twin": (
                    f"s3://{BUCKET}/{EVAL_PREFIX}/assets/digital_twins/"
                    f"{source_row['twin_file']}"
                ),
                "source_messaging": pretty(data["sources"][prompt["source_id"]]),
                "explanation": pretty(data["explanations"][source_row["prompt_key"]]),
                "generated_output": (
                    f"s3://{BUCKET}/{EVAL_PREFIX}/generated_v1/images/"
                    f"{record['output_image_filename']}"
                ),
                "rewritten_prompt": debug["usedPrompt"],
                "generation_debug": pretty(
                    {
                        "request_payload": record["request_payload"],
                        "debugData": debug,
                    }
                ),
                "source_product": prompt["source_product"],
                "environment": prompt["environment"],
                "device_category": prompt["device_category"],
                "source_id": prompt["source_id"],
                "prompt_id": prompt["prompt_id"],
                "twin_id": source_row["twin_id"],
                "twin_source_s3_uri": twin["s3_uri"],
                "output_seed": record["output_seed"],
                "rewrite_latency_ms": debug["rewriteLatencyMs"],
                "total_latency_ms": record.get("total_latency_ms"),
                "job_id": record["job_id"],
            }
        )

    if len(rows) != 192 or len({row["row_id"] for row in rows}) != 192:
        raise ValueError("Expected exactly 192 unique FE rows")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(args.output, index=False)
    print(
        json.dumps(
            {
                "rows": len(rows),
                "columns": list(rows[0]),
                "output": str(args.output),
                "bytes": args.output.stat().st_size,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
