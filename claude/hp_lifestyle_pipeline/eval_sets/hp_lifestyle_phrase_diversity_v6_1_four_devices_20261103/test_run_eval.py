from __future__ import annotations

import importlib.util
import json
import subprocess
import threading
import time
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).with_name("run_eval.py")
SPEC = importlib.util.spec_from_file_location("v6_eval_runner", MODULE_PATH)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def _prepare(tmp_path: Path, revision: str = "mock-r1") -> Path:
    return runner.prepare_revision(
        revision,
        runner.DEFAULT_CATALOG,
        eval_root=tmp_path,
        source_eval=runner.SOURCE_EVAL,
        runtime_source=runner.LIVE_V61,
    )


def _candidate(rank: int) -> dict:
    return {
        "id": f"p{rank}",
        "environment": "Office",
        "text": f"Mock office scene number {rank}.",
        "prop_ids": [],
        "score_components": {
            "smart_brief": {
                "setting": 0,
                "activity": 0,
                "materials": 0,
                "use_context": 0,
            },
            "source_messaging": {
                "setting": 0,
                "activity": 0,
                "materials": 0,
                "use_context": 0,
            },
        },
        "evidence": [],
        "relationship": "source_grounded",
        "explanation": "Mock explanation.",
        "creative_departures": [],
        "ctech_reference_id": "CT03",
        "ctech_reference_score": 80,
        "ctech_explanation": "Mock C-Tech explanation.",
        "camera_fit_explanation": "Mock camera explanation.",
        "source_relevance_score": 101 - rank,
    }


def _success_result() -> dict:
    return {
        "status": "ok",
        "prompts": [_candidate(rank) for rank in range(1, 11)],
        "debug": {
            "source_conflicts": [],
            "limitations": ["Mocked offline test."],
            "environment_rationale": "Mock rationale.",
            "service": {"semantic_repair_attempted": False},
        },
        "audit": {
            "semantic_calls": 1,
            "transport_attempts_known": 1,
            "transport_accounting_complete": True,
            "attempts": [
                {
                    "number": 1,
                    "kind": "initial",
                    "errors": [],
                    "provider": {
                        "model": "gpt-5.5",
                        "transport_attempts": 1,
                    },
                }
            ],
        },
    }


def _write_mock_call_artifacts(snapshot: Path, case_id: str) -> None:
    runner.write_json_exclusive(
        snapshot / "call_journals" / f"{case_id}.launch.json",
        {"case_id": case_id, "mock": True},
    )
    runner.write_json_exclusive(
        snapshot / "call_journals" / f"{case_id}.process.json",
        {"case_id": case_id, "returncode": 0, "mock": True},
    )
    journal = snapshot / "results" / f"{case_id}.json.run"
    runner.write_json_exclusive(
        journal / "attempt_1.request.json", {"messages": [], "schema": {}}
    )
    runner.write_json_exclusive(
        journal / "attempt_1.response.json",
        {"model": "gpt-5.5", "content": "mock"},
    )


def test_prepare_copies_exact_16_inputs_and_freezes_runtime(tmp_path: Path) -> None:
    snapshot = _prepare(tmp_path)
    manifest = runner.verify_snapshot(snapshot)

    assert manifest["scope"]["case_count"] == 16
    assert manifest["scope"]["candidate_count"] == 160
    assert manifest["scope"]["selected_prompt_count"] == 96
    assert manifest["catalog"]["approved_entries"] > 0
    assert len(manifest["cases"]) == 16
    assert "runtime/v6_1/system_prompt.md" in manifest["snapshot_assets"]
    assert "runtime/v6_1/validation.py" in manifest["snapshot_assets"]
    assert "runtime/v6_1/approved_catalog.json" in manifest["snapshot_assets"]

    for case in manifest["cases"]:
        frozen = snapshot / case["frozen_input_path"]
        source = Path(case["input_source_path"])
        assert frozen.read_bytes() == source.read_bytes()
        assert case["frozen_input_sha256"] == case["input_source_sha256"]
        assert "expected_camera" not in case
        assert "human_review_status" not in case


def test_snapshot_verification_detects_byte_change(tmp_path: Path) -> None:
    snapshot = _prepare(tmp_path)
    cache_file = snapshot / "runtime/v6_1/__pycache__/runtime.cpython-test.pyc"
    cache_file.parent.mkdir(parents=True)
    cache_file.write_bytes(b"disposable interpreter cache")
    runner.verify_snapshot(snapshot)
    path = snapshot / "runtime/v6_1/system_prompt.md"
    path.write_text(path.read_text(encoding="utf-8") + "\nchanged", encoding="utf-8")
    with pytest.raises(ValueError, match="snapshot bytes changed"):
        runner.verify_snapshot(snapshot)


