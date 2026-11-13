"""No paid calls: exact reuse, terminal-error/no-resampling, extractive display reasons."""
import json
from pathlib import Path

import pytest

import external_driver as driver


@pytest.fixture
def owned_scratch():
    folder = driver.HERE / ".test_work"
    folder.mkdir(exist_ok=True)
    yield folder
    import shutil
    shutil.rmtree(folder)


@pytest.mark.parametrize("state", ["missing_response", "failed_response", "terminal"])
def test_started_or_terminal_failure_never_resampled(owned_scratch, monkeypatch, state):
    root = owned_scratch / state
    case = root / "runs/r2/synthetic_case"
    role = case / "baseline"
    role.mkdir(parents=True)
    driver.write(role / "request.json", {"scheduled": True})
    if state == "failed_response":
        driver.write(role / "result.json", {"ok": False, "error_type": "ValueError"})
    elif state == "terminal":
        driver.write(case / "terminal.json", {"status": "error", "verdict": None})
    monkeypatch.setattr(driver, "HERE", root)
    monkeypatch.setattr(driver, "terminal_error",
                        lambda record, folder, kind: {"status": "error", "verdict": None, "error_type": kind})

    def forbidden(*args):
        pytest.fail("A started/failed role was resampled")
    result = driver.run_one({"id": "synthetic_case"}, judge=forbidden)
    assert result["status"] == "error"
    assert not (role / "response.json").exists()


def test_successful_partial_is_resumable_without_new_sample_for_that_role(owned_scratch):
    role = owned_scratch / "baseline"
    role.mkdir()
    driver.write(role / "request.json", {"scheduled": True})
    driver.write(role / "result.json", {"ok": True})
    driver.write(role / "response.json", {"unchanged_raw": True})
    assert driver.resume_state(owned_scratch) == "new_or_successful_partial"


def test_exact_reused_calibration_inputs_and_protocol_are_required():
    inventory = driver.read(driver.R1 / "evaluation/inventory.json")
    cases = {row["id"]: row for row in inventory["records"]}
    frozen = driver.read(driver.R2 / "calibration/results.json")["items"][0]
    case = cases[frozen["id"]]
    result, models, calls = driver.audit_result("r2", case, frozen["result_path"])
    assert result["runtime_input"] == driver.runtime(case)
    assert len(calls) == 2 and models
    changed = dict(case, scene_prompt=case["scene_prompt"] + " changed")
    with pytest.raises(ValueError, match="input/protocol"):
        driver.audit_result("r2", changed, frozen["result_path"])


def test_changed_protocol_is_not_reused(owned_scratch):
    inventory = driver.read(driver.R1 / "evaluation/inventory.json")
    cases = {row["id"]: row for row in inventory["records"]}
    frozen = driver.read(driver.R2 / "calibration/results.json")["items"][0]
    changed = driver.read(frozen["result_path"])
    changed["protocol_freeze_sha256"] = "0" * 64
    copied = owned_scratch / "changed_protocol.json"
    driver.write(copied, changed)
    with pytest.raises(ValueError, match="input/protocol"):
        driver.audit_result("r2", cases[frozen["id"]], copied)


def test_short_reason_is_extractive_and_preserves_negation():
    text = "No visible construction defect. " + "The remaining relationships are hidden. " * 20
    result = {
        "application_merged_judgment": {"observation": {
            "summary": text, "product_match": "match", "components": {}}},
        "final_decision": {"verdict": "pass"},
    }
    reason, source = driver.reason_for(result)
    assert reason.startswith("No visible construction defect.")
    assert reason.endswith("…") and len(reason) <= 260
    assert " ".join(source["original_text"].split()).startswith(reason[:-1])


def test_refreshed_source_and_exact_mapping():
    result = driver.verify_mapping(driver.read(driver.R1 / "evaluation/inventory.json"))
    assert result["refreshed_html_matches_original_snapshot"]
    assert result["generated_outputs"] == 128 and result["image_objects_hash_verified"] == 160
