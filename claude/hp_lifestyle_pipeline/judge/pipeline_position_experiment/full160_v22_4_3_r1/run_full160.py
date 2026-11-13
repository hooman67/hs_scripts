#!/usr/bin/env python3
"""Serial bounded-outer-retry V22.4.3-R1 qualitative-assembly runner."""
from __future__ import annotations

import fcntl
import json
import time
import urllib.request
from pathlib import Path

from common import atomic_json, load_json, require, sha256_file, sha256_json
from config import (
    FREEZE, JOB_ROOT, LOCAL_ENDPOINT, MAX_OUTER_JOBS, PIPELINE_VERSION,
    PROGRESS, RETRYABLE_GUARD_ERROR, SOURCE_HASHES, WRAPPER_VERSION,
)
from preflight import verify as verify_preflight


def job_id(slug: str, outer_attempt: int) -> str:
    require(1 <= outer_attempt <= MAX_OUTER_JOBS, "outer attempt out of range")
    return f"{slug}__outer_job_{outer_attempt}"


def request(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(LOCAL_ENDPOINT + path, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read())


def required_artifact_names(provenance: dict) -> set[str]:
    stage_b_count = len(provenance["stage_b_attempts"])
    image_count = int(provenance["image_calls"])
    require(stage_b_count in (1, 2) and image_count in (1, 2), "attempt counts invalid")
    required = {"result.json", "ours.png", "input.png", "mask.png", "ref_2.png", "geometry_guide.png", "geometry_text.txt", "geometry_request.json", "geometry_response.json", "calls.json", "submission_request.json"}
    for attempt in range(1, stage_b_count + 1):
        required |= {f"stage_b_attempt_{attempt}_request.json", f"stage_b_attempt_{attempt}_response.json"}
    if stage_b_count == 2:
        required.add("stage_b_attempt_2_raw_response.json")
    for attempt in range(1, image_count + 1):
        required |= {f"gpt_{attempt}.png", f"image_request_attempt_{attempt}.json", f"product_invariant_attempt_{attempt}.json"}
    return required


def _artifact_names(artifacts: dict) -> set[str]:
    return {Path(item["path"]).name for item in artifacts.values()}


def _validate_artifacts(jid: str, artifacts: dict) -> None:
    for name, item in artifacts.items():
        path = Path(item["path"])
        require(path.is_file(), f"{jid}: missing artifact {name}")
        require(sha256_file(path) == item["sha256"], f"{jid}: artifact hash mismatch: {name}")
        require(path.stat().st_size == item["bytes"], f"{jid}: artifact size mismatch: {name}")


def validate_completed(slug: str, outer_attempt: int, status: dict) -> dict:
    jid = job_id(slug, outer_attempt)
    require(status.get("jobId") == jid and status.get("rowSlug") == slug and status.get("outerAttempt") == outer_attempt, f"{jid}: identity mismatch")
    require(status.get("done") is True and status.get("stage") == "done", f"{jid}: job is not done")
    require(status.get("pipelineVersion") == PIPELINE_VERSION and status.get("wrapperVersion") == WRAPPER_VERSION, f"{jid}: version mismatch")
    require(status.get("sourceHashes") == SOURCE_HASHES, f"{jid}: source hash mismatch")
    job = JOB_ROOT / jid
    request_body = load_json(job / "submission_request.json")
    require(request_body == {"rowSlug": slug, "outerAttempt": outer_attempt}, f"{jid}: submission request differs")
    require(status["submissionRequestSha256"] == sha256_json(request_body), f"{jid}: request hash mismatch")
    provenance_path = job / "provenance.json"
    require(provenance_path.is_file() and sha256_file(provenance_path) == status["provenanceSha256"], f"{jid}: provenance hash mismatch")
    provenance = load_json(provenance_path)
    require(provenance["job_id"] == jid and provenance["row_slug"] == slug and provenance["outer_attempt"] == outer_attempt, f"{jid}: provenance identity mismatch")
    require(provenance["submission_request_sha256"] == status["submissionRequestSha256"], f"{jid}: provenance request mismatch")
    require(provenance["pipeline_version"] == PIPELINE_VERSION and provenance["wrapper_version"] == WRAPPER_VERSION and provenance["source_hashes"] == SOURCE_HASHES, f"{jid}: provenance version mismatch")
    guard = provenance["product_invariant_guard"]
    selected = guard["selected_attempt"]
    require(selected in (1, 2) and guard["attempts"][selected - 1]["verdict"] == "pass", f"{jid}: guard has no passing selection")
    require(len(guard["attempts"]) == provenance["image_calls"], f"{jid}: guard/image mismatch")
    artifacts = provenance["artifacts"]
    require(status["artifactManifestSha256"] == sha256_json(artifacts), f"{jid}: artifact manifest hash mismatch")
    require(required_artifact_names(provenance) <= _artifact_names(artifacts), f"{jid}: incomplete artifact manifest")
    _validate_artifacts(jid, artifacts)
    by_name = {Path(item["path"]).name: item for item in artifacts.values()}
    require(by_name["ours.png"]["sha256"] == by_name[f"gpt_{selected}.png"]["sha256"], f"{jid}: selected output differs from raw attempt")
    return provenance


def validate_failed(slug: str, outer_attempt: int, status: dict) -> dict:
    jid = job_id(slug, outer_attempt)
    require(status.get("jobId") == jid and status.get("rowSlug") == slug and status.get("outerAttempt") == outer_attempt, f"{jid}: identity mismatch")
    require(status.get("done") is True and status.get("stage") == "error" and isinstance(status.get("error"), str), f"{jid}: job is not a terminal error")
    require(status.get("pipelineVersion") == PIPELINE_VERSION and status.get("wrapperVersion") == WRAPPER_VERSION and status.get("sourceHashes") == SOURCE_HASHES, f"{jid}: failure version mismatch")
    job = JOB_ROOT / jid
    request_body = load_json(job / "submission_request.json")
    require(request_body == {"rowSlug": slug, "outerAttempt": outer_attempt}, f"{jid}: failure request differs")
    require(status["submissionRequestSha256"] == sha256_json(request_body), f"{jid}: failure request hash mismatch")
    path = job / "failure_provenance.json"
    require(path.is_file() and sha256_file(path) == status["failureProvenanceSha256"], f"{jid}: failure provenance hash mismatch")
    failure = load_json(path)
    require(failure["job_id"] == jid and failure["error"] == status["error"], f"{jid}: failure provenance differs")
    require(failure["submission_request_sha256"] == status["submissionRequestSha256"], f"{jid}: failure request provenance differs")
    require(failure["pipeline_version"] == PIPELINE_VERSION and failure["wrapper_version"] == WRAPPER_VERSION and failure["source_hashes"] == SOURCE_HASHES, f"{jid}: failure provenance version mismatch")
    require(status["artifactManifestSha256"] == sha256_json(failure["artifacts"]), f"{jid}: failure artifact manifest hash mismatch")
    _validate_artifacts(jid, failure["artifacts"])
    return failure


def should_retry(status: dict, outer_attempt: int) -> bool:
    return outer_attempt == 1 and status.get("stage") == "error" and status.get("error") == RETRYABLE_GUARD_ERROR


def wait_for_job(slug: str, outer_attempt: int) -> dict:
    submitted = request("POST", "/api/generate", {"rowSlug": slug, "outerAttempt": outer_attempt})
    require(submitted["jobId"] == job_id(slug, outer_attempt), "endpoint returned wrong job ID")
    while True:
        status = request("GET", submitted["statusUrl"])
        if status.get("done"):
            return status
        time.sleep(5)


def audit_summary(slug: str, outer_attempt: int, status: dict) -> dict:
    jid = job_id(slug, outer_attempt)
    job = JOB_ROOT / jid
    result = {
        "job_id": jid, "outer_attempt": outer_attempt, "outcome": status["stage"],
        "error": status.get("error"), "submission_request_sha256": status["submissionRequestSha256"],
        "status_path": str(job / "status.json"), "status_sha256": sha256_file(job / "status.json"),
        "artifact_manifest_sha256": status["artifactManifestSha256"],
    }
    if status["stage"] == "done":
        result.update(provenance_path=str(job / "provenance.json"), provenance_sha256=status["provenanceSha256"])
    else:
        result.update(failure_provenance_path=str(job / "failure_provenance.json"), failure_provenance_sha256=status["failureProvenanceSha256"])
    return result


def initial_progress(health: dict, freeze: dict) -> dict:
    return {
        "schema_version": "hp-position-flex-v22.4.3-r1-qualitative-assembly-progress-v1",
        "experiment_id": freeze["experiment_id"], "freeze_sha256": sha256_file(FREEZE),
        "endpoint_instance_id": health["instanceId"], "pipeline_version": health["pipelineVersion"],
        "wrapper_version": health["wrapperVersion"], "source_hashes": health["sourceHashes"],
        "protocol": {"serial": True, "max_outer_jobs_per_row": MAX_OUTER_JOBS, "retry_only_exact_error": RETRYABLE_GUARD_ERROR, "interpretation": "Qualitative-assembly completion statistics; not native V22.4.3 per-job reliability."},
        "total": 160, "done": [], "rows": {}, "counts": {"first_job_pass": 0, "recovered_on_retry": 0, "terminal_failure": 0}, "rates": {}, "first_error": None,
    }


def update_rates(progress: dict) -> None:
    counts = progress["counts"]
    attempted = sum(counts.values())
    progress["rates"] = {"denominator_rows_attempted": attempted, **{f"{key}_rate": (value / attempted if attempted else 0.0) for key, value in counts.items()}}


def main() -> int:
    verify_preflight(allow_progress=True)
    freeze = load_json(FREEZE)
    health = request("GET", "/health")
    require(health.get("ok") is True and health.get("records") == 160 and health.get("maxWorkers") == 1 and health.get("maxOuterJobs") == MAX_OUTER_JOBS, "endpoint contract failed")
    require(health.get("pipelineVersion") == PIPELINE_VERSION and health.get("wrapperVersion") == WRAPPER_VERSION and health.get("sourceHashes") == SOURCE_HASHES, "endpoint version contract failed")
    lock_path = PROGRESS.with_suffix(".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError("another full160 runner holds the progress lock") from error
        progress = load_json(PROGRESS) if PROGRESS.exists() else initial_progress(health, freeze)
        require(progress["experiment_id"] == freeze["experiment_id"] and progress["freeze_sha256"] == sha256_file(FREEZE), "progress identity mismatch")
        require(progress["pipeline_version"] == PIPELINE_VERSION and progress["wrapper_version"] == WRAPPER_VERSION and progress["source_hashes"] == SOURCE_HASHES, "progress version mismatch")
        require(progress.get("first_error") is None, "terminal failure preserved; inspect before any deliberate restart")
        ordered = sorted(freeze["records"], key=lambda x: (x["device_id"], x["camera_tag"], x["bank_rank"]))
        done = set(progress["done"])
        for ordinal, item in enumerate(ordered, 1):
            slug = item["row_slug"]
            if slug in done:
                chosen = progress["rows"][slug]["selected_job_id"]
                attempt = int(chosen.rsplit("_", 1)[1])
                validate_completed(slug, attempt, load_json(JOB_ROOT / chosen / "status.json"))
                continue
            jobs = []
            try:
                status1 = wait_for_job(slug, 1)
                if status1["stage"] == "done":
                    provenance = validate_completed(slug, 1, status1)
                    jobs.append(audit_summary(slug, 1, status1))
                    classification, chosen_attempt = "first_job_pass", 1
                else:
                    validate_failed(slug, 1, status1)
                    jobs.append(audit_summary(slug, 1, status1))
                    if not should_retry(status1, 1):
                        raise RuntimeError(f"non-retryable initial job error: {status1['error']}")
                    status2 = wait_for_job(slug, 2)
                    if status2["stage"] == "done":
                        provenance = validate_completed(slug, 2, status2)
                        jobs.append(audit_summary(slug, 2, status2))
                        classification, chosen_attempt = "recovered_on_retry", 2
                    else:
                        validate_failed(slug, 2, status2)
                        jobs.append(audit_summary(slug, 2, status2))
                        raise RuntimeError(f"second outer job failed: {status2['error']}")
            except Exception as error:
                progress["counts"]["terminal_failure"] += 1
                update_rates(progress)
                progress["first_error"] = {"row_slug": slug, "ordinal": ordinal, "error": f"{type(error).__name__}: {error}", "jobs": jobs}
                atomic_json(PROGRESS, progress)
                raise
            chosen = job_id(slug, chosen_attempt)
            guard = provenance["product_invariant_guard"]
            by_name = {Path(v["path"]).name: v for v in provenance["artifacts"].values()}
            progress["rows"][slug] = {
                "ordinal": ordinal, "classification": classification, "selected_job_id": chosen,
                "selected_raw_output_sha256": by_name[f"gpt_{guard['selected_attempt']}.png"]["sha256"],
                "jobs": jobs, "stage_b_attempts": len(provenance["stage_b_attempts"]),
                "image_attempts": provenance["image_calls"], "guard_verdicts": [x["verdict"] for x in guard["attempts"]],
                "selected_image_attempt": guard["selected_attempt"],
            }
            progress["counts"][classification] += 1
            done.add(slug)
            progress["done"] = [x["row_slug"] for x in ordered if x["row_slug"] in done]
            progress["last_completed"] = slug
            update_rates(progress)
            atomic_json(PROGRESS, progress)
            print(json.dumps({"completed": len(done), "total": 160, "row": slug, "classification": classification}), flush=True)
        progress["complete"] = True
        progress["methodological_note"] = "Each row may use a second independent endpoint job only after an exact product-invariant guard rejection. Rates describe this bounded-retry qualitative assembly protocol and must not be reported as native V22.4.3 reliability."
        update_rates(progress)
        atomic_json(PROGRESS, progress)
        print(json.dumps({"complete": True, "counts": progress["counts"], "rates": progress["rates"], "progress": str(PROGRESS)}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
