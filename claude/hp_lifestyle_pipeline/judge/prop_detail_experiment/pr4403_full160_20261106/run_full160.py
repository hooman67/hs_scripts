#!/usr/bin/env python3
"""Resumable serial V6.1 runner with Latin-square device/view interleaving."""

from __future__ import annotations

import json
import subprocess
import time
import urllib.request

from common import atomic_json, sha256_file
from config import DEVICE_ORDER, LOCAL_ENDPOINT, LOG_ROOT, PR_COMMIT, PROGRESS, PROMPTS, PROMPTS_SHA256, RECORDS, VIEW_ORDER


def request(method: str, path: str, body=None):
    data = json.dumps(body).encode() if body is not None else None
    message = urllib.request.Request(LOCAL_ENDPOINT + path, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(message, timeout=60) as response:
        return json.loads(response.read())


def load_rows() -> list[dict]:
    if sha256_file(PROMPTS) != PROMPTS_SHA256:
        raise RuntimeError("frozen prompt export changed")
    exported = {item["prompt_key"]: item for item in json.loads(PROMPTS.read_text())["prompts"]}
    rows = []
    for path in RECORDS.glob("*.json"):
        record = json.loads(path.read_text())
        if exported.get(record["row_id"], {}).get("text") != record["prompt"]:
            raise RuntimeError(f"record/export mismatch: {record['row_id']}")
        rows.append(record)
    if len(rows) != 160:
        raise RuntimeError(f"expected 160 rows, found {len(rows)}")
    by_key = {(row["device_id"], row["camera_id"], int(row["bank_rank"])): row for row in rows}
    ordered = []
    for rank in range(1, 11):
        for wave in range(4):
            for device_index, device in enumerate(DEVICE_ORDER):
                camera = VIEW_ORDER[device][(wave + device_index) % 4]
                ordered.append(by_key[(device, camera, rank)])
    if len(ordered) != 160 or len({row["row_slug"] for row in ordered}) != 160:
        raise RuntimeError("interleaved queue is incomplete")
    return ordered


def publish() -> None:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(["python", "build_live_report.py", "--upload"], capture_output=True, text=True)
    (LOG_ROOT / "last_publish.stdout.log").write_text(result.stdout)
    (LOG_ROOT / "last_publish.stderr.log").write_text(result.stderr)
    if result.returncode:
        (LOG_ROOT / "publish_failures.log").open("a").write(f"{time.time()}\n{result.stderr}\n")


def main() -> None:
    health = request("GET", "/health")
    if health.get("prCommit") != PR_COMMIT:
        raise RuntimeError(f"wrong endpoint commit: {health}")
    rows = load_rows()
    progress = json.loads(PROGRESS.read_text()) if PROGRESS.is_file() else {
        "schema_version": 1, "experiment": "PR4403 dynamic prop details on frozen V6.1 controls",
        "health": health, "prompt_export": str(PROMPTS), "prompt_export_sha256": PROMPTS_SHA256,
        "queue": [row["row_slug"] for row in rows], "done": [], "errors": {}, "total": 160,
    }
    if progress.get("health", {}).get("prCommit") != PR_COMMIT:
        raise RuntimeError("existing progress belongs to a different commit")
    done = set(progress["done"])
    for row in rows:
        slug = row["row_slug"]
        if slug in done:
            continue
        submitted = request("POST", "/api/generate", {"rowSlug": slug})
        while True:
            status = request("GET", submitted["statusUrl"])
            if status.get("done"):
                break
            time.sleep(5)
        if status.get("stage") != "done":
            progress["errors"][slug] = status.get("error")
            progress["last"] = slug
            atomic_json(PROGRESS, progress)
            publish()
            raise RuntimeError(f"{slug}: {status.get('error')}")
        done.add(slug)
        progress["done"] = [item for item in progress["queue"] if item in done]
        progress["last"] = slug
        progress["completed"] = len(done)
        atomic_json(PROGRESS, progress)
        print(json.dumps({"completed": len(done), "total": 160, "slug": slug}), flush=True)
        if len(done) <= 4 or len(done) % 4 == 0:
            publish()
    progress["complete"] = True
    atomic_json(PROGRESS, progress)
    publish()


if __name__ == "__main__":
    main()
