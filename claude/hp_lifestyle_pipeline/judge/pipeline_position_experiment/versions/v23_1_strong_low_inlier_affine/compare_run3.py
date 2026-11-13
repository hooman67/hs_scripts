#!/usr/bin/env python3
"""Compare candidate replay decisions with accepted V23 run 3."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "calibration/run_1/replay_results.json"
RUN3 = (
    HERE.parent / "v23_all_view_translation/calibration/run_3/replay_results.json"
)
OUT = HERE / "calibration/run_1/comparison_to_v23_run3.json"


def load(path: Path):
    return json.loads(path.read_text())


def decisions(payload: dict) -> dict:
    return {
        "real": [
            (item["path"], item["attempt"], item["v23_all_view"]["verdict"],
             item["v23_all_view"].get("reasons", []))
            for item in payload["real"]
        ],
        "frozen_synthetic": [
            (item["fixture"], str(item["transform"]), mode,
             item[mode]["result"]["verdict"],
             item[mode]["result"].get("reasons", []))
            for item in payload["frozen_synthetic"]
            for mode in ("all_view", "fixed_recovery")
        ],
        "added_synthetic": [
            (item["fixture"], item["name"], item.get("fixed_position"),
             item["result"]["verdict"], item["result"].get("reasons", []))
            for item in payload["added_synthetic"]
        ],
        "prior_selections": [
            (item["row"], item["v23_policy_selected_attempt"])
            for item in payload["prior_artifacts"]["rows"]
        ],
        "prior_attempts": [
            (item["row"], attempt["attempt"], attempt["all_view"]["verdict"],
             attempt["all_view"].get("reasons", []),
             attempt["fixed_recovery"]["verdict"],
             attempt["fixed_recovery"].get("reasons", []))
            for item in payload["prior_artifacts"]["rows"]
            for attempt in item["attempts"]
        ],
    }


def main() -> None:
    candidate, run3 = decisions(load(CANDIDATE)), decisions(load(RUN3))
    sections = {}
    for name in candidate:
        before, after = run3[name], candidate[name]
        sections[name] = {
            "run3_count": len(before),
            "candidate_count": len(after),
            "identical": before == after,
            "changed": [
                {"index": index, "run3": old, "candidate": new}
                for index, (old, new) in enumerate(zip(before, after)) if old != new
            ],
        }
    payload = {
        "comparison": "candidate decisions versus accepted V23 run 3",
        "all_sections_identical": all(item["identical"] for item in sections.values()),
        "sections": sections,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
