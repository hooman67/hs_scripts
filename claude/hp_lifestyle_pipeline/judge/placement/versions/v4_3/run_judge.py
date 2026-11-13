# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50", "jsonschema", "foundry-aws-gateway", "pillow", "opencv-python-headless"]
# ///
"""V4.3 compact evidence-graph placement judge with bounded objective retry."""

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
from typing import Any, Iterable, Mapping

import foundry_aws_gateway.llm

try:
    from .anchor_selection import CATALOG_PATH, file_sha, select_anchors, validate_catalog
    from .crop import create_support_crop
    from .scoring import ASSESSMENT_SCHEMA, PlacementValidationError, aggregate_assessment, canonical_json_sha256, validate_assessment, validate_result, validate_runtime_input
except ImportError:
    from anchor_selection import CATALOG_PATH, file_sha, select_anchors, validate_catalog
    from crop import create_support_crop
    from scoring import ASSESSMENT_SCHEMA, PlacementValidationError, aggregate_assessment, canonical_json_sha256, validate_assessment, validate_result, validate_runtime_input

ROOT = Path(__file__).resolve().parent
PROTOCOL_VERSION = "hp-natural-placement-v4.3-compact-canary-v1"
SUPPORTED_MIMES = {"image/png", "image/jpeg", "image/webp"}


def atomic_json(path: Path, value: Any) -> None:
    temp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    os.replace(temp, path)


WIRE_SCHEMA_PATH = ROOT / "wire_schema.json"
WIRE_SCHEMA = json.loads(WIRE_SCHEMA_PATH.read_text())
WIRE_SCHEMA_SHA256 = canonical_json_sha256(WIRE_SCHEMA)


def client():
    """Use the documented Direct OpenAI Foundry gateway, with SDK retries disabled."""
    return foundry_aws_gateway.llm.get_openai().with_options(timeout=600.0, max_retries=0), "foundry_direct_openai"


