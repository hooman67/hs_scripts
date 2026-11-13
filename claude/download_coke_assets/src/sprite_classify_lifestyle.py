#!/usr/bin/env python3
"""
Heuristic classifier: which Sprite assets are 'lifestyle' shots
(people interacting with bottles/cans) vs product silos / logos / packaging.
"""
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
manifest = json.load(open(ROOT / "sprite_image_manifest.json"))

# Strong lifestyle indicators (people / action / scene)
LIFESTYLE_TERMS = [
    # people
    r"\b(group|duo|trio|solo|couple|friends|family|multicultural|caucasian|asian|hispanic|latam|teen|teens|boy|boys|girl|girls|men|women|man|woman|people|crowd|kid|kids|consumer|consumers|player|players)\b",
    # action / interaction
    r"\b(celebrat|hugging|smile|smiling|drink|drinking|consum|consumption|anticipat|toast|cheers|laugh|laughing|jump|jumping|dance|dancing|party|hangout|share|sharing|pour|pouring|sip|sipping|hold|holding|hand|hands|grab|grabbing|cheer|cheering|fistbump|highfive)\b",
    # social / lifestyle scenes
    r"\b(lifestyle|lobby|pool|beach|stadium|fan|fans|street|kitchen|outdoor|backyard|bbq|picnic|eating|food|meal|moment|festival|concert|music|car|carduo|ride|drive)\b",
    # FIFA / sports lifestyle
    r"\b(scream|emotion|celebration|win|winning|goal|hugging)\b",
]
LIFESTYLE_RE = re.compile("|".join(LIFESTYLE_TERMS), re.IGNORECASE)

# Strong product-silo indicators (clean product, no people)
SILO_TERMS = [
    r"\b(silo|wordmark|logo|composite|partner|stamp|disc|vertical|horizontal|pack|6pk|12pk|18pk|35pk|fridge|fridge\s*pack|shrink|sleeve|carton|carton)\b",
    r"\b(can|bottle)\b.*\b(dry|wet|angle|straight|standalone|standalone)\b",
    r"\b(transparent|outline)\b",
]
SILO_RE = re.compile("|".join(SILO_TERMS), re.IGNORECASE)

# Numeric/SKU-only filenames (product shots from /products/)
SKU_RE = re.compile(r"^\d{8,}_[A-Z0-9]+\.(jpg|jpeg|png|tif|tiff)$", re.IGNORECASE)


def classify(asset):
    dam = asset["damPath"]
    name = asset["name"]
    lower = (dam + " " + name).lower()

    # 1. Product folder + SKU filename → silo product shot
    if "/products/" in dam and SKU_RE.match(name):
        return "product_silo"

    # 2. Strong lifestyle terms?
    has_lifestyle = bool(LIFESTYLE_RE.search(name))
    has_silo = bool(SILO_RE.search(name))

    if has_lifestyle and not has_silo:
        return "lifestyle"
    if has_lifestyle and has_silo:
        # Both — likely lifestyle scene WITH product (e.g. "GroupCelebrating_12oz_GlassBottle")
        return "lifestyle_with_product"
    if has_silo:
        return "product_silo"

    # 3. Marketing folder, no clear keyword → "marketing_other" (mixed bag)
    if "/marketing/" in dam:
        return "marketing_other"

    # 4. Products folder, no SKU pattern → product variants
    return "product_other"


# Classify all
counts = defaultdict(int)
samples = defaultdict(list)
for a in manifest:
    cls = classify(a)
    counts[cls] += 1
    if len(samples[cls]) < 8:
        samples[cls].append(a["damPath"])

total = sum(counts.values())
print(f"=== Sprite asset classification ({total} total) ===\n")
order = ["lifestyle", "lifestyle_with_product", "product_silo", "product_other", "marketing_other"]
for cls in order:
    pct = counts[cls] / total * 100
    print(f"  {counts[cls]:5d}  {pct:5.1f}%  {cls}")
print()

print("=== Lifestyle samples ===")
for s in samples["lifestyle"][:10]:
    print(f"  {s}")
print("\n=== Lifestyle_with_product samples ===")
for s in samples["lifestyle_with_product"][:10]:
    print(f"  {s}")
print("\n=== Marketing_other samples (uncertain — could be lifestyle OR silos) ===")
for s in samples["marketing_other"][:15]:
    print(f"  {s}")

# Save lists for downstream
out = {
    "lifestyle": [a["damPath"] for a in manifest if classify(a) == "lifestyle"],
    "lifestyle_with_product": [a["damPath"] for a in manifest if classify(a) == "lifestyle_with_product"],
    "marketing_other": [a["damPath"] for a in manifest if classify(a) == "marketing_other"],
}
out_file = ROOT / "sprite_lifestyle_classification.json"
json.dump(out, open(out_file, "w"), indent=2)
print(f"\nSaved → {out_file.name}")
