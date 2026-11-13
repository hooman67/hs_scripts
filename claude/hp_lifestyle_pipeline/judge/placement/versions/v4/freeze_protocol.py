#!/usr/bin/env python3
"""Freeze the exact V4 development protocol before model evaluation."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "data/protocol_freeze_development_15_v4_astra.json"
FILES = [
    "system_prompt.md",
    "assessment_schema.json",
    "result_schema.json",
    "scoring.py",
    "run_judge.py",
    "run_batch.py",
    "test_v4_scoring.py",
    "test_v4_runtime.py",
    "data/development_15_manifest.json",
    "data/development_15_expectations.json",
    "astra/astra_output.md",
    "astra/request_manifest.json",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    artifacts = []
    for relative in FILES:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"Missing freeze artifact: {path}")
        artifacts.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()
    payload = {
        "schema_version": "hp-natural-placement-v4-protocol-freeze-v1",
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "frozen_before_v4_astra_development_evaluation_after_gpt55_quality_stop",
        "git_head_at_freeze": commit,
        "model": "gpt-6-astra",
        "reasoning_effort": "high",
        "client_route": "foundry_direct_openai",
        "expected_returned_model_regex": r"^gpt-6-astra(?:-\d{4}-\d{2}-\d{2})?$",
        "batch_concurrency": 1,
        "transport_sdk_max_retries": 0,
        "transport_timeout_seconds": 600,
        "application_repair_policy": {
            "maximum_repair_attempts": 1,
            "trigger": "transient transport failure or invalid structured/semantic output only",
            "transport_failures_retried": True,
        },
        "development_record_count": 15,
        "labels_passed_to_model": False,
        "manual_output_edits_allowed": False,
        "artifacts": artifacts,
    }
    temporary = OUTPUT.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"output": str(OUTPUT), "sha256": sha256(OUTPUT), "artifacts": len(artifacts)}))


if __name__ == "__main__":
    main()
