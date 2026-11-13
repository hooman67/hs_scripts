# HP lifestyle V6.2 prompt writer and natural-placement judge V4 review

You are reviewing two tightly connected product-LLM components for an HP lifestyle-image pipeline. Work at high reasoning effort. Return concrete, patch-ready recommendations grounded in the supplied human feedback. Do not write generic advice.

## Pipeline context

The runtime receives a Smart Brief, source messaging, and a fixed `deviceType_CameraName` tag. The writer returns ten ranked scene prompts. The primary HP device itself is supplied later as a digital-twin image, so the scene text must not name or describe it. A downstream image model creates a lifestyle scene around it.

V6.1 already enforces:

- exactly ten prompts planned as a bank;
- diverse environments, phrasing, light, support-surface treatments, wall treatments, and atmospheres;
- no semantic repetition of a prop or distinctive phrase family across the ten prompts;
- a closed, approved, environment-specific prop catalogue;
- no generated faces and minimal generated text;
- camera-aware detail with qualitative close/medium/wide guidance and no numeric noun quota;
- laptops can appear in plausible Home, Office, Education, Gaming, Café, or Creative Studio settings;
- printers normally appear only in Office, Home workspace, Education, or Creative Studio, on dedicated equipment tables rather than occupied desks;
- populated shelving and pegboards;
- source relevance and C-Tech style scores independent of one another.

The V3 visual judge receives the generated scene, original digital twin, product type, and scene prompt. It currently scores support/scenario, access/usability, orientation/alignment, scale/perspective, and contact/integration. An application derives a 0–100 score and pass/review/fail. Unobservable relations are not penalized.

## Requested V6.2 behavior

1. Add credible support-shape diversity. Laptop scenes, especially neighborhood cafés and other layouts where it is natural, should sometimes use round tables. Do not force round tables into every bank or every laptop scene. Printer supports should remain sturdy rectangular/square equipment tables, usually aligned near a wall, because that is the natural use case.
2. Avoid empty, unresolved walls. Visible walls should carry a coherent environment-specific treatment such as substantially visible abstract art, populated shelves/ledges, acoustic panels, architectural panels, texture, relief, a populated pegboard, or a non-legible board. The treatment must fit the crop. A close-up should not demand a complete distant wall.
3. Picture frames and wall art must sit in a compositionally credible place: substantially within the composition instead of clipped at the extreme edge, related to the furniture grouping below, and not apparently balanced on furniture or hidden behind the product.
4. Props must have plausible relationships. Avoid liquid vessels crowded beside a laptop, arbitrary rocks/paperweights, random puzzles under printer tables, plants on top of printers, warped interactions around coat stands/drapes, and isolated unrelated objects used only to fill space.
5. Furniture must form a coherent room. Rectangular/square furniture marooned in the middle of a home room is usually unnatural unless it clearly functions as a work island or communal table. Round tables work better for many freestanding laptop/café/social arrangements. Printer tables should be wall-oriented, with believable clearance and accessible fronts.
6. Preserve V6.1's natural C-Tech prose, prop-bank constraints, source scoring, ten-prompt diversity, and camera-aware density. Avoid overconstraining the image model with exact measurements or long geometric instructions.

## Current V6.1 prompt rules to revise

The current system prompt includes these relevant passages:

> Before drafting, allocate a different subsetting, activity, support-surface treatment, light character, wall treatment and atmosphere to each scene where the camera and environment allow it.

> Shelving, display ledges, and pegboards must look intentionally populated. Never ask for empty or blank shelving or pegboards. Select at least one additional approved prop for the visible contents, declare its catalogue ID, and describe the relationship plainly.

> Close-up: retain the recognizable place, support, natural light and approved nearby detail that can plausibly fit. Use one coherent local arrangement rather than an overloaded tabletop inventory. A partial object or subordinate background cue may be enough. Do not demand a complete room, fully visible distant furniture, or a tabletop spread that would need the camera to move.

> Medium: preserve an ordinary local working or living area, coherent materials, and subordinate room furnishings. Avoid multiple distant activities or competing focal points.

> Wide: retain C-Tech's richer room descriptions and natural depth with approved, unused furnishings. Prefer a coherent room with several compatible furnishings over a tabletop trio plus one isolated background cue. Related shelving, artwork and wall treatments can coexist without an automatic object-count failure.

> Laptop-tag scenes may use any plausible environment and an ordinary dedicated desk, meeting table, study table, café table, gaming desk, drafting table, or studio worktable.

> Printer-tag scenes normally use only Office, a Home workspace, Education, or Creative Studio. For printer tags, make the unnamed primary support a dedicated table or worktable. It must read as equipment support, not an occupied desk or someone's personal workstation.

The approved catalogue already has many environment-specific wall families: framed abstract art, woven wall pieces, wood slats, textured plaster/brick/concrete, acoustic panels, wall reliefs, populated ledges, sconces, geometric wallpaper/murals, non-legible boards, tile walls, decorative plates, colored-glass inserts, wall grids, material boards, perforated panels, shadow boxes, and populated shelves/pegboards. V6.2 can add more safe visual alternatives if needed. Fixed walls, floors, windows, and the primary supporting table are exempt from prop non-repetition; selected wall treatments and furnishings are not.

