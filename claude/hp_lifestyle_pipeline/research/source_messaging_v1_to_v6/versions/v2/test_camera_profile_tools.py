#!/usr/bin/env python3
"""Tests for the camera-v2 type-camera compiler and resolver."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_system_prompt import PLACEHOLDER, build_offline_notes, compile_prompt
from camera_profile_resolver import (
    MINIMAL_FALLBACK,
    PROFILE_FIELDS,
    RegistryError,
    load_registry,
    resolve_profile,
    validate_registry,
)


class CameraProfileToolsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry()

    def test_every_registered_profile_resolves_exactly(self) -> None:
        for profile in self.registry["profiles"]:
            with self.subTest(tag=profile["tag"]):
                result = resolve_profile(self.registry, profile["tag"])
                self.assertEqual(result["resolution"], "exact")
                self.assertEqual(result["resolved_tag"], profile["tag"])
                self.assertEqual(result["device_type"], profile["device_family"])
                self.assertEqual(
                    result["source_camera_name"], profile["source_camera_name"]
                )
                self.assertFalse(result["used_minimal_fallback"])

    def test_case_and_surrounding_whitespace_are_exact_normalization(self) -> None:
        result = resolve_profile(self.registry, "  LAPTOP_backcloseup  ")
        self.assertEqual(result["resolution"], "exact")
        self.assertEqual(result["resolved_tag"], "laptop_BackCloseUp")
        self.assertEqual(result["device_type"], "laptop")

    def test_explicit_legacy_alias_resolves_without_fuzzy_matching(self) -> None:
        alias = resolve_profile(self.registry, " miniPC_Back_CloseUp ")
        self.assertEqual(alias["resolution"], "alias")
        self.assertEqual(alias["resolved_tag"], "miniPC_BackCloseUp")
        self.assertEqual(alias["device_type"], "miniPC")
        inferred = resolve_profile(self.registry, "miniPC Back CloseUp")
        self.assertEqual(inferred["resolution"], "unknown")
        self.assertIsNone(inferred["resolved_tag"])

    def test_unknown_and_missing_camera_use_minimal_fallback(self) -> None:
        for value, expected_resolution in (
            ("projector_FrontRightMedium", "unknown"),
            (None, "missing"),
            ("   ", "missing"),
        ):
            with self.subTest(value=value):
                result = resolve_profile(self.registry, value)
                self.assertEqual(result["resolution"], expected_resolution)
                self.assertEqual(result["effective_profile"], MINIMAL_FALLBACK)
                self.assertIsNone(result["device_type"])
                self.assertTrue(result["used_minimal_fallback"])

    def test_source_copy_cannot_change_registered_device_type(self) -> None:
        result = resolve_profile(self.registry, "miniPC_FrontRightMedium")
        self.assertEqual(result["device_type"], "miniPC")
        self.assertEqual(result["resolution"], "exact")

    def test_cross_type_camera_alias_is_rejected(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["aliases"]["printer_CrossTypeLegacy"] = "miniPC_BackCloseUp"
        with self.assertRaisesRegex(RegistryError, "crosses device types"):
            validate_registry(registry)

    def test_future_registered_device_type_is_generic(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["device_types"].append("projector")
        profile = copy.deepcopy(registry["profiles"][0])
        profile.update(
            {
                "tag": "projector_FrontMedium",
                "source_camera_name": "Front_Medium",
                "device_family": "projector",
                "framing": "medium",
                "elevation": "level",
                "max_local_props": 1,
                "max_background_details": 1,
                "people_policy": "optional_partial_activity",
            }
        )
        registry["profiles"].append(profile)
        result = resolve_profile(registry, " PROJECTOR_frontmedium ")
        self.assertEqual(result["resolution"], "exact")
        self.assertEqual(result["device_type"], "projector")
        notes = build_offline_notes(registry)
        self.assertIn("`projector_FrontMedium`", notes)
        self.assertIn("Registered device types", notes)

    def test_compiler_is_deterministic_complete_compact_and_product_free(self) -> None:
        notes_a = build_offline_notes(self.registry)
        notes_b = build_offline_notes(copy.deepcopy(self.registry))
        self.assertEqual(notes_a, notes_b)
        for profile in self.registry["profiles"]:
            self.assertIn(f"`{profile['tag']}`", notes_a)
        for alias, target in self.registry["aliases"].items():
            self.assertIn(f"{alias} -> {target}", notes_a)
        self.assertNotIn("product=", notes_a.casefold())
        self.assertNotIn("product override", notes_a.casefold())
        raw_dump = json.dumps(self.registry, indent=2)
        self.assertLess(len(notes_a), len(raw_dump) * 0.55)
        template = "before\n" + PLACEHOLDER + "\nafter\n"
        compiled = compile_prompt(template, self.registry)
        self.assertNotIn(PLACEHOLDER, compiled)
        self.assertEqual(compiled, compile_prompt(template, self.registry))

    def test_compiler_groups_equal_profiles_for_every_registered_type(self) -> None:
        notes = build_offline_notes(self.registry)
        source_profiles = [
            profile
            for profile in self.registry["profiles"]
            if profile["source_camera_name"] == "Back_CloseUp"
        ]
        signatures = {
            tuple(profile[field] for field in PROFILE_FIELDS)
            for profile in source_profiles
        }
        self.assertEqual(notes.count("source=`Back_CloseUp`"), len(signatures))
        for profile in source_profiles:
            self.assertIn(f"`{profile['tag']}`", notes)

    def test_top_oblique_background_is_capped_last(self) -> None:
        registry = copy.deepcopy(self.registry)
        profile = next(
            item
            for item in registry["profiles"]
            if item["tag"] == "miniPC_TopFrontMedium"
        )
        profile["max_background_details"] = 2
        result = resolve_profile(registry, profile["tag"])
        self.assertEqual(result["effective_profile"]["max_background_details"], 0)
        self.assertIn(
            "top_oblique_max_background_details_capped_at_0",
            result["restrictions_applied"],
        )

    def test_profile_specific_notes_remain_tag_scoped(self) -> None:
        notes = build_offline_notes(self.registry)
        specific = "Opaque review tag"
        evidence_boundary = notes.split("### Camera base profiles", 1)[0]
        self.assertNotIn(specific, evidence_boundary)
        matching_lines = [line for line in notes.splitlines() if specific in line]
        self.assertGreaterEqual(len(matching_lines), 1)
        self.assertTrue(any("CAMReview`" in line for line in matching_lines))


if __name__ == "__main__":
    unittest.main()
