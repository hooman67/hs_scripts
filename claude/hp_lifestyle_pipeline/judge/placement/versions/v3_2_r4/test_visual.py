"""Native coverage and independent acquisition cannot leak judging outcomes."""

import json
from pathlib import Path

import common
import pytest
import visual
from PIL import Image
from test_common import FakeClient, frame, observation


def setup(tmp_path, monkeypatch, size=(1600, 950)):
    monkeypatch.setattr(common, "ROOT", tmp_path)
    monkeypatch.setattr(common, "verify_freeze", lambda: "frozen")
    common.write_json(
        tmp_path / "visual_policy.json",
        {
            "tile_size_pixels": 768,
            "overlap_pixels": 192,
            "max_encoded_image_bytes": 45_000_000,
            "max_encoded_request_image_bytes": 105_000_000,
            "image_adapter_detail": "high",
        },
    )
    prompts = tmp_path / "prompts"
    prompts.mkdir()
    (prompts / "visual_acquisition.txt").write_text(
        "Actual acquisition policy fixture."
    )
    image = Image.new("RGB", size, (100, 130, 160))
    for x in range(size[0]):
        image.putpixel((x, size[1] // 2), (x % 256, (x // 256) % 256, 0))
    source = tmp_path / "source.png"
    image.save(source)
    return {
        "generated_image": str(source),
        "twin_image": str(source),
        "scene_prompt": "SECRET target-specific scene description.",
        "product_type": "laptop",
        "image_stage": "scene_generation",
    }


@pytest.mark.parametrize("size", [(1600, 950), (200, 150)])
def test_every_original_pixel_is_covered_without_resize_and_tiles_are_exact(
    tmp_path, monkeypatch, size
):
    runtime = setup(tmp_path, monkeypatch, size)
    packet = visual.prepare(runtime)
    assert packet["delivered_images"][0]["label"] == "A: full original image"
    assert any(
        item["label"] == "B: full original image" for item in packet["delivered_images"]
    )
    covered = Image.new("1", size)
    with Image.open(runtime["generated_image"]) as original:
        for item in packet["coverage"]:
            box = tuple(item["crop_box"])
            with Image.open(item["local_path"]) as tile:
                assert tile.size == tuple(item["tile_dimensions"])
                assert max(tile.size) <= 768
                assert tile.tobytes() == original.crop(box).tobytes()
            if item["source_role"] == "generated_image":
                covered.paste(1, box)
    assert covered.getextrema() == (1, 1)
    assert visual.prepare(runtime) == packet
    delivered = [
        item
        for item in packet["delivered_images"]
        if item["label"].startswith("A: neutral")
    ]
    assert len({item["sha256"] for item in delivered}) == len(delivered)


def test_acquisition_is_branch_independent_blind_unscored_and_replayed(
    tmp_path, monkeypatch
):
    runtime = setup(tmp_path, monkeypatch, (200, 150))
    packet = visual.prepare(runtime)
    client = FakeClient(
        [
            [frame('{"record":"A literal exposed edge."}', "stop")],
            [frame('{"record":"A separate independent observation."}', "stop")],
        ]
    )
    a = visual.acquire(
        runtime,
        "baseline",
        tmp_path / "baseline",
        packet,
        ["orientation_alignment"],
        client,
    )
    b = visual.acquire(
        runtime,
        "compact",
        tmp_path / "compact",
        packet,
        ["orientation_alignment"],
        client,
    )
    assert a["path"] != b["path"]
    assert a["record"] != b["record"]
    assert a["scored"] is b["scored"] is False
    assert len(client.requests) == 2
    for request in client.requests:
        assert "SECRET" not in json.dumps(request)
        assert "A literal exposed edge." not in json.dumps(request["messages"])
        assert request["response_format"]["json_schema"]["schema"]["required"] == [
            "record"
        ]
    assert (
        visual.acquire(
            runtime,
            "baseline",
            tmp_path / "baseline",
            packet,
            ["orientation_alignment"],
            client,
        )
        == a
    )
    assert len(client.requests) == 2
    with pytest.raises(ValueError, match="different branch"):
        visual.acquire(
            runtime, "use", tmp_path / "baseline", packet, ["access_usability"], client
        )


def test_changed_delivered_tile_is_rejected_without_another_draw(tmp_path, monkeypatch):
    runtime = setup(tmp_path, monkeypatch, (200, 150))
    packet = visual.prepare(runtime)
    tile = next(
        item for item in packet["delivered_images"] if "neutral tile" in item["label"]
    )
    Path(tile["local_path"]).write_bytes(b"changed")
    with pytest.raises(ValueError, match="packet changed"):
        visual.prepare(runtime)


def test_scored_stage_receives_its_own_acquisition_and_identical_visual_coverage(
    tmp_path, monkeypatch
):
    runtime = setup(tmp_path, monkeypatch, (200, 150))
    (tmp_path / "prompts/p1_compact.txt").write_text("Scored role fixture.")
    value = observation()
    client = FakeClient(
        [
            [frame('{"record":"Separate literal boundaries."}', "stop")],
            [frame(json.dumps(value), "stop")],
        ]
    )
    arguments = (
        runtime,
        "p1_compact",
        tmp_path / "judgment",
        common.OBSERVATION_SCHEMA,
        common.LEGACY.validate_new_observation,
    )
    result = common.call_stage(*arguments, client=client)
    assert result["observation"] == value
    assert result["visual_acquisition"]["record"] == "Separate literal boundaries."
    assert len(client.requests) == 2
    acquisition, judging = client.requests
    assert "SECRET" not in json.dumps(acquisition)
    assert "SECRET" in json.dumps(judging)
    assert "Separate literal boundaries." in json.dumps(judging)
    assert [
        item
        for item in acquisition["messages"][-1]["content"]
        if item["type"] == "image_url"
    ] == [
        item
        for item in judging["messages"][-1]["content"]
        if item["type"] == "image_url"
    ]
    assert common.call_stage(*arguments, client=client) == result
    assert len(client.requests) == 2
