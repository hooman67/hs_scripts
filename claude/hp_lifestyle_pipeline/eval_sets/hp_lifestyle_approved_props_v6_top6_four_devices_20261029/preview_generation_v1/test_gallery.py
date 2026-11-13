"""Contract and integrity tests for the V6 preview-generation gallery."""

from __future__ import annotations

import unittest
from pathlib import Path

import build_gallery
import validate_gallery


class V6PreviewGalleryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.build_record = build_gallery.build(build_gallery.DEFAULT_RUN_DIR, final=False)
        cls.validation = validate_gallery.validate(build_gallery.DEFAULT_RUN_DIR, final=False)
        cls.data = validate_gallery.read_data(build_gallery.DEFAULT_RUN_DIR / "gallery/data.js")

    def test_progressive_gallery_has_exact_inventory(self) -> None:
        self.assertEqual(self.build_record["row_count"], 160)
        self.assertEqual(self.build_record["generation_row_count"], 96)
        self.assertEqual(self.validation["row_count"], 160)
        self.assertEqual(self.validation["bank_count"], 16)
        self.assertEqual(self.validation["prompts_per_bank"], [10])
        self.assertEqual(self.validation["generated_image_count"], 96)
        self.assertEqual(self.validation["corrected_input_count"], 16)
        self.assertEqual(self.validation["source_bank_count"], 16)
        self.assertEqual(self.validation["download_count"], 6)

    def test_each_bank_has_ten_ranked_candidates_and_six_generated_outputs(self) -> None:
        self.assertEqual(len(self.data["banks"]), 16)
        for bank in self.data["banks"]:
            self.assertEqual(bank["candidate_count"], 10)
            self.assertEqual(bank["generated_selection_count"], 6)
            self.assertEqual(bank["prompt_only_count"], 4)
            rows = [next(row for row in self.data["rows"] if row["prompt_key"] == key) for key in bank["prompt_keys"]]
            self.assertEqual([row["candidate"]["bank_rank"] for row in rows], list(range(1, 11)))
            self.assertEqual([row["status"] for row in rows[6:]], ["prompt_only"] * 4)

    def test_all_source_documents_are_exact_r44_inputs(self) -> None:
        for bank_id, source in self.data["sources"].items():
            expected = build_gallery.INPUTS_DIR / f"{bank_id}.json"
            self.assertEqual(Path(source["input_path"]), expected.resolve())
            self.assertEqual(build_gallery.sha256_path(expected), source["input_sha256"])
            self.assertTrue(source["smart_brief"])
            self.assertTrue(source["source_messaging"])

    def test_prompt_scores_explanations_and_collapsed_details_are_present(self) -> None:
        self.assertEqual(len({row["prompt_key"] for row in self.data["rows"]}), 160)
        for row in self.data["rows"]:
            candidate = row["candidate"]
            self.assertIn("source_relevance_score", candidate)
            self.assertIn("ctech_reference_score", candidate)
            self.assertIn("score_components", candidate)
            self.assertIn("explanation", candidate)
        main = (build_gallery.TEMPLATE_DIR / "main.js").read_text(encoding="utf-8")
        for label in ("View Smart Brief", "View source messaging", "View explanation + score metadata", "View rewritten prompt", "View full debug / request"):
            self.assertIn(label, main)

    def test_sensitive_values_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Sensitive field"):
            build_gallery.assert_sanitized({"Authorization": "secret"})
        with self.assertRaisesRegex(ValueError, "Presigned credential"):
            build_gallery.assert_sanitized("https://example.invalid/a?X-Amz-Signature=secret")

    def test_final_validation_rejects_incomplete_inventory(self) -> None:
        statuses = self.data["metadata"]["status_counts"]
        if statuses == {"done": 96, "pending": 0, "failed": 0, "prompt_only": 64}:
            self.skipTest("The full authorized inventory is already complete")
        with self.assertRaisesRegex(ValueError, "Final gallery requires 96 generated"):
            validate_gallery.validate(build_gallery.DEFAULT_RUN_DIR, final=True)


if __name__ == "__main__":
    unittest.main()
