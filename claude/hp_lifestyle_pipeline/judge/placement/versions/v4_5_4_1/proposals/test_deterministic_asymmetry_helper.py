from __future__ import annotations

from pathlib import Path

import pytest
from deterministic_asymmetry_helper import propose_malformed_support_anatomy


def edge(p0, p1, owner="support_side"):
    return {"owner": owner, "p0": p0, "p1": p1, "raw_pixel_evidence": "visible edge"}


def test_detects_human_reviewed_asymmetry_measurements():
    width = 0.711
    result = propose_malformed_support_anatomy(
        [edge([0.1, 0.1], [0.111, 0.245]), edge([0.7, 0.1], [0.843, 0.245])],
        width,
    )
    assert result is not None
    assert result["subtype"] == "malformed_connected_furniture"
    assert result["measurements"]["horizontal_run_fractions"] == pytest.approx(
        [0.011 / width, 0.143 / width]
    )


@pytest.mark.parametrize(
    "edges,width",
    [
        ([edge([0.1, 0.1], [0.131, 0.245]), edge([0.7, 0.1], [0.9, 0.245])], 1.0),
        ([edge([0.1, 0.1], [0.11, 0.245]), edge([0.7, 0.1], [0.849, 0.245])], 1.0),
        ([edge([0.1, 0.1], [0.111, 0.17]), edge([0.7, 0.1], [0.843, 0.245])], 0.711),
        ([edge([0.1, 0.1], [0.111, 0.245])], 0.711),
    ],
)
def test_does_not_propose_when_threshold_or_comparability_requirement_fails(edges, width):
    assert propose_malformed_support_anatomy(edges, width) is None


def test_ignores_duplicate_and_non_support_side_edges():
    one = edge([0.1, 0.1], [0.111, 0.245])
    other = edge([0.7, 0.1], [0.843, 0.245], owner="support_front")
    assert propose_malformed_support_anatomy([one, dict(one), other], 0.711) is None


def test_rejects_nonpositive_tabletop_width():
    with pytest.raises(ValueError, match="positive"):
        propose_malformed_support_anatomy([], 0)


def test_proposal_is_not_wired_into_v4_5_4_runtime():
    candidate_root = Path(__file__).resolve().parent.parent
    for relative in ("run_judge.py", "scoring.py", "codebook.py"):
        assert "deterministic_asymmetry_helper" not in (candidate_root / relative).read_text()
