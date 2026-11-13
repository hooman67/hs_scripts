"""Model-free runtime and isolation checks for placement judge V3."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import run_batch
import run_judge


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_image(path: Path, data: bytes) -> str:
    path.write_bytes(data)
    return digest(data)


def anchor(asset_id: str, path: Path, kind: str, family: str | None = None) -> dict:
    value = {
        "asset_id": asset_id,
        "kind": kind,
        "local_path": str(path),
        "sha256": run_judge.sha256(path),
        "guidance": f"Guidance for {asset_id}.",
    }
    if family is not None:
        value["case_family"] = family
    return value


def test_versioned_runtime_defaults() -> None:
    assert run_judge.PROTOCOL_VERSION == "placement-judge-v3-request-v1"
    assert run_batch.MAX_WORKERS == 4
    args = run_batch.parser().parse_args(["--run-name", "diagnostic"])
    assert args.model == "gpt-5.5"
    assert args.workers == 4
    assert args.manifest == run_batch.ROOT / "data/diagnostic_cases.json"


def test_anchor_manifest_accepts_configurable_count_and_user_comment_kind(
    tmp_path: Path,
) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    first = tmp_path / "first.png"
    second = tmp_path / "second.jpg"
    first_hash = write_image(first, b"first")
    second_hash = write_image(second, b"second")
    payload = {
        "expected_count": 2,
        "exclusion_groups": {first_hash: "family-a"},
        "examples": [
            anchor("first", first, "user_comment_example", "family-a"),
            anchor("second", second, "researcher_interpreted_reference"),
        ],
    }
    (data_dir / "visual_anchors.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )

    assert run_judge._load_visual_anchors(tmp_path) == payload
    assert second_hash == payload["examples"][1]["sha256"]


@pytest.mark.parametrize("expected_count", (True, 0, -1, "2", 1))
def test_anchor_manifest_rejects_invalid_or_mismatched_count(
    tmp_path: Path, expected_count
) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    image = tmp_path / "anchor.png"
    write_image(image, b"anchor")
    payload = {
        "expected_count": expected_count,
        "examples": [
            anchor("one", image, "development_human_defect_anchor"),
            {**anchor("two", image, "user_comment_example"), "sha256": "0" * 64},
        ],
    }
    (data_dir / "visual_anchors.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="expected_count"):
        run_judge._load_visual_anchors(tmp_path)


def test_anchor_selection_records_exact_and_family_exclusions_separately() -> None:
    exact_hash = "1" * 64
    family_hash = "2" * 64
    keep_hash = "3" * 64
    twin_hash = "4" * 64
    manifest = {
        "expected_count": 3,
        "exclusion_groups": {
            exact_hash: "device-view-a",
            family_hash: "device-view-a",
        },
        "examples": [
            {"asset_id": "exact", "sha256": exact_hash},
            {
                "asset_id": "family",
                "sha256": family_hash,
                "case_family": "device-view-a",
            },
            {"asset_id": "keep", "sha256": keep_hash},
        ],
    }
    original = copy.deepcopy(manifest)
    files = {
        "generated_image": {"sha256": exact_hash},
        "twin_image": {"sha256": twin_hash},
    }

    selected, exact, family, target_family = run_judge._select_visual_anchors(
        manifest, files
    )

    assert manifest == original
    assert exact == ["exact"]
    assert family == ["family"]
    assert target_family == "device-view-a"
    assert selected["included_count"] == 1
    assert [item["asset_id"] for item in selected["examples"]] == ["keep"]


def test_anchor_selection_refuses_silent_empty_context() -> None:
    image_hash = "1" * 64
    manifest = {
        "expected_count": 1,
        "examples": [{"asset_id": "only", "sha256": image_hash}],
    }
    files = {
        "generated_image": {"sha256": image_hash},
        "twin_image": {"sha256": "2" * 64},
    }
    with pytest.raises(ValueError, match="every exemplar"):
        run_judge._select_visual_anchors(manifest, files)


def batch_record(tmp_path: Path) -> dict:
    generated = tmp_path / "generated.png"
    twin = tmp_path / "twin.png"
    generated_hash = write_image(generated, b"generated")
    twin_hash = write_image(twin, b"twin")
    scene_prompt = "Original scene prompt."
    prompt_hash = run_batch.text_sha256(scene_prompt)
    return {
        "id": "case-1",
        "device_type": "printer",
        "image_stage": "scene_generation",
        "scene_prompt": scene_prompt,
        "scene_prompt_sha256": prompt_hash,
        "scene_prompt_source": {"rewritten_prompt_included": False},
        "generated_image": {
            "local_path": str(generated.resolve()),
            "sha256": generated_hash,
        },
        "twin_image": {
            "local_path": str(twin.resolve()),
            "sha256": twin_hash,
        },
        "hashes": {
            "generated_image_sha256": generated_hash,
            "twin_image_sha256": twin_hash,
            "scene_prompt_sha256": prompt_hash,
        },
        "target_annotations": {"human_comment": "must never enter runtime"},
        "regression_expectation": {"verdict": "fail"},
    }


def test_batch_flatten_whitelists_inputs_and_drops_target_annotations(
    tmp_path: Path,
) -> None:
    record = batch_record(tmp_path)
    record_id, runtime_input = run_batch.flatten_record(record)

    assert record_id == "case-1"
    assert set(runtime_input) == {
        "generated_image",
        "twin_image",
        "product_type",
        "scene_prompt",
        "image_stage",
    }
    serialized = json.dumps(runtime_input)
    assert "human_comment" not in serialized
    assert "regression_expectation" not in serialized


def runtime_root(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True)
    (tmp_path / "system_prompt.md").write_text("Judge prompt.", encoding="utf-8")
    (tmp_path / "observation_schema.json").write_text("{}\n", encoding="utf-8")
    (tmp_path / "scoring.py").write_text("# test scoring marker\n", encoding="utf-8")
    return tmp_path


def test_three_attempt_retry_bound_and_raw_response_fidelity(
    tmp_path: Path, monkeypatch
) -> None:
    root = runtime_root(tmp_path / "runtime")
    generated = tmp_path / "generated.png"
    twin = tmp_path / "twin.png"
    write_image(generated, b"generated")
    write_image(twin, b"twin")
    runtime_input = {
        "generated_image": str(generated),
        "twin_image": str(twin),
        "product_type": "printer",
        "scene_prompt": "Original prompt.",
        "image_stage": "scene_generation",
    }
    observation = {"model": "observation", "untouched": [1, 2, 3]}
    raw_response = {
        "id": "raw-response-id",
        "model": "gpt-5.5",
        "choices": [{"message": {"content": json.dumps(observation)}}],
        "usage": {"prompt_tokens": 17, "completion_tokens": 5},
        "provider_extension": {"preserve": True},
    }

    class RetryableError(Exception):
        status_code = 429
        response = SimpleNamespace(headers={"retry-after": "0"})

    calls = 0

    class FakeCompletions:
        def create(self, **kwargs):
            nonlocal calls
            calls += 1
            if calls < 3:
                raise RetryableError()
            return SimpleNamespace(
                model="gpt-5.5",
                choices=[
                    SimpleNamespace(
                        finish_reason="stop",
                        message=SimpleNamespace(
                            refusal=False,
                            content=json.dumps(observation),
                        ),
                    )
                ],
                model_dump=lambda mode: copy.deepcopy(raw_response),
            )

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(completions=FakeCompletions())
    )
    monkeypatch.setattr(run_judge, "ROOT", root)
    monkeypatch.setattr(run_judge, "validate_runtime_input", lambda value: None)
    monkeypatch.setattr(
        run_judge,
        "aggregate",
        lambda value: {"observation": value, "aggregated": True},
    )
    monkeypatch.setattr(run_judge, "client", lambda: (fake_client, "test"))
    monkeypatch.setattr(run_judge.time, "sleep", lambda seconds: None)

    output = tmp_path / "output"
    result = run_judge.judge(runtime_input, output)

    assert calls == 3
    assert result["ok"] is True
    assert result["attempts"] == [
        {"attempt": 1, "error_type": "RetryableError", "status": 429},
        {"attempt": 2, "error_type": "RetryableError", "status": 429},
        {"attempt": 3, "status": "ok"},
    ]
    assert result["judgment"]["observation"] == observation
    assert json.loads((output / "response.json").read_text(encoding="utf-8")) == raw_response


def test_retryable_failures_stop_after_three_attempts(
    tmp_path: Path, monkeypatch
) -> None:
    root = runtime_root(tmp_path / "runtime")
    generated = tmp_path / "generated.png"
    twin = tmp_path / "twin.png"
    write_image(generated, b"generated")
    write_image(twin, b"twin")
    runtime_input = {
        "generated_image": str(generated),
        "twin_image": str(twin),
        "product_type": "printer",
        "scene_prompt": "Original prompt.",
        "image_stage": "scene_generation",
    }

    class RetryableError(Exception):
        status_code = 503
        response = SimpleNamespace(headers={})

    calls = 0

    class FakeCompletions:
        def create(self, **kwargs):
            nonlocal calls
            calls += 1
            raise RetryableError()

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(completions=FakeCompletions())
    )
    monkeypatch.setattr(run_judge, "ROOT", root)
    monkeypatch.setattr(run_judge, "validate_runtime_input", lambda value: None)
    monkeypatch.setattr(run_judge, "client", lambda: (fake_client, "test"))
    monkeypatch.setattr(run_judge.time, "sleep", lambda seconds: None)

    result = run_judge.judge(runtime_input, tmp_path / "output")

    assert calls == 3
    assert result["ok"] is False
    assert result["error_type"] == "RetryableError"
    assert len(result["attempts"]) == 3

