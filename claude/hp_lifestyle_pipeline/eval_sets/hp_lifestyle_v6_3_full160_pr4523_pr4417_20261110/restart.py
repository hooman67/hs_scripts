#!/usr/bin/env python3
"""Resume untouched work and explicitly replace four interrupted local attempts."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import httpx

import study

HERE = study.HERE
PLAN = HERE / "restart_manifest.json"


def verified_plan():
    if not PLAN.exists():
        return None
    plan = study.load(PLAN)
    if (plan["original_study_sha256"] != study.sha(HERE / "study_manifest.json")
            or plan["source_sha256"] != study.SOURCE_SHA
            or plan["restart_code_sha256"] != study.sha(Path(__file__))):
        raise ValueError("restart lost its frozen study/source/code binding")
    for path, digest in plan["frozen_restart_files"].items():
        if study.sha(path) != digest:
            raise ValueError("restart selection/run identity changed")
    return plan


def events(run_dir):
    path = Path(run_dir) / "journals/events.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def pending_jobs(cell):
    runner = study.image_runner()
    prompts = {p["prompt_key"]: p for p in study.load(study.SOURCE)["prompts"]}
    result = []
    for key in cell["new_row_ids"]:
        paths = runner.paths(Path(cell["run_dir"]), study.row_for(prompts[key]))
        if paths["job"].exists() and not paths["record"].exists():
            result.append((key, paths, study.load(paths["job"])))
    return result


def require_interrupted(status):
    scene = status["stages"]["scene"]
    if (not status["done"] or scene["status"] != "error" or scene["has_image"]
            or scene["error"] != "Endpoint restarted with an incomplete job. No automatic replay; inspect saved call journals."):
        raise ValueError("job is not an explicitly interrupted endpoint attempt; do not retry")


def command(cell, selection=None):
    args = study.command(cell)
    if selection is not None:
        args[args.index("--selection-file") + 1] = str(selection)
    return args


def prepare(endpoint_pid):
    if PLAN.exists():
        raise FileExistsError("restart is already frozen; do not prepare a second attempt")
    manifest = study.verified_manifest()
    if Path("/proc/1112789").exists():
        raise RuntimeError("original worker is still alive")
    endpoint = study.OLD / "endpoint_pr4523"
    if Path(f"/proc/{endpoint_pid}/cwd").resolve() != endpoint:
        raise ValueError("endpoint PID does not belong to this task's exact local service")
    health = httpx.get("http://127.0.0.1:8138/health", timeout=30).json()
    if (health["candidateLineage"]["sourceCommit"] != "d1e5ae5323dedebc3b06ed173a3731307bd0623a"
            or not health["generationEnabled"] or health["maxWorkers"] != 4):
        raise ValueError("restarted service differs from the frozen contract")
    local = next(c for c in manifest["cells"] if c["pr"] == "pr4523")
    remote = next(c for c in manifest["cells"] if c["pr"] == "pr4417")
    for cell in manifest["cells"]:
        study.submission_guard(cell)
    interrupted = pending_jobs(local)
    if len(interrupted) != 4:
        raise ValueError("only the four identified interrupted local jobs are authorized to restart")
    observed = study.load(HERE / "interruption_check_20261110.json")
    expected_ids = {job["job_id"] for job in observed["submitted_unmaterialized_jobs"]
                    if job["cell"] == local["name"]}
    if {job["submit_response"]["jobId"] for _, _, job in interrupted} != expected_ids:
        raise ValueError("the interrupted job identities differ from the user-authorized restart")
    preserved = {}
    abandoned = {}
    for key, paths, job in interrupted:
        job_id = job["submit_response"]["jobId"]
        native = endpoint / "run/jobs" / job_id
        status = study.load(native / "status.json")
        require_interrupted(status)
        abandoned[key] = {"job_id": job_id, "job_path": str(paths["job"]),
                          "job_sha256": study.sha(paths["job"]), "native_directory": str(native)}
        for path in native.rglob("*"):
            if path.is_file():
                preserved[str(path)] = study.sha(path)
    for cell in manifest["cells"]:
        for path in (Path(cell["run_dir"]) / "records").glob("*.json"):
            record = study.load(path)
            if record["status"] != "done":
                raise ValueError("unexpected pre-existing failure; restart scope needs investigation")
            row = {"row_slug": path.stem}
            paths = study.image_runner().paths(Path(cell["run_dir"]), row)
            for name in ("job", "record", "status", "image"):
                preserved[str(paths[name])] = study.sha(paths[name])
    for key, _, job in pending_jobs(remote):
        response = httpx.get(job["status_url"], timeout=30)
        response.raise_for_status()
        if not response.json()["done"]:
            raise ValueError("remote job is still running; preserve and investigate before queue restart")
    prompts = {p["prompt_key"]: p for p in study.load(study.SOURCE)["prompts"]}
    restart_rows = [key for key, _, _ in interrupted]
    directory = HERE / "restart"
    selection = directory / "interrupted_four.json"
    remaining = directory / "original_local_without_interrupted.json"
    for path, keys in (
        (selection, restart_rows),
        (remaining, [key for key in local["new_row_ids"] if key not in abandoned]),
    ):
        study.write(path, {"source_prompts_sha256": study.SOURCE_SHA, "row_ids": keys,
                           "rows": [prompts[key] for key in keys]}, exclusive=True)
    retry = {**local, "name": "v6_3_pr4523_restart4_20261110",
             "run_dir": str(HERE / "runs/v6_3_pr4523_restart4_20261110"),
             "selection_file": str(selection), "new_row_ids": restart_rows}
    study.run(retry, preflight=True)
    original_local = command(local, remaining)
    commands = {"local": [command(retry), original_local], "remote": [command(remote)]}
    frozen = {str(path): study.sha(path) for path in
              (selection, remaining, Path(retry["run_dir"]) / "run_manifest.json")}
    plan = {
        "version": "interrupted-run-restart-v1", "authorized_at_utc": study.now(),
        "authorization": "User: Ok. Restart those jobs",
        "original_study_sha256": study.sha(HERE / "study_manifest.json"),
        "source_sha256": study.SOURCE_SHA, "restart_code_sha256": study.sha(Path(__file__)),
        "original_submission_budget": 260, "additional_interrupted_restarts": 4,
        "maximum_total_new_submissions": 264, "completed_images_to_regenerate": 0,
        "origin_cell": local["name"], "retry_run": retry, "interrupted_attempts": abandoned,
        "commands": commands, "frozen_restart_files": frozen, "preserved_before_restart": preserved,
        "endpoint": {"pid": endpoint_pid, "instance_id": health["instanceId"]},
    }
    study.write(PLAN, plan, exclusive=True)
    study.write(directory / "previous_execution_status.json", study.load(HERE / "execution_status.json"))
    print({"prepared": True, "interrupted_local_restarts": 4, "untouched_new_jobs": 154,
           "existing_remote_jobs_to_retrieve": 4}, flush=True)


def submission_guard(require_terminal=False):
    plan = verified_plan()
    manifest = study.verified_manifest()
    for cell in manifest["cells"]:
        study.submission_guard(cell)
    retry = plan["retry_run"]
    study.submission_guard(retry)
    starts = [event for event in events(retry["run_dir"]) if event["event"] == "submit_started"]
    if len(starts) > 4 or (require_terminal and len(starts) != 4):
        raise ValueError("restart exceeds four explicitly authorized attempts")
    for path, digest in plan["preserved_before_restart"].items():
        if study.sha(path) != digest:
            raise ValueError("previous completed or interrupted evidence was changed")


def run_commands(name, commands):
    for position, args in enumerate(commands):
        log = HERE / "logs" / f"restart_{name}_{position}.log"
        with log.open("a") as out:
            process = subprocess.Popen(args, stdout=out, stderr=subprocess.STDOUT,
                                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
            study.write(HERE / "restart" / f"{name}_worker.json",
                        {"pid": process.pid, "command": args, "started_at_utc": study.now()})
            code = process.wait()
        if code:
            raise subprocess.CalledProcessError(code, args)


def generate():
    import report

    plan = verified_plan()
    lock = HERE / "restart.lock"
    with lock.open("x") as handle:
        handle.write(str(os.getpid()))
    submission_guard()
    old_lock = HERE / "generation.lock"
    if old_lock.exists():
        if old_lock.read_text() != "1112789" or Path("/proc/1112789").exists():
            raise RuntimeError("original generation lock is not safely abandoned")
        old_lock.rename(HERE / "restart/generation.lock.interrupted_1112789")
    state = {"status": "running", "pid": os.getpid(), "started_at_utc": study.now(),
             "restart_manifest_sha256": study.sha(PLAN)}
    study.write(HERE / "execution_status.json", state)
    previous_published = -1
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = {name: pool.submit(run_commands, name, commands)
                       for name, commands in plan["commands"].items()}
            while True:
                counts = report.completion_counts()
                done = sum(cell["done"] for cell in counts.values())
                study.write(HERE / "restart_status.json", {**state, "updated_at_utc": study.now(), "cells": counts})
                print(json.dumps({"at_utc": study.now(), "cells": counts}), flush=True)
                if previous_published < 0 or done - previous_published >= 24 or all(f.done() for f in futures.values()):
                    report.collect_inputs()
                    report.build()
                    report.publish()
                    previous_published = done
                if all(f.done() for f in futures.values()):
                    for future in futures.values():
                        future.result()
                    break
                time.sleep(30)
        submission_guard(require_terminal=True)
        report.collect_inputs()
        report.build()
        report.publish()
        report.final_audit()
        browser_log = HERE / "restart/browser.log"
        with browser_log.open("w") as out:
            subprocess.run(["uv", "run", "--no-project", "--with", "playwright",
                            sys.executable, str(HERE / "check_browser.py")],
                           stdout=out, stderr=subprocess.STDOUT, check=True)
        study.write(HERE / "execution_status.json", {
            **state, "status": "complete", "finished_at_utc": study.now(), "cells": report.completion_counts(),
        })
        health = httpx.get("http://127.0.0.1:8138/health", timeout=30).json()
        if health["instanceId"] != plan["endpoint"]["instance_id"]:
            raise RuntimeError("local endpoint ownership changed; do not stop it")
        os.kill(plan["endpoint"]["pid"], signal.SIGTERM)
    except BaseException as error:
        study.write(HERE / "execution_status.json", {
            **state, "status": "interrupted" if isinstance(error, KeyboardInterrupt) else "failed",
            "updated_at_utc": study.now(), "error": f"{type(error).__name__}: {error}",
            "cells": report.completion_counts(),
        })
        raise
    finally:
        lock.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "generate", "status"))
    parser.add_argument("--endpoint-pid", type=int)
    args = parser.parse_args()
    if args.command == "prepare":
        if args.endpoint_pid is None:
            parser.error("--endpoint-pid is required")
        prepare(args.endpoint_pid)
    elif args.command == "generate":
        generate()
    else:
        import report

        print(json.dumps(report.completion_counts(), indent=2))
