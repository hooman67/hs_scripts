#!/usr/bin/env python3
"""Build two isolated one-document V5 scoring-contract smoke inputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PILOT = HERE.parent
ROOT = HERE.parents[2]
VERSION = ROOT / "research/source_messaging_v1_to_v6/versions/v5"

CASE_SPECS = (
    {
        "case_id": "empty_brief__elitebook_source__laptop_FrontRightCloseUp",
        "source_wrapper": PILOT / "inputs/elitebook__laptop_FrontRightCloseUp.json",
        "camera_tag": "laptop_FrontRightCloseUp",
        "empty_document": "smart_brief",
        "nonempty_document": "source_messaging",
    },
    {
        "case_id": "deskjet_brief__empty_source__printer_FrontRightCloseUp",
        "source_wrapper": PILOT / "inputs/deskjet_2955__printer_FrontRightCloseUp.json",
        "camera_tag": "printer_FrontRightCloseUp",
        "empty_document": "source_messaging",
        "nonempty_document": "smart_brief",
    },
)


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def canonical_sha(value: Any) -> str:
    return sha_bytes(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    )


def record(path: Path) -> dict[str, Any]:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha_file(path)}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    cases = []
    for spec in CASE_SPECS:
        source = json.loads(spec["source_wrapper"].read_text(encoding="utf-8"))
        if set(source) != {"smart_brief", "source_messaging", "camera_tag"}:
            raise ValueError(f"source wrapper contract changed: {spec['source_wrapper']}")
        payload = {
            "smart_brief": source["smart_brief"],
            "source_messaging": source["source_messaging"],
            "camera_tag": spec["camera_tag"],
        }
        payload[spec["empty_document"]] = ""
        if payload[spec["nonempty_document"]] == "":
            raise ValueError(f"nonempty smoke document is empty: {spec['case_id']}")
        if payload[spec["empty_document"]] != "":
            raise AssertionError("empty document construction failed")
        input_path = HERE / "inputs" / f"{spec['case_id']}.json"
        write_json(input_path, payload)
        cases.append(
            {
                "case_id": spec["case_id"],
                "camera_tag": spec["camera_tag"],
                "empty_document": spec["empty_document"],
                "nonempty_document": spec["nonempty_document"],
                "source_wrapper_path": str(spec["source_wrapper"]),
                "source_wrapper_sha256": sha_file(spec["source_wrapper"]),
                "input_path": str(input_path),
                "input_sha256": sha_file(input_path),
                "input_semantic_sha256": canonical_sha(payload),
                "human_review_status": "pending",
                "launchable": False,
            }
        )

    manifest = {
        "version": "hp-lifestyle-v5-scoring-contract-smoke-v1",
        "as_of": "2026-10-27",
        "status": "authorized_two_case_isolated_scoring_contract_smoke",
        "separate_from_main_review_set": True,
        "main_manifest_path": str(PILOT / "manifest.json"),
        "main_manifest_sha256": sha_file(PILOT / "manifest.json"),
        "scope": {
            "case_count": 2,
            "candidates_per_case": 20,
            "candidate_count": 40,
            "semantic_attempts_per_exact_request": 1,
            "max_concurrency": 2,
            "max_transport_attempts": 100,
            "image_generation_authorized": False,
            "modric_included": False,
        },
        "model": {
            "deployment": "gpt-5.5",
            "reasoning_effort": "medium",
            "max_completion_tokens": 24000,
            "temperature": None,
            "strict_output_schema": True,
            "client_timeout_seconds": 120,
        },
        "scoring_contract": {
            "aggregation": "sum of per-component maximum across the two documents",
            "components": ["setting", "activity", "materials", "use_context"],
            "empty_document_components_must_be_zero": True,
            "missing_document_penalty": False,
            "full_score_from_either_document_possible": True,
        },
        "provenance": {
            "system_prompt": record(VERSION / "system_prompt.md"),
            "input_schema": record(VERSION / "input.schema.json"),
            "output_schema": record(VERSION / "output.schema.json"),
            "camera_profiles": record(VERSION / "camera_profiles.json"),
            "reference_library": record(VERSION / "reference_library.json"),
            "finalizer": record(VERSION / "scripts/finalize_output.py"),
            "validator": record(VERSION / "scripts/validate_output.py"),
        },
        "authorized_case_ids": [case["case_id"] for case in cases],
        "cases": cases,
    }
    manifest_path = HERE / "manifest.json"
    write_json(manifest_path, manifest)
    print(
        json.dumps(
            {
                "manifest": str(manifest_path),
                "manifest_sha256": sha_file(manifest_path),
                "system_prompt_sha256": manifest["provenance"]["system_prompt"]["sha256"],
                "cases": len(cases),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
