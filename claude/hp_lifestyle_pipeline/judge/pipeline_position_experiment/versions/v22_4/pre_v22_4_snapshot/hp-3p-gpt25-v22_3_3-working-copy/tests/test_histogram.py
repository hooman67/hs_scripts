import gzip
import json

import numpy as np
import pytest

from hp3p.histogram import HistogramLookup, build_index
from hp3p.reference_style import (
    lab,
    material_anchor,
    resolve_bindings,
    rgb,
    select_reference,
)


@pytest.fixture
def lookup(tmp_path):
    source = tmp_path / "source.csv.gz"
    with gzip.open(source, "wt") as stream:
        stream.write("category,hex,pixel_count,fraction_of_category_blue_pixels\n"
                     "chair,#357773,9,1\n"
                     "unassigned_blue_region,#357773,100,1\n"
                     "wall,#3E7872,3,0.0003\n"
                     "wall,#59636D,9000,0.9\n"
                     "wall,#010101,1000,0.0997\n")
    build_index(source, tmp_path / "index")
    return HistogramLookup(tmp_path / "index")


def test_full_histogram_keeps_rare_closer_shades_and_element_boundaries(lookup):
    match = lookup.nearest({"hex": "#357773"}, "wall")
    compact_distance = float(np.linalg.norm(lab(rgb("#59636D")) - lab(rgb("#357773"))))
    assert match["hex"] == "#3E7872" and match["exact_source_pixel_count"] == 3
    assert match["distance_CIELAB76"] < compact_distance / 5
    assert "#357773" not in lookup["wall"] and "#010101" not in lookup["wall"]
    assert lookup.nearest({"hex": "#357773"}, "chair")["distance_CIELAB76"] == 0
    assert "unassigned_blue_region" not in lookup
    with pytest.raises(ValueError, match="Unknown histogram"):
        lookup.nearest({"hex": "#357773"}, "missing")


def test_histogram_rejects_changed_source_and_index_bytes(lookup, tmp_path):
    source = tmp_path / "source.csv.gz"
    source.write_bytes(b"changed")
    with pytest.raises(ValueError, match="different source"):
        build_index(source, tmp_path / "index")
    path = tmp_path / "index/wall.npy"
    path.write_bytes(path.read_bytes() + b"changed")
    with pytest.raises(ValueError, match="bytes changed"):
        HistogramLookup(tmp_path / "index")["wall"]


def test_tag_filter_precedes_brightness_and_never_crosses_fallback():
    metadata = [
        {"id": identity, "human_presence": presence, "content": "Office", "brightness_score": score}
        for identity, presence, score in (("dark", "no_humans", 10), ("bright", "no_humans", 70),
                                          ("person", "human", 90), ("unknown", "unknown", 100))
    ]
    proposal = {"reference_ids": ["person", "dark", "bright"], "human_policy": "no_humans",
                "brightness": "balanced", "content": "Office"}
    assert select_reference(proposal, metadata, "A bright home with warm wood")["reference_id"] == "bright"
    people = {**proposal, "human_policy": "human", "content": "Missing"}
    assert select_reference(people, metadata, "A woman at work")["reference_id"] == "person"
    assert select_reference(people, metadata, "A cafe without a person")["human_policy"] == "no_humans"
    assert select_reference({**proposal, "brightness": "dim"}, metadata, "Dark walnut furniture")["resolved_brightness"] == "balanced"
    with pytest.raises(ValueError, match="required human-presence tag"):
        select_reference({**people, "reference_ids": ["dark", "bright"]}, metadata[:2], "A woman at work")


def test_material_pixels_and_consistent_prompt_substitution(lookup):
    from test_pipeline import _img

    reference = _img("#357773")
    binding = {"instance": "blue tiles", "element": "wall", "reference_region": [0, 0, 1, 1],
               "anchor_kind": "physical_blue", "reference_material": "tile"}
    response = {"blue_elements": [binding], "composition": "__BLUE_0_HEX__", "prompt": "__BLUE_0_HEX__"}
    rewritten, bindings = resolve_bindings(response, reference, lookup, "A cafe")
    assert rewritten["composition"] == rewritten["prompt"] == "#3E7872"
    assert bindings[0]["reference_anchor"]["hex"] == "#357773"
    assert response["prompt"] == "__BLUE_0_HEX__"
    for modified in ({**response, "composition": "missing"},
                     {**response, "prompt": "__BLUE_0_HEX__ __BLUE_1_HEX__"},
                     {**response, "blue_elements": [binding, binding]},
                     {**response, "blue_elements": []}):
        with pytest.raises(ValueError):
            resolve_bindings(modified, reference, lookup, "A cafe")
    assert resolve_bindings({"blue_elements": [], "composition": "", "prompt": ""},
                            reference, lookup, "A cafe without blue")[1] == []
    with pytest.raises(ValueError, match="No blue material binding"):
        resolve_bindings({"blue_elements": [], "composition": "", "prompt": ""},
                         reference, lookup, "A cafe with no people and blue tiles")
    with pytest.raises(ValueError, match="insufficient blue"):
        material_anchor(_img("white"), [0, 0, 1, 1], "physical_blue")
    with pytest.raises(ValueError, match="Empty reference"):
        material_anchor(reference, [1, 0, 0, 1], "physical_blue")
    assert material_anchor(_img("white"), [0, 0, 1, 1], "neutral_style_fallback")["hex"] == "#FFFFFF"


