from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from research.source_messaging_v1_to_v6.versions.v6_5_training.catalog import validate_catalog


HERE = Path(__file__).resolve().parents[1]
CATALOG = HERE / "approved-v6.5-20261111.catalog.json"


def test_compiled_v65_catalog_is_valid_and_retains_tightened_families() -> None:
    value = json.loads(CATALOG.read_text())
    validated = validate_catalog(value)
    assert validated["version"] == "hp-v6.5-approved-props-v1"
    provenance = json.loads((HERE / "authoring_provenance.json").read_text())
    assert len(validated["entries"]) == provenance["retained_entries"] + provenance["new_entries"]
    groups = {group for entry in validated["entries"] for group in entry["repetition_groups"]}
    assert {"paper_materials", "writing_tools", "wall_texture", "wall_slats"} <= groups


def test_catalog_rejects_v6_identity() -> None:
    value = json.loads(CATALOG.read_text())
    value["version"] = "hp-v6-approved-props-v1"
    with pytest.raises(ValueError, match="unsupported catalog version"):
        validate_catalog(value)


def test_catalog_rejects_unreviewed_fields() -> None:
    value = json.loads(CATALOG.read_text())
    value = copy.deepcopy(value)
    value["entries"][0]["invented"] = True
    with pytest.raises(ValueError, match="unreviewed fields"):
        validate_catalog(value)


def test_derivation_preserves_v64_entries_and_explicit_expansion_scope() -> None:
    base = json.loads((HERE.parent / "v6_4" / "approved-v6.3-20261109.catalog.json").read_text())
    current = json.loads(CATALOG.read_text())
    removed = set(json.loads((HERE / "authoring_provenance.json").read_text())["removed_legacy_ids"])
    current_by_id = {entry["id"]: entry for entry in current["entries"]}
    for entry in base["entries"]:
        if entry["id"] in removed:
            assert entry["id"] not in current_by_id
        else:
            assert {k: v for k, v in entry.items() if k != "aliases"} == {
                k: v for k, v in current_by_id[entry["id"]].items() if k != "aliases"
            }
    original_lexicon = json.loads((HERE.parent / "v6_4" / "prop_lexicon.json").read_text())
    new_phrases = {
        entry["phrase"]: set(entry["groups"])
        for entry in json.loads((HERE / "prop_lexicon.json").read_text())["entries"]
    }
    assert all(entry["phrase"] in new_phrases for entry in original_lexicon["entries"])
    assert {
        entry["environment"] for entry in current["entries"]
        if "laptop_bag" in entry["repetition_groups"]
    } == {"Home", "Office", "Education", "Gaming", "Café", "Creative Studio"}
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


def test_frozen_v64_sources_are_unchanged() -> None:
    baseline = json.loads((HERE / "baseline_manifest.json").read_text())
    for name, expected in baseline["files"].items():
        assert hashlib.sha256((HERE.parent / "v6_4" / name).read_bytes()).hexdigest() == expected
