from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import build_grouped_report as report
import run_batch

HERE = Path(__file__).resolve().parent
MANIFEST = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/"
    "judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json"
)
ASSET_MAP = Path(
    "/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/"
    "judge/placement/versions/v3/fe_reports/"
    "v6_1_consensus_v2_grouped_20261105/data.json"
)


def test_manifest_and_asset_map_are_complete() -> None:
    records = run_batch.validate_manifest(MANIFEST)
    urls = report.validated_asset_urls(ASSET_MAP, records)
    assert len(records) == len(urls) == 160
    assert len({record["twin_image"]["sha256"] for record in records}) == 16


def test_runtime_input_is_whitelisted_and_hash_bound() -> None:
    record = run_batch.validate_manifest(MANIFEST)[0]
    runtime = run_batch.runtime_input(record)
    assert set(runtime) == {
        "generated_image",
        "twin_image",
        "product_type",
        "scene_prompt",
        "target_record_id",
        "device",
        "camera",
        "prompt_rank",
    }
    assert runtime["target_record_id"] == record["id"]


def test_validate_only_has_no_run_side_effect(tmp_path: Path) -> None:
    run_dir = tmp_path / "never-created"
    command = [
        sys.executable,
        str(HERE / "run_batch.py"),
        "--run-dir",
        str(run_dir),
        "--validate-only",
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    payload = json.loads(completed.stdout)
    assert payload["status"] == "validated_no_model_calls"
    assert payload["model_calls"] == 0
    assert payload["records"] == 160
    assert not run_dir.exists()


def test_live_mode_requires_explicit_authorization(tmp_path: Path) -> None:
    run_dir = tmp_path / "never-created"
    completed = subprocess.run(
        [sys.executable, str(HERE / "run_batch.py"), "--run-dir", str(run_dir)],
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "--acknowledge-launch-authorized" in completed.stderr
    assert not run_dir.exists()


def test_worker_bound_is_two() -> None:
    completed = subprocess.run(
        [sys.executable, str(HERE / "run_batch.py"), "--run-dir", "/tmp/unused-placement-run", "--workers", "3", "--validate-only"],
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "between 1 and 2" in completed.stderr

