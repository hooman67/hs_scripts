import io
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image

from .openai_client import load_prompt

CAPTIONS = Path(__file__).parent / "data" / "ref_captions.json"

_S = {"type": "string"}
_B = {"type": "boolean"}
SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["summary", "setting", "shot_size", "palette_roles", "blue_elements", "primary_blue_carrier",
                 "blue_quality", "prominent_blue", "white_balance", "grade", "lighting", "subject_lighting",
                 "background_falloff", "lived_in_cues", "materials", "props", "camera", "mood", "brand_flags"],
    "properties": {
        "summary": _S,
        "setting": _S,
        "palette_roles": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["hex", "role"],
            "properties": {"hex": _S, "role": _S}}},
        "blue_elements": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["element", "hex", "extent", "placement"],
            "properties": {"element": _S, "hex": _S, "placement": _S,
                           "extent": {"type": "string", "enum": ["large", "medium", "small"]}}}},
        "shot_size": {"type": "string", "enum": ["close-up", "medium close-up", "medium", "wide"]},
        "primary_blue_carrier": {"type": "string", "enum": ["architecture/interior", "furniture/materials",
                                                             "sky/outdoor", "wardrobe", "props", "none"]},
        "blue_quality": {"type": "string", "enum": ["rich", "dusty/gray-blue", "none"]},
        "subject_lighting": {"type": "string", "enum": ["front", "front-quarter", "side", "back"]},
        "background_falloff": _S,
        "lived_in_cues": _S,
        "prominent_blue": _B,
        "white_balance": {"type": "string", "enum": ["cool", "neutral", "warm"]},
        "grade": _S,
        "lighting": _S,
        "materials": {"type": "array", "items": _S},
        "props": {"type": "array", "items": _S},
        "camera": _S,
        "mood": _S,
        "brand_flags": {"type": "object", "additionalProperties": False,
                        "required": ["people", "harsh_light", "vintage_or_orange", "oversaturated", "text_or_logos"],
                        "properties": {k: _B for k in
                                       ["people", "harsh_light", "vintage_or_orange", "oversaturated",
                                        "text_or_logos"]}},
    },
}


def palette(data: bytes, k: int = 6) -> list[dict]:
    """Dominant colors measured from pixels: exact hex and share of frame, largest first."""
    img = Image.open(io.BytesIO(data)).convert("RGB")
    img.thumbnail((256, 256))
    q = img.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal, total = q.getpalette(), img.width * img.height
    out = [{"hex": "#%02x%02x%02x" % tuple(pal[3 * i:3 * i + 3]), "share": round(n / total, 3)}
           for n, i in sorted(q.getcolors(), reverse=True)]
    return out


def blue_share(data: bytes) -> float:
    """Fraction of pixels that are saturated blue/teal (hue 185-250 deg); gray-blue is excluded."""
    img = Image.open(io.BytesIO(data)).convert("RGB")
    img.thumbnail((256, 256))
    h, s, v = np.moveaxis(np.asarray(img.convert("HSV"), dtype=float) / 255, -1, 0)
    return round(float(((h * 360 >= 185) & (h * 360 <= 250) & (s > 0.35) & (v > 0.2)).mean()), 3)


def format_caption(index: int, cap: dict) -> str:
    pal = ", ".join(f"{p['hex']} {round(p['share'] * 100)}%" for p in cap.get("palette", []))
    parts = [f"Image {index}: {cap['summary']}", f"measured palette: {pal}" if pal else "",
             f"measured rich-blue area: {cap['blue_share']:.0%}" if "blue_share" in cap else ""]
    skip = ("summary", "palette", "blue_share")
    parts += [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in cap.items() if k not in skip]
    return "\n  ".join(p for p in parts if p)


def caption_catalog(catalog, client, out: Path = CAPTIONS, workers: int = 6) -> dict:
    """Caption every style ref once; resumable (existing ids are kept), saved after each caption."""
    out = Path(out)
    caps = json.loads(out.read_text()) if out.exists() else {}
    todo = [r for r in catalog if r.id not in caps]
    lock, system = threading.Lock(), load_prompt("caption")

    def one(ref):
        pal, blue = palette(ref.data), blue_share(ref.data)
        text = ("Measured dominant palette: " + ", ".join(f"{p['hex']} ({p['share']:.0%})" for p in pal)
                + f"\nMeasured saturated blue area: {blue:.0%} of the frame")
        try:
            cap = client.chat_json(system, text, [(ref.mime, ref.data)], SCHEMA)
        except Exception as e:  # leave uncaptioned; a rerun picks it up
            print(ref.id, "error", f"{type(e).__name__}: {e}"[:200], flush=True)
            return
        with lock:
            caps[ref.id] = {**cap, "palette": pal, "blue_share": blue}
            out.parent.mkdir(parents=True, exist_ok=True)
            tmp = out.with_suffix(".tmp")
            tmp.write_text(json.dumps(caps, indent=1, sort_keys=True))
            tmp.replace(out)

    with ThreadPoolExecutor(workers) as pool:
        list(pool.map(one, todo))
    return caps
