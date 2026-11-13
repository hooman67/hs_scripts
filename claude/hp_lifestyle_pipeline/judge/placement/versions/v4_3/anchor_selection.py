"""Deterministic V4.3 anchor selection for arbitrary runtime targets."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable, Mapping

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "anchors" / "anchor_catalog.json"
SELECTION_SALT = "hp-placement-v4.3-anchor-selection-v1"


def file_sha(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pixel_sha(path: str | Path) -> str:
    with Image.open(path) as im:
        raw = ImageOps.exif_transpose(im).convert("RGB").tobytes()
    return hashlib.sha256(raw).hexdigest()


def normalize_camera(value: str | None) -> str | None:
    return re.sub(r"[^a-z0-9]+", "", value.lower()) if value else None


def target_fingerprint(target: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "generated_byte_sha256": file_sha(target["generated_image"]),
        "generated_pixel_sha256": pixel_sha(target["generated_image"]),
        "twin_byte_sha256": file_sha(target["twin_image"]),
        "twin_pixel_sha256": pixel_sha(target["twin_image"]),
        "prompt_sha256": hashlib.sha256(target["scene_prompt"].encode("utf-8")).hexdigest(),
        "product_type": target["product_type"],
        "device": target.get("device"),
        "camera": normalize_camera(target.get("camera")),
        "prompt_rank": str(target["prompt_rank"]) if target.get("prompt_rank") is not None else None,
    }


def select_anchors(
    target: Mapping[str, Any],
    *,
    catalog: Mapping[str, Any] | None = None,
    exclusion_targets: Iterable[Mapping[str, Any]] = (),
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if catalog is None:
        catalog = json.loads(CATALOG_PATH.read_text())
    fingerprints = [target_fingerprint(target), *(target_fingerprint(t) for t in exclusion_targets)]
    # Deduplicate target if it was included in the union.
    unique = {(f["generated_pixel_sha256"], f["twin_pixel_sha256"], f["prompt_sha256"]): f for f in fingerprints}
    fingerprints = list(unique.values())
    excluded: dict[str, list[str]] = {}
    eligible = []
    for anchor in catalog["records"]:
        reasons: set[str] = set()
        for fp in fingerprints:
            if anchor["generated"]["byte_sha256"] == fp["generated_byte_sha256"] or anchor["generated"]["pixel_sha256"] == fp["generated_pixel_sha256"]:
                reasons.add("exact_generated_hash")
            if anchor["twin"]["byte_sha256"] == fp["twin_byte_sha256"] or anchor["twin"]["pixel_sha256"] == fp["twin_pixel_sha256"]:
                reasons.add("same_twin_hash")
            if anchor["prompt_sha256"] == fp["prompt_sha256"]:
                reasons.add("exact_prompt_hash")
            if fp["camera"] and fp["prompt_rank"] is not None:
                same_ptype_family = anchor["product_type"] == fp["product_type"] and normalize_camera(anchor["camera"]) == fp["camera"] and str(anchor["prompt_rank"]) == fp["prompt_rank"]
                same_device_family = fp["device"] and anchor["device"] == fp["device"] and normalize_camera(anchor["camera"]) == fp["camera"] and str(anchor["prompt_rank"]) == fp["prompt_rank"]
                if same_ptype_family:
                    reasons.add("same_product_camera_rank_family")
                if same_device_family:
                    reasons.add("same_device_camera_rank_family")
        if reasons:
            excluded[anchor["anchor_id"]] = sorted(reasons)
        else:
            eligible.append(anchor)
    primary = target_fingerprint(target)
    def order_key(anchor: Mapping[str, Any]) -> str:
        raw = "".join([
            SELECTION_SALT, primary["product_type"], primary["generated_pixel_sha256"],
            primary["twin_pixel_sha256"], primary["prompt_sha256"], anchor["generated"]["pixel_sha256"],
        ])
        return hashlib.sha256(raw.encode()).hexdigest()
    by_type: dict[str, list[dict[str, Any]]] = {"laptop": [], "printer": []}
    for product_type in by_type:
        seen_twins = set()
        for anchor in sorted((a for a in eligible if a["product_type"] == product_type), key=order_key):
            if anchor["twin"]["pixel_sha256"] in seen_twins:
                continue
            seen_twins.add(anchor["twin"]["pixel_sha256"])
            by_type[product_type].append(anchor)
    n = min(2, len(by_type["laptop"]), len(by_type["printer"]))
    selected = by_type["laptop"][:n] + by_type["printer"][:n]
    audit = {
        "selection_version": SELECTION_SALT,
        "target_fingerprint": primary,
        "union_target_count": len(fingerprints),
        "excluded": excluded,
        "eligible_count": len(eligible),
        "selected_anchor_ids": [a["anchor_id"] for a in selected],
        "depleted": n == 0,
    }
    return selected, audit


def validate_catalog(catalog: Mapping[str, Any] | None = None) -> None:
    if catalog is None:
        catalog = json.loads(CATALOG_PATH.read_text())
    ids = set()
    for anchor in catalog["records"]:
        if anchor["anchor_id"] in ids:
            raise ValueError("duplicate anchor id")
        ids.add(anchor["anchor_id"])
        for kind in ("generated", "twin"):
            display = Path(anchor[kind]["display_path"])
            if not display.is_file() or file_sha(display) != anchor[kind]["display_sha256"]:
                raise ValueError(f"anchor display provenance mismatch: {anchor['anchor_id']} {kind}")
