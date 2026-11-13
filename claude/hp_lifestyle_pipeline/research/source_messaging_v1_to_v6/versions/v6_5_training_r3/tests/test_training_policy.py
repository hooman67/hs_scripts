import re

import pytest

from research.source_messaging_v1_to_v6.versions.v6_5_training_r3.content_policy import check_content_policy
from research.source_messaging_v1_to_v6.versions.v6_5_training_r3.validation import (
    _cited_setting, _object_mentions,
)
from research.source_messaging_v1_to_v6.versions.v6_5_training_r3.tests.test_runtime import (
    FakeProvider, invoke, production_catalog, response, select_prop, valid_output,
)


def test_ordinary_paper_forms_and_a_populated_pen_cup_can_coexist():
    value = valid_output()
    value["prompts"][0].update(
        text=(
            "An office desk anchors a reading area. An open paper notebook shows blank pages "
            "beside loose paper sheets with non-readable markings. Reference books with "
            "unmarked covers and spines stand nearby. A plain pen cup holds plain writing pens."
        ),
        prop_ids=[
            "V65-TR-OFF-paper_notebook", "V65-TR-OFF-loose_work_sheets",
            "V65-TR-OFF-reference_book_collection", "V65-TR-OFF-empty_stationery_cup",
            "V65-TR-OFF-plain_writing_pen",
        ],
        prop_mentions=[
            {"id": "V65-TR-OFF-paper_notebook", "quote": "paper notebook"},
            {"id": "V65-TR-OFF-loose_work_sheets", "quote": "loose paper sheets"},
            {"id": "V65-TR-OFF-reference_book_collection", "quote": "Reference books"},
            {"id": "V65-TR-OFF-empty_stationery_cup", "quote": "plain pen cup"},
            {"id": "V65-TR-OFF-plain_writing_pen", "quote": "plain writing pens"},
        ],
    )
    result = invoke(FakeProvider([response(output=value)]), catalog=production_catalog())
    assert result["status"] == "ok", result


@pytest.mark.parametrize("second_quote", ["paper notebook", "Reference books"])
def test_wrong_or_duplicate_object_declarations_are_rejected(second_quote):
    value = valid_output()
    value["prompts"][0].update(
        text="An office desk holds a paper notebook with blank pages. Reference books have unmarked covers.",
        prop_ids=["V65-TR-OFF-paper_notebook", "V65-TR-OFF-reference_book_collection"],
        prop_mentions=[
            {"id": "V65-TR-OFF-paper_notebook", "quote": "paper notebook"},
            {"id": "V65-TR-OFF-reference_book_collection", "quote": second_quote},
        ],
    )
    if second_quote == "Reference books":
        value["prompts"][0]["prop_mentions"][0]["quote"] = "Reference books"
    result = invoke(
        FakeProvider([response(output=value), response(output=value)]), catalog=production_catalog(),
    )
    assert result["status"] == "error"
    assert "prop_mention_form_mismatch" in {
        issue["code"] for issue in result["audit"]["attempts"][-1]["errors"]
    }


def test_reused_notebooks_do_not_consume_a_bank_wide_family():
    value = valid_output()
    for index, place in ((0, "office meeting area"), (2, "office reading corner")):
        select_prop(
            value["prompts"][index], "V65-TR-OFF-paper_notebook",
            f"An office desk anchors an {place}. A paper notebook shows blank pages.",
            "paper notebook",
        )
    result = invoke(FakeProvider([response(output=value)]), catalog=production_catalog())
    assert result["status"] == "ok", result


@pytest.mark.parametrize("description", [
    "A cropped hand rests on the table.", "A child stands behind the desk.",
    "A distant woman sits in the room.", "A human reflection appears in the glass.",
    "A mannequin stands beside the shelving.", "Cropped arms enter from the side.",
])
def test_unoccupied_means_no_people_or_partial_people(description):
    assert "people_request" in {code for code, _ in check_content_policy(description, set())}


@pytest.mark.parametrize("description", [
    "An unoccupied room without people, cropped hands or human reflections.",
    "A clock face and clock hands are unnumbered.",
    "The chair arms remain connected to its back.",
    "Window reflections brighten the room.",
    "Manual hand tools hang from a toolboard.",
])
def test_nonhuman_parts_and_explicit_exclusions_are_not_people(description):
    assert "people_request" not in {code for code, _ in check_content_policy(description, set())}


def test_a_safe_notebook_does_not_make_another_book_safe():
    value = valid_output()
    value["prompts"][0].update(
        text="An office desk holds a paper notebook with blank pages. Reference books stand nearby.",
        prop_ids=["V65-TR-OFF-paper_notebook", "V65-TR-OFF-reference_book_collection"],
        prop_mentions=[
            {"id": "V65-TR-OFF-paper_notebook", "quote": "paper notebook"},
            {"id": "V65-TR-OFF-reference_book_collection", "quote": "Reference books"},
        ],
    )
    result = invoke(
        FakeProvider([response(output=value), response(output=value)]), catalog=production_catalog(),
    )
    assert result["status"] == "error"
    assert any(
        issue["code"] == "text_bearing_prop_treatment"
        and "reference_book_collection" in issue["detail"]
        for issue in result["audit"]["attempts"][-1]["errors"]
    )


def test_printer_setting_requires_cited_content_not_metadata_keywords():
    pattern = re.compile(r"\bgaming\b", re.I)
    request = {
        "smart_brief": {"metadata": "gaming", "content": "A dedicated gaming room"},
        "source_messaging": "",
    }
    candidate = {"evidence": [{"document": "smart_brief", "path": "/metadata", "quote": "gaming"}]}
    assert not _cited_setting(candidate, request, pattern)
    candidate["evidence"][0]["path"] = "/content"
    assert _cited_setting(candidate, request, pattern)


@pytest.mark.parametrize("noun,group,code", [
    ("Sugar sachets", "sugar_sachets", "sugar_sachet_text_treatment"),
    ("Fabric swatches", "fabric_swatches", "swatch_text_treatment"),
    ("Color swatches", "color_swatches", "swatch_text_treatment"),
])
def test_readable_labels_are_not_a_safe_treatment(noun, group, code):
    issues = {issue[0] for issue in check_content_policy(
        noun + " with readable labels rest beside a blank notebook.", {group},
    )}
    assert code in issues
    assert "legible_text_request" in issues


@pytest.mark.parametrize("noun,group", [
    ("Sugar sachets", "sugar_sachets"),
    ("Fabric swatches", "fabric_swatches"),
    ("Color swatches", "color_swatches"),
])
@pytest.mark.parametrize("treatment", ["no readable labels", "non-readable labels", "indistinct labels"])
def test_each_local_label_safeguard_remains_valid(noun, group, treatment):
    assert check_content_policy(noun + " with " + treatment + " rest nearby.", {group}) == []


def test_two_ids_cannot_declare_the_same_physical_notebook():
    entries = {
        prop_id: {"id": prop_id, "aliases": ["notebook"], "name": "notebook", "repetition_groups": ["notebook"]}
        for prop_id in ("notebook-a", "notebook-b")
    }
    _, issues = _object_mentions({
        "text": "An open notebook has blank pages.",
        "prop_mentions": [
            {"id": prop_id, "quote": "open notebook"} for prop_id in entries
        ],
    }, entries)
    assert {issue[0] for issue in issues} == {"duplicate_physical_prop"}
