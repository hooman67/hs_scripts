"""Focused model-free contract tests for placement judge V2."""

from __future__ import annotations

import base64
import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import run_batch
import run_judge
import scoring


COMPONENTS = tuple(scoring.COMPONENT_WEIGHTS)
DEFAULT_CODE = {
    "support_scenario": "inappropriate_support",
    "access_usability": "excessive_reach",
    "orientation_alignment": "furniture_axis_conflict",
    "scale_perspective": "implausible_scale",
    "contact_integration": "floating",
}


def component(
    severity: int | None = 0,
    *,
    visibility: str = "observed",
    confidence: str = "high",
    issue_code: str | None = None,
) -> dict:
    if severity is None:
        issue_codes = []
    elif severity == 0:
        issue_codes = []
    else:
        issue_codes = [issue_code or "inappropriate_support"]
    return {
        "visibility": visibility,
        "severity": severity,
        "confidence": confidence,
        "evidence": "Concrete visible evidence.",
        "consequence": "Concrete placement consequence." if severity else "",
        "issue_codes": issue_codes,
    }


def observation(*, product_match: str = "match") -> dict:
    return {
        "schema_version": scoring.SCHEMA_VERSION,
        "product_match": product_match,
        "product_match_note": "Compared against the twin.",
        "components": {name: component() for name in COMPONENTS},
        "summary": "Placement assessment summary.",
        "suggested_scene_changes": [],
        "scene_reading": {
            "functional_front": "Visible at image left.",
            "support_surface": "Rectangular table.",
            "usable_approach_edge": "Near edge.",
            "actual_user_position": "Chair at near edge.",
            "access_path": "Clear from chair.",
            "device_support_axes": "Aligned with table axes.",
            "neighboring_furniture": "Chair and table only.",
            "narrative_status": "supported",
            "narrative_evidence": "The visible arrangement supports ordinary use.",
        },
    }


def set_problem(
    value: dict,
    name: str,
    severity: int,
    *,
    confidence: str = "high",
) -> None:
    value["components"][name] = component(
        severity,
        confidence=confidence,
        issue_code=DEFAULT_CODE[name],
    )


def set_unobservable(value: dict, name: str) -> None:
    value["components"][name] = component(
        None,
        visibility="unobservable",
        confidence="low",
    )


def test_severity_two_cannot_be_averaged_into_pass() -> None:
    value = observation()
    set_problem(value, "contact_integration", 2, confidence="medium")

    result = scoring.aggregate_observation(value)

    assert result["weighted_component_score"] == 92.5
    assert result["verdict"] == "fail"
    assert result["applied_score_cap"] == 59
    assert result["natural_placement_score"] == 59
    assert result["verdict_reasons"] == ["clear_placement_defect_veto"]


@pytest.mark.parametrize(("severity", "expected_cap"), ((3, 39), (4, 19)))
def test_severity_three_and_four_apply_distinct_caps(
    severity: int, expected_cap: int
) -> None:
    value = observation()
    set_problem(value, "contact_integration", severity, confidence="high")

    result = scoring.aggregate_observation(value)

    assert result["verdict"] == "fail"
    assert result["applied_score_cap"] == expected_cap
    assert result["natural_placement_score"] == expected_cap


def test_unobservable_noncore_components_do_not_reduce_score() -> None:
    value = observation()
    set_unobservable(value, "scale_perspective")
    set_unobservable(value, "contact_integration")

    result = scoring.aggregate_observation(value)

    assert result["weighted_component_score"] == 100.0
    assert result["natural_placement_score"] == 100.0
    assert result["component_scores"]["scale_perspective"] is None
    assert result["component_scores"]["contact_integration"] is None
    assert result["coverage"] == 0.7
    assert result["verdict"] == "pass"


def test_unobservable_core_component_forces_review_without_score_penalty() -> None:
    value = observation()
    set_unobservable(value, "access_usability")

    result = scoring.aggregate_observation(value)

    assert result["weighted_component_score"] == 100.0
    assert result["natural_placement_score"] == 100.0
    assert result["verdict"] == "review"
    assert "core_component_unassessable:access_usability" in result["verdict_reasons"]


