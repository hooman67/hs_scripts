#!/usr/bin/env python3
"""Isolated serial API for the frozen V22.3.3 full-160 treatment.

Selection, Stage-A geometry, and the rendered guide are replayed from each
original V6.1 record. Stage B and image generation are live. Every Stage-B
attempt, image attempt, affine-guard outcome, and selected artifact is retained
under this experiment's isolated run root.
"""

from __future__ import annotations

import base64
import io
import json
import shutil
import threading
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import foundry_aws_gateway.llm
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from common import atomic_json, load_json, require, sha256_bytes, sha256_file, sha256_json
from config import (
    FREEZE,
    INPUT_ROOT,
    JOB_ROOT,
    PACKAGE,
    PIPELINE_ROOT,
    PIPELINE_VERSION,
    RECORDS,
    REMOTE_CONTROL_ENDPOINT,
    SOURCE_HASHES,
)
from preflight import verify as verify_preflight

import sys

sys.path.insert(0, str(PACKAGE))

from hp3p.catalog import StyleRef  # noqa: E402
from hp3p.evalset import Row  # noqa: E402
from hp3p.openai_client import IMAGE_MODEL, TEXT_MODEL  # noqa: E402
import hp3p.pipeline as pipeline  # noqa: E402


verify_preflight(allow_progress=True)
require(pipeline.PIPELINE_VERSION == PIPELINE_VERSION, "imported pipeline version differs from freeze")
_freeze = load_json(FREEZE)
_frozen_record = {item["row_slug"]: item for item in _freeze["records"]}

INPUT_ROOT.mkdir(parents=True, exist_ok=True)
JOB_ROOT.mkdir(parents=True, exist_ok=True)
PIPELINE_ROOT.mkdir(parents=True, exist_ok=True)
_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="hp-v2233-full160")
_pipeline_lock = threading.Lock()
_instance_id = str(uuid.uuid4())


class AuditClient:
    """Replay frozen upstream calls and audit every live Stage-B/image call."""

    def __init__(self, debug: dict, expected_guide: bytes):
        self.debug = debug
        self.expected_guide = expected_guide
        self.client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=0, timeout=600.0)
        self.calls: list[dict] = []

    def chat_json(self, system: str, text: str, images: list[tuple[str, bytes]], schema: dict) -> dict:
        fields = set(schema["properties"])
        if fields == {"tone", "content", "rationale"}:
            self.calls.append({"kind": "selection_replay", "response_sha256": sha256_json(self.debug["selection"])})
            return dict(self.debug["selection"])
        if "geometry" in fields:
            self.calls.append({"kind": "geometry_replay", "response_sha256": sha256_json(self.debug["geometryResponse"])})
            return dict(self.debug["geometryResponse"])
        require(fields == {"layout", "camera", "composition", "prompt"}, f"unexpected schema fields: {sorted(fields)}")
        require(bool(images) and images[0][1] == self.expected_guide, "Stage B did not receive the frozen guide")
        content = [{"type": "text", "text": text}] + [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime};base64,{base64.b64encode(data).decode()}",
                    "detail": "high",
                },
            }
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
        parsed = json.loads(choice.message.content)
        self.calls.append(
            {
                "kind": "astra_write",
                "attempt": 1 + sum(call["kind"] == "astra_write" for call in self.calls),
                "model": response.model,
                "finish_reason": choice.finish_reason,
                "system_sha256": sha256_bytes(system.encode()),
                "text_sha256": sha256_bytes(text.encode()),
                "images_sha256": [sha256_bytes(data) for _, data in images],
                "schema_sha256": sha256_json(schema),
                "response_sha256": sha256_json(parsed),
                "usage": getattr(response.usage, "model_dump", lambda: {})(),
            }
        )
        return parsed

    def edit_image(
        self,
        prompt: str,
        images: list[tuple[str, bytes]],
        size: str,
        mask: bytes | None = None,
    ) -> bytes:
        require(mask is None and len(images) == 1 and images[0][1] == self.expected_guide, "image call must use only the frozen guide and no mask")
        files = [
            (f"image{i}.{mime.split('/')[1]}", io.BytesIO(data), mime)
            for i, (mime, data) in enumerate(images, 1)
        ]
        response = self.client.images.edit(
            model=IMAGE_MODEL,
            image=files,
            prompt=prompt,
            n=1,
            size=size,
            quality="high",
            output_format="png",
            background="opaque",
        )
        output = base64.b64decode(response.data[0].b64_json)
        self.calls.append(
            {
                "kind": "image_edit",
                "attempt": 1 + sum(call["kind"] == "image_edit" for call in self.calls),
                "model": IMAGE_MODEL,
                "size": size,
                "prompt_sha256": sha256_bytes(prompt.encode()),
                "guide_sha256": sha256_bytes(images[0][1]),
                "mask": False,
                "output_sha256": sha256_bytes(output),
            }
        )
        return output


