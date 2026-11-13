import io
import json

from PIL import Image

from hp3p.captions import caption_catalog, format_caption, palette
from hp3p.catalog import StyleRef


def _webp(color_split):
    img = Image.new("RGB", (100, 100), (16, 63, 178))
    img.paste((240, 240, 235), (0, 0, color_split, 100))
    buf = io.BytesIO()
    img.save(buf, "WEBP", lossless=True)
    return buf.getvalue()


def test_palette_measures_hex_and_share():
    pal = palette(_webp(75))
    assert pal[0]["share"] > pal[1]["share"]
    assert {p["hex"] for p in pal[:2]} == {"#f0f0eb", "#103fb2"}
    assert abs(sum(p["share"] for p in pal) - 1) < 0.01


class Fake:
    def __init__(self):
        self.texts = []

    def chat_json(self, system, text, images, schema):
        self.texts.append(text)
        return {"summary": "blue sofa cafe"}


def test_caption_catalog_passes_palette_and_skips_done(tmp_path):
    cat = [StyleRef(f"s{i}", "n", "Cool", "Cafe", "image/webp", _webp(50)) for i in range(3)]
    out = tmp_path / "caps.json"
    out.write_text(json.dumps({"s0": {"summary": "done", "palette": []}}))
    fake = Fake()
    caps = caption_catalog(cat, fake, out, workers=2)
    assert len(fake.texts) == 2 and "#103fb2" in fake.texts[0]
    assert caps["s0"]["summary"] == "done" and caps["s2"]["summary"] == "blue sofa cafe"
    assert caps["s1"]["palette"][0]["hex"] in {"#103fb2", "#f0f0eb"}
    assert json.loads(out.read_text()).keys() == {"s0", "s1", "s2"}


def test_format_caption_includes_measured_hex():
    text = format_caption(2, {"summary": "cafe", "palette": [{"hex": "#103fb2", "share": 0.4}]})
    assert text.startswith("Image 2:") and "#103fb2 40%" in text


def test_blue_share_counts_rich_blue_not_gray_blue():
    from hp3p.captions import blue_share

    img = Image.new("RGB", (100, 100), (240, 240, 235))
    img.paste((16, 63, 178), (0, 0, 40, 100))  # Electric Blue, 40%
    img.paste((120, 130, 140), (40, 0, 70, 100))  # gray-blue, not counted
    buf = io.BytesIO()
    img.save(buf, "PNG")
    assert abs(blue_share(buf.getvalue()) - 0.40) < 0.02