@pytest.mark.parametrize("presence", ["human", "no_humans"])
@pytest.mark.parametrize("with_dimensions", [False, True])
@pytest.mark.parametrize("size", [(1216, 912), (2368, 1776)])
def test_reference_blue_pipeline_and_audit_keep_native_one_call_contract(
    tmp_path, lookup, presence, with_dimensions, size, monkeypatch,
):
    from dataclasses import replace

    from PIL import Image
    from test_pipeline import ROW, SIZE_QUOTE, Fake, _hero, _img

    import hp3p.pipeline as pipeline
    from hp3p.catalog import StyleRef
    from hp3p.pipeline import run_row
    from hp3p.reference_blue import VERSION, ReferenceBlue

    monkeypatch.setattr(
        pipeline,
        "assess_product_affine",
        lambda *args, **kwargs: {"guard_version": "test", "verdict": "pass", "reasons": []},
    )

    reference = StyleRef("tagged", "Cafe", "Warm", "Cafe", "image/png", _img("#357773"), presence)
    policy = ReferenceBlue([reference], lookup)

    class ReferenceFake(Fake):
        def chat_json(self, system, text, images, schema):
            if "human_policy" in schema["properties"]:
                self.calls.append(("select", len(images)))
                return {"reference_ids": ["tagged"], "human_policy": presence, "content": "Cafe",
                        "tone": "Warm", "brightness": "balanced", "rationale": "original request"}
            return super().chat_json(system, text, images, schema)

    fake = ReferenceFake()
    row = replace(ROW, user_prompt="A woman at a cafe table" if presence == "human" else "A cafe without people")
    if with_dimensions:
        row = replace(row, user_prompt=row.user_prompt + " " + SIZE_QUOTE)
    result = run_row(row, fake, [reference], tmp_path, _hero(),
                     captions={"tagged": {"summary": "OLD_CAPTION_SENTINEL"}},
                     ref_count=1, reference_blue=policy, size=size)
    assert result["status"] == "ok" and result["pipeline_version"] == VERSION
    assert result["human_policy"] == presence and not result["captioned"]
    assert fake.calls == [("select", 1), ("chat", 2), ("chat", 3), ("edit", 1, f"{size[0]}x{size[1]}", False)]
    people = ("Include only the requested people" if presence == "human" else
              "No people, hands, human silhouettes or human reflections.")
    assert people in result["prompt"] and "blue_elements" not in result
    assert "Exact blue material colors" not in result["prompt"] and "cool blue window" not in result["prompt"]
    assert "OLD_CAPTION_SENTINEL" not in fake.last_text and row.raw_prompt not in fake.last_text
    assert "FULL_HISTOGRAM_LOOKUP_INVENTORY_JSON" not in fake.last_text
    assert "everyday color name" in " ".join(fake.rewrite_request["system"].split())
    assert "REFERENCE-ANCHORED" not in fake.rewrite_request["system"]
    assert fake.rewrite_request["images"][1][1] == reference.data
    assert "reference" not in result["prompt"].lower() and "Image 2" not in result["prompt"]
    out = tmp_path / "rows" / row.id
    assert (out / "ours.png").read_bytes() == (out / "gpt_1.png").read_bytes() == fake.generated
    request = json.loads((out / "image_request.json").read_text())
    assert request["prompt"] == result["prompt"]
    assert Image.open(out / "ours.png").size == size
    planning = json.loads((out / "planning_request.json").read_text())
    assert "scale_plan" not in json.loads((out / "geometry_request.json").read_text())["schema"]["properties"]
    assert "blue_elements" not in planning["schema"]["properties"]
    if with_dimensions:
        assert "Explicit user-supplied product size" in planning["text"]
    assert not (out / "resolved_bindings.json").exists()
    assert run_row(row, fake, [reference], tmp_path, _hero(),
                   ref_count=1, reference_blue=policy, size=size) == result
    changed = ReferenceBlue([replace(reference, id="different")], lookup)
    with pytest.raises(ValueError, match="catalog or histogram changed"):
        run_row(row, fake, [reference], tmp_path, _hero(), ref_count=1, reference_blue=changed, size=size)
    with pytest.raises(ValueError, match="different user input.*fresh run"):
        run_row(replace(row, user_prompt=row.user_prompt + " Changed product dimensions: 40 x 40 x 34 cm."),
                fake, [reference], tmp_path, _hero(), ref_count=1, reference_blue=policy, size=size)
    cached = out / "result.json"
    previous = {**result, "pipeline_version": "unified-blue-v6-full-histogram-reference-carriers-scale"}
    cached.write_text(json.dumps(previous))
    with pytest.raises(ValueError, match="different rewriting policy.*fresh run"):
        run_row(row, fake, [reference], tmp_path, _hero(), ref_count=1, reference_blue=policy, size=size)
    assert json.loads(cached.read_text()) == previous
    assert len(fake.calls) == 4


def test_reference_blue_rejects_untagged_catalog_and_four_reference_mode(tmp_path, lookup):
    from test_pipeline import CAT, ROW, Fake, _hero

    from hp3p.pipeline import run_row
    from hp3p.reference_blue import ReferenceBlue

    with pytest.raises(ValueError, match="existing human/no_humans tags"):
        ReferenceBlue(CAT, lookup)
    from dataclasses import replace

    policy = ReferenceBlue([replace(CAT[0], human_presence="no_humans")], lookup)
    fake = Fake()
    result = run_row(ROW, fake, CAT, tmp_path, _hero(), reference_blue=policy)
    assert result["status"] == "error" and "exactly one" in result["error"] and not fake.calls
