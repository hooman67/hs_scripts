#!/usr/bin/env python3
"""Fail-fast, atomically resumable, serial V22.4.2 full-160 submitter."""

from __future__ import annotations

import fcntl
import json
import time
import urllib.request
from pathlib import Path

from common import atomic_json, load_json, require, sha256_file
from config import FREEZE, JOB_ROOT, LOCAL_ENDPOINT, PIPELINE_VERSION, PROGRESS, SOURCE_HASHES
from preflight import verify as verify_preflight


def request(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        LOCAL_ENDPOINT + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read())


def validate_completed(slug: str, status: dict) -> dict:
    require(status.get("done") is True and status.get("stage") == "done", f"{slug}: job is not done")
    require(status.get("pipelineVersion") == PIPELINE_VERSION, f"{slug}: pipeline version mismatch")
    require(status.get("sourceHashes") == SOURCE_HASHES, f"{slug}: source hash mismatch")
    provenance_path = JOB_ROOT / slug / "provenance.json"
    require(provenance_path.is_file(), f"{slug}: missing provenance")
    require(sha256_file(provenance_path) == status["provenanceSha256"], f"{slug}: provenance hash mismatch")
    provenance = load_json(provenance_path)
    require(provenance["pipeline_version"] == PIPELINE_VERSION, f"{slug}: provenance pipeline mismatch")
    require(provenance["source_hashes"] == SOURCE_HASHES, f"{slug}: provenance source mismatch")
    attempts = provenance["product_invariant_guard"]["attempts"]
    selected = provenance["product_invariant_guard"]["selected_attempt"]
    require(selected in (1, 2) and attempts[selected - 1]["verdict"] == "pass", f"{slug}: guard has no passing selection")
    require(len(attempts) == provenance["image_calls"], f"{slug}: guard/image attempt mismatch")
    require(len(provenance["stage_b_attempts"]) in (1, 2), f"{slug}: Stage-B attempt count invalid")
    artifacts = provenance.get("artifacts") or {}
    required = {
        "result.json", "ours.png", "input.png", "mask.png", "ref_2.png",
        "geometry_guide.png", "geometry_text.txt", "geometry_request.json",
        "geometry_response.json", "planning_request.json", "planning_response.json",
        "calls.json",
    }
    require(required <= set(artifacts), f"{slug}: incomplete artifact manifest")
    for name, item in artifacts.items():
        path = Path(item["path"])
        require(path.is_file(), f"{slug}: missing artifact {name}")
        require(sha256_file(path) == item["sha256"], f"{slug}: artifact hash mismatch: {name}")
        require(path.stat().st_size == item["bytes"], f"{slug}: artifact size mismatch: {name}")
    selected_raw = artifacts[f"gpt_{selected}.png"]
    require(artifacts["ours.png"]["sha256"] == selected_raw["sha256"], f"{slug}: selected output differs from raw attempt")
    return provenance


def initial_progress(health: dict, freeze: dict) -> dict:
    return {
        "schema_version": "hp-position-flex-full160-progress-v1",
        "experiment_id": freeze["experiment_id"],
        "freeze_sha256": sha256_file(FREEZE),
        "endpoint_instance_id": health["instanceId"],
        "pipeline_version": health["pipelineVersion"],
        "source_hashes": health["sourceHashes"],
        "serial": True,
        "total": 160,
        "done": [],
        "rows": {},
        "first_error": None,
    }


def completed_progress_row(provenance: dict, ordinal: int) -> dict:
    """Summarize one validated row without assuming duplicate top-level guard data."""
    guard = provenance["product_invariant_guard"]
    return {
        "ordinal": ordinal,
        "stage_b_attempts": len(provenance["stage_b_attempts"]),
        "image_attempts": provenance["image_calls"],
        "guard_verdicts": [attempt["verdict"] for attempt in guard["attempts"]],
        "selected_attempt": guard["selected_attempt"],
    }


def main() -> int:
    verify_preflight(allow_progress=True)
    freeze = load_json(FREEZE)
    health = request("GET", "/health")
    require(health.get("ok") is True, "endpoint health failed")
    require(health.get("records") == 160 and health.get("maxWorkers") == 1, "endpoint is not frozen serial full160")
    require(health.get("pipelineVersion") == PIPELINE_VERSION, "endpoint pipeline version mismatch")
    require(health.get("sourceHashes") == SOURCE_HASHES, "endpoint source hash mismatch")

    lock_path = PROGRESS.with_suffix(".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError("another full160 runner holds the progress lock") from error

        progress = load_json(PROGRESS) if PROGRESS.exists() else initial_progress(health, freeze)
        require(progress["experiment_id"] == freeze["experiment_id"], "progress belongs to another experiment")
        require(progress["freeze_sha256"] == sha256_file(FREEZE), "progress freeze hash mismatch")
        require(progress["pipeline_version"] == PIPELINE_VERSION, "progress pipeline mismatch")
        require(progress["source_hashes"] == SOURCE_HASHES, "progress source mismatch")
        require(progress.get("first_error") is None, "previous first error is preserved; inspect before deliberate restart")

        ordered = sorted(
            freeze["records"],
            key=lambda item: (item["device_id"], item["camera_tag"], item["bank_rank"]),
        )
        done = set(progress["done"])
        for ordinal, item in enumerate(ordered, start=1):
            slug = item["row_slug"]
            if slug in done:
                status_path = JOB_ROOT / slug / "status.json"
                require(status_path.is_file(), f"{slug}: progress says done but status is missing")
                validate_completed(slug, load_json(status_path))
                continue
            try:
                submitted = request("POST", "/api/generate", {"rowSlug": slug})
                while True:
                    status = request("GET", submitted["statusUrl"])
                    if status.get("done"):
                        break
                    time.sleep(5)
                if status.get("stage") != "done":
                    raise RuntimeError(status.get("error") or "pipeline returned an unspecified error")
                provenance = validate_completed(slug, status)
            except Exception as error:
                progress["first_error"] = {
                    "row_slug": slug,
                    "ordinal": ordinal,
                    "error": f"{type(error).__name__}: {error}",
                }
                atomic_json(PROGRESS, progress)
                raise
            done.add(slug)
            progress["done"] = [record["row_slug"] for record in ordered if record["row_slug"] in done]
            row_progress = completed_progress_row(provenance, ordinal)
            row_progress.update({
                "status_sha256": sha256_file(JOB_ROOT / slug / "status.json"),
                "provenance_sha256": sha256_file(JOB_ROOT / slug / "provenance.json"),
            })
            progress["rows"][slug] = row_progress
            progress["last_completed"] = slug
            atomic_json(PROGRESS, progress)
            print(json.dumps({"completed": len(done), "total": 160, "row": slug}), flush=True)
        progress["complete"] = True
        atomic_json(PROGRESS, progress)
        print(json.dumps({"complete": True, "rows": len(done), "progress": str(PROGRESS)}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

