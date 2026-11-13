#!/usr/bin/env python3
"""Thirty C-Tech-review-slot-matched V6.5 images on the unchanged PR4523 source."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import sys

import httpx

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
OLD = PROJECT / "eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109"
BASELINE = PROJECT / "eval_sets/hp_lifestyle_v6_4_pr4523_30_20261110"
TEXT_SNAPSHOT = PROJECT / (
    "eval_sets/hp_lifestyle_v6_5_training_four_devices_20261111/revisions/"
    "v6.5-astra-training-20261111-r4-revalidation"
)
TEXT = TEXT_SNAPSHOT / "exports/prompts_all_160.json"
RUNNER = PROJECT / "eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/run_generation.py"
ENDPOINT = HERE / "endpoint_pr4523"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "eval_sets/hp_lifestyle_v6_5_training_pr4523_30_20261111"
TITLE = "V6.5 / PR 4523 - V15.7 shapes"
COMMIT = "d1e5ae5323dedebc3b06ed173a3731307bd0623a"
FEEDBACK = PROJECT / "research/prompt_writer_v6_5/data/ctech_review/bound_feedback.json"


def load(path):
    return json.loads(Path(path).read_text())


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
        raise ValueError(f"required helper unavailable: {path}")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def s3_client():
    import foundry_aws_gateway

    client = foundry_aws_gateway.maybe_s3_client(BUCKET)
    if client is None:
        raise RuntimeError("Managed Foundry S3 authentication is unavailable for the HP study bucket")
    return client


def image_runner():
    return module("v65_native_image_runner", RUNNER)


def slot(prompt):
    return prompt["device_id"], prompt["camera_tag"], prompt["bank_rank"]


def endpoint_url():
    return load(HERE / "study_manifest.json")["endpoint_base_url"]


def select_matched(baseline, full, feedback):
    by_slot = {slot(prompt): prompt for prompt in full["prompts"]}
    if len(full["prompts"]) != 160 or len(by_slot) != 160:
        raise ValueError("expected160 unique V6.5 ranked slots")
    baseline_slots = [tuple(row["key"]) for row in baseline["rows"]]
    feedback_slots = [tuple(row["slot"]) for row in feedback["rows"]]
    if len(baseline_slots) != 30 or len(set(baseline_slots)) != 30 or baseline_slots != feedback_slots:
        raise ValueError("baseline and C-Tech review must cover the same ordered thirty slots")
    selected = []
    for row in baseline["rows"]:
        old = row["prompt"]
        new = by_slot[slot(old)]
        for field in ("device_id", "camera_tag", "source_camera_name", "render_lookup"):
            if new[field] != old[field]:
                raise ValueError(f"fixed product/camera changed: {slot(old)} / {field}")
        if hashlib.sha256(new["text"].encode()).hexdigest() != new["text_sha256"]:
            raise ValueError("new source prompt text hash is invalid")
        if row["output"]["status"] != "done" or row["output"]["lineage"]["source_commit"] != COMMIT:
            raise ValueError("baseline is not a complete native PR4523 result")
        selected.append(copy.deepcopy(new))
    return selected


def prepare():
    if (HERE / "study_manifest.json").exists():
        raise FileExistsError("image study already frozen; do not refreeze")
    completion = load(TEXT_SNAPSHOT / "exports/completion_audit.json")
    if not completion["passed"] or completion["export_sha256"] != sha(TEXT):
        raise ValueError("all160 recovered text/score/input bindings must pass before images")
    if (
        completion["original_native_successful_banks"] != 0
        or completion["original_native_failed_banks"] != 16
        or completion["accepted_unchanged_banks"] + completion["additional_semantic_calls"] != 16
        or completion["explicit_additional_repair_authorization"]
        != "Fix recognition; allow one extra repair per genuinely invalid bank"
    ):
        raise ValueError("explicit native-versus-recovery provenance is required")
    client = s3_client()
    live = {}
    source_files = {
        "data/generation.json": BASELINE / "public/data/generation.json",
        "fe/data_source_prompts_20261110.json": (
            BASELINE / "fe_source_prompts_20261110/data_source_prompts_20261110.json"
        ),
        "gallery/index.html": BASELINE / "public/gallery/index.html",
    }
    annotations = load(FEEDBACK.parent / "annotation_source_receipt.json")["objects"]
    listed = {
        item["Key"]
        for page in client.get_paginator("list_objects_v2").paginate(
            Bucket=BUCKET, Prefix=f"eval_sets/{BASELINE.name}/fe/annotations/",
        )
        for item in page.get("Contents", []) if item["Key"].endswith(".json")
    }
    if listed != {item["key"] for item in annotations}:
        raise ValueError("published C-Tech annotation set changed since Astra reviewed it")
    for item in annotations:
        response = client.get_object(Bucket=BUCKET, Key=item["key"])
        if hashlib.sha256(response["Body"].read()).hexdigest() != item["sha256"]:
            raise ValueError("published C-Tech comments changed since Astra reviewed them")
        live[item["key"]] = {
            "key": item["key"], "sha256": item["sha256"], "etag": response["ETag"],
            "version_id": response.get("VersionId"),
        }
    for relative, local_source in source_files.items():
        key = "eval_sets/" + BASELINE.name + "/" + relative
        response = client.get_object(Bucket=BUCKET, Key=key)
        body = response["Body"].read()
        if hashlib.sha256(body).hexdigest() != sha(local_source):
            raise ValueError(f"baseline live data differs from preserved local evidence: {relative}")
        write(HERE / "baseline_live" / relative, body)
        live[relative] = {"key": key, "sha256": hashlib.sha256(body).hexdigest(),
                          "etag": response["ETag"], "version_id": response.get("VersionId")}
    full = load(TEXT)
    baseline = load(HERE / "baseline_live/data/generation.json")
    feedback = load(FEEDBACK)
    selected = select_matched(baseline, full, feedback)
    write(HERE / "selection/selected_v6_5_30.json", {
        "version": "hp-v6.5-pr4523-review-slot-matched30-v1",
        "source_prompts_path": str(TEXT), "source_prompts_sha256": sha(TEXT),
        "matching_is_not_semantic_equivalence": True,
        "selection_rule": "the exact thirty device/camera/bank-rank slots reviewed by C-Tech",
        "counts": {"prompts": 30, "banks": 16},
        "device_source_mapping": full["device_source_mapping"], "prompts": selected,
    })
    write(HERE / "selection/selected_v6_5_30.txt", "\n\n".join(
        f"[{row['prompt_key']} | {row['device_display_name']} | {row['camera_tag']} | rank {row['bank_rank']}]\n{row['text']}"
        for row in selected) + "\n")
    adapted = copy.deepcopy(full)
    for bank in adapted["bank_audit"].values():
        original = TEXT_SNAPSHOT / bank["case_metadata"]["frozen_input_path"]
        if load(original) != bank["source_input"] or sha(original) != bank["source_input_sha256"]:
            raise ValueError("native source input binding changed")
        bank["source_input_path"] = str(original)
    adapted["image_runner_adapter"] = {
        "original_export_path": str(TEXT), "original_export_sha256": sha(TEXT),
        "change": "metadata-only exact bank-input path binding; all160 prompt records unchanged",
    }
    write(HERE / "source/prompts_for_runner_160.json", adapted)
    write(HERE / "selection/runner_selection.json", {
        "source_prompts_sha256": sha(HERE / "source/prompts_for_runner_160.json"),
        "row_ids": [row["prompt_key"] for row in selected], "rows": selected,
    })
    native = OLD / "endpoint_pr4523"
    source_manifest = load(native / "source_manifest.json")
    deployment = load(native / "deployment_manifest.json")
    files = [
        *[{"path": "runtime/" + record["path"], "sha256": record["sha256"]}
          for record in source_manifest["source_files"]],
        *source_manifest["restored_assets"], *source_manifest["fixed_inputs"],
        *deployment["wrapper_files"],
        *[{"path": name, "sha256": sha(native / name)}
          for name in ("source_manifest.json", "deployment_manifest.json")],
    ]
    for record in files:
        path = native / record["path"]
        if sha(path) != record["sha256"]:
            raise ValueError(f"unchanged native endpoint bytes differ: {path}")
        write(ENDPOINT / record["path"], path.read_bytes())
    with socket.socket() as candidate:
        candidate.bind(("127.0.0.1", 0))
        port = candidate.getsockname()[1]
    frozen = [Path(__file__), TEXT, RUNNER, FEEDBACK, TEXT_SNAPSHOT / "exports/completion_audit.json",
              *[ENDPOINT / record["path"] for record in files],
              *[path for folder in ("selection", "source", "baseline_live")
                for path in (HERE / folder).rglob("*") if path.is_file()]]
    write(HERE / "study_manifest.json", {
        "version": "hp-v6.5-pr4523-review-slot-matched30-study-v1",
        "prepared_at_utc": now(), "title": TITLE,
        "source_export_path": str(TEXT), "source_export_sha256": sha(TEXT),
        "authorized_image_rows": 30, "runner_full_queue_count": 160,
        "authorized_row_ids": [row["prompt_key"] for row in selected],
        "source_commit": COMMIT, "endpoint_base_url": f"http://127.0.0.1:{port}",
        "baseline_live_objects": live, "normal_reference_selection": True,
        "failure_policy": "no replacements or semantic image resampling without further authorization",
        "new_writer_calls": 0, "judge_calls": 0,
        "frozen_files": {str(path): sha(path) for path in frozen},
    })
    probe = json.dumps({"study": PREFIX, "purpose": "authorized thirty-image publication preflight",
                        "manifest_sha256": sha(HERE / "study_manifest.json")}).encode()
    key = PREFIX + "/preflight/s3_access_probe.json"
    client.put_object(Bucket=BUCKET, Key=key, Body=probe, ContentType="application/json", IfNoneMatch="*")
    if client.get_object(Bucket=BUCKET, Key=key)["Body"].read() != probe:
        raise ValueError("current new-prefix S3 write/read failed")
    write(HERE / "s3_preflight.json", {"passed": True, "verified_at_utc": now(), "key": key})
    print(json.dumps({"selected": 30, "native_endpoint_files": len(files), "port": port}), flush=True)


def verify():
    manifest = load(HERE / "study_manifest.json")
    for path, digest in manifest["frozen_files"].items():
        if sha(path) != digest:
            raise ValueError(f"frozen image-study bytes changed: {path}")
    return manifest


def runner_command(preflight=False, row_ids=None):
    verify()
    base_url = endpoint_url()
    prior = module("v65_original_lineage_helpers", OLD / "study.py")
    response = httpx.get(base_url + "/api/catalog", timeout=60)
    response.raise_for_status()
    lineage = prior.catalog_lineage("pr4523", base_url, response.json())
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
    result = {"expected": 30, "done": 0, "failed": 0, "pending": 0}
    for row in rows:
        if row["row_id"] not in manifest["authorized_row_ids"]:
            continue
        if runner.valid_completed_record(HERE / "run", row) is not None:
            result["done"] += 1
        elif runner.paths(HERE / "run", row)["record"].exists():
            result["failed"] += 1
        else:
            result["pending"] += 1
    return result


def preflight():
    verify()
    if not load(HERE / "s3_preflight.json")["passed"]:
        raise ValueError("publication access preflight not passed")
    response = httpx.get(endpoint_url() + "/health", timeout=60)
    response.raise_for_status()
    health = response.json()
    if not health["generationEnabled"]:
        raise ValueError("owned endpoint generation is disabled")
    subprocess.run(runner_command(preflight=True), check=True)
    write(HERE / "endpoint_preflight.json", {
        "verified_at_utc": now(), "health": health,
        "catalog": httpx.get(endpoint_url() + "/api/catalog", timeout=60).json(),
        "model_calls": 0,
    })


def generate(smoke, authorized):
    manifest = verify()
    if not authorized:
        raise PermissionError("images require --paid-calls-authorized")
    gate = load(HERE / "endpoint_preflight.json")
    health = httpx.get(endpoint_url() + "/health", timeout=60)
    health.raise_for_status()
    if health.json()["instanceId"] != gate["health"]["instanceId"]:
        raise ValueError("owned endpoint instance changed")
    selected = load(HERE / "selection/selected_v6_5_30.json")["prompts"]
    if smoke:
        if counts() != {"expected": 30, "done": 0, "failed": 0, "pending": 30}:
            raise ValueError("included smoke is not a clean new launch")
        chosen = [next(row for row in selected if row["device_type"] == kind)
                  for kind in ("laptop", "printer")]
        row_ids = [row["prompt_key"] for row in chosen]
    else:
        load(HERE / "smoke_review.json")
        if counts()["failed"]:
            raise ValueError("terminal image failures need inspection and separate replacement authorization")
        runner = image_runner()
        done = {row["prompt_key"] for row in selected if runner.valid_completed_record(
            HERE / "run", {"row_id": row["prompt_key"], "row_slug": runner.slug(row["prompt_key"]),
                           "prompt_sha256": row["text_sha256"]}) is not None}
        row_ids = [row_id for row_id in manifest["authorized_row_ids"] if row_id not in done]
    if not row_ids:
        raise ValueError("no new authorized image rows")
    command = runner_command(row_ids=row_ids)
    write(HERE / ("smoke_launch.json" if smoke else "remaining_launch.json"), {
        "recorded_before_process_start": True, "at_utc": now(), "rows": row_ids,
        "command": command, "study_manifest_sha256": sha(HERE / "study_manifest.json"),
    })
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
