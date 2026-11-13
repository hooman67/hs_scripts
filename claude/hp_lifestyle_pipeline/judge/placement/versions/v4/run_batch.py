# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests"]
# ///
"""Run or resume a bounded placement-judge V4 manifest batch."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

try:
    from .run_judge import judge
    from .scoring import validate_runtime_input
except ImportError:  # Direct script execution.
    from run_judge import judge  # type: ignore
    from scoring import validate_runtime_input  # type: ignore


ROOT = Path(__file__).resolve().parent
RUNS_ROOT = ROOT / "runs"
DEFAULT_MANIFEST = ROOT / "data/development_15_manifest.json"
RUN_NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*$")
RECORD_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
MAX_RUN_NAME_LENGTH = 64
MAX_WORKERS = 4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def manifest_records(payload: Any) -> list[Mapping[str, Any]]:
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, Mapping) and isinstance(payload.get("records"), list):
        records = payload["records"]
        expected_count = payload.get("expected_count")
        if expected_count is not None:
            if isinstance(expected_count, bool) or not isinstance(expected_count, int):
                raise ValueError("Manifest expected_count must be an integer")
            if expected_count < 0:
                raise ValueError("Manifest expected_count must not be negative")
            if len(records) != expected_count:
                raise ValueError(
                    f"Manifest expected_count is {expected_count}, but records has "
                    f"{len(records)} entries"
                )
    else:
        raise ValueError("Manifest must be a list or an object with a records list")
    if not all(isinstance(record, Mapping) for record in records):
        raise ValueError("Every manifest record must be a JSON object")
    return records


def validate_run_name(value: str) -> str:
    if len(value) > MAX_RUN_NAME_LENGTH or not RUN_NAME_RE.fullmatch(value):
        raise argparse.ArgumentTypeError(
            "run name must be 1-64 lowercase characters, start with a letter, and "
            "contain only alphanumerics separated by single '-' or '_' characters"
        )
    return value


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def required_string(record: Mapping[str, Any], key: str, record_id: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{record_id}: {key} must be a nonempty string")
    return value


def image_input(
    record: Mapping[str, Any], key: str, record_id: str
) -> tuple[Path, Mapping[str, Any]]:
    value = record.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"{record_id}: {key} must be an object")
    local_path = value.get("local_path")
    expected_hash = value.get("sha256")
    if not isinstance(local_path, str) or not local_path:
        raise ValueError(f"{record_id}: {key}.local_path must be a nonempty string")
    if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
        raise ValueError(f"{record_id}: {key}.sha256 must be lowercase SHA-256")
    path = Path(local_path)
    if not path.is_absolute():
        raise ValueError(f"{record_id}: {key}.local_path must be absolute")
    if not path.is_file():
        raise ValueError(f"{record_id}: missing {key} file: {path}")
    actual_hash = file_sha256(path)
    if actual_hash != expected_hash:
        raise ValueError(
            f"{record_id}: {key} SHA-256 mismatch: expected {expected_hash}, "
            f"found {actual_hash}"
        )
    hashes = record.get("hashes")
    if isinstance(hashes, Mapping):
        aggregate_key = f"{key}_sha256"
        aggregate_hash = hashes.get(aggregate_key)
        if aggregate_hash is not None and aggregate_hash != actual_hash:
            raise ValueError(f"{record_id}: hashes.{aggregate_key} disagrees with {key}")
    return path, value


def flatten_record(record: Mapping[str, Any]) -> tuple[str, dict[str, str]]:
    """Whitelist runtime inputs; annotations and diagnostic labels are never returned."""
    raw_id = record.get("id")
    if not isinstance(raw_id, str) or not RECORD_ID_RE.fullmatch(raw_id):
        raise ValueError(
            "record id must be 1-128 path-safe characters: letters, digits, '.', '_', '-'"
        )
    record_id = raw_id
    generated_path, _ = image_input(record, "generated_image", record_id)
    twin_path, _ = image_input(record, "twin_image", record_id)

    scene_prompt = record.get("scene_prompt")
    if not isinstance(scene_prompt, str):
        raise ValueError(f"{record_id}: scene_prompt must be a string")
    prompt_hash = text_sha256(scene_prompt)
    expected_prompt_hash = record.get("scene_prompt_sha256")
    if expected_prompt_hash != prompt_hash:
        raise ValueError(
            f"{record_id}: scene_prompt_sha256 mismatch: expected "
            f"{expected_prompt_hash!r}, found {prompt_hash}"
        )
    hashes = record.get("hashes")
    if isinstance(hashes, Mapping):
        aggregate_hash = hashes.get("scene_prompt_sha256")
        if aggregate_hash is not None and aggregate_hash != prompt_hash:
            raise ValueError(
                f"{record_id}: hashes.scene_prompt_sha256 disagrees with scene_prompt"
            )
    prompt_source = record.get("scene_prompt_source")
    if not isinstance(prompt_source, Mapping):
        raise ValueError(f"{record_id}: scene_prompt_source must be an object")
    if prompt_source.get("rewritten_prompt_included") is not False:
        raise ValueError(
            f"{record_id}: scene_prompt_source must explicitly exclude rewritten prompts"
        )

    runtime_input = {
        "generated_image": str(generated_path.resolve()),
        "twin_image": str(twin_path.resolve()),
        "product_type": record.get("device_type", record.get("product_type")),
        "scene_prompt": scene_prompt,
        "image_stage": required_string(record, "image_stage", record_id),
    }
    validate_runtime_input(runtime_input)
    return record_id, runtime_input


class ProgressLedger:
    def __init__(
        self,
        path: Path,
        *,
        manifest: Path,
        manifest_sha256: str,
        run_name: str,
        model: str,
        workers: int,
        limit: int | None,
        record_ids: list[str],
    ) -> None:
        self.path = path
        self.lock = threading.Lock()
        if path.exists():
            payload = load_json(path)
            immutable = {
                "manifest_sha256": manifest_sha256,
                "run_name": run_name,
                "model": model,
                "record_ids": record_ids,
            }
            for key, expected in immutable.items():
                if payload.get(key) != expected:
                    raise RuntimeError(
                        f"Existing progress ledger has different {key}; use a new run name"
                    )
            payload["workers"] = workers
            payload["limit"] = limit
            payload["resumed_at_utc"] = utc_now()
        else:
            payload = {
                "schema_version": "placement-v4-batch-progress-v1",
                "run_name": run_name,
                "manifest": str(manifest),
                "manifest_sha256": manifest_sha256,
                "model": model,
                "workers": workers,
                "limit": limit,
                "record_ids": record_ids,
                "started_at_utc": utc_now(),
                "updated_at_utc": utc_now(),
                "status": "pending",
                "items": {record_id: {"status": "pending"} for record_id in record_ids},
            }
        self.payload = payload
        self._write_locked()

    def _write_locked(self) -> None:
        self.payload["updated_at_utc"] = utc_now()
        statuses = [item["status"] for item in self.payload["items"].values()]
        self.payload["counts"] = {
            status: statuses.count(status) for status in sorted(set(statuses))
        }
        atomic_json(self.path, self.payload)

    def update(self, record_id: str, status: str, **fields: Any) -> None:
        with self.lock:
            item = self.payload["items"][record_id]
            item.clear()
            item.update({"status": status, **fields})
            self._write_locked()

    def finish(self, status: str) -> None:
        with self.lock:
            self.payload["status"] = status
            self.payload["finished_at_utc"] = utc_now()
            self._write_locked()


def parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(
        description="Run or resume placement-judge V4 records in a verified manifest"
    )
    argument_parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    argument_parser.add_argument("--run-name", type=validate_run_name, required=True)
    argument_parser.add_argument("--workers", type=positive_int, default=4)
    argument_parser.add_argument("--limit", type=positive_int)
    argument_parser.add_argument("--model", default="gpt-5.5")
    argument_parser.add_argument(
        "--validate-only",
        action="store_true",
        help="verify inputs without creating a run or calling a model",
    )
    return argument_parser


def main() -> int:
    args = parser().parse_args()
    if args.workers > MAX_WORKERS:
        raise SystemExit(f"--workers must not exceed {MAX_WORKERS}")
    if not isinstance(args.model, str) or not args.model.strip():
        raise SystemExit("--model must be nonempty")

    manifest_path = args.manifest.expanduser().resolve()
    if not manifest_path.is_file():
        raise SystemExit(f"Manifest does not exist: {manifest_path}")
    manifest_hash = file_sha256(manifest_path)
    records = manifest_records(load_json(manifest_path))
    if args.limit is not None:
        records = records[: args.limit]
    if not records:
        raise SystemExit("Selected manifest is empty")

    flattened: list[tuple[str, dict[str, str]]] = []
    seen_ids: set[str] = set()
    for record in records:
        record_id, runtime_input = flatten_record(record)
        if record_id in seen_ids:
            raise SystemExit(f"Duplicate record id: {record_id}")
        seen_ids.add(record_id)
        flattened.append((record_id, runtime_input))
    summary = {
        "manifest": str(manifest_path),
        "manifest_sha256": manifest_hash,
        "run_name": args.run_name,
        "model": args.model,
        "workers": args.workers,
        "limit": args.limit,
        "selected_records": len(flattened),
        "validated_records": len(flattened),
    }
    if args.validate_only:
        print(json.dumps({**summary, "model_calls": 0}, indent=2))
        return 0

    run_dir = RUNS_ROOT / args.run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    ledger = ProgressLedger(
        run_dir / "progress.json",
        manifest=manifest_path,
        manifest_sha256=manifest_hash,
        run_name=args.run_name,
        model=args.model,
        workers=args.workers,
        limit=args.limit,
        record_ids=[record_id for record_id, _ in flattened],
    )
    print_lock = threading.Lock()

    def run_one(record_id: str, runtime_input: dict[str, str]) -> tuple[str, str]:
        output_dir = run_dir / record_id
        result_path = output_dir / "result.json"
        cached_before = result_path.is_file()
        ledger.update(
            record_id,
            "running",
            started_at_utc=utc_now(),
            result_path=str(result_path),
            cached_before_start=cached_before,
        )
        try:
            result = judge(
                runtime_input,
                output_dir,
                model=args.model,
            )
            if not isinstance(result, Mapping) or result.get("status") != "ok":
                raise RuntimeError("judge returned a non-success result")
            final_status = "cached" if cached_before else "done"
            ledger.update(
                record_id,
                final_status,
                finished_at_utc=utc_now(),
                result_path=str(result_path),
                result_sha256=file_sha256(result_path),
            )
            with print_lock:
                print(json.dumps({"id": record_id, "status": final_status}), flush=True)
            return record_id, final_status
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            ledger.update(
                record_id,
                "error",
                finished_at_utc=utc_now(),
                result_path=str(result_path),
                error=error,
            )
            with print_lock:
                print(
                    json.dumps({"id": record_id, "status": "error", "error": error}),
                    flush=True,
                )
            return record_id, "error"

    statuses: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run_one, record_id, runtime_input): record_id
            for record_id, runtime_input in flattened
        }
        for future in as_completed(futures):
            _, status = future.result()
            statuses.append(status)

    failed = statuses.count("error")
    ledger.finish("complete" if failed == 0 else "completed_with_errors")
    print(
        json.dumps(
            {
                **summary,
                "done": statuses.count("done"),
                "cached": statuses.count("cached"),
                "errors": failed,
                "progress": str(run_dir / "progress.json"),
            },
            indent=2,
        )
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
