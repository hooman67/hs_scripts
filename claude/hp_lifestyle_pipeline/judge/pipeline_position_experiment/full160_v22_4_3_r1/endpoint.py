#!/usr/bin/env python3
"""Serial endpoint for the audited V22.4.3-R1 qualitative assembly protocol.

The Foundry pipeline and prompts are byte-identical to V22.4.3.  The only
change is wrapper behavior: callers may create two immutable outer jobs for a
row.  Each job retains its own raw pipeline directory and complete audit.
"""
from __future__ import annotations

import base64
import io
import json
import sys
import threading
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import foundry_aws_gateway.llm
from common import atomic_json, load_json, require, sha256_bytes, sha256_file, sha256_json
from config import (
    FREEZE, INPUT_ROOT, JOB_ROOT, MAX_OUTER_JOBS, PACKAGE, PIPELINE_ROOT,
    PIPELINE_VERSION, RECORDS, REMOTE_CONTROL_ENDPOINT, SOURCE_HASHES,
    RETRYABLE_GUARD_ERROR, WRAPPER_VERSION,
)
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from preflight import verify as verify_preflight
from pydantic import BaseModel, Field

sys.path.insert(0, str(PACKAGE))
import hp3p.pipeline as pipeline  # noqa: E402
from hp3p.catalog import StyleRef  # noqa: E402
from hp3p.evalset import Row  # noqa: E402
from hp3p.openai_client import IMAGE_MODEL, TEXT_MODEL  # noqa: E402

verify_preflight(allow_progress=True)
require(pipeline.PIPELINE_VERSION == PIPELINE_VERSION, "imported pipeline version differs from freeze")
_freeze = load_json(FREEZE)
_frozen_record = {item["row_slug"]: item for item in _freeze["records"]}
INPUT_ROOT.mkdir(parents=True, exist_ok=True)
JOB_ROOT.mkdir(parents=True, exist_ok=True)
PIPELINE_ROOT.mkdir(parents=True, exist_ok=True)
_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="hp-v2243r1-full160")
_pipeline_lock = threading.Lock()
_instance_id = str(uuid.uuid4())


def job_id(row_slug: str, outer_attempt: int) -> str:
    require(outer_attempt in range(1, MAX_OUTER_JOBS + 1), "outer attempt out of range")
    return f"{row_slug}__outer_job_{outer_attempt}"


class AuditClient:
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
        content = [{"type": "text", "text": text}] + [{"type": "image_url", "image_url": {"url": f"data:{mime};base64,{base64.b64encode(data).decode()}", "detail": "high"}} for mime, data in images]
        response = self.client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[{"role": "developer", "content": system}, {"role": "user", "content": content}],
            response_format={"type": "json_schema", "json_schema": {"name": "result", "strict": True, "schema": schema}},
            max_completion_tokens=16384, store=False,
        )
        choice = response.choices[0]
        require(choice.finish_reason == "stop" and bool(choice.message.content), f"Astra incomplete: {choice.finish_reason}")
        parsed = json.loads(choice.message.content)
        self.calls.append({
            "kind": "astra_write", "attempt": 1 + sum(c["kind"] == "astra_write" for c in self.calls),
            "model": response.model, "finish_reason": choice.finish_reason,
            "system_sha256": sha256_bytes(system.encode()), "text_sha256": sha256_bytes(text.encode()),
            "images_sha256": [sha256_bytes(data) for _, data in images], "schema_sha256": sha256_json(schema),
            "response_sha256": sha256_json(parsed), "usage": getattr(response.usage, "model_dump", lambda: {})(),
        })
        return parsed

    def edit_image(self, prompt: str, images: list[tuple[str, bytes]], size: str, mask: bytes | None = None) -> bytes:
        require(mask is None and len(images) == 1 and images[0][1] == self.expected_guide, "image call must use only the frozen guide and no mask")
        files = [(f"image{i}.{mime.split('/')[1]}", io.BytesIO(data), mime) for i, (mime, data) in enumerate(images, 1)]
        response = self.client.images.edit(model=IMAGE_MODEL, image=files, prompt=prompt, n=1, size=size, quality="high", output_format="png", background="opaque")
        output = base64.b64decode(response.data[0].b64_json)
        self.calls.append({
            "kind": "image_edit", "attempt": 1 + sum(c["kind"] == "image_edit" for c in self.calls),
            "model": IMAGE_MODEL, "size": size, "prompt_sha256": sha256_bytes(prompt.encode()),
            "guide_sha256": sha256_bytes(images[0][1]), "mask": False, "output_sha256": sha256_bytes(output),
        })
        return output


