"""Deterministic validation and finalization for V6 model output.

Validation is deliberately read-only.  The finalizer owns only prompt IDs,
derived source scores, ranking, and debug provenance; it never repairs model
claims, evidence, or scene prose.
"""

from __future__ import annotations

import copy
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import jsonschema

try:  # Package import in production; direct import in isolated test runners.
    from .catalog import load_lexicon
    from .content_policy import check_content_policy
except ImportError:  # pragma: no cover
    from catalog import load_lexicon
    from content_policy import check_content_policy


HERE = Path(__file__).resolve().parent
MODEL_OUTPUT_SCHEMA = HERE / "model_output.schema.json"
DOCUMENTS = ("smart_brief", "source_messaging")
COMPONENTS = ("setting", "activity", "materials", "use_context")
ENVIRONMENTS = frozenset(
    {"Office", "Home", "Education", "Gaming", "Café", "Creative Studio"}
)

_DEVICE_RE = re.compile(
    r"\b(?:hp|elitebooks?|omnibooks?|laserjets?|laptops?|computers?|mini[ -]?pcs?|"
    r"desktops?|devices?|ports?|chassis|bezels?|hinges?|vents?|"
    r"all[ -]?in[ -]?one(?: computers?)?|printers?|scanners?|copiers?|monitors?|"
    r"portable displays?|phones?|smartphones?|tablets?|e[ -]?readers?|"
    r"game consoles?|handheld consoles?|screens?)\b",
    re.IGNORECASE,
)
_DISPLAY_SHELVING_RE = re.compile(r"\bdisplay\s+shelving\b", re.IGNORECASE)
_DESKTOP_SUPPORT_RE = re.compile(
    r"\b(?:(?:wood(?:en)?|walnut|oak|birch|maple|laminate|veneer|painted|"
    r"satin|matte|smooth|white|graphite)\s+desktop|desktop\s+surface)\b",
    re.IGNORECASE,
)
_FURNITURE_DESKTOP_RE = re.compile(
    rf"(?:{_DESKTOP_SUPPORT_RE.pattern}|\bdesktop\s+(?:organizer|calendar)\b)",
    re.IGNORECASE,
)
_NONCOMPUTING_SCREEN_RE = re.compile(
    r"\b(?:privacy|acoustic|folding|divider)\s+screens?\b", re.IGNORECASE
)
_CAMERA_MOTION_RE = re.compile(
    r"\b(?:zoom(?:ing)?|widen(?:ing)?|pull\s+back|push\s+in|dolly(?:ing)?|"
    r"pan(?:ning)?\s+(?:left|right)|tilt(?:ing)?\s+(?:up|down))\b",
    re.IGNORECASE,
)
_TOP_OBLIQUE_INCOMPATIBLE_RE = re.compile(
    r"\b(?:walls?|windows?|curtains?|ceiling|wall\s+art)\b", re.IGNORECASE
)
_UNNATURAL_PLACE_RE = re.compile(
    r"\b(?:(?:close|local|tight|compact|small)\s+"
    r"(?:section|patch|area|portion|piece|stretch|slice)\s+of|"
    r"shared department records counter|records counter|paperwork nook|"
    r"policy deployment counter|illustration worktop|teaching[- ]preparation table|"
    r"(?:records?|policy|deployment|paperwork|illustration|workflow|department|"
    r"administration|administrative|output check|queue)\s+"
    r"(?:counter|nook|corner|worktop|surface)|"
    r"(?:focus|planning|briefing|policy|operations|workflow|support|intake|output|"
    r"administration|administrative)\s+(?:table|desk|counter|surface|nook)|"
    r"(?:teaching[- ]preparation|content review|document review|records?|paperwork|"
    r"workflow|department)\s+(?:desk|table|counter|nook|worktop|surface)|"
    r"workspace feeling|document queue|office touchdown desk|policy[- ]planning table|"
    r"fleet[- ]planning meeting|workspace standards check|office support point|"
    r"forms intake check|workteam|shared office hub|shared department team|"
    r"(?:administrative|administration)\s+office\s+(?:desk|table|counter|surface|nook)|"
    r"(?:classroom\s+)?activity\s+table|family\s+learning\s+table|home\s+craft\s+table|"
    r"(?:it[- ]led\s+(?:fleet\s+)?planning|it\s+(?:fleet\s+)?planning|fleet\s+planning)|"
    r"it\s+rollout\s+discussion|"
    r"managed\s+workplace(?:\s+feel)?|handoffs?|workgroups?|home[- ]office\s+planning|"
    r"senior\s+leader|it\s+(?:team|department)|finance\s+team|departmental\s+team|"
    r"(?:small\s+)?learning\s+table|reception[- ]side\s+desk|without\s+turning|"
    r"content\s+project|lining\s+up\s+the\s+day|sorting\s+everyday\s+household\s+tasks|"
    r"family[- ]project\s+feel|used[- ]through[- ]the[- ]day\s+character|"
    r"reviewing\s+everyday\s+materials|shared\s+windowed\s+area|"
    r"without\s+adding\s+(?:an?\s+)?[^.]{0,40}\bscene|"
    r"rather\s+than\s+(?:an?\s+)?[^.]{0,40}\bscene|"
    r"quick\s+preparation\s+point|adds?\s+(?:an?\s+)?simple\s+arrival\s+cue|"
    r"content\s+creation|shaping\s+a\s+point\s+for\s+discussion|"
    r"shared[- ]space\s+(?:work\s+)?stop|(?:loose\s+office\s+)?tasks?\s+(?:are\s+)?kept\s+in\s+order|"
    r"background\s+(?:is\s+)?reduced\s+to|only\s+a\s+narrow\s+slice\s+of|"
    r"without\s+showing\s+(?:an?\s+)?wider\b|close\s+(?:view|arrangement|study\s+area)|"
    r"(?:strip|slice|section|portion|piece|part)\s+of\s+(?:an?\s+)?(?:upholstered\s+)?"
    r"(?:banquette|chair|sofa|cabinet|shelving|bookshelf|rug|curtain)|"
    r"(?:banquette|chair|sofa|cabinet|shelving)\s+falls?\s+(?:softly\s+)?(?:behind|beyond)|"
    r"(?:banquette|chair|stool|sofa|cabinet|shelving|bookshelf|whiteboard|pinboard)\s+"
    r"(?:is\s+)?(?:partly|partially)\s+visible|"
    r"(?:book|textbook|magazine)\s+(?:rests?\s+)?on\s+(?:an?|the|its)\s+"
    r"(?:plain\s+)?(?:unmarked|unlabelled|unlabeled)\s+cover|"
    r"set\s+into\s+(?:warm\s+)?(?:window\s+light|natural\s+light|daylight)|"
    r"(?:shared\s+)?work\s+(?:has\s+)?paused\s+between\s+tasks|paused\s+review|"
    r"organized\s+display\s+feeling\s+neat|sits?\s+softly\b|"
    r"background\s+edge|used\s+for\s+preparing\s+for|polished\s+and\s+quietly\s+active|"
    r"shared[- ]space|classroom\s+study\s+table|background\s+table|softly\s+used)\b",
    re.IGNORECASE,
)
_UNNATURAL_EXPLANATION_RE = re.compile(
    r"\b(?:sits?|falls?)\s+softly\b|"
    r"\b(?:banquette|chair|stool|sofa|cabinet|shelving|bookshelf|whiteboard|pinboard)\s+"
    r"(?:is\s+)?(?:partly|partially)\s+visible\b|"
    r"\b(?:book|textbook|magazine)\s+(?:rests?\s+)?on\s+(?:an?|the|its)\s+"
    r"(?:plain\s+)?(?:unmarked|unlabelled|unlabeled)\s+cover\b",
    re.IGNORECASE,
)
_ENTERPRISE_SCENE_RE = re.compile(
    r"\b(?:executive|leadership|senior\s+manager|departments?|departmental|fleet|"
    r"workflows?|standards?|contracts?|invoices?|"
    r"(?:administrative|business|intake|paper|printed|request)\s+forms?|meeting\s+packets?|"
    r"client[- ]facing|follow[- ]through|shared\s+office\s+work)\b",
    re.IGNORECASE,
)
_VISUAL_FORMS_RE = re.compile(
    r"\b(?:abstract|architectural|geometric|organic|simple|sculptural)\s+forms?\b",
    re.IGNORECASE,
)
_IMPLAUSIBLE_PROP_ARRANGEMENT_RE = re.compile(
    r"\b(?:open\s+(?:ring\s+)?binder\b[^.]{0,60}\b(?:in|inside|within)\s+(?:an?\s+)?letter\s+tray|"
    r"letter\s+tray\b[^.]{0,60}\b(?:holding|containing)\s+(?:an?\s+)?open\s+(?:ring\s+)?binder)\b",
    re.IGNORECASE,
)
_VAGUE_OBJECT_RE = re.compile(
    r"\b(?:accessories|personal\s+items|supplies|unspecified\s+shelf\s+contents|"
    r"(?:simple\s+)?workplace\s+materials)\b",
    re.IGNORECASE,
)
_ABSTRACT_PAPER_ACTIVITY_RE = re.compile(
    r"\b(?:forms?|records?|documents?|papers?)\s+"
    r"(?:intake|workflow|processing|management|review|planning|policy|check)\b",
    re.IGNORECASE,
)
_ENVIRONMENT_TEXT_CONFLICTS = {
    "Office": re.compile(
        r"\b(?:home[- ]office|home workspace|living room|household|residential)\b",
        re.I,
    ),
    "Home": re.compile(r"\b(?:corporate office|classroom|creative studio|gaming room|caf[ée])\b", re.I),
    "Education": re.compile(r"\b(?:corporate office|home workspace|living room|creative studio|gaming room|caf[ée])\b", re.I),
    "Gaming": re.compile(r"\b(?:corporate office|home workspace|living room|classroom|creative studio|caf[ée])\b", re.I),
    "Café": re.compile(r"\b(?:corporate office|home workspace|living room|classroom|creative studio|gaming room)\b", re.I),
    "Creative Studio": re.compile(r"\b(?:corporate office|home workspace|living room|classroom|gaming room|caf[ée])\b", re.I),
}
_METADATA_TOKENS = frozenset(
    {
        "_chatsession",
        "author",
        "authoring",
        "authoringmetadata",
        "metadata",
        "systeminstructions",
    }
)
_SUPPORT_OR_ARCHITECTURE_GROUPS = frozenset(
    {
        "architecture",
        "ceiling",
        "desk",
        "floor",
        "support_surface",
        "table",
        "wall",
        "window",
        "work_surface",
    }
)
_SUPPORT_PHRASE_RE = re.compile(
    r"(?:^|\s)(?:desks?|tables?|tabletops?|work surfaces?|worktops?|"
    r"counters?|countertops?)$"
)


