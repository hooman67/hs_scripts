"""Audit native inputs/calls and publish a clean, separate V6.4/V6.5 comparison."""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import mimetypes
from pathlib import Path
import posixpath
import sys
from types import SimpleNamespace
from urllib.parse import urljoin, urlsplit

import study

HERE = study.HERE
PUBLIC = HERE / "public"
BASE = f"https://foundry-aws-corp.adobe.io/asset/{study.BUCKET}/{study.PREFIX}/"
AUDITOR = study.PROJECT / "eval_sets/hp_lifestyle_v6_4_full160_pr4523_20261110/report.py"
AUTH = study.PROJECT / "eval_sets/hp_lifestyle_grouped_diversity_20261111/public/gallery/imsauth.js"
BASELINE_GALLERY = f"https://foundry-aws-corp.adobe.io/asset/{study.BUCKET}/eval_sets/{study.BASELINE.name}/gallery/index.html"


def emit(path, value):
    path = Path(path)
    if path.exists():
        raise FileExistsError(f"refusing to overwrite report evidence: {path}")
    study.write(path, value)


def row_for(prompt):
    return {
        "row_id": prompt["prompt_key"],
        "row_slug": study.image_runner().slug(prompt["prompt_key"]),
        "prompt_sha256": prompt["text_sha256"],
    }


def native_auditor():
    """Reuse the frozen strong raw-response/input auditor with explicit study bindings."""
    original_study = sys.modules["study"]
    baseline_study = study.module("v65_baseline_auditor_study", AUDITOR.parent / "study.py")
    try:
        sys.modules["study"] = baseline_study
        auditor = study.module("v65_strong_native_auditor", AUDITOR)
    finally:
        sys.modules["study"] = original_study
    auditor.HERE = HERE
    auditor.study = SimpleNamespace(**{**vars(study), "row_for": row_for})
    return auditor


def audit(selected=None):
    study.verify()
    full = study.load(HERE / "selection/selected_v6_5_30.json")["prompts"]
    prompts = full if selected is None else selected
    auditor = native_auditor()
    twins = {
        (row["digital_twin_id"], row["camera_id"]): row
        for row in study.load(study.ENDPOINT / "input_bundle/manifest.json")["entries"]
    }
    results = [auditor.audit_one(prompt, twins, False) for prompt in prompts]
    jobs = {result["job_id"] for result in results}
    models = Counter()
    for result in results:
        models.update(result["models"])
    expected_models = Counter({
        "gpt-6-astra": len(prompts) * 3,
        "gpt-image-2.5-sunburst-2026-09-08": len(prompts),
    })
    if models != expected_models or len(jobs) != len(prompts):
        raise ValueError("actual native jobs/models do not reconcile")
    if selected is not None:
        return {
            "passed": True, "at_utc": study.now(), "rows": [p["prompt_key"] for p in prompts],
            "models": dict(models), "new_model_calls_for_audit": 0,
            "native_auditor_sha256": study.sha(AUDITOR),
        }
    if study.counts() != {"expected": 30, "done": 30, "failed": 0, "pending": 0}:
        raise ValueError("all thirty actual outputs required")
    events = [study.json.loads(line) for line in
              (HERE / "run/journals/events.jsonl").read_text().splitlines()]
    submitted = [event["row_id"] for event in events if event["event"] == "submit_started"]
    if len(submitted) != 30 or set(submitted) != {p["prompt_key"] for p in full}:
        raise ValueError("submissions do not match exactly the thirty authorized rows")
    native_jobs = [p for p in (study.ENDPOINT / "run/jobs").iterdir() if p.is_dir()]
    if len(native_jobs) != 30 or {p.name for p in native_jobs} != jobs:
        raise ValueError("endpoint contains unexpected, missing or replacement jobs")
    raw_hashes = {
        study.image_runner().valid_completed_record(HERE / "run", row_for(p))["image_sha256"]
        for p in prompts
    }
    if len(raw_hashes) != 30:
        raise ValueError("expected thirty distinct raw output PNGs")
    emit(HERE / "generation_audit.json", {
        "passed": True, "at_utc": study.now(), "rows": 30, "models": dict(models),
        "unique_jobs": 30, "unique_raw_pngs": 30, "replacements": 0,
        "all_native_request_response_and_raw_output_hashes_verified": True,
        "native_auditor_path": str(AUDITOR), "native_auditor_sha256": study.sha(AUDITOR),
        "image_quality_acceptance_claimed": False,
    })
    return {"passed": True, "rows": 30, "models": dict(models)}


