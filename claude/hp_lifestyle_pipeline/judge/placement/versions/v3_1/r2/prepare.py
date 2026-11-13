"""Freeze one calibration selection and r1 integrity before r2 design/model calls."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R1 = ROOT.parent
ANCHORS = [
    "07_cashmere_x_Front_Wide_1",
    "07_cashmere_x_Front_Wide_4",
    "13_elitebook_13_Front_Left_Medium_4",
]
CONTROLS = [
    "01_cashmere_x_Front_CloseUp_2",
    "17_tassel_Front_CloseUp_1",
    "31_adf_printer_Front_Wide_1",
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    if (ROOT / "calibration_manifest.json").exists():
        raise RuntimeError("Preserve the frozen calibration selection")
    artifacts = json.loads((R1 / "ARTIFACT_MANIFEST.json").read_text())
    mismatches = [a["path"] for a in artifacts["files"] if sha(a["path"]) != a["sha256"]]
    if mismatches:
        raise RuntimeError("r1 artifact integrity mismatch")
    (ROOT / "r1_integrity_before.json").write_text(json.dumps({
        "verified_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_path": str(R1 / "ARTIFACT_MANIFEST.json"),
        "manifest_sha256": sha(R1 / "ARTIFACT_MANIFEST.json"),
        "indexed_files_verified": len(artifacts["files"]), "mismatches": [],
    }, indent=2) + "\n")
    inventory = json.loads((R1 / "evaluation/inventory.json").read_text())
    records = {r["id"]: r for r in inventory["records"]}
    cases = []
    for case_id in ANCHORS + CONTROLS:
        case = dict(records[case_id])
        case["role"] = "ctech_anchor" if case_id in ANCHORS else "stability_control"
        case["expectation"] = {
            "orientation_alignment": "no_material_defect",
            "scale_perspective": "no_new_material_defect" if case_id in CONTROLS else "unlabeled",
        }
        if case_id == ANCHORS[1]:
            case["expectation"]["orientation_alignment"] = "material_furniture_axis_conflict"
        elif case_id == ANCHORS[2]:
            case["expectation"]["scale_perspective"] = "material_malformed_support_furniture"
        case["expectation_provenance"] = (
            "User-provided C-Tech criterion label, not global positive."
            if case["role"] == "ctech_anchor"
            else "Both frozen V3 and r1 were clear across all dimensions. Locally inspected "
                 "as a cropped laptop, cropped printer, and fitted-counter/wide-printer "
                 "construction control. Model-selected stability check, not human gold.")
        cases.append(case)
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "r1_inventory_path": str(R1 / "evaluation/inventory.json"),
        "r1_inventory_sha256": sha(R1 / "evaluation/inventory.json"),
        "expected_count": 6, "anchor_count": 3, "control_count": 3,
        "selection_frozen_before_r2_design": True,
        "semantic_samples_per_case": 1,
        "full128_authorization": "Conditional on every stated calibration criterion passing.",
        "new_generation_judging_authorized": False,
        "cases": cases,
    }
    (ROOT / "calibration_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"frozen_cases": ANCHORS + CONTROLS, "r1_integrity_verified": True}))


if __name__ == "__main__":
    main()
