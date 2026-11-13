#!/usr/bin/env python3
"""Local live-style API for the isolated HP support-shape runtime candidate."""

from __future__ import annotations

import base64
import datetime as dt
import hashlib
import importlib.metadata as metadata
import io
import json
import os
import re
import secrets
import shutil
import sys
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, StrictStr

HERE = Path(__file__).resolve().parent
RUNTIME = HERE / "runtime"
INPUT_ROOT = HERE / "input_bundle"
RUN_ROOT = HERE / "run"
JOBS = RUN_ROOT / "jobs"
PIPELINE_RUN = RUN_ROOT / "pipeline"
CATALOG_PATH = RUNTIME / "assets/styles.json"
CAPTIONS_PATH = RUNTIME / "hp3p/data/ref_captions.json"
INPUT_MANIFEST_PATH = INPUT_ROOT / "manifest.json"
CANDIDATE_MANIFEST_PATH = HERE / "runtime_surface_shape_r1_manifest.json"
DEPLOYMENT_MANIFEST_PATH = HERE / "deployment_manifest.json"

CANDIDATE_ID = "hp-v6.2-surface-shape-r1"
SOURCE_COMMIT = "8c358bc7989cb0e137e89db0fd325168249e2a22"
PATCH_SHA256 = "95ddc80d7d62e75c6f7461a45011a6412a35a4bc03a36fada517fdf5888a8843"
CODE_TREE_SHA256 = "631fe047e7b82c6c690f038effda1155b0ffde5ecdbf8be745164db649a80de5"
CANDIDATE_MANIFEST_SHA256 = "17346485b892b02714f52940b2bbd1806de99c06c8c23816b5c1b11a4564d172"
INPUT_MANIFEST_SHA256 = "7cc98fe46f5983acbf5fd9b781bf108ecdee12a042e953686201e9900698a1c5"
REFERENCE_CATALOG_SHA256 = "d1e87ce902b7ad62d9dd7e8287326a0225270ad065a4efeba9dd167dc0b12771"
REFERENCE_CAPTIONS_SHA256 = "c92fd69684a64d0e6e1f4771c3d29a66ac07ba6f729c3843f83f59c7f16e3085"
SOURCE_TEXT_MANIFEST_SHA256 = "b701871a526d22f73c249cf28f02d19f42d330951967a76d5be8b3855fd6b30e"
SOURCE_ARTIFACT_MANIFEST_SHA256 = "2a4951b192fa313a1d58e700962c338e3af196349e7e4fe5cd492c1ebcc7e31b"
PIPELINE_VERSION = "unified-blue-scale-v20-surface-shape-r1"
GENERATOR = "GPT Image 2.5 / single reference / no grading"
REWRITER_VERSION = (
    "Adobe-Firefly/foundry#4349 / 8c358bc7989c + surface-shape-r1 / "
    "unified-blue-scale-v20-surface-shape-r1"
)
EXPECTED_IMAGE_MODEL = "gpt-image-2.5-sunburst-2026-09-08"
EXPECTED_TEXT_MODEL = "gpt-6-astra"
SOURCE_HASHES = {
    "hp3p/geometry.py": "1a0d872f1a03de280b07fb72e7e8ae22e019443844b974b5276ccd826049b4e5",
    "hp3p/pipeline.py": "ec795e2a69d7de2b2e28e0f433e8d433db73458a92e3976f7df4132562ad0b89",
    "hp3p/prompts/system_3p.txt": "178e9fac56cd5746384cdbe9a96deec0c92bac8c8225a68de3f5364067e4fdae",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(raw.encode("utf-8"))


CONFIG_IDENTITY = {
    "candidateId": CANDIDATE_ID,
    "sourceCommit": SOURCE_COMMIT,
    "patchSha256": PATCH_SHA256,
    "codeTreeSha256": CODE_TREE_SHA256,
    "candidateManifestSha256": CANDIDATE_MANIFEST_SHA256,
    "inputManifestSha256": INPUT_MANIFEST_SHA256,
    "referenceCatalogSha256": REFERENCE_CATALOG_SHA256,
    "referenceCaptionsSha256": REFERENCE_CAPTIONS_SHA256,
    "pipelineVersion": PIPELINE_VERSION,
    "generator": GENERATOR,
    "rewriterVersion": REWRITER_VERSION,
    "textModel": EXPECTED_TEXT_MODEL,
    "imageModel": EXPECTED_IMAGE_MODEL,
    "imageSettings": {
        "operation": "images.edit",
        "count": 1,
        "size": "2368x1776",
        "quality": "high",
        "outputFormat": "png",
        "background": "opaque",
        "inputs": "one generated geometry guide",
        "mask": False,
    },
}
CONFIG_SHA256 = canonical_sha256(CONFIG_IDENTITY)


def verify_files() -> None:
    expected = {
        CANDIDATE_MANIFEST_PATH: CANDIDATE_MANIFEST_SHA256,
        INPUT_MANIFEST_PATH: INPUT_MANIFEST_SHA256,
        CATALOG_PATH: REFERENCE_CATALOG_SHA256,
        CAPTIONS_PATH: REFERENCE_CAPTIONS_SHA256,
        RUNTIME / "assets/source_text_transfer_manifest.json": SOURCE_TEXT_MANIFEST_SHA256,
        RUNTIME / "assets/source_artifact_manifest.json": SOURCE_ARTIFACT_MANIFEST_SHA256,
        **{RUNTIME / relative: digest for relative, digest in SOURCE_HASHES.items()},
    }
    failures = {str(path): sha256_path(path) if path.is_file() else None for path, digest in expected.items()
                if not path.is_file() or sha256_path(path) != digest}
    if failures:
        raise RuntimeError(f"isolated endpoint source verification failed: {failures}")


verify_files()
sys.path.insert(0, str(RUNTIME))

import hp3p  # noqa: E402
import hp3p.geometry as geometry  # noqa: E402
import hp3p.pipeline as pipeline  # noqa: E402
from hp3p.catalog import load_catalog  # noqa: E402
from hp3p.evalset import Row  # noqa: E402
from hp3p.openai_client import IMAGE_MODEL, TEXT_MODEL  # noqa: E402

if pipeline.PIPELINE_VERSION != PIPELINE_VERSION:
    raise RuntimeError("imported pipeline version differs from candidate identity")
if IMAGE_MODEL != EXPECTED_IMAGE_MODEL or TEXT_MODEL != EXPECTED_TEXT_MODEL:
    raise RuntimeError("imported model configuration differs from candidate identity")
for module in (hp3p, geometry, pipeline):
    if not Path(module.__file__).resolve().is_relative_to(RUNTIME.resolve()):
        raise RuntimeError(f"import escaped isolated runtime: {module.__file__}")

INPUT_MANIFEST = json.loads(INPUT_MANIFEST_PATH.read_text(encoding="utf-8"))
ENTRIES = {(item["digital_twin_id"], item["camera_id"]): item for item in INPUT_MANIFEST["entries"]}
if len(ENTRIES) != 16:
    raise RuntimeError(f"expected 16 fixed twin views, found {len(ENTRIES)}")
for item in ENTRIES.values():
    product = INPUT_ROOT / item["product_path"]
    if sha256_path(product) != item["product_sha256"]:
        raise RuntimeError(f"fixed twin hash mismatch: {product}")

REFERENCE_CATALOG = load_catalog(CATALOG_PATH)
REFERENCE_CAPTIONS = json.loads(CAPTIONS_PATH.read_text(encoding="utf-8"))
if len(REFERENCE_CATALOG) != 341:
    raise RuntimeError(f"expected 341 byte-deduplicated references, found {len(REFERENCE_CATALOG)}")


def create_provider_client():
    import foundry_aws_gateway.llm
    import types_boto3_bedrock_runtime

    if not types_boto3_bedrock_runtime.__file__:
        raise RuntimeError("types_boto3_bedrock_runtime has no import path")
    return foundry_aws_gateway.llm.get_openai().with_options(max_retries=0, timeout=540.0)


def provider_preflight() -> dict[str, str | bool]:
    client = create_provider_client()
    if client.__class__.__name__ != "OpenAI":
        raise RuntimeError(f"unexpected provider client: {client.__class__.__name__}")
    return {
        "ready": True,
        "gatewayVersion": metadata.version("foundry-aws-gateway"),
        "bedrockTypesVersion": metadata.version("types-boto3-bedrock-runtime"),
        "clientClass": client.__class__.__name__,
        "modelRequestMade": False,
    }


PROVIDER_PREFLIGHT = provider_preflight()

JOBS.mkdir(parents=True, exist_ok=True)
PIPELINE_RUN.mkdir(parents=True, exist_ok=True)
_max_workers = int(os.environ.get("HP_SHAPE_MAX_WORKERS", "4"))
if not 1 <= _max_workers <= 4:
    raise RuntimeError("HP_SHAPE_MAX_WORKERS must be between 1 and 4")
_executor = ThreadPoolExecutor(max_workers=_max_workers, thread_name_prefix="hp-shape-r1")
_write_lock = threading.Lock()
_instance_id = str(uuid.uuid4())
_csrf = secrets.token_urlsafe(32)
_generation_enabled = os.environ.get("HP_SHAPE_GENERATION_ENABLED") == "1"
_expected_origin = os.environ.get("HP_SHAPE_PUBLIC_BASE_URL", "").rstrip("/")


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def lineage() -> dict[str, Any]:
    return {
        **CONFIG_IDENTITY,
        "configSha256": CONFIG_SHA256,
        "deploymentManifestSha256": (
            sha256_path(DEPLOYMENT_MANIFEST_PATH) if DEPLOYMENT_MANIFEST_PATH.is_file() else None
        ),
        "codeTreeScope": "41-file candidate source tree; restored runtime assets are pinned separately",
        "runtimeImports": {
            "hp3p": str(Path(hp3p.__file__).resolve()),
            "pipeline": str(Path(pipeline.__file__).resolve()),
            "geometry": str(Path(geometry.__file__).resolve()),
        },
    }


def twin_catalog() -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for item in INPUT_MANIFEST["entries"]:
        twin = grouped.setdefault(
            item["digital_twin_id"],
            {
                "id": item["digital_twin_id"],
                "name": item["digital_twin_name"],
                "lighting": item["lighting"],
                "cameras": [],
                "defaultCameraId": item["camera_id"],
            },
        )
        twin["cameras"].append({"id": item["camera_id"], "name": item["camera_id"]})
    return list(grouped.values())


CATALOG_RESPONSE = {
    "digitalTwins": twin_catalog(),
    "referenceCount": len(REFERENCE_CATALOG),
    "rewriterVersion": REWRITER_VERSION,
    "generator": GENERATOR,
    "candidateLineage": lineage(),
}


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=float) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def job_dir(job_id: str) -> Path:
    if not re.fullmatch(r"[0-9TZ_]+[0-9a-f]{12}", job_id):
        raise HTTPException(404, "unknown job")
    return JOBS / job_id


