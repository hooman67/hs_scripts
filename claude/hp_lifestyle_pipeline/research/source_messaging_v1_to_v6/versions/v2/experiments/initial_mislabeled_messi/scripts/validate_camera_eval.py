# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema"]
# ///
"""Validate camera-aware GPT-5.5 outputs, traceability, and deterministic resolution."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


V2_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(__file__).resolve().parents[3]
V1_AUDITOR_PATH = SOURCE_ROOT / "scripts/validate_outputs.py"
sys.path.insert(0, str(V2_ROOT))

from camera_profile_resolver import load_registry, resolve_profile  # noqa: E402

SPEC = importlib.util.spec_from_file_location("v1_output_auditor", V1_AUDITOR_PATH)
assert SPEC and SPEC.loader
V1_AUDITOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V1_AUDITOR)

TARGET_DEVICE_RE = re.compile(
    r"\b(?:laptops?|printers?|computers?|desktops?|monitors?|devices?|hardware|"
    r"screens?|touchscreens?|keyboards?|touchpads?|trackpads?|chassis|ports?|"
    r"lids?|ink\s+tanks?|EliteBook|LaserJet|Smart\s+Tank|SKU)\b|"
    r"\bHP\b|NOTEBOOK-|DESKTOP-|PRINT-",
    re.I,
)
TARGET_TRAY_RE = re.compile(
    r"\b(?:paper|input|output|printer|device)\s+trays?\b|"
    r"\btrays?\s+(?:on|of)\s+(?:the\s+)?(?:printer|device)\b",
    re.I,
)
CAMERA_DIRECTION_RE = re.compile(
    r"\b(?:camera|lens|close[- ]?up|wide[- ]angle|depth of field|"
    r"pull back|zoom|aspect ratio)\b|"
    r"\boverhead\s+(?:view|angle|camera|shot|perspective)\b|"
    r"\b(?:view|angle|camera|shot|perspective)\s+from\s+overhead\b",
    re.I,
)
CAMERA_FIELDS = (
    "requested_tag",
    "resolved_tag",
    "profile_version",
    "resolution",
    "framing",
    "elevation",
    "requested_product",
    "resolved_product",
    "product_resolution",
)


def resolver_expectation(
    registry: dict[str, Any], product_name: str, camera_tag: str
) -> dict[str, Any]:
    resolved = resolve_profile(registry, camera_tag, product_name)
    return {
        "requested_tag": resolved["requested_tag"],
        "resolved_tag": resolved["resolved_tag"],
        "profile_version": resolved["profile_version"],
        "resolution": resolved["resolution"],
        "framing": resolved["effective_profile"]["framing"],
        "elevation": resolved["effective_profile"]["elevation"],
        "requested_product": resolved["requested_product"],
        "resolved_product": resolved["resolved_product"],
        "product_resolution": resolved["product_resolution"],
    }


def validate_case(
    record: dict[str, Any], schema: dict[str, Any], registry: dict[str, Any]
) -> dict[str, Any]:
    case = record["case"]
    failures: list[str] = []
    base = V1_AUDITOR.audit(record, schema)
    failures.extend(base["failures"])
    output = record.get("parsed_output")
    if output is None:
        return {**base, "failures": failures}

    request_input = record.get("request_input") or {}
    raw_source = json.loads(record["raw_input_json"])
    if raw_source != request_input.get("source_messaging"):
        failures.append("Unwrapped raw_input_json does not match request source_messaging")
    if json.loads(record["raw_request_json"]) != request_input:
        failures.append("Raw request JSON does not match recorded request input")

    camera = output["debug"]["camera"]
    expected_camera = resolver_expectation(
        registry, request_input["product_name"], request_input["camera_tag"]
    )
    if case["expected_camera"] != expected_camera:
        failures.append("Manifest camera expectation differs from canonical resolver")
    for field in CAMERA_FIELDS:
        if camera.get(field) != expected_camera.get(field):
            failures.append(
                f"Camera resolver mismatch for {field}: "
                f"{camera.get(field)!r} != {expected_camera.get(field)!r}"
            )
    prompt_ids = [prompt["id"] for prompt in output["prompts"]]
    adjustment_ids = [item["prompt_id"] for item in camera["adjustments"]]
    if sorted(adjustment_ids) != sorted(prompt_ids):
        failures.append("Camera adjustments do not cover exactly the output prompts")

    for prompt in output["prompts"]:
        text = prompt["text"]
        forbidden = TARGET_DEVICE_RE.findall(text) + TARGET_TRAY_RE.findall(text)
        if forbidden:
            failures.append(
                f"{prompt['id']} contains generic or specific target-device wording: "
                + ", ".join(str(value) for value in forbidden)
            )
        camera_terms = CAMERA_DIRECTION_RE.findall(text)
        if camera_terms:
            failures.append(
                f"{prompt['id']} contains camera or framing directions: "
                + ", ".join(camera_terms)
            )

    return {
        **base,
        "failures": list(dict.fromkeys(failures)),
        "expected_camera": expected_camera,
        "actual_camera": {field: camera.get(field) for field in CAMERA_FIELDS},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest", type=Path, default=V2_ROOT / "eval/manifest.json"
    )
    parser.add_argument(
        "--schema", type=Path, default=V2_ROOT / "output.schema.json"
    )
    parser.add_argument(
        "--run-dir", type=Path, default=V2_ROOT / "eval/runs/gpt55_bounded"
    )
    parser.add_argument(
        "--output", type=Path, default=V2_ROOT / "eval/validation.json"
    )
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    registry = load_registry(V2_ROOT / "camera_profiles.json")
    expected_files = {f"{case['case_id']}.json" for case in manifest["cases"]}
    actual_files = {
        path.name
        for path in args.run_dir.glob("*.json")
        if not path.name.endswith(".pending.json") and path.name != "run_summary.json"
    }
    missing = sorted(expected_files - actual_files)
    unexpected = sorted(actual_files - expected_files)
    results = []
    for case in manifest["cases"]:
        path = args.run_dir / f"{case['case_id']}.json"
        if not path.is_file():
            continue
        record = json.loads(path.read_text(encoding="utf-8"))
        failures = []
        if record.get("case_id") != case["case_id"]:
            failures.append("Record case_id does not match manifest")
        if record.get("case") != case:
            failures.append("Recorded case metadata does not match manifest")
        result = validate_case(record, schema, registry)
        result["failures"] = failures + result["failures"]
        results.append({"case_id": case["case_id"], "path": str(path), **result})

    report = {
        "case_count": len(manifest["cases"]),
        "record_count": len(results),
        "missing_records": missing,
        "unexpected_records": unexpected,
        "passed": sum(not result["failures"] for result in results),
        "prompt_count": sum(result.get("prompt_count", 0) for result in results),
        "manual_review_required": [
            "Inventories and local/background object counts",
            "Naturalness and source-cue preservation after camera simplification",
            "Whether the prose asks for geometry that conflicts with the fixed view",
        ],
        "cases": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return int(bool(missing or unexpected or any(r["failures"] for r in results)))


if __name__ == "__main__":
    raise SystemExit(main())
