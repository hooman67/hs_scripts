"""Complete only missing image slots with unchanged native PR4523 calls."""

from __future__ import annotations

import argparse
import copy
import os
import shutil
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import httpx

import image_study as original
import scene_runner
from recovery.complete160 import text_recovery

HERE = text_recovery.HERE
ROOT = text_recovery.ROOT
ENDPOINT = HERE / "endpoint_pr4523"
PORT = 8153
BASE_URL = f"http://127.0.0.1:{PORT}"
COMMIT = original.COMMIT
load, sha, write = text_recovery.load, text_recovery.sha, text_recovery.write
row_for = original.row_for


def image_runner() -> Any:
    return scene_runner


def listener_owned(pid: int) -> bool:
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
        if fields[1] == f"0100007F:{PORT:04X}" and fields[3] == "0A":
            return fields[9] in sockets
    return False


def prepare() -> None:
    text_recovery.verify()
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", PORT))
    files = load(ROOT / "copied_source_manifest.json")["files"]
    copied = {}
    for name, digest in files.items():
        if not name.startswith("endpoint_pr4523/"):
            continue
        if sha(ROOT / name) != digest:
            raise ValueError("Original native endpoint changed")
        destination = HERE / name
        write(destination, (ROOT / name).read_bytes())
        copied[name] = digest
    preserved = {}
    for folder in ("run/records", "run/jobs", "run/images", "input_audit"):
        for path in (ROOT / folder).rglob("*"):
            if path.is_file():
                preserved[str(path.relative_to(ROOT))] = sha(path)
    write(
        HERE / "native_snapshot.json",
        {"files": copied, "code_sha256": sha(Path(__file__)), "port": PORT, "preserved_image_files": preserved},
    )


def verify() -> None:
    text_recovery.verify()
    snapshot = load(HERE / "native_snapshot.json")
    if sha(Path(__file__)) != snapshot["code_sha256"]:
        raise ValueError("Image recovery source changed after freeze")
    for name, digest in snapshot["files"].items():
        if sha(HERE / name) != digest:
            raise ValueError("Recovered native endpoint differs from original: " + name)
    for name, digest in snapshot["preserved_image_files"].items():
        if sha(ROOT / name) != digest:
            raise ValueError("Original image evidence changed: " + name)


def selected_rows() -> list[dict[str, Any]]:
    document = load(HERE / "exports/prompts_all_160.json")
    old = load(ROOT / "text/exports/prompts_all.json")
    old_prompts = {prompt["prompt_key"]: prompt for prompt in old["prompts"]}
    prompts = {prompt["prompt_key"]: prompt for prompt in document["prompts"]}
    for key, prompt in old_prompts.items():
        if prompts[key] != prompt:
            raise ValueError("An original accepted prompt was modified")
    successful = set()
    for path in (ROOT / "run/records").glob("*.json"):
        record = load(path)
        if record["status"] == "done":
            key = record["row_id"]
            if scene_runner.valid_completed_record(ROOT / "run", row_for(prompts[key])) is None:
                raise ValueError("Original successful image no longer matches its frozen native record")
            successful.add(key)
    if len(prompts) != 160 or len(successful) != 79:
        raise ValueError("Expected160 completed texts and79 preserved images")
    by_slot = {
        (prompt["device_id"], prompt["source_camera_name"], prompt["bank_rank"]): prompt
        for prompt in document["prompts"]
        if prompt["prompt_key"] not in successful
    }
    rows = []
    for rank in range(1, 11):
        for wave in range(4):
            for index, device in enumerate(scene_runner.DEVICE_ORDER):
                camera = scene_runner.VIEW_ORDER[device][(wave + index) % 4]
                if (device, camera, rank) in by_slot:
                    row = row_for(by_slot[(device, camera, rank)])
                    row["queue_position"] = len(rows) + 1
                    rows.append(row)
    if len(rows) != 81:
        raise ValueError("Missing-image queue must contain exactly81 slots")
    return rows