def read_json(path: Path) -> dict[str, Any] | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def write_status(job_id: str, value: dict[str, Any]) -> None:
    with _write_lock:
        atomic_json(job_dir(job_id) / "status.json", value)


def initial_status(job_id: str, request: dict[str, str], item: dict[str, Any]) -> dict[str, Any]:
    hero_detail = {
        "digitalTwinId": item["digital_twin_id"],
        "digitalTwinName": item["digital_twin_name"],
        "cameraId": item["camera_id"],
        "cameraPath": item["camera_path"],
        "heroLighting": item["lighting"],
        "productVersion": item["product_version"],
        "productSha256": item["product_sha256"],
    }
    return {
        "jobId": job_id,
        "done": False,
        "createdAt": now(),
        "instanceId": _instance_id,
        "candidateLineage": lineage(),
        "params": {
            **request,
            "digitalTwinName": item["digital_twin_name"],
            "cameraPath": item["camera_path"],
            "heroLighting": item["lighting"],
            "productVersion": item["product_version"],
            "generationMode": "sceneOnly",
            "candidateId": CANDIDATE_ID,
            "configSha256": CONFIG_SHA256,
        },
        "stages": {
            "hero": {"status": "done", "ms": 0, "error": None, "has_image": True, "detail": hero_detail},
            "scene": {"status": "queued", "ms": 0, "error": None, "has_image": False, "detail": {}},
            "ibl": {"status": "skipped", "ms": 0, "error": None, "has_image": False, "detail": {}},
            "backplate": {"status": "skipped", "ms": 0, "error": None, "has_image": False, "detail": {}},
            "recomposite": {"status": "skipped", "ms": 0, "error": None, "has_image": False, "detail": {}},
            "relight": {"status": "skipped", "ms": 0, "error": None, "has_image": False, "detail": {}},
        },
    }


