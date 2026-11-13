#!/usr/bin/env python3
"""Materialize native inputs and publish an owned, byte-verified full160 gallery."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
import mimetypes
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
import study

HERE = study.HERE
PUBLIC = HERE / "public"
ROLES = ("product", "reference", "geometry_guide")


def image_evidence(body, expected=None, size=None):
    from PIL import Image
    digest = hashlib.sha256(body).hexdigest()
    if expected and digest != expected:
        raise ValueError("actual input differs from its native/frozen hash")
    with Image.open(io.BytesIO(body)) as image:
        dimensions, fmt = image.size, image.format
        image.verify()
    if size and dimensions != size:
        raise ValueError("actual input has unexpected dimensions")
    suffix = {"PNG": "png", "WEBP": "webp", "JPEG": "jpg"}[fmt]
    path = HERE / "input_audit/assets" / (digest + "." + suffix)
    if path.exists() and study.sha(path) != digest:
        raise ValueError("cached input was modified")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
    return {"path": str(path), "sha256": digest, "bytes": len(body), "size": list(dimensions)}


def binding(cell, prompt):
    reused = next((r for r in cell["reused"] if r["prompt_key"] == prompt["prompt_key"]), None)
    if reused is None:
        from restart import verified_plan
        plan = verified_plan()
        if (plan and cell["name"] == plan["origin_cell"]
                and prompt["prompt_key"] in plan["interrupted_attempts"]):
            return Path(plan["retry_run"]["run_dir"]), "new", None
    return Path(cell["prior_run_dir"] if reused else cell["run_dir"]), "reused" if reused else "new", reused


def completion_counts(manifest=None):
    manifest = manifest or study.verified_manifest()
    runner = study.image_runner()
    prompts = study.load(study.SOURCE)["prompts"]
    counts = {}
    for cell in manifest["cells"]:
        statuses = []
        for prompt in prompts:
            run_dir, reuse_status, _ = binding(cell, prompt)
            row = study.row_for(prompt)
            record = runner.valid_completed_record(run_dir, row)
            status = "done" if record else (
                "failed" if runner.paths(run_dir, row)["record"].exists() else "pending")
            statuses.append((status, reuse_status))
        done = sum(status == "done" for status, _ in statuses)
        counts[cell["name"]] = {
            "expected": 160, "reused": 30, "new_expected": 130, "new_done": done - 30,
            "failed": sum(status == "failed" for status, _ in statuses),
            "pending": sum(status == "pending" for status, _ in statuses), "done": done,
        }
    return counts


def audit_path(cell, prompt):
    return HERE / "input_audit" / cell["name"] / (study.image_runner().slug(prompt["prompt_key"]) + ".json")


def checked_audit(path, record_path):
    audit = study.load(path)
    if (audit["study_manifest_sha256"] != study.sha(HERE / "study_manifest.json")
            or audit["record_sha256"] != study.sha(record_path)):
        raise ValueError("input evidence lost its study/record binding")
    for role in ROLES:
        if study.sha(audit[role]["path"]) != audit[role]["sha256"]:
            raise ValueError("actual input asset bytes changed")
    return audit


def collect_one(cell, prompt, twins):
    import httpx
    runner = study.image_runner()
    row = study.row_for(prompt)
    run_dir, reuse_status, reused = binding(cell, prompt)
    record = runner.valid_completed_record(run_dir, row)
    if record is None:
        return False
    paths = runner.paths(run_dir, row)
    receipt = audit_path(cell, prompt)
    if receipt.exists():
        checked_audit(receipt, paths["record"])
        return True
    if reused:
        prior_path = study.OLD / "input_audit" / cell["name"] / (row["row_slug"] + ".json")
        prior = study.load(prior_path)
        if (prior["record_sha256"] != study.sha(paths["record"])
                or prior["study_manifest_sha256"] != reused["origin_study_manifest_sha256"]):
            raise ValueError("reused input audit does not bind its original study/record")
        assets = {role: image_evidence(Path(prior[role]["path"]).read_bytes(), prior[role]["sha256"])
                  for role in ROLES}
        study.write(receipt, {**prior, **assets, "study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
                              "reuse_status": reuse_status, "origin_input_audit_path": str(prior_path),
                              "origin_input_audit_sha256": study.sha(prior_path),
                              "origin_study_manifest_sha256": prior["study_manifest_sha256"],
                              "origin_run_sha256": record["run_sha256"], "new_model_calls": 0})
        return True
    job = study.load(paths["job"])
    request = job["request"]
    twin = twins[(request["digitalTwinId"], request["cameraId"])]
    if (request != {"digitalTwinId": row_device(prompt), "cameraId": prompt["source_camera_name"],
                    "prompt": prompt["text"]} or str(job["submit_response"]["jobId"]) != str(record["job_id"])):
        raise ValueError("native input job/prompt identity mismatch")
    status = study.load(paths["status"])
    version = status["stages"]["hero"]["detail"].get("productVersion")
    if cell["pr"] == "pr4417" and version != twin["product_version"]:
        raise ValueError("remote productVersion drift")
    if cell["pr"] == "pr4523":
        native = study.OLD / "endpoint_pr4523/run/pipeline/rows" / record["job_id"]
        refs = list(native.glob("ref_2.*"))
        if len(refs) != 1:
            raise ValueError("native Astra reference is ambiguous")
        sources = {"product": native / "input.png", "reference": refs[0], "geometry_guide": native / "geometry_guide.png"}
        bodies = {role: path.read_bytes() for role, path in sources.items()}
        geometry = study.load(native / "geometry_request.json")["images"]
        call = study.load(study.OLD / "endpoint_pr4523/run/jobs" / record["job_id"] / "04_image_edit.request.json")
        if len(geometry) != 2 or len(call["image"]) != 1:
            raise ValueError("native input cardinality changed")
        expected_settings = {"model": "gpt-image-2.5-sunburst-2026-09-08", "n": 1, "size": "2368x1776",
                             "quality": "high", "output_format": "png", "background": "opaque",
                             "imageInputOrder": ["hp16_geometry_guide.png"]}
        if any(call.get(k) != v for k, v in expected_settings.items()) or call.get("mask"):
            raise ValueError("native image call settings changed")
        if call["prompt"] != record["scene_debug"]["finalPrompt"]:
            raise ValueError("native final prompt differs from saved debug")
        expected = {"product": geometry[0]["sha256"], "reference": geometry[1]["sha256"],
                    "geometry_guide": call["image"][0]["sha256"]}
        evidence = "Native planning/reference and image-guide request SHA-256 bindings and image settings verified."
    else:
        orders = {"imageInputOrder": ["hp16_geometry_guide.png"],
                  "planningInputOrder": ["hp16_product.png", "hp16_reference.png"],
                  "writingInputOrder": ["hp16_geometry_guide.png", "hp16_reference.png", "hp16_product.png"]}
        if any(record["scene_debug"].get(k) != v for k, v in orders.items()):
            raise ValueError("remote input orders changed")
        sources, bodies = {}, {}
        with httpx.Client(timeout=120) as client:
            for role, name in (("product", "hp16_product.png"), ("reference", "hp16_reference.png"),
                               ("geometry_guide", "hp16_geometry_guide.png")):
                url = cell["lineage_args"]["endpoint_base_url"] + "/api/jobs/" + record["job_id"] + "/artifacts/" + name
                response = client.get(url)
                response.raise_for_status()
                sources[role], bodies[role] = url, response.content
        expected = {"product": twin["product_sha256"], "reference": None, "geometry_guide": None}
        evidence = ("Native job exports and declared input order; actual product bytes/version match frozen inputs. "
                    "Remote API exposes input filenames, not model-request image hashes or all image settings.")
    if hashlib.sha256(bodies["product"]).hexdigest() != twin["product_sha256"]:
        raise ValueError("actual product PNG differs from the original frozen16 views")
    assets = {role: image_evidence(bodies[role], expected[role], (2368, 1776) if role != "reference" else None)
              for role in ROLES}
    study.write(receipt, {"study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
                          "record_sha256": study.sha(paths["record"]), "job_id": record["job_id"],
                          "digital_twin_id": request["digitalTwinId"], "camera_id": request["cameraId"],
                          "expected_product_version": twin["product_version"], "reported_product_version": version,
                          "sources": {k: str(v) for k, v in sources.items()}, **assets, "evidence": evidence,
                          "reuse_status": reuse_status, "origin_run_sha256": record["run_sha256"], "new_model_calls": 0})
    return True


def row_device(prompt):
    return study.image_runner().DEVICE_MAP[prompt["device_id"]]


def collect_inputs():
    m = study.verified_manifest()
    bundle = study.load(study.OLD / "endpoint_pr4523/input_bundle/manifest.json")
    twins = {(t["digital_twin_id"], t["camera_id"]): t for t in bundle["entries"]}
    prompts = study.load(study.SOURCE)["prompts"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        counts = {c["name"]: sum(pool.map(lambda p: collect_one(c, p, twins), prompts)) for c in m["cells"]}
    study.write(HERE / "input_audit/summary.json", {"verified_at_utc": study.now(), "cells": counts, "new_model_calls": 0})
    print({"actual_input_audits": counts}, flush=True)


def copy_asset(source, relative, expected=None):
    source = Path(source)
    digest = study.sha(source)
    if expected and expected != digest:
        raise ValueError("public source artifact hash mismatch")
    target = PUBLIC / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or study.sha(target) != digest:
        shutil.copyfile(source, target)
    return "../" + relative


def output(cell, prompt):
    runner = study.image_runner()
    row = study.row_for(prompt)
    run_dir, reuse_status, reused = binding(cell, prompt)
    paths = runner.paths(run_dir, row)
    record = runner.valid_completed_record(run_dir, row)
    base = {"reuse_status": reuse_status, "status": "pending", "error": None}
    if record is None:
        if paths["record"].exists():
            return {**base, "status": "failed", "error": study.load(paths["record"]).get("error"),
                    "record_url": copy_asset(paths["record"], f"data/records/{cell['name']}/{paths['record'].name}")}
        return base
    if record["prompt"] != prompt["text"] or not record["scene_debug"].get("finalPrompt"):
        raise ValueError("output text/final prompt binding mismatch")
    inputs = None
    ap = audit_path(cell, prompt)
    if ap.exists():
        audit = checked_audit(ap, paths["record"])
        inputs = {role: copy_asset(audit[role]["path"], "assets/model_inputs/" + Path(audit[role]["path"]).name,
                                  audit[role]["sha256"]) for role in ROLES}
        inputs["audit_url"] = copy_asset(ap, f"data/input_audits/{cell['name']}/{ap.name}")
    result = {**base, "status": "done",
            "image": copy_asset(paths["image"], f"assets/{cell['name']}/{paths['image'].name}", record["image_sha256"]),
            "record_url": copy_asset(paths["record"], f"data/records/{cell['name']}/{paths['record'].name}"),
            "job_url": copy_asset(paths["job"], f"data/jobs/{cell['name']}/{paths['job'].name}"),
            "status_url": copy_asset(paths["status"], f"data/status/{cell['name']}/{paths['status'].name}"),
            "inputs": inputs, "image_sha256": record["image_sha256"], "job_id": record["job_id"],
            "run_sha256": record["run_sha256"], "record_sha256": study.sha(paths["record"]),
            "origin_study_manifest_sha256": reused["origin_study_manifest_sha256"] if reused else study.sha(HERE / "study_manifest.json"),
            "lineage": record["lineage"], "scene_debug": record["scene_debug"], "judgment": "not evaluated"}
    if not reused and run_dir != Path(cell["run_dir"]):
        from restart import verified_plan
        plan = verified_plan()
        result["restart"] = {"original_interrupted_attempt": plan["interrupted_attempts"][prompt["prompt_key"]],
                             "restart_manifest_sha256": study.sha(HERE / "restart_manifest.json")}
    return result


def build():
    manifest = study.verified_manifest()
    document = study.load(study.SOURCE)
    rows = [{"key": [p["device_id"], p["camera_tag"], p["bank_rank"]], "device": p["device_display_name"],
             "camera": p["source_camera_name"], "rank": p["bank_rank"], "prompt": p,
             "source_input": document["bank_audit"][p["bank_debug_ref"]]["source_input"],
             "bank_audit": document["bank_audit"][p["bank_debug_ref"]],
             "outputs": {c["name"]: output(c, p) for c in manifest["cells"]}}
            for p in document["prompts"]]
    counts = {}
    for cell in manifest["cells"]:
        outputs = [row["outputs"][cell["name"]] for row in rows]
        counts[cell["name"]] = {
            "expected": 160, "reused": 30, "new_expected": 130,
            "new_done": sum(o["status"] == "done" and o["reuse_status"] == "new" for o in outputs),
            "failed": sum(o["status"] == "failed" for o in outputs),
            "pending": sum(o["status"] == "pending" for o in outputs),
            "done": sum(o["status"] == "done" for o in outputs),
        }
    audited = sum(bool(o.get("inputs")) for row in rows for o in row["outputs"].values())
    terminal = all(v["pending"] == 0 for v in counts.values())
    data = {"version": "hp-v63-full160-report-v1", "built_at_utc": study.now(), "cells": counts,
            "status": "complete" if terminal and audited == sum(v["done"] for v in counts.values()) else "in_progress",
            "actual_input_audits": audited, "manifest": manifest, "rows": rows,
            "evidence_limits": ["No judgments or image-quality significance claims.",
                                "Style references and stochastic outputs are not pair-controlled.",
                                "Exact product is instructed, not guaranteed pixel-locked.",
                                manifest["text_evidence_limit"]]}
    from restart import verified_plan
    restart_plan = verified_plan()
    if restart_plan:
        data["restart"] = restart_plan
        copy_asset(HERE / "restart_manifest.json", "data/restart_manifest.json")
    study.write(PUBLIC / "data/comparison.json", data)
    for source, target in ((study.SOURCE, "data/prompts_all_v6_3_160.json"),
                           (study.SOURCE.with_suffix(".txt"), "data/prompts_all_v6_3_160.txt"),
                           (HERE / "study_manifest.json", "data/study_manifest.json")):
        copy_asset(source, target)
    for name in ("index.html", "main.js", "style.css"):
        copy_asset(HERE / "gallery" / name, "gallery/" + name)
    copy_asset(study.PROJECT / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/imsauth.js", "gallery/imsauth.js")
    assets = {p.relative_to(PUBLIC).as_posix(): {"bytes": p.stat().st_size, "sha256": study.sha(p)}
              for p in sorted(PUBLIC.rglob("*")) if p.is_file() and p.name != "asset_manifest.json"}
    study.write(PUBLIC / "asset_manifest.json", {"study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
                                               "assets": assets})
    print({"status": data["status"], "actual_inputs": audited, "cells": counts, "assets": len(assets) + 1}, flush=True)


def s3_client():
    from s3_access import s3_client as scoped_client
    return scoped_client(study.BUCKET)


def publish():
    from botocore.exceptions import ClientError
    study.verified_manifest()
    client = s3_client()
    study_hash = study.sha(HERE / "study_manifest.json")
    previous_path = HERE / "publication_receipt.json"
    previous = study.load(previous_path)["objects"] if previous_path.exists() else {}
    assets = study.load(PUBLIC / "asset_manifest.json")["assets"]
    paths = sorted(p for p in PUBLIC.rglob("*") if p.is_file())
    if {p.relative_to(PUBLIC).as_posix() for p in paths} != set(assets) | {"asset_manifest.json"}:
        raise ValueError("public directory differs from explicit asset allowlist")

    def upload(path):
        relative = path.relative_to(PUBLIC).as_posix()
        key = study.PREFIX + "/" + relative
        digest, size = study.sha(path), path.stat().st_size
        if relative in assets and assets[relative] != {"sha256": digest, "bytes": size}:
            raise ValueError("artifact changed after allowlist was frozen")
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        head = None
        try:
            head = client.head_object(Bucket=study.BUCKET, Key=key)
        except ClientError as error:
            if error.response["Error"]["Code"] not in {"404", "NoSuchKey", "NotFound"}:
                raise
        if head and head.get("Metadata", {}).get("hp-study-sha256") != study_hash:
            raise FileExistsError("refusing to overwrite an object not owned by this study")
        if not head or (head.get("Metadata", {}).get("sha256") != digest or head["ContentLength"] != size
                        or head["ContentType"] != content_type):
            client.upload_file(str(path), study.BUCKET, key, ExtraArgs={"ContentType": content_type,
                               "CacheControl": "no-cache", "Metadata": {"sha256": digest, "hp-study-sha256": study_hash}})
            head = client.head_object(Bucket=study.BUCKET, Key=key)
        cached = previous.get(relative, {})
        if (cached.get("sha256") == digest and cached.get("etag") == head["ETag"]
                and cached.get("bytes") == size and cached.get("verification") == "downloaded_sha256"):
            return relative, cached
        response = client.get_object(Bucket=study.BUCKET, Key=key)
        remote, remote_size = hashlib.sha256(), 0
        try:
            for block in response["Body"].iter_chunks(chunk_size=1024 * 1024):
                remote.update(block)
                remote_size += len(block)
        finally:
            response["Body"].close()
        if remote.hexdigest() != digest or remote_size != size or response["ContentType"] != content_type:
            raise ValueError("published artifact hash/bytes/content-type mismatch")
        return relative, {"sha256": digest, "bytes": size, "etag": response["ETag"],
                          "content_type": content_type, "verification": "downloaded_sha256"}

    # Data and assets land before the gallery entry point, including on the first snapshot.
    entry = PUBLIC / "gallery/index.html"
    with ThreadPoolExecutor(max_workers=8) as pool:
        objects = dict(pool.map(upload, [p for p in paths if p != entry]))
    key, value = upload(entry)
    objects[key] = value
    receipt = {"verified_at_utc": study.now(), "study_manifest_sha256": study_hash,
               "objects": objects, "object_count": len(objects), "authentication": "user-refreshed credential file; frozen shlex allowlist parser; no execution or credential persistence",
               "url": f"https://foundry-aws-corp.adobe.io/asset/{study.BUCKET}/{study.PREFIX}/gallery/index.html"}
    study.write(previous_path, receipt)
    print({"published_verified_objects": len(objects), "url": receipt["url"]}, flush=True)


def final_audit():
    from PIL import Image
    m = study.verified_manifest()
    runner = study.image_runner()
    document = study.load(study.SOURCE)
    bundle = study.load(study.OLD / "endpoint_pr4523/input_bundle/manifest.json")
    twins = {(t["digital_twin_id"], t["camera_id"]): t for t in bundle["entries"]}
    counts = completion_counts(m)
    if any(v["pending"] for v in counts.values()):
        raise ValueError("not all320 outcomes are terminal")
    from restart import verified_plan, submission_guard
    restart_plan = verified_plan()
    if restart_plan:
        submission_guard(require_terminal=True)
    records, job_ids, hashes = [], set(), set()
    for cell in m["cells"]:
        study.submission_guard(cell)
        journal = Path(cell["run_dir"]) / "journals/events.jsonl"
        starts = [json.loads(line) for line in journal.read_text().splitlines()]
        if sum(e["event"] == "submit_started" for e in starts) != 130:
            raise ValueError("expected exactly130 new paid submissions per PR")
        for prompt in document["prompts"]:
            row = study.row_for(prompt)
            run_dir, reuse_status, reused = binding(cell, prompt)
            paths = runner.paths(run_dir, row)
            record = runner.valid_completed_record(run_dir, row)
            if record is None:
                records.append({"cell": cell["name"], "prompt_key": prompt["prompt_key"], "status": "failed",
                                "record_path": str(paths["record"]), "record_sha256": study.sha(paths["record"])})
                continue
            runner.validate_scene_detail(record["scene_debug"], {"prompt": prompt, **row}, record["lineage"],
                                         record.get("image_input_order_evidence"))
            expected_fields = {
                "row_id": prompt["prompt_key"], "device_id": prompt["device_id"],
                "digital_twin_id": row_device(prompt), "camera_id": prompt["source_camera_name"],
                "camera_tag": prompt["camera_tag"], "bank_rank": prompt["bank_rank"],
                "prompt": prompt["text"], "prompt_record_sha256": runner.canonical_sha256(prompt),
            }
            if any(record.get(k) != v for k, v in expected_fields.items()):
                raise ValueError("device/camera/rank/source-record binding mismatch")
            if record["lineage"]["source_commit"] != cell["lineage_args"]["lineage_source_commit"]:
                raise ValueError("record PR source differs")
            if any(record["stage_statuses"].get(s) != "skipped" for s in ("ibl", "backplate", "recomposite", "relight")):
                raise ValueError("unexpected downstream stage")
            with Image.open(paths["image"]) as image:
                if image.format != "PNG" or image.size != (2368, 1776):
                    raise ValueError("output contract mismatch")
                if image.convert("RGBA").getchannel("A").getextrema() != (255, 255):
                    raise ValueError("output is not opaque")
            audit = checked_audit(audit_path(cell, prompt), paths["record"])
            job = study.load(paths["job"])
            expected_request = {"digitalTwinId": row_device(prompt), "cameraId": prompt["source_camera_name"],
                                "prompt": prompt["text"]}
            if (job["request"] != expected_request or job["run_sha256"] != record["run_sha256"]
                    or job["request_sha256"] != runner.canonical_sha256(expected_request)
                    or str(job["submit_response"]["jobId"]) != str(record["job_id"])):
                raise ValueError("job/run/prompt binding mismatch")
            twin = twins[(expected_request["digitalTwinId"], expected_request["cameraId"])]
            if (audit["product"]["sha256"] != twin["product_sha256"]
                    or audit["expected_product_version"] != twin["product_version"]):
                raise ValueError("actual prepared product differs from frozen16 product views")
            if cell["pr"] == "pr4417" and audit["reported_product_version"] != twin["product_version"]:
                raise ValueError("remote productVersion drift")
            if record["job_id"] in job_ids or record["image_sha256"] in hashes:
                raise ValueError("duplicate job or raw image across full320")
            job_ids.add(record["job_id"])
            hashes.add(record["image_sha256"])
            records.append({"cell": cell["name"], "prompt_key": prompt["prompt_key"], "status": "done",
                            "reuse_status": reuse_status, "prompt_sha256": row["prompt_sha256"],
                            "job_id": record["job_id"], "image_sha256": record["image_sha256"],
                            "record_sha256": study.sha(paths["record"]), "run_sha256": record["run_sha256"],
                            "input_audit_sha256": study.sha(audit_path(cell, prompt)),
                            "origin_study_manifest_sha256": reused["origin_study_manifest_sha256"] if reused else study.sha(HERE / "study_manifest.json")})
    preserved = study.load(HERE / "preserved_files.json")
    changed = [p for p, digest in preserved.items() if not Path(p).exists() or study.sha(p) != digest]
    if changed:
        study.write(HERE / "preservation_mismatches.json", changed)
        raise ValueError("existing immutable evidence changed; inspect preservation_mismatches")
    receipt = study.load(HERE / "publication_receipt.json")
    public = study.load(PUBLIC / "data/comparison.json")
    if public["status"] != "complete" or public["cells"] != counts:
        raise ValueError("publication snapshot does not match final terminal counts")
    for relative, digest in receipt["objects"].items():
        if study.sha(PUBLIC / relative) != digest["sha256"]:
            raise ValueError("publication receipt is stale")
    value = {"verified_at_utc": study.now(), "status": "complete", "cells": counts,
             "initial_reused": 60, "new_submissions": 264 if restart_plan else 260,
             "interrupted_attempts_preserved": 4 if restart_plan else 0,
             "restart_manifest_sha256": study.sha(HERE / "restart_manifest.json") if restart_plan else None,
             "unique_job_ids": len(job_ids),
             "unique_raw_images": len(hashes), "actual_input_audits": len(job_ids),
             "preserved_existing_files": len(preserved), "preservation_mismatches": 0,
             "opaque_png_dimensions": [2368, 1776], "exact_frozen_product_views": 16,
             "study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
             "publication_receipt_sha256": study.sha(HERE / "publication_receipt.json"),
             "implementation_sha256": {name: study.sha(HERE / name) for name in
                                       ("study.py", "report.py", "s3_access.py", "progress.py",
                                        "gallery/index.html", "gallery/main.js", "gallery/style.css")},
             "extra_audit_model_calls": 0, "new_text_calls": 0, "new_judgments": 0, "records": records}
    study.write(HERE / "final_audit.json", value)
    print({k: v for k, v in value.items() if k != "records"}, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("collect-inputs", "build", "publish", "audit"))
    args = parser.parse_args()
    {"collect-inputs": collect_inputs, "build": build, "publish": publish, "audit": final_audit}[args.command]()
