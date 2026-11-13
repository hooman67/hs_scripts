import copy
import unittest
from urllib.parse import urljoin

import report


class GroupedGalleryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = report.load(report.HERE / "source/comparison.json")

    def test_all_banks_preserve_exact_images_prompts_sources_and_ranks(self):
        source = copy.deepcopy(self.source)
        source["rows"].reverse()
        grouped = report.group_data(source)
        self.assertEqual(len(grouped["groups"]), 16)
        original = {tuple(row["key"]): row for row in self.source["rows"]}
        for group in grouped["groups"]:
            for experiment, (cell, _, prompt_field, input_field) in zip(group["experiments"], report.EXPERIMENTS):
                self.assertEqual([card["rank"] for card in experiment["cards"]], list(range(1, 11)))
                for card in experiment["cards"]:
                    row = original[(group["device_id"], group["camera_tag"], card["rank"])]
                    self.assertEqual(card["prompt"], row[prompt_field]["text"])
                    self.assertEqual(card["image_sha256"], row["outputs"][cell]["image_sha256"])
                    self.assertEqual(urljoin(report.VIEWER_URL, card["image"]),
                                     urljoin(report.SOURCE_URL, row["outputs"][cell]["image"]))
                context = group["contexts"][1 if cell == "v6_4_pr4523" else 0]["input"]
                self.assertEqual(context, row[input_field])

    def test_duplicate_rank_missing_rank_source_drift_and_prompt_tampering_fail(self):
        for mutation in ("duplicate", "missing", "source", "camera", "text"):
            with self.subTest(mutation=mutation):
                source = copy.deepcopy(self.source)
                if mutation == "duplicate":
                    source["rows"][-1] = source["rows"][0]
                elif mutation == "missing":
                    source["rows"].pop()
                elif mutation == "source":
                    source["rows"][1]["source_input_v6_4"]["smart_brief"]["changed"] = True
                elif mutation == "camera":
                    source["rows"][1]["prompt_v6_4"]["source_camera_name"] += " changed"
                else:
                    source["rows"][1]["prompt_v6_4"]["text"] += " changed"
                with self.assertRaises(ValueError):
                    report.group_data(source)


if __name__ == "__main__":
    unittest.main()
