#!/usr/bin/env python3
"""Camera-v2 compiler/resolver tests.

Run from the project root with:
python3 -m unittest discover -s research/source_messaging/versions/v2 -p 'test_camera_profile_tools.py' -v
"""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_system_prompt import PLACEHOLDER, build_offline_notes, compile_prompt
from camera_profile_resolver import MINIMAL_FALLBACK, load_registry, resolve_profile


class CameraProfileToolsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry()

    def test_every_registered_supported_pair_resolves(self) -> None:
        for product in self.registry["products"]:
            for tag in product["supported_camera_tags"]:
                with self.subTest(product=product["product_name"], tag=tag):
                    result = resolve_profile(self.registry, tag, product["product_name"])
                    self.assertEqual(result["resolution"], "exact")
                    self.assertEqual(result["product_resolution"], "exact")
                    self.assertFalse(result["used_minimal_fallback"])
                    self.assertEqual(result["resolved_tag"], tag)
                    profile = next(
                        item for item in self.registry["profiles"] if item["tag"] == tag
                    )
                    self.assertEqual(
                        result["source_camera_name"], profile["source_camera_name"]
                    )

    def test_case_and_surrounding_whitespace_are_exact_normalization(self) -> None:
        result = resolve_profile(
            self.registry,
            "  laptop_back_closeup  ",
            "  cashmere-elitebookx-14_atmospheric-blue.LAPTOP.usdz ",
        )
        self.assertEqual(result["resolution"], "exact")
        self.assertEqual(result["product_resolution"], "exact")
        self.assertEqual(result["resolved_tag"], "Laptop_Back_CloseUp")

    def test_explicit_product_alias(self) -> None:
        result = resolve_profile(self.registry, "Laptop_Back_CloseUp", " cashmere ")
        self.assertEqual(result["product_resolution"], "alias")
        self.assertEqual(
            result["resolved_product"],
            "Cashmere-ElitebookX-14_Atmospheric-Blue.laptop.usdz",
        )

    def test_unknown_camera_uses_minimal_fallback(self) -> None:
        result = resolve_profile(self.registry, "Laptop_Not_A_Real_View", "Cashmere")
        self.assertEqual(result["resolution"], "unknown")
        self.assertEqual(result["product_resolution"], "alias")
        self.assertEqual(result["effective_profile"], MINIMAL_FALLBACK)
        self.assertTrue(result["used_minimal_fallback"])

    def test_family_conflict_is_incompatible(self) -> None:
        result = resolve_profile(self.registry, "Printer_Back_CloseUp", "Cashmere")
        self.assertEqual(result["product_resolution"], "incompatible")
        self.assertEqual(
            result["incompatible_reason"],
            "product_family_conflicts_with_camera_family",
        )
        self.assertEqual(result["effective_profile"], MINIMAL_FALLBACK)

    def test_unknown_product_keeps_known_camera_base_without_override(self) -> None:
        result = resolve_profile(
            self.registry, "Printer_Back_CloseUp", "not a registered product"
        )
        self.assertEqual(result["resolution"], "exact")
        self.assertEqual(result["product_resolution"], "unknown")
        self.assertEqual(result["resolved_product"], None)
        self.assertEqual(result["effective_profile"]["framing"], "tight")
        self.assertEqual(result["effective_profile"]["max_local_props"], 0)
        self.assertFalse(result["applied_overrides"])
        self.assertFalse(result["used_minimal_fallback"])

    def test_same_family_unsupported_camera_is_incompatible(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["products"][0]["supported_camera_tags"].remove("Laptop_Back_CloseUp")
        result = resolve_profile(
            registry,
            "Laptop_Back_CloseUp",
            registry["products"][0]["product_name"],
        )
        self.assertEqual(result["product_resolution"], "incompatible")
        self.assertEqual(result["incompatible_reason"], "camera_not_supported_by_product")

    def test_messi_override_then_top_oblique_geometry_cap(self) -> None:
        regular = resolve_profile(self.registry, "Printer_Back_CloseUp", "Messi")
        self.assertEqual(regular["effective_profile"]["framing"], "medium")
        self.assertEqual(regular["effective_profile"]["max_local_props"], 2)
        self.assertEqual(regular["effective_profile"]["max_background_details"], 1)

        top = resolve_profile(self.registry, "Printer_Top_Front_CloseUp", "Messi")
        self.assertEqual(top["effective_profile"]["elevation"], "top_oblique")
        self.assertEqual(top["effective_profile"]["framing"], "medium")
        self.assertEqual(top["effective_profile"]["max_background_details"], 0)
        self.assertIn(
            "top_oblique_max_background_details_capped_at_0",
            top["restrictions_applied"],
        )

    def test_viktor_override(self) -> None:
        result = resolve_profile(self.registry, "Laptop_Front_Right_CloseUp", "Viktor")
        self.assertEqual(result["effective_profile"]["max_local_props"], 0)
        self.assertEqual(result["effective_profile"]["max_background_details"], 0)
        self.assertEqual(len(result["applied_overrides"]), 1)

    def test_explicit_camera_alias_only(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["aliases"]["Laptop Back CU"] = "Laptop_Back_CloseUp"
        alias = resolve_profile(registry, " laptop back cu ", "Cashmere")
        self.assertEqual(alias["resolution"], "alias")
        inferred = resolve_profile(registry, "Laptop Back CloseUp", "Cashmere")
        self.assertEqual(inferred["resolution"], "unknown")

    def test_compiler_is_deterministic_complete_and_compact(self) -> None:
        notes_a = build_offline_notes(self.registry)
        notes_b = build_offline_notes(copy.deepcopy(self.registry))
        self.assertEqual(notes_a, notes_b)
        for profile in self.registry["profiles"]:
            self.assertIn(f"`{profile['tag']}`", notes_a)
            self.assertIn(f"source=`{profile['source_camera_name']}`", notes_a)
        for product in self.registry["products"]:
            self.assertIn(f"`{product['product_name']}`", notes_a)
            for alias in product["aliases"]:
                self.assertIn(f"`{alias}`", notes_a)
        # Notes remain far below a raw pretty-printed registry dump.
        raw_dump = __import__("json").dumps(self.registry, indent=2)
        self.assertLess(len(notes_a), len(raw_dump) * 0.55)
        self.assertNotIn("Support group 3", notes_a)

        template = "before\n" + PLACEHOLDER + "\nafter\n"
        compiled = compile_prompt(template, self.registry)
        self.assertNotIn(PLACEHOLDER, compiled)
        self.assertEqual(compiled, compile_prompt(template, self.registry))

    def test_compiler_deduplicates_only_equal_family_profiles(self) -> None:
        registry = copy.deepcopy(self.registry)
        printer = next(
            item for item in registry["profiles"] if item["tag"] == "Printer_Back_CloseUp"
        )
        printer["max_local_props"] = 1
        notes = build_offline_notes(registry)
        self.assertEqual(notes.count("source=`Back_CloseUp`"), 2)

    def test_profile_specific_notes_remain_tag_scoped(self) -> None:
        notes = build_offline_notes(self.registry)
        specific = "Reviewed printer render shows a near-level side face"
        evidence_boundary = notes.split("### Camera base profiles", 1)[0]
        self.assertNotIn(specific, evidence_boundary)
        matching_lines = [line for line in notes.splitlines() if specific in line]
        self.assertEqual(len(matching_lines), 1)
        self.assertIn("`Printer_Right_CloseUp`", matching_lines[0])


if __name__ == "__main__":
    unittest.main()
