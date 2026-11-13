#!/usr/bin/env python3
"""Thin local job API over the exact isolated PR4349 ``hp3p.pipeline.run_row``.

This is not the unavailable deployed UI wrapper. It is an experiment adapter that
freezes each V6.1 control's selection, Stage-A geometry and guide, then executes the
accepted PR4349 Stage-B/final translation-only prompt policy and one image call.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import threading
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from run_smoke import FrozenInputsClient, PACKAGE, PR_COMMIT, WORKTREE

from hp3p.catalog import StyleRef
from hp3p.evalset import Row
import hp3p.pipeline as pipeline

PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment")
RECORDS = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/"
    "hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/"
    "generation_gpt_image2_scene_v1/run/records"
)
RUN_ROOT = PROJECT / "full160/run"
INPUT_ROOT = PROJECT / "full160/inputs"
SMOKE_ROOT = PROJECT / "smoke/treatment"
REMOTE = "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev"
PINNED_HASHES = {
    "hp3p/prompts/system_3p.txt": "a401c604d284ec5a59d82f992e234821defee23eed01a289d8e79166fa40aa25",
    "hp3p/pipeline.py": "655dd194f6a4318edc897192191cd39044e9347a62ac4aa437131c5eebc00c45",
    "hp3p/geometry.py": "d97d0a2c2b739d6659b16dc68b2558697ae23432abdf869d1a12acb41a9479a7",
    "hp3p/grade.py": "22169e7fc7fe3ebfd561bb3edd04edf4f1c630752444b752d388305c35bafbf6",
    "hp3p/reference_blue.py": "f3c1a81c66b3c47c6734666343ed0273f6dad2f6610f5b47c523e8481baaeabe",
}

RUN_ROOT.mkdir(parents=True, exist_ok=True)
INPUT_ROOT.mkdir(parents=True, exist_ok=True)
_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="hp-position")
_pipeline_lock = threading.Lock()
_instance_id = str(uuid.uuid4())


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _verify_source() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=WORKTREE, text=True).strip()
    if commit != PR_COMMIT:
        raise RuntimeError(f"Foundry worktree moved from PR4349 head: {commit}")
    actual = {name: _sha(PACKAGE / name) for name in PINNED_HASHES}
    if actual != PINNED_HASHES:
        raise RuntimeError(f"Prompt source hash mismatch: {actual}")


_verify_source()


def _record(slug: str) -> dict:
    path = RECORDS / f"{slug}.json"
    if not path.exists():
        raise KeyError(slug)
    return json.loads(path.read_text())


def _download_inputs(record: dict) -> Path:
    slug = record["row_slug"]
    dest = INPUT_ROOT / slug
    dest.mkdir(parents=True, exist_ok=True)
    files = {
        "product.png": "hp16_product.png",
        "reference.png": "hp16_reference.png",
        "guide.png": "hp16_geometry_guide.png",
    }
    for local, remote in files.items():
        path = dest / local
        if not path.exists():
            url = f"{REMOTE}/api/jobs/{record['job_id']}/artifacts/{remote}"
            tmp = path.with_suffix(path.suffix + ".tmp")
            with urllib.request.urlopen(url, timeout=180) as response:
                tmp.write_bytes(response.read())
            tmp.replace(path)
    return dest


def _status_path(slug: str) -> Path:
    return RUN_ROOT / "jobs" / slug / "status.json"


def _write_status(slug: str, value: dict) -> None:
    path = _status_path(slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(value, indent=2))
    tmp.replace(path)


def _read_status(slug: str) -> dict | None:
    path = _status_path(slug)
    return json.loads(path.read_text()) if path.exists() else None


def _job_id(slug: str, cached_smoke: bool) -> str:
    return f"smoke-cache--{slug}" if cached_smoke else slug


def _execute(slug: str, cached_smoke: bool, job_id: str) -> None:
    record = _record(slug)
    _write_status(job_id, {"jobId": job_id, "rowSlug": slug, "done": False,
                           "stage": "running", "error": None, "instanceId": _instance_id})
    try:
        inputs = _download_inputs(record)
        debug = record["scene_debug"]
        guide = (inputs / "guide.png").read_bytes()
        hero = (inputs / "product.png").read_bytes()
        reference = (inputs / "reference.png").read_bytes()
        ref_meta = debug["reference"]
        ref = StyleRef(ref_meta["id"], ref_meta["name"], ref_meta["tone"], ref_meta["content"],
                       "image/png", reference)
        row = Row(slug, record["prompt"], "frozen-endpoint-artifact", 2368, 1776, [])
        client = FrozenInputsClient(debug, guide, RUN_ROOT / "jobs" / job_id)
        run_dir = SMOKE_ROOT / slug / "run" if cached_smoke else RUN_ROOT / "pipeline"
        original_builder = pipeline.build_guide

        def frozen_guide(_hero, _mask, geometry, camera):
            if geometry != debug["geometryResponse"]["geometry"] or camera != debug["twinCamera"]:
                raise RuntimeError("Frozen guide received different geometry or camera")
            return guide, dict(debug["guideInfo"])

        with _pipeline_lock:
            pipeline.build_guide = frozen_guide
            try:
                result = pipeline.run_row(row, client, [ref], run_dir, hero, ref_count=1,
                                          size=(2368, 1776), camera=debug["twinCamera"])
            finally:
                pipeline.build_guide = original_builder
        job_dir = RUN_ROOT / "jobs" / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        row_dir = run_dir / "rows" / slug
        (job_dir / "calls.json").write_text(json.dumps(client.calls, indent=2))
        if result["status"] != "ok":
            raise RuntimeError(result["error"])
        for source, name in ((row_dir / "ours.png", "output.png"),
                             (row_dir / "geometry_guide.png", "guide.png"),
                             (row_dir / "result.json", "result.json")):
            if source.resolve() != (job_dir / name).resolve():
                shutil.copy2(source, job_dir / name)
        if (job_dir / "guide.png").read_bytes() != guide:
            raise RuntimeError("Persisted guide is not byte-identical to frozen control")
        _write_status(job_id, {
            "jobId": job_id,
            "rowSlug": slug,
            "done": True,
            "stage": "done",
            "error": None,
            "cachedSmoke": cached_smoke,
            "pipelineVersion": result["pipeline_version"],
            "imageCalls": result["image_calls"],
            "outputUrl": f"/api/jobs/{job_id}/artifacts/output.png",
            "resultUrl": f"/api/jobs/{job_id}/artifacts/result.json",
            "sourceHashes": PINNED_HASHES,
            "instanceId": _instance_id,
        })
    except Exception as error:
        _write_status(job_id, {"jobId": job_id, "rowSlug": slug, "done": True,
                               "stage": "error", "instanceId": _instance_id,
                               "error": f"{type(error).__name__}: {error}"[:1000]})


class GenerateRequest(BaseModel):
    rowSlug: str
    cachedSmoke: bool = False


app = FastAPI(title="HP PR4349 translation-only experiment", version="1")


@app.get("/health")
def health():
    return {"ok": True, "prCommit": PR_COMMIT, "pipelineVersion": pipeline.PIPELINE_VERSION,
            "sourceHashes": PINNED_HASHES, "records": len(list(RECORDS.glob("*.json"))),
            "instanceId": _instance_id}


@app.post("/api/generate")
def generate(request: GenerateRequest):
    try:
        _record(request.rowSlug)
    except KeyError:
        raise HTTPException(404, "Unknown frozen V6.1 row") from None
    if request.cachedSmoke and request.rowSlug not in {
        "cashmere__laptop_FrontCloseUp__p1", "cashmere__laptop_FrontWide__p1",
        "magic__printer_FrontCloseUp__p1", "magic__printer_FrontWide__p1",
    }:
        raise HTTPException(400, "cachedSmoke is restricted to the frozen smoke fixtures")
    job_id = _job_id(request.rowSlug, request.cachedSmoke)
    existing = _read_status(job_id)
    if existing and existing.get("stage") == "done":
        return {"jobId": job_id, "statusUrl": f"/api/jobs/{job_id}"}
    if (existing and existing.get("stage") in {"queued", "running"}
            and existing.get("instanceId") == _instance_id):
        return {"jobId": job_id, "statusUrl": f"/api/jobs/{job_id}"}
    _write_status(job_id, {"jobId": job_id, "rowSlug": request.rowSlug, "done": False,
                           "stage": "queued", "error": None, "instanceId": _instance_id})
    _executor.submit(_execute, request.rowSlug, request.cachedSmoke, job_id)
    return {"jobId": job_id, "statusUrl": f"/api/jobs/{job_id}"}


@app.get("/api/jobs/{job_id}")
def status(job_id: str):
    value = _read_status(job_id)
    if value is None:
        raise HTTPException(404, "Unknown job")
    return value


@app.get("/api/jobs/{job_id}/artifacts/{filename}")
def artifact(job_id: str, filename: str):
    if filename not in {"output.png", "guide.png", "result.json", "calls.json"}:
        raise HTTPException(404, "Unknown artifact")
    path = RUN_ROOT / "jobs" / job_id / filename
    if not path.exists():
        raise HTTPException(404, "Artifact not ready")
    return FileResponse(path)
