"""A wrong-criterion failure cannot qualify a research promotion."""

import copy
import json

import common
import pytest
import release


def setup_version(tmp_path, mismatch, ctech=False):
    gates = tmp_path / "promotion_gates.json"
    common.write_json(
        gates,
        {
            "required": "All original criterion checks",
            **({"ctech_source_cases": 30} if ctech else {}),
        },
    )
    common.write_json(
        tmp_path / "protocol_freeze.json",
        {"files": [{"path": str(gates), "sha256": common.sha(gates)}]},
    )
    rows = []
    for candidate in ("p1", "p2"):
        for index in range(6):
            rows.append(
                {
                    "id": str(index),
                    "candidate": candidate,
                    "status": "complete",
                    "verdict": "fail" if index == 2 else "pass",
                    "checks": {"required_geometry": not (mismatch and index == 2)},
                }
            )
    common.write_json(
        tmp_path / "evaluation/calibration/summary.json", {"records": rows}
    )
    for dataset, count in (
        ("historical", 128),
        ("refiner", 81),
        *((("ctech", 30),) if ctech else ()),
    ):
        common.write_json(
            tmp_path / "evaluation" / dataset / "summary.json",
            {
                "protocol_freeze_sha256": common.sha(tmp_path / "protocol_freeze.json"),
                "records": [
                    {"id": str(index), "candidate": candidate, "status": "complete"}
                    for candidate in ("p1", "p2")
                    for index in range(count)
                ],
            },
        )


def test_wrong_criterion_failure_blocks_both_promotions(tmp_path):
    setup_version(tmp_path, True)
    result = release.assess(tmp_path)
    assert result["selected_candidate"] is None
    assert all(not value["promoted"] for value in result["candidates"].values())
    assert result["candidates"]["p2"]["unwaived_criterion_mismatches"][0]["id"] == "2"


def test_successful_calibration_still_requires_complete_error_free_expansion(tmp_path):
    setup_version(tmp_path, False)
    path = tmp_path / "evaluation/refiner/summary.json"
    document = copy.deepcopy(json.loads(path.read_text()))
    document["records"][0]["status"] = "error"
    common.write_json(path, document)
    result = release.assess(tmp_path)
    assert not result["candidates"]["p1"]["promoted"]
    assert result["candidates"]["p2"]["promoted"]
    assert result["selected_candidate"] == "p2"
    assert result["automatic_acceptance_authorized"] is False


def test_duplicate_ctech_rows_cannot_satisfy_complete_source_coverage(tmp_path):
    setup_version(tmp_path, False, ctech=True)
    path = tmp_path / "evaluation/ctech/summary.json"
    document = json.loads(path.read_text())
    document["records"][1]["id"] = document["records"][0]["id"]
    common.write_json(path, document)
    result = release.assess(tmp_path)
    assert not result["candidates"]["p1"]["promoted"]
    assert result["candidates"]["p2"]["promoted"]


def test_ctech_summary_from_another_protocol_is_rejected(tmp_path):
    setup_version(tmp_path, False, ctech=True)
    path = tmp_path / "evaluation/ctech/summary.json"
    document = json.loads(path.read_text())
    document["protocol_freeze_sha256"] = "different"
    common.write_json(path, document)
    with pytest.raises(ValueError, match="another protocol"):
        release.assess(tmp_path)
