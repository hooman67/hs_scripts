from __future__ import annotations

import sys
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
VERSION = HERE.parent
sys.path.insert(0, str(VERSION.parent))

from v6_5_training_r3.surfaces import SupportInferenceError, audit_bank, infer_primary_support


def assert_exact_span(text: str, evidence: dict) -> None:
    assert text[evidence["start"] : evidence["end"]] == evidence["phrase"]
    if evidence["shape_evidence"]:
        shape = evidence["shape_evidence"]
        assert text[shape["start"] : shape["end"]] == shape["phrase"]


@pytest.mark.parametrize(
    ("text", "shape", "phrase"),
    [
        (
            "A round wall mirror hangs above an ordinary wooden desk.",
            "unspecified",
            "ordinary wooden desk",
        ),
        (
            "An ordinary laptop desk anchors a quiet home workspace.",
            "unspecified",
            "ordinary laptop desk",
        ),
        (
            "A round table lamp illuminates a rectangular office desk.",
            "rectangular",
            "rectangular office desk",
        ),
        (
            "A background round table sits behind an ordinary desk used for focused work.",
            "unspecified",
            "ordinary desk",
        ),
        (
            "A rectangular table with rounded corners anchors the workspace.",
            "rectangular",
            "rectangular table",
        ),
        (
            "A dedicated plywood worktable with a softly curved edge anchors the studio.",
            "unspecified",
            "dedicated plywood worktable",
        ),
        (
            "A wooden table with a circular tabletop anchors the café.",
            "round",
            "wooden table",
        ),
    ],
)
def test_shape_is_attached_to_primary_support_only(text: str, shape: str, phrase: str) -> None:
    result = infer_primary_support(text, "laptop")

    assert result["shape"] == shape
    assert result["phrase"] == phrase
    assert_exact_span(text, result)


def test_only_first_sentence_is_considered() -> None:
    text = "A rectangular desk supports the laptop. A round table appears in the next room."

    result = infer_primary_support(text, "laptop")

    assert result["shape"] == "rectangular"
    assert result["sentence_end"] == text.index(".") + 1


@pytest.mark.parametrize(
    ("text", "code"),
    [
        ("A rectangular table with a circular top anchors the room.", "conflicting_support_shape"),
        ("A hexagonal worktable anchors the room.", "unknown_support_shape"),
        ("A table or cabinet supports the equipment.", "conflicting_primary_support"),
    ],
)
def test_unknown_or_conflicting_evidence_is_an_error(text: str, code: str) -> None:
    with pytest.raises(SupportInferenceError) as caught:
        infer_primary_support(text)

    assert caught.value.code == code
    evidence = caught.value.to_dict()
    if "phrase" in evidence:
        assert text[evidence["start"] : evidence["end"]] == evidence["phrase"]


@pytest.mark.parametrize(
    "text",
    [
        "A narrow storage cabinet supports the printer.",
        "A floating storage cabinet supports the printer.",
        "A high storage cabinet supports the printer.",
        "A fragile sideboard supports the printer.",
        "A customer café table supports the printer.",
        "A gaming desk supports the printer.",
    ],
)
def test_printer_rejects_unsafe_casework_and_customer_furniture(text: str) -> None:
    with pytest.raises(SupportInferenceError) as caught:
        infer_primary_support(text, "printer")

    assert caught.value.code == "unsafe_printer_support"
    evidence = caught.value.to_dict()
    assert text[evidence["start"] : evidence["end"]] == evidence["phrase"]
    assert text[evidence["unsafe_start"] : evidence["unsafe_end"]] == evidence["unsafe_phrase"]


def test_background_shelf_does_not_displace_printer_support() -> None:
    text = "A display shelf behind a dedicated output table holds decor."

    result = infer_primary_support(text, "printer")

    assert result["family"] == "table"
    assert result["phrase"] == "dedicated output table"


def test_printer_requires_a_named_equipment_role_for_table_family() -> None:
    with pytest.raises(SupportInferenceError) as caught:
        infer_primary_support("A wooden table supports the printer.", "printer")

    assert caught.value.code == "unsupported_printer_support"


@pytest.mark.parametrize("phrase", [
    "Fitted creative-studio base cabinets with a continuous worktop",
    "Fitted home workspace base cabinets with a continuous worktop",
])
def test_fitted_counter_accepts_environment_qualifiers_without_losing_exact_span(phrase):
    text = f"{phrase} form an output area. A background cabinet stands farther back."
    result = infer_primary_support(text, "printer")
    assert result["family"] == "fitted_counter"
    assert result["phrase"] == phrase
    assert_exact_span(text, result)
    from v6_5_training_r3.validation import _mask_primary_references
    assert "background cabinet" in _mask_primary_references(text, result)


