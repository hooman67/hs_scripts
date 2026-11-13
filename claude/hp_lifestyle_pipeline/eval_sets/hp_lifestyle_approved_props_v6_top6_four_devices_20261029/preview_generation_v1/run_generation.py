#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "pillow"]
# ///
"""Resumable V6 96-row preview-model generation with immutable provenance."""

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


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
MANIFEST_PATH = HERE / "image_generation_manifest.json"
EXPECTED_ROWS = 96
EXPECTED_BANKS = 16
EXPECTED_PER_BANK = 6
EXPECTED_RENDERS = 16
EXPECTED_SIZE = (2368, 1776)
MAX_WORKERS = 8
ROW_IDENTITY_FIELDS = (
    "row_id",
    "prompt_key",
    "device_id",
    "device_type",
    "camera_tag",
    "render_id",
    "candidate_id",
)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
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


def load_base(manifest: dict[str, Any]):
    specification = manifest["runner_dependency"]
    path = Path(specification["path"]).resolve()
    if not path.is_file() or sha256_path(path) != specification["sha256"]:
        raise ValueError("Frozen V4.1 generation engine is missing or changed")
    module_spec = importlib.util.spec_from_file_location("hp_v6_preview_base", path)
    if not module_spec or not module_spec.loader:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    module.ROW_IDENTITY_FIELDS = ROW_IDENTITY_FIELDS
    module.MANIFEST_PATH = MANIFEST_PATH
    module.DEFAULT_RUN_DIR = Path(manifest["run_dir"])
    return module


def load_inputs() -> tuple[dict[str, Any], str, dict[str, Any], str]:
    raw = MANIFEST_PATH.read_bytes()
    manifest = json.loads(raw)
    manifest_sha = sha256_bytes(raw)
    scope = manifest.get("scope") or {}
    expected_scope = {
        "image_generation_authorized": True,
        "expected_images": EXPECTED_ROWS,
        "device_count": 4,
        "views_per_device": 4,
        "bank_count": EXPECTED_BANKS,
        "prompts_per_bank": EXPECTED_PER_BANK,
        "render_count": EXPECTED_RENDERS,
        "candidate_texts_unchanged": True,
    }
    if manifest.get("status") != "authorized" or not manifest.get("authorized_at"):
        raise ValueError("Generation manifest is not authorized")
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            raise ValueError(f"Manifest scope.{key} must equal {expected!r}")
    expected_model = {
        "base_url": "https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8000.or2.colligo.dev",
        "model_id": "hp-image",
        "rewriter_model": "gemini-3.1-pro",
        "num_inference_steps": 50,
        "seed": 42,
        "n": 1,
        "width": 2368,
        "height": 1776,
        "enable_prompt_rewrite": True,
    }
    for key, expected in expected_model.items():
        if manifest.get("model", {}).get(key) != expected:
            raise ValueError(f"Manifest model.{key} must equal {expected!r}")
    prompt_path = Path(manifest["prompts"]["path"]).resolve()
    if not prompt_path.is_file() or sha256_path(prompt_path) != manifest["prompts"]["sha256"]:
        raise ValueError("Frozen V6 prompt export is missing or changed")
    prompts = read_json(prompt_path)
    if len(prompts.get("prompts") or []) != EXPECTED_ROWS:
        raise ValueError("V6 prompt export must contain exactly 96 rows")
    if len(manifest.get("renders") or []) != EXPECTED_RENDERS:
        raise ValueError("Manifest must contain 16 product-specific renders")
    if Path(manifest["run_dir"]).resolve() != (
        PROJECT
        / "local_data/generation_runs/hp_lifestyle_approved_props_v6_top6_four_devices_20261029_preview"
    ).resolve():
        raise ValueError("Manifest run directory differs from the isolated V6 preview run")
    return manifest, manifest_sha, prompts, manifest["prompts"]["sha256"]


