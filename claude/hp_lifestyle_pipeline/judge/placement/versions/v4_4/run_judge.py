# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema", "foundry-aws-gateway", "pillow", "opencv-python-headless"]
# ///
"""Two-pass V4.4 defect scout and independent material-defect verifier."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Mapping

import foundry_aws_gateway.llm

from geometry import create_geometry_overlay, create_support_crop
from scoring import (
    PlacementValidationError,
    canonical_sha,
    defect_proposals,
    error_sentinel,
    reconcile,
    validate_scout,
    validate_verifier,
)

ROOT = Path(__file__).resolve().parent
PROTOCOL_VERSION = "hp-natural-placement-v4.4-two-pass-v2"
SCOUT_SCHEMA = json.loads((ROOT / "scout_schema.json").read_text())
SCOUT_WIRE = json.loads((ROOT / "scout_wire_schema.json").read_text())
VERIFIER_SCHEMA = json.loads((ROOT / "verifier_schema.json").read_text())
VERIFIER_WIRE = json.loads((ROOT / "verifier_wire_schema.json").read_text())
SUPPORTED_MIMES = {"image/png", "image/jpeg", "image/webp"}


def file_sha(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    os.replace(temporary, path)


def _protocol_hashes() -> dict[str, Any]:
    return {
        "system_prompt_sha256": {"scout": file_sha(ROOT / "scout_system_prompt.md"), "verifier": file_sha(ROOT / "verifier_system_prompt.md")},
        "schema_sha256": {name: file_sha(ROOT / name) for name in ("scout_schema.json", "scout_wire_schema.json", "verifier_schema.json", "verifier_wire_schema.json")},
        "scoring_sha256": file_sha(ROOT / "scoring.py"),
        "geometry_sha256": file_sha(ROOT / "geometry.py"),
        "runner_sha256": file_sha(ROOT / "run_judge.py"),
    }


def client():
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
    for key in ("generated_image", "twin_image", "product_type", "scene_prompt"):
        if key not in runtime:
            errors.append(f"missing required field: {key}")
    if runtime.get("product_type") not in {"laptop", "printer"}:
        errors.append("product_type must be laptop or printer")
    for key in ("generated_image", "twin_image"):
        if key in runtime and not Path(str(runtime[key])).is_file():
            errors.append(f"file not found: {runtime[key]}")
    if errors:
        raise PlacementValidationError(errors)


def _images_and_context(runtime: Mapping[str, Any], crop: Path, overlay: Path, crop_provenance: Mapping[str, Any], overlay_provenance: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"type": "text", "text": "TARGET DATA — assess only raw target pixels; no evaluation label or expected answer is provided.\n" + json.dumps({"product_type": runtime["product_type"], "scene_prompt": runtime["scene_prompt"]}, ensure_ascii=False)},
        {"type": "text", "text": "RAW_SCENE — authoritative complete scene image"},
        _image(Path(runtime["generated_image"]), "high"),
        {"type": "text", "text": "ORIGINAL_TWIN — identity and functional-front reference only"},
        _image(Path(runtime["twin_image"]), "high"),
        {"type": "text", "text": "PRODUCT_SUPPORT_CROP — deterministic unwarped attention aid; raw scene controls"},
        _image(crop, "high"),
        {"type": "text", "text": "ALGORITHMIC_EDGE_AID — POSSIBLE FALSE OR MISSING LINES — RAW PIXELS CONTROL"},
        _image(overlay, "high"),
        {"type": "text", "text": "AID PROVENANCE — never geometry proof\n" + json.dumps({
            "crop": {key: crop_provenance.get(key) for key in ("localization_status", "device_box", "crop_box_full_scene_pixels", "fallback_reason")},
            "overlay": {key: overlay_provenance.get(key) for key in ("selected_segment_count", "localized_device_box_in_overlay", "scope_notice")},
        }, ensure_ascii=False)},
    ]


def _call_stage(
    *,
    api: Any,
    model: str,
    stage: str,
    system: str,
    content: list[dict[str, Any]],
    wire_schema: Mapping[str, Any],
    validator: Callable[[Mapping[str, Any]], Any],
    output_dir: Path,
    raw_calls: list[dict[str, Any]],
    repair_budget: list[int],
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
        metadata = {"request_started_at": started_at, "response_finished_at": None, "latency_ms": None, "response_id": None, "finish_reason": None, "prompt_tokens": None, "completion_tokens": None, "reasoning_tokens": None, "total_tokens": None, "refusal": None, "content_bytes": 0}
        raw_text = ""
        try:
            response = api.chat.completions.create(
                model=model,
                reasoning_effort="high",
                max_completion_tokens=max_completion_tokens,
                messages=messages,
                response_format={"type": "json_schema", "json_schema": {"name": f"hp_placement_v4_4_{stage}", "strict": True, "schema": wire_schema}},
            )
            choice = response.choices[0]
            raw_text = choice.message.content or ""
            usage = getattr(response, "usage", None)
            completion_details = getattr(usage, "completion_tokens_details", None)
            metadata = {
                "request_started_at": started_at,
                "response_finished_at": datetime.now(timezone.utc).isoformat(),
                "latency_ms": round((perf_counter() - started_clock) * 1000, 3),
                "response_id": getattr(response, "id", None),
                "finish_reason": getattr(choice, "finish_reason", None),
                "prompt_tokens": getattr(usage, "prompt_tokens", None),
                "completion_tokens": getattr(usage, "completion_tokens", None),
                "reasoning_tokens": getattr(completion_details, "reasoning_tokens", None),
                "total_tokens": getattr(usage, "total_tokens", None),
                "refusal": getattr(choice.message, "refusal", None),
                "content_bytes": len(raw_text.encode()),
                "model_returned": response.model,
            }
            atomic_json(output_dir / f"{stage}_attempt_{stage_attempt}_metadata.json", metadata)
            (output_dir / f"{stage}_attempt_{stage_attempt}_response.txt").write_text(raw_text)
            if not _model_matches(model, response.model):
                raise PlacementValidationError([f"model mismatch requested={model} returned={response.model}"])
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
            if objective:
                messages.extend([
                    {"role": "assistant", "content": raw_text},
                    {"role": "user", "content": "Return a complete replacement JSON. Fix only these objective validation failures; do not alter a valid visual conclusion merely to improve it:\n" + json.dumps(errors, ensure_ascii=False)},
                ])


def judge(runtime: Mapping[str, Any], output_dir: Path | str, *, model: str = "gpt-5.5") -> dict[str, Any]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / "result.json"
    _validate_runtime(runtime)
    identity = {
        "scene_sha256": file_sha(runtime["generated_image"]),
        "twin_sha256": file_sha(runtime["twin_image"]),
        "product_type": runtime["product_type"],
        "scene_prompt_sha256": hashlib.sha256(runtime["scene_prompt"].encode()).hexdigest(),
    }
    current_hashes = _protocol_hashes()
    if result_path.exists():
        cached = json.loads(result_path.read_text())
        audit = cached.get("audit") or {}
        expected = {"protocol_version": PROTOCOL_VERSION, "input_fingerprint": canonical_sha(identity), **current_hashes}
        mismatches = [key for key, value in expected.items() if audit.get(key) != value]
        if mismatches:
            raise PlacementValidationError(["stale cache refused; mismatch: " + ", ".join(mismatches)])
        return cached
    raw_calls: list[dict[str, Any]] = []
    audit = {
        "protocol_version": PROTOCOL_VERSION,
        "model_requested": model,
        "model_returned": [],
        "input_fingerprint": canonical_sha(identity),
        **current_hashes,
        "derived_sha256": None,
    }
    try:
        crop, crop_provenance = create_support_crop(runtime["generated_image"], runtime["twin_image"], output_dir)
        overlay, overlay_provenance = create_geometry_overlay(runtime["generated_image"], crop, crop_provenance, output_dir)
        scout_system = (ROOT / "scout_system_prompt.md").read_text()
        verifier_system = (ROOT / "verifier_system_prompt.md").read_text()
        context = _images_and_context(runtime, crop, overlay, crop_provenance, overlay_provenance)
        request = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "protocol_version": PROTOCOL_VERSION,
            "input": {key: runtime[key] for key in ("generated_image", "twin_image", "product_type", "scene_prompt")},
            "identity": identity,
            "model": model,
            "reasoning_effort": "high",
            "max_completion_tokens": {"scout": 9000, "verifier": 4000},
            "maximum_model_calls": 3,
            "global_objective_repair_budget": 1,
            "sdk_retries": 0,
            "labels_passed_to_model": False,
        }
        atomic_json(output_dir / "request.json", request)
        (output_dir / "scout_system_prompt.md").write_text(scout_system)
        (output_dir / "verifier_system_prompt.md").write_text(verifier_system)
        atomic_json(output_dir / "scout_schema.json", SCOUT_SCHEMA)
        atomic_json(output_dir / "verifier_schema.json", VERIFIER_SCHEMA)
        api, auth_mode = client()
        request["auth_mode"] = auth_mode
        atomic_json(output_dir / "request.json", request)
        repair_budget = [1]
        scout = _call_stage(
            api=api, model=model, stage="scout", system=scout_system, content=context,
            wire_schema=SCOUT_WIRE, validator=validate_scout, output_dir=output_dir,
            raw_calls=raw_calls, repair_budget=repair_budget, max_completion_tokens=9000,
        )
        proposals = defect_proposals(scout)
        verifier_content = context + [{"type": "text", "text": "SCOUT_DEFECT_PROPOSALS — independently verify every item; an empty list requires verified status and empty results. These are hypotheses, not evidence.\n" + json.dumps(proposals, ensure_ascii=False)}]
        verifier = _call_stage(
            api=api, model=model, stage="verifier", system=verifier_system, content=verifier_content,
            wire_schema=VERIFIER_WIRE, validator=lambda value: validate_verifier(value, proposals), output_dir=output_dir,
            raw_calls=raw_calls, repair_budget=repair_budget, max_completion_tokens=4000,
        )
        derived = reconcile(scout, verifier)
        audit["model_returned"] = sorted({call.get("model_returned") for call in raw_calls if call.get("model_returned")})
        audit["derived_sha256"] = canonical_sha(derived)
        envelope = {
            "schema_version": "hp-natural-placement-v4.4-result-v1",
            "status": "unassessable" if not derived["score_valid"] else "ok",
            "scout": scout,
            "defect_proposals": proposals,
            "verifier": verifier,
            "derived": derived,
            "error": None,
            "raw_calls": raw_calls,
            "audit": audit,
        }
    except Exception as exc:
        derived = error_sentinel(str(exc))
        audit["derived_sha256"] = canonical_sha(derived)
        envelope = {
            "schema_version": "hp-natural-placement-v4.4-result-v1",
            "status": "error",
            "scout": None,
            "defect_proposals": [],
            "verifier": None,
            "derived": derived,
            "error": {"type": type(exc).__name__, "message": str(exc)},
            "raw_calls": raw_calls,
            "audit": audit,
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
    print(json.dumps({"status": result["status"], "score": (result.get("derived") or {}).get("score"), "verdict": (result.get("derived") or {}).get("verdict"), "calls": len(result["raw_calls"])}, indent=2))


if __name__ == "__main__":
    main()
