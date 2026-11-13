# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema"]
# ///
"""Verify a complete frozen V6 evaluation and write its aggregate summary.

This script is model-free. It fails closed on partial runs and writes the output
only after every manifest, byte, request, response, and judgment check passes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Iterable, Mapping

from scoring import COMPONENT_WEIGHTS, aggregate_observation


ROOT = Path(__file__).resolve().parent
DEFAULT_MANIFEST = ROOT / "data/v6_assets.json"
DEFAULT_FREEZE = ROOT / "data/v6_run_freeze.json"
DEFAULT_RUN_DIR = ROOT / "runs/v6_batch_v1"
DEFAULT_OUTPUT = ROOT / "data/evaluation_summary.json"
MODEL_RETURNED_RE = re.compile(r"^gpt-5\.5-\d{4}-\d{2}-\d{2}$")
SUCCESS_ITEM_STATES = {"done", "cached"}



class AuditError(RuntimeError):
    """The evaluation cannot be certified."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def load_json(path: Path) -> Any:
    require(path.is_file(), f"missing JSON file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AuditError(f"invalid JSON file {path}: {error}") from error


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def exact_ids(values: Iterable[Any], label: str, expected_count: int) -> list[str]:
    ids = list(values)
    require(len(ids) == expected_count, f"{label} has {len(ids)} IDs, expected {expected_count}")
    require(all(isinstance(value, str) and value for value in ids), f"{label} has invalid IDs")
    require(len(set(ids)) == expected_count, f"{label} contains duplicate IDs")
    return ids


def percentile(values: list[float], percent: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    rank = max(1, math.ceil(percent * len(ordered)))
    return round(ordered[rank - 1], 3)


def numeric_summary(values: Iterable[Any]) -> dict[str, Any]:
    numbers = [float(value) for value in values if isinstance(value, (int, float)) and not isinstance(value, bool)]
    if not numbers:
        return {"count": 0, "sum": 0, "mean": None, "min": None, "p50": None, "p95": None, "max": None}
    return {
        "count": len(numbers),
        "sum": round(sum(numbers), 3),
        "mean": round(mean(numbers), 3),
        "min": round(min(numbers), 3),
        "p50": percentile(numbers, 0.50),
        "p95": percentile(numbers, 0.95),
        "max": round(max(numbers), 3),
    }


def counter_dict(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def runtime_input(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "generated_image": str(Path(record["generated_image"]["local_path"]).resolve()),
        "twin_image": str(Path(record["twin_image"]["local_path"]).resolve()),
        "product_type": record["device_type"],
        "scene_prompt": record["scene_prompt"],
        "image_stage": record["image_stage"],
    }


def verify_frozen_files(freeze: Mapping[str, Any]) -> dict[str, str]:
    hashes = freeze.get("hashes")
    require(isinstance(hashes, dict) and hashes, "freeze has no file hashes")
    verified: dict[str, str] = {}
    for relative, expected in hashes.items():
        require(isinstance(relative, str) and isinstance(expected, str), "invalid frozen hash entry")
        path = ROOT / relative
        actual = file_sha256(path)
        require(actual == expected, f"frozen file hash mismatch: {relative}")
        verified[relative] = actual
    return verified


def verify_anchor_manifest(freeze: Mapping[str, Any]) -> tuple[dict[str, Any], set[str]]:
    path = ROOT / "data/visual_anchors.json"
    expected_hash = freeze["hashes"].get("data/visual_anchors.json")
    require(file_sha256(path) == expected_hash, "visual anchor manifest differs from freeze")
    payload = load_json(path)
    examples = payload.get("examples")
    require(isinstance(examples, list) and len(examples) == 7, "visual anchor manifest must contain seven examples")
    ids = exact_ids((example.get("asset_id") for example in examples), "visual anchor manifest", 7)
    hashes = [example.get("sha256") for example in examples]
    require(all(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) for value in hashes), "visual anchor manifest has invalid hashes")
    require(len(set(hashes)) == 7, "visual anchor manifest has duplicate image hashes")
    for example in examples:
        path = Path(example["local_path"])
        require(file_sha256(path) == example["sha256"], f"visual anchor bytes changed: {example['asset_id']}")
    require(len(ids) == 7, "visual anchor ID verification failed")
    return payload, set(hashes)


def usage_value(usage: Mapping[str, Any], *path: str) -> Any:
    value: Any = usage
    for key in path:
        if not isinstance(value, Mapping):
            return None
        value = value.get(key)
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--freeze", type=Path, default=DEFAULT_FREEZE)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    manifest_path = args.manifest.expanduser().resolve()
    freeze_path = args.freeze.expanduser().resolve()
    run_dir = args.run_dir.expanduser().resolve()
    output_path = args.output.expanduser().resolve()
    freeze = load_json(freeze_path)
    manifest = load_json(manifest_path)
    target_count = freeze.get("target_count")
    require(target_count == 96, f"frozen target_count is {target_count!r}, expected 96")
    require(freeze.get("model") == "gpt-5.5", "frozen requested model is not gpt-5.5")
    require(freeze.get("reasoning_effort") == "high", "frozen reasoning effort is not high")
    frozen_hashes = verify_frozen_files(freeze)
    require(file_sha256(manifest_path) == freeze["hashes"].get("data/v6_assets.json"), "selected manifest differs from freeze")

    records = manifest.get("records")
    require(isinstance(records, list), "manifest records is not a list")
    require(manifest.get("expected_count") == target_count, "manifest expected_count differs from freeze")
    manifest_ids = exact_ids((record.get("id") for record in records), "manifest", target_count)
    by_id = dict(zip(manifest_ids, records, strict=True))

    progress_path = run_dir / "progress.json"
    progress = load_json(progress_path)
    require(progress.get("schema_version") == "placement-v2-batch-progress-v2", "progress ledger is not schema v2")
    require(progress.get("manifest_sha256") == file_sha256(manifest_path), "progress manifest hash mismatch")
    require(Path(progress.get("manifest", "")).resolve() == manifest_path, "progress manifest path mismatch")
    require(progress.get("model") == freeze["model"], "progress requested model mismatch")
    require(progress.get("visual_anchors") is True, "progress did not enable visual anchors")
    require(progress.get("run_name") == run_dir.name, "progress run name differs from run directory")
    require(progress.get("limit") is None, "progress ledger used a record limit")
    require(progress.get("status") == "complete", f"evaluation is partial: progress status is {progress.get('status')!r}")
    progress_ids = exact_ids(progress.get("record_ids", []), "progress", target_count)
    require(progress_ids == manifest_ids, "progress record IDs/order differ from manifest")
    items = progress.get("items")
    require(isinstance(items, dict) and set(items) == set(manifest_ids), "progress items differ from manifest IDs")
    incomplete = {record_id: item.get("status") for record_id, item in items.items() if item.get("status") not in SUCCESS_ITEM_STATES}
    require(not incomplete, f"evaluation is partial: {len(incomplete)} incomplete progress items")
    computed_progress_counts = counter_dict(
        Counter(item.get("status") for item in items.values())
    )
    require(
        progress.get("counts") == computed_progress_counts,
        "progress counts differ from item states",
    )

    result_ids = exact_ids(
        (path.parent.name for path in run_dir.glob("*/result.json")),
        "result files",
        target_count,
    )
    require(set(result_ids) == set(manifest_ids), "result file IDs differ from manifest")
    request_ids = exact_ids(
        (path.parent.name for path in run_dir.glob("*/request.json")),
        "request files",
        target_count,
    )
    response_ids = exact_ids(
        (path.parent.name for path in run_dir.glob("*/response.json")),
        "response files",
        target_count,
    )
    require(set(request_ids) == set(manifest_ids), "request file IDs differ from manifest")
    require(set(response_ids) == set(manifest_ids), "response file IDs differ from manifest")

    anchor_manifest, anchor_hashes = verify_anchor_manifest(freeze)
    anchors_sha = file_sha256(ROOT / "data/visual_anchors.json")
    model_returned_values: set[str] = set()
    counts: dict[str, Counter] = defaultdict(Counter)
    component_counts: dict[str, dict[str, Counter]] = {
        component: {
            "visibility": Counter(),
            "severity": Counter(),
            "confidence": Counter(),
            "issue_codes": Counter(),
        }
        for component in COMPONENT_WEIGHTS
    }
    usage_metrics: dict[str, list[Any]] = defaultdict(list)
    latency_metrics: dict[str, list[Any]] = defaultdict(list)
    result_set: list[dict[str, Any]] = []
    per_record: list[dict[str, Any]] = []

    for record_id in manifest_ids:
        record = by_id[record_id]
        generated = record.get("generated_image")
        twin = record.get("twin_image")
        require(isinstance(generated, dict) and isinstance(twin, dict), f"{record_id}: image metadata missing")
        generated_hash = file_sha256(Path(generated["local_path"]))
        twin_hash = file_sha256(Path(twin["local_path"]))
        prompt = record.get("scene_prompt")
        require(isinstance(prompt, str), f"{record_id}: scene prompt is not text")
        prompt_hash = text_sha256(prompt)
        hashes = record.get("hashes")
        require(isinstance(hashes, dict), f"{record_id}: aggregate hashes missing")
        require(generated_hash == generated.get("sha256") == hashes.get("generated_image_sha256"), f"{record_id}: generated image hash mismatch")
        require(twin_hash == twin.get("sha256") == hashes.get("twin_image_sha256"), f"{record_id}: twin image hash mismatch")
        require(prompt_hash == record.get("scene_prompt_sha256") == hashes.get("scene_prompt_sha256"), f"{record_id}: source prompt hash mismatch")
        prompt_source = record.get("scene_prompt_source")
        require(isinstance(prompt_source, dict) and prompt_source.get("kind") == "original_v6_prompt", f"{record_id}: prompt is not marked original V6")
        require(prompt_source.get("rewritten_prompt_included") is False, f"{record_id}: rewritten prompt inclusion is not false")
        require(generated_hash not in anchor_hashes and twin_hash not in anchor_hashes, f"{record_id}: target or twin overlaps a fixed anchor")

        case_dir = run_dir / record_id
        request_path = case_dir / "request.json"
        response_path = case_dir / "response.json"
        result_path = case_dir / "result.json"
        request = load_json(request_path)
        response = load_json(response_path)
        result = load_json(result_path)
        progress_item = items[record_id]
        require(
            Path(progress_item.get("result_path", "")).resolve() == result_path,
            f"{record_id}: progress result path mismatch",
        )
        require(
            progress_item.get("result_sha256") == file_sha256(result_path),
            f"{record_id}: progress result hash mismatch",
        )
        require(result.get("ok") is True, f"{record_id}: result is not successful")
        expected_input = runtime_input(record)
        require(request.get("input") == expected_input == result.get("input"), f"{record_id}: runtime input differs from manifest")
        for name, expected_hash in (("generated_image", generated_hash), ("twin_image", twin_hash)):
            require(request.get("images", {}).get(name, {}).get("sha256") == expected_hash, f"{record_id}: request {name} hash mismatch")
            require(result.get("images", {}).get(name, {}).get("sha256") == expected_hash, f"{record_id}: result {name} hash mismatch")
        for key, value in request.items():
            require(result.get(key) == value, f"{record_id}: result changed request field {key}")
        request_fingerprint = request.get("fingerprint")
        fingerprint_payload = {
            key: value
            for key, value in request.items()
            if key not in {"started_at", "fingerprint"}
        }
        require(
            request_fingerprint == json_sha256(fingerprint_payload),
            f"{record_id}: request fingerprint mismatch",
        )
        require(request.get("runner_sha256") == freeze["hashes"]["run_judge.py"], f"{record_id}: runner hash differs from freeze")
        require(request.get("system_prompt_sha256") == freeze["hashes"]["system_prompt.md"], f"{record_id}: prompt hash differs from freeze")
        require(request.get("schema_sha256") == freeze["hashes"]["observation_schema.json"], f"{record_id}: schema hash differs from freeze")
        require(request.get("scoring_sha256") == freeze["hashes"]["scoring.py"], f"{record_id}: scoring hash differs from freeze")
        require(request.get("model_requested") == freeze["model"], f"{record_id}: requested model differs from freeze")
        require(request.get("reasoning_effort") == freeze["reasoning_effort"], f"{record_id}: reasoning effort differs from freeze")
        require(request.get("visual_anchors_enabled") is True, f"{record_id}: anchors were not enabled")
        require(request.get("visual_anchor_manifest_sha256") == anchors_sha, f"{record_id}: anchor manifest hash mismatch")
        require(request.get("visual_anchors") == anchor_manifest, f"{record_id}: fixed anchors differ from frozen seven")
        require(len(request["visual_anchors"]["examples"]) == 7, f"{record_id}: request does not contain seven anchors")
        require(request.get("excluded_target_identical_anchor_ids") == [], f"{record_id}: target-identical anchor was present")

        choices = response.get("choices")
        require(isinstance(choices, list) and len(choices) == 1, f"{record_id}: response must have one choice")
        choice = choices[0]
        require(choice.get("finish_reason") == "stop", f"{record_id}: response did not finish normally")
        message = choice.get("message")
        require(isinstance(message, dict) and message.get("refusal") in (None, False), f"{record_id}: response was refused")
        content = message.get("content")
        require(isinstance(content, str), f"{record_id}: response content is missing")
        try:
            raw_observation = json.loads(content)
        except json.JSONDecodeError as error:
            raise AuditError(f"{record_id}: response content is invalid JSON: {error}") from error
        judgment = result.get("judgment")
        require(isinstance(judgment, dict), f"{record_id}: result judgment missing")
        require(raw_observation == judgment.get("observation"), f"{record_id}: response observation was modified")
        recomputed = aggregate_observation(raw_observation)
        require(recomputed == judgment, f"{record_id}: deterministic reaggregation differs from result")
        returned = response.get("model")
        require(returned == result.get("model_returned"), f"{record_id}: response/result model mismatch")
        require(isinstance(returned, str) and MODEL_RETURNED_RE.fullmatch(returned), f"{record_id}: returned model is not dated GPT-5.5")
        require(response.get("usage") == result.get("usage"), f"{record_id}: response/result usage mismatch")
        model_returned_values.add(returned)

        counts["device_type"][record["device_type"]] += 1
        counts["device"][record["device"]] += 1
        counts["camera_tag"][record["view"]["camera_tag"]] += 1
        counts["view_role"][record["view"]["view_role"]] += 1
        counts["verdict"][judgment["verdict"]] += 1
        counts["product_match"][raw_observation["product_match"]] += 1
        for component, value in raw_observation["components"].items():
            component_counts[component]["visibility"][value["visibility"]] += 1
            component_counts[component]["severity"]["null" if value["severity"] is None else str(value["severity"])] += 1
            component_counts[component]["confidence"][value["confidence"]] += 1
            component_counts[component]["issue_codes"].update(value["issue_codes"])

        usage = result["usage"]
        for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
            value = usage.get(key)
            require(
                isinstance(value, int) and not isinstance(value, bool) and value >= 0,
                f"{record_id}: invalid usage field {key}",
            )
            usage_metrics[key].append(value)
        require(
            usage["total_tokens"]
            == usage["prompt_tokens"] + usage["completion_tokens"],
            f"{record_id}: total token count is inconsistent",
        )
        usage_metrics["reasoning_tokens"].append(usage_value(usage, "completion_tokens_details", "reasoning_tokens"))
        usage_metrics["cached_tokens"].append(usage_value(usage, "prompt_tokens_details", "cached_tokens"))
        elapsed = result.get("elapsed_seconds")
        require(
            isinstance(elapsed, (int, float))
            and not isinstance(elapsed, bool)
            and elapsed >= 0,
            f"{record_id}: invalid elapsed_seconds",
        )
        latency_metrics["elapsed_seconds"].append(elapsed)
        latency = usage.get("latency_checkpoint") or {}
        require(
            isinstance(latency, dict),
            f"{record_id}: latency checkpoint is not an object",
        )
        for key, value in latency.items():
            require(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and value >= 0,
                f"{record_id}: invalid latency field {key}",
            )
            latency_metrics[key].append(value)

        request_hash = file_sha256(request_path)
        response_hash = file_sha256(response_path)
        result_hash = file_sha256(result_path)
        result_set.append({"id": record_id, "request_sha256": request_hash, "response_sha256": response_hash, "result_sha256": result_hash})
        per_record.append(
            {
                "id": record_id,
                "device_type": record["device_type"],
                "device": record["device"],
                "camera_tag": record["view"]["camera_tag"],
                "view_role": record["view"]["view_role"],
                "verdict": judgment["verdict"],
                "natural_placement_score": judgment["natural_placement_score"],
                "model_returned": returned,
                "request_sha256": request_hash,
                "response_sha256": response_hash,
                "result_sha256": result_hash,
            }
        )

    require(len(model_returned_values) == 1, f"multiple returned model versions: {sorted(model_returned_values)}")
    require(sum(counts["verdict"].values()) == target_count, "verdict counts do not total 96")
    summary = {
        "schema_version": "placement-v2-evaluation-summary-v1",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "verification_status": "VERIFIED_COMPLETE",
        "run": {
            "run_name": progress["run_name"],
            "run_dir": str(run_dir),
            "progress_path": str(progress_path),
            "manifest_path": str(manifest_path),
            "manifest_sha256": file_sha256(manifest_path),
            "freeze_path": str(freeze_path),
            "freeze_sha256": file_sha256(freeze_path),
            "record_count": target_count,
            "requested_model": freeze["model"],
            "returned_model": next(iter(model_returned_values)),
            "visual_anchor_count": 7,
            "result_set_sha256": json_sha256(result_set),
        },
        "verification": {
            "manifest_ids_exact": True,
            "progress_ids_exact": True,
            "request_response_result_ids_exact": True,
            "generated_image_twin_and_source_prompt_hashes_match": True,
            "frozen_root_file_hashes_match": True,
            "frozen_root_file_hashes": frozen_hashes,
            "judgments_equal_deterministic_reaggregation": True,
            "response_observations_unmodified": True,
            "single_dated_gpt55_model_returned": True,
            "fixed_visual_anchors_exact": True,
            "target_or_twin_anchor_overlaps": 0,
        },
        "counts": {name: counter_dict(counter) for name, counter in counts.items()},
        "components": {
            component: {
                dimension: counter_dict(counter)
                for dimension, counter in dimensions.items()
            }
            for component, dimensions in component_counts.items()
        },
        "usage": {key: numeric_summary(values) for key, values in usage_metrics.items()},
        "latency": {key: numeric_summary(values) for key, values in latency_metrics.items()},
        "records": per_record,
    }
    atomic_json(output_path, summary)
    print(
        json.dumps(
            {
                "ok": True,
                "output": str(output_path),
                "output_sha256": file_sha256(output_path),
                "records": target_count,
                "returned_model": summary["run"]["returned_model"],
                "verdicts": summary["counts"]["verdict"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditError as error:
        print(json.dumps({"ok": False, "error": str(error)}), file=sys.stderr)
        raise SystemExit(1)
