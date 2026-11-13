"""Fresh V3 calls using frozen original runners and unchanged consensus functions.

Only authentication and output-specific freeze plumbing are adapted in memory.
No historical prediction is reused and no frozen source file is modified.
"""
from __future__ import annotations

import copy
import importlib
import json
import sys
import threading
import types
from pathlib import Path

import run_judge as updated

ROOT = Path(__file__).resolve().parent
V3 = ROOT.parent / "v3"
V2 = ROOT.parent / "v2"
LOCAL = threading.local()


def original_package(name, root):
    package = types.ModuleType(name)
    package.__path__ = [str(root)]
    sys.modules[name] = package
    return importlib.import_module(name + ".run_judge")


BASELINE = original_package("v31_frozen_v2", V2)
COMPACT = original_package("v31_frozen_v3", V3)
V2_SCORING = importlib.import_module("v31_frozen_v2.scoring")
PROPOSAL = updated.load("v31_frozen_proposal", V3 / "experiments/verify_additions/run_verifier.py")
INDEPENDENT = updated.load(
    "v31_frozen_independent", V3 / "experiments/independent_component_check/run_check.py")


def auth():
    if not hasattr(LOCAL, "client"):
        import foundry_aws_gateway.llm
        LOCAL.client = foundry_aws_gateway.llm.get_azure_openai().with_options(
            max_retries=0, timeout=180)
    return LOCAL.client, "documented_policy_aware_foundry_gateway_azure_sdk"


def adapter_freeze():
    updated.verify_freeze()
    return json.loads((ROOT / "protocol_freeze.json").read_text())


BASELINE.client = COMPACT.client = auth
for module in (PROPOSAL, INDEPENDENT):
    module.CANONICAL.client = auth
    module.FREEZE_PATH = ROOT / "protocol_freeze.json"
    module.ensure_frozen = adapter_freeze


def aggregate(baseline, compact, proposal=None, independent=None):
    V2_SCORING.validate_observation(baseline)
    updated.SCORING.validate_observation(compact)
    names = updated.trigger_names(baseline, compact)
    if names and (proposal is None or independent is None):
        raise ValueError("Frozen V3 requires both checks for triggered additions")
    corrected = copy.deepcopy(compact)
    resolutions = {}
    for name in names:
        selected, resolution = updated.CONSENSUS.resolve_component(
            name, proposal["components"][name], independent["components"][name],
            baseline["components"][name])
        corrected["components"][name] = selected
        resolutions[name] = resolution
    baseline_score = V2_SCORING.aggregate_observation(baseline)
    compact_score = updated.SCORING.aggregate_observation(corrected)
    observation, provenance = updated.COMBINE.merge_observations(
        baseline, corrected, baseline_verdict=baseline_score["verdict"],
        compact_verdict=compact_score["verdict"])
    merged = updated.SCORING.aggregate_observation(observation)
    return {
        "application_merged_judgment": merged,
        "final_decision": updated.CONSENSUS.final_policy(baseline_score["verdict"], merged, resolutions),
        "consensus_resolution": resolutions, "component_provenance": provenance,
        "triggered_components": names,
    }


def judge(runtime_input, output):
    updated.verify_freeze()
    output = Path(output)
    primary = {
        "baseline": BASELINE.judge(runtime_input, output / "baseline", visual_anchors=True),
        "compact": COMPACT.judge(runtime_input, output / "compact", visual_anchors=False),
    }
    if not all(r["ok"] for r in primary.values()):
        raise RuntimeError("Frozen V3 primary failure; raw result preserved")
    baseline, compact = (primary[s]["judgment"]["observation"] for s in ("baseline", "compact"))
    names = updated.trigger_names(baseline, compact)
    checks = {}
    if names:
        images = {key: {"path": runtime_input[key], "sha256": updated.sha(runtime_input[key])}
                  for key in ("generated_image", "twin_image")}
        trigger = {
            "id": output.name, "runtime_input": runtime_input, "images": images,
            "proposed_components": {name: compact["components"][name] for name in names},
            "source_provenance": {
                stage: {"path": str(output / stage / "result.json"),
                        "sha256": updated.sha(output / stage / "result.json")}
                for stage in primary},
        }
        trigger_path = output / "trigger.json"
        updated.write_json(trigger_path, trigger)
        checks["proposal"] = PROPOSAL.verify(trigger, output / "proposal")
        independent_record = {
            "id": output.name, "runtime_input": runtime_input, "images": images,
            "requested_component_names": names, "cohort": "fresh_historical_html_comparison",
            "evaluation_status": "out_of_domain_development_diagnostic",
            "source_trigger": {"path": str(trigger_path), "sha256": updated.sha(trigger_path)},
        }
        checks["independent"] = INDEPENDENT.run(independent_record, output / "independent")
        if not all(r["ok"] for r in checks.values()):
            raise RuntimeError("Frozen V3 verification failed; preserve original responses")
        for stage in checks:
            raw = json.loads((output / stage / "response.json").read_text())
            if not updated.identity_matches(raw.get("model")) or raw["choices"][0]["finish_reason"] != "stop":
                raise RuntimeError("Frozen V3 verifier returned incomplete/unexpected model")
    merged = aggregate(baseline, compact, checks.get("proposal", {}).get("assessment"),
                       checks.get("independent", {}).get("assessment"))
    result = {
        "protocol_version": "frozen-v3-consensus-fresh-evaluation-adapter-v1",
        "ok": True, "runtime_input": runtime_input,
        "protocol_freeze_sha256": updated.verify_freeze(),
        "adapter_changes": "Only policy-aware auth and local freeze/output plumbing; original prompts, schemas, model settings and decision functions.",
        "stages": {s: {"path": str((output / s / "result.json").resolve()),
                       "sha256": updated.sha(output / s / "result.json")} for s in [*primary, *checks]},
        **merged,
    }
    updated.write_json(output / "result.json", result)
    return result
