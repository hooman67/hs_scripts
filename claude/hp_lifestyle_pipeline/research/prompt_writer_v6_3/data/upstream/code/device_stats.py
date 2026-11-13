import re

import analyze

FAMILIES = (
    "Laptop", "Monitor", "Desktop tower", "All-in-one computer",
    "Mini PC", "Tablet", "Printer", "Keyboard / mouse", "Point-of-sale terminal",
)
TITLES = {
    "Laptop": "Laptops", "Monitor": "Monitors",
    "Desktop tower": "Desktop towers", "All-in-one computer": "All-in-one computers",
    "Mini PC": "Mini PCs", "Tablet": "Tablets", "Printer": "Printers",
    "Keyboard / mouse": "Keyboards & mice", "Point-of-sale terminal": "Point-of-sale terminals",
}
LABELS = {
    "Laptop": r"\blaptops?\b|\bchromebook\b",
    "Monitor": r"\bmonitors?\b|display screen|flat.screen display",
    "Desktop tower": r"\btower\b|\bprodesk\b|desktop (?:computer|pc)|workstation computer|black hp workstation",
    "All-in-one computer": r"all.in.one",
    "Mini PC": r"\bmini (?:pc|workstation)\b|compact (?:desktop|computer)|\bz2 mini\b",
    "Tablet": r"\btablets?\b",
    "Printer": r"\bprinter\b|\bcopier\b|industrial flatbed printing",
    "Keyboard / mouse": r"\bkeyboard\b|\bmouse\b",
    "Point-of-sale terminal": r"point.of.sale|pos terminal",
}


def anchor(family):
    return "device-" + re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")


def matches(family, value):
    if family == "Desktop tower" and re.search(r"monitor|all.in.one|mini pc", value, re.I):
        return False
    if family == "All-in-one computer" and re.search(r"printer|copier", value, re.I):
        return False
    if family == "Keyboard / mouse" and re.search(r"\bmidi\b", value, re.I):
        return False
    return bool(re.search(LABELS[family], value, re.I))


def placement(phrase, evidence, basis):
    if re.search(r"\bmouse\s*pad\b|\bdesk mats?\b", phrase, re.I):
        immediate = "Mouse pad / desk mat"
    elif re.search(r"\bstands?\b|\b(?:monitor|articulated) arm\b", phrase, re.I):
        immediate = "Device stand"
    else:
        immediate = analyze.classify(analyze.SURFACE_RULES, phrase)
    if immediate == analyze.UNKNOWN:
        return None
    materials = [name for name, regex in analyze.MATERIAL_RULES if re.search(regex, phrase, re.I)]
    if re.search(r"\bplastic\b", phrase, re.I):
        materials.append("Plastic")
    return {
        "immediate": immediate, "underlying": analyze.UNKNOWN,
        "materials": materials or [analyze.UNKNOWN], "evidence": evidence, "basis": basis,
    }


