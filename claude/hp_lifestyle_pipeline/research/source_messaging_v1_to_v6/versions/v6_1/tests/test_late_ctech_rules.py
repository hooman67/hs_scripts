from __future__ import annotations

from pathlib import Path
import sys

VERSION = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(VERSION.parent))

from v6_1 import validation


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


def test_system_prompt_contains_late_ctech_rules() -> None:
    prompt = (VERSION / "system_prompt.md").read_text(encoding="utf-8")
    assert "Never ask for empty or blank shelving or pegboards." in prompt
    assert "Never use a desk or personal workstation as the primary printer-tag support." in prompt
    assert "Never copy an unresolved choice into scene text" in prompt


def test_visible_or_choices_are_rejected_but_safety_and_quantity_are_allowed() -> None:
    assert validation._find_unresolved_scene_alternative(
        "A classroom or library chair sits behind the table."
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
