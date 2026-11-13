import copy
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("rank_matched_v64_study", Path(__file__).with_name("study.py"))
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def sources():
    full = study.load(study.TEXT)
    prior = study.load(study.OLD / "public/data/comparison.json")
    return [r["prompts"]["v6_3"] for r in prior["rows"]], full


def test_matches_actual_thirty_slots_without_changing_records():
    old, full = sources()
    selected = study.select_matched(old, full)
    assert [study.slot(p) for p in selected] == [study.slot(p) for p in old]
    assert all(p in full["prompts"] for p in selected)
    assert len({(p["device_id"], p["camera_tag"]) for p in selected}) == 16
    selected[0]["text"] = "modified test copy"
    assert selected[0] not in full["prompts"]


def test_rejects_duplicate_or_missing_slots():
    old, full = sources()
    with pytest.raises(ValueError, match="thirty unique"):
        study.select_matched([old[0]] * 30, full)
    broken = copy.deepcopy(full)
    broken["prompts"][-1] = broken["prompts"][0]
    with pytest.raises(ValueError, match="160 unique"):
        study.select_matched(old, broken)


def test_rejects_camera_drift_and_text_tampering():
    old, full = sources()
    broken = copy.deepcopy(old)
    broken[0]["render_lookup"] = {}
    with pytest.raises(ValueError, match="binding differs"):
        study.select_matched(broken, full)
    broken = copy.deepcopy(full)
    target = next(p for p in broken["prompts"] if study.slot(p) == study.slot(old[0]))
    target["text"] += " altered"
    with pytest.raises(ValueError, match="text hash"):
        study.select_matched(old, broken)