class GatewayOpenAIClient:
    """Runtime protocol adapter with the package's exact model call settings."""

    def __init__(self) -> None:
        self.client = create_provider_client()
        self.calls: list[dict[str, Any]] = []

    def chat_json(self, system: str, text: str, images: list[tuple[str, bytes]], schema: dict) -> dict:
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
        if choice.finish_reason != "stop" or not choice.message.content:
            raise RuntimeError(f"Astra incomplete: {choice.finish_reason}")
        value = json.loads(choice.message.content)
        self.calls.append(
            {
                "kind": "chat_json",
                "model": response.model,
                "finishReason": choice.finish_reason,
                "systemSha256": sha256_bytes(system.encode()),
                "textSha256": sha256_bytes(text.encode()),
                "imageSha256": [sha256_bytes(data) for _, data in images],
                "schemaSha256": canonical_sha256(schema),
                "responseSha256": canonical_sha256(value),
            }
        )
        return value

    def edit_image(self, prompt: str, images: list[tuple[str, bytes]], size: str, mask: bytes | None = None) -> bytes:
        if mask is not None or len(images) != 1 or size != "2368x1776":
            raise RuntimeError("candidate image call must use one guide, no mask, and 2368x1776")
        files = [(f"image{i}.{mime.split('/')[1]}", io.BytesIO(data), mime)
                 for i, (mime, data) in enumerate(images, 1)]
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
                "model": IMAGE_MODEL,
                "size": size,
                "quality": "high",
                "outputFormat": "png",
                "background": "opaque",
                "count": 1,
                "mask": False,
                "promptSha256": sha256_bytes(prompt.encode()),
                "guideSha256": sha256_bytes(images[0][1]),
                "outputSha256": sha256_bytes(output),
            }
        )
        return output


