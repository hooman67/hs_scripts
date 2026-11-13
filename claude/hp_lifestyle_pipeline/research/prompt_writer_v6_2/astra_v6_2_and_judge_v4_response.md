## Findings: ownership before changes

The main change should be **better scene planning plus a judge that evaluates the supporting furniture and room arrangement—not just the device’s placement on the tabletop**. Wall richness should remain a separate creative-quality concern.

References below: **L1–L10** = laptop examples; **P1–P10** = printer examples; **D1–D12** = additional disagreement bullets, in order.

| Finding | Primary category | Consequence |
|---|---|---|
| Laptop support shapes lack credible variety | **Prompt-writer-preventable** | Add shape to bank planning; use round tables where the setting supports them, without a quota. |
| Equipment tables or home work surfaces lack a believable room position: L7, D4–D5, D8, D12 | **Prompt-writer-preventable** | Specify a plausible furniture grouping or wall-oriented station. |
| Visible backgrounds are unresolved; boards are blank; artwork sits at an extreme edge: L1, L4–L6, L9–L10, wall comments throughout P1–P10 | **Prompt-writer-preventable** | Add crop-aware wall treatment and artwork placement rules. |
| Carafes crowd the working area; props lack purpose or placement relationships: L2, L6, L9–L10, P9, D10, D12 | **Prompt-writer-preventable** | Require a useful relationship, not merely an approved catalogue ID. |
| A plant is rendered on the printer: P2 | **Downstream image-generation defect that the prompt can only weakly influence** | Give plants an explicit approved location away from the insertion area; judge the rendered result. |
| Furniture warps, mismatched or missing legs, impossible intersections, incoherent perspective: P2–P3, P6, P8, D4, D6–D7, D9 | **Downstream image-generation defect that the prompt can only weakly influence** | Add explicit furniture-structure detection to V4. More geometric prose is not the remedy. |
| Printer/table alignment is visibly wrong: D10 | **Downstream image-generation defect that the prompt can only weakly influence** | Judge the actual alignment; do not equate all rotation with error. |
| Eyeglasses are malformed: D11 | **Downstream image-generation defect that the prompt can only weakly influence** | At most a review-level, station-local artifact finding—not a placement failure. |
| Slightly displaced or unseen chairs cause failures: D1–D3 | **Visual-judge calibration/detection issue** | Distinguish movable furniture, actual unusability, and crop uncertainty. |
| Correctly placed devices mask defective tables or room layouts: P2–P3, P8–P9, D4–D5, D7–D8, D10, D12 | **Visual-judge calibration/detection issue** | Extend existing components to the complete station. |
| L8 and P1 were failed despite acceptable placement | **Visual-judge calibration/detection issue** | Remove unsupported penalties; retain only observable placement evidence. |
| More wall coverage, more attractive gaming props, or less sparse styling | **Outside the natural-placement judge’s intended scope** | Return creative advisories separately; do not lower placement scores. |
| An arbitrary rock or puzzle is aesthetically inappropriate, but does not obstruct or destabilize anything | **Outside the natural-placement judge’s intended scope** | Flag prop relevance separately. Do not manufacture a physical failure. |

These are distinct findings: for example, **writing an unresolved wall is writer-preventable**, while **penalizing insufficient wall decoration in a natural-placement score is out of scope**.

---

# A. V6.2 exact system-prompt patch text

The supplied excerpts do not include their actual heading names. To avoid inventing them, each patch identifies the **current owning section by an exact passage anchor**. These locations are unambiguous for implementation.

### A1. Bank planning — replace the paragraph beginning “Before drafting, allocate…”

> Before drafting, allocate a different subsetting, activity, support-surface treatment, light character, wall treatment and atmosphere to each scene where the camera and environment allow it. Include support shape and the support’s relationship to the room in this plan. Use round tables selectively in laptop scenes where café, social, communal or compact freestanding arrangements make them natural; do not require a round table in every bank. Keep all existing prop-family and distinctive-phrase non-repetition rules. Shape variety must improve plausibility rather than introduce an unusual table solely for variety.

### A2. Laptop environments/supports — replace the paragraph beginning “Laptop-tag scenes may use…”

