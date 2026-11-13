import copy
from urllib.parse import urljoin

import pytest

import report
import study


@pytest.fixture
def comparison_inputs():
    baseline = study.load(study.HERE / "baseline_live/data/generation.json")
    prompts = study.load(study.HERE / "selection/selected_v6_5_30.json")["prompts"]
    feedback = study.load(study.FEEDBACK)
    dispositions = study.load(
        study.PROJECT / "research/prompt_writer_v6_5/replacement_training_20261111/astra/proposal.json"
    )["feedback_disposition"]
    source = study.load(study.TEXT)
    outputs = {p["prompt_key"]: {"image": "new/" + p["prompt_key"]} for p in prompts}
    return baseline, prompts, feedback, dispositions, outputs, source


def test_comparison_preserves_exact_original_images_prompts_feedback_and_sources(comparison_inputs):
    baseline, prompts, feedback, actions, outputs, source = comparison_inputs
    result = report.assemble(baseline, list(reversed(prompts)), feedback, list(reversed(actions)), outputs, source)
    for row, original, note in zip(result, baseline["rows"], feedback["rows"], strict=True):
        assert row["key"] == original["key"]
        assert row["v6_4"]["image"] == note["image_url"]
        assert row["v6_4"]["original_image_reference"] == original["output"]["image"]
        assert row["v6_4"]["prompt"] == original["prompt"]["text"]
        assert row["source_input"] == original["source_input"]
        assert row["feedback"] == note["feedback"]["comment"]
        assert row["astra_disposition"]["review_key"] == note["review_key"]
        prompt = next(p for p in prompts if list(study.slot(p)) == row["key"])
        assert row["v6_5"]["prompt"] == prompt["text"]
        assert row["v6_5"]["image"] == outputs[prompt["prompt_key"]]["image"]


@pytest.mark.parametrize("mutation", ["old_prompt", "old_image", "source", "duplicate_note"])
def test_comparison_rejects_mismatched_review_or_source_bindings(comparison_inputs, mutation):
    args = copy.deepcopy(comparison_inputs)
    if mutation == "old_prompt":
        args[0]["rows"][0]["prompt"]["text"] += " changed"
    elif mutation == "old_image":
        args[0]["rows"][0]["output"]["image_sha256"] = "0" * 64
    elif mutation == "source":
        args[0]["rows"][0]["source_input"]["smart_brief"] = {}
    else:
        args[2]["rows"][1] = args[2]["rows"][0]
    with pytest.raises(ValueError):
        report.assemble(*args)


def test_relative_asset_paths_preserve_original_authenticated_objects(comparison_inputs):
    baseline, *_ = comparison_inputs
    for row in baseline["rows"]:
        original_url = urljoin(report.BASELINE_GALLERY, row["output"]["image"])
        relative = report.relative_asset(original_url)
        assert not relative.startswith(("http:", "https:", "/"))
        assert urljoin(report.BASE + "gallery/index.html", relative) == original_url
    with pytest.raises(ValueError):
        report.relative_asset("https://example.com/image.png")
