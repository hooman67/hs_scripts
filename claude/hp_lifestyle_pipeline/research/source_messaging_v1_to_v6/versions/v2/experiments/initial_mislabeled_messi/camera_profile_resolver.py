#!/usr/bin/env python3
"""Deterministic offline resolver for the camera-v2 profile registry.

This module is validation/build tooling. It is not a runtime image analyzer.
Matching follows the system-prompt contract: canonical names are compared after
case folding and trimming surrounding whitespace; only registry aliases add
alternate names.
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
OVERRIDABLE_FIELDS = (
    "framing",
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


def _unique_index(items: list[dict[str, Any]], field: str, label: str) -> dict[str, dict[str, Any]]:
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


def _camera_alias_index(
    aliases: dict[str, Any], profile_index: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    if not isinstance(aliases, dict):
        raise RegistryError("camera aliases must be an object mapping alias to canonical tag")
    index: dict[str, dict[str, Any]] = {}
    for alias, canonical in aliases.items():
        alias_key = normalize_lookup(alias)
        canonical_key = normalize_lookup(canonical)
        if alias_key is None or canonical_key is None:
            raise RegistryError(f"invalid camera alias mapping: {alias!r} -> {canonical!r}")
        if canonical_key not in profile_index:
            raise RegistryError(f"camera alias target is not registered: {canonical!r}")
        if alias_key in profile_index or alias_key in index:
            raise RegistryError(f"camera alias collides after normalization: {alias!r}")
        index[alias_key] = profile_index[canonical_key]
    return index


def _product_alias_index(
    products: list[dict[str, Any]], product_index: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    aliases: dict[str, dict[str, Any]] = {}
    for product in products:
        for alias in product.get("aliases", []):
            key = normalize_lookup(alias)
            if key is None:
                raise RegistryError(f"blank product alias for {product['product_name']!r}")
            if key in product_index or key in aliases:
                raise RegistryError(f"product alias collides after normalization: {alias!r}")
            aliases[key] = product
    return aliases


def validate_registry(registry: dict[str, Any]) -> dict[str, Any]:
    required = {
        "version",
        "status",
        "unknown_tag_policy",
        "aliases",
        "profiles",
        "products",
        "product_overrides",
        "unknown_product_policy",
        "incompatible_type_policy",
    }
    missing = sorted(required - registry.keys())
    if missing:
        raise RegistryError(f"registry missing keys: {missing}")

    profiles = registry["profiles"]
    products = registry["products"]
    if not isinstance(profiles, list) or not isinstance(products, list):
        raise RegistryError("profiles and products must be arrays")
    profile_index = _unique_index(profiles, "tag", "profile")
    product_index = _unique_index(products, "product_name", "product")
    camera_aliases = _camera_alias_index(registry["aliases"], profile_index)
    product_aliases = _product_alias_index(products, product_index)

    for profile in profiles:
        absent = [field for field in ("source_camera_name", "device_family", *PROFILE_FIELDS) if field not in profile]
        if absent:
            raise RegistryError(f"profile {profile['tag']!r} missing fields: {absent}")
        if profile["device_family"] not in {"laptop", "printer"}:
            raise RegistryError(f"unknown device family in {profile['tag']!r}")
        for field in ("max_local_props", "max_background_details"):
            if not isinstance(profile[field], int) or profile[field] < 0:
                raise RegistryError(f"{profile['tag']!r} has invalid {field}")

    for product in products:
        if product.get("device_family") not in {"laptop", "printer"}:
            raise RegistryError(f"unknown product family for {product['product_name']!r}")
        tags = product.get("supported_camera_tags")
        if not isinstance(tags, list) or len(tags) != len(set(tags)):
            raise RegistryError(f"invalid/duplicate supported tags for {product['product_name']!r}")
        for tag in tags:
            profile = profile_index.get(normalize_lookup(tag))
            if profile is None:
                raise RegistryError(f"unsupported tag reference {tag!r} for {product['product_name']!r}")
            if profile["device_family"] != product["device_family"]:
                raise RegistryError(
                    f"family conflict inside registry: {product['product_name']!r} supports {tag!r}"
                )

    for override in registry["product_overrides"]:
        product_key = normalize_lookup(override.get("product_name"))
        if product_key not in product_index:
            raise RegistryError(f"override has unknown product: {override.get('product_name')!r}")
        product = product_index[product_key]
        tags = override.get("camera_tags")
        if not isinstance(tags, list) or not tags:
            raise RegistryError(f"override camera_tags must be a nonempty list: {override!r}")
        for tag in tags:
            tag_key = normalize_lookup(tag)
            if tag_key not in profile_index:
                raise RegistryError(f"override has unknown tag: {tag!r}")
            if tag not in product["supported_camera_tags"]:
                raise RegistryError(
                    f"override tag {tag!r} is not supported by {product['product_name']!r}"
                )
        unknown_fields = sorted(
            set(override) - {"product_name", "camera_tags", "reason", *OVERRIDABLE_FIELDS}
        )
        if unknown_fields:
            raise RegistryError(f"override has unsupported fields: {unknown_fields}")

    return {
        "profiles": profile_index,
        "camera_aliases": camera_aliases,
        "products": product_index,
        "product_aliases": product_aliases,
    }


def _requested_string(value: Any) -> str:
    return value if isinstance(value, str) else ""


def resolve_profile(
    registry: dict[str, Any], camera_tag: Any, product_name: Any
) -> dict[str, Any]:
    """Resolve a product-camera pair for deterministic offline validation.

    Precedence is camera base, then matching product override, then immutable
    elevation restrictions. An incompatible or unresolved camera receives the
    minimal fallback and never inherits permissive profile limits.
    """

    indexes = validate_registry(registry)
    camera_key = normalize_lookup(camera_tag)
    product_key = normalize_lookup(product_name)

    profile = None
    camera_resolution = "missing" if camera_key is None else "unknown"
    if camera_key in indexes["profiles"]:
        profile = indexes["profiles"][camera_key]
        camera_resolution = "exact"
    elif camera_key in indexes["camera_aliases"]:
        profile = indexes["camera_aliases"][camera_key]
        camera_resolution = "alias"

    product = None
    product_resolution = "missing" if product_key is None else "unknown"
    if product_key in indexes["products"]:
        product = indexes["products"][product_key]
        product_resolution = "exact"
    elif product_key in indexes["product_aliases"]:
        product = indexes["product_aliases"][product_key]
        product_resolution = "alias"

    incompatible_reason = None
    if profile is not None and product is not None:
        if product["device_family"] != profile["device_family"]:
            incompatible_reason = "product_family_conflicts_with_camera_family"
        elif profile["tag"] not in product["supported_camera_tags"]:
            incompatible_reason = "camera_not_supported_by_product"
        if incompatible_reason:
            product_resolution = "incompatible"

    use_fallback = profile is None or incompatible_reason is not None
    effective = copy.deepcopy(MINIMAL_FALLBACK if use_fallback else {field: profile[field] for field in PROFILE_FIELDS})
    applied_overrides: list[dict[str, Any]] = []
    restrictions_applied: list[str] = []

    if not use_fallback and product is not None:
        for override in registry["product_overrides"]:
            if (
                normalize_lookup(override["product_name"])
                == normalize_lookup(product["product_name"])
                and profile["tag"] in override["camera_tags"]
            ):
                replacements = {
                    field: override[field]
                    for field in OVERRIDABLE_FIELDS
                    if field in override
                }
                effective.update(replacements)
                applied_overrides.append(
                    {
                        "product_name": product["product_name"],
                        "camera_tag": profile["tag"],
                        "replacements": replacements,
                        "reason": override.get("reason", ""),
                    }
                )

    # Geometry restriction is intentionally last and cannot be relaxed by an override.
    if effective["elevation"] == "top_oblique" and effective["max_background_details"] != 0:
        effective["max_background_details"] = 0
        restrictions_applied.append("top_oblique_max_background_details_capped_at_0")

    return {
        "requested_tag": _requested_string(camera_tag),
        "resolved_tag": profile["tag"] if profile is not None else None,
        "resolution": camera_resolution,
        "requested_product": _requested_string(product_name),
        "resolved_product": product["product_name"] if product is not None else None,
        "product_resolution": product_resolution,
        "profile_version": registry["version"],
        "registry_status": registry["status"],
        "device_family": profile["device_family"] if profile is not None else None,
        "source_camera_name": profile["source_camera_name"] if profile is not None else None,
        "effective_profile": effective,
        "applied_overrides": applied_overrides,
        "restrictions_applied": restrictions_applied,
        "incompatible_reason": incompatible_reason,
        "used_minimal_fallback": use_fallback,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("camera_tag")
    parser.add_argument("product_name")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args()
    print(
        json.dumps(
            resolve_profile(load_registry(args.registry), args.camera_tag, args.product_name),
            indent=2,
            ensure_ascii=False,
        )
    )
