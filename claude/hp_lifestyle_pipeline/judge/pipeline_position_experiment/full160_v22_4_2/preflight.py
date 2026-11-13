#!/usr/bin/env python3
"""Local preflight for the frozen experiment. Performs no network/model calls."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from common import load_json, require, sha256_file, sha256_json
from config import (
    CONTROL_GROUPED_JUDGE_REPORT,
    CONTROL_REPORT,
    FE_VIEWER,
    FREEZE,
    JOB_ROOT,
    PACKAGE,
    PIPELINE_ROOT,
    PIPELINE_VERSION,
    PR_COMMIT,
    PROGRESS,
    PROMPT_EXPORT,
    ROOT,
    RUN_ROOT,
    SOURCE_HASHES,
    WORKTREE,
)


def verify(allow_progress: bool = False) -> dict:
    require(FREEZE.is_file(), f"missing freeze: {FREEZE}")
    freeze = load_json(FREEZE)
    digest_payload = dict(freeze)
    frozen_digest = digest_payload.pop("freeze_payload_sha256")
    require(sha256_json(digest_payload) == frozen_digest, "freeze payload digest mismatch")
    require(freeze["treatment"]["pipeline_version"] == PIPELINE_VERSION, "pipeline version mismatch")
    require(freeze["treatment"]["base_commit"] == PR_COMMIT, "commit mismatch in freeze")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=WORKTREE, text=True).strip()
    require(head == PR_COMMIT, f"worktree moved: {head}")
    actual_sources = {name: sha256_file(PACKAGE / name) for name in SOURCE_HASHES}
    require(actual_sources == SOURCE_HASHES == freeze["treatment"]["source_hashes"], "source hashes changed")
    require(sha256_file(PROMPT_EXPORT) == freeze["prompt_export"]["sha256"], "prompt export changed")
    require(
        sha256_file(CONTROL_REPORT) == freeze["control_report"]["sha256"],
        "control report changed",
    )
    require(
        sha256_file(CONTROL_GROUPED_JUDGE_REPORT)
        == freeze["control_grouped_judge_report"]["sha256"],
        "control grouped judge report changed",
    )
    require(sha256_file(FE_VIEWER) == freeze["fe_viewer"]["sha256"], "canonical FE viewer changed")
    require(len(freeze["records"]) == 160, "freeze does not contain 160 records")
    require(sha256_json(freeze["records"]) == freeze["records_digest"], "record list digest changed")
    for item in freeze["records"]:
        require(sha256_file(__import__("pathlib").Path(item["path"])) == item["sha256"], f"record changed: {item['row_slug']}")

    # Explicitly prevent every previous treatment location from being reused.
    # Both previous full160 trees contain preserved failed first rows.
    forbidden = {
        str(ROOT.parent / "full160"),
        str(ROOT.parent / "smoke/treatment"),
        str(ROOT.parent / "full160_v22_3_3/run"),
        str(ROOT.parent / "full160_v22_4_1/run"),
    }
    for path in (RUN_ROOT, PIPELINE_ROOT, JOB_ROOT):
        require(
            not any(path == Path(item) or Path(item) in path.parents for item in forbidden),
            f"output collides with historical experiment: {path}",
        )
        require("full160_v22_4_2" in str(path), f"output is not isolated under V22.4.2: {path}")
    if PROGRESS.exists() and not allow_progress:
        progress = load_json(PROGRESS)
        require(not progress.get("done"), "progress exists; use --allow-progress to resume")
    return {
        "ok": True,
        "experiment_id": freeze["experiment_id"],
        "rows": 160,
        "banks": len(freeze["group_counts"]),
        "pipeline_version": PIPELINE_VERSION,
        "commit": head,
        "freeze_sha256": sha256_file(FREEZE),
        "records_digest": freeze["records_digest"],
        "isolated_run_root": str(RUN_ROOT),
        "serial_default": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-progress", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.allow_progress), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

