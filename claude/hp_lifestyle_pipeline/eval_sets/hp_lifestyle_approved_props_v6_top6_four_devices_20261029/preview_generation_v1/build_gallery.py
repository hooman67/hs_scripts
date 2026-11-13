#!/usr/bin/env python3
"""Build the V6 bank-organized prompt and preview-generation gallery."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
EVAL_ROOT = HERE.parent
PROJECT = HERE.parents[2]
RUNNER_PATH = HERE / "run_generation.py"
MANIFEST_PATH = HERE / "image_generation_manifest.json"
RECOVERY_MANIFEST_PATH = HERE / "recovery_manifest.json"
TEMPLATE_DIR = HERE / "gallery_template"
REVISION_DIR = EVAL_ROOT / "revisions/v6-approved-20261029-final-r44"
INPUTS_DIR = REVISION_DIR / "inputs"
ALL_PROMPTS_PATH = REVISION_DIR / "exports/final/prompts_all_160.json"
DEFAULT_RUN_DIR = (
    PROJECT
    / "local_data/generation_runs/hp_lifestyle_approved_props_v6_top6_four_devices_20261029_preview"
)
EXPECTED_GENERATED_ROWS = 96
EXPECTED_DISPLAY_ROWS = 160
EXPECTED_BANKS = 16
EXPECTED_GENERATED_PER_BANK = 6
EXPECTED_DISPLAY_PER_BANK = 10
EXPECTED_RENDERS = 16
EXPECTED_SIZE = (2368, 1776)
ALLOWED_STATUSES = {"done", "pending", "failed"}
SENSITIVE_KEYS = {
    "authorization",
    "presignedurl",
    "x-gw-ims-user-token",
    "x-amz-security-token",
    "x-amz-credential",
    "x-amz-signature",
}
SENSITIVE_MARKERS = (
    "x-amz-signature=",
    "x-amz-credential=",
    "x-amz-security-token=",
)


def load_runner():
    specification = importlib.util.spec_from_file_location("hp_v6_gallery_runner", RUNNER_PATH)
    if not specification or not specification.loader:
        raise RuntimeError(f"Cannot load V6 runner: {RUNNER_PATH}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_all_candidates() -> tuple[list[dict[str, Any]], str]:
    raw = ALL_PROMPTS_PATH.read_bytes()
    document = json.loads(raw)
    candidates = document.get("prompts") or []
    if len(candidates) != EXPECTED_DISPLAY_ROWS:
        raise ValueError(f"Expected {EXPECTED_DISPLAY_ROWS} V6 candidates")
    keys = [candidate.get("prompt_key") for candidate in candidates]
    if None in keys or len(set(keys)) != EXPECTED_DISPLAY_ROWS:
        raise ValueError("The 160-candidate V6 artifact has missing or duplicate prompt keys")
    bank_counts: dict[str, int] = {}
    bank_ranks: dict[str, set[int]] = {}
    for candidate in candidates:
        bank_id = candidate["prompt_key"].split("::", 1)[0]
        if candidate.get("bank_debug_ref") != bank_id:
            raise ValueError(f"Candidate bank metadata differs for {candidate['prompt_key']}")
        bank_counts[bank_id] = bank_counts.get(bank_id, 0) + 1
        bank_ranks.setdefault(bank_id, set()).add(candidate["bank_rank"])
        if sha256_bytes(candidate["text"].encode()) != candidate.get("text_sha256"):
            raise ValueError(f"Candidate text hash differs for {candidate['prompt_key']}")
    if len(bank_counts) != EXPECTED_BANKS or set(bank_counts.values()) != {EXPECTED_DISPLAY_PER_BANK}:
        raise ValueError(f"Expected 16 ten-candidate banks, found {bank_counts}")
    if any(ranks != set(range(1, EXPECTED_DISPLAY_PER_BANK + 1)) for ranks in bank_ranks.values()):
        raise ValueError("Each V6 bank must contain ranks 1 through 10")
    return candidates, sha256_bytes(raw)


def atomic_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(value)
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())


def assert_sanitized(value: Any, location: str = "gallery") -> None:
    """Reject credentials and presigned query material before gallery serialization."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key.casefold() in SENSITIVE_KEYS:
                raise ValueError(f"Sensitive field reached gallery at {location}.{key}")
            assert_sanitized(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_sanitized(child, f"{location}[{index}]")
    elif isinstance(value, str) and any(marker in value.casefold() for marker in SENSITIVE_MARKERS):
        raise ValueError(f"Presigned credential material reached gallery at {location}")


def copy_templates(run_dir: Path) -> None:
    gallery = run_dir / "gallery"
    gallery.mkdir(parents=True, exist_ok=True)
    expected = {"index.html", "main.js", "style.css", "imsauth.js"}
    actual = {path.name for path in TEMPLATE_DIR.iterdir() if path.is_file()}
    if actual != expected:
        raise ValueError(f"Gallery template inventory differs: {sorted(actual)}")
    for name in sorted(expected):
        raw = (TEMPLATE_DIR / name).read_bytes()
        target = gallery / name
        if not target.exists() or target.read_bytes() != raw:
            atomic_bytes(target, raw)


def copy_corrected_inputs(
    run_dir: Path, rows: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    destination = run_dir / "assets/corrected_inputs"
    destination.mkdir(parents=True, exist_ok=True)
    corrected: dict[str, dict[str, Any]] = {}
    intended: set[str] = set()
    for row in rows:
        render = row["render"]
        render_id = render["render_id"]
        if render_id in corrected:
            continue
        source = Path(render["path"]).resolve()
        raw = source.read_bytes()
        if len(raw) != render["bytes"] or sha256_bytes(raw) != render["sha256"]:
            raise ValueError(f"Corrected digital-twin bytes differ: {render_id}")
        if render["format"].upper() != "PNG" or not raw.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError(f"Corrected digital twin is not PNG: {render_id}")
        if (render["width"], render["height"]) != EXPECTED_SIZE:
            raise ValueError(f"Corrected digital-twin dimensions differ: {render_id}")
        filename = f"{render_id}.png"
        if not re.fullmatch(r"[A-Za-z0-9._-]+\.png", filename):
            raise ValueError(f"Unsafe corrected digital-twin filename: {filename}")
        intended.add(filename)
        target = destination / filename
        if not target.exists() or target.read_bytes() != raw:
            atomic_bytes(target, raw)
        if target.stat().st_size != render["bytes"] or sha256_path(target) != render["sha256"]:
            raise ValueError(f"Gallery corrected digital twin differs: {render_id}")
        corrected[render_id] = {
            **render,
            "source_path": str(source),
            "gallery_path": f"assets/corrected_inputs/{filename}",
            "same_bytes_as_endpoint_input": True,
        }
    unexpected = sorted(
        path.name for path in destination.iterdir() if path.is_file() and path.name not in intended
    )
    if unexpected:
        raise ValueError(f"Unexpected corrected inputs in V6 run: {unexpected}")
    if len(corrected) != EXPECTED_RENDERS:
        raise ValueError(f"Gallery requires {EXPECTED_RENDERS} corrected digital twins")
    return corrected


def load_source_documents(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    bank_ids = {row["accepted_case"]["bank"] for row in rows}
    if len(bank_ids) != EXPECTED_BANKS:
        raise ValueError(f"Expected {EXPECTED_BANKS} source-document banks")
    expected_files = {f"{bank_id}.json" for bank_id in bank_ids}
    actual_files = {path.name for path in INPUTS_DIR.glob("*.json")}
    if actual_files != expected_files:
        raise ValueError("V6 r44 source input inventory differs from the 16 prompt banks")
    sources: dict[str, dict[str, Any]] = {}
    for bank_id in sorted(bank_ids):
        path = INPUTS_DIR / f"{bank_id}.json"
        raw = path.read_bytes()
        value = json.loads(raw)
        if set(value) != {"smart_brief", "source_messaging", "camera_tag"}:
            raise ValueError(f"Unexpected source input envelope: {path}")
        if value["camera_tag"] != bank_id.split("__", 1)[1]:
            raise ValueError(f"Source camera tag differs for bank {bank_id}")
        if not value["smart_brief"] or not value["source_messaging"]:
            raise ValueError(f"Source documents are empty for bank {bank_id}")
        sources[bank_id] = {
            **value,
            "input_path": str(path.resolve()),
            "input_sha256": sha256_bytes(raw),
            "source_revision": "v6-approved-20261029-final-r44",
        }
    return sources


def resolved_generated_image(
    record: dict[str, Any], row_id: str, run_dir: Path
) -> dict[str, Any]:
    image = dict(record.get("generated_image") or {})
    required = {
        "path",
        "filename",
        "sha256",
        "bytes",
        "native_width",
        "native_height",
        "native_format",
        "content_type",
    }
    missing = sorted(required - set(image))
    if missing:
        raise ValueError(f"Done image metadata is incomplete for {row_id}: {missing}")
    path = Path(image["path"]).resolve()
    if path.parent != (run_dir / "images").resolve() or path.name != image["filename"]:
        raise ValueError(f"Generated image is outside the isolated V6 run: {row_id}")
    if not path.is_file() or path.stat().st_size != image["bytes"]:
        raise ValueError(f"Generated image bytes are missing for {row_id}")
    if sha256_path(path) != image["sha256"]:
        raise ValueError(f"Generated image SHA-256 differs for {row_id}")
    if (image["native_width"], image["native_height"]) != EXPECTED_SIZE:
        raise ValueError(f"Generated image dimensions differ for {row_id}")
    if image["native_format"].upper() != "PNG" or not path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Generated output is not PNG for {row_id}")
    image["path"] = str(path)
    image["gallery_path"] = f"images/{path.name}"
    return image


def project_record(
    runner: Any,
    base: Any,
    row: dict[str, Any],
    run_dir: Path,
) -> tuple[str, str, dict[str, Any] | None]:
    path = base.record_path(run_dir, row["row_id"])
    if not path.exists():
        return "pending", "not_started_or_submitted_no_durable_record", None
    record = read_json(path)
    assert_sanitized(record, f"record[{row['row_id']}]")
    status = record.get("status")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Unknown record status for {row['row_id']}: {status}")
    for field in runner.ROW_IDENTITY_FIELDS:
        if record.get(field) != row[field]:
            raise ValueError(f"Record identity differs for {row['row_id']} field {field}")
    payload = record.get("request_payload") or {}
    reference_blobs = payload.get("referenceBlobs") or []
    if len(reference_blobs) != 1 or not reference_blobs[0].get("id"):
        raise ValueError(f"Record must contain one reference blob ID for {row['row_id']}")
    expected_payload = base.build_payload(row, reference_blobs[0]["id"])
    if payload != expected_payload:
        raise ValueError(f"Record request payload differs for {row['row_id']}")
    provenance = record.get("provenance") or {}
    if provenance.get("candidate_row_sha256") != row["candidate_row_sha256"]:
        raise ValueError(f"Record candidate row provenance differs for {row['row_id']}")
    if provenance.get("candidate_text_sha256") != row["candidate_text_sha256"]:
        raise ValueError(f"Record candidate text provenance differs for {row['row_id']}")
    binding = record.get("reference_binding") or {}
    if binding.get("render_id") != row["render_id"]:
        raise ValueError(f"Record render binding differs for {row['row_id']}")
    if binding.get("original_png_sha256") != row["render"]["sha256"]:
        raise ValueError(f"Record corrected-reference bytes differ for {row['row_id']}")
    projected = dict(record)
    projected["record_path"] = str(path.resolve())
    projected["record_sha256"] = sha256_path(path)
    if status == "done":
        projected["generated_image"] = resolved_generated_image(record, row["row_id"], run_dir)
        if "usedPrompt" not in record or "debugData" not in record:
            raise ValueError(f"Done record lacks rewrite/debug data for {row['row_id']}")
    return status, str(record.get("failure_class") or record.get("job_status") or status), projected


def results_snapshot(run_dir: Path) -> bytes:
    source = run_dir / "results.jsonl"
    if source.exists():
        raw = source.read_bytes()
        for index, line in enumerate(raw.splitlines(), 1):
            if line.strip():
                assert_sanitized(json.loads(line), f"results.jsonl[{index}]")
        return raw
    records = []
    for path in sorted((run_dir / "records").glob("*.json")):
        record = read_json(path)
        assert_sanitized(record, f"record_snapshot[{path.name}]")
        records.append(record)
    return b"".join(
        (json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n").encode()
        for record in sorted(records, key=lambda item: item["row_id"])
    )


def copy_downloads(
    run_dir: Path,
    manifest: dict[str, Any],
    sources: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    destination = run_dir / "downloads"
    destination.mkdir(parents=True, exist_ok=True)
    source_input_document = {
        "version": "hp-v6-r44-gallery-source-inputs-v1",
        "revision": "v6-approved-20261029-final-r44",
        "inputs": sources,
    }
    items: list[tuple[str, bytes, str]] = [
        ("image_generation_manifest.json", MANIFEST_PATH.read_bytes(), "Download generation manifest"),
        ("prompts_top6_96.json", Path(manifest["prompts"]["path"]).read_bytes(), "Download 96 prompts"),
        ("prompts_all_160.json", ALL_PROMPTS_PATH.read_bytes(), "Download all 160 prompt candidates"),
        ("results.jsonl", results_snapshot(run_dir), "Download generation results"),
        (
            "source_inputs_r44.json",
            (json.dumps(source_input_document, ensure_ascii=False, indent=2) + "\n").encode(),
            "Download Smart Brief + source messaging inputs",
        ),
    ]
    if RECOVERY_MANIFEST_PATH.is_file():
        items.append(
            (
                "recovery_manifest.json",
                RECOVERY_MANIFEST_PATH.read_bytes(),
                "Download generation recovery manifest",
            )
        )
    downloads: list[dict[str, str]] = []
    intended = {name for name, _, _ in items}
    for filename, raw, label in items:
        target = destination / filename
        if not target.exists() or target.read_bytes() != raw:
            atomic_bytes(target, raw)
        downloads.append(
            {"label": label, "path": f"../downloads/{filename}", "sha256": sha256_bytes(raw)}
        )
    unexpected = sorted(
        path.name for path in destination.iterdir() if path.is_file() and path.name not in intended
    )
    if unexpected:
        raise ValueError(f"Unexpected V6 gallery downloads: {unexpected}")
    return downloads


def build(run_dir: Path, final: bool = False) -> dict[str, Any]:
    runner = load_runner()
    manifest, manifest_sha, prompt_document, prompts_sha = runner.load_inputs()
    if run_dir.resolve() != Path(manifest["run_dir"]).resolve() or run_dir.resolve() != DEFAULT_RUN_DIR.resolve():
        raise ValueError("Gallery run directory differs from the authorized isolated V6 run")
    base = runner.load_base(manifest)
    runner.install_hooks(base, manifest, prompts_sha)
    rows = runner.build_rows(base, manifest, prompt_document)
    if len(rows) != EXPECTED_GENERATED_ROWS:
        raise ValueError(f"V6 generation run requires {EXPECTED_GENERATED_ROWS} rows")
    all_candidates, all_prompts_sha = load_all_candidates()
    run_dir.mkdir(parents=True, exist_ok=True)
    copy_templates(run_dir)
    corrected = copy_corrected_inputs(run_dir, rows)
    sources = load_source_documents(rows)
    downloads = copy_downloads(run_dir, manifest, sources)

    generation_counts = {"done": 0, "pending": 0, "failed": 0}
    generated_rows: dict[str, dict[str, Any]] = {}
    bank_counts: dict[str, int] = {}
    for row in rows:
        bank_id = row["accepted_case"]["bank"]
        bank_counts[bank_id] = bank_counts.get(bank_id, 0) + 1
        status, reason, record = project_record(runner, base, row, run_dir)
        generation_counts[status] += 1
        generated_rows[row["prompt_key"]] = {
                **{field: row[field] for field in runner.ROW_IDENTITY_FIELDS},
                "bank_id": bank_id,
                "status": status,
                "status_reason": reason,
                "error": record.get("error") if record else None,
                "candidate": row["candidate"],
                "corrected_input": corrected[row["render_id"]],
                "provenance": {
                    "candidate_row_sha256": row["candidate_row_sha256"],
                    "candidate_text_sha256": row["candidate_text_sha256"],
                    "image_generation_manifest_sha256": manifest_sha,
                    "generated_prompts_sha256": prompts_sha,
                    "all_prompts_sha256": all_prompts_sha,
                    "source_input_sha256": sources[bank_id]["input_sha256"],
                    "source_input_path": sources[bank_id]["input_path"],
                    "source_revision": row["candidate"].get("source_revision"),
                    "gallery_source_revision": "v6-approved-20261029-final-r44",
                },
                "record": record,
            }
    if len(generated_rows) != EXPECTED_GENERATED_ROWS:
        raise ValueError("Generated prompt keys are not unique")
    all_by_key = {candidate["prompt_key"]: candidate for candidate in all_candidates}
    if not set(generated_rows).issubset(all_by_key):
        raise ValueError("Generated prompts are not a subset of the frozen 160-candidate artifact")
    for prompt_key, row in generated_rows.items():
        if row["candidate"] != all_by_key[prompt_key]:
            raise ValueError(f"Generated candidate differs from the 160-candidate artifact: {prompt_key}")

    representatives: dict[str, dict[str, Any]] = {}
    for row in generated_rows.values():
        representatives.setdefault(row["bank_id"], row)
    projected_rows: list[dict[str, Any]] = []
    for candidate in all_candidates:
        prompt_key = candidate["prompt_key"]
        bank_id = prompt_key.split("::", 1)[0]
        if prompt_key in generated_rows:
            projected_rows.append(generated_rows[prompt_key])
            continue
        representative = representatives[bank_id]
        projected_rows.append(
            {
                "row_id": f"prompt-only::{prompt_key}",
                "prompt_key": prompt_key,
                "device_id": candidate["device_id"],
                "device_type": candidate["device_type"],
                "camera_tag": candidate["camera_tag"],
                "render_id": representative["render_id"],
                "candidate_id": candidate["id"],
                "bank_id": bank_id,
                "status": "prompt_only",
                "status_reason": "Ranks 7–10 were authored and scored but were outside the top-six image-generation selection.",
                "error": None,
                "candidate": candidate,
                "corrected_input": representative["corrected_input"],
                "provenance": {
                    "candidate_text_sha256": candidate["text_sha256"],
                    "all_prompts_sha256": all_prompts_sha,
                    "source_input_sha256": sources[bank_id]["input_sha256"],
                    "source_input_path": sources[bank_id]["input_path"],
                    "source_revision": candidate.get("source_revision"),
                    "gallery_source_revision": "v6-approved-20261029-final-r44",
                    "generation_selection": "not_selected_for_top6_generation",
                },
                "record": None,
            }
        )
    referenced_outputs = {
        Path(row["record"]["generated_image"]["path"]).resolve()
        for row in projected_rows
        if row["status"] == "done"
    }
    image_inventory = {
        path.resolve() for path in (run_dir / "images").glob("*") if path.is_file()
    }
    if final and image_inventory != referenced_outputs:
        raise ValueError("Generated-image inventory differs from validated done records")
    if set(bank_counts.values()) != {EXPECTED_GENERATED_PER_BANK} or len(bank_counts) != EXPECTED_BANKS:
        raise ValueError(f"Expected 16 six-row banks, found {bank_counts}")
    if final and generation_counts != {"done": EXPECTED_GENERATED_ROWS, "pending": 0, "failed": 0}:
        raise ValueError(f"Final gallery requires {EXPECTED_GENERATED_ROWS} done rows: {generation_counts}")

    display_bank_counts: dict[str, int] = {}
    banks: list[dict[str, Any]] = []
    bank_order: list[str] = []
    for row in projected_rows:
        if row["bank_id"] not in display_bank_counts:
            bank_order.append(row["bank_id"])
        display_bank_counts[row["bank_id"]] = display_bank_counts.get(row["bank_id"], 0) + 1
    if len(projected_rows) != EXPECTED_DISPLAY_ROWS or set(display_bank_counts.values()) != {EXPECTED_DISPLAY_PER_BANK}:
        raise ValueError(f"Expected 16 ten-row display banks, found {display_bank_counts}")
    for bank_id in bank_order:
        bank_rows = sorted(
            (row for row in projected_rows if row["bank_id"] == bank_id),
            key=lambda row: row["candidate"]["bank_rank"],
        )
        representative = bank_rows[0]
        candidate = representative["candidate"]
        banks.append(
            {
                "bank_id": bank_id,
                "device_id": candidate["device_id"],
                "device_display_name": candidate["device_display_name"],
                "device_type": candidate["device_type"],
                "source_pair": candidate["source_pair"],
                "camera_tag": candidate["camera_tag"],
                "source_camera_name": candidate["source_camera_name"],
                "view_role": candidate["view_role"],
                "prompt_keys": [row["prompt_key"] for row in bank_rows],
                "candidate_count": len(bank_rows),
                "generated_selection_count": sum(row["status"] != "prompt_only" for row in bank_rows),
                "prompt_only_count": sum(row["status"] == "prompt_only" for row in bank_rows),
            }
        )

    data = {
        "version": "hp-v6-preview-generation-gallery-v2",
        "metadata": {
            "built_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "mode": "final" if final else "progressive",
            "row_count": EXPECTED_DISPLAY_ROWS,
            "candidate_row_count": EXPECTED_DISPLAY_ROWS,
            "generation_row_count": EXPECTED_GENERATED_ROWS,
            "bank_count": EXPECTED_BANKS,
            "prompts_per_bank": EXPECTED_DISPLAY_PER_BANK,
            "generated_prompts_per_bank": EXPECTED_GENERATED_PER_BANK,
            "corrected_input_count": EXPECTED_RENDERS,
            "status_counts": {**generation_counts, "prompt_only": EXPECTED_DISPLAY_ROWS - EXPECTED_GENERATED_ROWS},
            "generation_status_counts": generation_counts,
            "environments": sorted({row["candidate"]["environment"] for row in projected_rows}),
            "devices": sorted({row["device_id"] for row in projected_rows}),
            "views": sorted({row["candidate"]["view_role"] for row in projected_rows}),
            "run_dir": str(run_dir),
            "s3_prefix": manifest["s3"]["prefix"],
            "downloads": downloads,
            "image_generation_manifest_sha256": manifest_sha,
            "prompts_sha256": prompts_sha,
            "all_prompts_sha256": all_prompts_sha,
            "exact_reference_bytes_verified": True,
            "done_output_bytes_verified": True,
            "no_fake_results": True,
        },
        "sources": sources,
        "banks": banks,
        "rows": projected_rows,
    }
    assert_sanitized(data)
    atomic_bytes(
        run_dir / "gallery/data.js",
        ("const GENERATION_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n").encode(),
    )

    artifacts: dict[str, dict[str, Any]] = {}
    for root in (run_dir / "gallery", run_dir / "assets/corrected_inputs", run_dir / "downloads"):
        for path in sorted(root.rglob("*")):
            if path.is_file():
                artifacts[str(path.relative_to(run_dir))] = {
                    "bytes": path.stat().st_size,
                    "sha256": sha256_path(path),
                }
    for path in sorted(referenced_outputs):
        artifacts[str(path.relative_to(run_dir))] = {
            "bytes": path.stat().st_size,
            "sha256": sha256_path(path),
        }
    result = {
        "version": "hp-v6-preview-generation-gallery-build-v2",
        "mode": data["metadata"]["mode"],
        "built_at_utc": data["metadata"]["built_at_utc"],
        "run_dir": str(run_dir),
        "row_count": EXPECTED_DISPLAY_ROWS,
        "generation_row_count": EXPECTED_GENERATED_ROWS,
        "bank_count": EXPECTED_BANKS,
        "status_counts": {**generation_counts, "prompt_only": EXPECTED_DISPLAY_ROWS - EXPECTED_GENERATED_ROWS},
        "image_generation_manifest_sha256": manifest_sha,
        "prompts_sha256": prompts_sha,
        "corrected_input_hashes": {
            render_id: value["sha256"] for render_id, value in sorted(corrected.items())
        },
        "artifacts": artifacts,
    }
    atomic_json(run_dir / "generation_gallery_build.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build(args.run_dir.resolve(), args.final), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
