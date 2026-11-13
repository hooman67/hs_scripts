"""Verify exact row matching and preservation of the live four-column comparison."""
import copy
import unittest

import update


class ColumnUpdateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = update.load(update.HERE / "snapshot/target/data/comparison.json")
        cls.new = update.load(update.HERE / "snapshot/source/data/generation.json")

    def test_existing_rows_and_sections_are_preserved(self):
        reordered = copy.deepcopy(self.new)
        reordered["rows"].reverse()
        merged = update.merge(self.old, reordered)
        restored = copy.deepcopy(merged)
        for row in restored["rows"]:
            del row["prompts"]["v6_4"]
            del row["outputs"][update.CELL]
            del row["v6_4_source_input"]
        del restored["cells"][update.CELL]
        for field in ("actual_input_audits", "built_at_utc"):
            restored[field] = self.old[field]
        self.assertEqual(restored, self.old)
        self.assertEqual(merged["actual_input_audits"], 150)
        for row, source in zip(merged["rows"], self.new["rows"]):
            output = row["outputs"][update.CELL]
            self.assertEqual(row["prompts"]["v6_4"], source["prompt"])
            self.assertEqual(row["v6_4_source_input"], source["source_input"])
            self.assertEqual(output["job_id"], source["output"]["job_id"])
            self.assertEqual(output["image_sha256"], source["output"]["image_sha256"])
            self.assertEqual(output["guide"], output["inputs"]["geometry_guide"])
            self.assertEqual(update.urljoin(update.BASE, output["image"]),
                             update.urljoin(update.SOURCE_BASE, source["output"]["image"]))

    def test_duplicate_slot_is_rejected(self):
        source = copy.deepcopy(self.new)
        source["rows"][-1] = source["rows"][0]
        with self.assertRaisesRegex(ValueError, "unique device/camera/rank slots"):
            update.merge(self.old, source)

    def test_camera_drift_and_prompt_tampering_are_rejected(self):
        for field in ("source_camera_name", "text"):
            with self.subTest(field=field):
                source = copy.deepcopy(self.new)
                source["rows"][0]["prompt"][field] += " changed"
                with self.assertRaises(ValueError):
                    update.merge(self.old, source)


if __name__ == "__main__":
    unittest.main()
