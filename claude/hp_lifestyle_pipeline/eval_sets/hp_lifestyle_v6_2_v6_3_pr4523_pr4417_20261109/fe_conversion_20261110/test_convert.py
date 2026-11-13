import copy
import json

import pytest

import convert as fe
import clean_reports


@pytest.fixture(scope="module")
def source():
    return json.loads((fe.PUBLIC / "data/comparison.json").read_text())


def test_preserves_every_row_output_input_prompt_and_original_record(source):
    _, result = fe.convert(source)
    assert result["meta_texts"][0] == fe.TITLE
    assert result["is_secure"] is True
    assert len(result["rows"]) == 30
    for original, row in zip(source["rows"], result["rows"]):
        assets = row["images"]
        assert [a["image_src"] for a in assets[:4]] == [
            fe.media_url(original["outputs"][name]["image"]) for name, _ in fe.CELLS
        ]
        assert "NOT PR4523" in assets[4]["meta_text"]["label"]
        assert [a["image_src"] for a in assets[5:18]] == [
            fe.media_url(original["twin"]),
            *[fe.media_url(original["outputs"][name]["inputs"][field])
              for name, _ in fe.CELLS for field in ("geometry_guide", "product", "reference")],
        ]
        assert all(a["is_model_input_or_output"] == "model_input" for a in assets[5:18])
        assert [a["text_content"] for a in assets[18:20]] == [
            original["prompts"][writer]["text"] for writer in ("v6_2", "v6_3")
        ]
        assert json.loads(row["meta_data"]["key_val_informations"]["Complete original row JSON"]) == original
    assert len(result["links"]) == 12


@pytest.mark.parametrize("change,message", [
    ("duplicate", "duplicate comparison row"),
    ("prompt", "source prompt text/hash/bank binding"),
    ("pipeline", "wrong pinned pipeline"),
    ("image", "source media or record escapes"),
])
def test_rejects_lost_or_misattributed_source_evidence(source, change, message):
    data = copy.deepcopy(source)
    if change == "duplicate":
        data["rows"][1] = data["rows"][0]
    elif change == "prompt":
        data["rows"][0]["prompts"]["v6_3"]["text"] += " edited"
    elif change == "pipeline":
        data["rows"][0]["outputs"]["v6_3_pr4417"]["lineage"]["source_commit"] = "different"
    else:
        data["rows"][0]["outputs"]["v6_3_pr4417"]["image"] = "https://example.com/wrong.png"
    with pytest.raises(ValueError, match=message):
        fe.convert(data)


@pytest.mark.parametrize("cell", [None, *(name for name, _ in fe.CELLS)])
def test_clean_reports_have_only_requested_outputs_and_no_details(source, cell):
    result = clean_reports.convert(source, cell)
    choices = [(name, label) for name, label in fe.CELLS if cell is None or name == cell]
    assert set(result) == {"is_secure", "meta_texts", "rows"}
    assert result["is_secure"] is True
    assert len(result["meta_texts"]) == 1
    assert len(result["rows"]) == 30
    for original, row in zip(source["rows"], result["rows"]):
        assert row["meta_data"]["key_val_informations"] is None
        assert row["meta_data"]["evalset_item_id"] == " / ".join(map(str, original["key"]))
        assert row["images"] == [
            {"asset_type": "image", "image_src": fe.media_url(original["outputs"][name]["image"]),
             "meta_text": {"label": label}}
            for name, label in choices
        ]


def test_unknown_clean_report_is_an_error(source):
    with pytest.raises(ValueError, match="unknown comparison column"):
        clean_reports.convert(source, "historical")