## C-Tech feedback on ten Cashmere laptop FrontCloseUp scenes

Each entry gives the prompt and human comment.

1. Office folder + frosted partition. Human: good, but add one or two plausible table/background props and a wall hanging to break up the background.
2. Office meeting table + water carafe + framed art. Human: good composition; water carafe is not ideal so close to the laptop.
3. Painting studio + watercolor palette/brushes + drying rack. Human: good output.
4. Studio table + color swatches + wooden model + flat-file cabinet. Human: good; bring framed picture farther into frame.
5. Home wooden desk + reading glasses + curtains. Human: good; bring framed picture farther into frame.
6. Office side table + document box + stone paperweight + wood slats. Human: rock would probably fail; add wall hanging/art to break white space.
7. Living-room end table + key dish + sconce + sofa. Human: table placement does not replicate a real-life scenario.
8. Education table + globe + wall display. Human: good output even though V3 called it fail.
9. Gaming desk + collectible coin + light panels. Human: okay, but gaming props should be better chosen and wall art/detail should add depth.
10. Classroom table + counting blocks + empty whiteboard. Human: okay, but table props should differ and a whiteboard must not be blank.

## C-Tech feedback on ten Magic printer FrontWide scenes

1. Placement/framing okay; increase wall covering to reduce white space. V3 called it fail.
2. Fail: plant appears on top of product and geometry warps around coat rack; increase wall covering. V3 called it pass.
3. Fail: furniture on right is unrealistic; increase wall covering. V3 called it pass.
4. Okay; wall covering/detail should be greater.
5. Okay; wall covering/detail should be greater.
6. Fail: table legs do not match; increase wall covering/detail. V3 called it fail.
7. Okay; wall covering/detail should be greater.
8. Fail: table warps around drapes; increase wall covering/detail. V3 called it pass.
9. Fail: product is too isolated and prop/wall covering choices are random; increase wall covering/detail. V3 called it pass.
10. Okay; wall covering/detail should be greater.

## Additional judge disagreements from the same review

- Two laptop medium scenes were failed mainly because a chair was slightly displaced. Human says chairs move; modest chair displacement should be review or lower severity unless it faces far away or creates actual unusability.
- A laptop close-up was failed for no visible chair. Human says the crop may hide the chair; this is a warning/uncertainty, not fail.
- Two other laptop scenes failed for chair alignment should pass; the table angle may merit only a warning.
- A printer wide scene passed, but the human says fail: the table is deformed because its two rigid side edges are not parallel in perspective, and a rectangular table is implausibly marooned in the middle of a home room. The printer itself is correctly placed on the table.
- A printer close-up passed but should fail for the same rectangular-table-in-room problem.
- A printer close-up failed correctly, with added human evidence that the wall/table perspective is incoherent relative to a cabinet that actually touches the wall.
- A printer medium scene passed but should fail because the table legs are missing.
- Another printer medium passed but should fail because the printer/table station leaves an excessive gap from the wall even allowing cable clearance.
- A laptop medium failed partly for chair placement, but human says the decisive defect is a missing table leg.
- A printer close-up passed but should fail because the printer is slanted on the table and a random puzzle sits under the table.
- A printer close-up passed; human says review only because eyeglasses are malformed and the table may be too long. Everything else is good.
- Another printer close-up passed but should fail because the table placement is strange and a random puzzle lies on the floor.

## Required analysis and output

First separate each finding into one of these categories:

- prompt-writer-preventable;
- downstream image-generation defect that the prompt can only weakly influence;
- visual-judge calibration/detection issue;
- outside the natural-placement judge's intended scope.

Then return these sections:

### A. V6.2 exact system-prompt patch text

Provide concise replacement/addition paragraphs and state exactly after which current heading each belongs. Cover support shape, table placement in the room, wall composition, framed art placement, prop relationships, and camera adaptation. Avoid numeric object caps and exact geometric measurements. Do not require a visible wall when the camera/crop cannot show one.

### B. Catalogue/validator changes

List only deterministic checks that are safe and useful. Distinguish text-lint checks from constraints that require visual inspection after generation. Recommend any new approved wall or furnishing families needed for ten-prompt diversity. Do not claim a prompt validator can detect image warping.

### C. Judge V4 design

Recommend the smallest coherent change to V3 that captures the human feedback. Specify:

- whether to add a new room-composition component or extend existing components;
- exact issue codes and definitions;
- severity rules, especially chair displacement versus missing furniture legs/table deformation;
- crop/unobservable behavior;
- how to assess rigid-edge perspective without mistaking normal vanishing-point convergence for deformation;
- how to treat bare walls and sparse staging without allowing wall richness to overwhelm natural placement;
- deterministic score/cap changes, if any.

### D. Calibration table

For every disagreement bullet above and the 20 grouped examples, give an expected V4 verdict (`pass`, `review`, or `fail`) and the main issue code(s). Where the C-Tech comment is about style rather than natural placement, say so and do not manufacture a placement failure.

### E. Risks and ablations

Identify prompt changes most likely to create overconstraint or regress close-up composition. Propose a small text pilot and a held-out judge validation before a full image run.

Be decisive. The final V4 must measurably improve agreement on these annotated cases rather than merely add more prose.
