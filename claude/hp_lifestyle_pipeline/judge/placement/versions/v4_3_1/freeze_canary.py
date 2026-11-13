#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
V43 = ROOT.parent / "v4_3"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


paths = [
    "PROVENANCE.md",
    "system_prompt.md",
    "build_schema.py",
    "assessment_schema.json",
    "build_wire_schema.py",
    "wire_schema.json",
    "result_schema.json",
    "scoring.py",
    "crop.py",
    "anchor_selection.py",
    "anchors/anchor_catalog.json",
    "run_judge.py",
    "preflight_gate.py",
    "data/gate_6_preflight.json",
    "data/canary_input.json",
    "data/canary_manifest.json",
    "test_v4_3_1.py",
    "run_canary_tmux.sh",
]

source_artifacts = [
    V43 / "data/protocol_freeze_canary_v1.json",
    V43 / "runs/canary-v1-gpt55/result/result.json",
    V43 / "runs/canary-v1-gpt55/result/attempt_1_response.txt",
]

doc = {
    "schema_version": "hp-placement-v4.3.1-quality-canary-freeze-v1",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "frozen_before_quality_canary",
    "purpose": "same-case GPT-5.5 quality and transport gate for visible laptop chair displacement",
    "quality_requirement": {
        "target_record_id": "elitebook__laptop_FrontLeftMedium__p1",
        "required_verdict": "review",
        "required_owned_issue_code": "chair_displacement",
        "required_severity": 1,
        "required_warning_level": "review",
        "prohibited_reasoning": "do not invent a second centered off-frame chair when the visible chair is the only plausible associated user position",
    },
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
    "runtime": {
        "python": "3.12",
        "foundry_aws_gateway": ">=2.0.0",
        "jsonschema": "4.25.1",
        "pillow": "12.0.0",
        "opencv": "4.10.0.84",
    },
    "files": {path: sha(ROOT / path) for path in paths},
    "anchor_assets": {
        str(path.relative_to(ROOT)): sha(path)
        for path in sorted((ROOT / "anchors/assets").glob("*"))
    },
    "source_v4_3_artifacts": {
        str(path): sha(path) for path in source_artifacts
    },
}

output = ROOT / "data/protocol_freeze_quality_canary_v1.json"
output.write_text(json.dumps(doc, indent=2) + "\n")
print(output, sha(output))
