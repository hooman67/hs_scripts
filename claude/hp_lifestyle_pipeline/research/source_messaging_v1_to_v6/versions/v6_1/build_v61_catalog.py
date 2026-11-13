#!/usr/bin/env python3
"""Build the V6.1 runtime catalogue from frozen V6 and the V6.1 review menu.

V6 remains byte-for-byte untouched.  This compiler collapses visually similar
V6 repetition groups into the stricter V6.1 families, removes text/face-heavy
items that the V6.1 menu makes unavailable, and adds one environment-specific
entry for every new family in the V6.1 menu.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]
V6_CATALOG = HERE.parent / "v6" / "approved-20261029-r2.catalog.json"
V6_LEXICON = HERE.parent / "v6" / "prop_lexicon.json"
REVIEW = PROJECT / "research" / "approved_props_v6_1" / "PROPS_FOR_REVIEW.md"

CATALOG_VERSION = "hp-v6.1-approved-props-v1"
REVISION = "v6.1-expanded-20261103-r5"

PREFIX = {
    "Home": "HOM",
    "Office": "OFF",
    "Education": "EDU",
    "Gaming": "GAM",
    "Café": "CAF",
    "Creative Studio": "STU",
}

GROUP_MAP = {
    "notebook": "paper_materials", "ring_binder": "paper_materials",
    "document_folder": "paper_materials", "paper_documents": "paper_materials",
    "paper_cards": "paper_materials", "book": "paper_materials",
    "bookmark": "paper_materials", "rolled_drawing": "paper_materials",
    "pen": "writing_tools", "pencil": "writing_tools", "markers": "writing_tools",
    "crayons": "writing_tools", "charcoal": "writing_tools", "pastels": "writing_tools",
    "brush_holder": "tool_cup",
    "stapler": "paper_fasteners", "paper_clips": "paper_fasteners",
    "binder_clips": "paper_fasteners",
    "ruler": "measurement_tools", "protractor": "measurement_tools",
    "drawing_compass": "measurement_tools", "measuring_tape": "measurement_tools",
    "set_square": "measurement_tools",
    "cup_mug": "drinkware", "drinking_glass": "drinkware",
    "water_bottle": "drinkware",
    "teapot": "serving_vessels", "carafe": "serving_vessels",
    "milk_jug": "serving_vessels",
    "bowl": "food_bowl", "fruit": "food_bowl",
    "plate": "food_plate",
    "serving_tray": "tray_catchall", "dish_tray": "tray_catchall",
    "eyeglasses": "eyewear", "eyeglass_case": "eyewear",
    "shelving": "open_shelving", "storage_cabinet": "closed_storage",
    "rug": "floor_textile", "curtains": "window_textile",
    "throw_blanket": "soft_textile", "cushion": "soft_textile",
    "wall_art": "framed_wall_art", "pinboard": "wall_display_board",
    "whiteboard": "wall_writing_board", "chalkboard": "wall_writing_board",
    "banquette": "bench_seating", "globe": "relief_globe",
    "wooden_model": "prototype_model", "origami": "prototype_model",
    "basket": "woven_storage", "craft_cutting_mat": "work_mat",
    "chess_set": "strategy_game", "board_game": "strategy_game",
    "wooden_puzzle": "mechanical_puzzle", "candle": "decorative_candle",
    "ornament": "ceramic_object", "fabric_swatches": "material_swatches",
    "color_swatches": "material_swatches", "watercolor_paints": "paint_tools",
    "paintbrush": "paint_tools", "masking_tape": "adhesive",
    "scissors": "cutting_tools", "ribbon": "textile_notions",
    "thread_spool": "textile_notions", "storage_cart": "materials_cart",
    "light_panel": "wall_light_panels", "light_strip": "indirect_rgb",
    "knitting_needles": "fiber_craft", "yarn": "fiber_craft",
    "sewing_box": "sewing_kit", "eraser": "stationery_utility",
    "pencil_sharpener": "stationery_utility", "cake": "baked_food",
    "cookie": "baked_food", "pastry": "baked_food",
    "sandwich": "savory_food", "teaspoon": "cutlery",
    "napkin_holder": "napkin", "cut_flowers": "flower_vessel",
    "vase": "flower_vessel", "brick_sculpture": "block_sculpture",
    "hobby_model": "abstract_model", "display_stand": "display_plinth",
}

DROP_GROUPS = {
    "magazine", "photo_album", "business_card_holder", "calendar", "menu",
    "reference_photos", "card_album", "comic_book", "game_art_book",
    "letter_tiles", "wall_map", "playing_cards",
}
DROP_NAME_RE = re.compile(
    r"\b(?:magazine|photo album|business-card holder|desk calendar|receipt|"
    r"reference photograph|collectible-card album|comic book|game-art book|"
    r"table menu|letter tiles|wall map|playing cards)\b",
    re.I,
)

ROLE_HEADING = {
    "Smaller props": "tabletop_or_movable",
    "Background furnishings and décor": "background_furnishing_or_decor",
    "Wall and architectural details": "background_furnishing_or_decor",
}

EXTRA_ALIASES = {
    "paper_materials": ["stack of plain papers", "plain papers", "unlabelled folder", "paper notebook", "ring binder"],
    "reed_diffuser": ["reed diffuser", "glass diffuser"],
    "stone_object": ["river stones", "smooth stones", "stone arrangement"],
    "wood_sculpture": ["wood sculpture", "wooden sculpture", "abstract wooden sculpture", "abstract wooden tabletop sculpture", "original abstract wooden tabletop sculpture"],
    "ceramic_object": ["ceramic object", "ceramic ornament", "geometric ceramic form"],
    "blanket_ladder": ["blanket ladder", "wooden textile ladder"],
    "woven_wall_hanging": ["woven wall hanging", "fiber wall hanging"],
    "wall_slats": ["wood slats", "wood-slat wall", "ribbed wood panel", "slatted wall"],
    "wall_texture": ["limewash wall", "textured plaster", "plaster wall", "plaster test wall", "exposed brick", "concrete wall"],
    "acoustic_wall": ["acoustic panels", "felt panels", "sound-diffusion blocks", "sound diffuser"],
    "wall_relief": ["wall relief", "ceramic relief", "carved panel", "geometric relief panel"],
    "wall_display_board": ["corkboard", "corkboard with solid-color paper shapes", "pinboard", "material board", "abstract material board", "material board with color and texture samples"],
    "wall_shelving": ["floating shelf", "picture ledge", "wall-mounted ledge", "floating ledge"],
    "wall_lighting": ["wall sconce", "architectural sconce", "geometric wall light"],
    "geometric_wallpaper": ["geometric wallpaper", "nonfigurative wallpaper"],
    "peg_rail": ["peg rail", "wooden peg rail"],
    "tool_cup": ["pen cup", "pencil cup", "brush holder", "brush jar"],
    "paperweight": ["paperweight", "glass paperweight", "stone paperweight"],
    "tray_catchall": ["desk tray", "felt desk tray", "low felt tray", "ceramic desk tray", "serving tray", "key dish", "valet tray"],
    "decorative_candle": ["decorative candle", "pillar candle", "ceramic candleholder", "candleholder"],
    "desk_sculpture": ["desk sculpture", "abstract metal sculpture", "abstract wood sculpture"],
    "kinetic_object": ["kinetic object", "balance toy", "kinetic sculpture"],
    "material_samples": ["material samples", "finish samples", "architectural samples"],
    "room_divider": ["room divider", "ribbed-glass divider", "fluted-glass divider"],
    "meeting_screen": ["felt privacy screen", "freestanding privacy screen"],
    "wall_planter": ["wall planter", "wall-mounted planter"],
    "glass_partition": ["glass partition", "frosted glass partition", "clear architectural partition"],
    "perforated_panel": ["perforated metal panel", "perforated metal wall panel", "perforated panel"],
    "stationery_utility": ["eraser", "pencil sharpener", "manual pencil sharpener"],
    "geometric_solids": ["geometric solids", "wooden geometric solids"],
    "balance_scale": ["balance scale", "tabletop balance"],
    "magnifier": ["magnifying glass", "magnifier"],
    "mineral_samples": ["mineral samples", "mineral specimens"],
    "relief_globe": ["relief globe", "unlabelled globe", "globe showing raised land shapes"],
    "molecule_model": ["molecule model", "molecular model", "ball-and-stick model"],
    "gear_model": ["gear model", "wooden gear demonstration"],
    "color_sorting": ["color sorting cups", "solid-color counters"],
    "shape_puzzle": ["shape puzzle", "geometric inset puzzle"],
    "prism": ["optical prism", "glass prism"],
    "magnetic_tiles": ["magnetic tiles", "translucent geometric tiles"],
    "fossil_replica": ["fossil replica", "shell fossil replica", "leaf fossil replica"],
    "bridge_model": ["bridge model", "wooden truss model"],
    "materials_cart": ["materials cart", "rolling materials cart"],
    "geometric_mural": ["geometric mural", "color-block mural"],
    "relief_map": ["relief map", "raised geographic panel"],
    "shape_display": ["shape display", "geometric wall display"],
    "colored_glass": ["colored glass", "colored wall inserts", "translucent colored wall inserts", "stained-glass insert", "textured glass insert"],
    "mechanical_puzzle": ["mechanical puzzle", "interlocking puzzle"],
    "abstract_model": ["abstract model", "geometric vehicle model", "spacecraft-like model"],
    "geode": ["geode", "crystal specimen"],
    "lava_lamp": ["lava lamp"],
    "plasma_globe": ["plasma globe"],
    "metal_sculpture": ["metal sculpture", "abstract metal object"],
    "display_plinth": ["display plinth", "low plinth"],
    "marble_track": ["marble track", "sculptural marble track"],
    "backlit_niche": ["backlit niche", "recessed display niche"],
    "indirect_rgb": ["rgb light strip", "concealed rgb light strip", "concealed rgb lighting", "indirect rgb lighting"],
    "neon_shape": ["neon shape", "neon line", "geometric neon symbol"],
    "wall_light_panels": ["wall light panels", "decorative light panels"],
    "gradient_light": ["gradient light", "colored light wash"],
    "shadow_box": ["shadow box", "wall shadow box"],
    "sound_diffuser": ["sound diffuser", "wood sound-diffusion blocks"],
    "cutlery": ["teaspoon", "dessert fork"],
    "baked_food": ["croissant", "muffin", "cookie", "cake slice", "pastry"],
    "savory_food": ["sandwich"],
    "bread_basket": ["bread basket"],
    "napkin": ["cloth napkin", "folded napkin", "napkin holder"],
    "flower_vessel": ["bud vase", "flower vase"],
    "serving_tray": ["café tray", "serving tray"],
    "condiment_set": ["condiment set", "ceramic condiment pair"],
    "cake_stand": ["cake stand", "pastry stand", "pastry dome"],
    "decorative_tile": ["decorative tile", "ceramic tile accent"],
    "cafe_chair": ["café chair", "cafe chair", "bentwood chair"],
    "service_counter": ["café service counter", "service counter"],
    "pastry_display": ["pastry display", "pastry case"],
    "pendant_lighting": ["pendant lamp", "pendant lights", "pendant cluster"],
    "tile_wall": ["tile wall", "glazed tile wall", "zellige wall"],
    "decorative_plates": ["decorative wall plates", "ceramic wall plates"],
    "botanical_mural": ["botanical mural", "leaf-shape mural"],
    "plant_grid": ["plant grid", "wall grid with greenery"],
    "carved_panel": ["carved panel", "carved wood panel"],
    "paint_tools": ["watercolor palette", "paintbrushes", "palette knife", "mixing dish"],
    "material_swatches": ["fabric swatches", "color swatches", "wood swatches", "finish swatches"],
    "textile_notions": ["ribbon", "thread spool", "cord samples"],
    "cutting_tools": ["scissors", "craft knife"],
    "work_mat": ["cutting mat", "craft mat"],
    "adhesive": ["masking tape", "paper tape"],
    "ceramic_samples": ["ceramic test tile", "glaze sample"],
    "clay_samples": ["clay samples", "abstract clay forms"],
    "prototype_model": ["wooden model", "small wooden model", "origami model", "geometric origami form", "plaster prototype", "prototype model"],
    "wire_form": ["wire form", "wire armature"],
    "foam_forms": ["foam forms", "foam mock-up pieces"],
    "glass_samples": ["glass samples", "acrylic sample tiles"],
    "pigment_jars": ["pigment jars"],
    "stencil_shapes": ["geometric stencils", "stencil shapes"],
    "loom_sample": ["loom sample", "woven test panel"],
    "hand_roller": ["hand roller", "brayer", "printmaking roller"],
    "dowel_set": ["wooden dowels", "dowel set"],
    "easel": ["easel", "wooden easel"],
    "book_cart": ["book cart", "library cart", "rolling library cart"],
    "dress_form": ["dress form", "headless dress form"],
    "drying_rack": ["drying rack"],
    "material_roll_rack": ["material roll rack", "fabric roll rack", "paper roll rack"],
    "task_lighting": ["task lamp", "desk lamp", "studio lamp"],
    "display_pedestal": ["display pedestal", "studio pedestal"],
    "tool_pegboard": ["tool pegboard", "pegboard"],
    "large_canvas": ["abstract canvas", "large abstract canvas"],
    "wire_display_grid": ["wire display grid", "wall grid"],
    "hanging_textiles": ["hanging textiles", "hanging fabric strips"],
    "ceramic_tile_grid": ["ceramic tile grid", "tile sample grid"],
    "track_lighting": ["track lighting", "studio track lights"],
    "woven_wall_hanging": ["woven wall hanging", "woven fiber wall piece", "fiber wall piece"],
}

COMPOSITES = {
    "tool_cup": ["writing_tools"],
    "wall_planter": ["plant"],
    "plant_grid": ["plant"],
    "book_cart": ["paper_materials"],
    "easel": ["large_canvas"],
    "sewing_kit": ["measurement_tools"],
}


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold().replace("-", " ")
    value = re.sub(r"[^\w\s]", " ", value)
    return " ".join(value.split())


def plural(value: str) -> str:
    words = value.split()
    if not words:
        return value
    if words[-1].endswith("s"):
        return value
    words[-1] += "s"
    return " ".join(words)


def remap_group(group: str, *, entry_name: str, environment: str) -> str:
    if group == "chair":
        return "lounge_seating" if re.search(r"accent|lounge", entry_name, re.I) else (
            "café_chair" if environment == "Café" else "task_seating"
        )
    if group == "lamp":
        if "pendant" in entry_name.casefold():
            return "pendant_lighting"
        if "task" in entry_name.casefold():
            return "task_lighting"
        return "floor_lighting"
    return GROUP_MAP.get(group, group)


def parse_menu() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    environment = None
    role = None
    for raw in REVIEW.read_text(encoding="utf-8").splitlines():
        if raw.startswith("# "):
            name = raw[2:].strip()
            environment = name if name in PREFIX else None
            role = None
        elif raw.startswith("## "):
            role = ROLE_HEADING.get(raw[3:].strip()) if environment else None
        elif environment and role and raw.startswith("- `"):
            match = re.match(r"- `([a-z0-9_]+)`: (.+)", raw)
            if not match:
                raise ValueError(f"cannot parse V6.1 menu line: {raw}")
            family, description = match.groups()
            description = re.sub(r"\s*\*\*(?:New|Expanded)[^*]*\*\*", "", description).strip()
            if description.endswith("."):
                description = description[:-1]
            rows.append({"environment": environment, "role": role,
                         "family": family, "description": description})
    return rows


def main() -> None:
    base = json.loads(V6_CATALOG.read_text(encoding="utf-8"))
    review_bytes = REVIEW.read_bytes()
    entries: list[dict] = []
    inherited_aliases: dict[str, set[str]] = defaultdict(set)
    for old in base["entries"]:
        mapped = [remap_group(g, entry_name=old["name"], environment=old["environment"])
                  for g in old["repetition_groups"]]
        mapped = list(dict.fromkeys(mapped))
        if set(mapped).intersection(DROP_GROUPS) or DROP_NAME_RE.search(old["name"]):
            continue
        for group in mapped:
            inherited_aliases[group].update(
                norm(a) for a in old["aliases"]
                if norm(a) and norm(a) not in {"form", "forms", "document", "documents", "paper", "papers"}
            )

    counters = defaultdict(int)
    for row in parse_menu():
        counters[row["environment"]] += 1
        candidate_id = f"V61-{PREFIX[row['environment']]}-{counters[row['environment']]:03d}"
        groups = [row["family"], *COMPOSITES.get(row["family"], [])]
        aliases = {norm(row["family"].replace("_", " "))}
        aliases.update(inherited_aliases.get(row["family"], set()))
        aliases.update(norm(a) for a in EXTRA_ALIASES.get(row["family"], []))
        aliases = {a for a in aliases if a}
        aliases.update(plural(a) for a in list(aliases))
        entries.append({
            "id": candidate_id,
            "environment": row["environment"],
            "role": row["role"],
            "name": row["description"],
            "repetition_groups": list(dict.fromkeys(groups)),
            "aliases": sorted(aliases),
        })

    entries.sort(key=lambda item: (list(PREFIX).index(item["environment"]), item["role"], item["id"]))
    catalogue = {
        "version": CATALOG_VERSION,
        "revision": REVISION,
        "purpose": "production",
        "source_sha256": hashlib.sha256(review_bytes).hexdigest(),
        "entries": entries,
    }

    lexicon: dict[str, set[str]] = defaultdict(set)
    old_lexicon = json.loads(V6_LEXICON.read_text(encoding="utf-8"))
    for item in old_lexicon["entries"]:
        if norm(item["phrase"]) in {"form", "forms", "document", "documents", "paper", "papers"}:
            continue
        groups = {remap_group(g, entry_name=item["phrase"], environment="Office")
                  for g in item["groups"]}
        if groups.intersection(DROP_GROUPS):
            continue
        lexicon[norm(item["phrase"])].update(groups)
    for entry in entries:
        for alias in entry["aliases"]:
            lexicon[alias].update(entry["repetition_groups"])
    lexicon_doc = {
        "version": CATALOG_VERSION,
        "entries": [
            {"phrase": phrase, "groups": sorted(groups)}
            for phrase, groups in sorted(lexicon.items()) if phrase
        ],
    }

    (HERE / "approved-v6.1-20261103.catalog.json").write_text(
        json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (HERE / "prop_lexicon.json").write_text(
        json.dumps(lexicon_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "entries": len(entries),
        "groups": len({g for e in entries for g in e["repetition_groups"]}),
        "lexicon_phrases": len(lexicon_doc["entries"]),
        "new_entries": sum(counters.values()),
    }, indent=2))


if __name__ == "__main__":
    main()