def scene_detail(result: dict[str, Any], request: dict[str, str], item: dict[str, Any]) -> dict[str, Any]:
    reference = None
    if result.get("ref_ids"):
        ref_id = result["ref_ids"][0]
        reference_obj = next((ref for ref in REFERENCE_CATALOG if ref.id == ref_id), None)
        if reference_obj:
            reference = {
                "id": reference_obj.id,
                "name": reference_obj.name,
                "tone": reference_obj.tone,
                "content": reference_obj.content,
            }
    return {
        "rewriterVersion": REWRITER_VERSION,
        "rewriterBackend": "Astra / original request only",
        "pipelineVersion": PIPELINE_VERSION,
        "candidateLineage": lineage(),
        "baselinePromptUsed": False,
        "originalPrompt": request["prompt"],
        "textModel": TEXT_MODEL,
        "imageModel": IMAGE_MODEL,
        "size": "2368x1776",
        "refCount": 1,
        "imageCalls": result.get("image_calls", 0),
        "graded": False,
        "maskSource": "derived from frozen product render by pinned hp3p.mask.prepare",
        "productPixelLock": "Unmasked generation; product preservation is instructed, not guaranteed.",
        "imageMaskApplied": False,
        "twinCamera": item["camera"],
        "twinCameraSummary": result.get("twin_camera"),
        "selection": {
            "tone": result.get("tone"),
            "content": result.get("content"),
            "rationale": result.get("rationale"),
        },
        "reference": reference,
        "geometryResponse": {
            "geometry": result.get("geometry"),
            "product_category": result.get("product_category"),
        },
        "guideInfo": result.get("guide_info"),
        "geometryText": result.get("geometry_text"),
        "productCategory": result.get("product_category"),
        "layout": result.get("layout"),
        "camera": result.get("camera"),
        "composition": result.get("composition"),
        "finalPrompt": result.get("prompt"),
    }


