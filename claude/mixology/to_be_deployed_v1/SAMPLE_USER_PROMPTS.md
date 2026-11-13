# Sample user prompts by pipeline phase

These are user prompts only. They do not replace the packaged system prompts, mode clauses or ordered image inputs described in `README.md`.

## Phase A — generate one uniform single drink

Run Phase A once for each required drink. Image 1 must always be `01_single_drink/neutral_master_v1.png`.

### Recipe mode

Use with `01_single_drink/system_v1.txt` and `01_single_drink/recipe_mode_clause.txt`.

#### Clear strawberry-mint soda

```text
Make Fresh Breeze: 400 ml Sprite or Sprite Zero Sugar, 5 ml strawberry syrup,
10 ml mojito mint syrup, ice filling one third of the cup, and a vanilla
soft-serve float. Keep the soda mostly clear, with the strawberry concentrated
around the upper ice. Do not make the drink green and do not add mint leaves.
```

#### Red cherry cola

```text
Make Velvet Cherry: 400 ml Coca-Cola or Coca-Cola Zero Sugar, 5 ml vanilla
syrup, 15 ml cherry syrup, ice filling one third of the cup, and a vanilla
soft-serve float. Show a dark cola body with localized red cherry syrup and
subtle cream interaction near the top. Do not add cherries or other garnish.
```

#### Orange tropical soda

```text
Make Tropical Sunset: 400 ml Fanta Orange, 5 ml strawberry syrup, 5 ml coconut
syrup, ice filling one third of the cup, and a vanilla soft-serve float. Keep an
orange soda body with localized red strawberry syrup among the upper ice. Do
not add strawberries, coconut pieces, fruit slices or a straw.
```

#### Generic new recipe

```text
Make one drink using: [BASE DRINK AND QUANTITY], [SYRUP AND QUANTITY],
[ADDITIONAL SYRUP AND QUANTITY], [ICE AMOUNT], and [TOPPING]. Render only those
ingredients. Keep the liquid appearance [CLEAR / MIXED / LAYERED], with
[COLOR OR SYRUP] concentrated [LOCATION]. Do not add fruit, herbs, garnish,
straws, lids, labels or logos unless explicitly listed as ingredients.
```

### Appearance-reference mode

Use with `01_single_drink/system_v1.txt` and `01_single_drink/reference_image_mode_clause.txt`.

Ordered images:

1. Neutral master — geometry and camera authority.
2. User-provided drink — beverage appearance only.

#### Closely match the referenced beverage

```text
Create one finished drink whose beverage contents match Image 2: preserve its
liquid colors, layering, syrup placement, ice character, bubbles and visible
ingredient textures. Transfer only those beverage details into Image 1. Keep
Image 1's cup, rim, taper, molded base, soft-serve shape, size, position,
camera view, white background and contact shadow unchanged. Do not copy Image
2's vessel, framing, lighting, labels, logo, straw, lid or garnish.
```

#### Match selected details from the reference

```text
Use Image 2 only to define the drink's [LIQUID COLOR], [LAYERING], [SYRUP
PATTERN], [ICE APPEARANCE] and [BUBBLES OR TEXTURE]. Recreate those contents
inside Image 1 while preserving Image 1's complete cup, soft-serve silhouette,
viewpoint, framing and studio background. Ignore all other features from Image
2 and add no unrequested ingredients.
```

## Phase B — combine individual drinks into a group

Use `02_group_composition/system_v1.md` as the GPT-6 Astra system instruction.
Each supplied image must be one completed Phase A drink. Image numbers below
refer to their upload order.

### Two cups, side by side

```text
Arrange Image 1 on the left and Image 2 on the right, side by side in one row
on one baseline. Use a small clear gap with no overlap. Keep both drinks fully
visible and at comparable physical scale.
```

### Two cups, shallow stagger

```text
Arrange Image 1 slightly forward-left and Image 2 slightly back-right in a
compact shallow stagger. Use restrained overlap while keeping both toppings,
cup bodies and bases identifiable. Do not enlarge the foreground cup.
```

### Three cups, straight lineup

```text
Arrange Image 1 on the left, Image 2 in the center and Image 3 on the right in
one straight row on one baseline. Use small even gaps, no overlap and comparable
cup-body scale. Keep every complete drink inside the frame.
```

### Three cups, center drink in front

```text
Arrange Image 2 front-center, Image 1 back-left and Image 3 back-right in a
compact shallow staggered group. Use restrained overlap, keeping every topping,
most of each cup body and every base identifiable. Preserve comparable cup scale
and do not turn Image 2 into an oversized foreground hero.
```

### Three cups, named arrangement

```text
Arrange the [ORANGE] drink from Image 2 front-center, the [RED] drink from
Image 1 back-left and the [AMBER] drink from Image 3 back-right. Keep this exact
identity-to-slot mapping in a compact shallow group. Use modest depth offsets,
restrained overlap and comparable cup-body scale.
```

### Five cups, straight lineup

```text
Arrange Images 1 through 5 from left to right in their supplied order, in one
straight row on one baseline. Use small clear gaps and no overlap. Keep every
drink complete, upright and at comparable physical scale; fit the composition
by adjusting overall scale and spacing rather than changing cup proportions.
```

### Five cups, shallow stagger

```text
Create a compact five-cup group with Images 2 and 4 slightly forward and Images
1, 3 and 5 slightly behind. Preserve this exact identity-to-slot mapping. Use
only shallow depth offsets and restrained overlap so that every topping and base
remains identifiable. Keep foreground enlargement modest and preserve each
source drink's cup proportions and contents.
```

### Generic arrangement template

```text
Arrange [IMAGE NUMBER + DRINK IDENTITY + POSITION] and [REPEAT FOR EVERY
DRINK]. Use a [SIDE-BY-SIDE / STRAIGHT LINEUP / COMPACT SHALLOW STAGGER]
composition. Preserve the exact identity-to-slot mapping, comparable physical
cup scale, complete toppings and identifiable bases. Use restrained overlap and
keep the complete group inside the frame. Do not add refractions yet.
```

## Phase C — add refractions

Use `03_add_refractions/system_v3_frozen.md` as the GPT-6 Astra system
instruction.

Ordered images:

1. Phase B group output — authoritative edit target.
2. `03_add_refractions/style_reference_image_027.jpg` — lighting style only.

### Recommended default

```text
Add refractions. Keep the existing cup arrangement exactly.
```

### More explicit preservation request

```text
Add the Mixology refraction treatment. Keep the existing cup count, identities,
arrangement, relative scale, camera, crop, drink contents and white background
exactly. Use Image 2 only as the lighting-style reference.
```

### Single-drink refraction edit

```text
Add refractions. Preserve this exact drink, cup shape, viewpoint, crop and
contents. Use Image 2 only as the lighting-style reference.
```

## End-to-end three-cup example

1. Run Phase A separately for a red drink, an orange drink and an amber drink.
2. Upload those three outputs to Phase B as Images 1–3 and use:

```text
Arrange the orange drink from Image 2 front-center, the red drink from Image 1
back-left and the amber drink from Image 3 back-right in a compact shallow
staggered group. Keep comparable cup scale and preserve every drink's contents.
```

3. Upload the Phase B output as Phase C Image 1 and the packaged style reference
as Image 2, then use:

```text
Add refractions. Keep the existing cup arrangement exactly.
```