def _record(slug: str) -> tuple[dict, Path]:
    frozen = _frozen_record.get(slug)
    if frozen is None:
        raise KeyError(slug)
    path = Path(frozen["path"])
    require(path.parent == RECORDS and sha256_file(path) == frozen["sha256"], f"record changed: {slug}")
    record = load_json(path)
    require(record["prompt_sha256"] == frozen["prompt_sha256"], f"prompt hash changed: {slug}")
    return record, path


def _download_inputs(record: dict) -> tuple[Path, dict]:
    slug = record["row_slug"]
    dest = INPUT_ROOT / slug
    dest.mkdir(parents=True, exist_ok=True)
    files = {"product.png": "hp16_product.png", "reference.png": "hp16_reference.png", "guide.png": "hp16_geometry_guide.png"}
    provenance_path = dest / "input_provenance.json"
    frozen = load_json(provenance_path) if provenance_path.exists() else None
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
        if frozen is not None:
            require(frozen.get(local_name) == entry, f"cached frozen input changed for {slug}/{local_name}")
        provenance[local_name] = entry
    if frozen is None:
        atomic_json(provenance_path, provenance)
    return dest, provenance


def _status_path(jid: str) -> Path:
    return JOB_ROOT / jid / "status.json"


def _write_status(jid: str, value: dict) -> None:
    atomic_json(_status_path(jid), value)


def _read_status(jid: str) -> dict | None:
    path = _status_path(jid)
    return load_json(path) if path.exists() else None


def _all_artifacts(row_dir: Path, job_dir: Path) -> dict:
    artifacts = {}
    for label, root in (("pipeline", row_dir), ("job", job_dir)):
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.name not in {"provenance.json", "failure_provenance.json", "status.json"}:
                key = f"{label}/{path.relative_to(root)}"
                artifacts[key] = {"path": str(path), "sha256": sha256_file(path), "bytes": path.stat().st_size}
    return artifacts


def _validate_success_artifacts(row_dir: Path, result: dict, artifacts: dict) -> None:
    by_name = {Path(v["path"]).name: v for v in artifacts.values()}
    image_calls = int(result["image_calls"])
    stage_b = result.get("stage_b_attempts") or []
    guard = result.get("product_invariant_guard") or {}
    attempts = guard.get("attempts") or []
    require(image_calls in (1, 2) and len(stage_b) in (1, 2), "invalid attempt counts")
    require(len(attempts) == image_calls, "guard/image attempt count mismatch")
    selected = guard.get("selected_attempt")
    require(selected in (1, 2) and selected <= image_calls and attempts[selected - 1].get("verdict") == "pass", "guard did not select a passing attempt")
    core = {"result.json", "ours.png", "input.png", "mask.png", "ref_2.png", "geometry_guide.png", "geometry_text.txt", "geometry_request.json", "geometry_response.json", "stage_b_attempt_1_request.json", "stage_b_attempt_1_response.json", "calls.json"}
    require(core <= set(by_name), f"missing core artifacts: {sorted(core - set(by_name))}")
    for i in range(1, len(stage_b) + 1):
        require(f"stage_b_attempt_{i}_request.json" in by_name and f"stage_b_attempt_{i}_response.json" in by_name, f"missing Stage-B attempt {i}")
    if len(stage_b) == 2:
        require("stage_b_attempt_2_raw_response.json" in by_name, "missing raw Stage-B retry response")
    for i in range(1, image_calls + 1):
        for name in (f"gpt_{i}.png", f"image_request_attempt_{i}.json", f"product_invariant_attempt_{i}.json"):
            require(name in by_name, f"missing {name}")
    require(by_name["ours.png"]["sha256"] == by_name[f"gpt_{selected}.png"]["sha256"], "ours.png differs from selected attempt")