def _issue(code: str, path: str, detail: str) -> dict[str, str]:
    return {"code": code, "path": path, "detail": detail}


def _json_path(parts: Iterable[Any]) -> str:
    escaped = [str(part).replace("~", "~0").replace("/", "~1") for part in parts]
    return "" if not escaped else "/" + "/".join(escaped)


def _normalise_text(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def _words(value: str) -> tuple[str, ...]:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = value.replace("-", " ").replace("/", " ")
    return tuple(re.findall(r"[^\W_]+", value, flags=re.UNICODE))


def _decode_pointer(pointer: str) -> list[str]:
    if pointer == "":
        return []
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise KeyError(pointer)
    tokens: list[str] = []
    for encoded in pointer[1:].split("/"):
        if re.search(r"~(?:[^01]|$)", encoded):
            raise KeyError(pointer)
        tokens.append(encoded.replace("~1", "/").replace("~0", "~"))
    return tokens


def _pointer_value(root: Any, pointer: str) -> tuple[Any, list[str]]:
    tokens = _decode_pointer(pointer)
    current = root
    for token in tokens:
        if isinstance(current, dict) and token in current:
            current = current[token]
        elif (
            isinstance(current, list)
            and token.isdigit()
            and (token == "0" or not token.startswith("0"))
            and int(token) < len(current)
        ):
            current = current[int(token)]
        else:
            raise KeyError(pointer)
    return current, tokens


def normalize_invalid_evidence(
    output: Any, request: Any
) -> tuple[Any, list[dict[str, Any]]]:
    """Remove mechanically invalid citations without inventing evidence.

    The raw model object is never mutated. When no exact citation from a
    document remains for one candidate, that document's score components are
    zeroed. Scene prose, prop IDs, explanations, and valid citations are never
    changed here.
    """

    normalized = copy.deepcopy(output)
    changes: list[dict[str, Any]] = []
    if not isinstance(normalized, dict) or not isinstance(normalized.get("prompts"), list):
        return normalized, changes
    if not isinstance(request, dict):
        return normalized, changes

    for prompt_index, candidate in enumerate(normalized["prompts"]):
        if not isinstance(candidate, dict) or not isinstance(candidate.get("evidence"), list):
            continue
        kept: list[Any] = []
        valid_documents: set[str] = set()
        for evidence_index, evidence in enumerate(candidate["evidence"]):
            reason: str | None = None
            document: Any = None
            if not isinstance(evidence, dict) or set(evidence) != {"document", "path", "quote"}:
                kept.append(evidence)
                continue
            document = evidence["document"]
            pointer = evidence["path"]
            quote = evidence["quote"]
            if document not in DOCUMENTS or document not in request:
                reason = "document_invalid"
            elif not isinstance(pointer, str) or not isinstance(quote, str) or not quote.strip():
                reason = "citation_fields_invalid"
            else:
                try:
                    source_value, tokens = _pointer_value(request[document], pointer)
                except KeyError:
                    reason = "path_missing"
                else:
                    normalized_tokens = {
                        re.sub(r"[^a-z0-9_]", "", token.casefold()) for token in tokens
                    }
                    if normalized_tokens.intersection(_METADATA_TOKENS) or any(
                        token.startswith("_") for token in tokens
                    ):
                        reason = "authoring_metadata"
                    elif not isinstance(source_value, str):
                        reason = "path_not_string"
                    elif quote not in source_value:
                        reason = "quote_not_verbatim"
            if reason is None:
                kept.append(evidence)
                valid_documents.add(document)
            else:
                changes.append(
                    {
                        "action": "remove_invalid_evidence",
                        "prompt_index": prompt_index,
                        "evidence_index": evidence_index,
                        "document": document,
                        "reason": reason,
                    }
                )
        candidate["evidence"] = kept

        components = candidate.get("score_components")
        if isinstance(components, dict):
            for document in DOCUMENTS:
                document_components = components.get(document)
                if document in valid_documents or not isinstance(document_components, dict):
                    continue
                for component in COMPONENTS:
                    old_value = document_components.get(component)
                    if isinstance(old_value, int) and old_value != 0:
                        document_components[component] = 0
                        changes.append(
                            {
                                "action": "zero_ungrounded_component",
                                "prompt_index": prompt_index,
                                "document": document,
                                "component": component,
                                "before": old_value,
                                "after": 0,
                            }
                        )
        try:
            normalized_score = _source_score(candidate)
        except (KeyError, TypeError):
            normalized_score = None
        if normalized_score == 0 and candidate.get("relationship") != "creative_departure":
            old_relationship = candidate.get("relationship")
            candidate["relationship"] = "creative_departure"
            changes.append(
                {
                    "action": "align_zero_score_relationship",
                    "prompt_index": prompt_index,
                    "before": old_relationship,
                    "after": "creative_departure",
                }
            )
    return normalized, changes


def _source_score(candidate: dict[str, Any]) -> int:
    components = candidate["score_components"]
    return sum(
        max(components["smart_brief"][name], components["source_messaging"][name])
        for name in COMPONENTS
    )


def _camera_is_top_oblique(camera: Any) -> bool:
    return isinstance(camera, dict) and camera.get("elevation") == "top_oblique"


def _device_match(text: str) -> str | None:
    allowed_spans = [match.span() for match in _FURNITURE_DESKTOP_RE.finditer(text)]
    allowed_spans.extend(match.span() for match in _NONCOMPUTING_SCREEN_RE.finditer(text))
    # "display shelving" is room furnishing, not a computing display.
    allowed_spans.extend(match.span() for match in _DISPLAY_SHELVING_RE.finditer(text))
    for match in _DEVICE_RE.finditer(text):
        if any(start <= match.start() and match.end() <= end for start, end in allowed_spans):
            continue
        return match.group(0)
    return None


def _catalog_index(catalog: Any) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    required_catalog_fields = {
        "version", "revision", "purpose", "source_sha256", "entries"
    }
    if not isinstance(catalog, dict) or set(catalog) != required_catalog_fields:
        raise ValueError("catalog fields are malformed")
    if (
        catalog["version"] != "hp-v6-approved-props-v1"
        or not isinstance(catalog["revision"], str)
        or not catalog["revision"].strip()
        or catalog["purpose"] not in {"production", "test_fixture"}
        or not isinstance(catalog["source_sha256"], str)
        or not re.fullmatch(r"[0-9a-f]{64}", catalog["source_sha256"])
        or not isinstance(catalog["entries"], list)
    ):
        raise ValueError("catalog metadata is malformed")
    entries: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(catalog["entries"]):
        if not isinstance(entry, dict):
            raise ValueError(f"catalog entry {index} is not an object")
        required = {"id", "environment", "role", "name", "repetition_groups", "aliases"}
        if set(entry) != required:
            raise ValueError(f"catalog entry {index} has malformed fields")
        prop_id = entry["id"]
        groups = entry["repetition_groups"]
        aliases = entry["aliases"]
        if (
            not isinstance(prop_id, str)
            or not isinstance(entry["environment"], str)
            or entry["environment"] not in ENVIRONMENTS
            or not isinstance(groups, list)
            or not groups
            or any(not isinstance(group, str) or not group for group in groups)
            or len(groups) != len(set(groups))
            or not isinstance(aliases, list)
            or not aliases
            or any(not isinstance(alias, str) or not alias.strip() for alias in aliases)
        ):
            raise ValueError(f"catalog entry {index} is malformed")
        if prop_id in entries:
            raise ValueError(f"duplicate catalog ID {prop_id}")
        entries[prop_id] = entry

    lexicon = load_lexicon()
    if not isinstance(lexicon, list):
        raise ValueError("prop lexicon is malformed")
    return entries, lexicon


def _phrase_index(
    lexicon: list[dict[str, Any]], catalog_entries: Iterable[dict[str, Any]]
) -> dict[tuple[str, ...], set[str]]:
    phrases: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for item in lexicon:
        if not isinstance(item, dict) or set(item) != {"phrase", "groups"}:
            raise ValueError("prop lexicon entry is malformed")
        phrase = _words(item["phrase"]) if isinstance(item["phrase"], str) else ()
        groups = item["groups"]
        if not phrase or not isinstance(groups, list) or any(not isinstance(g, str) for g in groups):
            raise ValueError("prop lexicon entry is malformed")
        phrases[phrase].update(groups)
    # Test fixtures and pinned catalogs remain self-contained: their reviewed
    # aliases are always recognized even when absent from the broader lexicon.
    for entry in catalog_entries:
        for alias in entry["aliases"]:
            phrase = _words(alias)
            if phrase:
                phrases[phrase].update(entry["repetition_groups"])
    return phrases


def _known_matches(
    text: str, phrases: dict[tuple[str, ...], set[str]]
) -> list[tuple[str, set[str]]]:
    """Return longest, left-to-right, nonoverlapping known-object matches."""

    words = _words(text)
    by_first: dict[str, list[tuple[tuple[str, ...], set[str]]]] = defaultdict(list)
    for phrase, groups in phrases.items():
        by_first[phrase[0]].append((phrase, groups))
    for choices in by_first.values():
        choices.sort(key=lambda item: (-len(item[0]), item[0]))

    found: list[tuple[str, set[str]]] = []
    position = 0
    while position < len(words):
        selected: tuple[tuple[str, ...], set[str]] | None = None
        for phrase, groups in by_first.get(words[position], []):
            if words[position : position + len(phrase)] == phrase:
                selected = (phrase, groups)
                break
        if selected is None:
            position += 1
            continue
        phrase, groups = selected
        found.append((" ".join(phrase), set(groups)))
        position += len(phrase)
    return found


def _is_support_or_architecture(phrase: str, groups: set[str]) -> bool:
    return bool(groups) and (
        groups.issubset(_SUPPORT_OR_ARCHITECTURE_GROUPS)
        or bool(_SUPPORT_PHRASE_RE.search(phrase))
    )


def validate_references(references: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(references, dict) or not isinstance(references.get("references"), list):
        raise ValueError("reference_library must contain a references list")
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(references["references"]):
        if not isinstance(item, dict):
            raise ValueError(f"reference {index} is not an object")
        ref_id = item.get("id")
        if (
            not isinstance(ref_id, str)
            or not re.fullmatch(r"CT(?:0[1-9]|1[0-8])", ref_id)
            or item.get("environment") not in ENVIRONMENTS - {"Education"}
            or not isinstance(item.get("text"), str)
            or not item["text"].strip()
        ):
            raise ValueError(f"reference {index} is malformed")
        if ref_id in result:
            raise ValueError(f"duplicate reference ID {ref_id}")
        result[ref_id] = item
    if not result:
        raise ValueError("reference_library must not be empty")
    return result


def _validate_request(request: Any) -> list[dict[str, str]]:
    if not isinstance(request, dict):
        return [_issue("request_invalid", "", "request must be an object")]
    expected = {"smart_brief", "source_messaging", "camera_tag"}
    if set(request) != expected:
        return [
            _issue(
                "request_fields",
                "",
                f"request fields must be exactly {sorted(expected)}",
            )
        ]
    errors: list[dict[str, str]] = []
    for document in DOCUMENTS:
        value = request[document]
        if not isinstance(value, (str, dict)):
            errors.append(
                _issue("request_document_type", f"/{document}", "must be a string or object")
            )
    if not isinstance(request["camera_tag"], str) or not request["camera_tag"].strip():
        errors.append(_issue("camera_tag_invalid", "/camera_tag", "must be a non-blank string"))
    return errors


def validate_output(
    output: Any,
    request: Any,
    catalog: Any,
    camera: Any,
    references: Any,
) -> dict[str, Any]:
    """Validate raw V6 model output without modifying any caller-owned value."""

    errors = _validate_request(request)
    warnings: list[dict[str, str]] = []
    if errors:
        return {"passed": False, "errors": errors, "warnings": warnings}

    try:
        schema = json.loads(MODEL_OUTPUT_SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "passed": False,
            "errors": [_issue("schema_unavailable", "", str(exc))],
            "warnings": warnings,
        }
    schema_errors = sorted(
        jsonschema.Draft202012Validator(schema).iter_errors(output),
        key=lambda exc: tuple(str(part) for part in exc.absolute_path),
    )
    if schema_errors:
        errors.extend(
            _issue("schema_invalid", _json_path(exc.absolute_path), exc.message)
            for exc in schema_errors
        )
        return {"passed": False, "errors": errors, "warnings": warnings}

    try:
        catalog_by_id, lexicon = _catalog_index(catalog)
        phrases = _phrase_index(lexicon, catalog_by_id.values())
    except (ValueError, TypeError, OSError) as exc:
        return {
            "passed": False,
            "errors": [_issue("catalog_invalid", "", str(exc))],
            "warnings": warnings,
        }
    try:
        refs = validate_references(references)
    except (ValueError, TypeError) as exc:
        return {
            "passed": False,
            "errors": [_issue("references_invalid", "", str(exc))],
            "warnings": warnings,
        }

    prompts = output["prompts"]
    normalized_texts: dict[str, int] = {}
    global_groups: dict[str, list[int]] = defaultdict(list)
    represented_environments: set[str] = set()
    top_oblique = _camera_is_top_oblique(camera)

    for prompt_index, candidate in enumerate(prompts):
        base = f"/prompts/{prompt_index}"
        represented_environments.add(candidate["environment"])
        text = candidate["text"]
        if not text.strip():
            errors.append(_issue("prompt_text_blank", f"{base}/text", "text must not be blank"))
        else:
            normalized = _normalise_text(text)
            if normalized in normalized_texts:
                errors.append(
                    _issue(
                        "duplicate_prompt_text",
                        f"{base}/text",
                        f"duplicates prompt {normalized_texts[normalized] + 1} after normalization",
                    )
                )
            else:
                normalized_texts[normalized] = prompt_index
        for field in ("explanation", "ctech_explanation", "camera_fit_explanation"):
            if not candidate[field].strip():
                errors.append(
                    _issue("prompt_field_blank", f"{base}/{field}", f"{field} must not be blank")
                )
            else:
                unnatural_field = _UNNATURAL_EXPLANATION_RE.search(candidate[field])
                if unnatural_field:
                    errors.append(
                        _issue(
                            "unnatural_prompt_field_phrase",
                            f"{base}/{field}",
                            f"unnatural phrase: {unnatural_field.group(0)}",
                        )
                    )
        for departure_index, departure in enumerate(candidate["creative_departures"]):
            if not departure.strip():
                errors.append(
                    _issue(
                        "creative_departure_blank",
                        f"{base}/creative_departures/{departure_index}",
                        "creative departure descriptions must not be blank",
                    )
                )

        prop_ids = candidate["prop_ids"]
        if len(prop_ids) != len(set(prop_ids)):
            errors.append(_issue("duplicate_prop_id", f"{base}/prop_ids", "prop IDs must be unique"))
        declared_groups: set[str] = set()
        for prop_position, prop_id in enumerate(prop_ids):
            entry = catalog_by_id.get(prop_id)
            prop_path = f"{base}/prop_ids/{prop_position}"
            if entry is None:
                errors.append(_issue("unapproved_prop_id", prop_path, f"{prop_id!r} is not approved"))
                continue
            if entry["environment"] != candidate["environment"]:
                errors.append(
                    _issue(
                        "prop_environment_mismatch",
                        prop_path,
                        f"{prop_id} is approved for {entry['environment']}, not {candidate['environment']}",
                    )
                )
            for group in entry["repetition_groups"]:
                if group in declared_groups:
                    errors.append(
                        _issue(
                            "duplicate_candidate_group",
                            f"{base}/prop_ids",
                            f"repetition group {group!r} is declared more than once",
                        )
                    )
                declared_groups.add(group)
        for group in declared_groups:
            global_groups[group].append(prompt_index)

        # A material-qualified desktop or "desktop surface" is the focal
        # support, not an extra computer.  Mask it only for object recognition;
        # compounds such as "desktop calendar" remain catalog-controlled.
        object_text = _DESKTOP_SUPPORT_RE.sub(" ", text)
        # Business-language activity labels do not assert a visible paper prop.
        # They may still fail the separate natural-language rule.
        object_text = _ABSTRACT_PAPER_ACTIVITY_RE.sub(" ", object_text)
        # "architectural forms" and similar art/design phrases are shapes,
        # not administrative paper forms from the approved-object lexicon.
        object_text = _VISUAL_FORMS_RE.sub(" ", object_text)
        known_matches = _known_matches(object_text, phrases)
        detected_groups = {group for _, groups in known_matches for group in groups}
        for code, detail in check_content_policy(text, declared_groups | detected_groups):
            errors.append(_issue(code, f"{base}/text", detail))
        vague_object = _VAGUE_OBJECT_RE.search(text)
        if vague_object:
            errors.append(
                _issue(
                    "vague_unapproved_object_category",
                    f"{base}/text",
                    f"vague object category can introduce undeclared props: {vague_object.group(0)}",
                )
            )
        for phrase, groups in known_matches:
            missing = groups - declared_groups
            if missing and not _is_support_or_architecture(phrase, groups):
                errors.append(
                    _issue(
                        "undeclared_known_prop",
                        f"{base}/text",
                        f"known object {phrase!r} requires repetition group(s) {sorted(missing)}",
                    )
                )
        for group in sorted(declared_groups - detected_groups):
            errors.append(
                _issue(
                    "declared_prop_missing_from_text",
                    f"{base}/prop_ids",
                    f"declared repetition group {group!r} is not present in the prose",
                )
            )

        device = _device_match(text)
        if device:
            errors.append(_issue("computing_hardware", f"{base}/text", f"forbidden term: {device}"))
        motion = _CAMERA_MOTION_RE.search(text)
        if motion:
            errors.append(
                _issue("camera_motion_directive", f"{base}/text", f"forbidden directive: {motion.group(0)}")
            )
        unnatural = _UNNATURAL_PLACE_RE.search(text)
        if unnatural:
            errors.append(
                _issue("unnatural_place_phrase", f"{base}/text", f"unnatural phrase: {unnatural.group(0)}")
            )
        enterprise_language = _ENTERPRISE_SCENE_RE.search(text)
        if enterprise_language:
            errors.append(
                _issue(
                    "enterprise_scene_language",
                    f"{base}/text",
                    f"keep enterprise source language in explanation/evidence, not scene prose: {enterprise_language.group(0)}",
                )
            )
        implausible_arrangement = _IMPLAUSIBLE_PROP_ARRANGEMENT_RE.search(text)
        if implausible_arrangement:
            errors.append(
                _issue(
                    "implausible_prop_arrangement",
                    f"{base}/text",
                    "An open binder cannot plausibly sit inside a letter tray; place approved props separately.",
                )
            )
        environment_conflict = _ENVIRONMENT_TEXT_CONFLICTS[candidate["environment"]].search(text)
        if environment_conflict:
            errors.append(
                _issue(
                    "environment_text_conflict",
                    f"{base}/text",
                    f"{candidate['environment']} prompt contains a conflicting setting: {environment_conflict.group(0)}",
                )
            )
        if top_oblique:
            incompatible = _TOP_OBLIQUE_INCOMPATIBLE_RE.search(text)
            if incompatible:
                errors.append(
                    _issue(
                        "top_oblique_incompatible_scene",
                        f"{base}/text",
                        f"top-oblique framing cannot reliably show {incompatible.group(0)!r}",
                    )
                )

        cited_documents: set[str] = set()
        seen_evidence: set[tuple[str, str, str]] = set()
        for evidence_index, evidence in enumerate(candidate["evidence"]):
            evidence_path = f"{base}/evidence/{evidence_index}"
            document = evidence["document"]
            pointer = evidence["path"]
            quote = evidence["quote"]
            key = (document, pointer, quote)
            if key in seen_evidence:
                errors.append(_issue("duplicate_evidence", evidence_path, "evidence is repeated"))
            seen_evidence.add(key)
            document_value = request[document]
            if isinstance(document_value, str) and pointer != "":
                errors.append(
                    _issue("evidence_path_scope", f"{evidence_path}/path", "string documents require path ''")
                )
                continue
            try:
                source_value, tokens = _pointer_value(document_value, pointer)
            except KeyError:
                errors.append(
                    _issue("evidence_path_missing", f"{evidence_path}/path", f"path {pointer!r} does not resolve")
                )
                continue
            normalized_tokens = {
                re.sub(r"[^a-z0-9_]", "", token.casefold()) for token in tokens
            }
            if normalized_tokens.intersection(_METADATA_TOKENS) or any(
                token.startswith("_") for token in tokens
            ):
                errors.append(
                    _issue(
                        "evidence_authoring_metadata",
                        f"{evidence_path}/path",
                        "authoring/session metadata cannot be source evidence",
                    )
                )
                continue
            if not isinstance(source_value, str):
                errors.append(
                    _issue("evidence_not_string", f"{evidence_path}/path", "evidence path must resolve to a string")
                )
                continue
            if not quote.strip():
                errors.append(_issue("evidence_quote_blank", f"{evidence_path}/quote", "quote must not be blank"))
                continue
            if quote not in source_value:
                errors.append(
                    _issue("evidence_quote_not_verbatim", f"{evidence_path}/quote", "quote is not verbatim at the cited path")
                )
                continue
            cited_documents.add(document)

        for document in DOCUMENTS:
            if document not in cited_documents and any(
                candidate["score_components"][document].values()
            ):
                errors.append(
                    _issue(
                        "ungrounded_document_components",
                        f"{base}/score_components/{document}",
                        f"nonzero {document} components require valid evidence from that document",
                    )
                )

        source_score = _source_score(candidate)
        if source_score == 0 and candidate["relationship"] != "creative_departure":
            errors.append(
                _issue(
                    "zero_score_relationship",
                    f"{base}/relationship",
                    "zero source relevance requires relationship=creative_departure",
                )
            )
        if candidate["relationship"] == "creative_departure" and source_score > 59:
            errors.append(
                _issue(
                    "creative_departure_score",
                    f"{base}/relationship",
                    f"creative_departure cannot have derived source score {source_score}",
                )
            )

        reference = refs.get(candidate["ctech_reference_id"])
        if reference is None:
            errors.append(
                _issue(
                    "ctech_reference_missing",
                    f"{base}/ctech_reference_id",
                    "reference ID is absent from the supplied library",
                )
            )
        else:
            environment = candidate["environment"]
            ref_environment = reference["environment"]
            allowed_cross_reference = environment == "Education" and ref_environment in {
                "Home", "Office", "Creative Studio"
            }
            if environment != ref_environment and not allowed_cross_reference:
                errors.append(
                    _issue(
                        "ctech_environment_mismatch",
                        f"{base}/ctech_reference_id",
                        f"{environment} cannot cite a {ref_environment} reference",
                    )
                )
            if candidate["ctech_reference_score"] == 100 and (
                text != reference["text"] or environment != ref_environment
            ):
                errors.append(
                    _issue(
                        "ctech_exact_match_required",
                        f"{base}/ctech_reference_score",
                        "score 100 requires exact reference text and environment",
                    )
                )

    for group, prompt_indexes in sorted(global_groups.items()):
        if len(prompt_indexes) > 1:
            errors.append(
                _issue(
                    "repetition_group_reused",
                    "/prompts",
                    f"group {group!r} is used by prompts {[index + 1 for index in prompt_indexes]}",
                )
            )

    if len(represented_environments) < 4:
        errors.append(
            _issue(
                "insufficient_environment_diversity",
                "/prompts",
                "ten-candidate banks must use at least four plausible environments; "
                f"found {sorted(represented_environments)}",
            )
        )

    for field in ("source_conflicts", "limitations"):
        for index, value in enumerate(output["debug"][field]):
            if not value.strip():
                errors.append(
                    _issue("debug_item_blank", f"/debug/{field}/{index}", "debug items must not be blank")
                )
    if not output["debug"]["environment_rationale"].strip():
        errors.append(
            _issue(
                "environment_rationale_blank",
                "/debug/environment_rationale",
                "environment rationale must not be blank",
            )
        )

    warnings.append(
        _issue(
            "unknown_prose_objects_unverified",
            "/prompts",
            "Known-lexicon checks do not establish the absence of every possible unlisted object.",
        )
    )
    return {"passed": not errors, "errors": errors, "warnings": warnings}


def finalize_output(output: dict[str, Any], *, camera: Any, catalog: dict[str, Any]) -> dict[str, Any]:
    """Add host-owned derived fields and rank a raw, structurally valid bank."""

    if not isinstance(output, dict) or not isinstance(output.get("prompts"), list):
        raise ValueError("output must contain a prompts list")
    if len(output["prompts"]) != 10:
        raise ValueError("output must contain exactly ten prompts")
    if not isinstance(output.get("debug"), dict):
        raise ValueError("output must contain a debug object")
    if not isinstance(catalog, dict):
        raise ValueError("catalog must be an object")

    finalized = copy.deepcopy(output)
    indexed: list[tuple[int, dict[str, Any]]] = []
    for index, candidate in enumerate(finalized["prompts"]):
        try:
            candidate["source_relevance_score"] = _source_score(candidate)
            ctech_score = candidate["ctech_reference_score"]
        except (KeyError, TypeError) as exc:
            raise ValueError(f"prompt {index} cannot be finalized: {exc}") from exc
        indexed.append((index, candidate))

    ranked = sorted(
        indexed,
        key=lambda pair: (
            -pair[1]["source_relevance_score"],
            -pair[1]["ctech_reference_score"],
        ),
    )
    finalized["prompts"] = [candidate for _, candidate in ranked]
    for rank, candidate in enumerate(finalized["prompts"], start=1):
        candidate["id"] = f"p{rank}"

    finalized["debug"]["provenance"] = {
        "finalizer_version": "v6-deterministic-finalizer-r1",
        "camera": copy.deepcopy(camera),
        "catalog": {
            key: copy.deepcopy(catalog.get(key))
            for key in ("version", "revision", "purpose", "source_sha256")
        },
        "source_relevance": "sum of per-component maxima across the two documents",
        "ranking": "stable descending source relevance, then C-Tech reference score",
    }
    return finalized
