#!/usr/bin/env python3
"""Freeze a fresh V4.4 evaluation set from the verified 84-row comment corpus."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT.parent / "v4/validation_corpus/manifest.json"
V431_GATE = ROOT.parent / "v4_3_1/data/gate_6_manifest.json"
V431_ANCHORS = ROOT.parent / "v4_3_1/anchors/anchor_catalog.json"

SELECTED = [
    "cashmere__laptop_BackRightCloseUp__p6",
    "cashmere__laptop_FrontWide__p4",
    "elitebook__laptop_BackRightCloseUp__p5",
    "magic__printer_FrontCloseUp__p4",
    "cashmere__laptop_FrontCloseUp__p5",
    "magic__printer_FrontLeftMedium__p2",
    "magic__printer_FrontLeftMedium__p4",
    "magic__printer_FrontRightCloseUp__p1",
    "magic__printer_FrontWide__p5",
    "magic__printer_FrontWide__p6",
]

# Human-label interpretation is frozen before V4.4 calls. `verdict` is scored as
# independent only for direct free-text outcomes. Relational V2 outcomes remain
# explicitly relational and are never reported as independent accuracy labels.
EXPECTATIONS = {
    "cashmere__laptop_BackRightCloseUp__p6": {
        "basis": "direct_free_text_verdict",
        "verdict": "fail",
        "issue_any_of": ["no_feasible_user_position", "device_support_axis_conflict"],
        "family": "laptop_orientation_to_user_zone",
    },
    "cashmere__laptop_FrontWide__p4": {
        "basis": "direct_free_text_verdict",
        "verdict": "fail",
        "issue_any_of": ["unmotivated_device_position", "no_feasible_user_position"],
        "family": "stranded_laptop_position",
    },
    "elitebook__laptop_BackRightCloseUp__p5": {
        "basis": "direct_free_text_verdict",
        "verdict": "fail",
        "issue_any_of": ["no_feasible_user_position", "incoherent_use_zone"],
        "family": "ambiguous_competing_user_positions",
        "qualifier": "weak",
    },
    "magic__printer_FrontCloseUp__p4": {
        "basis": "direct_free_text_verdict",
        "verdict": "pass",
        "issue_any_of": [],
        "family": "clean_printer_placement_control",
        "forbid_material_placement_issue": True,
    },
    "cashmere__laptop_FrontCloseUp__p5": {
        "basis": "relational_agreement_with_frozen_v2",
        "relational_verdict": "pass",
        "issue_any_of": [],
        "family": "clean_laptop_closeup_control",
        "forbid_material_placement_issue": True,
    },
    "magic__printer_FrontLeftMedium__p2": {
        "basis": "issue_only_no_direct_verdict",
        "verdict": None,
        "issue_any_of": ["misplaced_support_furniture"],
        "family": "support_furniture_room_placement",
    },
    "magic__printer_FrontLeftMedium__p4": {
        "basis": "issue_only_no_direct_verdict",
        "verdict": None,
        "issue_any_of": ["unmotivated_device_position"],
        "family": "printer_wall_edge_distance",
    },
    "magic__printer_FrontRightCloseUp__p1": {
        "basis": "relational_agreement_with_concrete_comment",
        "relational_verdict": "fail",
        "issue_any_of": ["device_support_axis_conflict", "unmotivated_device_position", "occupied_workstation"],
        "family": "printer_alignment_and_workstation_role",
    },
    "magic__printer_FrontWide__p5": {
        "basis": "relational_agreement_with_concrete_comment",
        "relational_verdict": "fail",
        "issue_any_of": ["malformed_support_furniture", "missing_required_support"],
        "family": "support_anatomy_leg_alignment",
    },
    "magic__printer_FrontWide__p6": {
        "basis": "relational_agreement_with_concrete_comment",
        "relational_verdict": "fail",
        "issue_any_of": ["malformed_support_furniture", "incoherent_prop_arrangement"],
        "family": "joined_supports_and_prop_coherence",
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    corpus = json.loads(CORPUS.read_text())
    by_id = {row["id"]: row for row in corpus["records"]}
    gate_ids = {row["record_id"] for row in json.loads(V431_GATE.read_text())["records"]}
    anchor_ids = {
        row["source_record_id"]
        for row in json.loads(V431_ANCHORS.read_text())["records"]
    }
    if len(SELECTED) != 10 or len(set(SELECTED)) != 10:
        raise RuntimeError("fresh selection must contain ten unique cases")
    if set(SELECTED) & gate_ids:
        raise RuntimeError(f"development rows leaked: {sorted(set(SELECTED) & gate_ids)}")
    if set(SELECTED) & anchor_ids:
        raise RuntimeError(f"calibration anchor rows leaked: {sorted(set(SELECTED) & anchor_ids)}")

    manifest_rows = []
    expectation_rows = []
    seen_scene_hashes: set[str] = set()
    for record_id in SELECTED:
        source = by_id[record_id]
        scene = source["assets"]["generated_scene"]
        twin = source["assets"]["digital_twin_reference"]
        scene_path, twin_path = Path(scene["local_path"]), Path(twin["local_path"])
        if sha(scene_path) != scene["sha256"] or sha(twin_path) != twin["sha256"]:
            raise RuntimeError(f"asset hash mismatch: {record_id}")
        if scene["sha256"] in seen_scene_hashes:
            raise RuntimeError(f"duplicate scene hash: {record_id}")
        seen_scene_hashes.add(scene["sha256"])
        runtime = {
            "generated_image": str(scene_path),
            "twin_image": str(twin_path),
            "product_type": source["device_type"],
            "scene_prompt": source["scene_prompt"],
            "target_record_id": record_id,
            "device": source["device"],
            "camera": source["camera"]["camera_tag"],
            "prompt_rank": source["candidate_id"],
        }
        manifest_rows.append({
            "record_id": record_id,
            "runtime_input": runtime,
            "frozen_hashes": {
                "generated_image_sha256": scene["sha256"],
                "twin_image_sha256": twin["sha256"],
                "scene_prompt_sha256": source["scene_prompt_sha256"],
            },
        })
        expected = dict(EXPECTATIONS[record_id])
        expected.update({
            "record_id": record_id,
            "human_comment_exact": source["human_evidence"]["comment_exact"],
            "source_evidence_class": source["human_evidence"]["evidence_class"],
            "source_direct_label": source["human_evidence"]["direct_label"],
            "source_prior_judge_relation": source["human_evidence"]["prior_judge_relation"],
            "passed_to_judge": False,
        })
        expectation_rows.append(expected)

    data = ROOT / "data"
    data.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": "hp-placement-v4.4-fresh-ten-manifest-v1",
        "source_corpus": str(CORPUS.resolve()),
        "source_corpus_sha256": sha(CORPUS),
        "labels_passed_to_judge": False,
        "selection_frozen_before_v4_4_calls": True,
        "excluded_development_record_ids": sorted(gate_ids),
        "excluded_anchor_record_ids": sorted(anchor_ids),
        "records": manifest_rows,
    }
    expectations = {
        "schema_version": "hp-placement-v4.4-fresh-ten-expectations-v1",
        "claim_boundary": "development evidence; direct free-text verdicts are scored separately from relational agreement and issue-only evidence",
        "records": expectation_rows,
    }
    (data / "fresh_10_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (data / "fresh_10_expectations_withheld.json").write_text(json.dumps(expectations, indent=2) + "\n")
    print(json.dumps({
        "records": len(manifest_rows),
        "direct_verdicts": sum(row["basis"] == "direct_free_text_verdict" for row in expectation_rows),
        "issue_only": sum(row["basis"] == "issue_only_no_direct_verdict" for row in expectation_rows),
        "relational": sum(row["basis"].startswith("relational_") for row in expectation_rows),
        "manifest_sha256": sha(data / "fresh_10_manifest.json"),
        "expectations_sha256": sha(data / "fresh_10_expectations_withheld.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
