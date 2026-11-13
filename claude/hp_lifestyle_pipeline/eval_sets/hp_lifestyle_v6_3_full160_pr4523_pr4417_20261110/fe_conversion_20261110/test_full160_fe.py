import copy
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("hp_full160_fe_converter", Path(__file__).with_name("convert.py"))
convert = importlib.util.module_from_spec(spec)
spec.loader.exec_module(convert)


class ConversionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((convert.PUBLIC / "data/comparison.json").read_text())

    def test_preserves_every_pair_in_version_order_without_extra_content(self):
        data = convert.convert(self.source)
        self.assertEqual(len(data["rows"]), 160)
        for source, row in zip(self.source["rows"], data["rows"]):
            self.assertEqual(row["meta_data"]["evalset_item_id"], source["prompt"]["prompt_key"])
            self.assertIsNone(row["meta_data"]["key_val_informations"])
            self.assertEqual([a["image_src"] for a in row["images"]], [
                convert.media_url(source["outputs"][name]["image"]) for name, _ in convert.CELLS
            ])
            self.assertEqual([a["meta_text"] for a in row["images"]], [{"label": "V15.6"}, {"label": "V15.7"}])
            self.assertTrue(all(set(a) == {"asset_type", "image_src", "meta_text"} for a in row["images"]))
        self.assertEqual(set(data), {"is_secure", "meta_texts", "rows"})

    def test_rejects_duplicate_rows_wrong_pipeline_and_prompt_mismatch(self):
        for problem, message in (("duplicate", "duplicate comparison"), ("pipeline", "wrong pinned"),
                                 ("prompt", "source prompt binding")):
            with self.subTest(problem=problem):
                source = copy.deepcopy(self.source)
                if problem == "duplicate":
                    source["rows"][1] = source["rows"][0]
                elif problem == "pipeline":
                    source["rows"][0]["outputs"]["v6_3_pr4523"]["lineage"]["source_commit"] = "wrong"
                else:
                    source["rows"][0]["prompt"]["text"] += " changed"
                with self.assertRaisesRegex(ValueError, message):
                    convert.convert(source)

    def test_rejects_incomplete_images_and_assets_outside_the_study(self):
        source = copy.deepcopy(self.source)
        source["rows"][0]["outputs"]["v6_3_pr4417"]["status"] = "pending"
        with self.assertRaisesRegex(ValueError, "incomplete comparison"):
            convert.convert(source)
        for value in ("https://example.com/image.png", "../data/comparison.json", ""):
            with self.subTest(value=value), self.assertRaises(ValueError):
                convert.media_url(value)
