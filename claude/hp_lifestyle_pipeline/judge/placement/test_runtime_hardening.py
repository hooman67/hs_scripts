import copy
import json
from pathlib import Path

import pytest

from judge.placement import run_judge, run_pilot
from judge.placement.evaluate_pilot import evaluate
from judge.placement.scoring import aggregate_observation


def make_observation():
    component = {
        "visibility": "observed",
        "severity": 0,
        "confidence": "high",
        "evidence": "The relationship is visible.",
        "consequence": "No visible problem.",
        "issue_codes": [],
    }
    return {
        "schema_version": "placement-observations-v1",
        "product_match": "match",
        "product_match_note": "The product matches.",
        "components": {
            name: copy.deepcopy(component)
            for name in (
                "support_scenario",
                "access_usability",
                "orientation_alignment",
                "scale_perspective",
                "contact_integration",
            )
        },
        "summary": "No visible placement problem.",
        "suggested_scene_changes": [],
    }


def test_protocol_fingerprint_inputs_match_loaded_files():
    assert run_judge.PROTOCOL_VERSION == "placement-judge-request-v2"
    assert run_judge.RUNNER_SHA256 == run_judge.sha256(run_judge.__file__)
    assert run_judge.WIRE_SCHEMA_SHA256 == run_judge._json_sha256(
        run_judge.WIRE_SCHEMA
    )


def test_cached_result_is_revalidated_and_reaggregated():
    judgment = aggregate_observation(make_observation())
    cached = {"fingerprint": "abc", "ok": True, "judgment": judgment}
    assert run_judge._validate_cached_result(cached, "abc") is cached

    tampered = copy.deepcopy(cached)
    tampered["judgment"]["natural_placement_score"] = 99
    with pytest.raises(RuntimeError, match="deterministic aggregation"):
        run_judge._validate_cached_result(tampered, "abc")


@pytest.mark.parametrize(
    ("returned", "expected"),
    [
        ("gpt-5.5", True),
        ("gpt-5.5-2026-04-24", True),
        ("gpt-5.5-preview", False),
        ("gpt-5.5-2026-4-24", False),
        ("gpt-5.5-2026-04-24-extra", False),
        (None, False),
    ],
)
def test_model_identity_is_exact_or_iso_dated(returned, expected):
    assert run_judge._model_identity_matches("gpt-5.5", returned) is expected


def test_live_anchor_manifest_is_fixed_and_excludes_heldout():
    anchors = run_judge._load_visual_anchors()
    assert len(anchors["examples"]) == 5
    assert [anchor["kind"] for anchor in anchors["examples"]].count(
        "development_human_defect_anchor"
    ) == 3
    assert [anchor["kind"] for anchor in anchors["examples"]].count(
        "researcher_interpreted_reference"
    ) == 2

    split = json.loads(
        (run_judge.ROOT / "data/split.json").read_text(encoding="utf-8")
    )
    heldout_hashes = {
        value
        for case in split["cases"]
        if case["split"] == "held_out"
        for value in (case["image_sha256"], case["input_sha256"])
    }
    assert not heldout_hashes & {
        anchor["sha256"] for anchor in anchors["examples"]
    }
    assert run_pilot._anchor_demonstration_rows(anchors, split) == {2, 8, 21}


def test_safe_run_names_and_nonempty_selection():
    for unsafe in ("", ".", "..", "../escape", "nested/run"):
        with pytest.raises(ValueError):
            run_pilot._validate_run_name(unsafe)
    run_pilot._validate_run_name("pilot_v2")

    split = {
        "cases": [
            {"id": "comparison-row-01-v13", "split": "development", "row": 1}
        ]
    }
    assert len(run_pilot._select_cases(split, "development", [1], None)) == 1
    with pytest.raises(ValueError, match="not in development"):
        run_pilot._select_cases(split, "development", [2], None)
    with pytest.raises(ValueError, match="positive"):
        run_pilot._select_cases(split, "development", None, 0)