def test_suspected_low_confidence_material_problem_stays_review() -> None:
    value = observation()
    set_problem(value, "orientation_alignment", 2, confidence="low")

    result = scoring.aggregate_observation(value)

    assert result["weighted_component_score"] == 90.0
    assert result["natural_placement_score"] == 90.0
    assert result["applied_score_cap"] is None
    assert result["confidence"] == "low"
    assert result["verdict"] == "review"
    assert "severe_problem_low_confidence" in result["verdict_reasons"]


def test_product_mismatch_is_validity_review_even_with_clear_defect() -> None:
    value = observation(product_match="mismatch")
    set_problem(value, "contact_integration", 4, confidence="high")

    result = scoring.aggregate_observation(value)

    assert result["verdict"] == "review"
    assert result["verdict_reasons"] == ["product_mismatch"]
    assert result["applied_score_cap"] is None
    assert result["weighted_component_score"] == 85.0
    assert result["natural_placement_score"] == 85.0


def test_issue_code_cannot_be_used_for_wrong_component() -> None:
    value = observation()
    value["components"]["access_usability"] = component(
        2,
        issue_code="floating",
    )

    with pytest.raises(scoring.PlacementValidationError, match="floating"):
        scoring.validate_observation(value)


def test_schema_component_and_issue_code_enums_match_runtime() -> None:
    component_properties = scoring.OBSERVATION_SCHEMA["properties"]["components"][
        "properties"
    ]
    assert set(component_properties) == set(scoring.COMPONENT_WEIGHTS)
    assert set(component_properties) == set(scoring.ISSUE_CODES)

    definitions = scoring.OBSERVATION_SCHEMA["$defs"]
    for name, runtime_codes in scoring.ISSUE_CODES.items():
        schema_codes = definitions[name]["properties"]["issue_codes"]["items"][
            "enum"
        ]
        assert len(schema_codes) == len(set(schema_codes)), (
            f"{name} schema issue-code enum contains duplicates"
        )
        assert set(schema_codes) == set(runtime_codes)


def test_visibility_confidence_and_severity_enums_are_consistent() -> None:
    definitions = scoring.OBSERVATION_SCHEMA["$defs"]
    for name in COMPONENTS:
        properties = definitions[name]["properties"]
        assert properties["visibility"]["enum"] == [
            "observed",
            "partial",
            "unobservable",
        ]
        assert properties["confidence"]["enum"] == ["high", "medium", "low"]
        assert properties["severity"]["minimum"] == 0
        assert properties["severity"]["maximum"] == 4


def cache_fingerprint(runtime_input: dict[str, str], model: str = "gpt-5.5") -> str:
    files = {
        key: {
            "path": str(Path(runtime_input[key]).resolve()),
            "sha256": run_judge.sha256(runtime_input[key]),
        }
        for key in ("generated_image", "twin_image")
    }
    payload = {
        "protocol_version": run_judge.PROTOCOL_VERSION,
        "runner_sha256": run_judge.RUNNER_SHA256,
        "wire_schema_sha256": run_judge.WIRE_SCHEMA_SHA256,
        "input": runtime_input,
        "images": files,
        "model_requested": model,
        "reasoning_effort": "high",
        "max_completion_tokens": 12000,
        "system_prompt_sha256": run_judge.sha256(run_judge.ROOT / "system_prompt.md"),
        "schema_sha256": run_judge.sha256(
            run_judge.ROOT / "observation_schema.json"
        ),
        "scoring_sha256": run_judge.sha256(run_judge.ROOT / "scoring.py"),
        "image_detail": "high",
        "image_transform": "none; original bytes",
        "visual_anchors_enabled": False,
    }
    return run_judge._json_sha256(payload)


