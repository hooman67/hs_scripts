"""Original native-output checks with explicit recovery run/endpoint parameters."""

from __future__ import annotations

import base64
import hashlib
import io
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image

import scene_runner
from recovery.complete160 import image_recovery as study


def audit_one(prompt: dict[str, Any], run: Path) -> dict[str, Any]:
    row = study.row_for(prompt)
    record = scene_runner.valid_completed_record(run, row)
    if record is None:
        raise ValueError("Recovery output has no valid completed record")
    paths = scene_runner.paths(run, row)
    job = study.load(paths["job"])
    expected = {"digitalTwinId": row["digital_twin_id"], "cameraId": row["camera_id"], "prompt": prompt["text"]}
    if job["request"] != expected or str(job["submit_response"]["jobId"]) != record["job_id"]:
        raise ValueError("Recovered output does not bind its exact source prompt/view")
    if record["lineage"]["source_commit"] != study.COMMIT:
        raise ValueError("Recovered output pipeline changed")
    native = study.ENDPOINT / "run/jobs" / record["job_id"]
    inputs = study.ENDPOINT / "run/pipeline/rows" / record["job_id"]
    calls = study.load(native / "calls.json")
    if len(calls) != 4 or any(call["status"] != "done" for call in calls):
        raise ValueError("Recovered output has an incomplete native ledger")
    kinds = Counter()
    image_request: dict[str, Any] | None = None
    for call in calls:
        request = study.load(native / call["requestArtifact"])
        response = study.load(native / call["responseArtifact"])
        if (
            scene_runner.canonical_sha256(request) != call["requestSha256"]
            or scene_runner.canonical_sha256(response) != call["responseSha256"]
        ):
            raise ValueError("Recovered native request/response hash mismatch")
        kinds.update([call["kind"]])
        if call["kind"] == "image_edit":
            settings = {
                "model": "gpt-image-2.5-sunburst-2026-09-08",
                "n": 1,
                "size": "2368x1776",
                "quality": "high",
                "output_format": "png",
                "background": "opaque",
                "imageInputOrder": ["hp16_geometry_guide.png"],
            }
            if (
                any(request.get(key) != value for key, value in settings.items())
                or len(request["image"]) != 1
                or request.get("mask")
                or request["prompt"] != record["scene_debug"]["finalPrompt"]
            ):
                raise ValueError("Recovered native image policy changed")
            raw = base64.b64decode(response["data"][0]["b64_json"])
            if (
                hashlib.sha256(raw).hexdigest() != call["outputSha256"]
                or call["outputSha256"] != record["image_sha256"]
            ):
                raise ValueError("Recovered PNG differs from raw model output")
            image_request = request
        elif (
            request["model"] != "gpt-6-astra"
            or response["model"] != "gpt-6-astra"
            or request["max_completion_tokens"] != 16384
            or request["store"] is not False
            or "temperature" in request
            or "reasoning_effort" in request
        ):
            raise ValueError("Recovered native Astra policy/identity changed")
    if kinds != Counter({"chat_json": 3, "image_edit": 1}) or image_request is None:
        raise ValueError("Recovered native call mix changed")
    references = list(inputs.glob("ref_2.*"))
    geometry = study.load(inputs / "geometry_request.json")["images"]
    if len(references) != 1 or len(geometry) != 2:
        raise ValueError("Actual planning/reference inputs are ambiguous")
    hashes = {
        "product": geometry[0]["sha256"],
        "reference": geometry[1]["sha256"],
        "geometry_guide": image_request["image"][0]["sha256"],
    }
    twin = next(
        entry
        for entry in study.load(study.ENDPOINT / "input_bundle/manifest.json")["entries"]
        if (entry["digital_twin_id"], entry["camera_id"]) == (row["digital_twin_id"], row["camera_id"])
    )
    if hashes["product"] != twin["product_sha256"]:
        raise ValueError("Recovered product reference differs from original")
    assets = {}
    for role, path in {
        "product": inputs / "input.png",
        "reference": references[0],
        "geometry_guide": inputs / "geometry_guide.png",
    }.items():
        body = path.read_bytes()
        if hashlib.sha256(body).hexdigest() != hashes[role]:
            raise ValueError("Recovered native input bytes changed")
        with Image.open(io.BytesIO(body)) as image:
            dimensions, fmt = image.size, image.format
            image.verify()
        if fmt not in ("PNG", "WEBP", "JPEG"):
            raise ValueError("Recovered native input format is unsupported")
        if role != "reference" and dimensions != (2368, 1776):
            raise ValueError("Recovered native input dimensions changed")
        assets[role] = {
            "path": str(path),
            "sha256": hashes[role],
            "suffix": {"PNG": "png", "WEBP": "webp", "JPEG": "jpg"}[fmt],
        }
    with Image.open(paths["image"]) as image:
        if image.size != (2368, 1776) or image.format != "PNG":
            raise ValueError("Recovered final image format/dimensions changed")
    audit = {
        "job_id": record["job_id"],
        "record_sha256": study.sha(paths["record"]),
        "native_calls": calls,
        "new_model_calls_for_audit": 0,
        **assets,
    }
    study.write(study.HERE / "input_audit" / (row["row_slug"] + ".json"), audit)
    return audit
