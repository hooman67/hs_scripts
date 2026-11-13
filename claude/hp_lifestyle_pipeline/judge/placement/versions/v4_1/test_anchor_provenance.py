#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

import run_judge
from scoring import PlacementValidationError

ROOT = Path(__file__).resolve().parent


class AnchorProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "data/development_15_manifest.json").read_text())
        cls.records = {r["id"]: r for r in cls.manifest["records"]}

    @staticmethod
    def runtime(record):
        return {
            "generated_image": record["generated_image"]["local_path"],
            "twin_image": record["twin_image"]["local_path"],
            "product_type": record["device_type"],
            "scene_prompt": record["scene_prompt"],
            "image_stage": record["image_stage"],
        }

    def test_every_target_has_four_provenance_checked_leave_family_out_anchors(self):
        for target_id, record in self.records.items():
            runtime = self.runtime(record)
            selected = run_judge._target_anchor_selection(target_id, runtime)
            plan = run_judge.ANCHOR_TARGETS[target_id]
            self.assertEqual([a["anchor_id"] for a in selected], plan["selected_anchor_ids"])
            self.assertEqual(len(selected), 4)
            for anchor in selected:
                self.assertNotEqual(anchor["generated_image_sha256"], record["generated_image"]["sha256"])
                self.assertNotEqual(anchor["twin_image_sha256"], record["twin_image"]["sha256"])
                self.assertNotEqual(anchor["scene_prompt_sha256"], record["scene_prompt_sha256"])
                self.assertNotEqual(anchor["exact_family"], plan["target_exact_family"])
                self.assertNotEqual(anchor["near_duplicate_family"], plan["target_near_duplicate_family"])

    def test_target_metadata_contains_no_target_label_comment_score_or_verdict(self):
        record = next(iter(self.records.values()))
        runtime = self.runtime(record)
        selected = run_judge._target_anchor_selection(record["id"], runtime)
        content = run_judge._content(runtime, record["id"], selected)
        marker = next(i for i, item in enumerate(content) if item.get("text", "").startswith("TARGET INPUT"))
        metadata = json.loads(content[marker + 1]["text"])
        self.assertEqual(set(metadata), {"target_record_id", "product_type", "scene_prompt", "image_stage"})
        forbidden = {"comment", "label", "verdict", "score", "expected_issue"}
        self.assertTrue(forbidden.isdisjoint(metadata))

    def test_target_provenance_mismatch_is_rejected(self):
        record = next(iter(self.records.values()))
        runtime = self.runtime(record)
        runtime["scene_prompt"] += " tampered"
        with self.assertRaises(PlacementValidationError):
            run_judge._target_anchor_selection(record["id"], runtime)


if __name__ == "__main__":
    unittest.main()