def asset(path, relative, digest=None):
    body = Path(path).read_bytes()
    if digest is not None and hashlib.sha256(body).hexdigest() != digest:
        raise ValueError(f"audited asset changed: {path}")
    target = PUBLIC / relative
    if target.exists():
        if target.read_bytes() != body:
            raise ValueError(f"conflicting public asset: {relative}")
    else:
        emit(target, body)
    return BASE + relative


def relative_asset(url):
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https" or parsed.netloc != "foundry-aws-corp.adobe.io"
        or not parsed.path.startswith(f"/asset/{study.BUCKET}/")
        or parsed.query or parsed.fragment
    ):
        raise ValueError("gallery assets must stay in the authenticated HP bucket")
    return posixpath.relpath(parsed.path, urlsplit(BASE + "gallery/").path)


def assemble(baseline, new_prompts, feedback, dispositions, outputs, source):
    if not (len(baseline["rows"]) == len(new_prompts) == len(feedback["rows"]) == len(dispositions) == len(outputs) == 30):
        raise ValueError("comparison inputs must each cover exactly thirty reviewed slots")
    by_slot = {tuple(study.slot(p)): p for p in new_prompts}
    notes = {tuple(row["slot"]): row for row in feedback["rows"]}
    actions = {row["review_key"]: row for row in dispositions}
    if len(by_slot) != 30 or len(notes) != 30 or len(actions) != 30:
        raise ValueError("duplicate comparison/review keys")
    rows = []
    for original in baseline["rows"]:
        key = tuple(original["key"])
        prompt = by_slot[key]
        note = notes[key]
        old = original["prompt"]
        if (
            tuple(study.slot(old)) != key or note["scene_prompt"] != old["text"]
            or note["image_sha256"] != original["output"]["image_sha256"]
            or note["image_url"] != urljoin(BASELINE_GALLERY, original["output"]["image"])
        ):
            raise ValueError("original feedback-to-image/source binding changed")
        bank = source["bank_audit"][prompt["bank_debug_ref"]]
        if original["source_input"] != bank["source_input"]:
            raise ValueError("V6.4/V6.5 source input differs")
        rows.append({
            "key": list(key), "device": prompt["device_display_name"],
            "camera": prompt["camera_tag"], "rank": prompt["bank_rank"],
            "source_input": bank["source_input"], "feedback": note["feedback"]["comment"],
            "astra_disposition": actions[note["review_key"]],
            "v6_4": {"prompt": old["text"], "environment": old["environment"],
                     "image": urljoin(BASELINE_GALLERY, original["output"]["image"]),
                     "original_image_reference": original["output"]["image"],
                     "inputs": {key: urljoin(BASELINE_GALLERY, value)
                                for key, value in original["output"]["inputs"].items()},
                     "image_sha256": original["output"]["image_sha256"]},
            "v6_5": {"prompt": prompt["text"], "environment": prompt["environment"], **outputs[prompt["prompt_key"]]},
        })
    if len({tuple(row["key"]) for row in rows}) != 30:
        raise ValueError("comparison has duplicate slots")
    return rows