def entity_placements(row, family):
    found = []
    for entity in row["scap"]["entities"]:
        if not matches(family, entity["label"]):
            continue
        description = entity["description"]
        if re.search(r"\b(?:held|holding|handheld)\b", description, re.I) and re.search(r"person|people|hand|user", description, re.I):
            found.append({
                "immediate": "Handheld (person)", "underlying": analyze.UNKNOWN,
                "materials": [analyze.UNKNOWN], "evidence": description,
                "basis": "Device entity explicitly describes handheld use",
            })
            continue
        if re.search(r"\bwall.mounted\b", description, re.I):
            found.append({
                "immediate": "Wall mount", "underlying": analyze.UNKNOWN,
                "materials": [analyze.UNKNOWN], "evidence": description,
                "basis": "Device entity explicitly describes wall mounting",
            })
            continue
        entity_found = []
        for match in re.finditer(r"\b(?:on|atop|inside)\s+(.+?)(?=\b(?:on|atop|inside)\s+|[.;]|$)", description, re.I):
            prefix = re.split(r"[,;]", description[:match.start()])[-1]
            if re.search(r"\b(?:logo|text|interface|wallpaper|graphic|image|icons?|ports?|buttons?)\b.{0,50}$", prefix, re.I) and not re.search(
                r"\b(?:resting|sitting|stands?|placed|positioned|mounted)\b.{0,40}$", prefix, re.I
            ):
                continue
            phrase = re.split(
                r"\b(?:on|with|behind|beside|near|next to|in front of|while|and a|and an|and the)\b|,",
                match.group(1), maxsplit=1, flags=re.I,
            )[0]
            item = placement(phrase, f'{entity["label"]}: {description}', "Device entity placement")
            if item:
                entity_found.append(item)
        if entity_found:
            first = entity_found[0]
            if first["immediate"] in {"Device stand", "Mouse pad / desk mat"} and len(entity_found) > 1:
                first["underlying"] = entity_found[1]["immediate"]
            found.append(first)
    if found:
        return found
    for entity in row["scap"]["entities"]:
        if analyze.classify(analyze.SURFACE_RULES, entity["label"]) == analyze.UNKNOWN:
            continue
        if matches(family, entity["label"]):
            continue
        description = entity["description"]
        relation = re.search(r"\b(?:supporting|holding|holds|supports)\b([^.;]+)", description, re.I)
        if relation and matches(family, relation.group(1)):
            item = placement(entity["label"], f'{entity["label"]}: {description}', "Supporting entity explicitly names device")
            if item:
                found.append(item)
    return found


def observation(row, family):
    if family == "Printer":
        printer = row["printer_observation"]
        return {
            "role": printer["role"],
            "placements": [{
                "immediate": printer["support"], "underlying": analyze.UNKNOWN,
                "materials": printer["materials"], "evidence": printer["support_evidence"],
                "basis": "Reviewed printer-specific evidence",
            }],
        }
    primary = row["product_category"] == family
    role = "Primary / foreground" if primary else (
        "Workstation / mixed focus (not an exclusive device target)"
        if "workstation" in row["product_category"].lower() or "ambiguous" in row["product_category"].lower()
        else "Secondary / contextual"
    )
    placements = [row["support"]] if primary else entity_placements(row, family)
    if not placements:
        placements = [{
            "immediate": analyze.UNKNOWN, "underlying": analyze.UNKNOWN,
            "materials": [analyze.UNKNOWN], "evidence": "",
            "basis": "No explicit device-specific support relation; focal device's support not borrowed",
        }]
    return {"role": role, "placements": placements}


def annotate(rows):
    for row in rows:
        row["device_observations"] = {family: observation(row, family) for family in FAMILIES if family in row["device_presence"]}


def values(row, family, field):
    placements = row["device_observations"][family]["placements"]
    if field == "materials":
        return sorted({v for p in placements for v in p["materials"]})
    return sorted({p[field] for p in placements})


def group_counts(members, family):
    n = len(members)
    return {
        "supports": analyze.prevalence([values(r, family, "immediate") for r in members], n),
        "underlying_supports": analyze.prevalence([values(r, family, "underlying") for r in members], n),
        "support_materials": analyze.prevalence([values(r, family, "materials") for r in members], n),
        "roles": analyze.prevalence([[r["device_observations"][family]["role"]] for r in members], n),
        "support_evidence": analyze.prevalence(
            [list({p["basis"] for p in r["device_observations"][family]["placements"]}) for r in members], n),
        "surrounding_objects": analyze.prevalence([surroundings(r, family) for r in members], n),
    }


def surroundings(row, family):
    own = {
        "Laptop": {"Laptop"}, "Monitor": {"Monitor / display"},
        "Desktop tower": {"Desktop tower / mini PC"}, "Mini PC": {"Desktop tower / mini PC"},
        "All-in-one computer": {"All-in-one computer"}, "Tablet": {"Tablet"},
        "Printer": {"Printer"}, "Keyboard / mouse": {"Keyboard", "Mouse / mouse pad"},
        "Point-of-sale terminal": set(),
    }[family]
    return [name for name in row["objects"] if name not in own]
