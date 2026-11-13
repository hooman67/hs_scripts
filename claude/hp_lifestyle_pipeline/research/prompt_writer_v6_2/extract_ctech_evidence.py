#!/usr/bin/env python3
"""Join C-Tech FE annotations to the frozen V6.1 report rows.

The resulting packet is deliberately compact enough to provide to a reviewing
model while retaining the original comment, prompt, V3 verdict, and image URLs.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
EVIDENCE = ROOT / "research/prompt_writer_v6_2/evidence"
REPORT = (
    ROOT
    / "judge/placement/versions/v3/fe_reports/"
    "v6_1_consensus_v2_grouped_20261105/data.json"
)

ANNOTATIONS = (
    EVIDENCE / "combined_reviewer_0.json",
    EVIDENCE / "cashmere_laptop_front_closeup_reviewer_0.json",
    EVIDENCE / "magic_printer_front_wide_reviewer_0.json",
)


def image_urls(row: dict) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    images = row.get("images", [])
    if isinstance(images, dict):
        images = [images]
    for image in images:
        if not isinstance(image, dict):
            continue
        url = (
            image.get("url")
            or image.get("image_url")
            or image.get("image_src")
            or image.get("src")
        )
        meta_text = image.get("meta_text") if isinstance(image.get("meta_text"), dict) else {}
        label = (
            image.get("label")
            or image.get("name")
            or image.get("title")
            or meta_text.get("label")
            or "image"
        )
        if url:
            output.append({"label": str(label), "url": str(url)})
    return output


def main() -> None:
    report = json.loads(REPORT.read_text())
    report_by_id = {
        row["meta_data"]["evalset_item_id"]: row for row in report["rows"]
    }

    records: list[dict] = []
    for annotation_path in ANNOTATIONS:
        annotation = json.loads(annotation_path.read_text())
        for note in annotation["rows"]:
            item_id = note["evalset_item_id"]
            row = report_by_id[item_id]
            info = row["meta_data"]["key_val_informations"]
            records.append(
                {
                    "annotation_source": annotation_path.name,
                    "evalset_item_id": item_id,
                    "row_idx": note["row_idx"],
                    "device": info.get("Device"),
                    "product_type": info.get("Product type"),
                    "camera": info.get("Camera"),
                    "candidate": info.get("V6.1 candidate"),
                    "environment": info.get("Environment"),
                    "scene_prompt": info.get("Original scene prompt"),
                    "v3_verdict": info.get("Judge v3 predicted verdict"),
                    "v3_score": info.get("Judge score"),
                    "v3_summary": info.get("Judge evidence summary"),
                    "ctech_comment": note.get("comment", ""),
                    "images": image_urls(row),
                }
            )

    packet = {
        "source_report": str(REPORT),
        "annotation_files": [str(path) for path in ANNOTATIONS],
        "record_count": len(records),
        "records": records,
    }
    (EVIDENCE / "ctech_joined_evidence.json").write_text(
        json.dumps(packet, indent=2, ensure_ascii=False) + "\n"
    )

    lines = [
        "# C-Tech feedback joined to V6.1 prompts and V3 judgments",
        "",
        f"Records: {len(records)}",
        "",
    ]
    for record in records:
        lines.extend(
            [
                f"## {record['evalset_item_id']}",
                "",
                f"- Device/camera: {record['device']} / {record['camera']}",
                f"- Environment: {record['environment']}",
                f"- V3: {record['v3_verdict']} ({record['v3_score']})",
                f"- Prompt: {record['scene_prompt']}",
                f"- C-Tech: {record['ctech_comment']}",
            ]
        )
        for image in record["images"]:
            lines.append(f"- {image['label']}: {image['url']}")
        lines.append("")
    (EVIDENCE / "CTECH_JOINED_EVIDENCE.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