@pytest.mark.parametrize("phrase", [
    "Fitted creative-studio base cabinets",
    "Fitted home workspace base cabinets with a narrow worktop",
])
def test_environment_qualifiers_do_not_replace_continuous_worktop_requirement(phrase):
    with pytest.raises(SupportInferenceError):
        infer_primary_support(f"{phrase} form an output area.", "printer")


def test_printer_bank_counts_materially_distinct_synonyms() -> None:
    phrases = [
        "dedicated output table",
        "sturdy work table",
        "resource table",
        "studio table",
        "wide low floor-standing storage cabinet",
        "broad freestanding storage cabinet",
        "substantial low credenza",
        "wide low sideboard",
        "fitted base cabinets with a continuous worktop",
        "built-in equipment counter",
    ]
    rows = [
        {
            "id": f"P{index:02d}",
            "environment": "Office",
            "text": f"A calm office uses a {phrase} for shared output.",
        }
        for index, phrase in enumerate(phrases, start=1)
    ]

    result = audit_bank(rows, "printer")

    assert result["passed"] is True
    assert result["counts"]["families"] == {
        "credenza_sideboard": 2,
        "fitted_counter": 2,
        "freestanding_cabinet": 2,
        "table": 4,
    }
    assert not result["errors"]
    for source, row in zip(rows, result["rows"], strict=True):
        support = row["support"]
        assert source["text"][support["start"] : support["end"]] == support["phrase"]


def _laptop_rows(cafe_shape: str = "round") -> list[dict[str, str]]:
    rows = []
    for index in range(10):
        environment = "Café" if index in {2, 7} else "Office"
        if environment == "Café":
            phrase = f"{cafe_shape} wooden café table"
        elif index == 0:
            phrase = "circular office table"
        else:
            phrase = "ordinary wooden desk"
        rows.append(
            {
                "id": f"L{index + 1:02d}",
                "environment": environment,
                "text": f"A {phrase} anchors the scene.",
            }
        )
    return rows


def test_laptop_bank_requires_two_round_primary_surfaces_and_round_cafes() -> None:
    passed = audit_bank(_laptop_rows(), "laptop")
    failed = audit_bank(_laptop_rows("rectangular"), "laptop")

    assert passed["passed"] is True
    codes = {error["code"] for error in failed["errors"]}
    assert "laptop_round_primary_minimum" in codes
    assert "cafe_primary_support_not_round" in codes


def test_a_round_background_table_does_not_satisfy_laptop_minimum() -> None:
    rows = _laptop_rows("rectangular")
    rows[0]["text"] = (
        "A background round table sits behind an ordinary wooden desk used for focused work."
    )

    result = audit_bank(rows, "laptop")

    assert result["rows"][0]["support"]["phrase"] == "ordinary wooden desk"
    assert result["rows"][0]["support"]["shape"] == "unspecified"
    assert any(error["code"] == "laptop_round_primary_minimum" for error in result["errors"])


@pytest.mark.parametrize('phrase', ['round marble café table', 'circular pale wood meeting table', 'round natural-wood table'])
def test_round_material_modifiers(phrase):
    assert infer_primary_support(f'A {phrase} anchors the workspace.', 'laptop')['shape'] == 'round'


def test_definite_primary_references_do_not_exempt_background_furniture():
    from v6_5_training_r3.validation import _mask_primary_references
    text = 'A low storage cabinet supports the work area. The cabinet remains clear at the front.'
    result = _mask_primary_references(text, infer_primary_support(text, 'printer'))
    assert 'The cabinet' not in result
    text = 'A low storage cabinet supports the work area. A background cabinet stands behind it. The cabinet is open.'
    result = _mask_primary_references(text, infer_primary_support(text, 'printer'))
    assert 'background cabinet' in result
    assert 'The cabinet' in result


@pytest.mark.parametrize("accessory", ["desk tray", "table lamp", "desk clock"])
def test_furniture_accessory_does_not_make_primary_reference_ambiguous(accessory):
    from v6_5_training_r3.validation import _mask_primary_references

    text = (
        f"A rectangular office table anchors the room with a plain {accessory}. "
        "A frosted partition stands behind the table."
    )
    result = _mask_primary_references(text, infer_primary_support(text, "laptop"))
    assert accessory in result
    assert "the table" not in result


