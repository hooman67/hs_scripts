# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""One-call focused visual scan over the six reused V4.4 development cases."""

from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
import os
from datetime import datetime, timezone
from pathlib import Path

import foundry_aws_gateway.llm

ROOT = Path(__file__).resolve().parent
V44 = ROOT.parent.parent / "v4_4"
RUN_ROOT = ROOT / "runs" / "dev6_once_gpt55"
MODEL = "gpt-5.5"
CHECKS = [
    "support_anatomy",
    "load_path",
    "support_room_placement",
    "device_support_axes",
    "prop_activity_relation",
    "shared_perspective",
    "user_position",
]

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["checks", "general_artifact_warnings"],
    "properties": {
        "checks": {
            "type": "array",
            "minItems": 7,
            "maxItems": 7,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["check_id", "status", "severity", "visible_comparison", "visibility_limit", "region"],
                "properties": {
                    "check_id": {"type": "string", "enum": CHECKS},
                    "status": {"type": "string", "enum": ["defect", "clean", "unknown"]},
                    "severity": {"type": "integer", "minimum": 0, "maximum": 3},
                    "visible_comparison": {"type": "string", "minLength": 1, "maxLength": 700},
                    "visibility_limit": {"type": "string", "minLength": 1, "maxLength": 400},
                    "region": {
                        "anyOf": [
                            {"type": "null"},
                            {
                                "type": "array",
                                "items": {"type": "number", "minimum": 0, "maximum": 1},
                                "minItems": 4,
                                "maxItems": 4,
                            },
                        ]
                    },
                },
            },
        },
        "general_artifact_warnings": {"type": "array", "items": {"type": "string", "minLength": 1, "maxLength": 300}, "maxItems": 5},
    },
}


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def image_part(path: Path) -> dict:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    data = base64.b64encode(path.read_bytes()).decode()
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}", "detail": "high"}}


def check_output(value: dict) -> None:
    if not isinstance(value, dict) or set(value) != {"checks", "general_artifact_warnings"}:
        raise ValueError("response must contain only checks and general_artifact_warnings")
    if not isinstance(value["checks"], list) or len(value["checks"]) != 7:
        raise ValueError("checks must contain exactly seven items")
    if not isinstance(value["general_artifact_warnings"], list):
        raise ValueError("general_artifact_warnings must be an array")
    ids = [item["check_id"] for item in value["checks"]]
    if ids != CHECKS:
        raise ValueError(f"checks must be exact ordered list; got {ids}")
    for item in value["checks"]:
        if set(item) != {"check_id", "status", "severity", "visible_comparison", "visibility_limit", "region"}:
            raise ValueError(f"unexpected check fields: {item.get('check_id')}")
        if item["status"] not in {"defect", "clean", "unknown"}:
            raise ValueError(f"invalid status: {item['check_id']}")
        if not isinstance(item["severity"], int) or not 0 <= item["severity"] <= 3:
            raise ValueError(f"invalid severity: {item['check_id']}")
        expected = item["status"] == "defect"
        if expected != (item["severity"] > 0):
            raise ValueError(f"severity/status mismatch: {item['check_id']}")
        if expected != (item["region"] is not None):
            raise ValueError(f"region/status mismatch: {item['check_id']}")
        if item["region"] is not None and (
            not isinstance(item["region"], list)
            or len(item["region"]) != 4
            or any(not isinstance(v, (int, float)) or not 0 <= v <= 1 for v in item["region"])
        ):
            raise ValueError(f"invalid region: {item['check_id']}")


def main() -> None:
    manifest = json.loads((V44 / "data" / "dev_6_manifest.json").read_text())
    system = (ROOT / "focused_scan_system.md").read_text()
    api = foundry_aws_gateway.llm.get_openai().with_options(timeout=600.0, max_retries=0)
    progress_path = RUN_ROOT / "progress.json"
    progress = json.loads(progress_path.read_text()) if progress_path.exists() else {
        "schema_version": "hp-placement-v4.5-focused-scan-probe-v1",
        "development_only": True,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": None,
        "model": MODEL,
        "system_sha256": hashlib.sha256(system.encode()).hexdigest(),
        "records": [],
    }
    done = {record["record_id"] for record in progress["records"] if record["status"] == "ok"}
    for record in manifest["records"]:
        rid = record["record_id"]
        if rid in done:
            continue
        runtime = record["runtime_input"]
        out = RUN_ROOT / rid
        out.mkdir(parents=True, exist_ok=True)
        content = [
            {"type": "text", "text": "RAW_SCENE — authoritative target pixels"},
            image_part(Path(runtime["generated_image"])),
            {"type": "text", "text": "ORIGINAL_TWIN — product identity and functional-front reference only"},
            image_part(Path(runtime["twin_image"])),
            {"type": "text", "text": f"PRODUCT_TYPE: {runtime['product_type']}. Evaluate all seven fixed checks in order. No scene prompt is supplied."},
        ]
        request = {
            "record_id": rid,
            "model": MODEL,
            "reasoning_effort": "high",
            "system_sha256": hashlib.sha256(system.encode()).hexdigest(),
            "generated_image_sha256": hashlib.sha256(Path(runtime["generated_image"]).read_bytes()).hexdigest(),
            "twin_image_sha256": hashlib.sha256(Path(runtime["twin_image"]).read_bytes()).hexdigest(),
        }
        atomic_json(out / "request.json", request)
        try:
            response = api.chat.completions.create(
                model=MODEL,
                reasoning_effort="high",
                max_completion_tokens=6500,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": content}],
                response_format={"type": "json_schema", "json_schema": {"name": "hp_placement_v45_focused_probe", "strict": True, "schema": SCHEMA}},
            )
            choice = response.choices[0]
            raw = choice.message.content or ""
            (out / "response.txt").write_text(raw)
            parsed = json.loads(raw)
            check_output(parsed)
            atomic_json(out / "result.json", parsed)
            status = "ok"
            error = None
        except Exception as exc:
            status = "error"
            error = f"{type(exc).__name__}: {exc}"
            atomic_json(out / "error.json", {"error": error})
        progress["records"].append({"record_id": rid, "status": status, "error": error})
        atomic_json(progress_path, progress)
        if status != "ok":
            raise RuntimeError(error)
    progress["finished_at"] = datetime.now(timezone.utc).isoformat()
    atomic_json(progress_path, progress)


if __name__ == "__main__":
    main()