> Laptop-tag scenes may use any plausible environment and an ordinary dedicated desk, meeting table, study table, café table, gaming desk, drafting table or studio worktable. Choose a credible support shape for the setting. Round café or small communal tables are useful alternatives to rectangular desks, especially in freestanding arrangements. Rectangular or square furniture in a Home setting should belong to a recognizable workspace or furniture grouping, or clearly function as a work island or communal table; do not leave it arbitrarily marooned in the room. Describe the arrangement briefly and naturally.

### A3. Printer environments/supports — replace the paragraph beginning “Printer-tag scenes normally use…”

> Printer-tag scenes normally use only Office, a Home workspace, Education or Creative Studio. Make the unnamed primary support a sturdy rectangular or square dedicated equipment table or worktable, not an occupied desk or someone’s personal workstation. Usually place it near and coherently oriented to a wall, with ordinary service clearance and an accessible front. Avoid unexplained open space behind the station or an isolated equipment table in the middle of a domestic room. A freestanding arrangement is acceptable only when the room clearly establishes a purposeful equipment island or shared production area.

### A4. Wall composition — insert immediately after the existing shelving/display-ledges/pegboards paragraph

> When a meaningful area of wall is visible, give it a coherent, environment-specific treatment from the approved catalogue rather than leaving an unresolved blank backdrop. Use the treatment at a scale that reads in the intended crop: substantially visible abstract art, a populated shelf or ledge, acoustic or architectural panels, texture, relief, a populated pegboard, or a non-legible board can all work. Do not add wall art automatically when an existing material or architectural treatment already resolves the background. Do not require a wall when the camera cannot show one. Fixed walls remain exempt from prop non-repetition, but selected wall-treatment families do not.

Retain the existing populated-shelving rule unchanged. Add this sentence to it:

> Boards must contain abstract marks, diagrams or material groupings that read as intentional but are not legible text.

### A5. Framed art — insert immediately after A4

> Place framed art and wall hangings substantially within the composition and in a believable relationship to the furniture grouping below. Avoid an incidental frame sliver at the extreme edge, apparent balancing on furniture, or placement that leaves the artwork largely hidden by the insertion area. Make wall-mounted pieces read as wall-mounted. A close crop may show only part of a larger treatment, provided that part is intentional and visually useful; otherwise choose a treatment that reads locally instead of demanding a complete distant picture.

### A6. Prop relationships — insert after the printer-support paragraph

> Choose approved props for a recognizable activity or furnishing relationship, not merely to occupy empty space. Keep liquid vessels outside the principal working and insertion area rather than crowding it. Give plants and other decorative objects their own plausible approved location; do not stage them on the insertion area or as apparent accessories on top of the supplied product. Avoid arbitrary stones or paperweights, unrelated puzzles beneath equipment tables, and isolated floor objects without a clear scene purpose. Keep coat stands, drapes and other nearby furnishings visibly separate from the support rather than describing overlapping or entwined arrangements. Use ordinary furniture with a coherent supporting structure, but do not demand that every leg be visible.
>
> These are internal planning rules. In final scene prose, describe the furniture and prop relationships without naming or describing the supplied primary device or referring to a digital twin or insertion process.

This should not ban all plants, puzzles, curtains or coat stands. It bans the problematic **relationship**, not the entire object family.

### A7. Camera guidance — replace the three quoted camera paragraphs

> **Close-up:** Retain the recognizable place, support, natural light and approved nearby detail that can plausibly fit. Use one coherent local arrangement rather than an overloaded tabletop inventory. Show wall treatment only when a wall is naturally visible; a local texture, panel segment or intentional portion of artwork may be enough. Do not demand a complete room, a fully visible chair, distant furniture, all table legs or a tabletop spread that would require the camera to move.
>
> **Medium:** Preserve an ordinary local working or living area, coherent materials and subordinate furnishings. Where visible, establish how the support belongs to the room and how nearby objects relate to the activity. Keep wall treatment and artwork meaningfully in the composition without introducing competing focal points.
>
> **Wide:** Retain C-Tech’s richer room descriptions and natural depth with approved, unused furnishings. Establish a coherent furniture grouping, credible circulation and a resolved treatment for meaningful visible wall areas. Related shelving, artwork and architectural treatments may coexist without an automatic object-count failure. Do not substitute scattered decorative objects for a believable room.

