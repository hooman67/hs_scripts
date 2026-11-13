#!/usr/bin/env python3
"""Summarize frozen run-1/run-2 versus final run-3 V23 guard evidence."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load(path: Path):
    return json.loads(path.read_text())


def selected(rows):
    return {row["row"]: row for row in rows}


def main() -> None:
    run1 = load(ROOT / "run_1/replay_results.json")
    run2 = load(ROOT / "run_2/replay_results.json")
    final = load(ROOT / "run_3/replay_results.json")
    first = selected(run1["prior_artifacts"]["rows"])
    second = selected(run2["prior_artifacts"]["rows"])
    last = selected(final["prior_artifacts"]["rows"])
    lost1 = {
        key for key, row in first.items()
        if row.get("old_selection_observable")
        and row["old_selected_attempt"] is not None
        and row["v23_policy_selected_attempt"] is None
    }
    lost2 = {
        key for key, row in second.items()
        if row.get("old_selection_observable")
        and row["old_selected_attempt"] is not None
        and row["v23_policy_selected_attempt"] is None
    }
    lost3 = {
        key for key, row in last.items()
        if row.get("old_selection_observable")
        and row["old_selected_attempt"] is not None
        and row["v23_policy_selected_attempt"] is None
    }
    brightness = []
    fixed_12px = []
    for row in final["frozen_synthetic"]:
        if row["transform"] == "brightness_shift":
            brightness.append({
                "fixture": row["fixture"],
                "all_view": row["all_view"]["result"]["verdict"],
                "fixed_recovery": row["fixed_recovery"]["result"]["verdict"],
            })
        if row["transform"] == "excess_translation_12px":
            fixed_12px.append({
                "fixture": row["fixture"],
                "all_view": row["all_view"]["result"]["verdict"],
                "fixed_recovery": row["fixed_recovery"]["result"]["verdict"],
                "fixed_recovery_reasons": row["fixed_recovery"]["result"]["reasons"],
            })
    edge = [
        {"fixture": row["fixture"], "case": row["name"],
         "expected": row["expected"], "actual": row["result"]["verdict"],
         "reasons": row["result"]["reasons"]}
        for row in final["added_synthetic"]
        if row["name"].startswith(("legal_top_left_extreme", "legal_bottom_right_extreme",
                                   "one_pixel_crop_left", "one_pixel_crop_right"))
    ]
    comparison = {
        "run_1_source_sha256": run1["guard_source_sha256"],
        "run_2_source_sha256": run2["guard_source_sha256"],
        "run_3_source_sha256": final["guard_source_sha256"],
        "run_1_summary": run1["summary"],
        "run_2_summary": run2["summary"],
        "run_3_summary": final["summary"],
        "selection_compatibility": {
            "run_1_previously_selected_now_lost": len(lost1),
            "run_2_previously_selected_now_lost": len(lost2),
            "run_3_previously_selected_now_lost": len(lost3),
            "recovered_by_run_3_from_run_1": sorted(lost1 - lost3),
            "recovered_by_run_3_from_run_2": sorted(lost2 - lost3),
            "remaining_lost_in_run_3": sorted(lost3),
            "newly_lost_in_run_3_vs_run_1": sorted(lost3 - lost1),
            "newly_lost_in_run_3_vs_run_2": sorted(lost3 - lost2),
        },
        "brightness_shift": brightness,
        "fixed_12px": fixed_12px,
        "frame_edge_and_crop": edge,
    }
    output = ROOT / "run_3/run_comparison.json"
    output.write_text(json.dumps(comparison, indent=2) + "\n")
    print(json.dumps({
        "run_1_lost": len(lost1),
        "run_2_lost": len(lost2),
        "run_3_lost": len(lost3),
        "recovered_run_1_to_3": len(lost1 - lost3),
        "recovered_run_2_to_3": len(lost2 - lost3),
        "remaining": len(lost3),
        "brightness_fail_mode_checks": sum(
            row[mode] == "fail" for row in brightness for mode in ("all_view", "fixed_recovery")),
        "fixed_12px_all_view_pass": sum(row["all_view"] == "pass" for row in fixed_12px),
        "fixed_12px_recovery_fail": sum(row["fixed_recovery"] == "fail" for row in fixed_12px),
        "edge_unverifiable": sum(row["actual"] == "unverifiable" for row in edge),
    }, indent=2))


if __name__ == "__main__":
    main()
