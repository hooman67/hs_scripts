"""Contract tests for the V5 progressive generation gallery."""

from __future__ import annotations

import json
import unittest

import build_gallery
import validate_gallery


class GalleryTests(unittest.TestCase):
    def test_progressive_gallery_contains_all_80_rows(self) -> None:
        build_record = build_gallery.build(build_gallery.DEFAULT_RUN_DIR, final=False)
        validation = validate_gallery.validate(build_gallery.DEFAULT_RUN_DIR, final=False)
        self.assertEqual(build_record["row_count"], 80)
        self.assertEqual(validation["row_count"], 80)
        self.assertEqual(validation["selection_counts"], {"ctech": 40, "smart_brief": 40})
        self.assertEqual(validation["corrected_input_count"], 4)
        self.assertEqual(validation["source_bank_count"], 8)
        self.assertTrue(validation["selection_filter_present"])
        self.assertTrue(validation["sensitive_material_absent"])

    def test_gallery_data_keeps_selection_and_score_metadata(self) -> None:
        data = validate_gallery.read_data(build_gallery.DEFAULT_RUN_DIR / "gallery/data.js")
        rows = data["rows"]
        self.assertEqual(len({row["candidate_key"] for row in rows}), 80)
        for row in rows:
            self.assertIn(row["selection_type"], {"ctech", "smart_brief"})
            self.assertIn("combined_source_relevance_score", row["candidate"])
            self.assertIn("ctech_similarity_score", row["candidate"])
            self.assertIn("smart_brief_score_components", row["candidate"])
            self.assertIn("source_messaging_score_components", row["candidate"])

    def test_final_validation_rejects_incomplete_inventory(self) -> None:
        data = validate_gallery.read_data(build_gallery.DEFAULT_RUN_DIR / "gallery/data.js")
        if data["metadata"]["status_counts"] == {"done": 80, "pending": 0, "failed": 0}:
            self.skipTest("Full authorized inventory is already complete")
        with self.assertRaisesRegex(ValueError, "Final gallery requires 80 done rows"):
            validate_gallery.validate(build_gallery.DEFAULT_RUN_DIR, final=True)


if __name__ == "__main__":
    unittest.main()