**Leave unchanged:** ten-prompt output, ranking, closed catalogue, prop-family non-repetition, no faces, minimal generated text, and independent source-relevance/C-Tech scoring.

---

# B. Catalogue/validator changes

## Deterministic checks worth adding

| Check | Implementation | Enforcement |
|---|---|---|
| Primary support shape | Add an internal planning field: `supportShape = round / oval / rectangular / square / other_approved`. | Printer plans permit rectangular or square. Laptop plans have no round-table quota. |
| Room relationship | Add `supportPlacement = wall_oriented / furniture_grouped / purposeful_island / communal_freestanding`. | Check allowed values and product/environment compatibility. This validates the plan, not the image. |
| Selected wall-treatment family | Use catalogue family IDs, including architectural/material treatments. | Enforce bank non-repetition for selected treatments even though the underlying wall is exempt. |
| Populated display dependency | A selected shelf, ledge or pegboard requires at least one approved content ID, as in V6.1. | Hard validation. |
| Non-legible board treatment | A selected board requires an approved non-legible content/treatment value. | Hard validation of structured planning data. |
| Catalogue compatibility | Maintain environment and relationship suitability metadata. | Reject explicit incompatible selections, such as an educational puzzle selected as printer-floor decoration. Do not globally ban puzzles. |
| Existing invariants | Ten prompts, valid IDs, family non-repetition, approved environments, no named primary device. | Preserve existing checks. |

These fields can be internal planning metadata; they need not change the public ten-prompt schema.

## Conservative text lint

Use warnings for explicit positive phrases such as:

- “empty whiteboard,” “blank pegboard,” “empty shelving”;
- “frame barely visible at the edge”;
- “plant on top of the printer”;
- “puzzle on the floor beneath the equipment table”;
- “round equipment table” in a printer-tag scene;
- exact measurements or extended geometric construction instructions introduced by the patch.

Do not match quoted examples or negated instructions as violations. Do not use broad keywords such as `blank`, `plant`, `curtain` or `round` as standalone rejection rules.

## Requires visual inspection—not prompt validation

A text validator cannot determine:

- whether table legs are missing rather than occluded;
- whether perspective or furniture geometry is warped;
- whether artwork is substantially in frame;
- whether a plant actually landed on the device;
- whether a wall gap is excessive in the rendered room;
- whether a prop crowds the working area;
- whether a chair is usable;
- whether a freestanding station actually reads as purposeful.

## Catalogue additions

**No new wall families are required.** The existing catalogue already supports ten distinct, environment-appropriate treatments. Adding near-synonymous wall IDs would weaken semantic non-repetition.

Required catalogue work is narrower:

1. Add round/oval options to suitable **primary-support templates**, not as extra props.
2. Add relationship metadata to existing props: suitable surface/location, activity association, and whether non-legible content is required.
3. Canonicalize overlapping wall families so “slatted timber wall” and “wood-slat paneling” cannot evade repetition checks.

---

# C. Judge V4 design

## Smallest coherent change: keep five components

**Do not add a sixth aesthetic room-composition score.**

Extend the existing components as follows:

| Existing component | V4 extension |
|---|---|
| Support/scenario | Include support structure and whether the complete station belongs plausibly in the room. |
| Access/usability | Preserve functional access checks; explicitly downgrade movable-chair differences. |
| Orientation/alignment | Include meaningful product/support misalignment and visible room-plane conflicts. |
| Scale/perspective | Include rigid furniture geometry and perspective coherence. |
| Contact/integration | Include prop/device interference, impossible furniture intersections and review-only local prop artifacts. |

The judge should first inspect the **device–support–room chain**, then nearby prop relationships. A correctly placed printer cannot cancel a deformed table.

## Exact issue codes

Retain existing V3 codes for other defects. Add or normalize these codes:

