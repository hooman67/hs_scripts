"""Model-free checks for the isolated V3 spatial-crop experiment."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image

import run_spatial_crops as spatial


EXPERIMENT_BATCH = spatial._load_module(
    "placement_v3_spatial_crop_test_batch", spatial.ROOT / "run_batch.py"
)


def write_pattern(path: Path, size: tuple[int, int] = (10, 8)) -> None:
    image = Image.new("RGB", size)
    for y in range(size[1]):
        for x in range(size[0]):
            image.putpixel((x, y), (x * 17 % 256, y * 29 % 256, (x + y) * 13 % 256))
    image.save(path, format="PNG")


def observation() -> dict:
    scene_reading = {
        "functional_front": "The operating front is visible.",
        "support_surface": "A rectangular table supports the device.",
        "usable_approach_edge": "The near edge is available.",
        "actual_user_position": "A chair is placed at the near edge.",
        "access_path": "The access route is clear.",
        "device_support_axes": "The device and table axes align.",
        "neighboring_furniture": "The chair belongs to the table.",
        "narrative_status": "supported",
        "narrative_evidence": "The scene supports ordinary use.",
        "support_placement_in_room": "The table belongs in this location.",
        "usable_space_distribution": "Useful surface area remains clear.",
        "alternative_user_positions": "No alternative is needed.",
        "prop_relationships": "Nearby props fit the activity.",
        "lived_in_evidence": "The work props make the scene inhabited.",
    }
    component = {
        "visibility": "observed",
        "severity": 0,
        "confidence": "high",
        "evidence": "The relevant relation is plainly visible.",
        "consequence": "",
        "issue_codes": [],
    }
    return {
        "schema_version": "placement-observations-v3",
        "product_match": "match",
        "product_match_note": "The device matches the reference.",
        "scene_reading": scene_reading,
        "components": {
            name: dict(component) for name in spatial.SCORING.COMPONENT_WEIGHTS
        },
        "summary": "The visible arrangement supports normal use.",
        "suggested_scene_changes": [],
    }


def test_quadrants_extend_ten_percent_across_each_center_seam() -> None:
    boxes = spatial.quadrant_boxes(100, 80)
    assert [item["box_xyxy_exclusive"] for item in boxes] == [
        [0, 0, 60, 48],
        [40, 0, 100, 48],
        [0, 32, 60, 80],
        [40, 32, 100, 80],
    ]
    assert boxes[0]["normalized_xyxy_exclusive"] == [0.0, 0.0, 0.6, 0.6]


def test_lossless_crops_have_exact_source_pixels_and_no_resize(tmp_path: Path) -> None:
    source_path = tmp_path / "source.png"
    crop_dir = tmp_path / "crops"
    write_pattern(source_path)

    original, crops = spatial.build_crops(source_path, crop_dir)

    assert original["sha256"] == spatial.sha256_path(source_path)
    with Image.open(source_path) as source:
        for crop in crops:
            with Image.open(crop["path"]) as stored:
                expected = source.crop(tuple(crop["box_xyxy_exclusive"]))
                assert stored.size == expected.size
                assert list(stored.getdata()) == list(expected.getdata())
            assert crop["resize_applied"] is False
            assert crop["pixel_values_verified"] is True
            assert crop["sha256"] == spatial.sha256_path(crop["path"])
    with pytest.raises(FileExistsError):
        spatial.build_crops(source_path, crop_dir)


def test_prompt_is_root_authored_complete_prompt_sent_once() -> None:
    effective, hashes = spatial.combined_system_prompt()
    root = spatial.V3_SYSTEM_PROMPT.read_text(encoding="utf-8").strip()
    assert effective.count(root) == 1
    assert effective.startswith("VISUAL INSPECTION INPUTS")
    assert hashes["combined_system_prompt_sha256"] == spatial.sha256_bytes(
        effective.encode("utf-8")
    )


def test_message_image_order_is_twin_full_scene_then_four_crops(tmp_path: Path) -> None:
    generated = tmp_path / "generated.png"
    twin = tmp_path / "twin.png"
    write_pattern(generated)
    write_pattern(twin)
    _, crops = spatial.build_crops(generated, tmp_path / "crops")
    messages = spatial.build_messages(
        {
            "generated_image": str(generated),
            "twin_image": str(twin),
            "product_type": "laptop",
            "scene_prompt": "A normal office.",
            "image_stage": "scene_generation",
        },
        "system",
        crops,
    )
    content = messages[1]["content"]
    images = [item for item in content if item["type"] == "image_url"]
    labels = [item["text"] for item in content if item["type"] == "text"]
    assert len(images) == 6
    assert images[0] == spatial.image_content(twin)
    assert images[1] == spatial.image_content(generated)
    assert labels[1].startswith("B —")
    assert labels[2].startswith("A — full")
    assert "left=0, top=0, right=6, bottom=5" in labels[3]


def test_unlabeled_target_rejects_feedback_keys() -> None:
    payload = {
        "dataset_role": "evaluation_target_unlabeled",
        "separation_from_training": {
            "target_contains_human_feedback": False,
            "target_contains_diagnostic_expectations": False,
        },
        "records": [{"id": "case", "human_feedback": "bad placement"}],
    }
    with pytest.raises(ValueError, match=r"\$\.records\[0\]\.human_feedback"):
        EXPERIMENT_BATCH.validate_manifest_separation(payload)


def test_diagnostic_labels_are_source_only() -> None:
    payload = {
        "input_contract": {"annotations_passed_to_judge": False},
        "records": [
            {
                "id": "case",
                "human_feedback": "bad placement",
                "diagnostic_expectation": {"acceptable_verdicts": ["fail"]},
            }
        ],
    }
    kind, paths = EXPERIMENT_BATCH.validate_manifest_separation(payload)
    assert kind == "diagnostic_regression_labels_source_only"
    assert paths == [
        "$.records[0].human_feedback",
        "$.records[0].diagnostic_expectation",
    ]


def test_two_attempt_bound_raw_response_and_deterministic_outputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generated = tmp_path / "generated.png"
    twin = tmp_path / "twin.png"
    write_pattern(generated)
    write_pattern(twin)
    runtime_input = {
        "generated_image": str(generated),
        "twin_image": str(twin),
        "product_type": "printer",
        "scene_prompt": "A normal office printer station.",
        "image_stage": "scene_generation",
    }
    value = observation()
    raw = {
        "id": "response-id",
        "model": "gpt-5.5",
        "usage": {"prompt_tokens": 12, "completion_tokens": 34},
        "opaque_component": {"preserved": True},
    }

    class TransientError(Exception):
        status_code = 503
        response = SimpleNamespace(headers={"retry-after": "0"})

    class Response:
        model = "gpt-5.5"
        choices = [
            SimpleNamespace(
                finish_reason="stop",
                message=SimpleNamespace(
                    refusal=None, content=json.dumps(value, separators=(",", ":"))
                ),
            )
        ]

        def model_dump(self, mode: str) -> dict:
            assert mode == "json"
            return raw

    calls: list[dict] = []

    def create(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            raise TransientError("retry")
        return Response()

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )
    freeze = {
        "protocol_version": spatial.PROTOCOL_VERSION,
        "crop_policy": spatial.current_protocol_state()["crop_policy"],
        "request_policy": spatial.current_protocol_state()["request_policy"],
    }
    test_freeze = tmp_path / "freeze.json"
    test_freeze.write_text(json.dumps(freeze), encoding="utf-8")
    monkeypatch.setattr(spatial, "FREEZE_PATH", test_freeze)
    monkeypatch.setattr(spatial, "ensure_frozen", lambda: freeze)
    monkeypatch.setattr(spatial.CANONICAL, "client", lambda: (fake_client, "test"))
    monkeypatch.setattr(spatial.time, "sleep", lambda _seconds: None)

    output_dir = tmp_path / "output"
    crop_dir = tmp_path / "crop-output"
    result = spatial.judge(runtime_input, output_dir, crop_dir)

    assert result["ok"] is True
    assert len(calls) == spatial.MAX_ATTEMPTS == 2
    assert json.loads((output_dir / "response.json").read_text()) == raw
    assert json.loads((output_dir / "observation.json").read_text()) == value
    judgment = json.loads((output_dir / "judgment.json").read_text())
    assert result["judgment"] == judgment
    assert [attempt["status"] if "status" in attempt else None for attempt in result["attempts"]] == [503, "ok"]
    request = json.loads((output_dir / "request.json").read_text())
    assert request["original_images"]["generated_scene_A"]["sha256"] == spatial.sha256_path(generated)
    assert [item["name"] for item in request["crops"]] == [
        "top_left",
        "top_right",
        "bottom_left",
        "bottom_right",
    ]
    assert calls[1]["model"] == "gpt-5.5"
    assert calls[1]["reasoning_effort"] == "high"
    assert calls[1]["max_completion_tokens"] == 12000
    with pytest.raises(FileExistsError):
        spatial.judge(runtime_input, output_dir, tmp_path / "other-crops")
