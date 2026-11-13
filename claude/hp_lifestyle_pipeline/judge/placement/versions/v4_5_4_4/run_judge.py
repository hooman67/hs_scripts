# ruff: noqa: UP017
# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema", "foundry-aws-gateway", "pillow", "opencv-python-headless"]
# ///
"""Independent functional and geometry observers with deterministic V4.5.4.4 synthesis."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any

from geometry import (
    create_furniture_room_crop,
    create_geometry_overlay,
    create_support_crop,
)
from scoring import (
    PlacementValidationError,
    canonical_sha,
    error_sentinel,
    synthesize,
    validate_functional,
    validate_geometry,
)

ROOT = Path(__file__).resolve().parent
PROTOCOL_VERSION = "hp-natural-placement-v4.5.4.4-independent-observers-v1"
FUNCTIONAL_SCHEMA = json.loads((ROOT / "functional_observer_schema.json").read_text())
FUNCTIONAL_WIRE = json.loads((ROOT / "functional_observer_wire_schema.json").read_text())
GEOMETRY_SCHEMA = json.loads((ROOT / "geometry_observer_schema.json").read_text())
GEOMETRY_WIRE = json.loads((ROOT / "geometry_observer_wire_schema.json").read_text())
SUPPORTED_MIMES = {"image/png", "image/jpeg", "image/webp"}

def file_sha(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def atomic_json(path: Path, value: Any) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    os.replace(temporary, path)

def _protocol_hashes() -> dict[str, Any]:
    return {
        "system_prompt_sha256": {
            "functional": file_sha(ROOT / "functional_observer_system.md"),
            "geometry": file_sha(ROOT / "geometry_observer_system.md"),
        },
        "schema_sha256": {name: file_sha(ROOT / name) for name in (
            "functional_observer_schema.json", "functional_observer_wire_schema.json",
            "geometry_observer_schema.json", "geometry_observer_wire_schema.json",
        )},
        "geometry_algorithms_sha256": file_sha(ROOT / "geometry.py"),
        "synthesis_sha256": file_sha(ROOT / "scoring.py"),
        "taxonomy_sha256": file_sha(ROOT / "codebook.py"),
        "runtime_environment_sha256": file_sha(ROOT / "runtime_environment.json"),
        "runner_sha256": file_sha(ROOT / "run_judge.py"),
    }

def client():
    import foundry_aws_gateway.llm
    return foundry_aws_gateway.llm.get_openai().with_options(timeout=600.0, max_retries=0), "foundry_direct_openai"

def _mime(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in SUPPORTED_MIMES:
        raise PlacementValidationError([f"unsupported image format: {path}"])
    return mime

def _image(path: Path, detail: str = "high") -> dict[str, Any]:
    return {"type": "image_url", "image_url": {"url": f"data:{_mime(path)};base64," + base64.b64encode(path.read_bytes()).decode(), "detail": detail}}

def _model_matches(requested: str, returned: Any) -> bool:
    return isinstance(returned, str) and re.fullmatch(rf"{re.escape(requested)}(?:-\d{{4}}-\d{{2}}-\d{{2}})?", returned) is not None

def _validate_runtime(runtime: Mapping[str, Any]) -> None:
    errors = []
    for key in ("generated_image", "twin_image", "product_type"):
        if key not in runtime:
            errors.append(f"missing required field: {key}")
    if runtime.get("product_type") not in {"laptop", "printer"}:
        errors.append("product_type must be laptop or printer")
    for key in ("generated_image", "twin_image"):
        if key in runtime and not Path(str(runtime[key])).is_file():
            errors.append(f"file not found: {runtime[key]}")
    if errors:
        raise PlacementValidationError(errors)

def _functional_content(runtime: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"type": "text", "text": "TARGET DATA — no scene prompt, label, score, prior answer, or expected result is supplied.\n" + json.dumps({"product_type": runtime["product_type"]})},
        {"type": "text", "text": "RAW_SCENE — authoritative complete generated scene"},
        _image(Path(runtime["generated_image"]), "high"),
        {"type": "text", "text": "ORIGINAL_TWIN — product identity and functional-front reference only"},
        _image(Path(runtime["twin_image"]), "high"),
    ]

def _geometry_content(
    runtime: Mapping[str, Any], product_crop: Path, room_crop: Path, overlay: Path,
    product_meta: Mapping[str, Any], room_meta: Mapping[str, Any], overlay_meta: Mapping[str, Any],
) -> list[dict[str, Any]]:
    return [
        {"type": "text", "text": "TARGET DATA — no scene prompt, label, score, prior answer, or expected result is supplied.\n" + json.dumps({"product_type": runtime["product_type"]})},
        {"type": "text", "text": "RAW_SCENE — authoritative complete generated scene"},
        _image(Path(runtime["generated_image"]), "high"),
        {"type": "text", "text": "ORIGINAL_TWIN — footprint and functional-front identity only"},
        _image(Path(runtime["twin_image"]), "high"),
        {"type": "text", "text": "PRODUCT_SUPPORT_CROP — deterministic unwarped attention aid; raw pixels control"},
        _image(product_crop, "high"),
        {"type": "text", "text": "FURNITURE_ROOM_CROP — deterministic larger unwarped context aid; raw pixels control"},
        _image(room_crop, "high"),
        {"type": "text", "text": "ALGORITHMIC_EDGE_AID — OPTIONAL NAVIGATION AID WITH POSSIBLE FALSE OR MISSING LINES"},
        _image(overlay, "high"),
        {"type": "text", "text": "AID PROVENANCE — never visual proof\n" + json.dumps({
            "product_crop": {key: product_meta.get(key) for key in ("localization_status", "device_box", "crop_box_full_scene_pixels", "fallback_reason")},
            "room_crop": {key: room_meta.get(key) for key in ("crop_box_full_scene_pixels", "unwarped", "scope_notice")},
            "overlay": {key: overlay_meta.get(key) for key in ("selected_segment_count", "localized_device_box_in_overlay", "scope_notice")},
        }, ensure_ascii=False)},
    ]

def _call_stage(
    *, api: Any, model: str, stage: str, system: str, content: list[dict[str, Any]],
    wire_schema: Mapping[str, Any], validator: Callable[[Mapping[str, Any]], Any],
    output_dir: Path, raw_calls: list[dict[str, Any]], repair_budget: list[int],
    max_completion_tokens: int,
) -> Mapping[str, Any]:
    messages: list[dict[str, Any]] = [{"role": "system", "content": system}, {"role": "user", "content": content}]
    stage_attempt = 0
    while True:
        if len(raw_calls) >= 3:
            raise PlacementValidationError(["global model-call limit of 3 exhausted"])
        stage_attempt += 1
        global_attempt = len(raw_calls) + 1
        started_at = datetime.now(timezone.utc).isoformat()
        started_clock = perf_counter()
        metadata: dict[str, Any] = {"request_started_at": started_at, "response_finished_at": None, "latency_ms": None, "response_id": None, "finish_reason": None, "prompt_tokens": None, "completion_tokens": None, "reasoning_tokens": None, "total_tokens": None, "refusal": None, "content_bytes": 0, "model_returned": None}
        raw_text = ""
        try:
            response = api.chat.completions.create(
                model=model, reasoning_effort="high", max_completion_tokens=max_completion_tokens,
                messages=messages,
                response_format={"type": "json_schema", "json_schema": {"name": f"hp_placement_v4_5_4_4_{stage}", "strict": True, "schema": wire_schema}},
            )
            choice = response.choices[0]
            raw_text = choice.message.content or ""
            usage = getattr(response, "usage", None)
            details = getattr(usage, "completion_tokens_details", None)
            metadata.update({
                "response_finished_at": datetime.now(timezone.utc).isoformat(),
                "latency_ms": round((perf_counter() - started_clock) * 1000, 3),
                "response_id": getattr(response, "id", None), "finish_reason": getattr(choice, "finish_reason", None),
                "prompt_tokens": getattr(usage, "prompt_tokens", None), "completion_tokens": getattr(usage, "completion_tokens", None),
                "reasoning_tokens": getattr(details, "reasoning_tokens", None), "total_tokens": getattr(usage, "total_tokens", None),
                "refusal": getattr(choice.message, "refusal", None), "content_bytes": len(raw_text.encode()),
                "model_returned": getattr(response, "model", None),
            })
            atomic_json(output_dir / f"{stage}_attempt_{stage_attempt}_metadata.json", metadata)
            (output_dir / f"{stage}_attempt_{stage_attempt}_response.txt").write_text(raw_text)
            if not _model_matches(model, metadata["model_returned"]):
                raise PlacementValidationError([f"model mismatch requested={model} returned={metadata['model_returned']}"])
            if metadata["refusal"]:
                raise RuntimeError(f"model refusal in {stage}")
            if metadata["finish_reason"] != "stop":
                raise RuntimeError(f"non-stop finish_reason in {stage}: {metadata['finish_reason']}")
            parsed = json.loads(raw_text)
            validator(parsed)
            raw_calls.append({"global_attempt": global_attempt, "stage": stage, "stage_attempt": stage_attempt, "status": "valid", **metadata})
            return parsed
        except Exception as exc:
            if metadata["response_finished_at"] is None:
                metadata["response_finished_at"] = datetime.now(timezone.utc).isoformat()
                metadata["latency_ms"] = round((perf_counter() - started_clock) * 1000, 3)
            objective = isinstance(exc, (PlacementValidationError, json.JSONDecodeError))
            errors = list(exc.errors) if isinstance(exc, PlacementValidationError) else [f"{type(exc).__name__}: {exc}"]
            kind = "invalid" if objective else "transport_error"
            atomic_json(output_dir / f"{stage}_attempt_{stage_attempt}_error.json", {"kind": kind, "errors": errors})
            raw_calls.append({"global_attempt": global_attempt, "stage": stage, "stage_attempt": stage_attempt, "status": kind, "errors": errors, **metadata})
            if repair_budget[0] <= 0:
                raise
            repair_budget[0] -= 1
            if objective and raw_text:
                messages.extend([
                    {"role": "assistant", "content": raw_text},
                    {"role": "user", "content": "Return a complete replacement JSON. Fix only these objective schema/semantic failures; do not change a valid visual conclusion merely to improve it:\n" + json.dumps(errors, ensure_ascii=False)},
                ])

def judge(runtime: Mapping[str, Any], output_dir: Path | str, *, model: str = "gpt-5.5") -> dict[str, Any]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / "result.json"
    _validate_runtime(runtime)
    identity = {
        "scene_sha256": file_sha(runtime["generated_image"]),
        "twin_sha256": file_sha(runtime["twin_image"]),
        "product_type": runtime["product_type"], "model_requested": model,
    }
    hashes = _protocol_hashes()
    if result_path.exists():
        cached = json.loads(result_path.read_text())
        audit = cached.get("audit") or {}
        expected = {"protocol_version": PROTOCOL_VERSION, "input_fingerprint": canonical_sha(identity), **hashes}
        mismatches = [key for key, value in expected.items() if audit.get(key) != value]
        if mismatches:
            raise PlacementValidationError(["stale cache refused; mismatch: " + ", ".join(mismatches)])
        if not audit.get("model_returned"):
            raise PlacementValidationError(["stale cache refused; model_returned missing"])
        return cached
    raw_calls: list[dict[str, Any]] = []
    audit = {"protocol_version": PROTOCOL_VERSION, "model_requested": model, "model_returned": [], "input_fingerprint": canonical_sha(identity), **hashes, "derived_sha256": None}
    try:
        product_crop, product_meta = create_support_crop(runtime["generated_image"], runtime["twin_image"], output_dir)
        room_crop, room_meta = create_furniture_room_crop(runtime["generated_image"], product_crop, output_dir)
        overlay, overlay_meta = create_geometry_overlay(runtime["generated_image"], product_crop, product_meta, output_dir)
        functional_system = (ROOT / "functional_observer_system.md").read_text()
        geometry_system = (ROOT / "geometry_observer_system.md").read_text()
        request = {
            "started_at": datetime.now(timezone.utc).isoformat(), "protocol_version": PROTOCOL_VERSION,
            "input": {key: runtime[key] for key in ("generated_image", "twin_image", "product_type")},
            "identity": identity, "model": model, "reasoning_effort": "high",
            "max_completion_tokens": {"functional_observer": 6500, "geometry_observer": 16000},
            "normal_model_calls": 2, "maximum_model_calls": 3, "global_repair_budget": 1,
            "sdk_retries": 0, "labels_or_scene_prompt_passed_to_model": False,
        }
        atomic_json(output_dir / "request.json", request)
        (output_dir / "functional_observer_system.md").write_text(functional_system)
        (output_dir / "geometry_observer_system.md").write_text(geometry_system)
        atomic_json(output_dir / "functional_observer_schema.json", FUNCTIONAL_SCHEMA)
        atomic_json(output_dir / "geometry_observer_schema.json", GEOMETRY_SCHEMA)
        api, auth_mode = client()
        request["auth_mode"] = auth_mode
        atomic_json(output_dir / "request.json", request)
        repair_budget = [1]
        functional = _call_stage(
            api=api, model=model, stage="functional_observer", system=functional_system,
            content=_functional_content(runtime), wire_schema=FUNCTIONAL_WIRE,
            validator=lambda value: validate_functional(value, runtime["product_type"]),
            output_dir=output_dir, raw_calls=raw_calls, repair_budget=repair_budget, max_completion_tokens=6500,
        )
        geometry = _call_stage(
            api=api, model=model, stage="geometry_observer", system=geometry_system,
            content=_geometry_content(runtime, product_crop, room_crop, overlay, product_meta, room_meta, overlay_meta),
            wire_schema=GEOMETRY_WIRE, validator=validate_geometry,
            output_dir=output_dir, raw_calls=raw_calls, repair_budget=repair_budget, max_completion_tokens=16000,
        )
        derived = synthesize(functional, geometry, runtime["product_type"])
        audit["model_returned"] = sorted({call.get("model_returned") for call in raw_calls if call.get("model_returned")})
        audit["derived_sha256"] = canonical_sha(derived)
        envelope = {
            "schema_version": "hp-natural-placement-v4.5.4.4-result-v1",
            "status": "unassessable" if not derived["score_valid"] else "ok",
            "functional_observer": functional, "geometry_observer": geometry,
            "derived": derived, "error": None, "raw_calls": raw_calls, "audit": audit,
        }
    except Exception as exc:  # noqa: BLE001 - every runtime failure becomes a fail-closed sentinel
        derived = error_sentinel(str(exc))
        audit["model_returned"] = sorted({call.get("model_returned") for call in raw_calls if call.get("model_returned")})
        audit["derived_sha256"] = canonical_sha(derived)
        envelope = {
            "schema_version": "hp-natural-placement-v4.5.4.4-result-v1", "status": "error",
            "functional_observer": None, "geometry_observer": None, "derived": derived,
            "error": {"type": type(exc).__name__, "message": str(exc)},
            "raw_calls": raw_calls, "audit": audit,
        }
    atomic_json(result_path, envelope)
    return envelope

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model", default="gpt-5.5")
    args = parser.parse_args()
    result = judge(json.loads(Path(args.input).read_text()), args.output_dir, model=args.model)
    print(json.dumps({"status": result["status"], "score": result["derived"]["score"], "verdict": result["derived"]["verdict"], "calls": len(result["raw_calls"])}, indent=2))

if __name__ == "__main__":
    main()
