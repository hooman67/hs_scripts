import io
import json
import re
from dataclasses import replace

import numpy as np
import pytest
from PIL import Image

import hp3p.pipeline as pipeline
from hp3p.catalog import StyleRef
from hp3p.evalset import Row
from hp3p.pipeline import (
    _density_policy,
    _strip_fixed_meta_commentary,
    _validate_fixed_executable_prompt,
    run_row,
)


class Fake:
    def __init__(self, scale=1.0, shift=(0, 0)):
        self.calls = []
        self.scale, self.shift = scale, shift
        self.generated = None
        self.camera = "Near-frontal camera preserving the product viewpoint, with no zoom."
        self.composition = ("Preserve the product view and pixel size; build a usable support beneath its chosen "
                            "x-y position with believable edge clearances.")
        self.layout = "- The laptop remains near the user-facing edge of a shallow table."
        self.category = "laptop"
        self.rewrite_requests = []
        self.geometry = {
            "camera_height_m": 1.5, "support_height_m": 0.75, "look_at_height_m": 1.0,
            "horizontal_distance_m": 1.0, "vertical_fov_deg": 50, "axis_angle_deg": 20,
            "support_width_m": 1.2, "support_depth_m": 0.7, "product_footprint_width_m": 0.3,
            "product_footprint_depth_m": 0.2, "user_side": "near_camera", "user_edge_gap_m": 0.05,
            "support_lateral_offset_m": 0.0, "furniture_boxes": [],
        }

    def chat_json(self, system, text, images, schema):
        self.calls.append(("chat", len(images)))
        self.last_text = text
        if "Tones:" in system:
            self.selection_text = text
            return {"tone": "Warm", "content": "Cafe", "rationale": "cafe"}
        response = {"layout": self.layout, "camera": self.camera, "composition": self.composition,
                    "geometry": self.geometry,
                    "product_category": self.category, "prompt": "Place the laptop from Image 1 ..."}
        if "geometry" in schema["properties"]:
            self.geometry_request = {"images": images, "schema": schema, "system": system, "text": text}
        else:
            self.rewrite_request = {"images": images, "schema": schema, "system": system}
            self.rewrite_requests.append({"images": images, "schema": schema, "system": system, "text": text})
            if "FIXED-POSITION FALLBACK" in system:
                response.update(
                    layout="- The laptop stays at its initial frame position on a shallow table.",
                    camera="Near-frontal camera preserving the product viewpoint and initial framing.",
                    composition=("Keep the product at its exact initial frame position and build a usable support "
                                 "beneath it with believable edge clearances."),
                    prompt=("Turn Image 1 into a photograph; keep the laptop at its exact initial frame position "
                            "with its view, pixel size and details unchanged. Build the requested cafe scene around it."),
                )
        return {key: value for key, value in response.items() if key in schema["properties"]}

    def edit_image(self, prompt, images, size, mask=None):
        self.calls.append(("edit", len(images), size, mask is not None))
        self.edit_request = {"prompt": prompt, "images": images}
        hero = Image.open(io.BytesIO(images[-1][1])).convert("RGB")
        bg = Image.new("RGB", hero.size, (120, 110, 90))
        keep = Image.eval(hero.convert("L"), lambda v: 255 if v < 245 else 0)
        box = keep.getbbox()
        prod, m = hero.crop(box), keep.crop(box)
        size = (round(prod.width * self.scale), round(prod.height * self.scale))
        bg.paste(prod.resize(size), (box[0] + self.shift[0], box[1] + self.shift[1]), m.resize(size))
        buf = io.BytesIO()
        bg.save(buf, "PNG")
        self.generated = buf.getvalue()
        return self.generated


def _img(color, w=64, h=48, fmt="PNG"):
    buf = io.BytesIO()
    Image.new("RGB", (w, h), color).save(buf, fmt)
    return buf.getvalue()


@pytest.fixture(autouse=True)
def _stable_product_guard(monkeypatch):
    monkeypatch.setattr(
        pipeline,
        "assess_product_affine",
        lambda *args, **kwargs: {"guard_version": "test", "verdict": "pass", "reasons": []},
    )


CAT = [StyleRef(f"s{i}", "n", "Warm", "Cafe", "image/webp", _img((40, 60, 120 + i), fmt="WEBP")) for i in range(5)]
ROW = Row("b-1", "cafe table", "s3://x", 1024, 768, [], "laptop on a dark blue ottoman")


def _hero():
    img = Image.new("RGB", (400, 300), "white")
    img.paste((0, 0, 0), (100, 100, 200, 160))
    img.paste((200, 40, 40), (120, 110, 150, 130))
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


