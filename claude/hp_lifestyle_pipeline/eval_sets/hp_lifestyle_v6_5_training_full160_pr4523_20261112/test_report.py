"""Structural merge tests use actual frozen sources, not invented native-success evidence."""
import copy
from urllib.parse import urljoin

import pytest

import report
import study


@pytest.fixture
def sources():
    old = study.load(study.HERE / "baseline_live/full/data.json")
    grouped = study.load(study.HERE / "baseline_live/grouped/data.json")
    original_fe = study.load(study.HERE / "baseline_live/full/fe/data.json")
    prompts = study.load(study.SOURCE)
    original_slots = {tuple(row["key"]): row for row in old["rows"]}
    rows = []
    for prompt in prompts["prompts"]:
        slot = (prompt["device_id"], prompt["camera_tag"], prompt["bank_rank"])
        output = copy.deepcopy(original_slots[slot]["outputs"]["v6_4_pr4523"])
        origin = study.GATEWAY + report.FULL + "/gallery/index.html"
        for name in ("image", "record_url", "job_url", "status_url"):
            output[name] = urljoin(origin, output[name])
        output["inputs"] = {name: urljoin(origin, value) for name, value in output["inputs"].items()}
        bank = prompts["bank_audit"][prompt["bank_debug_ref"]]
        rows.append({
            "key": list(slot), "prompt": prompt, "source_input": bank["source_input"],
            "bank_audit": bank, "output": output,
        })
    mock_new = {
        "rows": list(reversed(rows)), "counts": {"done": 160}, "built_at_utc": "structural-test-only",
        "text_recovery_provenance": {"structural_fixture_not_native_generation": True},
    }
    return old, grouped, original_fe, mock_new


def test_actual_source_merges_preserve_original_cells_contexts_and_annotation_ids(sources):
    old, grouped, original_fe, mock_new = sources
    result = report.full_merge(old, mock_new)
    for before, after in zip(old["rows"], result["rows"]):
        restored = copy.deepcopy(after)
        for name in ("prompt_v6_5", "source_input_v6_5", "bank_audit_v6_5"):
            del restored[name]
        del restored["outputs"][report.CELL]
        assert restored == before
    fe = report.fe_merge(original_fe, old, mock_new)
    for before, after in zip(original_fe["rows"], fe["rows"]):
        restored = copy.deepcopy(after)
        assert len(restored["images"]) == 4
        restored["images"].pop()
        assert restored == before
    four, two = report.grouped_merge(grouped, mock_new, old)
    for before, after in zip(grouped["groups"], four["groups"]):
        restored = copy.deepcopy(after)
        restored["experiments"].pop()
        restored["contexts"].pop()
        assert restored == before
    assert two["experiment_count"] == 2 and two["image_count"] == 320
    assert four["experiment_count"] == 4 and four["image_count"] == 640
    for group in two["groups"]:
        assert [experiment["id"] for experiment in group["experiments"]] == ["v6_4_pr4523", report.CELL]
        for experiment in group["experiments"]:
            assert [card["rank"] for card in experiment["cards"]] == list(range(1, 11))
            assert all(card["inputs"] and card["generation_prompt"] for card in experiment["cards"])


@pytest.mark.parametrize("damage", ["duplicate", "missing", "camera", "source", "pending"])
def test_reject_incomplete_or_misbound_new_rows(sources, damage):
    old, _grouped, _fe, mock_new = sources
    if damage == "duplicate":
        mock_new["rows"][-1] = copy.deepcopy(mock_new["rows"][0])
    elif damage == "missing":
        mock_new["rows"].pop()
    elif damage == "camera":
        mock_new["rows"][0]["prompt"] = {**mock_new["rows"][0]["prompt"], "source_camera_name": "wrong"}
    elif damage == "source":
        mock_new["rows"][0]["source_input"] = {"unapproved": "other source"}
    else:
        mock_new["rows"][0]["output"]["status"] = "pending"
    with pytest.raises(ValueError):
        report.full_merge(old, mock_new)


def test_reject_original_grouped_card_drift_and_external_references(sources):
    old, grouped, _fe, mock_new = sources
    grouped["groups"][0]["experiments"][0]["cards"][0]["prompt"] += " altered"
    with pytest.raises(ValueError, match="existing grouped card"):
        report.grouped_merge(grouped, mock_new, old)
    with pytest.raises(ValueError, match="escapes"):
        report.rebase("https://example.invalid/output.png", study.PREFIX)
