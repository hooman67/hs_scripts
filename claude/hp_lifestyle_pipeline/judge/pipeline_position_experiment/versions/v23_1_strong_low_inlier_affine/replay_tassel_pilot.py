#!/usr/bin/env python3
"""Replay the two preserved Tassel pilot attempts without model calls."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROW = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/"
    "pipeline_position_experiment/pilot_v23_all_view_translation/run/pipeline/rows/"
    "tassel__printer_FrontWide__p1__outer_job_1"
)
OUT = HERE / "calibration/run_1/tassel_pilot_replay.json"
SPEC = importlib.util.spec_from_file_location(
    "v23_1_candidate_invariants", HERE / "candidate_invariants.py"
)
assert SPEC is not None and SPEC.loader is not None
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    guide_path, mask_path = ROW / "geometry_guide.png", ROW / "mask.png"
    attempts = []
    for attempt, fixed_position in ((1, False), (2, True)):
        audit_path = ROW / f"product_invariant_attempt_{attempt}.json"
        output_path = ROW / f"gpt_{attempt}.png"
        old = json.loads(audit_path.read_text())
        started = time.perf_counter()
        result = GUARD.assess_product_affine(
            guide_path.read_bytes(),
            output_path.read_bytes(),
            old["product_bounds_px"],
            fixed_position=fixed_position,
            product_mask=mask_path.read_bytes(),
        )
        attempts.append(
            {
                "attempt": attempt,
                "mode": "first_attempt_all_view" if not fixed_position else "fixed_recovery",
                "fixed_position": fixed_position,
                "runtime_ms": (time.perf_counter() - started) * 1000,
                "inputs": {
                    str(path): sha256(path)
                    for path in (guide_path, mask_path, output_path, audit_path)
                },
                "prior_verdict": old["verdict"],
                "prior_reasons": old["reasons"],
                "candidate_result": result,
            }
        )
    payload = {
        "guard_version": GUARD.GUARD_VERSION,
        "candidate_sha256": sha256(HERE / "candidate_invariants.py"),
        "row": str(ROW),
        "selection_under_v23_policy": next(
            item["attempt"] for item in attempts
            if item["mode"] == "first_attempt_all_view"
            and item["candidate_result"]["verdict"] == "pass"
        ),
        "attempts": attempts,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

