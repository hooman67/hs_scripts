"""Bounded text checks for C-Tech's text/face guidance, not image guarantees."""
import re


_NEGATED_LEGIBLE_TEXT_RE = re.compile(
    r"\b(?:without(?:\s+requiring)?|(?:kept\s+)?free\s+of|avoid(?:ing)?|no|not|never|"
    r"omit(?:ting)?|exclud(?:e|ing))\s+(?:any\s+)?(?:clearly\s+)?"
    r"(?:readable|legible)\s+(?:text|words|lettering|handwriting|labels?|titles?|menus?|numbers?)\b",
    re.IGNORECASE,
)

_TEXT_CARRIER_GROUPS = frozenset(
    {
        "board_game",
        "book",
        "business_card_holder",
        "calendar",
        "clipboard",
        "color_swatches",
        "document_folder",
        "document_box",
        "globe",
        "letter_tiles",
        "magazine",
        "measuring_tape",
        "notebook",
        "paper_cards",
        "paper_documents",
        "pinboard",
        "ring_binder",
        "ruler",
        "set_square",
        "sticky_notes",
        "sugar_sachets",
        "protractor",
        "wall_map",
        "whiteboard",
    }
)
_FACE_BEARING_GROUPS = frozenset(
    {
        "brick_sculpture",
        "card_album",
        "clay_model",
        "figurine",
        "hobby_model",
        "jigsaw_puzzle",
        "origami",
        "photo_album",
        "reference_photos",
        "wooden_model",
        "wooden_puzzle",
    }
)
_ART_GROUPS = frozenset({"wall_art"})

_SAFE_TEXT_CARRIER_RE = re.compile(
    r"\b(?:blank|(?<!mostly )(?<!nearly )(?<!partly )empty|unlabelled|unlabeled|unmarked|label[- ]free|"
    r"non[ -]?(?:legible|readable)|unreadable|illegible|indistinct|"
    r"face[- ]down|plain[- ]covered|plain\s+(?:unmarked|unlabelled|unlabeled)|"
    r"(?:kept\s+)?free\s+of\s+(?:readable|legible)\s+(?:labels?|text|writing|words?)|"
    r"no\s+(?:(?:visible|readable|legible)\s+)?(?:lettering|labels?|markings?|measurements?|numbers?|place\s+names?|titles?|writing|dates?|words?|text)|"
    r"(?:labels?|markings?|numbers?|place\s+names?|text)\s+(?:are\s+|is\s+)?too\s+small\s+to\s+read|"
    r"(?:notes?|dates?|markings?|labels?|writing|text)\s+(?:is|are|kept|remains?)\s+"
    r"(?:non[ -]?(?:legible|readable)|unreadable|illegible|indistinct)|"
    r"clean\s+whiteboard|plain\s+(?:(?:reference|cork|classroom)\s+)?"
    r"(?:pinboard|bulletin\s+board)|"
    r"(?:original\s+)?abstract\s+(?:design|graphics?|shapes?)|simple\s+geometric\s+pieces)\b",
    re.IGNORECASE,
)
_SAFE_FACE_CARRIER_RE = re.compile(
    r"\b(?:closed\b[^.]{0,50}\b(?:plain|unmarked|unlabelled|unlabeled)\b|"
    r"(?:plain|unmarked|unlabelled|unlabeled)\b[^.]{0,50}\bclosed\b|"
    r"abstract|geometric|botanical|architectur(?:e|al)|landscape|still\s+life|"
    r"materials?|textures?|objects?|nonhuman|"
    r"without\s+(?:people|portraits?|human\s+(?:faces?|figures?))|"
    r"no\s+(?:people|portraits?|human\s+(?:faces?|figures?)))\b",
    re.IGNORECASE,
)
_SAFE_ART_RE = re.compile(
    r"\b(?:abstract|geometric|landscape|still\s+life|botanical|nonfigurative|"
    r"non-figurative|without\s+(?:people|portraits?|human\s+faces?)|"
    r"no\s+(?:people|portraits?|human\s+faces?))\b",
    re.IGNORECASE,
)

