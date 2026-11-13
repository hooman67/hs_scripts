"""Render only accepted Astra prompts through the untouched, isolated PR4523."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import httpx

import scene_runner
import text_study

HERE = text_study.ROOT
ENDPOINT = HERE / "endpoint_pr4523"
RUN = HERE / "run"
COMMIT = "d1e5ae5323dedebc3b06ed173a3731307bd0623a"
BASE_URL = "http://127.0.0.1:8152"
PRIOR = text_study.PRIOR
SOURCE = HERE / "text/exports/prompts_all.json"
BUCKET = text_study.BUCKET
PREFIX = text_study.PREFIX
sha, load, write = text_study.sha, text_study.load, text_study.write


def image_runner() -> Any:
    return scene_runner


def owns_listener(pid: int) -> bool:
    sockets = set()
    for descriptor in Path(f"/proc/{pid}/fd").iterdir():
        try:
            target = os.readlink(descriptor)
        except FileNotFoundError:
            continue
        if target.startswith("socket:["):
            sockets.add(target[8:-1])
    for line in Path("/proc/net/tcp").read_text().splitlines()[1:]:
        fields = line.split()
        if fields[1] == f"0100007F:{8152:04X}" and fields[3] == "0A":
            return fields[9] in sockets
    return False


def row_for(prompt: dict[str, Any]) -> dict[str, Any]:
    return {
        "row_id": prompt["prompt_key"],
        "row_slug": scene_runner.slug(prompt["prompt_key"]),
        "prompt": prompt,
        "device_id": prompt["device_id"],
        "digital_twin_id": scene_runner.DEVICE_MAP[prompt["device_id"]],
        "camera_id": prompt["source_camera_name"],
        "bank_id": prompt["bank_debug_ref"],
        "rank": prompt["bank_rank"],
        "prompt_sha256": prompt["text_sha256"],
        "prompt_record_sha256": scene_runner.canonical_sha256(prompt),
    }


def rows() -> list[dict[str, Any]]:
    document = load(SOURCE)
    cases = {case["bank_id"]: case for case in load(HERE / "banks.json")["cases"]}
    accepted = {bank for bank, data in document["bank_audit"].items() if data["result"]["status"] == "ok"}
    expected = {bank + f"::p{rank}" for bank in accepted for rank in range(1, 11)}
    prompts = {prompt["prompt_key"]: prompt for prompt in document["prompts"]}
    if set(prompts) != expected or len(prompts) != len(document["prompts"]):
        raise ValueError("Accepted prompts must be complete ten-prompt banks without duplicates")
    for prompt in prompts.values():
        case = cases[prompt["bank_debug_ref"]]
        if (
            prompt["device_id"] != case["device_id"]
            or prompt["camera_tag"] != case["camera_tag"]
            or hashlib.sha256(prompt["text"].encode()).hexdigest() != prompt["text_sha256"]
        ):
            raise ValueError("Accepted source prompt/camera binding changed")
    by_slot = {(p["device_id"], p["source_camera_name"], p["bank_rank"]): p for p in prompts.values()}
    ordered = []
    for rank in range(1, 11):
        for wave in range(4):
            for index, device in enumerate(scene_runner.DEVICE_ORDER):
                camera = scene_runner.VIEW_ORDER[device][(wave + index) % 4]
                if (device, camera, rank) in by_slot:
                    ordered.append(row_for(by_slot[(device, camera, rank)]))
    if len(ordered) != len(prompts):
        raise ValueError("Image queue is not the exact accepted-prompt set")
    for position, row in enumerate(ordered, 1):
        row["queue_position"] = position
    return ordered


def lineage(catalog: dict[str, Any]) -> dict[str, Any]:
    original = load(HERE / "baseline/live/generation.json")["rows"][0]["output"]["lineage"]
    if original["source_commit"] != COMMIT or catalog["rewriterVersion"] != original["rewriterVersion"]:
        raise ValueError("The image pipeline differs from the actual GPT-5.5 baseline")
    arguments = {
        "endpoint_base_url": BASE_URL,
        "expected_generator": original["generator"],
        "expected_rewriter": original["rewriterVersion"],
        "expected_pipeline_version": original["pipelineVersion"],
        "lineage_label": original["label"],
        "lineage_source_commit": COMMIT,
        "lineage_patch_sha256": original["patch_sha256"],
        "lineage_runtime_tree_sha256": original["runtime_tree_sha256"],
        "lineage_source_manifest_sha256": original["source_manifest_sha256"],
        "lineage_deployment_manifest_sha256": original["deployment_manifest_sha256"],
        "lineage_candidate_config_sha256": original["candidate_config_sha256"],
    }
    result = scene_runner.lineage_from_args(argparse.Namespace(**arguments))
    scene_runner.validate_catalog(catalog, rows(), result["generator"], result["rewriterVersion"], result)
    return result


def accepted_queue(current_rows: list[dict[str, Any]]) -> dict[str, Any]:
    count = len(current_rows)
    if {row["queue_position"] for row in current_rows} != set(range(1, count + 1)):
        raise ValueError("Accepted queue positions must be contiguous")
    if len({row["row_id"] for row in current_rows}) != count:
        raise ValueError("Accepted queue contains duplicate prompt keys")
    fields = (
        "queue_position",
        "row_id",
        "device_id",
        "digital_twin_id",
        "camera_id",
        "bank_id",
        "rank",
        "prompt_sha256",
        "prompt_record_sha256",
    )
    return {
        "schema_version": 1,
        "expected_count": count,
        "planned_count": 160,
        "queue_policy": "Latin-square device/view/rank interleave, omitting failed writer banks",
        "rows": [{key: row[key] for key in fields} for row in current_rows],
    }


def prepare() -> dict[str, Any]:
    text_study.verify()
    health = httpx.get(BASE_URL + "/health", timeout=60)
    health.raise_for_status()
    catalog_response = httpx.get(BASE_URL + "/api/catalog", timeout=60)
    catalog_response.raise_for_status()
    catalog = catalog_response.json()
    current_rows = rows()
    identity = {
        "schema_version": 3,
        "prompts_sha256": sha(SOURCE),
        "planned_count": 160,
        "expected_count": len(current_rows),
        "catalog_sha256": scene_runner.canonical_sha256(catalog),
        "lineage": lineage(catalog),
        "writer_snapshot_sha256": sha(HERE / "writer_snapshot_manifest.json"),
        "policy": "Every accepted prompt once; zero image replacement/resampling; explicit terminal failures.",
        "files": {
            name: sha(HERE / name)
            for name in (
                "image_study.py",
                "scene_runner.py",
                "report.py",
                "audit_image.py",
                "check_browser.py",
                "public/gallery/index.html",
                "public/gallery/main.js",
                "public/gallery/style.css",
                "public/gallery/imsauth.js",
            )
        },
    }
    identity["run_sha256"] = scene_runner.canonical_sha256(identity)
    for name in ("jobs", "records", "status", "images", "twins", "source/bank_inputs", "journals"):
        (RUN / name).mkdir(parents=True, exist_ok=True)
    write(RUN / "run_manifest.json", identity)
    write(RUN / "catalog.json", catalog)
    write(RUN / "queue_manifest.json", accepted_queue(current_rows))
    write(HERE / "study_manifest.json", identity)
    write(HERE / "endpoint_preflight.json", {"health": health.json(), "model_calls": 0})
    twins = {
        (entry["digital_twin_id"], entry["camera_id"]): entry
        for entry in load(ENDPOINT / "input_bundle/manifest.json")["entries"]
    }
    for row in current_rows:
        entry = twins[(row["digital_twin_id"], row["camera_id"])]
        destination = RUN / "twins" / f"{row['device_id']}__{row['camera_id']}.png"
        data = (ENDPOINT / "input_bundle" / entry["product_path"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != entry["product_sha256"]:
            raise ValueError("Fixed twin bytes changed")
        if not destination.exists():
            write(destination, data)
    for case in load(HERE / "banks.json")["cases"]:
        data = (HERE / case["input"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != case["input_sha256"]:
            raise ValueError("Original source request changed")
        write(RUN / "source/bank_inputs" / f"{case['bank_id']}.json", data)
    print(json.dumps({"image_preflight": "passed", "accepted_prompts": len(current_rows)}), flush=True)
    return identity


def verify() -> dict[str, Any]:
    text_study.verify()
    manifest = load(HERE / "study_manifest.json")
    for name, expected in manifest["files"].items():
        if sha(HERE / name) != expected:
            raise ValueError("Frozen image/report orchestration changed: " + name)
    if sha(SOURCE) != manifest["prompts_sha256"]:
        raise ValueError("Accepted Astra source changed")
    return manifest


def generate() -> None:
    manifest = verify()
    descriptor = os.open(RUN / "generation.lock", os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.write(descriptor, str(os.getpid()).encode())
    os.close(descriptor)
    current_rows = rows()
    scene_runner.append_journal(
        RUN,
        {
            "event": "generation_invocation",
            "selected_count": len(current_rows),
            "selected_row_ids": [row["row_id"] for row in current_rows],
            "run_sha256": manifest["run_sha256"],
        },
    )
    with ThreadPoolExecutor(max_workers=4) as workers:
        futures = {
            workers.submit(
                scene_runner.process,
                RUN,
                row,
                manifest["catalog_sha256"],
                7200,
                manifest["run_sha256"],
                manifest["lineage"],
            ): row
            for row in current_rows
        }
        for future in as_completed(futures):
            row = futures[future]
            try:
                record = future.result()
            except Exception as error:
                record = {
                    "schema_version": 3,
                    "row_id": row["row_id"],
                    "status": "failed",
                    "prompt_sha256": row["prompt_sha256"],
                    "run_sha256": manifest["run_sha256"],
                    "catalog_sha256": manifest["catalog_sha256"],
                    "lineage": manifest["lineage"],
                    "error_type": type(error).__name__,
                    "error": "Scene generation failed; preserved job/status/call ledger is authoritative.",
                }
                scene_runner.atomic_json(scene_runner.paths(RUN, row)["record"], record)
                scene_runner.append_journal(
                    RUN, {"event": "row_failed", "row_id": row["row_id"], "error_type": type(error).__name__}
                )
            print(json.dumps({"row_id": row["row_id"], "status": record["status"]}), flush=True)
    records = [load(scene_runner.paths(RUN, row)["record"]) for row in current_rows]
    write(
        HERE / "image_terminal.json",
        {
            "expected": len(records),
            "done": sum(record["status"] == "done" for record in records),
            "failed": sum(record["status"] != "done" for record in records),
            "failed_writer_banks": load(HERE / "text/terminal.json")["failed_banks"],
            "image_replacements": 0,
            "status": "terminal",
        },
    )


def execute() -> None:
    descriptor = os.open(HERE / "pipeline.lock", os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.write(descriptor, str(os.getpid()).encode())
    os.close(descriptor)
    write(
        HERE / "pipeline_launch.json",
        {
            "pid": os.getpid(),
            "writer_snapshot_sha256": sha(HERE / "writer_snapshot_manifest.json"),
            "stages": ["wait for frozen writer", "accepted-prompt images", "HTML", "browser check", "S3 read-back"],
        },
    )
    scene_runner.atomic_json(HERE / "pipeline_status.json", {"phase": "waiting_for_writer", "pid": os.getpid()})
    while not (HERE / "text/terminal.json").exists():
        launch = load(HERE / "text/launch.json")
        os.kill(launch["pid"], 0)
        time.sleep(10)
    verify_source = text_study.verify()
    if not verify_source:
        raise ValueError("Writer freeze unavailable")
    log = (HERE / "endpoint_service.log").open("x")
    service = subprocess.Popen(
        [sys.executable, str(ENDPOINT / "endpoint.py")],
        stdout=log,
        stderr=subprocess.STDOUT,
        env={
            **os.environ,
            "HP_PR4523_PORT": "8152",
            "HP_PR4523_HOST": "127.0.0.1",
            "HP_PR4523_GENERATION_ENABLED": "1",
            "HP_PR4523_MAX_WORKERS": "4",
            "HP_PR4523_PUBLIC_BASE_URL": BASE_URL,
        },
    )
    try:
        for _ in range(60):
            if service.poll() is not None:
                raise RuntimeError("Owned PR4523 service failed to start; see endpoint_service.log")
            try:
                response = httpx.get(BASE_URL + "/health", timeout=2)
                response.raise_for_status()
                if not owns_listener(service.pid):
                    raise RuntimeError("Loopback listener is not the owned service; refusing to submit")
                break
            except (httpx.ConnectError, httpx.ReadTimeout):
                time.sleep(1)
        else:
            raise TimeoutError("Owned PR4523 service did not become ready")
        write(HERE / "service_ownership.json", {"pid": service.pid, "health": response.json(), "base_url": BASE_URL})
        prepare()
        scene_runner.atomic_json(HERE / "pipeline_status.json", {"phase": "generating_images", "pid": os.getpid()})
        generate()
        import report

        scene_runner.atomic_json(HERE / "pipeline_status.json", {"phase": "building_html", "pid": os.getpid()})
        report.build()
        subprocess.run([sys.executable, str(HERE / "check_browser.py")], check=True)
        report.publish()
    finally:
        if service.poll() is None:
            service.terminate()
            try:
                service.wait(timeout=30)
            except subprocess.TimeoutExpired:
                service.kill()
                service.wait()
        log.close()
        write(HERE / "service_cleanup.json", {"owned_pid": service.pid, "returncode": service.returncode})
    scene_runner.atomic_json(
        HERE / "pipeline_status.json",
        {
            "phase": "complete",
            "pid": os.getpid(),
            "result": load(HERE / "completion_receipt.json"),
        },
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("execute", "verify"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    arguments = parser.parse_args()
    if arguments.command == "execute":
        if not arguments.paid_calls_authorized:
            raise PermissionError("Explicit paid-call authorization required")
        try:
            execute()
        except Exception as error:
            lock = HERE / "pipeline.lock"
            if lock.exists() and lock.read_text().strip() == str(os.getpid()):
                scene_runner.atomic_json(
                    HERE / "pipeline_status.json",
                    {
                        "phase": "error",
                        "error_type": type(error).__name__,
                        "message": "Pipeline stopped; inspect pipeline_execution.log. No automatic semantic resampling.",
                    },
                )
            raise
    else:
        verify()