def test_prepare_case_checks_hashes_and_provenance(monkeypatch):
    image_hash = "a" * 64
    twin_hash = "b" * 64
    case = {
        "id": "comparison-row-01-v13",
        "split": "development",
        "row": 1,
        "variant": "v13",
        "device": "Laptop",
        "image_sha256": image_hash,
        "input_sha256": twin_hash,
    }
    image = {
        "id": case["id"],
        "row": 1,
        "variant": "v13",
        "device": "Laptop",
        "type": "generated_final",
        "source_report": "report",
        "case_id": "case",
        "original_prompt": "prompt",
        "local_path": "/synthetic/generated.png",
        "sha256": image_hash,
    }
    twin = {
        "id": "comparison-row-01-product_input",
        "row": 1,
        "variant": "product_input",
        "device": "Laptop",
        "type": "product_input",
        "source_report": "report",
        "case_id": "case",
        "original_prompt": "prompt",
        "local_path": "/synthetic/twin.png",
        "sha256": twin_hash,
    }
    monkeypatch.setattr(
        run_pilot,
        "sha256",
        lambda path: image_hash if "generated" in str(path) else twin_hash,
    )
    prepared = run_pilot._prepare_case(case, {case["id"]: image}, [image, twin])
    assert prepared["runtime"]["image_stage"] == "scene_generation"

    wrong_hash = copy.deepcopy(image)
    wrong_hash["sha256"] = "c" * 64
    with pytest.raises(ValueError, match="frozen split"):
        run_pilot._prepare_case(case, {case["id"]: wrong_hash}, [wrong_hash, twin])

    wrong_provenance = copy.deepcopy(twin)
    wrong_provenance["source_report"] = "different"
    with pytest.raises(ValueError, match="provenance differs"):
        run_pilot._prepare_case(
            case, {case["id"]: image}, [image, wrong_provenance]
        )


def test_safe_case_run_converts_preparation_exception_to_status(monkeypatch, tmp_path):
    def fail(*args, **kwargs):
        raise RuntimeError("details must not enter status")

    monkeypatch.setattr(run_pilot, "judge", fail)
    job = {
        "case": {
            "id": "comparison-row-01-v13",
            "split": "development",
        },
        "runtime": {},
    }
    result = run_pilot._safe_case_run(job, tmp_path, "gpt-5.5", False)
    assert result["ok"] is False
    assert result["error_type"] == "RuntimeError"
    assert result["error"] == "RuntimeError"
    assert result["natural_placement_score"] is None
    assert "details" not in json.dumps(result)


def test_anchor_target_is_rejected_before_client(monkeypatch, tmp_path):
    assets = json.loads(
        (run_judge.ROOT / "data/assets.json").read_text(encoding="utf-8")
    )["assets"]
    image = next(asset for asset in assets if asset["id"] == "comparison-row-02-v14")
    twin = next(
        asset
        for asset in assets
        if asset["id"] == "comparison-row-02-product_input"
    )
    runtime = {
        "generated_image": image["local_path"],
        "twin_image": twin["local_path"],
        "product_type": "laptop",
        "scene_prompt": image["original_prompt"],
        "image_stage": "scene_generation",
    }
    monkeypatch.setattr(
        run_judge,
        "client",
        lambda: pytest.fail("client must not be created for an anchor target"),
    )
    with pytest.raises(ValueError, match="match a visual anchor"):
        run_judge.judge(runtime, tmp_path / "result", visual_anchors=True)


def test_anchored_development_evaluation_excludes_demonstration_rows():
    report = evaluate("pilot_v1c", "development")

    assert report["visual_anchors_enabled"] is True
    assert report["metrics"]["excluded_demonstration_label_units"] == 3
    assert report["metrics"]["label_units"] == {
        "total": 4,
        "exact_target": 0,
        "comparison_set": 4,
    }
    assert {label["row"] for label in report["excluded_demonstration_labels"]} == {
        2,
        8,
        21,
    }
    assert {record["row"] for record in report["records"]} == {1, 5, 11, 25}

    labels = json.loads(
        (run_judge.ROOT / "data/pilot_labels.json").read_text(encoding="utf-8")
    )["labels"]
    quotes_by_record = {label["record"]: label["exact_quote"] for label in labels}
    for excluded in report["excluded_demonstration_labels"]:
        assert excluded["exact_quote"] == quotes_by_record[excluded["record"]]
