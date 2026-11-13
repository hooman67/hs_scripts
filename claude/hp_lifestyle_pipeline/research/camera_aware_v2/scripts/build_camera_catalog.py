#!/usr/bin/env python3
"""Safely inventory HP camera assets and build an auditable camera catalog.

The large originals and extracted images stay below local_data/ (Git-ignored).
Compact JSON/CSV evidence is written below research/camera_aware_v2/data/.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import shutil
import stat
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import PIL
import pypdf
from PIL import Image, ImageChops
from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[3]
LOCAL_ROOT = PROJECT_ROOT / "local_data" / "HP_scenes"
ORIGINALS = LOCAL_ROOT / "originals"
EXTRACTED = LOCAL_ROOT / "extracted"
DATA = PROJECT_ROOT / "research" / "camera_aware" / "data"
VOLATILE_SOURCE = Path("/mnt/localssd/HP_scenes")
TYPE_CORRECTIONS_PATH = DATA / "device_type_corrections.json"

PDF_SPECS = (
    {
        "path": ORIGINALS / "asset_comparison_report.pdf",
        "source_id": "standalone_laptop_customer_approved",
        "declared_device_types": ("laptop",),
        "approval_status": "customer_approved_user_confirmed",
        "approval_scope": "laptop camera names shown on the report",
    },
    {
        "path": ORIGINALS / "asset_comparison_report (1).pdf",
        "source_id": "standalone_printer_development",
        "declared_device_types": ("printer",),
        "approval_status": "development_assumption_actual_customer_approval_pending",
        "approval_scope": "printer camera names shown on the report",
    },
    {
        "path": EXTRACTED / "Shared" / "asset_comparison_report_2026-10-22_17-37-34.pdf",
        "source_id": "shared_zip_embedded_report",
        "declared_device_types": ("laptop", "printer"),
        "approval_status": "context_only_no_approval_claim",
        "approval_scope": "bundle inventory and page-to-asset comparison only",
    },
)

UNKNOWN_TYPE_APPROVAL_STATUS = "no_approved_report_for_source_declared_device_type"


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_type_corrections() -> tuple[dict, dict[str, dict]]:
    document = json.loads(TYPE_CORRECTIONS_PATH.read_text(encoding="utf-8"))
    if document.get("schema_version") != 1 or document.get("status") != "active":
        raise RuntimeError("device-type correction registry must be active schema version 1")
    by_device_id: dict[str, dict] = {}
    for correction in document.get("corrections", []):
        identity = correction.get("exact_source_identity", {})
        device_id = identity.get("device_id")
        if not device_id or device_id in by_device_id:
            raise RuntimeError(f"invalid/duplicate exact correction identity: {device_id!r}")
        enriched = dict(correction)
        enriched["correction_registry_version"] = document["version"]
        by_device_id[device_id] = enriched
    return document, by_device_id


def corrected_device_type(
    identity: dict[str, str], source_declared_device_type: str, corrections: dict[str, dict]
) -> tuple[str, dict | None]:
    correction = corrections.get(identity["device_id"])
    if correction is None:
        return source_declared_device_type, None
    expected = correction["exact_source_identity"]
    if identity != expected:
        raise RuntimeError(
            f"device-type correction identity mismatch: parsed={identity!r}, expected={expected!r}"
        )
    if correction["source_declared_device_type"] != source_declared_device_type:
        raise RuntimeError(
            f"correction declared type mismatch for {identity['device_id']!r}"
        )
    provenance = {
        "correction_id": correction["correction_id"],
        "correction_registry_version": correction["correction_registry_version"],
        "provenance": correction["provenance"],
    }
    return correction["effective_device_type"], provenance


def zip_member_is_safe(info: zipfile.ZipInfo) -> tuple[bool, str | None]:
    member = PurePosixPath(info.filename)
    if member.is_absolute() or ".." in member.parts:
        return False, "absolute_or_parent_traversal_path"
    unix_mode = info.external_attr >> 16
    if unix_mode and stat.S_ISLNK(unix_mode):
        return False, "symbolic_link"
    if info.flag_bits & 0x1:
        return False, "encrypted_entry"
    return True, None


def inventory_and_extract_zip(zip_path: Path) -> tuple[dict, list[zipfile.ZipInfo]]:
    entries: list[dict] = []
    safe_infos: list[zipfile.ZipInfo] = []
    seen: set[str] = set()
    duplicate_names: list[str] = []
    unsafe: list[dict] = []
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            safe, reason = zip_member_is_safe(info)
            if info.filename in seen:
                duplicate_names.append(info.filename)
            seen.add(info.filename)
            if not safe:
                unsafe.append({"filename": info.filename, "reason": reason})
            else:
                safe_infos.append(info)
            ratio = None
            if info.compress_size:
                ratio = round(info.file_size / info.compress_size, 4)
            entries.append(
                {
                    "filename": info.filename,
                    "is_directory": info.is_dir(),
                    "uncompressed_bytes": info.file_size,
                    "compressed_bytes": info.compress_size,
                    "compression_ratio": ratio,
                    "crc32": f"{info.CRC:08x}",
                    "compression_method": info.compress_type,
                    "modified_zip_local_time": "%04d-%02d-%02dT%02d:%02d:%02d" % info.date_time,
                    "safe_to_extract": safe,
                    "rejection_reason": reason,
                }
            )
        test_failure = archive.testzip()
        if unsafe or duplicate_names or test_failure:
            raise RuntimeError(
                f"ZIP rejected: unsafe={unsafe}, duplicates={duplicate_names}, CRC failure={test_failure}"
            )
        for info in safe_infos:
            destination = EXTRACTED.joinpath(*PurePosixPath(info.filename).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if info.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
                continue
            with archive.open(info) as source, destination.open("wb") as target:
                shutil.copyfileobj(source, target, length=1024 * 1024)

    summary = {
        "source_zip_absolute_path": str(zip_path),
        "source_zip_sha256": sha256_path(zip_path),
        "entry_count": len(entries),
        "file_count": sum(not item["is_directory"] for item in entries),
        "total_uncompressed_bytes": sum(item["uncompressed_bytes"] for item in entries),
        "total_compressed_bytes": sum(item["compressed_bytes"] for item in entries),
        "max_entry_compression_ratio": max(
            (item["compression_ratio"] or 0 for item in entries), default=0
        ),
        "duplicate_names": duplicate_names,
        "unsafe_entries": unsafe,
        "full_crc_test": "passed" if test_failure is None else f"failed:{test_failure}",
        "extraction_root_absolute_path": str(EXTRACTED),
        "entries": entries,
    }
    return summary, safe_infos


DEVICE_TYPE_IDENTIFIER_PATTERN = r"[A-Za-z][A-Za-z0-9_]*"
FOLDER_RE = re.compile(
    rf"^camera_(?P<family>{DEVICE_TYPE_IDENTIFIER_PATTERN})\.locator_"
    rf"(?P<device>.+\.(?P=family))$"
)
PDF_DEVICE_LINE_RE = re.compile(
    rf"(?m)^\s*(?P<device_asset_name>[^\n]+\."
    rf"(?P<family>{DEVICE_TYPE_IDENTIFIER_PATTERN})\.usdz)"
    rf"\s*(?:\[[^\]]+\])?\s*$"
)


def parse_asset_folder(folder: str) -> tuple[str, str] | None:
    """Return the literal declared type and device stem from a valid asset folder."""
    match = FOLDER_RE.fullmatch(folder)
    if match is None:
        return None
    return match.group("family"), match.group("device")


def pdf_page_approval(spec: dict, declared_device_type: str) -> tuple[str, str]:
    """Apply a report policy only to device types explicitly named by that policy."""
    if declared_device_type in spec["declared_device_types"]:
        return spec["approval_status"], spec["approval_scope"]
    return (
        UNKNOWN_TYPE_APPROVAL_STATUS,
        f"no approval policy for {declared_device_type!r} in report {spec['source_id']}",
    )


def parse_zip_assets(
    infos: list[zipfile.ZipInfo], corrections: dict[str, dict]
) -> tuple[list[dict], dict[str, dict]]:
    assets: list[dict] = []
    devices: dict[str, dict] = {}
    for info in infos:
        member = PurePosixPath(info.filename)
        if len(member.parts) < 3 or member.parts[0] != "Shared":
            continue
        folder = member.parts[1]
        parsed_folder = parse_asset_folder(folder)
        if parsed_folder is None:
            continue
        family, device_stem = parsed_folder
        device_asset_name = f"{device_stem}.usdz"
        device_id = folder
        identity = {
            "device_id": device_id,
            "device_asset_name_from_folder": device_asset_name,
            "zip_directory": f"Shared/{folder}/",
        }
        effective_type, correction_provenance = corrected_device_type(
            identity, family, corrections
        )
        devices.setdefault(
            device_id,
            {
                "device_id": device_id,
                "family": family,
                "source_declared_device_type": family,
                "effective_device_type": effective_type,
                "device_type_correction": correction_provenance,
                "device_type_correction_id": correction_provenance[
                    "correction_id"
                ]
                if correction_provenance
                else None,
                "device_type_correction_registry_version": correction_provenance[
                    "correction_registry_version"
                ]
                if correction_provenance
                else None,
                "device_asset_name_from_folder": device_asset_name,
                "zip_directory": f"Shared/{folder}/",
                "png_count": 0,
                "usdz_count": 0,
                "camera_names": [],
            },
        )
        extracted = EXTRACTED.joinpath(*member.parts)
        if member.suffix.lower() == ".usdz":
            devices[device_id]["usdz_count"] += 1
            devices[device_id]["usdz_zip_filename"] = info.filename
            devices[device_id]["usdz_sha256"] = sha256_path(extracted)
            continue
        if member.suffix.lower() != ".png":
            continue
        prefix = f"{folder}_"
        if not member.name.startswith(prefix):
            raise RuntimeError(f"PNG does not preserve its folder prefix: {info.filename}")
        camera_name = member.stem[len(prefix) :]
        with Image.open(extracted) as image:
            width, height = image.size
            image_format = image.format
        record = {
            "device_id": device_id,
            "device_family": family,
            "source_declared_device_type": family,
            "effective_device_type": effective_type,
            "device_type_correction": correction_provenance,
            "device_type_correction_id": correction_provenance["correction_id"]
            if correction_provenance
            else None,
            "device_type_correction_registry_version": correction_provenance[
                "correction_registry_version"
            ]
            if correction_provenance
            else None,
            "device_asset_name_from_folder": device_asset_name,
            "camera_name_exact": camera_name,
            "zip_filename": info.filename,
            "extracted_absolute_path": str(extracted),
            "width_px": width,
            "height_px": height,
            "image_format": image_format,
            "bytes": extracted.stat().st_size,
            "sha256": sha256_path(extracted),
            "zip_crc32": f"{info.CRC:08x}",
        }
        assets.append(record)
        devices[device_id]["png_count"] += 1
        devices[device_id]["camera_names"].append(camera_name)

    assets.sort(
        key=lambda item: (
            item["effective_device_type"],
            item["device_id"],
            item["camera_name_exact"],
        )
    )
    for device in devices.values():
        device["camera_names"] = sorted(device["camera_names"])
    return assets, devices


def page_device_name(text: str) -> tuple[str, str]:
    match = PDF_DEVICE_LINE_RE.search(text)
    if match is None:
        raise RuntimeError(f"Could not find page device name in extracted PDF text: {text[:300]!r}")
    return match.group("device_asset_name").strip(), match.group("family")


def extract_pdf_records(
    family_camera_names: dict[str, list[str]], devices: dict[str, dict], assets: list[dict]
) -> tuple[list[dict], dict[str, list[dict]]]:
    asset_by_device_camera = {
        (item["device_id"], item["camera_name_exact"]): item for item in assets
    }
    device_by_asset_name = {
        item["device_asset_name_from_folder"]: item for item in devices.values()
    }
    pdf_records: list[dict] = []
    provenance_by_family_camera: dict[str, list[dict]] = defaultdict(list)
    text_dir = DATA / "pdf_text"
    text_dir.mkdir(parents=True, exist_ok=True)

    for spec in PDF_SPECS:
        path = spec["path"]
        reader = PdfReader(str(path))
        page_records: list[dict] = []
        text_sections: list[str] = []
        for page_number, page in enumerate(reader.pages, 1):
            plain = page.extract_text() or ""
            layout = page.extract_text(extraction_mode="layout") or ""
            device_asset_name, family = page_device_name(plain)
            page_approval_status, page_approval_scope = pdf_page_approval(spec, family)
            # The Quartz report wraps several labels in narrow grid columns
            # (for example ``Front_Right_CloseU`` + ``pLow``). Every supplied
            # page otherwise uses the same alphabetical family list; the only
            # variant is whether the explicitly printed CAM_review tile exists.
            camera_names = sorted(family_camera_names[family])
            if "CAM_review" not in plain:
                camera_names.remove("CAM_review")
            if len(camera_names) != len(page.images):
                raise RuntimeError(
                    f"{path.name} page {page_number}: {len(camera_names)} names but "
                    f"{len(page.images)} images"
                )

            matched_device = device_by_asset_name.get(device_asset_name)
            effective_device_type = (
                matched_device["effective_device_type"] if matched_device else family
            )
            type_correction = (
                matched_device["device_type_correction"] if matched_device else None
            )
            image_records: list[dict] = []
            pixel_match_count = 0
            for index, (camera_name, pdf_image) in enumerate(zip(camera_names, page.images), 1):
                image = Image.open(io.BytesIO(pdf_image.data)).convert("RGBA")
                pdf_image_record = {
                    "image_index": index,
                    "pdf_object_name": pdf_image.name,
                    "camera_name_exact": camera_name,
                    "width_px": image.width,
                    "height_px": image.height,
                    "encoded_bytes": len(pdf_image.data),
                    "sha256": hashlib.sha256(pdf_image.data).hexdigest(),
                    "pixel_exact_with_matched_zip_asset": None,
                    "matched_zip_filename": None,
                }
                if matched_device:
                    zip_asset = asset_by_device_camera[(matched_device["device_id"], camera_name)]
                    with Image.open(zip_asset["extracted_absolute_path"]) as source_image:
                        source_rgba = source_image.convert("RGBA")
                    is_exact = (
                        image.size == source_rgba.size
                        and ImageChops.difference(image, source_rgba).getbbox() is None
                    )
                    pdf_image_record["pixel_exact_with_matched_zip_asset"] = is_exact
                    pdf_image_record["matched_zip_filename"] = zip_asset["zip_filename"]
                    pixel_match_count += int(is_exact)
                image_records.append(pdf_image_record)
                provenance_by_family_camera[f"{family}:{camera_name}"].append(
                    {
                        "source_id": spec["source_id"],
                        "pdf_absolute_path": str(path),
                        "pdf_page": page_number,
                        "page_device_asset_name": device_asset_name,
                        "source_declared_device_type": family,
                        "effective_device_type": effective_device_type,
                        "approval_status": page_approval_status,
                        "approval_scope": page_approval_scope,
                    }
                )

            page_record = {
                "page_number": page_number,
                "locator_asset_name": f"camera_{family}.locator.usdz",
                "device_family": family,
                "source_declared_device_type": family,
                "effective_device_type": effective_device_type,
                "approval_status": page_approval_status,
                "approval_scope": page_approval_scope,
                "device_type_correction": type_correction,
                "page_device_asset_name_exact": device_asset_name,
                "camera_names_exact": camera_names,
                "camera_count": len(camera_names),
                "page_image_count": len(page.images),
                "matched_zip_device_id": matched_device["device_id"] if matched_device else None,
                "page_images_pixel_exact_with_matched_zip_assets": pixel_match_count
                if matched_device
                else None,
                "plain_text_complete": plain,
                "layout_text_complete": layout,
                "images": image_records,
            }
            page_records.append(page_record)
            text_sections.append(
                f"===== PAGE {page_number}: {device_asset_name} [{family}] =====\n{layout.rstrip()}\n"
            )

        slug = re.sub(r"[^A-Za-z0-9._-]+", "_", path.name).strip("_")
        text_path = text_dir / f"{slug}.txt"
        text_path.write_text("\n\n".join(text_sections) + "\n", encoding="utf-8")
        pdf_records.append(
            {
                "source_id": spec["source_id"],
                "pdf_absolute_path": str(path),
                "pdf_sha256": sha256_path(path),
                "page_count": len(reader.pages),
                "approval_status": spec["approval_status"],
                "approval_scope": spec["approval_scope"],
                "complete_text_artifact_absolute_path": str(text_path),
                "metadata": {str(k): str(v) for k, v in (reader.metadata or {}).items()},
                "pages": page_records,
            }
        )
    return pdf_records, provenance_by_family_camera


def build_source_manifest() -> dict:
    originals = []
    for durable in sorted(ORIGINALS.iterdir(), key=lambda p: p.name):
        if not durable.is_file():
            continue
        volatile = VOLATILE_SOURCE / durable.name
        durable_hash = sha256_path(durable)
        source_hash = sha256_path(volatile) if volatile.exists() else None
        originals.append(
            {
                "filename": durable.name,
                "volatile_source_absolute_path": str(volatile),
                "durable_copy_absolute_path": str(durable),
                "bytes": durable.stat().st_size,
                "durable_copy_sha256": durable_hash,
                "volatile_source_sha256": source_hash,
                "copy_verified_sha256_equal": source_hash == durable_hash if source_hash else None,
            }
        )
    return {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "volatile_source_root": str(VOLATILE_SOURCE),
        "durable_copy_root": str(ORIGINALS),
        "file_count": len(originals),
        "all_available_sources_match_durable_copies": all(
            item["copy_verified_sha256_equal"] is not False for item in originals
        ),
        "files": originals,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    DATA.mkdir(parents=True, exist_ok=True)

    correction_document, corrections_by_device = load_type_corrections()
    source_manifest = build_source_manifest()
    zip_inventory, infos = inventory_and_extract_zip(ORIGINALS / "Shared.zip")
    assets, devices = parse_zip_assets(infos, corrections_by_device)
    family_names: dict[str, list[str]] = defaultdict(list)
    for asset in assets:
        family_names[asset["device_family"]].append(asset["camera_name_exact"])
    family_names = {
        family: sorted(set(names)) for family, names in family_names.items()
    }
    pdf_records, page_provenance = extract_pdf_records(family_names, devices, assets)

    standalone_by_family_name: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for report in pdf_records:
        if not report["source_id"].startswith("standalone_"):
            continue
        for page in report["pages"]:
            for camera_name in page["camera_names_exact"]:
                standalone_by_family_name[(page["device_family"], camera_name)].append(
                    {
                        "source_id": report["source_id"],
                        "pdf_absolute_path": report["pdf_absolute_path"],
                        "pdf_page": page["page_number"],
                        "page_device_asset_name": page["page_device_asset_name_exact"],
                        "approval_status": page["approval_status"],
                        "approval_scope": page["approval_scope"],
                    }
                )

    assets_by_effective_type_camera: dict[tuple[str, str], list[dict]] = defaultdict(list)
    effective_type_names: dict[str, set[str]] = defaultdict(set)
    for asset in assets:
        key = (asset["effective_device_type"], asset["camera_name_exact"])
        assets_by_effective_type_camera[key].append(asset)
        effective_type_names[asset["effective_device_type"]].add(asset["camera_name_exact"])

    definitions = []
    for effective_type in sorted(effective_type_names):
        for camera_name in sorted(effective_type_names[effective_type]):
            associated = assets_by_effective_type_camera[(effective_type, camera_name)]
            declared_types = sorted(
                {item["source_declared_device_type"] for item in associated}
            )
            report_family = effective_type if effective_type in {"laptop", "printer"} else None
            standalone = (
                standalone_by_family_name[(report_family, camera_name)]
                if report_family
                else []
            )
            if effective_type == "laptop" and standalone:
                status = "customer_approved_user_confirmed"
            elif effective_type == "laptop":
                status = "not_listed_in_customer_approved_standalone_laptop_report"
            elif effective_type == "printer":
                status = "development_assumption_actual_customer_approval_pending"
            else:
                status = "source_asset_only_no_customer_camera_approval"
            definitions.append(
                {
                    "effective_device_type": effective_type,
                    "type_tag": f"{effective_type}_{camera_name}",
                    "source_declared_device_types": declared_types,
                    "camera_name_exact": camera_name,
                    "approval_status": status,
                    "standalone_report_provenance": standalone,
                    "all_page_provenance": page_provenance[
                        f"{report_family}:{camera_name}"
                    ]
                    if report_family
                    else [],
                    "associated_high_resolution_asset_count": len(associated),
                    "associated_zip_filenames": [
                        item["zip_filename"] for item in associated
                    ],
                }
            )

    pdf_device_names = {
        page["page_device_asset_name_exact"]
        for report in pdf_records
        for page in report["pages"]
    }
    zip_device_names = {
        item["device_asset_name_from_folder"] for item in devices.values()
    }

    # The only PDF-only and ZIP-only printer devices form a tempting name-based
    # substitution. Compare their page/asset pixels explicitly so the mismatch
    # remains evidence rather than an inferred association.
    tassel_page = next(
        page
        for report in pdf_records
        if report["source_id"] == "standalone_printer_development"
        for page in report["pages"]
        if page["page_device_asset_name_exact"]
        == "Tassel_ConnectivityFacet-Wireless.printer.usdz"
    )
    messi_device = next(
        item
        for item in devices.values()
        if item["device_asset_name_from_folder"] == "Messi_Ceramic-White.printer.usdz"
    )
    messi_pixel_matches = 0
    printer_development_reader = PdfReader(
        str(ORIGINALS / "asset_comparison_report (1).pdf")
    )
    for image_record in tassel_page["images"]:
        candidate = next(
            item
            for item in assets
            if item["device_id"] == messi_device["device_id"]
            and item["camera_name_exact"] == image_record["camera_name_exact"]
        )
        pdf_image = printer_development_reader.pages[1].images[
            image_record["image_index"] - 1
        ]
        left = Image.open(io.BytesIO(pdf_image.data)).convert("RGBA")
        with Image.open(candidate["extracted_absolute_path"]) as right_source:
            right = right_source.convert("RGBA")
        messi_pixel_matches += int(
            left.size == right.size and ImageChops.difference(left, right).getbbox() is None
        )

    unmatched = {
        "pdf_devices_without_exact_zip_directory": sorted(pdf_device_names - zip_device_names),
        "zip_devices_without_exact_pdf_page": sorted(zip_device_names - pdf_device_names),
        "camera_name_gaps": [
            {
                "source_declared_device_type": "laptop",
                "effective_device_type": "laptop",
                "camera_name_exact": "CAM_review",
                "issue": "present for the Viktor ZIP device and ZIP-embedded report page, absent from the customer-approved standalone laptop PDF",
            }
        ],
        "bundle_internal_device_name_mismatch": {
            "pdf_name": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
            "pdf_effective_device_type": "printer",
            "zip_directory_device_name": "Messi_Ceramic-White.printer.usdz",
            "zip_source_declared_device_type": messi_device[
                "source_declared_device_type"
            ],
            "zip_effective_device_type": messi_device["effective_device_type"],
            "same_camera_name_count": 41,
            "pixel_exact_image_pairs": messi_pixel_matches,
            "conclusion": "unmatched and cross-type; do not alias printer Tassel to miniPC Messi",
        },
        "approval_gaps": [
            "Printer camera names are development assumptions; actual customer approval is pending.",
            "The Messi device-type correction is USER-CONFIRMED, but its miniPC camera names have no exact standalone customer-approval report.",
        ],
    }

    device_records = sorted(devices.values(), key=lambda item: item["device_id"])
    for device in device_records:
        device["exact_pdf_page_matches"] = [
            {
                "source_id": report["source_id"],
                "pdf_absolute_path": report["pdf_absolute_path"],
                "pdf_page": page["page_number"],
                "approval_status": page["approval_status"],
                "approval_scope": page["approval_scope"],
                "pixel_exact_image_pairs": page[
                    "page_images_pixel_exact_with_matched_zip_assets"
                ],
                "page_image_count": page["page_image_count"],
            }
            for report in pdf_records
            for page in report["pages"]
            if page["page_device_asset_name_exact"]
            == device["device_asset_name_from_folder"]
        ]

    catalog = {
        "schema_version": 2,
        "as_of": datetime.now(timezone.utc).isoformat(),
        "scope": "Camera-name and high-resolution asset inventory for supplied HP reports and Shared.zip, preserving source-declared device types separately from corrected effective device types.",
        "methodology": {
            "zip_extraction": "Central-directory entries were rejected if encrypted, duplicated, absolute, parent-traversing, or symlinks; the complete ZIP CRC test passed before catalog publication.",
            "pdf_camera_label_reconstruction": "Quartz split several labels across narrow columns. Exact names use the ZIP filename-suffix lexicon in the report's alphabetical grid order; CAM_review is included only when explicitly present in extracted page text. Every reconstructed page-name count must equal its embedded-image count.",
            "page_to_zip_association": "Device names require an exact report-to-ZIP device-name match. Embedded report pixels were compared with the corresponding high-resolution ZIP PNG after RGBA decoding.",
            "device_type_correction": "Source filenames and declared types are immutable evidence. Effective device types apply only through exact identities in device_type_corrections.json; no filename substring or visual inference is used.",
        },
        "tool_versions": {
            "python": sys.version.split()[0],
            "pypdf": pypdf.__version__,
            "pillow": PIL.__version__,
        },
        "confidence": {
            "source_inventory_and_checksums": "VERIFIED",
            "page_text_and_names": "VERIFIED",
            "laptop_approval": "USER-CONFIRMED",
            "printer_approval": "UNVERIFIED_PENDING_CUSTOMER_APPROVAL",
            "messi_effective_device_type": "USER-CONFIRMED_2026-10-22",
        },
        "device_type_fields": {
            "source_declared_device_type": "Literal type declared by the supplied folder/filename; preserved even when wrong.",
            "effective_device_type": "Corrected type for taxonomy, grouping, and downstream type tags.",
            "legacy_device_family_or_family": "Backward-compatible source-declared value; do not use for effective taxonomy.",
        },
        "device_type_corrections": {
            "registry_absolute_path": str(TYPE_CORRECTIONS_PATH),
            "registry_sha256": sha256_path(TYPE_CORRECTIONS_PATH),
            "registry_version": correction_document["version"],
            "applied_correction_count": sum(
                item["device_type_correction"] is not None for item in device_records
            ),
        },
        "counts": {
            "zip_device_directories": len(device_records),
            "zip_png_assets": len(assets),
            "laptop_camera_names": len(family_names["laptop"]),
            "printer_camera_names": len(family_names["printer"]),
            "source_declared_device_counts": dict(
                sorted(Counter(item["source_declared_device_type"] for item in device_records).items())
            ),
            "effective_device_counts": dict(
                sorted(Counter(item["effective_device_type"] for item in device_records).items())
            ),
            "camera_name_counts_by_effective_device_type": {
                key: len(value) for key, value in sorted(effective_type_names.items())
            },
            "pdf_reports": len(pdf_records),
            "pdf_pages": sum(item["page_count"] for item in pdf_records),
        },
        "camera_definitions": definitions,
        "devices": device_records,
        "high_resolution_assets": assets,
        "pdf_reports": pdf_records,
        "ambiguous_or_unmatched": unmatched,
    }

    json_dump(DATA / "source_manifest.json", source_manifest)
    json_dump(DATA / "zip_inventory.json", zip_inventory)
    json_dump(
        DATA / "pdf_extraction.json",
        {
            "methodology": catalog["methodology"]["pdf_camera_label_reconstruction"],
            "reports": pdf_records,
        },
    )
    json_dump(DATA / "camera_catalog.json", catalog)

    csv_path = DATA / "camera_assets.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
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
            "width_px",
            "height_px",
            "bytes",
            "sha256",
            "extracted_absolute_path",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(assets)

    print(
        json.dumps(
            {
                "originals": source_manifest["file_count"],
                "zip_entries": zip_inventory["entry_count"],
                "devices": len(device_records),
                "png_assets": len(assets),
                "pdf_pages": catalog["counts"]["pdf_pages"],
                "catalog": str(DATA / "camera_catalog.json"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
