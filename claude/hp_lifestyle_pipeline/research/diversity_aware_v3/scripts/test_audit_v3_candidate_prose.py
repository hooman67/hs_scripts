#!/usr/bin/env python3
"""Focused regressions for actual-prose candidate auditing."""

from __future__ import annotations

import unittest

import audit_v3_candidate_prose as audit


def candidate(text: str, props: list[str], backgrounds: list[str], people: list[str]) -> dict:
    return {
        "id": "p1",
        "candidate_key": "case::p1",
        "rank": 1,
        "text": text,
        "visual_signature": {
            "surface": "wood desk",
            "light": "daylight",
            "local_props": props,
            "background_details": backgrounds,
            "people": people,
        },
    }


class ProseAuditTests(unittest.TestCase):
    def test_person_must_replace_prop_at_full_budget(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A wood desk with a notebook and pen while a cropped hand sorts notes in daylight.",
                ["notebook", "pen"],
                [],
                ["cropped hand"],
            ),
            {"max_local_props": 2, "max_background_details": 1, "people_policy": "optional_partial_activity"},
        )
        codes = {finding["code"] for finding in value["findings"]}
        self.assertIn("people_activity_does_not_replace_a_prop", codes)
        self.assertEqual(value["actual_text_extraction"]["effective_prop_plus_people_count"], 3)

    def test_actual_unreported_objects_are_flagged(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A laminate desk with a notebook and small plant; shelving sits behind it.",
                ["notebook"],
                [],
                [],
            ),
            {"max_local_props": 3, "max_background_details": 2, "people_policy": "omit"},
        )
        codes = {finding["code"] for finding in value["findings"]}
        self.assertIn("actual_text_prop_missing_from_self_report", codes)
        self.assertIn("actual_text_background_missing_from_self_report", codes)

    def test_device_and_angle_terms_are_read_from_actual_text(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A right-side view of a printer on a plain oak worktop in daylight.",
                [],
                [],
                [],
            ),
            {"max_local_props": 0, "max_background_details": 0, "people_policy": "omit"},
        )
        codes = {finding["code"] for finding in value["findings"]}
        self.assertIn("device_term_in_actual_text", codes)
        self.assertIn("camera_or_angle_term_in_actual_text", codes)

    def test_surface_and_light_do_not_count_as_props(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A gently worn oak worktop with soft daylight against a plain background.",
                [],
                [],
                [],
            ),
            {"max_local_props": 0, "max_background_details": 0, "people_policy": "omit"},
        )
        self.assertEqual(value["actual_text_extraction"]["actual_prop_floor"], 0)
        self.assertFalse(value["findings"])

    def test_numbered_samples_expand_to_individual_prop_units(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A plywood table with a sketchbook and two paper samples in clear light.",
                ["sketchbook", "two paper samples"],
                [],
                [],
            ),
            {"max_local_props": 3, "max_background_details": 2, "people_policy": "optional_if_supported_and_unobtrusive"},
        )
        extraction = value["actual_text_extraction"]
        self.assertEqual(extraction["actual_prop_floor"], 3)
        self.assertEqual(extraction["reported_prop_units"], 3)
        self.assertEqual(extraction["effective_prop_count"], 3)
        codes = {finding["code"] for finding in value["findings"]}
        self.assertIn("self_report_list_length_undercounts_prop_units", codes)
        self.assertNotIn("actual_or_reported_prop_budget_exceeded", codes)

    def test_role_and_window_light_context_are_not_visible_entities(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A teacher planning desk with one worksheet in soft window-filtered light.",
                ["worksheet"],
                [],
                [],
            ),
            {"max_local_props": 1, "max_background_details": 0, "people_policy": "omit"},
        )
        extraction = value["actual_text_extraction"]
        self.assertEqual(extraction["people"], [])
        self.assertEqual(extraction["background_details"], [])
        self.assertFalse(value["findings"])

    def test_disclosed_object_can_be_lexically_classed_in_other_inventory(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A desk with a notebook; a wall calendar sits quietly behind it.",
                ["notebook"],
                ["wall calendar"],
                [],
            ),
            {"max_local_props": 1, "max_background_details": 1, "people_policy": "omit"},
        )
        codes = {finding["code"] for finding in value["findings"]}
        self.assertNotIn("actual_text_prop_missing_from_self_report", codes)

    def test_background_paper_does_not_inflate_local_prop_budget(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A desk with a notebook, pen, and folder; a tray of blank paper sits in the background.",
                ["notebook", "pen", "folder"],
                ["tray of blank paper"],
                [],
            ),
            {"max_local_props": 3, "max_background_details": 2, "people_policy": "omit"},
        )
        self.assertEqual(value["actual_text_extraction"]["effective_prop_count"], 3)
        codes = {finding["code"] for finding in value["findings"]}
        self.assertNotIn("actual_or_reported_prop_budget_exceeded", codes)

    def test_forms_folder_is_one_compound_prop(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A household records spot with one labeled forms folder on a wood table.",
                ["labeled forms folder"],
                [],
                [],
            ),
            {"max_local_props": 1, "max_background_details": 0, "people_policy": "omit"},
        )
        self.assertEqual(value["actual_text_extraction"]["effective_prop_count"], 1)
        self.assertFalse(value["findings"])

    def test_setting_label_noun_is_not_a_second_prop(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A forms review surface with one marked form sheet in task light.",
                ["marked form sheet"],
                [],
                [],
            ),
            {"max_local_props": 1, "max_background_details": 0, "people_policy": "omit"},
        )
        self.assertEqual(value["actual_text_extraction"]["effective_prop_count"], 1)
        self.assertFalse(value["findings"])

    def test_hand_drawn_is_not_a_visible_hand(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A table with a hand-drawn concept sheet in daylight.",
                ["hand-drawn concept sheet"],
                [],
                [],
            ),
            {"max_local_props": 2, "max_background_details": 0, "people_policy": "omit"},
        )
        self.assertEqual(value["actual_text_extraction"]["people"], [])

    def test_curtain_filtered_light_is_not_background_detail(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A desk with a notebook in soft curtain-filtered light.",
                ["notebook"],
                [],
                [],
            ),
            {"max_local_props": 1, "max_background_details": 0, "people_policy": "omit"},
        )
        self.assertEqual(value["actual_text_extraction"]["background_details"], [])

    def test_illuminated_from_above_is_not_camera_instruction(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A cork work surface softly illuminated from above.",
                [],
                [],
                [],
            ),
            {"max_local_props": 0, "max_background_details": 0, "people_policy": "omit"},
        )
        codes = {finding["code"] for finding in value["findings"]}
        self.assertNotIn("camera_or_angle_term_in_actual_text", codes)
        rules = {item["rule"] for item in audit.lexical_resolution_evidence(value["text"])}
        self.assertIn("illumination_from_above_is_not_camera_angle", rules)

    def test_surface_desktop_privacy_screen_and_paper_tray_are_not_devices(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A walnut desktop with a paper tray; a privacy screen sits behind it.",
                ["paper tray"],
                ["privacy screen"],
                [],
            ),
            {"max_local_props": 1, "max_background_details": 1, "people_policy": "omit"},
        )
        codes = {finding["code"] for finding in value["findings"]}
        self.assertNotIn("device_term_in_actual_text", codes)

    def test_folder_of_forms_is_one_compound_prop(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A table with a slim folder of practice forms in daylight.",
                ["slim folder of practice forms"],
                [],
                [],
            ),
            {"max_local_props": 1, "max_background_details": 0, "people_policy": "omit"},
        )
        self.assertEqual(value["actual_text_extraction"]["effective_prop_count"], 1)

    def test_tabbed_packet_matches_packet_marked_by_tab(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A counter with a packet marked by a simple tab in daylight.",
                ["tabbed packet"],
                [],
                [],
            ),
            {"max_local_props": 1, "max_background_details": 0, "people_policy": "omit"},
        )
        codes = {finding["code"] for finding in value["findings"]}
        self.assertNotIn("self_report_not_supported_by_actual_text_local_props", codes)

    def test_cropped_sleeve_is_people_slot_and_disclosed(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A counter with forms while a cropped sleeve reaches toward the tray.",
                ["forms"],
                [],
                ["cropped sleeve reaching toward the tray"],
            ),
            {"max_local_props": 2, "max_background_details": 0, "people_policy": "optional_partial_activity"},
        )
        self.assertEqual(value["actual_text_extraction"]["people_slot"], 1)
        codes = {finding["code"] for finding in value["findings"]}
        self.assertNotIn("self_report_not_supported_by_actual_text_people", codes)

    def test_curtain_filtered_daylight_is_not_background_detail(self) -> None:
        value = audit.audit_candidate(
            candidate(
                "A desk with a form in curtain-filtered daylight.",
                ["form"],
                [],
                [],
            ),
            {"max_local_props": 1, "max_background_details": 0, "people_policy": "omit"},
        )
        self.assertEqual(value["actual_text_extraction"]["background_details"], [])


if __name__ == "__main__":
    unittest.main()
