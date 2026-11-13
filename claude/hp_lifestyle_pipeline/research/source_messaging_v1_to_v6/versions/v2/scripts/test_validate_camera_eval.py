#!/usr/bin/env python3

from __future__ import annotations

import unittest

from validate_camera_eval import find_target_device_terms


class TargetDeviceTermsTest(unittest.TestCase):
    def test_wooden_desktop_surface_is_allowed(self) -> None:
        text = "A small section of matte wooden desktop in soft daylight."
        self.assertEqual(find_target_device_terms(text), [])

    def test_wooden_desktop_computer_is_still_rejected(self) -> None:
        text = "A wooden desktop computer beside the papers."
        terms = [item.casefold() for item in find_target_device_terms(text)]
        self.assertIn("desktop", terms)
        self.assertIn("computer", terms)

    def test_phone_and_computing_tablet_are_rejected(self) -> None:
        terms = [
            item.casefold()
            for item in find_target_device_terms(
                "A phone and a tablet sit beside the papers."
            )
        ]
        self.assertIn("phone", terms)
        self.assertIn("tablet", terms)

    def test_tabletop_and_game_controller_remain_allowed(self) -> None:
        text = "A wooden tabletop with a game controller in soft daylight."
        self.assertEqual(find_target_device_terms(text), [])


if __name__ == "__main__":
    unittest.main()
