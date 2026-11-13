from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from research.source_messaging_v1_to_v6.versions.v6_3.catalog import validate_catalog
from research.source_messaging_v1_to_v6.versions.v6_3.build_v63_catalog import (
    derive_catalog,
    derive_lexicon,
)


HERE = Path(__file__).resolve().parents[1]
CATALOG = HERE / "approved-v6.3-20261109.catalog.json"


def test_compiled_v63_catalog_is_valid_and_tightened() -> None:
    value = json.loads(CATALOG.read_text())
    validated = validate_catalog(value)
    assert validated["version"] == "hp-v6.3-approved-props-v1"
    assert len(validated["entries"]) == 265
    groups = {group for entry in validated["entries"] for group in entry["repetition_groups"]}
    assert {"paper_materials", "writing_tools", "wall_texture", "wall_slats"} <= groups


def test_catalog_rejects_v6_identity() -> None:
    value = json.loads(CATALOG.read_text())
    value["version"] = "hp-v6-approved-props-v1"
    with pytest.raises(ValueError, match="unsupported catalog version"):
        validate_catalog(value)


def test_composite_tool_cup_reserves_writing_tools() -> None:
    value = json.loads(CATALOG.read_text())
    cups = [entry for entry in value["entries"] if "tool_cup" in entry["repetition_groups"]]
    assert cups
    assert all("writing_tools" in entry["repetition_groups"] for entry in cups)


def test_catalog_rejects_unreviewed_fields() -> None:
    value = json.loads(CATALOG.read_text())
    value = copy.deepcopy(value)
    value["entries"][0]["invented"] = True
    with pytest.raises(ValueError, match="unreviewed fields"):
        validate_catalog(value)


def test_derivation_preserves_retained_v62_entries_and_explicit_approval_scope() -> None:
    base = json.loads(
        (HERE.parent / "v6_2" / "approved-v6.2-20261106.catalog.json").read_text()
    )
    current = json.loads(CATALOG.read_text())
    retained = [entry for entry in current["entries"] if not entry["id"].startswith("V63-")]
    assert retained == [entry for entry in base["entries"] if entry["id"] != "V61-OFF-014"]
    assert derive_catalog() == current
    assert derive_lexicon() == json.loads((HERE / "prop_lexicon.json").read_text())
    assert {
        entry["environment"] for entry in current["entries"]
        if "laptop_bag" in entry["repetition_groups"]
    } == {"Café", "Education"}
    assert not any(
        {"paperweight", "stone_object"}.intersection(entry["repetition_groups"])
        for entry in current["entries"]
    )


@pytest.mark.parametrize("name,groups", [
    ("stone paperweight", ["paperweight"]),
    ("clear glass paperweight", ["paperweight"]),
    ("river stones", ["stone_object"]),
    ("metal paper weight", ["desk_sculpture"]),
])
def test_removed_props_cannot_be_reapproved_through_a_catalogue(name, groups) -> None:
    value = json.loads(CATALOG.read_text())
    value["entries"].append({
        "id": "REJECTED-PROP", "environment": "Office",
        "role": "tabletop_or_movable", "name": name,
        "repetition_groups": groups, "aliases": [name],
    })
    with pytest.raises(ValueError, match="excluded paperweight or loose stone"):
        validate_catalog(value)


def test_frozen_v62_sources_are_unchanged() -> None:
    baseline = json.loads((HERE / "baseline_manifest.json").read_text())
    for name, expected in baseline["files"].items():
        assert hashlib.sha256((HERE.parent / "v6_2" / name).read_bytes()).hexdigest() == expected
