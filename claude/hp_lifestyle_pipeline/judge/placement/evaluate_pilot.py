"""Evaluate placement issue detection against the sparse pilot comment labels.

The evaluation unit is one manual placement-comment segment. This script does
not infer negative labels, severity labels, pass/fail calibration, or
false-positive statistics from the annotation set.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence


ROOT = Path(__file__).resolve().parent
COMPONENT_NAMES = (
    "support_scenario",
    "access_usability",
    "orientation_alignment",
    "scale_perspective",
    "contact_integration",
)
TARGET_VARIANTS = {"V13 final": "v13", "V14 final": "v14"}
RESULT_STATUSES = ("ok", "missing", "failed", "invalid")


class EvaluationInputError(ValueError):
    """The label, split, or run data violates the evaluator contract."""


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationInputError(f"Could not read valid JSON: {path}") from exc


def _validate_run_name(run: str) -> None:
    if not run or Path(run).name != run or run in {".", ".."}:
        raise EvaluationInputError("--run must be one directory name")


def _run_uses_visual_anchors(run_dir: Path) -> bool:
    """Infer the immutable request mode from stored request/result records."""

    flags = set()
    for case_dir in run_dir.iterdir() if run_dir.is_dir() else ():
        if not case_dir.is_dir():
            continue
        for name in ("request.json", "result.json"):
            path = case_dir / name
            if not path.is_file():
                continue
            document = _read_json(path)
            if not isinstance(document, dict):
                continue
            explicit = document.get("visual_anchors_enabled")
            if explicit is not None:
                if not isinstance(explicit, bool):
                    raise EvaluationInputError(
                        f"Invalid visual_anchors_enabled value: {path}"
                    )
                flags.add(explicit)
            else:
                # Backward compatibility for pre-hardening anchored records.
                flags.add("visual_anchors" in document)
    if len(flags) > 1:
        raise EvaluationInputError(
            "Run mixes anchored and unanchored request records"
        )
    return flags == {True}


def _development_anchor_rows(
    root: Path, split_document: Mapping[str, Any]
) -> set[int]:
    manifest = _read_json(root / "data" / "visual_anchors.json")
    examples = manifest.get("examples") if isinstance(manifest, dict) else None
    cases = split_document.get("cases")
    if not isinstance(examples, list) or not isinstance(cases, list):
        raise EvaluationInputError("Visual-anchor or split manifest is invalid")
    cases_by_id = {
        case.get("id"): case for case in cases if isinstance(case, dict)
    }
    rows = set()
    for anchor in examples:
        if not isinstance(anchor, dict):
            raise EvaluationInputError("Visual-anchor record is invalid")
        if anchor.get("kind") != "development_human_defect_anchor":
            continue
        case = cases_by_id.get(anchor.get("asset_id"))
        if not isinstance(case, dict) or case.get("split") != "development":
            raise EvaluationInputError(
                "Development demonstration does not map to a development case"
            )
        row = case.get("row")
        if not isinstance(row, int):
            raise EvaluationInputError("Development demonstration has no row")
        rows.add(row)
    if len(rows) != 3:
        raise EvaluationInputError(
            "Expected exactly three development demonstration rows"
        )
    return rows


def _prediction_from_result(result: Any) -> Dict[str, Any]:
    """Extract only fields needed for issue detection from a successful result."""

    if not isinstance(result, dict):
        raise EvaluationInputError("result root is not an object")
    if result.get("ok") is not True:
        raise EvaluationInputError("result is not successful")
    judgment = result.get("judgment")
    if not isinstance(judgment, dict):
        raise EvaluationInputError("successful result has no judgment object")
    observation = judgment.get("observation")
    if not isinstance(observation, dict):
        raise EvaluationInputError("judgment has no observation object")
    components = observation.get("components")
    if not isinstance(components, dict):
        raise EvaluationInputError("observation has no components object")

    prediction_components: Dict[str, Any] = {}
    for name in COMPONENT_NAMES:
        component = components.get(name)
        if not isinstance(component, dict):
            raise EvaluationInputError(f"missing prediction component: {name}")
        severity = component.get("severity")
        confidence = component.get("confidence")
        issue_codes = component.get("issue_codes")
        if not (
            severity is None
            or (isinstance(severity, int) and not isinstance(severity, bool) and 0 <= severity <= 4)
        ):
            raise EvaluationInputError(f"invalid predicted severity: {name}")
        if confidence not in {"high", "medium", "low"}:
            raise EvaluationInputError(f"invalid predicted confidence: {name}")
        if not (
            isinstance(issue_codes, list)
            and all(isinstance(code, str) for code in issue_codes)
        ):
            raise EvaluationInputError(f"invalid predicted issue codes: {name}")
        prediction_components[name] = {
            "severity": severity,
            "confidence": confidence,
            "issue_codes": list(issue_codes),
        }

    return {"components": prediction_components}


def _load_candidate_result(run_dir: Path, case: Mapping[str, Any]) -> Dict[str, Any]:
    result_path = run_dir / str(case["id"]) / "result.json"
    candidate = {
        "id": case["id"],
        "row": case["row"],
        "variant": case["variant"],
        "result_path": str(result_path),
    }
    if not result_path.is_file():
        return {**candidate, "status": "missing"}

    try:
        result = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {**candidate, "status": "invalid", "invalid_reason": "unreadable_json"}

    if not isinstance(result, dict):
        return {**candidate, "status": "invalid", "invalid_reason": "non_object_result"}
    if result.get("ok") is False:
        failed = {**candidate, "status": "failed"}
        if isinstance(result.get("error_type"), str):
            failed["error_type"] = result["error_type"]
        return failed
    if result.get("ok") is not True:
        return {**candidate, "status": "invalid", "invalid_reason": "missing_ok_status"}

    try:
        prediction = _prediction_from_result(result)
    except EvaluationInputError:
        return {**candidate, "status": "invalid", "invalid_reason": "invalid_judgment"}
    return {**candidate, "status": "ok", "prediction": prediction}


def _select_cases_for_label(
    label: Mapping[str, Any], cases_by_row: Mapping[int, Sequence[Mapping[str, Any]]]
) -> tuple[str, List[Mapping[str, Any]]]:
    targets = label.get("target_variant_labels")
    if not isinstance(targets, list) or len(targets) != 1:
        raise EvaluationInputError(
            f"Label must contain exactly one target marker: {label.get('record')}"
        )
    row = label.get("row")
    row_cases = list(cases_by_row.get(row, ()))
    if not row_cases:
        raise EvaluationInputError(f"No split case found for label row {row}")

    target = targets[0]
    if target == "comparison_set":
        if label.get("attribution_eligible") is not False:
            raise EvaluationInputError(
                f"Comparison-set label marked attribution eligible: {label.get('record')}"
            )
        return "comparison_set", sorted(row_cases, key=lambda case: case["id"])

    variant = TARGET_VARIANTS.get(target)
    if variant is None:
        raise EvaluationInputError(f"Unknown target variant label: {target}")
    selected = [case for case in row_cases if case.get("variant") == variant]
    if len(selected) != 1:
        raise EvaluationInputError(
            f"Expected one {variant} case at row {row}, found {len(selected)}"
        )
    expected_id = f"comparison-row-{row:02d}-{variant}"
    if selected[0].get("id") != expected_id:
        raise EvaluationInputError(
            f"Exact target id mismatch at row {row}: expected {expected_id}"
        )
    if label.get("attribution_eligible") is not True:
        raise EvaluationInputError(
            f"Exact-target label is not attribution eligible: {label.get('record')}"
        )
    return "exact_target", selected


def _positive_prediction(component: Mapping[str, Any]) -> bool:
    severity = component["severity"]
    return severity is not None and severity >= 1


def _assess_label(
    label: Mapping[str, Any], target_type: str, candidates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    expected_codes = label.get("expected_issue_codes")
    acceptable_components = label.get("acceptable_components")
    if not (
        isinstance(expected_codes, list)
        and expected_codes
        and all(isinstance(code, str) for code in expected_codes)
    ):
        raise EvaluationInputError(f"Invalid expected issue codes: {label.get('record')}")
    if not (
        isinstance(acceptable_components, list)
        and acceptable_components
        and all(component in COMPONENT_NAMES for component in acceptable_components)
    ):
        raise EvaluationInputError(f"Invalid acceptable components: {label.get('record')}")

    any_code_detection = False
    any_component_detection = False
    matched_codes_across_candidates = set()
    matched_components_across_candidates = set()
    output_candidates: List[Dict[str, Any]] = []
    for candidate in candidates:
        output_candidate = dict(candidate)
        if candidate["status"] == "ok":
            components = candidate["prediction"]["components"]
            positive_components = {
                name: component
                for name, component in components.items()
                if _positive_prediction(component)
            }
            predicted_codes = {
                code
                for component in positive_components.values()
                for code in component["issue_codes"]
            }
            matched_codes = sorted(set(expected_codes) & predicted_codes)
            matched_components = sorted(
                set(acceptable_components) & set(positive_components)
            )
            matched_codes_across_candidates.update(matched_codes)
            matched_components_across_candidates.update(matched_components)
            any_code_detection = any_code_detection or bool(matched_codes)
            any_component_detection = any_component_detection or bool(matched_components)
        output_candidates.append(output_candidate)

    all_candidates_ok = all(candidate["status"] == "ok" for candidate in candidates)

    def outcome(detected: bool) -> str:
        if detected:
            return "detected"
        if all_candidates_ok:
            return "not_detected"
        return "not_assessable"

    unavailable = [
        {"id": candidate["id"], "status": candidate["status"]}
        for candidate in candidates
        if candidate["status"] != "ok"
    ]
    return {
        "record": label["record"],
        "row": label["row"],
        "split": label["split"],
        # Copy verbatim. Do not normalize, tokenize, or reconstruct the quote.
        "exact_quote": label["exact_quote"],
        "target_type": target_type,
        "target_variant_labels": list(label["target_variant_labels"]),
        "target_basis": label["target_basis"],
        "expected_issue_codes": list(expected_codes),
        "acceptable_components": list(acceptable_components),
        "judgment_availability": (
            "complete" if all_candidates_ok else "incomplete"
        ),
        "unavailable_judgments": unavailable,
        "expected_issue_code_detection": outcome(any_code_detection),
        "matched_expected_issue_codes": sorted(matched_codes_across_candidates),
        "acceptable_component_detection": outcome(any_component_detection),
        "matched_acceptable_components": sorted(
            matched_components_across_candidates
        ),
        "candidates": output_candidates,
    }


def _count_outcomes(records: Iterable[Mapping[str, Any]], field: str) -> Dict[str, int]:
    records = list(records)
    counts = {name: sum(record[field] == name for record in records) for name in (
        "detected",
        "not_detected",
        "not_assessable",
    )}
    counts["assessed_denominator"] = counts["detected"] + counts["not_detected"]
    counts["total_label_denominator"] = len(records)
    return counts


def _metrics(records: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    candidates = [candidate for record in records for candidate in record["candidates"]]
    status_counts = {
        status: sum(candidate["status"] == status for candidate in candidates)
        for status in RESULT_STATUSES
    }
    status_counts["required_candidate_judgments"] = len(candidates)

    return {
        "label_units": {
            "total": len(records),
            "exact_target": sum(record["target_type"] == "exact_target" for record in records),
            "comparison_set": sum(record["target_type"] == "comparison_set" for record in records),
        },
        "judgment_availability": {
            "labels_complete": sum(
                record["judgment_availability"] == "complete" for record in records
            ),
            "labels_incomplete": sum(
                record["judgment_availability"] == "incomplete" for record in records
            ),
            "labels_affected_by_missing_judgment": sum(
                any(item["status"] == "missing" for item in record["unavailable_judgments"])
                for record in records
            ),
            "labels_affected_by_failed_judgment": sum(
                any(item["status"] == "failed" for item in record["unavailable_judgments"])
                for record in records
            ),
            "labels_affected_by_invalid_judgment": sum(
                any(item["status"] == "invalid" for item in record["unavailable_judgments"])
                for record in records
            ),
            "candidate_judgments": status_counts,
        },
        "expected_issue_code_detection": _count_outcomes(
            records, "expected_issue_code_detection"
        ),
        "acceptable_component_detection": _count_outcomes(
            records, "acceptable_component_detection"
        ),
    }


def evaluate(
    run: str,
    split_name: str,
    *,
    root: Path = ROOT,
) -> Dict[str, Any]:
    """Evaluate one stored run and return a JSON-serializable report."""

    _validate_run_name(run)
    if split_name not in {"development", "held_out", "all"}:
        raise EvaluationInputError(f"Unknown split: {split_name}")

    labels_path = root / "data" / "pilot_labels.json"
    split_path = root / "data" / "split.json"
    run_dir = root / "runs" / run
    labels_document = _read_json(labels_path)
    split_document = _read_json(split_path)
    if not isinstance(labels_document, dict) or not isinstance(labels_document.get("labels"), list):
        raise EvaluationInputError("pilot_labels.json has no labels array")
    if not isinstance(split_document, dict) or not isinstance(split_document.get("cases"), list):
        raise EvaluationInputError("split.json has no cases array")

    selected_splits = (
        {"development", "held_out"} if split_name == "all" else {split_name}
    )
    visual_anchors_enabled = _run_uses_visual_anchors(run_dir)
    labels = [
        label
        for label in labels_document["labels"]
        if isinstance(label, dict) and label.get("split") in selected_splits
    ]
    excluded_demonstration_labels = []
    if visual_anchors_enabled and "development" in selected_splits:
        demonstration_rows = _development_anchor_rows(root, split_document)
        retained_labels = []
        for label in labels:
            if (
                label.get("split") == "development"
                and label.get("row") in demonstration_rows
            ):
                excluded_demonstration_labels.append(
                    {
                        **label,
                        "exclusion_reason": (
                            "The comparison row is a development visual demonstration "
                            "included in this run's request context."
                        ),
                    }
                )
            else:
                retained_labels.append(label)
        labels = retained_labels
    cases = [
        case
        for case in split_document["cases"]
        if isinstance(case, dict) and case.get("split") in selected_splits
    ]
    cases_by_row: Dict[int, List[Mapping[str, Any]]] = {}
    for case in cases:
        row = case.get("row")
        if not isinstance(row, int):
            raise EvaluationInputError("split case has invalid row")
        cases_by_row.setdefault(row, []).append(case)

    records = []
    for label in labels:
        target_type, selected_cases = _select_cases_for_label(label, cases_by_row)
        candidate_results = [
            _load_candidate_result(run_dir, case) for case in selected_cases
        ]
        records.append(_assess_label(label, target_type, candidate_results))

    metrics = _metrics(records)
    metrics["excluded_demonstration_label_units"] = len(
        excluded_demonstration_labels
    )
    return {
        "schema_version": "placement-pilot-evaluation-v2",
        "run": run,
        "split": split_name,
        "visual_anchors_enabled": visual_anchors_enabled,
        "sources": {
            "pilot_labels": str(labels_path),
            "split": str(split_path),
            "run_directory": str(run_dir),
        },
        "evaluation_policy": {
            "unit": "one direct placement-specific comment segment",
            "exact_target": "Evaluate only the row-and-id matched target variant.",
            "comparison_set": "Evaluate once; detected when one or more row candidates shows the expected issue.",
            "unavailable_results": "A nondetection is reported only when all required candidate judgments succeeded.",
            "prediction_threshold": "Only predicted severity >=1 contributes issue codes or component alignment.",
            "development_demonstrations": (
                "When visual anchors are enabled, labels from the three development "
                "human-defect demonstration rows are excluded from all detection denominators."
            ),
            "limitations": [
                "Manual labels contain positive placement evidence only.",
                "Severity and confidence are prediction fields, not manual labels.",
                "No pass/fail threshold calibration is computed.",
            ],
        },
        "metrics": metrics,
        "excluded_demonstration_labels": excluded_demonstration_labels,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate stored placement pilot judgments against sparse issue labels."
    )
    parser.add_argument("--run", required=True)
    parser.add_argument(
        "--split", choices=("development", "held_out", "all"), required=True
    )
    args = parser.parse_args()

    report = evaluate(args.run, args.split)
    output_path = ROOT / "runs" / args.run / f"{args.split}_evaluation.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output_path),
                "run": args.run,
                "split": args.split,
                "metrics": report["metrics"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
