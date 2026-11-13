import io
import re

import numpy as np
from PIL import Image


def lab(rgb):
    value = np.asarray(rgb, dtype=float) / 255
    linear = np.where(value > .04045, ((value + .055) / 1.055) ** 2.4, value / 12.92)
    matrix = np.array([[.4124, .3576, .1805], [.2126, .7152, .0722], [.0193, .1192, .9505]])
    xyz = linear @ matrix.T / np.array([.95047, 1, 1.08883])
    f = np.where(xyz > .008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], axis=-1)


def rgb(hex_code):
    return [int(hex_code[index:index + 2], 16) for index in (1, 3, 5)]


def photometry(body):
    image = Image.open(io.BytesIO(body)).convert("RGB")
    image.thumbnail((256, 256))
    light = lab(np.asarray(image))[..., 0]
    shadow = float((light < 30).mean())
    return {"mean_L": round(float(light.mean()), 3), "shadow_fraction": round(shadow, 5),
            "brightness_score": round(float(light.mean()) - 20 * shadow, 3)}


def select_reference(proposal, metadata, prompt):
    indexed = {entry["id"]: entry for entry in metadata}
    ranked = list(dict.fromkeys(proposal["reference_ids"]))
    if not ranked or any(identity not in indexed for identity in ranked):
        raise ValueError("Reference selector returned an unknown candidate")
    human_policy = proposal["human_policy"]
    if re.search(r"\b(?:no|without|avoid|exclude)\s+(?:(?:any|visible|a|an)\s+)*(?:people|humans?|persons?|hands?)\b"
                 r"|\b(?:unoccupied|human-free|people-free|nobody|no-one)\b", prompt, re.I):
        human_policy = "no_humans"
    if human_policy not in ("human", "no_humans"):
        raise ValueError("Invalid request human policy")
    eligible = [entry for entry in metadata if entry["human_presence"] == human_policy]
    if not eligible:
        raise ValueError("No reference candidates have the required human-presence tag")
    pool = [entry for entry in eligible if entry["content"] == proposal["content"]] or eligible
    brightness = proposal["brightness"]
    if re.search(r"\b(?:bright|airy|sunlit|well[- ]lit|light[- ]filled)\b", prompt, re.I):
        brightness = "bright"
    elif re.search(r"\b(?:dim(?:ly)?[- ]lit|low[- ]key|moody lighting|nighttime)\b", prompt, re.I):
        brightness = "dim"
    elif brightness == "dim":
        brightness = "balanced"
    threshold = None
    if brightness == "bright":
        threshold = float(np.quantile([entry["brightness_score"] for entry in pool], .75))
        pool = [entry for entry in pool if entry["brightness_score"] >= threshold]
    elif brightness == "dim":
        threshold = float(np.quantile([entry["brightness_score"] for entry in pool], .25))
        pool = [entry for entry in pool if entry["brightness_score"] <= threshold]
    allowed = {entry["id"] for entry in pool}
    selected = next((identity for identity in ranked if identity in allowed), None)
    fallback = selected is None
    if selected is None:
        target = (max(entry["brightness_score"] for entry in pool) if brightness == "bright" else
                  min(entry["brightness_score"] for entry in pool) if brightness == "dim" else
                  float(np.median([entry["brightness_score"] for entry in pool])))
        selected = min(pool, key=lambda entry: (abs(entry["brightness_score"] - target), entry["id"]))["id"]
    return {
        "reference_id": selected, "resolved_brightness": brightness,
        "human_policy": human_policy, "proposed_human_policy": proposal["human_policy"],
        "eligible_human_tag_count": len(eligible), "brightness_threshold": threshold,
        "eligible_after_brightness": len(pool), "photometric_fallback": fallback,
        "selected_metadata": indexed[selected],
    }


def material_anchor(body, region, kind):
    box = np.asarray(region, dtype=float)
    if box.shape != (4,) or not np.isfinite(box).all() or (box < 0).any() or (box > 1).any():
        raise ValueError("Invalid reference material region")
    left, top, right, bottom = box
    if left >= right or top >= bottom:
        raise ValueError("Empty reference material region")
    image = Image.open(io.BytesIO(body)).convert("RGB")
    width, height = image.size
    crop = image.crop((int(left * width), int(top * height), max(int(right * width), int(left * width) + 1),
                       max(int(bottom * height), int(top * height) + 1)))
    pixels = np.asarray(crop).reshape(-1, 3)
    if len(pixels) < 16:
        raise ValueError("Reference material region too small")
    hsv = np.asarray(crop.convert("HSV"), dtype=float).reshape(-1, 3) / 255
    if kind == "physical_blue":
        mask = ((hsv[:, 0] * 360 >= 160) & (hsv[:, 0] * 360 <= 280)
                & (hsv[:, 1] >= .08) & (hsv[:, 2] >= .06))
        pixels = pixels[mask]
        if len(pixels) < 16:
            raise ValueError("Reference physical-blue region has insufficient blue-family pixels")
    elif kind != "neutral_style_fallback":
        raise ValueError("Unknown reference anchor kind")
    pixels = pixels[::max(1, len(pixels) // 20000)]
    values = lab(pixels)
    low, high = np.quantile(values[:, 0], [.45, .85])
    middle = (values[:, 0] >= low) & (values[:, 0] <= high)
    pixels, values = pixels[middle], values[middle]
    nearest = np.argmin(np.sum((values - values.mean(axis=0)) ** 2, axis=1))
    color = pixels[nearest]
    return {
        "hex": "#" + "".join(f"{int(channel):02X}" for channel in color),
        "kind": kind, "reference_region": list(map(float, box)), "sampled_material_pixels": len(pixels),
        "method": "Observed pixel nearest midtone Lab mean; blue-family masking for physical-blue anchors",
        "calibrated_albedo": False,
    }


def resolve_bindings(response, reference, lookup, prompt):
    bindings = response["blue_elements"]
    if not bindings and not re.search(
        r"\b(?:no|without|avoid|exclude)\s+(?:any\s+)?blue\b|\bblue[- ]free\b"
        r"|\b(?:do not|don't)\s+(?:use|add|include)\s+(?:any\s+)?blue\b", prompt, re.I
    ):
        raise ValueError("No blue material binding without an explicit no-blue override")
    rewritten = dict(response)
    resolved, instances = [], set()
    for index, binding in enumerate(bindings):
        instance = binding["instance"].strip().casefold()
        if not instance or instance in instances:
            raise ValueError("Empty or duplicate blue material instance")
        instances.add(instance)
        token = f"__BLUE_{index}_HEX__"
        if token not in response["composition"] or token not in response["prompt"]:
            raise ValueError("Missing blue material placeholder in composition or image prompt")
        anchor = material_anchor(reference, binding["reference_region"], binding["anchor_kind"])
        color = lookup.nearest(anchor, binding["element"])
        for field in ("composition", "prompt"):
            rewritten[field] = rewritten[field].replace(token, color["hex"])
        resolved.append({**binding, **color})
    if any(re.search(r"__BLUE_\d+_HEX__", rewritten[field]) for field in ("composition", "prompt")):
        raise ValueError("Unresolved blue material placeholder")
    rewritten["blue_elements"] = resolved
    return rewritten, resolved