_OPEN_BINDER_RE = re.compile(
    r"\b(?:open|opened|partly\s+open)\b[^.]{0,45}\b(?:ring\s+)?binder\b|"
    r"\b(?:ring\s+)?binder\b[^.]{0,45}\b(?:open|opened|partly\s+open)\b",
    re.IGNORECASE,
)
_SAFE_OPEN_BINDER_PAGES_RE = re.compile(
    r"\b(?:blank|unmarked|non[ -]?(?:legible|readable)|unreadable|illegible|indistinct)"
    r"\s+(?:binder\s+)?pages?\b|"
    r"\b(?:binder\s+)?pages?\b\s+(?:are|remain|show(?:ing)?|with)\s+"
    r"(?:blank|unmarked|non[ -]?(?:legible|readable)|unreadable|illegible|indistinct)\b",
    re.IGNORECASE,
)
_DOCUMENT_BOX_RE = re.compile(r"\bdocument(?:\s+storage)?\s+box(?:es)?\b", re.IGNORECASE)
_SAFE_DOCUMENT_BOX_RE = re.compile(
    r"\b(?:plain|unmarked|unlabelled|unlabeled|label[- ]free)\b[^.]{0,45}"
    r"\bdocument(?:\s+storage)?\s+box(?:es)?\b|"
    r"\bdocument(?:\s+storage)?\s+box(?:es)?\b[^.]{0,45}\b"
    r"(?:plain|unmarked|unlabelled|unlabeled|label[- ]free)\b",
    re.IGNORECASE,
)
_MEASUREMENT_TOOL_GROUPS = frozenset({"ruler", "measuring_tape", "set_square", "protractor"})
_SAFE_MEASUREMENT_TOOL_RE = re.compile(
    r"\b(?:unmarked|non[ -]?(?:legible|readable)|unreadable|illegible|indistinct)\s+"
    r"(?:ruler|measuring\s+tape|set\s+square|protractor)\b|"
    r"\b(?:ruler|measuring\s+tape|set\s+square|protractor)\b\s+(?:is\s+)?unmarked\b|"
    r"\b(?:ruler|measuring\s+tape|set\s+square|protractor)\b\s+"
    r"(?:with|showing)\s+(?:no\s+(?:readable|legible)\s+(?:markings?|measurements?|numbers?)|"
    r"(?:non[ -]?(?:legible|readable)|unreadable|illegible|indistinct)\s+"
    r"(?:(?:measurement|scale)\s+)?(?:markings?|measurements?|numbers?)|"
    r"(?:markings?|measurements?|numbers?)\s+(?:are\s+)?"
    r"(?:non[ -]?(?:legible|readable)|unreadable|illegible|indistinct))\b",
    re.IGNORECASE,
)
_SAFE_TROPHY_RE = re.compile(
    r"\b(?:plain\s+)?(?:unmarked|uninscribed|inscription[- ]free)\s+troph(?:y|ies)\b|"
    r"\btroph(?:y|ies)\b\s+(?:is\s+)?(?:plain|unmarked|uninscribed|inscription[- ]free)\b|"
    r"\btroph(?:y|ies)\b\s+(?:without\s+(?:an?\s+)?inscription|with\s+no\s+"
    r"(?:readable|legible)\s+(?:text|lettering|numbers?|inscription))\b",
    re.IGNORECASE,
)
_SAFE_MENU_COPY_RE = re.compile(
    r"\b(?:non[ -]?(?:legible|readable)|unreadable|illegible|indistinct|blurred|out.of.focus)\s+"
    r"(?:menu\s+)?(?:text|writing|lettering|markings?)\b|"
    r"\b(?:menu\s+)?(?:text|writing|lettering|markings?)\b\s+(?:is\s+|are\s+|remains?\s+)?"
    r"(?:non[ -]?(?:legible|readable)|unreadable|illegible|indistinct|blurred|out.of.focus)\b|"
    r"\b(?:menu\s+)?(?:text|writing|lettering|markings?)\b[^.]{0,20}\btoo\s+small\s+to\s+read\b",
    re.IGNORECASE,
)
_SAFE_SUGAR_SACHETS_RE = re.compile(
    r"\b(?:plain|unmarked|unlabelled|unlabeled|label[- ]free)\s+(?:paper\s+)?sugar\s+sachets?\b|"
    r"\bsugar\s+sachets?\b\s+(?:with|showing)\s+(?:no\s+)?"
    r"(?:readable|legible|indistinct|unreadable|illegible)?\s*(?:labels?|markings?|text)\b",
    re.IGNORECASE,
)


def _safe_swatch_type(text, kind):
    return re.search(
        rf"\b(?:unlabelled|unlabeled|unmarked|label[- ]free)\s+{kind}\s+swatches\b|"
        rf"\b{kind}\s+swatches\b\s+(?:with|showing)\s+(?:no\s+)?"
        rf"(?:readable|legible|indistinct|unreadable|illegible)?\s*(?:labels?|markings?)\b",
        text,
        re.IGNORECASE,
    )


