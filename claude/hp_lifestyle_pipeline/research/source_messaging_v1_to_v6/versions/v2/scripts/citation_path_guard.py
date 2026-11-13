#!/usr/bin/env python3
"""Deterministically normalize uniquely recoverable debug evidence paths."""

from __future__ import annotations

import copy
from typing import Any


def _pointer_escape(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _direct_path_value(
    source_messaging: dict[str, Any], block_name: str, path: Any
) -> Any:
    if not isinstance(path, str):
        return None
    parts = path.split(".")
    if len(parts) != 2 or parts[0] != block_name:
        return None
    block = source_messaging.get(block_name)
    if not isinstance(block, dict):
        return None
    return block.get(parts[1])


def _normalize_items(
    *,
    source_messaging: dict[str, Any],
    block_name: str,
    items: Any,
    pointer_base: str,
    repairs: list[dict[str, Any]],
    failures: list[dict[str, Any]],
) -> None:
    if not isinstance(items, list):
        return
    block = source_messaging.get(block_name)
    direct_strings = (
        {
            field: value
            for field, value in block.items()
            if isinstance(field, str) and isinstance(value, str)
        }
        if isinstance(block, dict)
        else {}
    )
    for item_index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        quote = item.get("quote")
        from_path = item.get("path")
        pointer = f"{pointer_base}/{item_index}/path"
        declared_parts = from_path.split(".") if isinstance(from_path, str) else []
        if len(declared_parts) != 2 or declared_parts[0] != block_name:
            failures.append(
                {
                    "json_pointer": pointer,
                    "declared_path": from_path,
                    "quote": quote,
                    "reason": "citation_path_wrong_scope",
                    "intended_scope": block_name,
                    "matching_paths": [],
                }
            )
            continue
        declared_value = _direct_path_value(
            source_messaging, block_name, from_path
        )
        if (
            isinstance(quote, str)
            and isinstance(declared_value, str)
            and quote in declared_value
        ):
            continue
        matches = [
            field
            for field, value in direct_strings.items()
            if isinstance(quote, str) and quote in value
        ]
        if len(matches) == 1:
            to_path = f"{block_name}.{matches[0]}"
            item["path"] = to_path
            repairs.append(
                {
                    "json_pointer": pointer,
                    "from_path": from_path,
                    "to_path": to_path,
                    "quote": quote,
                }
            )
            continue
        failures.append(
            {
                "json_pointer": pointer,
                "declared_path": from_path,
                "quote": quote,
                "reason": (
                    "citation_quote_not_found_in_intended_message"
                    if not matches
                    else "citation_quote_matches_multiple_fields_in_intended_message"
                ),
                "matching_paths": [f"{block_name}.{field}" for field in matches],
            }
        )


def normalize_citation_paths(
    output: dict[str, Any], source_messaging: dict[str, Any]
) -> dict[str, Any]:
    """Return a deep-copied output plus transparent path repairs/failures.

    A path is repaired only when its verbatim quote occurs in exactly one direct
    string field of the same KSP or ValueProposition object. Quotes and all
    non-path output content remain unchanged.
    """

    normalized = copy.deepcopy(output)
    repairs: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    debug = normalized.get("debug")
    if not isinstance(debug, dict):
        return {
            "validated_output": normalized,
            "citation_repairs": repairs,
            "failures": failures,
        }

    mappings = debug.get("ksp_mappings")
    if isinstance(mappings, list):
        for mapping_index, mapping in enumerate(mappings):
            if not isinstance(mapping, dict):
                continue
            block_name = mapping.get("ksp_id")
            if not isinstance(block_name, str):
                continue
            _normalize_items(
                source_messaging=source_messaging,
                block_name=block_name,
                items=mapping.get("source_evidence"),
                pointer_base=(
                    "/debug/ksp_mappings/"
                    f"{mapping_index}/source_evidence"
                ),
                repairs=repairs,
                failures=failures,
            )

    value_proposition = debug.get("value_proposition")
    if isinstance(value_proposition, dict):
        _normalize_items(
            source_messaging=source_messaging,
            block_name="ValueProposition",
            items=value_proposition.get("source_evidence"),
            pointer_base="/debug/value_proposition/source_evidence",
            repairs=repairs,
            failures=failures,
        )

    return {
        "validated_output": normalized,
        "citation_repairs": repairs,
        "failures": failures,
    }
