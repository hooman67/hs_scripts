"""V3.1 ensemble: V3 decision rules, revised rubrics, immutable model evidence."""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import importlib.metadata
import importlib.util
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

import trace_contract as TRACE

ROOT = Path(__file__).resolve().parent
V3 = ROOT.parent.parent / "v3"
INPUT_KEYS = {"generated_image", "twin_image", "product_type", "scene_prompt", "image_stage"}
MODEL = "gpt-5.5"
PROTOCOL_VERSION = "placement-judge-v3.1-r2-consensus-v1"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCORING = load("v31_scoring", ROOT.parent / "scoring.py") if (ROOT.parent / "scoring.py").exists() else None
COMBINE = load("v31_v3_combine", V3 / "experiments/two_pass/combine.py")
CONSENSUS = load("v31_v3_consensus", V3 / "experiments/consensus_policy/merge_consensus_v2.py")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def verify_freeze():
    frozen = json.loads((ROOT / "protocol_freeze.json").read_text())
    for item in frozen["files"]:
        if sha(item["path"]) != item["sha256"]:
            raise RuntimeError(f"Frozen protocol dependency changed: {item['path']}")
    return sha(ROOT / "protocol_freeze.json")


def wire_schema(value):
    if isinstance(value, dict):
        return {k: wire_schema(v) for k, v in value.items()
                if k not in {"$schema", "uniqueItems", "minLength"}}
    if isinstance(value, list):
        return [wire_schema(v) for v in value]
    return value


def component_schema(names):
    if not names or len(set(names)) != len(names) or set(names) - set(SCORING.COMPONENT_WEIGHTS):
        raise ValueError("Invalid verifier component names")
    return {
        "type": "object", "additionalProperties": False,
        "required": ["schema_version", "components"],
        "properties": {
            "schema_version": {"type": "string", "const": "placement-verifier-components-v1"},
            "components": {"type": "object", "additionalProperties": False,
                           "required": names,
                           "properties": {n: copy.deepcopy(SCORING.OBSERVATION_SCHEMA["$defs"][n])
                                          for n in names}},
        },
    }


def validate_components(value, schema):
    Draft202012Validator(schema).validate(value)
    # Apply the same semantic checks as primary observations, not just JSON shape.
    errors = SCORING._semantic_observation_errors({
        "components": {
            name: value["components"].get(name, {
                "visibility": "unobservable", "severity": None, "confidence": "low",
                "issue_codes": [], "evidence": "Not requested", "consequence": "",
            }) for name in SCORING.COMPONENT_WEIGHTS
        },
    })
    if errors:
        raise ValueError("; ".join(errors))
    reject_retired_code(value["components"])


def reject_retired_code(components):
    if any("chair_alignment_conflict" in c["issue_codes"] for c in components.values()):
        raise ValueError("V3.1 must not newly emit historical chair_alignment_conflict")


def validate_new_observation(value):
    SCORING.validate_observation(value)
    reject_retired_code(value["components"])


def select_anchors(runtime_input):
    manifest = json.loads((ROOT / "visual_anchors.json").read_text())
    targets = {sha(runtime_input[k]) for k in ("generated_image", "twin_image")}
    selected, excluded = [], []
    for anchor in manifest["examples"]:
        if sha(anchor["local_path"]) != anchor["sha256"]:
            raise ValueError("Frozen V2 exemplar bytes changed")
        if anchor["sha256"] in targets:
            excluded.append(anchor["asset_id"])
        else:
            selected.append(anchor)
    if not selected:
        raise ValueError("All baseline exemplars excluded")
    return selected, excluded


def image_parts(label, path):
    path = Path(path)
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in {"image/png", "image/jpeg", "image/webp"}:
        raise ValueError("Unsupported image format")
    return [
        {"type": "text", "text": label},
        {"type": "image_url", "image_url": {
            "url": f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode(),
            "detail": "high"}},
    ]


def identity_matches(model):
    import re
    return isinstance(model, str) and re.fullmatch(r"gpt-5\.5(?:-\d{4}-\d{2}-\d{2})?", model) is not None


