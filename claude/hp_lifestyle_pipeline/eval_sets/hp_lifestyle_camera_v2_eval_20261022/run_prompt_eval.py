# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "requests", "pyyaml", "tomli", "jsonschema"]
# ///
"""Run, validate, and progressively accept the camera-V2 GPT-5.5 prompt eval."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVAL_ROOT = Path(__file__).resolve().parent
V2_ROOT = PROJECT_ROOT / "research/source_messaging_v1_to_v6/versions/v2"
V2_SCRIPTS = V2_ROOT / "scripts"
SOURCE_SCRIPTS = PROJECT_ROOT / "research/source_messaging_v1_to_v6/scripts"
sys.path.insert(0, str(V2_SCRIPTS))
sys.path.insert(0, str(SOURCE_SCRIPTS))

from citation_path_guard import normalize_citation_paths  # noqa: E402
from probe_gpt55 import client_and_auth_mode  # noqa: E402
from run_gpt55 import checkpoint, retry_delay, transient  # noqa: E402
from validate_camera_eval import (  # noqa: E402
    CAMERA_FIELDS,
    load_registry,
    validate_case,
)


SETTINGS = {
    "model": "gpt-5.5",
    "reasoning_effort": "medium",
    "max_completion_tokens": 8000,
}
FROZEN_SYSTEM_SHA256 = (
    "00912f74c3ef11dece81c7e3ba7792ffafdf9f3fb12a2330923dd16c75dbd65e"
)
SURFACE_OR_LIGHT_RE = re.compile(
    r"\b(?:surface|table|tabletop|worktable|desk|counter|worktop|credenza|nook|wood|wooden|"
    r"laminate|material|texture|light|lighting|daylight|sunlight|shadow|"
    r"tone|plain background|neutral background|simple background|subdued background|"
    r"backdrop|surround|surroundings|"
    r"uncluttered|clutter|local presentation|kept[- ]clear(?: local)? work area|"
    r"paperwork corner|orderly local office feel|"
    r"school preparation context without visible supplies|"
    r"to (?:merge|suggest|support|retain|combine|convey|reflect))\b",
    re.I,
)
PERSON_RE = re.compile(
    r"\b(?:person|people|coworker|colleague|student|teacher)\b|"
    r"\bhand\b(?!-(?:sketched|drawn|written|marked))",
    re.I,
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    checkpoint(path, value)


def load_context(manifest_path: Path) -> dict[str, Any]:
    manifest_raw = manifest_path.read_bytes()
    manifest = json.loads(manifest_raw)
    provenance = manifest["provenance"]
    paths = {
        "system_prompt_sha256": Path(provenance["system_prompt_path"]),
        "input_schema_sha256": Path(provenance["input_schema_path"]),
        "output_schema_sha256": Path(provenance["output_schema_path"]),
        "camera_profiles_sha256": Path(provenance["camera_profiles_path"]),
        "camera_catalog_sha256": Path(provenance["camera_catalog_path"]),
        "historical_source_category_sha256": Path(
            provenance["historical_source_category_path"]
        ),
    }
    for hash_field, path in paths.items():
        actual = file_sha256(path)
        if actual != provenance[hash_field]:
            raise RuntimeError(f"Frozen provenance changed: {path}")
    if provenance["system_prompt_sha256"] != FROZEN_SYSTEM_SHA256:
        raise RuntimeError("System prompt does not match the authorized frozen SHA-256")
    if manifest["model"] != {
        "deployment": "gpt-5.5",
        "reasoning_effort": "medium",
        "max_completion_tokens": 8000,
        "temperature": None,
        "strict_output_schema": True,
        "max_concurrency": 2,
        "max_transient_attempts": 100,
    }:
        raise RuntimeError("Manifest model contract changed")
    if manifest["counts"]["case_count"] != 369:
        raise RuntimeError("Manifest case count changed")
    if manifest["counts"]["source_render_pair_count"] != 729:
        raise RuntimeError("Manifest source-render pair count changed")
    for case in manifest["cases"]:
        input_path = Path(case["input_path"])
        if file_sha256(input_path) != case["input_sha256"]:
            raise RuntimeError(f"Case input changed: {case['case_id']}")
        request_input = json.loads(input_path.read_text(encoding="utf-8"))
        if set(request_input) != {"source_messaging", "camera_tag"}:
            raise RuntimeError(f"Unexpected runtime fields: {case['case_id']}")
        if request_input["camera_tag"] != case["camera_tag"]:
            raise RuntimeError(f"Camera tag mismatch: {case['case_id']}")
    system = paths["system_prompt_sha256"].read_text(encoding="utf-8")
    input_schema = json.loads(paths["input_schema_sha256"].read_text(encoding="utf-8"))
    output_schema = json.loads(
        paths["output_schema_sha256"].read_text(encoding="utf-8")
    )
    jsonschema.Draft202012Validator.check_schema(input_schema)
    jsonschema.Draft202012Validator.check_schema(output_schema)
    registry = load_registry(paths["camera_profiles_sha256"])
    return {
        "manifest": manifest,
        "manifest_path": manifest_path,
        "manifest_sha256": sha256_bytes(manifest_raw),
        "system": system,
        "input_schema": input_schema,
        "output_schema": output_schema,
        "registry": registry,
    }


def compatible_case(case: dict[str, Any]) -> dict[str, Any]:
    """Adapt the richer eval expectation to the shared validator contract."""

    value = copy.deepcopy(case)
    value["expected_camera"] = {
        field: case["expected_camera"][field] for field in CAMERA_FIELDS
    }
    return value


def density_flags(output: dict[str, Any], case: dict[str, Any]) -> list[dict[str, Any]]:
    """Flag likely density overages for manual review; do not rewrite prose."""

    expected = case["expected_camera"]
    ceiling = expected["max_local_props"] + expected["max_background_details"]
    people_policy = expected["people_policy"]
    additions = {
        item["prompt_id"]: item["details"]
        for item in output["debug"]["creative_additions"]
    }
    flags = []
    for prompt in output["prompts"]:
        details = additions.get(prompt["id"], [])
        countable = [detail for detail in details if not SURFACE_OR_LIGHT_RE.search(detail)]
        reasons = []
        if len(countable) > ceiling:
            reasons.append(
                f"creative-addition heuristic counts {len(countable)} details "
                f"against combined prop/background ceiling {ceiling}"
            )
        if people_policy == "omit" and PERSON_RE.search(prompt["text"]):
            reasons.append("people wording appears under an omit policy")
        if reasons:
            flags.append(
                {
                    "prompt_id": prompt["id"],
                    "reasons": reasons,
                    "countable_details": countable,
                    "profile": {
                        "framing": expected["framing"],
                        "max_local_props": expected["max_local_props"],
                        "max_background_details": expected[
                            "max_background_details"
                        ],
                        "people_policy": people_policy,
                    },
                }
            )
    return flags


def audit_record(
    record: dict[str, Any],
    case: dict[str, Any],
    output_schema: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    adapted = copy.deepcopy(record)
    adapted["case"] = compatible_case(case)
    raw = validate_case(adapted, output_schema, registry)
    guard = normalize_citation_paths(
        record["parsed_output"], record["request_input"]["source_messaging"]
    )
    normalized = copy.deepcopy(adapted)
    normalized["parsed_output"] = guard["validated_output"]
    validated = validate_case(normalized, output_schema, registry)
    guard_failures = [
        "Citation path guard failure at "
        f"{item['json_pointer']}: {item['reason']}"
        for item in guard["failures"]
    ]
    raw_failures = list(dict.fromkeys(raw["failures"]))
    validated_failures = list(
        dict.fromkeys(validated["failures"] + guard_failures)
    )
    return {
        "raw_failures": raw_failures,
        "validated_failures": validated_failures,
        "citation_repairs": guard["citation_repairs"],
        "citation_guard_failures": guard["failures"],
        "validated_output": guard["validated_output"],
        "manual_density_flags": density_flags(guard["validated_output"], case),
    }


def prior_reuse_index() -> dict[str, dict[str, Any]]:
    prior_root = V2_ROOT / "eval/current"
    selection_path = prior_root / "accepted_samples.json"
    if not selection_path.is_file():
        return {}
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    index: dict[str, dict[str, Any]] = {}
    for selected in selection["cases"]:
        record_path = prior_root / selected["accepted_record_path"]
        if file_sha256(record_path) != selected["accepted_record_sha256"]:
            raise RuntimeError(f"Prior accepted record hash changed: {record_path}")
        record = json.loads(record_path.read_text(encoding="utf-8"))
        if (
            record.get("system_prompt_sha256") != FROZEN_SYSTEM_SHA256
            or record.get("output_schema_sha256")
            != file_sha256(V2_ROOT / "output.schema.json")
            or record.get("input_schema_sha256")
            != file_sha256(V2_ROOT / "input.schema.json")
            or record.get("settings") != SETTINGS
            or not record.get("schema_valid")
        ):
            continue
        key = canonical_sha256(record["request_input"])
        if key in index:
            raise RuntimeError("Duplicate exact request in prior accepted selection")
        index[key] = {
            "path": record_path,
            "sha256": selected["accepted_record_sha256"],
            "record": record,
        }
    return index


def make_base_record(
    context: dict[str, Any],
    case: dict[str, Any],
    request_input: dict[str, Any],
    raw_request: str,
    auth_mode: str,
) -> dict[str, Any]:
    source = request_input["source_messaging"]
    return {
        "case_id": case["case_id"],
        "case": case,
        "request_key": canonical_sha256(
            {
                "input": request_input,
                "system_prompt_sha256": FROZEN_SYSTEM_SHA256,
                "input_schema_sha256": context["manifest"]["provenance"][
                    "input_schema_sha256"
                ],
                "output_schema_sha256": context["manifest"]["provenance"][
                    "output_schema_sha256"
                ],
                "settings": SETTINGS,
            }
        ),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "input_path": case["input_path"],
        "input_sha256": case["input_sha256"],
        "source_sha256": canonical_sha256(source),
        "raw_request_json": raw_request,
        "request_input": request_input,
        "raw_input_json": json.dumps(source, ensure_ascii=False, indent=2),
        "system_prompt": context["system"],
        "system_prompt_sha256": FROZEN_SYSTEM_SHA256,
        "input_schema": context["input_schema"],
        "input_schema_sha256": context["manifest"]["provenance"][
            "input_schema_sha256"
        ],
        "schema": context["output_schema"],
        "output_schema_sha256": context["manifest"]["provenance"][
            "output_schema_sha256"
        ],
        "manifest_sha256": context["manifest_sha256"],
        "camera_profiles_sha256": context["manifest"]["provenance"][
            "camera_profiles_sha256"
        ],
        "settings": SETTINGS,
        "auth_mode": auth_mode,
        "retry_events": [],
    }


def run_case(
    *,
    context: dict[str, Any],
    case: dict[str, Any],
    client: Any,
    auth_mode: str,
    max_attempts: int,
    reuse_index: dict[str, dict[str, Any]],
    force_new_attempt: bool,
) -> dict[str, Any]:
    input_path = Path(case["input_path"])
    raw_request = input_path.read_text(encoding="utf-8")
    request_input = json.loads(raw_request)
    jsonschema.validate(request_input, context["input_schema"])
    target = EVAL_ROOT / "records/accepted" / f"{case['case_id']}.json"
    attempt_dir = EVAL_ROOT / "records/attempts" / case["case_id"]
    prior_rejected = None
    if target.is_file() and not force_new_attempt:
        record = json.loads(target.read_text(encoding="utf-8"))
        expected_key = make_base_record(
            context, case, request_input, raw_request, record.get("auth_mode", "preserved")
        )["request_key"]
        if record.get("request_key") != expected_key:
            raise RuntimeError(f"Existing record has different provenance: {case['case_id']}")
        record_hash = file_sha256(target)
        preserved_path = target
        for candidate in sorted(attempt_dir.glob("*.json")):
            if candidate.name == "pending.json":
                continue
            if file_sha256(candidate) == record_hash:
                preserved_path = candidate
                break
        return {
            "case": case,
            "record": record,
            "path": target,
            "attempt_path": preserved_path,
            "existing": True,
        }
    if target.is_file():
        prior_rejected = {
            "path": str(target.resolve()),
            "sha256": file_sha256(target),
        }

    base = make_base_record(
        context, case, request_input, raw_request, auth_mode
    )
    if prior_rejected:
        base["prior_rejected_record"] = prior_rejected
    reusable = (
        None
        if force_new_attempt
        else reuse_index.get(canonical_sha256(request_input))
    )
    if reusable:
        prior = reusable["record"]
        record = {
            **base,
            "origin": "reused_exact",
            "exact_request_object_match": True,
            "reused_source_record_path": str(reusable["path"].resolve()),
            "reused_source_record_sha256": reusable["sha256"],
            "attempt": 0,
            "sample_attempt_index": 0,
            "latency_seconds": 0.0,
            "response": prior["response"],
            "usage": prior.get("usage") or prior["response"].get("usage"),
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "parsed_output": prior["parsed_output"],
            "schema_valid": True,
        }
        write_json(target, record)
        return {
            "case": case,
            "record": record,
            "path": target,
            "attempt_path": target,
            "existing": False,
        }

    record = {**base, "origin": "api"}
    existing_sample_count = 0
    if attempt_dir.exists():
        for previous_path in attempt_dir.glob("*.json"):
            if previous_path.name == "pending.json":
                continue
            try:
                previous = json.loads(previous_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if previous.get("parsed_output") is not None:
                existing_sample_count += 1
    sample_index = existing_sample_count + 1
    record["sample_attempt_index"] = sample_index
    pending = attempt_dir / "pending.json"
    for attempt in range(1, max_attempts + 1):
        request_started = time.monotonic()
        try:
            response = client.chat.completions.create(
                **SETTINGS,
                messages=[
                    {"role": "system", "content": context["system"]},
                    {"role": "user", "content": raw_request},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "hp_camera_environment_prompts",
                        "strict": True,
                        "schema": context["output_schema"],
                    },
                },
            )
            record["attempt"] = attempt
            record["latency_seconds"] = round(time.monotonic() - request_started, 3)
            record["response"] = response.model_dump(mode="json")
            record["usage"] = record["response"].get("usage")
            record["completed_at"] = datetime.now(timezone.utc).isoformat()
            raw_attempt = (
                attempt_dir
                / f"sample_{sample_index:03d}_transport_{attempt:03d}.json"
            )
            write_json(raw_attempt, record)
            if (
                not response.model.startswith("gpt-5.5")
                or response.choices[0].finish_reason != "stop"
            ):
                raise RuntimeError("Unexpected model or incomplete response")
            parsed = json.loads(response.choices[0].message.content or "")
            jsonschema.validate(parsed, context["output_schema"])
            record["parsed_output"] = parsed
            record["schema_valid"] = True
            write_json(raw_attempt, record)
            write_json(target, record)
            if pending.exists():
                pending.unlink()
            return {
                "case": case,
                "record": record,
                "path": target,
                "attempt_path": raw_attempt,
                "existing": False,
            }
        except Exception as exc:
            if record.get("response") or not transient(exc) or attempt == max_attempts:
                record["failure"] = {
                    "type": type(exc).__name__,
                    "status_code": getattr(exc, "status_code", None),
                    "attempt": attempt,
                }
                write_json(
                    attempt_dir
                    / f"sample_{sample_index:03d}_transport_{attempt:03d}_failed.json",
                    record,
                )
                raise RuntimeError(
                    f"Case {case['case_id']} stopped: {type(exc).__name__}"
                ) from None
            delay = retry_delay(exc, attempt)
            record["retry_events"].append(
                {
                    "attempt": attempt,
                    "status_code": getattr(exc, "status_code", None),
                    "type": type(exc).__name__,
                    "wait_seconds": delay,
                }
            )
            write_json(pending, record)
            while delay > 0:
                step = min(30, delay)
                time.sleep(step)
                delay -= step
    raise AssertionError("unreachable")


def process_case(
    *,
    context: dict[str, Any],
    case: dict[str, Any],
    client: Any,
    auth_mode: str,
    max_attempts: int,
    reuse_index: dict[str, dict[str, Any]],
    force_new_attempt: bool,
    max_successful_samples: int = 3,
) -> dict[str, Any]:
    """Run one case through validation, retrying genuine validation failures."""

    force = force_new_attempt
    attempt_reports = []
    while True:
        result = run_case(
            context=context,
            case=case,
            client=client,
            auth_mode=auth_mode,
            max_attempts=max_attempts,
            reuse_index=reuse_index,
            force_new_attempt=force,
        )
        record = result["record"]
        audit = audit_record(
            record, case, context["output_schema"], context["registry"]
        )
        status = (
            "rejected"
            if audit["validated_failures"]
            else "manual_review"
            if audit["manual_density_flags"] and record["origin"] != "reused_exact"
            else "accepted"
        )
        sample_index = int(record.get("sample_attempt_index", 0))
        if record["origin"] == "api" and sample_index == 0:
            sample_index = 1
        report = {
            "case_id": case["case_id"],
            "successful_sample_attempt": sample_index,
            "status": status,
            "record_path": str(result["attempt_path"].resolve()),
            "record_sha256": file_sha256(result["attempt_path"]),
            **{key: value for key, value in audit.items() if key != "validated_output"},
        }
        validation_attempt = (
            EVAL_ROOT
            / "validation/attempts"
            / case["case_id"]
            / f"sample_{sample_index:03d}.json"
        )
        write_json(validation_attempt, report)
        attempt_reports.append(report)
        if (
            status == "rejected"
            and record["origin"] == "api"
            and sample_index < max_successful_samples
        ):
            force = True
            continue
        return {
            **result,
            "audit": audit,
            "status": status,
            "attempt_reports": attempt_reports,
        }


def accepted_entry(
    case: dict[str, Any], record: dict[str, Any], record_path: Path, audit: dict[str, Any]
) -> dict[str, Any]:
    output = audit["validated_output"]
    prompts = [
        {
            "prompt_id": prompt["id"],
            "environment": prompt["environment"],
            "text": prompt["text"],
            "text_sha256": sha256_bytes(prompt["text"].encode("utf-8")),
        }
        for prompt in output["prompts"]
    ]
    return {
        "case_id": case["case_id"],
        "source_id": case["source_id"],
        "device_type": case["device_type"],
        "camera_tag": case["camera_tag"],
        "input_path": case["input_path"],
        "input_sha256": case["input_sha256"],
        "render_ids": case["render_ids"],
        "expected_camera": case["expected_camera"],
        "status": "accepted",
        "launchable": True,
        "origin": record["origin"],
        "accepted_record_path": str(record_path.resolve()),
        "accepted_record_sha256": file_sha256(record_path),
        "validated_output_sha256": canonical_sha256(output),
        "prompts": prompts,
        "debug": output["debug"],
        "citation_repairs": audit["citation_repairs"],
        "citation_guard_failures": audit["citation_guard_failures"],
        "raw_failures": audit["raw_failures"],
        "validated_failures": audit["validated_failures"],
        "manual_density_flags": audit["manual_density_flags"],
    }


def update_inventory(
    manifest: dict[str, Any], accepted: dict[str, Any], validation_dir: Path
) -> dict[str, Any]:
    states = {"accepted": 0, "manual_review": 0, "rejected": 0}
    for path in validation_dir.glob("*.json"):
        status = json.loads(path.read_text(encoding="utf-8")).get("status")
        if status in states:
            states[status] += 1
    accepted_cases = accepted["cases"]
    accepted_prompt_count = sum(
        len(entry["prompts"]) for entry in accepted_cases.values()
    )
    launchable_pairs = sum(
        len(entry["render_ids"]) * len(entry["prompts"])
        for entry in accepted_cases.values()
        if entry["launchable"]
    )
    return {
        "version": "camera-v2-prompt-status-v1",
        "manifest_case_count": manifest["counts"]["case_count"],
        "manifest_source_render_pair_count": manifest["counts"][
            "source_render_pair_count"
        ],
        "accepted_case_count": len(accepted_cases),
        "manual_review_case_count": states["manual_review"],
        "rejected_case_count": states["rejected"],
        "unprocessed_case_count": manifest["counts"]["case_count"]
        - sum(states.values()),
        "accepted_prompt_count": accepted_prompt_count,
        "launchable_generation_row_count": launchable_pairs,
        "accepted_origin_counts": dict(
            __import__("collections").Counter(
                entry["origin"] for entry in accepted_cases.values()
            )
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=EVAL_ROOT / "manifest.json")
    parser.add_argument("--case", action="append", help="Exact case_id; repeatable")
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--max-attempts", type=int, default=100)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument(
        "--reuse-only",
        action="store_true",
        help="Process only exact matches from the prior accepted evaluation; make no API calls.",
    )
    parser.add_argument(
        "--retry-rejected",
        action="store_true",
        help="Make a new preserved sample attempt for explicitly selected rejected cases.",
    )
    args = parser.parse_args()
    if not 1 <= args.concurrency <= 2:
        parser.error("--concurrency must be 1 or 2")
    if not 1 <= args.max_attempts <= 100:
        parser.error("--max-attempts must be between 1 and 100")
    if args.retry_rejected and (not args.case or args.reuse_only or args.preflight_only):
        parser.error(
            "--retry-rejected requires explicit --case and cannot combine with "
            "--reuse-only or --preflight-only"
        )
    context = load_context(args.manifest.resolve())
    manifest = context["manifest"]
    cases_by_id = {case["case_id"]: case for case in manifest["cases"]}
    if args.case:
        unknown = sorted(set(args.case) - set(cases_by_id))
        if unknown:
            raise RuntimeError(f"Unknown case IDs: {unknown}")
        cases = [cases_by_id[case_id] for case_id in args.case]
    else:
        cases = manifest["cases"]
    accepted_path = EVAL_ROOT / "accepted_prompt_cases.json"
    accepted = json.loads(accepted_path.read_text(encoding="utf-8"))
    if accepted["manifest_sha256"] != context["manifest_sha256"]:
        raise RuntimeError("Accepted-case map belongs to a different manifest")
    pending_cases = [case for case in cases if case["case_id"] not in accepted["cases"]]
    reuse_index = prior_reuse_index()
    reusable = sum(
        canonical_sha256(json.loads(Path(case["input_path"]).read_text()))
        in reuse_index
        for case in pending_cases
    )
    if args.reuse_only:
        pending_cases = [
            case
            for case in pending_cases
            if canonical_sha256(json.loads(Path(case["input_path"]).read_text()))
            in reuse_index
        ]
    if args.preflight_only:
        print(
            json.dumps(
                {
                    "preflight": "ok",
                    "api_called": False,
                    "manifest_sha256": context["manifest_sha256"],
                    "selected_case_count": len(cases),
                    "already_accepted": len(cases) - len(pending_cases),
                    "pending_case_count": len(pending_cases),
                    "exact_reusable_case_count": reusable,
                    "new_api_case_count": len(pending_cases) - reusable,
                },
                indent=2,
            )
        )
        return 0
    if not pending_cases:
        print("All selected cases are already accepted")
        return 0

    if args.reuse_only:
        client, auth_mode = None, "not_used_exact_reuse"
    else:
        client, auth_mode = client_and_auth_mode()
    validation_dir = EVAL_ROOT / "validation/cases"
    failures = []
    lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = {
            executor.submit(
                process_case,
                context=context,
                case=case,
                client=client,
                auth_mode=auth_mode,
                max_attempts=args.max_attempts,
                reuse_index=reuse_index,
                force_new_attempt=args.retry_rejected,
            ): case
            for case in pending_cases
        }
        for future in as_completed(futures):
            case = futures[future]
            try:
                result = future.result()
                record = result["record"]
                record_path = result["path"]
                audit = result["audit"]
                status = result["status"]
                report = {
                    "case_id": case["case_id"],
                    "status": status,
                    "successful_sample_attempt_count": len(
                        result["attempt_reports"]
                    ),
                    "final_record_path": str(result["attempt_path"].resolve()),
                    "final_record_sha256": file_sha256(result["attempt_path"]),
                    "attempt_validation_paths": [
                        str(
                            (
                                EVAL_ROOT
                                / "validation/attempts"
                                / case["case_id"]
                                / f"sample_{attempt['successful_sample_attempt']:03d}.json"
                            ).resolve()
                        )
                        for attempt in result["attempt_reports"]
                    ],
                    **{key: value for key, value in audit.items() if key != "validated_output"},
                }
                write_json(validation_dir / f"{case['case_id']}.json", report)
                with lock:
                    if status == "accepted":
                        accepted["cases"][case["case_id"]] = accepted_entry(
                            case, record, record_path, audit
                        )
                    accepted["accepted_case_count"] = len(accepted["cases"])
                    inventory = update_inventory(manifest, accepted, validation_dir)
                    accepted["manual_review_case_count"] = inventory[
                        "manual_review_case_count"
                    ]
                    accepted["failed_case_count"] = inventory["rejected_case_count"]
                    accepted["status"] = (
                        "complete"
                        if accepted["accepted_case_count"] == accepted["case_count"]
                        else "progressive"
                    )
                    write_json(accepted_path, accepted)
                    write_json(EVAL_ROOT / "status_inventory.json", inventory)
                print(
                    json.dumps(
                        {
                            "case_id": case["case_id"],
                            "status": status,
                            "origin": record["origin"],
                            "successful_sample_attempt_count": len(
                                result["attempt_reports"]
                            ),
                            "prompt_count": len(record["parsed_output"]["prompts"]),
                            "latency_seconds": record.get("latency_seconds"),
                            "raw_failure_count": len(audit["raw_failures"]),
                            "validated_failure_count": len(
                                audit["validated_failures"]
                            ),
                            "citation_repair_count": len(audit["citation_repairs"]),
                            "manual_density_flag_count": len(
                                audit["manual_density_flags"]
                            ),
                        }
                    ),
                    flush=True,
                )
            except Exception as exc:
                failures.append({"case_id": case["case_id"], "error": str(exc)})
                print(json.dumps(failures[-1]), flush=True)
    if failures:
        write_json(EVAL_ROOT / "validation/run_failures.json", {"failures": failures})
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
