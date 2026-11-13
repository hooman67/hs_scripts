#!/usr/bin/env python3
"""Build the immutable source × camera/render manifest for the camera-V2 eval."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVAL_ROOT = Path(__file__).resolve().parent
V2_ROOT = PROJECT_ROOT / "research/source_messaging_v1_to_v6/versions/v2"
CAMERA_DATA_ROOT = PROJECT_ROOT / "research/camera_aware_v2/data"
SOURCE_ROOT = PROJECT_ROOT / "research/source_messaging_v1_to_v6/data/source_json"
HISTORICAL_DATA = (
    PROJECT_ROOT
    / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/data.js"
)
CATALOG_PATH = CAMERA_DATA_ROOT / "camera_catalog.json"
sys.path.insert(0, str(V2_ROOT))

from camera_profile_resolver import load_registry, resolve_profile  # noqa: E402


EXPECTED_SOURCE_COUNTS = {"laptop": 3, "printer": 6}
EXPECTED_RENDER_COUNTS = {"laptop": 161, "printer": 41}
EXPECTED_CASE_COUNT = 369
EXPECTED_PAIR_COUNT = 729
OUTPUT_DIMENSIONS = (2560, 1440)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def compact_camera_tag(device_type: str, source_camera_name: str) -> str:
    compact = "".join(
        part if part.isupper() else part[:1].upper() + part[1:]
        for part in source_camera_name.split("_")
    )
    return f"{device_type}_{compact}"


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")


def load_historical_data() -> dict[str, Any]:
    raw = HISTORICAL_DATA.read_text(encoding="utf-8")
    prefix = "const EVAL_DATA = "
    if not raw.startswith(prefix):
        raise RuntimeError("Historical gallery data has an unexpected wrapper")
    return json.loads(raw[len(prefix) :].strip().removesuffix(";"))


def source_inventory() -> list[dict[str, Any]]:
    historical = load_historical_data()
    category_by_source: dict[str, str] = {}
    first_seen: list[str] = []
    for prompt in historical["prompts"]:
        source_id = prompt["source_id"]
        category = prompt["device_category"].casefold()
        previous = category_by_source.setdefault(source_id, category)
        if previous != category:
            raise RuntimeError(f"Conflicting historical categories for {source_id}")
        if source_id not in first_seen:
            first_seen.append(source_id)
    if len(category_by_source) != 9:
        raise RuntimeError("Historical gallery must contain exactly nine source IDs")

    sources = []
    for device_type in ("laptop", "printer"):
        for source_id in first_seen:
            if category_by_source[source_id] != device_type:
                continue
            path = (SOURCE_ROOT / f"{source_id}.json").resolve()
            source_value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(source_value, dict):
                raise RuntimeError(f"Source is not a JSON object: {path}")
            sources.append(
                {
                    "source_id": source_id,
                    "device_type": device_type,
                    "source_json_path": str(path),
                    "sha256": file_sha256(path),
                    "bytes": path.stat().st_size,
                    "historical_category_evidence": {
                        "path": str(HISTORICAL_DATA.resolve()),
                        "device_category": device_type.title(),
                    },
                    "runtime_product_name_supplied": False,
                }
            )
    actual = Counter(source["device_type"] for source in sources)
    if dict(actual) != EXPECTED_SOURCE_COUNTS:
        raise RuntimeError(f"Unexpected source counts: {actual}")
    return sources


def render_inventory() -> list[dict[str, Any]]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    renders = []
    seen_ids: set[str] = set()
    for asset in catalog["high_resolution_assets"]:
        device_type = asset["effective_device_type"]
        if device_type == "miniPC":
            continue
        if device_type not in EXPECTED_RENDER_COUNTS:
            raise RuntimeError(f"Unexpected included device type: {device_type}")
        path = Path(asset["extracted_absolute_path"]).resolve()
        if file_sha256(path) != asset["sha256"]:
            raise RuntimeError(f"Render SHA-256 differs from catalog: {path}")
        if path.stat().st_size != asset["bytes"]:
            raise RuntimeError(f"Render byte size differs from catalog: {path}")
        if (asset["width_px"], asset["height_px"]) != (1024, 576):
            raise RuntimeError(f"Unexpected render dimensions: {path}")

        product_stem = asset["device_asset_name_from_folder"].split(".", 1)[0]
        render_id = (
            f"{device_type}_{slug(product_stem)}__{slug(asset['camera_name_exact'])}"
        )
        if render_id in seen_ids:
            raise RuntimeError(f"Duplicate render ID: {render_id}")
        seen_ids.add(render_id)
        camera_tag = compact_camera_tag(device_type, asset["camera_name_exact"])
        renders.append(
            {
                "render_id": render_id,
                "device_type": device_type,
                "product_provenance": {
                    "device_id": asset["device_id"],
                    "device_asset_name_from_folder": asset[
                        "device_asset_name_from_folder"
                    ],
                    "source_declared_device_type": asset[
                        "source_declared_device_type"
                    ],
                    "effective_device_type": device_type,
                    "zip_filename": asset["zip_filename"],
                },
                "source_camera_name": asset["camera_name_exact"],
                "camera_tag": camera_tag,
                "path": str(path),
                "sha256": asset["sha256"],
                "bytes": asset["bytes"],
                "width": asset["width_px"],
                "height": asset["height_px"],
                "output_width": OUTPUT_DIMENSIONS[0],
                "output_height": OUTPUT_DIMENSIONS[1],
                "preserve_aspect_ratio": True,
            }
        )
    actual = Counter(render["device_type"] for render in renders)
    if dict(actual) != EXPECTED_RENDER_COUNTS:
        raise RuntimeError(f"Unexpected render counts: {actual}")
    return renders


def expected_camera(registry: dict[str, Any], camera_tag: str) -> dict[str, Any]:
    resolved = resolve_profile(registry, camera_tag)
    profile = resolved["effective_profile"]
    return {
        "requested_tag": resolved["requested_tag"],
        "resolved_tag": resolved["resolved_tag"],
        "device_type": resolved["device_type"],
        "profile_version": resolved["profile_version"],
        "resolution": resolved["resolution"],
        "framing": profile["framing"],
        "elevation": profile["elevation"],
        "max_local_props": profile["max_local_props"],
        "max_background_details": profile["max_background_details"],
        "people_policy": profile["people_policy"],
    }


def build() -> dict[str, Any]:
    sources = source_inventory()
    renders = render_inventory()
    registry = load_registry(V2_ROOT / "camera_profiles.json")
    renders_by_type_tag: dict[tuple[str, str], list[str]] = {}
    for render in renders:
        renders_by_type_tag.setdefault(
            (render["device_type"], render["camera_tag"]), []
        ).append(render["render_id"])

    inputs_dir = EVAL_ROOT / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    cases = []
    for source in sources:
        tags = sorted(
            tag
            for device_type, tag in renders_by_type_tag
            if device_type == source["device_type"]
        )
        for camera_tag in tags:
            case_id = f"{source['source_id']}__{camera_tag}"
            source_value = json.loads(
                Path(source["source_json_path"]).read_text(encoding="utf-8")
            )
            request_input = {
                "source_messaging": source_value,
                "camera_tag": camera_tag,
            }
            input_path = (inputs_dir / f"{case_id}.json").resolve()
            input_path.write_text(
                json.dumps(request_input, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            expectation = expected_camera(registry, camera_tag)
            fallback = expectation["resolution"] in {"unknown", "missing"}
            if camera_tag == "laptop_CAMReview" and not fallback:
                raise RuntimeError("laptop_CAMReview must remain an unknown fallback")
            cases.append(
                {
                    "case_id": case_id,
                    "source_id": source["source_id"],
                    "device_type": source["device_type"],
                    "camera_tag": camera_tag,
                    "input_path": str(input_path),
                    "input_sha256": file_sha256(input_path),
                    "render_ids": sorted(
                        renders_by_type_tag[(source["device_type"], camera_tag)]
                    ),
                    "expected_camera": expectation,
                    "unknown_camera_fallback": fallback,
                    "requires_manual_fallback_review": fallback,
                }
            )

    pair_count = sum(len(case["render_ids"]) for case in cases)
    if len(cases) != EXPECTED_CASE_COUNT or pair_count != EXPECTED_PAIR_COUNT:
        raise RuntimeError(
            f"Expected {EXPECTED_CASE_COUNT} cases/{EXPECTED_PAIR_COUNT} pairs, "
            f"got {len(cases)}/{pair_count}"
        )
    unknown_cases = [case for case in cases if case["unknown_camera_fallback"]]
    if len(unknown_cases) != 3 or {
        case["camera_tag"] for case in unknown_cases
    } != {"laptop_CAMReview"}:
        raise RuntimeError("Expected exactly three laptop_CAMReview fallback cases")

    manifest = {
        "version": "hp-lifestyle-camera-v2-eval-2026-10-22-v1",
        "status": "manifest_ready_no_model_or_image_calls",
        "scope": {
            "production_sources_only": True,
            "excluded_device_types": ["miniPC"],
            "runtime_input_fields": ["source_messaging", "camera_tag"],
            "runtime_product_names_supplied": False,
            "render_aspect_ratio_policy": "preserve_original",
            "one_prompt_response_per_unique_source_camera_tag": True,
        },
        "model": {
            "deployment": "gpt-5.5",
            "reasoning_effort": "medium",
            "max_completion_tokens": 8000,
            "temperature": None,
            "strict_output_schema": True,
            "max_concurrency": 2,
            "max_transient_attempts": 100,
        },
        "provenance": {
            "system_prompt_path": str((V2_ROOT / "system_prompt.md").resolve()),
            "system_prompt_sha256": file_sha256(V2_ROOT / "system_prompt.md"),
            "input_schema_path": str((V2_ROOT / "input.schema.json").resolve()),
            "input_schema_sha256": file_sha256(V2_ROOT / "input.schema.json"),
            "output_schema_path": str((V2_ROOT / "output.schema.json").resolve()),
            "output_schema_sha256": file_sha256(V2_ROOT / "output.schema.json"),
            "camera_profiles_path": str(
                (V2_ROOT / "camera_profiles.json").resolve()
            ),
            "camera_profiles_sha256": file_sha256(V2_ROOT / "camera_profiles.json"),
            "camera_catalog_path": str(CATALOG_PATH.resolve()),
            "camera_catalog_sha256": file_sha256(CATALOG_PATH),
            "historical_source_category_path": str(HISTORICAL_DATA.resolve()),
            "historical_source_category_sha256": file_sha256(HISTORICAL_DATA),
        },
        "counts": {
            "source_count": len(sources),
            "source_counts_by_device_type": dict(
                Counter(source["device_type"] for source in sources)
            ),
            "included_render_count": len(renders),
            "render_counts_by_device_type": dict(
                Counter(render["device_type"] for render in renders)
            ),
            "excluded_minipc_render_count": 41,
            "unique_camera_tag_counts_by_device_type": {
                device_type: len(
                    {
                        render["camera_tag"]
                        for render in renders
                        if render["device_type"] == device_type
                    }
                )
                for device_type in ("laptop", "printer")
            },
            "case_count": len(cases),
            "source_render_pair_count": pair_count,
            "unknown_fallback_case_count": len(unknown_cases),
        },
        "join_contract": {
            "source_key": "sources[].source_id",
            "render_key": "renders[].render_id",
            "case_key": "cases[].case_id",
            "case_source_join": "cases[].source_id -> sources[].source_id",
            "case_render_join": "cases[].render_ids[] -> renders[].render_id",
            "case_output_join": "accepted_prompt_cases.cases[case_id]",
            "source_render_pair_id": "{case_id}__{render_id}",
        },
        "sources": sources,
        "renders": renders,
        "cases": cases,
    }
    return manifest


def main() -> None:
    manifest = build()
    target = EVAL_ROOT / "manifest.json"
    target.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "manifest": str(target.resolve()),
                "sha256": file_sha256(target),
                "counts": manifest["counts"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
