#!/usr/bin/env python3
"""Apply the approved minimal review plan and validate every complete V5 bank."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VERSION = ROOT / "research/source_messaging_v1_to_v6/versions/v5"
sys.path.insert(0, str(VERSION / "scripts"))

from camera_profile_resolver import load_registry  # noqa: E402
from validate_output import validate_output  # noqa: E402


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_sha(value: Any) -> str:
    return sha_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prompt_by_id(output: dict[str, Any], prompt_id: str) -> dict[str, Any]:
    matches = [item for item in output["prompts"] if item["id"] == prompt_id]
    if len(matches) != 1:
        raise ValueError(f"prompt path did not resolve uniquely: {prompt_id}")
    return matches[0]


def evidence_by_id(output: dict[str, Any], evidence_id: str) -> dict[str, Any]:
    matches = [item for item in output["debug"]["source_evidence"] if item["id"] == evidence_id]
    if len(matches) != 1:
        raise ValueError(f"evidence path did not resolve uniquely: {evidence_id}")
    return matches[0]


def resolve_path(output: dict[str, Any], path: str) -> tuple[dict[str, Any], str]:
    parts = path.strip("/").split("/")
    if len(parts) >= 3 and parts[0] == "prompts":
        current: Any = prompt_by_id(output, parts[1])
        parts = parts[2:]
    elif len(parts) >= 4 and parts[:2] == ["debug", "source_evidence"]:
        current = evidence_by_id(output, parts[2])
        parts = parts[3:]
    else:
        raise ValueError(f"unsupported review path: {path}")
    for part in parts[:-1]:
        current = current[part]
    return current, parts[-1]


def main() -> None:
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    plan = json.loads((HERE / "review_plan.json").read_text(encoding="utf-8"))
    schema = json.loads((VERSION / "output.schema.json").read_text(encoding="utf-8"))
    registry = load_registry(VERSION / "camera_profiles.json")
    reviewed_cases: dict[str, Any] = {}
    edit_count = 0

    for case in manifest["cases"]:
        case_id = case["case_id"]
        normalized_matches = list((HERE / "normalized_outputs").glob(f"{case_id}__*.json"))
        if len(normalized_matches) != 1:
            raise ValueError(f"expected one normalized output for {case_id}; got {normalized_matches}")
        normalized_path = normalized_matches[0]
        original = json.loads(normalized_path.read_text(encoding="utf-8"))
        reviewed = copy.deepcopy(original)
        edits = []
        for operation in plan["cases"].get(case_id, []):
            parent, key = resolve_path(reviewed, operation["path"])
            if parent[key] != operation["before"]:
                raise ValueError(f"review-plan drift at {case_id}{operation['path']}")
            parent[key] = operation["after"]
            edits.append(operation)
            edit_count += 1

        input_payload = json.loads(Path(case["input_path"]).read_text(encoding="utf-8"))
        validation = validate_output(reviewed, input_payload, schema, registry)
        if not validation["passed"]:
            raise ValueError(f"reviewed output failed validation for {case_id}: {validation['errors']}")
        reviewed_path = HERE / "reviewed_outputs" / f"{case_id}.json"
        write_json(reviewed_path, reviewed)
        log = {
            "version": "hp-lifestyle-dual-source-v5-top6-review-log-v1",
            "case_id": case_id,
            "normalized_output_path": str(normalized_path),
            "normalized_output_sha256": sha_bytes(normalized_path.read_bytes()),
            "reviewed_output_path": str(reviewed_path),
            "reviewed_output_sha256": sha_bytes(reviewed_path.read_bytes()),
            "reviewed_output_semantic_sha256": canonical_sha(reviewed),
            "text_changed": any(op["path"].endswith("/text") for op in edits),
            "edit_count": len(edits),
            "edits": edits,
        }
        log_path = HERE / "review_logs" / f"{case_id}.json"
        write_json(log_path, log)
        validation_path = HERE / "validation/reviewed" / f"{case_id}.json"
        write_json(validation_path, validation)
        candidates = [
            {
                "candidate_key": f"{case_id}::{candidate['id']}",
                "rank": rank,
                "text_sha256": sha_bytes(candidate["text"].encode("utf-8")),
                **candidate,
            }
            for rank, candidate in enumerate(reviewed["prompts"], 1)
        ]
        reviewed_cases[case_id] = {
            **case,
            "status": "reviewed_validator_passed",
            "human_review_status": "reviewed",
            "reviewed_output_path": str(reviewed_path),
            "reviewed_output_sha256": log["reviewed_output_sha256"],
            "review_log_path": str(log_path),
            "review_validation_path": str(validation_path),
            "review_edit_count": len(edits),
            "candidates": candidates,
            "debug": reviewed["debug"],
        }

    output = {
        "version": "hp-lifestyle-dual-source-v5-top6-reviewed-prompt-cases-v1",
        "status": "reviewed_validator_passed",
        "manifest_path": str(HERE / "manifest.json"),
        "manifest_sha256": sha_bytes((HERE / "manifest.json").read_bytes()),
        "review_plan_path": str(HERE / "review_plan.json"),
        "review_plan_sha256": sha_bytes((HERE / "review_plan.json").read_bytes()),
        "counts": {
            "cases": len(reviewed_cases),
            "candidates": sum(len(item["candidates"]) for item in reviewed_cases.values()),
            "review_edits": edit_count,
            "cases_with_edits": sum(bool(item["review_edit_count"]) for item in reviewed_cases.values()),
        },
        "cases": reviewed_cases,
    }
    write_json(HERE / "reviewed_prompt_cases.json", output)
    print(json.dumps(output["counts"], indent=2))


if __name__ == "__main__":
    main()
