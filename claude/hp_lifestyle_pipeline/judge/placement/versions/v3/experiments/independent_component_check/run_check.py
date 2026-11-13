# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests"]
# ///
"""Run one frozen names-only independent component check."""

from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import json
import mimetypes
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent
V3_ROOT = ROOT.parents[1]
PROMPT_PATH = ROOT / "system_prompt.md"
MANIFEST_PATH = ROOT / "input_manifest.json"
FREEZE_PATH = ROOT / "freeze.json"
RUNS_ROOT = ROOT / "runs"
PROTOCOL_VERSION = "placement-independent-component-check-v1"
INPUT_KEYS = frozenset({"generated_image", "twin_image", "product_type", "scene_prompt", "image_stage"})
MAX_ATTEMPTS = 2
MAX_COMPLETION_TOKENS = 6000


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if str(V3_ROOT) not in sys.path:
    sys.path.insert(0, str(V3_ROOT))
SCORING = load_module("independent_component_scoring", V3_ROOT / "scoring.py")
CANONICAL = load_module("independent_component_client", V3_ROOT / "run_judge.py")
DEFINITIONS = SCORING.OBSERVATION_SCHEMA["$defs"]


def sha256(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def response_schema(names: list[str]) -> dict[str, Any]:
    if not names or len(names) != len(set(names)):
        raise ValueError("Requested component names must be nonempty and unique")
    invalid = set(names) - set(DEFINITIONS)
    if invalid:
        raise ValueError(f"Unknown requested components: {sorted(invalid)}")
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "components"],
        "properties": {
            "schema_version": {"type": "string", "const": "placement-independent-components-v1"},
            "components": {"type": "object", "additionalProperties": False, "required": names, "properties": {name: copy.deepcopy(DEFINITIONS[name]) for name in names}},
        },
    }


def wire_schema(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: wire_schema(child) for key, child in value.items() if key not in ("$schema", "uniqueItems", "minLength")}
    if isinstance(value, list):
        return [wire_schema(child) for child in value]
    return value


def validate_response(value: Any, schema: Mapping[str, Any], names: list[str]) -> None:
    errors = list(Draft202012Validator(schema).iter_errors(value))
    if errors:
        raise ValueError("; ".join(error.message for error in errors))
    if set(value["components"]) != set(names):
        raise ValueError("Response dropped or added a requested component")
    for name, component in value["components"].items():
        visibility, severity = component["visibility"], component["severity"]
        if not component["evidence"].strip():
            raise ValueError(f"{name}: evidence must contain non-whitespace text")
        if visibility == "unobservable":
            if severity is not None or component["confidence"] != "low" or component["issue_codes"]:
                raise ValueError(f"{name}: invalid unobservable component")
        elif severity is None:
            raise ValueError(f"{name}: assessable component requires severity")
        if severity == 0 and component["issue_codes"]:
            raise ValueError(f"{name}: severity zero requires no issue codes")
        if isinstance(severity, int) and severity > 0 and not component["issue_codes"]:
            raise ValueError(f"{name}: positive severity requires issue codes")


def current_freeze() -> dict[str, Any]:
    return {
        "schema_version": "placement-independent-component-check-freeze-v1",
        "protocol_version": PROTOCOL_VERSION,
        "model": "gpt-5.5",
        "reasoning_effort": "high",
        "max_attempts": MAX_ATTEMPTS,
        "max_completion_tokens": MAX_COMPLETION_TOKENS,
        "input_whitelist": sorted(INPUT_KEYS),
        "hashes": {
            "runner_sha256": sha256(__file__),
            "batch_sha256": sha256(ROOT / "run_batch.py"),
            "manifest_sha256": sha256(MANIFEST_PATH),
            "system_prompt_sha256": sha256(PROMPT_PATH),
            "v3_schema_sha256": sha256(V3_ROOT / "observation_schema.json"),
            "v3_scoring_sha256": sha256(V3_ROOT / "scoring.py"),
            "v3_runner_sha256": sha256(V3_ROOT / "run_judge.py"),
        },
    }


def ensure_frozen() -> dict[str, Any]:
    frozen = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    current = current_freeze()
    for key, value in current.items():
        if frozen.get(key) != value:
            raise RuntimeError(f"Independent component freeze mismatch: {key}")
    return frozen


