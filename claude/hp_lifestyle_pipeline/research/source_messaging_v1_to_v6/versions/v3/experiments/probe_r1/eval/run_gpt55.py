#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml", "tomli", "jsonschema"]
# ///
"""Run selected V3 GPT-5.5 banks with transient-only retries and immutable raw records."""

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
sys.path.insert(0, str(ROOT / "research/source_messaging/scripts"))
sys.path.insert(0, str(HERE))
from probe_gpt55 import client_and_auth_mode  # noqa: E402
from validate_output import validate_output  # noqa: E402

SCRIPTS = ROOT / "research/source_messaging/versions/v3/scripts"
V3 = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
from camera_profile_resolver import load_registry  # noqa: E402

_SHARED_RUNNER_PATH = ROOT / "research/source_messaging/scripts/run_gpt55.py"
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


def run_case(case, manifest, client, auth_mode, system, schema, registry, max_attempts):
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
        if old.get("request_sha256") == request_hash:
            return case_id, old
    target = attempt_dir / f"sample_{len(previous_attempts)+1:03d}.json"
    record = {
        "version": "v3-gpt55-attempt-v1", "case_id": case_id,
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
                    "name": "hp_lifestyle_diversity_v3", "strict": True, "schema": schema}},
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
            validation = validate_output(parsed, raw_input, schema, registry)
            validation.update({"case_id": case_id, "request_sha256": request_hash,
                               "record_path": str(target)})
            validation_path = HERE / "validation" / f"{case_id}.json"
            checkpoint(validation_path, validation)
            record["schema_valid"] = not any(e["code"] == "schema_invalid" for e in validation["errors"])
            record["semantic_validation_passed"] = validation["passed"]
            record["validation_path"] = str(validation_path)
            record["status"] = ("validator_passed_pending_human_review" if validation["passed"]
                                else "validator_rejected")
            checkpoint(target, record)
            return case_id, record
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
    manifest_cases = {c["case_id"]: c for c in manifest["cases"]}
    for case_id, case in manifest_cases.items():
        attempts = sorted((HERE / "records/attempts" / case_id).glob("sample_[0-9][0-9][0-9].json"))
        if attempts:
            latest_status = json.loads(attempts[-1].read_text()).get("status", "unknown")
            status_counts[latest_status] = status_counts.get(latest_status, 0) + 1
        current_schema = json.loads((HERE / "output.schema.json").read_text())
        settings = {"model": "gpt-5.5", "reasoning_effort": "medium", "max_completion_tokens": 24000}
        expected_request = sha_obj({"system_sha256": manifest["provenance"]["system_prompt"]["sha256"],
                                    "schema": current_schema, "settings": settings,
                                    "input_sha256": case["input_sha256"]})
        eligible = []
        for path in attempts:
            candidate_record = json.loads(path.read_text())
            if (candidate_record.get("request_sha256") == expected_request
                    and candidate_record.get("input_sha256") == case["input_sha256"]
                    and candidate_record.get("system_prompt_sha256") == manifest["provenance"]["system_prompt"]["sha256"]
                    and candidate_record.get("output_schema_sha256") == manifest["provenance"]["output_schema"]["sha256"]
                    and candidate_record.get("parsed_output_sha256") == sha_obj(candidate_record.get("parsed_output"))
                    and candidate_record.get("semantic_validation_passed") is True):
                eligible.append((path, candidate_record))
        if not eligible:
            continue
        record_path, record = eligible[-1]
        if record.get("status") != "validator_passed_pending_human_review":
            continue
        output = record["parsed_output"]
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
            "parsed_output_sha256": record["parsed_output_sha256"],
            "status": "validator_passed_pending_human_review", "launchable": False,
            "candidates": enriched, "debug": output["debug"],
        }
    doc = {
        "version": "v3-accepted-prompt-cases-v1",
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
        status = "pending"
        if record_paths:
            status = json.loads(record_paths[-1].read_text()).get("status", "pending")
        counts[status] = counts.get(status, 0) + 1
        statuses[case_id] = {"case_id": case_id, "group_id": case["group_id"],
            "source_id": case["source_id"], "camera_tag": case["camera_tag"],
            "view_role": case["view_role"], "status": status}
    checkpoint(HERE / "status_inventory.json", {"version": "v3-status-inventory-v1",
        "manifest_sha256": sha_bytes((HERE / "manifest.json").read_bytes()),
        "counts": counts, "cases": statuses})
    return doc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append")
    parser.add_argument("--rebuild-only", action="store_true")
    parser.add_argument("--max-concurrency", type=int, default=2)
    parser.add_argument("--max-transient-attempts", type=int, default=100)
    args = parser.parse_args()
    manifest = json.loads((HERE / "manifest.json").read_text())
    if args.rebuild_only:
        print(json.dumps(rebuild_accepted(manifest)["counts"], indent=2))
        return
    if not args.case:
        parser.error("--case is required unless --rebuild-only is used")
    allowed = set(manifest["authorized_probe_case_ids"])
    requested = set(args.case)
    if not requested <= allowed:
        raise SystemExit(f"only authorized probe cases may run; rejected: {sorted(requested-allowed)}")
    cases_by_id = {c["case_id"]: c for c in manifest["cases"]}
    system = (HERE / "system_prompt.md").read_text()
    schema = json.loads((HERE / "output.schema.json").read_text())
    registry = load_registry(V3 / "camera_profiles.json")
    for key, local in (("system_prompt", HERE / "system_prompt.md"),
                       ("output_schema", HERE / "output.schema.json"),
                       ("camera_profiles", V3 / "camera_profiles.json")):
        if sha_bytes(local.read_bytes()) != manifest["provenance"][key]["sha256"]:
            raise SystemExit(f"provenance changed: {key}; rebuild manifest before any call")
    client, auth_mode = client_and_auth_mode()
    results = []
    with ThreadPoolExecutor(max_workers=min(args.max_concurrency, 2)) as pool:
        futures = {pool.submit(run_case, cases_by_id[cid], manifest, client, auth_mode,
                               system, schema, registry, args.max_transient_attempts): cid
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