@pytest.mark.parametrize(
    "bounds,size,expected",
    [
        ([0, 0, 450, 100], (1000, 1000), "HIGH-FILL/CLOSE"),
        ([0, 0, 100, 450], (1000, 1000), "HIGH-FILL/CLOSE"),
        ([0, 0, 449, 449], (1000, 1000), "LOWER-FILL/MEDIUM-WIDE"),
    ],
)
def test_density_policy_uses_inclusive_45_percent_of_either_canvas_axis(bounds, size, expected):
    density_class, message = _density_policy({"product_bounds_px": bounds}, size)
    assert density_class == expected
    assert expected in message
    if expected == "HIGH-FILL/CLOSE":
        assert "exact initial x-y coordinates" in message
        assert "do not move the product even if exact size could be preserved" in message


def test_final_executable_prompt_has_active_density_branch_and_no_shrink_fallback(tmp_path):
    fake = Fake()
    result = run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1)
    assert result["guide_density_class"] == "LOWER-FILL/MEDIUM-WIDE"
    for text in (fake.last_text, result["prompt"]):
        assert result["guide_density_policy"] in text
        assert ("Preserve exact product pixel width and height and every other product invariant. Never shrink, "
                "enlarge, zoom, reframe, rotate, reproject, or crop the product to make a move feasible.") in text
        assert "if a move cannot preserve every invariant, retain the initial x-y coordinates instead" in text


def test_failed_first_guard_uses_one_fixed_position_fallback_and_preserves_both_attempts(tmp_path, monkeypatch):
    decisions = iter([
        {"guard_version": "test", "verdict": "fail", "reasons": ["singular_min"],
         "checks": {"singular_min": np.bool_(False)}, "matrix": np.eye(2)},
        {"guard_version": "test", "verdict": "pass", "reasons": [],
         "checks": {"singular_min": np.bool_(True)}, "matrix": np.eye(2)},
    ])
    monkeypatch.setattr(pipeline, "assess_product_affine", lambda *args, **kwargs: next(decisions))
    fake = Fake()
    result = run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1)
    out = tmp_path / "rows/b-1"
    assert result["status"] == "ok" and result["image_calls"] == 2
    assert result["product_invariant_guard"]["selected_attempt"] == 2
    assert (out / "gpt_1.png").exists() and (out / "gpt_2.png").exists()
    assert (out / "ours.png").read_bytes() == (out / "gpt_2.png").read_bytes()
    assert "fixed product position and invariant appearance" in result["fallback_prompt"]
    assert "exact initial frame position" in result["fallback_prompt"]
    assert not re.search(r"LOWER-FILL|\bx\s*[-–]\s*y\b|translat|relocat", result["fallback_prompt"], re.I)
    assert len(result["stage_b_attempts"]) == 2 and len(fake.rewrite_requests) == 2
    assert all(item.get("request_sha256") and item.get("response_sha256")
               for item in result["stage_b_attempts"])
    assert result["stage_b_attempts"][1]["executable_prompt_sha256"]
    assert (out / "stage_b_attempt_1_request.json").exists()
    assert (out / "stage_b_attempt_1_response.json").exists()
    assert (out / "stage_b_attempt_2_request.json").exists()
    assert (out / "stage_b_attempt_2_response.json").exists()
    assert json.loads((out / "image_request_attempt_2.json").read_text())["stage_b_rewritten"] is True
    persisted = json.loads((out / "result.json").read_text())
    assert persisted == result
    assert persisted["product_invariant_guard"]["attempts"][0]["checks"]["singular_min"] is False
    assert persisted["product_invariant_guard"]["attempts"][1]["checks"]["singular_min"] is True


def test_failed_fallback_returns_explicit_error_and_no_selected_output(tmp_path, monkeypatch):
    monkeypatch.setattr(
        pipeline,
        "assess_product_affine",
        lambda *args, **kwargs: {
            "guard_version": "test", "verdict": "fail", "reasons": ["rotation"],
            "checks": {"rotation": np.bool_(False)}, "matrix": np.eye(2),
        },
    )
    result = run_row(ROW, Fake(), CAT, tmp_path, _hero(), ref_count=1)
    out = tmp_path / "rows/b-1"
    assert result["status"] == "error" and result["image_calls"] == 2
    assert "rejected both image attempts" in result["error"]
    assert (out / "gpt_1.png").exists() and (out / "gpt_2.png").exists()
    assert not (out / "ours.png").exists()
    persisted = json.loads((out / "result.json").read_text())
    assert persisted == result
    assert len(persisted["product_invariant_guard"]["attempts"]) == 2
    assert all(attempt["checks"]["rotation"] is False
               for attempt in persisted["product_invariant_guard"]["attempts"])
    assert len(result["stage_b_attempts"]) == 2


