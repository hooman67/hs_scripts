#!/usr/bin/env python3
"""Build an upload-ready fe-html report for natural-placement judge v2.

This script performs no model calls and no uploads. It reads the frozen v6 asset
manifest plus completed ``result.json`` files, writes the official fe-html
``data.json`` contract, and copies the vendored annotation viewer verbatim. The
printed query string preconfigures an editable Pass/Review/Fail question and
free-form comments for human review.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import parse_qs, urlencode


ROOT = Path(__file__).resolve().parent
DEFAULT_ASSETS = ROOT / "data" / "v6_assets.json"
DEFAULT_RESULTS_ROOT = ROOT / "runs" / "v6_batch_v1"
DEFAULT_OUTPUT = ROOT / "fe_reports"
DEFAULT_REGRESSION_ASSETS = ROOT / "data" / "regression_user_failures.json"
DEFAULT_REGRESSION_RESULTS_ROOT = ROOT / "runs" / "userfail_regression_v3"
DEFAULT_VISUAL_ANCHORS = ROOT / "data" / "visual_anchors.json"
DEFAULT_RESEARCHER_SPOT_CHECKS = ROOT / "data" / "researcher_spot_checks.json"
DEFAULT_REGRESSION_DIR = "user_feedback_regressions"
DEFAULT_TITLE = "HP V6 — Natural Placement Judge v2: Human Review"
VENDORED_VIEWER = Path(
    os.path.expanduser("~/.claude/scripts/fe_html/annotation_viewer.html")
)
GATEWAY = "https://foundry-aws-corp.adobe.io"

ID_KEYS = ("id", "asset_id", "evalset_item_id", "case_id", "record_id")
TARGET_URL_KEYS = (
    "generated_image_url",
    "scene_image_url",
    "target_image_url",
    "output_image_url",
    "generated_url",
    "scene_url",
    "target_url",
    "image_url",
    "asset_url",
)
TWIN_URL_KEYS = (
    "twin_image_url",
    "digital_twin_url",
    "product_image_url",
    "product_input_url",
    "reference_image_url",
    "twin_url",
    "product_url",
    "input_url",
)
PROMPT_KEYS = (
    "scene_prompt",
    "original_prompt",
    "user_prompt",
    "prompt",
)
PRODUCT_TYPE_KEYS = ("product_type", "type", "category", "device_type")
PRODUCT_NAME_KEYS = (
    "product_name",
    "product",
    "device_name",
    "device",
    "sku",
    "model_name",
)
BATCH_KEYS = ("batch", "dataset", "subset", "source", "collection", "split")
FEEDBACK_KEYS = (
    "human_feedback",
    "feedback",
    "feedback_text",
    "reviewer_feedback",
    "anchor_feedback",
    "expected_feedback",
)
EXPECTED_VERDICT_KEYS = (
    "expected_verdict",
    "human_verdict",
    "feedback_verdict",
    "ground_truth_verdict",
)
RUN_PROVENANCE_KEYS = (
    "protocol_version",
    "model_requested",
    "model_returned",
    "system_prompt_sha256",
    "schema_sha256",
    "scoring_sha256",
    "runner_sha256",
    "wire_schema_sha256",
)

QUESTION_WIRE = [
    {
        "text": (
            "Generated scene: natural-placement verdict "
            "(digital twin is product reference only)"
        ),
        "hard_check": False,
        "group": "Generated scene review",
        "comment_box": True,
        "rubric": {
            "key": "custom",
            "name": "Pass / Review / Fail",
            "options": [
                {"value": "pass", "label": "Pass", "tone": "good"},
                {"value": "review", "label": "Review", "tone": "neutral"},
                {"value": "fail", "label": "Fail", "tone": "bad"},
            ],
        },
    }
]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _nonempty(value: Any) -> bool:
    return value is not None and (not isinstance(value, str) or bool(value.strip()))


def _first_direct(record: Mapping[str, Any], keys: Sequence[str]) -> Any:
    lowered = {str(key).lower(): value for key, value in record.items()}
    for key in keys:
        value = lowered.get(key.lower())
        if _nonempty(value):
            return value
    return None


def _walk_mappings(value: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(value, Mapping):
        yield value
        for child in value.values():
            yield from _walk_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_mappings(child)


def find_value(record: Mapping[str, Any], keys: Sequence[str]) -> Any:
    """Find an exact-key value, preferring the top-level record over nested data."""
    direct = _first_direct(record, keys)
    if _nonempty(direct):
        return direct
    first = True
    for mapping in _walk_mappings(record):
        if first:
            first = False
            continue
        nested = _first_direct(mapping, keys)
        if _nonempty(nested):
            return nested
    return None


def _manifest_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = None
        for key in ("records", "assets", "cases", "items", "rows"):
            candidate = payload.get(key)
            if isinstance(candidate, list):
                records = candidate
                break
        if records is None:
            raise ValueError(
                "Asset manifest must be a list or contain records/assets/cases/items/rows"
            )
    else:
        raise ValueError("Asset manifest must contain a JSON list or object")
    if not all(isinstance(record, dict) for record in records):
        raise ValueError("Every asset-manifest record must be a JSON object")
    return records


def _manifest_expected_count(payload: Any) -> int | None:
    if not isinstance(payload, Mapping):
        return None
    value = _first_direct(
        payload,
        ("expected_count", "expected_rows", "asset_count", "record_count", "total"),
    )
    if value is None:
        counts = payload.get("counts")
        if isinstance(counts, Mapping):
            value = _first_direct(counts, ("records", "total", "expected_count"))
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("Manifest expected count must be an integer")
    try:
        count = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Manifest expected count is not an integer: {value!r}") from exc
    if count < 0:
        raise ValueError("Manifest expected count must be zero or positive")
    return count


def _manifest_product_count(payload: Any, product_type: str) -> int | None:
    if not isinstance(payload, Mapping):
        return None
    counts = payload.get("counts")
    by_type = counts.get("by_device_type") if isinstance(counts, Mapping) else None
    if not isinstance(by_type, Mapping) or product_type not in by_type:
        return None
    value = by_type[product_type]
    if isinstance(value, bool):
        raise ValueError(f"Manifest count for {product_type} must be an integer")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Manifest count for {product_type} is not an integer: {value!r}"
        ) from exc


def _record_id(record: Mapping[str, Any]) -> str:
    value = _first_direct(record, ID_KEYS)
    if not _nonempty(value):
        value = find_value(record, ID_KEYS)
    if not _nonempty(value):
        raise ValueError("Asset record is missing id/asset_id/evalset_item_id")
    return str(value).strip()


def _s3_to_gateway(uri: str) -> str:
    rest = uri[len("s3://") :]
    bucket, separator, key = rest.partition("/")
    if not bucket or not separator or not key:
        raise ValueError(f"Malformed S3 asset URI: {uri}")
    return f"{GATEWAY}/asset/{bucket}/{key}"


def asset_url(value: Any, *, asset_id: str, field: str) -> str:
    if isinstance(value, Mapping):
        value = _first_direct(value, ("url", "s3_url", "uri", "src", "image_src"))
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{asset_id}: missing {field} URL")
    value = value.strip()
    if value.startswith("s3://"):
        return _s3_to_gateway(value)
    if value.startswith(("https://", "http://")):
        return value
    raise ValueError(
        f"{asset_id}: {field} must be an http(s) or s3:// URL, got {value!r}"
    )


def _record_image_value(record: Mapping[str, Any], *, twin: bool) -> Any:
    """Resolve the verified v6 nested image records before legacy flat aliases."""
    container = record.get("twin_image" if twin else "generated_image")
    if isinstance(container, Mapping):
        keys = (
            (
                "source_public_url",
                "preview_public_url",
                "source_s3_uri",
                "preview_s3_uri",
                "public_url",
                "s3_uri",
                "url",
            )
            if twin
            else ("public_url", "s3_uri", "url")
        )
        value = _first_direct(container, keys)
        if _nonempty(value):
            return value
    return find_value(record, TWIN_URL_KEYS if twin else TARGET_URL_KEYS)


def _result_files(roots: Sequence[Path]) -> list[Path]:
    paths: set[Path] = set()
    for root in roots:
        if root.is_file():
            if root.name != "result.json":
                raise ValueError(f"Result file must be named result.json: {root}")
            paths.add(root.resolve())
        elif root.is_dir():
            paths.update(path.resolve() for path in root.rglob("result.json"))
        else:
            raise ValueError(f"Results root does not exist: {root}")
    return sorted(paths)


def _result_aliases(path: Path, result: Mapping[str, Any]) -> set[str]:
    aliases = {path.parent.name}
    for mapping in (result, result.get("input"), result.get("request")):
        if not isinstance(mapping, Mapping):
            continue
        value = _first_direct(mapping, ID_KEYS)
        if _nonempty(value):
            aliases.add(str(value).strip())
    return {alias for alias in aliases if alias}


def load_results(roots: Sequence[Path]) -> tuple[dict[str, dict[str, Any]], int]:
    by_alias: dict[str, tuple[Path, dict[str, Any]]] = {}
    files = _result_files(roots)
    if not files:
        raise ValueError(f"No result.json files found under: {', '.join(map(str, roots))}")
    for path in files:
        result = load_json(path)
        if not isinstance(result, dict):
            raise ValueError(f"Judge result must be a JSON object: {path}")
        for alias in _result_aliases(path, result):
            previous = by_alias.get(alias)
            if previous is not None and previous[0] != path:
                raise ValueError(
                    f"Ambiguous judge result alias {alias!r}: {previous[0]} and {path}"
                )
            by_alias[alias] = (path, result)
    return {alias: pair[1] for alias, pair in by_alias.items()}, len(files)


def _judgment(result: Mapping[str, Any], asset_id: str) -> Mapping[str, Any]:
    if result.get("ok") is False:
        raise ValueError(f"{asset_id}: judge result reports ok=false")
    value = result.get("judgment")
    if not isinstance(value, Mapping):
        # Accommodate runners that write the judgment fields at the top level.
        if any(key in result for key in ("verdict", "natural_placement_score", "score")):
            value = result
        else:
            raise ValueError(f"{asset_id}: result has no judgment object")
    return value


def _anchor_signature(
    examples: Any, *, asset_id: str
) -> tuple[tuple[str, str, str], ...]:
    if not isinstance(examples, list):
        raise ValueError(f"{asset_id}: visual-anchor examples must be a list")
    signature: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for example in examples:
        if not isinstance(example, Mapping):
            raise ValueError(f"{asset_id}: every visual anchor must be an object")
        values = tuple(
            str(example.get(key, "")).strip()
            for key in ("asset_id", "kind", "sha256")
        )
        if not all(values):
            raise ValueError(
                f"{asset_id}: visual anchor is missing asset_id/kind/sha256"
            )
        if values[0] in seen:
            raise ValueError(f"{asset_id}: duplicate visual anchor {values[0]!r}")
        seen.add(values[0])
        signature.append(values)
    return tuple(signature)


def _result_anchor_signature(
    result: Mapping[str, Any], *, asset_id: str
) -> tuple[tuple[str, str, str], ...]:
    visual_anchors = result.get("visual_anchors")
    examples = (
        visual_anchors.get("examples")
        if isinstance(visual_anchors, Mapping)
        else None
    )
    return _anchor_signature(examples, asset_id=asset_id)


def _consistent_result_value(
    selected: Sequence[tuple[str, Mapping[str, Any]]], key: str
) -> Any:
    values = [(asset_id, result.get(key)) for asset_id, result in selected]
    missing = [asset_id for asset_id, value in values if not _nonempty(value)]
    if missing:
        raise ValueError(f"Run results are missing {key}: {', '.join(missing[:8])}")
    canonical = values[0][1]
    different = [asset_id for asset_id, value in values if value != canonical]
    if different:
        raise ValueError(
            f"Run results disagree on {key}; first differing rows: "
            + ", ".join(different[:8])
        )
    return canonical


def validate_run_provenance(
    records: Sequence[Mapping[str, Any]],
    results: Mapping[str, Mapping[str, Any]],
    *,
    regression: bool,
    visual_anchors_path: Path = DEFAULT_VISUAL_ANCHORS,
) -> dict[str, Any]:
    """Validate one coherent judge run and derive its actual method metadata."""
    selected = [(_record_id(record), results[_record_id(record)]) for record in records]
    if not selected:
        raise ValueError("Cannot validate provenance for an empty report")

    provenance = {
        key: _consistent_result_value(selected, key) for key in RUN_PROVENANCE_KEYS
    }
    judgments = [(_id, _judgment(result, _id)) for _id, result in selected]
    for key in ("threshold_status", "policy_version"):
        provenance[key] = _consistent_result_value(judgments, key)

    enabled_values = {
        result.get("visual_anchors_enabled") for _, result in selected
    }
    if len(enabled_values) != 1 or enabled_values.pop() not in (True, False):
        raise ValueError(
            "Run results must consistently set visual_anchors_enabled to true or false"
        )
    enabled = selected[0][1].get("visual_anchors_enabled") is True
    provenance["visual_context_enabled"] = enabled
    if not enabled:
        for asset_id, result in selected:
            visual_anchors = result.get("visual_anchors")
            examples = (
                visual_anchors.get("examples")
                if isinstance(visual_anchors, Mapping)
                else None
            )
            if examples not in (None, []):
                raise ValueError(
                    f"{asset_id}: visual anchors are disabled but examples are present"
                )
        provenance.update(
            {
                "visual_context_mode": "disabled",
                "visual_examples_per_row": 0,
                "visual_example_union_size": 0,
                "visual_example_kind_counts": {},
                "visual_anchor_manifest_sha256": None,
            }
        )
        return provenance

    manifest_hash = _consistent_result_value(
        selected, "visual_anchor_manifest_sha256"
    )
    signatures = {
        asset_id: _result_anchor_signature(result, asset_id=asset_id)
        for asset_id, result in selected
    }
    union: dict[str, tuple[str, str, str]] = {}
    for signature in signatures.values():
        for item in signature:
            previous = union.get(item[0])
            if previous is not None and previous != item:
                raise ValueError(
                    f"Visual anchor {item[0]!r} has inconsistent kind/hash across rows"
                )
            union[item[0]] = item

    current_manifest_verified = False
    if visual_anchors_path.is_file() and sha256(visual_anchors_path) == manifest_hash:
        anchor_manifest = load_json(visual_anchors_path)
        manifest_signature = _anchor_signature(
            anchor_manifest.get("examples")
            if isinstance(anchor_manifest, Mapping)
            else None,
            asset_id=str(visual_anchors_path),
        )
        if set(manifest_signature) != set(union.values()):
            raise ValueError(
                "Embedded visual anchors do not match the recorded versioned manifest"
            )
        current_manifest_verified = True

    if regression:
        target_ids = {_record_id(record) for record in records}
        excluded_targets = target_ids.intersection(union)
        if excluded_targets and excluded_targets != target_ids:
            raise ValueError(
                "Regression visual context excludes exact targets inconsistently"
            )
        for asset_id, signature in signatures.items():
            expected = {
                item for anchor_id, item in union.items() if anchor_id != asset_id
            }
            if set(signature) != expected:
                raise ValueError(
                    f"{asset_id}: regression visual context is not the run union minus "
                    "the exact target"
                )
        mode = (
            "exact_target_excluded" if excluded_targets else "consistent_shared_set"
        )
    else:
        first_signature = next(iter(signatures.values()))
        different = [
            asset_id
            for asset_id, signature in signatures.items()
            if signature != first_signature
        ]
        if different:
            raise ValueError(
                "Standard report results use inconsistent visual contexts: "
                + ", ".join(different[:8])
            )
        mode = "consistent_shared_set"

    per_row_counts = {len(signature) for signature in signatures.values()}
    if len(per_row_counts) != 1:
        raise ValueError("Run results have inconsistent visual-example counts")
    kind_counts = Counter(item[1] for item in union.values())
    provenance.update(
        {
            "visual_context_mode": mode,
            "visual_examples_per_row": per_row_counts.pop(),
            "visual_example_union_size": len(union),
            "visual_example_kind_counts": dict(sorted(kind_counts.items())),
            "visual_anchor_manifest_sha256": manifest_hash,
            "visual_anchor_manifest_current": current_manifest_verified,
        }
    )
    return provenance


def _score(judgment: Mapping[str, Any]) -> Any:
    return find_value(
        judgment,
        ("natural_placement_score", "placement_score", "overall_score", "score"),
    )


def _verdict(judgment: Mapping[str, Any]) -> str:
    value = find_value(judgment, ("verdict", "decision", "label"))
    if not _nonempty(value):
        raise ValueError("Judgment is missing verdict")
    return str(value).strip()


def _string(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _score_is_100(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    try:
        return float(value) == 100.0
    except (TypeError, ValueError):
        return False


def _has_unobservable_component(observation: Any) -> bool:
    if not isinstance(observation, Mapping):
        return False
    components = observation.get("components")
    return isinstance(components, Mapping) and any(
        isinstance(component, Mapping)
        and str(component.get("visibility", "")).lower() == "unobservable"
        for component in components.values()
    )


def _evidence_text(judgment: Mapping[str, Any]) -> str:
    observation = judgment.get("observation")
    lines: list[str] = []
    verdict = _verdict(judgment).upper()
    score = _score(judgment)
    confidence = find_value(judgment, ("confidence", "overall_confidence"))
    coverage = find_value(judgment, ("coverage",))
    outcome = [f"Predicted verdict: {verdict}"]
    if _nonempty(score):
        outcome.append(f"Final score: {_string(score)}/100")
    if _nonempty(confidence):
        outcome.append(f"Confidence: {_string(confidence)}")
    if _nonempty(coverage):
        outcome.append(f"Coverage: {_string(coverage)}")
    lines.extend(("JUDGE RESULT", " · ".join(outcome), ""))
    if (
        verdict == "REVIEW"
        and _score_is_100(score)
        and _has_unobservable_component(observation)
    ):
        lines.extend(
            (
                "Score interpretation",
                "Score covers assessable components only; uncertainty prevents acceptance.",
                "",
            )
        )

    summary = None
    if isinstance(observation, Mapping):
        summary = find_value(observation, ("summary", "overall_summary"))
    if not _nonempty(summary):
        summary = find_value(judgment, ("summary", "rationale", "reasoning"))
    if _nonempty(summary):
        lines.extend(("Summary", _string(summary).strip(), ""))

    weighted_score = find_value(judgment, ("weighted_component_score",))
    score_cap = find_value(judgment, ("applied_score_cap",))
    if _nonempty(weighted_score) or _nonempty(score_cap):
        lines.append("Score calculation")
        if _nonempty(weighted_score):
            lines.append(f"Weighted component mean: {_string(weighted_score)}/100")
        if _nonempty(score_cap):
            lines.append(f"Applied score cap: {_string(score_cap)}/100")
            if _nonempty(weighted_score) and _nonempty(score):
                lines.append(
                    "Final score after cap: "
                    f"min({_string(weighted_score)}, {_string(score_cap)}) "
                    f"= {_string(score)}/100"
                )
        else:
            lines.append("Applied score cap: none")
        lines.append("")

    components = observation.get("components") if isinstance(observation, Mapping) else None
    if isinstance(components, Mapping):
        lines.append("Component evidence")
        for name, component in components.items():
            lines.append(f"\n{name}")
            if not isinstance(component, Mapping):
                lines.append(_string(component))
                continue
            for field in (
                "visibility",
                "severity",
                "confidence",
                "evidence",
                "consequence",
                "issue_codes",
            ):
                value = component.get(field)
                if _nonempty(value):
                    lines.append(f"{field}: {_string(value)}")

    direct_evidence = judgment.get("evidence")
    if _nonempty(direct_evidence):
        lines.extend(("", "Additional evidence", _string(direct_evidence)))

    reasons = judgment.get("verdict_reasons")
    if _nonempty(reasons):
        lines.extend(("", f"Verdict reasons: {_string(reasons)}"))

    changes = (
        observation.get("suggested_scene_changes")
        if isinstance(observation, Mapping)
        else None
    )
    if _nonempty(changes):
        lines.extend(("", "Suggested scene changes"))
        if isinstance(changes, list):
            lines.extend(f"- {_string(change)}" for change in changes)
        else:
            lines.append(_string(changes))

    scene_reading = (
        observation.get("scene_reading") if isinstance(observation, Mapping) else None
    )
    if isinstance(scene_reading, Mapping):
        lines.extend(("", "Detailed scene reading"))
        for field, value in scene_reading.items():
            if _nonempty(value):
                lines.append(f"{field}: {_string(value)}")
    elif _nonempty(scene_reading):
        lines.extend(("", "Detailed scene reading", _string(scene_reading).strip()))

    if not any(line.strip() for line in lines):
        # Preserve unknown v2 observation shapes rather than silently hiding evidence.
        fallback = observation if _nonempty(observation) else judgment
        return json.dumps(fallback, indent=2, ensure_ascii=False, sort_keys=True)
    return "\n".join(lines).strip()


def _component_scores(judgment: Mapping[str, Any]) -> str:
    scores = judgment.get("component_scores")
    if not isinstance(scores, Mapping):
        return ""
    return "; ".join(f"{name}={value}" for name, value in scores.items())


def _feedback_text(record: Mapping[str, Any]) -> str:
    value = find_value(record, FEEDBACK_KEYS)
    return _string(value).strip() if _nonempty(value) else ""


def load_researcher_spot_checks(path: Path | None) -> dict[str, str]:
    """Load optional display-only researcher questions keyed by exact asset ID."""
    if path is None or not path.is_file():
        return {}
    payload = load_json(path)
    if not isinstance(payload, Mapping) or not isinstance(payload.get("checks"), list):
        raise ValueError(f"Researcher spot checks must contain a checks list: {path}")
    checks: dict[str, str] = {}
    for index, item in enumerate(payload["checks"]):
        if not isinstance(item, Mapping):
            raise ValueError(f"Researcher spot check {index} must be an object: {path}")
        asset_id = item.get("id")
        question = item.get("researcher_question")
        if not isinstance(asset_id, str) or not asset_id.strip():
            raise ValueError(f"Researcher spot check {index} has no ID: {path}")
        if not isinstance(question, str) or not question.strip():
            raise ValueError(
                f"Researcher spot check {asset_id} has no researcher_question: {path}"
            )
        asset_id = asset_id.strip()
        if asset_id in checks:
            raise ValueError(f"Duplicate researcher spot check ID {asset_id}: {path}")
        checks[asset_id] = question.strip()
    return checks


def _meta_value(record: Mapping[str, Any], keys: Sequence[str], default: str = "") -> str:
    value = find_value(record, keys)
    return _string(value).strip() if _nonempty(value) else default


def make_row(
    record: Mapping[str, Any],
    result: Mapping[str, Any],
    row_idx: int,
    researcher_question: str | None = None,
) -> tuple[dict[str, Any], str]:
    asset_id = _record_id(record)
    target = asset_url(
        _record_image_value(record, twin=False),
        asset_id=asset_id,
        field="target scene image",
    )
    twin = asset_url(
        _record_image_value(record, twin=True),
        asset_id=asset_id,
        field="digital twin image",
    )
    judgment = _judgment(result, asset_id)
    score = _score(judgment)
    verdict = _verdict(judgment)
    observation = judgment.get("observation")
    judge_summary = ""
    if isinstance(observation, Mapping):
        judge_summary = _meta_value(observation, ("summary", "overall_summary"))
    if not judge_summary:
        judge_summary = _meta_value(judgment, ("summary", "rationale", "reasoning"))

    prompt = _meta_value(record, PROMPT_KEYS)
    if not prompt:
        input_record = result.get("input")
        if isinstance(input_record, Mapping):
            prompt = _meta_value(input_record, PROMPT_KEYS)
    if not prompt:
        raise ValueError(f"{asset_id}: missing original scene prompt")

    product_type = _meta_value(record, PRODUCT_TYPE_KEYS, "unknown")
    product_name = _meta_value(record, PRODUCT_NAME_KEYS)
    batch = _meta_value(record, BATCH_KEYS, product_type)
    feedback = _feedback_text(record)
    expected_verdict = _meta_value(record, EXPECTED_VERDICT_KEYS)
    expected_issue_codes = find_value(record, ("expected_issue_codes",))
    regression_expectation = record.get("regression_expectation")
    passed_to_judge = None
    if isinstance(regression_expectation, Mapping):
        passed_to_judge = regression_expectation.get("passed_to_judge")

    visual_context_enabled = result.get("visual_anchors_enabled") is True
    visual_example_count = (
        len(_result_anchor_signature(result, asset_id=asset_id))
        if visual_context_enabled
        else 0
    )
    meta: dict[str, Any] = {
        "Dataset / batch": batch,
        "Product type": product_type,
        "Original scene prompt": prompt,
        "Judge v2 predicted verdict": verdict,
        "Judge development visual context": (
            f"Enabled ({visual_example_count} examples)"
            if visual_context_enabled
            else "Disabled"
        ),
    }
    if product_name:
        meta["Product"] = product_name
    device = _meta_value(record, ("device", "device_id"))
    if device:
        meta["Device"] = device
    candidate = _meta_value(record, ("candidate_id",))
    if candidate:
        meta["V6 candidate"] = candidate
    view = record.get("view")
    if isinstance(view, Mapping):
        camera = _meta_value(view, ("camera_tag", "source_camera_name"))
        if camera:
            meta["Camera"] = camera
        view_role = _meta_value(view, ("view_role",))
        if view_role:
            meta["View role"] = view_role
    prompt_source = record.get("scene_prompt_source")
    if isinstance(prompt_source, Mapping):
        environment = _meta_value(prompt_source, ("environment",))
        if environment:
            meta["Environment"] = environment
    if score is not None:
        meta["Judge score"] = score
    weighted_score = find_value(judgment, ("weighted_component_score",))
    if _nonempty(weighted_score):
        meta["Judge weighted component score"] = weighted_score
    score_cap = find_value(judgment, ("applied_score_cap",))
    if _nonempty(score_cap):
        meta["Judge applied score cap"] = score_cap
    confidence = find_value(judgment, ("confidence", "overall_confidence"))
    if _nonempty(confidence):
        meta["Judge confidence"] = confidence
    coverage = find_value(judgment, ("coverage",))
    if _nonempty(coverage):
        meta["Judge coverage"] = coverage
    component_scores = _component_scores(judgment)
    if component_scores:
        meta["Judge component scores"] = component_scores
    if judge_summary:
        meta["Judge evidence summary"] = judge_summary
    if expected_verdict:
        meta["Known human verdict (historical reference)"] = expected_verdict
    if feedback:
        meta["Known human feedback (historical reference)"] = feedback
    if _nonempty(expected_issue_codes):
        meta["Known human issue codes (historical reference)"] = _string(
            expected_issue_codes
        )
    if passed_to_judge is not None:
        meta["Historical human label passed to judge"] = (
            "Yes" if bool(passed_to_judge) else "No"
        )
    threshold_status = find_value(judgment, ("threshold_status",))
    if _nonempty(threshold_status):
        meta["Judge policy status"] = threshold_status
    policy_version = find_value(judgment, ("policy_version",))
    if _nonempty(policy_version):
        meta["Judge policy version"] = policy_version

    evidence = _evidence_text(judgment)
    generated_scene_meta = {
        "label": "Generated scene — review this image",
        "Judge predicted verdict": verdict.upper(),
    }
    if _nonempty(score):
        generated_scene_meta["Judge final score"] = f"{_string(score)}/100"
    images: list[dict[str, Any]] = [
        {
            "asset_type": "image",
            "is_model_input_or_output": "model_output",
            "image_src": target,
            "meta_text": generated_scene_meta,
        },
        {
            "asset_type": "image",
            "is_model_input_or_output": "model_input",
            "image_src": twin,
            "meta_text": {
                "label": "Digital twin — product reference only; do not rate"
            },
        },
    ]
    if feedback:
        images.append(
            {
                "asset_type": "text",
                "text_content": feedback,
                "meta_text": {
                    "label": "Known human feedback — historical reference, not a review answer"
                },
            }
        )
    if researcher_question:
        images.append(
            {
                "asset_type": "text",
                "text_content": researcher_question,
                "meta_text": {
                    "label": "Researcher review question (not a human label)"
                },
            }
        )
    images.append(
        {
            "asset_type": "text",
            "text_content": evidence,
            "meta_text": {"label": "Judge v2 evidence and rationale"},
        }
    )

    return (
        {
            "meta_data": {
                "row_idx": row_idx,
                "evalset_item_id": asset_id,
                "key_val_informations": meta,
            },
            "images": images,
        },
        batch,
    )


def review_query(ldap: str = "hshariati") -> str:
    encoded = base64.b64encode(
        json.dumps(QUESTION_WIRE, ensure_ascii=False, separators=(",", ":")).encode(
            "utf-8"
        )
    ).decode("ascii")
    return "?" + urlencode({"ldap": ldap, "q": encoded})


def validate_review_query(query: str, ldap: str) -> None:
    """Verify the query against the viewer's exact ``atob`` + JSON wire contract."""
    try:
        parsed = parse_qs(query.removeprefix("?"), strict_parsing=True)
        if set(parsed) != {"ldap", "q"} or parsed["ldap"] != [ldap]:
            raise ValueError("review query does not contain exactly one expected LDAP and q")
        decoded = json.loads(base64.b64decode(parsed["q"][0], validate=True))
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid fe-html review query: {exc}") from exc
    if decoded != QUESTION_WIRE:
        raise ValueError("fe-html review query does not round-trip to the configured rubric")