| Code | Definition | Normal severity |
|---|---|---|
| `NP_ROOM_ANCHOR` | The support/station has an implausible relationship to the visible room: unexplained domestic-room isolation, an excessive purposeless wall gap, or an incoherent furniture grouping. | Review if questionable; fail when clearly established. |
| `NP_FURNITURE_GEOMETRY` | Visible rigid furniture has incompatible shape or construction: warped tabletop, impossible intersections, structurally inconsistent legs, or physically implausible adjoining furniture. | Fail for clear structural defects. |
| `NP_SUPPORT_MISSING` | A necessary supporting member is demonstrably absent, rather than cropped, occluded or replaced by a plausible pedestal/cantilever design. | Fail. |
| `NP_ROOM_PERSPECTIVE` | The support, wall and related furniture cannot be explained by a coherent room arrangement and plausible viewing geometry. | Review if ambiguous; fail if clear. |
| `NP_PRODUCT_ALIGNMENT` | The product’s placement or orientation relative to its support is materially implausible or functionally wrong. Ordinary intentional rotation is excluded. | Review or fail according to consequence. |
| `NP_PROP_CONFLICT` | A prop visibly intrudes onto the product, occupies an implausible product-contact position, blocks use, or creates an impossible intersection. | Review for localized interference; fail for substantial interference or impossible contact. |
| `NP_LIQUID_CROWDING` | A liquid vessel visibly crowds the immediate working area or makes normal use precarious. Proximity alone is insufficient. | Review; fail only with a separate serious access/contact defect. |
| `NP_CHAIR_RELATION` | A visible chair’s orientation or position affects the usability of the station. | Warning for ordinary displacement; review for substantial inconvenience; fail only for actual unusability. |
| `NP_PROP_ARTIFACT` | An unmistakably malformed incidental prop within the station, such as distorted eyeglasses. | Review maximum; never a placement fail by itself. |
| `OBS_CROP_UNKNOWN` | A relationship cannot be assessed because relevant evidence is outside the crop or occluded. | Neutral observation; no deduction. |

Separate, unscored advisories:

- `STYLE_WALL_UNRESOLVED`
- `STYLE_ART_FRAMING`
- `STYLE_PROP_RELEVANCE`
- `STYLE_SPARSE_STAGING`

`NP_PROP_ARTIFACT` is a narrow physical-integration extension to capture the eyeglasses feedback. It must not become a general aesthetic-quality detector.

## Evidence and severity rules

Each scored issue should contain:

```text
code
component
severity: warning | review | fail
confidence: medium | high
visible_evidence
affected_objects
```

A fail requires **high-confidence visible evidence**. Low-confidence hypotheses become observations, not scored defects.

Specific rules:

- A chair that can be pulled in or turned normally is not a failed station.
- A missing chair in a close-up is not evidence of unusability.
- A missing table leg is serious only when the image exposes where required support should exist and no plausible alternative support explains the structure.
- Mismatched legs fail when they establish impossible construction—not simply because the furniture is asymmetrical.
- A printer station may stand away from a wall if a credible production island or access arrangement explains it.
- Conversely, “the printer is correctly on the table” does not excuse a plainly marooned or malformed table.
- Random décor does not independently establish a placement failure.
- Ordinary printer yaw on a tabletop is not automatically misalignment.

## Crop/unobservable behavior

Judge the actual image, not what the camera tag usually shows.

- Never require a chair, wall, complete table or every leg to be visible.
- Do not penalize cropped evidence.
- A close-up **can** establish a bad room relationship if it shows enough relevant context.
- A wide tag does not justify inventing missing evidence.
- Prompt intent is context, not proof: “wall-oriented table” in the prompt does not override a visibly freestanding rendered table.

## Rigid-edge perspective

Replace any “parallel edges must look parallel” heuristic.

Use this instruction:

> Evaluate rigid edges as parts of coherent planes and objects. Parallel world-space edges may converge in the image. Do not flag convergence itself. Look for incompatible convergence among comparable straight edges, unexplained bends within a rigid edge, contradictory tabletop thickness, impossible corner connections, or support members that cannot attach to the visible structure. Account for ordinary lens distortion and do not assume adjacent furniture shares an orientation unless the image establishes that relationship.

For D4, the target is the human’s reported **deformation**, not the literal fact that two image-space edges are nonparallel.

For D6, the wall-touching cabinet is a useful reference only where visible contact establishes the relevant room plane. A separate rotated table need not share all of the cabinet’s vanishing directions.

## Bare walls and sparse staging

