"""Audit all160 outputs and stage assets for the third-column report extension."""
from __future__ import annotations

import argparse
import base64
from collections import Counter
import hashlib
import io
import json
from pathlib import Path

from PIL import Image

import study

HERE = study.HERE
PUBLIC = HERE / "public"
ROLES = ("product", "reference", "geometry_guide")
GATEWAY = "https://foundry-aws-corp.adobe.io/asset/" + study.BUCKET + "/"
BASE = GATEWAY + study.PREFIX + "/"
PRIOR_PREFIX = "eval_sets/" + study.PRIOR.name


def emit(path, value):
    body = value if isinstance(value, bytes) else (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()
    path = Path(path)
    if path.exists():
        if path.read_bytes() != body:
            raise ValueError("saved report evidence changed: " + str(path))
        return
    study.write(path, body)


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
    expected = {"digitalTwinId": runner.DEVICE_MAP[prompt["device_id"]],
                "cameraId": prompt["source_camera_name"], "prompt": prompt["text"]}
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
        if (runner.canonical_sha256(request) != call["requestSha256"]
                or runner.canonical_sha256(response) != call["responseSha256"]):
            raise ValueError("native request/response hash binding differs")
        kinds.update([call["kind"]])
        models.update([request["model"]])
        if call["kind"] == "image_edit":
            settings = {"model": "gpt-image-2.5-sunburst-2026-09-08", "n": 1,
                        "size": "2368x1776", "quality": "high", "output_format": "png",
                        "background": "opaque", "imageInputOrder": ["hp16_geometry_guide.png"]}
            if (any(request.get(key) != value for key, value in settings.items())
                    or len(request["image"]) != 1 or request.get("mask")
                    or request["prompt"] != record["scene_debug"]["finalPrompt"]):
                raise ValueError("native image settings/input/final prompt changed")
            raw = base64.b64decode(response["data"][0]["b64_json"])
            if hashlib.sha256(raw).hexdigest() != call["outputSha256"] or call["outputSha256"] != record["image_sha256"]:
                raise ValueError("saved image is not the raw model output")
            image_request = request
        elif (request["model"] != "gpt-6-astra" or request["max_completion_tokens"] != 16384
              or request["store"] is not False or "temperature" in request or "reasoning_effort" in request):
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
    hashes = {"product": geometry[0]["sha256"], "reference": geometry[1]["sha256"],
              "geometry_guide": image_request["image"][0]["sha256"]}
    if hashes["product"] != twin["product_sha256"]:
        raise ValueError("actual product input differs from the original frozen view")
    source_paths = {"product": inputs / "input.png", "reference": references[0],
                    "geometry_guide": inputs / "geometry_guide.png"}
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
        assets[role] = {"path": str(path), "sha256": hashes[role], "suffix": suffix,
                        "size": list(dimensions)}
    with Image.open(paths["image"]) as image:
        if image.size != (2368, 1776) or image.format != "PNG":
            raise ValueError("final image must remain the full-resolution raw PNG")
    audit = {"study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
             "record_sha256": study.sha(paths["record"]), "job_id": record["job_id"],
             "reuse_status": "reused" if reused else "new", "native_calls": calls,
             "models": dict(models), "new_model_calls_for_audit": 0, **assets}
    emit(HERE / "input_audit" / (row["row_slug"] + ".json"), audit)
    return audit


def collect_inputs():
    manifest = study.verify()
    if study.counts()["done"] != 160:
        raise ValueError("wait for all160 outputs before final auditing")
    twins = {(row["digital_twin_id"], row["camera_id"]): row for row in
             study.load(study.ENDPOINT / "input_bundle/manifest.json")["entries"]}
    reused = {row["prompt_key"]: row for row in manifest["reused"]}
    models, new_models = Counter(), Counter()
    ids, hashes = set(), set()
    for prompt in study.load(study.SOURCE)["prompts"]:
        audit = audit_one(prompt, twins, reused.get(prompt["prompt_key"]))
        models.update(audit["models"])
        if prompt["prompt_key"] not in reused:
            new_models.update(audit["models"])
        run = study.PRIOR / "run" if prompt["prompt_key"] in reused else HERE / "run"
        record = study.image_runner().valid_completed_record(run, study.row_for(prompt))
        ids.add(record["job_id"])
        hashes.add(record["image_sha256"])
    journal = [json.loads(line) for line in (HERE / "run/journals/events.jsonl").read_text().splitlines()]
    submitted = [row["row_id"] for row in journal if row["event"] == "submit_started"]
    if len(submitted) != len(set(submitted)) or set(submitted) != set(manifest["new_row_ids"]):
        raise ValueError("submissions do not equal exactly the authorized130 new IDs")
    native = [p for p in (study.ENDPOINT / "run/jobs").iterdir() if p.is_dir()]
    if len(native) != 130 or len(ids) != 160 or len(hashes) != 160:
        raise ValueError("native jobs or output identities do not reconcile")
    if new_models != Counter({"gpt-6-astra": 390, "gpt-image-2.5-sunburst-2026-09-08": 130}):
        raise ValueError("new native call accounting does not reconcile")
    emit(HERE / "generation_audit.json", {"status": "passed", "at_utc": study.now(), "rows": 160,
        "reused": 30, "new": 130, "new_submissions": 130, "failures": 0, "replacements": 0,
        "unique_jobs": len(ids), "unique_raw_pngs": len(hashes),
        "combined_models": dict(models), "new_models": dict(new_models),
        "all_native_request_response_and_raw_output_hashes_verified": True})
    print(json.dumps({"actual_input_audits": 160, "new_models": dict(new_models)}), flush=True)


def copy_asset(path, relative, expected=None):
    path = Path(path)
    body = path.read_bytes()
    if expected is not None and hashlib.sha256(body).hexdigest() != expected:
        raise ValueError("public source asset changed")
    emit(PUBLIC / relative, body)
    return BASE + relative


def build():
    manifest = study.verify()
    audit = study.load(HERE / "generation_audit.json")
    if audit["status"] != "passed" or audit["rows"] != 160:
        raise ValueError("all160 final audits are required")
    source = study.load(study.SOURCE)
    reused = {row["prompt_key"]: row for row in manifest["reused"]}
    rows = []
    for prompt in source["prompts"]:
        row = study.row_for(prompt)
        old = reused.get(prompt["prompt_key"])
        run = study.PRIOR / "run" if old else HERE / "run"
        paths = study.image_runner().paths(run, row)
        record = study.image_runner().valid_completed_record(run, row)
        audit_path = HERE / "input_audit" / (row["row_slug"] + ".json")
        inputs = study.load(audit_path)
        if inputs["record_sha256"] != study.sha(paths["record"]):
            raise ValueError("audited record changed before publication")
        if old:
            image_url = GATEWAY + PRIOR_PREFIX + "/assets/outputs/" + row["row_slug"] + ".png"
            input_urls = {role: GATEWAY + PRIOR_PREFIX + "/assets/inputs/" +
                          inputs[role]["sha256"] + "." + inputs[role]["suffix"] for role in ROLES}
        else:
            image_url = copy_asset(paths["image"], "assets/outputs/" + row["row_slug"] + ".png",
                                   record["image_sha256"])
            input_urls = {role: copy_asset(inputs[role]["path"], "assets/inputs/" +
                          inputs[role]["sha256"] + "." + inputs[role]["suffix"], inputs[role]["sha256"])
                          for role in ROLES}
        input_urls["audit_url"] = copy_asset(audit_path, "data/input_audits/" + audit_path.name)
        output = {"status": "done", "error": None, "reuse_status": "reused" if old else "new",
            "image": image_url, "inputs": input_urls, "job_id": record["job_id"],
            "image_sha256": record["image_sha256"], "run_sha256": record["run_sha256"],
            "record_sha256": study.sha(paths["record"]), "lineage": record["lineage"],
            "origin_study_manifest_sha256": study.sha(study.PRIOR / "study_manifest.json") if old
                else study.sha(HERE / "study_manifest.json"), "scene_debug": record["scene_debug"],
            "record_url": copy_asset(paths["record"], "data/records/" + paths["record"].name),
            "job_url": copy_asset(paths["job"], "data/jobs/" + paths["job"].name),
            "status_url": copy_asset(paths["status"], "data/status/" + paths["status"].name)}
        bank = source["bank_audit"][prompt["bank_debug_ref"]]
        rows.append({"key": [prompt["device_id"], prompt["camera_tag"], prompt["bank_rank"]],
                     "prompt": prompt, "source_input": bank["source_input"], "bank_audit": bank,
                     "output": output})
    emit(PUBLIC / "data/generation.json", {"title": study.TITLE, "status": "complete",
        "built_at_utc": study.now(), "counts": study.counts(), "actual_input_audits": 160,
        "matching": "device/camera/bank rank; not semantic equivalence", "rows": rows})
    copy_asset(manifest["source_export"], "data/prompts_all_v6_4_160.json",
               manifest["source_export_sha256"])
    copy_asset(Path(manifest["source_export"]).with_suffix(".txt"), "data/prompts_all_v6_4_160.txt")
    copy_asset(HERE / "study_manifest.json", "data/study_manifest.json")
    assets = {p.relative_to(PUBLIC).as_posix(): {"sha256": study.sha(p), "bytes": p.stat().st_size}
              for p in sorted(PUBLIC.rglob("*")) if p.is_file() and p.name != "asset_manifest.json"}
    emit(PUBLIC / "asset_manifest.json", {"assets": assets,
        "study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
        "reused_images_referenced_in_place": 30, "new_image_uploads": 130})
    print(json.dumps({"rows": 160, "public_objects": len(assets) + 1, "image_uploads": 130}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("collect-inputs", "build"))
    args = parser.parse_args()
    {"collect-inputs": collect_inputs, "build": build}[args.command]()
