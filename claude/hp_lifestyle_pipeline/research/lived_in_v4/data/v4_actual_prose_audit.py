#!/usr/bin/env python3
"""Audit actual V4 candidate prose independently of model visual signatures.

The tool is read-only with respect to V4 artifacts. It discovers the newest
normalized output for each completed case, counts objects directly in scene prose,
checks tight/wide geometry and forbidden language, and reports repeated artifacts
and lived-in/distress signals. Model-reported visual signatures are retained only
as a cross-check; they are not the source of the prose counts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from audit_lived_in_specificity import cohort_metrics, matched_cues, sha256, words


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_EVAL = ROOT / "eval_sets/hp_lifestyle_lived_in_v4_eval_20261026"
DEFAULT_JSON = Path(__file__).with_name("v4_actual_prose_audit.json")
DEFAULT_MD = Path(__file__).with_name("V4_ACTUAL_PROSE_AUDIT.md")


DEVICE_RE = re.compile(
    r"\b(?:laptops?|printers?|mini\s*pcs?|minipcs?|desktops?|computers?|monitors?|"
    r"hardware|devices?|skus?|phones?|smartphones?|tablets?|screens?|keyboards?|"
    r"hp|elitebooks?|omnibooks?|laserjets?)\b",
    re.I,
)
SURFACE_DESKTOP_RE = re.compile(
    r"\b(?:wooden|wood|walnut|oak|birch|maple|laminate|veneer|painted|satin|matte|smooth|white|graphite)\s+desktop\b",
    re.I,
)
NONCOMPUTING_SCREEN_RE = re.compile(r"\b(?:privacy|acoustic|folding|divider)\s+screen\b", re.I)
CAMERA_RE = re.compile(
    r"\b(?:camera|lens|render(?:ing)?|zoom|aspect ratio|depth of field|bokeh|pull back|"
    r"widen the view|wide(?:r)? (?:view|shot|crop)|close[- ]?up|medium shot|camera angle|"
    r"selected angle|reveal the whole|move the product|center the product|crop(?:ped)? view)\b",
    re.I,
)


# Longest non-overlapping matches are counted as visible prose objects. Compound
# paper clusters such as "a packet of forms" count as one object. A notebook and
# pen produce two matches. Surface, light, plain wall tone, and material are absent.
LOCAL_OBJECT_PATTERNS: dict[str, str] = {
    "document_compound": (
        r"\b(?:(?:a|an|one|the|small|compact|neat|tidy|slim|folded|creased|dog-eared|annotated|"
        r"marked|marked-up|clipped|tabbed|open|loose|handwritten|color-coded|corrected|recurring|repeated|"
        r"multi-page|rough|printed|household|family|business|admin|color|class|follow-up|sign-in)\s+)*"
        r"(?:forms?|paperwork|documents?|records?|handouts?|reports?|worksheets?|notebooks?|color materials?|"
        r"proof|record|recipe|sketch|newspaper)\s+"
        r"(?:packets?|folders?|binders?|envelopes?|sheets?|pages?|sets?|stacks?|sections?)"
        r"(?:\s+packets?)?\b"
    ),
    "document_container_compound": (
        r"\b(?:(?:a|an|one|the|small|compact|neat|tidy|slim|folded|creased|dog-eared|annotated|"
        r"marked|clipped|tabbed|open|loose|handwritten|manila|color)\s+)*"
        r"(?:folders?|binders?|envelopes?)\s+of\s+(?:(?:follow-up|client|household|business|class)\s+)*(?:forms?|papers?|records?|notes?|receipts?)\b"
    ),
    "standalone_document_bundle": r"\b(?:(?:a|an|one|the|small|compact|neat|thick|slim|folded|multi-page|admin|business|paperwork|follow-up)\s+)+(?:packets?|sets?|bundles?)\b",
    "paper_artifact": (
        r"\b(?:(?:a|an|one|the|small|compact|neat|tidy|slim|shallow|folded|creased|dog-eared|"
        r"annotated|marked|marked-up|clipped|stapled|tabbed|open|loose|handwritten|date-stamped|"
        r"color-coded|crossed-out|corrected|partly used|half-used|sealed|stacked|sorted|repeated|"
        r"multi-page|rough|printed|project|household|school|daily|recurring|routine|color|top|cover)\s+)*"
        r"(?:(?:stack|packet|pile|bundle|set|sheaf|tray|sleeve)\s+of\s+)?"
        r"(?:forms?|papers?|paperwork|pages?|sheets?|worksheets?|handouts?|proofs?|notices?|"
        r"reports?|records?|documents?|sketches?|reminders?|receipts?|bills?|rubrics?|outlines?|"
        r"document briefs?|summaries?|agendas?|schedules?|timetables?|planners?|calendars?|lists?|checklists?|"
        r"envelopes?|reams?|slips?|cards?|packets?|clippings?)\b"
    ),
    "notebook_or_book": r"\b(?:(?:an?|one|the|small|compact|creased|dog-eared|open|closed|travel|paperback|softcover|worked-on|spiral|clue|rules?)\s+)*(?:notebooks?|notepads?|sketchbooks?|workbooks?|textbooks?|booklets?|books?|magazines?)\b",
    "folder_or_binder": r"\b(?:(?:an?|one|the|small|compact|neat|slim|marked|clipped|tabbed|sealed|project|records?|household|confidential|color|manila)\s+)*(?:folders?|binders?|folios?|record sleeves?)\b",
    "writing_tool": r"\b(?:(?:an?|one|the|small|capped|uncapped|red|colored|diagonal|resting)\s+)*(?:pens?|pencils?|markers?|rulers?)\b",
    "drink_vessel": r"\b(?:(?:an?|one|the|small|ceramic|matte|half-finished|half-full|partly-filled|partially-filled|cooling|terracotta|coffee|tea|water)\s+)*(?:cups?|mugs?|glass(?:es)?)\b",
    "food_or_plate": r"\b(?:(?:an?|one|the|small|wrapped|half-eaten|snack)\s+)*(?:plates?|pastries|snacks?|cand(?:y|ies)|bowls?)\b",
    "coaster": r"\b(?:(?:an?|one|the|small)\s+)*coasters?\b",
    "controller_or_game_piece": r"\b(?:(?:an?|one|the|small|simple|game)\s+)*(?:controllers?|dice|game pieces?|score pads?)\b",
    "creative_material": r"\b(?:(?:an?|one|the|small|loose|arranged|fabric|color|paint)\s+)*(?:swatches?|design materials?|fabric samples?|paintbrushes?|brushes?|pencil cases?)\b",
    "personal_item": r"\b(?:(?:an?|one|the|small|visitor|travel)\s+)*(?:badges?|glasses|key rings?|keys?|wallets?|headphones?|wrist straps?)\b",
    "container_or_organizer": r"\b(?:(?:an?|one|the|small|compact|shallow|inbox|records?|pen|supply)\s+)*(?:trays?|organizers?|cups?|boxes?|bins?|baskets?)\b",
    "small_tool": r"\b(?:(?:an?|one|the|small|capped|kneaded|masking|metal|rinsed|paint)\s+)*(?:erasers?|highlighters?|tape rolls?|rolls? of tape|brush(?:es)?|needles?|palettes?)\b",
    "craft_or_hobby_item": r"\b(?:(?:an?|one|the|small|folded|loose|bisque|test|glaze|labeled|cloth|dice|watercolor|puzzle|clue)\s+)*(?:fabric squares?|tins? of (?:loose )?buttons?|needle cards?|buttons?|tiles?|jars?|pouches?|booklets?|puzzle pieces?|clusters? of pieces|yarn ends?|rags?)\b",
    "food_item": r"\b(?:(?:an?|one|the|small|paper-wrapped|half)\s+)*(?:sandwich(?:es)?|flakes?)\b",
    "utensil_or_rest": r"\b(?:(?:an?|one|the|small|butter|tea|stained|ceramic)\s+)*(?:kn(?:ife|ives)|teaspoons?|spoons?|forks?|brush rests?)\b",
    "napkin_towel_or_rag": r"\b(?:(?:an?|one|the|small|folded|linen|paper|stained|rumpled|snack)\s+)*(?:napkins?|towels?|rags?)\b",
}

BACKGROUND_PATTERNS: dict[str, str] = {
    "shelf_or_bookcase": r"\b(?:(?:an?|one|the|small|low|narrow|simple|plain|supply|file|open|full|blurred)\s+)*(?:shelves|shelving|shelf|bookshelves?|bookcases?)\b",
    "pinboard_or_wall_board": r"\b(?:(?:an?|one|the|small|simple|modest|muted|clipped|fabric|cork|bulletin|inspiration|chalk|white)\s+)*(?:pinboards?|noticeboards?|bulletin boards?|corkboards?|cork boards?|cork strips?|pegboards?|whiteboards?|menu boards?|chalk menus?)\b",
    "chair_or_seating": r"\b(?:(?:an?|one|the|small|simple|soft|softly worn|upholstered|fabric|tucked|askew|ergonomic|blurred)\s+)*(?:chairs?|stools?|seats?|banquettes?|benches?)\b",
    "plant": r"\b(?:(?:an?|one|the|small|slightly overgrown|potted|house)\s+)*(?:plants?|houseplants?|succulents?)\b",
    "window_or_curtain": r"\b(?:(?:an?|one|the|small|large|tall|nearby|plain|soft|relaxed|gathered)\s+)*(?:windows?|curtains?|roller shades?)\b",
    "cabinet_or_storage": r"\b(?:(?:an?|one|the|small|low|narrow|simple|plain|side|storage|file|book|drying|blurred)\s+)*(?:cabinets?|cubbies|lockers?|carts?|racks?)\b",
    "divider_or_partition": r"\b(?:(?:an?|one|the|small|partial|plain|neutral|frosted|glass|acoustic|blurred)\s+)*(?:dividers?|partitions?|glass walls?|acoustic panels?|wall panels?)\b",
    "art_or_photo": r"\b(?:(?:an?|one|the|small|framed|personal)\s+)*(?:artwork|art prints?|photos?|photographs?|posters?)\b",
    "lamp_or_fixture": r"\b(?:(?:an?|one|the|small|simple|desk|floor|pendant|sculptural|soft)\s+)*(?:lamps?|lampshades?|light fixtures?)\b",
    "wall_calendar_or_clock": r"\b(?:(?:an?|one|the|small|plain|soft)\s+)*(?:wall calendars?|clocks?)\b",
    "architectural_anchor": r"\b(?:(?:an?|one|the|small|simple|plain|blurred|partial|chair|wall)\s+)*(?:staircases?|corridors?|doorways?|peg rails?|chair rails?|wall hooks?|backsplashes?)\b",
}

PEOPLE_RE = re.compile(
    r"\b(?:cropped (?:\w+ )?hands?|hands? (?:rests?|straightens?|aligns?|writes?|holds?|reaches?|gestures?|types?)|"
    r"(?:a|one|two|three) (?:young )?(?:woman|man|person|professional|student|teacher|gamer|designer|worker|coworker|colleague|adult|child|patron)s?\b.{0,80}\b(?:sits?|stands?|walks?|types?|writes?|holds?|gestures?|wears?|works?|reads?|reviews?|plays?))",
    re.I,
)

USE_STATE_PATTERNS: dict[str, str] = {
    "open_or_unfinished": r"\b(?:open(?:ed)?|half-finished|unfinished|partly used|half-used|cooling|lowered .*? line)\b",
    "marked_or_worked": r"\b(?:annotated|marked-up|handwritten|crossed-out|corrected|date-stamped|color-coded|pencil revisions?|writing impressions?)\b",
    "casual_arrangement": r"\b(?:askew|out of square|diagonally|loosely arranged|casually arranged|slightly forward|left beside|left open|resting across|overlapping|unevenly aligned|irregularly aligned)\b",
    "use_residue": r"\b(?:crumbs?|wiped (?:drink )?rings?|faint rings?|paper-edge dust|wrapper|wrappers|creased|dog-eared|turned paper corner)\b",
    "gentle_surface_use": r"\b(?:softly burnished|uneven polish|uneven sheen|softly rubbed|gently rubbed|gently scuffed|lightly scuffed|faint scuffs?|small finish rubs?|shallow cut traces?|softened edge|rubbed finish|gentle patina)\b",
    "pause_or_handoff": r"\b(?:waiting for sign-off|ready for review|prepared for|in progress|handoff|pause|next pass|mid-conversation)\b",
    "surface_history": r"\b(?:pressure marks?|pressure lines?|rubbed|burnished|dulled|smoothed|smooth patch|wipe marks?|wipe streaks?|wipe arcs?|wiped matte spot|polished (?:area|patch|zone)|polish variations?|sleeve polish|palm wear|working zone|glossier|cloudy patch|crescent mark|faint grid|rubbed grain|powdery-looking matte patch|scoring|nicks?|cut ghosts?|dents?|worn spot|softened (?:edge|corner|front lip|shine|varnish)|rounded edge|thumbed edge|edge rubs?|hairline scuffs?|fine scratches?|shallow scratches?|knife marks?|brush marks?|paint-speckled|recently tended)\b",
    "active_material_state": r"\b(?:marked by underlines|underlined|margin notes?|margin arrow|registration mark|pencil bracket|penciled (?:correction|tick|initials?)|circled|sketched|revised|flattened from use|folded|loose buttons?|drying|rinsed|old tape marks?|partly sorted|condensation trail|smudged (?:fingerprints?|corner)|sanding dust|flour-dusted|erased pencil ghosts?|dried glaze|not quite square|slight(?:ly)? (?:skew|diagonal))\b",
}

DISTRESS_PATTERNS: dict[str, str] = {
    "dirt_or_grime": r"\b(?:dirty|filthy|grimy|grime|dusty|caked|soiled)\b",
    "damage": r"\b(?:damaged|broken|cracked|chipped|gouged|warped|peeling|battered|shattered)\b",
    "neglect": r"\b(?:neglected|shabby|decrepit|derelict|heavily worn|deep scratches?|heavy wear)\b",
    "stain_or_rust": r"\b(?:stained|rusty|rusted|watermarked)\b",
    "tear_or_fray": r"\b(?:torn|ripped|frayed)\b",
    "generic_wear": r"\b(?:worn|scuffed|scratched|scarred)\b",
}

SOFTENER_RE = re.compile(r"\b(?:faint|lightly|gently|softly|subtle|small|fine|shallow|slight|slightly|minor)\b", re.I)
ROOM_LAYOUT_RE = re.compile(r"\b(?:room layout|whole room|throughout the room|deep into the space|expansive floor plan|furniture collection|multiple workstations)\b", re.I)
HARD_SURFACE_RE = re.compile(r"\b(?:quartz|stone|concrete|glass|metal|ceramic|marble|granite)\b", re.I)
SOFT_MATERIAL_WEAR_RE = re.compile(r"\b(?:writing impressions?|pressure (?:marks?|dents?|lines?)|writing dents?|grooves? from .*?writing)\b", re.I)
GENERIC_ADJECTIVE_RE = re.compile(r"\b(?:lived-in|tidy|simple|quiet|minimal|clean|restrained|authentic|professional|inviting|believable)\b", re.I)
ARRANGEMENT_RE = re.compile(r"\b(?:askew|diagonally|overlapping|unevenly|irregularly|left open|left beside|left uncapped|resting|placed|arranged|stacked|clipped|folded|tucked|pulled forward|out of square|laid|lying|angled|balanced|nudged sideways|set down|fanned|slightly turned|pulled back)\b", re.I)

CONTEXT_PATTERNS = {
    "Home": re.compile(r"\b(?:home|residential|apartment|household|family|dining table|living room|bedroom)\b", re.I),
    "Office": re.compile(r"\b(?:office|corporate|department|administrative|business|reception|meeting room|records counter|coworking)\b", re.I),
    "Education": re.compile(r"\b(?:classroom|school|student|teacher|library|campus|education|lesson)\b", re.I),
    "Gaming": re.compile(r"\b(?:gaming|game night|gamer|controller)\b", re.I),
    "Café": re.compile(r"\b(?:café|cafe|coffee shop|banquette|pastry)\b", re.I),
    "Creative Studio": re.compile(r"\b(?:creative studio|design studio|maker studio|editorial studio|art studio|craft table)\b", re.I),
}


def file_record(path: Path) -> dict[str, Any]:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}


def prohibited_device_matches(text: str) -> list[dict[str, Any]]:
    allowed_spans = [m.span() for m in SURFACE_DESKTOP_RE.finditer(text)]
    allowed_spans += [m.span() for m in NONCOMPUTING_SCREEN_RE.finditer(text)]
    out = []
    for match in DEVICE_RE.finditer(text):
        if any(start <= match.start() and match.end() <= end for start, end in allowed_spans):
            continue
        context = text[max(0, match.start() - 35):min(len(text), match.end() + 35)]
        contextual_nonhardware = bool(
            (match.group(0).casefold() == "phone" and re.search(r"phone[- ]room", context, re.I))
            or (match.group(0).casefold() == "desktop" and not re.search(r"\b(?:computer|monitor|screen|keyboard|hardware)\b", context, re.I))
        )
        out.append({
            "term": match.group(0),
            "span": list(match.span()),
            "context": context,
            "contextual_nonhardware_usage": contextual_nonhardware,
        })
    return out


def nonoverlapping_matches(text: str, patterns: dict[str, str]) -> list[dict[str, Any]]:
    candidates: list[tuple[int, int, str, str]] = []
    for category, pattern in patterns.items():
        for match in re.finditer(pattern, text, re.I):
            candidates.append((match.start(), match.end(), category, match.group(0)))
    # Prefer longer matches at the same/overlapping span, then preserve reading order.
    candidates.sort(key=lambda x: (-(x[1] - x[0]), x[0], x[2]))
    kept: list[tuple[int, int, str, str]] = []
    for candidate in candidates:
        if any(not (candidate[1] <= x[0] or candidate[0] >= x[1]) for x in kept):
            continue
        kept.append(candidate)
    return [
        {"category": category, "text": value, "span": [start, end]}
        for start, end, category, value in sorted(kept)
    ]


def sentence_span(text: str, offset: int) -> str:
    start = max(text.rfind(".", 0, offset), text.rfind("!", 0, offset), text.rfind("?", 0, offset)) + 1
    ends = [p for p in (text.find(".", offset), text.find("!", offset), text.find("?", offset)) if p >= 0]
    end = min(ends) + 1 if ends else len(text)
    return text[start:end].strip()


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]


def local_inventory_clause(first_sentence: str) -> str:
    anchors = list(re.finditer(r"\b(?:with|holding|featuring)\b", first_sentence, re.I))
    if not anchors:
        return ""
    return first_sentence[anchors[0].end():]


def prose_inventory(text: str) -> dict[str, Any]:
    sentences = split_sentences(text)
    first_sentence = sentences[0] if sentences else text
    clause = local_inventory_clause(first_sentence)
    locals_all = nonoverlapping_matches(clause, LOCAL_OBJECT_PATTERNS) if clause else []
    # Objects named only as the historical cause of a surface trace are not
    # requested visible props (e.g. "dulled from repeated elbows and folders").
    causal_spans = [m.span() for m in re.finditer(
        r"\b(?:from repeated|where .*? usually|where .*? have|without (?:showing|bringing)|no materials?|no tools?)\b.*$",
        clause,
        re.I,
    )]
    content_spans = [m.span() for m in re.finditer(
        r"\b(?:opened to|left open to|filled with|showing)\b.*?(?=,\s+(?:and\s+)?(?:a|an|one)\b|\s+and\s+(?:a|an|one)\b|$)",
        clause,
        re.I,
    )]
    preliminary = [
        item for item in locals_all
        if not any(start <= item["span"][0] < end for start, end in causal_spans + content_spans)
    ]
    preliminary = [
        item for item in preliminary
        if not re.match(r"\s+queue\b", clause[item["span"][1]:], re.I)
    ]
    locals_kept = []
    seen_categories = Counter()
    seen_heads: set[str] = set()
    for item in preliminary:
        # Later definite mentions usually refer back to an already counted prop
        # ("the page", "the cup") instead of introducing another object.
        head_tokens = re.findall(r"[a-z]+", item["text"].casefold())
        head = head_tokens[-1] if head_tokens else ""
        if re.match(r"\s*the\b", item["text"], re.I) and (seen_categories[item["category"]] or head in seen_heads):
            continue
        if locals_kept:
            between = clause[locals_kept[-1]["span"][1]:item["span"][0]]
            if re.search(r"\bwith\s+(?:a|an|the)\b", between, re.I) and not re.search(r"[,;]", between):
                # A component/state of the previous object (pencil with eraser,
                # cup with lowered line) remains part of that prop.
                continue
        locals_kept.append(item)
        seen_categories[item["category"]] += 1
        if head:
            seen_heads.add(head)
    locals_background_contents: list[dict[str, Any]] = []

    backgrounds = []
    running_offset = 0
    for index, sentence in enumerate(sentences):
        sentence_start = text.find(sentence, running_offset)
        running_offset = sentence_start + len(sentence)
        has_background_relation = bool(re.search(
            r"\b(?:behind|background|depth|beyond|against the wall|sits?|stands?|hangs?|softens|forms the background|adds)\b",
            sentence,
            re.I,
        ))
        if not has_background_relation:
            continue
        found = nonoverlapping_matches(sentence, BACKGROUND_PATTERNS)
        # A repeated mention of a chair's seat or a shelf's edge remains one
        # fixture. Distinct fixture categories remain distinct details.
        seen_categories = set()
        for item in found:
            if item["category"] in seen_categories:
                continue
            seen_categories.add(item["category"])
            item = dict(item)
            item["span"] = [item["span"][0] + sentence_start, item["span"][1] + sentence_start]
            backgrounds.append(item)
    people = [{"text": m.group(0), "span": list(m.span())} for m in PEOPLE_RE.finditer(text)]
    return {
        "local_props": locals_kept,
        "background_details": backgrounds,
        "people": people,
        "excluded_background_contents": locals_background_contents,
        "counts": {
            "local_props": len(locals_kept),
            "background_details": len(backgrounds),
            "people": len(people),
        },
    }


def find_named_patterns(text: str, patterns: dict[str, str]) -> list[dict[str, Any]]:
    out = []
    for name, pattern in patterns.items():
        matches = [m.group(0) for m in re.finditer(pattern, text, re.I)]
        if matches:
            out.append({"type": name, "matches": matches})
    return out


def candidate_audit(case: dict[str, Any], prompt: dict[str, Any]) -> dict[str, Any]:
    text = prompt["text"]
    profile = case["expected_camera"]
    inventory = prose_inventory(text)
    device_terms = prohibited_device_matches(text)
    camera_terms = [m.group(0) for m in CAMERA_RE.finditer(text)]
    use_states = find_named_patterns(text, USE_STATE_PATTERNS)
    distress = find_named_patterns(text, DISTRESS_PATTERNS)
    generic_adjectives = [m.group(0) for m in GENERIC_ADJECTIVE_RE.finditer(text)]
    arrangement = [m.group(0) for m in ARRANGEMENT_RE.finditer(text)]
    severe_distress = [x for x in distress if x["type"] in {"dirt_or_grime", "damage", "neglect"}]
    unsoftened_generic_wear = []
    for match in re.finditer(DISTRESS_PATTERNS["generic_wear"], text, re.I):
        prefix = text[max(0, match.start() - 22):match.start()]
        if not SOFTENER_RE.search(prefix):
            unsoftened_generic_wear.append(match.group(0))
    contexts = [name for name, pattern in CONTEXT_PATTERNS.items() if pattern.search(text)]
    signature = prompt["visual_signature"]

    flags = []
    if device_terms:
        flags.append("host_forbidden_device_lexeme")
    if any(not x["contextual_nonhardware_usage"] for x in device_terms):
        flags.append("actual_hardware_reference")
    if camera_terms:
        flags.append("forbidden_camera_or_view_term")
    if inventory["counts"]["local_props"] > profile["max_local_props"]:
        flags.append("prose_local_prop_budget_exceeded")
    if inventory["counts"]["background_details"] > profile["max_background_details"]:
        flags.append("prose_background_budget_exceeded")
    if profile["people_policy"] == "omit" and inventory["counts"]["people"]:
        flags.append("prose_people_policy_exceeded")
    if profile["framing"] == "tight" and ROOM_LAYOUT_RE.search(text):
        flags.append("tight_room_layout_language")
    distress_match_total = sum(len(x["matches"]) for x in distress)
    compound_stain_damage = any(x["type"] == "stain_or_rust" for x in distress) and distress_match_total >= 2
    if severe_distress or compound_stain_damage or len(unsoftened_generic_wear) > 2:
        flags.append("excessive_or_unsoftened_distress")
    if len(contexts) > 1 and prompt["environment"] not in contexts:
        flags.append("mixed_context_without_declared_environment")
    if profile["framing"] == "tight" and not use_states:
        flags.append("tight_missing_specific_use_trace")
    if profile["framing"] == "wide" and not use_states:
        flags.append("wide_missing_specific_use_state")
    if profile["framing"] == "wide" and not arrangement:
        flags.append("wide_missing_arrangement_relation")
    if profile["framing"] == "wide" and inventory["counts"]["local_props"] == 0:
        flags.append("wide_no_detected_local_prop")
    if HARD_SURFACE_RE.search(text) and SOFT_MATERIAL_WEAR_RE.search(text):
        flags.append("implausible_material_wear_pairing")
    if len(signature["local_props"]) != inventory["counts"]["local_props"]:
        flags.append("signature_vs_prose_prop_count_disagreement")
    if len(signature["background_details"]) != inventory["counts"]["background_details"]:
        flags.append("signature_vs_prose_background_count_disagreement")
    if bool(signature["people"]) != bool(inventory["counts"]["people"]):
        flags.append("signature_vs_prose_people_disagreement")

    return {
        "candidate_key": f"{case['case_id']}::{prompt['id']}",
        "case_id": case["case_id"],
        "source_id": case["source_id"],
        "candidate_id": prompt["id"],
        "camera_tag": case["camera_tag"],
        "view_role": case["view_role"],
        "environment": prompt["environment"],
        "relationship": prompt["relationship"],
        "score": prompt["source_relevance_score"],
        "text": text,
        "word_count": len(words(text)),
        "prose_inventory": inventory,
        "profile_ceiling": {
            "framing": profile["framing"],
            "max_local_props": profile["max_local_props"],
            "max_background_details": profile["max_background_details"],
            "people_policy": profile["people_policy"],
        },
        "signature_counts_for_cross_check_only": {
            "local_props": len(signature["local_props"]),
            "background_details": len(signature["background_details"]),
            "people": len(signature["people"]),
        },
        "specific_use_states": use_states,
        "distress_signals": distress,
        "unsoftened_generic_wear": unsoftened_generic_wear,
        "generic_character_adjectives": generic_adjectives,
        "arrangement_relations": arrangement,
        "explicit_contexts": contexts,
        "forbidden_device_lexemes": device_terms,
        "forbidden_camera_or_view_terms": camera_terms,
        "flags": sorted(set(flags)),
    }


def latest_normalized_outputs(eval_dir: Path) -> dict[str, Path]:
    found: dict[str, list[Path]] = defaultdict(list)
    for path in sorted((eval_dir / "normalized_outputs").glob("*.json")):
        match = re.fullmatch(r"(.+)__(sample_\d{3})\.json", path.name)
        if match:
            found[match.group(1)].append(path)
    return {case_id: paths[-1] for case_id, paths in found.items()}


def aggregate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    flag_counts = Counter(flag for c in candidates for flag in c["flags"])
    artifact_presence = Counter()
    artifact_pair_presence = Counter()
    use_state_presence = Counter()
    distress_presence = Counter()
    broad_family_presence = Counter()
    for c in candidates:
        categories = sorted({x["category"] for x in c["prose_inventory"]["local_props"]})
        artifact_presence.update(categories)
        artifact_pair_presence.update(
            f"{categories[i]} + {categories[j]}"
            for i in range(len(categories)) for j in range(i + 1, len(categories))
        )
        use_state_presence.update({x["type"] for x in c["specific_use_states"]})
        distress_presence.update({x["type"] for x in c["distress_signals"]})
        category_set = set(categories)
        families = set()
        if category_set & {"document_compound", "document_container_compound", "standalone_document_bundle", "paper_artifact", "folder_or_binder", "notebook_or_book"}:
            families.add("paper_or_document")
        if category_set & {"writing_tool", "small_tool", "utensil_or_rest"}:
            families.add("hand_tool_or_utensil")
        if category_set & {"drink_vessel", "food_or_plate", "food_item", "coaster", "napkin_towel_or_rag"}:
            families.add("food_drink_or_pause")
        if category_set & {"creative_material", "craft_or_hobby_item"}:
            families.add("creative_or_hobby")
        if category_set & {"controller_or_game_piece"}:
            families.add("game")
        broad_family_presence.update(families)
    texts = [c["text"] for c in candidates]
    word_counts = [c["word_count"] for c in candidates]
    surface_history_count = sum(
        bool({x["type"] for x in c["specific_use_states"]} & {"surface_history", "gentle_surface_use"})
        for c in candidates
    )
    return {
        "candidate_count": len(candidates),
        "word_count": {
            "median": statistics.median(word_counts),
            "min": min(word_counts),
            "max": max(word_counts),
        },
        "flag_counts": dict(sorted(flag_counts.items())),
        "candidates_without_flags": sum(not c["flags"] for c in candidates),
        "prose_budget_exceedances": sum(
            any(f in c["flags"] for f in ["prose_local_prop_budget_exceeded", "prose_background_budget_exceeded", "prose_people_policy_exceeded"])
            for c in candidates
        ),
        "forbidden_term_candidates": sum(
            any(f in c["flags"] for f in ["host_forbidden_device_lexeme", "forbidden_camera_or_view_term"])
            for c in candidates
        ),
        "actual_hardware_reference_candidates": sum("actual_hardware_reference" in c["flags"] for c in candidates),
        "specific_use_state_candidates": sum(bool(c["specific_use_states"]) for c in candidates),
        "specific_use_state_fraction": round(sum(bool(c["specific_use_states"]) for c in candidates) / len(candidates), 6),
        "surface_history_candidates": surface_history_count,
        "surface_history_fraction": round(surface_history_count / len(candidates), 6),
        "surface_history_saturation_review": surface_history_count / len(candidates) >= 0.8,
        "excessive_distress_candidates": sum("excessive_or_unsoftened_distress" in c["flags"] for c in candidates),
        "artifact_category_presence": dict(artifact_presence.most_common()),
        "artifact_pair_presence": dict(artifact_pair_presence.most_common()),
        "broad_artifact_family_presence": dict(broad_family_presence.most_common()),
        "paper_or_document_omission_count": len(candidates) - broad_family_presence["paper_or_document"],
        "use_state_presence": dict(use_state_presence.most_common()),
        "distress_presence": dict(distress_presence.most_common()),
        "reference_compatible_lexical_metrics": cohort_metrics(texts),
    }


def concentration_findings(by_case: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    findings = []
    for case_id, candidates in sorted(by_case.items()):
        counts = Counter()
        pairs = Counter()
        for c in candidates:
            cats = sorted({x["category"] for x in c["prose_inventory"]["local_props"]})
            counts.update(cats)
            pairs.update(f"{cats[i]} + {cats[j]}" for i in range(len(cats)) for j in range(i + 1, len(cats)))
        repeated = {k: v for k, v in counts.items() if v >= 12}
        repeated_pairs = {k: v for k, v in pairs.items() if v >= 8}
        paper_presence = sum(
            bool({x["category"] for x in c["prose_inventory"]["local_props"]}
                 & {"document_compound", "document_container_compound", "standalone_document_bundle", "paper_artifact", "folder_or_binder", "notebook_or_book"})
            for c in candidates
        )
        paper_omissions = len(candidates) - paper_presence
        if repeated or repeated_pairs or paper_omissions < 10:
            findings.append({
                "case_id": case_id,
                "denominator": len(candidates),
                "artifact_categories_in_at_least_12_of_30": repeated,
                "artifact_pairs_in_at_least_8_of_30": repeated_pairs,
                "paper_or_document_presence": paper_presence,
                "paper_or_document_omission_count": paper_omissions,
                "dominant_artifact_omission_gate_passed": paper_omissions >= 10,
                "interpretation": "Configured screening threshold for stereotyped artifact concentration; requires prose review rather than automatic rejection.",
            })
    return findings


def render_markdown(audit: dict[str, Any]) -> str:
    s = audit["summary"]
    lines = [
        "# V4 actual-prose audit",
        "",
        f"As of {audit['generated_at_utc']}. This report audits {s['candidate_count']} candidates from {audit['completed_case_count']} completed cases. It does not edit V4 outputs.",
        "",
        "## Outcome",
        "",
        f"- Prose budget exceedances: **{s['prose_budget_exceedances']}** candidates.",
        f"- Host-forbidden device/camera lexemes: **{s['forbidden_term_candidates']}** candidates; actual hardware references: **{s['actual_hardware_reference_candidates']}**.",
        f"- Specific lived-in/use-state cues: **{s['specific_use_state_candidates']}/{s['candidate_count']}** candidates.",
        f"- Excessive or unsoftened distress flags: **{s['excessive_distress_candidates']}** candidates.",
        f"- Median words: **{s['word_count']['median']}** (range {s['word_count']['min']}–{s['word_count']['max']}).",
        "",
        "Prose counts come from physical noun phrases in each scene paragraph. Model visual signatures appear only as a cross-check and may produce review flags when the two disagree.",
        "",
        "## Flag counts",
        "",
    ]
    if s["flag_counts"]:
        lines += [f"- `{key}`: {value}" for key, value in s["flag_counts"].items()]
    else:
        lines.append("- None.")
    lines += ["", "## Repeated artifact screening", ""]
    if audit["repeated_artifact_findings"]:
        for item in audit["repeated_artifact_findings"]:
            lines.append(f"- `{item['case_id']}`: categories {item['artifact_categories_in_at_least_12_of_30']}; pairs {item['artifact_pairs_in_at_least_8_of_30']}")
    else:
        lines.append("- No completed 30-row bank crossed the configured category/pair concentration thresholds.")
    lines += ["", "## Candidates requiring prose review", ""]
    flagged = [c for c in audit["candidates"] if c["flags"]]
    if not flagged:
        lines.append("- None under the configured rules.")
    else:
        for c in flagged:
            lines += [
                f"### `{c['candidate_key']}`",
                "",
                f"Flags: {', '.join(f'`{x}`' for x in c['flags'])}",
                "",
                c["text"],
                "",
                f"Prose counts: {c['prose_inventory']['counts']}; signature cross-check: {c['signature_counts_for_cross_check_only']}",
                "",
            ]
    lines += [
        "## Limitations",
        "",
        "- Rule-based noun-phrase counts are intentionally conservative and surface all signature disagreements for human review.",
        "- A lexical cue is evidence in text, not proof that the downstream rewrite or image retains it.",
        "- Context mixing, distress, and coherence flags are screening signals rather than automatic quality verdicts.",
        "- Probe findings do not establish behavior of all 18 banks until all 540 candidates are available.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-dir", type=Path, default=DEFAULT_EVAL)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    manifest_path = args.eval_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    cases = {c["case_id"]: c for c in manifest["cases"]}
    outputs = latest_normalized_outputs(args.eval_dir)
    if not outputs:
        raise SystemExit("No normalized V4 outputs are available yet.")

    candidates = []
    completed_files = []
    completed_raw_records = []
    by_case: dict[str, list[dict[str, Any]]] = {}
    for case_id, path in sorted(outputs.items()):
        if case_id not in cases:
            raise RuntimeError(f"normalized output has unknown case: {case_id}")
        output = json.loads(path.read_text())
        audited = [candidate_audit(cases[case_id], p) for p in output["prompts"]]
        if len(audited) != 30:
            raise RuntimeError(f"expected 30 prompts: {case_id}")
        candidates.extend(audited)
        by_case[case_id] = audited
        completed_files.append(file_record(path))
        raw_record = args.eval_dir / "validation" / "raw" / path.name
        if raw_record.exists():
            completed_raw_records.append(file_record(raw_record))

    audit = {
        "version": "v4-actual-prose-audit-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "method": "Rule-based inventory of actual scene prose, with model visual_signature retained only as a cross-check.",
            "no_model_calls": True,
            "read_only_inputs": True,
            "reference_metrics_reused_from": str(Path(__file__).with_name("audit_lived_in_specificity.py")),
            "screening_thresholds": {
                "repeated_artifact_category": "at least 12 of 30 candidates in one completed bank",
                "repeated_artifact_pair": "at least 8 of 30 candidates in one completed bank",
                "excessive_distress": "any severe dirt/damage/neglect/stain/tear category, or more than one unsoftened generic-wear term",
            },
        },
        "provenance": {
            "manifest": file_record(manifest_path),
            "system_prompt_sha256_from_manifest": manifest["provenance"]["system_prompt"]["sha256"],
            "camera_profiles_sha256_from_manifest": manifest["provenance"]["camera_profiles"]["sha256"],
            "completed_normalized_outputs": completed_files,
            "completed_raw_validation_records": completed_raw_records,
        },
        "authorized_case_count": manifest["scope"]["authorized_text_case_count"],
        "completed_case_count": len(outputs),
        "pending_case_count": manifest["scope"]["authorized_text_case_count"] - len(outputs),
        "completed_case_ids": sorted(outputs),
        "summary": aggregate(candidates),
        "by_case": {case_id: aggregate(rows) for case_id, rows in sorted(by_case.items())},
        "repeated_artifact_findings": concentration_findings(by_case),
        "candidates": candidates,
        "method_limitations": [
            "The prose parser uses a bounded visible-object lexicon and longest non-overlapping phrase matching; unfamiliar nouns can be missed.",
            "Signature disagreements are review triggers because neither the parser nor the model inventory is treated as ground truth in isolation.",
            "Lexical reference metrics are descriptive and have no calibrated image-quality threshold.",
            "Generated-image cue survival, product salience, and occlusion are outside this text-only audit.",
        ],
    }
    args.output_json.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n")
    args.output_md.write_text(render_markdown(audit))
    print(json.dumps({
        "json": file_record(args.output_json),
        "markdown": file_record(args.output_md),
        "completed_cases": len(outputs),
        "candidates": len(candidates),
        "summary": audit["summary"],
    }, indent=2))


if __name__ == "__main__":
    main()
