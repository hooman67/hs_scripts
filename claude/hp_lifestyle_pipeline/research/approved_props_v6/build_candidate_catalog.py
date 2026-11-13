#!/usr/bin/env python3
"""Build a proposal for human approval; this is not a runtime allowlist.

The authored rows are environment-specific alternatives, not claims of product
category clearance. Stable review IDs and repetition groups make later decisions
auditable. Never run this over recorded reviewer decisions without merging them.
"""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# repetition groups | candidate name. Compound entries reserve all named groups.
MENUS = {
    "Office": ("OFF", """
notebook|Paper notebook
pen|Pen
pencil|Pencil
document_folder|Document folder
ring_binder|Ring binder
paper_documents|Stack of papers
clipboard|Clipboard
sticky_notes|Sticky notes
paper_cards|Index cards
calendar|Desk calendar
stapler|Stapler
paper_clips|Paper clips
binder_clips|Binder clips
ruler|Ruler
pencil_case|Pencil case
letter_tray|Letter tray
document_box|Document storage box
book|Reference book
magazine|Magazine
eyeglasses|Reading glasses
business_card_holder|Business-card holder
desk_nameplate|Desk nameplate
drinking_glass|Water glass
water_bottle|Reusable water bottle
cup_mug|Ceramic mug
coaster|Coaster
bowl|Small snack bowl
bowl,fruit|Fruit bowl
lunch_container|Lunch container
vase|Small ceramic vase
""", """
chair|Ordinary upholstered office chair
shelving|Bookcase
storage_cabinet|Low storage cabinet
pinboard|Cork pinboard
wall_art|Framed artwork
plant|Potted plant
lamp|Floor lamp
rug|Area rug
curtains|Curtains
coat_stand|Coat stand
"""),
    "Home": ("HOM", """
book|Paperback book
magazine|Magazine
notebook|Paper notebook
pen|Pen
document_folder|Document folder
paper_documents|Stack of household papers
photo_album|Photo album
eyeglasses|Reading glasses
eyeglass_case|Glasses case
bookmark|Bookmark
cup_mug|Ceramic mug
drinking_glass|Water glass
water_bottle|Reusable water bottle
coaster|Coaster
teapot|Teapot
carafe|Water carafe
bowl,fruit|Fruit bowl
bowl|Small snack bowl
serving_tray|Serving tray
napkin|Folded cloth napkin
vase|Small vase
ornament|Ceramic ornament
dish_tray|Small dish for keys
yarn|Ball of yarn
knitting_needles|Knitting needles
sewing_box|Sewing box
jigsaw_puzzle|Jigsaw puzzle
candle|Decorative candle
basket|Woven storage basket
chess_set|Chess set
""", """
sofa|Comfortable sofa
chair|Accent chair
throw_blanket|Casually draped throw blanket
cushion|Cushion
rug|Woven rug
curtains|Soft curtains
shelving|Bookshelf
lamp|Floor lamp
plant|Houseplant
photo_frame|Framed family photograph
"""),
    "Education": ("EDU", """
book|Textbook
notebook|Exercise notebook
pencil|Pencil
eraser|Eraser
pencil_sharpener|Manual pencil sharpener
ruler|Ruler
protractor|Protractor
drawing_compass|Drawing compass
paper_cards|Index cards
paper_cards|Flashcards
paper_documents|Worksheets
document_folder|Folder
ring_binder|Ring binder
clipboard|Clipboard
bookmark|Bookmark
sticky_notes|Sticky notes
pencil_case|Pencil pouch
crayons|Crayons
markers|Colored markers
watercolor_paints|Watercolor paint set
paintbrush|Paintbrushes
scissors|School scissors
glue_stick|Glue stick
counting_blocks|Counting blocks
letter_tiles|Letter tiles
globe|Tabletop globe
abacus|Abacus
hourglass|Sand timer
water_bottle|Reusable water bottle
clay_model|Student clay model
""", """
chair|Classroom or library chair
shelving|Low bookshelf
book_cart|Book cart
pinboard|Classroom bulletin board
whiteboard|Whiteboard
wall_map|Wall map
storage_cubbies|Open storage cubbies
plant|Potted plant
wall_art|Framed student artwork
rug|Reading-area rug
"""),
    "Gaming": ("GAM", """
book|Game-art book
magazine|Gaming magazine
book|Comic book
figurine|Original unbranded miniature figure
wooden_puzzle|Wooden puzzle
chess_set|Chess set
paper_cards|Playing cards
dice|Dice
board_game|Unbranded board game
puzzle_cube|Puzzle cube
hobby_model|Unbranded hobby model
card_album|Collectible-card album with original artwork
collector_coin|Decorative collector coin
trophy|Small unbranded trophy
brick_sculpture|Building-block sculpture
display_stand|Small display stand
water_bottle|Reusable water bottle
drinking_glass|Drinking glass
cup_mug|Ceramic mug
coaster|Coaster
bowl|Snack bowl
popcorn_tub|Popcorn tub
plate|Small snack plate
biscuit_tin|Biscuit tin
bowl,fruit|Fruit bowl
napkin|Folded napkin
carafe|Drink carafe
keepsake_box|Keepsake box
hourglass|Sand timer
ornament|Small metal desk ornament
""", """
shelving|Display shelving
storage_cabinet|White storage cabinet
wall_art|Bold wall art
light_strip|Decorative RGB light strip
light_panel|Decorative wall light panels
lamp|Floor lamp
cushion|Lounge cushion
throw_blanket|Throw blanket
rug|Area rug
ottoman|Upholstered ottoman
"""),
    "Café": ("CAF", """
cup_mug|Ceramic coffee cup
drinking_glass|Water glass
water_bottle|Reusable water bottle
teapot|Teapot
milk_jug|Small milk jug
bowl|Sugar bowl
sugar_sachets|Sugar sachets
teaspoon|Teaspoon
saucer|Saucer
plate|Small pastry plate
pastry|Croissant
pastry|Muffin
cake|Slice of cake
cookie|Cookie
sandwich|Sandwich
basket,bread|Bread basket
napkin|Folded napkin
napkin_holder|Napkin holder
menu|Table menu
book|Paperback book
magazine|Magazine
notebook|Paper notebook
pen|Pen
eyeglasses|Reading glasses
eyeglass_case|Glasses case
coaster|Coaster
carafe|Water carafe
vase,cut_flowers|Bud vase with a flower
serving_tray|Serving tray
paper_documents|Receipt
""", """
banquette|Upholstered banquette
chair|Bentwood café chair
shelving|Open shelving
chalkboard|Chalkboard menu
wall_art|Framed artwork
plant|Leafy plant
lamp|Pendant lamp
curtains|Café curtains
coat_stand|Coat stand
rug|Woven rug
"""),
    "Creative Studio": ("STU", """
notebook|Sketchbook
pencil|Graphite pencils
charcoal|Drawing charcoal
pencil|Colored pencils
pen|Drawing pens
markers|Marker set
pastels|Pastel sticks
watercolor_paints|Watercolor palette
paintbrush|Paintbrushes
brush_holder|Brush holder
fabric_swatches|Fabric swatches
color_swatches|Color swatches
ribbon|Ribbon
thread_spool|Thread spool
measuring_tape|Measuring tape
ruler|Ruler
set_square|Set square
scissors|Scissors
craft_cutting_mat|Craft cutting mat
masking_tape|Masking tape
binder_clips|Binder clips
reference_photos|Reference photographs
book|Art book
paper_documents|Rolled drawing
paper_documents|Drawing sheets
ceramic_tile|Ceramic test tile
wooden_model|Small wooden model
origami|Paper origami model
document_folder|Portfolio folder
pencil_case|Pencil case
""", """
stool|Studio stool
pinboard|Reference pinboard
easel|Easel
shelving|Open shelving
storage_cabinet|Side cabinet
storage_cart|Rolling materials cart
wall_art|Framed artwork
plant|Potted plant
curtains|Linen curtains
lamp|Task lamp
"""),
}