These must have **zero placement-score weight**.

- A bare wall can yield a placement pass plus `STYLE_WALL_UNRESOLVED`.
- A sparse but credible workspace passes.
- An elaborate room with a missing table leg fails.
- “Isolated” becomes `NP_ROOM_ANCHOR` only when it describes a defective spatial arrangement—not merely insufficient decoration.

## Deterministic scoring

Preserve the five-component architecture and existing component weights. Replace cumulative informal deductions with a severity normalization at the application boundary:

| Highest supported severity within a component | Component score |
|---|---:|
| No issue | 100 |
| Warning | 95 |
| Review | 75 |
| Fail | 40 |
| Entirely unobservable | Excluded from aggregation |

Then:

```text
baseScore = weighted mean of observable component scores

if any supported fail issue:
    finalScore = min(baseScore, 59)
    verdict = fail
else if any supported review issue:
    finalScore = min(baseScore, 79)
    verdict = review
else:
    finalScore = baseScore
    verdict = pass
```

Use 0–59 / 60–79 / 80–100 as the application bands.

Important implementation details:

- One physical defect receives one primary code/component; do not multiply deductions.
- Style advisories and `OBS_CROP_UNKNOWN` never enter aggregation.
- Several chair warnings cannot accumulate into failure.
- One missing structural support cannot be averaged into a pass.
- If nothing is observable, return a null score and an administrative insufficient-evidence state; do not fabricate a placement failure.
- This score is a **triage index**, not a probability of correctness.

---

# D. Calibration table

These are expected verdicts from the supplied annotations, not claims of a fresh image inspection. Clear human-reported structural defects are accepted as evidence; unspecified geometry is not invented.

## Cashmere laptop FrontCloseUp examples

| Case | Expected V4 | Main code(s) | Basis |
|---|---|---|---|
| **L1** Office folder + frosted partition | **pass** | `STYLE_WALL_UNRESOLVED`, optionally `STYLE_SPARSE_STAGING` | More background detail is a creative request, not a placement defect. |
| **L2** Meeting table + water carafe + art | **review** | `NP_LIQUID_CROWDING` | Preserve the good composition; review the reported crowding beside the working area. Mere presence of a carafe would not suffice. |
| **L3** Painting studio | **pass** | — | Human reports a good output. |
| **L4** Studio swatches/model/flat-file | **pass** | `STYLE_ART_FRAMING` | Bring the picture into frame; no placement failure is established. |
| **L5** Home desk/glasses/curtains | **pass** | `STYLE_ART_FRAMING` | Same distinction: artwork composition, not station failure. |
| **L6** Document box/stone paperweight/slats | **pass** | `STYLE_PROP_RELEVANCE`, `STYLE_WALL_UNRESOLVED` | The rock may fail creative approval. No obstruction, unstable contact or impossible placement is reported. |
| **L7** Living-room end table/key dish/sofa | **fail** | `NP_ROOM_ANCHOR` | Human explicitly identifies a table arrangement that does not replicate a real-life scenario. |
| **L8** Education table/globe/display | **pass** | — | Correct V3’s false fail; no placement defect is supplied. |
| **L9** Gaming coin/light panels | **pass** | `STYLE_PROP_RELEVANCE`, `STYLE_WALL_UNRESOLVED` | Better gaming props and background depth are style requirements. |
| **L10** Counting blocks/empty whiteboard | **pass** | `STYLE_PROP_RELEVANCE`, `STYLE_WALL_UNRESOLVED` | Writer violation and creative issue; a blank board does not make the table unusable. |

## Magic printer FrontWide examples

