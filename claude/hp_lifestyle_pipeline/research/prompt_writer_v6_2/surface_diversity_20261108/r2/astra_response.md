## Finding and scope

The frozen inputs requested round tables in **11/80 laptop prompts (13.75%)**, including **8/10 Café prompts (80%)**. That leaves **3/70 non-Café laptop prompts (4.29%)** requesting round tables.

Those are **prompt counts, not observed image counts**. I cannot establish whether the generated images depicted those tables or why a curved edge was absent.

The revision should therefore address both **explicit primary-surface wording** and **distribution beyond Café**, while removing the printer table-only restriction from both authoring and validation.

The reproduction comprises **16 independently generated banks × 10 candidates = 160 prompts**: eight laptop banks and eight printer banks. The corresponding 160 images must be generated downstream; none are generated or inspected here.

---

# 1. Exact replacement system-prompt passages

## A. Replace the complete “Ten scenes, planned together” section

> ## Ten scenes, planned together
>
> Produce exactly ten distinct prompts. Plan the complete bank together before writing paragraphs: choose plausible settings, assign the primary supporting furniture, and allocate non-overlapping approved prop families. This is internal planning; return concise output fields, not a planning transcript. Each bank is independent; prop and phrase non-repetition apply within that bank, not across separate banks.
>
> Use at least four permitted environments across the ten candidates, selected from Home, Office, Education, Gaming, Café, and Creative Studio. Respect the device-family environment rules below. Café and Creative Studio are separate environments, even when people work there. Do not invent source support, introduce unapproved furnishings, or change the camera to meet diversity targets. If the supplied inputs make a requirement infeasible, identify the specific conflict in limitations; do not silently waive it.
>
> Useful compatible evidence from either source document contributes to relevance, with neither document having higher authority. An unsupported but plausible scene may be a creative departure with a lower source score. The top six may favor the strongest source-supported environments, while the complete bank supplies broader choices. Never turn a gaming workspace into an office paperwork scene or a café into a document-processing counter merely to gain relevance points.
>
> Vary ordinary subsettings, activities, furniture arrangements, primary support forms, tabletop outlines, materials, and compatible light. These are different dimensions: wood and stone are materials; round, oval, and rectangular describe the supporting top’s outline; cabinet, credenza, and table describe furniture forms. Changing a material or renaming an object does not by itself create a different furniture family.
>
> Preserve meaningful differences among the strongest source-supported candidates as well as lower-ranked alternatives. Do not invent unusual occupations, contrived furniture names, or new device uses to make the bank different. Support novelty earns no relevance bonus. Score the final visible setting and use against the existing source rubric after all revisions.

## B. Replace only the first paragraph under “Plan phrase diversity across the complete bank”

Retain the existing collision-family list and subsequent phrase-diversity rules.

> Before drafting, allocate distinct subsettings, activities, arrangements, light descriptions, wall compositions, and atmosphere where the fixed camera and approved catalogue permit. Do not write ten prompts independently and then swap nouns. Repeated environments must remain visually and linguistically distinct without forcing every primary support to be unique.
>
> For this experiment, each laptop bank must contain at least two explicitly round or circular primary tables. Every laptop Café candidate must use a round or circular table as its main work surface. When the sources support a plausible office meeting, study, education, or home-table setting, include at least one round-table candidate in such a source-supported non-Café setting rather than placing all round tables in unsupported Café departures. Do not force a round table into an implausible use. Retain useful alternatives such as desks, oval shared tables, and studio worktables.
>
> For each printer bank, use at least three genuinely different primary furniture families and at least five non-table primary supports. The normalized families are table/worktable, freestanding cabinet, credenza/sideboard, fitted base cabinetry with countertop, and an explicitly approved substantial equipment cart. Different names, materials, finishes, or sizes within one family do not create additional families. A utility table, output table, resource table, and production table all remain table/worktable.
>
> These are bank-level experimental support targets, not object budgets or camera instructions. Do not expose a full tabletop, cabinet front, base, legs, or distant room merely to prove compliance. State the supporting furniture naturally and let the fixed view determine what can appear.
>
> Necessary furniture names and geometry words, including “table,” “cabinet,” “round,” and “curved rim,” may recur. Required safety relationships may also recur in concise ordinary language. This does not permit repeating a distinctive opening, lighting formula, arrangement, or atmosphere through paraphrase.

**Rationale:** Two round tables per bank is a useful, moderate experimental floor. Requiring all Café candidates to be round is an intentional experimental preference—not a claim that cafés universally have round tables. The non-Café condition addresses the more significant frozen-input gap.

## C. Replace the primary-support exemption paragraph

Replace the paragraph beginning “The primary supporting desk/table and fixed architecture…”

