"""Offline parity audit against the frozen research runner; no provider calls."""

import hashlib
import importlib.util
import json
from pathlib import Path

from services.firefly.foundry.standalone_apps.hp_image.prompt_rewrite.placement_judge.v3_2_r2 import run_judge as portable

RESEARCH = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/placement/versions")
ARTIFACTS = Path("/home/colligo/.copilot/session-state/af64bb86-fb62-4539-b910-640d76a93c88/files/astra_integration")
ARTIFACTS.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location("frozen_r2_common", RESEARCH / "v3_2_r2/common.py")
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)
original.verify_freeze()
cache = ARTIFACTS / "anchors"
cache.mkdir(exist_ok=True)
source_anchors = json.loads((RESEARCH / "v3_1/visual_anchors.json").read_text())["examples"]
package_anchors = json.loads((portable.legacy.ROOT / "visual_anchors.json").read_text())["examples"]
assert len(source_anchors) == len(package_anchors) == 7
for source, target in zip(source_anchors, package_anchors, strict=True):
    for key in ("asset_id", "guidance", "sha256"):
        assert source[key] == target[key]
    assert portable.sha(source["local_path"]) == target["sha256"]
    link = cache / target["filename"]
    if not link.exists():
        link.symlink_to(source["local_path"])
    assert portable.sha(link) == target["sha256"]

case = RESEARCH / "v3_2_r2/evaluation/refiner/p1/01_cashmere_x_Front_CloseUp__run1--baseline"
inputs = portable.validate_input(json.loads((case / "input.json").read_text()))
message_hashes = {}
for stage in ("baseline", "compact", "proposal", "independent"):
    reports = None
    if stage in ("proposal", "independent"):
        reports = {"requested_components": ["scale_perspective"]}
        if stage == "proposal":
            component = json.loads((case / "compact/result.json").read_text())["observation"]["components"]
            reports["proposals"] = {"scale_perspective": component["scale_perspective"]}
    captured = []

    def recording_completion(messages, schema, cap, output, client=None):
        captured.append((messages, schema, cap))
        if reports:
            value = {
                "schema_version": "placement-verifier-components-v1",
                "components": {
                    "scale_perspective": json.loads((case / "baseline/result.json").read_text())["observation"]["components"]["scale_perspective"]
                },
            }
        else:
            value = json.loads((case / "baseline/result.json").read_text())["observation"]
        return value, {}

    original.model_completion = recording_completion
    schema = portable.legacy.component_schema(["scale_perspective"]) if reports else portable.legacy.SCORING.OBSERVATION_SCHEMA
    original.call_stage(
        inputs, "p1_" + stage, ARTIFACTS / ("original_" + stage),
        schema, lambda value: None, reports=reports,
        cap=6000 if reports else 12000,
    )
    assert len(captured) == 1
    actual = portable.build_messages(inputs, stage, anchor_dir=cache, reports=reports)
    assert actual == captured[0][0], stage
    assert portable.legacy.wire_schema(schema) == original.LEGACY.wire_schema(captured[0][1])
    message_hashes[stage] = hashlib.sha256(json.dumps(actual, sort_keys=True).encode()).hexdigest()

counts = {}
for dataset in ("calibration", "historical", "refiner"):
    count = 0
    for result_path in sorted((RESEARCH / f"v3_2_r2/evaluation/{dataset}/p1").glob("*/result.json")):
        saved = json.loads(result_path.read_text())
        parent = result_path.parent
        stages = {name: json.loads((parent / name / "result.json").read_text())["observation"] for name in saved["stages"]}
        args = [stages["baseline"], stages["compact"], stages.get("proposal"), stages.get("independent")]
        old, new = original.LEGACY.aggregate_stages(*args), portable.legacy.aggregate_stages(*args)
        assert old == new
        assert all(saved[key] == value for key, value in new.items()), str(result_path)
        count += 1
    counts[dataset] = count
assert sum(counts.values()) == 209
receipt = {
    "source_freeze_sha256": original.verify_freeze(),
    "portable_freeze_sha256": portable.verify_freeze(),
    "exact_message_sha256_by_stage": message_hashes,
    "aggregate_parity_cases": counts,
    "exact_anchor_guidance_and_pixels": 7,
    "provider_calls": 0,
    "smoke_input": inputs,
    "anchor_cache": str(cache),
}
(ARTIFACTS / "parity_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({key: value for key, value in receipt.items() if key not in ("smoke_input",)}, indent=2))
