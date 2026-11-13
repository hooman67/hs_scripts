#!/usr/bin/env python3
"""Download placement-judge image assets and build audit manifests/contact sheets.

AWS credentials are intentionally supplied only by the caller's environment.
The project workflow runs this script after sourcing
~/.claude/hshariati/aws_creds.env in the same shell.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

import boto3
from botocore.config import Config
from PIL import Image, ImageDraw, ImageFont, ImageOps


PLACEMENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PLACEMENT_DIR.parents[1]
JUDGE_DIR = PLACEMENT_DIR.parent
SOURCE_DIR = PLACEMENT_DIR / "data" / "sources"
COMPARISON_REPORT = "hp-v13-v14-laptop-printer30-20261103T015107Z-viewer"
REFERENCE_REPORT = "printer-original-full-guidance-analysis-20261104T222046Z"
DEFAULT_ASSET_ROOT = JUDGE_DIR / "local_runs" / "placement_assets"
DEFAULT_MANIFEST = PLACEMENT_DIR / "data" / "assets.json"
BASELINE_SHEET_ROWS = (1, 2, 5, 11, 25)
PANEL_WIDTH = 600
PANEL_IMAGE_HEIGHT = 450
PANEL_LABEL_HEIGHT = 38


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asset-root", type=Path, default=DEFAULT_ASSET_ROOT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--comparison-data",
        type=Path,
        default=SOURCE_DIR / COMPARISON_REPORT / "data.json",
    )
    parser.add_argument(
        "--comparison-provenance",
        type=Path,
        default=SOURCE_DIR / COMPARISON_REPORT / "provenance.json",
    )
    parser.add_argument(
        "--reference-data",
        type=Path,
        default=SOURCE_DIR / REFERENCE_REPORT / "data.json",
    )
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=SOURCE_DIR / "manifest.json",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Download assets again even when an existing local file validates.",
    )
    parser.add_argument(
        "--skip-contact-sheets",
        action="store_true",
        help="Prepare images and the manifest without contact sheets.",
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_s3_uri(uri: str) -> tuple[str, str]:
    parsed = urlparse(uri)
    if parsed.scheme != "s3" or not parsed.netloc or not parsed.path.lstrip("/"):
        raise ValueError(f"Expected an s3:// URI, got {uri!r}")
    return parsed.netloc, unquote(parsed.path.lstrip("/"))


def report_s3_prefix(source_manifest: list[dict[str, Any]], report: str) -> str:
    suffix = f"/{report}/data.json"
    matches = [
        item["s3_uri"]
        for item in source_manifest
        if item.get("report") == report and item.get("s3_uri", "").endswith(suffix)
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected one S3 data.json source for {report}; found {len(matches)}")
    return matches[0].rsplit("/", 1)[0]


def gateway_url_to_s3(url: str) -> str:
    parsed = urlparse(url)
    marker = "/asset/"
    if parsed.scheme not in {"http", "https"} or marker not in parsed.path:
        raise ValueError(f"Unsupported reference image URL: {url!r}")
    asset_path = unquote(parsed.path.split(marker, 1)[1]).lstrip("/")
    bucket, separator, key = asset_path.partition("/")
    if not separator or not bucket or not key:
        raise ValueError(f"Reference URL does not contain bucket and key: {url!r}")
    return f"s3://{bucket}/{key}"


def image_metadata(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        return image.size


def download_asset(
    client: Any,
    s3_uri: str,
    local_path: Path,
    expected_sha256: str | None,
    refresh: bool,
) -> tuple[str, bool]:
    if local_path.exists() and not refresh:
        existing_hash = sha256_file(local_path)
        if expected_sha256 is None or existing_hash == expected_sha256:
            image_metadata(local_path)
            return existing_hash, False

    local_path.parent.mkdir(parents=True, exist_ok=True)
    bucket, key = parse_s3_uri(s3_uri)
    temporary_path = local_path.with_name(f".{local_path.name}.part")
    try:
        client.download_file(bucket, key, os.fspath(temporary_path))
        downloaded_hash = sha256_file(temporary_path)
        if expected_sha256 is not None and downloaded_hash != expected_sha256:
            raise ValueError(
                f"SHA-256 mismatch for {s3_uri}: expected {expected_sha256}, "
                f"downloaded {downloaded_hash}"
            )
        image_metadata(temporary_path)
        temporary_path.replace(local_path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return downloaded_hash, True


def comparison_specs(
    data: dict[str, Any],
    provenance: dict[str, Any],
    s3_prefix: str,
    asset_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    specs: list[dict[str, Any]] = []
    unavailable: list[dict[str, Any]] = []
    expected_hashes = provenance.get("sha256", {})
    variant_map = {
        "product_input.png": ("product_input", "product_input"),
        "v13_final.png": ("v13", "generated_final"),
        "v14_final.png": ("v14", "generated_final"),
    }

    if len(data.get("rows", [])) != 30:
        raise ValueError(f"Expected 30 comparison rows, found {len(data.get('rows', []))}")

    for row in data["rows"]:
        meta = row["meta_data"]
        row_number = int(meta["row_idx"])
        case_id = meta["evalset_item_id"]
        info = meta["key_val_informations"]
        seen_variants: set[str] = set()
        for image in row.get("images", []):
            source_path = image.get("image_src")
            if image.get("asset_type") != "image" or not source_path:
                label = image.get("meta_text", {}).get("Label", "").lower()
                if "v13" in label:
                    unavailable.append(
                        {
                            "source_report": COMPARISON_REPORT,
                            "row": row_number,
                            "case_id": case_id,
                            "variant": "v13",
                            "reason": "source report contains no image asset",
                        }
                    )
                continue
            basename = Path(source_path).name
            if basename not in variant_map:
                continue
            variant, asset_type = variant_map[basename]
            if variant in seen_variants:
                raise ValueError(f"Duplicate {variant} asset in comparison row {row_number}")
            seen_variants.add(variant)
            local_path = asset_root / "comparison" / f"row_{row_number:02d}" / basename
            specs.append(
                {
                    "id": f"comparison-row-{row_number:02d}-{variant}",
                    "source_report": COMPARISON_REPORT,
                    "row": row_number,
                    "case_id": case_id,
                    "device": info.get("Device"),
                    "variant": variant,
                    "type": asset_type,
                    "original_prompt": info.get("Original prompt"),
                    "s3_url": f"{s3_prefix}/{source_path}",
                    "local_path": os.fspath(local_path.resolve()),
                    "expected_sha256": expected_hashes.get(source_path),
                    "declared_width": image.get("width"),
                    "declared_height": image.get("height"),
                }
            )
        if "product_input" not in seen_variants or "v14" not in seen_variants:
            raise ValueError(f"Comparison row {row_number} lacks product_input or V14")
    return specs, unavailable


def reference_specs(data: dict[str, Any], asset_root: Path) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for row in data.get("rows", []):
        image_assets = [item for item in row.get("images", []) if item.get("asset_type") == "image"]
        if not image_assets:
            continue
        if len(image_assets) != 1:
            raise ValueError(f"Reference row {row['meta_data']['row_idx']} has multiple image assets")
        image = image_assets[0]
        gateway_url = image["image_src"]
        s3_uri = gateway_url_to_s3(gateway_url)
        _, key = parse_s3_uri(s3_uri)
        reference_id = row["meta_data"]["evalset_item_id"]
        local_path = asset_root / "references" / Path(key).name
        specs.append(
            {
                "id": f"printer-reference-{reference_id}",
                "source_report": REFERENCE_REPORT,
                "row": int(row["meta_data"]["row_idx"]),
                "reference_index": len(specs) + 1,
                "case_id": reference_id,
                "device": "Printer",
                "variant": "reference",
                "type": "reference",
                "original_prompt": None,
                "s3_url": s3_uri,
                "source_gateway_url": gateway_url,
                "local_path": os.fspath(local_path.resolve()),
                "expected_sha256": None,
                "declared_width": image.get("width"),
                "declared_height": image.get("height"),
            }
        )
    if len(specs) != 15:
        raise ValueError(f"Expected 15 printer reference images, found {len(specs)}")
    return specs


def render_panel(asset: dict[str, Any], label: str) -> Image.Image:
    panel = Image.new("RGB", (PANEL_WIDTH, PANEL_IMAGE_HEIGHT + PANEL_LABEL_HEIGHT), "white")
    with Image.open(asset["local_path"]) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        contained = ImageOps.contain(
            image,
            (PANEL_WIDTH, PANEL_IMAGE_HEIGHT),
            method=Image.Resampling.LANCZOS,
        )
    x = (PANEL_WIDTH - contained.width) // 2
    y = (PANEL_IMAGE_HEIGHT - contained.height) // 2
    panel.paste(contained, (x, y))
    draw = ImageDraw.Draw(panel)
    draw.rectangle((0, PANEL_IMAGE_HEIGHT, PANEL_WIDTH, panel.height), fill="#f2f2f2")
    draw.text((12, PANEL_IMAGE_HEIGHT + 11), label, fill="black", font=ImageFont.load_default())
    return panel


def save_grid(panels: list[Image.Image], columns: int, path: Path) -> None:
    rows = (len(panels) + columns - 1) // columns
    height = PANEL_IMAGE_HEIGHT + PANEL_LABEL_HEIGHT
    sheet = Image.new("RGB", (columns * PANEL_WIDTH, rows * height), "#d0d0d0")
    for index, panel in enumerate(panels):
        sheet.paste(panel, ((index % columns) * PANEL_WIDTH, (index // columns) * height))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, format="PNG", optimize=True)


def build_contact_sheets(assets: list[dict[str, Any]], asset_root: Path) -> list[str]:
    sheet_dir = asset_root / "contact_sheets"
    by_row_variant = {
        (asset["row"], asset["variant"]): asset
        for asset in assets
        if asset["source_report"] == COMPARISON_REPORT
    }
    baseline_panels: list[Image.Image] = []
    for row in BASELINE_SHEET_ROWS:
        row_assets = [by_row_variant[(row, variant)] for variant in ("product_input", "v13", "v14")]
        if not 2 <= len(row_assets) <= 3:
            raise ValueError(f"Baseline contact-sheet row {row} must have 2 or 3 images")
        for asset in row_assets:
            baseline_panels.append(render_panel(asset, f"Row {row:02d} · {asset['variant']}"))
    baseline_path = sheet_dir / "baseline_rows_01_02_05_11_25.png"
    save_grid(baseline_panels, 3, baseline_path)

    reference_assets = sorted(
        (asset for asset in assets if asset["source_report"] == REFERENCE_REPORT),
        key=lambda asset: asset["reference_index"],
    )
    paths = [os.fspath(baseline_path.resolve())]
    for start in range(0, len(reference_assets), 5):
        group = reference_assets[start : start + 5]
        panels = [render_panel(asset, asset["case_id"]) for asset in group]
        end = start + len(group)
        path = sheet_dir / f"printer_references_{start + 1:02d}_{end:02d}.png"
        save_grid(panels, 3, path)
        paths.append(os.fspath(path.resolve()))
    return paths


def duplicate_inputs(assets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for asset in assets:
        if asset["source_report"] == COMPARISON_REPORT and asset["type"] == "product_input":
            grouped[asset["sha256"]].append(asset)
    duplicates = []
    for digest, group in sorted(grouped.items()):
        if len(group) > 1:
            duplicates.append(
                {
                    "sha256": digest,
                    "rows": sorted(asset["row"] for asset in group),
                    "case_ids": sorted(asset["case_id"] for asset in group),
                    "local_paths": sorted(asset["local_path"] for asset in group),
                    "s3_urls": sorted(asset["s3_url"] for asset in group),
                }
            )
    return duplicates


def main() -> None:
    args = parse_args()
    required_aws_variables = ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN")
    missing_aws_variables = [name for name in required_aws_variables if not os.environ.get(name)]
    if missing_aws_variables:
        raise SystemExit(
            "Missing temporary AWS environment credentials. Source "
            "/home/colligo/.claude/hshariati/aws_creds.env in this shell before running."
        )
    asset_root = args.asset_root.expanduser().resolve()
    manifest_path = args.manifest.expanduser().resolve()
    comparison_data = load_json(args.comparison_data)
    comparison_provenance = load_json(args.comparison_provenance)
    reference_data = load_json(args.reference_data)
    source_manifest = load_json(args.source_manifest)
    comparison_prefix = report_s3_prefix(source_manifest, COMPARISON_REPORT)

    specs, unavailable = comparison_specs(
        comparison_data,
        comparison_provenance,
        comparison_prefix,
        asset_root,
    )
    specs.extend(reference_specs(reference_data, asset_root))

    client = boto3.client(
        "s3",
        region_name="us-west-2",
        config=Config(retries={"max_attempts": 8, "mode": "standard"}),
    )
    assets: list[dict[str, Any]] = []
    downloaded = 0
    for spec in specs:
        local_path = Path(spec["local_path"])
        digest, did_download = download_asset(
            client,
            spec["s3_url"],
            local_path,
            spec["expected_sha256"],
            args.refresh,
        )
        downloaded += int(did_download)
        width, height = image_metadata(local_path)
        if spec["declared_width"] is not None and width != spec["declared_width"]:
            raise ValueError(f"Width mismatch for {local_path}: declared {spec['declared_width']}, got {width}")
        if spec["declared_height"] is not None and height != spec["declared_height"]:
            raise ValueError(f"Height mismatch for {local_path}: declared {spec['declared_height']}, got {height}")
        asset = {key: value for key, value in spec.items() if key not in {"expected_sha256", "declared_width", "declared_height"}}
        asset.update(
            {
                "sha256": digest,
                "width": width,
                "height": height,
                "bytes": local_path.stat().st_size,
            }
        )
        assets.append(asset)

    duplicates = duplicate_inputs(assets)
    contact_sheets = [] if args.skip_contact_sheets else build_contact_sheets(assets, asset_root)
    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "asset_root": os.fspath(asset_root),
        "comparison_report": {
            "report_id": COMPARISON_REPORT,
            "data_file": os.fspath(args.comparison_data.resolve()),
            "s3_prefix": comparison_prefix,
        },
        "reference_report": {
            "report_id": REFERENCE_REPORT,
            "data_file": os.fspath(args.reference_data.resolve()),
        },
        "counts": {
            "assets": len(assets),
            "product_inputs": sum(asset["type"] == "product_input" for asset in assets),
            "generated_finals": sum(asset["type"] == "generated_final" for asset in assets),
            "printer_references": sum(asset["type"] == "reference" for asset in assets),
            "unavailable": len(unavailable),
        },
        "assets": assets,
        "unavailable": unavailable,
        "duplicate_product_inputs": duplicates,
        "contact_sheets": contact_sheets,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_manifest = manifest_path.with_name(f".{manifest_path.name}.part")
    with temporary_manifest.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    temporary_manifest.replace(manifest_path)

    print(
        f"assets={len(assets)} downloaded={downloaded} reused={len(assets) - downloaded} "
        f"unavailable={len(unavailable)}"
    )
    if duplicates:
        compact = "; ".join(
            f"{item['sha256'][:12]}:rows={','.join(map(str, item['rows']))}" for item in duplicates
        )
        print(f"duplicate_product_input_hashes={compact}")
    else:
        print("duplicate_product_input_hashes=none")


if __name__ == "__main__":
    main()