def call_stage(runtime_input, stage, output, client, names=None, proposals=None):
    output.mkdir(parents=True, exist_ok=True)
    prompt = (ROOT / "prompts" / f"{stage}.md").read_text()
    base_schema = component_schema(names) if names else SCORING.OBSERVATION_SCHEMA
    schema = TRACE.envelope_schema(base_schema)
    images = {k: {"path": runtime_input[k], "sha256": sha(runtime_input[k])}
              for k in ("generated_image", "twin_image")}
    anchors, excluded = select_anchors(runtime_input) if stage == "baseline" else ([], [])
    request = {
        "protocol_version": PROTOCOL_VERSION, "stage": stage,
        "runtime_input": runtime_input, "images": images,
        "model_requested": MODEL, "reasoning_effort": "high",
        "max_completion_tokens": 12000 if names is None else 6000,
        "route": "foundry_aws_gateway.llm.get_azure_openai",
        "timeout_seconds": 180, "transport_max_retries": 2,
        "semantic_retries": 0, "image_detail": "high",
        "image_transform": "none; exact original bytes",
        "system_prompt_sha256": sha(ROOT / "prompts" / f"{stage}.md"),
        "schema_sha256": json_sha(schema), "protocol_freeze_sha256": verify_freeze(),
        "requested_components": names, "proposals": proposals,
        "visual_anchors": anchors, "excluded_target_identical_anchor_ids": excluded,
        "target_comments_or_expectations_passed": False,
        "observation_payload_schema_sha256": json_sha(base_schema),
        "evidence_envelope_version": TRACE.VERSION,
    }
    fingerprint = json_sha(request)
    result_path = output / "result.json"
    if result_path.exists():
        old = json.loads(result_path.read_text())
        if old.get("fingerprint") != fingerprint or not old.get("ok"):
            raise RuntimeError("Stage exists for failed/different input; preserve it and use a new run")
        raw = json.loads((output / "response.json").read_text())
        if not identity_matches(raw.get("model")) or raw["choices"][0]["finish_reason"] != "stop":
            raise RuntimeError("Cached raw model identity/completion mismatch")
        evidence_envelope = json.loads(raw["choices"][0]["message"]["content"])
        value = TRACE.validate(evidence_envelope, base_schema)
        if names:
            validate_components(value, base_schema)
        else:
            validate_new_observation(value)
        if value != old["observation"] or evidence_envelope != old.get("evidence_envelope"):
            raise RuntimeError("Cached raw response differs from saved observation")
        return old
    write_json(output / "request.json", {**request, "fingerprint": fingerprint})
    (output / "system_prompt.md").write_text(prompt)
    write_json(output / "schema.json", schema)
    messages = [{"role": "system", "content": prompt}]
    if anchors:
        parts = [{"type": "text", "text": "Fixed DEVELOPMENT rubric exemplars; assess target independently. V3.1 chair-relaxation rules override historical chair-pose interpretations."}]
        for anchor in anchors:
            parts += image_parts(anchor["guidance"], anchor["local_path"])
        messages.extend([
            {"role": "user", "content": parts},
            {"role": "assistant", "content": "I will apply the V3.1 standards independently to the target."},
        ])
    payload = {k: runtime_input[k] for k in ("product_type", "scene_prompt", "image_stage")}
    if names:
        payload["requested_components"] = names
    if proposals is not None:
        payload["fallible_model_proposals"] = proposals
    parts = [{"type": "text", "text": json.dumps(payload)}]
    for label, key in (("A: generated image to assess", "generated_image"),
                       ("B: original product reference", "twin_image")):
        parts += image_parts(label, runtime_input[key])
    messages.append({"role": "user", "content": parts})
    result = {"fingerprint": fingerprint, "started_utc": datetime.now(timezone.utc).isoformat()}
    try:
        response = client.chat.completions.create(
            model=MODEL, reasoning_effort="high",
            max_completion_tokens=request["max_completion_tokens"], messages=messages,
            response_format={"type": "json_schema", "json_schema": {
                "name": "placement_observation", "strict": True, "schema": wire_schema(schema)}},
        )
        (output / "response.json").write_text(response.model_dump_json(indent=2))
        choice = response.choices[0]
        if not identity_matches(response.model) or choice.finish_reason != "stop" or choice.message.refusal:
            raise RuntimeError("Unexpected model, incomplete or refused response")
        evidence_envelope = json.loads(choice.message.content)
        observation = TRACE.validate(evidence_envelope, base_schema)
        if names:
            validate_components(observation, base_schema)
        else:
            validate_new_observation(observation)
        result.update(ok=True, model_returned=response.model, observation=observation,
                      evidence_envelope=evidence_envelope,
                      usage=response.usage.model_dump() if response.usage else None)
    except Exception as exc:
        result.update(ok=False, error_type=type(exc).__name__,
                      status_code=getattr(exc, "status_code", None))
    result["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_json(result_path, result)
    if not result["ok"]:
        raise RuntimeError(f"{stage} failed; preserved {result_path}")
    return result


def trigger_names(baseline, compact):
    return [name for name, component in compact["components"].items()
            if CONSENSUS.confidently_material(component)
            and (not (baseline["components"][name]["visibility"] in {"observed", "partial"}
                      and baseline["components"][name]["confidence"] in {"medium", "high"}
                      and isinstance(baseline["components"][name]["severity"], int))
                 or component["severity"] > baseline["components"][name]["severity"])]


def aggregate_stages(baseline, compact, proposal=None, independent=None):
    validate_new_observation(baseline)
    validate_new_observation(compact)
    names = trigger_names(baseline, compact)
    if names and (proposal is None or independent is None):
        raise ValueError("Triggered additions require both independent checks")
    if names:
        schema = component_schema(names)
        validate_components(proposal, schema)
        validate_components(independent, schema)
    elif proposal is not None or independent is not None:
        raise ValueError("Unexpected verifier results without triggers")
    corrected = copy.deepcopy(compact)
    resolutions = {}
    for name in names:
        selected, resolution = CONSENSUS.resolve_component(
            name, proposal["components"][name], independent["components"][name],
            baseline["components"][name])
        corrected["components"][name] = selected
        resolutions[name] = resolution
    base_score = SCORING.aggregate_observation(baseline)
    compact_score = SCORING.aggregate_observation(corrected)
    observation, provenance = COMBINE.merge_observations(
        baseline, corrected, baseline_verdict=base_score["verdict"],
        compact_verdict=compact_score["verdict"])
    observation["schema_version"] = SCORING.SCHEMA_VERSION
    merged = SCORING.aggregate_observation(observation)
    decision = CONSENSUS.final_policy(base_score["verdict"], merged, resolutions)
    return {
        "application_merged_judgment": merged, "final_decision": decision,
        "consensus_resolution": resolutions, "component_provenance": provenance,
        "triggered_components": names,
    }


def judge(runtime_input, output, client=None):
    if set(runtime_input) != INPUT_KEYS:
        raise ValueError("Only the canonical five runtime input fields are permitted")
    SCORING.validate_runtime_input(runtime_input)
    freeze = verify_freeze()
    if client is None:
        import foundry_aws_gateway.llm
        client = foundry_aws_gateway.llm.get_azure_openai().with_options(max_retries=2, timeout=180)
    output = Path(output)
    primary = {stage: call_stage(runtime_input, stage, output / stage, client)
               for stage in ("baseline", "compact")}
    baseline, compact = (primary[s]["observation"] for s in ("baseline", "compact"))
    names = trigger_names(baseline, compact)
    checks = {}
    if names:
        for stage in ("proposal", "independent"):
            checks[stage] = call_stage(
                runtime_input, stage, output / stage, client, names=names,
                proposals={n: compact["components"][n] for n in names} if stage == "proposal" else None)
    merged = aggregate_stages(
        baseline, compact, checks.get("proposal", {}).get("observation"),
        checks.get("independent", {}).get("observation"))
    envelope = {
        "protocol_version": PROTOCOL_VERSION, "ok": True, "runtime_input": runtime_input,
        "protocol_freeze_sha256": freeze,
        "stages": {s: {"path": str((output / s / "result.json").resolve()),
                       "sha256": sha(output / s / "result.json")}
                   for s in [*primary, *checks]},
        **merged,
    }
    result_path = output / "result.json"
    if result_path.exists() and json.loads(result_path.read_text()) != envelope:
        raise RuntimeError("Existing ensemble differs from reproducible recomputation")
    write_json(result_path, envelope)
    return envelope


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = judge(json.loads(args.input.read_text()), args.output)
    print(json.dumps({"verdict": result["final_decision"]["verdict"],
                      "score": result["application_merged_judgment"]["natural_placement_score"]}))


if __name__ == "__main__":
    main()