def _visual_context_description(provenance: Mapping[str, Any]) -> str:
    if not provenance["visual_context_enabled"]:
        return "Disabled for this run"
    per_row = provenance["visual_examples_per_row"]
    union_size = provenance["visual_example_union_size"]
    mode = provenance["visual_context_mode"]
    if mode == "exact_target_excluded":
        return (
            f"{per_row} development examples per row from a {union_size}-example run "
            "union; each exact regression target was excluded from its own judge call"
        )
    return f"One consistent set of {per_row} development examples per row"


def _visual_kind_description(provenance: Mapping[str, Any]) -> str:
    counts = provenance.get("visual_example_kind_counts") or {}
    if not counts:
        return "None"
    return "; ".join(f"{kind}={count}" for kind, count in counts.items())


def _report_context_notes(
    manifest: Any, regression: bool, provenance: Mapping[str, Any]
) -> list[Any]:
    run_note = [
        "Judge run provenance",
        {
            "Model requested": provenance["model_requested"],
            "Model returned": provenance["model_returned"],
            "Protocol": provenance["protocol_version"],
            "System prompt SHA-256": provenance["system_prompt_sha256"],
            "Scoring SHA-256": provenance["scoring_sha256"],
            "Visual context": _visual_context_description(provenance),
            "Visual example kinds in run union": _visual_kind_description(provenance),
            "Policy version": provenance["policy_version"],
            "Threshold status": provenance["threshold_status"],
            "Score interpretation": (
                "Scores cover assessable components only; unobservable components are "
                "excluded from the weighted mean. Uncertainty can still prevent acceptance "
                "even when the assessable-component score is 100."
            ),
        },
    ]
    if regression:
        return [
            [
                "Regression method",
                {
                    "Purpose": "Four historical user-feedback development regressions",
                    "Known human labels": (
                        "Displayed as historical reference only; they do not pre-populate "
                        "this review form"
                    ),
                    "Judge inputs": (
                        "Scene image, digital twin, product type, original scene prompt, and the "
                        "development visual context recorded below; human feedback for the "
                        "evaluated row was not passed to the judge"
                    ),
                    "Evaluation status": (
                        "Training/development examples used to validate distilled rules; "
                        "not a held-out evaluation"
                    ),
                    "Policy status": "Provisional and not yet human-calibrated",
                },
            ],
            run_note,
        ]

    coverage = manifest.get("coverage") if isinstance(manifest, Mapping) else None
    approved = (
        coverage.get("approved_v6_prompt_count")
        if isinstance(coverage, Mapping)
        else None
    )
    published = (
        coverage.get("published_preview_count")
        if isinstance(coverage, Mapping)
        else None
    )
    if approved is not None and published is not None:
        coverage_text = (
            f"{published} of {approved} approved V6 prompts have images in the verified "
            "published preview; this report covers those published examples"
        )
    else:
        coverage_text = "Covers the records in the verified input manifest"
    return [
        [
            "Evaluation context",
            {
                "Coverage": coverage_text,
                "Policy status": "Provisional and not yet human-calibrated",
                "Rule-design examples": (
                    "Four historical user-feedback cases informed offline rule design; "
                    "they are training/development examples, not held-out evaluation cases"
                ),
                "Runtime judge inputs": (
                    "Scene image, digital twin, product type, original scene prompt, and the "
                    "development visual context recorded below; no label for the evaluated case"
                ),
            },
        ],
        run_note,
    ]


