#!/usr/bin/env python3
"""Extract authoritative October guidance DOCX text with XML provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import ZipFile


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_DOCX = Path(
    "/mnt/localssd/HP_scenes/input_output_hp_rewriter/example_prompts/"
    "HP - mAIstro Prompt Guidance (Oct 2026).docx"
)
EXISTING_GUIDANCE = PROJECT_ROOT / "research/source_messaging_v1_to_v6/data/october_guidance.json"
DATA_DIR = PROJECT_ROOT / "research/diversity_aware_v3/data"
RAW_OUTPUT = DATA_DIR / "october_guidance_raw_extraction.json"
AUDIT_OUTPUT = DATA_DIR / "october_guidance_drift_audit.json"
DOCUMENT_MEMBER = "word/document.xml"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def paragraph_text_events(paragraph: ET.Element, location: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    replacements = {
        "tab": "\t",
        "br": "\n",
        "cr": "\n",
        "noBreakHyphen": "\u2011",
        "softHyphen": "\u00ad",
    }
    for element in paragraph.iter():
        name = local_name(element.tag)
        if name == "t":
            text = element.text or ""
        elif name in replacements:
            text = replacements[name]
        else:
            continue
        events.append(
            {
                "event": len(events) + 1,
                "location": f"{location}/text-event[{len(events) + 1}]",
                "xml_element": f"w:{name}",
                "text": text,
            }
        )
    return events


def paragraph_record(
    paragraph: ET.Element,
    *,
    location: str,
    body_order: int,
    paragraph_index: int,
    table_coordinates: dict[str, int] | None = None,
) -> dict[str, Any]:
    events = paragraph_text_events(paragraph, location)
    style_element = paragraph.find(f"{W}pPr/{W}pStyle")
    record: dict[str, Any] = {
        "paragraph": paragraph_index,
        "body_order": body_order,
        "location": location,
        "paragraph_style": style_element.get(f"{W}val") if style_element is not None else None,
        "text": "".join(event["text"] for event in events),
        "text_events": events,
    }
    if table_coordinates is not None:
        record["table_coordinates"] = table_coordinates
    return record


def extract_docx() -> dict[str, Any]:
    source_bytes = SOURCE_DOCX.read_bytes()
    with ZipFile(SOURCE_DOCX) as archive:
        member_names = archive.namelist()
        require(DOCUMENT_MEMBER in member_names, f"missing {DOCUMENT_MEMBER}")
        document_xml = archive.read(DOCUMENT_MEMBER)
    root = ET.fromstring(document_xml)
    body = root.find(f"{W}body")
    require(body is not None, "DOCX document.xml has no w:body")

    blocks: list[dict[str, Any]] = []
    references: list[dict[str, Any]] = []
    paragraph_index = 0
    table_index = 0
    table_row_count = 0
    table_cell_count = 0

    def add_reference(record: dict[str, Any], source_type: str) -> None:
        references.append(
            {
                "reference": len(references) + 1,
                "source_type": source_type,
                "body_order": record["body_order"],
                "location": record["location"],
                "paragraph": record["paragraph"],
                "table_coordinates": record.get("table_coordinates"),
                "text": record["text"],
            }
        )

    for body_order, child in enumerate(list(body), 1):
        name = local_name(child.tag)
        if name == "p":
            paragraph_index += 1
            location = f"/w:document/w:body/w:p[{paragraph_index}]"
            paragraph = paragraph_record(
                child,
                location=location,
                body_order=body_order,
                paragraph_index=paragraph_index,
            )
            blocks.append({"type": "paragraph", **paragraph})
            add_reference(paragraph, "body_paragraph")
        elif name == "tbl":
            table_index += 1
            table_location = f"/w:document/w:body/w:tbl[{table_index}]"
            rows: list[dict[str, Any]] = []
            for row_index, row in enumerate(child.findall(f"{W}tr"), 1):
                table_row_count += 1
                cells: list[dict[str, Any]] = []
                for cell_index, cell in enumerate(row.findall(f"{W}tc"), 1):
                    table_cell_count += 1
                    cell_paragraphs: list[dict[str, Any]] = []
                    for cell_paragraph_index, paragraph_element in enumerate(
                        cell.findall(f"{W}p"), 1
                    ):
                        paragraph_index += 1
                        location = (
                            f"{table_location}/w:tr[{row_index}]/w:tc[{cell_index}]"
                            f"/w:p[{cell_paragraph_index}]"
                        )
                        paragraph = paragraph_record(
                            paragraph_element,
                            location=location,
                            body_order=body_order,
                            paragraph_index=paragraph_index,
                            table_coordinates={
                                "table": table_index,
                                "row": row_index,
                                "cell": cell_index,
                                "cell_paragraph": cell_paragraph_index,
                            },
                        )
                        cell_paragraphs.append(paragraph)
                        add_reference(paragraph, "table_cell_paragraph")
                    cells.append(
                        {
                            "cell": cell_index,
                            "location": f"{table_location}/w:tr[{row_index}]/w:tc[{cell_index}]",
                            "paragraphs": cell_paragraphs,
                        }
                    )
                rows.append(
                    {
                        "row": row_index,
                        "location": f"{table_location}/w:tr[{row_index}]",
                        "cells": cells,
                    }
                )
            blocks.append(
                {
                    "type": "table",
                    "body_order": body_order,
                    "table": table_index,
                    "location": table_location,
                    "rows": rows,
                }
            )
        elif name == "sectPr":
            blocks.append(
                {
                    "type": "section_properties",
                    "body_order": body_order,
                    "location": "/w:document/w:body/w:sectPr[1]",
                }
            )
        else:
            blocks.append(
                {
                    "type": "unhandled_body_element",
                    "xml_element": f"w:{name}",
                    "body_order": body_order,
                    "location": f"/w:document/w:body/w:{name}[1]",
                }
            )

    return {
        "version": "october-guidance-docx-raw-extraction-v1",
        "authority": {
            "path": str(SOURCE_DOCX),
            "bytes": len(source_bytes),
            "sha256": sha256_bytes(source_bytes),
            "package_member": DOCUMENT_MEMBER,
            "package_member_bytes": len(document_xml),
            "package_member_sha256": sha256_bytes(document_xml),
        },
        "extraction_contract": {
            "scope": "word/document.xml body paragraphs and table-cell paragraphs",
            "ordering": "top-level w:body order; tables use row, cell, then paragraph order",
            "text_events": "w:t text plus literal tab, line-break, carriage-return, nonbreaking-hyphen, and soft-hyphen events",
            "normalization": "none",
            "empty_paragraphs_retained": True,
        },
        "counts": {
            "body_elements": len(list(body)),
            "top_level_paragraphs": sum(block["type"] == "paragraph" for block in blocks),
            "tables": table_index,
            "table_rows": table_row_count,
            "table_cells": table_cell_count,
            "all_paragraphs": paragraph_index,
            "references": len(references),
            "nonempty_references": sum(bool(reference["text"]) for reference in references),
        },
        "blocks": blocks,
        "references": references,
    }


def build_audit(raw_extraction: dict[str, Any], raw_bytes: bytes) -> dict[str, Any]:
    existing_bytes = EXISTING_GUIDANCE.read_bytes()
    existing = json.loads(existing_bytes)
    authority = raw_extraction["authority"]
    existing_source_path = Path(existing["path"])
    existing_source_exists = existing_source_path.is_file()
    existing_source_sha = (
        sha256_bytes(existing_source_path.read_bytes()) if existing_source_exists else None
    )
    extracted_body_paragraphs = [
        block for block in raw_extraction["blocks"] if block["type"] == "paragraph"
    ]
    existing_paragraphs = existing.get("paragraphs", [])
    paragraph_comparisons: list[dict[str, Any]] = []
    max_count = max(len(extracted_body_paragraphs), len(existing_paragraphs))
    for offset in range(max_count):
        extracted = extracted_body_paragraphs[offset] if offset < len(extracted_body_paragraphs) else None
        prior = existing_paragraphs[offset] if offset < len(existing_paragraphs) else None
        paragraph_comparisons.append(
            {
                "position": offset + 1,
                "extracted_location": extracted["location"] if extracted else None,
                "extracted_paragraph": extracted["paragraph"] if extracted else None,
                "existing_paragraph": prior.get("paragraph") if prior else None,
                "extracted_text": extracted["text"] if extracted else None,
                "existing_text": prior.get("text") if prior else None,
                "number_matches": bool(extracted and prior and extracted["paragraph"] == prior.get("paragraph")),
                "text_matches_exactly": bool(extracted and prior and extracted["text"] == prior.get("text")),
            }
        )

    content_matches = (
        len(extracted_body_paragraphs) == len(existing_paragraphs)
        and all(item["number_matches"] and item["text_matches_exactly"] for item in paragraph_comparisons)
    )
    discrepancies: list[dict[str, Any]] = []
    if Path(existing["path"]) != SOURCE_DOCX:
        discrepancies.append(
            {
                "type": "source_path_differs",
                "scope": "provenance",
                "authoritative_path": str(SOURCE_DOCX),
                "existing_recorded_path": existing["path"],
                "existing_recorded_path_exists": existing_source_exists,
                "existing_recorded_file_sha256": existing_source_sha,
                "content_impact": "none when the recorded file hash equals the authority hash",
            }
        )
    if existing.get("sha256") != authority["sha256"]:
        discrepancies.append(
            {
                "type": "declared_docx_sha256_differs",
                "scope": "content_provenance",
                "authoritative_sha256": authority["sha256"],
                "existing_declared_sha256": existing.get("sha256"),
            }
        )
    if not content_matches:
        discrepancies.append(
            {
                "type": "paragraph_content_or_order_differs",
                "scope": "content",
                "mismatched_positions": [
                    item["position"]
                    for item in paragraph_comparisons
                    if not item["number_matches"] or not item["text_matches_exactly"]
                ],
            }
        )
    if raw_extraction["counts"]["tables"] and "tables" not in existing:
        discrepancies.append(
            {
                "type": "existing_artifact_omits_tables",
                "scope": "content",
                "authoritative_table_count": raw_extraction["counts"]["tables"],
            }
        )

    return {
        "version": "october-guidance-drift-audit-v1",
        "authority": authority,
        "raw_extraction": {
            "path": str(RAW_OUTPUT),
            "bytes": len(raw_bytes),
            "sha256": sha256_bytes(raw_bytes),
            "reference_count": raw_extraction["counts"]["references"],
        },
        "existing_artifact": {
            "path": str(EXISTING_GUIDANCE),
            "bytes": len(existing_bytes),
            "sha256": sha256_bytes(existing_bytes),
            "recorded_docx_path": existing.get("path"),
            "recorded_docx_sha256": existing.get("sha256"),
            "recorded_docx_path_exists": existing_source_exists,
            "recorded_docx_file_sha256": existing_source_sha,
            "paragraph_count": len(existing_paragraphs),
        },
        "comparison": {
            "authority_docx_matches_existing_declared_sha256": existing.get("sha256") == authority["sha256"],
            "authority_docx_matches_existing_recorded_file_bytes": existing_source_sha == authority["sha256"],
            "paragraph_count_matches": len(extracted_body_paragraphs) == len(existing_paragraphs),
            "paragraph_text_and_order_match_exactly": content_matches,
            "authority_table_count": raw_extraction["counts"]["tables"],
            "content_drift_detected": any(item["scope"] == "content" for item in discrepancies),
            "provenance_drift_detected": any(item["scope"] == "provenance" for item in discrepancies),
        },
        "discrepancies": discrepancies,
        "paragraph_comparisons": paragraph_comparisons,
    }


def build_outputs() -> tuple[dict[str, Any], dict[str, Any]]:
    raw = extract_docx()
    raw_bytes = json_bytes(raw)
    audit = build_audit(raw, raw_bytes)
    return raw, audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify durable outputs are current")
    args = parser.parse_args()
    raw, audit = build_outputs()
    outputs = ((RAW_OUTPUT, raw), (AUDIT_OUTPUT, audit))
    if args.check:
        for path, document in outputs:
            require(path.is_file(), f"missing generated output: {path}")
            require(path.read_bytes() == json_bytes(document), f"stale generated output: {path}")
    else:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        for path, document in outputs:
            path.write_bytes(json_bytes(document))
    print(
        json.dumps(
            {
                "checked": args.check,
                "authority_sha256": raw["authority"]["sha256"],
                "reference_count": raw["counts"]["references"],
                "outputs": [
                    {
                        "path": str(path),
                        "bytes": len(json_bytes(document)),
                        "sha256": sha256_bytes(json_bytes(document)),
                    }
                    for path, document in outputs
                ],
                "comparison": audit["comparison"],
                "discrepancy_count": len(audit["discrepancies"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
