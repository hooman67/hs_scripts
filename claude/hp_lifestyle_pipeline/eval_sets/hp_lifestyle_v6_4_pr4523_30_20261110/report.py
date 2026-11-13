#!/usr/bin/env python3
"""Audit actual native inputs and publish separate detailed and minimal FE reports."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
import mimetypes
from pathlib import Path

from PIL import Image

import study

HERE = study.HERE
PUBLIC = HERE / "public"
VENDOR = Path.home() / ".claude/scripts/fe_html"
BASE = "https://foundry-aws-corp.adobe.io/asset/" + study.BUCKET + "/" + study.PREFIX + "/"
ROLES = ("product", "reference", "geometry_guide")


def emit(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, bytes):
        path.write_bytes(value)
    else:
        path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def copy_asset(source, relative, expected=None):
    source = Path(source)
    if expected is not None and study.sha(source) != expected:
        raise ValueError(f"asset hash differs: {source}")
    emit(PUBLIC / relative, source.read_bytes())
    return "../" + relative


def native_image(path, expected, size=None):
    body = path.read_bytes()
    digest = hashlib.sha256(body).hexdigest()
    if digest != expected:
        raise ValueError("actual native model input differs from its request hash")
    with Image.open(io.BytesIO(body)) as image:
        dimensions, fmt = image.size, image.format
        image.verify()
    if size is not None and dimensions != size:
        raise ValueError("actual native model input dimensions differ")
    suffix = {"PNG": "png", "WEBP": "webp", "JPEG": "jpg"}[fmt]
    target = HERE / "input_audit/assets" / f"{digest}.{suffix}"
    if target.exists() and study.sha(target) != digest:
        raise ValueError("cached input bytes changed")
    if not target.exists():
        study.write(target, body)
    return {"path": str(target), "sha256": digest, "bytes": len(body), "size": list(dimensions)}


def collect_inputs():
    study.verify()
    runner = study.image_runner()
    selected = study.load(HERE / "selection/selected_v6_4_30.json")["prompts"]
    twins = {(t["digital_twin_id"], t["camera_id"]): t for t in
             study.load(study.ENDPOINT / "input_bundle/manifest.json")["entries"]}
    done = 0
    for prompt in selected:
        row = {"row_id": prompt["prompt_key"], "row_slug": runner.slug(prompt["prompt_key"]),
               "prompt_sha256": prompt["text_sha256"]}
        record = runner.valid_completed_record(HERE / "run", row)
        if record is None:
            continue
        paths = runner.paths(HERE / "run", row)
        job = study.load(paths["job"])
        expected_request = {"digitalTwinId": runner.DEVICE_MAP[prompt["device_id"]],
                            "cameraId": prompt["source_camera_name"], "prompt": prompt["text"]}
        if job["request"] != expected_request or str(job["submit_response"]["jobId"]) != record["job_id"]:
            raise ValueError("native job/request does not match the selected source")
        if record["lineage"]["source_commit"] != study.COMMIT:
            raise ValueError("wrong pinned image pipeline")
        native = study.ENDPOINT / "run/pipeline/rows" / record["job_id"]
        refs = list(native.glob("ref_2.*"))
        if len(refs) != 1:
            raise ValueError("native Astra reference is ambiguous")
        geometry = study.load(native / "geometry_request.json")["images"]
        request = study.load(study.ENDPOINT / "run/jobs" / record["job_id"] / "04_image_edit.request.json")
        expected_settings = {
            "model": "gpt-image-2.5-sunburst-2026-09-08", "n": 1, "size": "2368x1776",
            "quality": "high", "output_format": "png", "background": "opaque",
            "imageInputOrder": ["hp16_geometry_guide.png"],
        }
        if (len(geometry) != 2 or len(request["image"]) != 1 or request.get("mask")
                or any(request.get(k) != v for k, v in expected_settings.items())
                or request["prompt"] != record["scene_debug"]["finalPrompt"]):
            raise ValueError("native image request settings/input cardinality changed")
        sources = {"product": native / "input.png", "reference": refs[0],
                   "geometry_guide": native / "geometry_guide.png"}
        expected = {"product": geometry[0]["sha256"], "reference": geometry[1]["sha256"],
                    "geometry_guide": request["image"][0]["sha256"]}
        twin = twins[(expected_request["digitalTwinId"], expected_request["cameraId"])]
        if expected["product"] != twin["product_sha256"]:
            raise ValueError("prepared product differs from the original frozen twin")
        assets = {role: native_image(sources[role], expected[role],
                                    (2368, 1776) if role != "reference" else None) for role in ROLES}
        calls = study.load(study.ENDPOINT / "run/jobs" / record["job_id"] / "calls.json")
        if len(calls) != 4 or any(c["status"] != "done" for c in calls):
            raise ValueError("native model-call ledger is incomplete")
        with Image.open(paths["image"]) as image:
            if image.size != (2368, 1776) or image.format != "PNG":
                raise ValueError("output must be an unmodified2368x1776 PNG")
        receipt = {
            "study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
            "record_sha256": study.sha(paths["record"]), "job_id": record["job_id"],
            "digital_twin_id": expected_request["digitalTwinId"], "camera_id": expected_request["cameraId"],
            "native_image_request_sha256": study.sha(study.ENDPOINT / "run/jobs" /
                                                      record["job_id"] / "04_image_edit.request.json"),
            "native_calls": calls, **assets, "model_calls_for_audit": 0,
        }
        target = HERE / "input_audit" / (row["row_slug"] + ".json")
        if target.exists():
            if study.load(target) != receipt:
                raise ValueError("saved input audit no longer matches native evidence")
        else:
            study.write(target, receipt)
        done += 1
    emit(HERE / "input_audit/summary.json", {"verified_at_utc": study.now(), "rows": done,
                                           "model_calls_for_audit": 0})
    print(json.dumps({"actual_input_audits": done}), flush=True)


def fe_document(rows):
    if len(rows) != 30 or any(r["output"]["status"] != "done" for r in rows):
        raise ValueError("FE report requires all thirty actual completed images")
    manifest = {"rows": [
        {"row_idx": i, "evalset_item_id": " / ".join(map(str, row["key"])),
         "assets": [{"kind": "image", "src": BASE + row["output"]["image"].removeprefix("../"),
                     "label": study.TITLE}]}
        for i, row in enumerate(rows, 1)
    ]}
    vendor = study.module("v64_official_fe_converter", VENDOR / "parquet_to_fe_html.py")
    return vendor.manifest_to_data_json(manifest, is_secure=True, title=study.TITLE)


def build():
    if (HERE / "publication_receipt.json").exists():
        raise FileExistsError("publication already finalized; do not silently rebuild it")
    manifest = study.verify()
    if study.counts() != {"expected": 30, "done": 30, "failed": 0, "pending": 0}:
        raise ValueError("all thirty generation records must complete before publication")
    runner = study.image_runner()
    selected = study.load(HERE / "selection/selected_v6_4_30.json")["prompts"]
    source = study.load(study.TEXT)
    rows = []
    job_ids, hashes = set(), set()
    for prompt in selected:
        row = {"row_id": prompt["prompt_key"], "row_slug": runner.slug(prompt["prompt_key"]),
               "prompt_sha256": prompt["text_sha256"]}
        record = runner.valid_completed_record(HERE / "run", row)
        paths = runner.paths(HERE / "run", row)
        audit_path = HERE / "input_audit" / (row["row_slug"] + ".json")
        audit = study.load(audit_path)
        if (audit["record_sha256"] != study.sha(paths["record"])
                or audit["study_manifest_sha256"] != study.sha(HERE / "study_manifest.json")):
            raise ValueError("actual input audit lost its study/record binding")
        inputs = {role: copy_asset(audit[role]["path"],
                                   "assets/inputs/" + Path(audit[role]["path"]).name,
                                   audit[role]["sha256"]) for role in ROLES}
        inputs["audit_url"] = copy_asset(audit_path, f"data/input_audits/{row['row_slug']}.json")
        output = {
            "status": "done",
            "image": copy_asset(paths["image"], f"assets/outputs/{row['row_slug']}.png",
                                record["image_sha256"]),
            "inputs": inputs, "job_id": record["job_id"], "image_sha256": record["image_sha256"],
            "record_url": copy_asset(paths["record"], f"data/records/{row['row_slug']}.json"),
            "lineage": record["lineage"], "scene_debug": record["scene_debug"],
        }
        job_ids.add(record["job_id"])
        hashes.add(record["image_sha256"])
        rows.append({"key": list(study.slot(prompt)), "prompt": prompt,
                     "source_input": source["bank_audit"][prompt["bank_debug_ref"]]["source_input"],
                     "output": output})
    if len(job_ids) != 30 or len(hashes) != 30:
        raise ValueError("duplicate actual jobs or generated image bytes")
    document = {"title": study.TITLE, "status": "complete", "built_at_utc": study.now(),
                "matching": "device/camera/bank rank; not semantic equivalence",
                "normal_reference_selection": True, "actual_input_audits": 30,
                "study_manifest": manifest, "rows": rows}
    emit(PUBLIC / "data/generation.json", document)
    for suffix in ("json", "txt"):
        copy_asset(HERE / f"selection/selected_v6_4_30.{suffix}", f"data/selected_v6_4_30.{suffix}")
    copy_asset(HERE / "study_manifest.json", "data/study_manifest.json")
    for name in ("index.html", "main.js"):
        copy_asset(HERE / "gallery" / name, "gallery/" + name)
    copy_asset(study.OLD / "gallery/style.css", "gallery/style.css")
    auth = study.PROJECT / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/imsauth.js"
    copy_asset(auth, "gallery/imsauth.js")
    emit(PUBLIC / "fe/data.json", fe_document(rows))
    copy_asset(VENDOR / "annotation_viewer.html", "fe/viewer.html")
    assets = {p.relative_to(PUBLIC).as_posix(): {"sha256": study.sha(p), "bytes": p.stat().st_size}
              for p in sorted(PUBLIC.rglob("*")) if p.is_file() and p.name != "asset_manifest.json"}
    emit(PUBLIC / "asset_manifest.json", {"study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
                                         "assets": assets})
    emit(HERE / "build_audit.json", {
        "status": "complete", "rows": 30, "unique_jobs": 30, "unique_images": 30,
        "actual_input_audits": 30, "fe_images_per_row": 1, "title": study.TITLE,
        "asset_manifest_sha256": study.sha(PUBLIC / "asset_manifest.json"),
        "viewer_template_sha256": study.sha(VENDOR / "annotation_viewer.html"),
    })
    print(json.dumps({"built": 30, "public_objects": len(assets) + 1}))


def verify_original(client):
    for expected in study.verify()["baseline_live_objects"].values():
        current = client.get_object(Bucket=study.BUCKET, Key=expected["key"])
        if hashlib.sha256(current["Body"].read()).hexdigest() != expected["sha256"]:
            raise ValueError("original live report changed; inspect it before publication")


def publish():
    from botocore.exceptions import ClientError

    client = study.s3_client()
    verify_original(client)
    browser = study.load(HERE / "browser_validation.json")
    if browser["status"] != "passed" or browser["asset_manifest_sha256"] != study.sha(
            PUBLIC / "asset_manifest.json"):
        raise ValueError("browser validation must bind the current exact report files")
    expected = study.load(PUBLIC / "asset_manifest.json")["assets"]
    paths = sorted(p for p in PUBLIC.rglob("*") if p.is_file())
    if {p.relative_to(PUBLIC).as_posix() for p in paths} != set(expected) | {"asset_manifest.json"}:
        raise ValueError("public directory differs from its explicit allowlist")

    def upload(path):
        relative = path.relative_to(PUBLIC).as_posix()
        body = path.read_bytes()
        digest = hashlib.sha256(body).hexdigest()
        if relative in expected and expected[relative] != {"sha256": digest, "bytes": len(body)}:
            raise ValueError("public artifact changed after build")
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if path.suffix == ".html":
            content_type = "text/html; charset=utf-8"
        key = study.PREFIX + "/" + relative
        try:
            response = client.get_object(Bucket=study.BUCKET, Key=key)
            existing = response["Body"].read()
        except ClientError as error:
            if error.response["Error"]["Code"] not in {"NoSuchKey", "404"}:
                raise
            existing = None
        if existing is None:
            client.put_object(Bucket=study.BUCKET, Key=key, Body=body, ContentType=content_type,
                              CacheControl="no-cache", Metadata={"sha256": digest}, IfNoneMatch="*")
        elif existing != body:
            raise ValueError(f"refusing to overwrite an existing different object: {key}")
        downloaded = client.get_object(Bucket=study.BUCKET, Key=key)
        if downloaded["Body"].read() != body or downloaded["ContentType"] != content_type:
            raise ValueError("published object bytes/type differ")
        return key, {"sha256": digest, "bytes": len(body), "content_type": content_type,
                     "etag": downloaded["ETag"], "version_id": downloaded.get("VersionId")}

    with ThreadPoolExecutor(max_workers=8) as pool:
        objects = dict(pool.map(upload, paths))
    verify_original(client)
    receipt = {"verified_at_utc": study.now(), "objects": objects, "original_report_unchanged": True,
               "gallery_url": BASE + "gallery/index.html",
               "fe_url": BASE + "fe/viewer.html?ldap=hshariati",
               "verification": "all uploaded objects downloaded and byte/type verified"}
    study.write(HERE / "publication_receipt.json", receipt)
    links = (f"{study.TITLE}\n\nDetailed gallery:\n{receipt['gallery_url']}\n\n"
             f"Clean FE viewer:\n{receipt['fe_url']}\n\n"
             f"Selected30 JSON:\n{BASE}data/selected_v6_4_30.json\n\n"
             f"Selected30 TXT:\n{BASE}data/selected_v6_4_30.txt\n")
    study.write(HERE / "report_links.txt", links)
    print(links)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("collect-inputs", "build", "publish"))
    args = parser.parse_args()
    if args.command == "collect-inputs":
        collect_inputs()
    elif args.command == "build":
        build()
    else:
        publish()
