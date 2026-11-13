#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

import scoring


CHECKS = tuple(scoring.CHECK_COMPONENT)


def clear_check():
    return {
        "visibility": "observed",
        "severity": 0,
        "confidence": "high",
        "warning_level": "none",
        "issue_codes": [],
        "evidence": "The relevant relation is directly visible and coherent.",
        "consequence": "",
        "alternative_explanation": "",
        "visibility_limit": "",
    }


def assessment():
    return {
        "stage_status": "assessed",
        "unable_reason": None,
        "functional_front": "The functional front is visible.",
        "context_reading": "The product and furniture form one visible use zone.",
        "checks": {name: clear_check() for name in CHECKS},
        "general_artifact_warnings": [],
    }


def issue(value, name, *, severity, confidence="high", warning="none", codes):
    value["checks"][name].update(
        severity=severity,
        confidence=confidence,
        warning_level=warning,
        issue_codes=codes,
        consequence="The arrangement needs correction." if severity >= 2 else "Minor adjustment.",
        alternative_explanation="A benign interpretation was considered but contradicted by visible geometry." if severity >= 2 else "",
    )


class ScoringTests(unittest.TestCase):
    def test_clear_complete_scene_passes(self):
        result = scoring.aggregate_assessment(assessment())
        self.assertEqual(result["verdict"], "pass")
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["coverage"], 1.0)

    def test_chair_advisory_can_pass(self):
        value = assessment()
        issue(value, "user_position", severity=1, warning="advisory", codes=["chair_displacement"])
        result = scoring.aggregate_assessment(value)
        self.assertEqual(result["verdict"], "pass")
        self.assertIn("placement_advisory", result["reason_codes"])

    def test_chair_review_warning_reviews(self):
        value = assessment()
        issue(value, "user_position", severity=1, warning="review", codes=["chair_displacement"])
        self.assertEqual(scoring.aggregate_assessment(value)["verdict"], "review")

    def test_chair_displacement_cannot_be_material(self):
        value = assessment()
        issue(value, "user_position", severity=2, codes=["chair_displacement"])
        with self.assertRaises(scoring.PlacementValidationError):
            scoring.validate_assessment(value)

    def test_high_confidence_material_fails_and_caps(self):
        value = assessment()
        issue(value, "support_anatomy", severity=3, codes=["missing_required_support"])
        result = scoring.aggregate_assessment(value)
        self.assertEqual(result["verdict"], "fail")
        self.assertLessEqual(result["score"], 39)

    def test_medium_material_reviews(self):
        value = assessment()
        issue(value, "shared_perspective", severity=2, confidence="medium", codes=["conflicting_perspective"])
        result = scoring.aggregate_assessment(value)
        self.assertEqual(result["verdict"], "review")
        self.assertLessEqual(result["score"], 79)

    def test_critical_unobservable_reviews_without_penalty(self):
        value = assessment()
        value["checks"]["user_position"] = {
            **clear_check(),
            "visibility": "unobservable",
            "severity": None,
            "confidence": "low",
            "evidence": "The close crop hides keyboard-side seating.",
            "visibility_limit": "The floor and chair-side edge are outside the frame.",
        }
        result = scoring.aggregate_assessment(value)
        self.assertEqual(result["verdict"], "review")
        self.assertIn("critical_relation_unobservable", result["reason_codes"])

    def test_unrelated_artifact_does_not_change_placement(self):
        value = assessment()
        value["general_artifact_warnings"] = [{"code": "unrelated_rendering_artifact", "evidence": "Eyeglasses are malformed."}]
        result = scoring.aggregate_assessment(value)
        self.assertEqual(result["verdict"], "pass")
        self.assertIn("general_artifact_warning", result["reason_codes"])

    def test_issue_ownership_is_enforced(self):
        value = assessment()
        issue(value, "support_anatomy", severity=2, codes=["chair_displacement"])
        with self.assertRaises(scoring.PlacementValidationError):
            scoring.validate_assessment(value)

    def test_partial_requires_visibility_limit(self):
        value = assessment()
        value["checks"]["support_contact"]["visibility"] = "partial"
        with self.assertRaises(scoring.PlacementValidationError):
            scoring.validate_assessment(value)


if __name__ == "__main__":
    unittest.main()