> The single primary supporting furniture assembly is identified in primary_support and authorized by the Natural device setting and support section. Its supporting top and integral base are exempt from catalogue prop selection and prop non-repetition. This exemption applies equally to an allowed desk, table, worktable, cabinet, credenza, fitted base-cabinetry assembly, or eligible equipment cart. Record this furniture in primary_support rather than prop_ids. Any catalogue authorization required for an equipment cart is recorded in primary_support.catalogue_id.
>
> The exemption is role-specific, not a blanket exemption for a furniture type. A separate background cabinet, sideboard, table, cart, or other furnishing must have an environment-approved catalogue ID, appear in prop_ids and prop_mentions, and consume its catalogue repetition groups. Calling extra furniture “equipment storage,” giving it a clear top, or placing it beside the primary support does not exempt it. A primary cabinet does not consume the background-cabinet repetition group; separately selected background cabinets do.
>
> The primary-support exemption covers only the supporting furniture and its integral construction. It does not cover chairs, lamps, curtains, nearby furniture, objects placed on top, visible stored contents, or decorative objects. Declare and validate those through the existing prop inventory. Do not use a fitted cabinetry run to introduce additional activity areas or unlisted furnishings.
>
> Bare fixed architecture—walls, floors, and windows—may recur. Selected wall treatments, decorative panels, frames, shelves, and their visible contents remain subject to their existing catalogue and non-repetition rules.

**Rationale:** Cabinet supports become an explicit authorized role, while additional cabinets remain ordinary catalogue-managed props. This closes the background-furniture loophole.

## D. Replace the complete “Natural device setting and support” section

> ## Natural device setting and support
>
> Infer the device family only from the trusted camera tag. Never name or describe the primary device, or introduce a generic substitute for it, in scene text. Name the supporting furniture and surrounding place normally.
>
> Every candidate must identify its actual main supporting furniture in primary_support. The text_evidence must be an exact, case-sensitive quotation from scene text that names that furniture and includes any claimed supporting-top shape. Select the furniture that carries the main work surface, not a nearby prop or background furnishing. Write the primary-support phrase in the opening sentence so its role is clear. Material, furniture form, and supporting-top outline are separate facts; do not infer one from another.
>
> Laptop-tag scenes may use any plausible permitted environment and an ordinary desk, meeting table, study table, café table, home table, drafting table, or studio worktable. Use a credible working surface with usable space and an ordinary user position. Round and oval tables can sit naturally in meeting areas, cafés, study settings, and homes. Rectangular desks and worktables normally relate to a wall, room axis, banquette, or clear working position; do not maroon a small table at an arbitrary angle merely to add variety.
>
> A round-table candidate must explicitly name a “round” or “circular” primary table in scene text. A round tray, curved chair, round object, background table, or rounded corner on a rectangular surface does not qualify. Where compatible with the trusted view, briefly describe a curved tabletop rim or edge. A close-up may reveal only an arc: never require the complete circumference, supporting legs, a central pedestal, or a wider frame. A circular top seen obliquely is still circular furniture; do not relabel it oval merely because of perspective. Shape requirements apply to the main supporting top, not to its material.
>
> Printer-tag scenes normally use only Office, a Home workspace, Education, or Creative Studio. Café or Gaming is allowed only when either source document explicitly supports that setting. Cite the supporting evidence and use a credible operational area, never customer or leisure furniture.
>
> The authorized primary printer supports are a substantial dedicated table or worktable; a dedicated freestanding cabinet with a broad usable top; a low substantial credenza or sideboard; and fitted base cabinetry with a substantial countertop in a workspace. A freestanding cabinet is a distinct standalone storage unit; a credenza or sideboard is a longer, low horizontal storage furnishing; fitted base cabinetry is integrated into a cabinetry run. Do not claim different families when the text merely renames the same furniture form.
>
> An equipment cart is eligible only when the trusted catalogue explicitly permits an environment-appropriate cart suitable for substantial equipment. Record that catalogue entry in primary_support.catalogue_id. Describe a stable, adequately sized cart in a stationary working position; an ordinary serving trolley, narrow rolling stand, or fragile display cart does not qualify. Otherwise do not select a cart.
>
> Every primary printer support must be stable, sufficiently broad and deep for the trusted product context, at a usable working height, and placed where standing access is believable. Relate it naturally to a wall, storage run, or room layout while allowing ordinary rear clearance. Keep the room-facing approach unobstructed, but do not require the camera to show the floor or the entire approach. Do not require cabinet doors, a complete base, legs, or the whole countertop to be visible. Avoid exact dimensions and unsupported load-capacity claims.
>
> Keep personal, leisure, learning, and creative work arrangements off the primary printer support. This includes notebooks, reading glasses, drinkware, food, sewing or craft tools, palettes, brushes, swatches, learning manipulatives, games, active paperwork, and seating aligned as a personal workstation. An approved letter tray, plain paper stack, unlabelled document box, or comparable neutral item may sit safely to one side if it leaves the support usable. Other approved activity props belong on a clearly separate background furnishing or activity area, with every required catalogue ID declared.
>
> Never use an occupied desk or personal workstation as the primary printer support. Never place it on a coffee table, end table, dining table, kitchen island, sofa-side surface, customer café table, bar counter, pastry table, gaming desk, lounge table, display shelf, small display plinth, narrow drafting ledge, or fragile stand. A fitted workspace countertop is not permission to use a kitchen island or bar.
>
> Do not impose a general ban on curved furniture or rounded supporting tops because the product has straight edges. Judge printer supports by their furniture role, stability, usable area, placement, and access. Other round furniture may appear when approved and appropriate.
>
> Before returning a bank, check that every primary_support record agrees with the scene, the support-family and round-table targets are met, and all additional furniture remains correctly inventoried. A support’s novelty or unusual shape never increases source relevance.