def test_fixed_fallback_contradiction_is_rejected_before_second_image_call(tmp_path, monkeypatch):
    class ContradictoryFake(Fake):
        def chat_json(self, system, text, images, schema):
            response = super().chat_json(system, text, images, schema)
            if "FIXED-POSITION FALLBACK" in system:
                response["composition"] = "Move the laptop to the right for a better scene."
            return response

    monkeypatch.setattr(
        pipeline,
        "assess_product_affine",
        lambda *args, **kwargs: {"guard_version": "test", "verdict": "fail", "reasons": ["scale"]},
    )
    fake = ContradictoryFake()
    result = run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1)
    out = tmp_path / "rows/b-1"
    assert result["status"] == "error"
    assert "contradictory placement language" in result["error"]
    assert result["image_calls"] == 1
    assert [call[0] for call in fake.calls].count("chat") == 4
    assert [call[0] for call in fake.calls].count("edit") == 1
    assert len(result["stage_b_attempts"]) == 2
    assert (out / "stage_b_attempt_2_request.json").exists()
    assert (out / "stage_b_attempt_2_response.json").exists()
    assert not (out / "image_request_attempt_2.json").exists()
    assert not (out / "gpt_2.png").exists() and not (out / "ours.png").exists()


def test_fixed_meta_cleanup_removes_exact_astra_conflict_sentence_and_keeps_scene():
    text = ("The requested right-of-center relocation conflicts with fixed-position preservation, so the printer "
            "remains unchanged. The pale oak table occupies the middle plane beneath the printer.")
    cleaned = _strip_fixed_meta_commentary(text)
    assert cleaned == "The pale oak table occupies the middle plane beneath the printer."
    assert "relocation" not in cleaned
    # The sentence is explanatory rather than permission, so the active-command
    # validator itself allows it; cleanup keeps it out of the image prompt.
    _validate_fixed_executable_prompt(text)


@pytest.mark.parametrize("text", [
    "Move the printer to the right side of the table.",
    "Relocate the laptop toward the window.",
    "The product may be moved for a better composition.",
    "The printer can be translated to the center.",
    "LOWER-FILL permits a new position.",
    "Choose the laptop's x-y position freely.",
])
def test_fixed_validator_rejects_active_product_movement(text):
    with pytest.raises(ValueError, match="contradictory placement language"):
        _validate_fixed_executable_prompt(text)


@pytest.mark.parametrize("text", [
    "Never move the product from its initial frame position.",
    "Do not relocate the printer.",
    "The requested right-of-center relocation conflicts with fixed-position preservation, so the printer remains unchanged.",
])
def test_fixed_validator_allows_negated_or_rejected_movement(text):
    _validate_fixed_executable_prompt(text)


def test_high_fill_guard_fallback_keeps_one_stage_b_call(tmp_path, monkeypatch):
    monkeypatch.setattr(
        pipeline,
        "_density_policy",
        lambda *_: ("HIGH-FILL/CLOSE", "ACTIVE BRANCH: HIGH-FILL/CLOSE. Keep exact initial position."),
    )
    decisions = iter([
        {"guard_version": "test", "verdict": "fail", "reasons": ["fixed_translation_x"]},
        {"guard_version": "test", "verdict": "pass", "reasons": []},
    ])
    monkeypatch.setattr(pipeline, "assess_product_affine", lambda *args, **kwargs: next(decisions))
    fake = Fake()
    result = run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1)
    assert result["status"] == "ok" and result["image_calls"] == 2
    assert len(result["stage_b_attempts"]) == 1 and len(fake.rewrite_requests) == 1
    assert [call[0] for call in fake.calls].count("chat") == 3
    assert [call[0] for call in fake.calls].count("edit") == 2
    assert json.loads((tmp_path / "rows/b-1/image_request_attempt_2.json").read_text())["stage_b_rewritten"] is False


def test_run_row_flow_and_idempotence(tmp_path):
    fake = Fake()
    res = run_row(ROW, fake, CAT, tmp_path, _hero())
    assert res["status"] == "ok" and len(res["ref_ids"]) == 4 and res["masked"] is False
    assert fake.calls == [("chat", 0), ("chat", 5), ("chat", 6), ("edit", 1, "1216x912", False)]
    assert Image.open(tmp_path / "rows/b-1/ours.png").size == (1216, 912)
    assert not (tmp_path / "rows/b-1/ours_graded.png").exists()
    assert res["generation_mode"] == "direct" and res["image_calls"] == 1
    assert "Measured grade of Images 2-5" in fake.last_text
    assert ROW.raw_prompt not in fake.last_text
    assert res["baseline_prompt_used"] is False
    assert run_row(ROW, fake, CAT, tmp_path, _hero()) == res and len(fake.calls) == 4


def test_run_row_sends_ref_captions_to_rewriter(tmp_path):
    fake = Fake()
    caps = {f"s{i}": {"summary": f"cap-s{i}", "palette": []} for i in range(5)}
    res = run_row(ROW, fake, CAT, tmp_path, _hero(), captions=caps)
    for i, rid in enumerate(res["ref_ids"], 2):
        assert f"Image {i}: cap-{rid}" in fake.last_text
    assert res["captioned"] is True


