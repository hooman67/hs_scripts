"""Reproduce the sole r2 change: evidence envelopes, unchanged V3 ensemble policy."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R1 = ROOT.parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    if (ROOT / "protocol_freeze.json").exists():
        raise RuntimeError("The single r2 revision is frozen; no rebuilding/tuning")
    source = (R1 / "run_judge.py").read_text()
    generated = source.replace(
        'V3 = ROOT.parent / "v3"', 'V3 = ROOT.parent.parent / "v3"').replace(
        'ROOT / "scoring.py"', 'ROOT.parent / "scoring.py"').replace(
        '"placement-judge-v3.1-consensus-v1"', '"placement-judge-v3.1-r2-consensus-v1"').replace(
        "from jsonschema import Draft202012Validator",
        "from jsonschema import Draft202012Validator\n\nimport trace_contract as TRACE")
    before, remainder = generated.split("def call_stage(", 1)
    stage, after = remainder.split("\ndef trigger_names(", 1)
    stage = stage.replace(
        'schema = component_schema(names) if names else SCORING.OBSERVATION_SCHEMA',
        'base_schema = component_schema(names) if names else SCORING.OBSERVATION_SCHEMA\n'
        '    schema = TRACE.envelope_schema(base_schema)')
    stage = stage.replace(
        'value = json.loads(raw["choices"][0]["message"]["content"])',
        'evidence_envelope = json.loads(raw["choices"][0]["message"]["content"])\n'
        '        value = TRACE.validate(evidence_envelope, base_schema)')
    stage = stage.replace('validate_components(value, schema)', 'validate_components(value, base_schema)')
    stage = stage.replace(
        'if value != old["observation"]:',
        'if value != old["observation"] or evidence_envelope != old.get("evidence_envelope"):')
    stage = stage.replace(
        'observation = json.loads(choice.message.content)',
        'evidence_envelope = json.loads(choice.message.content)\n'
        '        observation = TRACE.validate(evidence_envelope, base_schema)')
    stage = stage.replace(
        'validate_components(observation, schema)', 'validate_components(observation, base_schema)')
    stage = stage.replace(
        'result.update(ok=True, model_returned=response.model, observation=observation,',
        'result.update(ok=True, model_returned=response.model, observation=observation,\n'
        '                      evidence_envelope=evidence_envelope,')
    stage = stage.replace(
        '"target_comments_or_expectations_passed": False,',
        '"target_comments_or_expectations_passed": False,\n'
        '        "observation_payload_schema_sha256": json_sha(base_schema),\n'
        '        "evidence_envelope_version": TRACE.VERSION,')
    generated = before + "def call_stage(" + stage + "\ndef trigger_names(" + after
    (ROOT / "run_judge.py").write_text(generated)
    (ROOT / "prompts").mkdir(exist_ok=True)
    intro = (ROOT / "trace_instruction.md").read_text()
    for name in ("baseline", "compact", "proposal", "independent"):
        (ROOT / "prompts" / f"{name}.md").write_text(
            intro + (R1 / "prompts" / f"{name}.md").read_text())
    (ROOT / "visual_anchors.json").write_bytes((R1 / "visual_anchors.json").read_bytes())
    original_freeze = json.loads((R1 / "protocol_freeze.json").read_text())
    paths = {Path(row["path"]) for row in original_freeze["files"]}
    paths.update(ROOT / name for name in (
        "run_judge.py", "trace_contract.py", "trace_instruction.md", "build_version.py",
        "visual_anchors.json", "calibration_manifest.json", "astra/input.md",
        "astra/config.json", "astra/response.json", "astra/output.md", "astra/metadata.json"))
    paths.update((ROOT / "prompts").glob("*.md"))
    paths.add(R1 / "protocol_freeze.json")
    freeze = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_version": "placement-judge-v3.1-r2-consensus-v1",
        "revision_count": 1, "semantic_change": "Mandatory evidence-first structured trace in existing calls.",
        "unchanged": ["model/settings", "five observation components/schema", "scoring",
                      "primary/verifier count and roles", "trigger/consensus/fallback rules"],
        "r1_runtime_sha256": sha(R1 / "run_judge.py"),
        "astra_model": "gpt-6-astra", "astra_output_sha256": sha(ROOT / "astra/output.md"),
        "files": [{"path": str(path.resolve()), "sha256": sha(path)}
                  for path in sorted(paths)],
    }
    (ROOT / "protocol_freeze.json").write_text(json.dumps(freeze, indent=2) + "\n")
    print(json.dumps({"frozen_dependencies": len(paths), "protocol_freeze_sha256": sha(ROOT / "protocol_freeze.json")}))


if __name__ == "__main__":
    main()
