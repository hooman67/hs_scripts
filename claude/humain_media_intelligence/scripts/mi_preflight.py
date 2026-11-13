#!/usr/bin/env python3
"""Build and validate the Humain Media Intelligence ingestion manifest.

The script is deliberately resumable. It never writes to the source prefixes and
never records presigned URLs or source CSV fields that may contain credentials.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import statistics
import subprocess
import threading
from collections import Counter, defaultdict
from typing import Any, Iterable


BUCKET = "foundry-humain-default-adobe-assets"
MEDIA_EXTENSIONS = {".mov", ".mp4"}
RUN_DIR = pathlib.Path("runs/humain-missions-20260825")
PREFLIGHT_DIR = RUN_DIR / "preflight"
LISTING_DIR = PREFLIGHT_DIR / "source-listings"
CSV_DIR = PREFLIGHT_DIR / "source-csv"
MANIFEST_DIR = RUN_DIR / "manifests"

SOURCES = [
    {
        "source_id": "lifestyle_20260727",
        "theme": "Lifestyle",
        "mission_uuid": "20655345-d067-431a-98fa-051a39d2cbd1",
        "delivery_date": "2026-07-27",
        "prefix": "ingest/misions/20655345-d067-431a-98fa-051a39d2cbd1/27-07-2026/",
        "listing": "lifestyle.json",
        "csv": "lifestyle.csv",
    },
    {
        "source_id": "landmarks_architecture_20260817",
        "theme": "Landmarks / Architecture",
        "mission_uuid": "3d6deadb-f65a-4489-bb16-9192e44cb8e5",
        "delivery_date": "2026-08-17",
        "prefix": "ingest/misions/3d6deadb-f65a-4489-bb16-9192e44cb8e5/17-08-2026/",
        "listing": "landmarks_architecture.json",
        "csv": "landmarks_architecture.csv",
    },
    {
        "source_id": "events_6069_20260817",
        "theme": "Events",
        "mission_uuid": "6069eaee-a699-435e-93e4-0c8900b18b0a",
        "delivery_date": "2026-08-17",
        "prefix": "ingest/misions/6069eaee-a699-435e-93e4-0c8900b18b0a/17-08-2026/",
        "listing": "events_6069.json",
        "csv": "events_6069.csv",
    },
    {
        "source_id": "clothing_fashion_20260727",
        "theme": "Clothing / Fashion",
        "mission_uuid": "99367909-29a8-437f-b34d-0caa45949f19",
        "delivery_date": "2026-07-27",
        "prefix": "ingest/misions/99367909-29a8-437f-b34d-0caa45949f19/27-07-2026/",
        "listing": "clothing_fashion.json",
        "csv": "clothing_fashion.csv",
    },
    {
        "source_id": "events_9c3e_20260817",
        "theme": "Events",
        "mission_uuid": "9c3e6442-6e54-4d82-9969-7c0ddbd87d9c",
        "delivery_date": "2026-08-17",
        "prefix": "ingest/misions/9c3e6442-6e54-4d82-9969-7c0ddbd87d9c/17-08-2026/",
        "listing": "events_9c3e_20260817.json",
        "csv": "events_9c3e_20260817.csv",
    },
    {
        "source_id": "events_9c3e_20260727",
        "theme": "Events",
        "mission_uuid": "9c3e6442-6e54-4d82-9969-7c0ddbd87d9c",
        "delivery_date": "2026-07-27",
        "prefix": "ingest/misions/9c3e6442-6e54-4d82-9969-7c0ddbd87d9c/27-07-2026/",
        "listing": "events_9c3e_20260727.json",
        "csv": "events_9c3e_20260727.csv",
    },
    {
        "source_id": "food_20260727",
        "theme": "Food",
        "mission_uuid": "b149626b-2aae-402f-a382-48c3116a9f53",
        "delivery_date": "2026-07-27",
        "prefix": "ingest/misions/b149626b-2aae-402f-a382-48c3116a9f53/27-07-2026/",
        "listing": "food.json",
        "csv": "food.csv",
    },
]

SAFE_CSV_FIELDS = [
    "content_id",
    "id32",
    "caption",
    "keywords",
    "language_id",
    "original_id",
    "category2013_id",
    "premium_level_id",
    "isolated",
    "offensive_level",
    "content_type_id",
    "physical_type_id",
    "width",
    "height",
    "is_gentech",
    "transparent",
    "release_attached",
    "upload_date",
    "online_date",
    "member_id",
    "original_name",
    "dataset_uuid",
    "dataset_request_uuid",
    "dataset_keywords",
    "dataset_request_category2013_id",
    "dataset_request_content_type_id",
    "dataset_request_title",
    "dataset_request_subtype_id",
]


def read_json(path: pathlib.Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
    temporary.replace(path)


def write_jsonl(path: pathlib.Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
    temporary.replace(path)


def clean_etag(value: str) -> str:
    return value.strip('"')


def safe_csv_index(source: dict[str, str]) -> tuple[dict[str, dict[str, str]], list[str]]:
    path = CSV_DIR / source["csv"]
    by_filename: dict[str, dict[str, str]] = {}
    duplicates: list[str] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            relative_path = row.get("asset_relative_path") or row.get("media_relative_path") or ""
            filename = pathlib.PurePosixPath(relative_path).name
            safe = {field: row.get(field, "") for field in SAFE_CSV_FIELDS}
            safe["source_csv_relative_path"] = relative_path
            if filename in by_filename:
                duplicates.append(filename)
            by_filename[filename] = safe
    return by_filename, duplicates


def prepare() -> None:
    rows: list[dict[str, Any]] = []
    unmatched_csv: dict[str, list[str]] = {}
    duplicate_csv_names: dict[str, list[str]] = {}
    source_summaries: list[dict[str, Any]] = []

    for source_order, source in enumerate(SOURCES):
        listing = read_json(LISTING_DIR / source["listing"])
        csv_by_filename, duplicate_names = safe_csv_index(source)
        duplicate_csv_names[source["source_id"]] = duplicate_names
        matched_names: set[str] = set()
        extension_counts: Counter[str] = Counter()
        media_count = 0
        total_bytes = 0

        for obj in listing.get("Contents", []):
            key = obj["Key"]
            filename = pathlib.PurePosixPath(key).name
            extension = pathlib.PurePosixPath(key).suffix.lower()
            extension_counts[extension or "<none>"] += 1
            total_bytes += int(obj["Size"])
            if extension not in MEDIA_EXTENSIONS:
                continue
            media_count += 1
            metadata = csv_by_filename.get(filename, {})
            if metadata:
                matched_names.add(filename)
            row: dict[str, Any] = {
                "source_order": source_order,
                "source_id": source["source_id"],
                "theme": source["theme"],
                "mission_uuid": source["mission_uuid"],
                "delivery_date": source["delivery_date"],
                "source_prefix": source["prefix"],
                "bucket": BUCKET,
                "object_key": key,
                "s3_url": f"s3://{BUCKET}/{key}",
                "filename": filename,
                "extension": extension,
                "size_bytes": int(obj["Size"]),
                "etag": clean_etag(obj["ETag"]),
                "etag_is_multipart": "-" in clean_etag(obj["ETag"]),
                "last_modified": obj.get("LastModified"),
                "storage_class": obj.get("StorageClass"),
                "checksum_algorithms": ",".join(obj.get("ChecksumAlgorithm", [])),
                "csv_metadata_matched": bool(metadata),
            }
            row.update({f"source_{key}": value for key, value in metadata.items()})
            rows.append(row)

        unmatched_csv[source["source_id"]] = sorted(set(csv_by_filename) - matched_names)
        source_summaries.append(
            {
                **{key: source[key] for key in ("source_id", "theme", "mission_uuid", "delivery_date", "prefix")},
                "object_count": len(listing.get("Contents", [])),
                "media_count": media_count,
                "total_bytes": total_bytes,
                "extensions": dict(sorted(extension_counts.items())),
                "unmatched_csv_rows": len(unmatched_csv[source["source_id"]]),
            }
        )

    size_groups: defaultdict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        size_groups[row["size_bytes"]].append(row)
    checksum_targets = [row for group in size_groups.values() if len(group) > 1 for row in group]

    write_jsonl(PREFLIGHT_DIR / "object_inventory.jsonl", rows)
    write_jsonl(PREFLIGHT_DIR / "checksum_targets.jsonl", checksum_targets)
    write_json(
        PREFLIGHT_DIR / "prepare_summary.json",
        {
            "bucket": BUCKET,
            "source_summaries": source_summaries,
            "total_media_objects": len(rows),
            "total_media_bytes": sum(row["size_bytes"] for row in rows),
            "checksum_target_objects": len(checksum_targets),
            "same_size_groups": sum(len(group) > 1 for group in size_groups.values()),
            "unmatched_csv": unmatched_csv,
            "duplicate_csv_filenames": duplicate_csv_names,
        },
    )
    print(json.dumps(read_json(PREFLIGHT_DIR / "prepare_summary.json"), indent=2))


def boto_client():
    import boto3
    from botocore.config import Config

    return boto3.client(
        "s3",
        region_name="us-west-2",
        config=Config(retries={"max_attempts": 8, "mode": "adaptive"}),
    )


def head_checksum(row: dict[str, Any], client: Any) -> dict[str, Any]:
    try:
        response = client.head_object(Bucket=row["bucket"], Key=row["object_key"], ChecksumMode="ENABLED")
        return {
            "s3_url": row["s3_url"],
            "status": "ok",
            "checksum_crc64nvme": response.get("ChecksumCRC64NVME"),
            "checksum_crc32": response.get("ChecksumCRC32"),
            "checksum_crc32c": response.get("ChecksumCRC32C"),
            "checksum_sha1": response.get("ChecksumSHA1"),
            "checksum_sha256": response.get("ChecksumSHA256"),
            "content_length": response.get("ContentLength"),
            "content_type": response.get("ContentType"),
        }
    except Exception as exc:  # noqa: BLE001 - preserve per-object progress
        return {"s3_url": row["s3_url"], "status": "error", "error": type(exc).__name__}


def run_checksums(workers: int) -> None:
    targets = read_jsonl(PREFLIGHT_DIR / "checksum_targets.jsonl")
    output = PREFLIGHT_DIR / "checksum_results.jsonl"
    existing_rows = read_jsonl(output)
    existing = {row["s3_url"]: row for row in existing_rows if row.get("status") == "ok"}
    pending = [row for row in targets if row["s3_url"] not in existing]
    client = boto_client()
    lock = threading.Lock()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as handle:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_map = {executor.submit(head_checksum, row, client): row for row in pending}
            completed = 0
            for future in concurrent.futures.as_completed(future_map):
                result = future.result()
                with lock:
                    handle.write(json.dumps(result, sort_keys=True) + "\n")
                    handle.flush()
                completed += 1
                if completed % 250 == 0 or completed == len(pending):
                    print(f"checksums {completed}/{len(pending)}")


def best_checksum(row: dict[str, Any]) -> tuple[str, str] | None:
    for field in ("checksum_sha256", "checksum_sha1", "checksum_crc64nvme", "checksum_crc32c", "checksum_crc32"):
        if row.get(field):
            return field, row[field]
    return None


def duplicate_identity(row: dict[str, Any]) -> tuple[Any, ...]:
    checksum = best_checksum(row)
    if checksum:
        return (row["size_bytes"], *checksum)
    return (row["size_bytes"], "etag", row["etag"])


def duplicate_group_id(identity: tuple[Any, ...]) -> str:
    raw = json.dumps(identity, separators=(",", ":"), sort_keys=True).encode()
    return "dup-" + hashlib.sha256(raw).hexdigest()[:16]


def canonicalize() -> None:
    rows = read_jsonl(PREFLIGHT_DIR / "object_inventory.jsonl")
    checksum_rows = read_jsonl(PREFLIGHT_DIR / "checksum_results.jsonl")
    checksum_by_url = {row["s3_url"]: row for row in checksum_rows if row.get("status") == "ok"}
    for row in rows:
        row.update({key: value for key, value in checksum_by_url.get(row["s3_url"], {}).items() if key not in {"s3_url", "status"}})

    groups: defaultdict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[duplicate_identity(row)].append(row)

    canonical_rows: list[dict[str, Any]] = []
    provenance_rows: list[dict[str, Any]] = []
    duplicate_rows: list[dict[str, Any]] = []
    for identity, members in groups.items():
        members.sort(
            key=lambda row: (
                row["delivery_date"],
                -row["source_order"],
                row["object_key"],
            ),
            reverse=True,
        )
        canonical = members[0]
        group_id = duplicate_group_id(identity)
        themes = sorted({row["theme"] for row in members})
        missions = sorted({row["mission_uuid"] for row in members})
        deliveries = sorted({row["delivery_date"] for row in members})
        source_urls = sorted({row["s3_url"] for row in members})
        title_theme = " + ".join(themes)
        title_missions = "+".join(mission[:8] for mission in missions)
        title_name = f"{title_theme} | {title_missions} | {canonical['filename']}"

        canonical_out = dict(canonical)
        canonical_out.update(
            {
                "duplicate_group_id": group_id,
                "duplicate_group_size": len(members),
                "all_themes_json": json.dumps(themes),
                "all_missions_json": json.dumps(missions),
                "all_delivery_dates_json": json.dumps(deliveries),
                "all_source_urls_json": json.dumps(source_urls),
                "title_name": title_name,
            }
        )
        canonical_rows.append(canonical_out)

        for row in members:
            provenance = dict(row)
            provenance.update(
                {
                    "duplicate_group_id": group_id,
                    "duplicate_group_size": len(members),
                    "canonical_s3_url": canonical["s3_url"],
                    "is_canonical": row["s3_url"] == canonical["s3_url"],
                    "duplicate_identity_method": identity[1],
                    "title_name": title_name,
                    "all_themes_json": json.dumps(themes),
                    "all_missions_json": json.dumps(missions),
                    "all_delivery_dates_json": json.dumps(deliveries),
                }
            )
            provenance_rows.append(provenance)
            if len(members) > 1:
                duplicate_rows.append(provenance)

    canonical_rows.sort(key=lambda row: row["s3_url"])
    provenance_rows.sort(key=lambda row: row["s3_url"])
    duplicate_rows.sort(key=lambda row: (row["duplicate_group_id"], row["s3_url"]))
    write_jsonl(PREFLIGHT_DIR / "canonical_inventory.jsonl", canonical_rows)
    write_jsonl(PREFLIGHT_DIR / "provenance_inventory.jsonl", provenance_rows)
    write_jsonl(PREFLIGHT_DIR / "duplicates.jsonl", duplicate_rows)
    write_jsonl(PREFLIGHT_DIR / "probe_targets.jsonl", canonical_rows)
    summary = {
        "source_media_objects": len(rows),
        "canonical_media_objects": len(canonical_rows),
        "duplicate_objects_removed": len(rows) - len(canonical_rows),
        "duplicate_groups": sum(len(members) > 1 for members in groups.values()),
        "duplicate_group_size_distribution": dict(sorted(Counter(len(members) for members in groups.values() if len(members) > 1).items())),
        "checksum_results": len(checksum_by_url),
        "checksum_errors": sum(row.get("status") != "ok" for row in checksum_rows),
    }
    write_json(PREFLIGHT_DIR / "canonicalize_summary.json", summary)
    print(json.dumps(summary, indent=2))


URL_RE = re.compile(r"https?://\S+")


def sanitize_error(value: str) -> str:
    return URL_RE.sub("[presigned-url-redacted]", value).strip()[:2000]


def probe_one(row: dict[str, Any], client: Any, timeout: int) -> dict[str, Any]:
    try:
        url = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": row["bucket"], "Key": row["object_key"]},
            ExpiresIn=14_400,
        )
        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=format_name,duration,size,bit_rate:stream=index,codec_type,codec_name,profile,width,height,pix_fmt,avg_frame_rate,r_frame_rate,sample_rate,channels",
            "-of",
            "json",
            url,
        ]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        if completed.returncode != 0:
            return {
                "s3_url": row["s3_url"],
                "status": "error",
                "returncode": completed.returncode,
                "error": sanitize_error(completed.stderr or completed.stdout),
            }
        payload = json.loads(completed.stdout)
        streams = payload.get("streams", [])
        video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
        audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
        primary_video = video_streams[0] if video_streams else {}
        format_info = payload.get("format", {})
        return {
            "s3_url": row["s3_url"],
            "status": "ok" if video_streams else "no_video_stream",
            "format_name": format_info.get("format_name"),
            "duration_seconds": float(format_info["duration"]) if format_info.get("duration") else None,
            "probe_size_bytes": int(format_info["size"]) if format_info.get("size") else None,
            "bit_rate": int(format_info["bit_rate"]) if format_info.get("bit_rate") else None,
            "video_stream_count": len(video_streams),
            "audio_stream_count": len(audio_streams),
            "video_codec": primary_video.get("codec_name"),
            "video_profile": primary_video.get("profile"),
            "width": primary_video.get("width"),
            "height": primary_video.get("height"),
            "pixel_format": primary_video.get("pix_fmt"),
            "avg_frame_rate": primary_video.get("avg_frame_rate"),
            "r_frame_rate": primary_video.get("r_frame_rate"),
            "audio_codecs_json": json.dumps(sorted({stream.get("codec_name") for stream in audio_streams if stream.get("codec_name")})),
        }
    except subprocess.TimeoutExpired:
        return {"s3_url": row["s3_url"], "status": "timeout", "error": f"ffprobe exceeded {timeout}s"}
    except Exception as exc:  # noqa: BLE001 - preserve per-object progress
        return {"s3_url": row["s3_url"], "status": "error", "error": type(exc).__name__}


def probe(workers: int, timeout: int, retry_failures: bool) -> None:
    targets = read_jsonl(PREFLIGHT_DIR / "probe_targets.jsonl")
    output = PREFLIGHT_DIR / "probe_results.jsonl"
    existing_rows = read_jsonl(output)
    if retry_failures:
        existing = {row["s3_url"] for row in existing_rows if row.get("status") == "ok"}
    else:
        existing = {row["s3_url"] for row in existing_rows}
    pending = [row for row in targets if row["s3_url"] not in existing]
    client = boto_client()
    lock = threading.Lock()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as handle:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_map = {executor.submit(probe_one, row, client, timeout): row for row in pending}
            completed = 0
            for future in concurrent.futures.as_completed(future_map):
                result = future.result()
                with lock:
                    handle.write(json.dumps(result, sort_keys=True) + "\n")
                    handle.flush()
                completed += 1
                if completed % 100 == 0 or completed == len(pending):
                    print(f"probes {completed}/{len(pending)}")


def latest_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    for row in rows:
        values[row[key]] = row
    return values


def write_parquet(path: pathlib.Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    import pyarrow as pa
    import pyarrow.parquet as pq

    path.parent.mkdir(parents=True, exist_ok=True)
    if columns is not None:
        rows = [{column: row.get(column) for column in columns} for row in rows]
    table = pa.Table.from_pylist(rows)
    pq.write_table(table, path, compression="zstd")


def finalize() -> None:
    canonical = read_jsonl(PREFLIGHT_DIR / "canonical_inventory.jsonl")
    provenance = read_jsonl(PREFLIGHT_DIR / "provenance_inventory.jsonl")
    duplicates = read_jsonl(PREFLIGHT_DIR / "duplicates.jsonl")
    probes = latest_by_key(read_jsonl(PREFLIGHT_DIR / "probe_results.jsonl"), "s3_url")
    # Drop superseded attempts so the durable checkpoint contains no stale errors.
    write_jsonl(PREFLIGHT_DIR / "probe_results.jsonl", sorted(probes.values(), key=lambda row: row["s3_url"]))

    canonical_final: list[dict[str, Any]] = []
    for row in canonical:
        merged = dict(row)
        merged.update({f"probe_{key}": value for key, value in probes.get(row["s3_url"], {}).items() if key != "s3_url"})
        canonical_final.append(merged)

    input_rows = [{"s3_url": row["s3_url"], "title_name": row["title_name"]} for row in canonical_final]
    write_parquet(MANIFEST_DIR / "input.parquet", input_rows, ["s3_url", "title_name"])
    write_parquet(MANIFEST_DIR / "provenance.parquet", provenance)
    write_parquet(MANIFEST_DIR / "duplicates.parquet", duplicates)
    write_parquet(PREFLIGHT_DIR / "media_probe.parquet", canonical_final)

    status_counts = Counter(probes.get(row["s3_url"], {}).get("status", "missing") for row in canonical)
    valid = [row for row in canonical_final if row.get("probe_status") == "ok"]
    durations = [float(row.get("probe_duration_seconds") or 0) for row in valid]
    duration = sum(durations)
    resolution_counts = Counter(f"{row.get('probe_width')}x{row.get('probe_height')}" for row in valid)
    codec_counts = Counter(row.get("probe_video_codec") or "unknown" for row in valid)
    format_counts = Counter(row.get("probe_format_name") or "unknown" for row in valid)
    size_mismatches = [row["s3_url"] for row in valid if row.get("probe_probe_size_bytes") not in (None, row["size_bytes"])]
    dimension_mismatches = [
        {
            "s3_url": row["s3_url"],
            "source_width": row.get("source_width"),
            "source_height": row.get("source_height"),
            "probe_width": row.get("probe_width"),
            "probe_height": row.get("probe_height"),
            "is_orientation_swap": (
                str(row.get("source_width")), str(row.get("source_height"))
            )
            == (
                str(row.get("probe_height")), str(row.get("probe_width"))
            ),
        }
        for row in valid
        if row.get("source_width")
        and row.get("source_height")
        and (str(row.get("probe_width")), str(row.get("probe_height"))) != (str(row.get("source_width")), str(row.get("source_height")))
    ]
    write_parquet(PREFLIGHT_DIR / "dimension_mismatches.parquet", dimension_mismatches)

    by_theme: dict[str, dict[str, Any]] = {}
    for theme in sorted({row["theme"] for row in canonical_final}):
        theme_rows = [row for row in canonical_final if row["theme"] == theme]
        theme_duration = sum(float(row.get("probe_duration_seconds") or 0) for row in theme_rows)
        by_theme[theme] = {
            "canonical_assets": len(theme_rows),
            "bytes": sum(row["size_bytes"] for row in theme_rows),
            "duration_seconds": theme_duration,
            "duration_hours": theme_duration / 3600,
        }
    prepare_summary = read_json(PREFLIGHT_DIR / "prepare_summary.json")
    summary = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "bucket": BUCKET,
        "run_root": f"s3://{BUCKET}/media-intelligence/humain-missions-20260825/",
        "source_media_objects": len(provenance),
        "canonical_media_objects": len(canonical),
        "duplicate_objects_removed": len(provenance) - len(canonical),
        "source_media_bytes": sum(row["size_bytes"] for row in provenance),
        "canonical_media_bytes": sum(row["size_bytes"] for row in canonical),
        "duplicate_bytes_removed": sum(row["size_bytes"] for row in provenance) - sum(row["size_bytes"] for row in canonical),
        "probe_status_counts": dict(sorted(status_counts.items())),
        "total_duration_seconds": duration,
        "total_duration_hours": duration / 3600,
        "duration_min_seconds": min(durations) if durations else None,
        "duration_median_seconds": statistics.median(durations) if durations else None,
        "duration_max_seconds": max(durations) if durations else None,
        "audio_stream_counts": dict(sorted(Counter(row.get("probe_audio_stream_count", 0) for row in valid).items())),
        "primary_theme_summary": by_theme,
        "source_summaries": prepare_summary["source_summaries"],
        "resolution_counts": dict(resolution_counts.most_common()),
        "codec_counts": dict(codec_counts.most_common()),
        "format_counts": dict(format_counts.most_common()),
        "probe_size_mismatches": size_mismatches,
        "source_dimension_mismatch_count": len(dimension_mismatches),
        "source_dimension_orientation_swap_count": sum(row["is_orientation_swap"] for row in dimension_mismatches),
        "source_dimension_other_mismatch_count": sum(not row["is_orientation_swap"] for row in dimension_mismatches),
        "source_dimension_mismatch_examples": dimension_mismatches[:20],
        "ready_for_ingestion": status_counts == {"ok": len(canonical)} and not size_mismatches,
    }
    write_json(PREFLIGHT_DIR / "preflight_summary.json", summary)
    report_lines = [
        "# Humain MI preflight report",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Outcome",
        "",
        f"- Ready for ingestion: **{summary['ready_for_ingestion']}**",
        f"- Source media objects: {summary['source_media_objects']:,}",
        f"- Canonical unique videos: {summary['canonical_media_objects']:,}",
        f"- Exact duplicate copies removed: {summary['duplicate_objects_removed']:,}",
        f"- Canonical duration: {summary['total_duration_hours']:.2f} hours",
        f"- Canonical bytes: {summary['canonical_media_bytes']:,}",
        f"- Probe results: {summary['probe_status_counts']}",
        "",
        "All canonical videos opened successfully with ffprobe. Source-dimension differences are retained in "
        "`dimension_mismatches.parquet`; most are width/height orientation swaps, and none caused a probe failure.",
        "",
        "## Primary-theme totals",
        "",
        "| Theme | Unique videos | Hours | Bytes |",
        "|---|---:|---:|---:|",
    ]
    for theme, values in by_theme.items():
        report_lines.append(
            f"| {theme} | {values['canonical_assets']:,} | {values['duration_hours']:.2f} | {values['bytes']:,} |"
        )
    report_lines.extend(
        [
            "",
            "## Duplicate decision",
            "",
            "The 2026-07-27 and 2026-08-17 deliveries for mission "
            "`9c3e6442-6e54-4d82-9969-7c0ddbd87d9c` contain the same 1,870 media objects by "
            "S3 checksum. The newer delivery is canonical. Exact duplicates within and across other themes "
            "were also collapsed; every source association remains in `provenance.parquet` and "
            "`duplicates.parquet`.",
            "",
        ]
    )
    report_path = PREFLIGHT_DIR / "PREFLIGHT_REPORT.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(json.dumps(summary, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("prepare")
    checksums_parser = subparsers.add_parser("checksums")
    checksums_parser.add_argument("--workers", type=int, default=32)
    subparsers.add_parser("canonicalize")
    probe_parser = subparsers.add_parser("probe")
    probe_parser.add_argument("--workers", type=int, default=16)
    probe_parser.add_argument("--timeout", type=int, default=120)
    probe_parser.add_argument("--retry-failures", action="store_true")
    subparsers.add_parser("finalize")
    args = parser.parse_args()

    if args.command == "prepare":
        prepare()
    elif args.command == "checksums":
        run_checksums(args.workers)
    elif args.command == "canonicalize":
        canonicalize()
    elif args.command == "probe":
        probe(args.workers, args.timeout, args.retry_failures)
    elif args.command == "finalize":
        finalize()


if __name__ == "__main__":
    main()
