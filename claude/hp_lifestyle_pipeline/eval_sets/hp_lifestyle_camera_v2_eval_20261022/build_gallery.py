#!/usr/bin/env python3
"""Build the progressive/final camera-V2 image gallery from durable artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image


EVAL_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = EVAL_ROOT.parents[1]
MANIFEST_PATH = EVAL_ROOT / "manifest.json"
ACCEPTED_PATH = EVAL_ROOT / "accepted_prompt_cases.json"
TEMPLATE_DIR = EVAL_ROOT / "gallery"
DEFAULT_RUN_DIR = (
    PROJECT_ROOT
    / "local_data/generation_runs/hp_lifestyle_camera_v2_eval_20261022"
)
SHARED_IMS_AUTH = (
    PROJECT_ROOT
    / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/imsauth.js"
)
SECRET_PATTERNS = (
    re.compile(r"AWS_SECRET_ACCESS_KEY", re.I),
    re.compile(r"AWS_SESSION_TOKEN", re.I),
    re.compile(r"X-Amz-Signature", re.I),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r'"authorization"\s*:', re.I),
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json_bytes(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    return json.loads(raw), raw


def atomic_write(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(value)
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_write(
        path,
        (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )


def validate_file(path: Path, expected_sha: str, expected_bytes: int | None = None) -> bytes:
    raw = path.read_bytes()
    if expected_bytes is not None and len(raw) != expected_bytes:
        raise ValueError(f"Byte count mismatch: {path}")
    if sha256_bytes(raw) != expected_sha:
        raise ValueError(f"SHA-256 mismatch: {path}")
    return raw


def index_unique(items: list[dict[str, Any]], field: str) -> dict[str, dict[str, Any]]:
    result = {}
    for item in items:
        key = item.get(field)
        if not isinstance(key, str) or not key or key in result:
            raise ValueError(f"Invalid or duplicate {field}: {key!r}")
        result[key] = item
    return result


def load_records(run_dir: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / "records").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        row_id = record.get("row_id")
        if not isinstance(row_id, str) or not row_id:
            raise ValueError(f"Generation record has no row_id: {path}")
        if row_id in records:
            raise ValueError(f"Duplicate generation record row_id: {row_id}")
        if record.get("status") not in {"done", "pending", "failed"}:
            raise ValueError(f"Unknown generation status in {path}: {record.get('status')}")
        records[row_id] = record
    return records


def validate_generated_record(
    record: dict[str, Any], render: dict[str, Any], run_dir: Path
) -> None:
    for field in ("render_id", "device_type", "camera_tag"):
        if record.get(field) != render.get(field):
            raise ValueError(
                f"Generated record differs from manifest for {field}: {record['row_id']}"
            )
    if record["status"] != "done":
        return
    current = record.get("current_render") or {}
    binding = record.get("reference_binding") or {}
    if current.get("sha256") != render["sha256"]:
        raise ValueError(f"Current render hash mismatch: {record['row_id']}")
    if binding.get("original_png_sha256") != render["sha256"]:
        raise ValueError(f"Reference binding hash mismatch: {record['row_id']}")
    image = record.get("generated_image") or {}
    path = Path(image.get("path", ""))
    if not path.is_absolute():
        path = (run_dir / path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Generated image missing: {path}")
    raw = validate_file(path, image["sha256"], image["bytes"])
    with Image.open(path) as opened:
        if opened.size != (image["native_width"], image["native_height"]):
            raise ValueError(f"Generated native dimensions mismatch: {record['row_id']}")
    if Path(image["filename"]).name != image["filename"]:
        raise ValueError(f"Generated image filename is not flat: {record['row_id']}")
    destination = run_dir / "images" / image["filename"]
    if destination.resolve() != path.resolve():
        if destination.exists() and destination.read_bytes() != raw:
            raise ValueError(f"Generated image destination collision: {destination}")
        if not destination.exists():
            atomic_write(destination, raw)


def copy_reference_assets(
    renders: dict[str, dict[str, Any]], run_dir: Path, manifest_sha: str
) -> dict[str, Any]:
    assets_dir = run_dir / "assets/references"
    assets_dir.mkdir(parents=True, exist_ok=True)
    output: dict[str, Any] = {}
    for render_id, render in sorted(renders.items()):
        if render["device_type"] not in {"laptop", "printer"}:
            raise ValueError(f"Excluded device type in render manifest: {render_id}")
        source = Path(render["path"])
        raw = validate_file(source, render["sha256"], render["bytes"])
        if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError(f"Reference is not PNG: {source}")
        with Image.open(source) as opened:
            if opened.size != (render["width"], render["height"]):
                raise ValueError(f"Reference dimensions mismatch: {render_id}")
        filename = f"{render_id}.png"
        destination = assets_dir / filename
        if destination.exists():
            validate_file(destination, render["sha256"], render["bytes"])
        else:
            atomic_write(destination, raw)
        output[render_id] = {
            "render_id": render_id,
            "asset_filename": filename,
            "source_path": str(source.resolve()),
            "source_sha256": render["sha256"],
            "published_bytes_sha256": sha256_path(destination),
            "bytes": len(raw),
            "width": render["width"],
            "height": render["height"],
            "content_type": "image/png",
        }
    document = {
        "version": "camera-v2-reference-assets-v1",
        "manifest_sha256": manifest_sha,
        "asset_count": len(output),
        "total_bytes": sum(item["bytes"] for item in output.values()),
        "assets": output,
    }
    atomic_json(run_dir / "reference_assets.json", document)
    return document


def prompt_key(case_id: str, prompt_id: str) -> str:
    return f"{case_id}__{prompt_id}"


def build_data(run_dir: Path, final: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest, manifest_raw = read_json_bytes(MANIFEST_PATH)
    accepted, accepted_raw = read_json_bytes(ACCEPTED_PATH)
    manifest_sha = sha256_bytes(manifest_raw)
    accepted_sha = sha256_bytes(accepted_raw)
    if accepted.get("manifest_sha256") != manifest_sha:
        raise ValueError("Accepted prompt cases target a different manifest")
    if manifest["counts"]["included_render_count"] != 202:
        raise ValueError("Manifest must contain 202 included renders")
    if manifest["counts"]["excluded_minipc_render_count"] != 41:
        raise ValueError("Manifest must explicitly exclude 41 miniPC renders")

    sources = index_unique(manifest["sources"], "source_id")
    renders = index_unique(manifest["renders"], "render_id")
    cases = index_unique(manifest["cases"], "case_id")
    accepted_cases = accepted.get("cases", {})
    if not isinstance(accepted_cases, dict):
        raise ValueError("accepted_prompt_cases.cases must be an object")
    unknown_accepted = sorted(set(accepted_cases) - set(cases))
    if unknown_accepted:
        raise ValueError(f"Accepted prompt map has unknown cases: {unknown_accepted}")

    source_values: dict[str, Any] = {}
    for source_id, source in sources.items():
        path = Path(source["source_json_path"])
        raw = validate_file(path, source["sha256"], source["bytes"])
        source_values[source_id] = json.loads(raw)

    reference_manifest = copy_reference_assets(renders, run_dir, manifest_sha)
    records = load_records(run_dir)
    summary_path = run_dir / "summary.json"
    runner_summary = (
        json.loads(summary_path.read_text(encoding="utf-8"))
        if summary_path.is_file()
        else {}
    )

    case_data: dict[str, Any] = {}
    prompts: dict[str, Any] = {}
    rows: list[dict[str, Any]] = []
    expected_row_ids: set[str] = set()
    accepted_count = 0
    pending_count = 0
    placeholder_count = 0

    for case_id, case in cases.items():
        source_id = case["source_id"]
        input_path = Path(case["input_path"])
        input_raw = validate_file(input_path, case["input_sha256"])
        wrapper = json.loads(input_raw)
        expected_wrapper_keys = {"source_messaging", "camera_tag"}
        if set(wrapper) != expected_wrapper_keys:
            raise ValueError(f"Runtime input has unexpected fields: {case_id}")
        if wrapper["source_messaging"] != source_values[source_id]:
            raise ValueError(f"Runtime input source differs from canonical source: {case_id}")
        if wrapper["camera_tag"] != case["camera_tag"]:
            raise ValueError(f"Runtime input camera differs from manifest: {case_id}")
        entry = accepted_cases.get(case_id)
        status = entry.get("status") if entry else "pending"
        launchable = bool(entry and entry.get("status") == "accepted" and entry.get("launchable") is True)
        if launchable:
            accepted_count += 1
        else:
            pending_count += 1
        case_data[case_id] = {
            "manifest": case,
            "input": {
                "camera_tag": wrapper["camera_tag"],
                "source_messaging_ref": source_id,
                "input_path": str(input_path.resolve()),
                "input_sha256": case["input_sha256"],
            },
            "source": sources[source_id],
            "accepted": entry,
            "prompt_status": status,
        }

        if launchable:
            for field in (
                "case_id", "source_id", "device_type", "camera_tag", "input_path",
                "input_sha256", "render_ids",
            ):
                if entry.get(field) != case.get(field):
                    raise ValueError(f"Accepted case differs from manifest: {case_id}/{field}")
            if not entry.get("prompts"):
                raise ValueError(f"Accepted launchable case has no prompts: {case_id}")
            for prompt in entry["prompts"]:
                if sha256_bytes(prompt["text"].encode("utf-8")) != prompt["text_sha256"]:
                    raise ValueError(f"Accepted prompt text hash mismatch: {case_id}")
                key = prompt_key(case_id, prompt["prompt_id"])
                if key in prompts:
                    raise ValueError(f"Duplicate prompt key: {key}")
                prompts[key] = {
                    **prompt,
                    "case_id": case_id,
                    "source_id": source_id,
                    "device_type": case["device_type"],
                    "camera_tag": case["camera_tag"],
                }
                for render_id in case["render_ids"]:
                    row_id = f"{case_id}__{render_id}__{prompt['prompt_id']}"
                    expected_row_ids.add(row_id)
                    record = records.get(row_id)
                    if record:
                        if record.get("case_id") != case_id or record.get("prompt_id") != prompt["prompt_id"]:
                            raise ValueError(f"Generation record join mismatch: {row_id}")
                        validate_generated_record(record, renders[render_id], run_dir)
                        row_status = record["status"]
                    else:
                        row_status = "missing" if final else "generation_pending"
                    rows.append({
                        "row_id": row_id,
                        "case_id": case_id,
                        "source_id": source_id,
                        "render_id": render_id,
                        "prompt_id": prompt["prompt_id"],
                        "prompt_key": key,
                        "device_type": case["device_type"],
                        "camera_tag": case["camera_tag"],
                        "status": row_status,
                        "result": record,
                    })
        else:
            placeholder_status = (
                "prompt_pending"
                if entry is None or status in {"pending", "running", "manual_review"}
                else "prompt_failed"
            )
            for render_id in case["render_ids"]:
                placeholder_count += 1
                rows.append({
                    "row_id": f"{case_id}__{render_id}__prompt_pending",
                    "case_id": case_id,
                    "source_id": source_id,
                    "render_id": render_id,
                    "prompt_id": None,
                    "prompt_key": None,
                    "device_type": case["device_type"],
                    "camera_tag": case["camera_tag"],
                    "status": placeholder_status,
                    "result": None,
                })

    unexpected_records = sorted(set(records) - expected_row_ids)
    status_counts = Counter(row["status"] for row in rows)
    prompt_case_set_complete = (
        accepted_count == len(cases)
        and len(accepted_cases) == len(cases)
        and accepted.get("status") in {"complete", "accepted_complete"}
    )
    if final:
        if not prompt_case_set_complete:
            raise ValueError("Final gallery requires all prompt cases accepted and launchable")
        if placeholder_count:
            raise ValueError("Final gallery cannot contain prompt placeholders")
        if unexpected_records:
            raise ValueError(f"Final gallery has unexpected generation records: {unexpected_records}")
        incomplete = [row["row_id"] for row in rows if row["status"] in {"missing", "pending", "generation_pending"}]
        if incomplete:
            raise ValueError(f"Final gallery has {len(incomplete)} incomplete generation rows")

    system_prompt_path = Path(manifest["provenance"]["system_prompt_path"])
    system_prompt_raw = validate_file(
        system_prompt_path, manifest["provenance"]["system_prompt_sha256"]
    )
    input_schema_path = Path(manifest["provenance"]["input_schema_path"])
    output_schema_path = Path(manifest["provenance"]["output_schema_path"])
    input_schema_raw = validate_file(
        input_schema_path, manifest["provenance"]["input_schema_sha256"]
    )
    output_schema_raw = validate_file(
        output_schema_path, manifest["provenance"]["output_schema_sha256"]
    )
    for render_id, render in renders.items():
        render["reference_asset_filename"] = reference_manifest["assets"][render_id]["asset_filename"]

    build_metadata = {
        "version": "camera-v2-generated-gallery-v1",
        "mode": "final" if final else "progressive",
        "manifest_sha256": manifest_sha,
        "accepted_prompt_cases_sha256": accepted_sha,
        "manifest_case_count": len(cases),
        "accepted_case_count": accepted_count,
        "pending_case_count": pending_count,
        "prompt_case_set_complete": prompt_case_set_complete,
        "source_render_pair_count": manifest["counts"]["source_render_pair_count"],
        "planned_generation_row_count": len(expected_row_ids),
        "placeholder_row_count": placeholder_count,
        "display_row_object_count": len(rows),
        "generation_record_count": len(records),
        "status_counts": dict(sorted(status_counts.items())),
        "unexpected_record_ids": unexpected_records,
        "reference_asset_count": reference_manifest["asset_count"],
        "reference_asset_bytes": reference_manifest["total_bytes"],
    }
    run_context = {
        "gallery_build": build_metadata,
        "manifest": {
            "path": str(MANIFEST_PATH.resolve()),
            "sha256": manifest_sha,
            "version": manifest.get("version"),
            "status": manifest.get("status"),
            "scope": manifest.get("scope"),
            "counts": manifest.get("counts"),
            "join_contract": manifest.get("join_contract"),
            "provenance": manifest.get("provenance"),
        },
        "accepted_prompt_cases": {
            key: value for key, value in accepted.items() if key != "cases"
        },
        "runner_summary": runner_summary,
        "model_settings": manifest.get("model"),
        "system_prompt": system_prompt_raw.decode("utf-8"),
        "input_schema": json.loads(input_schema_raw),
        "output_schema": json.loads(output_schema_raw),
    }
    data = {
        "metadata": build_metadata,
        "run_context": run_context,
        "sources": source_values,
        "renders": renders,
        "cases": case_data,
        "prompts": prompts,
        "rows": rows,
    }
    return data, build_metadata


def assert_no_credentials(value: str, label: str) -> None:
    hits = [pattern.pattern for pattern in SECRET_PATTERNS if pattern.search(value)]
    if hits:
        raise ValueError(f"Credential-like content found in {label}: {hits}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()

    data, metadata = build_data(args.run_dir, args.final)
    gallery_dir = args.run_dir / "gallery"
    gallery_dir.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "style.css", "main.js"):
        raw = (TEMPLATE_DIR / name).read_bytes()
        atomic_write(gallery_dir / name, raw)
    ims_raw = SHARED_IMS_AUTH.read_bytes()
    if sha256_bytes(ims_raw) != "269ec81678b5cffb043d80a1340aa05ca5d2c24ea96396f0f97d690ddb772a1a":
        raise ValueError("Shared IMS auth asset changed unexpectedly")
    atomic_write(gallery_dir / "imsauth.js", ims_raw)
    data_text = "const EVAL_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
    assert_no_credentials(data_text, "gallery data")
    atomic_write(gallery_dir / "data.js", data_text.encode("utf-8"))

    artifacts = {}
    for path in sorted(gallery_dir.iterdir()):
        if path.is_file():
            artifacts[path.name] = {
                "path": str(path.resolve()),
                "bytes": path.stat().st_size,
                "sha256": sha256_path(path),
            }
    build_record = {
        **metadata,
        "run_dir": str(args.run_dir.resolve()),
        "gallery_dir": str(gallery_dir.resolve()),
        "artifacts": artifacts,
        "model_called_by_builder": False,
        "image_generation_called_by_builder": False,
    }
    atomic_json(args.run_dir / "gallery_build.json", build_record)
    print(json.dumps(build_record, indent=2))


if __name__ == "__main__":
    main()
