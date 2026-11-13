#!/usr/bin/env python3
"""Build and hash-verify the unified HP writer/pipeline comparison publication."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import mimetypes
import shlex
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("hp_study", HERE / "study.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)
PUBLIC = HERE / "public"


def image_evidence(body, expected_sha=None, expected_size=None):
    from PIL import Image

    digest = hashlib.sha256(body).hexdigest()
    if expected_sha is not None and digest != expected_sha:
        raise ValueError("actual model-input image differs from its frozen hash")
    with Image.open(io.BytesIO(body)) as image:
        size, image_format = image.size, image.format
        image.verify()
    if expected_size is not None and size != expected_size:
        raise ValueError("actual model-input image differs from its frozen dimensions")
    extension = {"PNG": "png", "WEBP": "webp", "JPEG": "jpg"}.get(image_format)
    if extension is None:
        raise ValueError(f"unsupported model-input image format: {image_format}")
    path = HERE / "input_audit/assets" / f"{digest}.{extension}"
    if path.exists() and study.sha(path) != digest:
        raise ValueError(f"cached model-input bytes changed: {path}")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
    return {"path": str(path), "sha256": digest, "bytes": len(body), "size": list(size)}


def audit_path(cell, row):
    return HERE / "input_audit" / cell["name"] / (row["row_slug"] + ".json")


def checked_audit(path, record_path):
    audit = study.load(path)
    if (audit["study_manifest_sha256"] != study.sha(HERE / "study_manifest.json")
            or audit["record_sha256"] != study.sha(record_path)):
        raise ValueError(f"model-input audit no longer binds this study/record: {path}")
    for role in ("product", "reference", "geometry_guide"):
        if study.sha(Path(audit[role]["path"])) != audit[role]["sha256"]:
            raise ValueError(f"model-input audit asset changed: {path} / {role}")
    return audit


def collect_inputs():
    """Fetch native job artifacts only; never submit or repeat a model call."""
    import httpx

    manifest = study.verified_manifest()
    runner = study.image_runner()
    bundle = study.load(HERE / "endpoint_pr4523/input_bundle/manifest.json")
    twins = {(item["digital_twin_id"], item["camera_id"]): item for item in bundle["entries"]}
    counts = {}
    with httpx.Client(timeout=120) as client:
        for cell in manifest["cells"]:
            run_dir = Path(cell["run_dir"])
            count = 0
            for prompt in study.load(Path(cell["selected"]))["prompts"]:
                row = {"row_id": prompt["prompt_key"], "row_slug": runner.slug(prompt["prompt_key"]),
                       "prompt_sha256": hashlib.sha256(prompt["text"].encode()).hexdigest()}
                record = runner.valid_completed_record(run_dir, row)
                if record is None:
                    continue
                paths = runner.paths(run_dir, row)
                receipt = audit_path(cell, row)
                if receipt.is_file():
                    checked_audit(receipt, paths["record"])
                    count += 1
                    continue
                job = study.load(paths["job"])
                request = job["request"]
                twin = twins[(request["digitalTwinId"], request["cameraId"])]
                if request["prompt"] != prompt["text"] or job["submit_response"]["jobId"] != record["job_id"]:
                    raise ValueError("actual-input audit job/prompt binding mismatch")
                status = study.load(paths["status"])
                version = status["stages"]["hero"]["detail"].get("productVersion")
                if cell["pr"] == "pr4417" and version != twin["product_version"]:
                    raise ValueError("remote productVersion differs from frozen local input")
                sources = {}
                if cell["pr"] == "pr4523":
                    native = HERE / "endpoint_pr4523/run/pipeline/rows" / record["job_id"]
                    references = list(native.glob("ref_2.*"))
                    if len(references) != 1:
                        raise ValueError(f"expected exactly one native Astra reference: {native}")
                    source_paths = {"product": native / "input.png", "reference": references[0],
                                    "geometry_guide": native / "geometry_guide.png"}
                    bodies = {role: path.read_bytes() for role, path in source_paths.items()}
                    sources = {role: str(path) for role, path in source_paths.items()}
                    geometry = study.load(native / "geometry_request.json")["images"]
                    image_call = study.load(
                        HERE / "endpoint_pr4523/run/jobs" / record["job_id"] / "04_image_edit.request.json"
                    )["image"]
                    if len(geometry) != 2 or len(image_call) != 1:
                        raise ValueError("native model-image input cardinality changed")
                    expected = {"product": geometry[0]["sha256"], "reference": geometry[1]["sha256"],
                                "geometry_guide": image_call[0]["sha256"]}
                else:
                    expected = {"product": twin["product_sha256"], "reference": None, "geometry_guide": None}
                    bodies = {}
                    for role, filename in (("product", "hp16_product.png"), ("reference", "hp16_reference.png"),
                                           ("geometry_guide", "hp16_geometry_guide.png")):
                        url = (cell["lineage_args"]["endpoint_base_url"] + "/api/jobs/"
                               + record["job_id"] + "/artifacts/" + filename)
                        response = client.get(url)
                        response.raise_for_status()
                        bodies[role], sources[role] = response.content, url
                if hashlib.sha256(bodies["product"]).hexdigest() != twin["product_sha256"]:
                    raise ValueError("actual product PNG differs from frozen local input")
                assets = {role: image_evidence(body, expected[role], (2368, 1776) if role != "reference" else None)
                          for role, body in bodies.items()}
                write(receipt, {
                    "study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
                    "record_sha256": study.sha(paths["record"]), "job_id": record["job_id"],
                    "digital_twin_id": request["digitalTwinId"], "camera_id": request["cameraId"],
                    "expected_product_version": twin["product_version"], "reported_product_version": version,
                    "sources": sources, **assets,
                    "evidence": ("Native planning/reference and image-guide request SHA-256 bindings verified."
                                 if cell["pr"] == "pr4523" else
                                 "Native job artifact exports; actual product bytes/version match frozen inputs. "
                                 "Remote API exposes input filenames, not model-request image hashes."),
                    "new_model_calls": 0,
                })
                count += 1
            counts[cell["name"]] = count
    write(HERE / "input_audit/summary.json", {"verified_at_utc": datetime.now(timezone.utc).isoformat(),
                                            "cells": counts, "new_model_calls": 0})
    print(json.dumps({"actual_input_audits": counts}))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, str):
        path.write_text(value, encoding="utf-8")
    else:
        path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def copy_asset(source, relative, expected=None):
    digest = study.sha(source)
    if expected is not None and digest != expected:
        raise ValueError(f"source artifact hash mismatch: {source}")
    target = PUBLIC / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.is_file() or study.sha(target) != digest:
        shutil.copyfile(source, target)
    return "../" + relative


def cell_output(cell, prompt, runner, *, historical=False):
    run_dir = Path(cell["run_dir"])
    row = {
        "row_id": prompt["prompt_key"], "row_slug": runner.slug(prompt["prompt_key"]),
        "prompt_sha256": hashlib.sha256(prompt["text"].encode()).hexdigest(),
    }
    record_path = runner.paths(run_dir, row)["record"]
    record = runner.valid_completed_record(run_dir, row)
    if record is None:
        if record_path.is_file():
            return {"status": "failed", "error": study.load(record_path).get("error", "invalid image binding")}
        return {"status": "pending", "error": None}
    if record.get("prompt") != prompt["text"]:
        raise ValueError(f"record text differs from selected prompt: {record_path}")
    if not isinstance(record.get("scene_debug", {}).get("finalPrompt"), str) or not record["scene_debug"]["finalPrompt"].strip():
        raise ValueError(f"completed image has no exact image-model prompt: {record_path}")
    name = "historical" if historical else cell["name"]
    relative = f"assets/{name}/{row['row_slug']}.png"
    image = copy_asset(runner.paths(run_dir, row)["image"], relative, record["image_sha256"])
    record_url = copy_asset(record_path, f"data/records/{name}/{row['row_slug']}.json")
    guide = None
    guide_path = runner.paths(run_dir, row)["guide"]
    if not guide_path.is_file() and not historical and cell["pr"] == "pr4523":
        guide_path = HERE / "endpoint_pr4523/run/jobs" / str(record["job_id"]) / "hp16_geometry_guide.png"
    if guide_path.is_file():
        guide = copy_asset(guide_path, f"assets/{name}/{row['row_slug']}.guide.png")
    inputs = None
    if not historical and audit_path(cell, row).is_file():
        receipt_path = audit_path(cell, row)
        audit = checked_audit(receipt_path, record_path)
        inputs = {role: copy_asset(Path(audit[role]["path"]),
                                  "assets/model_inputs/" + Path(audit[role]["path"]).name,
                                  audit[role]["sha256"])
                  for role in ("product", "reference", "geometry_guide")}
        inputs["audit_url"] = copy_asset(receipt_path, f"data/input_audits/{name}/{row['row_slug']}.json")
        guide = inputs["geometry_guide"]
    return {
        "status": "done", "image": image, "guide": guide, "record_url": record_url,
        "inputs": inputs,
        "image_sha256": record["image_sha256"], "job_id": record["job_id"],
        "lineage": record["lineage"], "scene_debug": record["scene_debug"],
        "judgment": "not evaluated; historical judge regression is a different image set",
    }


def build():
    manifest = study.verified_manifest()
    runner = study.image_runner()
    selected = {writer: study.load(HERE / f"selection/exports/selected_{writer}_30.json")
                for writer in ("v6_2", "v6_3")}
    by_key = {writer: {study.paired_key(row): row for row in document["prompts"]}
              for writer, document in selected.items()}
    if set(by_key["v6_2"]) != set(by_key["v6_3"]):
        raise ValueError("publication inputs are not rank paired")
    full_v63 = study.load(study.V63)
    full_v62 = study.load(study.BASELINE)
    old_dir = study.LEGACY / "runs/generated_surface_shape_r1_env2"
    old_manifest = study.load(old_dir / "run_manifest.json")
    if old_manifest["prompts_sha256"] != study.sha(study.BASELINE):
        raise ValueError("historical gallery source differs from the frozen V6.2 prompt set")
    rows = []
    for key in sorted(by_key["v6_3"]):
        prompts = {writer: by_key[writer][key] for writer in by_key}
        v62 = prompts["v6_2"]
        twin_name = f"{v62['device_id']}__{v62['source_camera_name']}.png"
        twin_source = old_dir / "twins" / twin_name
        twin_manifest = study.load(old_dir / "twin_manifest.json")
        twin = copy_asset(twin_source, "assets/twins/" + twin_name,
                          twin_manifest["assets"][twin_name]["sha256"])
        outputs = {cell["name"]: cell_output(cell, prompts[cell["writer"]], runner)
                   for cell in manifest["cells"]}
        historical = cell_output({"run_dir": str(old_dir)}, v62, runner, historical=True)
        if historical["status"] != "done":
            raise ValueError(f"the selected historical baseline image is unavailable: {key}")
        source_inputs = {}
        for writer, document in (("v6_2", full_v62), ("v6_3", full_v63)):
            prompt = prompts[writer]
            audit = document["bank_audit"][prompt["bank_debug_ref"]]
            source_inputs[writer] = audit["source_input"]
        if source_inputs["v6_2"] != source_inputs["v6_3"]:
            raise ValueError(f"rank-paired writer source inputs differ: {key}")
        rows.append({
            "key": list(key), "device": v62["device_display_name"],
            "camera": v62["source_camera_name"], "rank": v62["bank_rank"],
            "twin": twin, "twin_sha256": study.sha(twin_source),
            "prompts": prompts, "source_input": source_inputs["v6_3"],
            "outputs": outputs, "historical": historical,
        })
    for source, target in (
        (study.V63, "data/prompts_all_v6_3_160.json"),
        (study.V63.with_suffix(".txt"), "data/prompts_all_v6_3_160.txt"),
        (study.BASELINE, "data/prompts_all_v6_2_160.json"),
        (HERE / "study_manifest.json", "data/study_manifest.json"),
        (HERE / "selection/exports/selection_report.json", "data/selection_report.json"),
    ):
        copy_asset(source, target)
    for writer in selected:
        for suffix in ("json", "txt"):
            copy_asset(HERE / f"selection/exports/selected_{writer}_30.{suffix}",
                       f"data/selected_{writer}_30.{suffix}")
    counts = study.validate_cells(manifest, require_complete=False)
    audited = sum(bool(output.get("inputs")) for row in rows for output in row["outputs"].values())
    data = {
        "version": "hp-v62-v63-exact-pr-comparison-report-v1",
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "complete" if all(value["done"] == 30 for value in counts.values()) and audited == 120 else "in_progress",
        "actual_input_audits": audited,
        "cells": counts, "manifest": manifest,
        "selection_report": study.load(HERE / "selection/exports/selection_report.json"),
        "rows": rows, "all_v63": full_v63,
        "judge": {"status": "pending", "notice": "Separate historical128-image V3/V3.1 regression; not new-image judgments."},
    }
    judge_pointer = HERE / "judge_publication.json"
    if judge_pointer.is_file():
        judge = study.load(judge_pointer)
        for source_name, target_name in (("html", "judge/comparison.html"), ("json", "judge/comparison.json")):
            copy_asset(Path(judge[source_name]), target_name, judge[source_name + "_sha256"])
        data["judge"] = {**judge, "html_url": "../judge/comparison.html", "json_url": "../judge/comparison.json"}
        if "r1_json" in judge:
            data["judge"]["r1_json_url"] = copy_asset(
                Path(judge["r1_json"]), "judge/r1-comparison.json", judge["r1_json_sha256"]
            )
    write(PUBLIC / "data/comparison.json", data)
    for name in ("index.html", "main.js", "style.css"):
        copy_asset(HERE / "gallery" / name, "gallery/" + name)
    auth = study.PROJECT / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/imsauth.js"
    copy_asset(auth, "gallery/imsauth.js")
    assets = {path.relative_to(PUBLIC).as_posix(): {"bytes": path.stat().st_size, "sha256": study.sha(path)}
              for path in sorted(PUBLIC.rglob("*")) if path.is_file() and path.name != "asset_manifest.json"}
    write(PUBLIC / "asset_manifest.json", {
        "study_manifest_sha256": study.sha(HERE / "study_manifest.json"), "assets": assets,
    })
    print(json.dumps({"status": data["status"], "cells": counts, "public_artifacts": len(assets) + 1}))


def s3_client(credentials_file):
    import boto3

    values = {}
    allowed = {"AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN", "AWS_REGION", "AWS_DEFAULT_REGION"}
    for raw in credentials_file.read_text().splitlines():
        line = raw.strip()
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() in allowed:
            parts = shlex.split(value, comments=True)
            if len(parts) != 1:
                raise ValueError("malformed temporary AWS credential assignment")
            values[key.strip()] = parts[0]
    required = {"AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"}
    if not required <= values.keys():
        raise ValueError("temporary credential file is incomplete")
    return boto3.client(
        "s3", region_name=values.get("AWS_REGION", values.get("AWS_DEFAULT_REGION", "us-west-2")),
        aws_access_key_id=values["AWS_ACCESS_KEY_ID"], aws_secret_access_key=values["AWS_SECRET_ACCESS_KEY"],
        aws_session_token=values["AWS_SESSION_TOKEN"],
    )


def publish(credentials_file):
    from botocore.exceptions import ClientError

    study.verified_manifest()
    client = s3_client(credentials_file)
    study_hash = study.sha(HERE / "study_manifest.json")
    receipt_path = HERE / "publication_receipt.json"
    previous = study.load(receipt_path)["objects"] if receipt_path.is_file() else {}
    paths = sorted(path for path in PUBLIC.rglob("*") if path.is_file())
    if not (PUBLIC / "asset_manifest.json").is_file():
        raise FileNotFoundError("build the allowlisted publication first")
    expected_assets = study.load(PUBLIC / "asset_manifest.json")["assets"]
    allowlist = set(expected_assets) | {"asset_manifest.json"}
    if {path.relative_to(PUBLIC).as_posix() for path in paths} != allowlist:
        raise ValueError("public directory differs from its explicit asset manifest")

    def upload(path):
        relative = path.relative_to(PUBLIC).as_posix()
        key = study.PREFIX + "/" + relative
        digest, size = study.sha(path), path.stat().st_size
        if relative in expected_assets and expected_assets[relative] != {"sha256": digest, "bytes": size}:
            raise ValueError(f"public artifact changed after its manifest was built: {relative}")
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        head = None
        try:
            head = client.head_object(Bucket=study.BUCKET, Key=key)
        except ClientError as error:
            if error.response["Error"]["Code"] not in {"404", "NoSuchKey", "NotFound"}:
                raise
        if head and head.get("Metadata", {}).get("hp-study-sha256") != study_hash:
            raise FileExistsError(f"refusing to overwrite an object not owned by this study: {key}")
        if not head or (head.get("Metadata", {}).get("sha256") != digest
                        or head["ContentLength"] != size or head["ContentType"] != content_type):
            client.upload_file(str(path), study.BUCKET, key, ExtraArgs={
                "ContentType": content_type, "CacheControl": "no-cache",
                "Metadata": {"sha256": digest, "hp-study-sha256": study_hash},
            })
            head = client.head_object(Bucket=study.BUCKET, Key=key)
        cached = previous.get(relative, {})
        if cached.get("sha256") == digest and cached.get("etag") == head["ETag"] and cached.get("bytes") == size:
            return relative, cached
        response = client.get_object(Bucket=study.BUCKET, Key=key)
        remote = hashlib.sha256()
        remote_size = 0
        try:
            for block in response["Body"].iter_chunks(chunk_size=1024 * 1024):
                remote.update(block)
                remote_size += len(block)
        finally:
            response["Body"].close()
        if remote.hexdigest() != digest or remote_size != size or response["ContentType"] != content_type:
            raise ValueError(f"published bytes/content type differ: {key}")
        return relative, {"sha256": digest, "bytes": size, "etag": response["ETag"],
                          "content_type": content_type, "verification": "downloaded_sha256"}

    with ThreadPoolExecutor(max_workers=8) as pool:
        objects = dict(pool.map(upload, paths))
    write(receipt_path, {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(), "study_manifest_sha256": study_hash,
        "objects": objects, "object_count": len(objects),
        "url": f"https://foundry-aws-corp.adobe.io/asset/{study.BUCKET}/{study.PREFIX}/gallery/index.html",
    })
    print(json.dumps({"published_verified_objects": len(objects), "url": study.load(receipt_path)["url"]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "publish", "collect-inputs"))
    parser.add_argument("--credentials-file", type=Path)
    args = parser.parse_args()
    if args.command == "collect-inputs":
        collect_inputs()
    elif args.command == "build":
        build()
    else:
        if args.credentials_file is None:
            parser.error("--credentials-file is required for publication")
        publish(args.credentials_file)
