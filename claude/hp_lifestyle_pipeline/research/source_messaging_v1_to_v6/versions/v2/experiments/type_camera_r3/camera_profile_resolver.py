#!/usr/bin/env python3
"""Deterministic offline resolver for the camera-v2 type-camera registry.

This module is validation/build tooling, not a runtime image analyzer. Matching
case-folds and trims surrounding whitespace only. Alternate names resolve only
when the registry declares them as explicit aliases.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_REGISTRY = HERE / "camera_profiles.json"

PROFILE_FIELDS = (
    "framing",
    "elevation",
    "max_local_props",
    "max_background_details",
    "people_policy",
)
MINIMAL_FALLBACK = {
    "framing": "unknown",
    "elevation": "unknown",
    "max_local_props": 0,
    "max_background_details": 0,
    "people_policy": "omit",
}


class RegistryError(ValueError):
    """Raised when registry structure or references are internally invalid."""


def load_registry(path: Path | str = DEFAULT_REGISTRY) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_lookup(value: Any) -> str | None:
    """Normalize only case and surrounding whitespace; do not infer names."""

    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped.casefold() if stripped else None


def _unique_index(
    items: list[dict[str, Any]], field: str, label: str
) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for item in items:
        value = item.get(field)
        key = normalize_lookup(value)
        if key is None:
            raise RegistryError(f"{label} has missing/blank {field}: {value!r}")
        if key in index:
            raise RegistryError(f"normalized duplicate {label} {field}: {value!r}")
        index[key] = item
    return index


def _declared_type(value: str, device_types: list[str]) -> str | None:
    stripped = value.strip()
    prefix = stripped.split("_", 1)[0] if "_" in stripped else None
    prefix_key = normalize_lookup(prefix)
    return next(
        (
            device_type
            for device_type in device_types
            if normalize_lookup(device_type) == prefix_key
        ),
        None,
    )


def _camera_alias_index(
    aliases: dict[str, Any],
    profile_index: dict[str, dict[str, Any]],
    device_types: list[str],
) -> dict[str, dict[str, Any]]:
    if not isinstance(aliases, dict):
        raise RegistryError("camera aliases must map aliases to canonical tags")
    index: dict[str, dict[str, Any]] = {}
    for alias, canonical in aliases.items():
        alias_key = normalize_lookup(alias)
        canonical_key = normalize_lookup(canonical)
        if alias_key is None or canonical_key is None:
            raise RegistryError(f"invalid camera alias: {alias!r} -> {canonical!r}")
        if canonical_key not in profile_index:
            raise RegistryError(f"camera alias target is not registered: {canonical!r}")
        if alias_key in profile_index or alias_key in index:
            raise RegistryError(f"camera alias collides after normalization: {alias!r}")
        target = profile_index[canonical_key]
        alias_type = _declared_type(alias, device_types)
        if alias_type is not None and alias_type != target["device_family"]:
            raise RegistryError(
                f"camera alias crosses device types: {alias!r} -> {canonical!r}"
            )
        index[alias_key] = target
    return index


def validate_registry(registry: dict[str, Any]) -> dict[str, Any]:
    required = {
        "version",
        "status",
        "device_types",
        "unknown_tag_policy",
        "aliases",
        "profiles",
    }
    missing = sorted(required - registry.keys())
    if missing:
        raise RegistryError(f"registry missing keys: {missing}")

    device_types = registry["device_types"]
    profiles = registry["profiles"]
    if (
        not isinstance(device_types, list)
        or not device_types
        or any(normalize_lookup(item) is None for item in device_types)
        or len({normalize_lookup(item) for item in device_types}) != len(device_types)
    ):
        raise RegistryError("device_types must be a nonempty array of unique strings")
    if not isinstance(profiles, list) or not profiles:
        raise RegistryError("profiles must be a nonempty array")

    profile_index = _unique_index(profiles, "tag", "profile")
    seen_source_type: set[tuple[str, str]] = set()
    for profile in profiles:
        absent = [
            field
            for field in ("source_camera_name", "device_family", *PROFILE_FIELDS)
            if field not in profile
        ]
        if absent:
            raise RegistryError(f"profile {profile['tag']!r} missing fields: {absent}")
        device_type = profile["device_family"]
        if device_type not in device_types:
            raise RegistryError(f"unknown device type in {profile['tag']!r}")
        if _declared_type(profile["tag"], device_types) != device_type:
            raise RegistryError(
                f"profile tag prefix disagrees with device type in {profile['tag']!r}"
            )
        source_type = (profile["source_camera_name"], device_type)
        if source_type in seen_source_type:
            raise RegistryError(
                "multiple profiles for source camera and device type: "
                f"{source_type[0]!r}/{source_type[1]!r}"
            )
        seen_source_type.add(source_type)
        for field in ("max_local_props", "max_background_details"):
            if not isinstance(profile[field], int) or profile[field] < 0:
                raise RegistryError(f"{profile['tag']!r} has invalid {field}")

    camera_aliases = _camera_alias_index(
        registry["aliases"], profile_index, device_types
    )
    return {
        "profiles": profile_index,
        "camera_aliases": camera_aliases,
        "device_types": tuple(device_types),
    }


def _requested_string(value: Any) -> str:
    return value if isinstance(value, str) else ""


def resolve_profile(registry: dict[str, Any], camera_tag: Any) -> dict[str, Any]:
    """Resolve one type-camera tag or return the conservative fallback."""

    indexes = validate_registry(registry)
    camera_key = normalize_lookup(camera_tag)
    profile = None
    resolution = "missing" if camera_key is None else "unknown"
    if camera_key in indexes["profiles"]:
        profile = indexes["profiles"][camera_key]
        resolution = "exact"
    elif camera_key in indexes["camera_aliases"]:
        profile = indexes["camera_aliases"][camera_key]
        resolution = "alias"

    use_fallback = profile is None
    effective = copy.deepcopy(
        MINIMAL_FALLBACK
        if use_fallback
        else {field: profile[field] for field in PROFILE_FIELDS}
    )
    restrictions_applied: list[str] = []
    if (
        effective["elevation"] == "top_oblique"
        and effective["max_background_details"] != 0
    ):
        effective["max_background_details"] = 0
        restrictions_applied.append(
            "top_oblique_max_background_details_capped_at_0"
        )

    return {
        "requested_tag": _requested_string(camera_tag),
        "resolved_tag": profile["tag"] if profile is not None else None,
        "resolution": resolution,
        "profile_version": registry["version"],
        "registry_status": registry["status"],
        "device_type": profile["device_family"] if profile is not None else None,
        "source_camera_name": (
            profile["source_camera_name"] if profile is not None else None
        ),
        "effective_profile": effective,
        "restrictions_applied": restrictions_applied,
        "used_minimal_fallback": use_fallback,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("camera_tag")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args()
    print(
        json.dumps(
            resolve_profile(load_registry(args.registry), args.camera_tag),
            indent=2,
            ensure_ascii=False,
        )
    )
