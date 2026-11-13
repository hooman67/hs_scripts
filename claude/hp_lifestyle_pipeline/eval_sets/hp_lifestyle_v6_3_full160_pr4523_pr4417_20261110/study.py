#!/usr/bin/env python3
"""Extend the frozen V6.3 exact-PR study, without resampling or rewriting old runs."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

import httpx

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
OLD = HERE.parent / "hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109"
PREFIX = "eval_sets/" + HERE.name
BUCKET = "foundry-hp-enterprise-adobe-assets"
SOURCE = OLD / "revisions/v6.3-hp-associations-20261110-r2-recognition/exports/final/prompts_all_160.json"
SOURCE_SHA = "c0e7553848c3226a0bc3a83c24f161e6ff601ff76f8f0e0557f5bb5b317448c8"
RUNNER = PROJECT / "eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/run_generation.py"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write(path, value, *, exclusive=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x" if exclusive else "w", encoding="utf-8") as handle:
        handle.write(value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def image_runner():
    return module("full160_native_runner", RUNNER)


def partition(document, selected):
    all_rows = {r["prompt_key"]: r for r in document["prompts"]}
    if len(all_rows) != 160 or len(selected) != 30 or len(set(selected)) != 30:
        raise ValueError("expected unique160 universe and unique30 reuse")
    if not set(selected) <= all_rows.keys():
        raise ValueError("reuse keys are not in the frozen universe")
    fresh = [key for key in all_rows if key not in selected]
    if len(fresh) != 130 or set(fresh) & set(selected) or set(fresh) | set(selected) != all_rows.keys():
        raise ValueError("partition is not exactly30 reused +130 new")
    return fresh


def row_for(prompt):
    return {"row_id": prompt["prompt_key"], "row_slug": image_runner().slug(prompt["prompt_key"]),
            "prompt_sha256": hashlib.sha256(prompt["text"].encode()).hexdigest()}


def command(cell, preflight=False, existing_only=False):
    result = [sys.executable, str(RUNNER), "--prompts", str(SOURCE),
              "--prompts-sha256", SOURCE_SHA, "--run-dir", cell["run_dir"],
              "--prefix", PREFIX + "/runs/" + cell["name"], "--workers", "4", "--no-publish",
              "--twin-dir", cell["twin_dir"], "--selection-file", cell["selection_file"]]
    for key, value in cell["lineage_args"].items():
        if value is not None:
            result += ["--" + key.replace("_", "-"), value]
    if preflight:
        result.append("--preflight-only")
    if existing_only:
        result.append("--existing-jobs-only")
    return result


def run(cell, **kwargs):
    log = HERE / "logs" / (cell["name"] + ".log")
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as out:
        subprocess.run(command(cell, **kwargs), stdout=out, stderr=subprocess.STDOUT,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, check=True)


def prepare():
    if (HERE / "study_manifest.json").exists():
        raise FileExistsError("study identity is already frozen")
    runner = image_runner()
    document = load(SOURCE)
    runner.validate_prompt_document(document, SOURCE, SOURCE_SHA)
    old_module = module("old_hp_study_readonly", OLD / "study.py")
    old_manifest = old_module.verified_manifest()
    cells = []
    preserved = {str(RUNNER): sha(RUNNER), str(OLD / "study.py"): sha(OLD / "study.py"),
                 str(OLD / "report.py"): sha(OLD / "report.py")}
    # Existing immutable evidence remains in place. New native jobs may only add files.
    for root in ("runs", "revisions", "selection", "input_audit", "endpoint_pr4523"):
        for path in (OLD / root).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".log", ".pyc"}:
                preserved[str(path)] = sha(path)
    for name in ("study_manifest.json", "final_audit.json", "publication_receipt.json"):
        preserved[str(OLD / name)] = sha(OLD / name)
    for prior in old_manifest["cells"]:
        if prior["writer"] != "v6_3":
            continue
        selected = load(prior["selection_file"])["row_ids"]
        fresh = partition(document, selected)
        prompts = {p["prompt_key"]: p for p in document["prompts"]}
        reuse = []
        for key in selected:
            row = row_for(prompts[key])
            record = runner.valid_completed_record(Path(prior["run_dir"]), row)
            if not record or record["prompt"] != prompts[key]["text"]:
                raise ValueError("reused output is not valid for the frozen prompt")
            paths = runner.paths(Path(prior["run_dir"]), row)
            reuse.append({"prompt_key": key, "prompt_sha256": row["prompt_sha256"],
                          "record_path": str(paths["record"]), "record_sha256": sha(paths["record"]),
                          "job_path": str(paths["job"]), "job_sha256": sha(paths["job"]),
                          "job_id": record["job_id"], "image_path": str(paths["image"]),
                          "image_sha256": record["image_sha256"], "run_sha256": record["run_sha256"],
                          "origin_study_manifest_sha256": sha(OLD / "study_manifest.json")})
        url = prior["lineage_args"]["endpoint_base_url"]
        response = httpx.get(url + "/api/catalog", timeout=60)
        response.raise_for_status()
        settings = old_module.catalog_lineage(prior["pr"], url, response.json())
        if settings != prior["lineage_args"]:
            raise ValueError("live exact pipeline identity changed")
        binding = HERE / "selection" / (prior["name"] + ".json")
        write(binding, {"source_prompts_sha256": SOURCE_SHA, "row_ids": fresh,
                        "rows": [prompts[k] for k in fresh]}, exclusive=True)
        cell = {"name": prior["name"], "pr": prior["pr"], "writer": "v6_3",
                "run_dir": str(HERE / "runs" / prior["name"]), "prior_run_dir": prior["run_dir"],
                "twin_dir": str(Path(prior["run_dir"]) / "twins"),
                "selection_file": str(binding), "selection_sha256": sha(binding),
                "new_row_ids": fresh, "reused": reuse, "lineage_args": settings}
        run(cell, preflight=True)
        cell["run_manifest_sha256"] = sha(Path(cell["run_dir"]) / "run_manifest.json")
        cells.append(cell)
    if len(cells) != 2:
        raise ValueError("expected two exact V6.3 cells")
    write(HERE / "preserved_files.json", preserved, exclusive=True)
    manifest = {
        "version": "hp-v63-full160-two-exact-prs-v1", "frozen_at_utc": now(),
        "source": str(SOURCE), "source_sha256": SOURCE_SHA, "source_txt_sha256": sha(SOURCE.with_suffix(".txt")),
        "image_runner_path": str(RUNNER), "image_runner_sha256": sha(RUNNER),
        "orchestrator_sha256": sha(Path(__file__)), "preserved_files_sha256": sha(HERE / "preserved_files.json"),
        "universe": [{"prompt_key": p["prompt_key"], "device_id": p["device_id"],
                      "camera_tag": p["camera_tag"], "camera_id": p["source_camera_name"],
                      "rank": p["bank_rank"], "prompt_sha256": hashlib.sha256(p["text"].encode()).hexdigest(),
                      "prompt_record_sha256": runner.canonical_sha256(p)} for p in document["prompts"]],
        "authorized_new_submissions": 260, "new_per_pr": 130, "reused_per_pr": 30,
        "combined_per_pr": 160, "combined_total": 320, "workers_per_endpoint": 4,
        "contract": runner.EXPECTED_SCENE_CONTRACT,
        "image_settings": {"quality": "high", "output_format": "png", "background": "opaque"},
        "no_resampling": True, "no_new_text_calls": True, "no_judging": True,
        "text_evidence_limit": "15 successful r1 banks + one recognition false failure accepted under r2 unchanged; not fresh16/16r2 reliability.",
        "cells": cells,
    }
    write(HERE / "study_manifest.json", manifest, exclusive=True)
    write(HERE / "execution_commands.json", {"commands": [command(c) for c in cells],
                                            "resume": "generate requires explicit authorization; known jobs never re-POSTed"})
    print(json.dumps({"prepared": True, "reuse": 60, "new_authorized": 260}))


def verified_manifest():
    m = load(HERE / "study_manifest.json")
    for path, digest in ((SOURCE, SOURCE_SHA), (SOURCE.with_suffix(".txt"), m["source_txt_sha256"]),
                         (RUNNER, m["image_runner_sha256"]), (Path(__file__), m["orchestrator_sha256"]),
                         (HERE / "preserved_files.json", m["preserved_files_sha256"])):
        if sha(path) != digest:
            raise ValueError(f"frozen input changed: {path}")
    document = load(SOURCE)
    for c in m["cells"]:
        if sha(c["selection_file"]) != c["selection_sha256"]:
            raise ValueError("selected partition changed")
        if partition(document, [r["prompt_key"] for r in c["reused"]]) != c["new_row_ids"]:
            raise ValueError("partition changed")
        if sha(Path(c["run_dir"]) / "run_manifest.json") != c["run_manifest_sha256"]:
            raise ValueError("run identity changed")
        for r in c["reused"]:
            for field in ("record", "job", "image"):
                if sha(r[field + "_path"]) != r[field + "_sha256"]:
                    raise ValueError("reused evidence changed")
    return m


def submission_guard(cell):
    selected = set(cell["new_row_ids"])
    run_dir = Path(cell["run_dir"])
    journal = run_dir / "journals/events.jsonl"
    events = [json.loads(line) for line in journal.read_text().splitlines()] if journal.exists() else []
    starts = [e["row_id"] for e in events if e["event"] == "submit_started"]
    if len(starts) != len(set(starts)) or not set(starts) <= selected:
        raise ValueError("duplicate or unauthorized paid submission")
    runner = image_runner()
    for key in starts:
        row = {"row_slug": runner.slug(key)}
        if not runner.paths(run_dir, row)["job"].is_file():
            raise ValueError("ambiguous POST: preserve and investigate; never resubmit")
    for path in (run_dir / "jobs").glob("*.json"):
        if load(path)["row_id"] not in selected:
            raise ValueError("paid job outside authorized130 complement")


def counts(manifest=None):
    m = manifest or verified_manifest()
    runner = image_runner()
    prompts = {p["prompt_key"]: p for p in load(SOURCE)["prompts"]}
    result = {}
    for c in m["cells"]:
        n = {"expected": 160, "reused": 30, "new_expected": 130, "new_done": 0, "failed": 0, "pending": 0}
        for key in c["new_row_ids"]:
            row = row_for(prompts[key])
            record = runner.valid_completed_record(Path(c["run_dir"]), row)
            if record:
                n["new_done"] += 1
            elif runner.paths(Path(c["run_dir"]), row)["record"].is_file():
                n["failed"] += 1
            else:
                n["pending"] += 1
        n["done"] = n["reused"] + n["new_done"]
        result[c["name"]] = n
    return result


def generate(paid):
    if not paid:
        raise PermissionError("requires --paid-calls-authorized; maximum260 new submissions")
    lock = HERE / "generation.lock"
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.write(fd, str(os.getpid()).encode())
    os.close(fd)
    try:
        m = verified_manifest()
        for c in m["cells"]:
            submission_guard(c)
        write(HERE / "execution_status.json", {"status": "running", "pid": os.getpid(), "started_at_utc": now(),
                                              "cells": counts(m)})
        with ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(run, m["cells"]))
        for c in m["cells"]:
            submission_guard(c)
        write(HERE / "execution_status.json", {"status": "terminal", "finished_at_utc": now(), "cells": counts(m)})
        print(json.dumps(counts(m), indent=2))
    finally:
        lock.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "generate", "status"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "generate":
        generate(args.paid_calls_authorized)
    else:
        print(json.dumps(counts(), indent=2))