| Case | Expected V4 | Main code(s) | Basis |
|---|---|---|---|
| **P1** Placement/framing okay; insufficient wall treatment | **pass** | `STYLE_WALL_UNRESOLVED` | Correct V3’s false fail. |
| **P2** Plant on product; warped coat-rack interaction | **fail** | `NP_PROP_CONFLICT`, `NP_FURNITURE_GEOMETRY`; style advisory | Physical relationship/geometry defects—not the bare wall—drive failure. |
| **P3** Unrealistic right-side furniture | **fail** | `NP_FURNITURE_GEOMETRY`; style advisory | Accept the reported unrealistic furniture as the defect. The actual judge must locate and describe it rather than invent a particular missing leg or edge. |
| **P4** Okay; more wall detail requested | **pass** | `STYLE_WALL_UNRESOLVED` | Style-only request. |
| **P5** Okay; more wall detail requested | **pass** | `STYLE_WALL_UNRESOLVED` | Style-only request. |
| **P6** Table legs do not match | **fail** | `NP_FURNITURE_GEOMETRY`; style advisory | Reported construction defect is decisive. |
| **P7** Okay; more wall detail requested | **pass** | `STYLE_WALL_UNRESOLVED` | Style-only request. |
| **P8** Table warps around drapes | **fail** | `NP_FURNITURE_GEOMETRY`; style advisory | Correct V3’s false pass on an impossible rigid/soft-object interaction. |
| **P9** Product isolated; random props/wall choices | **review** | `NP_ROOM_ANCHOR` at review severity; `STYLE_PROP_RELEVANCE`, `STYLE_WALL_UNRESOLVED` | Inspect whether the reported isolation is an incoherent station arrangement. Random styling and sparse staging alone cannot justify a natural-placement fail. |
| **P10** Okay; more wall detail requested | **pass** | `STYLE_WALL_UNRESOLVED` | Style-only request. |

**P9 is the material scope exception.** The human’s overall creative verdict is fail. The annotation does not establish enough physical/layout evidence for an unconditional natural-placement fail. If the image shows a plainly marooned station, promote `NP_ROOM_ANCHOR` to fail; if it is merely sparse, remove the placement issue.

## Additional disagreements

The two paired laptop bullets are expanded so every annotated scene is represented.

| Case | Expected V4 | Main code(s) | Basis |
|---|---|---|---|
| **D1a** Laptop medium, slightly displaced chair | **pass** | `NP_CHAIR_RELATION` warning | Ordinary chair movement, with no actual unusability reported. |
| **D1b** Second laptop medium, slightly displaced chair | **pass** | `NP_CHAIR_RELATION` warning | Same rule. A visibly substantial inconvenience could warrant review, not automatic fail. |
| **D2** Laptop close-up, no visible chair | **pass** | `OBS_CROP_UNKNOWN` | The chair may be outside the crop. No deduction. |
| **D3a** Laptop chair-alignment false fail | **pass** | `NP_CHAIR_RELATION` warning at most | Human says pass; table angle alone is not failure. |
| **D3b** Second laptop chair-alignment false fail | **pass** | `NP_CHAIR_RELATION` warning at most | Same rule. |
| **D4** Printer wide, deformed table and marooned home placement | **fail** | `NP_FURNITURE_GEOMETRY`, `NP_ROOM_ANCHOR` | Correct device/table contact cannot rescue either defect. Do not use ordinary vanishing-point convergence as the geometry evidence. |
| **D5** Printer close-up, same marooned rectangular-table problem | **fail** | `NP_ROOM_ANCHOR` | Use the visible contextual evidence identified by the human—not the close-up tag or table shape alone. |
| **D6** Printer close-up, incoherent wall/table/cabinet perspective | **fail** | `NP_ROOM_PERSPECTIVE` | The visible wall-touching cabinet helps establish the reported room-plane conflict. |
| **D7** Printer medium, missing table legs | **fail** | `NP_SUPPORT_MISSING` | A confirmed absent necessary support is structural, not a styling issue. |
| **D8** Printer medium, excessive wall gap | **fail** | `NP_ROOM_ANCHOR` | Human explicitly says the gap exceeds a plausible service-clearance explanation. |
| **D9** Laptop medium, missing leg plus chair complaint | **fail** | `NP_SUPPORT_MISSING`; chair warning at most | Report the missing support as decisive, not the chair. |
| **D10** Printer close-up, slanted product and floor puzzle | **fail** | `NP_PRODUCT_ALIGNMENT`; `STYLE_PROP_RELEVANCE` | The reported material alignment defect drives failure. A puzzle alone does not. If the image shows only harmless yaw, that would not support this fail label. |
| **D11** Printer close-up, malformed glasses; possibly long table | **review** | `NP_PROP_ARTIFACT` | Malformed incidental geometry warrants review only. “May be too long” is not a confirmed room-layout defect. |
| **D12** Printer close-up, strange table placement and floor puzzle | **fail** | `NP_ROOM_ANCHOR`; `STYLE_PROP_RELEVANCE` | The room placement is decisive; the puzzle is a separate creative-relevance issue. |