def _mime(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in SUPPORTED_MIMES:
        raise PlacementValidationError([f"unsupported image format: {path}"])
    return mime


def _image_content(path: Path, detail: str) -> dict[str, Any]:
    return {"type": "image_url", "image_url": {"url": f"data:{_mime(path)};base64," + base64.b64encode(path.read_bytes()).decode("ascii"), "detail": detail}}


def _model_matches(requested: str, returned: Any) -> bool:
    return isinstance(returned, str) and re.fullmatch(rf"{re.escape(requested)}(?:-\d{{4}}-\d{{2}}-\d{{2}})?", returned) is not None


def _content(runtime: Mapping[str, Any], crop: Path, provenance: Mapping[str, Any], anchors: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = [{"type": "text", "text": "CALIBRATION EXAMPLES — independent prior scenes. Historical comments are calibration data, not universal rules. Inspect the target independently."}]
    for index, anchor in enumerate(anchors, 1):
        content.append({"type": "text", "text": json.dumps({
            "calibration_example": index,
            "product_type": anchor["product_type"],
            "scene_prompt": anchor["scene_prompt"],
            "comment_exact": anchor["comment_exact"],
            "human_label": anchor["human_label"],
            "scope_notice": "no human verdict means issue-only evidence; preserve weak, borderline, ambiguous, and placement-only qualifications",
        }, ensure_ascii=False)})
        content.append({"type": "text", "text": f"CALIBRATION_EXAMPLE_{index}_GENERATED_SCENE"})
        content.append(_image_content(Path(anchor["generated"]["display_path"]), "high"))
        content.append({"type": "text", "text": f"CALIBRATION_EXAMPLE_{index}_ORIGINAL_TWIN"})
        content.append(_image_content(Path(anchor["twin"]["display_path"]), "low"))
    target_metadata = {"product_type": runtime["product_type"], "scene_prompt": runtime["scene_prompt"]}
    # Optional audit metadata is intentionally omitted from target model content.
    content.extend([
        {"type": "text", "text": "TARGET INPUT — assess only this target. No target label, target comment, or expected answer is provided."},
        {"type": "text", "text": json.dumps(target_metadata, ensure_ascii=False)},
        {"type": "text", "text": "GENERATED_SCENE — complete scene-generation image to assess"},
        _image_content(Path(runtime["generated_image"]), "high"),
        {"type": "text", "text": "ORIGINAL_TWIN — identity and functional-orientation reference only"},
        _image_content(Path(runtime["twin_image"]), "high"),
        {"type": "text", "text": "PRODUCT_SUPPORT_CROP — deterministic unwarped attention aid; may equal full scene"},
        _image_content(crop, "high"),
        {"type": "text", "text": "CROP_PROVENANCE — application generated; never treat localization as geometry proof\n" + json.dumps(provenance, ensure_ascii=False)},
    ])
    return content


def _audit_id(value: Any) -> str:
    return canonical_json_sha256(value)


def _base_audit(runtime: Any, model: str) -> dict[str, Any]:
    identity = runtime
    if isinstance(runtime, Mapping):
        generated = Path(str(runtime.get("generated_image", "")))
        twin = Path(str(runtime.get("twin_image", "")))
        identity = {
            "generated_byte_sha256": file_sha(generated) if generated.is_file() else None,
            "twin_byte_sha256": file_sha(twin) if twin.is_file() else None,
            "product_type": runtime.get("product_type"),
            "scene_prompt_sha256": hashlib.sha256(str(runtime.get("scene_prompt", "")).encode("utf-8")).hexdigest(),
            "optional_audit_metadata": {key: runtime.get(key) for key in ("target_record_id", "device", "camera", "prompt_rank") if runtime.get(key) is not None},
        }
    return {
        "protocol_version": PROTOCOL_VERSION, "model_requested": model, "model_returned": None,
        "input_fingerprint": canonical_json_sha256(identity),
        "system_prompt_sha256": file_sha(ROOT / "system_prompt.md"),
        "assessment_schema_sha256": file_sha(ROOT / "assessment_schema.json"),
        "wire_schema_sha256": file_sha(WIRE_SCHEMA_PATH),
        "scoring_sha256": file_sha(ROOT / "scoring.py"),
        "crop_algorithm_sha256": file_sha(ROOT / "crop.py"),
        "anchor_catalog_sha256": file_sha(CATALOG_PATH),
        "target_record_id": runtime.get("target_record_id") if isinstance(runtime, Mapping) else None,
        "selected_anchor_ids": [], "crop_provenance_sha256": None, "derived_sha256": None,
    }


def judge(
    runtime_input: Mapping[str, Any], output_dir: Path | str, *, model: str = "gpt-5.5",
    exclusion_targets: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    audit = _base_audit(runtime_input, model)
    result_path = output_dir / "result.json"
    if result_path.exists():
        cached = json.loads(result_path.read_text())
        validate_result(cached)
        if cached["audit"]["input_fingerprint"] != audit["input_fingerprint"]:
            raise RuntimeError("cached result belongs to different input")
        return cached
    raw_attempts: list[dict[str, Any]] = []
    request: dict[str, Any] = {}
    try:
        validate_runtime_input(runtime_input)
        if not Path(runtime_input["generated_image"]).is_file() or not Path(runtime_input["twin_image"]).is_file():
            raise PlacementValidationError(["generated_image and twin_image must exist"])
        validate_catalog()
        anchors, anchor_audit = select_anchors(runtime_input, exclusion_targets=exclusion_targets)
        audit["selected_anchor_ids"] = [a["anchor_id"] for a in anchors]
        atomic_json(output_dir / "anchor_selection.json", anchor_audit)
        crop, provenance = create_support_crop(runtime_input["generated_image"], runtime_input["twin_image"], output_dir)
        audit["crop_provenance_sha256"] = file_sha(output_dir / "crop_provenance.json")
        system = (ROOT / "system_prompt.md").read_text()
        request = {
            "started_at": datetime.now(timezone.utc).isoformat(), "protocol_version": PROTOCOL_VERSION,
            "input": dict(runtime_input), "input_fingerprint": audit["input_fingerprint"],
            "image_hashes": {"generated": file_sha(runtime_input["generated_image"]), "twin": file_sha(runtime_input["twin_image"])},
            "model_requested": model, "reasoning_effort": "high", "max_completion_tokens": 24000,
            "max_total_attempts": 2, "sdk_retries": 0, "timeout_seconds": 600,
            "repair_policy": "one replacement only after transport or objective schema/semantic invalidity; never retry a valid judgment",
            "wire_schema_sha256": WIRE_SCHEMA_SHA256, "audit": audit,
        }
        atomic_json(output_dir / "request.json", request)
        (output_dir / "system_prompt.md").write_text(system)
        atomic_json(output_dir / "assessment_schema.json", ASSESSMENT_SCHEMA)
    except Exception as exc:
        raw_attempts.append({"attempt": 1, "audit_id": _audit_id({"error": str(exc)}), "validation_status": "invalid", "finish_reason": None, "total_tokens": None, "refusal": None, "content_bytes": 0})
        envelope = {"schema_version": "hp-natural-placement-v4.3-result-v1", "status": "error", "assessment": None, "derived": None,
                    "error": {"code": "invalid_input", "message": f"{type(exc).__name__}: {exc}"}, "raw_attempts": raw_attempts, "audit": audit}
        validate_result(envelope)
        atomic_json(result_path, envelope)
        return envelope

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system},
        {"role": "user", "content": _content(runtime_input, crop, provenance, anchors)},
    ]
    assessment = None
    last_error: Exception | None = None
    returned_model = None
    api, auth_mode = client()
    request["auth_mode"] = auth_mode
    atomic_json(output_dir / "request.json", request)
    for attempt in (1, 2):
        attempt_meta = {"finish_reason": None, "total_tokens": None, "refusal": None, "content_bytes": 0}
        try:
            response = api.chat.completions.create(
                model=model, reasoning_effort="high", max_completion_tokens=24000, messages=messages,
                response_format={"type": "json_schema", "json_schema": {"name": "hp_natural_placement_v4_3", "strict": True, "schema": WIRE_SCHEMA}},
            )
            returned_model = response.model
            choice = response.choices[0]
            raw_text = choice.message.content or ""
            refusal = getattr(choice.message, "refusal", None)
            usage = getattr(response, "usage", None)
            attempt_meta = {
                "finish_reason": getattr(choice, "finish_reason", None),
                "total_tokens": getattr(usage, "total_tokens", None),
                "refusal": refusal if isinstance(refusal, str) else None,
                "content_bytes": len(raw_text.encode("utf-8")),
            }
            atomic_json(output_dir / f"attempt_{attempt}_metadata.json", {"model_returned": returned_model, **attempt_meta})
            (output_dir / f"attempt_{attempt}_response.txt").write_text(raw_text)
            if not _model_matches(model, returned_model):
                raise PlacementValidationError([f"model mismatch requested={model} returned={returned_model}"])
            parsed = json.loads(raw_text)
            validate_assessment(parsed)
            raw_attempts.append({"attempt": attempt, "audit_id": _audit_id({"model": returned_model, "raw": raw_text, "metadata": attempt_meta}), "validation_status": "valid", **attempt_meta})
            assessment = parsed
            break
        except Exception as exc:
            last_error = exc
            kind = "transport_error" if not isinstance(exc, (PlacementValidationError, json.JSONDecodeError)) else "invalid"
            errors = list(exc.errors) if isinstance(exc, PlacementValidationError) else [f"{type(exc).__name__}: {exc}"]
            error_record = {"attempt": attempt, "kind": kind, "errors": errors}
            atomic_json(output_dir / f"attempt_{attempt}_error.json", error_record)
            raw_attempts.append({"attempt": attempt, "audit_id": _audit_id({"error": error_record, "metadata": attempt_meta}), "validation_status": kind, **attempt_meta})
            if attempt == 2:
                break
            # Repair only objective structure/transport. No labels or expected answers.
            if kind == "invalid":
                messages.extend([
                    {"role": "assistant", "content": (output_dir / f"attempt_{attempt}_response.txt").read_text() if (output_dir / f"attempt_{attempt}_response.txt").exists() else ""},
                    {"role": "user", "content": "Return a complete replacement JSON assessment. Fix only these objective validation failures; do not change a valid visual interpretation merely to improve it:\n" + json.dumps(errors, ensure_ascii=False)},
                ])

    audit["model_returned"] = returned_model
    if assessment is None:
        code = "transport_failure" if raw_attempts and all(a["validation_status"] == "transport_error" for a in raw_attempts) else "invalid_model_output"
        envelope = {"schema_version": "hp-natural-placement-v4.3-result-v1", "status": "error", "assessment": None, "derived": None,
                    "error": {"code": code, "message": f"{type(last_error).__name__}: {last_error}"}, "raw_attempts": raw_attempts, "audit": audit}
    elif assessment["stage_status"] == "unable":
        envelope = {"schema_version": "hp-natural-placement-v4.3-result-v1", "status": "unassessable", "assessment": assessment, "derived": None,
                    "error": None, "raw_attempts": raw_attempts, "audit": audit}
    else:
        derived = aggregate_assessment(assessment)
        audit["derived_sha256"] = canonical_json_sha256(derived)
        envelope = {"schema_version": "hp-natural-placement-v4.3-result-v1", "status": "ok", "assessment": assessment,
                    "derived": derived, "error": None, "raw_attempts": raw_attempts, "audit": audit}
    validate_result(envelope)
    atomic_json(result_path, envelope)
    return envelope


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model", default="gpt-5.5")
    args = parser.parse_args()
    runtime = json.loads(Path(args.input).read_text())
    result = judge(runtime, args.output_dir, model=args.model)
    print(json.dumps({"status": result["status"], "score": (result.get("derived") or {}).get("score"), "verdict": (result.get("derived") or {}).get("verdict")}, indent=2))


if __name__ == "__main__":
    main()
