#!/usr/bin/env python3
"""Validate, run, or resume the frozen V4.3.1 judge on original V6.1 rows.

Validation is read-only. Live execution additionally requires the explicit
``--acknowledge-launch-authorized`` flag so preparation cannot accidentally
call the model. Per-row raw responses and request evidence are written by the
frozen V4.3.1 runner beneath each record directory.
"""

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

HERE = Path(__file__).resolve().parent
VERSION_ROOT = HERE.parent
DEFAULT_MANIFEST = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/"
    "judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json"
)
DEFAULT_FREEZE = HERE / "protocol_freeze.json"
EXPECTED_MANIFEST_SHA256 = "fd84149fa421c32602358c325b4fb14ed555d3e5033fb92bc2800ab37e6daefc"
MODEL = "gpt-5.5"
MAX_WORKERS = 2
RECORD_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise ValueError(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_freeze(path: Path, manifest_path: Path) -> Mapping[str, Any]:
    freeze = load_json(path)
    require(freeze.get("schema_version") == "hp-placement-v4.3.1-full160-freeze-v1", "freeze schema differs")
    require(freeze.get("status") == "prepared_not_launched", "freeze status differs")
    require(freeze.get("model", {}).get("requested") == MODEL, "frozen model differs")
    require(freeze.get("model", {}).get("concurrency_default") == 2, "frozen default concurrency differs")
    manifest = freeze.get("manifest")
    require(isinstance(manifest, Mapping), "freeze manifest section missing")
    require(Path(str(manifest.get("path", ""))).resolve() == manifest_path, "frozen manifest path differs")
    require(manifest.get("sha256") == sha256(manifest_path), "frozen manifest hash differs")
    files = freeze.get("files")
    require(isinstance(files, Mapping), "freeze files map missing")
    for relative, expected in files.items():
        source = VERSION_ROOT / str(relative)
        require(source.is_file(), f"frozen source missing: {source}")
        require(sha256(source) == expected, f"frozen source hash differs: {source}")
    local_files = freeze.get("batch_files")
    require(isinstance(local_files, Mapping), "freeze batch files map missing")
    for name, expected in local_files.items():
        source = HERE / str(name)
        require(source.is_file(), f"frozen batch file missing: {source}")
        require(sha256(source) == expected, f"frozen batch file hash differs: {source}")
    return freeze


def validate_manifest(path: Path) -> list[Mapping[str, Any]]:
    require(sha256(path) == EXPECTED_MANIFEST_SHA256, "manifest SHA-256 differs from verified V6.1 snapshot")
    payload = load_json(path)
    require(isinstance(payload, Mapping), "manifest must be an object")
    records = payload.get("records")
    require(payload.get("expected_count") == 160, "manifest expected_count must be 160")
    require(isinstance(records, list) and len(records) == 160, "manifest must contain 160 records")
    require(all(isinstance(row, Mapping) for row in records), "manifest record is not an object")
    ids = [row.get("id") for row in records]
    require(all(isinstance(value, str) and RECORD_ID.fullmatch(value) for value in ids), "manifest has invalid record IDs")
    require(len(ids) == len(set(ids)), "manifest has duplicate IDs")
    return records


def runtime_input(record: Mapping[str, Any]) -> dict[str, Any]:
    record_id = str(record["id"])
    require(record.get("image_stage") == "scene_generation", f"{record_id}: stage must be scene_generation")
    product_type = record.get("device_type")
    require(product_type in {"laptop", "printer"}, f"{record_id}: product type differs")
    generated = record.get("generated_image")
    twin = record.get("twin_image")
    require(isinstance(generated, Mapping) and isinstance(twin, Mapping), f"{record_id}: image records missing")
    generated_path = Path(str(generated.get("local_path", ""))).resolve()
    twin_path = Path(str(twin.get("local_path", ""))).resolve()
    require(generated_path.is_file(), f"{record_id}: generated image missing: {generated_path}")
    require(twin_path.is_file(), f"{record_id}: twin image missing: {twin_path}")
    hashes = record.get("hashes")
    require(isinstance(hashes, Mapping), f"{record_id}: hashes map missing")
    require(sha256(generated_path) == generated.get("sha256") == hashes.get("generated_image_sha256"), f"{record_id}: generated hash differs")
    require(sha256(twin_path) == twin.get("sha256") == hashes.get("twin_image_sha256"), f"{record_id}: twin hash differs")
    prompt = record.get("scene_prompt")
    require(isinstance(prompt, str), f"{record_id}: prompt is not text")
    require(text_sha256(prompt) == record.get("scene_prompt_sha256") == hashes.get("scene_prompt_sha256"), f"{record_id}: prompt hash differs")
    source = record.get("scene_prompt_source")
    require(isinstance(source, Mapping) and source.get("rewritten_prompt_included") is False, f"{record_id}: prompt-source contract differs")
    rank = source.get("bank_rank")
    camera = record.get("view", {}).get("camera_tag") if isinstance(record.get("view"), Mapping) else None
    device = record.get("device")
    require(isinstance(rank, int) and 1 <= rank <= 10, f"{record_id}: bad rank")
    require(isinstance(camera, str) and camera and isinstance(device, str) and device, f"{record_id}: audit metadata missing")
    return {
        "generated_image": str(generated_path),
        "twin_image": str(twin_path),
        "product_type": product_type,
        "scene_prompt": prompt,
        "target_record_id": record_id,
        "device": device,
        "camera": camera,
        "prompt_rank": rank,
    }


def expected_input_fingerprint(runtime: Mapping[str, Any]) -> str:
    identity = {
        "generated_byte_sha256": sha256(Path(str(runtime["generated_image"]))),
        "twin_byte_sha256": sha256(Path(str(runtime["twin_image"]))),
        "product_type": runtime["product_type"],
        "scene_prompt_sha256": text_sha256(str(runtime["scene_prompt"])),
        "optional_audit_metadata": {
            key: runtime.get(key)
            for key in ("target_record_id", "device", "camera", "prompt_rank")
            if runtime.get(key) is not None
        },
    }
    return canonical_sha256(identity)


def validate_saved_result(result_path: Path, runtime: Mapping[str, Any], freeze: Mapping[str, Any]) -> Mapping[str, Any]:
    # Import only after static input validation so --validate-only catches bad files first.
    import sys
    if str(VERSION_ROOT) not in sys.path:
        sys.path.insert(0, str(VERSION_ROOT))
    from scoring import validate_result  # type: ignore

    result = load_json(result_path)
    validate_result(result)
    audit = result.get("audit")
    require(isinstance(audit, Mapping), "result audit missing")
    require(audit.get("protocol_version") == freeze.get("protocol_version"), "result protocol differs")
    require(audit.get("model_requested") == MODEL, "result requested model differs")
    returned = audit.get("model_returned")
    require(isinstance(returned, str) and re.fullmatch(r"gpt-5\.5(?:-\d{4}-\d{2}-\d{2})?", returned), "result returned model differs")
    require(audit.get("input_fingerprint") == expected_input_fingerprint(runtime), "result input fingerprint differs")
    expected_audit_hashes = freeze.get("result_audit_hashes")
    require(isinstance(expected_audit_hashes, Mapping), "freeze result-audit hash map missing")
    for key, expected in expected_audit_hashes.items():
        require(audit.get(key) == expected, f"result audit {key} differs")
    request_path = result_path.parent / "request.json"
    request = load_json(request_path)
    require(request.get("input") == dict(runtime), "saved request input differs")
    require(request.get("model_requested") == MODEL, "saved request model differs")
    require(request.get("input_fingerprint") == audit.get("input_fingerprint"), "saved request fingerprint differs")
    attempts = result.get("raw_attempts")
    require(isinstance(attempts, list) and attempts, "result raw_attempts missing")
    for item in attempts:
        require(isinstance(item, Mapping), "raw attempt invalid")
        number = item.get("attempt")
        require(number in {1, 2}, "raw attempt number differs")
        metadata = result_path.parent / f"attempt_{number}_metadata.json"
        response = result_path.parent / f"attempt_{number}_response.txt"
        error = result_path.parent / f"attempt_{number}_error.json"
        require(metadata.is_file() or error.is_file(), f"attempt {number} metadata/error missing")
        require(response.is_file() or error.is_file(), f"attempt {number} raw response/error missing")
    require(result.get("status") in {"ok", "unassessable"}, f"judge result is not successful: {result.get('status')}")
    return result


class Ledger:
    def __init__(self, path: Path, immutable: Mapping[str, Any], record_ids: list[str], workers: int) -> None:
        self.path = path
        self.lock = threading.Lock()
        if path.exists():
            payload = load_json(path)
            for key, expected in immutable.items():
                require(payload.get(key) == expected, f"existing progress has different {key}")
            require(payload.get("record_ids") == record_ids, "existing progress record order differs")
            payload["workers"] = workers
            payload["resumed_at_utc"] = utc_now()
            # Interrupted workers are safe to resume; judge() validates its cache.
            for item in payload["items"].values():
                if item.get("status") == "running":
                    item.clear()
                    item["status"] = "pending"
        else:
            payload = {
                "schema_version": "hp-placement-v4.3.1-full160-progress-v1",
                **immutable,
                "record_ids": record_ids,
                "workers": workers,
                "started_at_utc": utc_now(),
                "status": "pending",
                "items": {record_id: {"status": "pending"} for record_id in record_ids},
            }
        self.payload = payload
        self._write()

    def _write(self) -> None:
        self.payload["updated_at_utc"] = utc_now()
        statuses = [item["status"] for item in self.payload["items"].values()]
        self.payload["counts"] = {status: statuses.count(status) for status in sorted(set(statuses))}
        atomic_json(self.path, self.payload)

    def update(self, record_id: str, status: str, **fields: Any) -> None:
        with self.lock:
            self.payload["items"][record_id] = {"status": status, **fields}
            self._write()

    def finish(self, status: str) -> None:
        with self.lock:
            self.payload["status"] = status
            self.payload["finished_at_utc"] = utc_now()
            self._write()


def positive_workers(value: str) -> int:
    number = int(value)
    if not 1 <= number <= MAX_WORKERS:
        raise argparse.ArgumentTypeError(f"workers must be between 1 and {MAX_WORKERS}")
    return number


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--freeze", type=Path, default=DEFAULT_FREEZE)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--workers", type=positive_workers, default=2)
    parser.add_argument("--model", default=MODEL, choices=[MODEL])
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--acknowledge-launch-authorized", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = args.manifest.expanduser().resolve()
    freeze_path = args.freeze.expanduser().resolve()
    run_dir = args.run_dir.expanduser().resolve()
    records = validate_manifest(manifest_path)
    freeze = validate_freeze(freeze_path, manifest_path)
    flattened = [(str(record["id"]), runtime_input(record)) for record in records]
    summary = {
        "manifest": str(manifest_path),
        "manifest_sha256": sha256(manifest_path),
        "protocol_freeze": str(freeze_path),
        "protocol_freeze_sha256": sha256(freeze_path),
        "protocol_version": freeze["protocol_version"],
        "model": args.model,
        "workers": args.workers,
        "records": len(flattened),
    }
    if args.validate_only:
        print(json.dumps({**summary, "status": "validated_no_model_calls", "model_calls": 0}, indent=2))
        return 0
    require(args.acknowledge_launch_authorized, "live run requires --acknowledge-launch-authorized")

    import sys
    if str(VERSION_ROOT) not in sys.path:
        sys.path.insert(0, str(VERSION_ROOT))
    from run_judge import judge  # type: ignore

    run_dir.mkdir(parents=True, exist_ok=True)
    immutable = {
        "manifest": str(manifest_path),
        "manifest_sha256": sha256(manifest_path),
        "protocol_freeze": str(freeze_path),
        "protocol_freeze_sha256": sha256(freeze_path),
        "protocol_version": freeze["protocol_version"],
        "model": args.model,
    }
    ledger = Ledger(run_dir / "progress.json", immutable, [record_id for record_id, _ in flattened], args.workers)
    print_lock = threading.Lock()

    def run_one(record_id: str, runtime: dict[str, Any]) -> tuple[str, str]:
        output = run_dir / record_id
        result_path = output / "result.json"
        cached = result_path.is_file()
        ledger.update(record_id, "running", started_at_utc=utc_now(), result_path=str(result_path), cached_before_start=cached)
        try:
            result = judge(runtime, output, model=args.model)
            validate_saved_result(result_path, runtime, freeze)
            status = "cached" if cached else "done"
            ledger.update(
                record_id,
                status,
                finished_at_utc=utc_now(),
                result_path=str(result_path),
                result_sha256=sha256(result_path),
                judge_status=result["status"],
                verdict=(result.get("derived") or {}).get("verdict"),
                score=(result.get("derived") or {}).get("score"),
            )
        except Exception as exc:
            status = "error"
            ledger.update(record_id, status, finished_at_utc=utc_now(), result_path=str(result_path), error=f"{type(exc).__name__}: {exc}")
        with print_lock:
            print(json.dumps({"id": record_id, "status": status}), flush=True)
        return record_id, status

    statuses: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(run_one, record_id, runtime) for record_id, runtime in flattened]
        for future in as_completed(futures):
            _, status = future.result()
            statuses.append(status)
    errors = statuses.count("error")
    ledger.finish("complete" if errors == 0 else "completed_with_errors")
    print(json.dumps({**summary, "done": statuses.count("done"), "cached": statuses.count("cached"), "errors": errors, "progress": str(run_dir / "progress.json")}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