def build_rows(base: Any, manifest: dict[str, Any], prompt_document: dict[str, Any]) -> list[dict[str, Any]]:
    renders: dict[tuple[str, str], dict[str, Any]] = {}
    for raw_render in manifest["renders"]:
        render = base.normalized_render(raw_render)
        base.validate_render(render)
        if (render["output_width"], render["output_height"]) != EXPECTED_SIZE:
            raise ValueError(f"Unexpected output size for {render['render_id']}")
        key = (render["device_id"], render["camera_name"])
        if key in renders:
            raise ValueError(f"Duplicate render mapping: {key}")
        renders[key] = render

    rows = []
    prompt_keys: set[str] = set()
    bank_counts: dict[tuple[str, str], int] = {}
    bank_ranks: dict[tuple[str, str], set[int]] = {}
    for prompt in prompt_document["prompts"]:
        prompt_key = prompt["prompt_key"]
        if prompt_key in prompt_keys:
            raise ValueError(f"Duplicate prompt key: {prompt_key}")
        prompt_keys.add(prompt_key)
        render = renders.get((prompt["device_id"], prompt["source_camera_name"]))
        if not render:
            raise ValueError(f"No corrected render for {prompt_key}")
        if render["device_type"] != prompt["device_type"] or render["camera_tag"] != prompt["camera_tag"]:
            raise ValueError(f"Cross-device or camera render for {prompt_key}")
        candidate_id = prompt_key.rsplit("::", 1)[-1]
        rank = int(prompt["bank_rank"])
        bank = (prompt["device_id"], prompt["camera_tag"])
        bank_counts[bank] = bank_counts.get(bank, 0) + 1
        bank_ranks.setdefault(bank, set()).add(rank)
        row_id = f"{prompt['device_id']}__{prompt['camera_tag']}__{candidate_id}"
        rows.append(
            {
                "row_id": row_id,
                "prompt_key": prompt_key,
                "device_id": prompt["device_id"],
                "device_type": prompt["device_type"],
                "camera_tag": prompt["camera_tag"],
                "render_id": render["render_id"],
                "candidate_id": candidate_id,
                "render": render,
                "candidate": prompt,
                "accepted_case": {
                    "bank": f"{prompt['device_id']}__{prompt['camera_tag']}",
                    "source_pair": prompt["source_pair"],
                    "source_revision": prompt.get("source_revision"),
                },
                "candidate_text_sha256": sha256_bytes(prompt["text"].encode()),
                "candidate_row_sha256": canonical_sha256(prompt),
            }
        )
    if len(rows) != EXPECTED_ROWS or len(prompt_keys) != EXPECTED_ROWS:
        raise ValueError("Expected 96 distinct rows")
    if len(bank_counts) != EXPECTED_BANKS or any(value != EXPECTED_PER_BANK for value in bank_counts.values()):
        raise ValueError("Expected 16 banks with six prompts each")
    if any(value != set(range(1, 7)) for value in bank_ranks.values()):
        raise ValueError("Every bank must contain source ranks 1..6")
    if len({row["render_id"] for row in rows}) != EXPECTED_RENDERS:
        raise ValueError("Every corrected render must be used")
    return sorted(rows, key=lambda row: (row["device_id"], row["camera_tag"], row["candidate"]["bank_rank"]))


def install_hooks(base: Any, manifest: dict[str, Any], prompts_sha: str) -> None:
    def build_payload(row: dict[str, Any], blob_id: str) -> dict[str, Any]:
        return {
            "prompt": row["candidate"]["text"],
            "size": {"width": 2368, "height": 1776},
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
        _unused_a: str,
        _unused_b: str,
    ) -> dict[str, Any]:
        return {
            "image_generation_manifest_path": str(MANIFEST_PATH),
            "image_generation_manifest_sha256": manifest_sha,
            "prompts_path": manifest["prompts"]["path"],
            "prompts_sha256": prompts_sha,
            "candidate_row_sha256": row["candidate_row_sha256"],
            "candidate_text_sha256": row["candidate_text_sha256"],
            "source_revision": row["candidate"].get("source_revision"),
            "reference_source_s3_uri": row["render"]["source_s3_uri"],
            "reference_binding_sha256": canonical_sha256(base.stable_binding(binding)),
            "reference_blob_id": binding["blob_id"],
            "request_payload_sha256": canonical_sha256(payload),
        }

    base.build_payload = build_payload
    base.provenance = provenance


def load_records(base: Any, run_dir: Path) -> list[dict[str, Any]]:
    return base.load_all_records(run_dir)


