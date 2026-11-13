#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "pillow"]
# ///
"""Resumable generation runner for the two frozen V5 top-five selections.

This runner owns V5 input validation and provenance while reusing the frozen,
tested V4.1 submit/poll/materialize engine. It never uploads a new reference:
the four exact blob IDs and original PNG hashes are inherited from the corrected
V4.1 run and verified before every launch.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import httpx


GENERATION_DIR = Path(__file__).resolve().parent
EVAL_ROOT = GENERATION_DIR.parent
PROJECT_ROOT = EVAL_ROOT.parents[1]
MANIFEST_PATH = GENERATION_DIR / "image_generation_manifest.json"
DEFAULT_RUN_DIR = (
    PROJECT_ROOT
    / "local_data/generation_runs/hp_lifestyle_dual_source_v5_pilot_20261027_top5_dual"
)
EXPECTED_ROWS = 80
EXPECTED_SELECTIONS = {"smart_brief", "ctech"}
EXPECTED_SELECTION_ROWS = 40
EXPECTED_BANKS = 8
EXPECTED_PER_BANK_PER_SELECTION = 5
EXPECTED_RENDER_COUNT = 4
EXPECTED_OUTPUT_SIZE = (2368, 1776)
MAX_WORKERS = 8
ROW_IDENTITY_FIELDS = (
    "row_id",
    "selection_type",
    "selection_rank_in_bank",
    "case_id",
    "group_id",
    "candidate_key",
    "pair_id",
    "render_id",
    "candidate_id",
    "device_type",
    "camera_tag",
)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    )


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_pinned_file(specification: dict[str, Any], label: str) -> Path:
    path = Path(specification.get("path", "")).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"{label} is missing: {path}")
    actual = sha256_path(path)
    if actual != specification.get("sha256"):
        raise ValueError(f"{label} SHA-256 differs: {actual} != {specification.get('sha256')}")
    return path


def load_base_runner(manifest: dict[str, Any]):
    specification = manifest["runner_dependency"]
    path = require_pinned_file(specification, "frozen V4.1 runner dependency")
    module_spec = importlib.util.spec_from_file_location("hp_v41_frozen_generation_engine", path)
    if not module_spec or not module_spec.loader:
        raise RuntimeError(f"Cannot load frozen generation engine: {path}")
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    module.ROW_IDENTITY_FIELDS = ROW_IDENTITY_FIELDS
    module.MANIFEST_PATH = MANIFEST_PATH
    module.DEFAULT_RUN_DIR = DEFAULT_RUN_DIR
    return module


def load_inputs() -> tuple[
    dict[str, Any],
    str,
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
    str,
    dict[str, Any],
    str,
]:
    manifest_raw = MANIFEST_PATH.read_bytes()
    manifest = json.loads(manifest_raw)
    manifest_sha = sha256_bytes(manifest_raw)
    scope = manifest.get("scope") or {}
    if manifest.get("status") != "authorized" or not manifest.get("authorized_at"):
        raise ValueError("V5 image generation manifest is not durably authorized")
    if scope.get("image_generation_authorized") is not True:
        raise ValueError("V5 image generation is not authorized")
    expected_scope = {
        "expected_images": EXPECTED_ROWS,
        "selection_count": len(EXPECTED_SELECTIONS),
        "prompts_per_selection": EXPECTED_SELECTION_ROWS,
        "bank_count": EXPECTED_BANKS,
        "prompts_per_bank_per_selection": EXPECTED_PER_BANK_PER_SELECTION,
        "distinct_candidate_keys": EXPECTED_ROWS,
        "render_count": EXPECTED_RENDER_COUNT,
        "miniPC_excluded": True,
        "candidate_texts_unchanged": True,
    }
    for field, expected in expected_scope.items():
        if scope.get(field) != expected:
            raise ValueError(f"Manifest scope.{field} must equal {expected!r}")

    model = manifest.get("model") or {}
    expected_model = {
        "base_url": "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8000.or2.colligo.dev",
        "model_id": "hp-image",
        "rewriter_model": "gemini-3.1-pro",
        "num_inference_steps": 50,
        "seed": 42,
        "n": 1,
        "width": EXPECTED_OUTPUT_SIZE[0],
        "height": EXPECTED_OUTPUT_SIZE[1],
        "enable_prompt_rewrite": True,
    }
    for field, expected in expected_model.items():
        if model.get(field) != expected:
            raise ValueError(f"Manifest model.{field} must equal {expected!r}")
    if Path(manifest.get("run_dir", "")).resolve() != DEFAULT_RUN_DIR.resolve():
        raise ValueError("Manifest run_dir differs from the isolated V5 run directory")

    selection_documents: dict[str, dict[str, Any]] = {}
    selection_hashes: dict[str, str] = {}
    for item in manifest.get("selections") or []:
        selection_type = item.get("selection_type")
        if selection_type in selection_documents:
            raise ValueError(f"Duplicate selection type: {selection_type}")
        path = require_pinned_file(item, f"{selection_type} selection")
        document = read_json(path)
        if document.get("selection") != selection_type:
            raise ValueError(f"Selection identity differs in {path}")
        if document.get("prompt_count") != EXPECTED_SELECTION_ROWS:
            raise ValueError(f"Selection must contain {EXPECTED_SELECTION_ROWS} prompts: {path}")
        if len(document.get("prompts") or []) != EXPECTED_SELECTION_ROWS:
            raise ValueError(f"Selection prompt array differs: {path}")
        selection_documents[selection_type] = document
        selection_hashes[selection_type] = item["sha256"]
    if set(selection_documents) != EXPECTED_SELECTIONS:
        raise ValueError(f"Expected selections {sorted(EXPECTED_SELECTIONS)}")

    review_path = require_pinned_file(manifest["review_data"], "V5 reviewed prompt data")
    review_document = read_json(review_path)
    review_rows = review_document.get("rows") if isinstance(review_document, dict) else None
    if not isinstance(review_rows, list) or len(review_rows) != 160:
        raise ValueError("V5 reviewed prompt data must contain exactly 160 rows")
    review_by_key = {row["candidate_key"]: row for row in review_rows}
    if len(review_by_key) != len(review_rows):
        raise ValueError("V5 reviewed prompt data contains duplicate candidate keys")

    source_manifest_path = require_pinned_file(
        manifest["source_image_generation_manifest"], "corrected V4.1 image manifest"
    )
    source_manifest = read_json(source_manifest_path)
    if sha256_path(source_manifest_path) != manifest["reference_blob_bindings"]["source_manifest_sha256"]:
        raise ValueError("Blob bindings and corrected render manifest do not share the same source manifest")
    asset_path = require_pinned_file(manifest["corrected_asset_manifest"], "corrected asset manifest")
    asset_document = read_json(asset_path)
    if set(asset_document.get("scope", {}).get("device_types") or []) != {"laptop", "printer"}:
        raise ValueError("Corrected asset manifest must contain laptop and printer only")
    if len(source_manifest.get("renders") or []) != EXPECTED_RENDER_COUNT:
        raise ValueError("Corrected source manifest must contain exactly four renders")

    binding_path = require_pinned_file(manifest["reference_blob_bindings"], "corrected blob bindings")
    binding_document = read_json(binding_path)
    if binding_document.get("manifest_sha256") != manifest["reference_blob_bindings"]["source_manifest_sha256"]:
        raise ValueError("Corrected blob bindings belong to a different source manifest")
    return (
        manifest,
        manifest_sha,
        selection_documents,
        review_by_key,
        source_manifest,
        sha256_path(source_manifest_path),
        binding_document,
        sha256_path(binding_path),
    )


def normalized_render(base: Any, render: dict[str, Any]) -> dict[str, Any]:
    value = base.normalized_render(render)
    if (value["output_width"], value["output_height"]) != EXPECTED_OUTPUT_SIZE:
        raise ValueError(f"Corrected render does not resolve to 2368x1776: {render['render_id']}")
    base.validate_render(value)
    return value


def build_rows(
    base: Any,
    selection_documents: dict[str, dict[str, Any]],
    review_by_key: dict[str, dict[str, Any]],
    source_manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    renders = {
        item["camera_tag"]: normalized_render(base, item)
        for item in source_manifest["renders"]
    }
    if len(renders) != EXPECTED_RENDER_COUNT:
        raise ValueError("Corrected renders must have four unique camera tags")
    rows: list[dict[str, Any]] = []
    candidate_keys: set[str] = set()
    row_ids: set[str] = set()
    counts: dict[tuple[str, str], int] = {}
    ranks: dict[tuple[str, str], set[int]] = {}
    for selection_type, document in sorted(selection_documents.items()):
        for selected in document["prompts"]:
            candidate_key = selected["candidate_key"]
            if candidate_key in candidate_keys:
                raise ValueError(f"Cross-selection overlap is forbidden: {candidate_key}")
            candidate_keys.add(candidate_key)
            reviewed = review_by_key.get(candidate_key)
            if not reviewed:
                raise ValueError(f"Selection candidate is absent from reviewed data: {candidate_key}")
            exact_fields = {
                "case_id": "case_id",
                "pair_id": "pair_id",
                "device_type": "device_type",
                "camera_tag": "camera_tag",
                "view_role": "view_role",
                "environment": "environment",
                "subsetting": "subsetting",
                "prompt": "text",
                "combined_source_relevance_score": "source_relevance_score",
                "ctech_reference_id": "ctech_reference_id",
                "ctech_relationship": "ctech_relationship",
            }
            for selected_field, review_field in exact_fields.items():
                if selected.get(selected_field) != reviewed.get(review_field):
                    raise ValueError(
                        f"Selection/review mismatch for {candidate_key} field {selected_field}"
                    )
            if selected.get("ctech_similarity_score") != reviewed.get("ctech_reference_score"):
                raise ValueError(f"C-Tech score differs for {candidate_key}")
            source_components = reviewed.get("source_score_components") or {}
            if selected.get("smart_brief_score_components") != source_components.get("smart_brief"):
                raise ValueError(f"Smart Brief component scores differ for {candidate_key}")
            if selected.get("source_messaging_score_components") != source_components.get("source_messaging"):
                raise ValueError(f"Source messaging component scores differ for {candidate_key}")
            render = renders.get(selected["camera_tag"])
            if not render or render["device_type"] != selected["device_type"]:
                raise ValueError(f"Cross-device corrected render for {candidate_key}")
            if selected["device_type"] not in {"laptop", "printer"}:
                raise ValueError(f"Excluded device type reached runner: {selected['device_type']}")
            candidate_id = candidate_key.rsplit("::", 1)[-1]
            if reviewed.get("candidate_id") != candidate_id:
                raise ValueError(f"Candidate ID differs for {candidate_key}")
            rank = selected["selection_rank_in_bank"]
            count_key = (selection_type, selected["case_id"])
            counts[count_key] = counts.get(count_key, 0) + 1
            ranks.setdefault(count_key, set()).add(rank)
            row_id = (
                f"{selection_type}__{selected['case_id']}__{candidate_id}__{render['render_id']}"
            )
            if row_id in row_ids:
                raise ValueError(f"Duplicate generation row ID: {row_id}")
            row_ids.add(row_id)
            candidate = {
                **reviewed,
                **selected,
                "id": candidate_id,
                "text": selected["prompt"],
                "rank": rank,
                "selection_type": selection_type,
                "selection_document_label": selected["selection"],
            }
            rows.append(
                {
                    "row_id": row_id,
                    "selection_type": selection_type,
                    "selection_rank_in_bank": rank,
                    "case_id": selected["case_id"],
                    "group_id": reviewed["group_id"],
                    "candidate_key": candidate_key,
                    "pair_id": selected["pair_id"],
                    "render_id": render["render_id"],
                    "candidate_id": candidate_id,
                    "device_type": selected["device_type"],
                    "camera_tag": selected["camera_tag"],
                    "render": render,
                    "candidate": candidate,
                    "accepted_case": reviewed,
                    "selected_row_sha256": canonical_sha256(selected),
                    "reviewed_row_sha256": canonical_sha256(reviewed),
                    "candidate_text_sha256": sha256_bytes(selected["prompt"].encode()),
                }
            )
    if len(rows) != EXPECTED_ROWS or len(candidate_keys) != EXPECTED_ROWS:
        raise ValueError(f"Expected exactly {EXPECTED_ROWS} distinct generation rows")
    if len(counts) != len(EXPECTED_SELECTIONS) * EXPECTED_BANKS:
        raise ValueError(f"Expected {EXPECTED_BANKS} banks in each selection")
    if any(value != EXPECTED_PER_BANK_PER_SELECTION for value in counts.values()):
        raise ValueError(f"Each selection/bank must contain {EXPECTED_PER_BANK_PER_SELECTION} rows")
    if any(value != set(range(1, EXPECTED_PER_BANK_PER_SELECTION + 1)) for value in ranks.values()):
        raise ValueError("Each selection/bank must contain selection ranks 1..5")
    return sorted(rows, key=lambda row: row["row_id"])


def load_exact_bindings(
    base: Any,
    rows: list[dict[str, Any]],
    binding_document: dict[str, Any],
    source_manifest_sha: str,
) -> dict[str, dict[str, Any]]:
    required = {row["render_id"]: row["render"] for row in rows}
    bindings = binding_document.get("bindings") or {}
    if set(required) != set(bindings):
        raise ValueError("Exact corrected blob binding inventory differs from four required renders")
    for render_id, render in required.items():
        binding = bindings[render_id]
        expected = {
            "render_id": render_id,
            "original_png_sha256": render["sha256"],
            "original_png_bytes": render["bytes"],
            "original_png_width": render["width"],
            "original_png_height": render["height"],
            "camera_tag": render["camera_tag"],
            "device_type": render["device_type"],
            "role": render["role"],
            "image_generation_manifest_sha256": source_manifest_sha,
            "upload_endpoint": base.UPLOAD_URL,
            "content_type": "image/png",
        }
        for field, value in expected.items():
            if binding.get(field) != value:
                raise ValueError(f"Exact blob binding mismatch for {render_id} field {field}")
        if not isinstance(binding.get("blob_id"), str) or not binding["blob_id"].strip():
            raise ValueError(f"Exact blob ID missing for {render_id}")
    return {render_id: dict(bindings[render_id]) for render_id in sorted(required)}


def install_v5_engine_hooks(
    base: Any,
    manifest: dict[str, Any],
    selection_hashes: dict[str, str],
    review_data_sha: str,
    binding_document_sha: str,
) -> None:
    base.ROW_IDENTITY_FIELDS = ROW_IDENTITY_FIELDS

    def build_payload(row: dict[str, Any], blob_id: str) -> dict[str, Any]:
        return {
            "prompt": row["candidate"]["text"],
            "size": {"width": EXPECTED_OUTPUT_SIZE[0], "height": EXPECTED_OUTPUT_SIZE[1]},
            "referenceBlobs": [{"id": blob_id}],
            "seeds": [42],
            "n": 1,
            "modelSpecificPayload": {
                "enablePromptRewrite": True,
                "rewriterModel": "gemini-3.1-pro",
                "numInferenceSteps": 50,
            },
        }

    def provenance(
        row: dict[str, Any],
        payload: dict[str, Any],
        binding: dict[str, Any],
        manifest_sha: str,
        _selection_a_sha: str,
        _selection_b_sha: str,
    ) -> dict[str, Any]:
        candidate = row["candidate"]
        return {
            "image_generation_manifest_path": str(MANIFEST_PATH.resolve()),
            "image_generation_manifest_sha256": manifest_sha,
            "selection_type": row["selection_type"],
            "selection_sha256": selection_hashes[row["selection_type"]],
            "all_selection_hashes": dict(sorted(selection_hashes.items())),
            "review_data_path": manifest["review_data"]["path"],
            "review_data_sha256": review_data_sha,
            "selected_row_sha256": row["selected_row_sha256"],
            "reviewed_row_sha256": row["reviewed_row_sha256"],
            "candidate_text_sha256": row["candidate_text_sha256"],
            "input_path": candidate.get("input_path"),
            "input_sha256": candidate.get("input_sha256"),
            "source_scores": {
                "smart_brief_support_score": candidate.get("smart_brief_support_score"),
                "combined_source_relevance_score": candidate.get("combined_source_relevance_score"),
                "ctech_similarity_score": candidate.get("ctech_similarity_score"),
                "smart_brief_score_components": candidate.get("smart_brief_score_components"),
                "source_messaging_score_components": candidate.get("source_messaging_score_components"),
            },
            "reference_blob_bindings_path": manifest["reference_blob_bindings"]["path"],
            "reference_blob_bindings_sha256": binding_document_sha,
            "reference_binding_sha256": canonical_sha256(base.stable_binding(binding)),
            "reference_blob_id": binding["blob_id"],
            "request_payload_sha256": canonical_sha256(payload),
        }

    base.build_payload = build_payload
    base.provenance = provenance


def endpoint_preflight(base: Any, run_dir: Path, manifest: dict[str, Any], manifest_sha: str) -> dict[str, Any]:
    with httpx.Client(timeout=httpx.Timeout(60, connect=20)) as client:
        openapi_response = client.get(base.OPENAPI_URL, headers={"accept": "application/json"})
        openapi_response.raise_for_status()
        openapi_raw = openapi_response.content
        openapi = openapi_response.json()
        metadata_response = client.get(
            base.METADATA_URL,
            headers={"accept": "application/json", "x-foundry-model-id": "hp-image"},
        )
        metadata_response.raise_for_status()
        metadata = metadata_response.json()
    image_schema = openapi["components"]["schemas"]["ImageRequest"]
    model_schema = openapi["components"]["schemas"]["ImageModelSpecificPayload"]
    checks = {
        "explicit_seed_supported": "seeds" in image_schema["properties"],
        "n_supported": "n" in image_schema["properties"],
        "reference_blob_supported": "referenceBlobs" in image_schema["properties"],
        "prompt_rewrite_supported": "enablePromptRewrite" in model_schema["properties"],
        "rewriter_model_supported": "gemini-3.1-pro"
        in model_schema["properties"]["rewriterModel"]["enum"],
        "inference_steps_supported": "numInferenceSteps" in model_schema["properties"],
    }
    if not all(checks.values()):
        raise ValueError(f"Endpoint preflight checks failed: {checks}")
    result = {
        "schema_version": 1,
        "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "endpoint_called": True,
        "generation_submitted": False,
        "base_url": manifest["model"]["base_url"],
        "openapi_http_status": openapi_response.status_code,
        "openapi_sha256": sha256_bytes(openapi_raw),
        "metadata_http_status": metadata_response.status_code,
        "metadata": metadata,
        "manifest_sha256": manifest_sha,
        "request_checks": checks,
        "fixed_request_settings": {
            "size": {"width": 2368, "height": 1776},
            "seeds": [42],
            "n": 1,
            "enablePromptRewrite": True,
            "rewriterModel": "gemini-3.1-pro",
            "numInferenceSteps": 50,
            "model_id": "hp-image",
        },
    }
    base.atomic_write_json(run_dir / "endpoint_preflight.json", result)
    return result


def write_progress(
    base: Any,
    run_dir: Path,
    manifest: dict[str, Any],
    manifest_sha: str,
    selection_hashes: dict[str, str],
    rows: list[dict[str, Any]],
    invocation_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    records = base.load_all_records(run_dir)
    authorized = {row["row_id"] for row in rows}
    known = {record["row_id"] for record in records}
    if len(known) != len(records) or not known <= authorized:
        raise ValueError("Generation records contain duplicate or unauthorized row IDs")
    statuses: dict[str, int] = {}
    for record in records:
        statuses[record["status"]] = statuses.get(record["status"], 0) + 1
    invocation_ids = {row["row_id"] for row in invocation_rows}
    summary = {
        "schema_version": 1,
        "updated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "image_generation_manifest_path": str(MANIFEST_PATH.resolve()),
        "image_generation_manifest_sha256": manifest_sha,
        "selection_hashes": dict(sorted(selection_hashes.items())),
        "available_generation_row_count": len(rows),
        "invocation_generation_row_count": len(invocation_rows),
        "record_count": len(records),
        "record_status_counts": dict(sorted(statuses.items())),
        "missing_record_count": len(authorized - known),
        "invocation_missing_record_count": len(invocation_ids - known),
        "selection_counts": {
            name: sum(row["selection_type"] == name for row in rows)
            for name in sorted(EXPECTED_SELECTIONS)
        },
        "settings": manifest["model"],
        "exact_reference_blob_reuse": True,
    }
    base.atomic_write_json(run_dir / "summary.json", summary)
    lines = b"".join(
        (json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n").encode()
        for record in sorted(records, key=lambda record: record["row_id"])
    )
    base.atomic_write_bytes(run_dir / "results.jsonl", lines)
    return summary


def select_rows(
    rows: list[dict[str, Any]],
    requested_ids: list[str],
    selection_type: str | None,
    launch_all: bool,
) -> list[dict[str, Any]]:
    if launch_all:
        return rows
    if selection_type:
        return [row for row in rows if row["selection_type"] == selection_type]
    if not requested_ids:
        return []
    by_id = {row["row_id"]: row for row in rows}
    missing = sorted(set(requested_ids) - set(by_id))
    if missing:
        raise ValueError(f"Requested rows are outside the frozen V5 selection: {missing}")
    return [by_id[row_id] for row_id in requested_ids]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--list-row-ids", action="store_true")
    parser.add_argument("--row-id", action="append", default=[])
    parser.add_argument("--selection", choices=sorted(EXPECTED_SELECTIONS))
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--poll-window-seconds", type=int, default=1800)
    args = parser.parse_args()
    if args.workers < 1 or args.workers > MAX_WORKERS:
        parser.error(f"--workers must be between 1 and {MAX_WORKERS}")
    if sum((bool(args.all), bool(args.row_id), bool(args.selection))) > 1:
        parser.error("Use at most one of --all, --selection, or --row-id")

    (
        manifest,
        manifest_sha,
        selections,
        review_by_key,
        source_manifest,
        source_manifest_sha,
        binding_document,
        binding_document_sha,
    ) = load_inputs()
    base = load_base_runner(manifest)
    rows = build_rows(base, selections, review_by_key, source_manifest)
    selection_hashes = {
        item["selection_type"]: item["sha256"] for item in manifest["selections"]
    }
    install_v5_engine_hooks(
        base,
        manifest,
        selection_hashes,
        manifest["review_data"]["sha256"],
        binding_document_sha,
    )
    bindings = load_exact_bindings(base, rows, binding_document, source_manifest_sha)
    run_dir = args.run_dir.resolve()
    if run_dir != Path(manifest["run_dir"]).resolve():
        raise ValueError("Requested run directory differs from authorized V5 manifest")

    if args.validate_only:
        print(
            json.dumps(
                {
                    "image_generation_manifest_sha256": manifest_sha,
                    "selection_hashes": selection_hashes,
                    "review_data_sha256": manifest["review_data"]["sha256"],
                    "reference_blob_bindings_sha256": binding_document_sha,
                    "validated_generation_row_count": len(rows),
                    "selection_counts": {
                        name: sum(row["selection_type"] == name for row in rows)
                        for name in sorted(EXPECTED_SELECTIONS)
                    },
                    "distinct_candidate_key_count": len({row["candidate_key"] for row in rows}),
                    "reference_blob_count": len(bindings),
                    "output_size": {"width": 2368, "height": 1776},
                    "endpoint_called": False,
                    "generation_submitted": False,
                },
                indent=2,
            )
        )
        return 0

    for subdirectory in ("jobs", "records", "raw_responses", "images", "invocations"):
        (run_dir / subdirectory).mkdir(parents=True, exist_ok=True)
    if args.list_row_ids:
        print(json.dumps({"row_count": len(rows), "row_ids": [row["row_id"] for row in rows]}, indent=2))
        return 0
    preflight = endpoint_preflight(base, run_dir, manifest, manifest_sha)
    if args.preflight_only:
        summary = write_progress(base, run_dir, manifest, manifest_sha, selection_hashes, rows, [])
        print(json.dumps({"preflight": preflight, "summary": summary}, indent=2))
        return 0
    selected = select_rows(rows, args.row_id, args.selection, args.all)
    if not selected:
        parser.error("No generation rows selected; use --row-id, --selection, or --all")

    invocation = {
        "started_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "image_generation_manifest_sha256": manifest_sha,
        "selection_hashes": selection_hashes,
        "selected_row_ids": [row["row_id"] for row in selected],
        "workers": args.workers,
        "poll_window_seconds": args.poll_window_seconds,
        "exact_reference_blob_reuse": True,
    }
    invocation_name = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    base.atomic_write_json(run_dir / "invocations" / f"{invocation_name}.json", invocation)
    base.log(f"V5 rows selected={len(selected)} workers={args.workers}")
    selection_a_sha = selection_hashes["smart_brief"]
    selection_b_sha = selection_hashes["ctech"]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                base.process_row,
                run_dir,
                row,
                bindings[row["render_id"]],
                manifest_sha,
                selection_a_sha,
                selection_b_sha,
                args.poll_window_seconds,
            ): row
            for row in selected
        }
        for future in as_completed(futures):
            row = futures[future]
            try:
                record = future.result()
                base.log(f"{record['status']} {row['row_id']}")
            except Exception as exc:  # noqa: BLE001 - durable journals preserve details
                base.log(f"ERROR {row['row_id']}: {base.safe_error(exc)}")
            write_progress(base, run_dir, manifest, manifest_sha, selection_hashes, rows, selected)
    print(
        json.dumps(
            write_progress(base, run_dir, manifest, manifest_sha, selection_hashes, rows, selected),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
