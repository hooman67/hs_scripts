#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml", "tomli", "jsonschema"]
# ///
"""Run selected V4 GPT-5.5 banks with transient-only retries and immutable raw records."""

from __future__ import annotations

import argparse
import hashlib
import json
import importlib.util
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCRIPTS = ROOT / "research/source_messaging_v1_to_v6/versions/v4/scripts"
V4 = SCRIPTS.parent
sys.path.insert(0, str(ROOT / "research/source_messaging_v1_to_v6/scripts"))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SCRIPTS))
from probe_gpt55 import client_and_auth_mode  # noqa: E402
from finalize_output import finalize_output, semantic_sha256  # noqa: E402
from validate_output import validate_output  # noqa: E402

from camera_profile_resolver import load_registry  # noqa: E402

_SHARED_RUNNER_PATH = ROOT / "research/source_messaging_v1_to_v6/scripts/run_gpt55.py"
_spec = importlib.util.spec_from_file_location("shared_gpt55_runner", _SHARED_RUNNER_PATH)
_shared = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_shared)
checkpoint, retry_delay, transient = _shared.checkpoint, _shared.retry_delay, _shared.transient


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_obj(value) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                separators=(",", ":")).encode())


def derive_artifacts(case_id, target, record, raw_input, schema, registry, request_hash):
    """Create reproducible sidecars while leaving the raw record byte-for-byte unchanged."""
    parsed = record["parsed_output"]
    raw_record_sha256 = sha_bytes(target.read_bytes())
    sample_name = target.stem
    raw_validation = validate_output(parsed, raw_input, schema, registry)
    normalized, normalization_log = finalize_output(parsed, raw_input=raw_input, registry=registry)
    normalized_validation = validate_output(normalized, raw_input, schema, registry)
    artifact_stem = f"{case_id}__{sample_name}"
    normalized_path = HERE / "normalized_outputs" / f"{artifact_stem}.json"
    log_path = HERE / "normalization_logs" / f"{artifact_stem}.json"
    raw_validation_path = HERE / "validation/raw" / f"{artifact_stem}.json"
    normalized_validation_path = HERE / "validation/normalized" / f"{artifact_stem}.json"
    for path, value in ((normalized_path, normalized), (log_path, normalization_log),
                        (raw_validation_path, raw_validation),
                        (normalized_validation_path, normalized_validation)):
        path.parent.mkdir(parents=True, exist_ok=True)
        checkpoint(path, value)
    validation = {"version": "v4-raw-normalized-audit-v1", "case_id": case_id,
        "request_sha256": request_hash, "record_path": str(target),
        "raw_record_sha256": raw_record_sha256,
        "raw_validation": raw_validation, "normalized_validation": normalized_validation,
        "normalized_output_path": str(normalized_path),
        "normalized_output_file_sha256": sha_bytes(normalized_path.read_bytes()),
        "normalized_output_semantic_sha256": semantic_sha256(normalized),
        "normalization_log_path": str(log_path),
        "normalization_log_file_sha256": sha_bytes(log_path.read_bytes())}
    validation_path = HERE / "validation" / f"{case_id}.json"
    checkpoint(validation_path, validation)
    effective_status = ("normalized_validator_passed_pending_human_review"
                        if normalized_validation["passed"] else "normalized_validator_rejected")
    return {"status": effective_status, "elapsed_seconds": record.get("elapsed_seconds"),
            "record_path": str(target), "raw_record_sha256": raw_record_sha256}


