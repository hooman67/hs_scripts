from __future__ import annotations

import copy
import csv
import hashlib
from pathlib import Path

import pytest

import research.source_messaging_v1_to_v6.versions.v6.catalog as catalog_module
from research.source_messaging_v1_to_v6.versions.v6.catalog import (
    CATALOG_VERSION,
    compile_catalog,
    load_lexicon,
    validate_catalog,
)


ROOT = Path(__file__).resolve().parents[5]
SOURCE_CSV = ROOT / "research" / "approved_props_v6" / "data" / "prop_candidates.csv"


def _review_copy(tmp_path: Path, changes: dict[str, dict[str, str]]) -> Path:
    with SOURCE_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames
    assert fieldnames is not None
    for row in rows:
        row.update(changes.get(row["candidate_id"], {}))
    path = tmp_path / "review.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _approved_catalog(tmp_path: Path, **changes: str) -> dict:
    row_changes = {"reviewer_decision": "approve", **changes}
    path = _review_copy(tmp_path, {"OFF-01": row_changes})
    return compile_catalog(path, "test-revision", purpose="test_fixture")


def test_pending_source_compiles_empty_without_modifying_review_record() -> None:
    before = SOURCE_CSV.read_bytes()
    catalog = compile_catalog(SOURCE_CSV, "review-pending")

    assert catalog == {
        "version": CATALOG_VERSION,
        "revision": "review-pending",
        "purpose": "production",
        "source_sha256": hashlib.sha256(before).hexdigest(),
        "entries": [],
    }
    assert SOURCE_CSV.read_bytes() == before
    assert b"Proposed oardinary scene item" in before  # user edit is preserved
    with pytest.raises(ValueError, match="at least one approved"):
        validate_catalog(catalog)


def test_only_explicit_approve_is_compiled_and_runtime_flag_cannot_bypass_review(
    tmp_path: Path,
) -> None:
    path = _review_copy(
        tmp_path,
        {
            "OFF-01": {
                "reviewer_decision": "  ApPrOvE  ",
                "reviewer_notes": "Keep this exact reviewer note.",
            },
            "OFF-02": {"reviewer_decision": "reject", "runtime_allowed": "true"},
            "OFF-03": {"reviewer_decision": "hold", "runtime_allowed": "true"},
            "OFF-04": {"runtime_allowed": "true"},
        },
    )
    before = path.read_bytes()

    catalog = compile_catalog(path, "decision-separation", purpose="test_fixture")

    assert [entry["id"] for entry in catalog["entries"]] == ["OFF-01"]
    assert path.read_bytes() == before
    assert b"Keep this exact reviewer note." in before


@pytest.mark.parametrize("decision", ["yes", "approved", "approve later", "?"])
def test_unknown_reviewer_decision_fails_closed(tmp_path: Path, decision: str) -> None:
    path = _review_copy(tmp_path, {"OFF-01": {"reviewer_decision": decision}})
    with pytest.raises(ValueError, match="unknown reviewer decision"):
        compile_catalog(path, "bad-decision")


def test_cross_environment_approval_requires_explicit_environment_row(tmp_path: Path) -> None:
    path = _review_copy(tmp_path, {"UNC-05": {"reviewer_decision": "approve"}})
    with pytest.raises(ValueError, match="cross-environment"):
        compile_catalog(path, "cross-environment")


def test_future_environment_accessory_row_can_be_approved(tmp_path: Path) -> None:
    path = _review_copy(
        tmp_path,
        {
            "UNC-01": {
                "candidate_id": "OFF-KBD1",
                "environment": "Office",
                "role": "tabletop_or_movable",
                "reviewer_decision": "approve",
            }
        },
    )
    catalog = compile_catalog(path, "keyboard-approved", purpose="test_fixture")
    assert [entry["id"] for entry in catalog["entries"]] == ["OFF-KBD1"]


def test_computing_device_boundary_survives_manual_environment_approval(
    tmp_path: Path,
) -> None:
    path = _review_copy(
        tmp_path,
        {
            "UNC-21": {
                "candidate_id": "OFF-PC1",
                "environment": "Office",
                "role": "tabletop_or_movable",
                "reviewer_decision": "approve",
            }
        },
    )
    with pytest.raises(ValueError, match="computing-device boundary"):
        compile_catalog(path, "device-block")


def test_compiled_aliases_expose_repetition_family(tmp_path: Path) -> None:
    catalog = _approved_catalog(tmp_path)
    entry = catalog["entries"][0]
    assert entry["repetition_groups"] == ["notebook"]
    assert {"notebook", "notebooks", "sketchbook", "exercise book"} <= set(
        entry["aliases"]
    )


def test_new_reviewed_name_extends_pinned_group_aliases(tmp_path: Path) -> None:
    catalog = _approved_catalog(tmp_path, name="Field journal")
    aliases = set(catalog["entries"][0]["aliases"])

    assert {"field journal", "field journals"} <= aliases
    assert {"notebook", "sketchbook", "exercise book"} <= aliases


