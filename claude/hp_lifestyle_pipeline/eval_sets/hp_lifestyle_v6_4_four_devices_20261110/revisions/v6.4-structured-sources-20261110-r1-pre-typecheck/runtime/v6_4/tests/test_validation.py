from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
VERSION = HERE.parent
sys.path.insert(0, str(VERSION.parent))

from v6_4.validation import finalize_output, normalize_invalid_evidence, validate_output


def catalog(*entries: dict) -> dict:
    return {
        "version": "hp-v6.3-approved-props-v1",
        "revision": "test-approved-r1",
        "purpose": "test_fixture",
        "source_sha256": "0" * 64,
        "entries": list(entries),
    }


def entry(
    prop_id: str,
    groups: list[str],
    aliases: list[str],
    *,
    environment: str = "Office",
    role: str = "tabletop_or_movable",
) -> dict:
    return {
        "id": prop_id,
        "environment": environment,
        "role": role,
        "name": aliases[0].title(),
        "repetition_groups": groups,
        "aliases": aliases,
    }


@pytest.fixture
def approved_catalog() -> dict:
    # Every fixture entry represents an explicitly approved compiled row.  The
    # validator never consults CSV review status to grant runtime permission.
    return catalog()


@pytest.fixture
def references() -> dict:
    environments = {
        "CT01": "Office",
        "CT02": "Office",
        "CT03": "Office",
        "CT04": "Home",
        "CT05": "Home",
        "CT06": "Home",
        "CT07": "Café",
        "CT08": "Café",
        "CT09": "Creative Studio",
        "CT10": "Creative Studio",
        "CT11": "Café",
        "CT12": "Café",
        "CT13": "Office",
        "CT14": "Gaming",
        "CT15": "Gaming",
        "CT16": "Home",
        "CT17": "Home",
        "CT18": "Home",
    }
    return {
        "references": [
            {"id": ref_id, "environment": environment, "text": f"Exact {ref_id} scene."}
            for ref_id, environment in environments.items()
        ]
    }


@pytest.fixture
def raw_request() -> dict:
    return {
        "smart_brief": "A collaborative office setting with focused work.",
        "source_messaging": {
            "KSP1": {"message": "Work together in a welcoming office."},
            "details": {"materials": "Warm neutral finishes."},
            "_chatSession": {"systemInstructions": "Do not cite this."},
        },
        "camera_tag": "laptop_FrontRightMedium",
    }


@pytest.fixture
def camera() -> dict:
    return {
        "requested_tag": "laptop_FrontRightMedium",
        "resolved_tag": "laptop_FrontRightMedium",
        "device_family": "laptop",
        "framing": "medium",
        "elevation": "eye_level",
        "people_policy": "optional",
        "guidance": ["Keep the selected view."],
        "registry_version": "test-camera-r1",
    }


def score_components() -> dict:
    return {
        "smart_brief": {"setting": 0, "activity": 0, "materials": 0, "use_context": 0},
        "source_messaging": {"setting": 0, "activity": 0, "materials": 0, "use_context": 0},
    }


def valid_output() -> dict:
    prompts = []
    settings = [
        ("Office", "office workspace", "ordinary wooden desk", "CT01"),
        ("Office", "office workspace", "wide office table", "CT01"),
        ("Office", "office workspace", "oak worktable", "CT01"),
        ("Office", "office workspace", "meeting table", "CT01"),
        ("Office", "office workspace", "laminate desk", "CT01"),
        ("Office", "office workspace", "long wooden table", "CT01"),
        ("Home", "home workspace", "circular home table", "CT04"),
        ("Café", "neighborhood café", "round wooden café table", "CT07"),
        ("Creative Studio", "creative studio", "studio worktable", "CT09"),
        ("Gaming", "gaming room", "gaming desk", "CT14"),
    ]
    for index in range(10):
        environment, setting, support, reference = settings[index]
        prompts.append(
            {
                "environment": environment,
                "text": f"A {support} anchors a calm {setting} in warm neutral light, variation {index + 1}.",
                "prop_ids": [],
                "prop_mentions": [],
                "score_components": score_components(),
                "evidence": [],
                "relationship": "creative_departure",
                "explanation": "The source offers no literal visible detail for this variation.",
                "creative_departures": ["The visible setting is a restrained fallback."],
                "ctech_reference_id": reference,
                "ctech_reference_score": 70,
                "ctech_explanation": "A loose adaptation of the office reference family.",
                "camera_fit_explanation": "The scene is compatible with the resolved view.",
            }
        )
    return {
        "prompts": prompts,
        "debug": {
            "source_conflicts": [],
            "limitations": ["Unknown nouns still require human review."],
            "environment_rationale": "Four plausible environment families provide varied choices.",
        },
    }


