#!/usr/bin/env python3
"""Offline V23.1 pilot preflight; performs no network or model calls."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from common import load_json, require, sha256_file, sha256_json
from config import (
    EXPECTED_CELLS,
    FREEZE,
    MAX_OUTER_JOBS,
    PACKAGE,
    PIPELINE_VERSION,
    PR_COMMIT,
    PROGRESS,
    ROOT,
    RUN_ROOT,
    SELECTED_ROWS,
    SOURCE_HASHES,
    WORKTREE,
    WRAPPER_SOURCE_NAMES,
    WRAPPER_VERSION,
)


def verify(allow_progress: bool = False) -> dict:
    require(FREEZE.is_file(), f"missing freeze: {FREEZE}")
    freeze = load_json(FREEZE)
    payload = dict(freeze)
    digest = payload.pop("freeze_payload_sha256")
    require(sha256_json(payload) == digest, "freeze payload digest mismatch")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=WORKTREE, text=True).strip()
    require(head == PR_COMMIT == freeze["treatment"]["base_commit"], "Foundry commit changed")
    sources = {name: sha256_file(PACKAGE / name) for name in SOURCE_HASHES}
    require(sources == SOURCE_HASHES == freeze["treatment"]["source_hashes"], "V23.1 source drift")
    wrappers = {name: sha256_file(ROOT / name) for name in WRAPPER_SOURCE_NAMES}
    require(wrappers == freeze["treatment"]["wrapper_source_hashes"], "pilot wrapper drift")
    require(freeze["treatment"]["pipeline_version"] == PIPELINE_VERSION, "pipeline version drift")
    require(freeze["treatment"]["wrapper_version"] == WRAPPER_VERSION, "wrapper version drift")
    expected_slugs = [x[0] for x in SELECTED_ROWS]
    require(freeze["selected_row_slugs"] == expected_slugs, "pilot rows changed")
    require(tuple(tuple(x) for x in freeze["expected_cells"]) == EXPECTED_CELLS, "cells changed")
    require(len(freeze["records"]) == 8 and sha256_json(freeze["records"]) == freeze["records_digest"],
            "pilot record manifest changed")
    for item in freeze["records"]:
        require(sha256_file(Path(item["path"])) == item["sha256"],
                f"record changed: {item['source_row_slug']}")
        require(__import__("hashlib").sha256(item["prompt"].encode()).hexdigest()
                == item["prompt_sha256"], f"prompt changed: {item['row_slug']}")
    diagnostic = freeze["diagnostic_prompt_source"]
    require(sha256_file(Path(diagnostic["path"])) == diagnostic["sha256"],
            "diagnostic prompt source drift")
    require("pilot_v23_1_all_view_translation" in str(RUN_ROOT), "run root is not isolated")
    if PROGRESS.exists() and not allow_progress:
        require(not load_json(PROGRESS).get("complete"), "pilot already complete; use --allow-progress")
    return {
        "ok": True,
        "experiment_id": freeze["experiment_id"],
        "rows": 8,
        "representative_rows": 4,
        "movement_demand_rows": 4,
        "pipeline_version": PIPELINE_VERSION,
        "wrapper_version": WRAPPER_VERSION,
        "max_outer_jobs": MAX_OUTER_JOBS,
        "stop_on_first_failure": True,
        "commit": head,
        "freeze_sha256": sha256_file(FREEZE),
        "run_root": str(RUN_ROOT),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-progress", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.allow_progress), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
