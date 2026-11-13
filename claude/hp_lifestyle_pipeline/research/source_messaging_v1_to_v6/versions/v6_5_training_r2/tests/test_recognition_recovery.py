import pytest

from research.source_messaging_v1_to_v6.versions.v6_5_training_r2.content_policy import (
    check_content_policy,
)
from research.source_messaging_v1_to_v6.versions.v6_5_training_r2.validation import (
    _declared_carrier_pairs, _find_unresolved_scene_alternative, _form_spans,
    _mask_depicted_subjects, _mask_primary_references, _object_mentions, _printer_safety_text,
    _PRINTER_ACTIVE_SUPPORT_PROP_RE, _SECONDARY_FURNITURE_RE,
)
from research.source_messaging_v1_to_v6.versions.v6_5_training_r2.tests.test_runtime import (
    production_catalog,
)


def entries():
    return {entry["id"]: entry for entry in production_catalog()["entries"]}


@pytest.mark.parametrize("prop_id,concrete", [
    ("V61-OFF-042", "clear architectural partition"),
    ("V61-OFF-042", "frosted architectural partitions"),
    ("V61-OFF-035", "pale brick"),
    ("V61-OFF-035", "board-formed concrete finish"),
    ("V61-CAF-036", "warm plaster"),
    ("V61-STU-026", "drawer unit"),
    ("V61-STU-026", "flat-file cabinets"),
    ("V61-CAF-033", "chalkboard menu"),
    ("V61-CAF-018", "small unlabelled ceramic forms"),
])
def test_reviewed_choice_forms_have_concrete_aliases(prop_id, concrete):
    assert _form_spans(concrete, entries()[prop_id])


def test_ceramic_does_not_authorize_shelves_and_shelves_do_not_swallow_contents():
    catalog = entries()
    assert not _form_spans("shelves", catalog["V61-CAF-018"])
    text = "shelves with unlabelled jars or material samples"
    assert all(text[start:end] == "shelves" for start, end in _form_spans(
        text, catalog["V61-STU-027"],
    ))
    assert _find_unresolved_scene_alternative(
        "Sheets have no readable annotations, while shelves hold jars or material samples."
    )


@pytest.mark.parametrize("prop_id,declaration,reference", [
    ("V65-TR-HOM-modular_book_storage", "modular wooden bookcase with closed drawers", "the bookcase"),
    ("V65-TR-HOM-modular_book_storage", "modular wooden bookcase with closed drawers", "the counter and bookcase"),
    ("V65-TR-CAF-wooden_cafe_chair", "wooden café chairs", "the chairs"),
    ("V65-TR-CAF-wooden_cafe_chair", "wooden café chair", "the seating"),
    ("V65-TR-OFF-paper_notebook", "paper notebook", "the notebook"),
])
def test_same_object_references_require_an_earlier_concrete_declaration(prop_id, declaration, reference):
    entry = entries()[prop_id]
    assert not _form_spans(reference, entry)
    text = declaration + " is placed nearby. Beside " + reference + " is daylight."
    assert any(start > len(declaration) for start, _ in _form_spans(text, entry))
    assert not _form_spans("the notebook and loose sheets", entries()["V65-TR-OFF-reference_book_collection"])


def test_table_reading_lamp_does_not_break_primary_reference_tracking():
    text = "An office worktable stands nearby. A table reading lamp lights the worktable."
    support = {"family": "table", "end": len("An office worktable")}
    assert "the worktable" not in _mask_primary_references(text, support)
    assert all(match.group().strip() != "table" for match in _SECONDARY_FURNITURE_RE.finditer(
        "A table reading lamp stands at normal table height beside open table space."
    ))
    assert "the table" in _mask_primary_references(
        "An office table stands nearby. Another table stands behind the table.",
        {"family": "table", "end": len("An office table")},
    )