def test_run_row_records_error_without_retry(tmp_path):
    fake = Fake()
    fake.edit_image = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("429"))
    res = run_row(ROW, fake, CAT, tmp_path, _hero())
    assert res["status"] == "error" and "429" in res["error"]
    assert json.loads((tmp_path / "rows/b-1/result.json").read_text())["status"] == "error"


@pytest.mark.parametrize("user_prompt", [
    "Warm office with integrated shelves, books and papers.",
    "Warm office with integrated shelves and minimal blue accents.",
    "Warm office with integrated shelves and no blue.",
    "Warm office with blue covering about 10% of the setting.",
    "Warm office with blue only on the curtains.",
])
def test_run_row_plans_only_from_original_request_with_explicit_blue_precedence(tmp_path, user_prompt):
    row = replace(ROW, user_prompt=user_prompt, baseline_prompt="BASELINE_SENTINEL: replace shelves",
                  raw_prompt="RAW_SENTINEL: replace office with a cafe")
    fake = Fake()
    result = run_row(row, fake, CAT, tmp_path, _hero(), ref_count=1)
    assert result["status"] == "ok" and result["baseline_prompt_used"] is False
    assert fake.selection_text == f"Scene request: {user_prompt}"
    assert f"Original user request: {user_prompt}" in fake.last_text
    assert row.baseline_prompt not in fake.last_text and row.raw_prompt not in fake.last_text
    system = " ".join(fake.rewrite_request["system"].split())
    assert "Explicit requests win: minimal blue means a few small named accents" in system
    assert "including no blue, is followed exactly" in system
    assert "Explicit minimal-blue or no-blue requests override that default" in result["prompt"]
    for text in (fake.last_text, fake.edit_request["prompt"]):
        text = " ".join(text.split())
        assert "one large blue surface/furnishing or" in text
        assert "multiple clearly visible blue elements" in text
        assert "Tiny props, thin partition frames, screen graphics, sky and lighting casts" in text
        assert "never change the product or its camera viewpoint to make room for blue" in text.lower()
    assert "blue amount/carrier or no-blue requests override this default" in fake.last_text
    assert "as do explicit blue amounts or carriers" in result["prompt"]
    assert "sole photographic-style authority" not in result["prompt"]
    assert "#103FB2" not in fake.rewrite_request["system"] + result["prompt"]


def test_missing_original_request_is_recorded_before_any_model_call(tmp_path):
    fake = Fake()
    result = run_row(replace(ROW, user_prompt=" ", baseline_prompt="a valid scene"), fake,
                     CAT, tmp_path, _hero())
    assert result["status"] == "error" and "original user request" in result["error"]
    assert not fake.calls and result["image_calls"] == 0


@pytest.mark.parametrize("size", [(1216, 912), (2368, 1776)])
def test_run_row_uses_selected_native_canvas_and_keeps_response_bytes(tmp_path, size):
    fake = Fake()
    result = run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1, size=size)
    assert result["status"] == "ok"
    expected = f"{size[0]}x{size[1]}"
    assert fake.calls == [("chat", 0), ("chat", 2), ("chat", 3), ("edit", 1, expected, False)]
    assert expected in fake.last_text and result["size"] == expected
    out = tmp_path / "rows" / ROW.id
    for name in ("input.png", "mask.png", "geometry_guide.png", "gpt_1.png", "ours.png"):
        assert Image.open(out / name).size == size
    assert (out / "ours.png").read_bytes() == (out / "gpt_1.png").read_bytes() == fake.generated
    assert run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1, size=size) == result
    assert len(fake.calls) == 4


@pytest.mark.parametrize("version", [
    None, "older-unified-policy", "unified-blue-v1", "unified-blue-v2", "unified-blue-scale-v2",
    "unified-blue-scale-v3",
])
def test_historical_and_earlier_policy_caches_require_a_fresh_run(tmp_path, version):
    fake = Fake()
    result = run_row(ROW, fake, CAT, tmp_path, _hero())
    if version is None:
        result.pop("pipeline_version")
    else:
        result["pipeline_version"] = version
    path = tmp_path / "rows" / ROW.id / "result.json"
    path.write_text(json.dumps(result))
    with pytest.raises(ValueError, match="different rewriting policy.*fresh run"):
        run_row(ROW, fake, CAT, tmp_path, _hero())
    assert json.loads(path.read_text()) == result and len(fake.calls) == 4


def test_cached_canvas_cannot_be_reused_at_a_different_resolution(tmp_path):
    fake = Fake()
    run_row(ROW, fake, CAT, tmp_path, _hero())
    with pytest.raises(ValueError, match="different size.*fresh run"):
        run_row(ROW, fake, CAT, tmp_path, _hero(), size=(2368, 1776))
    assert len(fake.calls) == 4


