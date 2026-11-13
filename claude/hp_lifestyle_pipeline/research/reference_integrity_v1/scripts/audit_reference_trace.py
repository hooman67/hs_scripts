#!/usr/bin/env python3
"""Audit HP eval row/twin/blob/request/output joins without calling generation.

The generated run can be supplied either as its full ``results.json`` or as the
published gallery ``data.js``.  Full results retain row fields and the complete
sanitized response; gallery data retains only the subset rendered by the UI.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


FLAGGED_SAFE_IDS = {
    "ee810cf51bb82bb4__p1__baseline-0016",
    "ee810cf51bb82bb4__p1__baseline-0018",
    "160db92655412f4d__p1__baseline-0016",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_data_js(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = re.fullmatch(r"\s*const EVAL_DATA\s*=\s*(.*);\s*", text, re.S)
    if not match:
        raise ValueError(f"Could not parse EVAL_DATA from {path}")
    value = json.loads(match.group(1))
    if not isinstance(value, dict):
        raise ValueError(f"EVAL_DATA is not an object in {path}")
    return value


def safe_row_id(row_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "__", row_id)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_records(path: Path) -> tuple[dict[str, dict[str, Any]], str]:
    if path.name == "data.js":
        generated = load_data_js(path).get("generation") or {}
        records = generated.get("results") or {}
        return records, "published_gallery_subset"

    payload = load_json(path)
    raw = payload.get("records", payload)
    if isinstance(raw, list):
        return {record["row_id"]: record for record in raw}, "full_results"
    if isinstance(raw, dict):
        return raw, "record_mapping"
    raise ValueError(f"Unsupported record shape in {path}")


def file_evidence(directory: Path | None, filename: str) -> dict[str, Any] | None:
    if directory is None or not filename:
        return None
    path = directory / filename
    if not path.is_file():
        return {"path": str(path), "exists": False}
    return {
        "path": str(path),
        "exists": True,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-data", type=Path, required=True)
    parser.add_argument("--records", type=Path, required=True)
    parser.add_argument("--blob-ids", type=Path)
    parser.add_argument("--twin-dir", type=Path)
    parser.add_argument("--images-dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    eval_data = load_data_js(args.eval_data)
    records, record_source_kind = load_records(args.records)
    blobs = load_json(args.blob_ids) if args.blob_ids else {}

    prompts = {prompt["key"]: prompt for prompt in eval_data["prompts"]}
    twins = {twin["evalset_item_id"]: twin for twin in eval_data["twins"]}
    rows = {row["row_id"]: row for row in eval_data["rows"]}

    traces: list[dict[str, Any]] = []
    request_blob_ids_by_twin: dict[str, set[str]] = defaultdict(set)
    twin_ids_by_request_blob: dict[str, set[str]] = defaultdict(set)
    issues: list[dict[str, str]] = []

    def issue(row_id: str, kind: str, detail: str) -> None:
        issues.append({"row_id": row_id, "kind": kind, "detail": detail})

    for row_id, row in rows.items():
        prompt = prompts.get(row["prompt_key"])
        twin = twins.get(row["twin_id"])
        record = records.get(row_id)
        safe_id = safe_row_id(row_id)
        trace: dict[str, Any] = {
            "row_id": row_id,
            "safe_row_id": safe_id,
            "flagged": safe_id in FLAGGED_SAFE_IDS,
            "prompt_key": row["prompt_key"],
            "twin_id": row["twin_id"],
            "displayed_twin_filename": row["twin_file"],
            "displayed_twin_sha256": twin.get("sha256") if twin else None,
            "displayed_twin_source_s3_uri": row.get("original_twin_s3_uri"),
            "record_present": record is not None,
        }

        if prompt is None:
            issue(row_id, "missing_prompt", row["prompt_key"])
        if twin is None:
            issue(row_id, "missing_twin", row["twin_id"])
        elif twin.get("local_filename") != row["twin_file"]:
            issue(
                row_id,
                "displayed_twin_filename_disagrees",
                f"row={row['twin_file']} twin={twin.get('local_filename')}",
            )

        trace["durable_twin_file"] = file_evidence(args.twin_dir, row["twin_file"])
        if record is None:
            issue(row_id, "missing_generation_record", "")
            traces.append(trace)
            continue

        payload = record.get("request_payload") or {}
        refs = payload.get("referenceBlobs") or []
        request_blob_id = refs[0].get("id") if len(refs) == 1 else None
        cached = blobs.get(row["twin_id"]) or {}
        debug = record.get("debugData") or {}
        output_filename = record.get("output_image_filename", "")

        trace.update(
            {
                "record_row_id": record.get("row_id"),
                "record_prompt_key": record.get("prompt_key"),
                "record_twin_id": record.get("twin_id"),
                "cached_blob_id": cached.get("id"),
                "cached_blob_local_filename": cached.get("local_filename"),
                "request_reference_blobs": refs,
                "request_prompt_matches_eval": bool(
                    prompt and payload.get("prompt") == prompt.get("text")
                ),
                "job_id": record.get("job_id"),
                "output_image_id": record.get("output_image_id"),
                "output_image_filename": output_filename,
                "output_seed": record.get("output_seed"),
                "completed_at_utc": record.get("completed_at_utc"),
                "debug": {
                    "rawPrompt": debug.get("rawPrompt"),
                    "usedPrompt": debug.get("usedPrompt"),
                    "stage1Output": debug.get("stage1Output"),
                    "task": debug.get("task"),
                    "isInstructEdit": debug.get("isInstructEdit"),
                    "skuPick": debug.get("skuPick"),
                },
                "downloaded_output_file": file_evidence(args.images_dir, output_filename),
            }
        )

        if record.get("row_id") not in (None, row_id):
            issue(row_id, "record_row_id_disagrees", str(record.get("row_id")))
        if record.get("prompt_key") not in (None, row["prompt_key"]):
            issue(row_id, "record_prompt_key_disagrees", str(record.get("prompt_key")))
        if record.get("twin_id") not in (None, row["twin_id"]):
            issue(row_id, "record_twin_id_disagrees", str(record.get("twin_id")))
        if len(refs) != 1 or not request_blob_id:
            issue(row_id, "request_reference_blob_count_or_id", json.dumps(refs, sort_keys=True))
        else:
            request_blob_ids_by_twin[row["twin_id"]].add(request_blob_id)
            twin_ids_by_request_blob[request_blob_id].add(row["twin_id"])
        if cached:
            if cached.get("id") != request_blob_id:
                issue(
                    row_id,
                    "cached_blob_id_disagrees",
                    f"cache={cached.get('id')} request={request_blob_id}",
                )
            if cached.get("local_filename") != row["twin_file"]:
                issue(
                    row_id,
                    "cached_blob_filename_disagrees",
                    f"cache={cached.get('local_filename')} row={row['twin_file']}",
                )
        if prompt and payload.get("prompt") != prompt.get("text"):
            issue(row_id, "request_prompt_disagrees", "")
        if output_filename and not output_filename.startswith(safe_id + "."):
            issue(row_id, "output_filename_disagrees", output_filename)
        if debug.get("rawPrompt") is not None and debug.get("rawPrompt") != payload.get("prompt"):
            issue(row_id, "debug_raw_prompt_disagrees", "")

        traces.append(trace)

    for twin_id, blob_ids in request_blob_ids_by_twin.items():
        if len(blob_ids) != 1:
            issue("*", "twin_maps_to_multiple_request_blob_ids", f"{twin_id}: {sorted(blob_ids)}")
    for blob_id, twin_ids in twin_ids_by_request_blob.items():
        if len(twin_ids) != 1:
            issue("*", "request_blob_id_maps_to_multiple_twins", f"{blob_id}: {sorted(twin_ids)}")

    record_only_ids = sorted(set(records) - set(rows))
    for row_id in record_only_ids:
        issue(row_id, "generation_record_has_no_eval_row", "")

    output_hashes: dict[str, list[str]] = defaultdict(list)
    for trace in traces:
        file_info = trace.get("downloaded_output_file") or {}
        if file_info.get("exists"):
            output_hashes[file_info["sha256"]].append(trace["row_id"])

    result = {
        "sources": {
            "eval_data": str(args.eval_data.resolve()),
            "records": str(args.records.resolve()),
            "record_source_kind": record_source_kind,
            "blob_ids": str(args.blob_ids.resolve()) if args.blob_ids else None,
            "twin_dir": str(args.twin_dir.resolve()) if args.twin_dir else None,
            "images_dir": str(args.images_dir.resolve()) if args.images_dir else None,
        },
        "counts": {
            "eval_rows": len(rows),
            "unique_eval_row_ids": len(set(rows)),
            "generation_records": len(records),
            "record_only_ids": len(record_only_ids),
            "twins": len(twins),
            "request_blob_ids": len(twin_ids_by_request_blob),
            "issues": len(issues),
            "output_files_hashed": sum(
                bool((trace.get("downloaded_output_file") or {}).get("exists"))
                for trace in traces
            ),
            "unique_output_hashes": len(output_hashes),
        },
        "request_blob_ids_by_twin": {
            key: sorted(value) for key, value in sorted(request_blob_ids_by_twin.items())
        },
        "output_hash_duplicates": {
            key: value for key, value in sorted(output_hashes.items()) if len(value) > 1
        },
        "issues": issues,
        "flagged_traces": [trace for trace in traces if trace["flagged"]],
        "traces": traces,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"], indent=2))


if __name__ == "__main__":
    main()
