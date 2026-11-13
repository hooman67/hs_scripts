#!/usr/bin/env python3
"""Build a progressive, provenance-preserving gallery for the V5 80-row run."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any


GENERATION_DIR = Path(__file__).resolve().parent
EVAL_ROOT = GENERATION_DIR.parent
RUNNER_PATH = GENERATION_DIR / "run_generation.py"
TEMPLATE_DIR = GENERATION_DIR / "gallery_template"
DEFAULT_RUN_DIR = (
    EVAL_ROOT.parents[1]
    / "local_data/generation_runs/hp_lifestyle_dual_source_v5_pilot_20261027_top5_dual"
)
EXPECTED_ROWS = 80
SENSITIVE_KEYS = {
    "authorization",
    "presignedurl",
    "x-gw-ims-user-token",
    "x-amz-security-token",
    "x-amz-credential",
    "x-amz-signature",
}
SENSITIVE_MARKERS = ("x-amz-signature=", "x-amz-credential=", "x-amz-security-token=")


def load_runner():
    specification = importlib.util.spec_from_file_location("hp_v5_gallery_runner", RUNNER_PATH)
    if not specification or not specification.loader:
        raise RuntimeError(f"Cannot load V5 runner: {RUNNER_PATH}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(value)
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_sanitized(value: Any, location: str = "record") -> None:
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
    destination = run_dir / "gallery"
    destination.mkdir(parents=True, exist_ok=True)
    expected = {"index.html", "main.js", "style.css", "imsauth.js"}
    if {path.name for path in TEMPLATE_DIR.iterdir() if path.is_file()} != expected:
        raise ValueError("Gallery template inventory differs")
    for name in sorted(expected):
        raw = (TEMPLATE_DIR / name).read_bytes()
        target = destination / name
        if not target.exists() or target.read_bytes() != raw:
            atomic_bytes(target, raw)


def copy_corrected_inputs(run_dir: Path, rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    destination = run_dir / "assets/corrected_inputs"
    destination.mkdir(parents=True, exist_ok=True)
    rendered: dict[str, dict[str, Any]] = {}
    intended: set[str] = set()
    for row in rows:
        render = row["render"]
        if render["render_id"] in rendered:
            continue
        source = Path(render["path"]).resolve()
        raw = source.read_bytes()
        if len(raw) != render["bytes"] or sha256_path(source) != render["sha256"]:
            raise ValueError(f"Corrected input bytes differ: {render['render_id']}")
        filename = f"{render['render_id']}.png"
        intended.add(filename)
        target = destination / filename
        if not target.exists() or target.read_bytes() != raw:
            atomic_bytes(target, raw)
        if sha256_path(target) != render["sha256"]:
            raise ValueError(f"Gallery corrected input differs: {render['render_id']}")
        rendered[render["render_id"]] = {
            **render,
            "source_path": str(source),
            "gallery_path": f"assets/corrected_inputs/{filename}",
            "same_bytes_as_endpoint_input": True,
        }
    unexpected = sorted(path.name for path in destination.iterdir() if path.is_file() and path.name not in intended)
    if unexpected:
        raise ValueError(f"Unexpected corrected inputs in gallery run: {unexpected}")
    if len(rendered) != 4:
        raise ValueError("Gallery must contain exactly four corrected inputs")
    return rendered


def project_record(runner: Any, base: Any, row: dict[str, Any], run_dir: Path) -> tuple[str, str, dict[str, Any] | None]:
    path = base.record_path(run_dir, row["row_id"])
    if not path.exists():
        return "pending", "not_started_no_record", None
    record = read_json(path)
    assert_sanitized(record)
    status = record.get("status")
    if status not in {"done", "pending", "failed"}:
        raise ValueError(f"Unknown generation record status for {row['row_id']}: {status}")
    for field in runner.ROW_IDENTITY_FIELDS:
        if record.get(field) != row[field]:
            raise ValueError(f"Record identity differs for {row['row_id']} field {field}")
    payload = record.get("request_payload") or {}
    if payload.get("prompt") != row["candidate"]["text"]:
        raise ValueError(f"Record request prompt differs for {row['row_id']}")
    if payload.get("size") != {"width": 2368, "height": 1776}:
        raise ValueError(f"Record request dimensions differ for {row['row_id']}")
    if payload.get("seeds") != [42] or payload.get("n") != 1:
        raise ValueError(f"Record seed/count differs for {row['row_id']}")
    reference = payload.get("referenceBlobs") or []
    if len(reference) != 1:
        raise ValueError(f"Record must use exactly one reference blob: {row['row_id']}")
    projected = dict(record)
    projected["record_path"] = str(path.resolve())
    projected["record_sha256"] = sha256_path(path)
    if status == "done":
        image = dict(record.get("generated_image") or {})
        image_path = Path(image.get("path", "")).resolve()
        if image_path.parent != (run_dir / "images").resolve():
            raise ValueError(f"Generated image is outside the isolated V5 run: {row['row_id']}")
        if not image_path.is_file() or image_path.stat().st_size != image.get("bytes"):
            raise ValueError(f"Generated image bytes missing: {row['row_id']}")
        if sha256_path(image_path) != image.get("sha256"):
            raise ValueError(f"Generated image SHA-256 differs: {row['row_id']}")
        if (image.get("native_width"), image.get("native_height")) != (2368, 1776):
            raise ValueError(f"Generated image dimensions differ: {row['row_id']}")
        if "usedPrompt" not in record or "debugData" not in record:
            raise ValueError(f"Done record lacks rewrite/debug data: {row['row_id']}")
        image["gallery_path"] = f"images/{image_path.name}"
        projected["generated_image"] = image
    return status, str(record.get("failure_class") or record.get("job_status") or status), projected


def copy_downloads(run_dir: Path, manifest: dict[str, Any]) -> list[dict[str, str]]:
    destination = run_dir / "downloads"
    destination.mkdir(parents=True, exist_ok=True)
    downloads: list[dict[str, str]] = []
    sources = [
        (Path(item["path"]), Path(item["path"]).name, f"Download {item['selection_type']} selection")
        for item in manifest["selections"]
    ]
    sources.append((Path(__file__).with_name("image_generation_manifest.json"), "image_generation_manifest.json", "Download generation manifest"))
    results = run_dir / "results.jsonl"
    if results.exists():
        sources.append((results, "results.jsonl", "Download generation records"))
    for source, filename, label in sources:
        raw = source.read_bytes()
        target = destination / filename
        if not target.exists() or target.read_bytes() != raw:
            atomic_bytes(target, raw)
        downloads.append({"label": label, "path": f"../downloads/{filename}"})
    return downloads


def build(run_dir: Path, final: bool = False) -> dict[str, Any]:
    runner = load_runner()
    (
        manifest,
        manifest_sha,
        selections,
        review_by_key,
        source_manifest,
        source_manifest_sha,
        binding_document,
        binding_sha,
    ) = runner.load_inputs()
    if run_dir.resolve() != Path(manifest["run_dir"]).resolve():
        raise ValueError("Gallery run directory differs from authorized V5 manifest")
    base = runner.load_base_runner(manifest)
    rows = runner.build_rows(base, selections, review_by_key, source_manifest)
    runner.load_exact_bindings(base, rows, binding_document, source_manifest_sha)
    run_dir.mkdir(parents=True, exist_ok=True)
    copy_templates(run_dir)
    corrected = copy_corrected_inputs(run_dir, rows)
    downloads = copy_downloads(run_dir, manifest)

    status_counts = {"done": 0, "pending": 0, "failed": 0}
    projected_rows: list[dict[str, Any]] = []
    sources: dict[str, dict[str, Any]] = {}
    for row in rows:
        status, reason, record = project_record(runner, base, row, run_dir)
        status_counts[status] += 1
        source = row["accepted_case"]
        source_entry = {
            "smart_brief": source["smart_brief"],
            "source_messaging": source["source_messaging"],
            "input_path": source["input_path"],
            "input_sha256": source["input_sha256"],
        }
        if row["case_id"] in sources and sources[row["case_id"]] != source_entry:
            raise ValueError(f"Source documents differ within bank: {row['case_id']}")
        sources[row["case_id"]] = source_entry
        candidate = dict(row["candidate"])
        candidate.pop("smart_brief", None)
        candidate.pop("source_messaging", None)
        provenance = {
            "selection_type": row["selection_type"],
            "selected_row_sha256": row["selected_row_sha256"],
            "reviewed_row_sha256": row["reviewed_row_sha256"],
            "candidate_text_sha256": row["candidate_text_sha256"],
            "selection_file_sha256": next(
                item["sha256"] for item in manifest["selections"] if item["selection_type"] == row["selection_type"]
            ),
            "review_data_sha256": manifest["review_data"]["sha256"],
            "reference_blob_bindings_sha256": binding_sha,
            "image_generation_manifest_sha256": manifest_sha,
        }
        projected_rows.append(
            {
                **{field: row[field] for field in runner.ROW_IDENTITY_FIELDS},
                "status": status,
                "status_reason": reason,
                "error": record.get("error") if record else None,
                "candidate": candidate,
                "corrected_input": corrected[row["render_id"]],
                "provenance": provenance,
                "record": record,
            }
        )
    if final and status_counts != {"done": EXPECTED_ROWS, "pending": 0, "failed": 0}:
        raise ValueError(f"Final gallery requires 80 done rows: {status_counts}")
    if len(sources) != 8:
        raise ValueError("Gallery must contain eight source-document banks")

    data = {
        "version": "hp-v5-top5-dual-generation-gallery-v1",
        "metadata": {
            "built_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "mode": "final" if final else "progressive",
            "row_count": EXPECTED_ROWS,
            "selection_counts": {name: sum(row["selection_type"] == name for row in rows) for name in sorted(runner.EXPECTED_SELECTIONS)},
            "status_counts": status_counts,
            "case_count": 8,
            "corrected_input_count": 4,
            "selections": sorted(runner.EXPECTED_SELECTIONS),
            "environments": sorted({row["candidate"]["environment"] for row in rows}),
            "devices": sorted({row["device_type"] for row in rows}),
            "views": sorted({row["candidate"]["view_role"] for row in rows}),
            "run_dir": str(run_dir),
            "s3_prefix": manifest["s3"]["prefix"],
            "downloads": downloads,
            "exact_reference_blob_reuse": True,
            "no_fake_results": True,
            "done_rows_require_validated_local_image_bytes": True,
        },
        "sources": sources,
        "rows": projected_rows,
    }
    assert_sanitized(data)
    data_path = run_dir / "gallery/data.js"
    atomic_bytes(
        data_path,
        ("const GENERATION_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n").encode(),
    )
    artifacts: dict[str, dict[str, Any]] = {}
    for root in (run_dir / "gallery", run_dir / "assets", run_dir / "downloads"):
        for path in sorted(root.rglob("*")):
            if path.is_file():
                artifacts[str(path.relative_to(run_dir))] = {
                    "bytes": path.stat().st_size,
                    "sha256": sha256_path(path),
                }
    for path in sorted((run_dir / "images").glob("*")):
        if path.is_file():
            artifacts[str(path.relative_to(run_dir))] = {
                "bytes": path.stat().st_size,
                "sha256": sha256_path(path),
            }
    result = {
        "version": "hp-v5-top5-dual-generation-gallery-build-v1",
        "mode": data["metadata"]["mode"],
        "built_at_utc": data["metadata"]["built_at_utc"],
        "run_dir": str(run_dir),
        "row_count": EXPECTED_ROWS,
        "status_counts": status_counts,
        "image_generation_manifest_sha256": manifest_sha,
        "selection_hashes": {
            item["selection_type"]: item["sha256"] for item in manifest["selections"]
        },
        "reference_blob_bindings_sha256": binding_sha,
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
