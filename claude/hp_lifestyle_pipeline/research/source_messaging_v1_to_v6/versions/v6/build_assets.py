#!/usr/bin/env python3
"""Compile V6 contract assets and qualitative profiles from the pinned V5 sources.

Never reads or grants prop approvals. V5 files are read-only provenance.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
V5 = ROOT.parent / "v5"
ENVIRONMENTS = ["Home", "Office", "Education", "Gaming", "Café", "Creative Studio"]


def obj(properties):
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}


def array(items):
    return {"type": "array", "items": items}


def enum(values):
    return {"type": "string", "enum": values}


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    text = {"type": "string"}
    component = obj({
        key: {"type": "integer", "enum": [0, 10, 20, 30] if key in ("setting", "activity") else [0, 5, 10, 15, 20]}
        for key in ("setting", "activity", "materials", "use_context")
    })
    prompt = obj({
        "environment": enum(ENVIRONMENTS), "text": text,
        "prop_ids": array(text),
        "score_components": obj({"smart_brief": component, "source_messaging": component}),
        "evidence": array(obj({"document": enum(["smart_brief", "source_messaging"]), "path": text, "quote": text})),
        "relationship": enum(["source_grounded", "source_adjacent", "creative_departure"]),
        "explanation": text, "creative_departures": array(text),
        "ctech_reference_id": enum([f"CT{i:02d}" for i in range(1, 19)]),
        "ctech_reference_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "ctech_explanation": text, "camera_fit_explanation": text,
    })
    write("model_output.schema.json", obj({
        "prompts": {**array(prompt), "minItems": 10, "maxItems": 10},
        "debug": obj({"source_conflicts": array(text), "limitations": array(text), "environment_rationale": text}),
    }))
    write("input.schema.json", obj({
        "smart_brief": {"type": ["string", "object"]},
        "source_messaging": {"type": ["string", "object"]},
        "camera_tag": text,
    }))
    framing = {
        "tight": "Keep a recognizable setting, support surface and natural light. Use approved nearby details only where plausible in this close view; partial objects or subordinate background cues may suffice. Do not require a full room, multiple work areas or a spread of props that would need a wider view. No automatic zero-prop or zero-background rule applies.",
        "medium": "Describe a coherent local working or living area with casually arranged approved materials and subordinate furnishings. Keep detail at C-Tech's ordinary room-description level. Avoid several distant activity areas or competing focal arrangements that would need a wider view.",
        "wide": "Retain the richer C-Tech room descriptions and natural depth, using approved and unrepeated furnishings. A wall carrying shelving and artwork can be one coherent arrangement; there is no numeric object or zone quota. Do not require the whole building or several disconnected focal areas.",
        "unknown": "This preset has insufficient interpreted view notes. Do not infer usable space from its name; return an unsupported-camera error for deployment until reviewed offline.",
    }
    elevation = {
        "level": "Do not assume a large exposed tabletop. Nearby background details may fit even when little tabletop is visible.",
        "low": "Respect the limited exposed tabletop. Avoid arrangements that require seeing the top of every object or changing elevation.",
        "high": "Favor local horizontal surfaces and low-profile objects. Do not demand full-height fixtures or people outside the view.",
        "top_oblique": "Keep the scene on the visible horizontal surface; do not demand a horizon, visible windows, walls, or full-height room furnishings.",
        "oblique": "Keep depth and the angle of the fixed view; do not ask to rotate the view or reposition the primary subject to fit scene details.",
    }
    original = json.loads((V5 / "camera_profiles.json").read_text())
    profiles = []
    for p in original["profiles"]:
        profile = {k: p[k] for k in ("tag", "source_camera_name", "device_family", "framing", "elevation", "people_policy")}
        profile["guidance"] = [framing.get(p["framing"], framing["unknown"]), elevation.get(p["elevation"], "Use only the recorded view; do not infer an angle.")]
        profiles.append(profile)
    write("camera_profiles.json", {
        "version": "camera-v6-qualitative-2026-10-28-v1", "runtime_image_analysis": False,
        "source_registry_sha256": hashlib.sha256((V5 / "camera_profiles.json").read_bytes()).hexdigest(),
        "limitations": "Framing/elevation inherited from offline V2 review; qualitative density guidance is a design hypothesis, not measured image capacity or a new analysis of the latest renders.",
        "aliases": original["aliases"], "profiles": profiles,
    })
    write("reference_library.json", json.loads((V5 / "reference_library.json").read_text()))
    print(json.dumps({"prompt_count": 10, "camera_profiles": len(profiles), "numeric_camera_caps": False}))


if __name__ == "__main__":
    main()