def test_native_wrong_size_response_is_preserved_without_retry_or_upscaling(tmp_path):
    fake = Fake()
    calls = []

    def wrong_size(*args, **kwargs):
        calls.append(1)
        return _img("gray", w=1216, h=912)

    fake.edit_image = wrong_size
    result = run_row(ROW, fake, CAT, tmp_path, _hero(), size=(2368, 1776))
    out = tmp_path / "rows" / ROW.id
    assert result["status"] == "error" and "expected 2368x1776" in result["error"]
    assert len(calls) == 1 and (out / "gpt_1.png").exists()
    assert not (out / "ours.png").exists()


def test_native_planner_and_guide_ignore_isolated_protected_corner_pixel(tmp_path):
    hero = Image.new("RGB", (2368, 1776), "white")
    hero.paste((50, 50, 50), (500, 300, 1700, 1400))
    hero.paste((240, 240, 240), (0, 1774, 2, 1776))
    buf = io.BytesIO()
    hero.save(buf, "PNG")
    fake = Fake()
    result = run_row(ROW, fake, CAT, tmp_path, buf.getvalue(), ref_count=1, size=hero.size)
    assert result["status"] == "ok"
    assert '"product_bounds_px": [501, 301, 1699, 1399]' in fake.last_text
    assert '"contact_px": [1100.0, 1398.5]' in fake.last_text
    assert result["guide_info"]["product_bounds_px"] == [501, 301, 1699, 1399]
    assert result["guide_info"]["contact_px"] == [1100.0, 1398.5]


def test_run_row_uses_astra_camera_and_composition_in_image_request(tmp_path):
    fake = Fake()
    res = run_row(ROW, fake, CAT, tmp_path, _hero())
    assert res.get("camera") == fake.camera and res.get("composition") == fake.composition
    assert set(fake.geometry_request["schema"]["required"]) == {"geometry", "product_category"}
    assert set(fake.rewrite_request["schema"]["required"]) == {"layout", "camera", "composition", "prompt"}
    assert f"Camera: {fake.camera}" in fake.edit_request["prompt"]
    assert f"Composition: {fake.composition}" in fake.edit_request["prompt"]
    assert fake.edit_request["prompt"] == res["prompt"]
    rewrite_images = fake.rewrite_request["images"]
    guide = (tmp_path / "rows/b-1/geometry_guide.png").read_bytes()
    hero_image, *refs = fake.geometry_request["images"]
    assert rewrite_images == [("image/png", guide), *refs, hero_image]
    assert fake.edit_request["images"] == [("image/png", guide)]
    assert Image.open(io.BytesIO(guide)).size == (1216, 912)
    assert res["geometry"] == fake.geometry
    assert res["guide_info"]["camera_pitch_deg"] == pytest.approx(26.565051)
    assert rewrite_images[-1] == ("image/png", (tmp_path / "rows/b-1/input.png").read_bytes())
    product = Image.open(io.BytesIO(rewrite_images[-1][1])).convert("RGB")
    assert product.getpixel((410, 365)) == (200, 40, 40)



def test_geometry_is_planned_before_prompt_writer_sees_the_drawn_guide(tmp_path):
    fake = Fake()
    res = run_row(ROW, fake, CAT, tmp_path, _hero())
    out = tmp_path / "rows/b-1"
    assert "camera" not in fake.geometry_request["schema"]["properties"]
    assert "written in a later call after the geometry guide is drawn." in fake.geometry_request["text"]
    assert "back_edge_against_wall" in fake.geometry_request["schema"]["properties"]["geometry"]["required"]
    assert "STAGE-B PLACEMENT AND SUPPORT OVERRIDE" in fake.rewrite_request["system"]
    assert fake.last_text.startswith("STAGE B. Image 1 contains an initial support diagram and the real "
                                     "product at its initial x-y position")
    assert res["geometry_text"] in fake.last_text and json.dumps(fake.geometry) in fake.last_text
    assert "Choose coherent estimated camera dimensions" not in fake.last_text
    assert (out / "geometry_text.txt").read_text() == res["geometry_text"]
    assert res["prompt"].startswith("GEOMETRY \u2014 subordinate only to the product invariants.\n"
                                    "Use Image 1 for the product's exact appearance, view and pixel size")
    assert fake.layout in res["prompt"]
    assert res["layout"] == fake.layout and res["geometry_text"] not in res["prompt"]
    assert "WRITE IN PLAIN VISUAL WORDS" in fake.last_text and "plain visual words" in fake.rewrite_request["system"]
    assert res["prompt"].endswith("No diagram remnants, old contact shadow, ghost or duplicate product remain.")
    assert json.loads((out / "geometry_response.json").read_text())["geometry"] == fake.geometry


