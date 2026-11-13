# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema"]
# ///
"""Deterministically merge frozen V2 and compact V3 placement judgments."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parent
V3_ROOT = ROOT.parents[1]
V2_ROOT = V3_ROOT.parent / "v2"
POLICY_PATH = ROOT / "policy.json"
RUNS_ROOT = ROOT / "runs"
POLICY = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
POLICY_VERSION = POLICY["policy_version"]
SCHEMA_VERSION = "placement-two-pass-result-v1"
INPUT_KEYS = frozenset(
    {"generated_image", "twin_image", "product_type", "scene_prompt", "image_stage"}
)
SOURCE_LABEL_KEYS = frozenset(
    {"human_feedback", "diagnostic_expectation", "extended_validation_expectation"}
)
RUN_NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*$")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCORING = load_module("placement_two_pass_v3_scoring", V3_ROOT / "scoring.py")


def sha256_path(path: Path | str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    os.replace(temporary, path)


def validate_run_name(value: str) -> str:
    if len(value) > 64 or not RUN_NAME_RE.fullmatch(value):
        raise argparse.ArgumentTypeError("run name must be a path-safe lowercase identifier")
    return value


def manifest_records(payload: Any) -> list[Mapping[str, Any]]:
    if not isinstance(payload, Mapping) or not isinstance(payload.get("records"), list):
        raise ValueError("Manifest must be an object with a records list")
    records = payload["records"]
    expected = payload.get("expected_count")
    if expected is not None and expected != len(records):
        raise ValueError("Manifest expected_count differs from records length")
    if not all(isinstance(record, Mapping) for record in records):
        raise ValueError("Manifest records must be objects")
    return records


def record_identity(record: Mapping[str, Any]) -> dict[str, str]:
    record_id = record.get("id")
    if not isinstance(record_id, str) or not record_id:
        raise ValueError("Record id must be a nonempty string")
    generated = record.get("generated_image")
    twin = record.get("twin_image")
    if not isinstance(generated, Mapping) or not isinstance(twin, Mapping):
        raise ValueError(f"{record_id}: missing image objects")
    scene_prompt = record.get("scene_prompt")
    if not isinstance(scene_prompt, str):
        raise ValueError(f"{record_id}: scene_prompt must be a string")
    prompt_hash = hashlib.sha256(scene_prompt.encode("utf-8")).hexdigest()
    if record.get("scene_prompt_sha256") != prompt_hash:
        raise ValueError(f"{record_id}: scene prompt hash mismatch")
    identity = {
        "generated_image_sha256": generated.get("sha256"),
        "twin_image_sha256": twin.get("sha256"),
        "scene_prompt_sha256": prompt_hash,
        "product_type": record.get("device_type", record.get("product_type")),
        "image_stage": record.get("image_stage"),
    }
    if not all(isinstance(value, str) and value for value in identity.values()):
        raise ValueError(f"{record_id}: incomplete input identity")
    if identity["image_stage"] != "scene_generation":
        raise ValueError(f"{record_id}: only scene_generation is supported")
    identity["input_identity_sha256"] = json_sha256(identity)
    return identity


def _request_identity(request: Mapping[str, Any]) -> dict[str, str]:
    runtime_input = request.get("input")
    images = request.get("images")
    if not isinstance(runtime_input, Mapping) or set(runtime_input) != INPUT_KEYS:
        raise ValueError("Stage request violates the canonical five-field input whitelist")
    if any(key in runtime_input for key in SOURCE_LABEL_KEYS):
        raise ValueError("Source annotations entered a stage runtime input")
    if not isinstance(images, Mapping):
        raise ValueError("Stage request has no image hashes")
    prompt = runtime_input.get("scene_prompt")
    if not isinstance(prompt, str):
        raise ValueError("Stage scene prompt is not a string")
    identity = {
        "generated_image_sha256": images.get("generated_image", {}).get("sha256"),
        "twin_image_sha256": images.get("twin_image", {}).get("sha256"),
        "scene_prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "product_type": runtime_input.get("product_type"),
        "image_stage": runtime_input.get("image_stage"),
    }
    if not all(isinstance(value, str) and value for value in identity.values()):
        raise ValueError("Stage request has an incomplete input identity")
    identity["input_identity_sha256"] = json_sha256(identity)
    return identity


def _verify_actual_image_bytes(request: Mapping[str, Any], cache: dict[str, str]) -> None:
    for key in ("generated_image", "twin_image"):
        image = request["images"][key]
        path = Path(image["path"])
        if not path.is_file():
            raise ValueError(f"Missing stage input image: {path}")
        cache_key = str(path.resolve())
        actual = cache.setdefault(cache_key, sha256_path(path))
        if actual != image["sha256"]:
            raise ValueError(f"Stage input bytes changed: {path}")


def _raw_observation(response: Mapping[str, Any]) -> Any:
    try:
        content = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError("Raw response has no first message content") from error
    if not isinstance(content, str):
        raise ValueError("Raw response message content is not a string")
    return json.loads(content)


def _stage_protocol_fingerprint(request: Mapping[str, Any], role: str) -> dict[str, Any]:
    common = {
        key: request.get(key)
        for key in (
            "protocol_version",
            "fingerprint",
            "runner_sha256",
            "wire_schema_sha256",
            "system_prompt_sha256",
            "schema_sha256",
            "scoring_sha256",
            "model_requested",
            "reasoning_effort",
            "max_completion_tokens",
            "visual_anchors_enabled",
        )
    }
    if role == "baseline_v2":
        common["visual_anchor_manifest_sha256"] = request.get(
            "visual_anchor_manifest_sha256"
        )
        common["excluded_target_identical_anchor_ids"] = request.get(
            "excluded_target_identical_anchor_ids", []
        )
        anchors = request.get("visual_anchors", {}).get("examples", [])
        common["included_visual_anchor_count"] = len(anchors)
    return common


def load_stage(
    run_dirs: Sequence[Path],
    record_id: str,
    identity: Mapping[str, str],
    role: str,
    image_hash_cache: dict[str, str],
) -> dict[str, Any]:
    matches: list[dict[str, Any]] = []
    expected = POLICY["stages"][role]
    for run_dir in run_dirs:
        case_dir = run_dir / record_id
        request_path = case_dir / "request.json"
        result_path = case_dir / "result.json"
        response_path = case_dir / "response.json"
        if not request_path.is_file() or not result_path.is_file() or not response_path.is_file():
            continue
        request = json.loads(request_path.read_text(encoding="utf-8"))
        if _request_identity(request) != identity:
            continue
        result = json.loads(result_path.read_text(encoding="utf-8"))
        response = json.loads(response_path.read_text(encoding="utf-8"))
        if result.get("ok") is not True or result.get("fingerprint") != request.get("fingerprint"):
            raise ValueError(f"{record_id} {role}: failed or mismatched saved result")
        if request.get("protocol_version") != expected["protocol_version"]:
            raise ValueError(f"{record_id} {role}: wrong protocol")
        if request.get("model_requested") != expected["model"]:
            raise ValueError(f"{record_id} {role}: wrong requested model")
        if request.get("reasoning_effort") != expected["reasoning_effort"]:
            raise ValueError(f"{record_id} {role}: wrong reasoning effort")
        if request.get("visual_anchors_enabled") is not expected["visual_anchors"]:
            raise ValueError(f"{record_id} {role}: wrong anchor setting")
        if not re.fullmatch(r"gpt-5\.5(?:-\d{4}-\d{2}-\d{2})?", result.get("model_returned", "")):
            raise ValueError(f"{record_id} {role}: unexpected returned model")
        if role == "baseline_v2":
            if request.get("visual_anchor_manifest_sha256") != sha256_path(
                V2_ROOT / "data/visual_anchors.json"
            ):
                raise ValueError(f"{record_id}: V2 anchor manifest fingerprint changed")
            included = len(request.get("visual_anchors", {}).get("examples", []))
            excluded = len(request.get("excluded_target_identical_anchor_ids", []))
            if included + excluded != expected["frozen_anchor_manifest_expected_count"]:
                raise ValueError(f"{record_id}: V2 did not account for all seven anchors")
        else:
            current_hashes = {
                "runner_sha256": sha256_path(V3_ROOT / "run_judge.py"),
                "system_prompt_sha256": sha256_path(V3_ROOT / "system_prompt.md"),
                "schema_sha256": sha256_path(V3_ROOT / "observation_schema.json"),
                "scoring_sha256": sha256_path(V3_ROOT / "scoring.py"),
            }
            for key, current in current_hashes.items():
                if request.get(key) != current:
                    raise ValueError(f"{record_id}: compact V3 {key} is not current")
        _verify_actual_image_bytes(request, image_hash_cache)
        judgment = result.get("judgment")
        if not isinstance(judgment, Mapping) or _raw_observation(response) != judgment.get("observation"):
            raise ValueError(f"{record_id} {role}: raw response differs from saved judgment")
        matches.append(
            {
                "role": role,
                "case_dir": case_dir,
                "request_path": request_path,
                "result_path": result_path,
                "response_path": response_path,
                "request": request,
                "result": result,
                "response": response,
                "judgment": judgment,
            }
        )
    if len(matches) != 1:
        raise ValueError(
            f"{record_id} {role}: expected one exact-input saved result, found {len(matches)}"
        )
    return matches[0]


def assessable(component: Mapping[str, Any]) -> bool:
    return component.get("visibility") in {"observed", "partial"} and isinstance(
        component.get("severity"), int
    )


def confirmed_positive(component: Mapping[str, Any]) -> bool:
    return (
        assessable(component)
        and component["severity"] > 0
        and component.get("confidence") in {"medium", "high"}
    )


def choose_component(
    baseline: Mapping[str, Any], compact: Mapping[str, Any]
) -> tuple[str, str]:
    candidates = []
    if confirmed_positive(baseline):
        candidates.append((baseline["severity"], 1, "baseline_v2"))
    if confirmed_positive(compact):
        candidates.append((compact["severity"], 0, "compact_v3"))
    if candidates:
        _, _, source = max(candidates)
        return source, "highest_confirmed_positive_severity_tie_baseline"
    if assessable(baseline):
        if baseline.get("severity", 0) >= 2 and baseline.get("confidence") == "low":
            return "baseline_v2", "retained_baseline_low_confidence_material_uncertainty"
        return "baseline_v2", "no_confirmed_positive_baseline_assessable"
    return "compact_v3", "no_confirmed_positive_baseline_unassessable"


def merge_observations(
    baseline: Mapping[str, Any], compact: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    selected_components: dict[str, Any] = {}
    provenance: dict[str, Any] = {}
    for name in SCORING.COMPONENT_WEIGHTS:
        base_component = baseline["components"][name]
        compact_component = compact["components"][name]
        source, reason = choose_component(base_component, compact_component)
        selected_components[name] = dict(
            base_component if source == "baseline_v2" else compact_component
        )
        provenance[name] = {
            "selected_source": source,
            "selection_reason": reason,
            "baseline_v2": base_component,
            "compact_v3": compact_component,
        }
    product_values = {baseline["product_match"], compact["product_match"]}
    product_match = (
        "mismatch"
        if "mismatch" in product_values
        else "uncertain"
        if "uncertain" in product_values
        else "match"
    )
    source_summary = ", ".join(
        f"{name}={value['selected_source']}" for name, value in provenance.items()
    )
    changes: list[str] = []
    for source in (baseline, compact):
        for change in source.get("suggested_scene_changes", []):
            if change not in changes:
                changes.append(change)
    observation = {
        "schema_version": "placement-observations-v3",
        "product_match": product_match,
        "product_match_note": (
            f"baseline_v2={baseline['product_match']}: {baseline['product_match_note']} | "
            f"compact_v3={compact['product_match']}: {compact['product_match_note']}"
        ),
        "scene_reading": dict(compact["scene_reading"]),
        "components": selected_components,
        "summary": "Application-derived deterministic two-pass merge; " + source_summary,
        "suggested_scene_changes": changes,
    }
    SCORING.validate_observation(observation)
    return observation, provenance


def _stage_artifact(stage: Mapping[str, Any]) -> dict[str, Any]:
    request = stage["request"]
    return {
        "source_case_dir": str(stage["case_dir"].resolve()),
        "input_identity": _request_identity(request),
        "protocol_fingerprint": _stage_protocol_fingerprint(request, stage["role"]),
        "artifacts": {
            "request": {
                "path": str(stage["request_path"].resolve()),
                "sha256": sha256_path(stage["request_path"]),
            },
            "raw_response": {
                "path": str(stage["response_path"].resolve()),
                "sha256": sha256_path(stage["response_path"]),
            },
            "result": {
                "path": str(stage["result_path"].resolve()),
                "sha256": sha256_path(stage["result_path"]),
            },
        },
        "judgment": stage["judgment"],
    }


def combine_case(
    record: Mapping[str, Any],
    baseline_runs: Sequence[Path],
    compact_run: Path,
    output_dir: Path,
    image_hash_cache: dict[str, str],
) -> dict[str, Any]:
    record_id = record["id"]
    identity = record_identity(record)
    baseline = load_stage(
        baseline_runs, record_id, identity, "baseline_v2", image_hash_cache
    )
    compact = load_stage(
        [compact_run], record_id, identity, "compact_v3", image_hash_cache
    )
    observation, component_provenance = merge_observations(
        baseline["judgment"]["observation"], compact["judgment"]["observation"]
    )
    judgment = SCORING.aggregate_observation(observation)
    result = {
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "origin": "application_derived_deterministic_merge",
        "record_id": record_id,
        "input_identity": identity,
        "policy_sha256": sha256_path(POLICY_PATH),
        "combiner_sha256": sha256_path(__file__),
        "comment_input_exclusion": {
            "canonical_runtime_input_keys": sorted(INPUT_KEYS),
            "source_annotations_passed_to_either_model": False,
        },
        "component_provenance": component_provenance,
        "stages": {
            "baseline_v2": _stage_artifact(baseline),
            "compact_v3": _stage_artifact(compact),
        },
        "combined_observation": observation,
        "combined_judgment": judgment,
    }
    output_dir.mkdir(parents=True)
    for stage in (baseline, compact):
        destination = output_dir / "raw_responses" / stage["role"] / "response.json"
        destination.parent.mkdir(parents=True)
        shutil.copyfile(stage["response_path"], destination)
        if sha256_path(destination) != sha256_path(stage["response_path"]):
            raise RuntimeError("Raw response copy changed bytes")
    atomic_json(output_dir / "result.json", result)
    return result


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--manifest", type=Path, required=True)
    value.add_argument("--baseline-run", type=Path, action="append", required=True)
    value.add_argument("--compact-run", type=Path, required=True)
    value.add_argument("--run-name", type=validate_run_name, required=True)
    return value


def main() -> int:
    args = parser().parse_args()
    manifest_path = args.manifest.expanduser().resolve()
    baseline_runs = [path.expanduser().resolve() for path in args.baseline_run]
    compact_run = args.compact_run.expanduser().resolve()
    for path in [manifest_path, *baseline_runs, compact_run]:
        if not path.exists():
            raise SystemExit(f"Missing input: {path}")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = manifest_records(payload)
    run_dir = RUNS_ROOT / args.run_name
    if run_dir.exists():
        raise SystemExit(f"Output run already exists: {run_dir}")
    run_dir.mkdir(parents=True)
    image_hash_cache: dict[str, str] = {}
    items = []
    for record in records:
        result = combine_case(
            record,
            baseline_runs,
            compact_run,
            run_dir / record["id"],
            image_hash_cache,
        )
        items.append(
            {
                "id": record["id"],
                "verdict": result["combined_judgment"]["verdict"],
                "score": result["combined_judgment"]["natural_placement_score"],
            }
        )
    summary = {
        "schema_version": "placement-two-pass-run-v1",
        "policy_version": POLICY_VERSION,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest": str(manifest_path),
        "manifest_sha256": sha256_path(manifest_path),
        "baseline_runs": [str(path) for path in baseline_runs],
        "compact_run": str(compact_run),
        "record_count": len(items),
        "items": items,
    }
    atomic_json(run_dir / "summary.json", summary)
    print(json.dumps({"run": str(run_dir), "record_count": len(items)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
