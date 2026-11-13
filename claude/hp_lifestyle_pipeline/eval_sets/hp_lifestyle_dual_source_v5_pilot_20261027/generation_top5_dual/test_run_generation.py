"""Offline contract tests for the V5 dual-selection image runner."""

from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("run_generation.py")
SPEC = importlib.util.spec_from_file_location("hp_v5_top5_dual_runner", SCRIPT)
runner = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


class RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        (
            cls.manifest,
            cls.manifest_sha,
            cls.selections,
            cls.review_by_key,
            cls.source_manifest,
            cls.source_manifest_sha,
            cls.binding_document,
            cls.binding_sha,
        ) = runner.load_inputs()
        cls.base = runner.load_base_runner(cls.manifest)

    def test_frozen_inputs_expand_to_80_unique_rows(self) -> None:
        rows = runner.build_rows(
            self.base, self.selections, self.review_by_key, self.source_manifest
        )
        self.assertEqual(len(rows), 80)
        self.assertEqual(len({row["row_id"] for row in rows}), 80)
        self.assertEqual(len({row["candidate_key"] for row in rows}), 80)
        self.assertEqual(
            {name: sum(row["selection_type"] == name for row in rows) for name in runner.EXPECTED_SELECTIONS},
            {"smart_brief": 40, "ctech": 40},
        )
        self.assertEqual({row["device_type"] for row in rows}, {"laptop", "printer"})

    def test_fixed_payload_and_selection_identity(self) -> None:
        rows = runner.build_rows(
            self.base, self.selections, self.review_by_key, self.source_manifest
        )
        selection_hashes = {
            item["selection_type"]: item["sha256"] for item in self.manifest["selections"]
        }
        runner.install_v5_engine_hooks(
            self.base,
            self.manifest,
            selection_hashes,
            self.manifest["review_data"]["sha256"],
            self.binding_sha,
        )
        payload = self.base.build_payload(rows[0], "blob-id")
        self.assertEqual(payload["size"], {"width": 2368, "height": 1776})
        self.assertEqual(payload["seeds"], [42])
        self.assertEqual(payload["n"], 1)
        self.assertEqual(payload["referenceBlobs"], [{"id": "blob-id"}])
        self.assertEqual(
            payload["modelSpecificPayload"],
            {
                "enablePromptRewrite": True,
                "rewriterModel": "gemini-3.1-pro",
                "numInferenceSteps": 50,
            },
        )
        self.assertIn(rows[0]["selection_type"], rows[0]["row_id"])

    def test_cross_selection_overlap_is_rejected(self) -> None:
        selections = copy.deepcopy(self.selections)
        selections["ctech"]["prompts"][0] = copy.deepcopy(
            selections["smart_brief"]["prompts"][0]
        )
        with self.assertRaisesRegex(ValueError, "Cross-selection overlap"):
            runner.build_rows(self.base, selections, self.review_by_key, self.source_manifest)

    def test_exact_four_blob_bindings_are_reused(self) -> None:
        rows = runner.build_rows(
            self.base, self.selections, self.review_by_key, self.source_manifest
        )
        bindings = runner.load_exact_bindings(
            self.base, rows, self.binding_document, self.source_manifest_sha
        )
        self.assertEqual(len(bindings), 4)
        self.assertEqual(
            {binding["blob_id"] for binding in bindings.values()},
            {
                "e1751062-caca-451d-b0d7-57001ee02cfa",
                "05c2d656-28bc-4a8f-a3cd-5c6f01f6b739",
                "b663c46f-0d38-43cf-b312-551f24109d58",
                "319e45bb-ce56-46a5-9982-06ffe1b4cfed",
            },
        )

    def test_blob_or_render_drift_is_rejected(self) -> None:
        rows = runner.build_rows(
            self.base, self.selections, self.review_by_key, self.source_manifest
        )
        binding_document = copy.deepcopy(self.binding_document)
        first = next(iter(binding_document["bindings"].values()))
        first["original_png_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "Exact blob binding mismatch"):
            runner.load_exact_bindings(
                self.base, rows, binding_document, self.source_manifest_sha
            )

    def test_selection_filter_is_exact(self) -> None:
        rows = runner.build_rows(
            self.base, self.selections, self.review_by_key, self.source_manifest
        )
        selected = runner.select_rows(rows, [], "smart_brief", False)
        self.assertEqual(len(selected), 40)
        self.assertEqual({row["selection_type"] for row in selected}, {"smart_brief"})
        self.assertEqual(runner.select_rows(rows, [], None, False), [])


if __name__ == "__main__":
    unittest.main()
