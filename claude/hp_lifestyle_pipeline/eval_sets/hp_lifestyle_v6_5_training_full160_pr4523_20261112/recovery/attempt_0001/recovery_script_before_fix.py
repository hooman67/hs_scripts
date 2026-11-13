"""Retry only proven terminal pre-image failures, preserving every original attempt."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import time

import httpx

import study

RECOVERY = study.HERE / "recovery"
RETRYABLE = re.compile(
    r"Elliptical support must contain all four product footprint corners"
    r"|Image prompt mentions an image the image model does not receive"
    r"|rate.?limit|timed? ?out|temporar|server_error|InternalServerError"
    r"|ConnectionError|APIConnectionError|\b(?:429|500|502|503|504)\b",
    re.IGNORECASE,
)


def inspect_failure(prompt):
    runner = study.image_runner()
    row = study.row_for(prompt)
    if runner.valid_completed_record(study.HERE / "run", row):
        raise ValueError("refusing to retry a successful image")
    paths = runner.paths(study.HERE / "run", row)
    record = study.load(paths["record"])
    job = study.load(paths["job"])
    expected = {
        "digitalTwinId": runner.DEVICE_MAP[prompt["device_id"]],
        "cameraId": prompt["source_camera_name"], "prompt": prompt["text"],
    }
    if (
        record["status"] != "failed" or job["request"] != expected
        or record.get("job_id") != job["submit_response"]["jobId"]
    ):
        raise ValueError("failed submission is ambiguous or not the exact frozen request")
    native = study.ENDPOINT / "run/jobs" / record["job_id"]
    native_job = study.load(native / "job.json")
    status = study.load(native / "status.json")
    calls = study.load(native / "calls.json")
    if (
        native_job["request"] != expected or not status["done"]
        or status["stages"]["scene"]["status"] != "error"
        or status["instanceId"] != study.load(study.HERE / "endpoint_preflight.json")["health"]["instanceId"]
    ):
        raise ValueError("native terminal failure/ownership is unproven")
    if any(call["kind"] == "image_edit" for call in calls):
        raise ValueError("image edit was attempted; reconcile its raw result rather than blindly redraw")
    if not RETRYABLE.search(record["error"]):
        raise ValueError("failure is not an established operational retry; inspect before proceeding")
    return row, paths, record, native


def run(authorized):
    if not authorized:
        raise PermissionError("operational replacements require explicit authorization")
    primary = study.load(study.HERE / "generation_terminal.json")
    if primary["counts"]["pending"]:
        raise ValueError("finish and preserve the original primary pass before recovery")
    frozen = study.verify()
    selected = set(frozen["new_row_ids"])
    prompts = {p["prompt_key"]: p for p in study.load(study.SOURCE)["prompts"]}
    RECOVERY.mkdir(exist_ok=True)
    attempt = len(list(RECOVERY.glob("attempt_*/complete.json"))) + 1
    while True:
        counts = study.counts()
        if counts["done"] == 160 and not counts["failed"] and not counts["pending"]:
            study.write(RECOVERY / "complete.json", {"at_utc": study.now(), "counts": counts})
            print(study.json.dumps(counts), flush=True)
            return
        if counts["pending"]:
            raise ValueError("unreconciled missing/ambiguous records; do not blindly submit")
        response = httpx.get(study.endpoint_url() + "/health", timeout=30)
        response.raise_for_status()
        if response.json()["instanceId"] != study.load(study.HERE / "endpoint_preflight.json")["health"]["instanceId"]:
            raise ValueError("owned endpoint instance changed")
        failed = [
            prompts[key] for key in frozen["new_row_ids"]
            if not study.image_runner().valid_completed_record(study.HERE / "run", study.row_for(prompts[key]))
        ]
        if not failed or any(p["prompt_key"] not in selected for p in failed):
            raise ValueError("recovery selection escapes authorized primary rows")
        folder = RECOVERY / f"attempt_{attempt:04d}"
        if folder.exists():
            raise FileExistsError("incomplete recovery attempt exists; inspect before resuming")
        inspected = [inspect_failure(prompt) for prompt in failed]
        archived = []
        for row, paths, record, native in inspected:
            files = {}
            for name, path in paths.items():
                if path.exists():
                    target = folder / "original_client" / row["row_slug"] / path.name
                    study.write(target, path.read_bytes())
                    files[name] = {"original_path": str(path), "archived_path": str(target),
                                   "sha256": study.sha(target)}
            native_files = {
                str(path): study.sha(path) for path in native.rglob("*") if path.is_file()
            }
            archived.append({
                "row_id": row["row_id"], "failed_job_id": record["job_id"],
                "error": record["error"], "client_files": files, "native_files_sha256": native_files,
            })
        selection = folder / "selection.json"
        study.write(selection, {
            "source_prompts_sha256": study.sha(study.SOURCE),
            "row_ids": [p["prompt_key"] for p in failed], "rows": failed,
        })
        command = study.legacy().runner_command()
        command[command.index("--selection-file") + 1] = str(selection)
        study.write(folder / "manifest.json", {
            "at_utc": study.now(), "authorization": frozen["failure_policy"],
            "study_manifest_sha256": study.sha(study.HERE / "study_manifest.json"),
            "source_code_sha256": study.sha(Path(__file__)), "command": command, "failures": archived,
            "successful_images_redrawn": 0, "native_job_deletions": 0,
            "recorded_before_any_new_submission": True,
        })
        for row, paths, _record, _native in inspected:
            expected = next(item for item in archived if item["row_id"] == row["row_id"])
            if study.sha(paths["job"]) != expected["client_files"]["job"]["sha256"]:
                raise ValueError("client job changed after verified preservation")
            paths["job"].unlink()
        with (folder / "execution.log").open("x") as stream:
            result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        final = study.counts()
        study.write(folder / "complete.json", {
            "at_utc": study.now(), "process_exit_code": result.returncode, "counts": final,
        })
        print(study.json.dumps({"attempt": attempt, "selected": len(failed), "counts": final}), flush=True)
        if result.returncode:
            raise RuntimeError("recovery process failed; inspect saved jobs before any further operation")
        attempt += 1
        if final["failed"]:
            time.sleep(min(60, 2 ** min(attempt, 6)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paid-calls-authorized", action="store_true")
    run(parser.parse_args().paid_calls_authorized)
