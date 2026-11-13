"""Load paired customer JSON without flattening content or extracting ZIP paths."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any
import zipfile


MAX_DOCUMENT_BYTES = 16 * 1024 * 1024


def _unique_keys(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> Any:
    raise ValueError(f"non-JSON numeric constant: {value}")


def _role(name: str) -> str:
    stem = Path(name).stem.casefold().replace("-", " ").replace("_", " ")
    if stem.startswith("smart brief"):
        return "smart_brief"
    if stem.startswith("source messaging"):
        return "source_messaging"
    raise ValueError(f"unrecognized paired JSON filename: {name}")


def load_pair(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    path = path.resolve()
    documents: dict[str, Any] = {}
    records: dict[str, Any] = {}

    def add(name: str, body: bytes, member: str | None) -> None:
        if len(body) > MAX_DOCUMENT_BYTES:
            raise ValueError(f"paired JSON exceeds byte limit: {name}")
        role = _role(name)
        if role in documents:
            raise ValueError(f"ambiguous duplicate {role} in {path}")
        value = json.loads(
            body, object_pairs_hook=_unique_keys, parse_constant=_invalid_constant
        )
        if not isinstance(value, dict):
            raise ValueError(f"{role} must be a JSON object: {name}")
        documents[role] = value
        records[role] = {
            "source_path": str(path if member else path / name),
            "archive_member": member,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
        }

    if path.is_dir():
        for source in sorted(path.iterdir()):
            if source.is_file() and source.suffix.casefold() == ".json":
                with source.open("rb") as stream:
                    add(source.name, stream.read(MAX_DOCUMENT_BYTES + 1), None)
    elif path.suffix.casefold() == ".zip":
        with zipfile.ZipFile(path) as archive:
            for item in archive.infolist():
                member_path = PurePosixPath(item.filename)
                if item.is_dir() or "__MACOSX" in member_path.parts:
                    continue
                if member_path.suffix.casefold() != ".json":
                    continue
                if member_path.is_absolute() or ".." in member_path.parts:
                    raise ValueError(f"unsafe archive member: {item.filename}")
                with archive.open(item) as stream:
                    add(member_path.name, stream.read(MAX_DOCUMENT_BYTES + 1), item.filename)
    else:
        raise ValueError(f"paired input must be a directory or ZIP bundle: {path}")
    if set(documents) != {"smart_brief", "source_messaging"}:
        raise ValueError(f"expected exactly one Smart Brief and source messaging in {path}")
    return documents, records
