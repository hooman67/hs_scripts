"""Deterministic validation and finalization for V6.5 model output.

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
    from .surfaces import audit_bank, infer_primary_support
except ImportError:  # pragma: no cover
    from catalog import load_lexicon
    from content_policy import check_content_policy
    from surfaces import audit_bank, infer_primary_support


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
    r"game consoles?|handheld consoles?|screens?|headphones?|headsets?|keyboards?|"
    r"mice|mouse|controllers?|speakers?|webcams?|cameras?|televisions?|tv|chargers?|"
    r"audio equipment|plasma globe)\b",
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
    r"(?:focus|planning|briefing|policy|operations|workflow|support|intake|"
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
    r"shared[- ]space|classroom\s+study\s+table|softly\s+used)\b",
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
_OR_TOKEN_RE = re.compile(r"\bor\b", re.IGNORECASE)
_APPROXIMATE_QUANTITY_OR_RE = re.compile(
    r"\b(?:two|2)\s+or\s+(?:three|3)\b", re.IGNORECASE
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


def _find_unresolved_scene_alternative(text: str) -> re.Match[str] | None:
    """Return an `or` choice that leaves a visible scene detail unresolved."""

    quantity_spans = [match.span() for match in _APPROXIMATE_QUANTITY_OR_RE.finditer(text)]
    for match in _OR_TOKEN_RE.finditer(text):
        if any(start <= match.start() < end for start, end in quantity_spans):
            continue
        clause_start = max(
            text.rfind(".", 0, match.start()),
            text.rfind("!", 0, match.start()),
            text.rfind("?", 0, match.start()),
            text.rfind(";", 0, match.start()),
        )
        prefix = text[clause_start + 1 : match.start()]
        exclusion = (
            r"(?:(?:any|visible|readable|legible|human|cropped)\s+)*"
            r"(?:text|writing|lettering|annotations?|signatures?|labels?|logos?|"
            r"numbers?|titles?|people|faces?|portraits?|hands?|arms?|figures?)"
        )
        if re.search(
            rf"\b(?:without|no)\s+{exclusion}(?:\s*,\s*{exclusion})*\s*,?\s*$",
            prefix, re.I,
        ):
            continue
        return match
    return None
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
        "instructions",
        "rejectedcopy",
        "excludedexamples",
    }
)
_ARCHITECTURE_GROUPS = frozenset(
    {
        "architecture",
        "ceiling",
        "floor",
        "wall",
        "window",
    }
)

_SEMANTIC_PHRASE_FAMILIES = {
    "modern_office": re.compile(
        r"\b(?:modern(?: corporate)? office|contemporary corporate office|polished modern workplace)\b", re.I
    ),
    "bright_modern": re.compile(r"\b(?:bright modern|light-filled modern|bright contemporary)\b", re.I),
    "warm_natural_light": re.compile(
        r"\b(?:warm natural light|warm daylight|warm window light|soft warm daylight)\b", re.I
    ),
    "soft_daylight": re.compile(
        r"\b(?:soft daylight|gentle daylight|diffused daylight|soft natural light)\b", re.I
    ),
    "window_proximity": re.compile(
        r"\b(?:near|beside|positioned by) a window\b|\bwindow-side\b", re.I
    ),
    "paper_has_no_text": re.compile(
        r"\b(?:blank(?: unmarked)? pages|unmarked pages|plain blank paper)\b", re.I
    ),
    "markings_are_indistinct": re.compile(
        r"\b(?:indistinct markings|non-readable markings|illegible writing|non-legible details)\b", re.I
    ),
    "lived_in": re.compile(
        r"\b(?:lived-in|authentic everyday use|casually used|everyday working feel)\b", re.I
    ),
    "clean_professional": re.compile(
        r"\b(?:clean professional feel|polished workplace|refined professional atmosphere)\b", re.I
    ),
    "layered_depth": re.compile(
        r"\b(?:layered depth|natural depth|furnishings (?:extend|extending) into the background)\b", re.I
    ),
    "casual_arrangement": re.compile(
        r"\b(?:casually arranged|set slightly askew|loosely grouped|naturally scattered)\b", re.I
    ),
    "simple_uncluttered": re.compile(
        r"\b(?:simple and uncluttered|restrained workspace|tidy minimal setting)\b", re.I
    ),
}

_PRINTER_RANDOM_FLOOR_PROP_RE = re.compile(
    r"\b(?:puzzle|game|toy|blocks?)\b[^.]{0,45}\b(?:under|beneath|below|on)\s+"
    r"(?:the\s+)?(?:floor|rug|table)|"
    r"\b(?:under|beneath|below)\s+(?:the\s+)?(?:table|worktable)\b[^.]{0,45}"
    r"\b(?:puzzle|game|toy|blocks?)\b",
    re.IGNORECASE,
)
_PRINTER_SUPPORT_NOUN = (
    r"(?:work\s+table|worktable|table|work\s+surface|cabinet(?:\s+top)?|"
    r"credenza(?:\s+top)?|sideboard(?:\s+top)?|worktop|countertop|"
    r"equipment\s+counter|printer\s+counter|counter)"
)
_PRINTER_SUPPORT_DRINK_RE = re.compile(
    rf"\b{_PRINTER_SUPPORT_NOUN}\b[^.]{{0,160}}\b(?:water\s+carafe|water\s+glass|"
    r"drinking\s+glass|ceramic\s+mug|coffee\s+cup|reusable\s+water\s+bottle|teapot)\b|"
    r"\b(?:water\s+carafe|water\s+glass|drinking\s+glass|ceramic\s+mug|coffee\s+cup|"
    rf"reusable\s+water\s+bottle|teapot)\b[^.]{{0,160}}\b{_PRINTER_SUPPORT_NOUN}\b",
    re.IGNORECASE,
)
_PRINTER_SEATING_ALIGNMENT_RE = re.compile(
    r"\b(?:chair|stool)\b[^.]{0,55}\b(?:lines?\s+up\s+nearby|pulled\s+up|"
    r"pulled\s+into\s+(?:working\s+)?position|tucked\s+(?:under|at)|"
    rf"positioned\s+(?:at|beside|next\s+to)\s+(?:the\s+)?{_PRINTER_SUPPORT_NOUN})\b",
    re.IGNORECASE,
)
_PRINTER_ACTIVE_SUPPORT_PROP_RE = re.compile(
    rf"\b{_PRINTER_SUPPORT_NOUN}\b[^.]{{0,25}}\b(?:holds?|holding|supports?|"
    r"supporting|carries|carrying|features?|bearing|with)\b[^.]{0,100}\b(?:notebook|reading\s+glasses|"
    r"sewing\s+box|measuring\s+(?:strip|tape)|palette|paintbrush(?:es)?|swatches?|"
    r"scissors|puzzle|chess|game|globe|abacus|model|(?<!color-)blocks?|pencils?|pens?|craft\s+mat|"
    r"candle|pastry|food|cups?|mugs?|bowls?|plates?)\b|"
    r"\b(?:notebook|reading\s+glasses|sewing\s+box|measuring\s+(?:strip|tape)|palette|"
    r"paintbrush(?:es)?|swatches?|scissors|puzzle|chess|game|globe|abacus|model|(?<!color-)blocks?|"
    r"pencils?|pens?|craft\s+mat|candle|pastry|food|cups?|mugs?|bowls?|plates?)\b[^.]{0,170}"
    rf"\b(?:on|at|along)\b[^.]{{0,35}}\b(?:{_PRINTER_SUPPORT_NOUN}|table\s+edge|"
    r"table\s+corner|cabinet\s+edge|counter\s+edge|far\s+side)\b",
    re.IGNORECASE,
)

_SECONDARY_SUPPORT_FOR_SAFETY_RE = re.compile(
    r"\b(?:separate(?:\s+background)?|background|nearby)\s+"
    r"(?:(?:wide|low|storage|meeting|office|studio|service|work|study)\s+){0,4}"
    r"(?:cabinet|credenza|sideboard|work\s+table|worktable|table|counter)\b",
    re.I,
)
_WALL_DISPLAY_FOR_SAFETY_RE = re.compile(
    r"\b(?:a|an|the)\s+(?:(?:shallow|small|narrow|simple)\s+){0,3}"
    r"wall\s+(?:box|display\s+case)\s+(?:containing|holding|with)\s+"
    r"[^.;]{1,85}?\bmounted\s+on\s+(?:the\s+)?(?:(?:adjacent|side|back)\s+)?wall\b",
    re.I,
)
_FURNITURE_ACCESSORY_SUFFIX = (
    r"(?!\s+(?:(?:reading|task|writing)\s+)?"
    r"(?:lamp|clock|mirror|sculpture|ornament|mat|runner|tray|organizer|leg|edge|corner|"
    r"space|surface|height|top)s?\b)"
)
_SECONDARY_FURNITURE_RE = re.compile(
    r"\b(?:(?:background|nearby|separate|wide|low|storage|fitted|base|service|"
    r"office|studio|meeting|side)\s+){0,6}"
    r"(?:cabinets?|credenzas?|sideboards?|work\s+tables?|worktables?|tables?|desks?)\b"
    + _FURNITURE_ACCESSORY_SUFFIX,
    re.I,
)

_EMPTY_SHELF_RE = re.compile(
    r"\b(?:empty|blank|unpopulated|bare)\b[^.]{0,35}\b(?:(?:floating\s+)?shel(?:f|ves)|shelving|pegboard|display ledge)|"
    r"\b(?:(?:floating\s+)?shel(?:f|ves)|shelving|pegboard|display ledge)\b[^.]{0,35}\b(?:empty|blank|unpopulated|bare)\b",
    re.I,
)
_POPULATED_SHELF_RE = re.compile(
    r"\b(?:(?:floating\s+)?shel(?:f|ves)|shelving|pegboard|(?:storage\s+)?cubbies|display ledge|picture ledge|floating ledge)\b"
    r"[^.]{0,80}\b(?:holds?|holding|displays?|displaying|carries|carrying|contain(?:s|ing)?|lined with|with)\b|"
    r"\b(?:holds?|holding|displays?|displaying|carries|carrying|contains?|lined with)\b[^.]{0,80}"
    r"\b(?:(?:floating\s+)?shel(?:f|ves)|shelving|pegboard|(?:storage\s+)?cubbies|display ledge|picture ledge|floating ledge)\b",
    re.I,
)
_FURNITURE_SET_SQUARE_RE = re.compile(r"\bset\s+square\s+to\b", re.I)
_SHELF_GROUPS = frozenset({
    "open_shelving", "wall_shelving", "tool_pegboard", "storage_cubbies",
    "shadow_box", "peg_rail", "drying_rack", "material_roll_rack",
})
_CONTENT_CARRIER_GROUPS = _SHELF_GROUPS | frozenset({
    "tool_cup", "bread_basket", "reading_stand", "serving_board", "banding_wheel",
    "letter_tray", "wall_display_board", "flower_vessel", "napkin",
})
_CONTENT_CARRIER_NOUN_RE = re.compile(
    r"\b(?:bookcases?|bookshel(?:f|ves)|shel(?:f|ves)|shelving|"
    r"(?:display|picture|floating)\s+ledges?|ledges?|pegboards?|"
    r"(?:storage\s+)?cubb(?:y|ies)|(?:shadow|wall)\s+box(?:es)?|"
    r"(?:display\s+)?niches?|display\s+cases?|"
    r"(?:peg|wall)\s+rails?|(?:drying|roll|stock)\s+racks?|racks?|"
    r"(?:pen|pencil|tool)\s+cups?|brush\s+(?:holders?|jars?)|"
    r"bread\s+baskets?|book\s+rests?|reading\s+stands?|bread\s+boards?|"
    r"banding\s+wheels?|(?:letter|paper)\s+trays?|pinboards?|reference\s+boards?|"
    r"(?:book\s+)?cabinets?|vases?|napkin\s+holders?)\b",
    re.I,
)


def _declared_carrier_pairs(candidate, catalog_by_id):
    """Bind separately declared contents to an explicit local carrier relation."""
    mentions = {item["id"]: item["quote"] for item in candidate["prop_mentions"]}
    selected = {prop_id: catalog_by_id[prop_id] for prop_id in candidate["prop_ids"]
                if prop_id in catalog_by_id}
    pairs = {}
    for prop_id, carrier in selected.items():
        if not _CONTENT_CARRIER_GROUPS.intersection(carrier["repetition_groups"]):
            continue
        quote = mentions.get(prop_id, "")
        head = _CONTENT_CARRIER_NOUN_RE.search(quote)
        if head is None:
            continue
        pairs[prop_id] = set()
        if quote not in candidate["text"]:
            continue
        carrier_forms = set()
        for start, end in _form_spans(candidate["text"], carrier):
            carrier_forms.add(candidate["text"][start:end])
        if not carrier_forms:
            continue
        if len([
            entry for entry in selected.values()
            if _SHELF_GROUPS.intersection(entry["repetition_groups"])
        ]) == 1 and _SHELF_GROUPS.intersection(carrier["repetition_groups"]):
            carrier_forms.add("storage unit")
        carrier_phrase = "(?:" + "|".join(re.escape(form) for form in carrier_forms) + ")"
        for content_id, content in selected.items():
            content_quote = mentions.get(content_id, "")
            if (
                content_id == prop_id or content["role"] != "tabletop_or_movable"
                or not content_quote or content_quote not in candidate["text"]
            ):
                continue
            contents = re.escape(content_quote)
            forward = (
                rf"\b{carrier_phrase}\b"
                r"(?P<location>(?:(?!\b(?:that|which|who|while|whereas|but)\b)[^.!?;]){0,100}?)\b"
                r"(?P<relation>holds?|holding|displays?|displaying|shows?|contains?|containing|"
                r"carries|carry|carrying|stores?|has|have|filled\s+with|stocked\s+with|"
                r"populated\s+with|lined\s+with|with|supporting|supports?)\b"
                rf"(?:(?!\b(?:while|whereas|but)\b)[^.!?;]){{0,100}}{contents}"
            )
            reverse = (
                rf"{contents}[^.!?;]{{0,100}}\b(?:on|in|inside|within|from)\b"
                rf"\s+(?:(?:the|a|an)\s+)?{carrier_phrase}\b"
            )
            attached = False
            for match in re.finditer(forward, candidate["text"], re.I):
                location = match.group("location")
                if re.search(r",\s+(?:a|an|the)\s+", location, re.I):
                    continue
                if match.group("relation").casefold() == "with" and re.search(
                    r"\b(?:desk|table|worktable|cabinet|bookcase|shelf|cup|tray)\b", location, re.I,
                ):
                    continue
                attached = True
                break
            if attached or re.search(reverse, candidate["text"], re.I):
                pairs[prop_id].add(content_id)
    return pairs


def _source_text(request: dict[str, Any]) -> str:
    return json.dumps(
        {document: request.get(document) for document in DOCUMENTS},
        ensure_ascii=False,
        sort_keys=True,
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


def _non_content_evidence(document: str, root: Any, tokens: list[str]) -> bool:
    normalized = {re.sub(r"[^a-z0-9_]", "", token.casefold()) for token in tokens}
    if normalized.intersection(_METADATA_TOKENS) or any(
        token.startswith("_") for token in tokens
    ):
        return True
    if not isinstance(root, dict) or not tokens:
        return False
    if document == "smart_brief":
        section = root.get(tokens[0])
        if not isinstance(section, dict):
            return False
        if {"content", "confidence", "confidence_rationale"} <= section.keys():
            return len(tokens) == 2 and tokens[1] in {"confidence", "confidence_rationale"}
        if tokens[0] in {"voiceOfCustomer", "seoGeo"} and "available" in section:
            return section["available"] is False or (
                len(tokens) == 2 and tokens[1] in {"available", "confidenceLabel"}
            )
        return False
    if document != "source_messaging" or not (
        isinstance(root.get("source_messaging"), list)
        and isinstance(root.get("product_identity"), dict)
        and "template_id" in root
    ):
        return False
    if tokens == ["template_id"]:
        return True
    if len(tokens) == 2 and tokens[0] == "product_identity":
        return tokens[1] in {"long_name", "short_name", "codename", "launch_timeframe"}
    if tokens[0] == "source_messaging":
        return (
            len(tokens) == 3 and tokens[1].isdigit() and tokens[2] == "block"
        ) or (
            len(tokens) == 5 and tokens[1].isdigit() and tokens[2] == "fields"
            and tokens[3].isdigit() and tokens[4] in {"row", "label"}
        )
    return (
        len(tokens) == 3 and tokens[1].isdigit()
        and (
            tokens[0] == "etail_messaging" and tokens[2] in {"row", "label", "container"}
            or tokens[0] == "footnotes" and tokens[2] in {"number", "status"}
        )
    )


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
                    if _non_content_evidence(document, request[document], tokens):
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
        catalog["version"] != "hp-v6.5-approved-props-v1"
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
        # Reviewed names can contain alternatives missing from legacy aliases,
        # e.g. 'low storage cabinet or tall filing cabinet with no labels'.
        # Recognize those exact approved names without broadening their groups.
        named_furniture = [part for part in entry["name"].split(" or ")
                           if re.search(r"\b(?:cabinets?|credenzas?|sideboards?|worktables?|tables?|desks?)\b", part)]
        for alias in [*entry["aliases"], *named_furniture]:
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


def _form_spans(text, entry):
    spans = set()
    for alias in entry["aliases"]:
        words = _words(alias)
        if words:
            separator = r"[\W_]+(?:(?:plain|unmarked|unbranded|nonhuman|abstract|architectural|geometric)\s+){0,3}"
            pattern = r"\b" + separator.join(re.escape(word) for word in words) + r"\b"
            spans.update(match.span() for match in re.finditer(pattern, text, re.I))
    if spans:
        first_end = min(end for _, end in spans)
        heads = set(re.findall(
            r"\b(?:bookcases?|bookshel(?:f|ves)|notebooks?|chairs?|plants?|"
            r"desks?|worktables?|tables?|cups?|boards?|pinboards?|cabinets?|"
            r"sofas?|banquettes?|stools?|shelving)\b", entry["name"], re.I,
        ))
        heads.update(head + "s" for head in list(heads) if not head.endswith("s"))
        if heads.intersection({"chair", "chairs", "sofa", "banquette", "stool"}):
            heads.add("seating")
        if set(entry["repetition_groups"]).intersection(_SHELF_GROUPS):
            heads.add("book storage")
        if heads:
            references = re.compile(
                r"\b(?:the|this|that|same)\s+"
                r"(?:(?:counter|cabinet|worktop|desk|table|shelving)\s+and\s+)?"
                r"(?:mounted\s+)?(?P<head>"
                + "|".join(re.escape(head) for head in heads) + r")\b", re.I,
            )
            spans.update(
                match.span("head") for match in references.finditer(text)
                if match.start() >= first_end
            )
    return sorted(spans, key=lambda span: (-(span[1] - span[0]), span[0]))


def _mask_depicted_subjects(text, candidate, catalog_by_id):
    """Illustrated plants are not physical plants, but actual adjacent props are."""
    for mention in candidate["prop_mentions"]:
        entry = catalog_by_id.get(mention["id"])
        if (
            entry is None or mention["quote"] not in text
            or not re.search(r"\b(?:illustration|botanical|art|artwork|landscape)\b", entry["name"], re.I)
        ):
            continue
        quote = mention["quote"]
        offset = text.index(quote)
        for match in re.finditer(
            r"\b(?:showing|depicting|depicts?)\s+"
            r"(?P<subject>(?:(?:abstract|botanical|geometric|nonhuman|plant|plants|"
            r"leaves|flowers|landscape|studies|and|only)\b[\s,]*)+)",
            quote, re.I,
        ):
            text = _mask_span(text, offset + match.start("subject"), offset + match.end("subject"))
    return text


def _object_mentions(candidate, catalog_by_id):
    """Bind each declaration to a concrete noun, not an arbitrary exact quote."""
    bound, errors = {}, []
    for mention in candidate["prop_mentions"]:
        entry = catalog_by_id.get(mention["id"])
        quote = mention["quote"]
        if entry is None or quote not in candidate["text"]:
            continue
        spans = _form_spans(quote, entry)
        if not spans:
            errors.append(("prop_mention_form_mismatch", f"{mention['id']} quote must name its approved concrete form"))
            continue
        offset = candidate["text"].index(quote)
        bound[mention["id"]] = tuple(offset + value for value in spans[0])
    items = list(bound.items())
    for index, (prop_id, (start, end)) in enumerate(items):
        for other_id, (other_start, other_end) in items[index + 1:]:
            if max(start, other_start) < min(end, other_end):
                errors.append(("duplicate_physical_prop", f"{prop_id} and {other_id} identify the same object span"))
    return bound, errors


def _cited_setting(candidate, request, pattern):
    for evidence in candidate["evidence"]:
        document, pointer = evidence["document"], evidence["path"]
        try:
            value, tokens = _pointer_value(request[document], pointer)
        except KeyError:
            continue
        if (
            isinstance(value, str) and evidence["quote"] in value
            and not _non_content_evidence(document, request[document], tokens)
            and pattern.search(evidence["quote"])
        ):
            return True
    return False


def _is_architecture(groups: set[str]) -> bool:
    return bool(groups) and groups.issubset(_ARCHITECTURE_GROUPS)


def _furniture_head_has_alias(text, furniture, known_matches):
    """A catalogue alias can include modifiers outside the furniture detector.

    Match the noun at this exact location, not a matching alias elsewhere in
    the paragraph. For example, 'tall filing cabinet' stays catalogue-checked
    even when the broad detector captured only 'cabinet'.
    """
    head = re.search(r"\w+$", furniture.group(0))
    if head is None:
        return False
    start = furniture.start() + head.start()
    for phrase, _ in known_matches:
        pattern = r"\b" + r"[\W_]+".join(re.escape(word) for word in phrase.split()) + r"\b"
        for match in re.finditer(pattern, text, re.I):
            if match.start() <= start and match.end() >= furniture.end():
                return True
    return False


def _mask_span(text: str, start: int, end: int) -> str:
    """Replace one exact source span without changing later character offsets."""

    return text[:start] + (" " * (end - start)) + text[end:]


def _mask_primary_references(text: str, support: dict[str, Any]) -> str:
    """Exempt definite references to the same primary, never another furnishing.

    A later unqualified 'the cabinet' is ambiguous once a second cabinet has
    been named. Leave those later mentions visible to inventory checking.
    """
    groups = {
        "table": r"(?:worktable|table|desk)",
        "freestanding_cabinet": r"cabinet",
        "credenza_sideboard": r"(?:credenza|sideboard)",
        "fitted_counter": r"(?:cabinet|counter|countertop|worktop)",
    }
    noun = groups.get(support["family"])
    if not noun:
        return text
    pattern = re.compile(rf"\b(?:the|this)\s+(?P<noun>{noun})\b", re.I)
    head = re.compile(rf"\b{noun}s?\b" + _FURNITURE_ACCESSORY_SUFFIX, re.I)
    result = text
    previous = support["end"]
    for match in pattern.finditer(text, support["end"]):
        if head.search(text[previous:match.start()]):
            break
        result = _mask_span(result, match.start(), match.end())
        previous = match.end()
    return result


def _surface_device(camera: Any, request: Any) -> str | None:
    family = camera.get("device_family") if isinstance(camera, dict) else None
    if isinstance(family, str) and family.casefold() in {"laptop", "printer"}:
        return family.casefold()
    tag = request.get("camera_tag") if isinstance(request, dict) else None
    if isinstance(tag, str):
        normalized = tag.casefold()
        if normalized.startswith("laptop_"):
            return "laptop"
        if normalized.startswith("printer_"):
            return "printer"
    return None


def _surface_validation_issue(error: dict[str, Any], device_type: str) -> dict[str, str]:
    code = str(error.get("code", "primary_support_invalid"))
    row_id = error.get("row_id")
    path = f"/prompts/{row_id}/text" if isinstance(row_id, int) else "/prompts"
    compatible_codes = {
        "primary_support_not_found": (
            "printer_support_surface_missing"
            if device_type == "printer"
            else "laptop_support_surface_missing"
        ),
        "unsupported_printer_support": "printer_surface_implausible",
        "unsafe_printer_support": "printer_surface_implausible",
        "unsupported_laptop_support": "laptop_support_surface_implausible",
        "conflicting_primary_support": "primary_support_conflicting",
        "unknown_support_shape": "primary_support_shape_unknown",
        "conflicting_support_shape": "primary_support_shape_conflicting",
        "laptop_round_primary_minimum": "laptop_round_support_missing",
        "cafe_primary_support_not_round": "laptop_cafe_round_support_missing",
        "printer_support_family_minimum": "printer_support_family_diversity",
        "printer_non_table_primary_minimum": "printer_non_table_support_missing",
    }
    public_code = compatible_codes.get(code, code)
    bounded = {key: value for key, value in error.items() if key != "code"}
    if code == "primary_support_not_found":
        bounded["required_opening_support"] = (
            "Name an actual desk, table or worktable in the opening sentence, not an unspecified surface."
            if device_type == "laptop" else
            "Name a dedicated table/worktable, substantial cabinet/credenza/sideboard, or fitted base cabinets "
            "with a continuous worktop/countertop in the opening sentence."
        )
    return _issue(public_code, path, json.dumps(bounded, ensure_ascii=False, sort_keys=True))


def _printer_safety_text(text: str) -> str:
    """Mask explicitly secondary supports before checking the primary support role."""

    text = _WALL_DISPLAY_FOR_SAFETY_RE.sub(lambda match: " " * len(match.group(0)), text)
    text = re.sub(
        rf"\b(?:rather\s+than|not|never)\s+on\s+(?:the\s+)?{_PRINTER_SUPPORT_NOUN}\b|"
        r"\b(?:normal\s+)?(?:table|worktable|desk)\s+(?:height|space)\b",
        lambda match: " " * len(match.group(0)), text, flags=re.I,
    )
    text = re.sub(
        r"\b(?:separate|secondary)\s+(?:(?:background|work|study|office|studio|café|cafe)\s+){0,3}"
        r"(?:desks?|tables?|worktables?|side\s+tables?)\b",
        lambda match: " " * len(match.group(0)), text, flags=re.I,
    )
    return _SECONDARY_SUPPORT_FOR_SAFETY_RE.sub(lambda match: " " * len(match.group(0)), text)


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
    semantic_phrase_uses: dict[str, list[int]] = defaultdict(list)
    represented_environments: set[str] = set()
    top_oblique = _camera_is_top_oblique(camera)
    surface_device = _surface_device(camera, request)
    printer_request = surface_device == "printer"
    bank_policy = json.loads((HERE / "bank_policy.json").read_text())
    repeatable_phrases = set(bank_policy["repeatable_phrase_families"])

    primary_supports: dict[int, dict[str, Any]] = {}
    if surface_device is not None:
        surface_audit = audit_bank(prompts, surface_device)
        for row in surface_audit["rows"]:
            row_id = row["row_id"]
            if isinstance(row_id, int) and "support" in row:
                primary_supports[row_id] = row["support"]
        errors.extend(
            _surface_validation_issue(error, surface_device)
            for error in surface_audit["errors"]
        )

    for prompt_index, candidate in enumerate(prompts):
        base = f"/prompts/{prompt_index}"
        represented_environments.add(candidate["environment"])
        text = candidate["text"]
        primary_support = primary_supports.get(prompt_index)
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
            for family, pattern in _SEMANTIC_PHRASE_FAMILIES.items():
                if family not in repeatable_phrases and pattern.search(text):
                    semantic_phrase_uses[family].append(prompt_index)
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
        prop_mentions = candidate["prop_mentions"]
        mention_ids = [mention["id"] for mention in prop_mentions]
        if len(mention_ids) != len(set(mention_ids)):
            errors.append(
                _issue("duplicate_prop_mention", f"{base}/prop_mentions", "prop mention IDs must be unique")
            )
        if set(mention_ids) != set(prop_ids) or len(mention_ids) != len(prop_ids):
            errors.append(
                _issue(
                    "prop_mention_id_mismatch",
                    f"{base}/prop_mentions",
                    "prop_mentions must contain exactly one item for every declared prop ID",
                )
            )
        for mention_index, mention in enumerate(prop_mentions):
            quote = mention["quote"]
            mention_path = f"{base}/prop_mentions/{mention_index}/quote"
            if not quote.strip():
                errors.append(_issue("prop_mention_blank", mention_path, "mention quote must not be blank"))
            elif quote not in text:
                errors.append(
                    _issue(
                        "prop_mention_not_verbatim",
                        mention_path,
                        "mention quote must be an exact case-sensitive substring of scene text",
                    )
                )
            elif len(quote) > 160:
                errors.append(
                    _issue("prop_mention_too_long", mention_path, "mention quote must be 160 characters or fewer")
                )
        declared_groups: set[str] = set()
        object_spans, object_errors = _object_mentions(candidate, catalog_by_id)
        errors.extend(_issue(code, f"{base}/prop_mentions", detail) for code, detail in object_errors)
        carrier_pairs = _declared_carrier_pairs(candidate, catalog_by_id)
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
                declared_groups.add(group)
        for carrier_id, contents in carrier_pairs.items():
            groups = set(catalog_by_id[carrier_id]["repetition_groups"])
            if not contents and groups - {"letter_tray"}:
                errors.append(_issue(
                    "visible_contents_missing", f"{base}/prop_ids",
                    f"{carrier_id} needs an explicit local relationship to separately declared contents",
                ))

        selected_shelf_groups = declared_groups.intersection(_SHELF_GROUPS)
        if selected_shelf_groups:
            empty_shelf = _EMPTY_SHELF_RE.search(text)
            if empty_shelf:
                errors.append(
                    _issue(
                        "empty_shelving_or_pegboard",
                        f"{base}/text",
                        f"shelving and pegboards must be populated: {empty_shelf.group(0)}",
                    )
                )
            if not any(carrier_pairs.values()) and not _POPULATED_SHELF_RE.search(text):
                errors.append(_issue(
                    "shelf_population_missing", f"{base}/text",
                    "selected storage or display carrier must explicitly hold declared contents",
                ))
            if not any(
                catalog_by_id[prop_id]["role"] == "tabletop_or_movable"
                and prop_id not in carrier_pairs
                for prop_id in prop_ids if prop_id in catalog_by_id
            ):
                errors.append(_issue(
                    "shelf_contents_undeclared", f"{base}/prop_ids",
                    "selected storage or display carrier requires a separately declared content ID",
                ))
            for prop_id in prop_ids:
                entry = catalog_by_id.get(prop_id)
                if entry is not None and _SHELF_GROUPS.intersection(entry["repetition_groups"]):
                    if not carrier_pairs.get(prop_id):
                        errors.append(_issue(
                            "visible_contents_missing", f"{base}/prop_ids",
                            f"{prop_id} requires an explicit relationship to separately declared approved contents",
                        ))

        # Only the exact app-derived primary-support span is exempt from prop
        # recognition.  A second table, cabinet, credenza, sideboard, or other
        # furnishing remains visible to the closed-catalog checks below.
        object_text = text
        if primary_support is not None:
            object_text = _mask_primary_references(object_text, primary_support)
            object_text = _mask_span(
                object_text, primary_support["start"], primary_support["end"]
            )
        # Business-language activity labels do not assert a visible paper prop.
        # They may still fail the separate natural-language rule.
        object_text = _ABSTRACT_PAPER_ACTIVITY_RE.sub(" ", object_text)
        # "architectural forms" and similar art/design phrases are shapes,
        # not administrative paper forms from the approved-object lexicon.
        object_text = _VISUAL_FORMS_RE.sub(" ", object_text)
        # Furniture described as "set square to" a wall does not introduce
        # the triangular drafting tool named a set square.
        object_text = _FURNITURE_SET_SQUARE_RE.sub(" ", object_text)
        object_text = _mask_depicted_subjects(object_text, candidate, catalog_by_id)
        known_matches = _known_matches(object_text, phrases)
        detected_groups = {group for _, groups in known_matches for group in groups}
        selected_entries = [catalog_by_id[prop_id] for prop_id in prop_ids if prop_id in catalog_by_id]
        for code, detail in check_content_policy(
            text, declared_groups | detected_groups, objects=selected_entries, spans=object_spans,
            carriers=carrier_pairs,
        ):
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
        declared_spans = [span for entry in selected_entries for span in _form_spans(object_text, entry)]
        for phrase, groups in known_matches:
            pattern = r"\b" + r"[\W_]+".join(re.escape(word) for word in phrase.split()) + r"\b"
            covered = all(
                any(
                    (start <= match.start() and end >= match.end())
                    or (match.start() <= start and end == match.end())
                    for start, end in declared_spans
                )
                for match in re.finditer(pattern, object_text, re.I)
            )
            if not covered and not _is_architecture(groups):
                errors.append(
                    _issue(
                        "undeclared_known_prop",
                        f"{base}/text",
                        f"known object {phrase!r} requires its own approved concrete-form declaration",
                    )
                )
        for furniture in _SECONDARY_FURNITURE_RE.finditer(object_text):
            head = re.search(r"\w+$", furniture.group(0))
            if head is not None and any(
                start <= furniture.start() + head.start() and end >= furniture.end()
                for start, end in declared_spans
            ):
                continue
            # Catalog aliases (including fixture aliases) are handled by the
            # known-match loop.  This closes the bounded loophole for named
            # support furniture that has no approved alias at all.
            if not _known_matches(furniture.group(0), phrases) and not _furniture_head_has_alias(object_text, furniture, known_matches):
                errors.append(
                    _issue(
                        "undeclared_known_prop",
                        f"{base}/text",
                        f"support furniture {furniture.group(0)!r} has no approved catalogue entry",
                    )
                )
        for group in sorted(declared_groups - detected_groups):
            warnings.append(
                _issue(
                    "declared_prop_lexicon_match_unverified",
                    f"{base}/prop_ids",
                    f"declared repetition group {group!r} uses a verbatim model-supplied mention but is outside the bounded recognition lexicon",
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
        unresolved_alternative = _find_unresolved_scene_alternative(text)
        if unresolved_alternative:
            errors.append(
                _issue(
                    "unresolved_scene_alternative",
                    f"{base}/text",
                    "choose one concrete visible option instead of leaving an 'or' alternative",
                )
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
        if printer_request:
            random_floor_prop = _PRINTER_RANDOM_FLOOR_PROP_RE.search(text)
            if random_floor_prop:
                errors.append(
                    _issue(
                        "printer_random_floor_prop",
                        f"{base}/text",
                        f"printer-tag scene uses an unrelated floor/under-table prop: {random_floor_prop.group(0)}",
                    )
                )
            safety_text = _printer_safety_text(text)
            support_drink = _PRINTER_SUPPORT_DRINK_RE.search(safety_text)
            if support_drink:
                errors.append(
                    _issue(
                        "printer_support_drinkware",
                        f"{base}/text",
                        "printer equipment support must not double as a drink surface",
                    )
                )
            aligned_seating = _PRINTER_SEATING_ALIGNMENT_RE.search(safety_text)
            if aligned_seating:
                errors.append(
                    _issue(
                        "printer_support_seating",
                        f"{base}/text",
                        "printer equipment support must not read as an occupied seated workstation",
                    )
                )
            active_support_prop = _PRINTER_ACTIVE_SUPPORT_PROP_RE.search(safety_text)
            if active_support_prop:
                errors.append(
                    _issue(
                        "printer_support_personal_prop",
                        f"{base}/text",
                        "personal, leisure, learning, or creative activity props must stay off the dedicated printer support",
                    )
                )
            environment = candidate["environment"]
            if environment == "Café" and not _cited_setting(
                candidate, request, re.compile(r"\b(?:caf[ée]|coffee shop)\b", re.I),
            ):
                errors.append(
                    _issue(
                        "printer_environment_unsupported",
                        f"{base}/environment",
                        "Café requires explicit café or coffee-shop support in a source document for printer tags.",
                    )
                )
            if environment == "Gaming" and not _cited_setting(
                candidate, request, re.compile(r"\b(?:gaming|game room|gamer)\b", re.I),
            ):
                errors.append(
                    _issue(
                        "printer_environment_unsupported",
                        f"{base}/environment",
                        "Gaming requires explicit gaming support in a source document for printer tags.",
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
            if _non_content_evidence(document, document_value, tokens):
                errors.append(
                    _issue(
                        "evidence_authoring_metadata",
                        f"{evidence_path}/path",
                        "authoring/session or structured-document metadata cannot be source evidence",
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

    for family, prompt_indexes in sorted(semantic_phrase_uses.items()):
        if len(prompt_indexes) > 1:
            errors.append(
                _issue(
                    "semantic_phrase_family_reused",
                    "/prompts",
                    f"phrase family {family!r} is used by prompts {[index + 1 for index in prompt_indexes]}",
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

    surface_device = _surface_device(camera, {})
    if surface_device is not None:
        primary_support_audit = audit_bank(finalized["prompts"], surface_device)
        if not primary_support_audit["passed"]:
            raise ValueError("validated prompt bank failed primary-support finalization")
        supports_by_id = {
            row["row_id"]: row["support"] for row in primary_support_audit["rows"]
        }
        for candidate in finalized["prompts"]:
            candidate["primary_support"] = copy.deepcopy(
                supports_by_id[candidate["id"]]
            )
        finalized["debug"]["primary_support_audit"] = primary_support_audit

    finalized["debug"]["provenance"] = {
        "finalizer_version": "v6-deterministic-finalizer-r3-surface-recognition",
        "camera": copy.deepcopy(camera),
        "catalog": {
            key: copy.deepcopy(catalog.get(key))
            for key in ("version", "revision", "purpose", "source_sha256")
        },
        "source_relevance": "sum of per-component maxima across the two documents",
        "ranking": "stable descending source relevance, then C-Tech reference score",
    }
    return finalized