def image_content(path: Path) -> dict[str, Any]:
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in {"image/png", "image/jpeg", "image/webp"}:
        raise ValueError(f"Unsupported image: {path}")
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode(), "detail": "high"}}


def run(record: Mapping[str, Any], output_dir: Path, model: str = "gpt-5.5") -> dict[str, Any]:
    freeze = ensure_frozen()
    if output_dir.exists():
        raise FileExistsError(output_dir)
    runtime_input = record["runtime_input"]
    if set(runtime_input) != INPUT_KEYS:
        raise ValueError(f"{record['id']}: input whitelist changed")
    SCORING.validate_runtime_input(runtime_input)
    names = list(record["requested_component_names"])
    schema = response_schema(names)
    generated, twin = Path(runtime_input["generated_image"]), Path(runtime_input["twin_image"])
    for key, path in (("generated_image", generated), ("twin_image", twin)):
        if sha256(path) != record["images"][key]["sha256"]:
            raise ValueError(f"{record['id']}: source image hash mismatch")
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    sent_metadata = {
        "product_type": runtime_input["product_type"],
        "image_stage": runtime_input["image_stage"],
        "scene_prompt": runtime_input["scene_prompt"],
        "requested_component_names": names,
    }
    content = [
        {"type": "text", "text": json.dumps(sent_metadata, separators=(",", ":"))},
        {"type": "text", "text": "A — original full scene image."}, image_content(generated),
        {"type": "text", "text": "B — original digital-twin product reference."}, image_content(twin),
    ]
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": content}]
    request = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_version": PROTOCOL_VERSION,
        "protocol_freeze_sha256": sha256(FREEZE_PATH),
        "protocol_freeze": freeze,
        "record_id": record["id"],
        "cohort": record["cohort"],
        "evaluation_status": record["evaluation_status"],
        "runtime_input": runtime_input,
        "requested_component_names": names,
        "sent_metadata": sent_metadata,
        "images": record["images"],
        "source_trigger": record["source_trigger"],
        "model_requested": model,
        "reasoning_effort": "high",
        "max_completion_tokens": MAX_COMPLETION_TOKENS,
        "max_attempts": MAX_ATTEMPTS,
        "system_prompt_sha256": sha256(PROMPT_PATH),
        "response_schema_sha256": json_sha256(schema),
        "message_order": ["names_only_metadata", "A_scene", "B_twin"],
        "proposal_text_codes_severities_prior_verdicts_comments_passed": False,
    }
    output_dir.mkdir(parents=True)
    atomic_json(output_dir / "request.json", request)
    atomic_json(output_dir / "response_schema.json", schema)
    (output_dir / "system_prompt.md").write_bytes(PROMPT_PATH.read_bytes())
    result = dict(request)
    result["attempts"] = []
    started = time.monotonic()
    try:
        client, mode = CANONICAL.client()
        result["auth_mode"] = mode
        response = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                response = client.chat.completions.create(model=model, reasoning_effort="high", max_completion_tokens=MAX_COMPLETION_TOKENS, messages=messages, response_format={"type": "json_schema", "json_schema": {"name": "independent_component_check", "strict": True, "schema": wire_schema(schema)}})
                result["attempts"].append({"attempt": attempt, "status": "ok"})
                break
            except Exception as error:
                status = getattr(error, "status_code", None)
                result["attempts"].append({"attempt": attempt, "status": status, "error_type": type(error).__name__})
                if attempt == MAX_ATTEMPTS or status not in {429, 500, 502, 503, 504}:
                    raise
                time.sleep(min(8, 2 ** attempt))
        if response is None:
            raise RuntimeError("No response")
        atomic_json(output_dir / "response.json", response.model_dump(mode="json"))
        assessment = json.loads(response.choices[0].message.content)
        validate_response(assessment, schema, names)
        result.update({"ok": True, "assessment": assessment, "model_returned": response.model, "usage": response.usage.model_dump(mode="json") if response.usage else None})
    except Exception as error:
        result.update({"ok": False, "error": {"type": type(error).__name__, "message": str(error)}})
    result["elapsed_seconds"] = round(time.monotonic() - started, 2)
    atomic_json(output_dir / "result.json", result)
    return result

