"""Compile reviewed V6 prop candidates into a strict runtime catalog.

The review CSV is an input record and is never modified here.  A row is
eligible only when ``reviewer_decision`` is exactly ``approve`` after trimming
and case-folding.  The legacy ``status`` and ``runtime_allowed`` columns do not
grant approval.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


CATALOG_VERSION = "hp-v6.3-approved-props-v1"
ENVIRONMENTS = frozenset(
    {"Office", "Home", "Education", "Gaming", "Café", "Creative Studio"}
)
ROLES = frozenset({"tabletop_or_movable", "background_furnishing_or_decor"})
PURPOSES = frozenset({"production", "test_fixture"})

_HERE = Path(__file__).resolve().parent
_LEXICON_PATH = _HERE / "prop_lexicon.json"
_CSV_FIELDS = frozenset(
    {
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
    }
)
_ENTRY_FIELDS = frozenset(
    {"id", "environment", "role", "name", "repetition_groups", "aliases"}
)
_DECISIONS = frozenset({"", "approve", "reject", "hold"})
_GROUP_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_EXCLUDED_PROP_GROUPS = frozenset({"paperweight", "stone_object"})
_EXCLUDED_PROP_RE = re.compile(
    r"\b(?:paper\s*weights?|rocks?|pebbles?|(?:river|smooth|loose|decorative)\s+stones?)\b"
)

# These groups describe computing/product hardware that cannot be introduced as
# a prop.  Explicit environment-specific approval can admit ordinary accessory
# rows (keyboard, mouse mat, headset, etc.), but cannot cross this boundary.
_IMMUTABLE_DEVICE_GROUPS = frozenset(
    {"computer", "monitor", "phone_tablet", "printer_scanner", "game_console"}
)
_IMMUTABLE_DEVICE_PHRASES = frozenset(
    {
        "computer",
        "computers",
        "desktop",
        "desktops",
        "desktop computer",
        "desktop computers",
        "laptop",
        "laptops",
        "mini pc",
        "mini pcs",
        "minipc",
        "minipcs",
        "all in one computer",
        "all in one computers",
        "printer",
        "printers",
        "scanner",
        "scanners",
        "copier",
        "copiers",
        "label printer",
        "label printers",
        "monitor",
        "monitors",
        "portable display",
        "portable displays",
        "phone",
        "phones",
        "smartphone",
        "smartphones",
        "tablet",
        "tablets",
        "e reader",
        "e readers",
        "game console",
        "game consoles",
        "handheld console",
        "handheld consoles",
    }
)
_CONDITIONAL_ACCESSORY_GROUPS = frozenset(
    {
        "keyboard",
        "mouse",
        "headset",
        "speaker",
        "controller",
        "webcam",
        "microphone",
        "speakerphone",
        "dock",
        "drawing_tablet",
        "external_storage",
        "charging_accessory",
        "mouse_mat",
        "laptop_bag",
        "gaming_chair",
        "print_consumables",
        "branded_object",
    }
)
_DEVICE_WORD_RE = re.compile(
    r"\b(?:computer|desktop|laptop|minipc|printer|scanner|copier|monitor|"
    r"phone|smartphone|tablet)\b"
)


def _normalise_phrase(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = value.replace("-", " ").replace("/", " ")
    value = re.sub(r"[^\w\s]", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def _plural_phrase(phrase: str) -> str:
    """Return a conservative English plural for an exact noun phrase."""

    words = phrase.split()
    if not words:
        return phrase
    word = words[-1]
    if word.endswith("s") and not word.endswith("ss"):
        return phrase
    if word.endswith(("ss", "x", "z", "ch", "sh")):
        words[-1] = word + "es"
    elif word == "shelf":
        words[-1] = "shelves"
    elif len(word) > 1 and word.endswith("y") and word[-2] not in "aeiou":
        words[-1] = word[:-1] + "ies"
    else:
        words[-1] = word + "s"
    return " ".join(words)


def _name_aliases(name: str) -> set[str]:
    phrase = _normalise_phrase(name)
    return {phrase, _plural_phrase(phrase)} if phrase else set()


def _group_aliases(group: str) -> set[str]:
    phrase = group.replace("_", " ")
    return {phrase, _plural_phrase(phrase)}


def _base_aliases(name: str, groups: Iterable[str]) -> set[str]:
    """Build aliases for one reviewed row without conflating compounds.

    A compound row's complete name represents all of its groups together.
    Bare component phrases are separately declared in the pinned lexicon.
    """

    group_list = list(groups)
    aliases = _name_aliases(name)
    if len(group_list) == 1:
        aliases.update(_group_aliases(group_list[0]))
    return aliases


def _read_lexicon_file() -> list[dict[str, Any]]:
    try:
        raw = json.loads(_LEXICON_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load V6 prop lexicon: {exc}") from exc
    if not isinstance(raw, dict) or raw.get("version") != CATALOG_VERSION:
        raise ValueError("prop lexicon has an unsupported version")
    entries = raw.get("entries")
    if not isinstance(entries, list):
        raise ValueError("prop lexicon entries must be a list")
    return entries


def _add_lexicon_entry(
    merged: dict[str, set[str]], phrase: Any, groups: Any, *, source: str
) -> None:
    if not isinstance(phrase, str) or not _normalise_phrase(phrase):
        raise ValueError(f"{source} contains an invalid lexicon phrase")
    if (
        not isinstance(groups, list)
        or not groups
        or any(not isinstance(group, str) or not _GROUP_RE.fullmatch(group) for group in groups)
    ):
        raise ValueError(f"{source} contains invalid lexicon groups")
    merged[_normalise_phrase(phrase)].update(groups)


def load_lexicon() -> list[dict[str, Any]]:
    """Load exact known phrases for ordinary and currently uncertain props.

    This is a bounded recognition lexicon, not evidence that arbitrary nouns in
    prose are approved.  It deliberately uses exact normalised phrases rather
    than substring matching.
    """

    merged: dict[str, set[str]] = defaultdict(set)
    for index, item in enumerate(_read_lexicon_file(), start=1):
        if not isinstance(item, dict) or set(item) != {"phrase", "groups"}:
            raise ValueError(f"prop lexicon entry {index} is malformed")
        _add_lexicon_entry(
            merged, item["phrase"], item["groups"], source=f"prop lexicon entry {index}"
        )

    return [
        {"phrase": phrase, "groups": sorted(groups)}
        for phrase, groups in sorted(merged.items())
    ]


def _parse_groups(raw: Any, line_number: int) -> list[str]:
    if not isinstance(raw, str):
        raise ValueError(f"review CSV line {line_number} has malformed repetition groups")
    groups = [group.strip() for group in raw.split(",")]
    if (
        not groups
        or any(not group or not _GROUP_RE.fullmatch(group) for group in groups)
        or len(groups) != len(set(groups))
    ):
        raise ValueError(f"review CSV line {line_number} has invalid repetition groups")
    return groups


def _aliases_for(name: str, groups: list[str], lexicon: list[dict[str, Any]]) -> list[str]:
    aliases = _base_aliases(name, groups)
    group_set = set(groups)
    for item in lexicon:
        if set(item["groups"]) == group_set:
            aliases.add(item["phrase"])
    return sorted(aliases)


def _is_immutable_device(name: str, groups: list[str], aliases: Iterable[str]) -> bool:
    if _IMMUTABLE_DEVICE_GROUPS.intersection(groups):
        return True
    phrases = {_normalise_phrase(name), *(_normalise_phrase(alias) for alias in aliases)}
    if phrases.intersection(_IMMUTABLE_DEVICE_PHRASES):
        return True
    if _CONDITIONAL_ACCESSORY_GROUPS.intersection(groups):
        return False
    return any(_DEVICE_WORD_RE.search(phrase) for phrase in phrases)


def compile_catalog(
    csv_path: str | Path, revision: str, *, purpose: str = "production"
) -> dict[str, Any]:
    """Compile explicitly approved, environment-specific review rows."""

    if not isinstance(revision, str) or not revision.strip():
        raise ValueError("catalog revision must be a non-empty string")
    if not isinstance(purpose, str) or purpose not in PURPOSES:
        raise ValueError(f"unsupported catalog purpose: {purpose!r}")

    path = Path(csv_path)
    try:
        source = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"cannot read review CSV: {exc}") from exc
    source_sha256 = hashlib.sha256(source).hexdigest()
    try:
        text = source.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("review CSV must be UTF-8") from exc

    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames is None or not _CSV_FIELDS.issubset(reader.fieldnames):
        raise ValueError("review CSV is missing required columns")

    lexicon = load_lexicon()
    entries: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for line_number, row in enumerate(reader, start=2):
        if None in row:
            raise ValueError(f"review CSV line {line_number} has extra fields")
        candidate_id = (row.get("candidate_id") or "").strip()
        if not candidate_id:
            raise ValueError(f"review CSV line {line_number} has an invalid candidate ID")
        if candidate_id in seen_ids:
            raise ValueError(f"duplicate candidate ID: {candidate_id}")
        seen_ids.add(candidate_id)

        raw_decision = row.get("reviewer_decision")
        if not isinstance(raw_decision, str):
            raise ValueError(f"review CSV line {line_number} has a malformed reviewer decision")
        decision = raw_decision.strip().casefold()
        if decision not in _DECISIONS:
            raise ValueError(
                f"review CSV line {line_number} has unknown reviewer decision {raw_decision!r}"
            )
        if decision != "approve":
            continue

        environment = (row.get("environment") or "").strip()
        if environment not in ENVIRONMENTS:
            if environment == "Cross-environment":
                raise ValueError(
                    f"{candidate_id} is cross-environment; add and approve explicit "
                    "per-environment rows before runtime use"
                )
            raise ValueError(f"{candidate_id} has an invalid environment")
        role = (row.get("role") or "").strip()
        if role not in ROLES:
            raise ValueError(f"{candidate_id} has an invalid runtime role")
        name = (row.get("name") or "").strip()
        if not name:
            raise ValueError(f"{candidate_id} has no name")
        groups = _parse_groups(row.get("repetition_groups"), line_number)
        aliases = _aliases_for(name, groups, lexicon)
        if _is_immutable_device(name, groups, aliases):
            raise ValueError(f"{candidate_id} crosses the immutable computing-device boundary")
        entries.append(
            {
                "id": candidate_id,
                "environment": environment,
                "role": role,
                "name": name,
                "repetition_groups": groups,
                "aliases": aliases,
            }
        )

    catalog = {
        "version": CATALOG_VERSION,
        "revision": revision.strip(),
        "purpose": purpose,
        "source_sha256": source_sha256,
        "entries": entries,
    }
    if entries:
        _validate_catalog(catalog, allow_test_catalog=True, allow_empty=False)
    return catalog


def _validate_catalog(
    catalog: Any, *, allow_test_catalog: bool, allow_empty: bool
) -> dict[str, Any]:
    if not isinstance(catalog, dict):
        raise ValueError("catalog must be an object")
    required = {"version", "revision", "purpose", "source_sha256", "entries"}
    if set(catalog) != required:
        raise ValueError("catalog fields are malformed")
    if catalog["version"] != CATALOG_VERSION:
        raise ValueError("unsupported catalog version")
    if not isinstance(catalog["revision"], str) or not catalog["revision"].strip():
        raise ValueError("catalog revision must be a non-empty string")
    purpose = catalog["purpose"]
    if not isinstance(purpose, str) or purpose not in PURPOSES:
        raise ValueError(f"unsupported catalog purpose: {purpose!r}")
    if purpose == "test_fixture" and not allow_test_catalog:
        raise ValueError("test_fixture catalogs require allow_test_catalog=True")
    if not isinstance(catalog["source_sha256"], str) or not _SHA256_RE.fullmatch(
        catalog["source_sha256"]
    ):
        raise ValueError("catalog source_sha256 is malformed")
    entries = catalog["entries"]
    if not isinstance(entries, list) or (not entries and not allow_empty):
        raise ValueError("runtime catalog must contain at least one approved entry")

    declared_groups = {
        group for item in load_lexicon() for group in item["groups"]
    }
    seen_ids: set[str] = set()
    for index, entry in enumerate(entries):
        label = f"catalog entry {index}"
        if not isinstance(entry, dict) or set(entry) != _ENTRY_FIELDS:
            raise ValueError(f"{label} is malformed or contains unreviewed fields")
        candidate_id = entry["id"]
        if (
            not isinstance(candidate_id, str)
            or not candidate_id
            or candidate_id != candidate_id.strip()
        ):
            raise ValueError(f"{label} has an invalid ID")
        if candidate_id in seen_ids:
            raise ValueError(f"duplicate catalog entry ID: {candidate_id}")
        seen_ids.add(candidate_id)
        if (
            not isinstance(entry["environment"], str)
            or entry["environment"] not in ENVIRONMENTS
        ):
            raise ValueError(f"{candidate_id} has an invalid environment")
        if not isinstance(entry["role"], str) or entry["role"] not in ROLES:
            raise ValueError(f"{candidate_id} has an invalid role")
        if not isinstance(entry["name"], str) or not entry["name"].strip():
            raise ValueError(f"{candidate_id} has an invalid name")
        groups = entry["repetition_groups"]
        if (
            not isinstance(groups, list)
            or not groups
            or any(not isinstance(group, str) or not _GROUP_RE.fullmatch(group) for group in groups)
            or len(groups) != len(set(groups))
            or not set(groups).issubset(declared_groups)
        ):
            raise ValueError(f"{candidate_id} has invalid repetition groups")
        aliases = entry["aliases"]
        if (
            not isinstance(aliases, list)
            or not aliases
            or any(
                not isinstance(alias, str)
                or alias != _normalise_phrase(alias)
                or not alias
                for alias in aliases
            )
            or len(aliases) != len(set(aliases))
        ):
            raise ValueError(f"{candidate_id} has invalid aliases")
        if _is_immutable_device(entry["name"], groups, aliases):
            raise ValueError(f"{candidate_id} crosses the immutable computing-device boundary")
        if _EXCLUDED_PROP_GROUPS.intersection(groups) or any(
            _EXCLUDED_PROP_RE.search(_normalise_phrase(phrase))
            for phrase in (entry["name"], *aliases)
        ):
            raise ValueError(f"{candidate_id} uses an excluded paperweight or loose stone prop")
    return catalog


def validate_catalog(
    catalog: Any, allow_test_catalog: bool = False
) -> dict[str, Any]:
    """Validate a non-empty catalog before any model invocation."""

    if not isinstance(allow_test_catalog, bool):
        raise ValueError("allow_test_catalog must be a boolean")
    return _validate_catalog(
        catalog, allow_test_catalog=allow_test_catalog, allow_empty=False
    )
