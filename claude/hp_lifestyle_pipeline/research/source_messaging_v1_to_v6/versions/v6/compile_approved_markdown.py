#!/usr/bin/env python3
"""Compile the user-approved V6 Markdown menu into auditable approval artifacts.

Ordinary entries retained in the Markdown are approved for their exact
environment and role. Ordinary entries removed from the Markdown are rejected.
Every cross-environment uncertain candidate remains on hold, whether or not it
is still displayed in the Markdown's uncertain table.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parent))

from v6.catalog import compile_catalog, validate_catalog


ENVIRONMENTS = (
    "Home",
    "Office",
    "Education",
    "Gaming",
    "Café",
    "Creative Studio",
)
ROLE_HEADINGS = {
    "Smaller props": "tabletop_or_movable",
    "Background furnishings/decor": "background_furnishing_or_decor",
}
CSV_FIELDS = (
    "candidate_id",
    "environment",
    "role",
    "name",
    "repetition_groups",
    "status",
    "runtime_allowed",
    "review_reason",
    "reviewer_decision",
    "reviewer_notes",
)
DECISION_NOTES = {
    "approve": (
        "USER-CONFIRMED 2026-10-29: retained in the ordinary-prop Markdown menu "
        "for this exact environment and role."
    ),
    "reject": (
        "USER-CONFIRMED 2026-10-29: removed from the ordinary-prop Markdown menu "
        "for this exact environment and role."
    ),
    "hold": (
        "No explicit approval: uncertain candidates remain unavailable, including "
        "candidates omitted from the current uncertain table."
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalise_name(value: str) -> str:
    """Return the exact-match normalization used for Markdown-to-CSV mapping."""

    value = unicodedata.normalize("NFKC", value).casefold()
    value = value.replace("-", " ").replace("/", " ")
    value = re.sub(r"[^\w\s]", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def parse_ordinary_markdown(source: bytes) -> dict[tuple[str, str, str], dict[str, Any]]:
    """Parse only ordinary prop sections; the uncertain section is never approval."""

    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("approval Markdown must be UTF-8") from exc

    sections: dict[tuple[str, str], list[tuple[int, str]]] = {}
    current_environment: str | None = None
    current_role: str | None = None
    in_uncertain = False

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if line.startswith("# "):
            heading = line[2:].strip()
            if heading in ENVIRONMENTS:
                current_environment = heading
                current_role = None
                in_uncertain = False
            elif heading.startswith("Uncertain"):
                current_environment = None
                current_role = None
                in_uncertain = True
            else:
                raise ValueError(
                    f"approval Markdown line {line_number} has an unknown top-level heading: {heading!r}"
                )
            continue
        if line.startswith("## "):
            if in_uncertain:
                continue
            if current_environment is None:
                raise ValueError(
                    f"approval Markdown line {line_number} has a role before an environment"
                )
            heading = line[3:].strip()
            if heading not in ROLE_HEADINGS:
                raise ValueError(
                    f"approval Markdown line {line_number} has an unknown role heading: {heading!r}"
                )
            current_role = ROLE_HEADINGS[heading]
            sections.setdefault((current_environment, current_role), [])
            continue
        if line and current_environment is not None and current_role is not None:
            sections[(current_environment, current_role)].append((line_number, line))

    expected_sections = {
        (environment, role)
        for environment in ENVIRONMENTS
        for role in ROLE_HEADINGS.values()
    }
    if set(sections) != expected_sections:
        missing = sorted(expected_sections - set(sections))
        extra = sorted(set(sections) - expected_sections)
        raise ValueError(f"approval Markdown section mismatch; missing={missing}, extra={extra}")

    mentions: dict[tuple[str, str, str], dict[str, Any]] = {}
    for (environment, role), fragments in sections.items():
        if not fragments:
            raise ValueError(f"approval Markdown section {environment}/{role} is empty")
        paragraph = " ".join(fragment for _, fragment in fragments).strip()
        paragraph = paragraph[:-1] if paragraph.endswith(".") else paragraph
        for raw_name in paragraph.split(","):
            name = raw_name.strip()
            normalized = normalise_name(name)
            if not normalized:
                raise ValueError(f"approval Markdown has an empty entry in {environment}/{role}")
            key = (environment, role, normalized)
            if key in mentions:
                raise ValueError(
                    f"duplicate Markdown candidate in {environment}/{role}: {name!r}"
                )
            mentions[key] = {
                "environment": environment,
                "role": role,
                "markdown_name": name,
                "normalized_name": normalized,
                "markdown_line": fragments[0][0],
            }
    return mentions


def derive_decision_csv(
    markdown_source: bytes, csv_source: bytes
) -> tuple[bytes, list[dict[str, Any]]]:
    """Map the Markdown to the candidate CSV without mutating either source."""

    mentions = parse_ordinary_markdown(markdown_source)
    try:
        text = csv_source.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("candidate CSV must be UTF-8") from exc
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames is None or tuple(reader.fieldnames) != CSV_FIELDS:
        raise ValueError("candidate CSV fields do not match the pinned review schema")
    rows = list(reader)

    seen_ids: set[str] = set()
    candidate_keys: dict[tuple[str, str, str], str] = {}
    mappings: list[dict[str, Any]] = []
    consumed_mentions: set[tuple[str, str, str]] = set()
    for line_number, row in enumerate(rows, start=2):
        if None in row:
            raise ValueError(f"candidate CSV line {line_number} has extra fields")
        candidate_id = row["candidate_id"].strip()
        if not candidate_id or candidate_id in seen_ids:
            raise ValueError(f"candidate CSV has a blank or duplicate ID: {candidate_id!r}")
        seen_ids.add(candidate_id)

        environment = row["environment"].strip()
        role = row["role"].strip()
        name = row["name"].strip()
        normalized = normalise_name(name)
        key = (environment, role, normalized)
        markdown_line: int | None = None

        if environment == "Cross-environment" and role == "uncertain_accessory_or_product":
            decision = "hold"
            basis = "uncertain_never_approves"
        elif environment in ENVIRONMENTS and role in ROLE_HEADINGS.values():
            if key in candidate_keys:
                raise ValueError(
                    "duplicate normalized candidate key in CSV: "
                    f"{environment}/{role}/{normalized!r}"
                )
            candidate_keys[key] = candidate_id
            if key in mentions:
                decision = "approve"
                basis = "retained_ordinary_markdown_entry"
                markdown_line = mentions[key]["markdown_line"]
                consumed_mentions.add(key)
            else:
                decision = "reject"
                basis = "removed_ordinary_markdown_entry"
        else:
            raise ValueError(
                f"candidate {candidate_id} has unsupported environment/role: {environment}/{role}"
            )

        row["reviewer_decision"] = decision
        row["reviewer_notes"] = DECISION_NOTES[decision]
        mappings.append(
            {
                "candidate_id": candidate_id,
                "environment": environment,
                "role": role,
                "name": name,
                "normalized_name": normalized,
                "decision": decision,
                "basis": basis,
                "markdown_line": markdown_line,
            }
        )

    unknown_mentions = sorted(set(mentions) - consumed_mentions)
    if unknown_mentions:
        rendered = [
            {
                "environment": mentions[key]["environment"],
                "role": mentions[key]["role"],
                "name": mentions[key]["markdown_name"],
                "normalized_name": mentions[key]["normalized_name"],
            }
            for key in unknown_mentions
        ]
        raise ValueError(f"Markdown contains unknown candidates: {rendered}")

    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8"), mappings


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _write_new(path: Path, source: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(source)


def compile_markdown_approvals(
    markdown_path: Path,
    candidate_csv_path: Path,
    artifact_dir: Path,
    catalog_path: Path,
    revision: str = "approved-20261029",
) -> dict[str, Any]:
    """Create a raw snapshot, derived decisions, provenance, and runtime catalogue."""

    markdown_source = markdown_path.read_bytes()
    candidate_csv_source = candidate_csv_path.read_bytes()
    derived_csv, mappings = derive_decision_csv(markdown_source, candidate_csv_source)

    snapshot_path = artifact_dir / "PROPS_FOR_REVIEW.user-approved.md"
    derived_csv_path = artifact_dir / "prop_candidates.decisions.csv"
    provenance_path = artifact_dir / "provenance.json"
    outputs = (snapshot_path, derived_csv_path, provenance_path, catalog_path)
    existing = [str(path) for path in outputs if path.exists()]
    if existing:
        raise FileExistsError(f"refusing to overwrite approval artifacts: {existing}")

    # compile_catalog must hash the exact derived CSV bytes used as its source.
    derived_csv_path.parent.mkdir(parents=True, exist_ok=True)
    _write_new(derived_csv_path, derived_csv)
    try:
        catalog = compile_catalog(derived_csv_path, revision)
        validate_catalog(catalog)
        catalog_source = _json_bytes(catalog)
        counts = Counter(mapping["decision"] for mapping in mappings)
        provenance = {
            "artifact_version": "hp-v6-markdown-approval-provenance-v1",
            "decision_date": "2026-10-29",
            "decision_classification": "USER-CONFIRMED",
            "decision_rule": {
                "retained_ordinary_entry": "approve",
                "removed_ordinary_entry": "reject",
                "all_uncertain_candidates": "hold",
                "note": (
                    "The stale Markdown introduction does not override the user's explicit "
                    "approval. The uncertain section never grants approval, including to "
                    "entries removed from that table."
                ),
            },
            "sources": {
                "approved_markdown": {
                    "path": str(markdown_path.resolve()),
                    "sha256": sha256(markdown_source),
                    "bytes": len(markdown_source),
                    "snapshot_path": str(snapshot_path.resolve()),
                },
                "candidate_csv": {
                    "path": str(candidate_csv_path.resolve()),
                    "sha256": sha256(candidate_csv_source),
                    "bytes": len(candidate_csv_source),
                },
            },
            "derived": {
                "decision_csv": {
                    "path": str(derived_csv_path.resolve()),
                    "sha256": sha256(derived_csv),
                    "bytes": len(derived_csv),
                },
                "catalog": {
                    "path": str(catalog_path.resolve()),
                    "sha256": sha256(catalog_source),
                    "revision": revision,
                    "source_sha256": catalog["source_sha256"],
                },
            },
            "counts": {
                "candidate_rows": len(mappings),
                "approve": counts["approve"],
                "reject": counts["reject"],
                "hold": counts["hold"],
                "catalog_entries": len(catalog["entries"]),
            },
            "mappings": mappings,
        }
        provenance_source = _json_bytes(provenance)
        _write_new(snapshot_path, markdown_source)
        _write_new(catalog_path, catalog_source)
        _write_new(provenance_path, provenance_source)
    except Exception:
        # The derived CSV was newly created by this invocation. Remove only that
        # partial output so a corrected invocation can retry atomically.
        derived_csv_path.unlink(missing_ok=True)
        raise

    if snapshot_path.read_bytes() != markdown_source:
        raise RuntimeError("raw Markdown snapshot does not preserve source bytes")
    if catalog["source_sha256"] != sha256(derived_csv):
        raise RuntimeError("catalog source hash does not match derived decision CSV")
    return provenance


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--markdown",
        type=Path,
        default=PROJECT_ROOT / "research" / "approved_props_v6" / "PROPS_FOR_REVIEW.md",
    )
    parser.add_argument(
        "--candidate-csv",
        type=Path,
        default=(
            PROJECT_ROOT
            / "research"
            / "approved_props_v6"
            / "data"
            / "prop_candidates.csv"
        ),
    )
    parser.add_argument(
        "--artifact-dir",
        type=Path,
        default=(
            PROJECT_ROOT
            / "research"
            / "approved_props_v6"
            / "approvals"
            / "20261029"
        ),
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=HERE / "approved-20261029.catalog.json",
    )
    parser.add_argument("--revision", default="approved-20261029")
    args = parser.parse_args()

    provenance = compile_markdown_approvals(
        args.markdown,
        args.candidate_csv,
        args.artifact_dir,
        args.catalog,
        args.revision,
    )
    print(json.dumps(provenance["counts"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