def _execute(row_slug: str, outer_attempt: int, submission: dict, submission_sha: str) -> None:
    jid = job_id(row_slug, outer_attempt)
    job_dir = JOB_ROOT / jid
    row_dir = PIPELINE_ROOT / "rows" / jid
    client = None
    record = None
    record_path = None
    input_provenance = None
    result = None
    _write_status(jid, {"jobId": jid, "rowSlug": row_slug, "outerAttempt": outer_attempt, "done": False, "stage": "running", "error": None, "instanceId": _instance_id, "submissionRequestSha256": submission_sha})
    try:
        record, record_path = _record(row_slug)
        inputs, input_provenance = _download_inputs(record)
        debug = record["scene_debug"]
        guide, hero, reference = (inputs / "guide.png").read_bytes(), (inputs / "product.png").read_bytes(), (inputs / "reference.png").read_bytes()
        meta = debug["reference"]
        style_ref = StyleRef(meta["id"], meta["name"], meta["tone"], meta["content"], "image/png", reference)
        row = Row(jid, record["prompt"], "frozen-v6.1-control-inputs", 2368, 1776, [])
        client = AuditClient(debug, guide)
        original_builder = pipeline.build_guide

        def frozen_guide(_hero, _mask, geometry, camera):
            require(geometry == debug["geometryResponse"]["geometry"], "geometry replay differed")
            require(camera == debug["twinCamera"], "camera replay differed")
            return guide, dict(debug["guideInfo"])

        with _pipeline_lock:
            pipeline.build_guide = frozen_guide
            try:
                result = pipeline.run_row(row, client, [style_ref], PIPELINE_ROOT, hero, ref_count=1, size=(2368, 1776), camera=debug["twinCamera"])
            finally:
                pipeline.build_guide = original_builder
        require(result["status"] == "ok", f"pipeline error: {result.get('error')}")
        require(result["pipeline_version"] == PIPELINE_VERSION, "result pipeline version mismatch")
        require((row_dir / "geometry_guide.png").read_bytes() == guide, "persisted guide differs from frozen input")
        atomic_json(job_dir / "calls.json", client.calls)
        artifacts = _all_artifacts(row_dir, job_dir)
        _validate_success_artifacts(row_dir, result, artifacts)
        provenance = {
            "schema_version": "hp-position-flex-row-provenance-v22.4.3-r1",
            "experiment_id": _freeze["experiment_id"], "row_slug": row_slug, "job_id": jid,
            "outer_attempt": outer_attempt, "submission_request": submission,
            "submission_request_sha256": submission_sha, "row_id": record["row_id"],
            "record": {"path": str(record_path), "sha256": sha256_file(record_path)},
            "prompt_sha256": record["prompt_sha256"], "control_job_id": record["job_id"],
            "input_artifacts": input_provenance, "pipeline_version": result["pipeline_version"],
            "wrapper_version": WRAPPER_VERSION, "source_hashes": SOURCE_HASHES,
            "stage_b_attempts": result["stage_b_attempts"], "image_calls": result["image_calls"],
            "product_invariant_guard": result["product_invariant_guard"], "calls": client.calls,
            "artifacts": artifacts,
        }
        atomic_json(job_dir / "provenance.json", provenance)
        manifest_sha = sha256_json(artifacts)
        _write_status(jid, {
            "jobId": jid, "rowSlug": row_slug, "outerAttempt": outer_attempt, "done": True,
            "stage": "done", "error": None, "instanceId": _instance_id,
            "submissionRequestSha256": submission_sha, "pipelineVersion": PIPELINE_VERSION,
            "wrapperVersion": WRAPPER_VERSION, "sourceHashes": SOURCE_HASHES,
            "imageCalls": result["image_calls"], "stageBAttempts": len(result["stage_b_attempts"]),
            "selectedAttempt": result["product_invariant_guard"]["selected_attempt"],
            "guardVerdicts": [x["verdict"] for x in result["product_invariant_guard"]["attempts"]],
            "artifactManifestSha256": manifest_sha,
            "provenanceSha256": sha256_file(job_dir / "provenance.json"),
        })
    except Exception as error:
        error_text = f"{type(error).__name__}: {error}"[:4000]
        if client is not None:
            atomic_json(job_dir / "calls.json", client.calls)
        artifacts = _all_artifacts(row_dir, job_dir)
        failure = {
            "schema_version": "hp-position-flex-failure-provenance-v22.4.3-r1",
            "experiment_id": _freeze["experiment_id"], "row_slug": row_slug, "job_id": jid,
            "outer_attempt": outer_attempt, "submission_request": submission,
            "submission_request_sha256": submission_sha, "error": error_text,
            "record": ({"path": str(record_path), "sha256": sha256_file(record_path)} if record_path else None),
            "prompt_sha256": (record.get("prompt_sha256") if record else None),
            "input_artifacts": input_provenance, "pipeline_version": PIPELINE_VERSION,
            "wrapper_version": WRAPPER_VERSION, "source_hashes": SOURCE_HASHES,
            "pipeline_result": result, "calls": (client.calls if client else []), "artifacts": artifacts,
        }
        atomic_json(job_dir / "failure_provenance.json", failure)
        _write_status(jid, {
            "jobId": jid, "rowSlug": row_slug, "outerAttempt": outer_attempt, "done": True,
            "stage": "error", "instanceId": _instance_id, "error": error_text,
            "submissionRequestSha256": submission_sha, "pipelineVersion": PIPELINE_VERSION,
            "wrapperVersion": WRAPPER_VERSION, "sourceHashes": SOURCE_HASHES,
            "artifactManifestSha256": sha256_json(artifacts),
            "failureProvenanceSha256": sha256_file(job_dir / "failure_provenance.json"),
        })


