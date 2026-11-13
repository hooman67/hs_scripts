import base64
import hashlib
import io
from collections import Counter
from pathlib import Path

from PIL import Image

import image_study as study

HERE = study.HERE


def emit(path, value):
    study.write(Path(path), value)


def audit_one(prompt, twins, reused):
    runner = study.image_runner()
    row = study.row_for(prompt)
    run = study.PRIOR / "run" if reused else HERE / "run"
    endpoint = study.PRIOR / "endpoint_pr4523" if reused else study.ENDPOINT
    record = runner.valid_completed_record(run, row)
    if record is None:
        raise ValueError("all160 rows must have actual successful outputs")
    paths = runner.paths(run, row)
    job = study.load(paths["job"])
    expected = {
        "digitalTwinId": runner.DEVICE_MAP[prompt["device_id"]],
        "cameraId": prompt["source_camera_name"],
        "prompt": prompt["text"],
    }
    if job["request"] != expected or str(job["submit_response"]["jobId"]) != record["job_id"]:
        raise ValueError("output does not bind the exact frozen scene/product/view")
    if record["lineage"]["source_commit"] != study.COMMIT:
        raise ValueError("output is from another pipeline")
    native = endpoint / "run/jobs" / record["job_id"]
    inputs = endpoint / "run/pipeline/rows" / record["job_id"]
    calls = study.load(native / "calls.json")
    if len(calls) != 4 or any(call["status"] != "done" for call in calls):
        raise ValueError("native four-call ledger is incomplete")
    kinds = Counter()
    models = Counter()
    for call in calls:
        request = study.load(native / call["requestArtifact"])
        response = study.load(native / call["responseArtifact"])
        if (
            runner.canonical_sha256(request) != call["requestSha256"]
            or runner.canonical_sha256(response) != call["responseSha256"]
        ):
            raise ValueError("native request/response hash binding differs")
        kinds.update([call["kind"]])
        models.update([request["model"]])
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
                raise ValueError("native image settings/input/final prompt changed")
            raw = base64.b64decode(response["data"][0]["b64_json"])
            if (
                hashlib.sha256(raw).hexdigest() != call["outputSha256"]
                or call["outputSha256"] != record["image_sha256"]
            ):
                raise ValueError("saved image is not the raw model output")
            image_request = request
        elif (
            request["model"] != "gpt-6-astra"
            or request["max_completion_tokens"] != 16384
            or request["store"] is not False
            or "temperature" in request
            or "reasoning_effort" in request
        ):
            raise ValueError("native Astra settings changed")
    if kinds != Counter({"chat_json": 3, "image_edit": 1}):
        raise ValueError("unexpected native call mix")
    references = list(inputs.glob("ref_2.*"))
    if len(references) != 1:
        raise ValueError("actual style-reference input is ambiguous")
    geometry = study.load(inputs / "geometry_request.json")["images"]
    if len(geometry) != 2:
        raise ValueError("actual planning inputs changed")
    twin = twins[(expected["digitalTwinId"], expected["cameraId"])]
    hashes = {
        "product": geometry[0]["sha256"],
        "reference": geometry[1]["sha256"],
        "geometry_guide": image_request["image"][0]["sha256"],
    }
    if hashes["product"] != twin["product_sha256"]:
        raise ValueError("actual product input differs from the original frozen view")
    source_paths = {
        "product": inputs / "input.png",
        "reference": references[0],
        "geometry_guide": inputs / "geometry_guide.png",
    }
    assets = {}
    for role, path in source_paths.items():
        body = path.read_bytes()
        if hashlib.sha256(body).hexdigest() != hashes[role]:
            raise ValueError("native model input differs from its request hash")
        with Image.open(io.BytesIO(body)) as image:
            dimensions, fmt = image.size, image.format
            image.verify()
        if role != "reference" and dimensions != (2368, 1776):
            raise ValueError("native prepared product/guide dimensions changed")
        suffix = {"PNG": "png", "WEBP": "webp", "JPEG": "jpg"}[fmt]
        assets[role] = {"path": str(path), "sha256": hashes[role], "suffix": suffix, "size": list(dimensions)}
    with Image.open(paths["image"]) as image:
        if image.size != (2368, 1776) or image.format != "PNG":
            raise ValueError("final image must remain the full-resolution raw PNG")
    audit = {
        "study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
        "record_sha256": study.sha(paths["record"]),
        "job_id": record["job_id"],
        "reuse_status": "reused" if reused else "new",
        "native_calls": calls,
        "models": dict(models),
        "new_model_calls_for_audit": 0,
        **assets,
    }
    emit(HERE / "input_audit" / (row["row_slug"] + ".json"), audit)
    return audit
