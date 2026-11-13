"""Deterministic primary-support extraction and bank-level diversity checks.

The extractor intentionally reads only the first sentence.  It reports exact
source spans so callers can display bounded evidence instead of paraphrasing
scene content.  This module has no provider or model dependencies.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
import re
from typing import Any


_SENTENCE_END_RE = re.compile(r"[.!?](?=\s|$)")

_TABLE_MODIFIER = (
    r"(?:background|nearby|separate|secondary|dedicated|ordinary|sturdy|substantial|"
    r"small|large|wide|broad|long|low|round|circular|oval|rectangular|square|"
    r"hexagonal|triangular|kidney-shaped|irregular|amorphous|"
    r"wooden|wood|oak|maple|walnut|birch|bamboo|plywood|laminate|marble|stone|"
    r"metal|steel|reclaimed-wood|natural-wood|light-wood|dark-wood|solid-wood|"
    r"natural|solid|pale|light|dark|white|black|painted|smooth|matte|warm|"
    r"caf[ée]|office|home|classroom|library|meeting|study|breakfast|reading|"
    r"collaborative|shared|drafting|project|production|printer|laptop|"
    r"output|work|resource|utility|studio|equipment|service|back-office|"
    r"coffee|end|side|dining|lounge|gaming|customer|pastry|fragile|folding|"
    r"floating|wall-mounted)"
)
_CABINET_MODIFIER = (
    r"(?:background|nearby|separate|secondary|wide|broad|substantial|sturdy|low|"
    r"floor-standing|floorstanding|freestanding|free-standing|storage|output|"
    r"equipment|printer|wooden|wood|oak|maple|walnut|metal|steel|white|black|"
    r"narrow|slim|high|tall|fragile|floating|wall-mounted)"
)
_CREDENZA_MODIFIER = (
    r"(?:background|nearby|separate|secondary|wide|broad|substantial|sturdy|low|"
    r"floor-standing|floorstanding|freestanding|free-standing|storage|output|"
    r"equipment|printer|wooden|wood|oak|maple|walnut|metal|steel|white|black|"
    r"narrow|slim|high|tall|fragile|floating|wall-mounted)"
)

# Ordered from structurally specific to generic.  The overlap filter below
# keeps, for example, the cabinet inside a fitted-cabinet phrase from becoming
# a second candidate.
_SUPPORT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "fitted_counter",
        re.compile(
            r"\b(?:fitted|built-in)\s+base\s+cabinets?\s+with\s+(?:a\s+)?"
            r"continuous\s+(?:worktop|countertop)\b|"
            r"\bbuilt-in\s+(?:equipment|output|printer)\s+counter\b",
            re.I,
        ),
    ),
    (
        "freestanding_cabinet",
        re.compile(
            rf"\b(?:{_CABINET_MODIFIER}\s+){{0,7}}(?:storage\s+)?cabinets?\b",
            re.I,
        ),
    ),
    (
        "credenza_sideboard",
        re.compile(
            rf"\b(?:{_CREDENZA_MODIFIER}\s+){{0,7}}(?:credenzas?|sideboards?)\b",
            re.I,
        ),
    ),
    (
        "table",
        re.compile(
            r"\b(?:(?:wood(?:en)?|walnut|oak|birch|maple|laminate|veneer|painted|"
            r"satin|matte|smooth|white|graphite)\s+desktop|desktop\s+surface)\b",
            re.I,
        ),
    ),
    (
        "table",
        re.compile(
            rf"\b(?:{_TABLE_MODIFIER}\s+){{0,8}}(?:work\s+tables?|worktables?|tables?|desks?)\b"
            r"(?!\s+(?:lamp|clock|mirror|sculpture|ornament|mat|runner|leg|edge|corner)s?\b)",
            re.I,
        ),
    ),
    (
        "unsupported",
        re.compile(
            r"\b(?:(?:display|floating|wall-mounted|drafting|fragile)\s+)?"
            r"(?:shelves?|plinths?|ledges?|pedestals?)\b",
            re.I,
        ),
    ),
)

_SECONDARY_IN_PHRASE_RE = re.compile(r"\b(?:background|nearby|separate|secondary)\b", re.I)
_SECONDARY_SUFFIX_RE = re.compile(
    r"^\s+(?:(?:sits?|stands?|remains?)\s+)?(?:off\s+to\s+the\s+side|in\s+the\s+background)\b",
    re.I,
)
_BEHIND_ANOTHER_SUPPORT_RE = re.compile(
    r"^\s+(?:behind|beyond)\s+(?:an?\s+|the\s+)?(?:[^,;.]{0,35})"
    r"(?:work\s+table|worktable|table|desk|cabinet|credenza|sideboard)\b",
    re.I,
)

_KNOWN_SHAPE_RE = re.compile(
    r"\b(round|circular|oval|rectangular|square)\b(?![- ](?:edged?|corners?))",
    re.I,
)
_UNKNOWN_SHAPE_RE = re.compile(
    r"\b(hexagonal|triangular|kidney-shaped|irregular(?:ly shaped)?|amorphous)\b",
    re.I,
)
_ATTACHED_TOP_SHAPE_RE = re.compile(
    r"^\s+(?:with|having)\s+(?:an?\s+|the\s+)?"
    r"(round|circular|oval|rectangular|square|hexagonal|triangular|kidney-shaped)\s+"
    r"(?:top|tabletop|surface|footprint)\b",
    re.I,
)

_UNSAFE_PRINTER_FURNITURE_RE = re.compile(
    r"\b(?:gaming|customer|coffee|end|dining|lounge|pastry|sofa-side|bar|fragile)\b",
    re.I,
)
_UNSAFE_CASEWORK_RE = re.compile(
    r"\b(?:narrow|slim|high|tall|fragile|floating|wall-mounted)\b",
    re.I,
)
_PRINTER_TABLE_ROLE_RE = re.compile(
    r"\b(?:dedicated|printer|output|work|worktable|worktables|resource|utility|studio|"
    r"equipment|production|service)\b",
    re.I,
)
_CABINET_CREDIBILITY_RE = re.compile(
    r"\b(?:wide|broad|substantial|sturdy|low|floor-standing|floorstanding|"
    r"freestanding|free-standing|storage|output|equipment|printer)\b",
    re.I,
)
_CREDENZA_CREDIBILITY_RE = re.compile(r"\b(?:wide|broad|substantial|sturdy|low)\b", re.I)


@dataclass(frozen=True)
class _Candidate:
    family: str
    phrase: str
    start: int
    end: int


class SupportInferenceError(ValueError):
    """A bounded extraction failure with machine-readable evidence."""

    def __init__(self, code: str, **evidence: Any) -> None:
        self.code = code
        self.evidence = evidence
        super().__init__(code)

    def to_dict(self) -> dict[str, Any]:
        return {"code": self.code, **self.evidence}


def _first_sentence(text: str) -> tuple[str, int, int]:
    match = _SENTENCE_END_RE.search(text)
    end = match.end() if match else len(text)
    return text[:end], 0, end


def _overlaps(start: int, end: int, candidates: list[_Candidate]) -> bool:
    return any(start < candidate.end and end > candidate.start for candidate in candidates)


def _is_secondary(sentence: str, candidate: _Candidate) -> bool:
    if _SECONDARY_IN_PHRASE_RE.search(candidate.phrase):
        return True
    suffix = sentence[candidate.end : candidate.end + 70]
    return bool(
        _SECONDARY_SUFFIX_RE.search(suffix)
        or _BEHIND_ANOTHER_SUPPORT_RE.search(suffix)
    )


def _candidates(sentence: str) -> list[_Candidate]:
    found: list[_Candidate] = []
    for family, pattern in _SUPPORT_PATTERNS:
        for match in pattern.finditer(sentence):
            if _overlaps(match.start(), match.end(), found):
                continue
            candidate = _Candidate(family, match.group(0), match.start(), match.end())
            if not _is_secondary(sentence, candidate):
                found.append(candidate)
    return sorted(found, key=lambda item: (item.start, -(item.end - item.start)))


def _shape_evidence(sentence: str, support: _Candidate) -> tuple[str, dict[str, Any] | None]:
    evidence: list[tuple[str, str, int, int]] = []
    for match in _KNOWN_SHAPE_RE.finditer(support.phrase):
        raw = match.group(1)
        normalized = "round" if raw.casefold() in {"round", "circular"} else raw.casefold()
        evidence.append((normalized, raw, support.start + match.start(1), support.start + match.end(1)))
    for match in _UNKNOWN_SHAPE_RE.finditer(support.phrase):
        evidence.append(("unknown", match.group(1), support.start + match.start(1), support.start + match.end(1)))

    suffix = sentence[support.end : support.end + 65]
    attached = _ATTACHED_TOP_SHAPE_RE.match(suffix)
    if attached:
        raw = attached.group(1)
        normalized = "round" if raw.casefold() in {"round", "circular"} else raw.casefold()
        evidence.append(
            (
                "unknown" if normalized in {"hexagonal", "triangular", "kidney-shaped"} else normalized,
                raw,
                support.end + attached.start(1),
                support.end + attached.end(1),
            )
        )

    normalized_shapes = {item[0] for item in evidence}
    if "unknown" in normalized_shapes:
        unknown = next(item for item in evidence if item[0] == "unknown")
        raise SupportInferenceError(
            "unknown_support_shape",
            phrase=unknown[1],
            start=unknown[2],
            end=unknown[3],
            support_phrase=support.phrase,
            support_start=support.start,
            support_end=support.end,
        )
    if len(normalized_shapes) > 1:
        raise SupportInferenceError(
            "conflicting_support_shape",
            shapes=[
                {"shape": item[0], "phrase": item[1], "start": item[2], "end": item[3]}
                for item in evidence
            ],
            support_phrase=support.phrase,
            support_start=support.start,
            support_end=support.end,
        )
    if not evidence:
        return "unspecified", None
    item = evidence[0]
    return item[0], {"phrase": item[1], "start": item[2], "end": item[3]}


def _normalize_device_type(device_type: str | None) -> str | None:
    if device_type is None:
        return None
    normalized = device_type.strip().casefold()
    if normalized.startswith("laptop"):
        return "laptop"
    if normalized.startswith("printer"):
        return "printer"
    raise ValueError(f"unsupported device_type: {device_type!r}")


def _validate_printer_support(support: _Candidate) -> None:
    phrase = support.phrase
    unsafe = _UNSAFE_PRINTER_FURNITURE_RE.search(phrase)
    if unsafe or (support.family in {"freestanding_cabinet", "credenza_sideboard"} and (unsafe := _UNSAFE_CASEWORK_RE.search(phrase))):
        assert unsafe is not None
        raise SupportInferenceError(
            "unsafe_printer_support",
            phrase=phrase,
            start=support.start,
            end=support.end,
            unsafe_phrase=unsafe.group(0),
            unsafe_start=support.start + unsafe.start(),
            unsafe_end=support.start + unsafe.end(),
        )
    if support.family == "unsupported":
        raise SupportInferenceError(
            "unsupported_printer_support",
            phrase=phrase,
            start=support.start,
            end=support.end,
        )
    credible = {
        "table": _PRINTER_TABLE_ROLE_RE,
        "freestanding_cabinet": _CABINET_CREDIBILITY_RE,
        "credenza_sideboard": _CREDENZA_CREDIBILITY_RE,
    }.get(support.family)
    if credible is not None and not credible.search(phrase):
        raise SupportInferenceError(
            "unsupported_printer_support",
            phrase=phrase,
            start=support.start,
            end=support.end,
        )


def infer_primary_support(text: str, device_type: str | None = None) -> dict[str, Any]:
    """Return the first primary support named in the first sentence.

    The result contains only extracted labels and exact text spans.  Explicit
    exotic shapes and contradictory shape labels raise
    :class:`SupportInferenceError`; absence of a shape is ``unspecified``.
    """

    if not isinstance(text, str) or not text.strip():
        raise SupportInferenceError("primary_support_not_found", sentence_start=0, sentence_end=0)
    normalized_device = _normalize_device_type(device_type)
    sentence, sentence_start, sentence_end = _first_sentence(text)
    candidates = _candidates(sentence)
    if not candidates:
        raise SupportInferenceError(
            "primary_support_not_found",
            sentence_start=sentence_start,
            sentence_end=sentence_end,
        )

    support = candidates[0]
    if len(candidates) > 1:
        connector = sentence[support.end : candidates[1].start]
        if re.fullmatch(r"\s*(?:or|and/or)\s*", connector, re.I):
            raise SupportInferenceError(
                "conflicting_primary_support",
                supports=[
                    {
                        "family": candidate.family,
                        "phrase": candidate.phrase,
                        "start": candidate.start,
                        "end": candidate.end,
                    }
                    for candidate in candidates[:2]
                ],
            )

    if normalized_device == "laptop" and support.family != "table":
        raise SupportInferenceError(
            "unsupported_laptop_support",
            phrase=support.phrase,
            start=support.start,
            end=support.end,
            family=support.family,
        )
    if normalized_device == "printer":
        _validate_printer_support(support)

    shape, shape_evidence = _shape_evidence(sentence, support)
    return {
        "family": support.family,
        "shape": shape,
        "phrase": support.phrase,
        "start": support.start,
        "end": support.end,
        "shape_evidence": shape_evidence,
        "sentence_start": sentence_start,
        "sentence_end": sentence_end,
        "device_type": normalized_device,
    }


def _row_value(row: str | Mapping[str, Any], key: str, default: Any = None) -> Any:
    return row.get(key, default) if isinstance(row, Mapping) else default


def audit_bank(
    rows: Iterable[str | Mapping[str, Any]],
    device_type: str | None = None,
    *,
    laptop_round_minimum: int = 2,
    printer_family_minimum: int = 3,
    printer_non_table_minimum: int = 5,
) -> dict[str, Any]:
    """Audit extracted primary-support diversity for a prompt bank.

    Mapping rows use ``text``, optional ``device_type``, ``environment``, and
    ``id`` fields.  All errors contain codes, counts, row identifiers, or exact
    spans; the function does not generate descriptive scene claims.
    """

    default_device = _normalize_device_type(device_type)
    evidence_rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    family_counts: Counter[str] = Counter()
    shape_counts: Counter[str] = Counter()
    laptop_rows: list[dict[str, Any]] = []
    printer_rows: list[dict[str, Any]] = []

    for index, row in enumerate(rows):
        text = row if isinstance(row, str) else _row_value(row, "text")
        row_id = _row_value(row, "id", index)
        environment = _row_value(row, "environment")
        row_device = _normalize_device_type(_row_value(row, "device_type", default_device))
        record: dict[str, Any] = {
            "row_id": row_id,
            "environment": environment,
            "device_type": row_device,
        }
        try:
            support = infer_primary_support(text, row_device)
        except SupportInferenceError as exc:
            issue = {"row_id": row_id, **exc.to_dict()}
            errors.append(issue)
            record["error"] = exc.to_dict()
        else:
            record["support"] = support
            family_counts[support["family"]] += 1
            shape_counts[support["shape"]] += 1
            if row_device == "laptop":
                laptop_rows.append(record)
            elif row_device == "printer":
                printer_rows.append(record)
        evidence_rows.append(record)

    if laptop_rows:
        round_count = sum(row["support"]["shape"] == "round" for row in laptop_rows)
        if round_count < laptop_round_minimum:
            errors.append(
                {
                    "code": "laptop_round_primary_minimum",
                    "required": laptop_round_minimum,
                    "actual": round_count,
                }
            )
        cafe_failures = [
            row["row_id"]
            for row in laptop_rows
            if str(row["environment"]).casefold() in {"café", "cafe"}
            and row["support"]["shape"] != "round"
        ]
        if cafe_failures:
            errors.append({"code": "cafe_primary_support_not_round", "row_ids": cafe_failures})

    if printer_rows:
        printer_families = sorted({row["support"]["family"] for row in printer_rows})
        if len(printer_families) < printer_family_minimum:
            errors.append(
                {
                    "code": "printer_support_family_minimum",
                    "required": printer_family_minimum,
                    "actual": len(printer_families),
                    "families": printer_families,
                }
            )
        non_table_count = sum(row["support"]["family"] != "table" for row in printer_rows)
        if non_table_count < printer_non_table_minimum:
            errors.append(
                {
                    "code": "printer_non_table_primary_minimum",
                    "required": printer_non_table_minimum,
                    "actual": non_table_count,
                }
            )

    return {
        "passed": not errors,
        "rows": evidence_rows,
        "counts": {
            "families": dict(sorted(family_counts.items())),
            "shapes": dict(sorted(shape_counts.items())),
        },
        "errors": errors,
    }


__all__ = ["SupportInferenceError", "audit_bank", "infer_primary_support"]
