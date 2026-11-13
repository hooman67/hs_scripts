#!/usr/bin/env python3
"""Build and verify the V6 placement-judge asset manifest from live S3 bytes."""

from __future__ import annotations

import hashlib
import json
import struct
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
CACHE = ROOT / "judge/local_runs/v6_placement_assets"
SOURCE = CACHE / "source"
GENERATED = CACHE / "generated"
TWINS = CACHE / "twins"
OUTPUT = ROOT / "judge/placement/versions/v2/data/v6_assets.json"

BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = (
    "eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/"
    "generated_preview_v1"
)
PUBLIC_BASE = f"https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"not a PNG with an IHDR header: {path}")
    return struct.unpack(">II", header[16:24])


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"invalid JSONL at {path}:{line_number}") from exc
    return records


def main() -> None:
    results_path = SOURCE / "results.jsonl"
    top6_path = SOURCE / "prompts_top6_96.json"
    all160_path = SOURCE / "prompts_all_160.json"
    generation_manifest_path = SOURCE / "image_generation_manifest.json"
    inventory_path = SOURCE / "s3_inventory.json"
    gallery_path = SOURCE / "gallery_index.html"

    results = load_jsonl(results_path)
    top6_payload = load_json(top6_path)
    all160_payload = load_json(all160_path)
    generation_manifest = load_json(generation_manifest_path)
    inventory = load_json(inventory_path)

    prompts = top6_payload["prompts"]
    all_prompts = all160_payload["prompts"]
    prompt_by_key = {item["prompt_key"]: item for item in prompts}
    render_by_id = {
        item["render_id"]: item for item in generation_manifest["renders"]
    }
    s3_by_key = {item["Key"]: item for item in inventory["Contents"]}

    image_prefix = f"{PREFIX}/images/"
    twin_prefix = f"{PREFIX}/assets/corrected_inputs/"
    live_image_keys = sorted(key for key in s3_by_key if key.startswith(image_prefix))
    live_twin_keys = sorted(key for key in s3_by_key if key.startswith(twin_prefix))

    expected = generation_manifest["scope"]["expected_images"]
    assert expected == 96
    assert len(results) == expected
    assert len(prompts) == expected
    assert len(all_prompts) == 160
    assert len(live_image_keys) == expected
    assert len(live_twin_keys) == 16
    assert len(prompt_by_key) == expected
    assert len(render_by_id) == 16
    assert all(item["status"] == "done" for item in results)
    assert len({item["row_id"] for item in results}) == expected
    assert len({item["generated_image"]["filename"] for item in results}) == expected
    assert {item["candidate_id"] for item in results} == {
        "p1",
        "p2",
        "p3",
        "p4",
        "p5",
        "p6",
    }

    records = []
    seen_generated = set()
    seen_twins = set()
    for result in sorted(
        results,
        key=lambda item: (
            item["device_id"],
            item["camera_tag"],
            int(item["candidate_id"][1:]),
        ),
    ):
        row_id = result["row_id"]
        prompt_key = result["prompt_key"]
        prompt = prompt_by_key[prompt_key]
        render = render_by_id[result["render_id"]]

        generated_name = result["generated_image"]["filename"]
        generated_path = GENERATED / generated_name
        generated_key = f"{image_prefix}{generated_name}"
        generated_s3 = s3_by_key[generated_key]

        twin_name = f'{result["device_id"]}__{render["camera_name"]}.png'
        twin_path = TWINS / twin_name
        twin_key = f"{twin_prefix}{twin_name}"
        twin_s3 = s3_by_key[twin_key]

        assert generated_path.is_file()
        assert twin_path.is_file()
        generated_hash = sha256(generated_path)
        twin_hash = sha256(twin_path)
        generated_width, generated_height = png_dimensions(generated_path)
        twin_width, twin_height = png_dimensions(twin_path)

        original_prompt = prompt["text"]
        original_prompt_hash = text_sha256(original_prompt)

        assert result["pilot_candidate"]["text"] == original_prompt
        assert result["request_payload"]["prompt"] == original_prompt
        assert result["pilot_candidate"]["text_sha256"] == original_prompt_hash
        assert prompt["text_sha256"] == original_prompt_hash
        assert result["generated_image"]["sha256"] == generated_hash
        assert result["current_render"]["sha256"] == twin_hash
        assert render["sha256"] == twin_hash
        assert generated_s3["Size"] == generated_path.stat().st_size
        assert twin_s3["Size"] == twin_path.stat().st_size
        assert result["generated_image"]["native_width"] == generated_width
        assert result["generated_image"]["native_height"] == generated_height
        assert render["width"] == twin_width
        assert render["height"] == twin_height
        assert result["device_id"] == prompt["device_id"]
        assert result["device_type"] == prompt["device_type"]
        assert result["camera_tag"] == prompt["camera_tag"]
        assert result["candidate_id"] == prompt["id"]

        generated_public_url = f"{PUBLIC_BASE}/images/{generated_name}"
        twin_preview_public_url = (
            f"{PUBLIC_BASE}/assets/corrected_inputs/{twin_name}"
        )
        original_twin_public_url = render["source_gallery_url"]

        records.append(
            {
                "id": row_id,
                "product": prompt["device_display_name"],
                "device": result["device_id"],
                "device_type": result["device_type"],
                "view": {
                    "camera_tag": result["camera_tag"],
                    "source_camera_name": prompt["source_camera_name"],
                    "view_role": prompt["view_role"],
                },
                "image_stage": "scene_generation",
                "candidate_id": result["candidate_id"],
                "scene_prompt": original_prompt,
                "scene_prompt_sha256": original_prompt_hash,
                "scene_prompt_source": {
                    "kind": "original_v6_prompt",
                    "prompt_key": prompt_key,
                    "source_revision": prompt["source_revision"],
                    "bank_rank": prompt["bank_rank"],
                    "environment": prompt["environment"],
                    "rewritten_prompt_included": False,
                },
                "generated_image": {
                    "filename": generated_name,
                    "local_path": str(generated_path),
                    "sha256": generated_hash,
                    "bytes": generated_path.stat().st_size,
                    "width": generated_width,
                    "height": generated_height,
                    "s3_uri": f"s3://{BUCKET}/{generated_key}",
                    "public_url": generated_public_url,
                    "s3_etag": generated_s3["ETag"].strip('"'),
                    "s3_last_modified": generated_s3["LastModified"],
                },
                "twin_image": {
                    "render_id": render["render_id"],
                    "filename": twin_name,
                    "local_path": str(twin_path),
                    "sha256": twin_hash,
                    "bytes": twin_path.stat().st_size,
                    "width": twin_width,
                    "height": twin_height,
                    "source_s3_uri": render["source_s3_uri"],
                    "source_public_url": original_twin_public_url,
                    "preview_s3_uri": f"s3://{BUCKET}/{twin_key}",
                    "preview_public_url": twin_preview_public_url,
                    "s3_etag": twin_s3["ETag"].strip('"'),
                    "s3_last_modified": twin_s3["LastModified"],
                },
                "hashes": {
                    "generated_image_sha256": generated_hash,
                    "twin_image_sha256": twin_hash,
                    "scene_prompt_sha256": original_prompt_hash,
                },
                "dimensions": {
                    "generated_image": {
                        "width": generated_width,
                        "height": generated_height,
                    },
                    "twin_image": {"width": twin_width, "height": twin_height},
                },
                "original_public_urls": {
                    "generated_image": generated_public_url,
                    "twin_image": original_twin_public_url,
                },
            }
        )
        seen_generated.add(generated_name)
        seen_twins.add(twin_name)

    assert seen_generated == {Path(key).name for key in live_image_keys}
    assert seen_twins == {Path(key).name for key in live_twin_keys}

    source_files = {}
    for path in (
        results_path,
        top6_path,
        all160_path,
        generation_manifest_path,
        inventory_path,
        gallery_path,
    ):
        source_files[path.name] = {
            "local_path": str(path),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }

    by_device = {}
    by_device_type = {}
    by_camera_tag = {}
    for record in records:
        by_device[record["device"]] = by_device.get(record["device"], 0) + 1
        by_device_type[record["device_type"]] = (
            by_device_type.get(record["device_type"], 0) + 1
        )
        camera_tag = record["view"]["camera_tag"]
        by_camera_tag[camera_tag] = by_camera_tag.get(camera_tag, 0) + 1

    payload = {
        "schema_version": "hp-placement-v2-v6-assets-v1",
        "expected_count": len(records),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_contract": {
            "image_stage": "scene_generation",
            "judge_inputs": [
                "generated_image",
                "twin_image",
                "device_type",
                "scene_prompt",
            ],
            "scene_prompt_policy": (
                "Use the byte-verified original V6 scene prompt only. The generation "
                "service's rewritten usedPrompt/debugData fields are intentionally excluded."
            ),
        },
        "source": {
            "verification_status": "VERIFIED",
            "verified_as_of": datetime.now(timezone.utc).date().isoformat(),
            "source_class": "primary live S3 objects and frozen V6 exports",
            "bucket": BUCKET,
            "prefix": PREFIX,
            "gallery_url": f"{PUBLIC_BASE}/gallery/index.html",
            "local_cache_root": str(CACHE),
            "source_files": source_files,
        },
        "coverage": {
            "approved_v6_prompt_count": len(all_prompts),
            "published_preview_count": len(records),
            "published_prompt_subset_count": len(prompts),
            "unpublished_approved_prompt_count": len(all_prompts) - len(records),
            "included_candidate_ids": ["p1", "p2", "p3", "p4", "p5", "p6"],
            "excluded_candidate_ids": ["p7", "p8", "p9", "p10"],
            "scope_note": (
                "The live generated_preview_v1 S3 prefix contains 96 images. The 64 "
                "p7-p10 prompts have no image under that published preview prefix and are "
                "excluded even if later local extension artifacts exist."
            ),
        },
        "counts": {
            "records": len(records),
            "unique_generated_images": len(seen_generated),
            "unique_twin_images": len(seen_twins),
            "by_device": dict(sorted(by_device.items())),
            "by_device_type": dict(sorted(by_device_type.items())),
            "by_camera_tag": dict(sorted(by_camera_tag.items())),
        },
        "validation": {
            "all_local_files_present": True,
            "all_local_sha256_match_source_records": True,
            "all_png_dimensions_match_source_records": True,
            "all_live_s3_sizes_match_local_files": True,
            "all_scene_prompts_match_frozen_v6_export": True,
            "rewritten_prompt_fields_present_in_records": False,
            "mismatches": [],
        },
        "records": records,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "records": len(records),
                "unique_twins": len(seen_twins),
                "mismatches": payload["validation"]["mismatches"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
