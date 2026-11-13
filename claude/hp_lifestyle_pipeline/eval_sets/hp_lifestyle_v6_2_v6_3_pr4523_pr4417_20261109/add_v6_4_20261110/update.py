"""Extend the live comparison without regenerating or overwriting existing assets."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import posixpath
from urllib.parse import urljoin, urlsplit

HERE = Path(__file__).resolve().parent
OLD = HERE.parent
NEW = OLD.parent / "hp_lifestyle_v6_4_pr4523_30_20261110"
BUCKET = "foundry-hp-enterprise-adobe-assets"
TARGET = "eval_sets/" + OLD.name
SOURCE = "eval_sets/" + NEW.name
ORIGIN = "https://foundry-aws-corp.adobe.io"
BASE = f"{ORIGIN}/asset/{BUCKET}/{TARGET}/gallery/"
SOURCE_BASE = f"{ORIGIN}/asset/{BUCKET}/{SOURCE}/gallery/"
TITLE = "V6.4 / PR 4523 - V15.7 shapes"
CELL = "v6_4_pr4523"
DATA_PATH = "data/comparison_v6_4_20261110.json"
JS_PATH = "gallery/main.v6_4_20261110.js"
CSS_PATH = "gallery/style.v6_4_20261110.css"
MANIFEST_PATH = "data/comparison_v6_4_20261110_assets.json"


def load(path):
    return json.loads(Path(path).read_text())


def digest(body):
    return hashlib.sha256(body).hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = value if isinstance(value, bytes) else (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(body)


def client():
    spec = importlib.util.spec_from_file_location("approved_hp_s3", OLD.parent /
        "hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/s3_access.py")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    result = helper.s3_client()
    if "IfMatch" not in result.meta.service_model.operation_model("PutObject").input_shape.members:
        raise RuntimeError("current boto3 conditional PutObject support is required")
    return result


def snapshot():
    s3 = client()
    objects = {}
    targets = ("gallery/index.html", "gallery/main.js", "gallery/style.css",
               "gallery/imsauth.js", "data/comparison.json", "asset_manifest.json")
    sources = ("data/generation.json", "data/selected_v6_4_30.json", "asset_manifest.json")
    for label, prefix, names in (("target", TARGET, targets), ("source", SOURCE, sources)):
        for name in names:
            response = s3.get_object(Bucket=BUCKET, Key=prefix + "/" + name)
            body = response["Body"].read()
            local = label + "/" + name
            write(HERE / "snapshot" / local, body)
            objects[local] = {"key": prefix + "/" + name, "sha256": digest(body),
                             "bytes": len(body), "etag": response["ETag"],
                             "version_id": response.get("VersionId"),
                             "content_type": response["ContentType"],
                             "metadata": response.get("Metadata", {})}
    for source, target in (("gallery/index.html", "gallery/index.html"),
                           ("gallery/main.js", JS_PATH), ("gallery/style.css", CSS_PATH)):
        write(HERE / "staging" / target, (HERE / "snapshot/target" / source).read_bytes())
    write(HERE / "snapshot.json", {"retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                                  "objects": objects})
    old = load(HERE / "snapshot/target/data/comparison.json")
    new = load(HERE / "snapshot/source/data/generation.json")
    print(json.dumps({"live_target_rows": len(old["rows"]), "existing_cells": old["cells"],
                      "source_rows": len(new["rows"]), "source_title": new["title"],
                      "actual_input_audits": old["actual_input_audits"]}, indent=2))


def rebase(value):
    absolute = urljoin(SOURCE_BASE, value)
    parsed = urlsplit(absolute)
    if parsed.scheme != "https" or parsed.netloc != urlsplit(ORIGIN).netloc or parsed.query:
        raise ValueError("asset URL must remain on the same secure gateway without query tokens")
    if not parsed.path.startswith(f"/asset/{BUCKET}/{SOURCE}/"):
        raise ValueError("new asset reference escapes the frozen V6.4 report")
    return posixpath.relpath(parsed.path, urlsplit(BASE).path)


def merge(old, new):
    result = copy.deepcopy(old)
    if (len(old["rows"]) != 30 or len(new["rows"]) != 30 or CELL in old["cells"]
            or new["title"] != TITLE or new["actual_input_audits"] != 30
            or old["actual_input_audits"] != 120 or len(old["cells"]) != 4):
        raise ValueError("unexpected source/destination study identity or completeness")
    by_slot = {tuple(row["key"]): row for row in new["rows"]}
    if len(by_slot) != 30 or set(by_slot) != {tuple(row["key"]) for row in old["rows"]}:
        raise ValueError("the thirty unique device/camera/rank slots must match exactly")
    for row in result["rows"]:
        source = by_slot[tuple(row["key"])]
        prompt = source["prompt"]
        if (tuple(row["key"]) != (prompt["device_id"], prompt["camera_tag"], prompt["bank_rank"])
                or source["output"]["status"] != "done"
                or digest(prompt["text"].encode()) != prompt["text_sha256"]):
            raise ValueError("V6.4 prompt/output is not the selected actual completed record")
        for field in ("device_id", "camera_tag", "bank_rank", "source_camera_name", "render_lookup"):
            if prompt[field] != row["prompts"]["v6_3"][field]:
                raise ValueError("V6.4 product/view/rank binding differs")
        row["prompts"]["v6_4"] = copy.deepcopy(prompt)
        row["v6_4_source_input"] = copy.deepcopy(source["source_input"])
        output = copy.deepcopy(source["output"])
        for field in ("image", "record_url"):
            output[field] = rebase(output[field])
        output["inputs"] = {name: rebase(value) for name, value in output["inputs"].items()}
        output["guide"] = output["inputs"]["geometry_guide"]
        row["outputs"][CELL] = output
    result["cells"][CELL] = {"expected": 30, "done": 30, "failed": 0, "failed_keys": []}
    result["actual_input_audits"] = 150
    result["built_at_utc"] = datetime.now(timezone.utc).isoformat()
    return result


def build():
    for name, item in load(HERE / "snapshot.json")["objects"].items():
        if digest((HERE / "snapshot" / name).read_bytes()) != item["sha256"]:
            raise ValueError("live-source snapshot was modified")
    old = load(HERE / "snapshot/target/data/comparison.json")
    source = load(HERE / "snapshot/source/data/generation.json")
    result = merge(old, source)
    write(HERE / "staging" / DATA_PATH, result)
    paths = (DATA_PATH, JS_PATH, CSS_PATH, "gallery/index.html")
    assets = {name: {"sha256": digest((HERE / "staging" / name).read_bytes()),
                     "bytes": (HERE / "staging" / name).stat().st_size} for name in paths}
    write(HERE / "staging" / MANIFEST_PATH, {
        "assets": assets, "snapshot_sha256": digest((HERE / "snapshot.json").read_bytes()),
        "new_images": 0, "reused_v6_4_images": 30,
        "note": "The original asset manifest remains historical; existing assets are unchanged."})
    print(json.dumps({"rows": 30, "generation_columns": 5, "new_model_calls": 0,
                      "new_image_uploads": 0, "publication_objects": len(paths) + 1}))


def publish():
    s3 = client()
    snapshot = load(HERE / "snapshot.json")
    manifest = load(HERE / "staging" / MANIFEST_PATH)
    browser = load(HERE / "browser_validation.json")
    if browser["status"] != "passed" or browser["manifest_sha256"] != digest(
            (HERE / "staging" / MANIFEST_PATH).read_bytes()):
        raise ValueError("browser proof must bind the exact publication")

    def verify_sources():
        for name, expected in snapshot["objects"].items():
            response = s3.get_object(Bucket=BUCKET, Key=expected["key"])
            if digest(response["Body"].read()) != expected["sha256"] or response["ETag"] != expected["etag"]:
                raise ValueError(f"live source changed after preparation: {name}")

    verify_sources()
    verified = {}

    def put_new(key, body, content_type):
        from botocore.exceptions import ClientError
        try:
            s3.put_object(Bucket=BUCKET, Key=key, Body=body, ContentType=content_type,
                          CacheControl="no-cache", Metadata={"sha256": digest(body)}, IfNoneMatch="*")
        except ClientError as error:
            if error.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
                raise
        response = s3.get_object(Bucket=BUCKET, Key=key)
        if response["Body"].read() != body or response["ContentType"] != content_type:
            raise ValueError("published object differs from the intended bytes/type")
        verified[key] = {"sha256": digest(body), "etag": response["ETag"],
                         "version_id": response.get("VersionId")}

    for name, expected in manifest["assets"].items():
        if digest((HERE / "staging" / name).read_bytes()) != expected["sha256"]:
            raise ValueError("staged artifact changed after browser verification")
    for name, old in snapshot["objects"].items():
        if name.startswith("target/"):
            put_new(TARGET + "/comparison_backups/v6_4_20261110/" + name.removeprefix("target/"),
                    (HERE / "snapshot" / name).read_bytes(), old["content_type"])
    for name, content_type in ((DATA_PATH, "application/json"), (JS_PATH, "application/javascript"),
                               (CSS_PATH, "text/css"), (MANIFEST_PATH, "application/json")):
        put_new(TARGET + "/" + name, (HERE / "staging" / name).read_bytes(), content_type)
    verify_sources()
    html_key = TARGET + "/gallery/index.html"
    original = snapshot["objects"]["target/gallery/index.html"]
    body = (HERE / "staging/gallery/index.html").read_bytes()
    s3.put_object(Bucket=BUCKET, Key=html_key, Body=body, ContentType="text/html; charset=utf-8",
                  CacheControl="no-cache", Metadata={**original["metadata"], "sha256": digest(body)},
                  IfMatch=original["etag"])
    response = s3.get_object(Bucket=BUCKET, Key=html_key)
    if response["Body"].read() != body or response["ContentType"] != "text/html; charset=utf-8":
        raise ValueError("updated live HTML differs from the verified bytes/type")
    verified[html_key] = {"sha256": digest(body), "etag": response["ETag"],
                          "version_id": response.get("VersionId")}
    for name, expected in snapshot["objects"].items():
        if name == "target/gallery/index.html":
            continue
        current = s3.head_object(Bucket=BUCKET, Key=expected["key"])
        if current["ETag"] != expected["etag"] or current.get("VersionId") != expected["version_id"]:
            raise ValueError("an original supporting asset or V6.4 source changed during publication")
    write(HERE / "publication_receipt.json", {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(), "objects": verified,
        "url": BASE + "index.html", "rows": 30, "generation_columns": 5,
        "original_supporting_files_unchanged": True, "source_v6_4_unchanged": True,
        "new_model_calls": 0, "new_image_uploads": 0,
    })
    print(BASE + "index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("snapshot", "build", "publish"))
    command = parser.parse_args().command
    {"snapshot": snapshot, "build": build, "publish": publish}[command]()
