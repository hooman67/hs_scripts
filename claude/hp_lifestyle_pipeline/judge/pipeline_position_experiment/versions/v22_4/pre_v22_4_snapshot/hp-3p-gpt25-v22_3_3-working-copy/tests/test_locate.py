import io

import numpy as np
from PIL import Image

from hp3p.locate import locate


def _png(img):
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def _product(w, h):
    p = Image.new("RGB", (w, h), (40, 40, 45))
    p.paste((200, 30, 30), (w // 5, h // 4, w // 2, h // 2))
    p.paste((30, 160, 220), (w // 2, h // 2, 4 * w // 5, 3 * h // 4))
    return p


def test_locate_finds_moved_and_scaled_product():
    hero = Image.new("RGB", (800, 600), "white")
    hero.paste(_product(160, 100), (500, 200))
    rng = np.random.RandomState(0)
    out = Image.fromarray(rng.randint(90, 170, (600, 800, 3)).astype(np.uint8))
    out.paste(_product(208, 130), (420, 300))  # moved and 1.3x larger
    mask_png, info = locate(_png(hero), _png(out))
    alpha = np.asarray(Image.open(io.BytesIO(mask_png)).getchannel("A")) > 0
    ys, xs = np.where(alpha)
    assert info["score"] > 0.8 and abs(info["scale"] - 1.3) < 0.1 and info["confident"]
    assert abs(xs.min() - 420) < 12 and abs(ys.min() - 300) < 12
    assert abs(xs.max() - 628) < 12 and abs(ys.max() - 430) < 12


def test_locate_handles_product_filling_the_frame():
    hero = Image.new("RGB", (200, 150), "white")
    hero.paste(_product(190, 140), (5, 5))
    _, info = locate(_png(hero), _png(hero))
    assert info["score"] > 0.8 and abs(info["scale"] - 1) < 0.06 and abs(info["dx"]) <= 8 and abs(info["dy"]) <= 8