def test_paid_calls_require_explicit_root_go_flag(tmp_path: Path) -> None:
    with pytest.raises(PermissionError, match="root GO"):
        runner.run_revision(
            "does-not-exist",
            paid_calls_authorized=False,
            eval_root=tmp_path,
        )


def test_mock_run_uses_at_most_two_workers_and_refuses_resume(
    tmp_path: Path,
) -> None:
    snapshot = _prepare(tmp_path)
    active = 0
    maximum_active = 0
    lock = threading.Lock()

    def fake_command(command: list[str]) -> subprocess.CompletedProcess[str]:
        nonlocal active, maximum_active
        with lock:
            active += 1
            maximum_active = max(maximum_active, active)
        try:
            time.sleep(0.01)
            output = Path(command[command.index("--output") + 1])
            runner.write_json_exclusive(output, _success_result())
            journal = output.with_suffix(output.suffix + ".run")
            runner.write_json_exclusive(
                journal / "attempt_1.request.json", {"messages": [], "schema": {}}
            )
            runner.write_json_exclusive(
                journal / "attempt_1.response.json",
                {"model": "gpt-5.5", "content": "mock"},
            )
            return subprocess.CompletedProcess(command, 0, "mock ok", "")
        finally:
            with lock:
                active -= 1

    summary = runner.run_revision(
        "mock-r1",
        paid_calls_authorized=True,
        max_concurrency=2,
        eval_root=tmp_path,
        command_runner=fake_command,
    )
    assert summary["all_processes_succeeded"] is True
    assert maximum_active == 2
    assert len(list((snapshot / "call_journals").glob("*.launch.json"))) == 16
    assert len(list((snapshot / "call_journals").glob("*.process.json"))) == 16
    with pytest.raises(FileExistsError, match="already finished"):
        runner.run_revision(
            "mock-r1",
            paid_calls_authorized=True,
            eval_root=tmp_path,
            command_runner=fake_command,
        )


def test_export_requires_all_16_successes_and_writes_exact_shapes(
    tmp_path: Path,
) -> None:
    snapshot = _prepare(tmp_path)
    manifest = runner.verify_snapshot(snapshot)
    runner.write_json_exclusive(
        snapshot / "run_complete.json",
        {
            "version": "mock",
            "all_processes_succeeded": True,
            "case_count": 16,
        },
    )
    for case_id in manifest["authorized_text_case_ids"]:
        runner.write_json_exclusive(
            snapshot / "results" / f"{case_id}.json", _success_result()
        )
        _write_mock_call_artifacts(snapshot, case_id)

    destination = runner.export_revision("mock-r1", eval_root=tmp_path)
    all_output = json.loads(
        (destination / "prompts_all_160.json").read_text(encoding="utf-8")
    )
    top_output = json.loads(
        (destination / "prompts_top6_96.json").read_text(encoding="utf-8")
    )
    validation = json.loads(
        (destination / "validation.json").read_text(encoding="utf-8")
    )

    assert set(("prompts", "counts", "device_source_mapping")) <= set(all_output)
    assert set(("prompts", "counts", "device_source_mapping")) <= set(top_output)
    assert all_output["counts"]["prompts"] == len(all_output["prompts"]) == 160
    assert top_output["counts"]["prompts"] == len(top_output["prompts"]) == 96
    assert len(all_output["bank_audit"]) == 16
    assert len({row["prompt_key"] for row in all_output["prompts"]}) == 160
    assert all("text_sha256" in row for row in all_output["prompts"])
    assert all(row["bank_rank"] <= 6 for row in top_output["prompts"])
    assert validation["passed"] is True


def test_export_refuses_a_missing_or_failed_bank(tmp_path: Path) -> None:
    snapshot = _prepare(tmp_path)
    manifest = runner.verify_snapshot(snapshot)
    runner.write_json_exclusive(snapshot / "run_complete.json", {"version": "mock"})
    for case_id in manifest["authorized_text_case_ids"][:-1]:
        runner.write_json_exclusive(
            snapshot / "results" / f"{case_id}.json", _success_result()
        )
        _write_mock_call_artifacts(snapshot, case_id)

    with pytest.raises(ValueError, match="result is missing"):
        runner.export_revision("mock-r1", eval_root=tmp_path)
