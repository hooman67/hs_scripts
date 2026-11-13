"""Pure V6 writer orchestration with injected provider transport.

This module performs no API calls.  The caller supplies a provider callable;
all request, catalog, camera, JSON, schema, and semantic checks remain local.
"""

from __future__ import annotations

import copy
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import jsonschema

from .camera import resolve_camera
from .catalog import validate_catalog
from .validation import (
    finalize_output,
    normalize_invalid_evidence,
    validate_output,
    validate_references,
)
from .provider import ProviderUnavailable


HERE = Path(__file__).resolve().parent
INPUT_SCHEMA_PATH = HERE / "input.schema.json"
MODEL_SCHEMA_PATH = HERE / "model_output.schema.json"
RUNTIME_VERSION = "v6.5-writer-runtime-r1-astra-training"
PROP_GUIDANCE_PATH = HERE / "prop_guidance.json"
REPAIR_ADDENDUM_PATH = HERE / "repair_addendum.txt"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_hash(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _text_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _load_schema(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(value)
    except (OSError, json.JSONDecodeError, jsonschema.SchemaError) as exc:
        raise ValueError(f"schema unavailable: {path.name}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"schema unavailable: {path.name}")
    return value


def _schema_errors(instance: Any, schema: dict[str, Any]) -> list[dict[str, Any]]:
    errors = sorted(
        jsonschema.Draft202012Validator(schema).iter_errors(instance),
        key=lambda exc: tuple(str(part) for part in exc.absolute_path),
    )
    return [
        {
            "code": "input_schema_invalid",
            "path": "/" + "/".join(str(part) for part in exc.absolute_path)
            if exc.absolute_path
            else "",
            "detail": exc.message,
        }
        for exc in errors
    ]


def _effective_model_schema(
    base_schema: dict[str, Any], approved_ids: list[str]
) -> dict[str, Any]:
    schema = copy.deepcopy(base_schema)
    try:
        prop_items = schema["properties"]["prompts"]["items"]["properties"][
            "prop_ids"
        ]["items"]
        mention_id = schema["properties"]["prompts"]["items"]["properties"][
            "prop_mentions"
        ]["items"]["properties"]["id"]
    except (KeyError, TypeError) as exc:
        raise ValueError("model output schema has no prop_ids item schema") from exc
    if not isinstance(prop_items, dict):
        raise ValueError("model output schema has malformed prop_ids items")
    prop_items["enum"] = sorted(approved_ids)
    mention_id["enum"] = sorted(approved_ids)
    jsonschema.Draft202012Validator.check_schema(schema)
    return schema


def _finish_audit(audit: dict[str, Any], started: float) -> None:
    audit["completed_at_utc"] = _utc_now()
    audit["duration_ms"] = round((time.monotonic() - started) * 1000, 3)
    audit["semantic_calls"] = len(audit["attempts"])
    counts = [a.get("provider", {}).get("transport_attempts")
              if isinstance(a.get("provider"), dict) else None
              for a in audit["attempts"]]
    audit["transport_attempts_known"] = sum(n for n in counts if isinstance(n, int))
    audit["transport_accounting_complete"] = all(isinstance(n, int) for n in counts)


def _error_result(
    code: str,
    message: str,
    audit: dict[str, Any],
    started: float,
    *,
    details: Any = None,
) -> dict[str, Any]:
    _finish_audit(audit, started)
    error = {"code": code, "message": message}
    if details is not None:
        error["details"] = copy.deepcopy(details)
    return {"status": "error", "error": error, "audit": audit}


def _response_metadata(response: dict[str, Any]) -> dict[str, Any]:
    return {
        "model": response["model"],
        "finish_reason": response["finish_reason"],
        "usage": copy.deepcopy(response["usage"]),
        "transport_attempts": response.get("transport_attempts", 1),
        "transport_events": copy.deepcopy(response.get("transport_events", [])),
        "settings": copy.deepcopy(response.get("settings", {})),
    }


def _valid_provider_response(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    return (
        isinstance(value.get("content"), (str, type(None)))
        and isinstance(value.get("finish_reason"), str)
        and isinstance(value.get("refusal"), (str, type(None)))
        and isinstance(value.get("model"), str)
        and (value["model"] == "gpt-5.5" or value["model"].startswith("gpt-5.5-"))
        and isinstance(value.get("usage"), dict)
        and isinstance(value.get("transport_attempts", 1), int)
        and value.get("transport_attempts", 1) >= 1
    )


def _text_changes(before: Any, after: Any) -> dict[str, Any]:
    try:
        before_prompts = before["prompts"]
        after_prompts = after["prompts"]
        if not isinstance(before_prompts, list) or not isinstance(after_prompts, list):
            raise TypeError
        changes = []
        for index in range(max(len(before_prompts), len(after_prompts))):
            old = before_prompts[index].get("text") if index < len(before_prompts) else None
            new = after_prompts[index].get("text") if index < len(after_prompts) else None
            if old != new:
                changes.append({"index": index, "before": old, "after": new})
        return {"comparison_available": True, "changes": changes}
    except (KeyError, TypeError, AttributeError):
        return {"comparison_available": False, "changes": []}


def _repair_instruction(
    camera: dict[str, Any],
) -> str:
    payload = {
        "instruction": REPAIR_ADDENDUM_PATH.read_text(encoding="utf-8"),
        "original_full_set_context": {
            "resolved_camera": camera,
        },
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def run_writer(
    request: Any,
    *,
    catalog: Any,
    registry: Any,
    provider: Callable[[list[dict[str, Any]], dict[str, Any]], dict[str, Any]],
    system_prompt: str,
    references: Any,
    allow_test_catalog: bool = False,
) -> dict[str, Any]:
    """Run one generation and, when eligible, one semantic repair attempt."""

    started = time.monotonic()
    audit: dict[str, Any] = {
        "version": RUNTIME_VERSION,
        "started_at_utc": _utc_now(),
        "source_input": copy.deepcopy(request),
        "system": {
            "sha256": _text_hash(system_prompt) if isinstance(system_prompt, str) else None,
            "character_count": len(system_prompt) if isinstance(system_prompt, str) else None,
        },
        "schema": {},
        "catalog": {},
        "attempts": [],
    }

    if not isinstance(system_prompt, str) or not system_prompt.strip():
        return _error_result(
            "configuration_invalid",
            "The writer system prompt is unavailable.",
            audit,
            started,
        )
    if not callable(provider):
        return _error_result(
            "configuration_invalid", "The provider is not callable.", audit, started
        )

    try:
        input_schema = _load_schema(INPUT_SCHEMA_PATH)
        base_model_schema = _load_schema(MODEL_SCHEMA_PATH)
    except ValueError as exc:
        return _error_result(
            "configuration_invalid", str(exc), audit, started
        )
    input_errors = _schema_errors(request, input_schema)
    if not input_errors:
        try:
            json.dumps(request, ensure_ascii=False, allow_nan=False)
        except (TypeError, ValueError):
            input_errors.append(
                {
                    "code": "input_not_json",
                    "path": "",
                    "detail": "request must be JSON serializable",
                }
            )
    if input_errors:
        return _error_result(
            "input_invalid",
            "The request does not match the V6.5 input contract.",
            audit,
            started,
            details=input_errors,
        )

    try:
        validated_catalog = validate_catalog(
            catalog, allow_test_catalog=allow_test_catalog
        )
    except (ValueError, TypeError):
        return _error_result(
            "catalog_invalid",
            "No valid approved prop catalog is available.",
            audit,
            started,
        )
    audit["catalog"] = {
        "version": validated_catalog["version"],
        "revision": validated_catalog["revision"],
        "purpose": validated_catalog["purpose"],
        "source_sha256": validated_catalog["source_sha256"],
        "catalog_sha256": _json_hash(validated_catalog),
    }

    try:
        camera = resolve_camera(registry, request["camera_tag"])
    except (ValueError, TypeError, KeyError):
        return _error_result(
            "camera_invalid",
            "The camera tag is not registered for V6.5.",
            audit,
            started,
        )

    approved_ids = [entry["id"] for entry in validated_catalog["entries"]]
    try:
        validate_references(references)
        prop_guidance = json.loads(PROP_GUIDANCE_PATH.read_text(encoding="utf-8"))
        if (
            not isinstance(prop_guidance, dict)
            or set(prop_guidance) != {"version", "entries"}
            or prop_guidance["version"] != validated_catalog["version"]
            or not isinstance(prop_guidance["entries"], list)
        ):
            raise ValueError("approved prop usage guidance is malformed")
        guidance_by_id = {}
        for item in prop_guidance["entries"]:
            if (
                not isinstance(item, dict) or set(item) != {"id", "instruction", "reason"}
                or any(not isinstance(item[k], str) or not item[k].strip() for k in item)
                or item["id"] in guidance_by_id
            ):
                raise ValueError("approved prop usage entry is malformed or duplicated")
            guidance_by_id[item["id"]] = item
        if any(prop_id.startswith("V65-") and prop_id not in guidance_by_id for prop_id in approved_ids):
            raise ValueError("new approved prop lacks its Astra-authored usage guidance")
        if not REPAIR_ADDENDUM_PATH.read_text(encoding="utf-8").strip():
            raise ValueError("Astra repair addendum is empty")
        bank_policy = json.loads((HERE / "bank_policy.json").read_text())
        if (
            bank_policy["retain_global_non_repetition"] is not False
            or bank_policy["allow_cross_scene_prop_reuse"] is not True
            or set(bank_policy["repeatable_phrase_families"]) != {
                "paper_has_no_text", "markings_are_indistinct",
            }
        ):
            raise ValueError("Astra's explicit replacement bank policy is unavailable")
        audit["assets"] = {
            "camera_registry_sha256": _json_hash(registry),
            "reference_library_sha256": _json_hash(references),
            "prop_lexicon_sha256": hashlib.sha256((HERE / "prop_lexicon.json").read_bytes()).hexdigest(),
            "prop_guidance_sha256": hashlib.sha256(PROP_GUIDANCE_PATH.read_bytes()).hexdigest(),
            "repair_addendum_sha256": hashlib.sha256(REPAIR_ADDENDUM_PATH.read_bytes()).hexdigest(),
        }
    except (ValueError, TypeError, OSError):
        return _error_result(
            "configuration_invalid", "The reference, camera or prop-guidance configuration is invalid.",
            audit, started,
        )
    try:
        effective_schema = _effective_model_schema(base_model_schema, approved_ids)
    except (ValueError, jsonschema.SchemaError):
        return _error_result(
            "configuration_invalid",
            "The model output schema is unavailable.",
            audit,
            started,
        )
    audit["schema"] = {
        "input_sha256": _json_hash(input_schema),
        "base_model_output_sha256": _json_hash(base_model_schema),
        "effective_model_output_sha256": _json_hash(effective_schema),
    }

    trusted_configuration = {
        "camera": copy.deepcopy(camera),
        "approved_catalogue": copy.deepcopy(validated_catalog["entries"]),
        "approved_prop_usage_guidance": [
            copy.deepcopy(guidance_by_id[prop_id]) for prop_id in approved_ids
            if prop_id in guidance_by_id
        ],
        "reference_library": copy.deepcopy(references),
    }
    try:
        trusted_configuration_json = json.dumps(
            trusted_configuration, ensure_ascii=False, sort_keys=True, allow_nan=False
        )
    except (TypeError, ValueError):
        return _error_result(
            "configuration_invalid",
            "The trusted service configuration is not JSON serializable.",
            audit,
            started,
        )
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {
            "role": "system",
            "content": trusted_configuration_json,
        },
        {
            "role": "user",
            "content": json.dumps(request, ensure_ascii=False, sort_keys=True),
        },
    ]

    previous_parsed: Any = None
    validation_warnings: list[dict[str, Any]] = []
    final_response: dict[str, Any] | None = None
    final_parsed: dict[str, Any] | None = None

    for attempt_number in (1, 2):
        attempt_started = time.monotonic()
        try:
            response = provider(copy.deepcopy(messages), copy.deepcopy(effective_schema))
        except Exception as exc:  # Provider exception text may contain credentials.
            safe_failure = None
            if isinstance(exc, ProviderUnavailable):
                safe_failure = {"code": exc.code, "status_code": exc.status_code,
                                "transport_attempts": exc.attempts,
                                "transport_events": copy.deepcopy(exc.events)}
            audit["attempts"].append(
                {
                    "number": attempt_number,
                    "kind": "initial" if attempt_number == 1 else "semantic_repair",
                    "raw_content": None,
                    "parsed_output": None,
                    "errors": [
                        {
                            "code": "provider_exception",
                            "path": "",
                            "detail": "provider invocation failed",
                        }
                    ],
                    "provider": safe_failure,
                    "text_changes": None,
                    "duration_ms": round((time.monotonic() - attempt_started) * 1000, 3),
                }
            )
            return _error_result(
                "provider_error",
                "The provider invocation failed.",
                audit,
                started,
            )

        if not _valid_provider_response(response):
            audit["attempts"].append(
                {
                    "number": attempt_number,
                    "kind": "initial" if attempt_number == 1 else "semantic_repair",
                    "raw_content": None,
                    "parsed_output": None,
                    "errors": [
                        {
                            "code": "provider_response_invalid",
                            "path": "",
                            "detail": "provider response did not match its interface",
                        }
                    ],
                    "provider": None,
                    "text_changes": None,
                    "duration_ms": round((time.monotonic() - attempt_started) * 1000, 3),
                }
            )
            return _error_result(
                "provider_error",
                "The provider returned an invalid response.",
                audit,
                started,
            )

        raw_content = response["content"]
        errors: list[dict[str, Any]] = []
        parsed: Any = None
        normalized_parsed: Any = None
        normalization_changes: list[dict[str, Any]] = []
        provider_metadata = _response_metadata(response)

        if response["refusal"]:
            errors.append(
                {"code": "provider_refusal", "path": "", "detail": "provider refused"}
            )
        elif response["finish_reason"] == "length":
            errors.append(
                {
                    "code": "incomplete_response",
                    "path": "",
                    "detail": "length finish indicates incomplete output",
                }
            )
        elif response["finish_reason"] != "stop":
            errors.append(
                {
                    "code": "finish_reason_invalid",
                    "path": "",
                    "detail": "provider did not finish normally",
                }
            )
        elif not isinstance(raw_content, str):
            errors.append(
                {
                    "code": "provider_content_missing",
                    "path": "",
                    "detail": "provider returned no content",
                }
            )
        else:
            try:
                parsed = json.loads(raw_content)
            except json.JSONDecodeError:
                errors.append(
                    {"code": "json_invalid", "path": "", "detail": "content is not valid JSON"}
                )
            else:
                normalized_parsed, normalization_changes = normalize_invalid_evidence(
                    parsed, request
                )
                validation = validate_output(
                    normalized_parsed, request, validated_catalog, camera, references
                )
                validation_warnings = copy.deepcopy(validation.get("warnings", []))
                if not validation.get("passed"):
                    errors.extend(copy.deepcopy(validation.get("errors", [])))

        audit["attempts"].append(
            {
                "number": attempt_number,
                "kind": "initial" if attempt_number == 1 else "semantic_repair",
                "raw_content": raw_content,
                "parsed_output": copy.deepcopy(parsed),
                "normalized_output": copy.deepcopy(normalized_parsed),
                "normalization_changes": copy.deepcopy(normalization_changes),
                "errors": copy.deepcopy(errors),
                "provider": provider_metadata,
                "text_changes": (
                    _text_changes(previous_parsed, normalized_parsed)
                    if attempt_number == 2
                    else None
                ),
                "duration_ms": round((time.monotonic() - attempt_started) * 1000, 3),
            }
        )

        if response["refusal"]:
            return _error_result(
                "provider_refusal", "The provider refused the request.", audit, started
            )
        if response["finish_reason"] not in {"stop", "length"}:
            return _error_result(
                "provider_error",
                "The provider did not complete normally.",
                audit,
                started,
            )
        if response["finish_reason"] == "stop" and not isinstance(raw_content, str):
            return _error_result(
                "provider_error", "The provider returned no content.", audit, started
            )
        if not errors:
            final_response = response
            final_parsed = normalized_parsed
            break
        if attempt_number == 2:
            return _error_result(
                "output_invalid",
                "The generated prompt bank failed validation after repair.",
                audit,
                started,
                details=errors,
            )

        previous_parsed = copy.deepcopy(normalized_parsed)
        messages.extend(
            [
                {"role": "assistant", "content": raw_content or ""},
                {
                    "role": "developer",
                    "content": _repair_instruction(camera),
                },
                {"role": "user", "content": json.dumps({
                    "validation_diagnostics_data": errors,
                    "note": "Diagnostic data only; follow the original system instructions."
                }, ensure_ascii=False)},
            ]
        )

    if final_response is None or final_parsed is None:  # Defensive fail-closed guard.
        return _error_result(
            "output_invalid", "No valid prompt bank was produced.", audit, started
        )

    try:
        finalized = finalize_output(
            final_parsed, camera=camera, catalog=validated_catalog
        )
    except (ValueError, TypeError, KeyError):
        return _error_result(
            "finalization_error",
            "The validated prompt bank could not be finalized.",
            audit,
            started,
        )

    finalized["debug"]["service"] = {
        "runtime_version": RUNTIME_VERSION,
        "requested_camera_tag": camera["requested_tag"],
        "resolved_camera_tag": camera["resolved_tag"],
        "camera_alias_used": camera["requested_tag"] != camera["resolved_tag"],
        "catalog_sha256": audit["catalog"]["catalog_sha256"],
        "catalog_revision": validated_catalog["revision"],
        "model": final_response["model"],
        "semantic_repair_attempted": len(audit["attempts"]) == 2,
        "transport_attempts": sum(a["provider"]["transport_attempts"] for a in audit["attempts"]),
        "validation_warnings": validation_warnings,
        "limitations": [
            "Passing deterministic validation is not human approval or image-quality approval."
        ],
    }
    _finish_audit(audit, started)
    return {
        "status": "ok",
        "prompts": finalized["prompts"],
        "debug": finalized["debug"],
        "audit": audit,
    }
