from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "research/source_messaging_v1_to_v6/versions/v3/scripts"))
from finalize_output import PREFIX, finalize_output, semantic_sha256
from camera_profile_resolver import load_registry, resolve_profile


def candidate(pid, score, components, evidence, relationship="source_grounded"):
    return {"id": pid, "source_relevance_score": score,
            "score_components": components, "evidence_ids": evidence,
            "relationship": relationship, "explanation": f"original {pid}", "text": f"scene {pid}"}


class FinalizerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_registry(ROOT / "research/source_messaging_v1_to_v6/versions/v3/camera_profiles.json")

    def test_empty_evidence_is_zeroed_without_text_edit(self):
        raw = {"prompts": [candidate("p1", 20, {"setting": 20, "activity": 0,
               "materials": 0, "use_context": 0}, [], "source_adjacent")],
               "debug": {"limitations": []}}
        before = copy.deepcopy(raw)
        normalized, log = finalize_output(raw)
        self.assertEqual(raw, before)
        self.assertEqual(normalized["prompts"][0]["source_relevance_score"], 0)
        self.assertEqual(normalized["prompts"][0]["relationship"], "creative_departure")
        self.assertTrue(normalized["prompts"][0]["explanation"].startswith(PREFIX))
        self.assertEqual(normalized["prompts"][0]["text"], raw["prompts"][0]["text"])
        self.assertEqual(log["changed_candidate_count"], 1)

    def test_valid_scored_candidate_unchanged(self):
        raw = {"prompts": [candidate("p1", 30, {"setting": 20, "activity": 10,
               "materials": 0, "use_context": 0}, ["e1"])], "debug": {"limitations": []}}
        normalized, log = finalize_output(raw)
        self.assertEqual(normalized, raw)
        self.assertEqual(log["changed_candidate_count"], 0)

    def test_valid_zero_evidence_candidate_unchanged(self):
        raw = {"prompts": [candidate("p1", 0, {"setting": 0, "activity": 0,
               "materials": 0, "use_context": 0}, [], "creative_departure")],
               "debug": {"limitations": []}}
        normalized, log = finalize_output(raw)
        self.assertEqual(normalized, raw)
        self.assertEqual(log["changed_candidate_count"], 0)

    def test_stable_ranking_and_id_map(self):
        raw = {"prompts": [
            candidate("p1", 10, {"setting": 10, "activity": 0, "materials": 0, "use_context": 0}, ["e1"]),
            candidate("p2", 30, {"setting": 30, "activity": 0, "materials": 0, "use_context": 0}, ["e1"]),
            candidate("p3", 30, {"setting": 20, "activity": 10, "materials": 0, "use_context": 0}, ["e1"]),
        ], "debug": {"limitations": []}}
        normalized, log = finalize_output(raw)
        self.assertEqual([p["text"] for p in normalized["prompts"]], ["scene p2", "scene p3", "scene p1"])
        self.assertEqual([(x["original_id"], x["normalized_id"]) for x in log["id_map"]],
                         [("p2", "p1"), ("p3", "p2"), ("p1", "p3")])

    def test_hash_reconstruction_is_deterministic(self):
        raw = {"prompts": [candidate("p1", 10, {"setting": 10, "activity": 0,
               "materials": 0, "use_context": 0}, [])], "debug": {"limitations": []}}
        first, first_log = finalize_output(raw)
        second, second_log = finalize_output(raw)
        self.assertEqual(first, second)
        self.assertEqual(first_log, second_log)
        self.assertEqual(first_log["raw_output_semantic_sha256"], semantic_sha256(raw))
        self.assertEqual(first_log["normalized_output_semantic_sha256"], semantic_sha256(first))

    def test_wrong_unknown_camera_metadata_is_repaired_only_in_debug(self):
        raw = {"prompts": [candidate("p1", 0, {"setting": 0, "activity": 0,
               "materials": 0, "use_context": 0}, [], "creative_departure")],
               "debug": {"limitations": [], "camera": {"requested_tag": "futureType_NewView",
                   "resolved_tag": None, "device_type": None, "profile_version": self.registry["version"],
                   "resolution": "unknown", "framing": "tight", "elevation": "unspecified",
                   "max_local_props": 0, "max_background_details": 0, "people_policy": "omit"}}}
        normalized, log = finalize_output(raw,
            raw_input={"source_messaging": {}, "camera_tag": "futureType_NewView"}, registry=self.registry)
        self.assertEqual(normalized["prompts"], raw["prompts"])
        self.assertEqual((normalized["debug"]["camera"]["framing"],
                          normalized["debug"]["camera"]["elevation"]), ("unknown", "unknown"))
        self.assertEqual(log["camera_metadata_repair"]["original_camera"], raw["debug"]["camera"])

    def test_correct_known_camera_preserves_legacy_output_and_log(self):
        raw_input = {"source_messaging": {}, "camera_tag": "laptop_FrontRightWide"}
        resolved = resolve_profile(self.registry, raw_input["camera_tag"])
        camera = {"requested_tag": raw_input["camera_tag"], "resolved_tag": resolved["resolved_tag"],
                  "device_type": resolved["device_type"], "profile_version": resolved["profile_version"],
                  "resolution": resolved["resolution"], **resolved["effective_profile"]}
        raw = {"prompts": [candidate("p1", 0, {"setting": 0, "activity": 0,
               "materials": 0, "use_context": 0}, [], "creative_departure")],
               "debug": {"limitations": [], "camera": camera}}
        legacy_output, legacy_log = finalize_output(raw)
        normalized, log = finalize_output(raw, raw_input=raw_input, registry=self.registry)
        self.assertEqual(normalized, legacy_output)
        self.assertEqual(log, legacy_log)
        self.assertNotIn("camera_metadata_repair", log)

    def test_source_product_word_cannot_override_tag_and_scene_is_untouched(self):
        raw_input = {"source_messaging": {"KSP1": {"headline": "Printer workflow"}},
                     "camera_tag": "laptop_FrontRightWide"}
        raw = {"prompts": [candidate("p1", 0, {"setting": 0, "activity": 0,
               "materials": 0, "use_context": 0}, [], "creative_departure")],
               "debug": {"limitations": [], "camera": {"requested_tag": raw_input["camera_tag"],
                   "resolved_tag": "printer_FrontRightWide", "device_type": "printer",
                   "profile_version": self.registry["version"], "resolution": "exact", "framing": "wide",
                   "elevation": "oblique", "max_local_props": 3, "max_background_details": 2,
                   "people_policy": "optional_if_supported_and_unobtrusive"}}}
        normalized, log = finalize_output(raw, raw_input=raw_input, registry=self.registry)
        self.assertEqual(normalized["prompts"], raw["prompts"])
        self.assertEqual(normalized["debug"]["camera"]["device_type"], "laptop")
        self.assertIn("camera_metadata_repair", log)


if __name__ == "__main__":
    unittest.main()
