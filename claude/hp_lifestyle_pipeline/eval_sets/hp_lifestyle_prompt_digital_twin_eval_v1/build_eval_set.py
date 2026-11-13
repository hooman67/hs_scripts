#!/usr/bin/env python3
"""Build the first HP lifestyle prompt-by-digital-twin evaluation set."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVAL_ROOT = Path(__file__).resolve().parent
GALLERY_ROOT = EVAL_ROOT / "gallery"

PRODUCTION_OUTPUTS = (
    PROJECT_ROOT
    / "research/source_messaging_v1_to_v6/artifacts/production_outputs.json"
)
GENERATION_PROMPTS = (
    PROJECT_ROOT
    / "research/source_messaging_v1_to_v6/artifacts/generation_prompts.json"
)
DIGITAL_TWIN_MANIFEST = (
    PROJECT_ROOT / "digital_twin_assets/first_column_manifest.json"
)
MODEL_OUTPUT_EVALSET = (
    PROJECT_ROOT
    / "research/source_messaging_v1_to_v6/data/model_output_evalset.json"
)

S3_BUCKET = "foundry-hp-enterprise-adobe-assets"
S3_PREFIX = "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1"
TITLE = "HP Lifestyle Prompt × Digital Twin Eval v1"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def classify_source(source: dict[str, Any]) -> tuple[str, str]:
    """Return the source product label and its digital-twin category."""
    source_text = json.dumps(source, ensure_ascii=False)
    rules = (
        ("HP EliteBook X Flip G2i", "Laptop", r"EliteBook X Flip G2i"),
        ("HP EliteBook X G2i", "Laptop", r"EliteBook X G2i"),
        ("HP LaserJet Enterprise 6501dn", "Printer", r"LaserJet Enterprise 6501dn"),
        ("HP Smart Tank 7602 All-in-One", "Printer", r"Smart Tank 7602"),
    )
    matches = [(label, category) for label, category, pattern in rules if re.search(pattern, source_text, re.I)]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one source product match; found {matches}")
    return matches[0]


def device_labels_from_evalset(payload: dict[str, Any]) -> dict[str, dict[str, str]]:
    sheet = next(sheet for sheet in payload["sheets"] if sheet["name"] == "Eval Set")
    rows: dict[int, dict[str, str]] = {}
    for cell in sheet["cells"]:
        match = re.fullmatch(r"([A-Z]+)(\d+)", cell["cell"])
        if not match:
            continue
        column, row_number = match.group(1), int(match.group(2))
        rows.setdefault(row_number, {})[column] = cell.get("text", "")

    labels: dict[str, dict[str, str]] = {}
    for row in rows.values():
        baseline_id = row.get("A", "")
        if baseline_id.startswith("baseline-"):
            labels[baseline_id] = {
                "device_category": row.get("D", ""),
                "scene_environment": row.get("B", ""),
                "scene_surface": row.get("C", ""),
            }
    return labels


def explanation_for_prompt(debug: dict[str, Any], prompt_id: str) -> dict[str, Any]:
    value_proposition = debug.get("value_proposition") or {}
    if prompt_id not in value_proposition.get("prompt_ids", []):
        value_proposition = {}

    return {
        "input_assessment": debug.get("input_assessment", ""),
        "count_explanation": debug.get("count_explanation", ""),
        "used_fallback": bool(debug.get("used_fallback", False)),
        "ksp_mappings": [
            mapping
            for mapping in debug.get("ksp_mappings", [])
            if prompt_id in mapping.get("prompt_ids", [])
        ],
        "value_proposition": value_proposition,
        "creative_additions": [
            addition
            for addition in debug.get("creative_additions", [])
            if addition.get("prompt_id") == prompt_id
        ],
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    production_records = load_json(PRODUCTION_OUTPUTS)
    flattened_prompts = load_json(GENERATION_PROMPTS)["prompts"]
    twin_manifest = load_json(DIGITAL_TWIN_MANIFEST)
    device_labels = device_labels_from_evalset(load_json(MODEL_OUTPUT_EVALSET))

    flattened_by_key = {
        (prompt["source_id"], prompt["id"]): prompt for prompt in flattened_prompts
    }

    sources: dict[str, Any] = {}
    explanations: dict[str, Any] = {}
    prompts: list[dict[str, Any]] = []

    for record in production_records:
        source_id = record["source_id"]
        source_path = Path(record["source_json_path"])
        if not source_path.exists():
            source_path = (
                PROJECT_ROOT
                / "research/source_messaging_v1_to_v6/data/source_json"
                / f"{source_id}.json"
            )
        source = load_json(source_path)
        product_label, device_category = classify_source(source)
        sources[source_id] = source

        output = record["output"]
        for prompt in output["prompts"]:
            prompt_key = f"{source_id}:{prompt['id']}"
            flat = flattened_by_key.get((source_id, prompt["id"]))
            if not flat or flat["text"] != prompt["text"]:
                raise ValueError(f"Flattened prompt mismatch for {prompt_key}")

            prompts.append(
                {
                    "key": prompt_key,
                    "source_id": source_id,
                    "prompt_id": prompt["id"],
                    "environment": prompt["environment"],
                    "text": prompt["text"],
                    "source_product": product_label,
                    "device_category": device_category,
                }
            )
            explanations[prompt_key] = explanation_for_prompt(
                output["debug"], prompt["id"]
            )

    twins: list[dict[str, Any]] = []
    for asset in twin_manifest["assets"]:
        baseline_id = asset["evalset_item_id"]
        if baseline_id not in device_labels:
            raise ValueError(f"No eval-workbook device label for {baseline_id}")
        twins.append({**asset, **device_labels[baseline_id]})

    prompt_categories = {prompt["device_category"] for prompt in prompts}
    used_twins = [
        twin for twin in twins if twin["device_category"] in prompt_categories
    ]
    excluded_twins = [
        twin for twin in twins if twin["device_category"] not in prompt_categories
    ]

    rows: list[dict[str, Any]] = []
    for prompt in prompts:
        compatible_twins = [
            twin
            for twin in used_twins
            if twin["device_category"] == prompt["device_category"]
        ]
        if not compatible_twins:
            raise ValueError(f"No compatible twins for prompt {prompt['key']}")
        for twin in compatible_twins:
            rows.append(
                {
                    "row_id": f"{prompt['key']}:{twin['evalset_item_id']}",
                    "prompt_key": prompt["key"],
                    "twin_id": twin["evalset_item_id"],
                    "twin_file": twin["local_filename"],
                    "device_category": twin["device_category"],
                    "original_twin_s3_uri": twin["s3_uri"],
                }
            )

    prompt_counts = Counter(prompt["device_category"] for prompt in prompts)
    twin_counts = Counter(twin["device_category"] for twin in used_twins)
    row_counts = Counter(row["device_category"] for row in rows)

    data = {
        "metadata": {
            "title": TITLE,
            "built_on": date.today().isoformat(),
            "matching_policy": (
                "Match each prompt to every digital twin with the same device category."
            ),
            "s3_bucket": S3_BUCKET,
            "s3_prefix": S3_PREFIX,
            "prompt_count": len(prompts),
            "source_count": len(sources),
            "available_twin_count": len(twins),
            "used_twin_count": len(used_twins),
            "excluded_twin_count": len(excluded_twins),
            "row_count": len(rows),
            "prompt_counts_by_category": dict(sorted(prompt_counts.items())),
            "used_twin_counts_by_category": dict(sorted(twin_counts.items())),
            "row_counts_by_category": dict(sorted(row_counts.items())),
        },
        "prompts": prompts,
        "twins": used_twins,
        "sources": sources,
        "explanations": explanations,
        "rows": rows,
    }

    manifest = {
        **data["metadata"],
        "inputs": {
            "production_outputs": str(PRODUCTION_OUTPUTS),
            "generation_prompts": str(GENERATION_PROMPTS),
            "digital_twin_manifest": str(DIGITAL_TWIN_MANIFEST),
            "device_label_workbook_extraction": str(MODEL_OUTPUT_EVALSET),
        },
        "excluded_twins": [
            {
                "twin_id": twin["evalset_item_id"],
                "device_category": twin["device_category"],
                "local_filename": twin["local_filename"],
                "reason": "No source-messaging prompt for this device category.",
            }
            for twin in excluded_twins
        ],
    }
    return data, manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate inputs and report counts without rewriting artifacts.",
    )
    args = parser.parse_args()

    data, manifest = build()
    if not args.check:
        GALLERY_ROOT.mkdir(parents=True, exist_ok=True)
        (GALLERY_ROOT / "data.js").write_text(
            "const EVAL_DATA = "
            + json.dumps(data, ensure_ascii=False, indent=2)
            + ";\n",
            encoding="utf-8",
        )
        write_json(EVAL_ROOT / "manifest.json", manifest)

    print(json.dumps(data["metadata"], indent=2))


if __name__ == "__main__":
    main()
