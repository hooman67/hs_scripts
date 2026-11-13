from __future__ import annotations

import json
from pathlib import Path
import sys

VERSION = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(VERSION.parent))

from v6_5 import validation
from v6_5.surfaces import SupportInferenceError, infer_primary_support


def test_composite_catalog_props_declare_every_visual_family() -> None:
    catalog = json.loads(
        (VERSION / "approved-v6.5-20261111.catalog.json").read_text(encoding="utf-8")
    )
    by_id = {entry["id"]: set(entry["repetition_groups"]) for entry in catalog["entries"]}
    expected = {
        "V61-HOM-038": {"peg_rail", "woven_storage"},
        "V61-HOM-008": {"sewing_kit", "measurement_tools", "textile_notions"},
        "V61-OFF-039": {"wall_shelving", "ceramic_object"},
        "V61-OFF-015": {"desk_sculpture", "wood_sculpture"},
        "V61-EDU-030": {"storage_cubbies", "open_shelving"},
        "V61-EDU-042": {"shape_display", "geometric_solids"},
        "V61-STU-045": {"shadow_box", "abstract_model"},
        "V61-STU-043": {"ceramic_tile_grid", "ceramic_samples", "ceramic_tile"},
    }
    for prop_id, required_groups in expected.items():
        assert required_groups <= by_id[prop_id]


def test_printer_support_accepts_each_primary_family() -> None:
    phrases = {
        "office worktable": "table",
        "wide worktable": "table",
        "wide low freestanding storage cabinet": "freestanding_cabinet",
        "substantial low sideboard": "credenza_sideboard",
        "fitted base cabinets with a continuous countertop": "fitted_counter",
    }
    for phrase, family in phrases.items():
        assert infer_primary_support(f"A {phrase} anchors the room.", "printer")["family"] == family


def test_printer_support_rejects_desks_and_personal_workstations() -> None:
    for text in (
        "A gaming desk sits beside the window.",
        "A customer café table fills the corner.",
    ):
        try:
            infer_primary_support(text, "printer")
        except SupportInferenceError as exc:
            assert exc.code == "unsafe_printer_support"
        else:  # pragma: no cover - fail with a useful assertion below
            raise AssertionError(text)
    assert infer_primary_support(
        "A dedicated output table sits beside the wall.", "printer"
    )["family"] == "table"


def test_empty_shelving_and_pegboards_are_detected() -> None:
    pattern = validation._EMPTY_SHELF_RE
    assert pattern.search("Empty shelving lines the wall.")
    assert pattern.search("A pegboard is left blank above the table.")
    assert not pattern.search("Shelving holds unlabelled ceramics.")
    assert validation._POPULATED_SHELF_RE.search(
        "A floating shelf holds small unlabelled pigment jars."
    )
    assert validation._POPULATED_SHELF_RE.search(
        "Open cubbies hold plain color bins."
    )


def test_furniture_set_square_is_not_the_drafting_tool() -> None:
    assert validation._FURNITURE_SET_SQUARE_RE.search(
        "A classroom resource table is set square to the wall."
    )


def test_system_prompt_contains_late_ctech_rules() -> None:
    prompt = (VERSION / "system_prompt.md").read_text(encoding="utf-8")
    assert "Never ask for empty or blank shelving or pegboards." in prompt
    assert "Never use a desk or personal workstation as the primary printer support." in prompt
    assert "Never copy an unresolved choice into scene text" in prompt
    assert "Each laptop bank must contain at least two explicitly round or circular primary tables." in prompt
    assert "When a wall is plausibly visible" in prompt
    assert "Never ask for an empty or blank wall-mounted board" in prompt
    assert "Do not maroon a small table" in prompt
    assert "at least five non-table primary supports" in prompt
    assert "No chair or stool should imply a seated workstation at the primary support." in prompt
    assert "task seating off the primary support" in prompt


def test_visible_or_choices_are_rejected_but_safety_and_quantity_are_allowed() -> None:
    assert validation._find_unresolved_scene_alternative(
        "A classroom or library chair sits behind the table."
    )


def test_round_support_detection_is_bounded_to_table_shapes() -> None:
    assert infer_primary_support(
        "A round wooden café table sits in an open seating area.", "laptop"
    )["shape"] == "round"
    assert infer_primary_support(
        "A circular collaborative study table sits near the library wall.", "laptop"
    )["shape"] == "round"
    assert infer_primary_support(
        "A round ceramic coaster rests on a rectangular office worktable.", "laptop"
    )["shape"] == "rectangular"


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
        validation._printer_safety_text(
            "A water carafe sits on a separate meeting credenza in the background."
        )
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
        validation._printer_safety_text("A watercolor palette sits on a separate background cabinet.")
    )
    assert not validation._PRINTER_ACTIVE_SUPPORT_PROP_RE.search(
        "A letter tray holds plain papers at the side of the output table."
    )
    assert not validation._PRINTER_ACTIVE_SUPPORT_PROP_RE.search(
        "A library worktable sits close to a color-block mural on the wall."
    )
    assert not validation._PRINTER_ACTIVE_SUPPORT_PROP_RE.search(
        "A wide project table runs beneath a wall box containing an abstract model."
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
