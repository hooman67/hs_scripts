#!/usr/bin/env python3
"""Freeze V4.2 code, schemas, calibration assets, and first-gate protocol."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    paths = [
        "README.md", "system_prompt.md", "assessment_schema.json", "result_schema.json",
        "build_schema.py", "build_wire_schema.py", "wire_schema.json", "scoring.py", "crop.py", "build_anchor_catalog.py",
        "anchor_selection.py", "anchors/anchor_catalog.json", "run_judge.py", "build_gate.py",
        "preflight_gate.py", "run_batch.py", "run_gate_tmux.sh", "evaluate_gate.py",
        "data/gate_6_manifest.json", "data/gate_6_expectations_withheld.json",
        "data/gate_6_preflight.json", "test_v4_2.py",
    ]
    assets = sorted((ROOT / "anchors" / "assets").glob("*"))
    freeze = {
        "schema_version": "hp-placement-v4.2-protocol-freeze-v3",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "frozen_before_first_model_call",
        "model": {"requested": "gpt-6-astra", "route": "foundry_direct_openai", "reasoning_effort": "high", "max_completion_tokens": 24000, "sdk_retries": 0, "application_total_attempts_max": 2, "timeout_seconds": 600, "concurrency": 1},
        "runtime_environment": {"python": "3.12", "foundry_aws_gateway": ">=2.0.0", "jsonschema": "4.25.1", "pillow": "12.0.0", "opencv_python_headless": "4.10.0.84"},
        "runtime_contract": {"required": ["generated_image", "twin_image", "product_type", "scene_prompt"], "optional_audit_only": ["target_record_id", "device", "camera", "prompt_rank"]},
        "anchor_exclusions": ["exact_generated_byte_or_pixel_hash", "same_twin_byte_or_pixel_hash", "exact_prompt_hash", "optional_same_product_camera_rank_family", "optional_same_device_camera_rank_family"],
        "gate": {"count": 6, "labels_or_comments_passed_to_judge": False, "union_exclusions_across_all_gate_targets": True},
        "files": {path: sha(ROOT / path) for path in paths},
        "anchor_assets": {str(path.relative_to(ROOT)): sha(path) for path in assets},
    }
    out = ROOT / "data" / "protocol_freeze_gate_6_v3.json"
    out.write_text(json.dumps(freeze, indent=2) + "\n")
    print(out, sha(out))


if __name__ == "__main__":
    main()