def build_report(
    *,
    assets_path: Path,
    results_roots: Sequence[Path],
    output_dir: Path,
    title: str,
    expected_rows: int | None,
    ldap: str,
    product_type: str | None = None,
    regression: bool = False,
    visual_anchors_path: Path = DEFAULT_VISUAL_ANCHORS,
    researcher_spot_checks_path: Path | None = DEFAULT_RESEARCHER_SPOT_CHECKS,
) -> dict[str, Any]:
    manifest = load_json(assets_path)
    records = _manifest_records(manifest)
    manifest_expected = _manifest_expected_count(manifest)
    count_gate = expected_rows if expected_rows is not None else manifest_expected
    ids = [_record_id(record) for record in records]
    duplicate_ids = sorted(asset_id for asset_id, n in Counter(ids).items() if n > 1)
    if duplicate_ids:
        raise ValueError(f"Duplicate asset IDs: {', '.join(duplicate_ids)}")
    if count_gate is not None and len(records) != count_gate:
        raise ValueError(
            f"Expected {count_gate} asset rows, found {len(records)} in {assets_path}"
        )
    source_row_count = len(records)
    if product_type is not None:
        records = [
            record
            for record in records
            if _meta_value(record, PRODUCT_TYPE_KEYS).lower() == product_type.lower()
        ]
        ids = [_record_id(record) for record in records]
        expected_product_count = _manifest_product_count(manifest, product_type)
        if expected_product_count is not None and len(records) != expected_product_count:
            raise ValueError(
                f"Expected {expected_product_count} {product_type} rows, found {len(records)}"
            )
        if not records:
            raise ValueError(f"Manifest contains no {product_type} rows")

    researcher_spot_checks = load_researcher_spot_checks(
        researcher_spot_checks_path
    )
    matched_researcher_questions = {
        asset_id: researcher_spot_checks[asset_id]
        for asset_id in ids
        if asset_id in researcher_spot_checks
    }

    results, result_file_count = load_results(results_roots)
    missing = [asset_id for asset_id in ids if asset_id not in results]
    if missing:
        preview = ", ".join(missing[:12])
        suffix = " ..." if len(missing) > 12 else ""
        raise ValueError(f"Missing judge results for {len(missing)} assets: {preview}{suffix}")
    provenance = validate_run_provenance(
        records,
        results,
        regression=regression,
        visual_anchors_path=visual_anchors_path,
    )

    rows: list[dict[str, Any]] = []
    batches: Counter[str] = Counter()
    verdicts: Counter[str] = Counter()
    for row_idx, record in enumerate(records, start=1):
        asset_id = ids[row_idx - 1]
        row, batch = make_row(
            record,
            results[asset_id],
            row_idx,
            researcher_question=matched_researcher_questions.get(asset_id),
        )
        rows.append(row)
        batches[batch] += 1
        verdict = row["meta_data"]["key_val_informations"][
            "Judge v2 predicted verdict"
        ]
        verdicts[str(verdict)] += 1

    if not VENDORED_VIEWER.is_file():
        raise ValueError(f"Vendored annotation viewer not found: {VENDORED_VIEWER}")
    if not title.strip():
        raise ValueError("Report title must be nonempty")
    if not ldap.strip():
        raise ValueError("Reviewer LDAP must be nonempty")

    data = {
        "is_secure": True,
        "meta_texts": [
            title.strip(),
            *_report_context_notes(manifest, regression, provenance),
            *(
                [
                    [
                        "Researcher spot checks",
                        {
                            "Questions displayed": len(matched_researcher_questions),
                            "Status": (
                                "Display-only researcher review questions; not human labels, "
                                "not review answers, and no judge result was edited"
                            ),
                        },
                    ]
                ]
                if matched_researcher_questions
                else []
            ),
            ["Review scope", {"Rows": len(rows), **dict(sorted(batches.items()))}],
            ["Judge verdicts", dict(sorted(verdicts.items()))],
            [
                "Human annotation",
                {
                    "Review target": (
                        "Only the generated scene image; the digital twin is product reference "
                        "and must not receive a verdict"
                    ),
                    "Question": QUESTION_WIRE[0]["text"],
                    "Options": "Pass / Review / Fail",
                    "Comments": "Per-question and overall free-form comments enabled",
                    "Comment guidance": (
                        "For Review or Fail, note the primary dimension when useful: alignment, "
                        "reach/access, support, scale, contact, or narrative"
                    ),
                },
            ],
        ],
        "rows": rows,
    }

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}-", dir=output_dir.parent))
    try:
        (temporary / "data.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        shutil.copyfile(VENDORED_VIEWER, temporary / "viewer.html")
        output_dir.mkdir(parents=True, exist_ok=True)
        os.replace(temporary / "data.json", output_dir / "data.json")
        os.replace(temporary / "viewer.html", output_dir / "viewer.html")
    finally:
        shutil.rmtree(temporary, ignore_errors=True)

    query = review_query(ldap.strip())
    validate_review_query(query, ldap.strip())
    summary = {
        "title": title.strip(),
        "rows": len(rows),
        "scope": "regression" if regression else (product_type or "combined"),
        "source_rows": source_row_count,
        "batches": dict(sorted(batches.items())),
        "judge_verdicts": dict(sorted(verdicts.items())),
        "result_files_discovered": result_file_count,
        "researcher_spot_checks_displayed": len(matched_researcher_questions),
        "source_expected_rows": count_gate,
        "run_provenance": provenance,
        "output_dir": str(output_dir.resolve()),
        "data_json": str((output_dir / "data.json").resolve()),
        "viewer_html": str((output_dir / "viewer.html").resolve()),
        "viewer_sha256": sha256(output_dir / "viewer.html"),
        "review_query": query,
    }
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    parser.add_argument(
        "--results-root",
        type=Path,
        action="append",
        dest="results_roots",
        help="Directory containing result.json files; repeat for multiple run roots",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Root for combined/, laptops/, and printers/ report directories",
    )
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument(
        "--expected-rows",
        type=int,
        default=None,
        help="Override the manifest's expected-count completeness gate",
    )
    parser.add_argument("--ldap", default="hshariati")
    parser.add_argument(
        "--visual-anchors",
        type=Path,
        default=DEFAULT_VISUAL_ANCHORS,
        help="Current versioned visual-anchor manifest for provenance verification",
    )
    parser.add_argument(
        "--researcher-spot-checks",
        type=Path,
        default=DEFAULT_RESEARCHER_SPOT_CHECKS,
        help=(
            "Optional display-only researcher questions; a missing file is ignored and "
            "questions never alter judge results or human review answers"
        ),
    )
    parser.add_argument(
        "--separate-four",
        nargs="?",
        const=DEFAULT_REGRESSION_DIR,
        default=None,
        metavar="OUTPUT_DIR",
        help=(
            "also build the four historical user-feedback regressions; optionally "
            "set their output directory (relative paths are under --output-dir)"
        ),
    )
    parser.add_argument(
        "--regression-assets", type=Path, default=DEFAULT_REGRESSION_ASSETS
    )
    parser.add_argument(
        "--regression-results-root",
        type=Path,
        default=DEFAULT_REGRESSION_RESULTS_ROOT,
    )
    parser.add_argument(
        "--regression-only",
        action="store_true",
        help="build only the separate four-case regression report",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.expected_rows is not None and args.expected_rows < 0:
        raise SystemExit("--expected-rows must be zero or positive")
    roots = args.results_roots or [DEFAULT_RESULTS_ROOT]
    try:
        output_root = args.output_dir.resolve()
        summaries = []
        if not args.regression_only:
            for directory, product_type, title_suffix in (
                ("combined", None, ""),
                ("laptops", "laptop", " — Laptops"),
                ("printers", "printer", " — Printers"),
            ):
                summaries.append(
                    build_report(
                        assets_path=args.assets.resolve(),
                        results_roots=[path.resolve() for path in roots],
                        output_dir=output_root / directory,
                        title=args.title + title_suffix,
                        expected_rows=args.expected_rows,
                        ldap=args.ldap,
                        product_type=product_type,
                        visual_anchors_path=args.visual_anchors.resolve(),
                        researcher_spot_checks_path=args.researcher_spot_checks.resolve(),
                    )
                )
        if args.separate_four is not None or args.regression_only:
            regression_output = Path(args.separate_four or DEFAULT_REGRESSION_DIR)
            if not regression_output.is_absolute():
                regression_output = output_root / regression_output
            summaries.append(
                build_report(
                    assets_path=args.regression_assets.resolve(),
                    results_roots=[args.regression_results_root.resolve()],
                    output_dir=regression_output.resolve(),
                    title=(
                        args.title
                        + " — Four User-Feedback Development Regressions"
                    ),
                    expected_rows=None,
                    ldap=args.ldap,
                    product_type=None,
                    regression=True,
                    visual_anchors_path=args.visual_anchors.resolve(),
                    researcher_spot_checks_path=args.researcher_spot_checks.resolve(),
                )
            )
    except ValueError as exc:
        raise SystemExit(f"error: {exc}") from exc
    print(json.dumps({"reports": summaries}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
