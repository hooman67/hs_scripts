#!/usr/bin/env python3
"""Freeze sixteen new-format banks, run bounded GPT-5.5 calls and export160 prompts."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
VERSIONS = PROJECT / "research/source_messaging_v1_to_v6/versions"
RUNTIME = VERSIONS / "v6_4"
LEGACY = PROJECT / "eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109"
OLD_INPUTS = PROJECT / "eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028"
INVENTORY = PROJECT / "research/prompt_writer_v6_4/data/source_manifest.json"
ORIGINALS = Path("/home/colligo/hp_lifestyle_source_format_review_20261110/originals/new")
SNAPSHOT = HERE / "revisions/v6.4-structured-sources-20261110-r1"
ADOBE_INDEX = "https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple"
SELECTION = {
    "cashmere": ("viktor-smart-brief-source-messaging", "viktor-smart-brief-source-messaging.zip",
                 "One of the two supplied notebook pairs, selected under user authorization."),
    "elitebook": ("elitebook", "elitebook",
                 "The supplied EliteBook notebook pair retains the closest product-family overlap."),
    "tassel": ("magic", "magic.zip",
               "Smaller home-office source:420x365x245mm,7.4kg; compact twin:425x304x155mm."),
    "magic": ("tassel-smart-brief-source-messaging", "tassel-smart-brief-source-messaging.zip",
              "Larger shared-office source:390x410x280mm,12.8kg; large twin:407x399x386mm."),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def helpers(path: Path):
    spec = importlib.util.spec_from_file_location("frozen_text_audit_helpers", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"unavailable audit helpers: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def asset_hashes() -> dict[str, str]:
    return {
        str(path.relative_to(SNAPSHOT)): sha(path)
        for directory in ("inputs", "runtime", "scripts")
        for path in sorted((SNAPSHOT / directory).rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
        and ".pytest_cache" not in path.parts and path.suffix not in {".pyc", ".pyo"}
    }


def verify() -> dict[str, Any]:
    manifest = load(SNAPSHOT / "snapshot_manifest.json")
    if asset_hashes() != manifest["snapshot_assets"]:
        raise ValueError("frozen V6.4 runtime/input/script bytes changed")
    cases = manifest["cases"]
    if len(cases) != 16 or len({case["case_id"] for case in cases}) != 16:
        raise ValueError("expected sixteen unique banks")
    if Counter(case["device_id"] for case in cases) != Counter({d: 4 for d in SELECTION}):
        raise ValueError("expected four camera banks per existing device")
    return manifest


def prepare() -> None:
    inventory = load(INVENTORY)
    for record in inventory["files"]:
        for key in ("source_path", "durable_path"):
            if sha(Path(record[key])) != record["sha256"]:
                raise ValueError(f"source evidence changed: {record[key]}")
    for name, expected in inventory["v63_baseline_sha256"].items():
        if sha(VERSIONS / "v6_3" / name) != expected:
            raise ValueError(f"frozen V6.3 changed: {name}")
    sys.path.insert(0, str(VERSIONS))
    from v6_4.camera import resolve_camera
    from v6_4.catalog import validate_catalog
    from v6_4.runtime import _schema_errors
    from v6_4.source_inputs import load_pair

    release = load(RUNTIME / "assets_manifest.json")
    for name, expected in release["files"].items():
        if sha(RUNTIME / name) != expected:
            raise ValueError(f"V6.4 release hash mismatch: {name}")
    pairs = {}
    mapping = []
    for device, (pair_id, relative, rationale) in SELECTION.items():
        documents, provenance = load_pair(ORIGINALS / relative)
        pairs[device] = documents
        mapping.append({
            "device_id": device, "source_pair": pair_id,
            "selection_rationale": rationale, "document_provenance": provenance,
            "source_status": "supplied_product_brief" if device == "elitebook" else "fictional_development_concept",
            "exact_product_specification_match_claimed": False,
        })
    SNAPSHOT.mkdir(parents=True, exist_ok=False)
    shutil.copytree(
        RUNTIME, SNAPSHOT / "runtime/v6_4",
        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc"),
    )
    (SNAPSHOT / "scripts").mkdir()
    shutil.copyfile(LEGACY / "run_text_eval.py", SNAPSHOT / "scripts/legacy_audit_helpers.py")
    shutil.copyfile(Path(__file__), SNAPSHOT / "scripts/run_text_eval.py")
    audit_helpers = helpers(SNAPSHOT / "scripts/legacy_audit_helpers.py")
    registry = load(RUNTIME / "camera_profiles.json")
    schema = load(RUNTIME / "input.schema.json")
    catalogue = load(RUNTIME / "approved-v6.3-20261109.catalog.json")
    validate_catalog(catalogue)
    cases = []
    for original in load(OLD_INPUTS / "manifest.json")["cases"]:
        device = original["device_id"]
        request = {**copy.deepcopy(pairs[device]), "camera_tag": original["camera_tag"]}
        errors = _schema_errors(request, schema)
        if errors:
            raise ValueError(errors)
        camera = resolve_camera(registry, request["camera_tag"])
        if camera["resolution"] != "exact":
            raise ValueError(f"camera did not resolve exactly: {request['camera_tag']}")
        case = {
            key: copy.deepcopy(original[key]) for key in audit_helpers.CASE_METADATA_FIELDS
            if key not in {"pair_id", "source_pair", "source_input_path",
                           "source_input_sha256", "product_identity_conflict"}
        }
        case.update(
            source_pair=SELECTION[device][0], pair_id=SELECTION[device][0],
            frozen_input_path=f"inputs/{case['case_id']}.json",
        )
        destination = SNAPSHOT / case["frozen_input_path"]
        write(destination, request)
        case["frozen_input_sha256"] = sha(destination)
        cases.append(case)
    native_bundle = LEGACY / "endpoint_pr4523/input_bundle/manifest.json"
    manifest = {
        "version": "hp-lifestyle-v6.4-four-devices-snapshot-v1",
        "prepared_at_utc": now(), "cases": cases, "device_source_mapping": mapping,
        "source_inventory": {"path": str(INVENTORY), "sha256": sha(INVENTORY)},
        "native_twin_geometry_evidence": {"path": str(native_bundle), "sha256": sha(native_bundle)},
        "runtime_version": "v6.4-writer-runtime-r1-structured-sources",
        "model": "gpt-5.5", "reasoning_effort": "medium", "max_completion_tokens": 16000,
        "semantic_limit": "one initial plus at most one complete-bank repair",
        "expected_prompts": 160, "max_concurrency": 2,
        "image_generation_authorized": False, "snapshot_assets": asset_hashes(),
    }
    write(SNAPSHOT / "snapshot_manifest.json", manifest)
    verify()
    print(json.dumps({"prepared": str(SNAPSHOT), "banks": len(cases)}), flush=True)


def run_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = case["case_id"]
    result_path = SNAPSHOT / "results" / f"{case_id}.json"
    command = [
        "uv", "run", "--extra-index-url", ADOBE_INDEX, "--script",
        str(SNAPSHOT / "runtime/v6_4/cli.py"), "run",
        "--input", str(SNAPSHOT / case["frozen_input_path"]),
        "--catalog", str(SNAPSHOT / "runtime/v6_4/approved-v6.3-20261109.catalog.json"),
        "--output", str(result_path),
    ]
    write(SNAPSHOT / "call_journals" / f"{case_id}.launch.json", {
        "case_id": case_id, "recorded_at_utc": now(), "command": command,
        "input_sha256": case["frozen_input_sha256"],
        "recorded_before_provider_process_start": True,
    })
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    record = {
        "case_id": case_id, "completed_at_utc": now(), "returncode": completed.returncode,
        "stdout": completed.stdout, "stderr": completed.stderr,
        "output_exists": result_path.is_file(),
        "output_sha256": sha(result_path) if result_path.is_file() else None,
    }
    write(SNAPSHOT / "call_journals" / f"{case_id}.process.json", record)
    print(json.dumps({"case_id": case_id, "returncode": completed.returncode}), flush=True)
    return record


def run(paid_calls_authorized: bool) -> None:
    if not paid_calls_authorized:
        raise PermissionError("paid calls require explicit authorization")
    manifest = verify()
    if (SNAPSHOT / "run_complete.json").exists():
        raise FileExistsError("run already terminal; never resample completed banks")
    pending = []
    for case in manifest["cases"]:
        stem = case["case_id"]
        result = SNAPSHOT / "results" / f"{stem}.json"
        process = SNAPSHOT / "call_journals" / f"{stem}.process.json"
        launch = SNAPSHOT / "call_journals" / f"{stem}.launch.json"
        if process.is_file() and result.is_file():
            continue
        if process.exists() or result.exists() or launch.exists():
            raise FileExistsError(f"ambiguous/interrupted case; inspect before retry: {stem}")
        pending.append(case)
    if not (SNAPSHOT / "run_started.json").exists():
        write(SNAPSHOT / "run_started.json", {
            "started_at_utc": now(), "expected_prompts": 160,
            "paid_calls_authorized": True, "max_concurrency": 2,
        })
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(run_case, case) for case in pending]
        for future in as_completed(futures):
            future.result()
    records = {
        case["case_id"]: load(SNAPSHOT / "call_journals" / f"{case['case_id']}.process.json")
        for case in manifest["cases"]
    }
    successes = sum(record["returncode"] == 0 and record["output_exists"] for record in records.values())
    write(SNAPSHOT / "run_complete.json", {
        "completed_at_utc": now(), "cases": records,
        "successful_banks": successes, "failed_banks": 16 - successes,
    })
    print(json.dumps({"successful_banks": successes, "failed_banks": 16 - successes}), flush=True)


def export() -> None:
    manifest = verify()
    terminal = load(SNAPSHOT / "run_complete.json")
    audit_helpers = helpers(SNAPSHOT / "scripts/legacy_audit_helpers.py")
    rows = []
    bank_audit = {}
    for case in manifest["cases"]:
        case_id = case["case_id"]
        result_path = SNAPSHOT / "results" / f"{case_id}.json"
        if sha(result_path) != terminal["cases"][case_id]["output_sha256"]:
            raise ValueError(f"terminal result was altered: {case_id}")
        result = load(result_path)
        audit_helpers._validate_successful_bank(case_id, result)
        journals = audit_helpers._validate_call_journals(SNAPSHOT, case_id, result)
        bank_audit[case_id] = {
            "case_metadata": case, "source_input": load(SNAPSHOT / case["frozen_input_path"]),
            "result_path": str(result_path), "result_sha256": sha(result_path),
            "run": audit_helpers._bank_audit_summary(result),
            "debug": result["debug"], "journals": journals,
        }
        for rank, candidate in enumerate(result["prompts"], 1):
            rows.append({
                **{key: copy.deepcopy(case[key]) for key in (
                    "device_id", "device_display_name", "device_type", "source_pair",
                    "camera_tag", "source_camera_name", "view_role", "render_gallery_url", "render_lookup",
                )},
                "prompt_key": f"{case_id}::{candidate['id']}", "bank_rank": rank,
                **copy.deepcopy(candidate),
                "text_sha256": hashlib.sha256(candidate["text"].encode()).hexdigest(),
                "bank_debug_ref": case_id,
            })
    if len(rows) != 160 or len({row["prompt_key"] for row in rows}) != 160:
        raise ValueError("expected160 unique prompt keys")
    destination = SNAPSHOT / "exports"
    write(destination / "prompts_all_160.json", {
        "version": "hp-lifestyle-v6.4-four-devices-all160-v1",
        "snapshot_manifest_path": str(SNAPSHOT / "snapshot_manifest.json"),
        "snapshot_manifest_sha256": sha(SNAPSHOT / "snapshot_manifest.json"),
        "selection_rule": "all ten source/C-Tech-ranked candidates in every one of sixteen camera banks",
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16,
                   "candidates_per_bank": 10, "prompts": 160},
        "device_source_mapping": manifest["device_source_mapping"],
        "bank_audit": bank_audit, "prompts": rows,
    })
    with (destination / "prompts_all_160.txt").open("x", encoding="utf-8") as stream:
        stream.write("\n\n".join(audit_helpers._plain_text_block(row) for row in rows) + "\n")
    write(destination / "validation.json", {
        "passed": True, "prompt_count": len(rows),
        "distinct_text_count": len({row["text"] for row in rows}),
        "successful_banks": 16, "source_inputs_and_journals_preserved": True,
        "semantic_calls": sum(bank["run"]["semantic_calls"] for bank in bank_audit.values()),
        "files": {name: sha(destination / name) for name in ("prompts_all_160.json", "prompts_all_160.txt")},
    })
    print(json.dumps({"exported": str(destination), "prompts": len(rows)}), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "verify", "run", "export"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "verify":
        print(json.dumps({"verified": len(verify()["cases"])}))
    elif args.command == "run":
        run(args.paid_calls_authorized)
    else:
        export()


if __name__ == "__main__":
    main()