def execute(job_id: str, request: dict[str, str], item: dict[str, Any]) -> None:
    status_path = job_dir(job_id) / "status.json"
    status = read_json(status_path) or initial_status(job_id, request, item)
    status["stages"]["scene"]["status"] = "running"
    write_status(job_id, status)
    try:
        client = GatewayOpenAIClient()
        row = Row(job_id, request["prompt"], "frozen-local-twin", 2368, 1776, [])
        product_path = INPUT_ROOT / item["product_path"]
        result = pipeline.run_row(
            row,
            client,
            REFERENCE_CATALOG,
            PIPELINE_RUN,
            product_path.read_bytes(),
            REFERENCE_CAPTIONS,
            ref_count=1,
            size=(2368, 1776),
            camera=item["camera"],
        )
        atomic_json(job_dir(job_id) / "calls.json", client.calls)
        source_row = PIPELINE_RUN / "rows" / job_id
        for source_name, target_name in (
            ("result.json", "result.json"),
            ("geometry_guide.png", "hp16_geometry_guide.png"),
            ("input.png", "hp16_product.png"),
        ):
            source = source_row / source_name
            if source.is_file():
                shutil.copy2(source, job_dir(job_id) / target_name)
        detail = scene_detail(result, request, item)
        if result.get("status") != "ok":
            raise RuntimeError(result.get("error") or "pipeline returned an unsuccessful result")
        shutil.copy2(source_row / "ours.png", job_dir(job_id) / "2_scene.png")
        status["stages"]["scene"].update(
            status="done",
            ms=int(float(result.get("elapsed_s", 0)) * 1000),
            error=None,
            has_image=True,
            detail=detail,
        )
        status["done"] = True
        status["completedAt"] = now()
        status["imageSha256"] = sha256_path(job_dir(job_id) / "2_scene.png")
        write_status(job_id, status)
    except Exception as error:
        status = read_json(status_path) or status
        status["stages"]["scene"].update(
            status="error",
            error=f"{type(error).__name__}: {error}"[:2000],
            has_image=False,
        )
        status["done"] = True
        status["completedAt"] = now()
        write_status(job_id, status)


class GenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    digitalTwinId: StrictStr
    cameraId: StrictStr
    prompt: StrictStr


app = FastAPI(title="HP V6.2 support-shape candidate endpoint", version="1")


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "generationEnabled": _generation_enabled,
        "instanceId": _instance_id,
        "maxWorkers": _max_workers,
        "fixedTwinViews": len(ENTRIES),
        "referenceCount": len(REFERENCE_CATALOG),
        "providerPreflight": PROVIDER_PREFLIGHT,
        "candidateLineage": lineage(),
    }


@app.get("/api/credentials")
def credentials(response: Response) -> dict[str, Any]:
    response.set_cookie("hp_shape_session", _instance_id, httponly=True, samesite="strict")
    return {"csrfToken": _csrf, "generationEnabled": _generation_enabled, "candidateId": CANDIDATE_ID}


