#!/usr/bin/env python3
"""Losslessly inventory and normalize the bounded V5 dual-source inputs.

Only Python's standard library is used. The script copies source files from the
volatile input directory into the durable project tree without overwriting an
existing different file, verifies every copy by SHA-256, and emits auditable
JSON extractions for TXT, DOCX, and XLSX inputs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
from typing import Any, Iterable
import xml.etree.ElementTree as ET
import zipfile


EXPECTED_FOLDERS = ("Cashmere", "Deskjet 2955", "Elitebook", "Laserjet", "Modric")

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
X_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"

W = f"{{{W_NS}}}"
X = f"{{{X_NS}}}"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    path.write_text(rendered, encoding="utf-8")


def classify_role(name: str) -> str:
    lowered = name.lower().replace("-", "_").replace(" ", "_")
    if "source_messaging" in lowered or "source_etail_messaging" in lowered:
        return "source_messaging"
    if "source" in lowered and "messaging" in lowered:
        return "source_messaging"
    if "smartbrief" in lowered or "smart_brief" in lowered:
        return "smart_brief"
    return "unclassified"


def decoded_text_lines(text: str) -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = []
    start = 0
    for line_number, line_with_ending in enumerate(text.splitlines(keepends=True), start=1):
        ending = ""
        content = line_with_ending
        if line_with_ending.endswith("\r\n"):
            ending = "\r\n"
            content = line_with_ending[:-2]
        elif line_with_ending.endswith(("\r", "\n")):
            ending = line_with_ending[-1]
            content = line_with_ending[:-1]
        end = start + len(line_with_ending)
        lines.append(
            {
                "line_number": line_number,
                "char_start": start,
                "char_end": end,
                "text": content,
                "line_ending": ending,
            }
        )
        start = end
    if not text or (text and not text.endswith(("\r", "\n")) and not lines):
        lines.append(
            {
                "line_number": 1,
                "char_start": 0,
                "char_end": len(text),
                "text": text,
                "line_ending": "",
            }
        )
    return lines


def extract_txt(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
        encoding = "utf-8-sig"
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="surrogateescape")
        encoding = "utf-8-surrogateescape"

    result: dict[str, Any] = {
        "format": "txt",
        "encoding": encoding,
        "decoded_character_count": len(text),
        "raw_text": text,
        "lines": decoded_text_lines(text),
    }
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        result["json_parse"] = {
            "valid": False,
            "error": exc.msg,
            "line": exc.lineno,
            "column": exc.colno,
            "character": exc.pos,
        }
    else:
        result["json_parse"] = {"valid": True}
        result["json_value"] = parsed
    return result


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def paragraph_segments(paragraph: ET.Element) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []

    def visit(node: ET.Element, ancestry: tuple[str, ...]) -> None:
        name = local_name(node.tag)
        next_ancestry = ancestry + (name,)
        if node.tag in {W + "t", W + "delText", W + "instrText"}:
            kind = {
                W + "t": "text",
                W + "delText": "deleted_text",
                W + "instrText": "field_instruction",
            }[node.tag]
            segments.append(
                {
                    "kind": kind,
                    "text": node.text or "",
                    "xml_space": node.attrib.get("{http://www.w3.org/XML/1998/namespace}space"),
                    "revision_context": [
                        part for part in ancestry if part in {"ins", "del", "moveFrom", "moveTo"}
                    ],
                }
            )
            return
        if node.tag == W + "tab":
            segments.append({"kind": "tab", "text": "\t", "revision_context": []})
            return
        if node.tag in {W + "br", W + "cr"}:
            segments.append({"kind": "break", "text": "\n", "revision_context": []})
            return
        if node.tag in {W + "noBreakHyphen", W + "softHyphen"}:
            segments.append(
                {
                    "kind": local_name(node.tag),
                    "text": "‑" if node.tag == W + "noBreakHyphen" else "\u00ad",
                    "revision_context": [],
                }
            )
            return
        for child in node:
            visit(child, next_ancestry)

    visit(paragraph, ())
    return segments


def paragraph_record(paragraph: ET.Element, provenance: str) -> dict[str, Any]:
    style_node = paragraph.find(f"./{W}pPr/{W}pStyle")
    style = style_node.attrib.get(W + "val") if style_node is not None else None
    segments = paragraph_segments(paragraph)
    return {
        "block_type": "paragraph",
        "provenance": provenance,
        "style": style,
        "text": "".join(segment["text"] for segment in segments),
        "segments": segments,
    }


def blocks_from_container(container: ET.Element, provenance: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    block_index = 0
    for child in container:
        if child.tag == W + "p":
            block_index += 1
            blocks.append(paragraph_record(child, f"{provenance}/block[{block_index}]/paragraph"))
        elif child.tag == W + "tbl":
            block_index += 1
            blocks.append(table_record(child, f"{provenance}/block[{block_index}]/table"))
    return blocks


def table_record(table: ET.Element, provenance: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for row_index, row in enumerate(table.findall(f"./{W}tr"), start=1):
        cells: list[dict[str, Any]] = []
        for cell_index, cell in enumerate(row.findall(f"./{W}tc"), start=1):
            cell_provenance = f"{provenance}/row[{row_index}]/cell[{cell_index}]"
            cell_blocks = blocks_from_container(cell, cell_provenance)
            cells.append(
                {
                    "cell_index": cell_index,
                    "provenance": cell_provenance,
                    "text": "\n".join(
                        block.get("text", "")
                        if block["block_type"] == "paragraph"
                        else table_plain_text(block)
                        for block in cell_blocks
                    ),
                    "blocks": cell_blocks,
                }
            )
        rows.append({"row_index": row_index, "cells": cells})
    return {"block_type": "table", "provenance": provenance, "rows": rows}


def table_plain_text(table: dict[str, Any]) -> str:
    return "\n".join(
        "\t".join(cell["text"] for cell in row["cells"]) for row in table["rows"]
    )


def walk_docx_blocks(blocks: list[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    for block in blocks:
        yield block
        if block["block_type"] == "table":
            for row in block["rows"]:
                for cell in row["cells"]:
                    yield from walk_docx_blocks(cell["blocks"])


def extract_docx(path: Path) -> dict[str, Any]:
    stories: list[dict[str, Any]] = []
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        candidate_names = ["word/document.xml"]
        candidate_names += sorted(
            name
            for name in names
            if re.fullmatch(r"word/(?:header\d+|footer\d+|footnotes|endnotes|comments)\.xml", name)
        )
        for story_name in candidate_names:
            if story_name not in names:
                continue
            root = ET.fromstring(archive.read(story_name))
            if story_name == "word/document.xml":
                container = root.find(f"./{W}body")
            else:
                container = root
            if container is None:
                blocks: list[dict[str, Any]] = []
            else:
                blocks = blocks_from_container(container, story_name)
            flat_blocks = list(walk_docx_blocks(blocks))
            # The hierarchical body/table walk above is convenient for consumers, but
            # OOXML may wrap paragraphs in structured-document tags, text boxes, or
            # other containers. These flat XML-order inventories are the completeness
            # gate: every w:p and w:tbl in every story part is represented exactly once.
            all_paragraphs = [
                paragraph_record(paragraph, f"{story_name}/xml_paragraph[{index}]")
                for index, paragraph in enumerate(root.iter(W + "p"), start=1)
            ]
            all_tables = [
                table_record(table, f"{story_name}/xml_table[{index}]")
                for index, table in enumerate(root.iter(W + "tbl"), start=1)
            ]
            stories.append(
                {
                    "story_part": story_name,
                    "blocks": blocks,
                    "hierarchical_block_paragraph_count": sum(
                        block["block_type"] == "paragraph" for block in flat_blocks
                    ),
                    "hierarchical_block_table_count": sum(
                        block["block_type"] == "table" for block in flat_blocks
                    ),
                    "all_paragraphs_xml_order": all_paragraphs,
                    "all_tables_xml_order": all_tables,
                    "paragraph_count": len(all_paragraphs),
                    "table_count": len(all_tables),
                }
            )
    return {
        "format": "docx",
        "stories": stories,
        "paragraph_count": sum(story["paragraph_count"] for story in stories),
        "table_count": sum(story["table_count"] for story in stories),
    }


def relationship_targets(xml_bytes: bytes) -> dict[str, str]:
    root = ET.fromstring(xml_bytes)
    return {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in root.findall(f".//{{{PKG_REL_NS}}}Relationship")
    }


def shared_string_value(si: ET.Element) -> str:
    return "".join(node.text or "" for node in si.iter(X + "t"))


def resolve_xlsx_target(target: str) -> str:
    target_path = PurePosixPath(target)
    if target_path.is_absolute():
        return str(target_path).lstrip("/")
    combined = PurePosixPath("xl") / target_path
    parts: list[str] = []
    for part in combined.parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part != ".":
            parts.append(part)
    return "/".join(parts)


def extract_xlsx(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in names:
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared_strings = [shared_string_value(si) for si in shared_root.findall(f"./{X}si")]

        rel_targets = relationship_targets(archive.read("xl/_rels/workbook.xml.rels"))
        workbook_root = ET.fromstring(archive.read("xl/workbook.xml"))
        sheets: list[dict[str, Any]] = []
        for sheet_index, sheet in enumerate(workbook_root.findall(f"./{X}sheets/{X}sheet"), start=1):
            name = sheet.attrib["name"]
            rel_id = sheet.attrib[f"{{{R_NS}}}id"]
            target = resolve_xlsx_target(rel_targets[rel_id])
            sheet_root = ET.fromstring(archive.read(target))
            cells: list[dict[str, Any]] = []
            for cell in sheet_root.findall(f".//{X}sheetData/{X}row/{X}c"):
                coordinate = cell.attrib.get("r")
                cell_type = cell.attrib.get("t")
                style_index = cell.attrib.get("s")
                formula_node = cell.find(f"./{X}f")
                value_node = cell.find(f"./{X}v")
                inline_node = cell.find(f"./{X}is")
                formula = formula_node.text if formula_node is not None else None
                raw_value = value_node.text if value_node is not None else None
                value: Any = raw_value
                if cell_type == "s" and raw_value is not None:
                    try:
                        shared_index = int(raw_value)
                        value = shared_strings[shared_index]
                    except (ValueError, IndexError):
                        value = None
                elif cell_type == "inlineStr" and inline_node is not None:
                    value = "".join(node.text or "" for node in inline_node.iter(X + "t"))
                elif cell_type == "b" and raw_value is not None:
                    value = raw_value == "1"
                if formula is None and (value is None or value == ""):
                    continue
                cells.append(
                    {
                        "coordinate": coordinate,
                        "provenance": f"{name}!{coordinate}",
                        "cell_type": cell_type,
                        "style_index": style_index,
                        "formula": formula,
                        "raw_value": raw_value,
                        "value": value,
                    }
                )
            sheets.append(
                {
                    "sheet_index": sheet_index,
                    "sheet_name": name,
                    "source_part": target,
                    "nonempty_cell_count": len(cells),
                    "cells": cells,
                }
            )
    return {
        "format": "xlsx",
        "sheet_count": len(sheets),
        "sheets": sheets,
        "nonempty_cell_count": sum(sheet["nonempty_cell_count"] for sheet in sheets),
    }


def extract_file(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return extract_txt(path)
    if suffix == ".docx":
        return extract_docx(path)
    if suffix == ".xlsx":
        return extract_xlsx(path)
    raise ValueError(f"unsupported input extension: {path}")


def plain_strings(value: Any, provenance: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        yield provenance, value
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from plain_strings(item, f"{provenance}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from plain_strings(item, f"{provenance}.{key}")


def instruction_candidates(extraction: dict[str, Any]) -> list[dict[str, Any]]:
    patterns = {
        "instruction_or_prompt": re.compile(r"\b(?:system instructions?|developer instructions?|prompt instructions?|ignore previous|ignore all|you are (?:an?|the)|assistant:)\b", re.I),
        "chat_metadata": re.compile(r"\b(?:_chatSession|chat session|system prompt|user prompt)\b", re.I),
    }
    candidates: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for provenance, text in plain_strings(extraction):
        for category, pattern in patterns.items():
            match = pattern.search(text)
            if match is None:
                continue
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 180)
            key = (category, provenance, text[start:end])
            if key in seen:
                continue
            seen.add(key)
            candidates.append(
                {
                    "category": category,
                    "provenance": provenance,
                    "matched_text": match.group(0),
                    "context": text[start:end],
                }
            )
    return candidates


def extraction_stats(extraction: dict[str, Any]) -> dict[str, Any]:
    fmt = extraction["format"]
    if fmt == "txt":
        return {
            "format": fmt,
            "characters": extraction["decoded_character_count"],
            "lines": len(extraction["lines"]),
            "valid_json": extraction["json_parse"]["valid"],
        }
    if fmt == "docx":
        paragraph_texts = [
            paragraph["text"]
            for story in extraction["stories"]
            for paragraph in story["all_paragraphs_xml_order"]
        ]
        return {
            "format": fmt,
            "stories": len(extraction["stories"]),
            "paragraphs": extraction["paragraph_count"],
            "tables": extraction["table_count"],
            "paragraph_text_characters": sum(len(text) for text in paragraph_texts),
        }
    if fmt == "xlsx":
        value_character_count = sum(
            len(str(cell["value"]))
            for sheet in extraction["sheets"]
            for cell in sheet["cells"]
            if cell["value"] is not None
        )
        return {
            "format": fmt,
            "sheets": extraction["sheet_count"],
            "nonempty_cells": extraction["nonempty_cell_count"],
            "value_characters": value_character_count,
            "sheet_names": [sheet["sheet_name"] for sheet in extraction["sheets"]],
        }
    raise AssertionError(fmt)


def safe_output_stem(path: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "_", path.stem.lower()).strip("_")


def copy_verified(source: Path, destination: Path) -> tuple[str, str]:
    source_hash = sha256(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination_hash = sha256(destination)
        if destination_hash != source_hash:
            raise RuntimeError(f"refusing to overwrite different existing file: {destination}")
        status = "already_present_identical"
    else:
        shutil.copy2(source, destination)
        destination_hash = sha256(destination)
        status = "copied"
    if destination.stat().st_size != source.stat().st_size or destination_hash != source_hash:
        raise RuntimeError(f"copy verification failed: {source} -> {destination}")
    return source_hash, status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()

    source_root = args.source_root.resolve()
    output_root = args.output_root.resolve()
    originals_root = output_root / "inputs" / "originals"
    normalized_root = output_root / "inputs" / "normalized"
    run_time = utc_now()

    source_folders = sorted(path.name for path in source_root.iterdir() if path.is_dir())
    if source_folders != sorted(EXPECTED_FOLDERS):
        raise RuntimeError(
            f"bounded folder set changed: expected {sorted(EXPECTED_FOLDERS)}, got {source_folders}"
        )

    originals_manifest_files: list[dict[str, Any]] = []
    extraction_manifest_files: list[dict[str, Any]] = []
    pairs: list[dict[str, Any]] = []

    for folder_name in EXPECTED_FOLDERS:
        folder = source_root / folder_name
        source_files = sorted(path for path in folder.iterdir() if path.is_file())
        if len(source_files) != 2:
            raise RuntimeError(f"expected exactly two files in {folder}, found {len(source_files)}")
        pair_files: list[dict[str, Any]] = []
        roles: list[str] = []
        for source in source_files:
            role = classify_role(source.name)
            roles.append(role)
            destination = originals_root / folder_name / source.name
            source_hash, copy_status = copy_verified(source, destination)
            relative_original = destination.relative_to(output_root).as_posix()
            file_id = source_hash[:16]
            extraction = extract_file(destination)
            extraction["source_file"] = {
                "file_id": file_id,
                "folder": folder_name,
                "role": role,
                "filename": source.name,
                "durable_original": relative_original,
                "sha256": source_hash,
                "size_bytes": source.stat().st_size,
            }
            candidates = instruction_candidates(extraction)
            normalized_filename = f"{role}__{safe_output_stem(source)}__{file_id}.json"
            normalized_path = normalized_root / "files" / normalized_filename
            write_json(normalized_path, extraction)
            normalized_relative = normalized_path.relative_to(output_root).as_posix()

            originals_manifest_files.append(
                {
                    "file_id": file_id,
                    "folder": folder_name,
                    "role": role,
                    "source_path": str(source),
                    "durable_path": str(destination),
                    "relative_durable_path": relative_original,
                    "size_bytes": source.stat().st_size,
                    "sha256": source_hash,
                    "copy_status": copy_status,
                    "copy_verified": True,
                }
            )
            file_manifest_record = {
                "file_id": file_id,
                "folder": folder_name,
                "role": role,
                "filename": source.name,
                "sha256": source_hash,
                "normalized_path": normalized_relative,
                "stats": extraction_stats(extraction),
                "potential_hidden_instruction_candidates": candidates,
            }
            extraction_manifest_files.append(file_manifest_record)
            pair_files.append(file_manifest_record)

        if sorted(roles) != ["smart_brief", "source_messaging"]:
            raise RuntimeError(f"could not identify one brief and one source-messaging file in {folder}")
        pair_id = re.sub(r"[^a-z0-9]+", "_", folder_name.lower()).strip("_")
        pair_record = {
            "pair_id": pair_id,
            "source_folder": folder_name,
            "pairing_basis": "exactly one smart-brief role and one source-messaging role in the same supplied folder",
            "structural_pair_confidence": "high",
            "files": sorted(pair_files, key=lambda item: item["role"]),
        }
        pair_path = normalized_root / "pairs" / f"{pair_id}.json"
        write_json(pair_path, pair_record)
        pair_record["normalized_pair_path"] = pair_path.relative_to(output_root).as_posix()
        pairs.append(pair_record)

    originals_manifest = {
        "manifest_schema_version": 1,
        "created_at": run_time,
        "source_root": str(source_root),
        "durable_originals_root": str(originals_root),
        "source_storage": "volatile /mnt/localssd",
        "destination_storage": "backed-up /home/colligo checkout",
        "copy_policy": "non-destructive; refuse overwrite when bytes differ",
        "verification": "source and durable copy size plus SHA-256 equality",
        "folder_count": len(EXPECTED_FOLDERS),
        "file_count": len(originals_manifest_files),
        "files": originals_manifest_files,
        "restore_procedure": (
            "Use relative_durable_path entries beneath the V5 output root; verify SHA-256 before "
            "copying to any restored scratch location."
        ),
    }
    write_json(output_root / "inputs" / "originals_manifest.json", originals_manifest)

    extraction_manifest = {
        "manifest_schema_version": 1,
        "created_at": run_time,
        "extractor": str(Path(__file__).resolve()),
        "python_version": sys.version.split()[0],
        "normalization_contract": {
            "txt": "complete decoded text and line provenance; parsed JSON included only when valid",
            "docx": "all main/header/footer/footnote/endnote/comment paragraphs and tables in document order",
            "xlsx": "all workbook sheets in workbook order and every nonempty cell with coordinate, type, formula, raw and decoded value",
        },
        "files": extraction_manifest_files,
        "pairs": pairs,
    }
    write_json(output_root / "inputs" / "normalized" / "extraction_manifest.json", extraction_manifest)
    print(json.dumps({"files": len(extraction_manifest_files), "pairs": len(pairs), "output": str(output_root)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
