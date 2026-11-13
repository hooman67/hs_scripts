from __future__ import annotations

from pathlib import Path
import sys

VERSION = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(VERSION.parent))

from v6_2 import validation


def test_printer_office_support_accepts_natural_office_modifier() -> None:
    pattern = validation._PRINTER_SUPPORT_RE["Office"]
    assert pattern.search("A substantial side table stands against the wall.")
    assert pattern.search("A substantial office side table stands against the wall.")


def test_printer_support_rejects_desks_and_personal_workstations() -> None:
    pattern = validation._PRINTER_FORBIDDEN_SURFACE_RE
    assert pattern.search("An occupied desk sits beside the window.")
    assert pattern.search("A personal workstation fills the corner.")
    assert not pattern.search("A dedicated output table sits beside the wall.")


def test_empty_shelving_and_pegboards_are_detected() -> None:
    pattern = validation._EMPTY_SHELF_RE
    assert pattern.search("Empty shelving lines the wall.")
    assert pattern.search("A pegboard is left blank above the table.")
    assert not pattern.search("Shelving holds unlabelled ceramics.")
    assert validation._POPULATED_SHELF_RE.search(
        "A floating shelf holds small unlabelled pigment jars."
    )


def test_system_prompt_contains_late_ctech_rules() -> None:
    prompt = (VERSION / "system_prompt.md").read_text(encoding="utf-8")
    assert "Never ask for empty or blank shelving or pegboards." in prompt
    assert "Never use a desk or personal workstation as the primary printer-tag support." in prompt
    assert "Never copy an unresolved choice into scene text" in prompt
    assert "In every laptop bank, make at least one support a natural round or circular table" in prompt
    assert "When a wall is plausibly visible" in prompt
    assert "Never ask for an empty or blank wall-mounted board" in prompt
    assert "Do not maroon a small rectangular table" in prompt
    assert "Keep a printer's rectilinear support" in prompt
    assert "Do not align a chair or stool with the printer table" in prompt
    assert "keep personal, leisure, learning, and creative activity props off that support" in prompt


def test_visible_or_choices_are_rejected_but_safety_and_quantity_are_allowed() -> None:
    assert validation._find_unresolved_scene_alternative(
        "A classroom or library chair sits behind the table."
    )


def test_round_support_detection_is_bounded_to_table_shapes() -> None:
    assert validation._ROUND_SUPPORT_RE.search(
        "A round wooden café table sits in an open seating area."
    )
    assert validation._ROUND_SUPPORT_RE.search(
        "A circular collaborative study table sits near the library wall."
    )
    assert not validation._ROUND_SUPPORT_RE.search(
        "A round ceramic coaster rests on a rectangular office worktable."
    )


def test_printer_floor_clutter_detection() -> None:
    assert validation._PRINTER_RANDOM_FLOOR_PROP_RE.search(
        "A jigsaw puzzle rests on the rug beneath the utility table."
    )
    assert validation._PRINTER_RANDOM_FLOOR_PROP_RE.search(
        "Under the worktable, a toy is left on the floor."
    )
    assert not validation._PRINTER_RANDOM_FLOOR_PROP_RE.search(
        "A rolling materials cart stands beside the utility table."
    )


def test_printer_support_does_not_become_a_drink_or_seated_work_surface() -> None:
    assert validation._PRINTER_SUPPORT_DRINK_RE.search(
        "A water carafe sits to one side of the dedicated output table."
    )
    assert not validation._PRINTER_SUPPORT_DRINK_RE.search(
        "A water carafe sits on a separate meeting credenza in the background."
    )
    assert validation._PRINTER_SEATING_ALIGNMENT_RE.search(
        "A classroom chair lines up nearby."
    )
    assert validation._PRINTER_SEATING_ALIGNMENT_RE.search(
        "A task chair is pulled up to the worktable."
    )
    assert not validation._PRINTER_SEATING_ALIGNMENT_RE.search(
        "A lounge chair sits across the room near a reading area."
    )


def test_printer_support_does_not_become_an_activity_workstation() -> None:
    assert validation._PRINTER_ACTIVE_SUPPORT_PROP_RE.search(
        "A studio worktable holds a watercolor palette and paintbrushes to one side."
    )
    assert validation._PRINTER_ACTIVE_SUPPORT_PROP_RE.search(
        "Folded reading glasses rest at the utility table edge."
    )
    assert not validation._PRINTER_ACTIVE_SUPPORT_PROP_RE.search(
        "A watercolor palette sits on a separate background cabinet."
    )
    assert not validation._PRINTER_ACTIVE_SUPPORT_PROP_RE.search(
        "A letter tray holds plain papers at the side of the output table."
    )
    assert validation._find_unresolved_scene_alternative(
        "A small ceramic or carved-wood relief hangs on the wall."
    )
    assert (
        validation._find_unresolved_scene_alternative(
            "Abstract art without text or faces hangs above the table."
        )
        is None
    )
    assert (
        validation._find_unresolved_scene_alternative(
            "Two or three abstract clay forms rest on the worktable."
        )
        is None
    )