def runtime_input(tmp_path: Path) -> dict[str, str]:
    generated = tmp_path / "generated.png"
    twin = tmp_path / "twin.png"
    generated.write_bytes(b"generated-image-bytes")
    twin.write_bytes(b"twin-image-bytes")
    return {
        "generated_image": str(generated),
        "twin_image": str(twin),
        "product_type": "printer",
        "scene_prompt": "Original scene prompt.",
        "image_stage": "scene_generation",
    }


def test_valid_cache_returns_without_model_call(tmp_path: Path, monkeypatch) -> None:
    inputs = runtime_input(tmp_path)
    output = tmp_path / "run"
    output.mkdir()
    cached = {
        "ok": True,
        "fingerprint": cache_fingerprint(inputs),
        "judgment": scoring.aggregate_observation(observation()),
    }
    (output / "result.json").write_text(json.dumps(cached), encoding="utf-8")

    def forbidden_client():
        raise AssertionError("cache hit attempted a model client")

    monkeypatch.setattr(run_judge, "client", forbidden_client)
    assert run_judge.judge(inputs, output) == cached


def test_cache_rejects_changed_request_fingerprint_before_model_call(
    tmp_path: Path, monkeypatch
) -> None:
    inputs = runtime_input(tmp_path)
    output = tmp_path / "run"
    output.mkdir()
    cached = {
        "ok": True,
        "fingerprint": cache_fingerprint(inputs),
        "judgment": scoring.aggregate_observation(observation()),
    }
    (output / "result.json").write_text(json.dumps(cached), encoding="utf-8")
    changed = {**inputs, "scene_prompt": "Changed prompt."}

    def forbidden_client():
        raise AssertionError("cache mismatch attempted a model client")

    monkeypatch.setattr(run_judge, "client", forbidden_client)
    with pytest.raises(RuntimeError, match="different request"):
        run_judge.judge(changed, output)


def test_cache_rejects_tampered_deterministic_judgment() -> None:
    judgment = scoring.aggregate_observation(observation())
    tampered = copy.deepcopy(judgment)
    tampered["natural_placement_score"] = 0
    cached = {"ok": True, "fingerprint": "fingerprint", "judgment": tampered}

    with pytest.raises(RuntimeError, match="deterministic aggregation"):
        run_judge._validate_cached_result(cached, "fingerprint")


def batch_record(tmp_path: Path) -> dict:
    inputs = runtime_input(tmp_path)
    generated = Path(inputs["generated_image"])
    twin = Path(inputs["twin_image"])
    prompt_hash = run_batch.text_sha256(inputs["scene_prompt"])
    generated_hash = run_batch.file_sha256(generated)
    twin_hash = run_batch.file_sha256(twin)
    return {
        "id": "test-case",
        "device_type": "printer",
        "image_stage": "scene_generation",
        "scene_prompt": inputs["scene_prompt"],
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
    }


def test_batch_flatten_rejects_missing_image(tmp_path: Path) -> None:
    record = batch_record(tmp_path)
    Path(record["generated_image"]["local_path"]).unlink()

    with pytest.raises(ValueError, match="missing generated_image"):
        run_batch.flatten_record(record)


