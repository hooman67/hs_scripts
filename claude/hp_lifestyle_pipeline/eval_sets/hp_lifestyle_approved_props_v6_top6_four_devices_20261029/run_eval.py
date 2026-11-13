#!/usr/bin/env python3
"""Prepare, run, verify, and export the bounded 16-bank V6 text evaluation."""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
SOURCE_EVAL = (
    PROJECT_ROOT
    / "eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028"
)
LIVE_V6 = PROJECT_ROOT / "research/source_messaging_v1_to_v6/versions/v6"
DEFAULT_CATALOG = LIVE_V6 / "approved-20261029.catalog.json"
REVISION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
CASE_METADATA_FIELDS = (
    "case_id",
    "group_id",
    "pair_id",
    "device_id",
    "device_display_name",
    "device_type",
    "camera_tag",
    "source_camera_name",
    "view_role",
    "render_gallery_url",
    "render_lookup",
    "source_pair",
    "product_identity_conflict",
    "source_input_path",
    "source_input_sha256",
)
REQUIRED_RUNTIME_FILES = {
    "__init__.py",
    "camera.py",
    "camera_profiles.json",
    "catalog.py",
    "cli.py",
    "input.schema.json",
    "model_output.schema.json",
    "prop_lexicon.json",
    "provider.py",
    "reference_library.json",
    "runtime.py",
    "system_prompt.md",
    "validation.py",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def canonical_json_hash(value: Any) -> str:
    return sha_bytes(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_exclusive(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def write_text_exclusive(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(value)
        handle.flush()
        os.fsync(handle.fileno())


def revision_dir(revision: str, eval_root: Path = HERE) -> Path:
    if not REVISION_RE.fullmatch(revision):
        raise ValueError(
            "revision must start with an alphanumeric character and contain only "
            "letters, digits, dot, underscore, or hyphen"
        )
    return eval_root / "revisions" / revision


def _runtime_source_files(runtime_source: Path) -> list[Path]:
    files = []
    for path in runtime_source.rglob("*"):
        relative = path.relative_to(runtime_source)
        if not path.is_file():
            continue
        if "__pycache__" in relative.parts or ".pytest_cache" in relative.parts:
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(runtime_source).as_posix())


def _copy_runtime(runtime_source: Path, runtime_target: Path) -> None:
    source_files = _runtime_source_files(runtime_source)
    available = {
        path.relative_to(runtime_source).as_posix() for path in source_files
    }
    missing = sorted(REQUIRED_RUNTIME_FILES - available)
    if missing:
        raise ValueError(f"V6 runtime package is incomplete: {missing}")
    hashes_before = {
        path.relative_to(runtime_source).as_posix(): sha_file(path)
        for path in source_files
    }
    for source in source_files:
        relative = source.relative_to(runtime_source)
        target = runtime_target / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    hashes_after = {
        path.relative_to(runtime_source).as_posix(): sha_file(path)
        for path in _runtime_source_files(runtime_source)
    }
    if hashes_before != hashes_after:
        raise ValueError("live V6 runtime changed while it was being snapshotted")
    copied_hashes = {
        path.relative_to(runtime_target).as_posix(): sha_file(path)
        for path in _runtime_source_files(runtime_target)
    }
    if hashes_before != copied_hashes:
        raise ValueError("frozen V6 runtime does not match the live source bytes")


def _check_catalog(runtime_dir: Path, catalog_path: Path) -> dict[str, Any]:
    command = [
        sys.executable,
        str(runtime_dir / "cli.py"),
        "check-catalog",
        "--catalog",
        str(catalog_path),
    ]
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )
    if completed.returncode != 0:
        detail = completed.stdout.strip() or completed.stderr.strip() or "unknown failure"
        raise ValueError(f"approved catalogue failed V6 validation: {detail}")
    response = json.loads(completed.stdout)
    if response.get("status") != "ok" or response.get("approved_entries", 0) <= 0:
        raise ValueError("approved catalogue is empty or invalid")
    return response


def _asset_hashes(snapshot: Path) -> dict[str, dict[str, Any]]:
    assets: dict[str, dict[str, Any]] = {}
    inputs = snapshot / "inputs"
    runtime = snapshot / "runtime/v6"
    paths = sorted(path for path in inputs.rglob("*") if path.is_file())
    paths.extend(_runtime_source_files(runtime))
    paths.extend(sorted(path for path in (snapshot / "scripts").rglob("*.py") if path.is_file()))
    for path in paths:
        relative = path.relative_to(snapshot).as_posix()
        assets[relative] = {
            "bytes": path.stat().st_size,
            "sha256": sha_file(path),
        }
    return assets


def verify_snapshot(snapshot: Path) -> dict[str, Any]:
    manifest_path = snapshot / "snapshot_manifest.json"
    manifest = load_json(manifest_path)
    expected = manifest["snapshot_assets"]
    actual = _asset_hashes(snapshot)
    if set(actual) != set(expected):
        missing = sorted(set(expected) - set(actual))
        unexpected = sorted(set(actual) - set(expected))
        raise ValueError(
            f"snapshot file set changed; missing={missing}, unexpected={unexpected}"
        )
    mismatches = [
        relative
        for relative, record in expected.items()
        if actual[relative] != record
    ]
    if mismatches:
        raise ValueError(f"snapshot bytes changed: {mismatches}")
    if len(manifest["cases"]) != 16:
        raise ValueError("snapshot must contain exactly 16 cases")
    return manifest


def prepare_revision(
    revision: str,
    catalog_source: Path,
    *,
    eval_root: Path = HERE,
    source_eval: Path = SOURCE_EVAL,
    runtime_source: Path = LIVE_V6,
) -> Path:
    """Create an immutable, exclusive snapshot. This operation makes no API calls."""

    destination = revision_dir(revision, eval_root)
    if destination.exists():
        raise FileExistsError(f"revision already exists: {destination}")
    source_manifest_path = source_eval / "manifest.json"
    source_manifest = load_json(source_manifest_path)
    case_ids = source_manifest.get("authorized_text_case_ids")
    source_cases = {case["case_id"]: case for case in source_manifest.get("cases", [])}
    if (
        not isinstance(case_ids, list)
        or len(case_ids) != 16
        or len(set(case_ids)) != 16
        or set(case_ids) != set(source_cases)
    ):
        raise ValueError("source eval does not contain the exact 16 authorized banks")
    if not catalog_source.is_file():
        raise FileNotFoundError(f"approved catalogue is unavailable: {catalog_source}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{revision}.prepare-", dir=destination.parent))
    try:
        runtime_target = stage / "runtime/v6"
        _copy_runtime(runtime_source, runtime_target)
        helper_source = PROJECT_ROOT / "research/source_messaging_v1_to_v6/scripts/probe_gpt55.py"
        helper_target = stage / "scripts/probe_gpt55.py"
        helper_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(helper_source, helper_target)
        frozen_catalog = runtime_target / "approved_catalog.json"
        catalog_hash_before = sha_file(catalog_source)
        shutil.copyfile(catalog_source, frozen_catalog)
        if catalog_hash_before != sha_file(catalog_source):
            raise ValueError("approved catalogue changed while it was being snapshotted")
        if catalog_hash_before != sha_file(frozen_catalog):
            raise ValueError("frozen approved catalogue does not match its source bytes")
        catalog_check = _check_catalog(runtime_target, frozen_catalog)

        prepared_cases = []
        for case_id in case_ids:
            source_case = source_cases[case_id]
            source_input = source_eval / "inputs" / f"{case_id}.json"
            if not source_input.is_file():
                raise FileNotFoundError(f"source input is unavailable: {source_input}")
            if sha_file(source_input) != source_case["input_sha256"]:
                raise ValueError(f"source input hash disagrees with V5 manifest: {case_id}")
            payload = load_json(source_input)
            if set(payload) != {"smart_brief", "source_messaging", "camera_tag"}:
                raise ValueError(f"source input contract changed: {case_id}")
            if payload["camera_tag"] != source_case["camera_tag"]:
                raise ValueError(f"camera mapping changed in source input: {case_id}")
            frozen_input = stage / "inputs" / source_input.name
            frozen_input.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_input, frozen_input)
            if source_input.read_bytes() != frozen_input.read_bytes():
                raise ValueError(f"input was not copied byte-for-byte: {case_id}")
            metadata = {
                field: copy.deepcopy(source_case[field])
                for field in CASE_METADATA_FIELDS
            }
            metadata.update(
                {
                    "input_source_path": str(source_input.resolve()),
                    "input_source_sha256": sha_file(source_input),
                    "frozen_input_path": f"inputs/{source_input.name}",
                    "frozen_input_sha256": sha_file(frozen_input),
                    "input_semantic_sha256": canonical_json_hash(payload),
                }
            )
            prepared_cases.append(metadata)

        manifest = {
            "version": "hp-lifestyle-approved-props-v6-top6-four-devices-snapshot-v1",
            "revision": revision,
            "prepared_at_utc": utc_now(),
            "status": "prepared_no_model_calls",
            "source_eval": {
                "path": str(source_eval.resolve()),
                "manifest_path": str(source_manifest_path.resolve()),
                "manifest_sha256": sha_file(source_manifest_path),
                "inputs_copied_byte_for_byte": True,
            },
            "scope": {
                "device_count": 4,
                "views_per_device": 4,
                "case_count": 16,
                "candidates_per_case": 10,
                "selected_per_case": 6,
                "candidate_count": 160,
                "selected_prompt_count": 96,
                "selection_rule": (
                    "first six candidates after the V6 runtime stable descending "
                    "source-relevance and C-Tech-score ordering"
                ),
                "model": "gpt-5.5",
                "max_concurrency": 2,
                "semantic_calls_per_case": "one initial call plus at most one V6 repair",
                "image_generation_authorized": False,
            },
            "device_source_mapping": copy.deepcopy(
                source_manifest["device_source_mapping"]
            ),
            "catalog": {
                "source_path": str(catalog_source.resolve()),
                "frozen_path": "runtime/v6/approved_catalog.json",
                "source_sha256": sha_file(catalog_source),
                "frozen_sha256": sha_file(frozen_catalog),
                "approved_entries": catalog_check["approved_entries"],
                "revision": load_json(frozen_catalog).get("revision"),
            },
            "authorized_text_case_ids": case_ids,
            "cases": prepared_cases,
            "snapshot_assets": _asset_hashes(stage),
        }
        write_json_exclusive(stage / "snapshot_manifest.json", manifest)
        stage.rename(destination)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    verify_snapshot(destination)
    return destination


