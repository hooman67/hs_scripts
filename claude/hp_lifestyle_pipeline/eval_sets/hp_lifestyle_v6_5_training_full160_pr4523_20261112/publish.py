"""Conditionally publish the new assets and three live entry-point updates, with safe resume."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import mimetypes
from pathlib import Path

import report
import study


def content_type(path):
    return {
        ".html": "text/html; charset=utf-8", ".js": "application/javascript",
        ".json": "application/json", ".css": "text/css", ".webp": "image/webp",
    }.get(path.suffix) or mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def publish():
    from botocore.exceptions import ClientError

    frozen = study.verify()
    manifest = study.load(study.HERE / "publication_manifest.json")
    proof = study.load(study.HERE / "browser_validation.json")
    if not proof["passed"] or proof["publication_manifest_sha256"] != study.sha(
        study.HERE / "publication_manifest.json"
    ):
        raise ValueError("browser proof must bind this exact publication")
    for name, digest in manifest["source_code_sha256"].items():
        if study.sha(study.HERE / name) != digest:
            raise ValueError("report code changed after build")
    for item in manifest["entries"].values():
        path = Path(item["path"])
        if study.sha(path) != item["sha256"] or path.stat().st_size != item["bytes"]:
            raise ValueError("browser-verified public bytes changed")
    client = study.s3_client()
    owner = study.sha(study.HERE / "study_manifest.json")
    mutable = set(manifest["mutable_keys"])
    originals = {item["key"]: item for item in frozen["baseline_live_objects"].values()}
    if not mutable <= set(originals):
        raise ValueError("in-place publication escapes frozen original targets")

    def get(key):
        response = client.get_object(Bucket=study.BUCKET, Key=key)
        return response, response["Body"].read()

    def verify_originals(allow_owned):
        for key, expected in originals.items():
            response, body = get(key)
            digest = hashlib.sha256(body).hexdigest()
            unchanged = (
                digest == expected["sha256"] and response["ETag"] == expected["etag"]
                and response.get("VersionId") == expected["version_id"]
            )
            owned = (
                allow_owned and key in mutable
                and digest == manifest["entries"][key]["sha256"]
                and response.get("Metadata", {}).get("hp-study-sha256") == owner
            )
            if not (unchanged or owned):
                raise ValueError(f"live source changed; re-read and merge rather than overwrite: {key}")
        if study.annotations(client) != frozen["baseline_annotations"]:
            raise ValueError("published annotation set changed; inspect and preserve before updating")

    def upload_new(item):
        key, path = item
        path = Path(path)
        body = path.read_bytes()
        digest, kind = hashlib.sha256(body).hexdigest(), content_type(path)
        try:
            client.put_object(
                Bucket=study.BUCKET, Key=key, Body=body, ContentType=kind,
                CacheControl="no-cache", Metadata={"sha256": digest}, IfNoneMatch="*",
            )
        except ClientError as error:
            if error.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
                raise
        response, saved = get(key)
        if saved != body or response["ContentType"] != kind:
            raise ValueError(f"published bytes/content type differ: {key}")
        return key, {
            "sha256": digest, "bytes": len(body), "content_type": kind,
            "etag": response["ETag"], "version_id": response.get("VersionId"),
        }

    verify_originals(True)
    items = [(key, item["path"]) for key, item in manifest["entries"].items() if key not in mutable]
    for name, item in frozen["baseline_live_objects"].items():
        items.append((
            study.PREFIX + "/backups/" + name,
            str(study.HERE / "baseline_live" / name),
        ))
    with ThreadPoolExecutor(max_workers=8) as pool:
        objects = dict(pool.map(upload_new, items))
    verify_originals(True)
    for key in manifest["mutable_keys"]:
        item = manifest["entries"][key]
        path = Path(item["path"])
        body, kind = path.read_bytes(), content_type(path)
        response, current = get(key)
        if hashlib.sha256(current).hexdigest() != item["sha256"]:
            expected = originals[key]
            if response["ETag"] != expected["etag"] or hashlib.sha256(current).hexdigest() != expected["sha256"]:
                raise ValueError("conditional live target changed")
            client.put_object(
                Bucket=study.BUCKET, Key=key, Body=body, ContentType=kind, CacheControl="no-cache",
                Metadata={**expected["metadata"], "sha256": item["sha256"],
                          "hp-study-sha256": owner, "hp-extended-from-sha256": expected["sha256"]},
                IfMatch=expected["etag"],
            )
        response, current = get(key)
        if (
            current != body or response["ContentType"] != kind
            or response.get("Metadata", {}).get("hp-study-sha256") != owner
        ):
            raise ValueError("in-place report bytes/type/ownership differ")
        objects[key] = {
            "sha256": item["sha256"], "bytes": len(body), "content_type": kind,
            "etag": response["ETag"], "version_id": response.get("VersionId"),
        }
        report.emit(study.HERE / "publication_updates" / (hashlib.sha256(key.encode()).hexdigest() + ".json"),
                    {"key": key, **objects[key]})
    verify_originals(True)
    receipt = {
        "verified_at_utc": study.now(), "objects": objects, "verified_by_download": True,
        "new_grouped_url": report.BASE + "gallery/index.html",
        "existing_grouped_url": study.GATEWAY + report.GROUPED + "/gallery/index.html",
        "detailed_url": study.GATEWAY + report.FULL + "/gallery/index.html",
        "fe_url": study.GATEWAY + report.FULL + "/fe/viewer.html?ldap=hshariati",
        "original_three_columns_and_grouped_cards_preserved": True,
        "official_fe_viewer_and_row_annotation_ids_unchanged": True,
        "prior30_report_unchanged": True, "live_gateway_and_ims_certified": False,
        "publication_manifest_sha256": study.sha(study.HERE / "publication_manifest.json"),
    }
    report.emit(study.HERE / "publication_receipt.json", receipt)
    links = "\n\n".join(f"{label}\n{receipt[key]}" for label, key in (
        ("NEW: V6.4 vs training-grounded V6.5 -16 inputs,10 images each", "new_grouped_url"),
        ("Updated grouped diversity -four experiments,640 images", "existing_grouped_url"),
        ("Updated full160 detailed comparison -four columns", "detailed_url"),
        ("Updated full160 clean FE comparison -four columns", "fe_url"),
    )) + (
        "\n\nAll160 V6.5 prompts (TXT)\n" + report.BASE + "data/prompts_all_v6_5_160.txt\n"
        "\nAll160 V6.5 prompts (JSON)\n" + report.BASE + "data/prompts_all_v6_5_160.json\n"
    )
    report.emit(study.HERE / "report_links.txt", links.encode())
    print(links)


if __name__ == "__main__":
    publish()