def write_progress(
    base: Any,
    run_dir: Path,
    manifest: dict[str, Any],
    manifest_sha: str,
    prompts_sha: str,
    rows: list[dict[str, Any]],
    invocation_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    records = load_records(base, run_dir)
    authorized = {row["row_id"] for row in rows}
    known = {record["row_id"] for record in records}
    if len(known) != len(records) or not known <= authorized:
        raise ValueError("Generation records contain duplicate or unauthorized row IDs")
    counts: dict[str, int] = {}
    for record in records:
        counts[record["status"]] = counts.get(record["status"], 0) + 1
    invocation_ids = {row["row_id"] for row in invocation_rows}
    summary = {
        "schema_version": 1,
        "updated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "image_generation_manifest_path": str(MANIFEST_PATH),
        "image_generation_manifest_sha256": manifest_sha,
        "prompts_sha256": prompts_sha,
        "available_generation_row_count": len(rows),
        "invocation_generation_row_count": len(invocation_rows),
        "record_count": len(records),
        "record_status_counts": dict(sorted(counts.items())),
        "missing_record_count": len(authorized - known),
        "invocation_missing_record_count": len(invocation_ids - known),
        "settings": manifest["model"],
        "product_specific_reference_count": EXPECTED_RENDERS,
    }
    base.atomic_write_json(run_dir / "summary.json", summary)
    base.atomic_write_bytes(
        run_dir / "results.jsonl",
        b"".join(
            (json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n").encode()
            for record in sorted(records, key=lambda value: value["row_id"])
        ),
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--list-row-ids", action="store_true")
    parser.add_argument("--row-id", action="append", default=[])
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--upload-workers", type=int, default=4)
    parser.add_argument("--poll-window-seconds", type=int, default=1800)
    args = parser.parse_args()
    if not 1 <= args.workers <= MAX_WORKERS or not 1 <= args.upload_workers <= MAX_WORKERS:
        parser.error(f"worker counts must be between 1 and {MAX_WORKERS}")
    if bool(args.all) and args.row_id:
        parser.error("Use --all or --row-id, not both")

    manifest, manifest_sha, prompt_document, prompts_sha = load_inputs()
    base = load_base(manifest)
    install_hooks(base, manifest, prompts_sha)
    rows = build_rows(base, manifest, prompt_document)
    run_dir = (args.run_dir or Path(manifest["run_dir"])).resolve()
    if run_dir != Path(manifest["run_dir"]).resolve():
        raise ValueError("Requested run directory differs from the authorized manifest")

    if args.validate_only:
        print(
            json.dumps(
                {
                    "manifest_sha256": manifest_sha,
                    "prompts_sha256": prompts_sha,
                    "rows": len(rows),
                    "banks": len({(row['device_id'], row['camera_tag']) for row in rows}),
                    "renders": len({row['render_id'] for row in rows}),
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
    preflight = base.endpoint_preflight(run_dir, manifest, manifest_sha)
    if args.preflight_only:
        print(
            json.dumps(
                {
                    "preflight": preflight,
                    "summary": write_progress(base, run_dir, manifest, manifest_sha, prompts_sha, rows, []),
                },
                indent=2,
            )
        )
        return 0

    by_id = {row["row_id"]: row for row in rows}
    if args.all:
        selected = rows
    elif args.row_id:
        missing = sorted(set(args.row_id) - set(by_id))
        if missing:
            raise ValueError(f"Requested rows are outside the frozen V6 selection: {missing}")
        selected = [by_id[row_id] for row_id in args.row_id]
    else:
        parser.error("No rows selected; use --row-id or --all")

    invocation = {
        "started_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "image_generation_manifest_sha256": manifest_sha,
        "prompts_sha256": prompts_sha,
        "selected_row_ids": [row["row_id"] for row in selected],
        "workers": args.workers,
        "upload_workers": args.upload_workers,
        "poll_window_seconds": args.poll_window_seconds,
    }
    name = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    base.atomic_write_json(run_dir / "invocations" / f"{name}.json", invocation)
    bindings = base.ensure_bindings(run_dir, selected, manifest_sha, args.upload_workers)
    base.log(f"V6 preview rows selected={len(selected)} workers={args.workers}")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                base.process_row,
                run_dir,
                row,
                bindings[row["render_id"]],
                manifest_sha,
                prompts_sha,
                prompts_sha,
                args.poll_window_seconds,
            ): row
            for row in selected
        }
        for future in as_completed(futures):
            row = futures[future]
            try:
                record = future.result()
                base.log(f"{record['status']} {row['row_id']}")
            except Exception as exc:  # noqa: BLE001
                base.log(f"ERROR {row['row_id']}: {base.safe_error(exc)}")
            write_progress(base, run_dir, manifest, manifest_sha, prompts_sha, rows, selected)
    print(json.dumps(write_progress(base, run_dir, manifest, manifest_sha, prompts_sha, rows, selected), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