def run_case(case, manifest, client, auth_mode, system, schema, registry, max_attempts,
             force_new_attempt=False):
    case_id = case["case_id"]
    input_path = Path(case["input_path"])
    raw_input_bytes = input_path.read_bytes()
    if sha_bytes(raw_input_bytes) != case["input_sha256"]:
        raise RuntimeError(f"input hash changed: {case_id}")
    raw_input = json.loads(raw_input_bytes)
    settings = {"model": "gpt-5.5", "reasoning_effort": "medium",
                "max_completion_tokens": 24000}
    request_hash = sha_obj({"system_sha256": sha_bytes(system.encode()),
                            "schema": schema, "settings": settings,
                            "input_sha256": case["input_sha256"]})
    attempt_dir = HERE / "records/attempts" / case_id
    attempt_dir.mkdir(parents=True, exist_ok=True)
    previous_attempts = sorted(attempt_dir.glob("sample_[0-9][0-9][0-9].json"))
    for prior_path in previous_attempts:
        old = json.loads(prior_path.read_text())
        if old.get("request_sha256") == request_hash and not force_new_attempt:
            if old.get("parsed_output") is not None:
                return case_id, derive_artifacts(case_id, prior_path, old, raw_input, schema,
                                                  registry, request_hash)
            return case_id, old
    target = attempt_dir / f"sample_{len(previous_attempts)+1:03d}.json"
    record = {
        "version": "v4-gpt55-attempt-v2", "case_id": case_id,
        "group_id": case["group_id"], "semantic_attempt": 1,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "request_sha256": request_hash, "input_path": str(input_path),
        "input_sha256": case["input_sha256"], "raw_input_json": raw_input_bytes.decode(),
        "system_prompt_path": manifest["provenance"]["system_prompt"]["path"],
        "system_prompt_sha256": manifest["provenance"]["system_prompt"]["sha256"],
        "output_schema_path": manifest["provenance"]["output_schema"]["path"],
        "output_schema_sha256": manifest["provenance"]["output_schema"]["sha256"],
        "settings": settings, "auth_mode": auth_mode, "retry_events": [],
    }
    started = time.monotonic()
    for transport_attempt in range(1, max_attempts + 1):
        try:
            response = client.chat.completions.create(
                **settings,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": raw_input_bytes.decode()}],
                response_format={"type": "json_schema", "json_schema": {
                    "name": "hp_lifestyle_lived_in_v4", "strict": True, "schema": schema}},
            )
            record["response"] = response.model_dump(mode="json")
            record["completed_at"] = datetime.now(timezone.utc).isoformat()
            record["elapsed_seconds"] = round(time.monotonic() - started, 3)
            record["transport_attempts"] = transport_attempt
            checkpoint(target, record)  # preserve provider response before parsing/validation
            if not response.model.startswith("gpt-5.5") or response.choices[0].finish_reason != "stop":
                raise RuntimeError("unexpected model or incomplete successful response")
            parsed = json.loads(response.choices[0].message.content or "")
            record["parsed_output"] = parsed
            record["parsed_output_sha256"] = sha_obj(parsed)
            record["status"] = "raw_response_preserved_pending_derived_audit"
            checkpoint(target, record)
            return case_id, derive_artifacts(case_id, target, record, raw_input, schema,
                                              registry, request_hash)
        except Exception as exc:
            if record.get("response") or not transient(exc) or transport_attempt == max_attempts:
                record["status"] = "failed_preserved"
                record["failure"] = {"type": type(exc).__name__,
                                     "status_code": getattr(exc, "status_code", None),
                                     "transport_attempt": transport_attempt,
                                     "detail": str(exc)[:1200]}
                record["elapsed_seconds"] = round(time.monotonic() - started, 3)
                checkpoint(target, record)
                return case_id, record
            delay = retry_delay(exc, transport_attempt)
            record["retry_events"].append({"transport_attempt": transport_attempt,
                "type": type(exc).__name__, "status_code": getattr(exc, "status_code", None),
                "wait_seconds": delay})
            checkpoint(attempt_dir / "sample_001.pending.json", record)
            time.sleep(delay)
    raise AssertionError("unreachable")