---

# 2. Contradictory lines and validation assumptions to remove

These are necessary consistency edits, not optional softening.

| Location | Exact change |
|---|---|
| First sentence under **Approved props and global non-repetition** | Replace with: **“Except for the authorized primary supporting furniture and bare fixed architecture described below, every requested movable object and background furnishing must be covered by an approved catalogue entry for that prompt’s environment and declared in prop_ids.”** |
| Opening sentence of the inventory paragraph | Replace “Use prop_ids to describe exactly what the text requests.” with: **“Use prop_ids and prop_mentions to inventory exactly the requested catalogue-managed props, selected wall treatments, additional furniture, and visible contents; use primary_support for the authorized main supporting furniture.”** |
| Same inventory paragraph | Replace “or omit visible objects from the inventory” with **“or omit requested catalogue-managed objects from the inventory.”** |
| **Device and color boundary** furniture-naming paragraph | Replace with: **“Use ordinary furniture names such as ‘desk,’ ‘table,’ ‘worktable,’ ‘cabinet,’ ‘credenza,’ ‘countertop,’ or ‘work surface,’ as appropriate to the actual support. Never use ‘desktop’ as a standalone noun because it can be interpreted as computing hardware.”** |
| Final bank checklist | Replace “no recycled repetition groups, including furnishings and named contents” with **“no recycled non-exempt catalogue repetition groups, including additional furnishings and named contents; primary_support agrees with the text and meets the bank support targets.”** |

The section replacements above also delete:

- “For printer banks, keep the equipment supports sturdy and rectilinear.”
- The printer **dedicated table or worktable** requirement.
- The environment-specific whitelist of narrowly named printer tables.
- The instruction to name “only the credible table.”
- Any assumption that a cabinet can appear only as background furniture.

### Integration gate

The existing table-only recognizer must be **replaced**, not retained alongside the new rules. Otherwise valid cabinet scenes will still fail.

This requires an explicitly approved writer-schema/validator revision. It does **not** authorize changing downstream system prompts, the image endpoint, model, camera tags, or other request settings. If an immutable downstream check still requires tables, report the incompatibility and block deployment rather than silently altering it.

---

# 3. Minimum schema and bank acceptance policy

## Minimal response-schema addition

Add one `primary_support` object per candidate. Keep all existing source evidence, scores, prop inventory, explanations, and debug fields.

| Field | Allowed content |
|---|---|
| `kind` | `desk`, `table`, `worktable`, `freestanding_cabinet`, `credenza_sideboard`, `fitted_base_cabinetry`, `equipment_cart` |
| `shape` | `round`, `oval`, `rectangular`, `other`, `unspecified` |
| `text_evidence` | Exact scene-text quotation identifying the primary supporting furniture and any asserted top shape |
| `catalogue_id` | Required for an equipment cart; otherwise null |

`shape` describes the **supporting top’s outline**, not the furniture base or material. Use `unspecified` when the text does not establish an outline.

For printer diversity counting:

- `table` and `worktable` map to **one family**.
- Each permitted cabinet form maps to its stated family.
- Material and wording changes do not create families.
- `desk` is invalid as a printer primary support.

### Important validation boundary

Enums, exact quotations, counts, catalogue permissions, and score arithmetic are deterministically checkable. They do not prove physical plausibility or truthful furniture-role assignment. The writer must check those semantic conditions against the final prose; acceptance fixtures should explicitly test them. Do not treat substring matching as proof that a background table is the primary support.

## Acceptance gates

### A. Existing hard requirements remain hard

Accept a bank only when it has:

