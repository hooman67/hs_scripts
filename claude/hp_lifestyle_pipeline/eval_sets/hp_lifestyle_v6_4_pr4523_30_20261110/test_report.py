import copy
import importlib.util
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location("single_column_v64_report", HERE / "report.py")
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)


def rows():
    prompts = report.study.load(HERE / "selection/selected_v6_4_30.json")["prompts"]
    return [{"key": list(report.study.slot(p)),
             "prompt": p, "source_input": {"must_not_be_an_fe_column": "full input"},
             "output": {"status": "done", "image": f"../assets/outputs/{i}.png",
                        "inputs": {"must_not_be_an_fe_column": "model input"},
                        "scene_debug": {"must_not_be_an_fe_column": "debug"}}}
            for i, p in enumerate(prompts)]


def test_fe_preserves_order_and_only_one_output_image_per_row():
    source = rows()
    data = report.fe_document(source)
    assert data["meta_texts"] == [report.study.TITLE]
    assert len(data["rows"]) == 30
    for i, (actual, original) in enumerate(zip(data["rows"], source), 1):
        assert actual["meta_data"] == {
            "row_idx": i, "evalset_item_id": " / ".join(map(str, original["key"])),
            "key_val_informations": None,
        }
        assert actual["images"] == [{
            "asset_type": "image", "image_src": report.BASE + f"assets/outputs/{i - 1}.png",
            "meta_text": {"label": report.study.TITLE},
        }]


def test_fe_rejects_missing_or_incomplete_rows():
    source = rows()
    with pytest.raises(ValueError, match="all thirty"):
        report.fe_document(source[:-1])
    broken = copy.deepcopy(source)
    broken[3]["output"]["status"] = "failed"
    with pytest.raises(ValueError, match="all thirty"):
        report.fe_document(broken)
