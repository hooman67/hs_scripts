"""Verify exact original-column preservation and slot-based full160 matching."""
import copy
import unittest

import extend_comparisons as extension
import study


class ExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = study.load(study.HERE / "baseline_live/full160/data/comparison.json")
        cls.fe = study.load(study.HERE / "baseline_live/full160/fe/data.json")
        cls.source = study.load(study.HERE / "public/data/generation.json")

    def test_existing_gallery_is_identical_after_removing_the_extension(self):
        reordered = {**self.source, "rows": list(reversed(self.source["rows"]))}
        merged = extension.merge(self.old, reordered)
        restored = copy.deepcopy(merged)
        for row in restored["rows"]:
            for name in ("prompt_v6_4", "source_input_v6_4", "bank_audit_v6_4"):
                del row[name]
            del row["outputs"][extension.CELL]
        del restored["cells"][extension.CELL]
        for field in ("actual_input_audits", "built_at_utc"):
            restored[field] = self.old[field]
        self.assertEqual(restored, self.old)
        expected = {tuple(row["key"]): row for row in self.source["rows"]}
        for row in merged["rows"]:
            self.assertEqual(row["prompt_v6_4"], expected[tuple(row["key"])]["prompt"])
            self.assertEqual(row["outputs"][extension.CELL]["image_sha256"],
                             expected[tuple(row["key"])]["output"]["image_sha256"])

    def test_fe_preserves_existing_images_metadata_and_annotation_ids(self):
        result = extension.fe_merge(self.fe, self.old, self.source)
        restored = copy.deepcopy(result)
        by_slot = {tuple(row["key"]): row for row in self.source["rows"]}
        for index, row in enumerate(restored["rows"]):
            image = row["images"].pop()
            self.assertEqual(image["image_src"], by_slot[tuple(self.old["rows"][index]["key"])]["output"]["image"])
            self.assertEqual(image["meta_text"]["label"], study.TITLE)
        restored["meta_texts"] = self.fe["meta_texts"]
        self.assertEqual(restored, self.fe)

    def test_duplicate_slots_and_camera_drift_fail(self):
        for mutation in ("duplicate", "camera"):
            with self.subTest(mutation=mutation):
                source = copy.deepcopy(self.source)
                if mutation == "duplicate":
                    source["rows"][-1] = source["rows"][0]
                else:
                    source["rows"][0]["prompt"]["source_camera_name"] += " changed"
                with self.assertRaises(ValueError):
                    extension.merge(self.old, source)


if __name__ == "__main__":
    unittest.main()
