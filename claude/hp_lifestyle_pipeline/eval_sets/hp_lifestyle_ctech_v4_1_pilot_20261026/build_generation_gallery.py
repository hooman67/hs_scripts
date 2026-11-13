#!/usr/bin/env python3
"""Build a provenance-preserving progressive gallery for the V4.1 image run.

This builder is read-only with respect to generation records. It presents all
120 frozen prompts even before records exist, and only exposes output images
that are backed by a validated atomic ``done`` record.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any


EVAL_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = EVAL_ROOT.parents[1]
DEFAULT_RUN_DIR = PROJECT_ROOT / "local_data/generation_runs/hp_lifestyle_ctech_v4_1_pilot_20261026_corrected_twins_20261027"
MANIFEST_PATH = EVAL_ROOT / "image_generation_manifest.json"
PILOT_PATH = EVAL_ROOT / "pilot_prompts.json"
ACCEPTED_PATH = EVAL_ROOT / "accepted_prompt_cases.json"
SYSTEM_PROMPT_PATH = PROJECT_ROOT / "research/source_messaging_v1_to_v6/versions/v4.1/system_prompt.md"
INPUTS_DIR = EVAL_ROOT / "inputs"
TEMPLATE_DIR = EVAL_ROOT / "generation_gallery"
IMS_AUTH_PATH = PROJECT_ROOT / "eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/gallery/imsauth.js"
EXPECTED_PILOT_SHA256 = "1e99134ab8e1c1bab1f91eb74dc6d35b22b44c5a33d11b66566d84869957e57a"
EXPECTED_ACCEPTED_SHA256 = "c1300c01f001dc57a1a00e380399473ed70e8b38dfc9dd3e17d45d420b8c8173"
EXPECTED_ROWS = 120
EXPECTED_CASES = 4
EXPECTED_PER_CASE = 30
ALLOWED_RECORD_STATUSES = {"done", "pending", "failed"}
SENSITIVE_MARKERS = ("x-amz-signature=", "x-amz-credential=", "x-amz-security-token=")


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(value)
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())


def artifact_stem(row_id: str) -> str:
    readable = re.sub(r"[^A-Za-z0-9._-]+", "_", row_id).strip("_")[:90]
    return f"{sha256_bytes(row_id.encode())[:20]}__{readable}"


def require_exact_file(path: Path, expected_sha256: str, label: str) -> bytes:
    if not path.is_file():
        raise FileNotFoundError(f"{label} is missing: {path}")
    raw = path.read_bytes()
    actual = sha256_bytes(raw)
    if actual != expected_sha256:
        raise ValueError(f"{label} SHA-256 differs: {actual} != {expected_sha256}")
    return raw


def assert_sanitized(value: Any, location: str = "record") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            folded = key.casefold()
            if folded in {"authorization", "presignedurl", "x-gw-ims-user-token", "x-amz-security-token", "x-amz-credential", "x-amz-signature"}:
                raise ValueError(f"Sensitive field reached gallery at {location}.{key}")
            assert_sanitized(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_sanitized(child, f"{location}[{index}]")
    elif isinstance(value, str) and any(marker in value.casefold() for marker in SENSITIVE_MARKERS):
        raise ValueError(f"Presigned credential material reached gallery at {location}")


def load_frozen_inputs() -> tuple[dict[str, Any], str, dict[str, Any], str, dict[str, Any], str]:
    manifest_raw = MANIFEST_PATH.read_bytes()
    manifest = json.loads(manifest_raw)
    manifest_sha = sha256_bytes(manifest_raw)
    pilot_raw = require_exact_file(PILOT_PATH, EXPECTED_PILOT_SHA256, "pilot prompts")
    accepted_raw = require_exact_file(ACCEPTED_PATH, EXPECTED_ACCEPTED_SHA256, "accepted prompt cases")
    pilot, accepted = json.loads(pilot_raw), json.loads(accepted_raw)
    if manifest.get("status") != "authorized" or not manifest.get("authorized_at"):
        raise ValueError("Image generation manifest is not durably authorized")
    scope = manifest.get("scope") or {}
    if scope.get("image_generation_authorized") is not True or scope.get("expected_images") != EXPECTED_ROWS:
        raise ValueError("Image generation manifest does not authorize exactly 120 images")
    for name, expected_path, actual_sha in (
        ("pilot_prompts", PILOT_PATH, EXPECTED_PILOT_SHA256),
        ("accepted_prompt_cases", ACCEPTED_PATH, EXPECTED_ACCEPTED_SHA256),
    ):
        item = manifest.get(name) or {}
        if Path(item.get("path", "")).resolve() != expected_path.resolve() or item.get("sha256") != actual_sha:
            raise ValueError(f"Manifest {name} does not pin the current frozen input")
    if Path(manifest.get("run_dir", "")).resolve() != DEFAULT_RUN_DIR.resolve():
        raise ValueError("Manifest run_dir differs from the isolated V4.1 run directory")
    if pilot.get("prompt_count") != EXPECTED_ROWS or len(pilot.get("prompts") or []) != EXPECTED_ROWS:
        raise ValueError("Frozen pilot prompt inventory must contain exactly 120 rows")
    if len(manifest.get("renders") or []) != EXPECTED_CASES:
        raise ValueError("Image generation manifest must bind exactly four corrected inputs")
    return manifest, manifest_sha, pilot, EXPECTED_PILOT_SHA256, accepted, EXPECTED_ACCEPTED_SHA256


def validate_render(render: dict[str, Any]) -> tuple[Path, bytes]:
    required = {"render_id", "device_type", "camera_tag", "role", "path", "sha256", "bytes", "width", "height", "format"}
    missing = sorted(required - set(render))
    if missing:
        raise ValueError(f"Corrected render lacks fields: {missing}")
    source = Path(render["path"]).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Corrected render missing: {source}")
    raw = source.read_bytes()
    if len(raw) != render["bytes"] or sha256_bytes(raw) != render["sha256"]:
        raise ValueError(f"Corrected render bytes differ from manifest: {render['render_id']}")
    if render["format"].upper() != "PNG" or not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Corrected render is not an original PNG: {render['render_id']}")
    return source, raw


def copy_corrected_inputs(manifest: dict[str, Any], run_dir: Path) -> dict[str, dict[str, Any]]:
    destination_dir = run_dir / "assets/corrected_inputs"
    destination_dir.mkdir(parents=True, exist_ok=True)
    rendered: dict[str, dict[str, Any]] = {}
    intended_names: set[str] = set()
    for render in manifest["renders"]:
        source, raw = validate_render(render)
        filename = f"{render['render_id']}.png"
        if not re.fullmatch(r"[A-Za-z0-9._-]+\.png", filename):
            raise ValueError(f"Unsafe corrected-input filename: {filename}")
        destination = destination_dir / filename
        intended_names.add(filename)
        if not destination.exists() or destination.read_bytes() != raw:
            atomic_bytes(destination, raw)
        if sha256_path(destination) != render["sha256"]:
            raise ValueError(f"Gallery copy differs from endpoint input bytes: {render['render_id']}")
        rendered[render["camera_tag"]] = {
            **render,
            "source_path": str(source),
            "gallery_path": f"assets/corrected_inputs/{filename}",
            "gallery_copy_path": str(destination),
            "same_bytes_as_endpoint_input": True,
        }
    unexpected = sorted(path.name for path in destination_dir.iterdir() if path.is_file() and path.name not in intended_names)
    if unexpected:
        raise ValueError(f"Unowned corrected-input files in isolated run directory: {unexpected}")
    if len(rendered) != EXPECTED_CASES:
        raise ValueError("Corrected renders must have four unique camera tags")
    return rendered


def load_source_inputs(case_ids: set[str]) -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    for case_id in sorted(case_ids):
        path = INPUTS_DIR / f"{case_id}.json"
        value = read_json(path)
        if set(value) != {"source_messaging", "camera_tag"}:
            raise ValueError(f"Unexpected input envelope for {case_id}: {sorted(value)}")
        values[case_id] = value
    return values


def generation_rows(manifest: dict[str, Any], pilot: dict[str, Any], accepted: dict[str, Any], corrected: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    cases = accepted.get("cases") or {}
    rows: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    seen: set[str] = set()
    for candidate in pilot["prompts"]:
        case_id = candidate["case_id"]
        reviewed_case = cases.get(case_id)
        if not reviewed_case:
            raise ValueError(f"Missing reviewed case for {candidate['candidate_key']}")
        render = corrected.get(candidate["camera_tag"])
        if not render or render["device_type"] != candidate["device_type"]:
            raise ValueError(f"Corrected-input mapping differs for {candidate['candidate_key']}")
        candidate_id = candidate["reviewed_candidate_id"]
        if candidate["candidate_key"] != f"{case_id}::{candidate_id}":
            raise ValueError(f"Candidate identity differs: {candidate['candidate_key']}")
        selected = next((item for item in reviewed_case["candidates"] if item["candidate_key"] == candidate["candidate_key"]), None)
        if not selected or selected["text"] != candidate["text"] or selected["rank"] != candidate["rank"]:
            raise ValueError(f"Pilot/accepted candidate differs: {candidate['candidate_key']}")
        row_id = f"{case_id}__{candidate_id}__{render['render_id']}"
        if row_id in seen:
            raise ValueError(f"Duplicate row ID: {row_id}")
        seen.add(row_id)
        counts[case_id] = counts.get(case_id, 0) + 1
        rows.append({
            "row_id": row_id,
            "case_id": case_id,
            "group_id": reviewed_case["group_id"],
            "candidate_key": candidate["candidate_key"],
            "source_id": candidate["source_id"],
            "render_id": render["render_id"],
            "candidate_id": candidate_id,
            "device_type": candidate["device_type"],
            "camera_tag": candidate["camera_tag"],
            "candidate": candidate,
            "reviewed_case": reviewed_case,
            "corrected_input": render,
            "pilot_row_sha256": canonical_sha256(candidate),
            "candidate_text_sha256": sha256_bytes(candidate["text"].encode()),
        })
    if len(rows) != EXPECTED_ROWS or len(counts) != EXPECTED_CASES or set(counts.values()) != {EXPECTED_PER_CASE}:
        raise ValueError(f"Expected four 30-row cases, found {counts}")
    return sorted(rows, key=lambda item: item["row_id"])


def resolved_generated_image(record: dict[str, Any], run_dir: Path) -> dict[str, Any]:
    image = dict(record.get("generated_image") or {})
    required = {"path", "filename", "sha256", "bytes", "native_width", "native_height", "native_format", "content_type"}
    missing = sorted(required - set(image))
    if missing:
        raise ValueError(f"Done record generated_image lacks fields: {missing}")
    path = Path(image["path"]).resolve()
    images_root = (run_dir / "images").resolve()
    if path.parent != images_root or path.name != image["filename"]:
        raise ValueError(f"Done image is outside isolated images directory: {path}")
    if not path.is_file() or path.stat().st_size != image["bytes"] or sha256_path(path) != image["sha256"]:
        raise ValueError(f"Done image bytes differ from record: {path}")
    image["path"] = str(path)
    image["gallery_path"] = f"images/{path.name}"
    return image


def project_record(row: dict[str, Any], run_dir: Path) -> tuple[str, str, dict[str, Any] | None]:
    path = run_dir / "records" / f"{artifact_stem(row['row_id'])}.json"
    if not path.exists():
        return "pending", "not_started_no_record", None
    record = read_json(path)
    assert_sanitized(record)
    status = record.get("status")
    if status not in ALLOWED_RECORD_STATUSES:
        raise ValueError(f"Unknown record status for {row['row_id']}: {status}")
    for field in ("row_id", "case_id", "group_id", "candidate_key", "source_id", "render_id", "candidate_id", "device_type", "camera_tag"):
        if record.get(field) != row[field]:
            raise ValueError(f"Record identity differs for {row['row_id']} field {field}")
    payload = record.get("request_payload") or {}
    if payload.get("prompt") != row["candidate"]["text"]:
        raise ValueError(f"Record request prompt differs for {row['row_id']}")
    reference_blobs = payload.get("referenceBlobs") or []
    if len(reference_blobs) != 1:
        raise ValueError(f"Record must contain one corrected-input reference for {row['row_id']}")
    provenance = record.get("provenance") or {}
    if provenance.get("pilot_row_sha256") != row["pilot_row_sha256"] or provenance.get("candidate_text_sha256") != row["candidate_text_sha256"]:
        raise ValueError(f"Record prompt provenance differs for {row['row_id']}")
    binding = record.get("reference_binding")
    if binding and binding.get("original_png_sha256") != row["corrected_input"]["sha256"]:
        raise ValueError(f"Record reference bytes differ for {row['row_id']}")
    projected = dict(record)
    projected["record_path"] = str(path)
    projected["record_sha256"] = sha256_path(path)
    if status == "done":
        projected["generated_image"] = resolved_generated_image(record, run_dir)
        if "usedPrompt" not in record or "debugData" not in record:
            raise ValueError(f"Done record lacks endpoint rewrite/debug fields: {row['row_id']}")
    return status, str(record.get("failure_class") or record.get("job_status") or status), projected


def provenance_projection(row: dict[str, Any], manifest_sha: str, pilot_sha: str, accepted_sha: str) -> dict[str, Any]:
    candidate = row["candidate"]
    reviewed = row["reviewed_case"]
    return {
        "image_generation_manifest_path": str(MANIFEST_PATH.resolve()),
        "image_generation_manifest_sha256": manifest_sha,
        "pilot_prompts_path": str(PILOT_PATH.resolve()),
        "pilot_prompts_sha256": pilot_sha,
        "accepted_prompt_cases_path": str(ACCEPTED_PATH.resolve()),
        "accepted_prompt_cases_sha256": accepted_sha,
        "input_path": reviewed.get("input_path"),
        "input_sha256": reviewed.get("input_sha256"),
        "first_draw_raw_record_path": candidate.get("first_draw_raw_record_path"),
        "first_draw_raw_record_sha256": candidate.get("first_draw_raw_record_sha256"),
        "correction_provider_response_path": candidate.get("correction_provider_response_path"),
        "correction_provider_response_sha256": candidate.get("correction_provider_response_sha256"),
        "pilot_row_sha256": row["pilot_row_sha256"],
        "candidate_text_sha256": row["candidate_text_sha256"],
        "corrected_input_sha256": row["corrected_input"]["sha256"],
    }


def copy_gallery_inputs(run_dir: Path, manifest: dict[str, Any], source_inputs: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    gallery = run_dir / "gallery"
    gallery.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "main.js", "style.css"):
        shutil.copyfile(TEMPLATE_DIR / name, gallery / name)
    shutil.copyfile(IMS_AUTH_PATH, gallery / "imsauth.js")
    downloads = gallery / "downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    copies = [
        (PILOT_PATH, downloads / "pilot_prompts.json", "Frozen 120 prompts"),
        (SYSTEM_PROMPT_PATH, downloads / "system_prompt.md", "Prompt-authoring system prompt"),
        (MANIFEST_PATH, downloads / "image_generation_manifest.json", "Authorized image manifest"),
    ]
    result: list[dict[str, str]] = []
    for source, destination, label in copies:
        atomic_bytes(destination, source.read_bytes())
        result.append({"label": label, "path": f"./downloads/{destination.name}", "sha256": sha256_path(destination)})
    source_path = downloads / "source_inputs.json"
    atomic_json(source_path, {"version": "hp-ctech-v4.1-generation-source-inputs-v1", "inputs": source_inputs})
    result.append({"label": "Full source messaging + camera", "path": "./downloads/source_inputs.json", "sha256": sha256_path(source_path)})
    return result


def build(run_dir: Path, final: bool) -> dict[str, Any]:
    manifest, manifest_sha, pilot, pilot_sha, accepted, accepted_sha = load_frozen_inputs()
    if run_dir.resolve() != DEFAULT_RUN_DIR.resolve():
        raise ValueError(f"Only the isolated authorized run directory is allowed: {DEFAULT_RUN_DIR}")
    run_dir.mkdir(parents=True, exist_ok=True)
    corrected = copy_corrected_inputs(manifest, run_dir)
    base_rows = generation_rows(manifest, pilot, accepted, corrected)
    source_inputs = load_source_inputs({row["case_id"] for row in base_rows})
    downloads = copy_gallery_inputs(run_dir, manifest, source_inputs)
    projected_rows: list[dict[str, Any]] = []
    counts = {"done": 0, "pending": 0, "failed": 0}
    missing_record_count = 0
    for row in base_rows:
        status, reason, record = project_record(row, run_dir)
        counts[status] += 1
        if record is None:
            missing_record_count += 1
        projected_rows.append({
            **{key: row[key] for key in ("row_id", "case_id", "group_id", "candidate_key", "source_id", "render_id", "candidate_id", "device_type", "camera_tag")},
            "candidate": row["candidate"],
            "corrected_input": row["corrected_input"],
            "source_input": source_inputs[row["case_id"]],
            "provenance": provenance_projection(row, manifest_sha, pilot_sha, accepted_sha),
            "status": status,
            "status_reason": reason,
            "error": record.get("error") if record else None,
            "record": record,
        })
    if final and counts != {"done": EXPECTED_ROWS, "pending": 0, "failed": 0}:
        raise ValueError(f"Final gallery requires 120 validated done rows, found {counts}")
    environments = sorted({row["candidate"]["environment"] for row in projected_rows})
    if len(environments) != 6:
        raise ValueError(f"Expected the same six environment filters, found {environments}")
    data = {
        "metadata": {
            "version": "hp-ctech-v4.1-corrected-input-generation-gallery-v1",
            "mode": "final" if final else "progressive",
            "built_at_utc": utc_now(),
            "row_count": len(projected_rows),
            "case_count": len({row["case_id"] for row in projected_rows}),
            "corrected_input_count": len(corrected),
            "status_counts": counts,
            "missing_record_count": missing_record_count,
            "environments": environments,
            "devices": sorted({row["device_type"] for row in projected_rows}),
            "views": sorted({row["candidate"]["view_role"] for row in projected_rows}),
            "image_generation_manifest_sha256": manifest_sha,
            "pilot_prompts_sha256": pilot_sha,
            "accepted_prompt_cases_sha256": accepted_sha,
            "run_dir": str(run_dir),
            "downloads": downloads,
            "no_fake_results": True,
            "done_rows_require_validated_local_image_bytes": True,
            "corrected_gallery_inputs_match_endpoint_input_bytes": True,
        },
        "rows": projected_rows,
    }
    data_path = run_dir / "gallery/data.js"
    atomic_bytes(data_path, ("const GENERATION_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n").encode())
    artifacts = {}
    for path in sorted((run_dir / "gallery").rglob("*")):
        if path.is_file():
            artifacts[str(path.relative_to(run_dir))] = {"bytes": path.stat().st_size, "sha256": sha256_path(path)}
    build_record = {
        "version": "hp-ctech-v4.1-generation-gallery-build-v1",
        "mode": data["metadata"]["mode"],
        "built_at_utc": data["metadata"]["built_at_utc"],
        "run_dir": str(run_dir),
        "row_count": EXPECTED_ROWS,
        "status_counts": counts,
        "missing_record_count": missing_record_count,
        "image_generation_manifest_sha256": manifest_sha,
        "pilot_prompts_sha256": pilot_sha,
        "accepted_prompt_cases_sha256": accepted_sha,
        "corrected_input_hashes": {tag: value["sha256"] for tag, value in sorted(corrected.items())},
        "artifacts": artifacts,
    }
    atomic_json(run_dir / "generation_gallery_build.json", build_record)
    return build_record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--final", action="store_true", help="Require exactly 120 validated done rows")
    args = parser.parse_args()
    result = build(args.run_dir, args.final)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
