#!/usr/bin/env python3
"""Build the FE review payload for the frozen V6.2 R3 text pilot."""

from __future__ import annotations

import json
import shutil
from collections import Counter
from pathlib import Path


ROOT = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/"
    "hp_lifestyle_spatial_composition_v6_2_four_devices_20261106"
)
REVISION = ROOT / "revisions/v6.2-pilot-20261106-r3"
EXPORT = REVISION / "pilot_export/prompts_pilot_40.json"
SOURCE_MANIFEST = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions/v3/"
    "data/new_v6_1_eval_20261105/manifest.json"
)
OUT = ROOT / "reports/v6.2-pilot-20261106-r3"
VIEWER = Path("/home/colligo/.claude/scripts/fe_html/annotation_viewer.html")
S3_PREFIX = (
    "eval_sets/hp_lifestyle_spatial_composition_v6_2_pilot_20261106/gallery"
)
GATEWAY = "https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets"


def _compact_evidence(evidence: list[dict]) -> str:
    return "\n".join(
        f"- {item.get('document', '')}: {item.get('quote', '')}"
        for item in evidence
    )


def main() -> None:
    pilot = json.loads(EXPORT.read_text())
    source = json.loads(SOURCE_MANIFEST.read_text())

    twin_by_case: dict[str, dict] = {}
    for record in source["records"]:
        case_id = record["id"].rsplit("__p", 1)[0]
        if case_id not in twin_by_case:
            twin_by_case[case_id] = record["twin_image"]

    if OUT.exists():
        shutil.rmtree(OUT)
    assets = OUT / "assets/twins"
    assets.mkdir(parents=True)
    shutil.copy2(VIEWER, OUT / "viewer.html")

    case_ids = sorted({row["case_id"] for row in pilot["prompts"]})
    for case_id in case_ids:
        twin = twin_by_case[case_id]
        src = Path(twin["local_path"])
        if not src.is_file():
            raise FileNotFoundError(src)
        shutil.copy2(src, assets / twin["filename"])

    counts = Counter(row["environment"] for row in pilot["prompts"])
    rows = []
    for row_idx, prompt in enumerate(pilot["prompts"], start=1):
        case_id = prompt["case_id"]
        audit = pilot["bank_audit"][case_id]
        twin = twin_by_case[case_id]
        twin_url = f"{GATEWAY}/{S3_PREFIX}/assets/twins/{twin['filename']}"
        text = (
            f"SCENE PROMPT\n{prompt['text']}\n\n"
            f"WHY THIS PROMPT\n{prompt['explanation']}\n\n"
            f"CAMERA FIT\n{prompt['camera_fit_explanation']}\n\n"
            f"SOURCE EVIDENCE\n{_compact_evidence(prompt['evidence'])}\n\n"
            f"C-TECH RELATIONSHIP\n{prompt['ctech_explanation']}"
        )
        rows.append(
            {
                "meta_data": {
                    "row_idx": row_idx,
                    "evalset_item_id": prompt["prompt_key"],
                    "key_val_informations": {
                        "V6.2 prompt bank": case_id,
                        "Device": prompt["device_display_name"],
                        "Product type": prompt["device_type"],
                        "Camera": prompt["camera_tag"],
                        "Rank": prompt["rank"],
                        "Environment": prompt["environment"],
                        "Scene prompt": prompt["text"],
                        "Source relevance score": prompt["source_relevance_score"],
                        "C-Tech reference score": prompt["ctech_reference_score"],
                        "C-Tech reference": prompt["ctech_reference_id"],
                        "Relationship": prompt["relationship"],
                        "Approved prop IDs": ", ".join(prompt["prop_ids"]),
                        "Creative departures": "\n".join(prompt["creative_departures"])
                        or "None",
                        "Camera-fit explanation": prompt["camera_fit_explanation"],
                        "Source explanation": prompt["explanation"],
                        "Source evidence": _compact_evidence(prompt["evidence"]),
                        "Bank semantic calls": audit["run"]["semantic_calls"],
                        "Automatic repair used": audit["run"][
                            "semantic_repair_attempted"
                        ],
                        "Manual prose edits": "No",
                    },
                },
                "images": [
                    {
                        "asset_type": "image",
                        "is_model_input_or_output": "model_input",
                        "image_src": twin_url,
                        "meta_text": {
                            "label": "Digital twin / fixed camera reference",
                            "Device": prompt["device_display_name"],
                            "Camera": prompt["camera_tag"],
                        },
                    },
                    {
                        "asset_type": "text",
                        "is_model_input_or_output": "model_output",
                        "text_content": text,
                        "meta_text": {
                            "label": "V6.2 scene prompt and rationale",
                            "Rank": prompt["rank"],
                            "Environment": prompt["environment"],
                            "Source score": prompt["source_relevance_score"],
                            "C-Tech score": prompt["ctech_reference_score"],
                        },
                    },
                ],
            }
        )

    report = {
        "is_secure": True,
        "meta_texts": [
            "HP Lifestyle Prompt Writer V6.2 — Spatial Composition Text Pilot (R3, 40 prompts)",
            [
                "Pilot scope",
                {
                    "Revision": "v6.2-pilot-20261106-r3",
                    "Rows": 40,
                    "Prompt banks": 4,
                    "Banks": ", ".join(case_ids),
                    "Environment distribution": "; ".join(
                        f"{name} {counts[name]}" for name in sorted(counts)
                    ),
                    "Images generated": "No — text pilot with digital-twin camera references",
                },
            ],
            [
                "V6.2 checks",
                {
                    "Laptop support diversity": "At least one context-compatible round/circular table in every 10-prompt laptop bank",
                    "Printer support": "Dedicated rectilinear equipment table with open standing approach",
                    "Walls": "Coherent approved treatment; artwork tied to the furniture composition; no empty wall boards",
                    "Shelves / pegboards": "Must be populated with declared approved prop families",
                    "Detail density": "Qualitative and camera-aware; no noun-count ceilings",
                },
            ],
            [
                "Runtime audit",
                {
                    "Banks passed": "4 / 4",
                    "Prompts per bank": 10,
                    "Automatic repair": "Used once in all four banks",
                    "Manual prompt edits": "None",
                    "Initial validation errors": "8 undeclared-known-prop; 1 repeated semantic group",
                    "Final validation errors": 0,
                    "Approved-catalog note": "Two printer prompts use the approved V61-OFF-006 wording 'empty architectural letter tray'; retained for reproducibility and flagged for later catalog review.",
                },
            ],
        ],
        "rows": rows,
    }
    (OUT / "data.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (OUT / "prompts_pilot_40.json").write_bytes(EXPORT.read_bytes())
    (OUT / "prompts_pilot_40.txt").write_bytes(
        (REVISION / "pilot_export/prompts_pilot_40.txt").read_bytes()
    )
    (OUT / "validation.json").write_bytes(
        (REVISION / "pilot_export/validation.json").read_bytes()
    )
    print(OUT)
    print(f"rows={len(rows)} assets={len(list(assets.iterdir()))}")


if __name__ == "__main__":
    main()
