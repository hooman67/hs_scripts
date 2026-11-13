# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests"]
# ///
"""Single-pass V4 placement judge with one bounded structured-output repair."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import foundry_aws_gateway.llm

try:
    from .scoring import (
        ASSESSMENT_SCHEMA,
        PlacementValidationError,
        aggregate_assessment,
        validate_assessment,
        validate_result,
        validate_runtime_input,
    )
except ImportError:
    from scoring import (  # type: ignore
        ASSESSMENT_SCHEMA,
        PlacementValidationError,
        aggregate_assessment,
        validate_assessment,
        validate_result,
        validate_runtime_input,
    )


ROOT = Path(__file__).resolve().parent
PROTOCOL_VERSION = "hp-natural-placement-v4-request-v2-astra"
SUPPORTED_IMAGE_MIMES = {"image/png", "image/jpeg", "image/webp"}


def sha256(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def client():
    api_client = foundry_aws_gateway.llm.get_openai().with_options(
        timeout=600.0,
        max_retries=0,
    )
    return api_client, "foundry_direct_openai"


def wire_schema(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: wire_schema(child)
            for key, child in value.items()
            if key not in ("$schema", "$id", "title", "uniqueItems", "minLength")
        }
    if isinstance(value, list):
        return [wire_schema(child) for child in value]
    return value


WIRE_SCHEMA = wire_schema(ASSESSMENT_SCHEMA)
WIRE_SCHEMA_SHA256 = json_sha256(WIRE_SCHEMA)


def _image_mime(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in SUPPORTED_IMAGE_MIMES:
        raise ValueError(f"Unsupported image format: {path.name}")
    return mime


def _model_identity_matches(requested: str, returned: Any) -> bool:
    return isinstance(returned, str) and re.fullmatch(
        rf"{re.escape(requested)}(?:-\d{{4}}-\d{{2}}-\d{{2}})?", returned
    ) is not None


def _content(runtime_input: dict[str, str]) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": json.dumps(
                {
                    "product_type": runtime_input["product_type"],
                    "scene_prompt": runtime_input["scene_prompt"],
                    "image_stage": runtime_input["image_stage"],
                },
                ensure_ascii=False,
            ),
        }
    ]
    for label, key in (
        ("GENERATED_SCENE — scene-generation image to assess", "generated_image"),
        ("ORIGINAL_TWIN — product identity/orientation reference only", "twin_image"),
    ):
        path = Path(runtime_input[key])
        content.extend(
            [
                {"type": "text", "text": label},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{_image_mime(path)};base64," + base64.b64encode(path.read_bytes()).decode("ascii"),
                        "detail": "high",
                    },
                },
            ]
        )
    return content


def _audit_id(payload: Any) -> str:
    return json_sha256(payload)


def judge(runtime_input: Any, output_dir: Path | str, model: str = "gpt-5.5") -> dict[str, Any]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    system_path = ROOT / "system_prompt.md"
    schema_path = ROOT / "assessment_schema.json"
    scoring_path = ROOT / "scoring.py"
    system = system_path.read_text(encoding="utf-8")
    started = time.monotonic()
    input_fingerprint = json_sha256(runtime_input)
    audit = {
        "protocol_version": PROTOCOL_VERSION,
        "model_requested": model,
        "model_returned": None,
        "input_fingerprint": input_fingerprint,
        "system_prompt_sha256": sha256(system_path),
        "assessment_schema_sha256": sha256(schema_path),
        "scoring_sha256": sha256(scoring_path),
    }
    result_path = output_dir / "result.json"
    if result_path.exists():
        cached = json.loads(result_path.read_text(encoding="utf-8"))
        validate_result(cached)
        if cached["audit"]["input_fingerprint"] != input_fingerprint:
            raise RuntimeError("Cached result belongs to different input")
        return cached

    raw_attempts: list[dict[str, Any]] = []
    try:
        validate_runtime_input(runtime_input)
        if not isinstance(model, str) or not model:
            raise PlacementValidationError(["model must be a nonempty string"])
        files = {
            key: {"path": str(Path(runtime_input[key]).resolve()), "sha256": sha256(runtime_input[key])}
            for key in ("generated_image", "twin_image")
        }
        request = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "protocol_version": PROTOCOL_VERSION,
            "input": runtime_input,
            "input_fingerprint": input_fingerprint,
            "images": files,
            "model_requested": model,
            "reasoning_effort": "high",
            "max_completion_tokens": 24000,
            "max_model_attempts": 2,
            "repair_policy": "one complete replacement only after invalid structured output",
            "system_prompt_sha256": audit["system_prompt_sha256"],
            "assessment_schema_sha256": audit["assessment_schema_sha256"],
            "wire_schema_sha256": WIRE_SCHEMA_SHA256,
            "scoring_sha256": audit["scoring_sha256"],
            "image_detail": "high",
            "image_transform": "none; original bytes",
        }
        atomic_json(output_dir / "request.json", request)
        (output_dir / "system_prompt.md").write_text(system, encoding="utf-8")
        atomic_json(output_dir / "assessment_schema.json", ASSESSMENT_SCHEMA)
    except Exception as error:
        envelope = {
            "schema_version": "hp-natural-placement-v4-result-v1",
            "status": "error",
            "assessment": None,
            "derived": None,
            "error": {"code": "invalid_input", "message": f"{type(error).__name__}: {error}"},
            "raw_attempts": [{"attempt": 1, "audit_id": _audit_id({"error": str(error)}), "validation_status": "invalid"}],
            "audit": audit,
        }
        validate_result(envelope)
        atomic_json(result_path, envelope)
        return envelope

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system},
        {"role": "user", "content": _content(runtime_input)},
    ]
    assessment = None
    last_error: Exception | None = None
    try:
        api_client, auth_mode = client()
        request["auth_mode"] = auth_mode
        atomic_json(output_dir / "request.json", request)
        for attempt in (1, 2):
            try:
                response = api_client.chat.completions.create(
                    model=model,
                    reasoning_effort="high",
                    max_completion_tokens=24000,
                    messages=messages,
                    response_format={
                        "type": "json_schema",
                        "json_schema": {"name": "hp_natural_placement_v4", "strict": True, "schema": WIRE_SCHEMA},
                    },
                )
            except Exception as error:
                error_payload = {
                    "attempt": attempt,
                    "error_type": type(error).__name__,
                    "status_code": getattr(error, "status_code", None),
                    "message": str(error),
                }
                atomic_json(output_dir / f"transport_error_{attempt}.json", error_payload)
                raw_attempts.append({"attempt": attempt, "audit_id": _audit_id(error_payload), "validation_status": "transport_error"})
                last_error = error
                if attempt == 1:
                    continue
                break

            raw = response.model_dump(mode="json")
            atomic_json(output_dir / f"response_{attempt}.json", raw)
            audit["model_returned"] = getattr(response, "model", None)
            try:
                if not _model_identity_matches(model, audit["model_returned"]):
                    raise PlacementValidationError(["unexpected model returned"])
                choice = response.choices[0]
                if choice.finish_reason != "stop" or choice.message.refusal:
                    raise PlacementValidationError(["incomplete or refused structured response"])
                candidate = json.loads(choice.message.content)
                validate_assessment(candidate)
                assessment = candidate
                raw_attempts.append({"attempt": attempt, "audit_id": _audit_id(raw), "validation_status": "valid"})
                break
            except Exception as error:
                last_error = error
                errors = list(error.errors) if hasattr(error, "errors") else [f"{type(error).__name__}: {error}"]
                raw_attempts.append({"attempt": attempt, "audit_id": _audit_id(raw), "validation_status": "invalid"})
                atomic_json(output_dir / f"validation_errors_{attempt}.json", {"errors": errors})
                if attempt == 1:
                    messages.extend(
                        [
                            {"role": "assistant", "content": choice.message.content or ""},
                            {
                                "role": "user",
                                "content": (
                                    "The prior structured response was invalid. Return a complete replacement assessment for the same images and inputs. "
                                    "Do not discuss the errors. Validation errors: " + json.dumps(errors)
                                ),
                            },
                        ]
                    )
                    continue
                break
    except Exception as error:
        last_error = error

    if assessment is None:
        if not raw_attempts:
            error_payload = {"error_type": type(last_error).__name__, "message": str(last_error)}
            raw_attempts.append({"attempt": 1, "audit_id": _audit_id(error_payload), "validation_status": "transport_error"})
        code = "transport_failure" if raw_attempts[-1]["validation_status"] == "transport_error" else "invalid_model_output"
        envelope = {
            "schema_version": "hp-natural-placement-v4-result-v1",
            "status": "error",
            "assessment": None,
            "derived": None,
            "error": {"code": code, "message": f"{type(last_error).__name__}: {last_error}"},
            "raw_attempts": raw_attempts or [{"attempt": 1, "audit_id": _audit_id({"error": str(last_error)}), "validation_status": "transport_error"}],
            "audit": audit,
        }
    elif assessment["stage_status"] == "unable":
        envelope = {
            "schema_version": "hp-natural-placement-v4-result-v1",
            "status": "error",
            "assessment": assessment,
            "derived": None,
            "error": {"code": "unassessable_input", "message": assessment["unable_reason"]},
            "raw_attempts": raw_attempts,
            "audit": audit,
        }
    else:
        envelope = {
            "schema_version": "hp-natural-placement-v4-result-v1",
            "status": "ok",
            "assessment": assessment,
            "derived": aggregate_assessment(assessment),
            "error": None,
            "raw_attempts": raw_attempts,
            "audit": audit,
        }
    validate_result(envelope)
    atomic_json(result_path, envelope)
    atomic_json(output_dir / "timing.json", {"elapsed_seconds": round(time.monotonic() - started, 3)})
    return envelope


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="gpt-5.5")
    args = parser.parse_args()
    result = judge(json.loads(Path(args.input).read_text(encoding="utf-8")), args.output, args.model)
    print(json.dumps({"status": result["status"], "verdict": (result.get("derived") or {}).get("verdict"), "error": result.get("error")}))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