def test_accessory_does_not_hide_an_actual_second_table():
    from v6_5_training_r3.validation import _mask_primary_references

    text = (
        "A rectangular office table anchors the room. "
        "A background table holds a desk tray. A partition stands behind the table."
    )
    result = _mask_primary_references(text, infer_primary_support(text, "laptop"))
    assert "background table" in result
    assert "the table" in result


@pytest.mark.parametrize('phrase,family', [
    ('low office credenza', 'credenza_sideboard'),
    ('low residential sideboard', 'credenza_sideboard'),
    ('wide flat-file cabinet', 'freestanding_cabinet'),
    ('fitted base cabinetry with a continuous countertop', 'fitted_counter'),
])
def test_ordinary_support_modifiers_and_cabinetry(phrase, family):
    result = infer_primary_support(f'A {phrase} anchors the room.', 'printer')
    assert result['family'] == family
    assert result['phrase'] == phrase


def test_predicate_round_shape_and_attached_accessory():
    assert infer_primary_support('A café table is circular and small.', 'laptop')['shape'] == 'round'
    result = infer_primary_support('A felt desk tray sits on a round oak table.', 'laptop')
    assert result['shape'] == 'round'
    assert result['phrase'] == 'round oak table'


def test_catalogue_alias_covers_furniture_only_at_its_actual_location():
    from v6_5_training_r3.validation import _SECONDARY_FURNITURE_RE, _furniture_head_has_alias
    text = 'A tall filing cabinet and another cabinet stand behind the main surface.'
    detected = list(_SECONDARY_FURNITURE_RE.finditer(text))
    known = [('tall filing cabinet', {'filing_cabinet'})]
    assert _furniture_head_has_alias(text, detected[0], known)
    assert not _furniture_head_has_alias(text, detected[1], known)
    assert not list(_SECONDARY_FURNITURE_RE.finditer('A felt desk tray holds keys.'))


def test_exact_approved_name_alternative_is_recognized_without_alias_expansion():
    from v6_5_training_r3.validation import _phrase_index, _known_matches
    entries = [{'name': 'low storage cabinet or tall filing cabinet with no labels',
                'aliases': ['storage cabinet'], 'repetition_groups': ['closed_storage']}]
    phrases = _phrase_index([], entries)
    assert _known_matches('A tall filing cabinet with no labels stands behind it.', phrases) == [
        ('tall filing cabinet with no labels', {'closed_storage'})]
    assert not _known_matches('A display cabinet stands behind it.', phrases)


def test_wall_anchored_model_is_not_a_personal_prop_on_the_printer_counter():
    from v6_5_training_r3.validation import _printer_safety_text, _PRINTER_ACTIVE_SUPPORT_PROP_RE
    wall = 'a shallow wall box containing an abstract model mounted on the adjacent wall'
    text = 'A built-in equipment counter is the main support, with ' + wall + '.'
    assert not _PRINTER_ACTIVE_SUPPORT_PROP_RE.search(_printer_safety_text(text))
    occupied = 'The equipment counter holds an open notebook, with ' + wall + '.'
    assert _PRINTER_ACTIVE_SUPPORT_PROP_RE.search(_printer_safety_text(occupied))
    unanchored = 'An equipment counter holds a shallow box containing an abstract model.'
    assert _PRINTER_ACTIVE_SUPPORT_PROP_RE.search(_printer_safety_text(unanchored))


def test_round_living_room_table_shape_is_not_lost():
    assert infer_primary_support('A circular living-room end table sets a home work spot.', 'laptop')['shape'] == 'round'


def test_cubbies_containing_bins_are_explicitly_populated():
    from v6_5_training_r3.validation import _POPULATED_SHELF_RE
    assert _POPULATED_SHELF_RE.search('Open cubbies containing plain color bins sit farther back.')
    assert not _POPULATED_SHELF_RE.search('Open cubbies stand against the wall.')

@pytest.mark.parametrize('phrase,family', [
    ('substantial home workspace sideboard', 'credenza_sideboard'),
    ('fitted office base cabinets with a continuous worktop', 'fitted_counter'),
])
def test_contextual_support_modifiers(phrase, family):
    assert infer_primary_support(f'A {phrase} anchors the room.', 'printer')['family'] == family
