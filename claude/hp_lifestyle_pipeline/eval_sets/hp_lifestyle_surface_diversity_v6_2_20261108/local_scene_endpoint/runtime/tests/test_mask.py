import io

import numpy as np
from PIL import Image

from hp3p.mask import prepare


def _png(img):
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def test_prepare_resizes_and_protects_product_only():
    hero = Image.new("RGB", (400, 300), "white")
    hero.paste((20, 20, 40), (100, 100, 200, 160))
    image, mask = prepare(_png(hero), (800, 600))
    im, m = Image.open(io.BytesIO(image)), Image.open(io.BytesIO(mask))
    assert im.size == m.size == (800, 600) and m.mode == "RGBA"
    alpha = np.asarray(m)[..., 3]
    assert alpha[260, 300] == 255  # product interior is preserved
    assert alpha[20, 20] == 0  # white background is editable
    assert 0.04 < (alpha == 255).mean() < 0.08


def test_prepare_leaves_white_rim_and_product_boundary_editable():
    hero = Image.new("RGB", (100, 80), "white")
    hero.paste((20, 20, 40), (30, 20, 70, 60))
    image, mask = prepare(_png(hero), hero.size)
    rgb = np.asarray(Image.open(io.BytesIO(image)).convert("RGB"))
    alpha = np.asarray(Image.open(io.BytesIO(mask)).getchannel("A"))
    assert not alpha[rgb.min(-1) >= 245].any()
    assert alpha[40, 30] == 0
    assert alpha[40, 40] == 255


def test_prepare_removes_isolated_corner_alpha_without_changing_rgb():
    hero = Image.new("RGB", (100, 80), "white")
    hero.paste((20, 20, 40), (30, 20, 70, 60))
    hero.paste((240, 240, 240), (0, 78, 2, 80))
    image, mask = prepare(_png(hero), hero.size)
    assert Image.open(io.BytesIO(image)).tobytes() == hero.tobytes()
    alpha = np.asarray(Image.open(io.BytesIO(mask)).getchannel("A"))
    assert alpha[79, 0] == 0 and alpha[40, 40] == 255
    ys, xs = np.where(alpha)
    assert (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1) == (31, 21, 69, 59)


def test_prepare_fill_zooms_to_medium_close_up_without_cutting_product():
    hero = Image.new("RGB", (400, 300), "white")
    hero.paste((20, 20, 40), (280, 130, 380, 190))  # 100x60 box near the right edge, 5% of frame
    image, mask = prepare(_png(hero), (800, 600), fill=0.30)
    alpha = np.asarray(Image.open(io.BytesIO(mask)))[..., 3] == 255
    ys, xs = np.where(alpha)
    box = (np.ptp(xs) + 1) * (np.ptp(ys) + 1) / alpha.size
    assert 0.27 < box < 0.36
    assert xs.min() > 0.03 * 800 and xs.max() < 0.97 * 800  # fully in frame with a margin
    assert Image.open(io.BytesIO(image)).size == (800, 600)
