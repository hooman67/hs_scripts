from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from research.source_messaging_v1_to_v6.versions.v6_2.catalog import validate_catalog


HERE = Path(__file__).resolve().parents[1]
CATALOG = HERE / "approved-v6.2-20261106.catalog.json"


def test_compiled_v62_catalog_is_valid_and_tightened() -> None:
    value = json.loads(CATALOG.read_text())
    validated = validate_catalog(value)
    assert validated["version"] == "hp-v6.2-approved-props-v1"
    assert len(validated["entries"]) == 260
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