---

# E. Risks and ablations

## Highest-risk prompt changes

| Risk | Likely regression | Control |
|---|---|---|
| Requiring wall art everywhere | Close-ups pull back; crowded backgrounds; repeated frames | Require a resolved **visible wall area**, not a picture or a complete wall. Allow local texture/panel treatments. |
| Making artwork fully visible | Camera/crop conflict | Require substantial, intentional visibility—not the entire frame. |
| Requiring visible legs or chairs | Wider-than-requested framing | Explicitly prohibit such completeness requirements. |
| Enforcing round-table quotas | Implausible gaming/studio scenes; reduced diversity | Shape is planned contextually, without a per-bank quota. |
| Making all tables wall-aligned | Loss of credible café, meeting and production-island scenes | Product-specific defaults plus explicit purposeful exceptions. |
| Adding long spatial instructions | Brittle prose and more generation artifacts | Use one natural relationship clause; no measurements or vanishing-point instructions in scene text. |
| Banning curtains/plants/coat stands | Unnecessary catalogue contraction | Correct their placement relationships; leave geometry to visual detection. |
| Treating “random” as a fail code | Judge becomes an aesthetic taste classifier | Keep relevance advisories separate from physical placement. |

## Small text pilot

Generate **six paired banks**, V6.1 versus V6.2: **120 prompts total**.

Use:

1. Cashmere laptop FrontCloseUp with the reviewed office/home/studio mix.
2. Laptop medium with Home and neighborhood café settings.
3. Laptop wide with café/social/communal opportunities.
4. Printer FrontCloseUp.
5. Printer medium.
6. Magic printer FrontWide.

Hold briefs, source messages and tags constant.

Check:

- all existing deterministic constraints still pass;
- round tables appear naturally somewhere in the café-rich pilot, without becoming universal;
- printer supports remain equipment-oriented and rectangular/square;
- meaningful visible walls have approved treatments;
- close-ups do not demand full rooms, chairs, legs or distant pictures;
- no new product naming, numerical geometry or repeated phrase families;
- source relevance and C-Tech scores remain independent.

Have a C-Tech reviewer blind-rank paired prompts for natural prose, plausible staging and crop fit.

### Focused text ablations

On the laptop close-up and printer wide briefs, compare full V6.2 against:

- **minus support-shape/room-placement patch**;
- **minus wall/art-placement patch**;
- **minus prop-relationship patch**.

This identifies whether wall improvements are coming at the cost of close-up fit, and whether room coherence improves independently of decorative richness.

## Held-out judge validation before a full image run

Use the 34 annotated scenes above for calibration, then freeze the prompt and scoring logic.

Validate on approximately **60 separate existing images**, including:

- valid displaced or cropped chairs;
- plausible pedestal/cantilever tables;
- normal perspective convergence;
- legitimate freestanding islands;
- genuinely missing supports and warped furniture;
- excessive wall gaps;
- bare-but-plausible rooms;
- richly decorated rooms with severe structural defects;
- minor malformed props.

Have reviewers label **natural placement and creative quality separately**. Resolve P9-like ambiguity before measuring agreement.

### Release gates

1. **Calibration cases:** all clearly annotated structural failures are detected; no failures caused solely by a cropped chair, modest chair displacement, bare walls or unattractive prop choice.
2. **Critical corrections:** L8/P1 pass; P2/P3/P8 fail; D4–D10 and D12 receive the specified decisive physical/layout reason; D11 remains review.
3. **Held-out improvement:** V4 must improve placement-verdict agreement over V3 while reducing both chair-related false failures and structural false passes.
4. **No style leakage:** changing wall richness alone must not change a placement verdict.
5. **No perspective shortcut:** normal convergence and plausible alternative support designs must not trigger structural failure.

Report the paired confusion matrix, severe-defect recall, valid-scene false-fail rate, and issue-code accuracy—not only average score. This makes V4’s improvement testable rather than an increase in instruction length.