def _record(slug: str) -> tuple[dict, Path]:
    frozen = _frozen_record.get(slug)
    if frozen is None:
        raise KeyError(slug)
    path = Path(frozen["path"])
    require(path.parent == RECORDS, f"record is outside frozen record root: {path}")
    require(sha256_file(path) == frozen["sha256"], f"record changed: {slug}")
    record = load_json(path)
    require(record["prompt_sha256"] == frozen["prompt_sha256"], f"prompt hash changed: {slug}")
    return record, path


def _download_inputs(record: dict) -> tuple[Path, dict]:
    slug = record["row_slug"]
    dest = INPUT_ROOT / slug
    dest.mkdir(parents=True, exist_ok=True)
    files = {
        "product.png": "hp16_product.png",
        "reference.png": "hp16_reference.png",
        "guide.png": "hp16_geometry_guide.png",
    }
    provenance_path = dest / "input_provenance.json"
    frozen_provenance = load_json(provenance_path) if provenance_path.exists() else None
    provenance = {}
    for local_name, remote_name in files.items():
        path = dest / local_name
        url = f"{REMOTE_CONTROL_ENDPOINT}/api/jobs/{record['job_id']}/artifacts/{remote_name}"
        if not path.exists():
            temp = path.with_name(path.name + f".tmp.{uuid.uuid4().hex}")
            with urllib.request.urlopen(url, timeout=180) as response:
                temp.write_bytes(response.read())
            temp.replace(path)
        entry = {"path": str(path), "sha256": sha256_file(path), "source_url": url}
        if frozen_provenance is not None:
            require(
                frozen_provenance.get(local_name) == entry,
                f"cached frozen input changed for {slug}/{local_name}",
            )
        provenance[local_name] = entry
    if frozen_provenance is None:
        atomic_json(provenance_path, provenance)
    return dest, provenance


def _status_path(slug: str) -> Path:
    return JOB_ROOT / slug / "status.json"


def _write_status(slug: str, value: dict) -> None:
    atomic_json(_status_path(slug), value)


def _read_status(slug: str) -> dict | None:
    path = _status_path(slug)
    return load_json(path) if path.exists() else None


