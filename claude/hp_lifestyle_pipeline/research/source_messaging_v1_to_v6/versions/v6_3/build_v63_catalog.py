#!/usr/bin/env python3
"""Derive V6.3 assets from frozen V6.2 and explicit new approval decisions."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "v6_2"
OUT = HERE / "approved-v6.3-20261109.catalog.json"
VERSION = "hp-v6.3-approved-props-v1"
REVISION = "v6.3-hp-associations-20261109-r1"
sys.path.insert(0, str(HERE.parent))
from v6_3.catalog import compile_catalog, validate_catalog


LEXICON_ADDITIONS = {
    "laptop_bag": ("bag", "bags", "backpacks", "shoulder bag", "shoulder bags"),
    "drinkware": ("ceramic cup", "ceramic cups", "pottery cup", "pottery cups"),
    "food_bowl": ("ceramic bowl", "ceramic bowls", "pottery bowl", "pottery bowls"),
    "food_plate": ("ceramic plate", "ceramic plates", "pottery plate", "pottery plates"),
    "clock": (
        "clock", "clocks", "analog clock", "analog clocks",
        "wall clock", "wall clocks", "desk clock", "desk clocks",
    ),
    # Recognition is not approval: retain these phrases to catch undeclared props.
    "stone_object": ("rock", "rocks", "pebble", "pebbles", "river rock", "river rocks"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derive_lexicon() -> dict:
    value = json.loads((BASE / "prop_lexicon.json").read_text(encoding="utf-8"))
    value["version"] = VERSION
    phrases = {item["phrase"]: item["groups"] for item in value["entries"]}
    for group, additions in LEXICON_ADDITIONS.items():
        for phrase in additions:
            if phrase in phrases and phrases[phrase] != [group]:
                raise ValueError(f"conflicting lexicon groups for {phrase!r}")
            phrases[phrase] = [group]
    value["entries"] = [
        {"phrase": phrase, "groups": groups}
        for phrase, groups in sorted(phrases.items())
    ]
    return value


def derive_catalog() -> dict:
    base_path = BASE / "approved-v6.2-20261106.catalog.json"
    value = json.loads(base_path.read_text(encoding="utf-8"))
    additions = compile_catalog(HERE / "approved_additions.csv", REVISION)
    removed = {
        entry["id"] for entry in value["entries"]
        if {"paperweight", "stone_object"}.intersection(entry["repetition_groups"])
    }
    if removed != {"V61-OFF-014"}:
        raise ValueError(f"unexpected V6.2 paperweight inventory: {sorted(removed)}")
    value.update(
        version=VERSION,
        revision=REVISION,
        source_sha256=sha256(base_path),
        entries=[
            entry for entry in value["entries"] if entry["id"] not in removed
        ] + additions["entries"],
    )
    return validate_catalog(value)


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> None:
    baseline = json.loads((HERE / "baseline_manifest.json").read_text(encoding="utf-8"))
    for name, expected in baseline["files"].items():
        if sha256(BASE / name) != expected:
            raise ValueError(f"frozen V6.2 source changed: {name}")
    write_json(HERE / "prop_lexicon.json", derive_lexicon())
    catalog = derive_catalog()
    write_json(OUT, catalog)
    assets = sorted([
        *HERE.glob("*.py"), *HERE.glob("*.json"), HERE / "system_prompt.md",
        HERE / "approved_additions.csv",
    ])
    write_json(HERE / "assets_manifest.json", {
        "version": REVISION,
        "baseline": baseline,
        "files": {
            path.name: sha256(path) for path in assets
            if path.name != "assets_manifest.json"
        },
    })
    print(json.dumps({
        "output": str(OUT), "entries": len(catalog["entries"]),
        "version": VERSION, "revision": REVISION,
    }, indent=2))


if __name__ == "__main__":
    main()