UNCERTAIN = [
    ("keyboard", "Keyboard", "Computing peripheral; prior writer excluded. Unbranded does not establish approval."),
    ("mouse", "Mouse or trackball", "Computing peripheral; category clearance required."),
    ("headset", "Headset, headphones, or earbuds", "Audio/gaming accessory; category clearance required."),
    ("speaker", "Speakers or soundbar", "Audio/conferencing accessory; category clearance required."),
    ("controller", "Game controller", "Gaming accessory; category clearance required."),
    ("webcam", "Webcam", "Computing/conferencing accessory; category clearance required."),
    ("microphone", "Microphone", "Gaming/conferencing accessory; category clearance required."),
    ("speakerphone", "Conference speakerphone", "Conferencing hardware; previously added downstream despite omission upstream."),
    ("dock", "Docking station or USB hub", "Computing accessory; category clearance required."),
    ("drawing_tablet", "Drawing tablet or digital stylus", "Digital drawing hardware; distinct from an ordinary pen/pencil."),
    ("monitor", "Monitor or portable display", "Extra computing hardware already excluded by the writer boundary."),
    ("phone_tablet", "Phone, tablet, or e-reader", "Extra computing hardware; no approval currently granted."),
    ("game_console", "Game console, handheld console, or VR headset", "Gaming hardware; no approval currently granted."),
    ("external_storage", "External drive, USB drive, or memory card", "Computing accessory; category clearance required."),
    ("charging_accessory", "Charger, charging stand, power bank, or device cable", "Device accessory; could imply or introduce additional hardware."),
    ("mouse_mat", "Mouse mat, desk mat, or wrist rest", "Computing/gaming accessory, even without a visible brand."),
    ("laptop_bag", "Laptop bag, sleeve, or backpack", "Potential computing-accessory overlap; omit pending category decision."),
    ("gaming_chair", "Specialized gaming chair", "Specialized gaming furniture; ordinary chairs are separate review candidates."),
    ("print_consumables", "Ink, toner, refill bottle, or branded paper packaging", "Printing consumables; no approval. Loose scene papers require their own approval, not a consumable-product claim."),
    ("printer_scanner", "Extra printer, scanner, copier, or label printer", "Extra product hardware already excluded by the writer boundary."),
    ("computer", "Extra laptop, desktop, miniPC, or all-in-one", "Extra product hardware already excluded. Primary device comes only from the supplied twin."),
    ("branded_object", "Recognizably branded or licensed props", "Approval for a generic object does not approve branded/recognizable product versions."),
]


