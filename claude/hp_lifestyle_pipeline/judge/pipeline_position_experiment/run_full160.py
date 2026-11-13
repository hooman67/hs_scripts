#!/usr/bin/env python3
"""Resumable serial submission of the frozen V6.1 160 rows to the local API."""

import json
import hashlib
import time
import urllib.request
from pathlib import Path

BASE = "http://127.0.0.1:8126"
RECORDS = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/"
    "hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/"
    "generation_gpt_image2_scene_v1/run/records"
)
PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment")
PROGRESS = PROJECT / "full160/progress.json"
PROMPTS = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/"
    "hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/revisions/"
    "v6.1-expanded-20261103-r6/exports/final/prompts_all_160.json"
)
PROMPTS_SHA256 = "adcb9edb2643e45acb0cb882cdc4d65b8c256a52d58ad4a44ddd9c235287b3cd"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def request(method: str, path: str, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read())


def save(value):
    PROGRESS.parent.mkdir(parents=True, exist_ok=True)
    tmp = PROGRESS.with_suffix(".tmp")
    tmp.write_text(json.dumps(value, indent=2))
    tmp.replace(PROGRESS)


def main():
    health = request("GET", "/health")
    records = [json.loads(path.read_text()) for path in sorted(RECORDS.glob("*.json"))]
    if len(records) != 160:
        raise RuntimeError(f"Expected 160 frozen records; found {len(records)}")
    if sha256(PROMPTS) != PROMPTS_SHA256:
        raise RuntimeError("Frozen V6.1 prompt export hash changed")
    export = json.loads(PROMPTS.read_text())
    prompts = {row["prompt_key"]: row for row in export["prompts"]}
    if len(prompts) != 160:
        raise RuntimeError(f"Expected 160 exported prompts; found {len(prompts)}")
    for record in records:
        key = record["row_id"]
        if key not in prompts or prompts[key]["text"] != record["prompt"]:
            raise RuntimeError(f"Frozen record/export mismatch: {key}")
    progress = json.loads(PROGRESS.read_text()) if PROGRESS.exists() else {
        "schema_version": 1, "health": health, "promptExport": str(PROMPTS),
        "promptExportSha256": PROMPTS_SHA256, "done": [], "errors": {},
        "total": len(records)
    }
    if progress.get("promptExportSha256") != PROMPTS_SHA256:
        raise RuntimeError("Existing progress belongs to a different prompt export")
    done = set(progress["done"])
    for index, record in enumerate(records, 1):
        slug = record["row_slug"]
        if slug in done:
            continue
        response = request("POST", "/api/generate", {"rowSlug": slug})
        while True:
            status = request("GET", response["statusUrl"])
            if status.get("done"):
                break
            time.sleep(5)
        if status["stage"] != "done":
            progress["errors"][slug] = status["error"]
            save(progress)
            raise RuntimeError(f"{slug}: {status['error']}")
        done.add(slug)
        progress["done"] = sorted(done)
        progress["last"] = slug
        save(progress)
        print(json.dumps({"completed": len(done), "total": len(records), "slug": slug}), flush=True)
    print(json.dumps({"complete": len(done), "total": len(records)}), flush=True)


if __name__ == "__main__":
    main()