def _run_cli(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def _run_case(
    snapshot: Path,
    manifest: dict[str, Any],
    case_id: str,
    command_runner: Callable[[list[str]], subprocess.CompletedProcess[str]],
) -> dict[str, Any]:
    case = next(item for item in manifest["cases"] if item["case_id"] == case_id)
    input_path = snapshot / case["frozen_input_path"]
    output_path = snapshot / "results" / f"{case_id}.json"
    launch_path = snapshot / "call_journals" / f"{case_id}.launch.json"
    process_path = snapshot / "call_journals" / f"{case_id}.process.json"
    command = [
        "uv",
        "run",
        "--script",
        str(snapshot / "runtime/v6/cli.py"),
        "run",
        "--input",
        str(input_path),
        "--catalog",
        str(snapshot / "runtime/v6/approved_catalog.json"),
        "--output",
        str(output_path),
    ]
    write_json_exclusive(
        launch_path,
        {
            "version": "v6-eval-pre-call-journal-v1",
            "case_id": case_id,
            "recorded_before_provider_process_start": True,
            "recorded_at_utc": utc_now(),
            "input_path": str(input_path),
            "input_sha256": sha_file(input_path),
            "catalog_sha256": sha_file(
                snapshot / "runtime/v6/approved_catalog.json"
            ),
            "runtime_cli_sha256": sha_file(snapshot / "runtime/v6/cli.py"),
            "output_path": str(output_path),
            "command": command,
        },
    )
    completed = command_runner(command)
    process_record = {
        "version": "v6-eval-process-result-v1",
        "case_id": case_id,
        "completed_at_utc": utc_now(),
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "output_exists": output_path.is_file(),
        "output_sha256": sha_file(output_path) if output_path.is_file() else None,
    }
    write_json_exclusive(process_path, process_record)
    return process_record


def run_revision(
    revision: str,
    *,
    paid_calls_authorized: bool,
    max_concurrency: int = 2,
    eval_root: Path = HERE,
    command_runner: Callable[[list[str]], subprocess.CompletedProcess[str]] = _run_cli,
    selected_case_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Run all 16 banks once. Existing journals or outputs are a hard stop."""

    if not paid_calls_authorized:
        raise PermissionError(
            "paid calls are gated; pass --paid-calls-authorized only after root GO"
        )
    if max_concurrency not in {1, 2}:
        raise ValueError("max concurrency must be one or two")
    snapshot = revision_dir(revision, eval_root)
    manifest = verify_snapshot(snapshot)
    if (snapshot / "run_complete.json").exists():
        raise FileExistsError(
            "revision already finished; do not repeat terminal model calls"
        )
    case_ids = manifest["authorized_text_case_ids"]
    selected = selected_case_ids or case_ids
    if len(selected) != len(set(selected)) or not set(selected).issubset(case_ids):
        raise ValueError("selected case IDs must be unique registered banks")
    pending = []
    for case_id in selected:
        result_path = snapshot / "results" / f"{case_id}.json"
        process_path = snapshot / "call_journals" / f"{case_id}.process.json"
        launch_path = snapshot / "call_journals" / f"{case_id}.launch.json"
        if result_path.exists() and process_path.exists():
            continue  # Terminal results, including failures, never get a new call.
        if result_path.exists() or process_path.exists() or launch_path.exists():
            raise FileExistsError(f"ambiguous interrupted case; inspect before any retry: {case_id}")
        pending.append(case_id)
    if not pending:
        raise FileExistsError("no untouched selected cases remain")
    if not (snapshot / "run_started.json").exists():
        write_json_exclusive(snapshot / "run_started.json", {
            "version": "v6-eval-run-start-v1",
            "revision": revision,
            "started_at_utc": utc_now(),
            "paid_calls_authorized_flag": True,
            "case_ids": case_ids,
            "max_concurrency": max_concurrency,
            "expected_candidate_count": 160,
        })
    records: dict[str, Any] = {}
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_concurrency
    ) as executor:
        futures = {
            executor.submit(
                _run_case, snapshot, manifest, case_id, command_runner
            ): case_id
            for case_id in pending
        }
        for future in concurrent.futures.as_completed(futures):
            case_id = futures[future]
            records[case_id] = future.result()
            print(json.dumps({"case_id": case_id, "returncode": records[case_id]["returncode"]}), flush=True)
    successes = sum(
        record["returncode"] == 0 and record["output_exists"]
        for record in records.values()
    )
    summary = {
        "version": "v6-eval-run-complete-v1",
        "revision": revision,
        "completed_at_utc": utc_now(),
        "case_count": len(pending),
        "process_successes": successes,
        "process_failures": len(pending) - successes,
        "all_processes_succeeded": successes == len(pending),
        "cases": {case_id: records[case_id] for case_id in pending},
    }
    batch_dir = snapshot / "batches"
    batch_number = len(list(batch_dir.glob("*.json"))) + 1
    write_json_exclusive(batch_dir / f"batch_{batch_number:03d}.json", summary)
    if all((snapshot / "call_journals" / f"{case_id}.process.json").exists() for case_id in case_ids):
        terminal = {case_id: load_json(snapshot / "call_journals" / f"{case_id}.process.json") for case_id in case_ids}
        total_successes = sum(record["returncode"] == 0 and record["output_exists"] for record in terminal.values())
        write_json_exclusive(snapshot / "run_complete.json", {
            **summary, "case_count": len(case_ids), "process_successes": total_successes,
            "process_failures": len(case_ids) - total_successes,
            "all_processes_succeeded": total_successes == len(case_ids), "cases": terminal,
        })
    return summary


def _bank_audit_summary(result: dict[str, Any]) -> dict[str, Any]:
    audit = result["audit"]
    attempts = audit.get("attempts", [])
    return {
        "status": result["status"],
        "semantic_calls": audit.get("semantic_calls"),
        "semantic_repair_attempted": len(attempts) == 2,
        "initial_validation_errors": copy.deepcopy(
            attempts[0].get("errors", []) if attempts else []
        ),
        "final_validation_errors": copy.deepcopy(
            attempts[-1].get("errors", []) if attempts else []
        ),
        "transport_attempts_known": audit.get("transport_attempts_known"),
        "transport_accounting_complete": audit.get(
            "transport_accounting_complete"
        ),
        "provider_attempts": [
            copy.deepcopy(attempt.get("provider")) for attempt in attempts
        ],
    }


def _validate_successful_bank(case_id: str, result: Any) -> None:
    if not isinstance(result, dict) or result.get("status") != "ok":
        raise ValueError(f"bank did not succeed: {case_id}")
    prompts = result.get("prompts")
    if not isinstance(prompts, list) or len(prompts) != 10:
        raise ValueError(f"bank does not contain ten prompts: {case_id}")
    if [item.get("id") for item in prompts] != [f"p{i}" for i in range(1, 11)]:
        raise ValueError(f"bank IDs are not p1 through p10: {case_id}")
    ranks = [
        (item.get("source_relevance_score"), item.get("ctech_reference_score"))
        for item in prompts
    ]
    if any(
        not isinstance(source, int) or not isinstance(ctech, int)
        for source, ctech in ranks
    ) or ranks != sorted(ranks, reverse=True):
        raise ValueError(f"bank is not in V6 source/C-Tech rank order: {case_id}")
    audit = result.get("audit")
    if not isinstance(audit, dict) or len(audit.get("attempts", [])) not in {1, 2}:
        raise ValueError(f"bank audit does not prove bounded semantics: {case_id}")
    if not isinstance(result.get("debug"), dict):
        raise ValueError(f"bank debug is missing: {case_id}")


def _validate_call_journals(
    snapshot: Path, case_id: str, result: dict[str, Any]
) -> dict[str, Any]:
    launch_path = snapshot / "call_journals" / f"{case_id}.launch.json"
    process_path = snapshot / "call_journals" / f"{case_id}.process.json"
    cli_journal = snapshot / "results" / f"{case_id}.json.run"
    for required in (launch_path, process_path):
        if not required.is_file():
            raise ValueError(f"durable call journal is missing: {required}")
    attempt_count = len(result["audit"]["attempts"])
    raw_attempts = []
    for attempt_number in range(1, attempt_count + 1):
        request_path = cli_journal / f"attempt_{attempt_number}.request.json"
        response_path = cli_journal / f"attempt_{attempt_number}.response.json"
        if not request_path.is_file() or not response_path.is_file():
            raise ValueError(
                f"raw request/response journal is incomplete: {case_id} attempt {attempt_number}"
            )
        raw_attempts.append(
            {
                "number": attempt_number,
                "request_path": str(request_path),
                "request_sha256": sha_file(request_path),
                "response_path": str(response_path),
                "response_sha256": sha_file(response_path),
            }
        )
    return {
        "launch_path": str(launch_path),
        "launch_sha256": sha_file(launch_path),
        "process_path": str(process_path),
        "process_sha256": sha_file(process_path),
        "cli_journal_path": str(cli_journal),
        "raw_attempts": raw_attempts,
    }


def export_revision(
    revision: str,
    *,
    eval_root: Path = HERE,
) -> Path:
    """Export 160 candidates and source-ranked top 96 only after 16 successes."""

    snapshot = revision_dir(revision, eval_root)
    manifest = verify_snapshot(snapshot)
    if not (snapshot / "run_complete.json").is_file():
        raise ValueError("run_complete.json is missing")
    cases_by_id = {case["case_id"]: case for case in manifest["cases"]}
    all_rows: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []
    bank_audit: dict[str, Any] = {}
    for case_id in manifest["authorized_text_case_ids"]:
        result_path = snapshot / "results" / f"{case_id}.json"
        if not result_path.is_file():
            raise ValueError(f"result is missing: {case_id}")
        result = load_json(result_path)
        _validate_successful_bank(case_id, result)
        journal_audit = _validate_call_journals(snapshot, case_id, result)
        case = cases_by_id[case_id]
        source_input = load_json(snapshot / case["frozen_input_path"])
        bank_audit[case_id] = {
            "case_metadata": copy.deepcopy(case),
            "source_input": source_input,
            "source_input_sha256": sha_file(snapshot / case["frozen_input_path"]),
            "result_path": str(result_path),
            "result_sha256": sha_file(result_path),
            "debug": copy.deepcopy(result["debug"]),
            "run": _bank_audit_summary(result),
            "journals": journal_audit,
        }
        for bank_rank, candidate in enumerate(result["prompts"], start=1):
            row = {
                "prompt_key": f"{case_id}::{candidate['id']}",
                "device_id": case["device_id"],
                "device_display_name": case["device_display_name"],
                "device_type": case["device_type"],
                "source_pair": case["source_pair"],
                "camera_tag": case["camera_tag"],
                "source_camera_name": case["source_camera_name"],
                "view_role": case["view_role"],
                "render_gallery_url": case["render_gallery_url"],
                "render_lookup": copy.deepcopy(case["render_lookup"]),
                "bank_rank": bank_rank,
                **copy.deepcopy(candidate),
                "text_sha256": sha_bytes(candidate["text"].encode("utf-8")),
                "bank_debug_ref": case_id,
            }
            all_rows.append(row)
            if bank_rank <= 6:
                selected_rows.append(copy.deepcopy(row))

    if len(all_rows) != 160 or len(selected_rows) != 96:
        raise ValueError("export counts do not equal 160 candidates and 96 selected")
    bank_counts = Counter(row["bank_debug_ref"] for row in selected_rows)
    if len(bank_counts) != 16 or set(bank_counts.values()) != {6}:
        raise ValueError("top-six export does not contain six prompts from every bank")
    if len({row["prompt_key"] for row in all_rows}) != 160:
        raise ValueError("prompt keys are not unique")

    shared = {
        "revision": revision,
        "snapshot_manifest_path": str(snapshot / "snapshot_manifest.json"),
        "snapshot_manifest_sha256": sha_file(snapshot / "snapshot_manifest.json"),
        "selection_rule": manifest["scope"]["selection_rule"],
        "device_source_mapping": copy.deepcopy(
            manifest["device_source_mapping"]
        ),
        "bank_audit": bank_audit,
    }
    all_output = {
        "version": "hp-lifestyle-approved-props-v6-all-four-devices-v1",
        **copy.deepcopy(shared),
        "counts": {
            "devices": 4,
            "views_per_device": 4,
            "banks": 16,
            "candidates_per_bank": 10,
            "prompts": 160,
        },
        "prompts": all_rows,
    }
    top_output = {
        "version": "hp-lifestyle-approved-props-v6-top6-four-devices-v1",
        **copy.deepcopy(shared),
        "counts": {
            "devices": 4,
            "views_per_device": 4,
            "banks": 16,
            "selected_per_bank": 6,
            "prompts": 96,
        },
        "prompts": selected_rows,
    }
    export_root = snapshot / "exports"
    destination = export_root / "final"
    if destination.exists():
        raise FileExistsError(f"export already exists: {destination}")
    export_root.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".final.export-", dir=export_root))
    try:
        write_json_exclusive(stage / "prompts_all_160.json", all_output)
        write_json_exclusive(stage / "prompts_top6_96.json", top_output)
        write_text_exclusive(
            stage / "prompts_all_160.txt",
            "\n\n".join(
                _plain_text_block(row) for row in all_rows
            )
            + "\n",
        )
        write_text_exclusive(
            stage / "prompts_top6_96.txt",
            "\n\n".join(
                _plain_text_block(row) for row in selected_rows
            )
            + "\n",
        )
        validation = {
            "version": "hp-lifestyle-approved-props-v6-export-validation-v1",
            "passed": True,
            "checks": {
                "snapshot_integrity_passed": True,
                "all_16_banks_status_ok": True,
                "all_banks_have_10_ranked_prompts": True,
                "semantic_calls_bounded_to_initial_plus_one_repair": True,
                "all_160_candidates_exported": True,
                "source_rank_top_6_per_bank_exported": True,
                "top_96_prompt_keys_unique": True,
                "source_inputs_and_bank_debug_preserved": True,
            },
            "bank_counts": dict(sorted(bank_counts.items())),
            "files": {
                name: {
                    "bytes": (stage / name).stat().st_size,
                    "sha256": sha_file(stage / name),
                }
                for name in (
                    "prompts_all_160.json",
                    "prompts_all_160.txt",
                    "prompts_top6_96.json",
                    "prompts_top6_96.txt",
                )
            },
        }
        write_json_exclusive(stage / "validation.json", validation)
        stage.rename(destination)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return destination


def _plain_text_block(row: dict[str, Any]) -> str:
    return (
        f"[{row['prompt_key']} | {row['device_display_name']} | "
        f"{row['camera_tag']} | rank {row['bank_rank']} | "
        f"source {row['source_relevance_score']} | "
        f"C-Tech {row['ctech_reference_score']}]\n{row['text']}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare", help="freeze runtime, catalog, and inputs")
    prepare.add_argument("--revision", required=True)
    prepare.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    run = commands.add_parser("run", help="make the authorized GPT-5.5 calls")
    run.add_argument("--revision", required=True)
    run.add_argument("--max-concurrency", type=int, choices=(1, 2), default=2)
    run.add_argument("--paid-calls-authorized", action="store_true")
    run.add_argument("--case-ids", nargs="+")
    export = commands.add_parser("export", help="gate and export 160 + top 96")
    export.add_argument("--revision", required=True)
    verify = commands.add_parser("verify", help="verify immutable snapshot bytes")
    verify.add_argument("--revision", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "prepare":
        path = prepare_revision(args.revision, args.catalog.resolve())
        print(json.dumps({"status": "prepared", "snapshot": str(path)}))
        return 0
    if args.command == "verify":
        snapshot = revision_dir(args.revision)
        manifest = verify_snapshot(snapshot)
        print(
            json.dumps(
                {
                    "status": "ok",
                    "revision": manifest["revision"],
                    "assets": len(manifest["snapshot_assets"]),
                }
            )
        )
        return 0
    if args.command == "run":
        summary = run_revision(
            args.revision,
            paid_calls_authorized=args.paid_calls_authorized,
            max_concurrency=args.max_concurrency,
            selected_case_ids=args.case_ids,
        )
        print(json.dumps(summary, indent=2))
        return 0 if summary["all_processes_succeeded"] else 2
    destination = export_revision(args.revision)
    print(json.dumps({"status": "exported", "path": str(destination)}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileExistsError, FileNotFoundError, PermissionError, ValueError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}), file=sys.stderr)
        raise SystemExit(2)
