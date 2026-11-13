import io

import numpy as np
from PIL import Image, ImageFilter

WHITE_THRESHOLD = 245
MARGIN = 0.05


def _png(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def _product(img: Image.Image) -> np.ndarray:
    return np.asarray(img).min(axis=-1) < WHITE_THRESHOLD


def _zoom_box(img: Image.Image, fill: float) -> tuple[int, int, int, int]:
    """Same-aspect crop where the product box covers ~`fill` of the frame (never zooms out).

    Zooms about the product center so its relative position is kept, then shifts to keep the
    whole product inside with a margin.
    """
    W, H = img.size
    ys, xs = np.where(_product(img))
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    s = min(1.0, ((x1 - x0) * (y1 - y0) / (fill * W * H)) ** 0.5)
    s = min(1.0, max(s, (x1 - x0) / (W * (1 - 2 * MARGIN)), (y1 - y0) / (H * (1 - 2 * MARGIN))))
    cw, ch = W * s, H * s
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    left, top = cx - cw * cx / W, cy - ch * cy / H
    left = min(max(left, x1 + MARGIN * cw - cw), x0 - MARGIN * cw)
    top = min(max(top, y1 + MARGIN * ch - ch), y0 - MARGIN * ch)
    left, top = min(max(left, 0), W - cw), min(max(top, 0), H - ch)
    return round(left), round(top), round(left + cw), round(top + ch)


def prepare(hero_png: bytes, size: tuple[int, int], fill: float | None = None) -> tuple[bytes, bytes]:
    """Resize (optionally zoom to a medium close-up) the product-on-white hero and build an edit mask.

    Opaque pixels protect the product interior; its boundary and white background remain editable.
    Isolated protected pixels are removed before deriving product bounds/contact.
    """
    hero = Image.open(io.BytesIO(hero_png)).convert("RGB")
    if fill:
        hero = hero.crop(_zoom_box(hero, fill))
    hero = hero.resize(size, Image.LANCZOS)
    keep = Image.fromarray((_product(hero) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3))
    pixels = np.asarray(keep) > 0
    h, w = pixels.shape
    padded = np.pad(pixels, 1)
    neighbors = np.zeros_like(pixels)
    for dy, dx in ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                   (0, 1), (1, -1), (1, 0), (1, 1)):
        neighbors |= padded[1 + dy:1 + dy + h, 1 + dx:1 + dx + w]
    keep = Image.fromarray((pixels & neighbors).astype(np.uint8) * 255)
    mask = Image.new("RGBA", size, (0, 0, 0, 0))
    mask.putalpha(keep)
    return _png(hero), _png(mask)
