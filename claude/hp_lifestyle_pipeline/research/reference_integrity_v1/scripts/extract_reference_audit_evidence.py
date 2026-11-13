#!/usr/bin/env python3
"""Create a compact, credential-free reference-integrity audit from run artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


FLAGGED = (
    "ee810cf51bb82bb4:p1:baseline-0016",
    "ee810cf51bb82bb4:p1:baseline-0018",
    "160db92655412f4d:p1:baseline-0016",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_eval(path: Path) -> dict[str, Any]:
    match = re.fullmatch(r"\s*const EVAL_DATA\s*=\s*(.*);\s*", path.read_text(), re.S)
    if not match:
        raise ValueError(f"Could not parse {path}")
    return json.loads(match.group(1))


def safe_row_id(row_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "__", row_id)


def image_label_map(fe_row: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {asset["meta_text"]["label"]: asset for asset in fe_row["images"]}


def file_record(path: Path) -> dict[str, Any]:
    md5 = hashlib.md5()  # S3 ETags for these sub-8 MiB single-part uploads.
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            md5.update(chunk)
    return {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "md5": md5.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-data", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--published-fe-data", type=Path, required=True)
    parser.add_argument("--s3-listing", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    eval_data = load_eval(args.eval_data)
    rows = {row["row_id"]: row for row in eval_data["rows"]}
    twins = {twin["evalset_item_id"]: twin for twin in eval_data["twins"]}
    prompts = {prompt["key"]: prompt for prompt in eval_data["prompts"]}
    result_payload = json.loads(args.results.read_text())
    records = {record["row_id"]: record for record in result_payload["records"]}
    fe_payload = json.loads(args.published_fe_data.read_text())
    fe_rows = {row["meta_data"]["evalset_item_id"]: row for row in fe_payload["rows"]}
    listing = json.loads(args.s3_listing.read_text())
    listed = {item["Key"]: item for item in listing["Contents"]}

    problems: list[str] = []
    if set(rows) != set(records):
        problems.append("eval row IDs and result row IDs differ")
    if set(rows) != set(fe_rows):
        problems.append("eval row IDs and published FE row IDs differ")

    by_twin: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "request_blob_ids": set(),
            "device_categories": set(),
            "debug_first_entity_labels": set(),
            "row_ids": [],
        }
    )
    twin_ids_by_blob: dict[str, set[str]] = defaultdict(set)
    for row_id, row in rows.items():
        record = records[row_id]
        if record.get("prompt_key") != row["prompt_key"]:
            problems.append(f"{row_id}: prompt_key differs")
        if record.get("twin_id") != row["twin_id"]:
            problems.append(f"{row_id}: twin_id differs")
        if record.get("request_payload", {}).get("prompt") != prompts[row["prompt_key"]]["text"]:
            problems.append(f"{row_id}: request prompt differs")
        refs = record.get("request_payload", {}).get("referenceBlobs") or []
        if len(refs) != 1 or not refs[0].get("id"):
            problems.append(f"{row_id}: expected exactly one reference blob ID")
            continue
        blob_id = refs[0]["id"]
        stage1 = (record.get("debugData") or {}).get("stage1Output") or {}
        entities = (stage1.get("prompt") or {}).get("entities") or []
        first_label = entities[0].get("label") if entities else None
        bucket = by_twin[row["twin_id"]]
        bucket["request_blob_ids"].add(blob_id)
        bucket["device_categories"].add(row["device_category"])
        bucket["debug_first_entity_labels"].add(first_label)
        bucket["row_ids"].append(row_id)
        twin_ids_by_blob[blob_id].add(row["twin_id"])

    multiple_blob_twins = sorted(
        twin_id for twin_id, value in by_twin.items() if len(value["request_blob_ids"]) != 1
    )
    reused_blob_ids = sorted(
        blob_id for blob_id, twin_ids in twin_ids_by_blob.items() if len(twin_ids) != 1
    )
    if multiple_blob_twins:
        problems.append(f"twins with multiple request blob IDs: {multiple_blob_twins}")
    if reused_blob_ids:
        problems.append(f"blob IDs used by multiple twins: {reused_blob_ids}")

    twin_audit = []
    for twin_id, value in sorted(by_twin.items()):
        twin = twins[twin_id]
        twin_audit.append(
            {
                "twin_id": twin_id,
                "displayed_filename": twin["local_filename"],
                "manifest_sha256": twin["sha256"],
                "request_blob_ids": sorted(value["request_blob_ids"]),
                "device_categories": sorted(value["device_categories"]),
                "debug_first_entity_labels": sorted(value["debug_first_entity_labels"], key=str),
                "row_ids": value["row_ids"],
            }
        )

    flagged_records = []
    for row_id in FLAGGED:
        row = rows[row_id]
        twin = twins[row["twin_id"]]
        record = records[row_id]
        fe_assets = image_label_map(fe_rows[row_id])
        image_filename = record["output_image_filename"]
        output_path = args.artifact_dir / image_filename
        twin_path = args.artifact_dir / row["twin_file"]
        s3_key = (
            "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/generated_v1/images/"
            + image_filename
        )
        output_object = listed.get(s3_key)
        twin_download = file_record(twin_path)
        if twin_download["sha256"] != twin["sha256"]:
            problems.append(f"{row_id}: downloaded displayed twin hash differs from manifest")
        output_download = file_record(output_path)
        if output_object and output_download["md5"] != output_object["ETag"].strip('"'):
            problems.append(f"{row_id}: downloaded output MD5 differs from S3 ETag")
        response = record.get("response") or {}
        flagged_records.append(
            {
                "row_id": row_id,
                "safe_row_id": safe_row_id(row_id),
                "displayed_twin": {
                    "twin_id": row["twin_id"],
                    "filename": row["twin_file"],
                    "manifest_sha256": twin["sha256"],
                    "downloaded_file": twin_download,
                    "published_url": fe_assets["digital_twin"]["image_src"],
                },
                "submitted_request": record["request_payload"],
                "job_id": record["job_id"],
                "completed_at_utc": record["completed_at_utc"],
                "output_image_id": record["output_image_id"],
                "saved_response_metadata": {
                    "modelVersion": response.get("modelVersion"),
                    "size": response.get("size"),
                    "outputs": response.get("outputs"),
                },
                "debugData": record["debugData"],
                "published_output": {
                    "filename": image_filename,
                    "url": fe_assets["generated_output"]["image_src"],
                    "downloaded_file": output_download,
                    "s3_listing_metadata": output_object,
                },
                "imported_from_smoke": record.get("imported_from_smoke", False),
            }
        )

    evidence = {
        "as_of": "2026-10-22",
        "sources": {
            "eval_data": file_record(args.eval_data),
            "results": file_record(args.results),
            "published_fe_data": file_record(args.published_fe_data),
            "s3_listing": file_record(args.s3_listing),
        },
        "counts": {
            "eval_rows": len(rows),
            "result_records": len(records),
            "published_fe_rows": len(fe_rows),
            "twins_used": len(by_twin),
            "distinct_request_blob_ids": len(twin_ids_by_blob),
            "join_or_mapping_problems": len(problems),
        },
        "problems": problems,
        "twin_audit": twin_audit,
        "flagged_records": flagged_records,
        "limits": {
            "actual_uploaded_bytes_hash_preserved": False,
            "server_blob_id_to_bytes_mapping_inspectable": False,
            "original_response_download_url_preserved": False,
            "explanation": (
                "The legacy upload cache stored blob ID and claimed filename, but no hash of the "
                "bytes actually posted. The server's internal blob-ID mapping is unavailable. "
                "The runner deliberately removed presigned response URLs before saving results. "
                "The published output bytes are preserved and hashed here, and the saved response "
                "retains output image IDs."
            ),
        },
    }
    serialized = json.dumps(evidence, ensure_ascii=False, indent=2) + "\n"
    forbidden = ("X-Amz-Signature", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN")
    if any(token in serialized for token in forbidden):
        raise ValueError("Credential-like material was about to be preserved")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(serialized)
    print(json.dumps({"output": str(args.output), "bytes": len(serialized)}, indent=2))


if __name__ == "__main__":
    main()