def _artifact_manifest(row_dir: Path, result: dict) -> dict:
    names = [
        "result.json",
        "ours.png",
        "geometry_guide.png",
        "geometry_request.json",
        "geometry_response.json",
        "planning_request.json",
        "planning_response.json",
        "stage_b_attempt_2_raw_response.json",
    ]
    for attempt in (1, 2):
        names.extend(
            [
                f"stage_b_attempt_{attempt}_request.json",
                f"stage_b_attempt_{attempt}_response.json",
                f"gpt_{attempt}.png",
                f"image_request_attempt_{attempt}.json",
                f"product_invariant_attempt_{attempt}.json",
            ]
        )
    artifacts = {}
    for name in names:
        path = row_dir / name
        if path.is_file():
            artifacts[name] = {"path": str(path), "sha256": sha256_file(path), "bytes": path.stat().st_size}
    image_calls = int(result["image_calls"])
    stage_b = result.get("stage_b_attempts") or []
    guard = result.get("product_invariant_guard") or {}
    guard_attempts = guard.get("attempts") or []
    require(image_calls in (1, 2), f"unexpected image call count: {image_calls}")
    require(len(stage_b) in (1, 2), f"unexpected Stage-B attempt count: {len(stage_b)}")
    for attempt in range(1, len(stage_b) + 1):
        require(f"stage_b_attempt_{attempt}_request.json" in artifacts, f"missing Stage-B request {attempt}")
        require(f"stage_b_attempt_{attempt}_response.json" in artifacts, f"missing Stage-B response {attempt}")
    require(len(guard_attempts) == image_calls, "guard attempt count does not equal image attempt count")
    selected = guard.get("selected_attempt")
    require(selected in (1, 2) and selected <= image_calls, "guard did not select a valid attempt")
    require(guard_attempts[selected - 1].get("verdict") == "pass", "selected image attempt did not pass guard")
    for attempt in range(1, image_calls + 1):
        require(f"gpt_{attempt}.png" in artifacts, f"missing image attempt {attempt}")
        require(f"image_request_attempt_{attempt}.json" in artifacts, f"missing image request {attempt}")
        require(f"product_invariant_attempt_{attempt}.json" in artifacts, f"missing guard metrics {attempt}")
    require("ours.png" in artifacts and "result.json" in artifacts, "selected output/result missing")
    selected_sha = artifacts[f"gpt_{selected}.png"]["sha256"]
    require(artifacts["ours.png"]["sha256"] == selected_sha, "ours.png differs from guard-selected attempt")
    return artifacts


def _execute(slug: str) -> None:
    job_dir = JOB_ROOT / slug
    job_dir.mkdir(parents=True, exist_ok=True)
    _write_status(
        slug,
        {"jobId": slug, "rowSlug": slug, "done": False, "stage": "running", "error": None, "instanceId": _instance_id},
    )
    try:
        record, record_path = _record(slug)
        inputs, input_provenance = _download_inputs(record)
        debug = record["scene_debug"]
        guide = (inputs / "guide.png").read_bytes()
        hero = (inputs / "product.png").read_bytes()
        reference = (inputs / "reference.png").read_bytes()
        meta = debug["reference"]
        style_ref = StyleRef(meta["id"], meta["name"], meta["tone"], meta["content"], "image/png", reference)
        row = Row(slug, record["prompt"], "frozen-v6.1-control-inputs", 2368, 1776, [])
        client = AuditClient(debug, guide)
        original_builder = pipeline.build_guide

        def frozen_guide(_hero, _mask, geometry, camera):
            require(geometry == debug["geometryResponse"]["geometry"], "geometry replay differed")
            require(camera == debug["twinCamera"], "camera replay differed")
            return guide, dict(debug["guideInfo"])

        with _pipeline_lock:
            pipeline.build_guide = frozen_guide
            try:
                result = pipeline.run_row(
                    row,
                    client,
                    [style_ref],
                    PIPELINE_ROOT,
                    hero,
                    ref_count=1,
                    size=(2368, 1776),
                    camera=debug["twinCamera"],
                )
            finally:
                pipeline.build_guide = original_builder
        require(result["status"] == "ok", f"pipeline error: {result.get('error')}")
        require(result["pipeline_version"] == PIPELINE_VERSION, "result pipeline version mismatch")
        row_dir = PIPELINE_ROOT / "rows" / slug
        require((row_dir / "geometry_guide.png").read_bytes() == guide, "persisted guide differs from frozen input")
        artifacts = _artifact_manifest(row_dir, result)
        atomic_json(job_dir / "calls.json", client.calls)
        artifacts["calls.json"] = {
            "path": str(job_dir / "calls.json"),
            "sha256": sha256_file(job_dir / "calls.json"),
            "bytes": (job_dir / "calls.json").stat().st_size,
        }
        provenance = {
            "schema_version": "hp-position-flex-row-provenance-v1",
            "experiment_id": _freeze["experiment_id"],
            "row_slug": slug,
            "row_id": record["row_id"],
            "record": {"path": str(record_path), "sha256": sha256_file(record_path)},
            "prompt_sha256": record["prompt_sha256"],
            "control_job_id": record["job_id"],
            "input_artifacts": input_provenance,
            "pipeline_version": result["pipeline_version"],
            "source_hashes": SOURCE_HASHES,
            "stage_b_attempts": result["stage_b_attempts"],
            "image_calls": result["image_calls"],
            "product_invariant_guard": result["product_invariant_guard"],
            "selected_attempt": result["product_invariant_guard"]["selected_attempt"],
            "calls": client.calls,
            "artifacts": artifacts,
        }
        atomic_json(job_dir / "provenance.json", provenance)
        _write_status(
            slug,
            {
                "jobId": slug,
                "rowSlug": slug,
                "done": True,
                "stage": "done",
                "error": None,
                "instanceId": _instance_id,
                "pipelineVersion": PIPELINE_VERSION,
                "sourceHashes": SOURCE_HASHES,
                "imageCalls": result["image_calls"],
                "stageBAttempts": len(result["stage_b_attempts"]),
                "selectedAttempt": result["product_invariant_guard"]["selected_attempt"],
                "guardVerdicts": [item["verdict"] for item in result["product_invariant_guard"]["attempts"]],
                "provenanceSha256": sha256_file(job_dir / "provenance.json"),
            },
        )
    except Exception as error:  # Preserve the first failing row for fail-fast runner diagnostics.
        _write_status(
            slug,
            {"jobId": slug, "rowSlug": slug, "done": True, "stage": "error", "instanceId": _instance_id, "error": f"{type(error).__name__}: {error}"[:4000]},
        )


