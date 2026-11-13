#!/usr/bin/env python3
"""Freeze the exact V6.1 records, prompt export, FE sources, and V22.4.2 pipeline code plus V22.4.2.1 wrapper code.

This script is local-only: it performs no network or model calls. Re-running it
is intentionally refused once ``freeze.json`` exists unless ``--verify-only``
is supplied; this prevents a later checkout mutation from silently redefining
the experiment.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
from collections import Counter

from common import atomic_json, load_json, require, sha256_file, sha256_json
from config import (
    CONTROL_GROUPED_JUDGE_REPORT,
    CONTROL_REPORT,
    EXPERIMENT_ID,
    FE_VIEWER,
    FREEZE,
    PACKAGE,
    PIPELINE_VERSION,
    PR_COMMIT,
    PROMPT_EXPORT,
    PROMPT_EXPORT_SHA256,
    RECORDS,
    ROOT,
    SOURCE_HASHES,
    WORKTREE,
    WRAPPER_SOURCE_NAMES,
    WRAPPER_VERSION,
)


def collect() -> dict:
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=WORKTREE, text=True
    ).strip()
    require(head == PR_COMMIT, f"worktree HEAD changed: {head}")
    actual_sources = {name: sha256_file(PACKAGE / name) for name in SOURCE_HASHES}
    require(actual_sources == SOURCE_HASHES, f"V22.4.2 source mismatch: {actual_sources}")
    wrapper_hashes = {name: sha256_file(ROOT / name) for name in WRAPPER_SOURCE_NAMES}
    require(sha256_file(PROMPT_EXPORT) == PROMPT_EXPORT_SHA256, "prompt export hash changed")

    export = load_json(PROMPT_EXPORT)
    exported = export.get("prompts")
    require(isinstance(exported, list) and len(exported) == 160, "prompt export must contain 160 prompts")
    prompt_by_key = {row["prompt_key"]: row for row in exported}
    require(len(prompt_by_key) == 160, "prompt keys are not unique")

    record_paths = sorted(RECORDS.glob("*.json"))
    require(len(record_paths) == 160, f"expected 160 record files; found {len(record_paths)}")
    records = []
    group_counts: Counter[str] = Counter()
    ranks: dict[str, set[int]] = {}
    for path in record_paths:
        record = load_json(path)
        row_id = record["row_id"]
        row_slug = record["row_slug"]
        require(path.stem == row_slug, f"record filename/slug mismatch: {path}")
        require(row_id in prompt_by_key, f"record absent from prompt export: {row_id}")
        require(prompt_by_key[row_id]["text"] == record["prompt"], f"prompt text mismatch: {row_id}")
        require(
            record["prompt_sha256"] == hashlib.sha256(record["prompt"].encode()).hexdigest(),
            f"prompt hash mismatch: {row_id}",
        )
        group = f"{record['device_id']}__{record['camera_tag']}"
        rank = int(record["bank_rank"])
        group_counts[group] += 1
        ranks.setdefault(group, set()).add(rank)
        records.append(
            {
                "path": str(path.resolve()),
                "sha256": sha256_file(path),
                "row_id": row_id,
                "row_slug": row_slug,
                "device_id": record["device_id"],
                "digital_twin_id": record["digital_twin_id"],
                "device_type": record["device_type"],
                "camera_id": record["camera_id"],
                "camera_tag": record["camera_tag"],
                "bank_rank": rank,
                "prompt_sha256": record["prompt_sha256"],
                "control_job_id": record["job_id"],
                "control_image_sha256": record["image_sha256"],
            }
        )
    require(len(group_counts) == 16, f"expected 16 banks; found {len(group_counts)}")
    require(set(group_counts.values()) == {10}, f"every bank must have ten rows: {group_counts}")
    require(all(value == set(range(1, 11)) for value in ranks.values()), "bank ranks must be 1..10")

    manifest = {
        "schema_version": "hp-position-flex-full160-freeze-v1",
        "experiment_id": EXPERIMENT_ID,
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "treatment": {
            "pipeline_version": PIPELINE_VERSION,
            "base_pr": "Adobe-Firefly/foundry#4349",
            "base_commit": PR_COMMIT,
            "source_hashes": actual_sources,
            "wrapper_version": WRAPPER_VERSION,
            "wrapper_source_hashes": wrapper_hashes,
            "policy": (
                "V22.4.2 density-aware x-y translation with the full-affine guard, "
                "a calibrated alpha-masked fixed-position fallback for no/too-few "
                "descriptors or affine-fit failure at boundary agreement >= 0.80, and one bounded "
                "fixed-position image retry"
            ),
        },
        "prompt_export": {
            "path": str(PROMPT_EXPORT.resolve()),
            "sha256": PROMPT_EXPORT_SHA256,
            "count": 160,
        },
        "records_directory": str(RECORDS.resolve()),
        "records_digest": sha256_json(records),
        "records": records,
        "group_counts": dict(sorted(group_counts.items())),
        "control_report": {
            "path": str(CONTROL_REPORT.resolve()),
            "sha256": sha256_file(CONTROL_REPORT),
        },
        "control_grouped_judge_report": {
            "path": str(CONTROL_GROUPED_JUDGE_REPORT.resolve()),
            "sha256": sha256_file(CONTROL_GROUPED_JUDGE_REPORT),
        },
        "fe_viewer": {"path": str(FE_VIEWER.resolve()), "sha256": sha256_file(FE_VIEWER)},
    }
    manifest["freeze_payload_sha256"] = sha256_json(manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    candidate = collect()
    if args.verify_only:
        require(FREEZE.is_file(), f"missing frozen manifest: {FREEZE}")
        frozen = load_json(FREEZE)
        # Time and the self-digest do not participate in live verification.
        for key in ("created_at_utc", "freeze_payload_sha256"):
            candidate.pop(key, None)
            frozen.pop(key, None)
        require(candidate == frozen, "live inputs or code differ from freeze.json")
        print(json.dumps({"ok": True, "freeze": str(FREEZE), "rows": 160, "banks": 16}, indent=2))
        return 0
    require(not FREEZE.exists(), f"refusing to overwrite existing freeze: {FREEZE}")
    atomic_json(FREEZE, candidate)
    print(json.dumps({"freeze": str(FREEZE), "sha256": sha256_file(FREEZE)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

