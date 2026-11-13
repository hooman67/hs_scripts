import io
import json
from dataclasses import replace

import numpy as np
import pytest
from PIL import Image

from hp3p import grade
from hp3p.catalog import StyleRef
from hp3p.grade import lab_stats, match_grade


def _png(img, fmt="PNG"):
    buf = io.BytesIO()
    img.save(buf, fmt)
    return buf.getvalue()


def _ramp(tint):
    """Horizontal dark-to-light ramp; `tint` RGB offset applied to the darker half (shadows)."""
    x = np.linspace(20, 235, 256)
    rgb = np.repeat(np.repeat(x[None, :, None], 3, 2), 192, 0)
    rgb[:, :128] += tint
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def test_match_grade_moves_scene_toward_ref_tint_and_protects_product():
    ours = _ramp((10, 6, -10))  # warm/yellow shadows
    refs = [_png(_ramp((-8, 0, 14)))] * 2  # cool blue shadows
    mask = Image.new("RGBA", ours.size, (0, 0, 0, 0))
    mask.paste((0, 0, 0, 255), (0, 0, 32, 32))  # protected product in the top-left corner
    out = Image.open(io.BytesIO(match_grade(_png(ours), refs, _png(mask), strength=1.0)))
    before, after, ref = lab_stats(_png(ours)), lab_stats(_png(out)), lab_stats(refs[0])
    assert abs(after["sh_b"] - ref["sh_b"]) < 0.5 * abs(before["sh_b"] - ref["sh_b"])
    assert np.abs(np.asarray(out, int)[:16, :16] - np.asarray(ours, int)[:16, :16]).max() <= 2


def test_global_reference_grade_matches_tint_and_lightness_contrast():
    from hp3p.grade import match_reference

    x = np.tile(np.linspace(30, 220, 256), (192, 1))
    source = _png(Image.fromarray(np.stack([x + 8, x + 2, x - 6], -1).astype(np.uint8)))
    x = np.tile(np.linspace(100, 155, 256), (192, 1))
    reference = _png(Image.fromarray(np.stack([x - 4, x + 1, x + 8], -1).astype(np.uint8)))
    output, metadata = match_reference(source, reference)
    after, target = lab_stats(output), lab_stats(reference)
    for channel in ("L", "L_std", "a", "b"):
        assert abs(after[channel] - target[channel]) < 1.0, channel
    assert after["L_std"] < 0.5 * lab_stats(source)["L_std"]
    assert Image.open(io.BytesIO(output)).size == (256, 192)
    assert metadata["scope"] == "whole_image" and not metadata["product_colors_preserved"]


@pytest.mark.parametrize("flat_source", [True, False])
def test_global_reference_grade_rejects_flat_images_instead_of_faking_contrast(flat_source):
    from hp3p.grade import match_reference

    flat = _png(Image.new("RGB", (64, 48), (100, 100, 100)))
    ramp = _png(_ramp((0, 0, 0)))
    with pytest.raises(ValueError, match="tonal variation"):
        match_reference(flat if flat_source else ramp, ramp if flat_source else flat)


def test_nearest_reference_searches_whole_catalog_not_original_style_bucket(tmp_path):
    source = _png(_ramp((0, 0, 0)))
    dark = _png(Image.eval(_ramp((0, 0, 0)), lambda v: v // 3))
    catalog = [StyleRef("original", "dark", "Dark", "Office", "image/png", dark),
               StyleRef("closest", "bright", "Bright", "Home", "image/png", source)]
    index = grade.reference_statistics(catalog, tmp_path / "stats.json")
    chosen, selection = grade.nearest_reference(source, catalog, index)
    assert chosen.id == "closest"
    assert selection["distance"] == pytest.approx(0)
    assert selection["candidate_count"] == 2
    assert all(np.isfinite(v) and v > 0 for v in selection["scales"].values())


def test_reference_statistics_reuses_cache_and_invalidates_changed_image_bytes(tmp_path, monkeypatch):
    reference = StyleRef("ref", "n", "Warm", "Cafe", "image/png", _png(_ramp((0, 0, 0))))
    cache = tmp_path / "stats.json"
    first = grade.reference_statistics([reference], cache)
    with monkeypatch.context() as patch:
        def must_not_recompute(data):
            pytest.fail("A valid image-statistics cache must not decode the reference again.")
        patch.setattr(grade, "lab_stats", must_not_recompute)
        assert grade.reference_statistics([reference], cache) == first
    changed = replace(reference, data=_png(Image.eval(_ramp((0, 0, 0)), lambda v: v // 3)))
    second = grade.reference_statistics([changed], cache)
    assert second["entries"][0]["sha256"] != first["entries"][0]["sha256"]
    assert second["entries"][0]["stats"]["L"] < first["entries"][0]["stats"]["L"] - 20
    assert json.loads(cache.read_text()) == second


def test_nearest_reference_breaks_equal_distance_ties_by_id(tmp_path):
    source = _png(_ramp((0, 0, 0)))
    catalog = [StyleRef(i, "n", "Warm", "Cafe", "image/png", source) for i in ("z", "a")]
    index = grade.reference_statistics(catalog, tmp_path / "stats.json")
    assert grade.nearest_reference(source, catalog, index)[0].id == "a"
    assert grade.nearest_reference(source, catalog[::-1], index)[0].id == "a"


@pytest.mark.parametrize("bad_value", [float("nan"), float("inf")])
def test_nearest_reference_rejects_nonfinite_cached_statistics(tmp_path, bad_value):
    source = _png(_ramp((0, 0, 0)))
    catalog = [StyleRef("r", "n", "Warm", "Cafe", "image/png", source)]
    index = grade.reference_statistics(catalog, tmp_path / "stats.json")
    index["entries"][0]["stats"]["L"] = bad_value
    with pytest.raises(ValueError, match="finite"):
        grade.nearest_reference(source, catalog, index)


def test_nearest_reference_rejects_empty_or_stale_catalog(tmp_path):
    source = _png(_ramp((0, 0, 0)))
    catalog = [StyleRef("r", "n", "Warm", "Cafe", "image/png", source)]
    with pytest.raises(ValueError, match="empty"):
        grade.reference_statistics([], tmp_path / "empty.json")
    index = grade.reference_statistics(catalog, tmp_path / "stats.json")
    changed = [replace(catalog[0], data=_png(_ramp((0, 0, 10))))]
    with pytest.raises(ValueError, match="catalog"):
        grade.nearest_reference(source, changed, index)
