# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests", "pillow>=10"]
# ///
"""Run a new, immutable spatial-crop experiment batch."""

from __future__ import annotations

import argparse
import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from run_spatial_crops import (
    CROP_ROOT,
    ROOT,
    V3_ROOT,
    _load_module,
    atomic_json,
    ensure_frozen,
    judge,
    sha256_path,
)


CANONICAL_BATCH = _load_module(
    "placement_v3_spatial_canonical_batch", V3_ROOT / "run_batch.py"
)
RUNS_ROOT = ROOT / "runs"
MAX_WORKERS = 4
RUN_NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*$")
FORBIDDEN_TARGET_LABEL_KEYS = frozenset(
    {
        "annotations",
        "diagnostic_expectation",
        "diagnostic_label",
        "human_feedback",
        "human_label",
        "regression_expectation",
        "target_annotations",
        "target_label",
    }
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_run_name(value: str) -> str:
    if len(value) > 64 or not RUN_NAME_RE.fullmatch(value):
        raise argparse.ArgumentTypeError(
            "run name must be 1-64 lowercase characters, start with a letter, and "
            "contain only alphanumerics separated by single '-' or '_' characters"
        )
    return value


def positive_int(value: str) -> int:
    try:
        result = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be an integer") from error
    if result < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return result


def label_key_paths(value: Any, path: str = "$") -> list[str]:
    """Return exact forbidden label-key paths without inspecting free text."""
    found: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_TARGET_LABEL_KEYS:
                found.append(child_path)
            found.extend(label_key_paths(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(label_key_paths(child, f"{path}[{index}]"))
    return found


def validate_manifest_separation(payload: Any) -> tuple[str, list[str]]:
    if not isinstance(payload, Mapping):
        raise ValueError("Experiment manifest must be an object")
    forbidden = label_key_paths(payload)
    if payload.get("dataset_role") == "evaluation_target_unlabeled":
        if forbidden:
            raise ValueError("Unlabeled target has forbidden label keys: " + ", ".join(forbidden))
        separation = payload.get("separation_from_training")
        if not isinstance(separation, Mapping):
            raise ValueError("Unlabeled target must document separation_from_training")
        if separation.get("target_contains_human_feedback") is not False:
            raise ValueError("Unlabeled target must explicitly have no human feedback")
        if separation.get("target_contains_diagnostic_expectations") is not False:
            raise ValueError("Unlabeled target must explicitly have no diagnostic expectations")
        return "evaluation_target_unlabeled", forbidden

    contract = payload.get("input_contract")
    if not isinstance(contract, Mapping) or contract.get("annotations_passed_to_judge") is not False:
        raise ValueError(
            "Diagnostic manifest must explicitly set input_contract.annotations_passed_to_judge=false"
        )
    return "diagnostic_regression_labels_source_only", forbidden


def validated_records(payload: Any) -> list[tuple[str, dict[str, str]]]:
    manifest_kind, _ = validate_manifest_separation(payload)
    records = CANONICAL_BATCH.manifest_records(payload)
    if not records:
        raise ValueError("Manifest records must not be empty")
    flattened: list[tuple[str, dict[str, str]]] = []
    seen: set[str] = set()
    for record in records:
        if manifest_kind == "evaluation_target_unlabeled":
            if record.get("dataset_role") != "evaluation_target_unlabeled":
                raise ValueError(
                    f"{record.get('id', '<unknown>')}: dataset_role must be "
                    "evaluation_target_unlabeled"
                )
            provenance = record.get("label_provenance")
            if not isinstance(provenance, Mapping):
                raise ValueError(f"{record.get('id', '<unknown>')}: missing label_provenance")
            required_false = (
                "human_annotations_included",
                "diagnostic_expectations_included",
                "passed_to_judge",
            )
            if any(provenance.get(key) is not False for key in required_false):
                raise ValueError(
                    f"{record.get('id', '<unknown>')}: label_provenance must explicitly "
                    "exclude annotations, expectations and judge inputs"
                )
        record_id, runtime_input = CANONICAL_BATCH.flatten_record(record)
        if set(runtime_input) != {
            "generated_image",
            "twin_image",
            "product_type",
            "scene_prompt",
            "image_stage",
        }:
            raise ValueError(f"{record_id}: canonical runtime whitelist changed")
        if record_id in seen:
            raise ValueError(f"Duplicate record id: {record_id}")
        seen.add(record_id)
        flattened.append((record_id, runtime_input))
    return flattened


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Run the isolated V3 spatial-crop placement experiment"
    )
    result.add_argument("--manifest", type=Path, required=True)
    result.add_argument("--run-name", type=validate_run_name, required=True)
    result.add_argument("--model", default="gpt-5.5")
    result.add_argument("--workers", type=positive_int, default=4)
    result.add_argument(
        "--validate-only",
        action="store_true",
        help="verify the freeze and all target inputs without creating files or calling a model",
    )
    return result


def main() -> int:
    args = parser().parse_args()
    if args.workers > MAX_WORKERS:
        raise SystemExit(f"--workers must not exceed {MAX_WORKERS}")
    if not isinstance(args.model, str) or not args.model.strip():
        raise SystemExit("--model must be nonempty")

    # This is deliberately before run-directory creation and before any worker
    # can make an API call.
    frozen = ensure_frozen()
    manifest_path = args.manifest.expanduser().resolve()
    if not manifest_path.is_file():
        raise SystemExit(f"Manifest does not exist: {manifest_path}")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_kind, source_label_paths = validate_manifest_separation(payload)
    records = validated_records(payload)
    manifest_hash = sha256_path(manifest_path)
    summary = {
        "protocol_version": frozen["protocol_version"],
        "protocol_freeze_sha256": sha256_path(ROOT / "freeze.json"),
        "manifest": str(manifest_path),
        "manifest_sha256": manifest_hash,
        "run_name": args.run_name,
        "model": args.model,
        "workers": args.workers,
        "validated_records": len(records),
        "manifest_kind": manifest_kind,
        "source_label_fields_present": len(source_label_paths),
        "target_label_fields_passed_to_model": 0,
    }
    if args.validate_only:
        print(json.dumps({**summary, "model_calls": 0}, indent=2))
        return 0

    run_dir = RUNS_ROOT / args.run_name
    crop_run_dir = CROP_ROOT / args.run_name
    if run_dir.exists() or crop_run_dir.exists():
        raise SystemExit(
            "Run output already exists; choose a new --run-name: "
            f"{run_dir} or {crop_run_dir}"
        )
    run_dir.mkdir(parents=True)
    crop_run_dir.mkdir(parents=True)
    progress_path = run_dir / "progress.json"
    progress: dict[str, Any] = {
        "schema_version": "placement-v3-spatial-crops-batch-v1",
        **summary,
        "started_at_utc": utc_now(),
        "status": "running",
        "records": {record_id: {"status": "pending"} for record_id, _ in records},
    }
    lock = threading.Lock()

    def save_progress() -> None:
        progress["updated_at_utc"] = utc_now()
        atomic_json(progress_path, progress)

    def update(record_id: str, status: str, **fields: Any) -> None:
        with lock:
            progress["records"][record_id] = {"status": status, **fields}
            save_progress()

    save_progress()

    def run_one(record_id: str, runtime_input: dict[str, str]) -> str:
        output_dir = run_dir / record_id
        crop_dir = crop_run_dir / record_id
        update(record_id, "running", started_at_utc=utc_now())
        try:
            result = judge(
                runtime_input,
                output_dir,
                crop_dir,
                model=args.model,
            )
            if result.get("ok") is not True:
                raise RuntimeError(
                    f"judge failed with {result.get('error_type', 'unknown error')}"
                )
            result_path = output_dir / "result.json"
            update(
                record_id,
                "done",
                finished_at_utc=utc_now(),
                result_path=str(result_path),
                result_sha256=sha256_path(result_path),
                crop_manifest_path=str(crop_dir / "crop_manifest.json"),
                crop_manifest_sha256=sha256_path(crop_dir / "crop_manifest.json"),
            )
            return "done"
        except Exception as error:
            update(
                record_id,
                "error",
                finished_at_utc=utc_now(),
                error_type=type(error).__name__,
                error=str(error),
            )
            return "error"

    statuses: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(run_one, record_id, runtime_input)
            for record_id, runtime_input in records
        ]
        for future in as_completed(futures):
            statuses.append(future.result())

    with lock:
        progress["status"] = "complete" if "error" not in statuses else "completed_with_errors"
        progress["finished_at_utc"] = utc_now()
        progress["counts"] = {
            "done": statuses.count("done"),
            "error": statuses.count("error"),
        }
        save_progress()
    print(json.dumps({**summary, **progress["counts"], "progress": str(progress_path)}, indent=2))
    return 1 if "error" in statuses else 0


if __name__ == "__main__":
    raise SystemExit(main())
