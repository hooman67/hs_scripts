"""Publish verified support objects before three conditional in-place report updates."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import generate
import study


def original_matches(response, body, expected):
    return (
        study.digest(body) == expected["sha256"]
        and response["ETag"] == expected["etag"]
        and response.get("VersionId") == expected["version_id"]
        and response["ContentType"] == expected["content_type"]
        and response.get("Metadata", {}) == expected["metadata"]
    )


def owned_matches(response, body, item, owner):
    return (
        study.digest(body) == item["sha256"]
        and response["ContentType"] == item["content_type"]
        and response.get("Metadata", {}).get("hp-study-sha256") == owner
    )


def publish():
    from botocore.exceptions import ClientError

    generate.verify()
    source = study.load(study.HERE / "source_manifest.json")
    manifest_path = study.HERE / "publication_manifest.json"
    manifest = study.load(manifest_path)
    proof = study.load(study.HERE / "browser_validation.json")
    if not proof["passed"] or proof["publication_manifest_sha256"] != study.sha(manifest_path):
        raise ValueError("Actual browser proof must bind this exact publication manifest")
    if (proof["checker_sha256"] != study.sha(study.HERE / "check_browser.py")
            or proof["transport_helper_sha256"] != study.sha(study.PRIOR / "check_browser.py")
            or proof["media_inventory_sha256"] != study.sha(study.HERE / "media_inventory.json")):
        raise ValueError("Browser checker/transport/media inventory changed after verification")
    if (study.sha(study.HERE / "report.py") != manifest["builder_sha256"]
            or study.sha(study.HERE / "generation_audit.json") != manifest["generation_audit_sha256"]
            or study.sha(study.HERE / "baseline_bindings.json") != manifest["baseline_bindings_sha256"]):
        raise ValueError("Built report sources/audits changed after browser verification")
    entries = manifest["entries"]
    mutable = {key for key, value in entries.items() if value["original"] is not None}
    expected_mutable = {
        study.FE_PREFIX + "/data.json", study.FE_PREFIX + "/viewer.html",
        study.GROUP_PREFIX + "/index.html",
    }
    if mutable != expected_mutable:
        raise ValueError("In-place writes must be exactly the three authorized report objects")
    for key, item in entries.items():
        if (key not in mutable and not key.startswith(study.PREFIX + "/")
                and not key.startswith(study.GROUP_PREFIX + "/main_v6_5_pr4619_")
                and not key.startswith(study.GROUP_PREFIX + "/data_v6_5_pr4619_")
                and not key.startswith(study.GROUP_PREFIX + "/style_v6_5_pr4619_")):
            raise ValueError("Publication escapes the authorized report support prefixes")
        path = Path(item["path"])
        if study.sha(path) != item["sha256"] or path.stat().st_size != item["bytes"]:
            raise ValueError("Browser-verified source asset changed")
    c = study.client()
    owner = study.sha(study.HERE / "execution_manifest.json")
    originals = {item["key"]: item for item in source["objects"].values()}
    media = study.load(study.HERE / "media_inventory.json")["objects"]

    def get(key):
        response = c.get_object(Bucket=study.BUCKET, Key=key)
        return response, response["Body"].read()

    def check_sources():
        for key, expected in originals.items():
            response, body = get(key)
            if not (original_matches(response, body, expected)
                    or (key in mutable and owned_matches(response, body, entries[key], owner))):
                raise ValueError(f"Live source changed; re-read and merge rather than overwrite: {key}")

    def check_media():
        def one(pair):
            url, expected = pair
            response = c.head_object(Bucket=study.BUCKET, Key=study.key_for(url))
            if (response["ETag"] != expected["etag"]
                    or response.get("VersionId") != expected["version_id"]
                    or response["ContentLength"] != expected["bytes"]
                    or response["ContentType"] != expected["content_type"]
                    or response.get("Metadata", {}) != expected["metadata"]):
                raise ValueError(f"Existing dependency changed after its browser/source audit: {url}")
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(one, media.items()))

    def annotations(stage):
        found = {}
        prefix = study.FE_PREFIX + "/annotations/"
        for page in c.get_paginator("list_objects_v2").paginate(Bucket=study.BUCKET, Prefix=prefix):
            for item in page.get("Contents", []):
                if item["Key"].endswith(".json"):
                    response, body = get(item["Key"])
                    saved = study.HERE / "publication_annotations" / stage / (
                        study.digest(item["Key"].encode()) + "_" + study.digest(body) + ".json")
                    study.emit(saved, body)
                    found[item["Key"]] = {
                        "sha256": study.digest(body), "etag": response["ETag"],
                        "version_id": response.get("VersionId"), "snapshot_path": str(saved),
                    }
        return found

    def upload_new(pair):
        key, item = pair
        body = Path(item["path"]).read_bytes()
        try:
            c.put_object(
                Bucket=study.BUCKET, Key=key, Body=body, ContentType=item["content_type"],
                CacheControl="no-cache",
                Metadata={"sha256": item["sha256"], "hp-study-sha256": owner},
                IfNoneMatch="*",
            )
        except ClientError as error:
            if error.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
                raise
        response, saved = get(key)
        if saved != body or not owned_matches(response, saved, item, owner):
            raise ValueError(f"New object conflicts with existing bytes/type/ownership: {key}")
        return key, {
            "sha256": item["sha256"], "bytes": len(body), "content_type": item["content_type"],
            "etag": response["ETag"], "version_id": response.get("VersionId"),
        }

    check_sources()
    check_media()
    before_annotations = annotations("before")
    new_entrypoints = {study.PREFIX + "/fe/viewer.html", study.PREFIX + "/gallery/index.html"}
    items = [(key, item) for key, item in entries.items() if key not in mutable | new_entrypoints]
    for relative, expected in source["objects"].items():
        path = study.HERE / "source" / relative
        items.append((study.PREFIX + "/backups/" + relative, {
            "path": str(path), "sha256": expected["sha256"], "bytes": path.stat().st_size,
            "content_type": expected["content_type"],
        }))
    with ThreadPoolExecutor(max_workers=8) as pool:
        published = dict(pool.map(upload_new, items))
    check_sources()
    for key in sorted(new_entrypoints):
        saved_key, receipt = upload_new((key, entries[key]))
        published[saved_key] = receipt
    order = [study.FE_PREFIX + "/data.json", study.FE_PREFIX + "/viewer.html",
             study.GROUP_PREFIX + "/index.html"]
    for key in order:
        item = entries[key]
        response, body = get(key)
        if not owned_matches(response, body, item, owner):
            expected = item["original"]
            if not original_matches(response, body, expected):
                raise ValueError("Conditional target changed after support-object publication")
            c.put_object(
                Bucket=study.BUCKET, Key=key, Body=Path(item["path"]).read_bytes(),
                ContentType=item["content_type"], CacheControl="no-cache",
                Metadata={**expected["metadata"], "sha256": item["sha256"],
                          "hp-study-sha256": owner, "hp-extended-from-sha256": expected["sha256"]},
                IfMatch=expected["etag"],
            )
        response, saved = get(key)
        if saved != Path(item["path"]).read_bytes() or not owned_matches(response, saved, item, owner):
            raise ValueError("Updated report differs from the browser-verified bytes/type/ownership")
        receipt = {"sha256": item["sha256"], "etag": response["ETag"],
                   "version_id": response.get("VersionId"), "bytes": len(saved),
                   "content_type": item["content_type"]}
        study.emit(study.HERE / "publication_updates" / (study.digest(key.encode()) + ".json"),
                   {"key": key, **receipt})
        published[key] = receipt
    check_sources()
    check_media()
    after_annotations = annotations("after")
    receipt = {
        "at_utc": study.now(), "objects": published, "full_get_bytes_and_types_verified": True,
        "publication_manifest_sha256": study.sha(manifest_path),
        "annotations_before": before_annotations, "annotations_after": after_annotations,
        "annotation_objects_written": 0, "source_row_and_first_five_rating_ids_preserved": True,
        "unchanged_source_dependency_objects": len(media),
        "reports": manifest["links"], "live_gateway_sso_or_server_annotation_writes_certified": False,
    }
    study.emit(study.HERE / "publication_receipt.json", receipt)
    root = Path(study.load(study.HERE / "storage.json")["artifact_root"])
    study.emit(root / "publication_receipt.json", receipt)
    print({"verified_objects": len(published), "reports": manifest["links"]})


if __name__ == "__main__":
    publish()
