# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "tomli", "pyyaml", "requests"]
# ///
"""Verify proposed compact-V3 component additions against original images."""

from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import json
import mimetypes
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent
V3_ROOT = ROOT.parents[1]
PROMPT_PATH = ROOT / "system_prompt.md"
TRIGGER_PATH = ROOT / "triggers.json"
FREEZE_PATH = ROOT / "freeze.json"
RUNS_ROOT = ROOT / "runs"
PROTOCOL_VERSION = "placement-addition-verifier-v1"
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
SCORING = load_module("placement_verifier_scoring", V3_ROOT / "scoring.py")
CANONICAL = load_module("placement_verifier_client", V3_ROOT / "run_judge.py")
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


def response_schema(component_names: list[str]) -> dict[str, Any]:
    if not component_names or len(component_names) != len(set(component_names)):
        raise ValueError("Proposed component names must be nonempty and unique")
    invalid = set(component_names) - set(DEFINITIONS)
    if invalid:
        raise ValueError(f"Unknown proposed components: {sorted(invalid)}")
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "components"],
        "properties": {
            "schema_version": {"type": "string", "const": "placement-verifier-components-v1"},
            "components": {
                "type": "object",
                "additionalProperties": False,
                "required": component_names,
                "properties": {name: copy.deepcopy(DEFINITIONS[name]) for name in component_names},
            },
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
        raise ValueError("Verifier dropped or added a proposed component")
    for name, component in value["components"].items():
        visibility, severity = component["visibility"], component["severity"]
        confidence, codes = component["confidence"], component["issue_codes"]
        if not component["evidence"].strip():
            raise ValueError(f"{name}: evidence must contain non-whitespace text")
        if visibility == "unobservable":
            if severity is not None or confidence != "low" or codes:
                raise ValueError(f"{name}: invalid unobservable component")
        elif severity is None:
            raise ValueError(f"{name}: assessable component requires severity")
        if severity == 0 and codes:
            raise ValueError(f"{name}: severity zero requires no codes")
        if isinstance(severity, int) and severity > 0 and not codes:
            raise ValueError(f"{name}: positive severity requires codes")


def current_freeze() -> dict[str, Any]:
    value = {
        "schema_version": "placement-addition-verifier-freeze-v1",
        "protocol_version": PROTOCOL_VERSION,
        "model": "gpt-5.5",
        "reasoning_effort": "high",
        "max_attempts": MAX_ATTEMPTS,
        "hashes": {
            "runner_sha256": sha256(__file__),
            "batch_sha256": sha256(ROOT / "run_batch.py"),
            "merge_sha256": sha256(ROOT / "merge_verified.py"),
            "merge_v2_sha256": sha256(ROOT / "merge_verified_v2.py"),
            "trigger_builder_sha256": sha256(ROOT / "build_triggers.py"),
            "trigger_manifest_sha256": sha256(TRIGGER_PATH),
            "system_prompt_sha256": sha256(PROMPT_PATH),
            "v3_schema_sha256": sha256(V3_ROOT / "observation_schema.json"),
            "v3_scoring_sha256": sha256(V3_ROOT / "scoring.py"),
            "v3_runner_sha256": sha256(V3_ROOT / "run_judge.py"),
        },
    }
    selected = ROOT / "selected_protocol_v2.json"
    selected_snapshot = ROOT / "selected_protocol_snapshot_manifest.json"
    if selected.exists() or selected_snapshot.exists():
        if not selected.exists() or not selected_snapshot.exists():
            raise RuntimeError("Selected protocol freeze files must be present together")
        value["selected_protocol"] = {
            "path": str(selected.resolve()),
            "sha256": sha256(selected),
            "snapshot_manifest_path": str(selected_snapshot.resolve()),
            "snapshot_manifest_sha256": sha256(selected_snapshot),
        }
    return value


def ensure_frozen() -> dict[str, Any]:
    frozen = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    current = current_freeze()
    for key in current:
        if frozen.get(key) != current[key]:
            raise RuntimeError(f"Verifier freeze mismatch: {key}")
    return frozen


def image_content(path: Path) -> dict[str, Any]:
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in {"image/png", "image/jpeg", "image/webp"}:
        raise ValueError(f"Unsupported image: {path}")
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode(), "detail": "high"}}


def verify(record: Mapping[str, Any], output_dir: Path, model: str = "gpt-5.5") -> dict[str, Any]:
    freeze = ensure_frozen()
    if output_dir.exists():
        raise FileExistsError(output_dir)
    runtime_input = record["runtime_input"]
    SCORING.validate_runtime_input(runtime_input)
    names = list(record["proposed_components"])
    schema = response_schema(names)
    generated, twin = Path(runtime_input["generated_image"]), Path(runtime_input["twin_image"])
    for key, path in (("generated_image", generated), ("twin_image", twin)):
        if sha256(path) != record["images"][key]["sha256"]:
            raise ValueError(f"{record['id']}: source image hash mismatch")
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    content = [
        {"type": "text", "text": json.dumps({"product_type": runtime_input["product_type"], "image_stage": runtime_input["image_stage"], "scene_prompt": runtime_input["scene_prompt"], "proposed_components": record["proposed_components"]}, separators=(",", ":"))},
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
        "runtime_input": runtime_input,
        "proposed_components": record["proposed_components"],
        "proposed_component_names": names,
        "proposal_sha256": json_sha256(record["proposed_components"]),
        "source_provenance": record["source_provenance"],
        "images": record["images"],
        "model_requested": model,
        "reasoning_effort": "high",
        "max_completion_tokens": MAX_COMPLETION_TOKENS,
        "max_attempts": MAX_ATTEMPTS,
        "system_prompt_sha256": sha256(PROMPT_PATH),
        "response_schema_sha256": json_sha256(schema),
        "message_order": ["metadata_and_fallible_proposals", "A_scene", "B_twin"],
        "comments_or_expectations_passed": False,
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
                response = client.chat.completions.create(model=model, reasoning_effort="high", max_completion_tokens=MAX_COMPLETION_TOKENS, messages=messages, response_format={"type": "json_schema", "json_schema": {"name": "component_verification", "strict": True, "schema": wire_schema(schema)}})
                result["attempts"].append({"attempt": attempt, "status": "ok"})
                break
            except Exception as error:
                status = getattr(error, "status_code", None)
                result["attempts"].append({"attempt": attempt, "status": status, "error_type": type(error).__name__})
                if attempt == MAX_ATTEMPTS or status not in {429, 500, 502, 503, 504}:
                    raise
                time.sleep(5)
        assert response is not None
        raw = response.model_dump(mode="json")
        atomic_json(output_dir / "response.json", raw)
        returned = getattr(response, "model", "")
        if not re.fullmatch(rf"{re.escape(model)}(?:-\d{{4}}-\d{{2}}-\d{{2}})?", returned):
            raise RuntimeError("Unexpected returned model")
        choice = response.choices[0]
        if choice.finish_reason != "stop" or choice.message.refusal:
            raise RuntimeError("Incomplete/refused verification")
        assessment = json.loads(choice.message.content)
        validate_response(assessment, schema, names)
        atomic_json(output_dir / "assessment.json", assessment)
        result.update(ok=True, model_returned=returned, usage=raw.get("usage"), assessment=assessment)
    except Exception as error:
        result.update(ok=False, error_type=type(error).__name__, status_code=getattr(error, "status_code", None), error_message=str(error))
    result["elapsed_seconds"] = round(time.monotonic() - started, 2)
    atomic_json(output_dir / "result.json", result)
    return result
