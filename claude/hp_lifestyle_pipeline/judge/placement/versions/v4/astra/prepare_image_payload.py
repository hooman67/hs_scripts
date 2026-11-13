#!/usr/bin/env python3
"""Create bounded, hash-bound JPEG derivatives for the Astra feedback call."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ANNOTATION = HERE / "evidence" / "reviewer_0.json"
SOURCE_MANIFEST = (
    ROOT / "judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json"
)
OUTPUT_DIR = HERE / "image_payload"
OUTPUT_MANIFEST = HERE / "evidence" / "image_payload_manifest.json"
MAX_DIMENSION = 1280
JPEG_QUALITY = 82


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def make_derivative(source: Path, expected_sha: str) -> dict:
    if sha256(source) != expected_sha:
        raise RuntimeError(f"Source image hash mismatch: {source}")
    output = OUTPUT_DIR / f"{expected_sha[:24]}.jpg"
    if not output.is_file():
        with Image.open(source) as opened:
            image = ImageOps.exif_transpose(opened).convert("RGB")
            image.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)
            image.save(
                output,
                format="JPEG",
                quality=JPEG_QUALITY,
                optimize=True,
                progressive=True,
                exif=b"",
            )
    with Image.open(output) as derived:
        width, height = derived.size
    return {
        "source_path": str(source),
        "source_sha256": expected_sha,
        "source_bytes": source.stat().st_size,
        "derivative_path": str(output),
        "derivative_sha256": sha256(output),
        "derivative_bytes": output.stat().st_size,
        "derivative_width": width,
        "derivative_height": height,
        "format": "image/jpeg",
        "max_dimension": MAX_DIMENSION,
        "jpeg_quality": JPEG_QUALITY,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    annotations = load(ANNOTATION)
    source_records = {record["id"]: record for record in load(SOURCE_MANIFEST)["records"]}
    pairs = []
    unique: dict[str, dict] = {}
    for annotation in annotations["rows"]:
        record_id = annotation["evalset_item_id"]
        source = source_records[record_id]
        pair = {"record_id": record_id}
        for role, key in (("generated_scene", "generated_image"), ("digital_twin", "twin_image")):
            image = source[key]
            source_path = Path(image["local_path"])
            expected_sha = image["sha256"]
            derivative = unique.get(expected_sha)
            if derivative is None:
                derivative = make_derivative(source_path, expected_sha)
                unique[expected_sha] = derivative
            pair[role] = derivative
        pairs.append(pair)

    payload = {
        "schema_version": "hp-placement-astra-image-payload-v1",
        "source_manifest_path": str(SOURCE_MANIFEST),
        "source_manifest_sha256": sha256(SOURCE_MANIFEST),
        "pair_count": len(pairs),
        "unique_image_count": len(unique),
        "source_bytes_in_sequence": sum(
            pair[role]["source_bytes"]
            for pair in pairs
            for role in ("generated_scene", "digital_twin")
        ),
        "derivative_bytes_in_sequence": sum(
            pair[role]["derivative_bytes"]
            for pair in pairs
            for role in ("generated_scene", "digital_twin")
        ),
        "unique_derivative_bytes": sum(item["derivative_bytes"] for item in unique.values()),
        "pairs": pairs,
    }
    temporary = OUTPUT_MANIFEST.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT_MANIFEST)
    print(json.dumps({
        "manifest": str(OUTPUT_MANIFEST),
        "pairs": len(pairs),
        "unique_images": len(unique),
        "sequence_bytes": payload["derivative_bytes_in_sequence"],
        "unique_bytes": payload["unique_derivative_bytes"],
        "manifest_sha256": sha256(OUTPUT_MANIFEST),
    }))


if __name__ == "__main__":
    main()
