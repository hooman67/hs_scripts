from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path

import pytest

from research.source_messaging_v1_to_v6.versions.v6.compile_approved_markdown import (
    compile_markdown_approvals,
    derive_decision_csv,
)


ROOT = Path(__file__).resolve().parents[5]
SOURCE_MD = ROOT / "research" / "approved_props_v6" / "PROPS_FOR_REVIEW.md"
SOURCE_CSV = ROOT / "research" / "approved_props_v6" / "data" / "prop_candidates.csv"


def _decisions(csv_bytes: bytes) -> dict[str, str]:
    return {
        row["candidate_id"]: row["reviewer_decision"]
        for row in csv.DictReader(io.StringIO(csv_bytes.decode("utf-8")))
    }


def test_live_markdown_maps_retained_deletions_and_all_uncertain_explicitly() -> None:
    derived, mappings = derive_decision_csv(SOURCE_MD.read_bytes(), SOURCE_CSV.read_bytes())
    decisions = _decisions(derived)

    assert list(decisions.values()).count("approve") == 237
    assert list(decisions.values()).count("reject") == 3
    assert list(decisions.values()).count("hold") == 22
    assert decisions["HOM-40"] == "reject"  # Framed family photograph
    assert decisions["OFF-19"] == "reject"  # Office magazine
    assert decisions["OFF-22"] == "reject"  # Desk nameplate
    assert decisions["HOM-02"] == "approve"  # Same name, different environment
    assert decisions["CAF-21"] == "approve"
    # Retained text/face-risk ordinary props are approvals; prompt policy carries
    # their conditional-use constraints rather than removing them from catalog.
    assert decisions["CAF-19"] == "approve"  # Table menu
    assert decisions["CAF-34"] == "approve"  # Chalkboard menu
    assert decisions["EDU-39"] == "approve"  # Framed student artwork
    assert decisions["GAM-12"] == "approve"  # Original-artwork card album
    assert decisions["STU-22"] == "approve"  # Reference photographs
    # These entries were removed from the uncertain table, but removal is not approval.
    assert decisions["UNC-10"] == "hold"
    assert decisions["UNC-11"] == "hold"
    assert decisions["UNC-12"] == "hold"
    assert decisions["UNC-20"] == "hold"
    assert decisions["UNC-21"] == "hold"
    assert decisions["UNC-22"] == "hold"
    assert all(
        item["basis"] == "uncertain_never_approves"
        for item in mappings
        if item["candidate_id"].startswith("UNC-")
    )


def test_compilation_preserves_sources_and_hashes_derived_csv(tmp_path: Path) -> None:
    markdown_before = SOURCE_MD.read_bytes()
    csv_before = SOURCE_CSV.read_bytes()
    artifacts = tmp_path / "approvals"
    catalog_path = tmp_path / "approved.catalog.json"

    provenance = compile_markdown_approvals(
        SOURCE_MD, SOURCE_CSV, artifacts, catalog_path, "test-approved-20261029"
    )

    assert SOURCE_MD.read_bytes() == markdown_before
    assert SOURCE_CSV.read_bytes() == csv_before
    assert (artifacts / "PROPS_FOR_REVIEW.user-approved.md").read_bytes() == markdown_before
    derived = (artifacts / "prop_candidates.decisions.csv").read_bytes()
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    assert catalog["source_sha256"] == hashlib.sha256(derived).hexdigest()
    assert len(catalog["entries"]) == 237
    assert {entry["id"] for entry in catalog["entries"]}.isdisjoint(
        {"HOM-40", "OFF-19", "OFF-22", "UNC-10", "UNC-20", "UNC-22"}
    )
    assert provenance["sources"]["approved_markdown"]["sha256"] == hashlib.sha256(
        markdown_before
    ).hexdigest()
    assert provenance["counts"] == {
        "candidate_rows": 262,
        "approve": 237,
        "reject": 3,
        "hold": 22,
        "catalog_entries": 237,
    }


def test_unknown_markdown_candidate_fails_closed() -> None:
    source = SOURCE_MD.read_text(encoding="utf-8").replace(
        "Paperback book, magazine", "Imaginary approval token, paperback book, magazine", 1
    )
    with pytest.raises(ValueError, match="unknown candidates"):
        derive_decision_csv(source.encode("utf-8"), SOURCE_CSV.read_bytes())


def test_duplicate_markdown_candidate_fails_closed() -> None:
    source = SOURCE_MD.read_text(encoding="utf-8").replace(
        "Paperback book, magazine", "Paperback book, paperback book, magazine", 1
    )
    with pytest.raises(ValueError, match="duplicate Markdown candidate"):
        derive_decision_csv(source.encode("utf-8"), SOURCE_CSV.read_bytes())
