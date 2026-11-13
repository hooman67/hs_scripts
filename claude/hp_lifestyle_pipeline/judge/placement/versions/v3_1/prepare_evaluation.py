"""Resolve the live viewer's entire actual image inventory for the authorized comparison."""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import foundry_aws_gateway
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
BASE = ("https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/"
        "hp-data-artifacts/hp-3p-gpt25/"
        "hp16-v6prompt-v156-vs-v164-vs-v166-vs-v166noguide-v2-e2e32-20261106T181903Z/")
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = urlparse(BASE).path.split(f"/asset/{BUCKET}/", 1)[1]


def main():
    destination = ROOT / "evaluation"
    destination.mkdir(exist_ok=True)
    out = destination / "inventory.json"
    if out.exists():
        raise RuntimeError("Evaluation inventory exists; preserve the frozen snapshot")
    viewer = ROOT / "sources/viewer.html"
    soup = BeautifulSoup(viewer.read_text(), "html.parser")
    records, asset_urls = [], set()
    for section in soup.find_all("section"):
        heading = section.find("h2")
        row = section.find("div", class_="row")
        if not heading or not row:
            continue
        row_id = heading.get_text(" ", strip=True)
        twin = urljoin(BASE, section.find("details", class_="in").find("a", href=True)["href"])
        prompt = section.find("p", class_="req").get_text(" ", strip=True)
        if not prompt.startswith("User request:"):
            raise ValueError("Missing original scene prompt")
        product = section.find("p", class_="meta").get_text(" ", strip=True).split(" · ", 1)[0].strip()
        if product not in {"laptop", "printer"}:
            raise ValueError("Unsupported source product type")
        figures = row.find_all("figure", recursive=False)
        for position, figure in enumerate(figures):
            image = urljoin(BASE, figure.find("a", href=True)["href"])
            records.append({
                "id": Path(urlparse(image).path).stem, "source_row_id": row_id,
                "variant": figure.find("figcaption").get_text(" ", strip=True),
                "column_index_0based": position,
                "generated_image_url": image, "twin_image_url": twin,
                "scene_prompt": prompt.removeprefix("User request:").strip(),
                "product_type": product, "source_image_stage": "e2e_comparison_output",
            })
            asset_urls.update([image, twin])
    ids = [r["id"] for r in records]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Empty or duplicated source inventory")
    client = foundry_aws_gateway.maybe_s3_client(BUCKET)
    if client is None:
        raise RuntimeError("Approved S3 client unavailable")

    def fetch(url):
        key = urlparse(url).path.split(f"/asset/{BUCKET}/", 1)[1]
        relative = key.removeprefix(PREFIX)
        if relative == key or ".." in Path(relative).parts:
            raise ValueError("Image outside supplied source prefix")
        obj = client.get_object(Bucket=BUCKET, Key=key)
        data = obj["Body"].read()
        path = ROOT / "sources" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_bytes() != data:
            raise ValueError("Live source bytes changed since anchor consultation")
        path.write_bytes(data)
        return url, {"url": url, "local_path": str(path),
                     "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                     "s3_uri": f"s3://{BUCKET}/{key}", "etag": obj.get("ETag"),
                     "last_modified": obj["LastModified"].isoformat(),
                     "content_type": obj.get("ContentType")}

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        assets = dict(pool.map(fetch, sorted(asset_urls)))
    for record in records:
        for key in ("generated_image", "twin_image"):
            record[key] = assets[record.pop(key + "_url")]
        record["scene_prompt_sha256"] = hashlib.sha256(record["scene_prompt"].encode()).hexdigest()
    inventory = {
        "schema_version": "placement-v3-v3.1-historical-inventory-v1",
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "source_viewer": {"url": BASE + "viewer.html", "local_path": str(viewer),
                          "sha256": hashlib.sha256(viewer.read_bytes()).hexdigest()},
        "row_count": len({r["source_row_id"] for r in records}),
        "output_count": len(records), "unique_asset_count": len(assets),
        "input_twin_count": len({r["twin_image"]["sha256"] for r in records}),
        "stage_adapter": "Canonical runtime literal scene_generation; actual source stage remains e2e_comparison_output, an out-of-domain diagnostic.",
        "records": records,
    }
    out.write_text(json.dumps(inventory, indent=2) + "\n")
    print(json.dumps({key: inventory[key] for key in (
        "row_count", "output_count", "unique_asset_count", "input_twin_count")}))


if __name__ == "__main__":
    main()