def retryable_record(record: dict[str, Any]) -> bool:
    message = record.get("error", "")
    return any(
        marker in message
        for marker in (
            "Error code: 408",
            "Error code: 409",
            "Error code: 429",
            "Error code: 500",
            "Error code: 502",
            "Error code: 503",
            "Error code: 504",
            "APITimeoutError",
            "APIConnectionError",
            "ReadTimeout",
            "ConnectTimeout",
        )
    )


def render(row: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    result_path = HERE / "image_results" / (row["row_slug"] + ".json")
    if result_path.exists():
        result = load(result_path)
        if scene_runner.valid_completed_record(Path(result["run"]), row) is None:
            raise ValueError("Saved recovery success is not a valid native output")
        return result
    number = 0
    while True:
        number += 1
        run = HERE / "image_attempts" / row["row_slug"] / f"attempt_{number:04d}"
        if not run.exists():
            for name in ("jobs", "records", "status", "images", "journals"):
                (run / name).mkdir(parents=True, exist_ok=True)
            write(run / "run_manifest.json", manifest)
        paths = scene_runner.paths(run, row)
        if not paths["job"].exists() and (run / "journals/events.jsonl").exists():
            raise RuntimeError("Interrupted image submission without a saved job; inspect before replay")
        if not paths["job"].exists() and shutil.disk_usage(HERE).free < 512 * 1024**2:
            raise OSError("Less than512MiB free on durable storage; preserve existing jobs and stop new submissions")
        if paths["record"].exists() and load(paths["record"])["status"] == "failed":
            record = load(paths["record"])
        else:
            while True:
                try:
                    record = scene_runner.process(
                        run, row, manifest["catalog_sha256"], 7200, manifest["run_sha256"], manifest["lineage"]
                    )
                    break
                except (httpx.HTTPError, TimeoutError):
                    if not paths["job"].exists():
                        raise RuntimeError(
                            "Ambiguous image submission; inspect native jobs before any replay"
                        ) from None
                    if not listener_owned(load(HERE / "service_ownership.json")["pid"]):
                        raise RuntimeError("Owned image service is no longer available") from None
                    time.sleep(30)
        scene_runner.atomic_json(
            HERE / "image_status" / (row["row_slug"] + ".json"),
            {"attempt": number, "status": record["status"], "job_id": record["job_id"], "run": str(run)},
        )
        print({"row": row["row_id"], "attempt": number, "status": record["status"]}, flush=True)
        if record["status"] == "done":
            result = {
                "row_id": row["row_id"],
                "run": str(run),
                "record_sha256": sha(paths["record"]),
                "attempts": number,
                "job_id": record["job_id"],
                "image_sha256": record["image_sha256"],
            }
            write(result_path, result)
            return result
        if not retryable_record(record):
            raise RuntimeError("Nontransient native failure; original record is preserved: " + row["row_id"])
        time.sleep(min(300, number * 15))


@contextmanager
def native_service(enabled: bool, label: str):
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", PORT))
    log = (HERE / (label + "_execution.log")).open("x")
    service = subprocess.Popen(
        [sys.executable, str(ENDPOINT / "endpoint.py")],
        stdout=log,
        stderr=subprocess.STDOUT,
        env={
            **os.environ,
            "HP_PR4523_HOST": "127.0.0.1",
            "HP_PR4523_PORT": str(PORT),
            "HP_PR4523_GENERATION_ENABLED": "1" if enabled else "0",
            "HP_PR4523_MAX_WORKERS": "4",
            "HP_PR4523_PUBLIC_BASE_URL": BASE_URL,
        },
    )
    try:
        for _ in range(60):
            if service.poll() is not None:
                raise RuntimeError("Recovered native endpoint failed to start")
            try:
                response = httpx.get(BASE_URL + "/health", timeout=2)
                response.raise_for_status()
            except (httpx.ConnectError, httpx.ReadTimeout):
                time.sleep(1)
                continue
            if not listener_owned(service.pid):
                raise RuntimeError("Port8153 is not owned by the launched child")
            break
        else:
            raise TimeoutError("Recovered native endpoint readiness timed out")
        health = response.json()
        if health["candidateLineage"]["sourceCommit"] != COMMIT or health["generationEnabled"] != enabled:
            raise ValueError("Recovered endpoint is not exact PR4523")
        write(HERE / (label + "_ownership.json"), {"pid": service.pid, "health": health, "base_url": BASE_URL})
        yield health
    finally:
        if service.poll() is None:
            service.terminate()
            try:
                service.wait(timeout=30)
            except subprocess.TimeoutExpired:
                service.kill()
                service.wait()
        log.close()
        write(HERE / (label + "_cleanup.json"), {"owned_pid": service.pid, "returncode": service.returncode})


def catalog_lineage(rows: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    response = httpx.get(BASE_URL + "/api/catalog", timeout=60)
    response.raise_for_status()
    catalog = response.json()
    lineage = copy.deepcopy(load(ROOT / "study_manifest.json")["lineage"])
    lineage.update(endpoint_base_url=BASE_URL, endpoint=BASE_URL + "/api/generate")
    scene_runner.validate_catalog(catalog, rows, lineage["generator"], lineage["rewriterVersion"], lineage)
    return catalog, lineage


def preflight() -> None:
    verify()
    with native_service(False, "preflight_service") as health:
        catalog, lineage = catalog_lineage(original.rows())
        write(
            HERE / "native_preflight.json",
            {
                "health": health,
                "catalog_sha256": scene_runner.canonical_sha256(catalog),
                "lineage": lineage,
                "model_calls": 0,
            },
        )


def execute() -> None:
    verify()
    descriptor = os.open(HERE / "pipeline.lock", os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.write(descriptor, str(os.getpid()).encode())
    os.close(descriptor)
    write(HERE / "pipeline_launch.json", {"pid": os.getpid(), "text_owner": load(HERE / "text_launch.json")})
    scene_runner.atomic_json(HERE / "pipeline_status.json", {"phase": "waiting_for_text", "pid": os.getpid()})
    while not (HERE / "text_terminal.json").exists():
        os.kill(load(HERE / "text_launch.json")["pid"], 0)
        time.sleep(15)
    rows = selected_rows()
    write(HERE / "image_queue.json", {"actual_count": 81, "final_astra_count": 160, "rows": rows})
    with native_service(True, "service"):
        catalog, lineage = catalog_lineage(rows)
        manifest = {
            "schema_version": 3,
            "expected_count": 81,
            "catalog_sha256": scene_runner.canonical_sha256(catalog),
            "lineage": lineage,
            "source_export_sha256": sha(HERE / "exports/prompts_all_160.json"),
            "native_snapshot_sha256": sha(HERE / "native_snapshot.json"),
        }
        manifest["run_sha256"] = scene_runner.canonical_sha256(manifest)
        write(HERE / "image_manifest.json", manifest)
        scene_runner.atomic_json(
            HERE / "pipeline_status.json", {"phase": "generating_81_missing_images", "pid": os.getpid()}
        )
        with ThreadPoolExecutor(max_workers=4) as workers:
            futures = [workers.submit(render, row, manifest) for row in rows]
            results = [future.result() for future in as_completed(futures)]
        write(
            HERE / "image_terminal.json",
            {"status": "complete", "new_images": 81, "preserved_images": 79, "final_images": 160, "results": results},
        )
    from recovery.complete160 import completed_report

    scene_runner.atomic_json(HERE / "pipeline_status.json", {"phase": "building_completed_report", "pid": os.getpid()})
    completed_report.execute()
    scene_runner.atomic_json(HERE / "pipeline_status.json", {"phase": "complete", "pid": os.getpid()})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "preflight", "execute"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    arguments = parser.parse_args()
    if arguments.command == "prepare":
        prepare()
    elif arguments.command == "preflight":
        preflight()
    elif arguments.paid_calls_authorized:
        execute()
    else:
        raise PermissionError("Paid-call authorization required")
