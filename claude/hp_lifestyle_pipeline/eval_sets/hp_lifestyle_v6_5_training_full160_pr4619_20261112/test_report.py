import copy
import json
import re

import pytest

import report
import study


@pytest.fixture
def sources():
    original = study.load(study.HERE / "source/fe/data.json")
    cases = study.load(study.HERE / "cases.json")
    new = {
        case["prompt_key"]: {
            "prompt": case["prompt"],
            "output": {
                "image": study.GATEWAY + "unit-test-only/" + case["id"] + ".png",
                "statistics_status": "NO STATISTICS - test fixture",
            },
        } for case in cases
    }
    return original, cases, new


def test_six_and_two_column_views_preserve_actual_source_assets_and_join_by_key(sources):
    original, _, new = sources
    original["rows"].reverse()
    before = copy.deepcopy(original)
    six, pair = report.merge_fe(original, new)
    assert original == before
    for old, extended, paired in zip(original["rows"], six["rows"], pair["rows"]):
        key = study.prompt_key(old)
        assert extended["images"][:5] == old["images"][:5]
        assert extended["images"][6:] == old["images"][5:]
        assert extended["images"][5]["image_src"] == new[key]["output"]["image"]
        assert paired["images"] == [
            old["images"][1], extended["images"][5], old["images"][5], old["images"][6],
        ]
        assert extended["meta_data"]["evalset_item_id"] == old["meta_data"]["evalset_item_id"]
        old_fields = old["meta_data"]["key_val_informations"]
        assert all(extended["meta_data"]["key_val_informations"][k] == v for k, v in old_fields.items())
        assert "NO STATISTICS" in extended["meta_data"]["key_val_informations"]["V6.5 / V15.8 statistics"]


@pytest.mark.parametrize("damage", ["missing", "duplicate", "changed_prompt", "wrong_rank"])
def test_fe_rejects_missing_duplicate_or_misbound_sources(sources, damage):
    original, _, new = sources
    key = study.prompt_key(original["rows"][0])
    if damage == "missing":
        del new[key]
    elif damage == "duplicate":
        original["rows"][1] = copy.deepcopy(original["rows"][0])
    elif damage == "changed_prompt":
        new[key]["prompt"] = {**new[key]["prompt"], "text": "Not the frozen original prompt"}
    else:
        original["rows"][0]["meta_data"]["key_val_informations"]["Prompt rank"] = 99
    with pytest.raises(ValueError):
        report.merge_fe(original, new)


def test_grouped_views_preserve_every_original_card_and_reject_wrong_native_rank(sources):
    _, cases, _ = sources
    original = study.load(study.HERE / "source/grouped/data.json")
    before = copy.deepcopy(original)
    new = {case["prompt_key"]: {
        "prompt_key": case["prompt_key"], "rank": case["rank"], "image": "test-only.png",
    } for case in cases}
    old = {key: {**value, "label": "Existing native V6.4"} for key, value in new.items()}
    extended, paired = report.merge_grouped(original, new, old)
    assert original == before
    assert extended["image_count"] == 480 and paired["image_count"] == 320
    for source, three, pair in zip(original["groups"], extended["groups"], paired["groups"]):
        assert three["experiments"][:2] == source["experiments"]
        assert three["contexts"] == source["contexts"] == pair["contexts"]
        assert pair["experiments"][1] == three["experiments"][2]
        assert len(pair["experiments"][0]["cards"]) == 10
    key = next(iter(new))
    new[key]["rank"] = 99
    with pytest.raises(ValueError, match="incorrect key/rank"):
        report.merge_grouped(original, new, old)


def test_viewer_appends_sixth_method_without_redefining_original_five(sources):
    original, _, _ = sources
    html = (study.HERE / "source/fe/viewer.html").read_text()
    labels = [a["meta_text"]["label"] for a in original["rows"][0]["images"][:5]]
    six = report.viewer(html, labels + [study.LABEL], "Six", 6)
    pair = report.viewer(html, [labels[1], study.LABEL], "Pair", 2)
    pattern = r"const METHOD_RATING_DEFS = (\[[^\n]*\])\.map"
    assert json.loads(re.search(pattern, six)[1]) == labels + [study.LABEL]
    assert json.loads(re.search(pattern, pair)[1]) == [labels[1], study.LABEL]
    assert "grid-template-columns: repeat(6, auto);" in six
    assert "grid-template-columns: repeat(2, auto);" in pair
    scope = r"const (?:ANNO_KEY|STORE_SCOPE|QUESTIONS_KEY|HIDDEN_COLUMNS_KEY) = [^\n]+"
    assert re.findall(scope, six) == re.findall(scope, html)
    with pytest.raises(ValueError, match="method-rating identities"):
        report.viewer(html, ["Different first column"] + labels[1:] + [study.LABEL], "Bad", 6)
