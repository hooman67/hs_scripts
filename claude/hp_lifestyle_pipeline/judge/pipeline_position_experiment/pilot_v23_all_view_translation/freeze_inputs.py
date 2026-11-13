#!/usr/bin/env python3
"""Freeze the V23 source and four audited V6.1 pilot rows; no network calls."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess

from common import atomic_json, load_json, require, sha256_file, sha256_json
from config import (
    EXPECTED_CELLS,
    EXPERIMENT_ID,
    FREEZE,
    PACKAGE,
    PIPELINE_VERSION,
    PR_COMMIT,
    RECORDS,
    ROOT,
    SELECTED_ROW_SLUGS,
    SOURCE_HASHES,
    WORKTREE,
    WRAPPER_SOURCE_NAMES,
    WRAPPER_VERSION,
)


def collect() -> dict:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=WORKTREE, text=True).strip()
    require(head == PR_COMMIT, f"worktree HEAD changed: {head}")
    sources = {name: sha256_file(PACKAGE / name) for name in SOURCE_HASHES}
    require(sources == SOURCE_HASHES, f"V23 source mismatch: {sources}")
    wrappers = {name: sha256_file(ROOT / name) for name in WRAPPER_SOURCE_NAMES}
    records = []
    cells = []
    for slug in SELECTED_ROW_SLUGS:
        path = RECORDS / f"{slug}.json"
        require(path.is_file(), f"missing record: {path}")
        record = load_json(path)
        require(record["row_slug"] == slug and int(record["bank_rank"]) == 1,
                f"wrong frozen row: {slug}")
        require(record["prompt_sha256"] == hashlib.sha256(record["prompt"].encode()).hexdigest(),
                f"prompt digest mismatch: {slug}")
        cell = (record["device_type"], record["camera_id"])
        cells.append(cell)
        records.append({
            "path": str(path.resolve()), "sha256": sha256_file(path),
            "row_id": record["row_id"], "row_slug": slug,
            "device_id": record["device_id"], "digital_twin_id": record["digital_twin_id"],
            "device_type": record["device_type"], "camera_id": record["camera_id"],
            "camera_tag": record["camera_tag"], "bank_rank": 1,
            "prompt_sha256": record["prompt_sha256"], "control_job_id": record["job_id"],
            "control_image_sha256": record["image_sha256"],
        })
    require(tuple(cells) == EXPECTED_CELLS, f"four-cell selection changed: {cells}")
    manifest = {
        "schema_version": "hp-position-flex-v23-four-row-pilot-freeze-v1",
        "experiment_id": EXPERIMENT_ID,
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "treatment": {
            "pipeline_version": PIPELINE_VERSION, "base_pr": "Adobe-Firefly/foundry#4349",
            "base_commit": PR_COMMIT, "source_hashes": sources,
            "wrapper_version": WRAPPER_VERSION, "wrapper_source_hashes": wrappers,
            "policy": "Frozen V23 source; serial four-row pilot; one immutable job per row; stop on first terminal failure.",
        },
        "records_directory": str(RECORDS.resolve()), "records": records,
        "records_digest": sha256_json(records), "selected_row_slugs": list(SELECTED_ROW_SLUGS),
        "expected_cells": [list(x) for x in EXPECTED_CELLS],
    }
    manifest["freeze_payload_sha256"] = sha256_json(manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    candidate = collect()
    if args.verify_only:
        require(FREEZE.is_file(), f"missing freeze: {FREEZE}")
        frozen = load_json(FREEZE)
        for key in ("created_at_utc", "freeze_payload_sha256"):
            candidate.pop(key, None)
            frozen.pop(key, None)
        require(candidate == frozen, "live inputs, source, or wrapper differ from freeze")
        print(json.dumps({"ok": True, "rows": 4, "freeze": str(FREEZE)}, indent=2))
        return 0
    require(not FREEZE.exists(), f"refusing to overwrite freeze: {FREEZE}")
    atomic_json(FREEZE, candidate)
    print(json.dumps({"freeze": str(FREEZE), "sha256": sha256_file(FREEZE)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
