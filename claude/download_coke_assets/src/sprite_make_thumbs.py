#!/usr/bin/env python3
"""
Convert all Sprite originals → JPEG thumbnails (max 1200px, q=82), upload to html_gallery/.
Streams S3 → ImageMagick (stdin/stdout) → S3 with no local disk persistence.
Idempotent: skips files that already exist at the destination.
"""
# /// script
# requires-python = ">=3.9"
# dependencies = ["boto3"]
# ///

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

ROOT = Path(__file__).resolve().parent.parent
BUCKET = os.environ.get("S3_BUCKET", "foundry-tccc-enterprise-adobe-assets")
SRC_PREFIX = os.environ.get("SRC_PREFIX", "dam_assets_downloaded_by_hs_sprite/orig_assets")
DST_PREFIX = os.environ.get("DST_PREFIX", "dam_assets_downloaded_by_hs_sprite/html_gallery")
REGION = os.environ.get("AWS_REGION", "us-west-2")
CONCURRENCY = int(os.environ.get("CONCURRENCY", "10"))
MAX_DIM = int(os.environ.get("MAX_DIM", "1200"))
QUALITY = int(os.environ.get("QUALITY", "82"))

s3 = boto3.client("s3", region_name=REGION)


def list_existing(prefix: str) -> set:
    paginator = s3.get_paginator("list_objects_v2")
    keys = set()
    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix + "/"):
        for obj in page.get("Contents", []) or []:
            keys.add(obj["Key"])
    return keys


def src_key_for(dam_path: str) -> str:
    rel = dam_path.replace("/content/dam/", "")
    return f"{SRC_PREFIX}/{rel}"


def dst_key_for(dam_path: str) -> str:
    rel = dam_path.replace("/content/dam/", "")
    base, _ = os.path.splitext(rel)
    return f"{DST_PREFIX}/{base}.jpg"


def convert_one(asset, src_keys_existing, dst_keys_existing, results):
    dam_path = asset["damPath"]
    src_key = src_key_for(dam_path)
    dst_key = dst_key_for(dam_path)

    if dst_key in dst_keys_existing:
        return ("skip", dam_path, "already-exists")
    if src_key not in src_keys_existing:
        return ("skip", dam_path, "missing-src")

    try:
        # Stream original from S3
        obj = s3.get_object(Bucket=BUCKET, Key=src_key)
        body = obj["Body"].read()

        # ImageMagick: read first frame from stdin, auto-orient, resize, JPEG out
        # For PSD/AI, ImageMagick reads the embedded preview/composite. [0] selects layer 0.
        cmd = [
            "magick",
            "-",  # read from stdin
            "-flatten",
            "-auto-orient",
            "-resize", f"{MAX_DIM}x{MAX_DIM}>",
            "-background", "white",
            "-alpha", "remove",
            "-quality", str(QUALITY),
            "jpg:-",
        ]
        proc = subprocess.run(cmd, input=body, capture_output=True, timeout=int(os.environ.get("MAGICK_TIMEOUT", "180")))
        if proc.returncode != 0 or not proc.stdout:
            err = proc.stderr.decode("utf-8", errors="replace")[:200]
            return ("fail", dam_path, f"magick rc={proc.returncode}: {err}")

        s3.put_object(
            Bucket=BUCKET,
            Key=dst_key,
            Body=proc.stdout,
            ContentType="image/jpeg",
        )
        return ("ok", dam_path, len(proc.stdout))
    except subprocess.TimeoutExpired:
        return ("fail", dam_path, "magick timeout")
    except ClientError as e:
        return ("fail", dam_path, f"s3 {e.response['Error']['Code']}")
    except Exception as e:
        return ("fail", dam_path, f"{type(e).__name__}: {e}")


def main():
    manifest = json.load(open(ROOT / "sprite_image_manifest.json"))
    print(f"→ Manifest: {len(manifest)} assets")

    print(f"→ Listing src keys under {SRC_PREFIX}/ ...")
    src_keys = list_existing(SRC_PREFIX)
    print(f"  Found {len(src_keys)} originals on S3")

    print(f"→ Listing dst keys under {DST_PREFIX}/ ...")
    dst_keys = list_existing(DST_PREFIX)
    print(f"  Found {len(dst_keys)} existing thumbnails on S3")

    # Filter
    todo = []
    skip_existing = 0
    skip_missing = 0
    for a in manifest:
        if dst_key_for(a["damPath"]) in dst_keys:
            skip_existing += 1
            continue
        if src_key_for(a["damPath"]) not in src_keys:
            skip_missing += 1
            continue
        todo.append(a)
    print(f"  To convert: {len(todo)}  (skip existing: {skip_existing}, missing src: {skip_missing})")

    if not todo:
        print("Nothing to do.")
        return

    ok = fail = 0
    failures = []
    start = time.time()
    last_log = start

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futures = [ex.submit(convert_one, a, src_keys, dst_keys, None) for a in todo]
        for i, fut in enumerate(as_completed(futures), 1):
            status, dam, info = fut.result()
            if status == "ok":
                ok += 1
            else:
                fail += 1
                failures.append({"damPath": dam, "info": info})
                if fail <= 30:
                    print(f"  ✗ {dam}: {info}", file=sys.stderr)

            now = time.time()
            if i % 100 == 0 or (now - last_log) > 30:
                rate = i / (now - start)
                eta = (len(todo) - i) / max(rate, 0.01)
                print(f"── {i}/{len(todo)} (ok={ok}, fail={fail}) | {rate:.1f}/s | eta {eta/60:.1f}m ──")
                last_log = now

    elapsed = (time.time() - start) / 60
    print(f"\n✅ Done in {elapsed:.1f}m. Converted={ok}, Failed={fail}")
    if failures:
        with open(ROOT / "sprite_thumb_failures.json", "w") as f:
            json.dump(failures, f, indent=2)
        print(f"⚠️  Failures → sprite_thumb_failures.json")


if __name__ == "__main__":
    main()
