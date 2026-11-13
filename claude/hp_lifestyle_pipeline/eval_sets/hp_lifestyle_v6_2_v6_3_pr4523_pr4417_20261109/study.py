#!/usr/bin/env python3
"""Freeze and execute the four exact-pipeline, thirty-row HP comparison cells."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
LEGACY = PROJECT / "eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108"
BASELINE = LEGACY / "exports/v6.2-surfaces-20261109-r5-final/prompts_all_160.json"
V63 = HERE / "revisions/v6.3-hp-associations-20261110-r2-recognition/exports/final/prompts_all_160.json"
REMOTE = "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev"
PREFIX = "eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109"
BUCKET = "foundry-hp-enterprise-adobe-assets"
COMMITS = {
    "pr4523": "d1e5ae5323dedebc3b06ed173a3731307bd0623a",
    "pr4417": "1f66c0b68c5ecdc7bee8ace9fa247ee72e04e6dc",
}
PIPELINES = {
    "pr4523": "unified-blue-scale-v21.3-surface-shapes-geometry-from-guide",
    "pr4417": "unified-blue-scale-v21.2-disjoint-stage-b-fields-geometry-from-guide",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")


def image_runner():
    spec = importlib.util.spec_from_file_location("hp_frozen_image_runner", LEGACY / "run_generation.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def paired_key(row):
    return row["device_id"], row["camera_tag"], row["bank_rank"]


def validate_matched(selected, full):
    rows = selected["prompts"]
    if len(rows) != 30 or len({paired_key(row) for row in rows}) != 30:
        raise ValueError("the selection must contain thirty unique device/camera/rank keys")
    original = {row["prompt_key"]: row for row in full["prompts"]}
    if any(row != original.get(row["prompt_key"]) for row in rows):
        raise ValueError("selected records differ from the actual full source records")
    banks = {}
    for row in rows:
        bank = row["device_id"], row["camera_tag"]
        banks[bank] = banks.get(bank, 0) + 1
    if len(banks) != 16 or sorted(banks.values()) != [1, 1] + [2] * 14:
        raise ValueError("selection does not cover all sixteen banks with the 30-row quotas")
    return {paired_key(row) for row in rows}


def catalog_lineage(name, url, catalog):
    rewriter = catalog["rewriterVersion"]
    if f"#{name[2:]}" not in rewriter or COMMITS[name][:12] not in rewriter:
        raise ValueError(f"{name} live catalog does not identify its pinned PR/commit")
    if PIPELINES[name] not in rewriter:
        raise ValueError(f"{name} live catalog does not identify the expected pipeline")
    candidate = catalog.get("candidateLineage") or {}
    if candidate and candidate.get("sourceCommit") != COMMITS[name]:
        raise ValueError(f"{name} candidate source commit differs from the exact PR")
    return {
        "endpoint_base_url": url,
        "expected_generator": "GPT Image 2.5 / single reference / no grading",
        "expected_rewriter": rewriter,
        "expected_pipeline_version": PIPELINES[name],
        "lineage_label": candidate.get("candidateId", f"exact-{name}-{COMMITS[name][:12]}"),
        "lineage_source_commit": COMMITS[name],
        "lineage_patch_sha256": candidate.get("patchSha256"),
        "lineage_runtime_tree_sha256": candidate.get("codeTreeSha256"),
        "lineage_source_manifest_sha256": candidate.get("candidateManifestSha256"),
        "lineage_deployment_manifest_sha256": candidate.get("deploymentManifestSha256"),
        "lineage_candidate_config_sha256": candidate.get("configSha256"),
    }


def prepare():
    if (HERE / "study_manifest.json").exists():
        raise FileExistsError("study already frozen; do not replace its identity")
    sources = {"v6_2": BASELINE, "v6_3": V63}
    selections = {writer: HERE / f"selection/exports/selected_{writer}_30.json" for writer in sources}
    documents = {writer: load(path) for writer, path in sources.items()}
    selected = {writer: load(path) for writer, path in selections.items()}
    keys = [validate_matched(selected[writer], documents[writer]) for writer in sources]
    if keys[0] != keys[1]:
        raise ValueError("V6.2 and V6.3 are not matched by device/camera/bank rank")
    runner = image_runner()
    endpoints = {}
    for name, url in (("pr4523", "http://127.0.0.1:8138"), ("pr4417", REMOTE)):
        response = httpx.get(url + "/api/catalog", timeout=60)
        response.raise_for_status()
        endpoints[name] = catalog_lineage(name, url, response.json())
    cells = []
    for writer, source in sources.items():
        for endpoint, settings in endpoints.items():
            name = f"{writer}_{endpoint}"
            selection_file = HERE / f"selection/bindings/{name}.json"
            write_new(selection_file, {
                "source_prompts_sha256": sha(source),
                "row_ids": [row["prompt_key"] for row in selected[writer]["prompts"]],
                "rows": selected[writer]["prompts"],
            })
            cells.append({
                "name": name, "writer": writer, "pr": endpoint,
                "source": str(source), "source_sha256": sha(source),
                "selected": str(selections[writer]), "selected_sha256": sha(selections[writer]),
                "selection_file": str(selection_file), "selection_sha256": sha(selection_file),
                "run_dir": str(HERE / "runs" / name),
                "lineage_args": settings,
            })
    manifest = {
        "version": "hp-v62-v63-exact-pr-comparison-v1",
        "selected_per_writer": 30, "new_image_count": 120,
        "historical_reference_count": 30,
        "matching": "device_id + camera_tag + bank_rank; not semantic equivalence",
        "historical_lineage": "PR4349/8c358bc7989c + local V20 surface-shape-r1; NOT PR4523",
        "image_runner_path": str(LEGACY / "run_generation.py"),
        "image_runner_sha256": sha(LEGACY / "run_generation.py"),
        "orchestrator_sha256": sha(Path(__file__)),
        "selection_report_sha256": sha(HERE / "selection/exports/selection_report.json"),
        "cells": cells,
    }
    for cell in cells:
        run_cell(cell, preflight=True)
    write_new(HERE / "study_manifest.json", manifest)
    print(json.dumps({"status": "prepared", "new_images": 120, "historical_images": 30}))


def run_cell(cell, *, preflight=False, row_ids=None):
    command = [
        sys.executable, str(LEGACY / "run_generation.py"),
        "--prompts", cell["source"], "--prompts-sha256", cell["source_sha256"],
        "--run-dir", cell["run_dir"], "--prefix", PREFIX + "/runs/" + cell["name"],
        "--workers", "2", "--no-publish",
    ]
    for key, value in cell["lineage_args"].items():
        if value is not None:
            command.extend(["--" + key.replace("_", "-"), value])
    if row_ids is not None:
        command.extend(["--row-ids", *row_ids])
    else:
        command.extend(["--selection-file", cell["selection_file"]])
    if preflight:
        command.append("--preflight-only")
    log = HERE / "logs" / f"{cell['name']}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as output:
        subprocess.run(command, stdout=output, stderr=subprocess.STDOUT, check=True)


def verified_manifest():
    manifest = load(HERE / "study_manifest.json")
    if manifest["image_runner_sha256"] != sha(LEGACY / "run_generation.py"):
        raise ValueError("the frozen runner changed")
    if manifest["orchestrator_sha256"] != sha(Path(__file__)):
        raise ValueError("the frozen study orchestrator changed")
    if manifest["selection_report_sha256"] != sha(HERE / "selection/exports/selection_report.json"):
        raise ValueError("the selection report changed")
    for cell in manifest["cells"]:
        for field in ("source", "selected", "selection"):
            path = Path(cell["selection_file"] if field == "selection" else cell[field])
            if sha(path) != cell[field + "_sha256"]:
                raise ValueError(f"{cell['name']}: {field} bytes changed")
    return manifest


def validate_cells(manifest, *, require_complete):
    runner = image_runner()
    result = {}
    for cell in manifest["cells"]:
        source = Path(cell["source"])
        rows = runner.validate_prompt_document(load(source), source, cell["source_sha256"])
        selected = set(load(Path(cell["selection_file"]))["row_ids"])
        run_dir = Path(cell["run_dir"])
        records = {row["row_id"]: runner.valid_completed_record(run_dir, row)
                   for row in rows if row["row_id"] in selected}
        failed = []
        for row in rows:
            if row["row_id"] not in selected or records[row["row_id"]]:
                continue
            record_path = runner.paths(run_dir, row)["record"]
            if record_path.is_file():
                failed.append(row["row_id"])
        result[cell["name"]] = {"expected": 30, "done": sum(value is not None for value in records.values()),
                                "failed": len(failed), "failed_keys": failed}
    if require_complete and any(item["done"] != 30 or item["failed"] for item in result.values()):
        raise ValueError(f"study incomplete: {json.dumps(result)}")
    return result


def generate(*, smoke, paid, reviewed=False):
    if not paid:
        raise PermissionError("paid execution requires --paid-calls-authorized")
    manifest = verified_manifest()
    if not smoke and (not reviewed or not (HERE / "smoke_complete.json").is_file()):
        raise PermissionError("inspect the successful eight-image smoke, then pass --smoke-reviewed")
    before = validate_cells(manifest, require_complete=False)
    if any(item["failed"] for item in before.values()):
        raise ValueError("inspect existing terminal failures before any continuation")
    smoke_rows = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = []
        for cell in manifest["cells"]:
            row_ids = None
            if smoke:
                prompts = load(Path(cell["selected"]))["prompts"]
                laptops = [row for row in prompts if row["device_type"] == "laptop"]
                printers = [row for row in prompts if row["device_type"] == "printer"]
                laptop = next((row for row in laptops if row["primary_support"]["shape"] == "round"), laptops[0])
                printer = next((row for row in printers if row["primary_support"]["family"] != "table"), printers[0])
                row_ids = [laptop["prompt_key"], printer["prompt_key"]]
                smoke_rows[cell["name"]] = row_ids
            futures.append(pool.submit(run_cell, cell, row_ids=row_ids))
        for future in concurrent.futures.as_completed(futures):
            future.result()
    counts = validate_cells(manifest, require_complete=not smoke)
    print(json.dumps(counts, indent=2))
    if any(item["failed"] for item in counts.values()):
        raise RuntimeError("bounded smoke has failed records; do not continue the full queues")
    if smoke:
        if any(value["done"] != 2 for value in counts.values()):
            raise ValueError("the bounded smoke did not produce exactly two valid images per cell")
        write_new(HERE / "smoke_complete.json", {
            "status": "technical_contracts_passed_not_visual_acceptance",
            "rows": smoke_rows, "cells": counts,
            "selection": "prefer a round laptop support and a non-table printer support when available",
        })
    else:
        write_new(HERE / "completion.json", {"status": "complete", "cells": counts, "new_images": 120})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "smoke", "generate", "status"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    parser.add_argument("--smoke-reviewed", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "status":
        print(json.dumps(validate_cells(verified_manifest(), require_complete=False), indent=2))
    else:
        generate(smoke=args.command == "smoke", paid=args.paid_calls_authorized, reviewed=args.smoke_reviewed)


if __name__ == "__main__":
    main()
