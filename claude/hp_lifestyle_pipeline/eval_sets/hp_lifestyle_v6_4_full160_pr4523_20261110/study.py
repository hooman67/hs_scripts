"""Extend V6.4 to160 outputs: preserve30 and submit exactly130 new scene prompts."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import httpx

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
PRIOR = HERE.parent / "hp_lifestyle_v6_4_pr4523_30_20261110"
COMPARISON = HERE.parent / "hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110"
SMALL = HERE.parent / "hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109"
ENDPOINT = HERE / "endpoint_pr4523"
SOURCE = HERE / "source/prompts_for_runner_160.json"
PREFIX = "eval_sets/" + HERE.name
BUCKET = "foundry-hp-enterprise-adobe-assets"
BASE_URL = "http://127.0.0.1:8140"
TITLE = "V6.4 / PR 4523 - V15.7 shapes"
COMMIT = "d1e5ae5323dedebc3b06ed173a3731307bd0623a"
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


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = value if isinstance(value, bytes) else (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(body)


def s3_client():
    return module("v64_full160_approved_s3", COMPARISON / "s3_access.py").s3_client()


def image_runner():
    return module("v64_full160_image_runner", RUNNER)


def row_for(prompt):
    return {"row_id": prompt["prompt_key"], "row_slug": image_runner().slug(prompt["prompt_key"]),
            "prompt_sha256": prompt["text_sha256"]}


def partition(prompts, reused):
    keys = [p["prompt_key"] for p in prompts]
    if len(keys) != len(set(keys)) or len(keys) != 160 or len(reused) != len(set(reused)) or len(reused) != 30:
        raise ValueError("expected160 unique source prompts and30 unique reused outputs")
    if not set(reused) <= set(keys):
        raise ValueError("reuse keys escape the accepted V6.4 source")
    return [key for key in keys if key not in set(reused)]


def prepare():
    prior = module("v64_full160_prior_study", PRIOR / "study.py")
    original = prior.verify()
    if prior.counts() != {"expected": 30, "done": 30, "failed": 0, "pending": 0}:
        raise ValueError("all thirty prior outputs must be valid before reuse")
    write(SOURCE, (PRIOR / "source/prompts_for_runner_160.json").read_bytes())
    document = load(SOURCE)
    accepted = load(prior.TEXT)
    if document["prompts"] != accepted["prompts"]:
        raise ValueError("runner adapter altered an accepted V6.4 prompt")
    runner = image_runner()
    runner.validate_prompt_document(document, SOURCE, sha(SOURCE))
    reused = []
    for prompt in load(PRIOR / "selection/selected_v6_4_30.json")["prompts"]:
        row = row_for(prompt)
        record = runner.valid_completed_record(PRIOR / "run", row)
        paths = runner.paths(PRIOR / "run", row)
        if record is None or record["lineage"]["source_commit"] != COMMIT:
            raise ValueError("reused output is invalid or from another pipeline")
        audit = PRIOR / "input_audit" / (row["row_slug"] + ".json")
        reused.append({"prompt_key": prompt["prompt_key"], "job_id": record["job_id"],
                       "record_path": str(paths["record"]), "image_path": str(paths["image"]),
                       "job_path": str(paths["job"]), "status_path": str(paths["status"]),
                       "audit_path": str(audit), "image_sha256": record["image_sha256"]})
    fresh = partition(document["prompts"], [r["prompt_key"] for r in reused])
    write(HERE / "selection/remaining130.json", {"source_prompts_sha256": sha(SOURCE),
        "row_ids": fresh, "rows": [p for p in document["prompts"] if p["prompt_key"] in set(fresh)]})
    copied = []
    for path, expected in original["frozen_files"].items():
        path = Path(path)
        if path.is_relative_to(prior.ENDPOINT):
            relative = path.relative_to(prior.ENDPOINT)
            if sha(path) != expected:
                raise ValueError("pinned endpoint source changed")
            write(ENDPOINT / relative, path.read_bytes())
            copied.append(ENDPOINT / relative)
    if len(copied) != 70:
        raise ValueError("the isolated pipeline must contain the same70 frozen files")
    s3 = s3_client()
    live = {}
    comparison_files = ("gallery/index.html", "gallery/main.js", "gallery/style.css", "gallery/imsauth.js",
                        "data/comparison.json", "asset_manifest.json", "fe/viewer.html", "fe/data.json")
    small_files = ("gallery/index.html", "gallery/main.v6_4_20261110.js",
                   "data/comparison_v6_4_20261110.json")
    for label, root, names in (("full160", COMPARISON, comparison_files), ("small30", SMALL, small_files)):
        for name in names:
            key = "eval_sets/" + root.name + "/" + name
            response = s3.get_object(Bucket=BUCKET, Key=key)
            body = response["Body"].read()
            write(HERE / "baseline_live" / label / name, body)
            live[label + "/" + name] = {"key": key, "sha256": hashlib.sha256(body).hexdigest(),
                "etag": response["ETag"], "version_id": response.get("VersionId"),
                "content_type": response["ContentType"], "metadata": response.get("Metadata", {})}
    old = load(HERE / "baseline_live/full160/data/comparison.json")
    if len(old["rows"]) != 160 or any(len(row["outputs"]) != 2 for row in old["rows"]):
        raise ValueError("the live full160 comparison must have exactly two original columns")
    slots = lambda p: (p["device_id"], p["camera_tag"], p["bank_rank"])
    if {tuple(row["key"]) for row in old["rows"]} != {slots(p) for p in document["prompts"]}:
        raise ValueError("full160 comparison and V6.4 source slots do not match")
    preserved = [PRIOR / "study_manifest.json", PRIOR / "completion_receipt.json",
                 PRIOR / "selection/selected_v6_4_30.json", prior.TEXT, RUNNER, Path(__file__), SOURCE,
                 HERE / "selection/remaining130.json", *copied]
    for record in reused:
        for name in ("record_path", "image_path", "job_path", "status_path", "audit_path"):
            preserved.append(Path(record[name]))
    manifest = {"version": "hp-v6.4-full160-pr4523-v1", "frozen_at_utc": now(),
        "title": TITLE, "source_export": str(prior.TEXT), "source_export_sha256": sha(prior.TEXT),
        "runner_source_sha256": sha(SOURCE), "source_commit": COMMIT, "endpoint_base_url": BASE_URL,
        "reused": reused, "new_row_ids": fresh, "authorized_primary_submissions": 130,
        "authorized_replacements": "one per confirmed transient failure; preserve originals; never ambiguous POSTs",
        "new_text_calls": 0, "new_judge_calls": 0, "workers": 4,
        "targets": "add third column to BOTH full160 FE and detailed reports; preserve small30 comparison",
        "baseline_live_objects": live, "frozen_files": {str(path): sha(path) for path in preserved}}
    write(HERE / "study_manifest.json", manifest)
    probe = json.dumps({"study": PREFIX, "manifest_sha256": sha(HERE / "study_manifest.json")}).encode()
    key = PREFIX + "/preflight/s3_access_probe.json"
    s3.put_object(Bucket=BUCKET, Key=key, Body=probe, ContentType="application/json", IfNoneMatch="*")
    if s3.get_object(Bucket=BUCKET, Key=key)["Body"].read() != probe:
        raise ValueError("new-prefix S3 write/read preflight failed")
    write(HERE / "s3_preflight.json", {"passed": True, "at_utc": now(), "key": key})
    print(json.dumps({"reused": 30, "new_authorized": len(fresh), "endpoint_files": len(copied),
                      "full160_rows_match": True, "s3_write_read": "passed"}))


def verify():
    manifest = load(HERE / "study_manifest.json")
    for path, expected in manifest["frozen_files"].items():
        if sha(path) != expected:
            raise ValueError("frozen source/reuse/pipeline changed: " + path)
    return manifest


def runner_command(preflight=False):
    response = httpx.get(BASE_URL + "/api/catalog", timeout=60)
    response.raise_for_status()
    prior = module("v64_full160_lineage", SMALL / "study.py")
    lineage = prior.catalog_lineage("pr4523", BASE_URL, response.json())
    command = [sys.executable, str(RUNNER), "--prompts", str(SOURCE), "--prompts-sha256", sha(SOURCE),
               "--run-dir", str(HERE / "run"), "--prefix", PREFIX + "/run", "--workers", "4",
               "--no-publish", "--selection-file", str(HERE / "selection/remaining130.json")]
    for key, value in lineage.items():
        if value is not None:
            command.extend(["--" + key.replace("_", "-"), value])
    if preflight:
        command.append("--preflight-only")
    return command


def preflight():
    verify()
    response = httpx.get(BASE_URL + "/health", timeout=60)
    response.raise_for_status()
    if not load(HERE / "s3_preflight.json")["passed"]:
        raise ValueError("S3 preflight missing")
    subprocess.run(runner_command(preflight=True), check=True)
    write(HERE / "endpoint_preflight.json", {"at_utc": now(), "health": response.json(),
        "run_manifest_sha256": sha(HERE / "run/run_manifest.json"), "model_calls": 0})


def counts():
    manifest = verify()
    runner = image_runner()
    prompts = {p["prompt_key"]: p for p in load(SOURCE)["prompts"]}
    result = {"expected": 160, "reused": 30, "new_expected": 130, "new_done": 0, "failed": 0, "pending": 0}
    for key in manifest["new_row_ids"]:
        row = row_for(prompts[key])
        if runner.valid_completed_record(HERE / "run", row):
            result["new_done"] += 1
        elif runner.paths(HERE / "run", row)["record"].exists():
            result["failed"] += 1
        else:
            result["pending"] += 1
    result["done"] = 30 + result["new_done"]
    return result


def generate(authorized):
    manifest = verify()
    if not authorized:
        raise PermissionError("paid calls require explicit authorization")
    preflight = load(HERE / "endpoint_preflight.json")
    if sha(HERE / "run/run_manifest.json") != preflight["run_manifest_sha256"]:
        raise ValueError("runner identity changed after preflight")
    write(HERE / "generation_launch.json", {"at_utc": now(), "row_ids": manifest["new_row_ids"],
        "recorded_before_process_start": True, "study_manifest_sha256": sha(HERE / "study_manifest.json"),
        "command": runner_command()})
    log = HERE / "generation_execution.log"
    with log.open("x") as stream:
        subprocess.run(runner_command(), stdout=stream, stderr=subprocess.STDOUT, check=True,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    result = counts()
    write(HERE / "generation_terminal.json", {"at_utc": now(), "counts": result})
    if result["done"] != 160 or result["failed"] or result["pending"]:
        raise RuntimeError("inspect terminal failures before any authorized transient replacement")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "preflight", "generate", "counts", "verify"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    args = parser.parse_args()
    if args.command == "generate":
        generate(args.paid_calls_authorized)
    else:
        value = {"prepare": prepare, "preflight": preflight, "counts": counts, "verify": verify}[args.command]()
        if args.command == "counts":
            print(json.dumps(value))
