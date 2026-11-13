#!/usr/bin/env python3
"""Strictly revalidate and export the final recorded bank from one revision.

The source is always each bank's final actual attempt ``normalized_output``.
There is no retry, fallback revision, earlier-attempt selection, or model call.
Validation and finalization come only from the supplied frozen validation
snapshot.  Any missing artifact, integrity error, or failed bank aborts the
entire export before an output directory is created.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from collections import Counter
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Any


EXPECTED_BANKS = 16
EXPECTED_PER_BANK = 10
EXPECTED_ALL = 160
EXPECTED_TOP = 96
CASE_ID_FIELDS = (
    "case_id", "group_id", "pair_id", "device_id", "device_display_name", "device_type",
    "camera_tag", "source_camera_name", "view_role", "render_gallery_url", "render_lookup",
    "source_pair", "product_identity_conflict", "source_input_path", "source_input_sha256",
)
MODEL_PROMPT_FIELDS = {
    "environment", "text", "prop_ids", "prop_mentions", "score_components", "evidence", "relationship",
    "explanation", "creative_departures", "ctech_reference_id", "ctech_reference_score",
    "ctech_explanation", "camera_fit_explanation",
}
FINALIZER_PROMPT_FIELDS = {"id", "source_relevance_score", "primary_support"}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                   separators=(",", ":"), allow_nan=False).encode("utf-8"))


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(value)
        handle.flush()
        os.fsync(handle.fileno())


def _runtime_files(runtime: Path) -> list[Path]:
    return sorted(
        (path for path in runtime.rglob("*")
         if path.is_file() and "__pycache__" not in path.relative_to(runtime).parts
         and ".pytest_cache" not in path.relative_to(runtime).parts and path.suffix not in {".pyc", ".pyo"}),
        key=lambda path: path.relative_to(runtime).as_posix(),
    )


def _snapshot_assets(snapshot: Path) -> dict[str, dict[str, Any]]:
    paths = sorted(path for path in (snapshot / "inputs").rglob("*") if path.is_file())
    paths.extend(_runtime_files(snapshot / "runtime/v6_2"))
    scripts = snapshot / "scripts"
    if scripts.is_dir():
        paths.extend(sorted(path for path in scripts.rglob("*.py") if path.is_file()))
    return {
        path.relative_to(snapshot).as_posix(): {"bytes": path.stat().st_size, "sha256": sha256_path(path)}
        for path in paths
    }


def verify_snapshot(snapshot: Path, label: str) -> tuple[dict[str, Any], dict[str, Any]]:
    snapshot = snapshot.resolve()
    manifest_path = snapshot / "snapshot_manifest.json"
    manifest = load_json(manifest_path)
    expected = manifest.get("snapshot_assets")
    if not isinstance(expected, dict):
        raise ValueError(f"{label}: snapshot_manifest has no snapshot_assets")
    actual = _snapshot_assets(snapshot)
    if set(actual) != set(expected):
        raise ValueError(f"{label}: snapshot file set changed; missing={sorted(set(expected)-set(actual))}, "
                         f"unexpected={sorted(set(actual)-set(expected))}")
    changed = [name for name in expected if expected[name] != actual[name]]
    if changed:
        raise ValueError(f"{label}: snapshot bytes changed: {changed}")
    case_ids = manifest.get("authorized_text_case_ids")
    cases = manifest.get("cases")
    if (not isinstance(case_ids, list) or len(case_ids) != EXPECTED_BANKS or len(set(case_ids)) != EXPECTED_BANKS
            or not isinstance(cases, list) or {case.get("case_id") for case in cases} != set(case_ids)):
        raise ValueError(f"{label}: snapshot does not define the exact 16 unique banks")
    if manifest.get("revision") != snapshot.name:
        raise ValueError(f"{label}: manifest revision does not match directory name")
    record = {
        "path": str(snapshot), "manifest_path": str(manifest_path),
        "manifest_sha256": sha256_path(manifest_path), "asset_count": len(actual),
        "assets_sha256": canonical_sha256(actual), "revision": manifest["revision"],
    }
    return manifest, record


def verify_matching_inputs(
    source_dir: Path, source_manifest: dict[str, Any], validation_dir: Path, validation_manifest: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    source_ids = source_manifest["authorized_text_case_ids"]
    if validation_manifest["authorized_text_case_ids"] != source_ids:
        raise ValueError("validation snapshot bank order differs from source revision")
    source_cases = {item["case_id"]: item for item in source_manifest["cases"]}
    validation_cases = {item["case_id"]: item for item in validation_manifest["cases"]}
    verified: dict[str, dict[str, Any]] = {}
    for case_id in source_ids:
        source_case, validation_case = source_cases[case_id], validation_cases[case_id]
        for field in CASE_ID_FIELDS:
            if source_case.get(field) != validation_case.get(field):
                raise ValueError(f"{case_id}: validation snapshot case metadata differs at {field}")
        source_path = source_dir / source_case["frozen_input_path"]
        validation_path = validation_dir / validation_case["frozen_input_path"]
        source_bytes, validation_bytes = source_path.read_bytes(), validation_path.read_bytes()
        source_hash, validation_hash = sha256_bytes(source_bytes), sha256_bytes(validation_bytes)
        for case, actual, label in ((source_case, source_hash, "source"), (validation_case, validation_hash, "validation")):
            if actual != case.get("frozen_input_sha256"):
                raise ValueError(f"{case_id}: {label} frozen input hash disagrees with its manifest")
        if source_bytes != validation_bytes:
            raise ValueError(f"{case_id}: source input bytes differ between snapshots")
        verified[case_id] = {"sha256": source_hash, "bytes": len(source_bytes),
                             "source_path": str(source_path), "validation_path": str(validation_path)}
    source_catalog = source_dir / source_manifest["catalog"]["frozen_path"]
    validation_catalog = validation_dir / validation_manifest["catalog"]["frozen_path"]
    if source_catalog.read_bytes() != validation_catalog.read_bytes():
        raise ValueError("approved catalog differs between source and validation snapshots")
    return verified


class FrozenRuntime(AbstractContextManager["FrozenRuntime"]):
    """Load only one frozen runtime package under a unique isolated name."""

    def __init__(self, snapshot: Path, manifest_sha256: str) -> None:
        self.runtime = snapshot.resolve() / "runtime/v6_2"
        self.package = f"_hp_frozen_v6_2_{manifest_sha256}"
        self.validation: Any = None
        self.camera: Any = None

    def __enter__(self) -> "FrozenRuntime":
        init = self.runtime / "__init__.py"
        if not init.is_file():
            raise FileNotFoundError(init)
        spec = importlib.util.spec_from_file_location(
            self.package, init, submodule_search_locations=[str(self.runtime)]
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot import frozen runtime {self.runtime}")
        package = importlib.util.module_from_spec(spec)
        sys.modules[self.package] = package
        try:
            spec.loader.exec_module(package)
            self.validation = importlib.import_module(f"{self.package}.validation")
            self.camera = importlib.import_module(f"{self.package}.camera")
        except Exception:
            self.__exit__(None, None, None)
            raise
        for module, function in ((self.validation, "validate_output"), (self.validation, "finalize_output"),
                                 (self.camera, "resolve_camera")):
            if not callable(getattr(module, function, None)):
                self.__exit__(None, None, None)
                raise TypeError(f"frozen runtime lacks callable {function}")
        return self

    def __exit__(self, *args: Any) -> None:
        for name in list(sys.modules):
            if name == self.package or name.startswith(self.package + "."):
                sys.modules.pop(name, None)


def verify_terminal_run(source_dir: Path, source_manifest: dict[str, Any]) -> dict[str, Any]:
    run_complete_path = source_dir / "run_complete.json"
    run_complete = load_json(run_complete_path)
    case_ids = source_manifest["authorized_text_case_ids"]
    if set((run_complete.get("cases") or {})) != set(case_ids) or run_complete.get("case_count") != 16:
        raise ValueError("source run_complete.json does not cover all 16 registered banks")
    for case_id in case_ids:
        process = load_json(source_dir / "call_journals" / f"{case_id}.process.json")
        if run_complete["cases"][case_id] != process:
            raise ValueError(f"{case_id}: run_complete terminal record differs from process journal")
    return {"path": str(run_complete_path), "sha256": sha256_path(run_complete_path),
            "source_all_processes_succeeded": run_complete.get("all_processes_succeeded"),
            "source_process_successes": run_complete.get("process_successes"),
            "source_process_failures": run_complete.get("process_failures")}


def verify_source_audit_assets(source_dir: Path, case_id: str, source_input: dict[str, Any], result: dict[str, Any]) -> None:
    runtime = source_dir / "runtime/v6_2"
    audit = result.get("audit") or {}
    if audit.get("source_input") != source_input:
        raise ValueError(f"{case_id}: result audit source input differs from frozen bank input")
    system_path = runtime / "system_prompt.md"
    system = audit.get("system") or {}
    if system.get("sha256") != sha256_path(system_path) or system.get("character_count") != len(system_path.read_text(encoding="utf-8")):
        raise ValueError(f"{case_id}: result audit system prompt provenance is invalid")
    schema = audit.get("schema") or {}
    if (schema.get("input_sha256") != canonical_sha256(load_json(runtime / "input.schema.json"))
            or schema.get("base_model_output_sha256") != canonical_sha256(load_json(runtime / "model_output.schema.json"))):
        raise ValueError(f"{case_id}: result audit schema provenance is invalid")
    catalog = audit.get("catalog") or {}
    if catalog.get("catalog_sha256") != canonical_sha256(load_json(runtime / "approved_catalog.json")):
        raise ValueError(f"{case_id}: result audit catalog provenance is invalid")
    assets = audit.get("assets") or {}
    expected_assets = {
        "camera_registry_sha256": canonical_sha256(load_json(runtime / "camera_profiles.json")),
        "reference_library_sha256": canonical_sha256(load_json(runtime / "reference_library.json")),
        "prop_lexicon_sha256": sha256_path(runtime / "prop_lexicon.json"),
    }
    if assets != expected_assets:
        raise ValueError(f"{case_id}: result audit runtime asset provenance is invalid")


def verify_journals(source_dir: Path, case_id: str, result_path: Path, result: dict[str, Any]) -> dict[str, Any]:
    launch_path = source_dir / "call_journals" / f"{case_id}.launch.json"
    process_path = source_dir / "call_journals" / f"{case_id}.process.json"
    launch, process = load_json(launch_path), load_json(process_path)
    if launch.get("case_id") != case_id or process.get("case_id") != case_id:
        raise ValueError(f"{case_id}: launch/process journal case ID mismatch")
    input_path = source_dir / "inputs" / f"{case_id}.json"
    catalog_path = source_dir / "runtime/v6_2/approved_catalog.json"
    cli_path = source_dir / "runtime/v6_2/cli.py"
    if (launch.get("recorded_before_provider_process_start") is not True
            or launch.get("input_sha256") != sha256_path(input_path)
            or launch.get("catalog_sha256") != sha256_path(catalog_path)
            or launch.get("runtime_cli_sha256") != sha256_path(cli_path)):
        raise ValueError(f"{case_id}: launch journal no longer matches frozen input/catalog/runtime")
    result_hash = sha256_path(result_path)
    if process.get("output_exists") is not True or process.get("output_sha256") != result_hash:
        raise ValueError(f"{case_id}: process journal does not match terminal result bytes")
    attempts = (result.get("audit") or {}).get("attempts")
    if not isinstance(attempts, list) or len(attempts) not in {1, 2}:
        raise ValueError(f"{case_id}: terminal result must contain one initial and at most one repair attempt")
    journal_dir = result_path.with_name(result_path.name + ".run")
    expected_names = {f"attempt_{number}.{kind}.json" for number in range(1, len(attempts) + 1)
                      for kind in ("request", "response")}
    actual_names = {path.name for path in journal_dir.iterdir() if path.is_file()} if journal_dir.is_dir() else set()
    if actual_names != expected_names:
        raise ValueError(f"{case_id}: raw request/response journal set is incomplete or has extras")
    records = []
    transport_total = 0
    for number, attempt in enumerate(attempts, start=1):
        if attempt.get("number") != number or attempt.get("kind") not in ({"initial"} if number == 1 else {"semantic_repair"}):
            raise ValueError(f"{case_id}: attempt numbering/kind is invalid")
        request_path = journal_dir / f"attempt_{number}.request.json"
        response_path = journal_dir / f"attempt_{number}.response.json"
        request, response = load_json(request_path), load_json(response_path)
        if not isinstance(request.get("messages"), list) or not isinstance(request.get("schema"), dict):
            raise ValueError(f"{case_id}: raw request journal {number} is malformed")
        if canonical_sha256(request["schema"]) != (result["audit"].get("schema") or {}).get("effective_model_output_sha256"):
            raise ValueError(f"{case_id}: raw request schema differs from the audited effective schema")
        if response.get("content") != attempt.get("raw_content"):
            raise ValueError(f"{case_id}: raw response content differs from result audit attempt {number}")
        provider = attempt.get("provider") or {}
        for field in ("model", "finish_reason", "usage", "transport_attempts", "transport_events", "settings"):
            if response.get(field) != provider.get(field):
                raise ValueError(f"{case_id}: raw response/provider metadata differs at attempt {number} {field}")
        if not isinstance(attempt.get("parsed_output"), dict) or not isinstance(attempt.get("normalized_output"), dict):
            raise ValueError(f"{case_id}: attempt {number} lacks parsed/normalized output")
        transport_total += provider.get("transport_attempts", 0)
        records.append({
            "number": number, "kind": attempt["kind"], "errors": copy.deepcopy(attempt.get("errors") or []),
            "normalization_changes": copy.deepcopy(attempt.get("normalization_changes") or []),
            "text_changes": copy.deepcopy(attempt.get("text_changes")), "provider": copy.deepcopy(provider),
            "raw_content_sha256": sha256_bytes(attempt["raw_content"].encode("utf-8")),
            "parsed_output_sha256": canonical_sha256(attempt["parsed_output"]),
            "normalized_output_sha256": canonical_sha256(attempt["normalized_output"]),
            "request": {"path": str(request_path), "sha256": sha256_path(request_path), "bytes": request_path.stat().st_size},
            "response": {"path": str(response_path), "sha256": sha256_path(response_path), "bytes": response_path.stat().st_size},
        })
    audit = result["audit"]
    if (audit.get("semantic_calls") != len(attempts) or audit.get("transport_accounting_complete") is not True
            or audit.get("transport_attempts_known") != transport_total):
        raise ValueError(f"{case_id}: semantic/transport accounting is incomplete")
    return {
        "launch": {"path": str(launch_path), "sha256": sha256_path(launch_path)},
        "process": {"path": str(process_path), "sha256": sha256_path(process_path),
                    "returncode": process.get("returncode")},
        "attempt_count": len(attempts), "attempts": records,
    }


def _model_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(candidate[key]) for key in MODEL_PROMPT_FIELDS if key in candidate}


def verify_finalization(normalized: dict[str, Any], finalized: dict[str, Any], case_id: str) -> dict[str, Any]:
    raw_prompts, final_prompts = normalized.get("prompts"), finalized.get("prompts")
    if not isinstance(raw_prompts, list) or len(raw_prompts) != 10 or not isinstance(final_prompts, list) or len(final_prompts) != 10:
        raise ValueError(f"{case_id}: normalized/finalized output does not contain ten prompts")
    if any(set(candidate) != MODEL_PROMPT_FIELDS for candidate in raw_prompts):
        raise ValueError(f"{case_id}: final normalized_output does not match the frozen model prompt schema")
    if any(set(candidate) != MODEL_PROMPT_FIELDS | FINALIZER_PROMPT_FIELDS for candidate in final_prompts):
        raise ValueError(f"{case_id}: frozen finalizer added or removed an unexpected prompt field")
    raw_hashes = Counter(canonical_sha256(candidate) for candidate in raw_prompts)
    finalized_model_hashes = Counter(canonical_sha256(_model_payload(candidate)) for candidate in final_prompts)
    if raw_hashes != finalized_model_hashes:
        raise AssertionError(f"{case_id}: frozen finalizer changed model text/evidence/props/scores")
    if [item.get("id") for item in final_prompts] != [f"p{number}" for number in range(1, 11)]:
        raise ValueError(f"{case_id}: frozen finalizer did not assign p1 through p10")
    ranks = [(item.get("source_relevance_score"), item.get("ctech_reference_score")) for item in final_prompts]
    if ranks != sorted(ranks, reverse=True):
        raise ValueError(f"{case_id}: frozen finalizer rank order is invalid")
    raw_debug, final_debug = normalized.get("debug"), finalized.get("debug")
    if not isinstance(raw_debug, dict) or not isinstance(final_debug, dict):
        raise ValueError(f"{case_id}: normalized/finalized debug is missing")
    stripped_debug = copy.deepcopy(final_debug)
    stripped_debug.pop("primary_support_audit", None)
    stripped_debug.pop("provenance", None)
    if stripped_debug != raw_debug:
        raise AssertionError(f"{case_id}: frozen finalizer changed model-authored debug")
    if not isinstance(final_debug.get("primary_support_audit"), dict) or final_debug["primary_support_audit"].get("passed") is not True:
        raise ValueError(f"{case_id}: frozen finalizer has no passing primary-support audit")
    return {
        "model_candidate_multiset_sha256": canonical_sha256(sorted(raw_hashes.elements())),
        "finalized_model_candidate_multiset_sha256": canonical_sha256(sorted(finalized_model_hashes.elements())),
        "model_fields_unchanged": True, "model_debug_unchanged": True,
        "deterministic_fields_added": sorted(FINALIZER_PROMPT_FIELDS),
    }


def validate_export_document(document: dict[str, Any], expected: int, per_bank: int) -> None:
    prompts = document.get("prompts")
    if not isinstance(prompts, list) or len(prompts) != expected:
        raise ValueError(f"export has {len(prompts) if isinstance(prompts, list) else 'invalid'} prompts, expected {expected}")
    keys = [row.get("prompt_key") for row in prompts]
    if any(not isinstance(key, str) for key in keys) or len(set(keys)) != expected:
        raise ValueError("export prompt keys are missing or duplicated")
    counts = Counter(row.get("bank_debug_ref") for row in prompts)
    if len(counts) != 16 or set(counts.values()) != {per_bank}:
        raise ValueError("export bank coverage is invalid")
    for row in prompts:
        if row.get("prompt_key") != f"{row.get('bank_debug_ref')}::{row.get('id')}":
            raise ValueError("export prompt key/id/bank mapping is invalid")
        if row.get("text_sha256") != sha256_bytes(row["text"].encode("utf-8")):
            raise ValueError(f"{row.get('prompt_key')}: text hash mismatch")
    for bank_id in counts:
        bank_rows = [row for row in prompts if row["bank_debug_ref"] == bank_id]
        expected_ranks = set(range(1, per_bank + 1))
        if {row.get("bank_rank") for row in bank_rows} != expected_ranks or {row.get("id") for row in bank_rows} != {
            f"p{rank}" for rank in expected_ranks
        }:
            raise ValueError(f"{bank_id}: export ranks/IDs are not exactly 1 through {per_bank}")
    if set(document.get("bank_audit") or {}) != set(counts):
        raise ValueError("export bank_audit does not cover the exported banks")


def text_export(rows: list[dict[str, Any]]) -> str:
    return "\n\n".join(
        f"[{row['prompt_key']} | {row['device_display_name']} | {row['camera_tag']} | rank {row['bank_rank']} | "
        f"source {row['source_relevance_score']} | C-Tech {row['ctech_reference_score']}]\n{row['text']}"
        for row in rows
    ) + "\n"


def export_revalidated(source_dir: Path, validation_dir: Path, output_dir: Path) -> dict[str, Any]:
    source_dir, validation_dir, output_dir = source_dir.resolve(), validation_dir.resolve(), output_dir.resolve()
    if output_dir.exists():
        raise FileExistsError(f"immutable output directory already exists: {output_dir}")
    source_manifest, source_snapshot = verify_snapshot(source_dir, "source revision")
    validation_manifest, validation_snapshot = verify_snapshot(validation_dir, "validation snapshot")
    matching_inputs = verify_matching_inputs(source_dir, source_manifest, validation_dir, validation_manifest)
    terminal_run = verify_terminal_run(source_dir, source_manifest)

    runtime_dir = validation_dir / "runtime/v6_2"
    catalog = load_json(validation_dir / validation_manifest["catalog"]["frozen_path"])
    camera_registry = load_json(runtime_dir / "camera_profiles.json")
    references = load_json(runtime_dir / "reference_library.json")
    tool_path = Path(__file__).resolve()
    tool_record = {"path": str(tool_path), "sha256": sha256_path(tool_path)}
    cases = {item["case_id"]: item for item in source_manifest["cases"]}
    all_rows: list[dict[str, Any]] = []
    top_rows: list[dict[str, Any]] = []
    bank_audit: dict[str, Any] = {}
    failures: list[dict[str, Any]] = []

    with FrozenRuntime(validation_dir, validation_snapshot["manifest_sha256"]) as runtime:
        for case_id in source_manifest["authorized_text_case_ids"]:
            case = cases[case_id]
            result_path = source_dir / "results" / f"{case_id}.json"
            result = load_json(result_path)
            journal_record = verify_journals(source_dir, case_id, result_path, result)
            attempts = result["audit"]["attempts"]
            final_attempt = attempts[-1]
            normalized = final_attempt["normalized_output"]
            normalized_before = canonical_sha256(normalized)
            source_input_path = source_dir / case["frozen_input_path"]
            source_input = load_json(source_input_path)
            verify_source_audit_assets(source_dir, case_id, source_input, result)
            camera = runtime.camera.resolve_camera(camera_registry, case["camera_tag"])
            current_validation = runtime.validation.validate_output(normalized, source_input, catalog, camera, references)
            if canonical_sha256(normalized) != normalized_before:
                raise AssertionError(f"{case_id}: frozen validator mutated normalized_output")
            if not isinstance(current_validation, dict) or current_validation.get("passed") is not True:
                failures.append({"case_id": case_id, "source_status": result.get("status"),
                                 "final_attempt": len(attempts), "validation": current_validation})
                continue
            finalized = runtime.validation.finalize_output(normalized, camera=camera, catalog=catalog)
            if canonical_sha256(normalized) != normalized_before:
                raise AssertionError(f"{case_id}: frozen finalizer mutated normalized_output")
            finalization_invariants = verify_finalization(normalized, finalized, case_id)
            if len(finalized["prompts"]) != 10:
                raise ValueError(f"{case_id}: finalized prompt count is not ten")
            source_terminal_error = copy.deepcopy(result.get("error"))
            source_status = result.get("status")
            bank_audit[case_id] = {
                "selection_policy": "strict source-revision final actual attempt normalized_output only",
                "selected_attempt": len(attempts), "attempt_count": len(attempts),
                "selected_final_attempt_only": True, "earlier_attempt_selection_allowed": False,
                "fallback_revision_allowed": False, "retry_or_model_call_performed": False,
                "manual_prompt_edits": False, "additional_model_calls": 0,
                "case_metadata": copy.deepcopy(case),
                "source_input": copy.deepcopy(source_input),
                "source_input_path": str(source_input_path), "source_input_sha256": sha256_path(source_input_path),
                "source_terminal_result": {
                    "path": str(result_path), "sha256": sha256_path(result_path), "status": source_status,
                    "error": source_terminal_error,
                    "service_prompts_sha256": canonical_sha256(result.get("prompts")),
                    "service_debug_sha256": canonical_sha256(result.get("debug")),
                },
                "original_debug": copy.deepcopy(result.get("debug")),
                "debug": copy.deepcopy(finalized["debug"]),
                "recorded_attempts": journal_record["attempts"],
                "journals": {"launch": journal_record["launch"], "process": journal_record["process"]},
                "source_final_attempt_normalized_output_sha256": normalized_before,
                "frozen_revalidation": copy.deepcopy(current_validation),
                "frozen_revalidation_sha256": canonical_sha256(current_validation),
                "finalization_invariants": finalization_invariants,
            }
            for rank, candidate in enumerate(finalized["prompts"], start=1):
                row = {
                    "prompt_key": f"{case_id}::{candidate['id']}",
                    "device_id": case["device_id"], "device_display_name": case["device_display_name"],
                    "device_type": case["device_type"], "source_pair": case["source_pair"],
                    "camera_tag": case["camera_tag"], "source_camera_name": case["source_camera_name"],
                    "view_role": case["view_role"], "render_gallery_url": case["render_gallery_url"],
                    "render_lookup": copy.deepcopy(case["render_lookup"]), "bank_rank": rank,
                    **copy.deepcopy(candidate), "text_sha256": sha256_bytes(candidate["text"].encode("utf-8")),
                    "bank_debug_ref": case_id,
                }
                all_rows.append(row)
                if rank <= 6:
                    top_rows.append(copy.deepcopy(row))

    if failures:
        raise ValueError(f"frozen revalidation failed for {len(failures)} bank(s): {json.dumps(failures, ensure_ascii=False)}")
    if len(bank_audit) != 16 or len(all_rows) != 160 or len(top_rows) != 96:
        raise ValueError("strict export is incomplete after frozen revalidation")

    provenance = {
        "kind": "deterministic_revalidation_of_recorded_gpt_final_normalized_outputs",
        "source_policy": "each registered bank's final actual attempt normalized_output; no older attempt or revision",
        "source_revision": source_snapshot, "validation_snapshot": validation_snapshot,
        "terminal_run": terminal_run, "matching_source_inputs": matching_inputs,
        "validation_runtime": {
            name: {"path": str(runtime_dir / name), "sha256": sha256_path(runtime_dir / name)}
            for name in ("validation.py", "surfaces.py", "content_policy.py", "camera.py", "catalog.py",
                         "model_output.schema.json", "camera_profiles.json", "reference_library.json",
                         "approved_catalog.json")
        },
        "utility": tool_record, "manual_prompt_edits": False, "additional_model_calls": 0,
        "source_service_acceptance_recomputed": False,
        "note": "Passing frozen revalidation is deterministic export qualification, not an assertion that the original service accepted the bank.",
    }
    shared = {
        "revision": output_dir.name, "source_revision": source_manifest["revision"],
        "validation_revision": validation_manifest["revision"],
        "selection_rule": source_manifest["scope"]["selection_rule"],
        "device_source_mapping": copy.deepcopy(source_manifest["device_source_mapping"]),
        "bank_audit": bank_audit, "provenance": provenance,
    }
    all_output = {
        "version": "hp-lifestyle-spatial-composition-v6.2-all-four-devices-v1", **copy.deepcopy(shared),
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16, "candidates_per_bank": 10, "prompts": 160},
        "prompts": all_rows,
    }
    top_output = {
        "version": "hp-lifestyle-spatial-composition-v6.2-top6-four-devices-v1", **copy.deepcopy(shared),
        "counts": {"devices": 4, "views_per_device": 4, "banks": 16, "selected_per_bank": 6, "prompts": 96},
        "prompts": top_rows,
    }
    validate_export_document(all_output, 160, 10)
    validate_export_document(top_output, 96, 6)

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.", dir=output_dir.parent))
    try:
        write_json(stage / "prompts_all_160.json", all_output)
        write_text(stage / "prompts_all_160.txt", text_export(all_rows))
        write_json(stage / "prompts_top6_96.json", top_output)
        write_text(stage / "prompts_top6_96.txt", text_export(top_rows))
        # Independent parse and semantic verification from serialized bytes.
        parsed_all, parsed_top = load_json(stage / "prompts_all_160.json"), load_json(stage / "prompts_top6_96.json")
        validate_export_document(parsed_all, 160, 10)
        validate_export_document(parsed_top, 96, 6)
        if parsed_all != all_output or parsed_top != top_output:
            raise AssertionError("serialized export does not round-trip exactly")
        if parsed_top["prompts"] != [row for row in parsed_all["prompts"] if row["bank_rank"] <= 6]:
            raise AssertionError("serialized top-six export is not the exact rank<=6 subset")
        artifact_names = ("prompts_all_160.json", "prompts_all_160.txt", "prompts_top6_96.json", "prompts_top6_96.txt")
        validation = {
            "schema_version": "hp-v6.2-strict-final-attempt-revalidation-export-v1", "passed": True,
            "checks": {
                "source_snapshot_integrity": True, "validation_snapshot_integrity": True,
                "all_16_source_inputs_byte_identical": True, "terminal_run_covers_all_16_banks": True,
                "all_raw_request_response_journals_verified": True,
                "selected_only_each_final_actual_attempt_normalized_output": True,
                "all_16_banks_pass_frozen_revalidation": True, "all_model_fields_unchanged_by_finalizer": True,
                "no_manual_prompt_edits": True, "no_additional_model_calls": True,
                "all_160_and_top6_96_round_trip": True,
            },
            "source_status_counts": dict(sorted(Counter(item["source_terminal_result"]["status"] for item in bank_audit.values()).items())),
            "bank_validation_sha256": {case_id: item["frozen_revalidation_sha256"] for case_id, item in bank_audit.items()},
            "files": {name: {"sha256": sha256_path(stage / name), "bytes": (stage / name).stat().st_size}
                      for name in artifact_names},
        }
        write_json(stage / "validation.json", validation)
        os.replace(stage, output_dir)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return {"output": str(output_dir), "prompts": 160, "top6": 96, "banks": 16,
            "source_status_counts": validation["source_status_counts"],
            "validation_sha256": sha256_path(output_dir / "validation.json")}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-revision", type=Path, required=True)
    parser.add_argument("--validation-snapshot", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True, help="must not exist")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(json.dumps(export_revalidated(args.source_revision, args.validation_snapshot, args.output_dir), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