class GenerateRequest(BaseModel):
    rowSlug: str
    outerAttempt: int = Field(ge=1, le=MAX_OUTER_JOBS)


app = FastAPI(title="HP V22.4.3-R1 audited qualitative assembly", version="1")


@app.get("/health")
def health():
    return {"ok": True, "experimentId": _freeze["experiment_id"], "pipelineVersion": PIPELINE_VERSION, "wrapperVersion": WRAPPER_VERSION, "sourceHashes": SOURCE_HASHES, "records": len(_frozen_record), "maxWorkers": 1, "maxOuterJobs": MAX_OUTER_JOBS, "instanceId": _instance_id, "runRoot": str(PIPELINE_ROOT)}


@app.post("/api/generate")
def generate(request: GenerateRequest):
    try:
        _record(request.rowSlug)
    except KeyError:
        raise HTTPException(404, "unknown frozen V6.1 row") from None
    jid = job_id(request.rowSlug, request.outerAttempt)
    if request.outerAttempt == 2:
        first = _read_status(job_id(request.rowSlug, 1))
        if not (
            first
            and first.get("done") is True
            and first.get("stage") == "error"
            and first.get("error") == RETRYABLE_GUARD_ERROR
        ):
            raise HTTPException(409, "outer job 2 requires the exact frozen guard rejection from outer job 1")
    submission = {"rowSlug": request.rowSlug, "outerAttempt": request.outerAttempt}
    submission_sha = sha256_json(submission)
    existing = _read_status(jid)
    if existing:
        require(existing.get("submissionRequestSha256") == submission_sha, "immutable job request differs")
        return {"jobId": jid, "statusUrl": f"/api/jobs/{jid}"}
    (JOB_ROOT / jid).mkdir(parents=True, exist_ok=False)
    atomic_json(JOB_ROOT / jid / "submission_request.json", submission)
    _write_status(jid, {"jobId": jid, "rowSlug": request.rowSlug, "outerAttempt": request.outerAttempt, "done": False, "stage": "queued", "error": None, "instanceId": _instance_id, "submissionRequestSha256": submission_sha})
    _executor.submit(_execute, request.rowSlug, request.outerAttempt, submission, submission_sha)
    return {"jobId": jid, "statusUrl": f"/api/jobs/{jid}"}


@app.get("/api/jobs/{jid}")
def status(jid: str):
    value = _read_status(jid)
    if value is None:
        raise HTTPException(404, "unknown job")
    return value


@app.get("/api/jobs/{jid}/artifacts/{filename}")
def artifact(jid: str, filename: str):
    allowed = {"provenance.json", "failure_provenance.json", "calls.json", "submission_request.json", "result.json", "ours.png", "gpt_1.png", "gpt_2.png", "geometry_guide.png"}
    if filename not in allowed or not (JOB_ROOT / jid).is_dir():
        raise HTTPException(404, "unknown artifact")
    path = JOB_ROOT / jid / filename if filename in {"provenance.json", "failure_provenance.json", "calls.json", "submission_request.json"} else PIPELINE_ROOT / "rows" / jid / filename
    if not path.is_file():
        raise HTTPException(404, "artifact not ready")
    return FileResponse(path)