def main():
    target = ROOT / "data" / "prop_candidates.csv"
    if target.exists():
        with target.open(newline="", encoding="utf-8") as handle:
            if any(row.get("reviewer_decision") or row.get("reviewer_notes") for row in csv.DictReader(handle)):
                raise SystemExit("Reviewer decisions exist: merge source updates; do not overwrite this file.")
    rows = []
    for environment, (prefix, small, background) in MENUS.items():
        for role, block, first_index, expected in [
            ("tabletop_or_movable", small, 1, 30),
            ("background_furnishing_or_decor", background, 31, 10),
        ]:
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            assert len(lines) == expected, (environment, role, len(lines))
            for number, line in enumerate(lines, first_index):
                groups, name = line.split("|", 1)
                rows.append(dict(candidate_id=f"{prefix}-{number:02d}", environment=environment,
                                 role=role, name=name, repetition_groups=groups,
                                 status="pending_review", runtime_allowed="false",
                                 review_reason="Proposed ordinary scene item; customer approval pending.",
                                 reviewer_decision="", reviewer_notes=""))
    for number, (group, name, reason) in enumerate(UNCERTAIN, 1):
        rows.append(dict(candidate_id=f"UNC-{number:02d}", environment="Cross-environment",
                         role="uncertain_accessory_or_product", name=name, repetition_groups=group,
                         status="uncertain_not_approved", runtime_allowed="false",
                         review_reason=reason, reviewer_decision="", reviewer_notes=""))
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    summary = ROOT / "SUMMARY.md"
    if summary.exists():
        menu = []
        for environment in ("Home", "Office", "Education", "Gaming", "Café", "Creative Studio"):
            members = [row for row in rows if row["environment"] == environment]
            menu.extend([f"### {environment}", "", "| Review IDs | Role | Candidates |", "|---|---|---|"])
            for offset in range(0, 40, 10):
                group = members[offset:offset + 10]
                role = "Tabletop / movable" if offset < 30 else "Background / décor"
                names = "; ".join(row["name"] for row in group)
                menu.append(f"| {group[0]['candidate_id']}–{group[-1]['candidate_id']} | {role} | {names} |")
            menu.append("")
        menu.extend(["### Uncertain — not approved for use", "", "These entries are retained for an explicit approve/reject/hold decision; none is available to the runtime.", "", "| ID | Candidate category | Reason for hold |", "|---|---|---|"])
        for row in rows:
            if row["status"] == "uncertain_not_approved":
                menu.append(f"| {row['candidate_id']} | {row['name']} | {row['review_reason']} |")
        text = summary.read_text(encoding="utf-8")
        before, remainder = text.split("<!-- PROP_MENU_START -->", 1)
        _, after = remainder.split("<!-- PROP_MENU_END -->", 1)
        summary.write_text(before + "<!-- PROP_MENU_START -->\n\n" + "\n".join(menu) + "\n\n<!-- PROP_MENU_END -->" + after, encoding="utf-8")
    counts = Counter(row["environment"] for row in rows)
    assert len({row["candidate_id"] for row in rows}) == len(rows)
    assert all(row["runtime_allowed"] == "false" for row in rows)
    print(json.dumps({"rows": len(rows), "counts": counts, "approved": 0}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
