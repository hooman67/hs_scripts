import copy

import pytest

import build_report as build


@pytest.fixture(scope="module")
def sources():
    return (
        build.study.load(build.HERE / "source/data.json"),
        build.study.load(build.V65 / "public/data/generation.json"),
        build.study.load(build.V65 / "extension/full/fe/data.json"),
        build.study.load(build.V65 / "extension/full/data/comparison_v6_5_training_160_20261112.json"),
    )


def test_all_source_columns_metadata_and_prompts_survive_exact_key_join(sources):
    original, generation, official, baseline = sources
    result, mapping, _labels = build.merge(original, generation, official, baseline)
    by_key = {row["prompt"]["prompt_key"]: row for row in generation["rows"]}
    for before, after, binding in zip(original["rows"], result["rows"], mapping):
        assert after["meta_data"] == before["meta_data"]
        assert after["images"][:4] == before["images"][:4]
        assert after["images"][5] == before["images"][4]
        native = by_key[binding["v65_prompt_key"]]
        assert after["images"][4]["image_src"] == native["output"]["image"]
        assert after["images"][6]["text_content"] == native["prompt"]["text"]
    assert len({item["v65_prompt_key"] for item in mapping}) == 160


@pytest.mark.parametrize("defect", ("duplicate", "rank", "prompt", "missing"))
def test_mismatched_or_incomplete_sources_are_rejected(sources, defect):
    original, generation, official, baseline = sources
    original, generation = copy.deepcopy(original), copy.deepcopy(generation)
    if defect == "duplicate":
        original["rows"][1] = copy.deepcopy(original["rows"][0])
    elif defect == "rank":
        original["rows"][0]["meta_data"]["key_val_informations"]["Prompt rank"] = 10
    elif defect == "prompt":
        original["rows"][0]["images"][4]["text_content"] += " changed"
    else:
        generation["rows"].pop()
    with pytest.raises(ValueError):
        build.merge(original, generation, official, baseline)