@pytest.mark.parametrize("description", [
    "A notebook has no readable annotations.",
    "Loose sheets have no readable writing.",
    "Reference sheets are without legible signatures.",
])
def test_object_attached_equivalent_text_exclusions_are_safe(description):
    assert check_content_policy(description, {"paper_documents"}) == []
    assert any(code == "legible_text_request" for code, _ in check_content_policy(
        "A notebook has readable labels.", {"paper_documents"},
    ))


def test_depicted_botanical_subjects_are_not_physical_flowers_or_plants():
    entry = entries()["V65-TR-STU-botanical_reference_sheets"]
    quote = "botanical reference sheets showing leaves and flowers only"
    text = quote + " with no readable annotations. Actual flowers stand beside a plant."
    masked = _mask_depicted_subjects(
        text, {"prop_mentions": [{"id": entry["id"], "quote": quote}]}, {entry["id"]: entry},
    )
    assert "leaves and flowers only" not in masked
    assert "Actual flowers stand beside a plant" in masked
    assert len(masked) == len(text)


@pytest.mark.parametrize("safe_child", [True, False])
def test_board_safety_uses_declared_contents_without_sanitizing_unsafe_children(safe_child):
    catalog = entries()
    board = catalog["V65-TR-STU-working_reference_pinboard"]
    sheets = catalog["V65-TR-STU-botanical_reference_sheets"]
    quote = "botanical reference sheets"
    candidate = {
        "text": "A fabric-covered reference pinboard carries " + quote
                + (" with no readable annotations." if safe_child else "."),
        "prop_ids": [board["id"], sheets["id"]],
        "prop_mentions": [
            {"id": board["id"], "quote": "fabric-covered reference pinboard"},
            {"id": sheets["id"], "quote": quote},
        ],
    }
    spans, problems = _object_mentions(candidate, catalog)
    assert not problems
    issues = check_content_policy(
        candidate["text"], set(), objects=[board, sheets], spans=spans,
        carriers=_declared_carrier_pairs(candidate, catalog),
    )
    assert bool(issues) is not safe_child
    if not safe_child:
        assert any(sheets["id"] in detail for _, detail in issues)


@pytest.mark.parametrize("grammar", ["carry", "are filled with"])
def test_declared_shelves_bind_plural_carrier_grammar(grammar):
    carrier = entries()["V61-STU-027"]
    child = entries()["V65-TR-STU-reference_book_collection"]
    quote = "reference books with unmarked covers"
    candidate = {
        "text": f"Shelves {grammar} {quote}.",
        "prop_ids": [carrier["id"], child["id"]],
        "prop_mentions": [
            {"id": carrier["id"], "quote": "Shelves"},
            {"id": child["id"], "quote": quote},
        ],
    }
    catalog = {entry["id"]: entry for entry in (carrier, child)}
    assert _declared_carrier_pairs(candidate, catalog)[carrier["id"]] == {child["id"]}
    candidate["text"] = f"Shelves stand near the window. A separate desk holds {quote}."
    assert not _declared_carrier_pairs(candidate, catalog)[carrier["id"]]
    candidate["text"] = f"Shelves stand behind a desk that holds {quote}."
    assert not _declared_carrier_pairs(candidate, catalog)[carrier["id"]]


@pytest.mark.parametrize("suffix", [
    "rather than on the work surface",
    "at normal table height",
])
def test_printer_secondary_location_is_not_an_affirmative_primary_placement(suffix):
    text = f"A separate background worktable holds a notebook with blank pages {suffix}."
    assert not _PRINTER_ACTIVE_SUPPORT_PROP_RE.search(_printer_safety_text(text))
    assert _PRINTER_ACTIVE_SUPPORT_PROP_RE.search(_printer_safety_text(
        "A dedicated printer counter holds a notebook with blank pages."
    ))


@pytest.mark.parametrize("text", [
    "No readable annotations or signatures appear.",
    "There are no people, cropped hands or human figures.",
])
def test_actual_exclusion_lists_are_not_visible_choices(text):
    assert _find_unresolved_scene_alternative(text) is None
