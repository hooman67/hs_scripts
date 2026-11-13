#!/usr/bin/env python3
"""Audit v3 diagnostic runs and evaluate frozen development expectations.

This script never calls a model and never changes predictions. By default it
fails if any of the 20 frozen diagnostic cases is missing. ``--allow-incomplete``
permits a partial artifact for inspecting cases already marked done/cached in
the progress ledger; every present case still receives the full audit.

Expectation matches are development checks against researcher mappings, not
gold-label accuracy. Empty expectation lists are not counted as checks. The
manifest, protocol snapshot, run directory, and output are all CLI-selectable;
the defaults preserve the original 20-case gpt-5.5 diagnostic audit.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import types
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parent
V2_ROOT = ROOT.parent / "v2"
DEFAULT_MANIFEST = ROOT / "data" / "diagnostic_cases.json"
DEFAULT_FREEZE = ROOT / "data" / "protocol_freeze_v1.json"
DEFAULT_RUN_DIR = ROOT / "runs" / "diagnostic_v1"
DEFAULT_OUTPUT = ROOT / "data" / "diagnostic_evaluation_v1.json"
DEFAULT_CORE_ROOT = ROOT
SUCCESS_STATES = {"done", "cached"}
OLD_REGRESSION_IDS = {
    "regression-userfail-row25-v14",
    "regression-userfail-row12-v13",
}
EXPECTED_INPUT_KEYS = {
    "generated_image",
    "twin_image",
    "product_type",
    "scene_prompt",
    "image_stage",
}


class AuditError(RuntimeError):
    """A diagnostic artifact cannot be certified."""


@dataclass(frozen=True)
class CoreRuntime:
    """Functions and constants loaded from one immutable protocol core."""

    root: Path
    flatten_record: Any
    protocol_version: str
    wire_schema_sha256: str
    load_visual_anchors: Any
    model_identity_matches: Any
    select_visual_anchors: Any
    issue_codes: Mapping[str, Any]
    aggregate_observation: Any


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def load_json(path: Path) -> Any:
    require(path.is_file(), f"missing JSON file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuditError(f"invalid JSON file {path}: {exc}") from exc


def file_sha256(path: Path) -> str:
    require(path.is_file(), f"missing file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def json_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
        temporary = Path(handle.name)
    temporary.chmod(0o644)
    os.replace(temporary, path)


def exact_ids(values: Iterable[Any], label: str, expected_count: int) -> list[str]:
    ids = list(values)
    require(len(ids) == expected_count, f"{label} has {len(ids)} IDs; expected {expected_count}")
    require(all(isinstance(value, str) and value for value in ids), f"{label} has invalid IDs")
    require(len(set(ids)) == expected_count, f"{label} contains duplicate IDs")
    return ids


def recursive_contains_text(value: Any, needle: str) -> bool:
    if not needle:
        return False
    if isinstance(value, str):
        return needle in value
    if isinstance(value, Mapping):
        return any(
            recursive_contains_text(key, needle) or recursive_contains_text(child, needle)
            for key, child in value.items()
        )
    if isinstance(value, list):
        return any(recursive_contains_text(child, needle) for child in value)
    return False


def counter_dict(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def load_core_runtime(core_root: Path) -> CoreRuntime:
    require(core_root.is_dir(), f"protocol core root is not a directory: {core_root}")
    required = ("observation_schema.json", "scoring.py", "run_judge.py", "run_batch.py")
    for relative in required:
        require((core_root / relative).is_file(), f"protocol core file missing: {core_root / relative}")

    package_name = f"_placement_diagnostic_core_{text_sha256(str(core_root))[:16]}"
    package = types.ModuleType(package_name)
    package.__path__ = [str(core_root)]  # type: ignore[attr-defined]
    package.__package__ = package_name
    sys.modules[package_name] = package

    modules: dict[str, Any] = {}
    for module_name in ("scoring", "run_judge", "run_batch"):
        qualified_name = f"{package_name}.{module_name}"
        module_path = core_root / f"{module_name}.py"
        spec = importlib.util.spec_from_file_location(qualified_name, module_path)
        require(spec is not None and spec.loader is not None, f"cannot load protocol module: {module_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[qualified_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception as exc:
            raise AuditError(f"cannot import protocol module {module_path}: {exc}") from exc
        modules[module_name] = module

    scoring = modules["scoring"]
    run_judge = modules["run_judge"]
    run_batch = modules["run_batch"]
    return CoreRuntime(
        root=core_root,
        flatten_record=run_batch.flatten_record,
        protocol_version=run_judge.PROTOCOL_VERSION,
        wire_schema_sha256=run_judge.WIRE_SCHEMA_SHA256,
        load_visual_anchors=run_judge._load_visual_anchors,
        model_identity_matches=run_judge._model_identity_matches,
        select_visual_anchors=run_judge._select_visual_anchors,
        issue_codes=scoring.ISSUE_CODES,
        aggregate_observation=scoring.aggregate_observation,
    )


def verify_freeze(
    freeze: Mapping[str, Any],
    *,
    core_root: Path,
    manifest_path: Path,
    manifest_sha256: str,
) -> tuple[dict[str, str], dict[str, str], str]:
    require(
        isinstance(freeze.get("model"), str) and freeze["model"],
        "protocol snapshot model is missing",
    )
    require(freeze.get("reasoning_effort") == "high", "frozen reasoning effort is not high")
    require(
        isinstance(freeze.get("status"), str) and freeze["status"],
        "protocol snapshot status is missing",
    )
    if "visual_anchors" in freeze:
        require(
            isinstance(freeze["visual_anchors"], bool),
            "protocol snapshot visual_anchors must be boolean",
        )
    files = freeze.get("files")
    require(isinstance(files, Mapping) and files, "protocol freeze has no files map")
    verified: dict[str, str] = {}
    verified_paths: dict[str, str] = {}
    manifest_keys = [
        relative
        for relative, expected_hash in files.items()
        if isinstance(relative, str)
        and isinstance(expected_hash, str)
        and Path(relative).name == manifest_path.name
        and expected_hash == manifest_sha256
    ]
    require(
        len(manifest_keys) == 1,
        "selected manifest does not have one exact path/hash entry in protocol freeze",
    )
    manifest_key = manifest_keys[0]
    for relative, expected_hash in files.items():
        require(
            isinstance(relative, str) and isinstance(expected_hash, str),
            "invalid protocol-freeze file entry",
        )
        path = manifest_path if relative == manifest_key else core_root / relative
        actual_hash = file_sha256(path)
        require(actual_hash == expected_hash, f"frozen core file changed: {relative}")
        verified[relative] = actual_hash
        verified_paths[relative] = str(path.resolve())
    return verified, verified_paths, manifest_key


def validate_cases(
    payload: Any, issue_code_groups: Mapping[str, Any]
) -> tuple[list[str], dict[str, Mapping[str, Any]]]:
    require(isinstance(payload, Mapping), "diagnostic cases must be an object")
    expected_count = payload.get("expected_count")
    require(
        isinstance(expected_count, int) and not isinstance(expected_count, bool),
        "diagnostic expected_count must be an integer",
    )
    records = payload.get("records")
    require(isinstance(records, list), "diagnostic records must be a list")
    require(
        expected_count > 0 and len(records) == expected_count,
        "diagnostic manifest record count differs from expected_count",
    )
    require(
        payload.get("input_contract", {}).get("annotations_passed_to_judge") is False,
        "diagnostic input contract does not exclude annotations",
    )
    require(all(isinstance(record, Mapping) for record in records), "invalid diagnostic record")
    ids = exact_ids(
        (record.get("id") for record in records),
        "diagnostic manifest",
        expected_count,
    )
    by_id = dict(zip(ids, records, strict=True))
    valid_issue_codes = set().union(*issue_code_groups.values())
    for record_id, record in by_id.items():
        feedback = record.get("human_feedback")
        require(isinstance(feedback, str), f"{record_id}: human_feedback must be text")
        expectation = record.get("diagnostic_expectation")
        require(isinstance(expectation, Mapping), f"{record_id}: diagnostic expectation missing")
        for field in ("acceptable_verdicts", "expected_issue_any"):
            values = expectation.get(field)
            require(
                isinstance(values, list)
                and all(isinstance(value, str) and value for value in values),
                f"{record_id}: {field} must be a string list",
            )
            require(len(values) == len(set(values)), f"{record_id}: duplicate {field}")
        require(
            set(expectation["acceptable_verdicts"]) <= {"pass", "review", "fail"},
            f"{record_id}: acceptable_verdicts contains an invalid verdict",
        )
        require(
            set(expectation["expected_issue_any"]) <= valid_issue_codes,
            f"{record_id}: expected_issue_any contains a code outside the v3 schema",
        )
        require(
            isinstance(expectation.get("question"), str) and expectation["question"],
            f"{record_id}: diagnostic question missing",
        )
        require(
            expectation.get("passed_to_judge") is False,
            f"{record_id}: diagnostic expectation is not marked withheld",
        )
    return ids, by_id


def verify_comment_sources(
    manifest_ids: list[str],
    by_id: Mapping[str, Mapping[str, Any]],
    *,
    core_root: Path,
    manifest_path: Path,
) -> dict[str, dict[str, Any]]:
    inventory_path = core_root / "data" / "comment_inventory.json"
    inventory = load_json(inventory_path)
    require(isinstance(inventory, Mapping), "comment inventory must be an object")
    records = inventory.get("records")
    require(isinstance(records, list), "comment inventory records must be a list")
    inventory_by_id: dict[str, Mapping[str, Any]] = {}
    for record in records:
        require(isinstance(record, Mapping), "comment inventory record is invalid")
        record_id = record.get("id")
        require(isinstance(record_id, str) and record_id, "comment inventory ID is invalid")
        require(record_id not in inventory_by_id, f"duplicate comment inventory ID: {record_id}")
        inventory_by_id[record_id] = record

    sources: dict[str, dict[str, Any]] = {}
    for record_id in manifest_ids:
        if record_id in OLD_REGRESSION_IDS:
            require(
                record_id not in inventory_by_id,
                f"{record_id}: old regression unexpectedly appears in v3 comment inventory",
            )
            sources[record_id] = {
                "kind": "earlier_user_failure_feedback_frozen_in_diagnostic_manifest",
                "path": str(manifest_path.resolve()),
            }
            continue
        require(record_id in inventory_by_id, f"{record_id}: missing from comment inventory")
        inventory_comment = inventory_by_id[record_id].get("comments", {}).get("row")
        require(
            inventory_comment == by_id[record_id]["human_feedback"],
            f"{record_id}: diagnostic human feedback differs from exact comment inventory text",
        )
        sources[record_id] = {
            "kind": "exact_v3_comment_inventory_row",
            "path": str(inventory_path.resolve()),
            "inventory_record_id": record_id,
        }
    return sources


def expected_runtime_input(record: Mapping[str, Any], core: CoreRuntime) -> dict[str, str]:
    record_id, runtime_input = core.flatten_record(record)
    require(record_id == record.get("id"), f"{record_id}: runner flattened a different ID")
    require(set(runtime_input) == EXPECTED_INPUT_KEYS, f"{record_id}: unexpected runtime input keys")
    return runtime_input


def baseline_result_path(record_id: str) -> Path:
    batch = "userfail_regression_v3" if record_id in OLD_REGRESSION_IDS else "v6_batch_v1"
    return V2_ROOT / "runs" / batch / record_id / "result.json"


def issue_codes(judgment: Mapping[str, Any]) -> dict[str, list[str]]:
    components = judgment.get("observation", {}).get("components", {})
    require(isinstance(components, Mapping), "judgment components missing")
    result: dict[str, list[str]] = {}
    for component, value in components.items():
        require(isinstance(value, Mapping), f"invalid component: {component}")
        codes = value.get("issue_codes")
        require(
            isinstance(codes, list) and all(isinstance(code, str) for code in codes),
            f"invalid issue codes: {component}",
        )
        result[str(component)] = list(codes)
    return result


def score_summary(judgment: Mapping[str, Any]) -> dict[str, Any]:
    summary = {key: value for key, value in judgment.items() if key != "observation"}
    summary["issue_codes_by_component"] = issue_codes(judgment)
    return summary


def verify_baseline(record_id: str, expected_input: Mapping[str, Any]) -> dict[str, Any]:
    path = baseline_result_path(record_id)
    result = load_json(path)
    require(isinstance(result, Mapping), f"{record_id}: v2 baseline is not an object")
    require(result.get("ok") is True, f"{record_id}: v2 baseline is not successful")
    require(result.get("input") == expected_input, f"{record_id}: v2 baseline input mismatch")
    judgment = result.get("judgment")
    require(isinstance(judgment, Mapping), f"{record_id}: v2 baseline judgment missing")
    return {
        "result_path": str(path.resolve()),
        "result_sha256": file_sha256(path),
        "source_batch": path.parent.parent.name,
        "model_requested": result.get("model_requested"),
        "model_returned": result.get("model_returned"),
        "scores": score_summary(judgment),
    }


def verify_source_bytes(record_id: str, record: Mapping[str, Any]) -> dict[str, Any]:
    generated = record.get("generated_image")
    twin = record.get("twin_image")
    hashes = record.get("hashes")
    require(
        isinstance(generated, Mapping)
        and isinstance(twin, Mapping)
        and isinstance(hashes, Mapping),
        f"{record_id}: source byte metadata missing",
    )
    generated_path = Path(str(generated.get("local_path"))).resolve()
    twin_path = Path(str(twin.get("local_path"))).resolve()
    generated_hash = file_sha256(generated_path)
    twin_hash = file_sha256(twin_path)
    prompt = record.get("scene_prompt")
    require(isinstance(prompt, str), f"{record_id}: scene prompt is not text")
    prompt_hash = text_sha256(prompt)
    require(
        generated_hash == generated.get("sha256") == hashes.get("generated_image_sha256"),
        f"{record_id}: generated image bytes differ from manifest",
    )
    require(
        twin_hash == twin.get("sha256") == hashes.get("twin_image_sha256"),
        f"{record_id}: twin image bytes differ from manifest",
    )
    require(
        prompt_hash == record.get("scene_prompt_sha256") == hashes.get("scene_prompt_sha256"),
        f"{record_id}: scene prompt bytes differ from manifest",
    )
    return {
        "generated_image": {"path": str(generated_path), "sha256": generated_hash},
        "twin_image": {"path": str(twin_path), "sha256": twin_hash},
        "scene_prompt_sha256": prompt_hash,
    }


def verify_progress(
    *,
    progress: Mapping[str, Any],
    manifest_path: Path,
    manifest_sha256: str,
    run_dir: Path,
    manifest_ids: list[str],
    freeze: Mapping[str, Any],
    allow_incomplete: bool,
    expected_visual_anchors: bool,
) -> tuple[list[str], list[dict[str, str]]]:
    require(
        progress.get("schema_version") == "placement-v3-batch-progress-v1",
        "unexpected progress schema",
    )
    require(
        Path(progress.get("manifest", "")).resolve() == manifest_path,
        "progress manifest path mismatch",
    )
    require(
        progress.get("manifest_sha256") == manifest_sha256,
        "progress manifest hash mismatch",
    )
    require(progress.get("run_name") == run_dir.name, "progress run name mismatch")
    require(progress.get("model") == freeze["model"], "progress model differs from freeze")
    require(
        progress.get("visual_anchors") is expected_visual_anchors,
        "progress visual-anchor mode differs from protocol snapshot",
    )
    require(progress.get("limit") is None, "diagnostic run used a record limit")
    progress_ids = exact_ids(progress.get("record_ids", []), "progress", len(manifest_ids))
    require(progress_ids == manifest_ids, "progress IDs/order differ from diagnostic manifest")
    items = progress.get("items")
    require(isinstance(items, Mapping) and set(items) == set(manifest_ids), "progress items differ from manifest")
    require(all(isinstance(item, Mapping) for item in items.values()), "progress item is invalid")
    require(
        all(isinstance(item.get("status"), str) for item in items.values()),
        "progress item status is invalid",
    )
    states = Counter(item.get("status") for item in items.values())
    require(progress.get("counts") == counter_dict(states), "progress counts differ from item states")
    completed = [record_id for record_id in manifest_ids if items[record_id].get("status") in SUCCESS_STATES]
    missing = [
        {"id": record_id, "progress_status": str(items[record_id].get("status"))}
        for record_id in manifest_ids
        if items[record_id].get("status") not in SUCCESS_STATES
    ]
    if not allow_incomplete:
        require(progress.get("status") == "complete", f"diagnostic run is not complete: {progress.get('status')}")
        require(not missing, f"diagnostic run has {len(missing)} incomplete cases")
    return completed, missing


def verify_case(
    *,
    record_id: str,
    record: Mapping[str, Any],
    progress_item: Mapping[str, Any],
    run_dir: Path,
    freeze: Mapping[str, Any],
    frozen_hashes: Mapping[str, str],
    anchor_manifest: Mapping[str, Any] | None,
    expected_visual_anchors: bool,
    comment_source: Mapping[str, Any],
    core: CoreRuntime,
) -> tuple[dict[str, Any], bool | None, bool | None]:
    expected_input = expected_runtime_input(record, core)
    source_bytes = verify_source_bytes(record_id, record)
    case_dir = run_dir / record_id
    request_path = case_dir / "request.json"
    response_path = case_dir / "response.json"
    result_path = case_dir / "result.json"
    request = load_json(request_path)
    response = load_json(response_path)
    result = load_json(result_path)
    require(
        all(isinstance(value, Mapping) for value in (request, response, result)),
        f"{record_id}: run artifacts must be objects",
    )
    require(
        Path(progress_item.get("result_path", "")).resolve() == result_path.resolve(),
        f"{record_id}: progress result path mismatch",
    )
    require(
        progress_item.get("result_sha256") == file_sha256(result_path),
        f"{record_id}: progress result hash mismatch",
    )
    require(result.get("ok") is True, f"{record_id}: result is not successful")
    require(request.get("input") == expected_input == result.get("input"), f"{record_id}: runtime input mismatch")
    require(set(request["input"]) == EXPECTED_INPUT_KEYS, f"{record_id}: runtime input has extra fields")

    feedback = record["human_feedback"]
    question = record["diagnostic_expectation"]["question"]
    require(
        not recursive_contains_text(request["input"], feedback),
        f"{record_id}: target human feedback leaked into runtime input",
    )
    require(
        not recursive_contains_text(request["input"], question),
        f"{record_id}: diagnostic question leaked into runtime input",
    )
    require(
        not recursive_contains_text(request, feedback),
        f"{record_id}: target human feedback leaked into request record",
    )
    require(
        not recursive_contains_text(request, question),
        f"{record_id}: diagnostic question leaked into request record",
    )

    for name in ("generated_image", "twin_image"):
        expected_hash = source_bytes[name]["sha256"]
        require(
            request.get("images", {}).get(name, {}).get("sha256") == expected_hash,
            f"{record_id}: request {name} hash mismatch",
        )
        require(
            result.get("images", {}).get(name, {}).get("sha256") == expected_hash,
            f"{record_id}: result {name} hash mismatch",
        )

    for key, value in request.items():
        require(result.get(key) == value, f"{record_id}: result changed request field {key}")
    fingerprint_payload = {
        key: value for key, value in request.items() if key not in {"started_at", "fingerprint"}
    }
    require(
        request.get("fingerprint") == json_sha256(fingerprint_payload),
        f"{record_id}: request fingerprint mismatch",
    )
    require(
        request.get("protocol_version") == core.protocol_version,
        f"{record_id}: protocol version mismatch",
    )
    require(request.get("runner_sha256") == frozen_hashes["run_judge.py"], f"{record_id}: runner hash mismatch")
    require(
        request.get("wire_schema_sha256") == core.wire_schema_sha256,
        f"{record_id}: wire schema hash mismatch",
    )
    require(
        request.get("system_prompt_sha256") == frozen_hashes["system_prompt.md"],
        f"{record_id}: system prompt hash mismatch",
    )
    require(
        request.get("schema_sha256") == frozen_hashes["observation_schema.json"],
        f"{record_id}: observation schema hash mismatch",
    )
    require(
        request.get("scoring_sha256") == frozen_hashes["scoring.py"],
        f"{record_id}: scoring hash mismatch",
    )
    require(request.get("model_requested") == freeze["model"], f"{record_id}: requested model mismatch")
    require(
        request.get("reasoning_effort") == freeze["reasoning_effort"],
        f"{record_id}: reasoning effort mismatch",
    )
    require(
        request.get("visual_anchors_enabled") is expected_visual_anchors,
        f"{record_id}: request visual-anchor mode differs from protocol snapshot",
    )
    require(
        file_sha256(case_dir / "system_prompt.md") == frozen_hashes["system_prompt.md"],
        f"{record_id}: preserved system prompt differs from freeze",
    )
    require(
        file_sha256(case_dir / "observation_schema.json") == frozen_hashes["observation_schema.json"],
        f"{record_id}: preserved observation schema differs from freeze",
    )

    if expected_visual_anchors:
        require(anchor_manifest is not None, f"{record_id}: anchor manifest was not loaded")
        require(
            request.get("visual_anchor_manifest_sha256")
            == frozen_hashes["data/visual_anchors.json"],
            f"{record_id}: visual-anchor manifest hash mismatch",
        )
        files_for_helper = {
            name: {
                "path": source_bytes[name]["path"],
                "sha256": source_bytes[name]["sha256"],
            }
            for name in ("generated_image", "twin_image")
        }
        selected, exact_ids, family_ids, target_family = core.select_visual_anchors(
            anchor_manifest, files_for_helper
        )
        require(
            request.get("visual_anchors") == selected,
            f"{record_id}: selected anchors differ from runner helper",
        )
        require(
            request.get("excluded_target_identical_anchor_ids") == exact_ids,
            f"{record_id}: exact-target anchor exclusions differ from runner helper",
        )
        require(
            request.get("excluded_same_case_family_anchor_ids") == family_ids,
            f"{record_id}: same-family anchor exclusions differ from runner helper",
        )
        require(
            request.get("target_case_family") == target_family,
            f"{record_id}: target anchor family differs from runner helper",
        )
        anchor_assertions = {
            "enabled": True,
            "runner_helper": "run_judge._select_visual_anchors",
            "target_case_family": target_family,
            "excluded_target_identical_anchor_ids": exact_ids,
            "excluded_same_case_family_anchor_ids": family_ids,
            "recorded_values_match_helper_exactly": True,
        }
    else:
        anchor_only_fields = {
            "visual_anchor_manifest_sha256",
            "visual_anchors",
            "excluded_target_identical_anchor_ids",
            "excluded_same_case_family_anchor_ids",
            "target_case_family",
        }
        present_anchor_fields = sorted(anchor_only_fields & set(request))
        require(
            not present_anchor_fields,
            f"{record_id}: no-anchor request retained anchor-only fields: {present_anchor_fields}",
        )
        anchor_assertions = {
            "enabled": False,
            "anchor_only_fields_absent": True,
        }

    choices = response.get("choices")
    require(isinstance(choices, list) and len(choices) == 1, f"{record_id}: response must have one choice")
    choice = choices[0]
    require(isinstance(choice, Mapping), f"{record_id}: response choice is invalid")
    require(choice.get("finish_reason") == "stop", f"{record_id}: response did not stop normally")
    message = choice.get("message")
    require(isinstance(message, Mapping), f"{record_id}: response message missing")
    require(message.get("refusal") in (None, False), f"{record_id}: response was refused")
    content = message.get("content")
    require(isinstance(content, str), f"{record_id}: raw response content missing")
    try:
        raw_observation = json.loads(content)
    except json.JSONDecodeError as exc:
        raise AuditError(f"{record_id}: raw response content is invalid JSON: {exc}") from exc
    judgment = result.get("judgment")
    require(isinstance(judgment, Mapping), f"{record_id}: result judgment missing")
    require(
        raw_observation == judgment.get("observation"),
        f"{record_id}: result observation differs from raw response content",
    )
    recomputed = core.aggregate_observation(raw_observation)
    require(recomputed == judgment, f"{record_id}: v3 scores differ from deterministic recomputation")
    returned_model = response.get("model")
    require(returned_model == result.get("model_returned"), f"{record_id}: response/result model mismatch")
    require(
        core.model_identity_matches(freeze["model"], returned_model),
        f"{record_id}: returned model identity does not match requested model",
    )
    require(response.get("usage") == result.get("usage"), f"{record_id}: response/result usage mismatch")

    observed_by_component = issue_codes(judgment)
    observed_codes = sorted({code for codes in observed_by_component.values() for code in codes})
    expectation = record["diagnostic_expectation"]
    acceptable_verdicts = expectation["acceptable_verdicts"]
    expected_issue_any = expectation["expected_issue_any"]
    actual_verdict = judgment.get("verdict")
    verdict_match = actual_verdict in acceptable_verdicts if acceptable_verdicts else None
    matched_issues = sorted(set(observed_codes) & set(expected_issue_any))
    issue_match = bool(matched_issues) if expected_issue_any else None

    baseline = verify_baseline(record_id, expected_input)
    per_case = {
        "id": record_id,
        "exact_human_comment": feedback,
        "exact_human_comment_sha256": text_sha256(feedback),
        "exact_human_comment_source": dict(comment_source),
        "mapped_expectations": dict(expectation),
        "expectation_checks": {
            "verdict": None
            if not acceptable_verdicts
            else {
                "actual": actual_verdict,
                "acceptable": acceptable_verdicts,
                "matched": verdict_match,
            },
            "issue_any": None
            if not expected_issue_any
            else {
                "observed": observed_codes,
                "expected_any": expected_issue_any,
                "matched_values": matched_issues,
                "matched": issue_match,
            },
        },
        "v2_baseline": baseline,
        "v3_scores": score_summary(judgment),
        "audit": {
            "source_bytes": source_bytes,
            "request_path": str(request_path.resolve()),
            "request_sha256": file_sha256(request_path),
            "raw_response_path": str(response_path.resolve()),
            "raw_response_sha256": file_sha256(response_path),
            "result_path": str(result_path.resolve()),
            "result_sha256": file_sha256(result_path),
            "raw_response_content_parsed_and_exact": True,
            "v3_scores_recomputed_exact": True,
            "model_identity_verified": True,
            "model_requested": request.get("model_requested"),
            "model_returned": returned_model,
            "protocol_freeze_verified": True,
            "protocol_hashes": {
                "runner_sha256": request.get("runner_sha256"),
                "wire_schema_sha256": request.get("wire_schema_sha256"),
                "system_prompt_sha256": request.get("system_prompt_sha256"),
                "observation_schema_sha256": request.get("schema_sha256"),
                "scoring_sha256": request.get("scoring_sha256"),
                "visual_anchor_manifest_sha256": request.get("visual_anchor_manifest_sha256"),
            },
            "target_comment_absent_from_input": True,
            "target_comment_absent_from_request_record": True,
            "anchor_exclusion_assertions": anchor_assertions,
        },
    }
    return per_case, verdict_match, issue_match


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        "--cases",
        dest="manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="diagnostic case manifest (--cases is retained as a compatibility alias)",
    )
    parser.add_argument("--freeze", type=Path, default=DEFAULT_FREEZE)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--core-root",
        type=Path,
        default=DEFAULT_CORE_ROOT,
        help="protocol core containing scoring.py, run_judge.py, schema, prompt, and anchor data",
    )
    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help="write a partial audit for progress items already marked done/cached",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = args.manifest.expanduser().resolve()
    freeze_path = args.freeze.expanduser().resolve()
    run_dir = args.run_dir.expanduser().resolve()
    output_path = args.output.expanduser().resolve()
    core_root = args.core_root.expanduser().resolve()
    core = load_core_runtime(core_root)
    freeze = load_json(freeze_path)
    require(isinstance(freeze, Mapping), "protocol freeze must be an object")
    manifest_payload = load_json(manifest_path)
    manifest_sha256 = file_sha256(manifest_path)
    frozen_hashes, frozen_paths, manifest_relative = verify_freeze(
        freeze,
        core_root=core_root,
        manifest_path=manifest_path,
        manifest_sha256=manifest_sha256,
    )
    expected_visual_anchors = freeze.get("visual_anchors", True)
    require(
        isinstance(expected_visual_anchors, bool),
        "protocol snapshot visual_anchors must be boolean",
    )
    manifest_ids, by_id = validate_cases(manifest_payload, core.issue_codes)
    comment_sources = verify_comment_sources(
        manifest_ids,
        by_id,
        core_root=core_root,
        manifest_path=manifest_path,
    )
    progress_path = run_dir / "progress.json"
    progress = load_json(progress_path)
    require(isinstance(progress, Mapping), "progress ledger must be an object")
    completed_ids, missing = verify_progress(
        progress=progress,
        manifest_path=manifest_path,
        manifest_sha256=manifest_sha256,
        run_dir=run_dir,
        manifest_ids=manifest_ids,
        freeze=freeze,
        allow_incomplete=args.allow_incomplete,
        expected_visual_anchors=expected_visual_anchors,
    )

    for pattern in ("*/request.json", "*/response.json", "*/result.json"):
        unexpected = sorted(
            path.parent.name for path in run_dir.glob(pattern) if path.parent.name not in by_id
        )
        require(not unexpected, f"unexpected run artifact IDs for {pattern}: {unexpected}")

    anchor_manifest = None
    if expected_visual_anchors:
        anchor_manifest = core.load_visual_anchors(core_root)
        require(
            file_sha256(core_root / "data" / "visual_anchors.json")
            == frozen_hashes["data/visual_anchors.json"],
            "visual-anchor manifest differs from protocol snapshot",
        )
    per_case: list[dict[str, Any]] = []
    verdict_results: list[bool] = []
    issue_results: list[bool] = []
    for record_id in completed_ids:
        case, verdict_match, issue_match = verify_case(
            record_id=record_id,
            record=by_id[record_id],
            progress_item=progress["items"][record_id],
            run_dir=run_dir,
            freeze=freeze,
            frozen_hashes=frozen_hashes,
            anchor_manifest=anchor_manifest,
            expected_visual_anchors=expected_visual_anchors,
            comment_source=comment_sources[record_id],
            core=core,
        )
        per_case.append(case)
        if verdict_match is not None:
            verdict_results.append(verdict_match)
        if issue_match is not None:
            issue_results.append(issue_match)

    mapped_verdict_total = sum(
        bool(by_id[record_id]["diagnostic_expectation"]["acceptable_verdicts"])
        for record_id in manifest_ids
    )
    mapped_issue_total = sum(
        bool(by_id[record_id]["diagnostic_expectation"]["expected_issue_any"])
        for record_id in manifest_ids
    )
    evaluation = {
        "schema_version": "placement-v3-diagnostic-evaluation-v1",
        "status": "complete" if not missing else "partial_allow_incomplete",
        "interpretation": (
            "Comment-driven development expectation checks; not held-out data, gold labels, "
            "or an accuracy estimate. Empty expectation lists are not checks."
        ),
        "sources": {
            "manifest": {
                "path": str(manifest_path),
                "sha256": manifest_sha256,
                "relative_protocol_path": manifest_relative,
            },
            "protocol_freeze": {
                "path": str(freeze_path),
                "sha256": file_sha256(freeze_path),
                "status": freeze.get("status"),
                "visual_anchors": expected_visual_anchors,
                "verified_core_files": frozen_hashes,
                "verified_file_paths": frozen_paths,
            },
            "core_root": str(core_root),
            "progress": {
                "path": str(progress_path.resolve()),
                "sha256_at_evaluation": file_sha256(progress_path),
                "status": progress.get("status"),
                "updated_at_utc": progress.get("updated_at_utc"),
            },
            "run_dir": str(run_dir),
        },
        "counts": {
            "manifest_cases": len(manifest_ids),
            "evaluated_cases": len(per_case),
            "missing_or_incomplete_cases": len(missing),
            "verdict_expectations_nonempty": {
                "matched": sum(verdict_results),
                "evaluated_denominator": len(verdict_results),
                "mapped_total_in_manifest": mapped_verdict_total,
            },
            "issue_any_expectations_nonempty": {
                "matched": sum(issue_results),
                "evaluated_denominator": len(issue_results),
                "mapped_total_in_manifest": mapped_issue_total,
            },
        },
        "missing_or_incomplete": missing,
        "cases": per_case,
    }
    atomic_json(output_path, evaluation)
    print(
        json.dumps(
            {
                "output": str(output_path),
                "status": evaluation["status"],
                "counts": evaluation["counts"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditError as exc:
        raise SystemExit(f"AUDIT FAILED: {exc}") from exc
