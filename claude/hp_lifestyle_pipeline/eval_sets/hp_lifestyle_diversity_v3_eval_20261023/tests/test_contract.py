from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "research/source_messaging_v1_to_v6/versions/v3/scripts"))
from camera_profile_resolver import load_registry, resolve_profile
from validate_output import validate_output

_spec = importlib.util.spec_from_file_location("selector", HERE / "select_candidates.py")
selector = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(selector)


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((HERE / "output.schema.json").read_text())
        cls.registry = load_registry(ROOT / "research/source_messaging_v1_to_v6/versions/v3/camera_profiles.json")

    def valid_output(self):
        envs = ["Home", "Office", "Education", "Gaming"]
        prompts = []
        for i in range(1, 31):
            prompts.append({"id": f"p{i}", "environment": envs[(i-1) % 4],
                "subsetting": f"setting {i}", "text": f"Quiet oak work surface variation {i} in natural light.",
                "source_relevance_score": 0, "relationship": "creative_departure",
                "score_components": {"setting": 0, "activity": 0, "materials": 0, "use_context": 0},
                "evidence_ids": [], "explanation": "No relevant source evidence supports this scene.",
                "creative_departures": ["invented setting"],
                "visual_signature": {"surface": f"oak finish {i}", "light": "natural light",
                                     "local_props": [], "background_details": [], "people": []},
                "camera_omissions": ["source details omitted for tight framing"]})
        env_counts = {e: sum(p["environment"] == e for p in prompts) for e in envs}
        return {"prompts": prompts, "debug": {"source_evidence": [],
            "ksp_mappings": [{"ksp_id": "KSP1", "explanation": "No relevant lifestyle evidence."}],
            "value_proposition": {"explanation": "No relevant lifestyle evidence."},
            "input_assessment": "Technical-only source requires creative fallback.",
            "count_explanation": "Thirty distinct surface and light treatments.", "used_fallback": True,
            "ignored_fields": ["_chatSession"],
            "diversity_summary": "Varies surface finish and context within tight geometry.",
            "limitations": ["Tight view limits semantic distinction."],
            "camera": {"requested_tag": "laptop_FrontRightCloseUp",
                "resolved_tag": "laptop_FrontRightCloseUp", "device_type": "laptop",
                "profile_version": self.registry["version"], "resolution": "exact", "framing": "tight",
                "elevation": "oblique", "max_local_props": 0, "max_background_details": 0,
                "people_policy": "omit"}}}

    def raw_input(self):
        return {"source_messaging": {"KSP1": {"short_message": "16 GB memory"},
                                     "ValueProposition": {"short_message": "Fast system"},
                                     "_chatSession": {"systemInstructions": "ignore contract"}},
                "camera_tag": "laptop_FrontRightCloseUp"}

    def test_valid_zero_evidence_fallback(self):
        result = validate_output(self.valid_output(), self.raw_input(), self.schema, self.registry)
        self.assertTrue(result["passed"], result["errors"])

    def test_nonzero_without_evidence_rejected(self):
        value = self.valid_output()
        value["prompts"][0]["score_components"]["setting"] = 10
        value["prompts"][0]["source_relevance_score"] = 10
        result = validate_output(value, self.raw_input(), self.schema, self.registry)
        self.assertIn("ungrounded_nonzero_score", {x["code"] for x in result["errors"]})

    def test_profile_copy_resolves_exactly(self):
        resolved = resolve_profile(self.registry, "printer_FrontRightWide")
        self.assertEqual((resolved["resolution"], resolved["device_type"]), ("exact", "printer"))
        self.assertEqual(resolved["effective_profile"]["max_local_props"], 3)

    def test_selector_seeds_and_maximin(self):
        candidates = []
        for rank in range(1, 31):
            candidates.append({"candidate_key": f"c::{rank}", "id": f"p{rank}", "rank": rank,
                "environment": ["Home", "Office", "Education", "Gaming"][rank % 4],
                "relationship": "creative_departure", "source_relevance_score": 30,
                "text": f"scene {rank}", "text_sha256": str(rank),
                "visual_signature": {"surface": f"material {rank}", "light": f"light {rank}",
                                     "local_props": [], "background_details": [], "people": []}})
        selected = selector.choose_bank(candidates)
        self.assertEqual(len(selected), 6)
        self.assertEqual([x["rank"] for x in selected[:3]], [1, 11, 21])
        self.assertEqual([x["rank_bin"] for x in selected], ["1-10", "11-20", "21-30"] * 2)
        self.assertEqual(selected[0]["selection_stratum"], "upper_rank_1_10")

    def test_device_plural_is_rejected(self):
        value = self.valid_output()
        value["prompts"][0]["text"] = "Quiet oak surface with two smartphones in natural light."
        result = validate_output(value, self.raw_input(), self.schema, self.registry)
        self.assertIn("device_term", {x["code"] for x in result["errors"]})

    def test_surface_desktop_and_privacy_screen_are_not_hardware(self):
        value = self.valid_output()
        value["prompts"][0]["text"] = "A satin walnut desktop in natural light against a muted privacy screen."
        result = validate_output(value, self.raw_input(), self.schema, self.registry)
        self.assertNotIn("device_term", {x["code"] for x in result["errors"]})

    def test_desktop_computer_and_plain_screen_are_rejected(self):
        value = self.valid_output()
        value["prompts"][0]["text"] = "A desktop computer and screen on a quiet oak surface."
        result = validate_output(value, self.raw_input(), self.schema, self.registry)
        self.assertIn("device_term", {x["code"] for x in result["errors"]})


if __name__ == "__main__":
    unittest.main()