def test_lexicon_has_exact_synonym_families_without_unsafe_conflation() -> None:
    lexicon = {item["phrase"]: item["groups"] for item in load_lexicon()}

    for phrase in ("notebook", "sketchbook", "exercise book"):
        assert lexicon[phrase] == ["notebook"]
    for phrase in ("mug", "cup", "coffee cup"):
        assert lexicon[phrase] == ["cup_mug"]
    for phrase in ("plant", "plants", "houseplant"):
        assert lexicon[phrase] == ["plant"]
    for phrase in ("chair", "armchair"):
        assert lexicon[phrase] == ["chair"]
    for phrase in ("shelf", "bookshelf", "bookcase"):
        assert lexicon[phrase] == ["shelving"]
    for phrase in ("document", "form", "paper stack"):
        assert lexicon[phrase] == ["paper_documents"]
    assert lexicon["binder"] == ["ring_binder"]
    assert lexicon["binder clip"] == ["binder_clips"]
    assert lexicon["glasses"] == ["eyeglasses"]
    assert lexicon["water glass"] == ["drinking_glass"]
    assert lexicon["gaming controller"] == ["controller"]


def test_compound_aliases_do_not_assign_all_groups_to_bare_components() -> None:
    lexicon = {item["phrase"]: item["groups"] for item in load_lexicon()}

    assert lexicon["fruit bowl"] == ["bowl", "fruit"]
    assert lexicon["snack bowl"] == ["bowl"]
    assert lexicon["bowl"] == ["bowl"]
    assert lexicon["fruit"] == ["fruit"]
    assert lexicon["bud vase with a flower"] == ["cut_flowers", "vase"]
    assert lexicon["vase"] == ["vase"]
    assert lexicon["flower"] == ["cut_flowers"]


def test_lexicon_runtime_load_has_no_review_csv_dependency(monkeypatch) -> None:
    def csv_access_would_fail(*args, **kwargs):
        raise AssertionError("runtime lexicon attempted to read the review CSV")

    monkeypatch.setattr(catalog_module.csv, "DictReader", csv_access_would_fail)
    assert any(item["phrase"] == "keyboard" for item in load_lexicon())


def test_all_ordinary_rows_can_compile_without_compound_alias_pollution(
    tmp_path: Path,
) -> None:
    with SOURCE_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames
    assert fieldnames is not None
    for row in rows:
        if row["environment"] != "Cross-environment":
            row["reviewer_decision"] = "approve"
    path = tmp_path / "all-ordinary-approved.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    compiled = compile_catalog(path, "all-ordinary", purpose="test_fixture")

    assert len(compiled["entries"]) == 240
    fruit_bowl = next(item for item in compiled["entries"] if item["id"] == "OFF-28")
    assert "fruit bowl" in fruit_bowl["aliases"]
    assert "bowl" not in fruit_bowl["aliases"]
    assert "fruit" not in fruit_bowl["aliases"]
    snack_bowl = next(item for item in compiled["entries"] if item["id"] == "OFF-27")
    assert snack_bowl["repetition_groups"] == ["bowl"]
    assert "fruit" not in snack_bowl["aliases"]


def test_runtime_validation_accepts_only_explicit_test_catalog_opt_in(
    tmp_path: Path,
) -> None:
    catalog = _approved_catalog(tmp_path)
    with pytest.raises(ValueError, match="allow_test_catalog"):
        validate_catalog(catalog)
    assert validate_catalog(catalog, allow_test_catalog=True) is catalog


def test_runtime_validation_rejects_duplicate_ids_and_invalid_groups(
    tmp_path: Path,
) -> None:
    catalog = _approved_catalog(tmp_path)
    duplicate = copy.deepcopy(catalog)
    duplicate["entries"].append(copy.deepcopy(duplicate["entries"][0]))
    with pytest.raises(ValueError, match="duplicate catalog entry ID"):
        validate_catalog(duplicate, allow_test_catalog=True)

    repeated_group = copy.deepcopy(catalog)
    repeated_group["entries"][0]["repetition_groups"] = ["notebook", "notebook"]
    with pytest.raises(ValueError, match="invalid repetition groups"):
        validate_catalog(repeated_group, allow_test_catalog=True)

    malformed_group = copy.deepcopy(catalog)
    malformed_group["entries"][0]["repetition_groups"] = ["Notebook"]
    with pytest.raises(ValueError, match="invalid repetition groups"):
        validate_catalog(malformed_group, allow_test_catalog=True)

    unknown_group = copy.deepcopy(catalog)
    unknown_group["entries"][0]["repetition_groups"] = ["arbitrary_prose_noun"]
    with pytest.raises(ValueError, match="invalid repetition groups"):
        validate_catalog(unknown_group, allow_test_catalog=True)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("environment", "Cross-environment", "invalid environment"),
        ("role", "uncertain_accessory_or_product", "invalid role"),
    ],
)
def test_runtime_validation_rejects_non_runtime_entry_fields(
    tmp_path: Path, field: str, value: str, message: str
) -> None:
    catalog = _approved_catalog(tmp_path)
    catalog["entries"][0][field] = value
    with pytest.raises(ValueError, match=message):
        validate_catalog(catalog, allow_test_catalog=True)


def test_runtime_validation_rejects_raw_unreviewed_metadata(tmp_path: Path) -> None:
    catalog = _approved_catalog(tmp_path)
    catalog["entries"][0]["reviewer_decision"] = "approve"
    with pytest.raises(ValueError, match="unreviewed fields"):
        validate_catalog(catalog, allow_test_catalog=True)


def test_runtime_validation_rejects_unsupported_purpose(tmp_path: Path) -> None:
    catalog = _approved_catalog(tmp_path)
    catalog["purpose"] = "development"
    with pytest.raises(ValueError, match="unsupported catalog purpose"):
        validate_catalog(catalog, allow_test_catalog=True)
