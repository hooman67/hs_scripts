#!/usr/bin/env python3
"""Compile camera-v2's prompt template with compact deterministic registry notes."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from camera_profile_resolver import PROFILE_FIELDS, load_registry, validate_registry


HERE = Path(__file__).resolve().parent
DEFAULT_REGISTRY = HERE / "camera_profiles.json"
DEFAULT_TEMPLATE = HERE / "system_prompt.template.md"
DEFAULT_OUTPUT = HERE / "system_prompt.md"
PLACEHOLDER = "{{OFFLINE_NOTES}}"


def inline_code(value: Any) -> str:
    escaped = str(value).replace("`", "\\`")
    return f"`{escaped}`"


def joined_codes(values: list[Any]) -> str:
    return ", ".join(inline_code(value) for value in values) if values else "none"


def _profile_signature(profile: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(profile[field] for field in PROFILE_FIELDS)


def _camera_profile_lines(
    registry: dict[str, Any], common_profile_notes: set[str]
) -> list[str]:
    by_source: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    source_order: list[str] = []
    for profile in registry["profiles"]:
        source = profile["source_camera_name"]
        if source not in by_source:
            source_order.append(source)
        if profile["device_family"] in by_source[source]:
            raise ValueError(
                "multiple profiles for source camera and device type: "
                f"{source!r}/{profile['device_family']!r}"
            )
        by_source[source][profile["device_family"]] = profile

    lines = [
        "### Camera base profiles",
        "",
        "Each row gives exact registered tag(s), source camera name, framing, elevation, local-prop ceiling, background-detail ceiling, and people policy. Equal limits across registered device types are written once while every exact tag remains explicit.",
        "",
    ]
    for source in source_order:
        profiles = [
            by_source[source][device_type]
            for device_type in registry["device_types"]
            if device_type in by_source[source]
        ]
        grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
        for profile in profiles:
            grouped.setdefault(_profile_signature(profile), []).append(profile)
        for matching_profiles in grouped.values():
            profile = matching_profiles[0]
            tags = [item["tag"] for item in matching_profiles]
            line = (
                f"- {joined_codes(tags)}; source={inline_code(source)}; "
                f"framing={inline_code(profile['framing'])}; elevation={inline_code(profile['elevation'])}; "
                f"props<={profile['max_local_props']}; background<={profile['max_background_details']}; "
                f"people={inline_code(profile['people_policy'])}."
            )
            scoped_notes = []
            for item in matching_profiles:
                for note in item.get("notes", []):
                    if note not in common_profile_notes:
                        scoped_notes.append(f"{inline_code(item['tag'])}: {note}")
            if scoped_notes:
                line += " Tag-scoped notes: " + " ".join(scoped_notes)
            lines.append(line)
    return lines


def build_offline_notes(registry: dict[str, Any]) -> str:
    validate_registry(registry)
    approval_by_family: dict[str, set[str]] = defaultdict(set)
    review_bases: list[str] = []
    note_tags: dict[str, set[str]] = defaultdict(set)
    for profile in registry["profiles"]:
        approval_by_family[profile["device_family"]].add(profile["source_approval_status"])
        if profile["review_basis"] not in review_bases:
            review_bases.append(profile["review_basis"])
        for note in profile.get("notes", []):
            note_tags[note].add(profile["tag"])
    common_profile_notes = {
        note for note, tags in note_tags.items() if len(tags) == len(registry["profiles"])
    }

    lines = [
        f"Registry version: {inline_code(registry['version'])}.",
        f"Registry status: {inline_code(registry['status'])}.",
        f"Registered device types: {joined_codes(registry['device_types'])}.",
        f"Runtime image analysis: {inline_code(str(registry.get('runtime_image_analysis', False)).lower())}.",
        f"Fixed presets user-confirmed: {inline_code(str(registry.get('fixed_presets_user_confirmed', False)).lower())}.",
        f"Source catalog: {inline_code(registry.get('source_catalog', ''))}.",
        "",
        "### Exact matching and unresolved inputs",
        "",
        "- Compare canonical type-camera tags after case folding and trimming surrounding whitespace only. Do not remove or collapse internal characters. A normalized canonical match is `exact`; only an explicit registry alias is `alias`.",
        f"- Explicit camera aliases (alias -> canonical): {joined_codes([f'{alias} -> {target}' for alias, target in registry['aliases'].items()])}.",
        f"- Unknown/missing camera policy: {inline_code(registry['unknown_tag_policy'])}.",
        "- Resolve device type only from the registered tag. Never infer it from source messaging or translate a tag across device types.",
        "",
        "### Registry evidence boundaries",
        "",
        f"- Review basis: {joined_codes(review_bases)}.",
    ]
    for device_type in registry["device_types"]:
        lines.append(
            f"- {device_type} source approval status: "
            f"{joined_codes(sorted(approval_by_family[device_type]))}."
        )
    for note in sorted(common_profile_notes):
        lines.append(f"- {note}")
    for limitation in registry.get("limitations", []):
        lines.append(f"- Limitation: {limitation}")
    lines.extend([""] + _camera_profile_lines(registry, common_profile_notes))
    return "\n".join(lines).rstrip() + "\n"


def compile_prompt(template: str, registry: dict[str, Any]) -> str:
    count = template.count(PLACEHOLDER)
    if count != 1:
        raise ValueError(f"template must contain exactly one {PLACEHOLDER}; found {count}")
    notes = build_offline_notes(registry).rstrip()
    return template.replace(PLACEHOLDER, notes).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if output does not already match deterministic compilation",
    )
    args = parser.parse_args()
    registry = load_registry(args.registry)
    template = args.template.read_text(encoding="utf-8")
    compiled = compile_prompt(template, registry)
    if args.check:
        existing = args.output.read_text(encoding="utf-8") if args.output.exists() else None
        if existing != compiled:
            raise SystemExit(f"compiled output is stale or missing: {args.output}")
    else:
        args.output.write_text(compiled, encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "characters": len(compiled),
                "sha256": hashlib.sha256(compiled.encode("utf-8")).hexdigest(),
                "registry_version": registry["version"],
                "check": args.check,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
