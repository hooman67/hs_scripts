#!/usr/bin/env python3
"""Extract exact, provenance-bearing October and column-A style references."""

from __future__ import annotations

import hashlib
import json
import os
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = PROJECT_ROOT / "input_output_hp_rewriter_10_03_26/example_prompts"
DOCX_PATH = SOURCE_ROOT / "HP - mAIstro Prompt Guidance (Oct 2026).docx"
WORKBOOK_PATH = SOURCE_ROOT / "Eval-Set_Lifestyle-Photography_wSKUs.xlsx"
OCTOBER_EXTRACTION_PATH = PROJECT_ROOT / "research/source_messaging_v1_to_v6/data/october_guidance.json"
OUTPUT_PATH = PROJECT_ROOT / "research/diversity_aware_v3/data/style_reference_audit.json"

SPREADSHEET_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def extract_docx_paragraphs(path: Path) -> list[dict[str, object]]:
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    paragraphs = []
    for index, paragraph in enumerate(root.iter(f"{{{WORD_NS}}}p"), 1):
        text = "".join(node.text or "" for node in paragraph.iter(f"{{{WORD_NS}}}t"))
        if text:
            paragraphs.append({"paragraph": index, "text": text})
    return paragraphs


def workbook_column_a(path: Path, sheet_name: str) -> dict[int, str]:
    with zipfile.ZipFile(path) as archive:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in root.findall(f"{{{SPREADSHEET_NS}}}si"):
                shared_strings.append(
                    "".join(node.text or "" for node in item.iter(f"{{{SPREADSHEET_NS}}}t"))
                )

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {
            item.attrib["Id"]: item.attrib["Target"]
            for item in relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
        }
        sheet_path = None
        for sheet in workbook.iter(f"{{{SPREADSHEET_NS}}}sheet"):
            if sheet.attrib.get("name") == sheet_name:
                target = targets[sheet.attrib[f"{{{OFFICE_REL_NS}}}id"]]
                sheet_path = target if target.startswith("xl/") else f"xl/{target.lstrip('/')}"
                break
        if not sheet_path:
            raise ValueError(f"Worksheet not found: {sheet_name}")

        root = ET.fromstring(archive.read(sheet_path))
        values: dict[int, str] = {}
        for cell in root.iter(f"{{{SPREADSHEET_NS}}}c"):
            reference = cell.attrib.get("r", "")
            match = re.fullmatch(r"A([0-9]+)", reference)
            if not match:
                continue
            row = int(match.group(1))
            cell_type = cell.attrib.get("t")
            if cell_type == "inlineStr":
                value = "".join(
                    node.text or "" for node in cell.iter(f"{{{SPREADSHEET_NS}}}t")
                )
            else:
                value_node = cell.find(f"{{{SPREADSHEET_NS}}}v")
                if value_node is None or value_node.text is None:
                    continue
                value = (
                    shared_strings[int(value_node.text)]
                    if cell_type == "s"
                    else value_node.text
                )
            values[row] = value
    return values


