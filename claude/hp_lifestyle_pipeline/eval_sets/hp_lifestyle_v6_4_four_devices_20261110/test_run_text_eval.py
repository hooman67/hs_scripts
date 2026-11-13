import importlib.util
import json
from pathlib import Path
import zipfile

import pytest


@pytest.fixture
def runner(tmp_path, monkeypatch):
    source = Path(__file__).with_name("run_text_eval.py")
    spec = importlib.util.spec_from_file_location("v64_text_eval_test", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "SNAPSHOT", tmp_path / "snapshot")
    inventory = tmp_path / "inventory.json"
    inventory.write_text(json.dumps({"files": [], "v63_baseline_sha256": {}}))
    monkeypatch.setattr(module, "INVENTORY", inventory)
    originals = tmp_path / "originals"
    originals.mkdir()
    monkeypatch.setattr(module, "ORIGINALS", originals)
    for pair_id, relative, _ in module.SELECTION.values():
        brief = json.dumps({"USE CASES": {"content": "Office context for " + pair_id}})
        messaging = json.dumps({"source_messaging": [{"fields": [{"value": "Office work."}]}]})
        path = originals / relative
        if path.suffix == ".zip":
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("smart-brief.json", brief)
                archive.writestr("source-messaging.json", messaging)
        else:
            path.mkdir()
            (path / "smart-brief.json").write_text(brief)
            (path / "source-messaging.json").write_text(messaging)
    return module


def test_preparation_preserves_new_object_pairs_and_exact_existing_cameras(runner):
    runner.prepare()
    manifest = runner.verify()
    assert len(manifest["cases"]) == 16
    for case in manifest["cases"]:
        request = runner.load(runner.SNAPSHOT / case["frozen_input_path"])
        assert set(request) == {"smart_brief", "source_messaging", "camera_tag"}
        assert request["camera_tag"] == case["camera_tag"]
        assert request["smart_brief"]["USE CASES"]["content"] == (
            "Office context for " + case["source_pair"]
        )
        assert isinstance(request["source_messaging"], dict)
    assert not (runner.SNAPSHOT / "run_started.json").exists()


def test_changed_input_stops_before_a_paid_process_can_start(runner, monkeypatch):
    runner.prepare()
    case = runner.verify()["cases"][0]
    request_path = runner.SNAPSHOT / case["frozen_input_path"]
    request_path.write_text("{}")
    calls = []
    monkeypatch.setattr(runner, "run_case", lambda *args: calls.append(args))
    with pytest.raises(ValueError, match="bytes changed"):
        runner.run(True)
    assert calls == []
    assert not (runner.SNAPSHOT / "run_started.json").exists()