def rebuild_accepted(manifest):
    cases = {}
    status_counts = {}
    effective_by_case = {}
    overrides_path = HERE / "manual_review_overrides.json"
    overrides = json.loads(overrides_path.read_text()) if overrides_path.exists() else {"rejected_attempts": []}
    rejected_raw_hashes = {item["raw_record_sha256"]: item for item in overrides["rejected_attempts"]}
    manifest_cases = {c["case_id"]: c for c in manifest["cases"]}
    for case_id, case in manifest_cases.items():
        attempts = sorted((HERE / "records/attempts" / case_id).glob("sample_[0-9][0-9][0-9].json"))
        current_schema = json.loads((V4 / "output.schema.json").read_text())
        registry = load_registry(V4 / "camera_profiles.json")
        raw_input = json.loads(Path(case["input_path"]).read_text())
        settings = {"model": "gpt-5.5", "reasoning_effort": "medium", "max_completion_tokens": 24000}
        expected_request = sha_obj({"system_sha256": manifest["provenance"]["system_prompt"]["sha256"],
                                    "schema": current_schema, "settings": settings,
                                    "input_sha256": case["input_sha256"]})
        eligible = []
        for path in attempts:
            candidate_record = json.loads(path.read_text())
            if not (candidate_record.get("request_sha256") == expected_request
                    and candidate_record.get("input_sha256") == case["input_sha256"]
                    and candidate_record.get("system_prompt_sha256") == manifest["provenance"]["system_prompt"]["sha256"]
                    and candidate_record.get("output_schema_sha256") == manifest["provenance"]["output_schema"]["sha256"]
                    and candidate_record.get("parsed_output_sha256") == sha_obj(candidate_record.get("parsed_output"))):
                continue
            audit_path = HERE / "validation" / f"{case_id}.json"
            if not audit_path.exists():
                continue
            audit = json.loads(audit_path.read_text())
            if audit.get("record_path") != str(path) or audit.get("raw_record_sha256") != sha_bytes(path.read_bytes()):
                continue
            if sha_bytes(path.read_bytes()) in rejected_raw_hashes:
                continue
            normalized_path = Path(audit["normalized_output_path"])
            log_path = Path(audit["normalization_log_path"])
            if not normalized_path.exists() or not log_path.exists():
                continue
            normalized = json.loads(normalized_path.read_text())
            log = json.loads(log_path.read_text())
            rebuilt, rebuilt_log = finalize_output(candidate_record["parsed_output"],
                                                    raw_input=raw_input, registry=registry)
            current_validation = validate_output(normalized, raw_input, current_schema, registry)
            if (normalized != rebuilt or log != rebuilt_log
                    or audit.get("normalized_output_file_sha256") != sha_bytes(normalized_path.read_bytes())
                    or audit.get("normalization_log_file_sha256") != sha_bytes(log_path.read_bytes())
                    or audit.get("normalized_output_semantic_sha256") != semantic_sha256(normalized)
                    or not current_validation["passed"]):
                continue
            eligible.append((path, candidate_record, normalized_path, normalized, log_path, log,
                             audit_path, current_validation))
        if not eligible:
            current_attempts = [json.loads(p.read_text()) for p in attempts
                                if json.loads(p.read_text()).get("request_sha256") == expected_request]
            current_paths = [p for p in attempts if json.loads(p.read_text()).get("request_sha256") == expected_request]
            status = current_attempts[-1].get("status", "pending_derived_audit") if current_attempts else "pending"
            if current_paths and sha_bytes(current_paths[-1].read_bytes()) in rejected_raw_hashes:
                status = rejected_raw_hashes[sha_bytes(current_paths[-1].read_bytes())]["decision"]
            else:
                audit_path = HERE / "validation" / f"{case_id}.json"
                if audit_path.exists():
                    audit = json.loads(audit_path.read_text())
                    if (current_paths and audit.get("record_path") == str(current_paths[-1])
                            and audit.get("normalized_validation", {}).get("passed") is False):
                        status = "normalized_validator_rejected"
            effective_by_case[case_id] = status
            status_counts[status] = status_counts.get(status, 0) + 1
            continue
        record_path, record, normalized_path, output, log_path, log, audit_path, current_validation = eligible[-1]
        effective_status = "normalized_validator_passed_pending_human_review"
        effective_by_case[case_id] = effective_status
        status_counts[effective_status] = status_counts.get(effective_status, 0) + 1
        enriched = []
        for rank, candidate in enumerate(output["prompts"], 1):
            row = {"candidate_key": f"{case_id}::{candidate['id']}", "rank": rank,
                   "rank_bin": "1-10" if rank <= 10 else "11-20" if rank <= 20 else "21-30",
                   "text_sha256": sha_bytes(candidate["text"].encode()), **candidate}
            enriched.append(row)
        cases[case_id] = {
            "case_id": case_id, "group_id": case["group_id"], "source_id": case["source_id"],
            "device_type": case["device_type"], "camera_tag": case["camera_tag"],
            "view_role": case["view_role"], "render_id": case["render_id"],
            "input_path": case["input_path"], "input_sha256": case["input_sha256"],
            "record_path": str(record_path), "record_sha256": sha_bytes(record_path.read_bytes()),
            "raw_parsed_output_sha256": record["parsed_output_sha256"],
            "normalized_output_path": str(normalized_path),
            "normalized_output_file_sha256": sha_bytes(normalized_path.read_bytes()),
            "normalized_output_semantic_sha256": semantic_sha256(output),
            "normalization_log_path": str(log_path),
            "normalization_log_file_sha256": sha_bytes(log_path.read_bytes()),
            "validation_audit_path": str(audit_path),
            "raw_record_status": record.get("status"),
            "status": effective_status, "human_review_status": "pending_root_review",
            "launchable": False,
            "rejected_attempts": [item for item in overrides["rejected_attempts"]
                                  if item["case_id"] == case_id],
            "candidates": enriched, "debug": output["debug"],
        }
    doc = {
        "version": "v4-accepted-prompt-cases-v1-normalized",
        "status": "progressive_human_review_required" if len(cases) < len(manifest["cases"]) else "complete_human_review_required",
        "manifest_path": str(HERE / "manifest.json"),
        "manifest_sha256": sha_bytes((HERE / "manifest.json").read_bytes()),
        "selection_status": "not_yet_performed",
        "counts": {"manifest_cases": len(manifest["cases"]), "accepted_cases": len(cases),
                   "status_counts": status_counts, "candidates": len(cases) * 30},
        "cases": cases,
    }
    checkpoint(HERE / "accepted_prompt_cases.json", doc)
    statuses = {}
    counts = {"total": len(manifest["cases"]), "pending": 0,
              "accepted": 0, "rejected_semantic": 0, "failed_preserved": 0}
    for case in manifest["cases"]:
        case_id = case["case_id"]
        record_paths = sorted((HERE / "records/attempts" / case_id).glob("sample_[0-9][0-9][0-9].json"))
        status = effective_by_case.get(case_id, "pending")
        counts[status] = counts.get(status, 0) + 1
        statuses[case_id] = {"case_id": case_id, "group_id": case["group_id"],
            "source_id": case["source_id"], "camera_tag": case["camera_tag"],
            "view_role": case["view_role"], "status": status}
    checkpoint(HERE / "status_inventory.json", {"version": "v4-status-inventory-v2",
        "manifest_sha256": sha_bytes((HERE / "manifest.json").read_bytes()),
        "counts": counts, "cases": statuses})
    return doc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append")
    parser.add_argument("--replacement-case", action="append")
    parser.add_argument("--all-authorized", action="store_true")
    parser.add_argument("--rebuild-only", action="store_true")
    parser.add_argument("--max-concurrency", type=int, default=2)
    parser.add_argument("--max-transient-attempts", type=int, default=100)
    args = parser.parse_args()
    manifest = json.loads((HERE / "manifest.json").read_text())
    if args.rebuild_only:
        print(json.dumps(rebuild_accepted(manifest)["counts"], indent=2))
        return
    allowed = set(manifest["authorized_text_case_ids"])
    replacements = set(args.replacement_case or [])
    requested = allowed if args.all_authorized else set(args.case or []) | replacements
    if not requested:
        parser.error("--case or --all-authorized is required unless --rebuild-only is used")
    if not requested <= allowed:
        raise SystemExit(f"only authorized probe cases may run; rejected: {sorted(requested-allowed)}")
    if replacements:
        overrides = json.loads((HERE / "manual_review_overrides.json").read_text())
        authorized_replacements = {x["case_id"] for x in overrides["rejected_attempts"]
                                   if x.get("authorized_replacement_attempt") is True}
        if not replacements <= authorized_replacements:
            raise SystemExit(f"replacement not authorized: {sorted(replacements-authorized_replacements)}")
    cases_by_id = {c["case_id"]: c for c in manifest["cases"]}
    system = (V4 / "system_prompt.md").read_text()
    schema = json.loads((V4 / "output.schema.json").read_text())
    registry = load_registry(V4 / "camera_profiles.json")
    for key, local in (("system_prompt", V4 / "system_prompt.md"),
                       ("output_schema", V4 / "output.schema.json"),
                       ("camera_profiles", V4 / "camera_profiles.json")):
        if sha_bytes(local.read_bytes()) != manifest["provenance"][key]["sha256"]:
            raise SystemExit(f"provenance changed: {key}; rebuild manifest before any call")
    client, auth_mode = client_and_auth_mode()
    results = []
    with ThreadPoolExecutor(max_workers=min(args.max_concurrency, 2)) as pool:
        futures = {pool.submit(run_case, cases_by_id[cid], manifest, client, auth_mode,
                               system, schema, registry, args.max_transient_attempts,
                               cid in replacements): cid
                   for cid in sorted(requested)}
        for future in as_completed(futures):
            case_id, record = future.result()
            results.append({"case_id": case_id, "status": record.get("status"),
                            "elapsed_seconds": record.get("elapsed_seconds")})
            accepted = rebuild_accepted(manifest)
            print(json.dumps({"completed": results[-1], "accepted_count": accepted["counts"]["accepted_cases"]}), flush=True)
    raise SystemExit(0 if all(r["status"] == "validator_passed_pending_human_review" for r in results) else 2)


if __name__ == "__main__":
    main()