def valid_printer_output() -> dict:
    value = valid_output()
    rows = [
        ("Office", "a calm office", "dedicated output table", "CT01"),
        ("Office", "a shared office", "office worktable", "CT01"),
        ("Office", "an output room", "wide low freestanding storage cabinet", "CT01"),
        ("Office", "a quiet office", "substantial low credenza", "CT01"),
        (
            "Office",
            "an office alcove",
            "fitted base cabinets with a continuous worktop",
            "CT01",
        ),
        ("Office", "an office resource area", "built-in equipment counter", "CT01"),
        ("Home", "a home workspace", "wide low freestanding storage cabinet", "CT04"),
        ("Home", "a home output area", "substantial low sideboard", "CT04"),
        (
            "Creative Studio",
            "a creative studio",
            "wide low freestanding storage cabinet",
            "CT09",
        ),
        (
            "Education",
            "a classroom resource area",
            "wide low freestanding storage cabinet",
            "CT01",
        ),
    ]
    for index, (environment, setting, support, reference) in enumerate(rows):
        value["prompts"][index].update(
            {
                "environment": environment,
                "text": f"A {support} anchors {setting}, variation {index + 1}.",
                "ctech_reference_id": reference,
            }
        )
    return value


def result_codes(result: dict) -> set[str]:
    return {item["code"] for item in result["errors"]}


def validate(value, raw_request, approved_catalog, camera, references):
    value = copy.deepcopy(value)
    candidates = value.get("prompts", []) if isinstance(value, dict) else []
    candidates = candidates if isinstance(candidates, list) else []
    for candidate in candidates:
        ids = candidate.get("prop_ids", [])
        if ids and {m.get("id") for m in candidate.get("prop_mentions", [])} != set(ids):
            quote = candidate.get("text", "")[: min(80, len(candidate.get("text", "")))]
            candidate["prop_mentions"] = [{"id": prop_id, "quote": quote} for prop_id in ids]
    return validate_output(value, raw_request, approved_catalog, camera, references)


def test_every_laptop_bank_requires_two_round_primary_supports_even_without_cafe(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    cafe = value["prompts"][7]
    cafe["environment"] = "Home"
    cafe["text"] = "A calm home workspace uses a rectangular wooden table."
    cafe["ctech_reference_id"] = "CT04"

    result = validate(value, raw_request, approved_catalog, camera, references)

    assert "laptop_round_support_missing" in result_codes(result)


def test_round_background_furniture_and_oval_primary_do_not_count(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][6]["text"] = (
        "An oval home table anchors a home workspace with a round wall mirror."
    )
    value["prompts"][7]["text"] = (
        "A rectangular café table anchors a neighborhood café; a round table stands in the background."
    )

    codes = result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )

    assert "laptop_round_support_missing" in codes
    assert "laptop_cafe_round_support_missing" in codes