def test_batch_flatten_rejects_image_and_prompt_hash_mismatch(tmp_path: Path) -> None:
    record = batch_record(tmp_path)
    record["generated_image"]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        run_batch.flatten_record(record)

    record = batch_record(tmp_path)
    record["scene_prompt_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="scene_prompt_sha256 mismatch"):
        run_batch.flatten_record(record)


def test_batch_manifest_rejects_declared_count_mismatch() -> None:
    with pytest.raises(ValueError, match="expected_count"):
        run_batch.manifest_records(
            {"expected_count": 2, "records": [{"id": "only-one"}]}
        )


@pytest.mark.parametrize("expected_count", (True, -1, "1"))
def test_batch_manifest_rejects_invalid_expected_count(expected_count) -> None:
    with pytest.raises(ValueError, match="expected_count"):
        run_batch.manifest_records(
            {"expected_count": expected_count, "records": [{"id": "only-one"}]}
        )


def test_progress_ledger_rejects_cache_identity_mismatch(tmp_path: Path) -> None:
    progress = tmp_path / "progress.json"
    common = {
        "path": progress,
        "manifest": tmp_path / "manifest.json",
        "manifest_sha256": "a" * 64,
        "run_name": "test-run",
        "model": "gpt-5.5",
        "visual_anchors": False,
        "workers": 1,
        "limit": None,
        "record_ids": ["test-case"],
    }
    run_batch.ProgressLedger(**common)

    with pytest.raises(RuntimeError, match="manifest_sha256"):
        run_batch.ProgressLedger(**{**common, "manifest_sha256": "b" * 64})

    with pytest.raises(RuntimeError, match="visual_anchors"):
        run_batch.ProgressLedger(**{**common, "visual_anchors": True})

    legacy = json.loads(progress.read_text(encoding="utf-8"))
    legacy.pop("visual_anchors")
    progress.write_text(json.dumps(legacy), encoding="utf-8")
    with pytest.raises(RuntimeError, match="visual_anchors"):
        run_batch.ProgressLedger(**common)


def test_visual_anchors_exclude_identical_target_image_and_label(
    tmp_path: Path, monkeypatch
) -> None:
    manifest = json.loads(
        (run_judge.ROOT / "data/regression_user_failures.json").read_text(
            encoding="utf-8"
        )
    )
    record = manifest["records"][0]
    assert record["id"] == "regression-userfail-row25-v14"
    inputs = {
        "generated_image": record["generated_image"]["local_path"],
        "twin_image": record["twin_image"]["local_path"],
        "product_type": record["device_type"],
        "scene_prompt": record["scene_prompt"],
        "image_stage": record["image_stage"],
    }
    frozen_anchors = run_judge._load_visual_anchors()
    target_anchor = next(
        anchor
        for anchor in frozen_anchors["examples"]
        if anchor["asset_id"] == record["id"]
    )
    assert target_anchor["sha256"] == record["generated_image"]["sha256"]

    captured: dict = {}

    class FakeCompletions:
        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(
                model="gpt-5.5",
                choices=[
                    SimpleNamespace(
                        finish_reason="stop",
                        message=SimpleNamespace(
                            refusal=False,
                            content=json.dumps(observation()),
                        ),
                    )
                ],
                model_dump=lambda mode: {"usage": {}},
            )

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(completions=FakeCompletions())
    )
    monkeypatch.setattr(run_judge, "client", lambda: (fake_client, "test"))

    result = run_judge.judge(
        inputs,
        tmp_path / "anchor-exclusion",
        visual_anchors=True,
    )

    assert result["ok"] is True
    assert result["excluded_target_identical_anchor_ids"] == [record["id"]]
    included = result["visual_anchors"]["examples"]
    assert len(included) == len(frozen_anchors["examples"]) - 1
    assert target_anchor["asset_id"] not in {anchor["asset_id"] for anchor in included}
    assert target_anchor["sha256"] not in {anchor["sha256"] for anchor in included}

    messages = captured["messages"]
    assert [message["role"] for message in messages] == [
        "system",
        "user",
        "assistant",
        "user",
    ]
    anchor_content = messages[1]["content"]
    anchor_text = "\n".join(
        item["text"] for item in anchor_content if item["type"] == "text"
    )
    anchor_image_urls = {
        item["image_url"]["url"]
        for item in anchor_content
        if item["type"] == "image_url"
    }
    target_bytes_url = "data:image/png;base64," + base64.b64encode(
        Path(target_anchor["local_path"]).read_bytes()
    ).decode()

    assert target_anchor["guidance"] not in anchor_text
    assert record["regression_expectation"]["human_comment"] not in anchor_text
    assert target_bytes_url not in anchor_image_urls
    assert len(anchor_image_urls) == len(included)
    for anchor in included:
        assert anchor["guidance"] in anchor_text
