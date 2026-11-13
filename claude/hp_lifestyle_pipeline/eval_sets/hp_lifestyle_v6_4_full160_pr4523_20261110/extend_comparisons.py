"""Append V6.4 to both live full160 reports, preserving the original two columns."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import json
import mimetypes
from pathlib import Path
import posixpath
from urllib.parse import urlsplit

import report
import study

HERE = study.HERE
STAGING = HERE / "extension"
TARGET = "eval_sets/" + study.COMPARISON.name
TARGET_BASE = report.GATEWAY + TARGET + "/"
CELL = "v6_4_pr4523"
DATA_PATH = "data/comparison_v6_4_160_20261110.json"
JS_PATH = "gallery/main.v6_4_160_20261110.js"
CSS_PATH = "gallery/style.v6_4_160_20261110.css"
MANIFEST_PATH = "data/comparison_v6_4_160_20261110_assets.json"


def templates():
    for source, target in (("gallery/index.html", "gallery/index.html"),
                           ("gallery/main.js", JS_PATH), ("gallery/style.css", CSS_PATH)):
        study.write(STAGING / target, (HERE / "baseline_live/full160" / source).read_bytes())


def rebase(value):
    parsed = urlsplit(value)
    if parsed.scheme != "https" or parsed.netloc != "foundry-aws-corp.adobe.io" or parsed.query:
        raise ValueError("all new references must remain secure gateway URLs without query tokens")
    if not any(parsed.path.startswith("/asset/" + study.BUCKET + "/" + prefix + "/")
               for prefix in (study.PREFIX, report.PRIOR_PREFIX)):
        raise ValueError("new reference escapes the frozen V6.4 assets")
    return posixpath.relpath(parsed.path, urlsplit(TARGET_BASE + "gallery/").path)


def merge(old, source):
    if len(old["rows"]) != 160 or len(source["rows"]) != 160 or CELL in old["cells"]:
        raise ValueError("expected the original two-column160 comparison and a new160 source")
    by_slot = {tuple(row["key"]): row for row in source["rows"]}
    if len(by_slot) != 160 or set(by_slot) != {tuple(row["key"]) for row in old["rows"]}:
        raise ValueError("the160 unique device/camera/rank slots must match")
    result = copy.deepcopy(old)
    for row in result["rows"]:
        new = by_slot[tuple(row["key"])]
        for field in ("device_id", "camera_tag", "bank_rank", "source_camera_name", "render_lookup"):
            if new["prompt"][field] != row["prompt"][field]:
                raise ValueError("V6.4 product/view/rank binding differs")
        if new["output"]["status"] != "done":
            raise ValueError("all160 new outputs must be complete")
        row["prompt_v6_4"] = copy.deepcopy(new["prompt"])
        row["source_input_v6_4"] = copy.deepcopy(new["source_input"])
        row["bank_audit_v6_4"] = copy.deepcopy(new["bank_audit"])
        output = copy.deepcopy(new["output"])
        for field in ("image", "record_url", "job_url", "status_url"):
            output[field] = rebase(output[field])
        output["inputs"] = {name: rebase(value) for name, value in output["inputs"].items()}
        row["outputs"][CELL] = output
    result["cells"][CELL] = source["counts"]
    result["actual_input_audits"] = 480
    result["built_at_utc"] = study.now()
    return result


def fe_merge(old_fe, old_gallery, source):
    if len(old_fe["rows"]) != 160 or any(len(row["images"]) != 2 for row in old_fe["rows"]):
        raise ValueError("expected the clean original two-image-per-row FE report")
    by_slot = {tuple(row["key"]): row for row in source["rows"]}
    result = copy.deepcopy(old_fe)
    vendor = study.module("v64_full160_official_fe", Path.home() / ".claude/scripts/fe_html/parquet_to_fe_html.py")
    for fe_row, gallery_row in zip(result["rows"], old_gallery["rows"]):
        if fe_row["meta_data"]["evalset_item_id"] != gallery_row["prompt"]["prompt_key"]:
            raise ValueError("existing FE row identity differs from its detailed source")
        new = by_slot[tuple(gallery_row["key"])]
        item = vendor.manifest_to_data_json({"rows": [{
            "row_idx": fe_row["meta_data"]["row_idx"],
            "evalset_item_id": fe_row["meta_data"]["evalset_item_id"],
            "assets": [{"kind": "image", "src": new["output"]["image"], "label": study.TITLE}],
        }]}, is_secure=True, title=None)
        fe_row["images"].append(item["rows"][0]["images"][0])
    result["meta_texts"][0] += " + V6.4 / V15.7"
    return result


def build():
    old = study.load(HERE / "baseline_live/full160/data/comparison.json")
    source = study.load(report.PUBLIC / "data/generation.json")
    report.emit(STAGING / DATA_PATH, merge(old, source))
    report.emit(STAGING / "fe/data.json", fe_merge(
        study.load(HERE / "baseline_live/full160/fe/data.json"), old, source))
    files = ("gallery/index.html", JS_PATH, CSS_PATH, DATA_PATH, "fe/data.json")
    assets = {name: {"sha256": study.sha(STAGING / name), "bytes": (STAGING / name).stat().st_size}
              for name in files}
    report.emit(STAGING / MANIFEST_PATH, {"assets": assets,
        "study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
        "public_asset_manifest_sha256": study.sha(report.PUBLIC / "asset_manifest.json"),
        "rows": 160, "generation_columns": 3, "new_image_uploads": 130, "reused_v6_4_images": 30})
    print(json.dumps({"rows": 160, "comparison_columns": 3, "output_bindings": 480}))


def publish():
    from botocore.exceptions import ClientError
    s3 = study.s3_client()
    frozen = study.verify()
    proof = study.load(HERE / "browser_validation.json")
    if proof["status"] != "passed" or proof["extension_manifest_sha256"] != study.sha(STAGING / MANIFEST_PATH):
        raise ValueError("exact browser verification is required before publication")
    asset_manifest = study.load(report.PUBLIC / "asset_manifest.json")
    extension = study.load(STAGING / MANIFEST_PATH)
    if extension["public_asset_manifest_sha256"] != study.sha(report.PUBLIC / "asset_manifest.json"):
        raise ValueError("publication asset manifest changed")
    for root, assets in ((report.PUBLIC, asset_manifest["assets"]), (STAGING, extension["assets"])):
        for name, expected in assets.items():
            if study.sha(root / name) != expected["sha256"] or (root / name).stat().st_size != expected["bytes"]:
                raise ValueError("staged artifact changed after browser verification")

    def verify_originals():
        for expected in frozen["baseline_live_objects"].values():
            response = s3.get_object(Bucket=study.BUCKET, Key=expected["key"])
            if response["ETag"] != expected["etag"] or hashlib.sha256(response["Body"].read()).hexdigest() != expected["sha256"]:
                raise ValueError("live source/target changed; re-read and merge rather than overwrite")

    verify_originals()

    def upload_new(item):
        key, body, content_type = item
        if isinstance(body, Path):
            body = body.read_bytes()
        try:
            s3.put_object(Bucket=study.BUCKET, Key=key, Body=body, ContentType=content_type,
                          CacheControl="no-cache", Metadata={"sha256": hashlib.sha256(body).hexdigest()},
                          IfNoneMatch="*")
        except ClientError as error:
            if error.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
                raise
        response = s3.get_object(Bucket=study.BUCKET, Key=key)
        if response["Body"].read() != body or response["ContentType"] != content_type:
            raise ValueError("published object differs from intended bytes/type")
        return key, {"sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
                     "content_type": content_type, "etag": response["ETag"],
                     "version_id": response.get("VersionId")}

    items = []
    for path in sorted(report.PUBLIC.rglob("*")):
        if path.is_file():
            name = path.relative_to(report.PUBLIC).as_posix()
            if name not in asset_manifest["assets"] and name != "asset_manifest.json":
                raise ValueError("public directory differs from its explicit allowlist")
            content_type = {".webp": "image/webp"}.get(path.suffix) or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            items.append((study.PREFIX + "/" + name, path, content_type))
    with ThreadPoolExecutor(max_workers=8) as pool:
        objects = dict(pool.map(upload_new, items))
    for name, expected in frozen["baseline_live_objects"].items():
        if name.startswith("full160/"):
            relative = name.removeprefix("full160/")
            key = TARGET + "/comparison_backups/v6_4_full160_20261110/" + relative
            objects.update([upload_new((key, (HERE / "baseline_live" / name).read_bytes(), expected["content_type"]))])
    for name, content_type in ((JS_PATH, "application/javascript"), (CSS_PATH, "text/css"),
                               (DATA_PATH, "application/json"), (MANIFEST_PATH, "application/json")):
        objects.update([upload_new((TARGET + "/" + name, (STAGING / name).read_bytes(), content_type))])
    verify_originals()
    for name, content_type in (("fe/data.json", "application/json"), ("gallery/index.html", "text/html; charset=utf-8")):
        expected = frozen["baseline_live_objects"]["full160/" + name]
        body = (STAGING / name).read_bytes()
        key = TARGET + "/" + name
        s3.put_object(Bucket=study.BUCKET, Key=key, Body=body, ContentType=content_type,
                      CacheControl="no-cache", Metadata={**expected["metadata"],
                      "sha256": hashlib.sha256(body).hexdigest(),
                      "hp-study-sha256": study.sha(HERE / "study_manifest.json"),
                      "hp-extended-from-sha256": expected["sha256"]}, IfMatch=expected["etag"])
        response = s3.get_object(Bucket=study.BUCKET, Key=key)
        if response["Body"].read() != body or response["ContentType"] != content_type:
            raise ValueError("updated report bytes/type differ")
        objects[key] = {"sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
                        "etag": response["ETag"], "version_id": response.get("VersionId"),
                        "content_type": content_type}
    for name, expected in frozen["baseline_live_objects"].items():
        if name in ("full160/gallery/index.html", "full160/fe/data.json"):
            continue
        current = s3.head_object(Bucket=study.BUCKET, Key=expected["key"])
        if current["ETag"] != expected["etag"] or current.get("VersionId") != expected["version_id"]:
            raise ValueError("an original supporting asset or small30 report changed during publication")
    receipt = {"verified_at_utc": study.now(), "rows": 160, "generation_columns": 3,
        "objects": objects, "gallery_url": TARGET_BASE + "gallery/index.html",
        "fe_url": TARGET_BASE + "fe/viewer.html?ldap=hshariati",
        "small30_comparison_unchanged": True, "official_fe_viewer_unchanged": True,
        "original_two_columns_preserved": True, "reused_v6_4_images": 30, "new_v6_4_images": 130}
    report.emit(HERE / "publication_receipt.json", receipt)
    report.emit(HERE / "report_links.txt", (receipt["fe_url"] + "\n\n" + receipt["gallery_url"] + "\n").encode())
    print(json.dumps({key: receipt[key] for key in ("rows", "fe_url", "gallery_url")}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("templates", "build", "publish"))
    args = parser.parse_args()
    {"templates": templates, "build": build, "publish": publish}[args.command]()