class GenerateRequest(BaseModel):
    rowSlug: str


app = FastAPI(title="HP V22.3.3 position-flex full160", version="1")


@app.get("/health")
def health():
    return {
        "ok": True,
        "experimentId": _freeze["experiment_id"],
        "pipelineVersion": PIPELINE_VERSION,
        "sourceHashes": SOURCE_HASHES,
        "records": len(_frozen_record),
        "maxWorkers": 1,
        "instanceId": _instance_id,
        "runRoot": str(PIPELINE_ROOT),
    }


@app.post("/api/generate")
def generate(request: GenerateRequest):
    try:
        _record(request.rowSlug)
    except KeyError:
        raise HTTPException(404, "unknown frozen V6.1 row") from None
    existing = _read_status(request.rowSlug)
    if existing and existing.get("stage") == "done":
        return {"jobId": request.rowSlug, "statusUrl": f"/api/jobs/{request.rowSlug}"}
    if existing and existing.get("stage") in {"queued", "running"} and existing.get("instanceId") == _instance_id:
        return {"jobId": request.rowSlug, "statusUrl": f"/api/jobs/{request.rowSlug}"}
    _write_status(
        request.rowSlug,
        {"jobId": request.rowSlug, "rowSlug": request.rowSlug, "done": False, "stage": "queued", "error": None, "instanceId": _instance_id},
    )
    _executor.submit(_execute, request.rowSlug)
    return {"jobId": request.rowSlug, "statusUrl": f"/api/jobs/{request.rowSlug}"}


@app.get("/api/jobs/{job_id}")
def status(job_id: str):
    value = _read_status(job_id)
    if value is None:
        raise HTTPException(404, "unknown job")
    return value


@app.get("/api/jobs/{job_id}/artifacts/{filename}")
def artifact(job_id: str, filename: str):
    allowed = {"provenance.json", "calls.json", "result.json", "ours.png", "gpt_1.png", "gpt_2.png", "geometry_guide.png"}
    if filename not in allowed or job_id not in _frozen_record:
        raise HTTPException(404, "unknown artifact")
    if filename in {"provenance.json", "calls.json"}:
        path = JOB_ROOT / job_id / filename
    else:
        path = PIPELINE_ROOT / "rows" / job_id / filename
    if not path.is_file():
        raise HTTPException(404, "artifact not ready")
    return FileResponse(path)