def build():
    manifest = study.verify()
    if not study.load(HERE / "generation_audit.json")["passed"]:
        raise ValueError("native generation audit required")
    prompts = study.load(HERE / "selection/selected_v6_5_30.json")["prompts"]
    outputs = {}
    for prompt in prompts:
        row = row_for(prompt)
        paths = study.image_runner().paths(HERE / "run", row)
        record = study.image_runner().valid_completed_record(HERE / "run", row)
        if record is None:
            raise ValueError("completed output changed")
        audited_path = HERE / "input_audit" / (row["row_slug"] + ".json")
        inputs = study.load(audited_path)
        if inputs["record_sha256"] != study.sha(paths["record"]):
            raise ValueError("audited native record changed")
        urls = {
            role: asset(inputs[role]["path"], "assets/inputs/" + inputs[role]["sha256"] + "." +
                        inputs[role]["suffix"], inputs[role]["sha256"])
            for role in ("product", "reference", "geometry_guide")
        }
        urls["audit_url"] = asset(audited_path, "data/input_audits/" + audited_path.name)
        outputs[prompt["prompt_key"]] = {
            "image": asset(paths["image"], "assets/outputs/" + row["row_slug"] + ".png",
                           record["image_sha256"]),
            "image_sha256": record["image_sha256"], "inputs": urls,
        }
    baseline = study.load(HERE / "baseline_live/data/generation.json")
    source = study.load(study.TEXT)
    proposal = study.load(study.PROJECT / "research/prompt_writer_v6_5/astra/proposal.json")
    rows = assemble(baseline, prompts, study.load(study.FEEDBACK), proposal["feedback_disposition"], outputs, source)
    for row in rows:
        for version in ("v6_4", "v6_5"):
            cell = row[version]
            cell["image"] = relative_asset(cell["image"])
            cell["inputs"] = {key: relative_asset(value) for key, value in cell["inputs"].items()}
    emit(PUBLIC / "gallery/data.json", {
        "title": "HP lifestyle V6.4 / V6.5", "rows": rows, "image_count": 60,
        "matching": "same device/camera/bank-rank slots, not paired scenes or random seeds",
        "image_pipeline": "Exact PR4523 / V15.7 shapes, unchanged settings and normal reference selection",
        "image_quality_acceptance_claimed": False,
    })
    for name in ("index.html", "main.js", "style.css"):
        asset(HERE / "gallery" / name, "gallery/" + name)
    asset(AUTH, "gallery/imsauth.js")
    asset(study.TEXT, "downloads/prompts_all_v6_5_160.json")
    asset(study.TEXT.with_suffix(".txt"), "downloads/prompts_all_v6_5_160.txt")
    asset(HERE / "selection/selected_v6_5_30.json", "downloads/selected_v6_5_30.json")
    asset(HERE / "selection/selected_v6_5_30.txt", "downloads/selected_v6_5_30.txt")
    asset(HERE / "generation_audit.json", "downloads/generation_audit.json")
    asset(HERE / "study_manifest.json", "downloads/study_manifest.json")
    for row in rows:
        if row["v6_4"]["original_image_reference"] != next(
            old["output"]["image"] for old in baseline["rows"] if old["key"] == row["key"]
        ):
            raise ValueError("baseline images must remain in place")
    assets = {
        p.relative_to(PUBLIC).as_posix(): {"sha256": study.sha(p), "bytes": p.stat().st_size}
        for p in sorted(PUBLIC.rglob("*")) if p.is_file()
    }
    emit(PUBLIC / "asset_manifest.json", {
        "assets": assets, "study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
        "baseline_images_reused_in_place": 30, "new_image_uploads": 30,
        "original_native_text_outcomes": {"successful": 15, "failed": 1, "offline_revalidated_banks": 16},
        "source_export_sha256": manifest["source_export_sha256"],
    })
    print(study.json.dumps({"rows": 30, "images": 60, "public_objects": len(assets) + 1}))


def verify_baseline(client):
    for item in study.verify()["baseline_live_objects"].values():
        response = client.get_object(Bucket=study.BUCKET, Key=item["key"])
        if (
            hashlib.sha256(response["Body"].read()).hexdigest() != item["sha256"]
            or response["ETag"] != item["etag"] or response.get("VersionId") != item["version_id"]
        ):
            raise ValueError("original live baseline/annotations changed; inspect before publication")
    receipt = study.load(HERE / "baseline_image_receipt.json")
    if not receipt["passed"] or len(receipt["objects"]) != 30:
        raise ValueError("all thirty live baseline images must be hash-verified")
    for key, expected in receipt["objects"].items():
        response = client.head_object(Bucket=study.BUCKET, Key=key)
        if response["ETag"] != expected["etag"] or response.get("VersionId") != expected["version_id"]:
            raise ValueError("original baseline image identity changed")


