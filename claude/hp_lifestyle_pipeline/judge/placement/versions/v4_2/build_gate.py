#!/usr/bin/env python3
"""Build the six-case V4.2 gate with comments/labels kept outside runtime records."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
V4 = ROOT.parent / "v4"
TARGETS = [
    "elitebook__laptop_FrontLeftMedium__p1",
    "tassel__printer_FrontWide__p1",
    "magic__printer_FrontLeftMedium__p1",
    "tassel__printer_FrontCloseUp__p2",
    "tassel__printer_FrontRightCloseUp__p1",
    "magic__printer_FrontRightCloseUp__p2",
]
REQUIRED = {
    TARGETS[0]: {"verdict": "review", "issues": ["chair_displacement"], "forbidden": ["missing_required_support"]},
    TARGETS[1]: {"verdict": "fail", "issues": ["misplaced_support_furniture", "malformed_support_furniture"], "forbidden": []},
    TARGETS[2]: {"verdict": "fail", "issues": ["missing_required_support"], "forbidden": []},
    TARGETS[3]: {"verdict": "fail", "issues": ["device_support_axis_conflict", "incoherent_prop_arrangement"], "forbidden": []},
    TARGETS[4]: {"verdict": None, "issues": ["conflicting_perspective"], "forbidden": []},
    TARGETS[5]: {"verdict": "pass", "issues": [], "forbidden": ["missing_required_support", "malformed_support_furniture", "conflicting_perspective"]},
}


def main() -> None:
    manifest = json.loads((V4 / "data" / "development_15_manifest.json").read_text())
    expectations = json.loads((V4 / "data" / "development_15_expectations.json").read_text())
    rows = {r["id"]: r for r in manifest["records"]}
    exps = {r["record_id"]: r for r in expectations["records"]}
    runtime_records, withheld = [], []
    for target in TARGETS:
        r = rows[target]
        runtime_records.append({
            "record_id": target,
            "runtime_input": {
                "generated_image": r["generated_image"]["local_path"],
                "twin_image": r["twin_image"]["local_path"],
                "product_type": r["device_type"],
                "scene_prompt": r["scene_prompt"],
                "target_record_id": target,
                "device": r["device"],
                "camera": r["view"]["camera_tag"],
                "prompt_rank": r["candidate_id"],
            },
        })
        e = exps[target]
        withheld.append({
            "record_id": target,
            "human_comment_exact": e["human_comment_exact"],
            "original_explicit_verdict": e["explicit_verdict"],
            "original_expected_issue_any": e["expected_issue_any"],
            "v4_2_gate_requirement": REQUIRED[target],
            "passed_to_judge": False,
        })
    data = ROOT / "data"
    data.mkdir(exist_ok=True)
    (data / "gate_6_manifest.json").write_text(json.dumps({"schema_version": "hp-placement-v4.2-gate-manifest-v1", "labels_passed_to_judge": False, "records": runtime_records}, indent=2) + "\n")
    (data / "gate_6_expectations_withheld.json").write_text(json.dumps({"schema_version": "hp-placement-v4.2-gate-expectations-v1", "records": withheld}, indent=2) + "\n")
    print("built gate", len(runtime_records))


if __name__ == "__main__":
    main()
