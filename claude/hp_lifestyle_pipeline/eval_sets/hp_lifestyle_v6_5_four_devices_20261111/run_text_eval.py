#!/usr/bin/env python3
"""Freeze the same sixteen V6.4 inputs and generate bounded actual V6.5 banks."""
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

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
VERSIONS = PROJECT / "research/source_messaging_v1_to_v6/versions"
RUNTIME = VERSIONS / "v6_5"
BASELINE = PROJECT / (
    "eval_sets/hp_lifestyle_v6_4_four_devices_20261110/revisions/"
    "v6.4-structured-sources-20261110-r1"
)
SNAPSHOT = HERE / "revisions/v6.5-astra-rich-scenes-20261111-r1"
AUDIT_HELPERS = PROJECT / "eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109/run_text_eval.py"
ADOBE_INDEX = "https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple"
CATALOGUE = "approved-v6.5-20261111.catalog.json"


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def helpers():
    path = SNAPSHOT / "scripts/legacy_audit_helpers.py"
    spec = importlib.util.spec_from_file_location("v65_frozen_text_audit", path)
    if spec is None or spec.loader is None:
        raise ValueError("frozen text audit helper unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hashes():
    return {
        str(path.relative_to(SNAPSHOT)): sha(path)
        for directory in ("inputs", "runtime", "scripts")
        for path in sorted((SNAPSHOT / directory).rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
        and ".pytest_cache" not in path.parts and path.suffix not in {".pyc", ".pyo"}
    }


def verify():
    manifest = load(SNAPSHOT / "snapshot_manifest.json")
    if hashes() != manifest["snapshot_assets"]:
        raise ValueError("frozen V6.5 runtime/input/script bytes changed")
    if sha(BASELINE / "snapshot_manifest.json") != manifest["baseline_snapshot_sha256"]:
        raise ValueError("accepted V6.4 input manifest changed")
    if len(manifest["cases"]) != 16 or len({case["case_id"] for case in manifest["cases"]}) != 16:
        raise ValueError("expected sixteen unique input banks")
    if Counter(case["device_id"] for case in manifest["cases"]) != Counter(
        {"cashmere": 4, "elitebook": 4, "magic": 4, "tassel": 4}
    ):
        raise ValueError("expected four unchanged camera banks per device")
    return manifest


def prepare():
    if SNAPSHOT.exists():
        raise FileExistsError("V6.5 text snapshot already exists; do not refreeze")
    release = load(RUNTIME / "assets_manifest.json")
    for name, digest in release["files"].items():
        if sha(RUNTIME / name) != digest:
            raise ValueError(f"verified V6.5 asset changed: {name}")
    baseline = load(BASELINE / "snapshot_manifest.json")
    for name, digest in baseline["snapshot_assets"].items():
        if sha(BASELINE / name) != digest:
            raise ValueError(f"accepted V6.4 snapshot changed: {name}")
    sys.path.insert(0, str(VERSIONS))
    from v6_5.camera import resolve_camera
    from v6_5.catalog import validate_catalog
    from v6_5.runtime import _schema_errors

    schema = load(RUNTIME / "input.schema.json")
    registry = load(RUNTIME / "camera_profiles.json")
    validate_catalog(load(RUNTIME / CATALOGUE))
    SNAPSHOT.mkdir(parents=True)
    shutil.copytree(RUNTIME, SNAPSHOT / "runtime/v6_5", ignore=shutil.ignore_patterns(
        "__pycache__", ".pytest_cache", "*.pyc", "*.pyo",
    ))
    (SNAPSHOT / "scripts").mkdir()
    shutil.copyfile(AUDIT_HELPERS, SNAPSHOT / "scripts/legacy_audit_helpers.py")
    shutil.copyfile(Path(__file__), SNAPSHOT / "scripts/run_text_eval.py")
    cases = copy.deepcopy(baseline["cases"])
    for case in cases:
        original = BASELINE / case["frozen_input_path"]
        destination = SNAPSHOT / case["frozen_input_path"]
        request = load(original)
        if _schema_errors(request, schema):
            raise ValueError(f"same source no longer satisfies the three-field input contract: {case['case_id']}")
        camera = resolve_camera(registry, request["camera_tag"])
        if camera["resolved_tag"] != case["camera_tag"]:
            raise ValueError("camera binding differs from accepted V6.4")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original, destination)
        if sha(destination) != case["frozen_input_sha256"]:
            raise ValueError("source input bytes were not preserved")
    write(SNAPSHOT / "snapshot_manifest.json", {
        "version": "hp-lifestyle-v6.5-four-devices-snapshot-v1",
        "prepared_at_utc": now(), "cases": cases,
        "device_source_mapping": baseline["device_source_mapping"],
        "native_twin_geometry_evidence": baseline["native_twin_geometry_evidence"],
        "baseline_snapshot_path": str(BASELINE),
        "baseline_snapshot_sha256": sha(BASELINE / "snapshot_manifest.json"),
        "runtime_version": "v6.5-writer-runtime-r1-astra-rich-scenes",
        "runtime_asset_manifest_sha256": sha(RUNTIME / "assets_manifest.json"),
        "astra_authoring_provenance": load(RUNTIME / "authoring_provenance.json"),
        "model": "gpt-5.5", "reasoning_effort": "medium", "max_completion_tokens": 16000,
        "max_concurrency": 2, "expected_prompts": 160,
        "semantic_limit": "one initial plus at most one complete-bank repair",
        "terminal_bank_resampling_authorized": False,
        "snapshot_assets": hashes(),
    })
    verify()
    print(json.dumps({"prepared": str(SNAPSHOT), "banks": len(cases)}), flush=True)


def run_case(case):
    stem = case["case_id"]
    output = SNAPSHOT / "results" / (stem + ".json")
    command = [
        "uv", "run", "--extra-index-url", ADOBE_INDEX, "--script",
        str(SNAPSHOT / "runtime/v6_5/cli.py"), "run",
        "--input", str(SNAPSHOT / case["frozen_input_path"]),
        "--catalog", str(SNAPSHOT / "runtime/v6_5" / CATALOGUE),
        "--output", str(output),
    ]
    write(SNAPSHOT / "call_journals" / (stem + ".launch.json"), {
        "case_id": stem, "recorded_at_utc": now(), "command": command,
        "input_sha256": case["frozen_input_sha256"], "recorded_before_provider_process_start": True,
    })
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    record = {
        "case_id": stem, "completed_at_utc": now(), "returncode": completed.returncode,
        "stdout": completed.stdout, "stderr": completed.stderr,
        "output_exists": output.is_file(), "output_sha256": sha(output) if output.is_file() else None,
    }
    write(SNAPSHOT / "call_journals" / (stem + ".process.json"), record)
    print(json.dumps({"case_id": stem, "returncode": completed.returncode}), flush=True)
    return record


def run(authorized, case_ids):
    if not authorized:
        raise PermissionError("text generation requires --paid-calls-authorized")
    manifest = verify()
    if (SNAPSHOT / "run_complete.json").exists():
        raise FileExistsError("text run is terminal; no bank resampling")
    by_id = {case["case_id"]: case for case in manifest["cases"]}
    selected = case_ids if case_ids else list(by_id)
    if len(selected) != len(set(selected)) or set(selected) - by_id.keys():
        raise ValueError("invalid bank selection")
    pending = []
    for stem in selected:
        output = SNAPSHOT / "results" / (stem + ".json")
        process = SNAPSHOT / "call_journals" / (stem + ".process.json")
        launch = SNAPSHOT / "call_journals" / (stem + ".launch.json")
        if output.is_file() and process.is_file():
            record = load(process)
            if record["returncode"] != 0 or sha(output) != record["output_sha256"]:
                raise ValueError(f"terminal failed or changed bank; inspect rather than resample: {stem}")
            continue
        if output.exists() or process.exists() or launch.exists():
            raise FileExistsError(f"ambiguous/interrupted bank; inspect before retry: {stem}")
        pending.append(by_id[stem])
    if not pending:
        raise ValueError("no new banks selected")
    with ThreadPoolExecutor(max_workers=2) as executor:
        for future in as_completed([executor.submit(run_case, case) for case in pending]):
            future.result()
    records = {
        stem: load(SNAPSHOT / "call_journals" / (stem + ".process.json"))
        for stem in by_id if (SNAPSHOT / "call_journals" / (stem + ".process.json")).is_file()
    }
    successes = sum(record["returncode"] == 0 and record["output_exists"] for record in records.values())
    receipt = {
        "completed_at_utc": now(), "selected": selected, "cases": records,
        "successful_banks": successes, "failed_banks": len(records) - successes,
        "pending_banks": 16 - len(records),
    }
    batch_key = hashlib.sha256("\n".join(selected).encode()).hexdigest()[:16]
    name = "run_complete.json" if len(records) == 16 else f"batches/{batch_key}.json"
    write(SNAPSHOT / name, receipt)
    print(json.dumps({k: receipt[k] for k in ("successful_banks", "failed_banks", "pending_banks")}), flush=True)


def export():
    manifest = verify()
    terminal = load(SNAPSHOT / "run_complete.json")
    if terminal["successful_banks"] != 16 or terminal["failed_banks"]:
        raise ValueError("export requires sixteen actual successful banks")
    auditor = helpers()
    rows, banks = [], {}
    for case in manifest["cases"]:
        stem = case["case_id"]
        path = SNAPSHOT / "results" / (stem + ".json")
        if sha(path) != terminal["cases"][stem]["output_sha256"]:
            raise ValueError("terminal provider result changed")
        result = load(path)
        auditor._validate_successful_bank(stem, result)
        journals = auditor._validate_call_journals(SNAPSHOT, stem, result)
        banks[stem] = {
            "case_metadata": case, "source_input": load(SNAPSHOT / case["frozen_input_path"]),
            "source_input_path": str(SNAPSHOT / case["frozen_input_path"]),
            "source_input_sha256": case["frozen_input_sha256"],
            "result_path": str(path), "result_sha256": sha(path),
            "run": auditor._bank_audit_summary(result), "debug": result["debug"], "journals": journals,
        }
        for rank, candidate in enumerate(result["prompts"], 1):
            rows.append({
                **{key: copy.deepcopy(case[key]) for key in (
                    "device_id", "device_display_name", "device_type", "source_pair", "camera_tag",
                    "source_camera_name", "view_role", "render_gallery_url", "render_lookup",
                )},
                "prompt_key": f"{stem}::{candidate['id']}", "bank_rank": rank,
                **copy.deepcopy(candidate),
                "text_sha256": hashlib.sha256(candidate["text"].encode()).hexdigest(),
                "bank_debug_ref": stem,
            })
    if len(rows) != 160 or len({row["prompt_key"] for row in rows}) != 160 or len({row["text"] for row in rows}) != 160:
        raise ValueError("expected160 unique prompt keys and actual scene texts")
    destination = SNAPSHOT / "exports"
    write(destination / "prompts_all_160.json", {
        "version": "hp-lifestyle-v6.5-four-devices-all160-v1",
        "snapshot_manifest_path": str(SNAPSHOT / "snapshot_manifest.json"),
        "snapshot_manifest_sha256": sha(SNAPSHOT / "snapshot_manifest.json"),
        "selection_rule": "all ten source/C-Tech-ranked candidates in each of the same sixteen V6.4 input banks",
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16, "candidates_per_bank": 10, "prompts": 160},
        "device_source_mapping": manifest["device_source_mapping"],
        "bank_audit": banks, "prompts": rows,
    })
    with (destination / "prompts_all_160.txt").open("x") as stream:
        stream.write("\n\n".join(auditor._plain_text_block(row) for row in rows) + "\n")
    write(destination / "validation.json", {
        "passed": True, "prompt_count": 160, "distinct_text_count": 160,
        "semantic_calls": sum(bank["run"]["semantic_calls"] for bank in banks.values()),
        "files": {name: sha(destination / name) for name in ("prompts_all_160.json", "prompts_all_160.txt")},
    })
    print(json.dumps({"exported": str(destination), "prompts": len(rows)}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "verify", "run", "export"))
    parser.add_argument("--paid-calls-authorized", action="store_true")
    parser.add_argument("--case-ids", nargs="+")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "verify":
        print(json.dumps({"verified": len(verify()["cases"])}))
    elif args.command == "run":
        run(args.paid_calls_authorized, args.case_ids)
    else:
        export()
