from pathlib import Path

import pytest

from prepare import parse_cases


def test_real_report_separates_human_comments_from_generated_refiner_scope():
    cases = parse_cases((Path(__file__).parent / "source/full_evalset.html").read_text())
    assert len(cases) == 64
    assert sum(case["status"] == "refined" for case in cases) == 17
    assert cases[0]["reviewer_feedback"] == "Prefer the reflections in the second run"
    assert "Good-rated" in cases[0]["refiner_scope_text"]
    missing_legs = next(case for case in cases if case["id"] == "10_elitebook_13_Front_Wide__run1")
    assert missing_legs["reviewer_feedback"] == "Chair legs don't exist."
    assert missing_legs["media"][1].endswith("/baseline.png")


def test_incomplete_or_rebound_report_is_rejected():
    source = (Path(__file__).parent / "source/full_evalset.html").read_text()
    with pytest.raises(ValueError, match="image order or case binding"):
        parse_cases(source.replace("01_cashmere_x_Front_CloseUp__run1/baseline.png", "wrong.png", 1))
    with pytest.raises(ValueError, match="exactly64"):
        parse_cases("")
