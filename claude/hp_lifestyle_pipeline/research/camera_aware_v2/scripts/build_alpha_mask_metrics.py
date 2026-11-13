#!/usr/bin/env python3
"""Measure RGBA mask occupancy and bounds for extracted HP camera PNGs."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import PIL
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA = PROJECT_ROOT / "research" / "camera_aware" / "data"


def rounded(value: float) -> float:
    return round(value, 8)


def normalized_bbox(
    bbox: tuple[int, int, int, int] | None, width: int, height: int
) -> dict | None:
    if bbox is None:
        return None
    left, top, right, bottom = bbox
    return {
        "pixel_xyxy_right_bottom_exclusive": [left, top, right, bottom],
        "normalized_xyxy_right_bottom_exclusive": [
            rounded(left / width),
            rounded(top / height),
            rounded(right / width),
            rounded(bottom / height),
        ],
        "width_px": right - left,
        "height_px": bottom - top,
        "normalized_width": rounded((right - left) / width),
        "normalized_height": rounded((bottom - top) / height),
        "normalized_area": rounded(((right - left) * (bottom - top)) / (width * height)),
        "edge_contact": {
            "left": left == 0,
            "top": top == 0,
            "right": right == width,
            "bottom": bottom == height,
            "any": left == 0 or top == 0 or right == width or bottom == height,
        },
    }


def measure(asset: dict) -> dict:
    path = Path(asset["extracted_absolute_path"])
    with Image.open(path) as image:
        bands = image.getbands()
        has_alpha = "A" in bands
        width, height = image.size
        total = width * height
        result = {
            "device_family": asset["device_family"],
            "source_declared_device_type": asset["source_declared_device_type"],
            "effective_device_type": asset["effective_device_type"],
            "device_type_correction_id": asset.get("device_type_correction_id"),
            "device_type_correction_registry_version": asset.get(
                "device_type_correction_registry_version"
            ),
            "device_id": asset["device_id"],
            "device_asset_name_from_folder": asset["device_asset_name_from_folder"],
            "camera_name_exact": asset["camera_name_exact"],
            "zip_filename": asset["zip_filename"],
            "extracted_absolute_path": str(path),
            "source_png_sha256": asset["sha256"],
            "width_px": width,
            "height_px": height,
            "source_mode": image.mode,
            "source_bands": list(bands),
            "has_alpha_channel": has_alpha,
        }
        if not has_alpha:
            result.update(
                {
                    "alpha_validity": "no_alpha_channel",
                    "alpha_extrema": None,
                    "alpha_unique_value_count": 0,
                    "transparent_pixel_count": None,
                    "semitransparent_pixel_count": None,
                    "opaque_pixel_count": None,
                    "alpha_nonzero_pixel_count": None,
                    "alpha_nonzero_occupancy_fraction": None,
                    "alpha_weighted_occupancy_fraction": None,
                    "alpha_opaque_occupancy_fraction": None,
                    "alpha_nonzero_bbox": None,
                    "alpha_core_ge_128_bbox": None,
                }
            )
            return result

        alpha = image.getchannel("A")
        histogram = alpha.histogram()
        minimum, maximum = alpha.getextrema()
        transparent = histogram[0]
        semitransparent = sum(histogram[1:255])
        opaque = histogram[255]
        nonzero = total - transparent
        unique = sum(count > 0 for count in histogram)
        alpha_weight = sum(value * count for value, count in enumerate(histogram))
        if minimum == maximum == 255:
            validity = "alpha_present_but_fully_opaque"
        elif minimum == maximum == 0:
            validity = "alpha_present_but_fully_transparent"
        elif minimum == 0 and maximum > 0:
            validity = "genuine_varying_transparency"
        else:
            validity = "varying_alpha_without_fully_transparent_pixels"

        core = alpha.point(lambda value: 255 if value >= 128 else 0)
        result.update(
            {
                "alpha_validity": validity,
                "alpha_extrema": [minimum, maximum],
                "alpha_unique_value_count": unique,
                "transparent_pixel_count": transparent,
                "semitransparent_pixel_count": semitransparent,
                "opaque_pixel_count": opaque,
                "alpha_nonzero_pixel_count": nonzero,
                "alpha_nonzero_occupancy_fraction": rounded(nonzero / total),
                "alpha_weighted_occupancy_fraction": rounded(alpha_weight / (255 * total)),
                "alpha_opaque_occupancy_fraction": rounded(opaque / total),
                "alpha_nonzero_bbox": normalized_bbox(alpha.getbbox(), width, height),
                "alpha_core_ge_128_bbox": normalized_bbox(core.getbbox(), width, height),
                "mask_semantics": "All alpha>0 pixels are counted. Any shadow encoded in alpha is included because alpha alone does not identify semantic product body versus shadow.",
            }
        )
        return result


def comparison_record(
    grouping_basis: str, grouping_value: str, camera: str, records: list[dict]
) -> dict:
    ordered = sorted(
        records,
        key=lambda item: (
            item["alpha_nonzero_occupancy_fraction"] is None,
            item["alpha_nonzero_occupancy_fraction"] or 0,
            item["device_id"],
        ),
    )
    valid = [item for item in ordered if item["alpha_nonzero_occupancy_fraction"] is not None]
    minimum = valid[0] if valid else None
    maximum = valid[-1] if valid else None
    min_fraction = minimum["alpha_nonzero_occupancy_fraction"] if minimum else None
    max_fraction = maximum["alpha_nonzero_occupancy_fraction"] if maximum else None
    ratio = None
    if len(valid) >= 2 and min_fraction and max_fraction is not None:
        ratio = rounded(max_fraction / min_fraction)
    effective_types = sorted({item["effective_device_type"] for item in records})
    source_declared_types = sorted(
        {item["source_declared_device_type"] for item in records}
    )
    return {
        "grouping_basis": grouping_basis,
        "grouping_value": grouping_value,
        "comparison_scope": "cross_type"
        if len(effective_types) > 1
        else "within_effective_type",
        "source_declared_device_types": source_declared_types,
        "effective_device_types": effective_types,
        "camera_name_exact": camera,
        "model_count": len(records),
        "models": [
            {
                "device_id": item["device_id"],
                "source_declared_device_type": item[
                    "source_declared_device_type"
                ],
                "effective_device_type": item["effective_device_type"],
                "occupancy_fraction": item["alpha_nonzero_occupancy_fraction"],
                "alpha_weighted_occupancy_fraction": item[
                    "alpha_weighted_occupancy_fraction"
                ],
                "bbox_normalized_xyxy": item["alpha_nonzero_bbox"][
                    "normalized_xyxy_right_bottom_exclusive"
                ]
                if item["alpha_nonzero_bbox"]
                else None,
                "edge_contact": item["alpha_nonzero_bbox"]["edge_contact"]
                if item["alpha_nonzero_bbox"]
                else None,
            }
            for item in ordered
        ],
        "minimum": {
            "device_id": minimum["device_id"],
            "effective_device_type": minimum["effective_device_type"],
            "occupancy_fraction": min_fraction,
        }
        if minimum
        else None,
        "maximum": {
            "device_id": maximum["device_id"],
            "effective_device_type": maximum["effective_device_type"],
            "occupancy_fraction": max_fraction,
        }
        if maximum
        else None,
        "absolute_spread_fraction": rounded(max_fraction - min_fraction)
        if len(valid) >= 2 and minimum and maximum
        else None,
        "max_to_min_ratio": ratio,
        "edge_contact_model_count": sum(
            bool(item["alpha_nonzero_bbox"] and item["alpha_nonzero_bbox"]["edge_contact"]["any"])
            for item in records
        ),
    }


def main() -> None:
    catalog = json.loads((DATA / "camera_catalog.json").read_text(encoding="utf-8"))
    metrics = [measure(asset) for asset in catalog["high_resolution_assets"]]
    source_declared_groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    effective_type_groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for item in metrics:
        source_declared_groups[
            (item["source_declared_device_type"], item["camera_name_exact"])
        ].append(item)
        effective_type_groups[
            (item["effective_device_type"], item["camera_name_exact"])
        ].append(item)
    source_group_comparisons = [
        comparison_record("source_declared_device_type", declared, camera, records)
        for (declared, camera), records in sorted(source_declared_groups.items())
    ]
    within_effective_type_comparisons = [
        comparison_record("effective_device_type", effective, camera, records)
        for (effective, camera), records in sorted(effective_type_groups.items())
    ]
    summary = {
        "schema_version": 2,
        "as_of": datetime.now(timezone.utc).isoformat(),
        "source_catalog_absolute_path": str(DATA / "camera_catalog.json"),
        "device_type_correction_registry_absolute_path": str(
            DATA / "device_type_corrections.json"
        ),
        "source_asset_count": len(metrics),
        "tool_versions": {"pillow": PIL.__version__},
        "alpha_validity_counts": dict(
            sorted(
                {
                    validity: sum(item["alpha_validity"] == validity for item in metrics)
                    for validity in {item["alpha_validity"] for item in metrics}
                }.items()
            )
        ),
        "all_assets_have_genuine_varying_transparency": all(
            item["alpha_validity"] == "genuine_varying_transparency" for item in metrics
        ),
        "edge_contact_asset_count": sum(
            bool(item["alpha_nonzero_bbox"] and item["alpha_nonzero_bbox"]["edge_contact"]["any"])
            for item in metrics
        ),
        "core_ge_128_edge_contact_asset_count": sum(
            bool(
                item["alpha_core_ge_128_bbox"]
                and item["alpha_core_ge_128_bbox"]["edge_contact"]["any"]
            )
            for item in metrics
        ),
        "occupancy_definition": "alpha_nonzero_pixel_count / total pixels; includes any shadow represented by nonzero alpha",
        "bbox_definition": "tight bounds around alpha>0 pixels; right/bottom are exclusive and normalized by source width/height",
        "shadow_limitation": "The alpha channel does not label product body and shadow separately. Metrics therefore include any shadow carried by alpha; no shadow exclusion is claimed.",
        "comparison_semantics": "Comparisons grouped by source-declared filename type are explicitly marked cross_type when corrected effective types differ. Within-effective-type comparisons never compare printer Magic with miniPC Messi.",
        "assets": metrics,
        "same_camera_source_declared_group_comparisons": source_group_comparisons,
        "same_camera_within_effective_type_comparisons": within_effective_type_comparisons,
    }
    output = DATA / "camera_alpha_mask_metrics.json"
    output.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with (DATA / "camera_alpha_mask_metrics.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        fields = [
            "device_family",
            "source_declared_device_type",
            "effective_device_type",
            "device_type_correction_id",
            "device_type_correction_registry_version",
            "device_id",
            "device_asset_name_from_folder",
            "camera_name_exact",
            "zip_filename",
            "source_png_sha256",
            "width_px",
            "height_px",
            "source_mode",
            "alpha_validity",
            "alpha_unique_value_count",
            "alpha_nonzero_occupancy_fraction",
            "alpha_weighted_occupancy_fraction",
            "alpha_opaque_occupancy_fraction",
            "bbox_left_normalized",
            "bbox_top_normalized",
            "bbox_right_normalized",
            "bbox_bottom_normalized",
            "edge_contact_left",
            "edge_contact_top",
            "edge_contact_right",
            "edge_contact_bottom",
            "edge_contact_any",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in metrics:
            bbox = item["alpha_nonzero_bbox"]
            coords = bbox["normalized_xyxy_right_bottom_exclusive"] if bbox else [None] * 4
            edge = bbox["edge_contact"] if bbox else {}
            writer.writerow(
                {
                    **{key: item.get(key) for key in fields},
                    "bbox_left_normalized": coords[0],
                    "bbox_top_normalized": coords[1],
                    "bbox_right_normalized": coords[2],
                    "bbox_bottom_normalized": coords[3],
                    "edge_contact_left": edge.get("left"),
                    "edge_contact_top": edge.get("top"),
                    "edge_contact_right": edge.get("right"),
                    "edge_contact_bottom": edge.get("bottom"),
                    "edge_contact_any": edge.get("any"),
                }
            )

    with (DATA / "same_camera_occupancy_comparison.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        fields = [
            "grouping_basis",
            "grouping_value",
            "comparison_scope",
            "source_declared_device_types",
            "effective_device_types",
            "camera_name_exact",
            "model_count",
            "minimum_device_id",
            "minimum_effective_device_type",
            "minimum_occupancy_fraction",
            "maximum_device_id",
            "maximum_effective_device_type",
            "maximum_occupancy_fraction",
            "absolute_spread_fraction",
            "max_to_min_ratio",
            "edge_contact_model_count",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in source_group_comparisons:
            writer.writerow(
                {
                    "grouping_basis": item["grouping_basis"],
                    "grouping_value": item["grouping_value"],
                    "comparison_scope": item["comparison_scope"],
                    "source_declared_device_types": "|".join(
                        item["source_declared_device_types"]
                    ),
                    "effective_device_types": "|".join(
                        item["effective_device_types"]
                    ),
                    "camera_name_exact": item["camera_name_exact"],
                    "model_count": item["model_count"],
                    "minimum_device_id": item["minimum"]["device_id"]
                    if item["minimum"]
                    else None,
                    "minimum_effective_device_type": item["minimum"][
                        "effective_device_type"
                    ]
                    if item["minimum"]
                    else None,
                    "minimum_occupancy_fraction": item["minimum"]["occupancy_fraction"]
                    if item["minimum"]
                    else None,
                    "maximum_device_id": item["maximum"]["device_id"]
                    if item["maximum"]
                    else None,
                    "maximum_effective_device_type": item["maximum"][
                        "effective_device_type"
                    ]
                    if item["maximum"]
                    else None,
                    "maximum_occupancy_fraction": item["maximum"]["occupancy_fraction"]
                    if item["maximum"]
                    else None,
                    "absolute_spread_fraction": item["absolute_spread_fraction"],
                    "max_to_min_ratio": item["max_to_min_ratio"],
                    "edge_contact_model_count": item["edge_contact_model_count"],
                }
            )
    effective_csv = DATA / "same_camera_within_effective_type_comparison.csv"
    with effective_csv.open("w", newline="", encoding="utf-8") as handle:
        fields = [
            "effective_device_type",
            "camera_name_exact",
            "model_count",
            "minimum_device_id",
            "minimum_occupancy_fraction",
            "maximum_device_id",
            "maximum_occupancy_fraction",
            "absolute_spread_fraction",
            "max_to_min_ratio",
            "edge_contact_model_count",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in within_effective_type_comparisons:
            writer.writerow(
                {
                    "effective_device_type": item["grouping_value"],
                    "camera_name_exact": item["camera_name_exact"],
                    "model_count": item["model_count"],
                    "minimum_device_id": item["minimum"]["device_id"]
                    if item["minimum"]
                    else None,
                    "minimum_occupancy_fraction": item["minimum"][
                        "occupancy_fraction"
                    ]
                    if item["minimum"]
                    else None,
                    "maximum_device_id": item["maximum"]["device_id"]
                    if item["maximum"]
                    else None,
                    "maximum_occupancy_fraction": item["maximum"][
                        "occupancy_fraction"
                    ]
                    if item["maximum"]
                    else None,
                    "absolute_spread_fraction": item["absolute_spread_fraction"],
                    "max_to_min_ratio": item["max_to_min_ratio"],
                    "edge_contact_model_count": item["edge_contact_model_count"],
                }
            )
    print(
        json.dumps(
            {
                "assets": len(metrics),
                "alpha_validity_counts": summary["alpha_validity_counts"],
                "edge_contact_asset_count": summary["edge_contact_asset_count"],
                "source_declared_group_comparisons": len(source_group_comparisons),
                "within_effective_type_comparisons": len(
                    within_effective_type_comparisons
                ),
                "output": str(output),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
