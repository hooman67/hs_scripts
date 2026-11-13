#!/usr/bin/env python3
"""Publish the full160 comparison with only its two output-image columns."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import shutil
from urllib.parse import urljoin

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
PUBLIC = STUDY / "public"
PREFIX = "eval_sets/" + STUDY.name
BUCKET = "foundry-hp-enterprise-adobe-assets"
BASE = "https://foundry-aws-corp.adobe.io/asset/" + BUCKET + "/" + PREFIX + "/"
SOURCE_URL = BASE + "gallery/index.html"
VIEWER_URL = BASE + "fe/viewer.html?ldap=hshariati"
TITLE = "HP V6.3 prmpts - V15.6 vs V15.7"
CELLS = (("v6_3_pr4417", "V15.6"), ("v6_3_pr4523", "V15.7"))
SOURCE_FILES = ("gallery/index.html", "gallery/main.js", "gallery/style.css", "data/comparison.json")
REPORT = HERE / "report"

prior_path = STUDY.parent / "hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109/fe_conversion_20261110/convert.py"
spec = importlib.util.spec_from_file_location("hp_prior_fe_helpers", prior_path)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def media_url(value):
    if not isinstance(value, str) or not value:
        raise ValueError("missing generated image URL")
    result = urljoin(SOURCE_URL, value)
    if not result.startswith(BASE + "assets/"):
        raise ValueError("generated image escapes the published study assets")
    return result


def convert(document):
    if document["status"] != "complete" or len(document["rows"]) != 160:
        raise ValueError("expected the completed160-row comparison")
    rows, seen, images = [], set(), set()
    for index, row in enumerate(document["rows"]):
        prompt = row["prompt"]
        key = prompt["prompt_key"]
        if key in seen:
            raise ValueError("duplicate comparison row")
        seen.add(key)
        if (row["key"] != [prompt["device_id"], prompt["camera_tag"], prompt["bank_rank"]]
                or prior.digest(prompt["text"].encode()) != prompt["text_sha256"]):
            raise ValueError("source prompt binding changed")
        if set(row["outputs"]) != {name for name, _ in CELLS}:
            raise ValueError("unexpected comparison columns")
        assets = []
        for name, label in CELLS:
            output = row["outputs"][name]
            if output["status"] != "done":
                raise ValueError("incomplete comparison image")
            if output["lineage"]["source_commit"] != prior.COMMITS[name.rsplit("_", 1)[1]]:
                raise ValueError("wrong pinned pipeline")
            image = media_url(output["image"])
            if image in images:
                raise ValueError("duplicate generated image binding")
            images.add(image)
            assets.append({"kind": "image", "src": image, "label": label})
        rows.append({"row_idx": index + 1, "evalset_item_id": key, "assets": assets})
    return prior.load_vendor().manifest_to_data_json({"rows": rows}, is_secure=True, title=TITLE)


def verify_live_source(client):
    identities = {}
    for name in SOURCE_FILES:
        body, metadata = prior.get_bytes(client, PREFIX + "/" + name)
        if body != (PUBLIC / name).read_bytes():
            raise ValueError("live source changed; re-read before converting: " + name)
        identities[name] = {
            "sha256": prior.digest(body), "bytes": len(body), "etag": metadata["ETag"],
            "version_id": metadata.get("VersionId"),
        }
    return identities


def preflight(client):
    from botocore.exceptions import ClientError

    identities = verify_live_source(client)
    audit = json.loads((STUDY / "final_audit.json").read_text())
    receipt = json.loads((STUDY / "publication_receipt.json").read_text())
    if (audit["status"] != "complete" or audit["unique_raw_images"] != 320
            or audit["publication_receipt_sha256"] != prior.digest((STUDY / "publication_receipt.json").read_bytes())):
        raise ValueError("completed source audit/publication identity changed")
    source = json.loads((PUBLIC / "data/comparison.json").read_text())
    convert(source)
    outputs = [output for row in source["rows"] for output in row["outputs"].values()]

    def verify_image(output):
        relative = media_url(output["image"]).removeprefix(BASE)
        expected = receipt["objects"][relative]
        head = client.head_object(Bucket=BUCKET, Key=PREFIX + "/" + relative)
        if (expected["verification"] != "downloaded_sha256"
                or expected["sha256"] != output["image_sha256"]
                or head["ETag"] != expected["etag"]
                or head["ContentLength"] != expected["bytes"]
                or head["ContentType"] != expected["content_type"]
                or head.get("Metadata", {}).get("sha256") != expected["sha256"]):
            raise ValueError("published image changed: " + relative)
        return relative, {"sha256": expected["sha256"], "etag": head["ETag"],
                          "version_id": head.get("VersionId"), "bytes": head["ContentLength"]}

    with ThreadPoolExecutor(max_workers=8) as pool:
        images = dict(pool.map(verify_image, outputs))
    for filename in ("data.json", "viewer.html"):
        try:
            prior.get_bytes(client, PREFIX + "/fe/" + filename)
        except ClientError as error:
            if error.response["Error"]["Code"] not in {"NoSuchKey", "404", "NotFound"}:
                raise
        else:
            raise FileExistsError("FE target already exists; inspect before replacing: " + filename)
    prior.write_json(HERE / "preflight.json", {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": identities, "images": images,
        "source_audit_sha256": prior.digest((STUDY / "final_audit.json").read_bytes()),
        "source_publication_sha256": prior.digest((STUDY / "publication_receipt.json").read_bytes()),
    })
    print({"verified_source_files": len(identities), "verified_existing_images": len(images)})


def build():
    preflight = json.loads((HERE / "preflight.json").read_text())
    for name, identity in preflight["source"].items():
        if prior.digest((PUBLIC / name).read_bytes()) != identity["sha256"]:
            raise ValueError("source changed after preflight")
    data = convert(json.loads((PUBLIC / "data/comparison.json").read_text()))
    prior.write_json(REPORT / "data.json", data)
    shutil.copyfile(prior.VENDOR / "annotation_viewer.html", REPORT / "viewer.html")
    audit = {
        "title": TITLE, "url": VIEWER_URL, "rows": 160, "images_per_row": 2, "images": 320,
        "source": preflight["source"], "columns": dict(CELLS),
        "files": {name: prior.digest((REPORT / name).read_bytes()) for name in ("data.json", "viewer.html")},
        "vendor_converter_sha256": prior.digest((prior.VENDOR / "parquet_to_fe_html.py").read_bytes()),
        "vendor_viewer_sha256": prior.digest((prior.VENDOR / "annotation_viewer.html").read_bytes()),
        "image_reuploads": 0, "extra_assets_text_metadata_links": 0,
    }
    prior.write_json(HERE / "build_audit.json", audit)
    print({key: audit[key] for key in ("title", "url", "rows", "images")})


def publish(client):
    from botocore.exceptions import ClientError

    audit = json.loads((HERE / "build_audit.json").read_text())
    browser = json.loads((HERE / "browser_validation.json").read_text())
    if browser["status"] != "passed" or browser["files"] != audit["files"]:
        raise ValueError("browser validation must match the exact report files")
    if verify_live_source(client) != audit["source"]:
        raise ValueError("live comparison source changed")
    verified = {}
    for filename in ("data.json", "viewer.html"):
        body = (REPORT / filename).read_bytes()
        if prior.digest(body) != audit["files"][filename]:
            raise ValueError("report changed after browser validation")
        key = PREFIX + "/fe/" + filename
        content_type = "application/json" if filename.endswith(".json") else "text/html; charset=utf-8"
        try:
            current, metadata = prior.get_bytes(client, key)
        except ClientError as error:
            if error.response["Error"]["Code"] not in {"NoSuchKey", "404", "NotFound"}:
                raise
            client.put_object(
                Bucket=BUCKET, Key=key, Body=body, ContentType=content_type,
                CacheControl="no-cache", Metadata={"sha256": audit["files"][filename]},
                IfNoneMatch="*",
            )
        else:
            if current != body or metadata["ContentType"] != content_type:
                raise FileExistsError("refusing to overwrite a changed FE object: " + key)
        downloaded, metadata = prior.get_bytes(client, key)
        if downloaded != body or metadata["ContentType"] != content_type:
            raise ValueError("published FE object differs: " + key)
        verified[key] = {"sha256": prior.digest(downloaded), "bytes": len(downloaded),
                         "content_type": metadata["ContentType"], "etag": metadata["ETag"],
                         "version_id": metadata.get("VersionId")}
    prior.write_json(HERE / "publication_receipt.json", {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(), "url": VIEWER_URL,
        "verification": "downloaded_sha256", "objects": verified, "referenced_existing_images": 320,
    })
    print(VIEWER_URL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("preflight", "build", "publish"))
    parser.add_argument("--credentials-file", type=Path)
    args = parser.parse_args()
    if args.command == "build":
        build()
    else:
        if args.credentials_file is None:
            parser.error("--credentials-file is required")
        client = prior.client_for(args.credentials_file)
        if args.command == "preflight":
            preflight(client)
        else:
            publish(client)