def test_recomposed_support_policy_reaches_every_prompt_layer_without_changing_guide_flow(tmp_path):
    fake = Fake()
    res = run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1)
    assert res["status"] == "ok"
    stage_a = fake.geometry_request["system"] + fake.geometry_request["text"]
    stage_b = fake.rewrite_request["system"] + fake.last_text
    image_prompt = fake.edit_request["prompt"]
    for text in (stage_a, stage_b, image_prompt):
        assert "TRANSLATION-ONLY PRODUCT PLACEMENT; RECOMPOSED SUPPORT" in text
        assert "yaw, pitch, roll, viewing angle" in text
        assert "exact pixel width and height" in text
    assert "Do not pretranslate the guide" in stage_a
    assert "HIGH-FILL permits no geometric product change" in stage_b
    assert "LOWER-FILL permits only rigid image-plane x-y translation" in stage_b
    assert "ACTIVE BRANCH: LOWER-FILL/MEDIUM-WIDE" in stage_b
    assert "Choose product x-y freely for usable composition" in stage_b
    assert "support may change independently of the product's translation" in image_prompt
    assert "do not preserve baseline product-to-edge distances" in image_prompt
    assert "Do not move the product merely to center it" in image_prompt
    assert "ghost or duplicate product" in image_prompt
    assert not re.search(r"\breference\b", image_prompt, re.IGNORECASE)
    translation_policy = stage_b.split("WRITE IN PLAIN VISUAL WORDS", 1)[0]
    assert not re.search(r"\breference\b", translation_policy, re.IGNORECASE)
    for old_lock in ("Never move, resize, rotate", "unchanged in its place",
                     "Follow Image 1 exactly", "unchanged in position, size and orientation",
                     "tabletop covers exactly that area", "same displacement",
                     "preserve the planned support relationship"):
        assert old_lock not in stage_b + image_prompt
    assert fake.calls == [("chat", 0), ("chat", 2), ("chat", 3), ("edit", 1, "1216x912", False)]
    assert fake.edit_request["images"] == [
        ("image/png", (tmp_path / "rows/b-1/geometry_guide.png").read_bytes())
    ]


def test_non_laptop_category_rewords_geometry_text_for_its_support(tmp_path):
    fake = Fake()
    fake.category = "printer"
    res = run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1)
    assert res["status"] == "ok" and res["product_category"] == "printer"
    words = res["geometry_text"] + fake.last_text.split("Fixed geometry JSON")[0]
    assert "the printer is" in words and "Support orientation" in words
    assert "laptop" not in words and " table" not in words and "tabletop" not in words
    assert "support may change independently of the product's translation" in res["prompt"]
    assert "PRINTER AGAINST THE WALL" not in fake.rewrite_request["system"]
    fake.geometry = {**fake.geometry, "back_edge_against_wall": True}
    run_row(ROW, fake, CAT, tmp_path / "wall", _hero(), ref_count=1)
    assert "printer's back stands right against the wall" in fake.rewrite_request["system"]
    assert "PRINTER AGAINST THE WALL" not in fake.geometry_request["system"] + fake.geometry_request["text"]

def test_invalid_geometry_is_reported_before_image_generation(tmp_path):
    fake = Fake()
    fake.geometry["horizontal_distance_m"] = 0
    res = run_row(ROW, fake, CAT, tmp_path, _hero())
    assert res["status"] == "error" and "horizontal_distance_m" in res["error"]
    assert res["image_calls"] == 0 and fake.calls == [("chat", 0), ("chat", 5)]
    assert not (tmp_path / "rows/b-1/ours.png").exists()


def test_v8_lifestyle_composition_reaches_planner(tmp_path):
    fake = Fake()
    result = run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1)
    assert result["status"] == "ok"
    system = " ".join(fake.rewrite_request["system"].split())
    prompt = fake.edit_request["prompt"]
    assert "as if someone has just stepped away from using the product" in system
    assert "Plan furniture orientation and spacing together" in system
    assert "keep user_edge_gap_m small so the laptop sits near the desk's user-facing edge" in system
    assert "Describe the same support placement in composition and the final prompt" in system
    assert "Adapt furniture to the product's unchanged view and scale and its final permitted location" in system
    assert "Image 1 is the current canvas to edit" in prompt and "Estimated camera/support plan" not in prompt
    assert "envelope" not in prompt and "Furniture may extend beyond the frame" not in prompt
    planner = " ".join(fake.last_text.split())
    assert "physically plausible initial support plan take priority over requested layout" in planner
    assert "Priority for Stage B and final-scene construction: Image 3's exact" in system
    assert "never override explicit user requirements" not in system
    assert "never between the product and that edge or beyond it" in system
    assert "There is no tabletop beyond the user-facing edge" in system
    assert prompt.startswith("GEOMETRY — subordinate only to the product invariants")
    assert "Final check before rendering" in prompt
    assert fake.calls == [("chat", 0), ("chat", 2), ("chat", 3), ("edit", 1, "1216x912", False)]


SIZE_QUOTE = 'Product dimensions: 15.7" x 15.7" x 13.4".'


