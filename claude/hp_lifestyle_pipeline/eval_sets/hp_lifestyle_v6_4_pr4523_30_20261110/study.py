#!/usr/bin/env python3
"""Thirty rank-matched V6.4 images on the frozen, unmodified PR4523 pipeline."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import httpx

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
OLD = PROJECT / "eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109"
TEXT = PROJECT / (
    "eval_sets/hp_lifestyle_v6_4_four_devices_20261110/revisions/"
    "v6.4-structured-sources-20261110-r1/exports/prompts_all_160.json"
)
RUNNER = PROJECT / "eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/run_generation.py"
ENDPOINT = HERE / "endpoint_pr4523"
BASE_URL = "http://127.0.0.1:8139"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_v6_4_pr4523_30_20261110"
TITLE = "V6.4 / PR 4523 - V15.7 shapes"
ORIGINAL_PREFIX = "eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109"
BASELINE_OBJECTS = ("gallery/index.html", "gallery/main.js", "data/comparison.json",
                    "data/selected_v6_3_30.json")
COMMIT = "d1e5ae5323dedebc3b06ed173a3731307bd0623a"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, bytes):
        with path.open("xb") as stream:
            stream.write(value)
    else:
        with path.open("x", encoding="utf-8") as stream:
            if isinstance(value, str):
                stream.write(value)
            else:
                json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
                stream.write("\n")


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"unavailable helper: {path}")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def s3_client():
    return module("v64_approved_s3_access", OLD.parent /
                  "hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/s3_access.py").s3_client()


def image_runner():
    return module("v64_native_image_runner", RUNNER)


def slot(prompt):
    return prompt["device_id"], prompt["camera_tag"], prompt["bank_rank"]


def select_matched(old_rows, full):
    by_slot = {slot(row): row for row in full["prompts"]}
    if len(full["prompts"]) != 160 or len(by_slot) != 160:
        raise ValueError("expected160 unique V6.4 source slots")
    keys = [slot(row) for row in old_rows]
    if len(keys) != 30 or len(set(keys)) != 30:
        raise ValueError("expected thirty unique V6.3 comparison slots")
    selected = []
    for old in old_rows:
        if slot(old) not in by_slot:
            raise ValueError(f"missing V6.4 slot: {slot(old)}")
        new = by_slot[slot(old)]
        for field in ("device_id", "camera_tag", "source_camera_name", "render_lookup"):
            if old[field] != new[field]:
                raise ValueError(f"product/camera binding differs: {slot(old)} / {field}")
        if hashlib.sha256(new["text"].encode()).hexdigest() != new["text_sha256"]:
            raise ValueError("selected V6.4 text hash is invalid")
        selected.append(copy.deepcopy(new))
    return selected


def prepare():
    if (HERE / "study_manifest.json").exists():
        raise FileExistsError("study already frozen; do not overwrite or refreeze")
    client = s3_client()
    live = {}
    for relative in BASELINE_OBJECTS:
        response = client.get_object(Bucket=BUCKET, Key=ORIGINAL_PREFIX + "/" + relative)
        body = response["Body"].read()
        if hashlib.sha256(body).hexdigest() != sha(OLD / "public" / relative):
            raise ValueError(f"live baseline differs from local evidence: {relative}")
        write(HERE / "baseline_live" / relative, body)
        live[relative] = {
            "key": ORIGINAL_PREFIX + "/" + relative, "sha256": hashlib.sha256(body).hexdigest(),
            "etag": response["ETag"], "version_id": response.get("VersionId"),
        }
    comparison = load(HERE / "baseline_live/data/comparison.json")
    baseline = load(HERE / "baseline_live/data/selected_v6_3_30.json")
    if comparison["status"] != "complete" or len(comparison["rows"]) != 30:
        raise ValueError("original comparison must be complete with thirty rows")
    old_rows = [row["prompts"]["v6_3"] for row in comparison["rows"]]
    if {r["prompt_key"]: r for r in old_rows} != {
            r["prompt_key"]: r for r in baseline["prompts"]}:
        raise ValueError("live gallery rows do not match its selected V6.3 export")
    if any(row["outputs"]["v6_3_pr4523"]["status"] != "done"
           or row["outputs"]["v6_3_pr4523"]["lineage"]["source_commit"] != COMMIT
           for row in comparison["rows"]):
        raise ValueError("original V6.3 images do not bind the exact PR4523 commit")
    full = load(TEXT)
    completion = load(PROJECT / "research/prompt_writer_v6_4/data/completion_audit.json")
    if not completion["passed"] or sha(TEXT) != completion["export_file_sha256"]["prompts_all_160.json"]:
        raise ValueError("V6.4 export differs from its completed actual-response audit")
    selected = select_matched(old_rows, full)
    bindings = [{"slot": list(slot(old)), "v63_prompt_key": old["prompt_key"],
                 "v64_prompt_key": new["prompt_key"], "v63_text_sha256": old["text_sha256"],
                 "v64_text_sha256": new["text_sha256"],
                 "v63_environment": old["environment"], "v64_environment": new["environment"]}
                for old, new in zip(old_rows, selected)]
    selected_document = {
        "version": "hp-v6.4-pr4523-rank-matched30-v1",
        "source_prompts_path": str(TEXT), "source_prompts_sha256": sha(TEXT),
        "selection_rule": "same device_id/camera_tag/bank_rank as the original V6.3 thirty",
        "matching_is_not_semantic_equivalence": True,
        "counts": {"prompts": 30, "banks": 16}, "bindings": bindings,
        "device_source_mapping": full["device_source_mapping"], "prompts": selected,
    }
    write(HERE / "selection/selected_v6_4_30.json", selected_document)
    write(HERE / "selection/selected_v6_4_30.txt", "\n\n".join(
        f"[{r['prompt_key']} | {r['device_display_name']} | {r['camera_tag']} | rank {r['bank_rank']}]\n{r['text']}"
        for r in selected) + "\n")
    adapted = copy.deepcopy(full)
    text_snapshot = Path(full["snapshot_manifest_path"]).parent
    for bank in adapted["bank_audit"].values():
        source = text_snapshot / bank["case_metadata"]["frozen_input_path"]
        if load(source) != bank["source_input"]:
            raise ValueError("actual frozen source document mismatch")
        bank["source_input_path"], bank["source_input_sha256"] = str(source), sha(source)
    adapted["image_runner_adapter"] = {
        "original_export_path": str(TEXT), "original_export_sha256": sha(TEXT),
        "change": "external bank-input path/hash metadata only; all160 prompt records unchanged",
    }
    write(HERE / "source/prompts_for_runner_160.json", adapted)
    write(HERE / "selection/runner_selection.json", {
        "source_prompts_sha256": sha(HERE / "source/prompts_for_runner_160.json"),
        "row_ids": [r["prompt_key"] for r in selected], "rows": selected,
    })
    source_manifest = load(OLD / "endpoint_pr4523/source_manifest.json")
    deployment = load(OLD / "endpoint_pr4523/deployment_manifest.json")
    files = [
        *[{"path": "runtime/" + r["path"], "sha256": r["sha256"]}
          for r in source_manifest["source_files"]],
        *source_manifest["restored_assets"], *source_manifest["fixed_inputs"],
        *deployment["wrapper_files"],
        *[{"path": name, "sha256": sha(OLD / "endpoint_pr4523" / name)}
          for name in ("source_manifest.json", "deployment_manifest.json")],
    ]
    for record in files:
        relative = record["path"]
        source = OLD / "endpoint_pr4523" / relative
        if sha(source) != record["sha256"]:
            raise ValueError(f"pinned endpoint file changed: {relative}")
        write(ENDPOINT / relative, source.read_bytes())
    frozen_paths = [
        HERE / "study.py", TEXT, RUNNER,
        *[ENDPOINT / r["path"] for r in files],
        *[p for d in ("selection", "source", "baseline_live")
          for p in (HERE / d).rglob("*") if p.is_file()],
    ]
    manifest = {
        "version": "hp-v6.4-pr4523-rank-matched30-study-v1", "prepared_at_utc": now(),
        "title": TITLE, "source_export_path": str(TEXT), "source_export_sha256": sha(TEXT),
        "authorized_image_rows": 30, "runner_full_queue_count": 160,
        "authorized_row_ids": [r["prompt_key"] for r in selected],
        "source_commit": COMMIT, "endpoint_base_url": BASE_URL,
        "baseline_live_objects": live, "normal_reference_selection": True,
        "failure_policy": "at most one replacement per confirmed transient failure; preserve originals",
        "new_writer_calls": 0, "judge_calls": 0,
        "frozen_files": {str(p): sha(p) for p in frozen_paths},
    }
    write(HERE / "study_manifest.json", manifest)
    probe = json.dumps({"study": PREFIX, "purpose": "authorized new-prefix write/read preflight",
                        "study_manifest_sha256": sha(HERE / "study_manifest.json")}).encode()
    key = PREFIX + "/preflight/s3_access_probe.json"
    client.put_object(Bucket=BUCKET, Key=key, Body=probe, ContentType="application/json",
                      IfNoneMatch="*")
    if client.get_object(Bucket=BUCKET, Key=key)["Body"].read() != probe:
        raise ValueError("new-prefix S3 write/read verification failed")
    write(HERE / "s3_preflight.json", {"verified_at_utc": now(), "key": key,
                                      "sha256": hashlib.sha256(probe).hexdigest(), "passed": True})
    print(json.dumps({"selected": 30, "endpoint_files_copied": len(files), "s3_write_read": "passed"}))


def verify():
    manifest = load(HERE / "study_manifest.json")
    for path, digest in manifest["frozen_files"].items():
        if sha(path) != digest:
            raise ValueError(f"frozen study/input/source changed: {path}")
    return manifest


def runner_command(*, preflight=False, row_ids=None):
    prior = module("v64_prior_lineage_helpers", OLD / "study.py")
    response = httpx.get(BASE_URL + "/api/catalog", timeout=60)
    response.raise_for_status()
    lineage = prior.catalog_lineage("pr4523", BASE_URL, response.json())
    command = [
        sys.executable, str(RUNNER), "--prompts", str(HERE / "source/prompts_for_runner_160.json"),
        "--prompts-sha256", sha(HERE / "source/prompts_for_runner_160.json"),
        "--run-dir", str(HERE / "run"), "--prefix", PREFIX + "/run",
        "--workers", "4", "--no-publish",
    ]
    for key, value in lineage.items():
        if value is not None:
            command.extend(["--" + key.replace("_", "-"), value])
    command.extend(["--row-ids", *row_ids] if row_ids is not None else
                   ["--selection-file", str(HERE / "selection/runner_selection.json")])
    if preflight:
        command.append("--preflight-only")
    return command


def counts():
    manifest = verify()
    runner = image_runner()
    rows = runner.validate_prompt_document(load(HERE / "source/prompts_for_runner_160.json"),
                                          HERE / "source/prompts_for_runner_160.json",
                                          sha(HERE / "source/prompts_for_runner_160.json"))
    selected = set(manifest["authorized_row_ids"])
    result = {"expected": 30, "done": 0, "failed": 0, "pending": 0}
    for row in rows:
        if row["row_id"] not in selected:
            continue
        if runner.valid_completed_record(HERE / "run", row):
            result["done"] += 1
        elif runner.paths(HERE / "run", row)["record"].exists():
            result["failed"] += 1
        else:
            result["pending"] += 1
    return result


def preflight():
    verify()
    if not load(HERE / "s3_preflight.json")["passed"]:
        raise ValueError("publication access gate not passed")
    response = httpx.get(BASE_URL + "/health", timeout=60)
    response.raise_for_status()
    health = response.json()
    subprocess.run(runner_command(preflight=True), check=True)
    write(HERE / "endpoint_preflight.json", {"verified_at_utc": now(), "health": health,
                                            "catalog": httpx.get(BASE_URL + "/api/catalog", timeout=60).json(),
                                            "model_calls": 0})


def generate(smoke, authorized):
    manifest = verify()
    if not authorized:
        raise PermissionError("generation requires --paid-calls-authorized")
    load(HERE / "endpoint_preflight.json")
    selected = load(HERE / "selection/selected_v6_4_30.json")["prompts"]
    if smoke:
        chosen = [next(p for p in selected if p["device_type"] == kind)
                  for kind in ("laptop", "printer")]
        row_ids = [p["prompt_key"] for p in chosen]
    else:
        if not (HERE / "smoke_review.json").exists():
            raise ValueError("review the two included smoke outputs before continuation")
        runner = image_runner()
        done = {p["prompt_key"] for p in selected if runner.valid_completed_record(
            HERE / "run", {"row_id": p["prompt_key"], "row_slug": runner.slug(p["prompt_key"]),
                           "prompt_sha256": p["text_sha256"]})}
        row_ids = [key for key in manifest["authorized_row_ids"] if key not in done]
        if counts()["failed"]:
            raise ValueError("inspect terminal failures before any continuation/replacement")
    journal = HERE / ("smoke_launch.json" if smoke else "remaining_launch.json")
    command = runner_command(row_ids=row_ids)
    write(journal, {"recorded_before_process_start": True, "at_utc": now(), "rows": row_ids,
                    "command": command, "study_manifest_sha256": sha(HERE / "study_manifest.json")})
    subprocess.run(command, check=True)
    write(HERE / ("smoke_complete.json" if smoke else "generation_complete.json"),
          {"completed_at_utc": now(), "counts": counts()})
    print(json.dumps(counts()), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "verify", "preflight", "smoke", "generate", "counts"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "verify":
        print(json.dumps({"frozen_files": len(verify()["frozen_files"])}))
    elif args.command == "preflight":
        preflight()
    elif args.command == "counts":
        print(json.dumps(counts()))
    else:
        generate(args.command == "smoke", args.paid_calls_authorized)
