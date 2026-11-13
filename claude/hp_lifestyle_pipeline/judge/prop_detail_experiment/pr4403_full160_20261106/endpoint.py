#!/usr/bin/env python3
"""Serial local API for the exact PR 4403 Stage-B dynamic-prop treatment."""

from __future__ import annotations

import base64
import io
import json
import shutil
import sys
import threading
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import foundry_aws_gateway.llm
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from common import atomic_json, require, sha256_bytes, sha256_file, sha256_json
from config import INPUT_ROOT, JOB_ROOT, PACKAGE, PIPELINE_ROOT, PIPELINE_VERSION, PR_COMMIT, RECORDS, REMOTE_CONTROL, SOURCE_HASHES
from preflight import verify

sys.path.insert(0, str(PACKAGE))
import hp3p.pipeline as pipeline  # noqa: E402
from hp3p.catalog import StyleRef  # noqa: E402
from hp3p.evalset import Row  # noqa: E402
from hp3p.openai_client import IMAGE_MODEL, TEXT_MODEL  # noqa: E402

verify()
require(pipeline.PIPELINE_VERSION == PIPELINE_VERSION, "imported pipeline version differs from freeze")
INPUT_ROOT.mkdir(parents=True, exist_ok=True)
JOB_ROOT.mkdir(parents=True, exist_ok=True)
PIPELINE_ROOT.mkdir(parents=True, exist_ok=True)
_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="hp-pr4403-props")
_pipeline_lock = threading.Lock()
_instance_id = str(uuid.uuid4())


class AuditClient:
    def __init__(self, debug: dict, expected_guide: bytes):
        self.debug = debug
        self.expected_guide = expected_guide
        self.client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=0, timeout=600.0)
        self.calls: list[dict] = []

    def chat_json(self, system: str, text: str, images: list[tuple[str, bytes]], schema: dict) -> dict:
        fields = set(schema["properties"])
        if fields == {"tone", "content", "rationale"}:
            value = dict(self.debug["selection"])
            self.calls.append({"kind": "selection_replay", "response_sha256": sha256_json(value)})
            return value
        if "geometry" in fields:
            value = dict(self.debug["geometryResponse"])
            self.calls.append({"kind": "geometry_replay", "response_sha256": sha256_json(value)})
            return value
        require(fields == {"layout", "camera", "composition", "prompt", "prop_details"}, f"unexpected schema: {sorted(fields)}")
        require(images and images[0][1] == self.expected_guide, "Stage B did not receive frozen guide")
        content = [{"type": "text", "text": text}] + [
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{base64.b64encode(data).decode()}", "detail": "high"}}
            for mime, data in images
        ]
        response = self.client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[{"role": "developer", "content": system}, {"role": "user", "content": content}],
            response_format={"type": "json_schema", "json_schema": {"name": "result", "strict": True, "schema": schema}},
            max_completion_tokens=16384,
            store=False,
        )
        choice = response.choices[0]
        require(choice.finish_reason == "stop" and bool(choice.message.content), f"Astra incomplete: {choice.finish_reason}")
        value = json.loads(choice.message.content)
        self.calls.append({
            "kind": "astra_write", "model": response.model, "finish_reason": choice.finish_reason,
            "system_sha256": sha256_bytes(system.encode()), "text_sha256": sha256_bytes(text.encode()),
            "images_sha256": [sha256_bytes(data) for _, data in images], "schema_sha256": sha256_json(schema),
            "response_sha256": sha256_json(value), "usage": getattr(response.usage, "model_dump", lambda: {})(),
        })
        return value

    def edit_image(self, prompt: str, images: list[tuple[str, bytes]], size: str, mask: bytes | None = None) -> bytes:
        require(mask is None and len(images) == 1 and images[0][1] == self.expected_guide, "image call must use frozen guide only")
        files = [(f"image{i}.{mime.split('/')[1]}", io.BytesIO(data), mime) for i, (mime, data) in enumerate(images, 1)]
        response = self.client.images.edit(
            model=IMAGE_MODEL, image=files, prompt=prompt, n=1, size=size,
            quality="high", output_format="png", background="opaque",
        )
        output = base64.b64decode(response.data[0].b64_json)
        self.calls.append({
            "kind": "image_edit", "model": IMAGE_MODEL, "size": size,
            "prompt_sha256": sha256_bytes(prompt.encode()), "guide_sha256": sha256_bytes(images[0][1]),
            "output_sha256": sha256_bytes(output), "mask": False,
        })
        return output


def _record(slug: str) -> dict:
    path = RECORDS / f"{slug}.json"
    if not path.is_file():
        raise KeyError(slug)
    return json.loads(path.read_text())


def _inputs(record: dict) -> Path:
    destination = INPUT_ROOT / record["row_slug"]
    destination.mkdir(parents=True, exist_ok=True)
    for local, remote in {"product.png": "hp16_product.png", "reference.png": "hp16_reference.png", "guide.png": "hp16_geometry_guide.png"}.items():
        path = destination / local
        if not path.is_file():
            temporary = path.with_suffix(path.suffix + f".{uuid.uuid4().hex}.tmp")
            url = f"{REMOTE_CONTROL}/api/jobs/{record['job_id']}/artifacts/{remote}"
            with urllib.request.urlopen(url, timeout=180) as response:
                temporary.write_bytes(response.read())
            temporary.replace(path)
    return destination


