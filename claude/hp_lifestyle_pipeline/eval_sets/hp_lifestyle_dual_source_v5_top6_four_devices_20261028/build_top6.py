#!/usr/bin/env python3
"""Select and export the six most source-relevant V5 prompts from each bank."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    manifest_path = HERE / "manifest.json"
    accepted_path = HERE / "reviewed_prompt_cases.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    accepted = json.loads(accepted_path.read_text(encoding="utf-8"))
    cases_by_id = {case["case_id"]: case for case in manifest["cases"]}
    if len(cases_by_id) != 16 or set(cases_by_id) != set(accepted["cases"]):
        raise ValueError("accepted V5 banks must exactly match the 16-case manifest")

    selected: list[dict[str, Any]] = []
    all_candidates: list[dict[str, Any]] = []
    for case_id in manifest["authorized_text_case_ids"]:
        case = cases_by_id[case_id]
        bank = accepted["cases"][case_id]
        if bank["status"] != "reviewed_validator_passed":
            raise ValueError(f"bank has not passed reviewed deterministic validation: {case_id}")
        candidates = bank["candidates"]
        if len(candidates) != 20 or [item["id"] for item in candidates] != [f"p{i}" for i in range(1, 21)]:
            raise ValueError(f"bank is not the ordered 20-candidate V5 contract: {case_id}")
        ranks = [(item["source_relevance_score"], item["ctech_reference_score"]) for item in candidates]
        if ranks != sorted(ranks, reverse=True):
            raise ValueError(f"bank is not ordered by source relevance with C-Tech tie-break: {case_id}")
        for rank, candidate in enumerate(candidates, 1):
            row = {
                "prompt_key": f"{case_id}::{candidate['id']}",
                "device_id": case["device_id"],
                "device_display_name": case["device_display_name"],
                "device_type": case["device_type"],
                "source_pair": case["source_pair"],
                "camera_tag": case["camera_tag"],
                "source_camera_name": case["source_camera_name"],
                "view_role": case["view_role"],
                "render_gallery_url": case["render_gallery_url"],
                "render_lookup": case["render_lookup"],
                "bank_rank": rank,
                **candidate,
            }
            all_candidates.append(row)
            if rank <= 6:
                selected.append(row)

    if len(all_candidates) != 320 or len(selected) != 96:
        raise ValueError("expected 320 generated candidates and 96 selected prompts")
    bank_counts = Counter((row["device_id"], row["camera_tag"]) for row in selected)
    if len(bank_counts) != 16 or set(bank_counts.values()) != {6}:
        raise ValueError(f"expected six selected prompts in each of 16 banks: {bank_counts}")
    if len({row["prompt_key"] for row in selected}) != 96:
        raise ValueError("selected prompt keys are not unique")
    unnatural_pattern = re.compile(
        r"workteam|workgroup|shared office hub|fleet operations|workflow area|"
        r"daily office output|managed enterprise team|policy deployment|records counter|"
        r"paperwork nook|illustration worktop|close section of|close patch of",
        re.IGNORECASE,
    )
    unnatural_hits = []
    for row in selected:
        for field in ("subsetting", "text", "ctech_explanation", "explanation"):
            if unnatural_pattern.search(row[field]):
                unnatural_hits.append({"prompt_key": row["prompt_key"], "field": field})
    if unnatural_hits:
        raise ValueError(f"selected prompts contain rejected unnatural phrasing: {unnatural_hits}")

    output = {
        "version": "hp-lifestyle-dual-source-v5-top6-four-devices-selection-v1",
        "manifest_path": str(manifest_path),
        "manifest_sha256": sha_bytes(manifest_path.read_bytes()),
        "selection_rule": manifest["scope"]["selection_rule"],
        "counts": {
            "devices": 4,
            "views_per_device": 4,
            "banks": 16,
            "selected_per_bank": 6,
            "prompts": 96,
        },
        "device_source_mapping": manifest["device_source_mapping"],
        "prompts": selected,
    }
    data_dir = HERE / "data"
    write_json(data_dir / "prompts_top6_96.json", output)
    write_json(
        data_dir / "prompts_all_320.json",
        {
            "version": "hp-lifestyle-dual-source-v5-all-four-devices-candidates-v1",
            "manifest_sha256": output["manifest_sha256"],
            "counts": {"banks": 16, "prompts": 320},
            "prompts": all_candidates,
        },
    )
    text_blocks = [
        (
            f"[{row['device_display_name']} | {row['camera_tag']} | rank {row['bank_rank']} | "
            f"source {row['source_relevance_score']} | C-Tech {row['ctech_reference_score']}]\n"
            f"{row['text']}"
        )
        for row in selected
    ]
    (data_dir / "prompts_top6_96.txt").write_text(
        "\n\n".join(text_blocks) + "\n", encoding="utf-8"
    )
    fieldnames = [
        "prompt_key", "device_display_name", "device_type", "source_pair", "camera_tag",
        "source_camera_name", "bank_rank", "environment", "subsetting", "text",
        "source_relevance_score", "ctech_reference_score", "ctech_reference_id",
        "relationship", "ctech_relationship", "explanation", "ctech_explanation",
        "render_gallery_url",
    ]
    with (data_dir / "prompts_top6_96.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(selected)
    validation = {
        "version": "hp-lifestyle-dual-source-v5-top6-four-devices-validation-v1",
        "passed": True,
        "checks": {
            "accepted_cases_match_manifest": True,
            "all_16_banks_passed_reviewed_v5_validator": True,
            "all_banks_have_20_ordered_candidates": True,
            "selected_first_six_per_bank": True,
            "selected_prompt_count_is_96": True,
            "prompt_keys_unique": True,
            "selected_fields_avoid_rejected_unnatural_phrasing": True,
        },
        "distribution": {
            "device_counts": dict(sorted(Counter(row["device_display_name"] for row in selected).items())),
            "environment_counts": dict(sorted(Counter(row["environment"] for row in selected).items())),
            "relationship_counts": dict(sorted(Counter(row["relationship"] for row in selected).items())),
            "distinct_prompt_texts": len({" ".join(row["text"].casefold().split()) for row in selected}),
            "source_relevance_score": {
                "minimum": min(row["source_relevance_score"] for row in selected),
                "maximum": max(row["source_relevance_score"] for row in selected),
                "mean": round(statistics.mean(row["source_relevance_score"] for row in selected), 2),
            },
            "ctech_reference_score": {
                "minimum": min(row["ctech_reference_score"] for row in selected),
                "maximum": max(row["ctech_reference_score"] for row in selected),
                "mean": round(statistics.mean(row["ctech_reference_score"] for row in selected), 2),
            },
        },
        "bank_counts": [
            {"device_id": device, "camera_tag": tag, "prompts": count}
            for (device, tag), count in sorted(bank_counts.items())
        ],
        "output_sha256": sha_bytes((data_dir / "prompts_top6_96.json").read_bytes()),
    }
    write_json(HERE / "validation/top6_validation.json", validation)
    print(json.dumps(output["counts"], indent=2))


if __name__ == "__main__":
    main()
