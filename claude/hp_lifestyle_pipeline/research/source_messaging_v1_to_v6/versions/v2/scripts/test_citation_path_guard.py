#!/usr/bin/env python3

from __future__ import annotations

import copy
import unittest

from citation_path_guard import normalize_citation_paths


def output_with(block: str, path: str, quote: str) -> dict:
    mapping = {
        "ksp_id": block,
        "source_evidence": [{"path": path, "quote": quote}],
    }
    return {
        "prompts": [{"id": "p1", "text": "unchanged"}],
        "debug": {
            "ksp_mappings": [mapping] if block != "ValueProposition" else [],
            "value_proposition": (
                {"source_evidence": [{"path": path, "quote": quote}]}
                if block == "ValueProposition"
                else {"source_evidence": []}
            ),
        },
    }


class CitationPathGuardTest(unittest.TestCase):
    def test_unique_copy_variant_repairs_only_path(self) -> None:
        source = {
            "ValueProposition": {
                "short_message": "polished collaboration anywhere",
                "long_message_best_sku": "different text",
            }
        }
        raw = output_with(
            "ValueProposition",
            "ValueProposition.long_message_best_sku",
            "polished collaboration anywhere",
        )
        original = copy.deepcopy(raw)
        result = normalize_citation_paths(raw, source)
        self.assertEqual(raw, original)
        self.assertEqual(
            result["validated_output"]["debug"]["value_proposition"][
                "source_evidence"
            ][0]["path"],
            "ValueProposition.short_message",
        )
        self.assertEqual(len(result["citation_repairs"]), 1)
        self.assertEqual(result["failures"], [])
        repaired_copy = copy.deepcopy(result["validated_output"])
        repaired_copy["debug"]["value_proposition"]["source_evidence"][0][
            "path"
        ] = "ValueProposition.long_message_best_sku"
        self.assertEqual(repaired_copy, raw)

    def test_never_crosses_ksp_objects(self) -> None:
        source = {
            "KSP1": {"short_message": "not here"},
            "KSP2": {"short_message": "unique elsewhere"},
        }
        raw = output_with("KSP1", "KSP1.long_message", "unique elsewhere")
        result = normalize_citation_paths(raw, source)
        self.assertEqual(result["citation_repairs"], [])
        self.assertEqual(
            result["failures"][0]["reason"],
            "citation_quote_not_found_in_intended_message",
        )

    def test_declared_cross_ksp_scope_is_rejected(self) -> None:
        source = {
            "KSP1": {"short_message": "same quote"},
            "KSP2": {"short_message": "same quote"},
        }
        raw = output_with("KSP1", "KSP2.short_message", "same quote")
        result = normalize_citation_paths(raw, source)
        self.assertEqual(result["citation_repairs"], [])
        self.assertEqual(
            result["failures"][0]["reason"], "citation_path_wrong_scope"
        )
        self.assertEqual(result["failures"][0]["intended_scope"], "KSP1")

    def test_no_match_is_explicit_failure(self) -> None:
        raw = output_with("KSP1", "KSP1.missing", "absent")
        result = normalize_citation_paths(raw, {"KSP1": {"short_message": "other"}})
        self.assertEqual(result["citation_repairs"], [])
        self.assertEqual(result["failures"][0]["matching_paths"], [])

    def test_ambiguous_match_is_not_repaired(self) -> None:
        source = {"KSP1": {"short_message": "same quote", "long_message": "same quote"}}
        raw = output_with("KSP1", "KSP1.missing", "same quote")
        result = normalize_citation_paths(raw, source)
        self.assertEqual(result["citation_repairs"], [])
        self.assertEqual(
            result["failures"][0]["reason"],
            "citation_quote_matches_multiple_fields_in_intended_message",
        )

    def test_already_valid_is_unchanged_and_unreported(self) -> None:
        source = {"KSP1": {"short_message": "exact quote"}}
        raw = output_with("KSP1", "KSP1.short_message", "exact quote")
        original = copy.deepcopy(raw)
        result = normalize_citation_paths(raw, source)
        self.assertEqual(raw, original)
        self.assertEqual(result["validated_output"], original)
        self.assertEqual(result["citation_repairs"], [])
        self.assertEqual(result["failures"], [])


if __name__ == "__main__":
    unittest.main()
