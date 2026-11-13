#!/usr/bin/env python3
"""Validate the Fremont pilot claim-ledger schema and controlled labels."""

from __future__ import annotations

import csv
from pathlib import Path


REQUIRED = [
    "claim_id",
    "project",
    "candidate",
    "topic",
    "claim",
    "evidence_status",
    "confidence",
    "source_publisher",
    "source_title",
    "source_url",
    "source_date",
    "retrieved_at",
    "source_location",
    "evidence_excerpt",
    "geography",
    "unit",
    "calculation",
    "limitations",
    "refresh_after",
    "reviewer",
]

EVIDENCE = {
    "PRIMARY",
    "SECONDARY",
    "QUOTED",
    "INFERRED",
    "ESTIMATE",
    "SPECULATIVE",
    "CONFLICTED",
    "UNKNOWN",
}
CONFIDENCE = {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}


def main() -> None:
    ledger = Path(__file__).parents[1] / "evidence" / "claims.csv"
    with ledger.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == REQUIRED, (reader.fieldnames, REQUIRED)
        rows = list(reader)

    ids = [row["claim_id"] for row in rows]
    assert len(ids) == len(set(ids)), "duplicate claim_id"
    for number, row in enumerate(rows, start=2):
        assert row["claim_id"], f"row {number}: missing claim_id"
        assert row["claim"], f"row {number}: missing claim"
        assert row["evidence_status"] in EVIDENCE, f"row {number}: bad evidence status"
        assert row["confidence"] in CONFIDENCE, f"row {number}: bad confidence"
        assert row["retrieved_at"] == "2026-09-12", f"row {number}: bad retrieval date"
        assert row["limitations"], f"row {number}: missing limitations"
        assert row["refresh_after"], f"row {number}: missing refresh rule"
        assert row["reviewer"], f"row {number}: missing reviewer"
        if row["evidence_status"] != "UNKNOWN":
            assert row["source_publisher"], f"row {number}: missing publisher"
            assert row["source_title"], f"row {number}: missing source title"
            assert row["source_url"], f"row {number}: missing source URL/path"
            assert row["source_location"], f"row {number}: missing source location"
            assert row["evidence_excerpt"], f"row {number}: missing evidence excerpt"

    print(f"PASS: {len(rows)} unique claims; schema and controlled labels valid")


if __name__ == "__main__":
    main()

