#!/usr/bin/env python3
"""Download frozen S3-backed calibration assets and build a verified batch manifest."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlparse


HERE = Path(__file__).resolve().parent
CASES = HERE / "evidence/calibration_cases.json"
SCRATCH = Path("/mnt/localssd/hp_natural_placement_v4_calibration_20261106")
MANIFEST = HERE / "evidence/calibration_manifest.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def download(url: str, path: Path) -> str:
    parsed = urlparse(url)
    prefix = "/asset/"
    if parsed.netloc != "foundry-aws-corp.adobe.io" or not parsed.path.startswith(prefix):
        raise ValueError(f"unsupported asset URL: {url}")
    bucket_and_key = unquote(parsed.path[len(prefix) :])
    bucket, separator, key = bucket_and_key.partition("/")
    if not separator or not bucket or not key:
        raise ValueError(f"malformed asset URL: {url}")
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "aws",
            "s3",
            "cp",
            f"s3://{bucket}/{key}",
            str(path),
            "--region",
            "us-west-2",
            "--only-show-errors",
        ],
        check=True,
    )
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    payload = json.loads(CASES.read_text())
    records = []
    for case in payload["cases"]:
        record_id = case["id"]
        record_dir = SCRATCH / record_id
        generated = record_dir / "generated.png"
        twin = record_dir / "twin.png"
        generated_hash = download(case["generated_image"], generated)
        twin_hash = download(case["twin_image"], twin)
        prompt_hash = hashlib.sha256(case["scene_prompt"].encode("utf-8")).hexdigest()
        records.append(
            {
                "id": record_id,
                "generated_image": {
                    "local_path": str(generated),
                    "sha256": generated_hash,
                    "source_url": case["generated_image"],
                },
                "twin_image": {
                    "local_path": str(twin),
                    "sha256": twin_hash,
                    "source_url": case["twin_image"],
                },
                "device_type": case["product_type"],
                "scene_prompt": case["scene_prompt"],
                "scene_prompt_sha256": prompt_hash,
                "scene_prompt_source": {
                    "kind": "frozen_v6_1_scene_prompt",
                    "rewritten_prompt_included": False,
                },
                "image_stage": "scene_generation",
                "hashes": {
                    "generated_image_sha256": generated_hash,
                    "twin_image_sha256": twin_hash,
                    "scene_prompt_sha256": prompt_hash,
                },
            }
        )
    manifest = {
        "schema_version": 1,
        "expected_count": len(records),
        "calibration_labels": str(CASES),
        "records": records,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(MANIFEST)


if __name__ == "__main__":
    main()