- Exactly ten candidates and valid JSON.
- Permitted environments and the retained environment-diversity requirement.
- Unchanged fixed camera guidance.
- No primary-device descriptions, placeholders, faces, or legible text.
- Correct environment-specific prop approvals, mentions, and repetition groups.
- No repeated distinctive phrase or lighting template.
- Natural C-Tech prose and camera-appropriate furnishing density.
- Valid source quotations and independently supported component scores.
- Independent C-Tech scoring and correctly labelled creative departures.

No support-diversity requirement overrides these gates.

### B. Experimental support gates

**Laptop bank**

- At least **two** qualifying round/circular primary tables.
- **Every Café candidate** has a round/circular primary table.
- At least one source-supported non-Café round-table candidate when such a setting is plausible and permitted.
- No credit for background tables, round props, or rounded rectangular corners.

**Printer bank**

- At least **three normalized furniture families**.
- At least **five non-table supports**.
- Every support passes placement, scale, usability, and standing-access checks.
- Additional background cabinets retain their normal prop IDs and repetition groups.

These thresholds are **researcher-selected acceptance gates for this experiment**, not attributed to Hooman as numeric requirements. They are reasonable starting targets: two round laptop tables creates a measurable increase without making every setting circular; five non-table printer supports directly breaks the existing table-only pattern.

If all banks pass, the 80 laptop prompts contain at least **16 round-table candidates**, and the 80 printer prompts contain at least **40 non-table supports**.

### C. Source ranking stays unchanged

Compute relevance exactly as before:

- Take the higher independently supported value from the two documents for each component.
- Sum those component maxima.
- Sort descending by source relevance, then C-Tech score.
- Do not reserve high ranks for novel supports.

A round office table should enter the source-supported candidate pool where appropriate; it should not receive a ranking bonus. Surface shape is not a material score, and novelty is not evidence. Creative departures remain labelled and below 60 under the existing rule.

### D. One complete-bank repair, maximum

For each of the 16 banks:

1. Generate ten candidates together from that bank’s frozen inputs and fixed tag.
2. Validate the complete bank.
3. If it fails, provide the violations for **one complete-bank repair**.
4. Revalidate all ten repaired candidates, including prop collisions, evidence, scores, and ranking.
5. If it still fails, reject the bank and report the unmet gates.

Do not manually rewrite individual scenes, splice candidates from different attempts, or add a second repair. Only accepted banks proceed to downstream image generation. A run with rejected banks is not reported as a completed 160-prompt reproduction.

## Essential acceptance fixtures

| Fixture | Expected result |
|---|---|
| Rectangular main desk; round café table in background | Does not count as a round primary support |
| “Round wooden table” with only its curved rim feasible in a close-up | Counts; no full-circle visibility requirement |
| Circular tray on rectangular table | Does not count |
| Utility table, output table, resource table | One printer support family |
| Cabinet primary supports recur across several candidates | Allowed |
| Extra background cabinets recur across separate candidates in the same bank | Repetition failure |
| Cabinet primary support plus visible undeclared contents | Inventory failure |
| Unsupported Café changed from rectangular to round | No source-score increase |
| Equally valid evidence supplied by either document | Same component credit |
| Printer cabinet close-up without visible doors or floor | May pass; absence of those features is not a failure |
| Metadata says cabinet but prose names a table | Support-consistency failure |
| Second validation still fails after full-bank repair | Reject; no further repair or image submission |

---

# 4. Four compact prose examples

These illustrate scene language, not catalogue authorization. The optional furnishings below use forms found in the frozen examples; actual generation must still resolve their environment-approved IDs and repetition groups. The primary cabinet and credenza roles are authorized by the replacement section.

### Laptop — Café, close-up

> A neighborhood café has a round wooden table with a gently curved rim and room for a short work pause. An upholstered banquette sits behind it, with small reflections moving across the glazed tile wall.

### Laptop — Office, medium

> An office meeting area centers on a circular table with a smooth curved edge, ready for a discussion. A whiteboard with sparse distant non-legible geometric marks hangs beside a wall-mounted planter, and cool morning light settles across the table.

### Printer — cabinet, close-up

> A home workspace has a dedicated freestanding cabinet with a broad oak top and an unobstructed approach from the room. A ceramic relief of geometric shapes hangs to one side in shaded afternoon light.

### Printer — credenza, wide

> An office has a low, substantial credenza along one wall, its deep flat top reserved for equipment and the aisle in front kept clear. A freestanding felt screen separates the area from a background storage cabinet, with framed geometric artwork mounted beside the cabinet. A ribbed-glass partition and even ceiling light give the room a practical, settled character.

In the last example, the **credenza is the exempt primary support**; the **background storage cabinet remains a declared, repetition-counted furnishing**.