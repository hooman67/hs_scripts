"""Verify existing report dependencies without changing or regenerating any source asset."""
from concurrent.futures import ThreadPoolExecutor
import io
from pathlib import Path
from urllib.parse import urljoin

from PIL import Image

import study


def inventory():
    assets = {}

    def add(base, value, kind):
        url = urljoin(base, value)
        study.key_for(url)
        if url in assets and assets[url] != kind:
            raise ValueError("An existing dependency is inconsistently typed as image and record")
        assets[url] = kind

    fe = study.load(study.HERE / "source/fe/data.json")
    for row in fe["rows"]:
        for asset in row["images"]:
            if asset["asset_type"] == "image":
                add(study.GATEWAY + study.FE_PREFIX + "/viewer.html", asset["image_src"], "image")
    grouped = study.load(study.HERE / "source/grouped/data.json")
    base = study.GATEWAY + study.GROUP_PREFIX + "/index.html"
    for group in grouped["groups"]:
        for experiment in group["experiments"]:
            for card in experiment["cards"]:
                add(base, card["image"], "image")
                for role, value in card.get("inputs", {}).items():
                    add(base, value, "record" if role == "audit_url" else "image")
                if card.get("record_url"):
                    add(base, card["record_url"], "record")
    baseline = study.load(study.HERE / "baseline_bindings.json")
    for item in baseline["bindings"].values():
        add(base, item["guide"]["url"], "image")
        add(base, item["original_record_url"], "record")
        add(base, item["image_request_url"], "record")
    return assets


def main():
    c = study.client()
    assets = inventory()
    root = Path(study.load(study.HERE / "storage.json")["artifact_root"])

    def one(pair):
        url, kind = pair
        response = c.head_object(Bucket=study.BUCKET, Key=study.key_for(url))
        untyped = kind == "image" and response["ContentType"] in (
            "application/octet-stream", "binary/octet-stream")
        if (response["ContentLength"] <= 0
                or (kind == "image" and not response["ContentType"].startswith("image/") and not untyped)
                or (kind == "record" and response["ContentType"] != "application/json")):
            raise ValueError(f"Existing dependency is absent, empty or incorrectly typed: {url}")
        result = {
            "kind": kind, "bytes": response["ContentLength"],
            "content_type": response["ContentType"], "etag": response["ETag"],
            "version_id": response.get("VersionId"), "metadata": response.get("Metadata", {}),
        }
        if untyped:
            fetched = c.get_object(Bucket=study.BUCKET, Key=study.key_for(url))
            body = fetched["Body"].read()
            if (fetched["ETag"] != response["ETag"] or len(body) != response["ContentLength"]
                    or fetched.get("VersionId") != response.get("VersionId")):
                raise ValueError("An existing untyped image changed during content verification")
            with Image.open(io.BytesIO(body)) as image:
                image.verify()
                kind = image.format
            path = root / "browser_cache" / (study.digest(url.encode()) + "." + kind.lower())
            study.emit(path, body)
            result.update(actual_image_format=kind, sha256=study.digest(body), cached_path=str(path))
        return url, result

    with ThreadPoolExecutor(max_workers=8) as pool:
        objects = dict(pool.map(one, assets.items()))
    baseline = study.load(study.HERE / "baseline_bindings.json")
    for item in baseline["bindings"].values():
        head = objects[item["image"]]
        if head["etag"] != item["etag"] or head["version_id"] != item["version_id"]:
            raise ValueError("Reused baseline image changed after its actual pixel audit")
    study.emit(study.HERE / "media_inventory.json", {
        "at_utc": study.now(), "objects": objects, "fe_image_bindings": 800,
        "grouped_image_bindings": 320, "existing_images": sum(v == "image" for v in assets.values()),
        "records": sum(v == "record" for v in assets.values()),
        "untyped_existing_images_verified_by_actual_decode": sum(
            "actual_image_format" in item for item in objects.values()),
        "baseline_bindings_sha256": study.sha(study.HERE / "baseline_bindings.json"),
    })
    print({"existing_dependencies_verified": len(objects),
           "existing_image_urls": sum(v == "image" for v in assets.values())})


if __name__ == "__main__":
    main()
