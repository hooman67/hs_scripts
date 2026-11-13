#!/usr/bin/env python3
"""Freeze V23.1 source and eight audited pilot rows; no network calls."""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path

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
    SELECTED_ROWS,
    SOURCE_HASHES,
    WORKTREE,
    WRAPPER_SOURCE_NAMES,
    WRAPPER_VERSION,
)
from diagnostic_prompts import PROMPTS
from diagnostic_prompts import SOURCE as DIAGNOSTIC_PROMPT_SOURCE


def audited_diagnostic_prompts(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "RELOCATION_PROMPTS"
            for target in node.targets
        ):
            source = ast.literal_eval(node.value)
            return {f"{slug}__relocation_demand": prompt for slug, prompt in source.items()}
    raise RuntimeError(f"RELOCATION_PROMPTS missing from {path}")


def collect() -> dict:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=WORKTREE, text=True).strip()
    require(head == PR_COMMIT, f"worktree HEAD changed: {head}")
    sources = {name: sha256_file(PACKAGE / name) for name in SOURCE_HASHES}
    require(sources == SOURCE_HASHES, f"V23.1 source mismatch: {sources}")
    wrappers = {name: sha256_file(ROOT / name) for name in WRAPPER_SOURCE_NAMES}
    diagnostic_source = Path(DIAGNOSTIC_PROMPT_SOURCE)
    require(diagnostic_source.is_file(), f"missing diagnostic prompt source: {diagnostic_source}")
    require(PROMPTS == audited_diagnostic_prompts(diagnostic_source),
            "packaged diagnostic prompts differ from audited source")

    records = []
    cells = []
    for execution_slug, source_slug, cohort in SELECTED_ROWS:
        path = RECORDS / f"{source_slug}.json"
        require(path.is_file(), f"missing record: {path}")
        record = load_json(path)
        require(record["row_slug"] == source_slug and int(record["bank_rank"]) == 1,
                f"wrong frozen source row: {source_slug}")
        source_prompt_sha = hashlib.sha256(record["prompt"].encode()).hexdigest()
        require(record["prompt_sha256"] == source_prompt_sha, f"source prompt mismatch: {source_slug}")
        prompt = record["prompt"] if cohort == "representative_v6_1" else PROMPTS[execution_slug]
        prompt_sha = hashlib.sha256(prompt.encode()).hexdigest()
        cells.append((cohort, record["device_type"], record["camera_id"]))
        records.append({
            "path": str(path.resolve()),
            "sha256": sha256_file(path),
            "row_id": record["row_id"],
            "row_slug": execution_slug,
            "source_row_slug": source_slug,
            "cohort": cohort,
            "device_id": record["device_id"],
            "digital_twin_id": record["digital_twin_id"],
            "device_type": record["device_type"],
            "camera_id": record["camera_id"],
            "camera_tag": record["camera_tag"],
            "bank_rank": 1,
            "prompt": prompt,
            "prompt_sha256": prompt_sha,
            "source_prompt_sha256": source_prompt_sha,
            "control_job_id": record["job_id"],
            "control_image_sha256": record["image_sha256"],
        })
    require(tuple(cells) == EXPECTED_CELLS, f"eight-cell selection changed: {cells}")
    require(len({x["row_slug"] for x in records}) == 8, "execution slugs are not unique")
    require(sum(x["cohort"] == "representative_v6_1" for x in records) == 4,
            "representative cohort changed")
    require(sum(x["cohort"] == "movement_demand_diagnostic" for x in records) == 4,
            "diagnostic cohort changed")

    manifest = {
        "schema_version": "hp-position-flex-v23.1-eight-row-pilot-freeze-v1",
        "experiment_id": EXPERIMENT_ID,
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "treatment": {
            "pipeline_version": PIPELINE_VERSION,
            "base_pr": "Adobe-Firefly/foundry#4349",
            "base_commit": PR_COMMIT,
            "source_hashes": sources,
            "wrapper_version": WRAPPER_VERSION,
            "wrapper_source_hashes": wrappers,
            "policy": (
                "Frozen V23.1 source; serial eight-row pilot; one immutable job per row; "
                "stop and preserve on first terminal failure."
            ),
        },
        "cohorts": {
            "representative_v6_1": (
                "The four original rank-1 Cashmere/Tassel V6.1 representative prompts."
            ),
            "movement_demand_diagnostic": (
                "Four existing audited Cashmere/Magic movement-demand prompts from run_v22_smoke.py, "
                "replayed with their corresponding frozen V6.1 product, Stage-A and guide inputs."
            ),
        },
        "diagnostic_prompt_source": {
            "path": str(diagnostic_source.resolve()),
            "sha256": sha256_file(diagnostic_source),
        },
        "records_directory": str(RECORDS.resolve()),
        "records": records,
        "records_digest": sha256_json(records),
        "selected_row_slugs": [x["row_slug"] for x in records],
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
        require(candidate == frozen, "live inputs, source, prompts, or wrappers differ from freeze")
        print(json.dumps({"ok": True, "rows": 8, "freeze": str(FREEZE)}, indent=2))
        return 0
    require(not FREEZE.exists(), f"refusing to overwrite freeze: {FREEZE}")
    atomic_json(FREEZE, candidate)
    print(json.dumps({"freeze": str(FREEZE), "sha256": sha256_file(FREEZE)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
