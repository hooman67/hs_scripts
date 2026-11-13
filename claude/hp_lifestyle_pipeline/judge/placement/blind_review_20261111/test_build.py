import copy

import build
import pytest


def rows():
    result = []
    for device in ("cashmere", "elitebook", "magic", "tassel"):
        for camera in ("front", "left", "right", "wide"):
            for number in range(10):
                key = [device, camera, number]
                result.append(
                    {
                        "key": key,
                        "prompt": {"text_sha256": build.rank("prompt", key)},
                        "output": {
                            "image_sha256": build.rank("pixels", key),
                            "reuse_status": "new",
                        },
                    }
                )
    return result


def test_selection_excludes_source_pixel_and_prompt_reuse_and_is_order_independent():
    source = rows()
    keys = {build.identity(source[0])}
    pixels = {source[1]["output"]["image_sha256"]}
    prompts = {source[2]["prompt"]["text_sha256"]}
    source[3]["output"]["reuse_status"] = "reused"
    chosen, partitions, eligible = build.select(source, keys, pixels, prompts)
    assert build.select(list(reversed(source)), keys, pixels, prompts) == (
        chosen,
        partitions,
        eligible,
    )
    assert eligible == 156
    assert len(chosen) == len(partitions) == 30
    assert not {build.identity(row) for row in chosen} & keys
    assert not {row["output"]["image_sha256"] for row in chosen} & pixels
    assert not {row["prompt"]["text_sha256"] for row in chosen} & prompts
    assert build.Counter(partitions.values()) == {"calibration": 20, "held_out": 10}
    assert build.Counter(row["key"][0] for row in chosen) == {
        "cashmere": 8,
        "elitebook": 8,
        "magic": 7,
        "tassel": 7,
    }
    assert len({tuple(row["key"][:2]) for row in chosen}) == 16


def test_exact_scene_variants_cannot_cross_partition():
    source = rows()
    source[40]["prompt"]["text_sha256"] = source[0]["prompt"]["text_sha256"]
    source[80]["output"]["image_sha256"] = source[1]["output"]["image_sha256"]
    chosen, _, _ = build.select(source, set(), set(), set())
    assert len({row["prompt"]["text_sha256"] for row in chosen}) == 30
    assert len({row["output"]["image_sha256"] for row in chosen}) == 30


def test_unresolved_annotation_keys_fail_instead_of_silent_exclusion():
    source = {
        "rows": [
            {"meta_data": {"row_idx": 1, "evalset_item_id": "cashmere / front / 2"}}
        ]
    }
    document = {
        "rows": [
            {"row_idx": 1, "key": "cashmere / front / 2", "comment": "Human words"}
        ]
    }
    assert build.annotation_exclusions(document, source) == {"cashmere / front / 2"}
    changed = copy.deepcopy(document)
    changed["rows"][0]["key"] = "wrong"
    with pytest.raises(ValueError, match="identity mismatch"):
        build.annotation_exclusions(changed, source)


def test_evidence_write_is_immutable(tmp_path):
    path = tmp_path / "evidence.json"
    build.emit(path, {"original": True})
    build.emit(path, {"original": True})
    with pytest.raises(ValueError, match="overwrite frozen"):
        build.emit(path, {"original": False})
