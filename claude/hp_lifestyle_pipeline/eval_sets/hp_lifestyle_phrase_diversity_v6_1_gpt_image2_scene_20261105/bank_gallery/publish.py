# /// script
# dependencies = ["boto3"]
# ///
"""Publish the separate bank gallery; never overwrite the source gallery."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import mimetypes
import boto3
from botocore.config import Config

ROOT = Path(__file__).resolve().parent
BUCKET = "foundry-hp-enterprise-adobe-assets"
BASE = "eval_sets/hp_lifestyle_phrase_diversity_v6_1_gpt_image2_scene_20261105"
PREFIX = BASE + "/bank_gallery"
s3 = boto3.client("s3", region_name="us-west-2", config=Config(max_pool_connections=12))
sha = lambda raw: hashlib.sha256(raw).hexdigest()


def main():
    expected = json.loads((ROOT / "build_manifest.json").read_text())
    assert json.loads((ROOT / "browser_verification.json").read_text())["total_rows"] == 160
    current = s3.get_object(Bucket=BUCKET, Key=BASE + "/gallery/data.json")["Body"].read()
    assert sha(current) == expected["source_gallery_sha256"], "Original gallery changed; rebuild first"
    assert s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX + "/", MaxKeys=1).get("KeyCount", 0) == 0, "Destination already exists"
    data = json.loads((ROOT / "built/downloads/gallery_data.json").read_text())

    def verify_source(row):
        image = row["record"]["generated_image"]
        head = s3.head_object(Bucket=BUCKET, Key=BASE + "/images/" + image["filename"])
        assert head["ContentLength"] == image["bytes"]
        assert head["Metadata"].get("sha256") == image["sha256"]
        return row["prompt_key"]

    with ThreadPoolExecutor(max_workers=8) as pool:
        verified_sources = list(pool.map(verify_source, data["rows"]))
    files = sorted(expected["files"], key=lambda f: f["path"] == "index.html")
    uploaded = []
    for entry in files:
        raw = (ROOT / "built" / entry["path"]).read_bytes()
        assert sha(raw) == entry["sha256"] and len(raw) == entry["bytes"]
        mime = mimetypes.guess_type(entry["path"])[0] or "application/octet-stream"
        if entry["path"].endswith(".js"):
            mime = "application/javascript"
        key = PREFIX + "/" + entry["path"]
        s3.put_object(Bucket=BUCKET, Key=key, Body=raw, ContentType=mime,
                      CacheControl="no-cache", Metadata={"sha256": entry["sha256"]})
        actual = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
        assert sha(actual) == entry["sha256"]
        uploaded.append({**entry, "s3_uri": f"s3://{BUCKET}/{key}", "download_verified": True})
    report = {"published_at_utc": datetime.now(timezone.utc).isoformat(),
              "url": f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}/index.html",
              "source_images_verified": len(verified_sources), "original_gallery_unchanged": True,
              "files": uploaded}
    (ROOT / "publication.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k:v for k,v in report.items() if k != "files"}))


if __name__ == "__main__":
    main()
