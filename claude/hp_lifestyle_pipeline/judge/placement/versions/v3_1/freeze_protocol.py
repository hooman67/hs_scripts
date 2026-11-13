"""Freeze the actual Astra-reviewed V3.1 and original V3 evaluation dependencies."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
V3 = ROOT.parent / "v3"
V2 = ROOT.parent / "v2"


def main():
    output = ROOT / "protocol_freeze.json"
    if output.exists():
        raise RuntimeError("Freeze exists; do not overwrite a model-call protocol")
    local = [
        "run_judge.py", "scoring.py", "observation_schema.json", "visual_anchors.json",
        "reviewed_rules.json", "build_version.py", "frozen_v3.py", "run_comparison.py",
        "calibrate_anchors.py", "audit_evidence.py", "freeze_protocol.py",
        "implementation_provenance.json", "sources/manifest.json",
        "evaluation/inventory.json", "astra/attempt_1/input.md", "astra/attempt_1/config.json",
        "astra/attempt_1/output.md", "astra/attempt_1/response.json", "astra/attempt_1/metadata.json",
    ]
    paths = [ROOT / p for p in local] + sorted((ROOT / "prompts").glob("*.md"))
    paths += [V2 / p for p in ("scoring.py", "observation_schema.json", "system_prompt.md",
                              "run_judge.py", "data/visual_anchors.json")]
    paths += [V3 / p for p in (
        "scoring.py", "observation_schema.json", "system_prompt.md", "run_judge.py",
        "experiments/two_pass/combine.py", "experiments/two_pass/policy.json",
        "experiments/consensus_policy/merge_consensus_v2.py", "experiments/consensus_policy/policy.json",
        "experiments/verify_additions/run_verifier.py", "experiments/verify_additions/system_prompt.md",
        "experiments/independent_component_check/run_check.py",
        "experiments/independent_component_check/system_prompt.md")]
    for anchor_path in (V2 / "data/visual_anchors.json", ROOT / "visual_anchors.json"):
        paths += [Path(a["local_path"]) for a in json.loads(anchor_path.read_text())["examples"]]
    paths = sorted(set(paths))
    result = {
        "schema_version": "placement-v3.1-frozen-protocol-v1",
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
        "selected_v3_semantics": "V2 exemplars + compact V3 + two-check additions consensus-v2",
        "v3_1_delta": "Astra-reviewed C-Tech laptop/chair tolerance and explicit table/chair geometry; same dimensions, schema registry, scoring and consensus functions.",
        "models": {"consultation": "gpt-6-astra/high", "judge_both_versions": "gpt-5.5/high"},
        "fresh_historical_evaluation_authorized": True,
        "new_generation_evaluation_authorized": False,
        "files": [{"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                   "bytes": p.stat().st_size} for p in paths],
    }
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"freeze": str(output), "file_count": len(paths),
                      "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