@pytest.mark.parametrize("ref_count,size", [(1, (1216, 912)), (4, (2368, 1776))])
def test_supplied_size_reaches_planner_and_final_prompt_without_extra_calls(tmp_path, ref_count, size):
    row = replace(ROW, user_prompt="Office table with papers. " + SIZE_QUOTE)
    fake = Fake()
    result = run_row(row, fake, CAT, tmp_path, _hero(), ref_count=ref_count, size=size)
    assert result["status"] == "ok"
    assert fake.calls == [
        ("chat", 0), ("chat", ref_count + 1), ("chat", ref_count + 2),
        ("edit", 1, f"{size[0]}x{size[1]}", False),
    ]
    assert "product_width_fraction" in fake.last_text
    assert "Explicit user-supplied product size" in fake.last_text
    assert "[0.39878, 0.39878, 0.34036]" in fake.geometry_request["text"]
    assert "Physical scale plan" not in fake.edit_request["prompt"]
    assert (tmp_path / "rows/b-1/ours.png").read_bytes() == fake.generated


def test_changed_dimension_input_cannot_reuse_same_row_cache(tmp_path):
    fake = Fake()
    before = run_row(ROW, fake, CAT, tmp_path, _hero())
    with pytest.raises(ValueError, match="different user input.*fresh run"):
        run_row(replace(ROW, user_prompt=ROW.user_prompt + " " + SIZE_QUOTE),
                fake, CAT, tmp_path, _hero())
    assert json.loads((tmp_path / "rows/b-1/result.json").read_text()) == before
    assert len(fake.calls) == 4


@pytest.mark.parametrize("scale,shift", [(1.0, (0, 0)), (0.8, (60, -40)), (1.3, (420, 0))])
def test_run_row_keeps_generated_bytes_without_geometry_or_grade_repairs(tmp_path, scale, shift):
    fake = Fake(scale=scale, shift=shift)
    res = run_row(ROW, fake, CAT, tmp_path, _hero())
    assert [c[0] for c in fake.calls].count("edit") == 1
    assert not res["aligned"] and not res["graded"] and res["locate"] is None
    out = tmp_path / "rows/b-1"
    assert (out / "ours.png").read_bytes() == (out / "gpt_1.png").read_bytes() == fake.generated
    assert Image.open(out / "ours.png").size == (1216, 912)
    assert not (out / "ours_graded.png").exists()


def test_run_row_reports_unexpected_output_size_without_resizing_or_retry(tmp_path):
    fake = Fake()
    image_calls = []

    def wrong_size(*args, **kwargs):
        image_calls.append(1)
        return _img("gray")

    fake.edit_image = wrong_size
    res = run_row(ROW, fake, CAT, tmp_path, _hero())
    assert res["status"] == "error" and "64x48" in res["error"] and "1216x912" in res["error"]
    assert len(image_calls) == 1 and not (tmp_path / "rows/b-1/ours.png").exists()


def test_single_reference_mode_passes_only_first_reference_and_guide(tmp_path):
    from hp3p.catalog import pick_refs

    fake = Fake()
    res = run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1)
    first = pick_refs(CAT, "Warm", "Cafe", seed=ROW.id)[0]
    assert res["status"] == "ok" and res["ref_ids"] == [first.id]
    assert fake.calls == [("chat", 0), ("chat", 2), ("chat", 3), ("edit", 1, "1216x912", False)]
    assert fake.geometry_request["images"][1:] == [(first.mime, first.data)]
    out = tmp_path / "rows/b-1"
    assert fake.edit_request["images"] == [("image/png", (out / "geometry_guide.png").read_bytes())]
    assert fake.rewrite_request["images"][2] == ("image/png", (out / "input.png").read_bytes())
    assert "Image 6" not in fake.rewrite_request["system"] + fake.edit_request["prompt"]
    assert "Images 2-5" not in fake.last_text + fake.rewrite_request["system"] + fake.edit_request["prompt"]
    assert "Image 3" not in fake.edit_request["prompt"] and "Image 2" not in fake.edit_request["prompt"]
    assert "Image 2" in fake.last_text
    assert (out / "ours.png").read_bytes() == fake.generated
    assert not (out / "ours_graded.png").exists()


def test_reference_grade_saves_separate_output_without_another_image_call(tmp_path):
    from hp3p.pipeline import grade_row

    reference = Image.new("RGB", (64, 48), "white")
    reference.paste((50, 80, 130), (0, 0, 32, 48))
    buf = io.BytesIO()
    reference.save(buf, "PNG")
    cat = [StyleRef("only", "n", "Warm", "Cafe", "image/png", buf.getvalue())]
    fake = Fake()
    run_row(ROW, fake, cat, tmp_path, _hero(), ref_count=1)
    out = tmp_path / "rows/b-1"
    res = grade_row(out)
    assert res["graded"] and res["grading"]["scope"] == "whole_image"
    assert not res["grading"]["product_colors_preserved"]
    assert res["grade_error"] is None
    assert (out / "ours.png").read_bytes() == (out / "gpt_1.png").read_bytes() == fake.generated
    assert Image.open(out / "ours_graded.png").size == (1216, 912)
    assert (out / "ours_graded.png").read_bytes() != fake.generated
    assert res == json.loads((out / "result.json").read_text())
    assert grade_row(out) == res
    assert sum(c[0] == "edit" for c in fake.calls) == 1