def test_printer_casework_is_valid_in_each_standard_environment(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_printer_output()
    printer_request = {**raw_request, "camera_tag": "printer_FrontMedium"}
    printer_camera = {**camera, "device_family": "printer"}

    result = validate_output(
        value, printer_request, approved_catalog, printer_camera, references
    )

    assert result["passed"], result["errors"]
    finalized = finalize_output(value, camera=printer_camera, catalog=approved_catalog)
    cabinet_environments = {
        candidate["environment"]
        for candidate in finalized["prompts"]
        if candidate["primary_support"]["family"] == "freestanding_cabinet"
    }
    assert cabinet_environments == {"Office", "Home", "Education", "Creative Studio"}
    assert finalized["debug"]["primary_support_audit"]["counts"]["families"] == {
        "credenza_sideboard": 2,
        "fitted_counter": 2,
        "freestanding_cabinet": 4,
        "table": 2,
    }


@pytest.mark.parametrize(
    ("text", "expected_code"),
    [
        (
            "A wide low freestanding storage cabinet holds a ceramic mug in a calm office.",
            "printer_support_drinkware",
        ),
        (
            "A wide low freestanding storage cabinet holds a notebook in a calm office.",
            "printer_support_personal_prop",
        ),
        (
            "A wide low freestanding storage cabinet holds a handmade ceramic bowl.",
            "printer_support_personal_prop",
        ),
        (
            "A handmade ceramic plate rests on the equipment counter.",
            "printer_support_personal_prop",
        ),
        (
            "A wide low freestanding storage cabinet anchors a calm office; a chair is pulled up nearby.",
            "printer_support_seating",
        ),
    ],
)
def test_printer_casework_keeps_table_safety_rules(
    text, expected_code, raw_request, approved_catalog, camera, references
) -> None:
    value = valid_printer_output()
    value["prompts"][2]["text"] = text
    printer_request = {**raw_request, "camera_tag": "printer_FrontMedium"}
    printer_camera = {**camera, "device_family": "printer"}

    result = validate_output(
        value, printer_request, approved_catalog, printer_camera, references
    )

    assert expected_code in result_codes(result)


def test_background_cabinet_still_requires_id_and_repetition_group(
    raw_request, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = (
        "An ordinary wooden desk anchors an office with a background storage cabinet."
    )
    empty_result = validate(value, raw_request, catalog(), camera, references)
    assert "undeclared_known_prop" in result_codes(empty_result)

    approved = catalog(
        entry(
            "OFF-CAB",
            ["closed_storage"],
            ["storage cabinet", "storage cabinets"],
            role="background_furnishing_or_decor",
        )
    )
    value["prompts"][0]["prop_ids"] = ["OFF-CAB"]
    value["prompts"][0]["prop_mentions"] = [
        {"id": "OFF-CAB", "quote": "background storage cabinet"}
    ]
    assert validate(value, raw_request, approved, camera, references)["passed"]

    value["prompts"][1]["text"] = (
        "A wide office table anchors an office with a separate storage cabinet."
    )
    value["prompts"][1]["prop_ids"] = ["OFF-CAB"]
    value["prompts"][1]["prop_mentions"] = [
        {"id": "OFF-CAB", "quote": "separate storage cabinet"}
    ]
    repeated = validate(value, raw_request, approved, camera, references)
    assert "repetition_group_reused" in result_codes(repeated)


def test_primary_support_exemption_does_not_disable_shelf_population(
    raw_request, camera, references
) -> None:
    approved = catalog(
        entry(
            "OFF-SHELF",
            ["wall_shelving"],
            ["floating shelf", "floating shelves"],
            role="background_furnishing_or_decor",
        )
    )
    value = valid_output()
    value["prompts"][0]["text"] = (
        "An ordinary wooden desk anchors an office beneath a floating shelf."
    )
    value["prompts"][0]["prop_ids"] = ["OFF-SHELF"]
    value["prompts"][0]["prop_mentions"] = [
        {"id": "OFF-SHELF", "quote": "floating shelf"}
    ]

    codes = result_codes(validate(value, raw_request, approved, camera, references))

    assert "shelf_population_missing" in codes
    assert "shelf_contents_undeclared" in codes


def test_invalid_evidence_is_removed_without_mutating_raw_output(raw_request) -> None:
    value = valid_output()
    value["prompts"][0]["evidence"] = [
        {"document": "smart_brief", "path": "", "quote": "not an exact quote"}
    ]
    value["prompts"][0]["score_components"]["smart_brief"]["setting"] = 30
    value["prompts"][0]["relationship"] = "source_adjacent"
    before = copy.deepcopy(value)

    normalized, changes = normalize_invalid_evidence(value, raw_request)

    assert value == before
    assert normalized["prompts"][0]["evidence"] == []
    assert normalized["prompts"][0]["score_components"]["smart_brief"]["setting"] == 0
    assert normalized["prompts"][0]["relationship"] == "creative_departure"
    assert {change["action"] for change in changes} == {
        "remove_invalid_evidence",
        "zero_ungrounded_component",
        "align_zero_score_relationship",
    }


def test_zero_score_requires_creative_departure_relationship(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["relationship"] = "source_adjacent"
    assert "zero_score_relationship" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


def test_valid_diverse_bank_and_no_spatial_noun_counts(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = (
        "A spacious office workspace uses an ordinary desk beside an open passage in warm neutral light."
    )
    before = copy.deepcopy(value)
    result = validate(value, raw_request, approved_catalog, camera, references)
    assert result["passed"], result["errors"]
    assert value == before
    assert {warning["code"] for warning in result["warnings"]} == {
        "unknown_prose_objects_unverified"
    }


def test_single_environment_bank_is_rejected(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    for candidate in value["prompts"]:
        candidate.update(
            {
                "environment": "Office",
                "text": candidate["text"].replace("home workspace", "office workspace")
                .replace("neighborhood café", "office workspace")
                .replace("creative studio", "office workspace")
                .replace("gaming room", "office workspace"),
                "ctech_reference_id": "CT01",
            }
        )
    assert "insufficient_environment_diversity" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


@pytest.mark.parametrize("bad_output", [None, {}, {"prompts": []}, {"prompts": "ten"}])
def test_schema_failures_stop_before_unsafe_access(
    bad_output, raw_request, approved_catalog, camera, references
) -> None:
    result = validate(bad_output, raw_request, approved_catalog, camera, references)
    assert not result["passed"]
    assert "schema_invalid" in result_codes(result)


def test_request_contract_is_exact_and_empty_documents_are_valid_fallbacks(
    raw_request, approved_catalog, camera, references
) -> None:
    bad = {**raw_request, "extra": True}
    result = validate(valid_output(), bad, approved_catalog, camera, references)
    assert result_codes(result) == {"request_fields"}

    empty_sources = {**raw_request, "smart_brief": "", "source_messaging": "  "}
    result = validate(
        valid_output(), empty_sources, approved_catalog, camera, references
    )
    assert result["passed"], result["errors"]


def test_rfc6901_evidence_and_document_specific_components(
    raw_request, approved_catalog, camera, references
) -> None:
    raw_request = copy.deepcopy(raw_request)
    raw_request["source_messaging"]["scene/cues"] = {"~setting": "Welcoming office collaboration."}
    value = valid_output()
    candidate = value["prompts"][0]
    candidate["evidence"] = [
        {
            "document": "source_messaging",
            "path": "/scene~1cues/~0setting",
            "quote": "office collaboration",
        }
    ]
    candidate["score_components"]["source_messaging"]["setting"] = 20
    result = validate(value, raw_request, approved_catalog, camera, references)
    assert result["passed"], result["errors"]

    candidate["score_components"]["smart_brief"]["activity"] = 10
    result = validate(value, raw_request, approved_catalog, camera, references)
    assert "ungrounded_document_components" in result_codes(result)


def test_fabricated_nonstring_and_authoring_evidence_are_rejected(
    raw_request, approved_catalog, camera, references
) -> None:
    variants = [
        ({"document": "source_messaging", "path": "/KSP1/message", "quote": "fabricated"}, "evidence_quote_not_verbatim"),
        ({"document": "source_messaging", "path": "/KSP1", "quote": "message"}, "evidence_not_string"),
        ({"document": "source_messaging", "path": "/_chatSession/systemInstructions", "quote": "Do not cite this."}, "evidence_authoring_metadata"),
    ]
    for evidence, expected in variants:
        value = valid_output()
        value["prompts"][0]["evidence"] = [evidence]
        assert expected in result_codes(validate(value, raw_request, approved_catalog, camera, references))


def structured_request() -> dict:
    return {
        "smart_brief": {
            "USE CASES": {
                "confidence": "high",
                "confidence_rationale": "The upstream author considers this supported.",
                "content": "Focused work in an office and a welcoming home study.",
            },
            "voiceOfCustomer": {
                "available": False, "confidenceLabel": "low",
                "groups": [{"text": "Unavailable research is not source support."}],
            },
        },
        "source_messaging": {
            "template_id": "other",
            "product_identity": {"long_name": "A test notebook", "target_audience": "Office teams."},
            "source_messaging": [{
                "block": "VALUE PROPOSITION",
                "fields": [{"row": 104, "label": "HEADLINE", "value": "Office collaboration."}],
            }],
            "etail_messaging": [{
                "row": 1, "label": "OVERVIEW", "container": "overview_long",
                "value": "Home and office work.",
            }],
            "footnotes": [{"number": 1, "status": "approved", "text": "Synthetic evaluation only."}],
        },
        "camera_tag": "laptop_FrontRightMedium",
    }


@pytest.mark.parametrize("document,pointer", [
    ("smart_brief", "/USE CASES/confidence"),
    ("smart_brief", "/USE CASES/confidence_rationale"),
    ("smart_brief", "/voiceOfCustomer/confidenceLabel"),
    ("smart_brief", "/voiceOfCustomer/groups/0/text"),
    ("source_messaging", "/template_id"),
    ("source_messaging", "/product_identity/long_name"),
    ("source_messaging", "/source_messaging/0/block"),
    ("source_messaging", "/source_messaging/0/fields/0/label"),
    ("source_messaging", "/etail_messaging/0/container"),
    ("source_messaging", "/footnotes/0/status"),
])
def test_structured_non_content_is_rejected_consistently(
    document, pointer, approved_catalog, camera, references
):
    from v6_4.validation import _pointer_value

    request = structured_request()
    quote, _ = _pointer_value(request[document], pointer)
    value = valid_output()
    candidate = value["prompts"][0]
    candidate["evidence"] = [{"document": document, "path": pointer, "quote": quote}]
    candidate["score_components"][document]["setting"] = 10
    candidate["relationship"] = "source_adjacent"
    assert "evidence_authoring_metadata" in result_codes(
        validate(value, request, approved_catalog, camera, references)
    )
    normalized, changes = normalize_invalid_evidence(value, request)
    assert normalized["prompts"][0]["evidence"] == []
    assert normalized["prompts"][0]["score_components"][document]["setting"] == 0
    assert normalized["prompts"][0]["relationship"] == "creative_departure"
    assert any(item.get("reason") == "authoring_metadata" for item in changes)
    assert value["prompts"][0]["evidence"]


@pytest.mark.parametrize("document,pointer,quote", [
    ("smart_brief", "/USE CASES/content", "Focused work"),
    ("source_messaging", "/product_identity/target_audience", "Office teams."),
    ("source_messaging", "/source_messaging/0/fields/0/value", "Office collaboration."),
    ("source_messaging", "/etail_messaging/0/value", "Home and office work."),
    ("source_messaging", "/footnotes/0/text", "Synthetic evaluation only."),
])
def test_structured_content_and_qualifications_remain_citable(
    document, pointer, quote, approved_catalog, camera, references
):
    request = structured_request()
    value = valid_output()
    value["prompts"][0]["evidence"] = [{"document": document, "path": pointer, "quote": quote}]
    result = validate(value, request, approved_catalog, camera, references)
    assert result["passed"], result["errors"]
    normalized, changes = normalize_invalid_evidence(value, request)
    assert normalized == value
    assert changes == []


def test_structured_row_id_is_not_an_array_index():
    request = structured_request()
    value = valid_output()
    value["prompts"][0]["evidence"] = [{
        "document": "source_messaging",
        "path": "/source_messaging/0/fields/104/value",
        "quote": "Office collaboration.",
    }]
    normalized, changes = normalize_invalid_evidence(value, request)
    assert normalized["prompts"][0]["evidence"] == []
    assert any(item.get("reason") == "path_missing" for item in changes)


def test_arbitrary_legacy_label_and_confidence_keys_are_not_globally_blocked():
    request = {
        "smart_brief": {"confidence": "A welcoming office."},
        "source_messaging": {"label": "Useful office context."},
    }
    value = valid_output()
    value["prompts"][0]["evidence"] = [
        {"document": "smart_brief", "path": "/confidence", "quote": "A welcoming office."},
        {"document": "source_messaging", "path": "/label", "quote": "Useful office context."},
    ]
    normalized, changes = normalize_invalid_evidence(value, request)
    assert normalized == value
    assert changes == []


def test_creative_departure_uses_derived_component_max_score(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    candidate = value["prompts"][0]
    candidate["evidence"] = [
        {"document": "smart_brief", "path": "", "quote": "collaborative office"}
    ]
    candidate["score_components"]["smart_brief"].update(
        {"setting": 30, "activity": 30, "materials": 0, "use_context": 0}
    )
    assert "creative_departure_score" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


def test_duplicate_prompt_normalization(raw_request, approved_catalog, camera, references) -> None:
    value = valid_output()
    value["prompts"][1]["text"] = "  " + value["prompts"][0]["text"].upper() + "  "
    assert "duplicate_prompt_text" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


def test_longest_object_matches_protect_binder_clips_and_water_glass(
    raw_request, camera, references
) -> None:
    approved = catalog(
        entry("OFF-BINDER", ["paper_fasteners"], ["binder clip", "binder clips"]),
        entry("OFF-GLASS", ["drinkware"], ["water glass", "water glasses"]),
    )
    value = valid_output()
    value["prompts"][0]["text"] = (
        "An ordinary office desk has binder clips and a water glass in warm light."
    )
    value["prompts"][0]["prop_ids"] = ["OFF-BINDER", "OFF-GLASS"]
    result = validate(value, raw_request, approved, camera, references)
    assert result["passed"], result["errors"]


def test_sticky_note_pad_is_the_declared_sticky_notes_group(
    raw_request, camera, references
) -> None:
    approved = catalog(
        entry("OFF-STICKY", ["sticky_notes"], ["sticky notes"]),
    )
    value = valid_output()
    value["prompts"][0]["text"] = (
        "An ordinary office desk has a pair of blank sticky-note pads in warm light."
    )
    value["prompts"][0]["prop_ids"] = ["OFF-STICKY"]
    result = validate(value, raw_request, approved, camera, references)
    assert result["passed"], result["errors"]


def test_business_activity_does_not_invent_a_visible_paper_prop(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = (
        "A calm office workspace for a forms intake check in warm light."
    )
    codes = result_codes(validate(value, raw_request, approved_catalog, camera, references))
    assert "unnatural_place_phrase" in codes
    assert "undeclared_known_prop" not in codes


@pytest.mark.parametrize(
    "phrase",
    [
        "office focus table",
        "planning desk",
        "operations counter",
        "administration nook",
        "administrative office desk",
        "shared office hub",
        "shared department team",
        "classroom activity table",
        "family learning table",
        "home craft table",
        "IT fleet planning",
        "managed workplace feel",
        "meeting handoff",
        "meeting handoffs",
        "office workgroups",
        "senior leader",
        "IT team",
        "finance team",
        "shared-space work stop",
        "shared-space stop",
        "background reduced to a soft office wall",
        "only a narrow slice of the room",
        "without showing a wider studio spread",
        "close view",
        "close arrangement",
        "close study area",
        "an upholstered banquette falls softly behind the table",
        "a sand timer set into warm window light",
        "ordinary shared work paused between tasks",
        "work has paused between tasks",
        "the paused review",
        "the organized display feeling neat",
        "the banquette sits softly behind the table",
        "an RGB strip along the background edge",
        "a desk used for preparing for a meeting",
        "the office feels polished and quietly active",
        "a shared-space setting",
        "shared space calm between appointments",
        "a classroom study table",
        "a strip of upholstered banquette in the background",
        "a section of a sofa beside the table",
        "an ordinary upholstered office chair partly visible nearby",
        "a studio stool partially visible near the table",
        "a low storage cabinet sits softly in the background",
        "a textbook on a plain unmarked cover",
        "a menu on a background table",
        "loose office tasks are kept in order",
    ],
)
def test_business_activity_is_not_a_furniture_type(
    phrase, raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = f"A calm {phrase} in warm light."
    assert "unnatural_place_phrase" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


def test_unnatural_physical_language_is_rejected_in_explanations(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["camera_fit_explanation"] = (
        "The artwork can sit softly in the nearby wall area."
    )
    assert "unnatural_prompt_field_phrase" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


@pytest.mark.parametrize(
    "phrase",
    [
        "executive refresh meeting",
        "leadership meeting",
        "senior manager desk",
        "busy department",
        "fleet-standardization meeting",
        "office workflow",
        "standards discussion",
        "contracts and invoices",
        "meeting packets",
        "client-facing discussion",
        "follow-through session",
        "shared office work",
    ],
)
def test_enterprise_source_language_stays_out_of_scene_prose(
    phrase, raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = f"An office desk prepared for a {phrase}."
    assert "enterprise_scene_language" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


@pytest.mark.parametrize("phrase", ["supplies", "personal items", "accessories", "simple workplace materials"])
def test_vague_object_categories_cannot_introduce_unapproved_props(
    phrase, raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = f"An office desk with shared {phrase} in warm light."
    assert "vague_unapproved_object_category" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


def test_environment_label_must_match_scene_setting(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = "A home-office desk in warm daylight."
    assert "environment_text_conflict" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


@pytest.mark.parametrize(
    "phrase,code",
    [
        ("near a shared windowed area", "unnatural_place_phrase"),
        ("ready for a household task", "environment_text_conflict"),
        ("rather than a formal workplace scene", "unnatural_place_phrase"),
        ("without adding a busy office scene", "unnatural_place_phrase"),
    ],
)
def test_scene_does_not_use_meta_or_cross_environment_wording(
    phrase, code, raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = f"An office desk {phrase}."
    assert code in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


def test_known_object_must_be_declared_and_mentions_must_be_verbatim(
    raw_request, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = "A calm office workspace with a notebook in warm light."
    assert "undeclared_known_prop" in result_codes(
        validate(value, raw_request, catalog(), camera, references)
    )

    approved = catalog(entry("OFF-NOTE", ["paper_materials"], ["notebook", "notebooks"]))
    value = valid_output()
    value["prompts"][0]["prop_ids"] = ["OFF-NOTE"]
    value["prompts"][0]["prop_mentions"] = [{"id": "OFF-NOTE", "quote": "notebook"}]
    assert "prop_mention_not_verbatim" in result_codes(
        validate_output(value, raw_request, approved, camera, references)
    )


def test_generic_seating_is_a_declared_chair_furnishing(
    raw_request, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = (
        "An office workspace with nearby seating in warm light."
    )
    assert "undeclared_known_prop" in result_codes(
        validate(value, raw_request, catalog(), camera, references)
    )

    approved = catalog(
        entry(
            "OFF-CHAIR",
            ["task_seating"],
            ["chair", "chairs"],
            role="background_furnishing_or_decor",
        )
    )
    value["prompts"][0]["prop_ids"] = ["OFF-CHAIR"]
    result = validate(value, raw_request, approved, camera, references)
    assert "undeclared_known_prop" not in result_codes(result)
    assert "declared_prop_missing_from_text" not in result_codes(result)


def test_nonhuman_safety_adjective_preserves_declared_figurine_match(
    raw_request, camera, references
) -> None:
    approved = catalog(
        entry(
            "GAM-FIG",
            ["figurine"],
            ["original unbranded miniature figure"],
            environment="Gaming",
        )
    )
    value = valid_output()
    value["prompts"][9]["text"] = (
        "A gaming room with an original unbranded nonhuman miniature figure in warm light."
    )
    value["prompts"][9]["prop_ids"] = ["GAM-FIG"]
    result = validate(value, raw_request, approved, camera, references)
    assert "declared_prop_missing_from_text" not in result_codes(result)
    assert "human_face_request" not in result_codes(result)


def test_safe_adjectives_preserve_declared_wooden_model_match(
    raw_request, camera, references
) -> None:
    approved = catalog(
        entry(
            "STU-MODEL",
            ["prototype_model"],
            ["small wooden model"],
            environment="Creative Studio",
        )
    )
    value = valid_output()
    value["prompts"][8]["text"] = (
        "A creative studio table with a small abstract wooden architectural model."
    )
    value["prompts"][8]["prop_ids"] = ["STU-MODEL"]
    result = validate(value, raw_request, approved, camera, references)
    assert "declared_prop_missing_from_text" not in result_codes(result)
    assert "face_bearing_prop_treatment" not in result_codes(result)


def test_prop_approval_environment_and_duplicate_groups(raw_request, camera, references) -> None:
    duplicate_group_catalog = catalog(
        entry("OFF-NOTE-A", ["paper_materials"], ["paper_materials"]),
        entry("OFF-NOTE-B", ["paper_materials"], ["sketchbook"]),
    )
    value = valid_output()
    value["prompts"][0]["text"] = "An office workspace with a notebook in warm light."
    value["prompts"][0]["prop_ids"] = ["OFF-NOTE-A", "OFF-NOTE-B"]
    assert "duplicate_candidate_group" in result_codes(
        validate(value, raw_request, duplicate_group_catalog, camera, references)
    )

    home_catalog = catalog(
        entry("HOM-NOTE", ["paper_materials"], ["paper_materials"], environment="Home")
    )
    value["prompts"][0]["prop_ids"] = ["HOM-NOTE"]
    assert "prop_environment_mismatch" in result_codes(
        validate(value, raw_request, home_catalog, camera, references)
    )


def test_repetition_groups_are_global_across_environment_and_background(
    raw_request, camera, references
) -> None:
    approved = catalog(
        entry("OFF-PLANT", ["plant"], ["plant", "plants"], role="background_furnishing_or_decor"),
        entry(
            "HOM-PLANT",
            ["plant"],
            ["plant", "plants"],
            environment="Home",
            role="background_furnishing_or_decor",
        ),
    )
    value = valid_output()
    value["prompts"][0]["text"] = "An office workspace with a plant in warm light."
    value["prompts"][0]["prop_ids"] = ["OFF-PLANT"]
    value["prompts"][1].update(
        {
            "environment": "Home",
            "text": "A home workspace with a plant in warm light.",
            "prop_ids": ["HOM-PLANT"],
            "ctech_reference_id": "CT04",
        }
    )
    assert "repetition_group_reused" in result_codes(
        validate(value, raw_request, approved, camera, references)
    )


def test_hardware_boundary_furniture_desktop_and_display_shelving(
    raw_request, camera, references
) -> None:
    approved = catalog(
        entry(
            "OFF-SHELF",
            ["open_shelving"],
            ["display shelving", "shelving"],
            role="background_furnishing_or_decor",
        ),
        entry(
            "OFF-SCULPTURE",
            ["desk_sculpture"],
            ["abstract wood sculpture", "wood sculpture"],
        ),
    )
    value = valid_output()
    value["prompts"][0]["text"] = (
        "An office with a walnut desktop and display shelving holding an abstract wood sculpture in warm neutral light."
    )
    value["prompts"][0]["prop_ids"] = ["OFF-SHELF", "OFF-SCULPTURE"]
    result = validate(value, raw_request, approved, camera, references)
    assert result["passed"], result["errors"]

    value["prompts"][0]["text"] = "An office workspace with a laptop in warm light."
    value["prompts"][0]["prop_ids"] = []
    assert "computing_hardware" in result_codes(
        validate(value, raw_request, approved, camera, references)
    )


@pytest.mark.parametrize(
    "product_description",
    [
        "a desktop",
        "two desktops",
        "the primary device",
        "visible ports",
        "a narrow bezel",
        "the screen",
    ],
)
def test_primary_device_and_appearance_descriptions_are_forbidden(
    product_description, raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = (
        f"An office workspace showing {product_description} in warm neutral light."
    )
    assert "computing_hardware" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


def test_noncomputing_room_screen_is_not_treated_as_hardware(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = (
        "An office desk stands beside an acoustic screen in warm neutral light."
    )
    result = validate(value, raw_request, approved_catalog, camera, references)
    assert result["passed"], result["errors"]


def test_no_object_noun_quota_when_approved_groups_are_not_repeated(
    raw_request, camera, references
) -> None:
    approved = catalog(
        entry(
            "OFF-CHAIR",
            ["task_seating"],
            ["chair", "chairs"],
            role="background_furnishing_or_decor",
        ),
        entry(
            "OFF-PLANT",
            ["plant"],
            ["plant", "plants"],
            role="background_furnishing_or_decor",
        ),
        entry(
            "OFF-ART",
            ["framed_wall_art"],
            ["wall art"],
            role="background_furnishing_or_decor",
        ),
    )
    value = valid_output()
    value["prompts"][0]["text"] = (
        "An office desk sits with chairs, a plant, and abstract wall art in warm neutral light."
    )
    value["prompts"][0]["prop_ids"] = ["OFF-CHAIR", "OFF-PLANT", "OFF-ART"]
    result = validate(value, raw_request, approved, camera, references)
    assert result["passed"], result["errors"]


def test_camera_directives_and_obvious_top_oblique_conflicts(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0]["text"] = "An office workspace; widen the view toward warm light."
    assert "camera_motion_directive" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )

    value = valid_output()
    value["prompts"][0]["text"] = "An office workspace beneath tall windows in warm light."
    eye_level_with_negative_guidance = {
        **camera,
        "guidance": ["The selected view is not overhead or top-oblique."],
    }
    assert "top_oblique_incompatible_scene" not in result_codes(
        validate(
            value,
            raw_request,
            approved_catalog,
            eye_level_with_negative_guidance,
            references,
        )
    )

    top = {**camera, "elevation": "top_oblique"}
    assert "top_oblique_incompatible_scene" in result_codes(
        validate(value, raw_request, approved_catalog, top, references)
    )


def test_open_binder_cannot_be_contained_by_letter_tray(
    raw_request, camera, references
) -> None:
    approved = catalog(
        entry("OFF-BINDER", ["paper_materials"], ["ring binder"]),
        entry("OFF-TRAY", ["letter_tray"], ["letter tray"]),
    )
    value = valid_output()
    value["prompts"][0]["text"] = (
        "An office desk with an open ring binder showing blank pages in a letter tray."
    )
    value["prompts"][0]["prop_ids"] = ["OFF-BINDER", "OFF-TRAY"]
    assert "implausible_prop_arrangement" in result_codes(
        validate(value, raw_request, approved, camera, references)
    )

    value["prompts"][0]["text"] = (
        "An office desk with an open ring binder showing blank pages beside a letter tray."
    )
    assert "implausible_prop_arrangement" not in result_codes(
        validate(value, raw_request, approved, camera, references)
    )


def test_architectural_forms_are_not_paper_forms_or_enterprise_language(
    raw_request, camera, references
) -> None:
    approved = catalog(
        entry(
            "STU-MODEL",
            ["prototype_model"],
            ["wooden model"],
            environment="Creative Studio",
        )
    )
    value = valid_output()
    value["prompts"][8]["text"] = (
        "A creative studio table with a small wooden model of simple architectural forms "
        "and no human figures."
    )
    value["prompts"][8]["prop_ids"] = ["STU-MODEL"]
    result = validate(value, raw_request, approved, camera, references)
    codes = result_codes(result)
    assert "undeclared_known_prop" not in codes
    assert "enterprise_scene_language" not in codes
    assert "face_bearing_prop_treatment" not in codes


def test_ctech_environment_rules_and_score_100_exactness(
    raw_request, approved_catalog, camera, references
) -> None:
    value = valid_output()
    value["prompts"][0].update(
        {"environment": "Education", "ctech_reference_id": "CT04"}
    )
    result = validate(value, raw_request, approved_catalog, camera, references)
    assert "ctech_environment_mismatch" not in result_codes(result)

    value["prompts"][0].update(
        {"environment": "Gaming", "ctech_reference_id": "CT04"}
    )
    assert "ctech_environment_mismatch" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )

    value = valid_output()
    value["prompts"][0]["ctech_reference_score"] = 100
    assert "ctech_exact_match_required" in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )
    value["prompts"][0]["text"] = "Exact CT01 scene."
    assert "ctech_exact_match_required" not in result_codes(
        validate(value, raw_request, approved_catalog, camera, references)
    )


def test_finalizer_ranks_adds_ids_and_preserves_raw_fields(camera, approved_catalog) -> None:
    value = valid_output()
    original = copy.deepcopy(value)
    first, second, third = value["prompts"][:3]
    first["ctech_reference_score"] = 60
    second["ctech_reference_score"] = 90
    for candidate in value["prompts"][3:]:
        candidate["ctech_reference_score"] = 50
    third["score_components"]["smart_brief"]["setting"] = 10
    # Unsupported source-messaging score is deliberately retained; validation
    # reports it and finalization must not silently zero it.
    third["score_components"]["source_messaging"]["activity"] = 20
    original = copy.deepcopy(value)

    finalized = finalize_output(value, camera=camera, catalog=approved_catalog)
    assert value == original
    assert [item["id"] for item in finalized["prompts"]] == [f"p{i}" for i in range(1, 11)]
    assert finalized["prompts"][0]["text"] == third["text"]
    assert finalized["prompts"][0]["source_relevance_score"] == 30
    assert finalized["prompts"][0]["score_components"]["source_messaging"]["activity"] == 20
    assert finalized["prompts"][1]["text"] == second["text"]
    assert finalized["prompts"][2]["text"] == first["text"]
    assert finalized["prompts"][0]["evidence"] == third["evidence"]
    assert finalized["prompts"][0]["primary_support"]["phrase"] in third["text"]
    assert finalized["debug"]["primary_support_audit"]["passed"] is True
    assert finalized["debug"]["provenance"]["camera"] == camera
    assert finalized["debug"]["provenance"]["catalog"]["revision"] == "test-approved-r1"


def test_finalizer_stable_for_exact_score_ties(camera, approved_catalog) -> None:
    value = valid_output()
    texts = [candidate["text"] for candidate in value["prompts"]]
    finalized = finalize_output(value, camera=camera, catalog=approved_catalog)
    assert [candidate["text"] for candidate in finalized["prompts"]] == texts


def test_finalizer_shape_audit_counts_primary_oval_without_counting_it_round(
    camera, approved_catalog
) -> None:
    value = valid_output()
    value["prompts"][1]["text"] = (
        "An oval office table anchors a calm office workspace beside a round wall mirror."
    )

    finalized = finalize_output(value, camera=camera, catalog=approved_catalog)

    counts = finalized["debug"]["primary_support_audit"]["counts"]["shapes"]
    assert counts["round"] == 2
    assert counts["oval"] == 1
    candidate = next(item for item in finalized["prompts"] if "oval office table" in item["text"])
    assert candidate["primary_support"]["shape"] == "oval"
