#!/usr/bin/env python3
"""Offline V23 pilot preflight; performs no network or model calls."""

from __future__ import annotations

import argparse
import json
import subprocess

from common import load_json, require, sha256_file, sha256_json
from config import (
    FREEZE,
    MAX_OUTER_JOBS,
    PACKAGE,
    PIPELINE_VERSION,
    PR_COMMIT,
    PROGRESS,
    ROOT,
    RUN_ROOT,
    SELECTED_ROW_SLUGS,
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
    require(sources == SOURCE_HASHES == freeze["treatment"]["source_hashes"], "V23 source drift")
    wrappers = {name: sha256_file(ROOT / name) for name in WRAPPER_SOURCE_NAMES}
    require(wrappers == freeze["treatment"]["wrapper_source_hashes"], "pilot wrapper drift")
    require(freeze["treatment"]["pipeline_version"] == PIPELINE_VERSION, "pipeline version drift")
    require(freeze["treatment"]["wrapper_version"] == WRAPPER_VERSION, "wrapper version drift")
    require(tuple(freeze["selected_row_slugs"]) == SELECTED_ROW_SLUGS, "pilot rows changed")
    require(len(freeze["records"]) == 4 and sha256_json(freeze["records"]) == freeze["records_digest"],
            "pilot record manifest changed")
    for item in freeze["records"]:
        require(sha256_file(__import__("pathlib").Path(item["path"])) == item["sha256"],
                f"record changed: {item['row_slug']}")
    require("pilot_v23_all_view_translation" in str(RUN_ROOT), "run root is not isolated")
    if PROGRESS.exists() and not allow_progress:
        require(not load_json(PROGRESS).get("complete"), "pilot already complete; use --allow-progress")
    return {
        "ok": True, "experiment_id": freeze["experiment_id"], "rows": 4,
        "pipeline_version": PIPELINE_VERSION, "wrapper_version": WRAPPER_VERSION,
        "max_outer_jobs": MAX_OUTER_JOBS, "stop_on_first_failure": True,
        "commit": head, "freeze_sha256": sha256_file(FREEZE),
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