def check_content_policy(text, groups):
    """Return bounded errors for explicit and catalog-declared content risks."""
    errors = []
    background = re.search(r"\b(?:background|behind|beyond|distant)\b", text, re.I)
    if groups.intersection({"menu", "chalkboard"}) and not (_SAFE_MENU_COPY_RE.search(text) and background):
        errors.append((
            "menu_text_treatment",
            "The scene text must explicitly call the menu/chalkboard a non-legible background detail, using both a non-legible term and a background term; otherwise remove it.",
        ))
    if groups.intersection(
        {"pinboard", "whiteboard", "wall_display_board", "wall_writing_board"}
    ) and re.search(
        r"\b(?:(?:fully|completely|mostly|nearly|partly)\s+)?(?:empty|blank)\s+"
        r"(?:(?:reference|cork|classroom)\s+)?(?:pinboard|bulletin\s+board|whiteboard)\b|"
        r"\b(?:(?:reference|cork|classroom)\s+)?(?:pinboard|bulletin\s+board|whiteboard)\b"
        r"[^.]{0,24}\b(?:empty|blank)\b",
        text,
        re.IGNORECASE,
    ):
        errors.append((
            "blank_board_treatment",
            "A wall-mounted board must not be empty or blank. Describe sparse distant "
            "non-legible geometric marks or choose another approved wall treatment.",
        ))
    if "ring_binder" in groups and _OPEN_BINDER_RE.search(text) and not _SAFE_OPEN_BINDER_PAGES_RE.search(text):
        errors.append((
            "open_binder_page_treatment",
            "An open or partly open binder must explicitly show blank, unmarked, indistinct, or non-readable pages; an unlabelled binder alone does not control visible page text.",
        ))
    if "document_box" in groups and _DOCUMENT_BOX_RE.search(text) and not _SAFE_DOCUMENT_BOX_RE.search(text):
        errors.append((
            "document_box_label_treatment",
            "A document storage box must explicitly be plain, unmarked, unlabelled, or label-free so it does not invite generated filing text.",
        ))
    if groups.intersection(_MEASUREMENT_TOOL_GROUPS) and not _SAFE_MEASUREMENT_TOOL_RE.search(text):
        errors.append((
            "measurement_tool_text_treatment",
            "Every selected ruler, measuring tape, set square, or protractor must explicitly be unmarked or have non-readable/indistinct measurement markings.",
        ))
    if "trophy" in groups and not _SAFE_TROPHY_RE.search(text):
        errors.append((
            "trophy_text_treatment",
            "A trophy must explicitly be plain, unmarked, uninscribed, inscription-free, or have no readable inscription; unbranded alone is insufficient.",
        ))
    if "sugar_sachets" in groups and not _SAFE_SUGAR_SACHETS_RE.search(text):
        errors.append((
            "sugar_sachet_text_treatment",
            "Sugar sachets must explicitly be plain, unmarked, unlabelled, or label-free, or have no readable label/text.",
        ))
    for swatch_group, swatch_kind in (("fabric_swatches", "fabric"), ("color_swatches", "color")):
        if swatch_group in groups and not _safe_swatch_type(text, swatch_kind):
            errors.append((
                "swatch_text_treatment",
                f"Selected {swatch_kind} swatches must explicitly be unlabelled, unmarked, label-free, or have non-readable labels; a safeguard on another swatch type does not apply.",
            ))
    risky_text_groups = sorted(groups.intersection(_TEXT_CARRIER_GROUPS))
    if risky_text_groups and not _SAFE_TEXT_CARRIER_RE.search(text):
        errors.append((
            "text_bearing_prop_treatment",
            "Text-bearing prop groups " + repr(risky_text_groups)
            + " need a visible safe treatment in the scene itself, such as blank pages, "
            "an unmarked cover, a face-down card, or indistinct/non-readable markings. "
            "Wall-mounted boards must use sparse non-legible nonhuman content rather than remain empty.",
        ))
    risky_face_groups = sorted(groups.intersection(_FACE_BEARING_GROUPS))
    if risky_face_groups and not _SAFE_FACE_CARRIER_RE.search(text):
        errors.append((
            "face_bearing_prop_treatment",
            "Face-bearing prop groups " + repr(risky_face_groups)
            + " must be closed with a plain cover or explicitly limited to abstract, "
            "geometric, botanical, architectural, landscape, still-life, material, "
            "or other nonhuman content.",
        ))
    if groups.intersection(_ART_GROUPS) and not _SAFE_ART_RE.search(text):
        errors.append((
            "artwork_face_treatment",
            "Artwork must explicitly be abstract, geometric, botanical, a landscape, "
            "a still life, or otherwise free of people and portraits.",
        ))
    excluded_item = r"(?:visible\s+|human\s+|any\s+)*(?:faces?|portraits?|headshots?|legible\s+text|readable\s+text)"
    positive = re.sub(r"\b(?:no|without|avoid|omitting|excluding)\s+" + excluded_item + r"(?:\s+(?:or|and)\s+" + excluded_item + r")*\b", "", text, flags=re.I)
    positive = _NEGATED_LEGIBLE_TEXT_RE.sub("", positive)
    positive = re.sub(r"\bnon[ -]legible\b", "indistinct", positive, flags=re.I)
    if re.search(r"\b(?:portrait(?:s|ure)?|headshots?|smiling\s+(?:person|woman|man|student)|(?:human|visible)\s+faces?)\b", positive, re.I):
        errors.append(("human_face_request", "Use abstract/landscape art and head-out-of-frame activity rather than faces or portraits."))
    if re.search(r"\b(?:clearly\s+)?(?:readable|legible)\s+(?:text|words|lettering|handwriting|labels?|titles?|menus?|numbers?)\b", positive, re.I):
        errors.append(("legible_text_request", "Avoid requests for readable text; use plain or non-legible visual alternatives."))
    if re.search(r"\breturn[ -]?labels?(?:\s+sheets?)?\b", positive, re.I):
        errors.append((
            "text_carrier_risk",
            "Do not request return-label sheets; they invite generated addresses, barcodes, logos, or other legible text.",
        ))
    return errors
