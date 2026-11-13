#!/usr/bin/env python3
"""Serial V23 four-row pilot runner; stop and preserve state on first failure."""

from __future__ import annotations

import fcntl
import json
import time
import urllib.request
from pathlib import Path

from common import atomic_json, load_json, require, sha256_file, sha256_json
from config import (
    FREEZE,
    JOB_ROOT,
    LOCAL_ENDPOINT,
    PIPELINE_VERSION,
    PROGRESS,
    SOURCE_HASHES,
    WRAPPER_VERSION,
)
from preflight import verify as verify_preflight


def job_id(slug: str) -> str:
    return f"{slug}__outer_job_1"


def request(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(LOCAL_ENDPOINT + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read())


def wait_for_job(slug: str) -> dict:
    submitted = request("POST", "/api/generate", {"rowSlug": slug, "outerAttempt": 1})
    require(submitted["jobId"] == job_id(slug), "endpoint returned wrong job ID")
    while True:
        status = request("GET", submitted["statusUrl"])
        if status.get("done"):
            return status
        time.sleep(5)


def validate_terminal(slug: str, status: dict) -> tuple[bool, dict]:
    jid = job_id(slug)
    require(status.get("jobId") == jid and status.get("rowSlug") == slug,
            f"{jid}: terminal identity mismatch")
    require(status.get("done") is True and status.get("stage") in {"done", "error"},
            f"{jid}: status is not terminal")
    require(status.get("pipelineVersion") == PIPELINE_VERSION, f"{jid}: pipeline version mismatch")
    require(status.get("wrapperVersion") == WRAPPER_VERSION, f"{jid}: wrapper version mismatch")
    require(status.get("sourceHashes") == SOURCE_HASHES, f"{jid}: source hashes mismatch")
    job = JOB_ROOT / jid
    submission = load_json(job / "submission_request.json")
    require(submission == {"rowSlug": slug, "outerAttempt": 1}, f"{jid}: request mismatch")
    require(status["submissionRequestSha256"] == sha256_json(submission),
            f"{jid}: request hash mismatch")
    success = status["stage"] == "done"
    provenance_name = "provenance.json" if success else "failure_provenance.json"
    hash_key = "provenanceSha256" if success else "failureProvenanceSha256"
    provenance_path = job / provenance_name
    require(provenance_path.is_file() and sha256_file(provenance_path) == status[hash_key],
            f"{jid}: provenance mismatch")
    provenance = load_json(provenance_path)
    require(provenance["job_id"] == jid and provenance["source_hashes"] == SOURCE_HASHES,
            f"{jid}: provenance identity/source mismatch")
    artifacts = provenance["artifacts"]
    require(status["artifactManifestSha256"] == sha256_json(artifacts),
            f"{jid}: artifact manifest mismatch")
    for name, item in artifacts.items():
        path = Path(item["path"])
        require(path.is_file() and sha256_file(path) == item["sha256"]
                and path.stat().st_size == item["bytes"], f"{jid}: artifact mismatch: {name}")
    if success:
        guard = provenance["product_invariant_guard"]
        selected = guard["selected_attempt"]
        require(selected in (1, 2) and guard["attempts"][selected - 1]["verdict"] == "pass",
                f"{jid}: no passing selected image attempt")
    return success, provenance


def main() -> int:
    verify_preflight(allow_progress=True)
    freeze = load_json(FREEZE)
    health = request("GET", "/health")
    require(health.get("ok") is True and health.get("records") == 4
            and health.get("maxWorkers") == 1 and health.get("maxOuterJobs") == 1,
            "endpoint contract failed")
    require(health.get("pipelineVersion") == PIPELINE_VERSION
            and health.get("wrapperVersion") == WRAPPER_VERSION
            and health.get("sourceHashes") == SOURCE_HASHES, "endpoint freeze mismatch")
    lock_path = PROGRESS.with_suffix(".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        progress = load_json(PROGRESS) if PROGRESS.exists() else {
            "schema_version": "hp-position-flex-v23-four-row-pilot-progress-v1",
            "experiment_id": freeze["experiment_id"], "freeze_sha256": sha256_file(FREEZE),
            "pipeline_version": PIPELINE_VERSION, "wrapper_version": WRAPPER_VERSION,
            "source_hashes": SOURCE_HASHES, "total": 4, "done": [], "rows": {},
            "first_failure": None, "complete": False,
        }
        require(progress["freeze_sha256"] == sha256_file(FREEZE), "progress freeze mismatch")
        require(progress.get("first_failure") is None, "first failure is preserved; inspect before restart")
        for ordinal, item in enumerate(freeze["records"], 1):
            slug = item["row_slug"]
            if slug in progress["done"]:
                validate_terminal(slug, load_json(JOB_ROOT / job_id(slug) / "status.json"))
                continue
            try:
                status = wait_for_job(slug)
                success, provenance = validate_terminal(slug, status)
                if not success:
                    raise RuntimeError(status.get("error") or "pilot row failed")
            except Exception as error:
                progress["first_failure"] = {
                    "ordinal": ordinal, "row_slug": slug,
                    "error": f"{type(error).__name__}: {error}",
                    "status_path": str(JOB_ROOT / job_id(slug) / "status.json"),
                }
                atomic_json(PROGRESS, progress)
                raise
            guard = provenance["product_invariant_guard"]
            progress["rows"][slug] = {
                "ordinal": ordinal, "job_id": job_id(slug),
                "image_calls": provenance["image_calls"],
                "guard_verdicts": [x["verdict"] for x in guard["attempts"]],
                "selected_image_attempt": guard["selected_attempt"],
                "provenance_sha256": sha256_file(JOB_ROOT / job_id(slug) / "provenance.json"),
            }
            progress["done"].append(slug)
            atomic_json(PROGRESS, progress)
            print(json.dumps({"completed": len(progress["done"]), "total": 4, "row": slug}), flush=True)
        progress["complete"] = True
        atomic_json(PROGRESS, progress)
        print(json.dumps({"complete": True, "progress": str(PROGRESS)}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
