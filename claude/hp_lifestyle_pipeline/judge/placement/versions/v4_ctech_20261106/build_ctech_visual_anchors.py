#!/usr/bin/env python3
"""Build durable C-Tech-derived development anchors with exact-target exclusion."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "evidence/calibration_manifest.json"
LABELS = ROOT / "evidence/calibration_cases.json"
ASSET_DIR = ROOT / "data/ctech_visual_anchors"
TARGET = ROOT / "data/visual_anchors.json"

SELECTED = {
    "magic__printer_FrontLeftMedium__p1": "FAIL: C-Tech identifies a visibly missing required table support. Inspect the exposed under-table load path; do not assume a hidden leg merely because another leg exists or the far edge approaches the crop.",
    "elitebook__laptop_FrontLeftMedium__p2": "FAIL: C-Tech identifies a missing table leg/support. A plausible laptop arrangement does not rescue visibly incomplete support furniture.",
    "tassel__printer_FrontWide__p1": "FAIL: C-Tech identifies a deformed rectangular tabletop and a conventional open-leg rectangular printer table stranded in the middle of a home room. Decorative proximity to a sideboard does not make it a functional equipment grouping.",
    "magic__printer_FrontWide__p6": "FAIL: C-Tech identifies mismatched table legs. Compare visible supports, attachments, and load paths rather than accepting the scene from its overall office appearance.",
    "magic__printer_FrontWide__p8": "FAIL: C-Tech identifies rigid table geometry warping around the curtains. Distinguish ordinary fabric overlap from a table edge or support that bends/intersects to accommodate fabric.",
    "elitebook__laptop_FrontLeftMedium__p1": "PASS: the chair is only modestly displaced and can move. Do not escalate mild chair movement when a believable user position remains.",
    "cashmere__laptop_FrontCloseUp__p5": "PASS for placement: clipped framed artwork is only a creative framing advisory. It must not change placement severity.",
    "cashmere__laptop_FrontCloseUp__p2": "REVIEW: the water carafe visibly crowds the laptop's immediate work area. This is access/usability severity 2, not a fail.",
    "magic__printer_FrontRightCloseUp__p2": "REVIEW: the reading glasses are visibly malformed. This is a localized incidental-geometry severity 2 and cannot fail placement by itself.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    records = {record["id"]: record for record in json.loads(SOURCE.read_text())["records"]}
    labels = {case["id"]: case for case in json.loads(LABELS.read_text())["cases"]}
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    examples = []
    exclusions = {}
    for case_id, guidance in SELECTED.items():
        source = Path(records[case_id]["generated_image"]["local_path"])
        target = ASSET_DIR / f"{case_id}.png"
        shutil.copyfile(source, target)
        digest = sha256(target)
        family = f"ctech-calibration:{case_id}"
        exclusions[digest] = family
        examples.append(
            {
                "asset_id": f"ctech-{case_id}",
                "kind": "user_comment_example",
                "case_family": family,
                "local_path": str(target),
                "sha256": digest,
                "guidance": guidance,
                "source_public_url": labels[case_id]["generated_image"],
                "label_status": "C-Tech development comment; exact target excluded; not held-out",
            }
        )
    payload = {
        "status": "Nine C-Tech-derived V6.1 development anchors; exact target bytes and case family excluded.",
        "expected_count": len(examples),
        "exclusion_groups": exclusions,
        "examples": examples,
    }
    TARGET.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(TARGET)


if __name__ == "__main__":
    main()
