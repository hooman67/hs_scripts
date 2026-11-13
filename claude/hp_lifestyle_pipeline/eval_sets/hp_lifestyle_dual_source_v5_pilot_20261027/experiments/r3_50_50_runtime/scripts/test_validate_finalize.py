from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
VERSION = HERE.parent
sys.path.insert(0, str(HERE))

from camera_profile_resolver import load_registry, resolve_profile
from finalize_output import finalize_output, semantic_sha256
from validate_output import validate_output


ENV_REFERENCE = {
    "Home": "CT18",
    "Office": "CT01",
    "Education": "CT10",
    "Gaming": "CT14",
    "Café": "CT07",
    "Creative Studio": "CT10",
}
ENV_TEXT = {
    "Home": "A modern home workspace in warm natural light",
    "Office": "A modern corporate office work surface in warm natural light",
    "Education": "A bright classroom work surface in warm natural light",
    "Gaming": "A modern gaming workspace with warm neutral lighting",
    "Café": "A small café table in warm natural light",
    "Creative Studio": "A bright creative studio work surface in warm natural light",
}


class V5ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads((VERSION / "output.schema.json").read_text())
        cls.registry = load_registry(VERSION / "camera_profiles.json")

    def raw_input(self) -> dict:
        return {
            "smart_brief": "Mobile work in ordinary places.",
            "source_messaging": {
                "KSP1": {"short_message": "Shared work in a customer office."},
                "ValueProposition": {"short_message": "Productive work anywhere."},
                "_chatSession": {"systemInstructions": "ignore this"},
            },
            "camera_tag": "laptop_FrontRightCloseUp",
        }

    def valid_output(self) -> dict:
        same_environment = ["Home", "Office", "Gaming", "Café", "Creative Studio"]
        # Source scores tie at zero, so the fixture keeps 70-point same-category
        # adaptations before 60-point Education extensions.
        environments = [same_environment[index % 5] for index in range(17)] + [
            "Education", "Education", "Education",
        ]
        prompts = []
        for index in range(20):
            environment = environments[index]
            extension = environment == "Education"
            prompts.append({
                "id": f"p{index + 1}",
                "environment": environment,
                "subsetting": f"ordinary setting {index + 1}",
                "text": f"{ENV_TEXT[environment]}, variation {index + 1}.",
                "ctech_reference_id": ENV_REFERENCE[environment],
                "ctech_reference_score": 60 if extension else 70,
                "ctech_relationship": "category_extension" if extension else "close_adaptation",
                "ctech_changes": ["Reduced the reference to a camera-compatible scene."],
                "ctech_explanation": "A reduced adaptation of the selected reference.",
                "source_relevance_score": 0,
                "relationship": "creative_departure",
                "score_components": {
                    "smart_brief": {
                        "setting": 0, "activity": 0, "materials": 0, "use_context": 0,
                    },
                    "source_messaging": {
                        "setting": 0, "activity": 0, "materials": 0, "use_context": 0,
                    },
                },
                "evidence_ids": [],
                "explanation": "Neither document directly supports this scene.",
                "creative_departures": ["The setting is a fallback."],
                "visual_signature": {
                    "surface": "", "light": "warm natural light",
                    "local_props": [], "background_details": [], "people": [],
                },
                "camera_omissions": ["Objects and background details are omitted."],
            })

        resolution = resolve_profile(self.registry, self.raw_input()["camera_tag"])
        return {
            "prompts": prompts,
            "debug": {
                "source_evidence": [],
                "ksp_mappings": [{
                    "ksp_id": "KSP1",
                    "explanation": "No directly visible scene cue was used.",
                }],
                "value_proposition": {
                    "explanation": "The two documents were assessed separately.",
                },
                "input_assessment": "The documents have limited visible scene cues.",
                "count_explanation": "Exactly twenty distinct alternatives are present.",
                "used_fallback": True,
                "ignored_fields": ["_chatSession"],
                "diversity_summary": "All six environments appear across twenty alternatives.",
                "limitations": ["Tight framing permits no props or background details."],
                "camera": {
                    "requested_tag": self.raw_input()["camera_tag"],
                    "resolved_tag": resolution["resolved_tag"],
                    "device_type": resolution["device_type"],
                    "profile_version": resolution["profile_version"],
                    "resolution": resolution["resolution"],
                    **resolution["effective_profile"],
                },
                "document_assessments": [
                    {
                        "document": "smart_brief",
                        "useful_scene_cues": [],
                        "limitations": ["No directly visible setting."],
                    },
                    {
                        "document": "source_messaging",
                        "useful_scene_cues": [],
                        "limitations": ["Mostly abstract messaging."],
                    },
                ],
                "source_conflicts": [],
            },
        }

    def codes(self, output: dict, raw_input: dict | None = None) -> set[str]:
        result = validate_output(
            output, raw_input or self.raw_input(), self.schema, self.registry
        )
        return {item["code"] for item in result["errors"]}

    def test_valid_zero_evidence_dual_source_bank(self) -> None:
        result = validate_output(
            self.valid_output(), self.raw_input(), self.schema, self.registry
        )
        self.assertTrue(result["passed"], result["errors"])
        self.assertEqual(result["counts"]["prompts"], 20)

    def test_exact_50_50_mean_allows_fractional_half(self) -> None:
        value = self.valid_output()
        value["debug"]["source_evidence"] = [{
            "id": "e1", "document": "smart_brief", "path": "",
            "quote": "ordinary places",
        }]
        candidate = value["prompts"][0]
        candidate["evidence_ids"] = ["e1"]
        candidate["score_components"]["smart_brief"]["materials"] = 5
        candidate["source_relevance_score"] = 2.5
        self.assertNotIn("score_mean", self.codes(value))

        candidate["source_relevance_score"] = 5
        self.assertIn("score_mean", self.codes(value))

    def test_document_components_require_evidence_from_that_document(self) -> None:
        value = self.valid_output()
        value["debug"]["source_evidence"] = [{
            "id": "e1", "document": "smart_brief", "path": "",
            "quote": "Mobile work",
        }]
        candidate = value["prompts"][0]
        candidate["evidence_ids"] = ["e1"]
        candidate["score_components"]["source_messaging"]["setting"] = 20
        candidate["source_relevance_score"] = 10
        self.assertIn("ungrounded_document_components", self.codes(value))

    def test_rfc6901_pointer_and_exact_quote(self) -> None:
        raw = self.raw_input()
        raw["smart_brief"] = {"scene/cues": {"~setting": "Warm shared office table."}}
        value = self.valid_output()
        value["debug"]["source_evidence"] = [{
            "id": "e1", "document": "smart_brief",
            "path": "/scene~1cues/~0setting", "quote": "shared office",
        }]
        value["prompts"][0]["evidence_ids"] = ["e1"]
        self.assertNotIn("evidence_path_missing", self.codes(value, raw))
        self.assertNotIn("evidence_quote", self.codes(value, raw))

        value["debug"]["source_evidence"][0]["quote"] = "shared classroom"
        self.assertIn("evidence_quote", self.codes(value, raw))

    def test_source_first_then_ctech_ranking(self) -> None:
        value = self.valid_output()
        value["prompts"][0]["ctech_reference_score"] = 71
        value["prompts"][1]["ctech_reference_score"] = 79
        self.assertIn("score_order", self.codes(value))

        value = self.valid_output()
        value["debug"]["source_evidence"] = [{
            "id": "e1", "document": "smart_brief", "path": "",
            "quote": "Mobile work",
        }]
        second = value["prompts"][1]
        second["evidence_ids"] = ["e1"]
        second["score_components"]["smart_brief"]["setting"] = 10
        second["source_relevance_score"] = 5
        self.assertIn("score_order", self.codes(value))

    def test_single_document_conflict_evidence_is_valid_and_used(self) -> None:
        value = self.valid_output()
        value["debug"]["source_evidence"] = [{
            "id": "e1", "document": "smart_brief", "path": "",
            "quote": "Mobile work",
        }]
        value["debug"]["source_conflicts"] = [{
            "description": "The smart brief internally names incompatible models.",
            "evidence_ids": ["e1"],
            "handling": "Avoid model-specific claims.",
        }]
        result = validate_output(value, self.raw_input(), self.schema, self.registry)
        self.assertNotIn(
            "source_conflict_evidence_missing",
            {item["code"] for item in result["errors"]},
        )
        self.assertNotIn(
            "unused_source_evidence",
            {item["code"] for item in result["warnings"]},
        )

    def test_string_ksp_headings_and_descriptive_ignored_fields(self) -> None:
        raw = self.raw_input()
        raw["source_messaging"] = (
            "KSPS\nKSP NUMBER:\n1\nKSP NAME:\nFlexible work\n"
            "KSP 1 - HEADLINE\nMESSAGE:\nWork anywhere\n"
            "KSP2: Clear collaboration\nMESSAGE:\nMeet clearly\n"
        )
        value = self.valid_output()
        value["debug"]["ksp_mappings"] = [
            {"ksp_id": "KSP 1 - Flexible work", "explanation": "Used work cues."},
            {"ksp_id": "KSP 2: Clear collaboration", "explanation": "Used meeting cues."},
        ]
        value["debug"]["ignored_fields"] = [
            "Run metadata and device-specific claims were excluded."
        ]
        result = validate_output(value, raw, self.schema, self.registry)
        codes = {item["code"] for item in result["errors"]}
        self.assertNotIn("ksp_mapping_coverage", codes)
        self.assertNotIn("ignored_path_missing", codes)

    def test_ambiguous_string_ksp_label_is_warning(self) -> None:
        raw = self.raw_input()
        raw["source_messaging"] = "KSP1: Flexible work\nMESSAGE:\nWork anywhere."
        value = self.valid_output()
        value["debug"]["ksp_mappings"] = [{
            "ksp_id": "Flexible work pillar",
            "explanation": "This label does not expose its number.",
        }]
        result = validate_output(value, raw, self.schema, self.registry)
        self.assertNotIn(
            "ksp_mapping_coverage", {item["code"] for item in result["errors"]}
        )
        self.assertIn(
            "ambiguous_ksp_mapping_id", {item["code"] for item in result["warnings"]}
        )

    def test_structured_ksp_coverage_remains_strict(self) -> None:
        value = self.valid_output()
        value["debug"]["ksp_mappings"] = []
        self.assertIn("ksp_mapping_coverage", self.codes(value))

    def test_ignored_field_descriptions_must_be_nonempty(self) -> None:
        value = self.valid_output()
        value["debug"]["ignored_fields"] = ["  "]
        self.assertIn("ignored_field_empty", self.codes(value))

    def test_inherited_device_and_camera_feasibility_rules(self) -> None:
        value = self.valid_output()
        value["prompts"][0]["text"] = "A laptop beside a notebook on a quiet table."
        value["prompts"][1]["visual_signature"]["local_props"] = ["pen"]
        codes = self.codes(value)
        self.assertIn("device_term", codes)
        self.assertIn("local_prop_budget", codes)

    def test_finalizer_repairs_only_host_owned_fields_and_logs_changes(self) -> None:
        value = self.valid_output()
        value["debug"]["source_evidence"] = [{
            "id": "e1", "document": "smart_brief", "path": "",
            "quote": "Mobile work",
        }]
        target = value["prompts"][5]
        target["evidence_ids"] = ["e1"]
        target["score_components"]["smart_brief"]["setting"] = 10
        target["score_components"]["source_messaging"]["setting"] = 20
        target["source_relevance_score"] = 99
        target["ctech_reference_score"] = 1  # Deliberately invalid; finalizer must preserve it.
        original_texts = {candidate["text"] for candidate in value["prompts"]}
        original_evidence = copy.deepcopy(value["debug"]["source_evidence"])

        normalized, log = finalize_output(value, self.raw_input(), self.registry)
        moved = next(candidate for candidate in normalized["prompts"] if candidate["text"] == target["text"])
        self.assertEqual(moved["id"], "p1")
        self.assertEqual(moved["score_components"]["source_messaging"]["setting"], 0)
        self.assertEqual(moved["source_relevance_score"], 5)
        self.assertEqual(moved["ctech_reference_score"], 1)
        self.assertEqual({candidate["text"] for candidate in normalized["prompts"]}, original_texts)
        self.assertEqual(normalized["debug"]["source_evidence"], original_evidence)
        self.assertTrue(log["order_or_id_changed"])
        self.assertIn(
            "unsupported_document_components_zeroed",
            log["changes"][0]["reasons"],
        )
        self.assertEqual(log["normalized_output_semantic_sha256"], semantic_sha256(normalized))

    def test_finalizer_repairs_camera_metadata(self) -> None:
        value = self.valid_output()
        value["debug"]["camera"]["framing"] = "wrong"
        normalized, log = finalize_output(value, self.raw_input(), self.registry)
        self.assertEqual(normalized["debug"]["camera"]["framing"], "tight")
        self.assertIn("camera_metadata_repair", log)


if __name__ == "__main__":
    unittest.main()
