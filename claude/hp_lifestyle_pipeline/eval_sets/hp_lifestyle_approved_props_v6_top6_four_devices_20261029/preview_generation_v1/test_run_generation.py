from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_runner():
    spec = importlib.util.spec_from_file_location("v6_preview_runner_test", HERE / "run_generation.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class V6PreviewRunnerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = load_runner()
        cls.manifest, cls.manifest_sha, cls.prompts, cls.prompts_sha = cls.runner.load_inputs()
        cls.base = cls.runner.load_base(cls.manifest)
        cls.runner.install_hooks(cls.base, cls.manifest, cls.prompts_sha)
        cls.rows = cls.runner.build_rows(cls.base, cls.manifest, cls.prompts)

    def test_frozen_inventory(self) -> None:
        self.assertEqual(len(self.rows), 96)
        self.assertEqual(len({row["prompt_key"] for row in self.rows}), 96)
        self.assertEqual(len({row["render_id"] for row in self.rows}), 16)
        counts = {}
        for row in self.rows:
            key = (row["device_id"], row["camera_tag"])
            counts[key] = counts.get(key, 0) + 1
        self.assertEqual(len(counts), 16)
        self.assertEqual(set(counts.values()), {6})

    def test_exact_preview_request_contract(self) -> None:
        payload = self.base.build_payload(self.rows[0], "blob-id")
        self.assertEqual(payload["prompt"], self.rows[0]["candidate"]["text"])
        self.assertEqual(payload["size"], {"width": 2368, "height": 1776})
        self.assertEqual(payload["referenceBlobs"], [{"id": "blob-id"}])
        self.assertEqual(payload["seeds"], [42])
        self.assertEqual(payload["n"], 1)
        self.assertEqual(
            payload["modelSpecificPayload"],
            {
                "enablePromptRewrite": True,
                "rewriterModel": "gemini-3.1-pro",
                "numInferenceSteps": 50,
            },
        )

    def test_preview_endpoint_not_e2e(self) -> None:
        model = self.manifest["model"]
        self.assertIn("-8000.", model["base_url"])
        self.assertNotIn("-8016.", model["base_url"])
        self.assertEqual(model["model_id"], "hp-image")

    def test_product_specific_bindings(self) -> None:
        for row in self.rows:
            render = row["render"]
            self.assertEqual(render["device_id"], row["device_id"])
            self.assertEqual(render["camera_tag"], row["camera_tag"])
            self.assertEqual(render["camera_name"], row["candidate"]["source_camera_name"])
            self.assertEqual((render["width"], render["height"]), (2368, 1776))
            self.assertEqual(self.runner.sha256_path(Path(render["path"])), render["sha256"])


if __name__ == "__main__":
    unittest.main()
