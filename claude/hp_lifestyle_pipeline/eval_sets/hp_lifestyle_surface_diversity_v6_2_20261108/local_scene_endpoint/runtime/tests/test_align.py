import io

import numpy as np
from PIL import Image

from hp3p.align import align, product_alpha
from hp3p.locate import locate


def _png(img):
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def _hero(size=(608, 456)):
    img = Image.new("RGB", size, "white")
    img.paste((20, 20, 30), (250, 200, 370, 290))
    img.paste((200, 40, 40), (270, 215, 320, 245))
    img.paste((250, 250, 250), (330, 250, 350, 270))  # near-white detail inside the product
    return img


def _scene(hero, scale, dx, dy):
    """Textured scene with the hero product pasted at a drifted scale/offset."""
    rng = np.random.default_rng(0)
    w, h = hero.size
    yy, xx = np.mgrid[0:h, 0:w]
    bg = np.stack([60 + 0.2 * xx, 90 + 0.15 * yy, 140 + 0.1 * (xx + yy) % 60], -1) + rng.normal(0, 3, (h, w, 3))
    scene = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8))
    ys, xs = np.where(np.asarray(hero).min(-1) < 245)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    prod = hero.crop(box).resize((round(120 * scale), round(90 * scale)), Image.LANCZOS)
    scene.paste(prod, (box[0] + dx, box[1] + dy))
    return scene


def test_product_alpha_fills_interior_highlights():
    a = np.asarray(Image.open(io.BytesIO(product_alpha(_png(_hero())))))
    assert a[260, 340] == 255 and a[10, 10] == 0


def test_align_restores_exact_hero_size_and_position():
    hero = _hero()
    out = _scene(hero, 0.8, 40, -30)
    aligned, info = align(_png(hero), _png(out), {"scale": 0.8, "dx": 38, "dy": -28, "confident": True})
    a = np.asarray(Image.open(io.BytesIO(aligned)).convert("RGB")).astype(int)
    h = np.asarray(hero).astype(int)
    assert np.abs(a[206:284, 256:364] - h[206:284, 256:364]).max() == 0  # exact hero pixels
    assert abs(info["scale"] - 0.8) < 0.02 and abs(info["upscale"] - 1.25) < 0.03
    assert (info["gpt_x"], info["gpt_y"]) == (290, 170) and info["uncovered"] == 0.0


def test_align_reports_uncovered_border_when_zooming_out():
    hero = _hero()
    out = _scene(hero, 1.2, 0, 0)
    _, info = align(_png(hero), _png(out), {"scale": 1.2, "dx": 0, "dy": 0, "confident": True})
    assert info["uncovered"] > 0.05


def test_align_fill_is_tone_matched_to_avoid_seams():
    hero = _hero()
    out = _scene(hero, 1.3, 0, 0)

    def tinted_fill(img_png, mask_png):  # GPT's fill regenerates the frame with a global tone shift
        a = np.asarray(Image.open(io.BytesIO(img_png)).convert("RGB")).astype(int) + 35
        return _png(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))

    aligned, info = align(_png(hero), _png(out), {"scale": 1.3, "dx": 0, "dy": 0, "confident": True}, fill=tinted_fill)
    a = np.asarray(Image.open(io.BytesIO(aligned)).convert("RGB")).astype(float)
    base = np.asarray(Image.open(io.BytesIO(align(_png(hero), _png(out), {"scale": 1.3, "dx": 0, "dy": 0,
                                                                            "confident": True})[0])).convert("RGB"))
    assert info["filled"] and abs((a[:, :20] - base[:, :20]).mean()) < 6  # the +35 tint was removed


def test_align_realigns_the_fill_frame_instead_of_blending():
    hero = _hero()
    out = _scene(hero, 1.3, 0, 0)
    _, info = align(_png(hero), _png(out), {"scale": 1.3, "dx": 0, "dy": 0, "confident": True},
                    fill=lambda img, m: img)
    assert info["fill_mode"] == "full"

    def drifting_fill(img_png, mask_png):  # GPT re-composed the frame and moved the product while filling
        return _png(_scene(hero, 0.8, 50, 30))

    aligned, info = align(_png(hero), _png(out), {"scale": 1.3, "dx": 0, "dy": 0, "confident": True},
                          fill=drifting_fill)
    a = np.asarray(Image.open(io.BytesIO(aligned)).convert("RGB")).astype(int)
    _, floc = locate(_png(hero), drifting_fill(None, None))
    expect = np.asarray(Image.open(io.BytesIO(align(_png(hero), drifting_fill(None, None), floc)[0])))
    corr = np.corrcoef(a.reshape(-1), expect.astype(int).reshape(-1))[0, 1]  # fill frame is tone-matched first
    assert info["fill_mode"] == "realigned" and corr > 0.98


def test_align_crops_final_window_from_wider_generation():
    hero = _hero()  # 608x456 final frame
    canvas = Image.new("RGB", (768, 576), "white")
    canvas.paste(hero, (80, 60))
    out = _scene(canvas, 0.9, 30, -20)  # GPT drifted inside the margin
    loc = {"scale": 0.9, "dx": 30, "dy": -20, "confident": True}
    aligned, info = align(_png(canvas), _png(out), loc, window=(80, 60, 608, 456))
    a = np.asarray(Image.open(io.BytesIO(aligned)).convert("RGB")).astype(int)
    assert a.shape == (456, 608, 3) and info["uncovered"] == 0.0
    assert np.abs(a[206:284, 256:364] - np.asarray(hero).astype(int)[206:284, 256:364]).max() == 0
