#!/usr/bin/env python3
"""Focused checks for generic source-declared device-type parsing."""

from __future__ import annotations

import json
import unittest
from pathlib import Path, PurePosixPath

from build_camera_catalog import (
    UNKNOWN_TYPE_APPROVAL_STATUS,
    PDF_SPECS,
    page_device_name,
    parse_asset_folder,
    pdf_page_approval,
)


DATA = Path(__file__).resolve().parents[1] / "data"


class SourceParserTests(unittest.TestCase):
    def test_current_mislabeled_folder_preserves_printer_declaration(self) -> None:
        self.assertEqual(
            parse_asset_folder(
                "camera_printer.locator_Messi_Ceramic-White.printer"
            ),
            ("printer", "Messi_Ceramic-White.printer"),
        )

    def test_corrected_future_minipc_export_is_accepted_literally(self) -> None:
        folder = "camera_miniPC.locator_Messi_Ceramic-White.miniPC"
        self.assertEqual(
            parse_asset_folder(folder),
            ("miniPC", "Messi_Ceramic-White.miniPC"),
        )
        self.assertEqual(
            page_device_name("Messi_Ceramic-White.miniPC.usdz [miniPC]\n"),
            ("Messi_Ceramic-White.miniPC.usdz", "miniPC"),
        )

    def test_unknown_valid_future_type_is_retained_without_approval_guess(self) -> None:
        self.assertEqual(
            parse_asset_folder("camera_spatialDock2.locator_Concept-A.spatialDock2"),
            ("spatialDock2", "Concept-A.spatialDock2"),
        )
        status, scope = pdf_page_approval(PDF_SPECS[0], "spatialDock2")
        self.assertEqual(status, UNKNOWN_TYPE_APPROVAL_STATUS)
        self.assertIn("spatialDock2", scope)

    def test_folder_prefix_and_asset_suffix_types_must_match(self) -> None:
        self.assertIsNone(
            parse_asset_folder("camera_miniPC.locator_Messi_Ceramic-White.printer")
        )

    def test_all_243_current_assets_keep_their_declared_classification(self) -> None:
        catalog = json.loads((DATA / "camera_catalog.json").read_text(encoding="utf-8"))
        assets = catalog["high_resolution_assets"]
        self.assertEqual(len(assets), 243)
        for asset in assets:
            folder = PurePosixPath(asset["zip_filename"]).parts[1]
            parsed = parse_asset_folder(folder)
            self.assertIsNotNone(parsed, asset["zip_filename"])
            declared_type, device_stem = parsed
            self.assertEqual(declared_type, asset["source_declared_device_type"])
            self.assertEqual(device_stem + ".usdz", asset["device_asset_name_from_folder"])


if __name__ == "__main__":
    unittest.main()
