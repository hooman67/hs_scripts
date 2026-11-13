"""Deterministic validation and aggregation for placement observations.

This module deliberately contains no model calls or generated-text repair. Invalid
observations fail closed with explicit validation errors.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

from jsonschema import Draft202012Validator


SCHEMA_PATH = Path(__file__).with_name("observation_schema.json")
SCHEMA_VERSION = "placement-observations-v1"
POLICY_VERSION = "placement-scoring-policy-v1"
THRESHOLD_STATUS = "provisional_not_human_calibrated"

COMPONENT_WEIGHTS = {
    "support_scenario": 20,
    "access_usability": 30,
    "orientation_alignment": 20,
    "scale_perspective": 15,
    "contact_integration": 15,
}
CORE_PASS_COMPONENTS = (
    "support_scenario",
    "access_usability",
    "orientation_alignment",
)
VISIBILITY_COVERAGE = {"observed": 1.0, "partial": 0.5, "unobservable": 0.0}

ISSUE_CODES = {
    "support_scenario": frozenset(
        {
            "inappropriate_support",
            "occupied_workstation",
            "implausible_scenario",
            "unsupported_base",
        }
    ),
    "access_usability": frozenset(
        {
            "excessive_reach",
            "precarious_edge",
            "blocked_operating_side",
            "no_user_position",
            "furniture_collision",
            "blocked_paper_or_lid_path",
        }
    ),
    "orientation_alignment": frozenset(
        {
            "corner_facing",
            "furniture_axis_conflict",
            "chair_alignment_conflict",
        }
    ),
    "scale_perspective": frozenset(
        {"implausible_scale", "conflicting_perspective"}
    ),
    "contact_integration": frozenset(
        {
            "floating",
            "sinking_or_intersection",
            "inconsistent_shadow",
            "inconsistent_reflection",
        }
    ),
}

INPUT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "generated_image",
        "twin_image",
        "product_type",
        "scene_prompt",
        "image_stage",
    ],
    "properties": {
        "generated_image": {"type": "string", "minLength": 1},
        "twin_image": {"type": "string", "minLength": 1},
        "product_type": {"enum": ["laptop", "printer"]},
        "scene_prompt": {"type": "string"},
        "image_stage": {"const": "scene_generation"},
    },
}


with SCHEMA_PATH.open(encoding="utf-8") as schema_file:
    OBSERVATION_SCHEMA = json.load(schema_file)

Draft202012Validator.check_schema(OBSERVATION_SCHEMA)
Draft202012Validator.check_schema(INPUT_SCHEMA)
_OBSERVATION_VALIDATOR = Draft202012Validator(OBSERVATION_SCHEMA)
_INPUT_VALIDATOR = Draft202012Validator(INPUT_SCHEMA)


class PlacementValidationError(ValueError):
    """One or more structural or semantic validation errors."""

    def __init__(self, errors: Iterable[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


def _format_jsonschema_error(error: Any) -> str:
    path = "$"
    for part in error.absolute_path:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return f"{path}: {error.message}"


def _schema_errors(
    instance: Any, validator: Draft202012Validator
) -> List[str]:
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    return [_format_jsonschema_error(error) for error in errors]


def validate_runtime_input(runtime_input: Any) -> Mapping[str, Any]:
    """Validate the exact runtime-input shape and return it unchanged."""

    errors = _schema_errors(runtime_input, _INPUT_VALIDATOR)
    if errors:
        raise PlacementValidationError(errors)
    return runtime_input


def _semantic_observation_errors(observation: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    for name in COMPONENT_WEIGHTS:
        component = observation["components"][name]
        visibility = component["visibility"]
        severity = component["severity"]
        confidence = component["confidence"]
        issue_codes = component["issue_codes"]
        prefix = f"$.components.{name}"

        if not component["evidence"].strip():
            errors.append(f"{prefix}.evidence: must contain non-whitespace evidence")

        if visibility == "unobservable":
            if severity is not None:
                errors.append(
                    f"{prefix}.severity: must be null when visibility is unobservable"
                )
            if confidence != "low":
                errors.append(
                    f"{prefix}.confidence: must be low when visibility is unobservable"
                )
            if issue_codes:
                errors.append(
                    f"{prefix}.issue_codes: must be empty when visibility is unobservable"
                )
        elif severity is None:
            errors.append(
                f"{prefix}.severity: must be an integer when visibility is {visibility}"
            )

        if severity == 0 and issue_codes:
            errors.append(f"{prefix}.issue_codes: must be empty when severity is 0")
        elif isinstance(severity, int) and not isinstance(severity, bool) and severity > 0:
            if not issue_codes:
                errors.append(
                    f"{prefix}.issue_codes: at least one code is required when severity is positive"
                )

        invalid_codes = sorted(set(issue_codes) - ISSUE_CODES[name])
        if invalid_codes:
            errors.append(
                f"{prefix}.issue_codes: codes are not valid for this component: "
                + ", ".join(invalid_codes)
            )

    return errors


def validate_observation(observation: Any) -> Mapping[str, Any]:
    """Validate schema and cross-field semantics; return the input unchanged."""

    schema_errors = _schema_errors(observation, _OBSERVATION_VALIDATOR)
    if schema_errors:
        raise PlacementValidationError(schema_errors)

    semantic_errors = _semantic_observation_errors(observation)
    if semantic_errors:
        raise PlacementValidationError(semantic_errors)
    return observation


def _component_scores(components: Mapping[str, Mapping[str, Any]]) -> Dict[str, Optional[int]]:
    return {
        name: None if component["severity"] is None else 100 - 25 * component["severity"]
        for name, component in components.items()
    }


def _natural_placement_score(
    component_scores: Mapping[str, Optional[int]],
) -> Optional[float]:
    eligible_weight = sum(
        COMPONENT_WEIGHTS[name]
        for name, component_score in component_scores.items()
        if component_score is not None
    )
    if eligible_weight == 0:
        return None

    weighted_score = sum(
        COMPONENT_WEIGHTS[name] * component_score
        for name, component_score in component_scores.items()
        if component_score is not None
    )
    return round(weighted_score / eligible_weight, 1)


def _coverage(components: Mapping[str, Mapping[str, Any]]) -> float:
    coverage = sum(
        COMPONENT_WEIGHTS[name] * VISIBILITY_COVERAGE[component["visibility"]]
        for name, component in components.items()
    ) / 100
    return round(coverage, 3)


def _overall_confidence(
    coverage: float, components: Mapping[str, Mapping[str, Any]]
) -> str:
    eligible_confidences = [
        component["confidence"]
        for component in components.values()
        if component["severity"] is not None
    ]
    if coverage >= 0.85 and all(
        confidence == "high" for confidence in eligible_confidences
    ):
        return "high"
    if coverage >= 0.6 and all(
        confidence != "low" for confidence in eligible_confidences
    ):
        return "medium"
    return "low"


def _review_reasons(
    observation: Mapping[str, Any], score: float, coverage: float, confidence: str
) -> List[str]:
    components = observation["components"]
    reasons: List[str] = []

    if score < 80:
        reasons.append("score_below_pass_threshold")
    if coverage < 0.70:
        reasons.append("coverage_below_pass_threshold")
    if confidence == "low":
        reasons.append("overall_confidence_low")

    for name in CORE_PASS_COMPONENTS:
        component = components[name]
        if component["severity"] is None:
            reasons.append(f"core_component_unassessable:{name}")
        elif component["confidence"] == "low":
            reasons.append(f"core_component_low_confidence:{name}")

    if any(
        component["severity"] is not None and component["severity"] >= 2
        for component in components.values()
    ):
        reasons.append("material_component_problem")
    if any(
        component["severity"] is not None
        and component["severity"] >= 3
        and component["confidence"] == "low"
        for component in components.values()
    ):
        reasons.append("severe_problem_low_confidence")
    return reasons or ["pass_criteria_not_met"]


def _verdict(
    observation: Mapping[str, Any],
    score: Optional[float],
    coverage: float,
    confidence: str,
) -> tuple[str, List[str]]:
    components = observation["components"]

    # Contract precedence is intentional: an input-product mismatch or an
    # unscorable observation remains review even if another rule could fail it.
    initial_review_reasons: List[str] = []
    if observation["product_match"] == "mismatch":
        initial_review_reasons.append("product_mismatch")
    elif observation["product_match"] == "uncertain":
        initial_review_reasons.append("product_match_uncertain")
    if score is None:
        initial_review_reasons.append("no_assessable_components")
    if initial_review_reasons:
        return "review", initial_review_reasons

    if any(
        component["severity"] >= 3
        and component["confidence"] in {"medium", "high"}
        for component in components.values()
        if component["severity"] is not None
    ):
        return "fail", ["major_problem_veto"]

    if score < 60 and confidence != "low":
        return "fail", ["score_below_fail_threshold"]

    core_assessable = all(
        components[name]["severity"] is not None
        and components[name]["confidence"] in {"medium", "high"}
        for name in CORE_PASS_COMPONENTS
    )
    no_material_problem = all(
        component["severity"] is None or component["severity"] < 2
        for component in components.values()
    )
    if (
        score >= 80
        and coverage >= 0.70
        and confidence != "low"
        and core_assessable
        and no_material_problem
    ):
        return "pass", ["pass_criteria_met"]

    return "review", _review_reasons(observation, score, coverage, confidence)


def aggregate_observation(observation: Any) -> Dict[str, Any]:
    """Validate and deterministically enrich one model observation.

    The original observation is retained under ``observation`` and is never
    mutated. The aggregate metric is exposed under its canonical contract name,
    ``natural_placement_score``.
    """

    validate_observation(observation)
    components = observation["components"]
    component_scores = _component_scores(components)
    score = _natural_placement_score(component_scores)
    coverage = _coverage(components)
    confidence = _overall_confidence(coverage, components)
    verdict, verdict_reasons = _verdict(
        observation, score, coverage, confidence
    )

    return {
        "observation": copy.deepcopy(observation),
        "natural_placement_score": score,
        "component_scores": component_scores,
        "coverage": coverage,
        "confidence": confidence,
        "verdict": verdict,
        "verdict_reasons": verdict_reasons,
        "threshold_status": THRESHOLD_STATUS,
        "policy_version": POLICY_VERSION,
    }


# Concise alias for callers that treat this module as the scoring runtime.
aggregate = aggregate_observation