def verify_baseline_images():
    client = study.s3_client()
    notes = study.load(study.FEEDBACK)["rows"]

    def verify_image(note):
        prefix = f"/asset/{study.BUCKET}/"
        parsed = urlsplit(note["image_url"])
        if parsed.netloc != "foundry-aws-corp.adobe.io" or not parsed.path.startswith(
            prefix + f"eval_sets/{study.BASELINE.name}/assets/outputs/"
        ):
            raise ValueError("baseline image outside the approved original prefix")
        key = parsed.path[len(prefix):]
        response = client.get_object(Bucket=study.BUCKET, Key=key)
        body = response["Body"].read()
        if hashlib.sha256(body).hexdigest() != note["image_sha256"]:
            raise ValueError("live baseline PNG changed from Astra's exact reviewed image")
        return key, {
            "sha256": note["image_sha256"], "bytes": len(body), "etag": response["ETag"],
            "version_id": response.get("VersionId"),
        }

    with ThreadPoolExecutor(max_workers=8) as pool:
        objects = dict(pool.map(verify_image, notes))
    if len(objects) != 30:
        raise ValueError("expected thirty distinct live original images")
    emit(HERE / "baseline_image_receipt.json", {
        "passed": True, "at_utc": study.now(), "objects": objects, "original_image_writes": 0,
    })
    print(study.json.dumps({"original_live_image_hashes_verified": 30}))


def publish():
    from botocore.exceptions import ClientError

    client = study.s3_client()
    verify_baseline(client)
    browser = study.load(HERE / "browser_validation.json")
    if not browser["passed"] or browser["asset_manifest_sha256"] != study.sha(PUBLIC / "asset_manifest.json"):
        raise ValueError("browser proof must bind exact current public files")
    allowed = study.load(PUBLIC / "asset_manifest.json")["assets"]
    paths = sorted(path for path in PUBLIC.rglob("*") if path.is_file())
    if {p.relative_to(PUBLIC).as_posix() for p in paths} != set(allowed) | {"asset_manifest.json"}:
        raise ValueError("public directory differs from explicit allowlist")

    def upload(path):
        relative = path.relative_to(PUBLIC).as_posix()
        body = path.read_bytes()
        digest = hashlib.sha256(body).hexdigest()
        if relative in allowed and allowed[relative] != {"sha256": digest, "bytes": len(body)}:
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
            raise ValueError(f"refusing to replace different existing bytes: {key}")
        downloaded = client.get_object(Bucket=study.BUCKET, Key=key)
        if downloaded["Body"].read() != body or downloaded["ContentType"] != content_type:
            raise ValueError("published object bytes/type differ")
        return key, {"sha256": digest, "bytes": len(body), "content_type": content_type,
                     "etag": downloaded["ETag"], "version_id": downloaded.get("VersionId")}

    with ThreadPoolExecutor(max_workers=8) as pool:
        objects = dict(pool.map(upload, paths))
    verify_baseline(client)
    receipt = {
        "verified_at_utc": study.now(), "objects": objects, "original_baseline_and_comments_unchanged": True,
        "gallery_url": BASE + "gallery/index.html", "verified_by_download": True,
        "live_gateway_and_ims_certified": False,
    }
    emit(HERE / "publication_receipt.json", receipt)
    links = (
        "V6.4 / V6.5 - PR4523 / V15.7 shapes comparison (30 matched slots)\n" +
        receipt["gallery_url"] + "\n\nAll160 V6.5 prompts (TXT)\n" +
        BASE + "downloads/prompts_all_v6_5_160.txt\n\nAll160 V6.5 prompts (JSON)\n" +
        BASE + "downloads/prompts_all_v6_5_160.json\n"
    )
    emit(HERE / "report_links.txt", links)
    print(links)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("smoke-audit", "audit", "build", "publish", "verify-baseline-images"))
    command = parser.parse_args().command
    if command == "smoke-audit":
        ids = set(study.load(HERE / "smoke_launch.json")["rows"])
        selected = [p for p in study.load(HERE / "selection/selected_v6_5_30.json")["prompts"]
                    if p["prompt_key"] in ids]
        if len(selected) != 2:
            raise ValueError("included smoke must contain exactly two original selected rows")
        emit(HERE / "smoke_review.json", audit(selected))
    elif command == "audit":
        print(study.json.dumps(audit()))
    elif command == "build":
        build()
    elif command == "publish":
        publish()
    else:
        verify_baseline_images()