def test_reference_grading_failure_is_explicit_and_keeps_raw_output(tmp_path):
    from hp3p.pipeline import grade_row

    fake = Fake()
    run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1)
    out = tmp_path / "rows/b-1"
    res = grade_row(out)
    assert res["status"] == "ok" and not res["graded"]
    assert "tonal variation" in res["grade_error"]
    assert (out / "ours.png").read_bytes() == fake.generated
    assert not (out / "ours_graded.png").exists()


def test_cached_row_cannot_silently_change_reference_mode(tmp_path):
    fake = Fake()
    before = run_row(ROW, fake, CAT, tmp_path, _hero())
    with pytest.raises(ValueError, match="fresh run"):
        run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1)
    assert len(fake.calls) == 4
    assert json.loads((tmp_path / "rows/b-1/result.json").read_text()) == before


@pytest.mark.parametrize("size", ["1216x912", "2368x1776"])
def test_cli_renders_raw_and_grade_error_before_exiting(tmp_path, monkeypatch, size):
    from hp3p import cli, openai_client

    def download(row, dest):
        path = dest / "hero.png"
        path.write_bytes(_hero())
        return path

    fake = Fake()
    monkeypatch.setattr(cli, "ROOT", tmp_path)
    monkeypatch.setattr(cli, "load_rows", lambda *args: [ROW])
    monkeypatch.setattr(cli, "load_catalog", lambda *args: CAT)
    monkeypatch.setattr(cli, "download_hero", download)
    monkeypatch.setattr(openai_client, "OpenAIClient", lambda: fake)
    monkeypatch.setattr("sys.argv", ["hp3p", "run", "--run-id", "grade-error",
                                  "--refs", "1", "--grade", "--no-captions", "--size", size])
    with pytest.raises(RuntimeError, match="grading failed"):
        cli.main()
    html = (tmp_path / "runs/grade-error/viewer.html").read_text()
    assert "insufficient tonal variation" in html
    assert "1 HP style ref" in html and "4 HP style refs" not in html
    assert 'href="rows/b-1/ours.png"' in html
    assert Image.open(tmp_path / "runs/grade-error/rows/b-1/ours.png").size == tuple(
        int(value) for value in size.split("x"))
    assert sum(c[0] == "edit" for c in fake.calls) == 1


def test_nearest_grade_replaces_stale_grade_from_raw_without_changing_generation_refs(tmp_path):
    from hp3p.grade import reference_statistics
    from hp3p.pipeline import grade_row

    raw = _hero()
    old_reference = _img((30, 40, 50))
    (tmp_path / "ours.png").write_bytes(raw)
    (tmp_path / "gpt_1.png").write_bytes(raw)
    (tmp_path / "ours_graded.png").write_bytes(_img("blue"))
    (tmp_path / "ref_2.png").write_bytes(old_reference)
    (tmp_path / "result.json").write_text(json.dumps({
        "status": "ok", "generation_mode": "direct", "ref_ids": ["original"],
        "graded": True, "grading": {"reference_file": "ref_2.png"},
    }))
    catalog = [StyleRef("nearest", "n", "Other", "Home", "image/png", raw)]
    index = reference_statistics(catalog, tmp_path / "stats.json")
    result = grade_row(tmp_path, catalog=catalog, reference_stats=index)
    assert result["graded"] and result["grade_error"] is None
    assert result["ref_ids"] == ["original"]
    assert result["grading"]["reference_file"] == "grade_reference.png"
    assert result["grading"]["selection"]["reference_id"] == "nearest"
    assert (tmp_path / "grade_reference.png").read_bytes() == raw
    assert (tmp_path / "ours.png").read_bytes() == (tmp_path / "gpt_1.png").read_bytes() == raw
    assert (tmp_path / "ref_2.png").read_bytes() == old_reference
    pixels = Image.open(tmp_path / "ours_graded.png").convert("RGB")
    assert pixels.size == (400, 300) and pixels.getpixel((0, 0)) == (255, 255, 255)
    assert max(pixels.getpixel((110, 110))) <= 2


def test_image_prompt_naming_an_unsent_image_fails_before_the_image_call(tmp_path):
    fake = Fake()
    fake.composition = "Match Image 2's soft daylight and the reference's oak texture."
    res = run_row(ROW, fake, CAT, tmp_path, _hero(), ref_count=1)
    assert res["status"] == "error" and "does not receive" in res["error"]
    assert "edit" not in [call[0] for call in fake.calls]