def device_family(text: str) -> str | None:
    if "NOTEBOOK-" in text:
        return "laptop"
    if "PRINT-" in text:
        return "printer"
    if "DESKTOP-" in text:
        return "desktop"
    return None


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def main() -> None:
    docx_sha = sha256_path(DOCX_PATH)
    workbook_sha = sha256_path(WORKBOOK_PATH)
    paragraphs = extract_docx_paragraphs(DOCX_PATH)
    stored_extraction = json.loads(OCTOBER_EXTRACTION_PATH.read_text(encoding="utf-8"))
    if stored_extraction["sha256"] != docx_sha:
        raise ValueError("Stored October extraction targets a different DOCX")
    if stored_extraction["paragraphs"] != paragraphs:
        raise ValueError("Stored October paragraph extraction differs from DOCX bytes")

    by_paragraph = {item["paragraph"]: item["text"] for item in paragraphs}
    subsettings = [
        ("corporate_office", 5, [6, 7, 8], ["laptop"]),
        ("home_workspace", 9, [10, 11, 12], ["laptop", "printer"]),
        ("coffee_shop", 13, [14, 15], ["laptop"]),
        ("creative_studio", 16, [17, 18], ["laptop"]),
    ]
    october_examples = []
    october_subsettings = []
    for subsetting_id, heading_paragraph, example_paragraphs, compatible_families in subsettings:
        heading = by_paragraph[heading_paragraph]
        october_subsettings.append(
            {
                "subsetting_id": subsetting_id,
                "heading_paragraph": heading_paragraph,
                "heading_text": heading,
                "compatible_device_families": compatible_families,
                "example_paragraphs": example_paragraphs,
            }
        )
        for paragraph in example_paragraphs:
            text = by_paragraph[paragraph]
            family = text.split(":", 1)[0].lower()
            october_examples.append(
                {
                    "subsetting_id": subsetting_id,
                    "paragraph": paragraph,
                    "device_family": family,
                    "text": text,
                    "text_sha256": sha256_bytes(text.encode("utf-8")),
                }
            )

    column_a = workbook_column_a(WORKBOOK_PATH, "Eval Set Prompts")
    if column_a.get(1) != "BASE PROMPTS – NO VISUAL STYLE MENTIONS":
        raise ValueError("Unexpected column-A header")
    excerpts = []
    exclusions = []
    for row in sorted(key for key in column_a if key > 1):
        text = column_a[row]
        family = device_family(text)
        if family in {"laptop", "printer"}:
            excerpts.append(
                {
                    "cell": f"A{row}",
                    "row": row,
                    "device_family": family,
                    "text": text,
                    "text_sha256": sha256_bytes(text.encode("utf-8")),
                }
            )
        else:
            exclusions.append(
                {
                    "cell": f"A{row}",
                    "detected_device_family": family,
                    "reason": "Outside the authorized laptop/printer V3 source families.",
                }
            )
    family_counts = {
        family: sum(item["device_family"] == family for item in excerpts)
        for family in ("laptop", "printer")
    }

    output = {
        "version": "hp-diversity-style-reference-audit-v1",
        "as_of_date": "2026-10-23",
        "claim_status": "VERIFIED",
        "scope": {
            "purpose": "Exact style-reference evidence for the separate V3 diversity evaluation.",
            "authorized_device_families": ["laptop", "printer"],
            "authorized_source_counts": {"laptop": 3, "printer": 6},
            "runtime_identity_rule": "Tag-only; product names in historical excerpts are provenance text and are not runtime inputs.",
        },
        "sources": {
            "october_guidance_docx": {
                "path": str(DOCX_PATH),
                "sha256": docx_sha,
                "bytes": DOCX_PATH.stat().st_size,
                "source_class": "primary internal artifact",
                "document_title": by_paragraph[1],
                "document_period": "October 2026",
            },
            "verified_october_extraction": {
                "path": str(OCTOBER_EXTRACTION_PATH),
                "sha256": sha256_path(OCTOBER_EXTRACTION_PATH),
                "verification": "Paragraph list exactly matches direct DOCX XML extraction.",
            },
            "lifestyle_workbook": {
                "path": str(WORKBOOK_PATH),
                "sha256": workbook_sha,
                "bytes": WORKBOOK_PATH.stat().st_size,
                "source_class": "primary internal artifact",
                "worksheet": "Eval Set Prompts",
                "text_column": "A only",
                "header_cell": "A1",
                "header_text": column_a[1],
            },
        },
        "october_guidance": {
            "reusable_template": {
                "paragraph": 3,
                "text": by_paragraph[3],
                "text_sha256": sha256_bytes(by_paragraph[3].encode("utf-8")),
            },
            "optional_blue_carrier_modifier": {
                "paragraph": 4,
                "text": by_paragraph[4],
                "text_sha256": sha256_bytes(by_paragraph[4].encode("utf-8")),
                "interpretation": "The source introduces this with 'To increase'; it is optional rather than a universal requirement.",
            },
            "compatible_allowed_subsettings": october_subsettings,
            "sample_prompts": october_examples,
            "sample_prompt_count": len(october_examples),
        },
        "workbook_column_a": {
            "extraction_rule": "Only exact cell text from column A of worksheet 'Eval Set Prompts'; columns B through F and worksheet 'Theme Styles' are not excerpt sources.",
            "compatible_excerpt_count": len(excerpts),
            "compatible_excerpt_counts_by_device_family": family_counts,
            "compatible_excerpts": excerpts,
            "excluded_cells": exclusions,
            "observed_source_qualification": "Some included column-A cells contain explicit visual-style language even though A1 says 'NO VISUAL STYLE MENTIONS'; exact source text is preserved without normalizing that inconsistency.",
        },
        "usage_constraints": [
            "Use these snippets as reference evidence, not as a runtime product-identity source.",
            "The requested camera tag remains authoritative; do not copy a historical shot or angle instruction that conflicts with the selected V3 tag.",
            "Preserve creative departures as explicit labels instead of presenting them as source-supported facts.",
            "Do not automatically apply the optional blue-carrier modifier to every candidate.",
            "Do not import workbook columns D through F or the Theme Styles worksheet through this audit artifact.",
        ],
        "limitations": [
            "Workbook excerpt compatibility is limited to device-family tokens present in column A: NOTEBOOK- maps to laptop and PRINT- maps to printer.",
            "The excerpts retain historical product tokens and human descriptions verbatim; downstream V3 runtime inputs remain tag-only.",
            "This artifact does not define the V3 prompt, ranking rubric, or candidate-selection policy.",
        ],
    }
    atomic_json(OUTPUT_PATH, output)
    print(
        json.dumps(
            {
                "output": str(OUTPUT_PATH),
                "sha256": sha256_path(OUTPUT_PATH),
                "october_sample_prompts": len(october_examples),
                "column_a_compatible_excerpts": len(excerpts),
                "family_counts": family_counts,
                "excluded_cells": len(exclusions),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