@app.get("/api/catalog")
def catalog() -> dict[str, Any]:
    return CATALOG_RESPONSE


@app.get("/api/debug/imports")
def debug_imports() -> dict[str, Any]:
    return {
        "instanceId": _instance_id,
        "generationEnabled": _generation_enabled,
        "python": sys.executable,
        "providerPreflight": PROVIDER_PREFLIGHT,
        "lineage": lineage(),
        "sourceHashes": SOURCE_HASHES,
    }


@app.post("/api/generate", status_code=202)
def generate(
    body: GenerateRequest,
    request: Request,
    x_hp12_csrf: str | None = Header(default=None),
) -> dict[str, Any]:
    if not _generation_enabled:
        raise HTTPException(503, "generation is disabled until the bounded smoke is explicitly authorized")
    if not secrets.compare_digest(x_hp12_csrf or "", _csrf):
        raise HTTPException(403, "invalid CSRF token")
    origin = request.headers.get("origin", "").rstrip("/")
    if _expected_origin and origin != _expected_origin:
        raise HTTPException(403, "invalid request origin")
    payload = body.model_dump()
    if not payload["prompt"].strip():
        raise HTTPException(422, "prompt must not be empty")
    item = ENTRIES.get((payload["digitalTwinId"], payload["cameraId"]))
    if item is None:
        raise HTTPException(404, "unknown fixed digital-twin/camera view")
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    job_id = f"{timestamp}_{uuid.uuid4().hex[:12]}"
    directory = job_dir(job_id)
    directory.mkdir(parents=True, exist_ok=False)
    atomic_json(
        directory / "job.json",
        {
            "schemaVersion": 1,
            "jobId": job_id,
            "submittedAt": now(),
            "request": payload,
            "requestSha256": canonical_sha256(payload),
            "candidateLineage": lineage(),
            "input": {
                "productSha256": item["product_sha256"],
                "controlJobId": item["control_job_id"],
                "controlRecordSha256": item["control_record_sha256"],
            },
        },
    )
    write_status(job_id, initial_status(job_id, payload, item))
    _executor.submit(execute, job_id, payload, item)
    return {
        "jobId": job_id,
        "statusUrl": f"/api/jobs/{job_id}",
        "imageUrl": f"/api/jobs/{job_id}/artifacts/2_scene.png",
        "debugUrl": f"/api/jobs/{job_id}/debug",
        "candidateId": CANDIDATE_ID,
        "configSha256": CONFIG_SHA256,
    }


@app.get("/api/jobs/{job_id}")
def job_status(job_id: str) -> dict[str, Any]:
    value = read_json(job_dir(job_id) / "status.json")
    if value is None:
        raise HTTPException(404, "unknown job")
    return value


@app.get("/api/jobs/{job_id}/debug")
def job_debug(job_id: str) -> dict[str, Any]:
    directory = job_dir(job_id)
    job = read_json(directory / "job.json")
    if job is None:
        raise HTTPException(404, "unknown job")
    return {
        "job": job,
        "status": read_json(directory / "status.json"),
        "calls": read_json(directory / "calls.json"),
        "result": read_json(directory / "result.json"),
    }


@app.get("/api/jobs/{job_id}/artifacts/{filename}")
def artifact(job_id: str, filename: str) -> FileResponse:
    allowed = {
        "2_scene.png",
        "hp16_product.png",
        "hp16_geometry_guide.png",
        "result.json",
        "calls.json",
        "job.json",
        "status.json",
    }
    if filename not in allowed:
        raise HTTPException(404, "unknown artifact")
    path = job_dir(job_id) / filename
    if not path.is_file():
        raise HTTPException(404, "artifact not ready")
    return FileResponse(path)


if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("HP_SHAPE_HOST", "127.0.0.1")
    port = int(os.environ.get("HP_SHAPE_PORT", "8137"))
    uvicorn.run(app, host=host, port=port, access_log=False)
