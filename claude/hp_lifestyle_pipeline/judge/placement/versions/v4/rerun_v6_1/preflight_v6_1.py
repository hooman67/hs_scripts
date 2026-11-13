#!/usr/bin/env python3
"""Read-only validation of the frozen V6.1 160-image judge input."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/"
    "judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json"
)
EXPECTED_MANIFEST_SHA256 = (
    "fd84149fa421c32602358c325b4fb14ed555d3e5033fb92bc2800ab37e6daefc"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--expected-sha256", default=EXPECTED_MANIFEST_SHA256)
    args = parser.parse_args()

    manifest_path = args.manifest.expanduser().resolve()
    require(manifest_path.is_file(), f"missing manifest: {manifest_path}")
    manifest_hash = sha256(manifest_path)
    require(
        manifest_hash == args.expected_sha256,
        f"manifest SHA-256 differs: expected {args.expected_sha256}, found {manifest_hash}",
    )
    payload: Any = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), "manifest must be an object")
    records = payload.get("records")
    require(payload.get("expected_count") == 160, "expected_count must be 160")
    require(isinstance(records, list) and len(records) == 160, "records must contain 160 rows")

    seen_ids: set[str] = set()
    groups: OrderedDict[str, list[int]] = OrderedDict()
    generated_hashes: set[str] = set()
    twin_hashes: set[str] = set()
    device_types: dict[str, int] = {"laptop": 0, "printer": 0}

    for index, record in enumerate(records):
        require(isinstance(record, dict), f"row {index}: record must be an object")
        record_id = record.get("id")
        require(isinstance(record_id, str) and record_id, f"row {index}: missing ID")
        require(record_id not in seen_ids, f"duplicate ID: {record_id}")
        seen_ids.add(record_id)

        product_type = record.get("device_type")
        require(product_type in device_types, f"{record_id}: invalid device_type")
        device_types[product_type] += 1
        require(record.get("image_stage") == "scene_generation", f"{record_id}: bad image stage")

        prompt = record.get("scene_prompt")
        require(isinstance(prompt, str), f"{record_id}: scene_prompt must be text")
        prompt_hash = text_sha256(prompt)
        require(record.get("scene_prompt_sha256") == prompt_hash, f"{record_id}: prompt hash differs")

        hashes = record.get("hashes")
        require(isinstance(hashes, dict), f"{record_id}: hashes object missing")
        require(hashes.get("scene_prompt_sha256") == prompt_hash, f"{record_id}: aggregate prompt hash differs")

        for key, unique_hashes in (
            ("generated_image", generated_hashes),
            ("twin_image", twin_hashes),
        ):
            image = record.get(key)
            require(isinstance(image, dict), f"{record_id}: {key} missing")
            local_path = image.get("local_path")
            expected_hash = image.get("sha256")
            require(isinstance(local_path, str), f"{record_id}: {key}.local_path missing")
            path = Path(local_path)
            require(path.is_absolute() and path.is_file(), f"{record_id}: missing {key}: {path}")
            actual_hash = sha256(path)
            require(actual_hash == expected_hash, f"{record_id}: {key} hash differs")
            require(hashes.get(f"{key}_sha256") == actual_hash, f"{record_id}: aggregate {key} hash differs")
            unique_hashes.add(actual_hash)

        device = record.get("device")
        view = record.get("view")
        source = record.get("scene_prompt_source")
        require(isinstance(device, str) and device, f"{record_id}: device missing")
        require(isinstance(view, dict), f"{record_id}: view missing")
        camera = view.get("camera_tag")
        require(isinstance(camera, str) and camera, f"{record_id}: camera tag missing")
        require(isinstance(source, dict), f"{record_id}: prompt source missing")
        rank = source.get("bank_rank")
        require(isinstance(rank, int) and 1 <= rank <= 10, f"{record_id}: bad bank rank")
        require(record.get("candidate_id") == f"p{rank}", f"{record_id}: candidate/rank mismatch")
        groups.setdefault(f"{device} | {camera}", []).append(rank)

    require(device_types == {"laptop": 80, "printer": 80}, "device type split must be 80/80")
    require(len(generated_hashes) == 160, "generated images must be unique")
    require(len(twin_hashes) == 16, "expected 16 unique digital twins")
    require(len(groups) == 16, f"expected 16 device+camera groups, found {len(groups)}")
    for key, ranks in groups.items():
        require(sorted(ranks) == list(range(1, 11)), f"{key}: ranks must be exactly 1..10")

    print(
        json.dumps(
            {
                "status": "validated_no_model_calls",
                "manifest": str(manifest_path),
                "manifest_sha256": manifest_hash,
                "records": len(records),
                "device_types": device_types,
                "unique_generated_images": len(generated_hashes),
                "unique_twin_images": len(twin_hashes),
                "groups": [{"key": key, "rows": len(ranks)} for key, ranks in groups.items()],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
