#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


files = [
    "PROVENANCE.md",
    "system_prompt.md",
    "assessment_schema.json",
    "wire_schema.json",
    "result_schema.json",
    "scoring.py",
    "crop.py",
    "anchor_selection.py",
    "anchors/anchor_catalog.json",
    "run_judge.py",
    "run_remaining_five.py",
    "run_remaining_five_tmux.sh",
    "evaluate_combined_gate.py",
    "preflight_gate.py",
    "data/gate_6_manifest.json",
    "data/gate_6_expectations_withheld.json",
    "data/gate_6_preflight.json",
    "data/protocol_freeze_quality_canary_v1.json",
    "test_v4_3_1.py",
]

canary_result = ROOT / "runs/quality-canary-v1-gpt55/result/result.json"
canary_response = ROOT / "runs/quality-canary-v1-gpt55/result/attempt_1_response.txt"
manifest = json.loads((ROOT / "data/gate_6_manifest.json").read_text())
canary_id = "elitebook__laptop_FrontLeftMedium__p1"
remaining_ids = [row["record_id"] for row in manifest["records"] if row["record_id"] != canary_id]

doc = {
    "schema_version": "hp-placement-v4.3.1-remaining-five-freeze-v1",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "frozen_before_remaining_five_gate",
    "model": {
        "requested": "gpt-5.5",
        "route": "foundry_direct_openai",
        "reasoning_effort": "high",
        "max_completion_tokens": 24000,
        "sdk_retries": 0,
        "application_total_attempts_max": 2,
        "timeout_seconds": 600,
        "concurrency": 1,
    },
    "canary": {
        "record_id": canary_id,
        "result_path": str(canary_result),
        "result_sha256": sha(canary_result),
        "raw_response_sha256": sha(canary_response),
        "derived_sha256": json.loads(canary_result.read_text())["audit"]["derived_sha256"],
        "verdict": json.loads(canary_result.read_text())["derived"]["verdict"],
        "owned_issue_codes": json.loads(canary_result.read_text())["derived"]["owned_issue_codes"],
    },
    "remaining_record_ids": remaining_ids,
    "anchor_exclusion_record_ids": [row["record_id"] for row in manifest["records"]],
    "expectations_policy": "withheld file is frozen for post-run evaluation and is never passed to the judge",
    "files": {path: sha(ROOT / path) for path in files},
    "anchor_assets": {
        str(path.relative_to(ROOT)): sha(path)
        for path in sorted((ROOT / "anchors/assets").glob("*"))
    },
}

output = ROOT / "data/protocol_freeze_remaining_five_v1.json"
output.write_text(json.dumps(doc, indent=2) + "\n")
print(output, sha(output))