def _status_path(slug: str) -> Path:
    return JOB_ROOT / slug / "status.json"


def _status(slug: str) -> dict | None:
    path = _status_path(slug)
    return json.loads(path.read_text()) if path.is_file() else None


def _write_status(slug: str, value: dict) -> None:
    atomic_json(_status_path(slug), value)


def _execute(slug: str) -> None:
    record = _record(slug)
    job_dir = JOB_ROOT / slug
    row_dir = PIPELINE_ROOT / "rows" / slug
    _write_status(slug, {"jobId": slug, "rowSlug": slug, "done": False, "stage": "running", "instanceId": _instance_id, "error": None})
    try:
        inputs = _inputs(record)
        debug = record["scene_debug"]
        guide = (inputs / "guide.png").read_bytes()
        hero = (inputs / "product.png").read_bytes()
        reference = (inputs / "reference.png").read_bytes()
        meta = debug["reference"]
        style_ref = StyleRef(meta["id"], meta["name"], meta["tone"], meta["content"], "image/png", reference)
        row = Row(slug, record["prompt"], "frozen-v6.1-control-input", 2368, 1776, [])
        client = AuditClient(debug, guide)
        original = pipeline.build_guide

        def frozen_guide(_hero, _mask, geometry, camera):
            require(geometry == debug["geometryResponse"]["geometry"], "geometry replay differed")
            require(camera == debug["twinCamera"], "camera replay differed")
            return guide, dict(debug["guideInfo"])

        with _pipeline_lock:
            pipeline.build_guide = frozen_guide
            try:
                result = pipeline.run_row(row, client, [style_ref], PIPELINE_ROOT, hero, ref_count=1, size=(2368, 1776), camera=debug["twinCamera"])
            finally:
                pipeline.build_guide = original
        job_dir.mkdir(parents=True, exist_ok=True)
        atomic_json(job_dir / "calls.json", client.calls)
        require(result.get("status") == "ok", result.get("error") or "pipeline failed")
        for source, target in (
            (row_dir / "ours.png", job_dir / "output.png"),
            (row_dir / "geometry_guide.png", job_dir / "guide.png"),
            (row_dir / "result.json", job_dir / "result.json"),
            (row_dir / "prop_details.json", job_dir / "prop_details.json"),
        ):
            shutil.copy2(source, target)
        require((job_dir / "guide.png").read_bytes() == guide, "persisted guide changed")
        _write_status(slug, {
            "jobId": slug, "rowSlug": slug, "done": True, "stage": "done", "error": None,
            "instanceId": _instance_id, "prCommit": PR_COMMIT, "pipelineVersion": result["pipeline_version"],
            "imageCalls": result["image_calls"], "propDetailCount": len(result.get("prop_details", [])),
            "outputSha256": sha256_file(job_dir / "output.png"), "sourceHashes": SOURCE_HASHES,
        })
    except Exception as error:
        _write_status(slug, {"jobId": slug, "rowSlug": slug, "done": True, "stage": "error", "instanceId": _instance_id, "error": f"{type(error).__name__}: {error}"[:2000]})


class GenerateRequest(BaseModel):
    rowSlug: str


app = FastAPI(title="HP PR4403 dynamic-prop experiment", version="1")


@app.get("/health")
def health():
    return {"ok": True, "prCommit": PR_COMMIT, "pipelineVersion": PIPELINE_VERSION, "records": len(list(RECORDS.glob("*.json"))), "instanceId": _instance_id}


@app.post("/api/generate")
def generate(request: GenerateRequest):
    try:
        _record(request.rowSlug)
    except KeyError:
        raise HTTPException(404, "unknown frozen V6.1 row") from None
    existing = _status(request.rowSlug)
    if existing and existing.get("stage") == "done":
        return {"jobId": request.rowSlug, "statusUrl": f"/api/jobs/{request.rowSlug}"}
    if existing and existing.get("stage") in {"queued", "running"} and existing.get("instanceId") == _instance_id:
        return {"jobId": request.rowSlug, "statusUrl": f"/api/jobs/{request.rowSlug}"}
    _write_status(request.rowSlug, {"jobId": request.rowSlug, "rowSlug": request.rowSlug, "done": False, "stage": "queued", "instanceId": _instance_id, "error": None})
    _executor.submit(_execute, request.rowSlug)
    return {"jobId": request.rowSlug, "statusUrl": f"/api/jobs/{request.rowSlug}"}


@app.get("/api/jobs/{job_id}")
def status(job_id: str):
    value = _status(job_id)
    if value is None:
        raise HTTPException(404, "unknown job")
    return value


@app.get("/api/jobs/{job_id}/artifacts/{filename}")
def artifact(job_id: str, filename: str):
    if filename not in {"output.png", "guide.png", "result.json", "prop_details.json", "calls.json"}:
        raise HTTPException(404, "unknown artifact")
    path = JOB_ROOT / job_id / filename
    if not path.is_file():
        raise HTTPException(404, "artifact not ready")
    return FileResponse(path)
