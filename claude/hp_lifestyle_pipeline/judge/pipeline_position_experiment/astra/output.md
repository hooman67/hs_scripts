## Recommendation

Run a **prompt-only, translation-only experiment**. Keep Stage A and the guide renderer producing the original baseline layout. Change its authority from **absolute frame coordinates** to **a reference layout whose product and support relationship may undergo one common 2D translation**.

**Keep scale fixed.** Translation does not require resizing. Allowing scale changes would introduce a second variable, weaken downstream compatibility, and make it harder to attribute improvements to translation.

The permitted operation is:

> Move the product and its planned support relationship by the same image-plane displacement, without rotation, resizing, reflection, perspective change, or independent movement of the support relative to the product.

GPT Image should retain the baseline location unless moving it improves support geometry, realistic use/access, furniture alignment, or composition. It must construct the surrounding scene consistently with the translated layout—not retain an incompatible room perspective.

This is a coherent prompt-only experiment, but **not a guarantee of pixel-exact preservation**: a maskless generative edit can still redraw the product. Also, successful translation does not establish downstream compatibility if the downstream paste remains hard-coded to the original coordinates.

The wording below is based on the supplied excerpts; it is not an independent inspection of the repository or deployed wrapper.

---

## 1. Exact prompt-language changes

Keep all unrelated instructions, schema fields, word limits, styling, blue requirements, and user-request handling unchanged.

### Shared translation rule

Use this exact block in the Stage-A system instructions, Stage-B priority instructions, and final GPT Image prompt. Repetition here makes the allowed operation explicit at each decision boundary.

```text
TRANSLATION-ONLY EXCEPTION
The guide gives the baseline product location and support layout. Keep that
location unless one rigid 2D translation improves realistic product use,
access, support-surface geometry, furniture alignment or composition.
Do not move the product merely to center it or make it more prominent.

Only a common image-plane x-y translation of the product and its planned
support relationship is allowed. Keep product pixel width and height
unchanged. Preserve the exact original yaw, pitch, roll, viewing angle,
visible faces, camera-facing surfaces, perspective and foreshortening,
silhouette, aspect proportions, open/closed state and all product details.
Do not rotate, mirror, resize, shear, warp, reproject, redraw or activate
the product. Do not zoom or change the product's camera viewpoint.

If translated, shift the planned support/contact geometry by the same
displacement: preserve support-edge directions, the user-facing edge,
product-to-edge distances and tabletop extents relative to the product.
Do not move the product independently of its support relationship.
Construct the surrounding furniture and room with perspective consistent
with this translated reference geometry; do not retain incompatible
vanishing geometry anchored to the original frame location.

Keep the entire product inside the frame and fully visible, with plausible
weight-bearing contact and a corresponding contact shadow. No prop,
furniture edge or foreground object may occlude the product. If no feasible
translation meets all these constraints, retain the baseline location.
```

“Preserve silhouette” means preserve its shape **after accounting for translation**, not preserve the original silhouette’s frame coordinates.

### `hp3p/prompts/system_3p.txt`

#### Authority and product invariants

Replace the first two quoted bullets with:

```text
- Priority: {product_image}'s exact product identity, orientation/view,
  scale and full visibility first; then the planned support relationship
  under the translation-only exception; then the user request; then defaults.
- {product_image} defines the product's exact orientation/view, size,
  visible faces, camera-facing surfaces, perspective/foreshortening,
  silhouette, aspect proportions, open/closed state, finish, ports,
  logo and display content. Its x-y location is the baseline, not an
  immutable frame position. Apply the TRANSLATION-ONLY EXCEPTION below.
```

Insert the shared translation rule immediately afterward.

#### Product-first planning

Replace step 1 with:

```text
1. Identify the product category, visible front/top/side faces, chassis
   edge directions, baseline frame region and user side. Use the supplied
   pixel bounds and contact point to plan the baseline layout; do not
   invent a newly centered, resized or reoriented product. These bounds
   and contact point may later shift only by the common translation
   allowed above.
```

Replace step 4 with:

```text
4. Arrange the scene around the product and its planned support
   relationship. Stage A plans that relationship at the supplied baseline
   location. Subsequent scene construction may translate the relationship
   as a unit, but must preserve its relative geometry and the product's
   exact orientation/view and scale.
```

#### Framing restriction

Replace “Preserve … exact framing” with:

```text
- Preserve {product_image}'s exact product scale and orientation/view;
  preserve its frame location unless the translation-only exception
  improves the scene. The product may remain small or off-center and
  need not dominate the image. Never shrink it to reveal furniture;
  crop the furniture at the frame instead. Never crop the product.
```

#### Support alignment

Replace the printer/laptop alignment bullets with:

```text
- A printer sits square on its support: construct the support so that
  its corresponding edges are parallel in 3D to the printer's front
  and side faces. Never rotate or reproject the printer to achieve this.
- A laptop need not sit exactly square to its desk; construct the desk
  from the laptop's supplied chassis yaw and viewpoint. Never change
  the laptop's yaw or viewpoint to fit the desk.
```

Retain the existing full-visibility/no-clutter bullet. Its ban on objects touching the silhouette should not be interpreted as prohibiting necessary underside contact:

```text
- Required weight-bearing contact with the support is not an occlusion;
  the support must not cross over or hide the product.
```

#### Output wording

Replace the quoted `"prompt"` instruction with:

```text
- "prompt": one 180-320-word photorealistic edit instruction starting
  "Turn {guide_image} into a photograph; preserve the [category]'s exact
  orientation/view, scale and details; translate it only under the rule
  below." State the translation-only exception, unchanged product
  orientation/view/scale/details, coherent support translation, full
  visibility and physical contact. Describe the support relative to
  the product, not as immutable absolute frame coordinates. Remove the
  diagram appearance; leave only one product at its final location.
```

The standalone final-prompt translation block can be outside this existing 180–320-word generated field; do not silently increase that field’s word limit.

---

### `hp3p/pipeline.py`

#### `_PRIORITY`

Replace the supplied fixed-geometry passage with:

```text
STAGE B. Image 1 contains the baseline support geometry and the real
product at the Image 3 baseline location. The product's exact
orientation/view and scale are fixed. Absolute x-y placement is subject
only to the TRANSLATION-ONLY EXCEPTION.

PRIORITY ORDER (strict):
1. The product: exact identity, orientation/view, perspective,
   foreshortening, scale, silhouette, state, details and full visibility.
   Never rotate, mirror, resize, reproject, redraw, crop or occlude it.
2. The planned product-to-support relationship: support orientation,
   user-facing edge, product-to-edge distances and tabletop extents
   relative to the product. Preserve this relationship under any
   permitted common translation.
3. The user request, followed by defaults.
```

Append the shared translation rule, then:

```text
When the user request requires a different product size, viewpoint,
orientation or support relationship, drop that part. Layout, emphasis,
framing and focal-point requests may be satisfied only within the
translation-only exception; they do not authorize arbitrary movement.

Your camera, composition and prompt must describe Image 1's reference
geometry in product-relative terms. The gray support defines the
reference tabletop and its user-facing edge, not immutable frame
coordinates. If translated, use the corresponding translated tabletop
region and edge locations. Keep the original restrictions on tabletop
extent, props, plausible scale and product visibility relative to that
translated reference. Do not lock room geometry to the old frame
coordinates.
```

This replaces—not supplements—the old “same table … drawn support … same near edge” paragraph.

#### `_WRITE_OVERRIDE`

Replace the fixed-input/unchanged-place wording with:

```text
The supplied geometry is the baseline reference layout, not an absolute
x-y placement lock. Preserve the product's exact orientation/view and
scale and the planned product-to-support relationship. The layout opens
the image prompt as its GEOMETRY section.

Describe which edge faces the user, where it lies relative to the product,
the product-to-edge distance and how much tabletop continues on each side.
Treat any absolute coordinates as baseline references that share the
same permitted translation. Do not independently relocate support edges.

Include the translation-only exception. Do not require a new location:
leave the baseline unchanged unless a feasible common translation improves
realistic use, access, support geometry, furniture alignment or composition.
Use "product" or the actual category, not "laptop" for printer scenes.
```

#### `_LEGEND`

Replace the supplied legend with:

```text
Image 1 is the canvas to edit: a geometry-only diagram containing the
real product at its baseline location and scale. Preserve the product
without redrawing it; only the permitted rigid 2D translation may change
its frame location.

The flat gray area defines the baseline support top surface and edge
locations. Preserve its geometry relative to the product. If the product
is translated, translate this support reference by exactly the same
displacement. It is not an immutable gray region that must remain at
its original coordinates.

Replace diagram styling with photographic materials and physically
plausible furniture and room geometry. Leave no gray guide remnants,
diagram lines, duplicate product or product-shaped remnant at the
original location. Keep only one intact product at the final location.
```

#### `_FINAL_CHECK`

Replace with:

```text
Final check before rendering: the product retains its exact identity,
orientation/view, visible faces, perspective/foreshortening, scale,
silhouette, state and details. Its only permitted geometric change is
one rigid x-y translation. Any translated support/contact reference
shares exactly that displacement and preserves the planned relative
geometry. The surrounding scene has consistent perspective. The product
is fully visible, unoccluded and physically supported with a plausible
contact shadow. No diagram remnants or duplicate product remain.
```

#### Stage-A body

Replace the two quoted sentences with:

```text
The product's exact orientation/view, scale and visibility and its planned
support relationship take priority over requested layout, extent and
emphasis. Plan the structured support geometry around the supplied
baseline product bounds and contact point. Do not pretranslate the guide
or invent a new viewpoint. Later scene construction may apply only the
common translation allowed by the translation-only exception.

Keep the product's color, finish, exact orientation/view, scale and
visibility unchanged. Blue requirements do not justify moving, resizing,
reorienting or otherwise changing the product or its camera viewpoint.
A translation must independently satisfy the translation-only exception.
```

#### Final prompt assembly

Replace the heading with:

```text
GEOMETRY — subordinate only to the product invariants.
Use Image 1 as the baseline reference layout, not an absolute x-y lock.
Preserve its product-to-support geometry under the translation-only
exception below.
```

Insert the shared translation rule in the actual GPT Image prompt. Do not rely on it existing only in Astra’s instructions.

Replace the final color/position restriction with:

```text
Keep the product's original color, finish, exact orientation/view, scale,
details and full visibility. Only the translation-only exception may
change its x-y location. Never change the product or its camera viewpoint
to make room for blue.
```

---

## 2. Stage-A geometry decision

**Continue planning and rendering at the original location. No renderer change is needed for this experiment.**

Treat the resulting guide as:

- An exact product-view and product-scale reference.
- A baseline support layout.
- A product-relative geometry constraint that can shift as a unit.

Do **not** reduce the polygon to loose “orientation inspiration.” That would also permit changing support distances, extents, or alignment independently, creating a broader experiment.

Stage B should describe this relationship relatively and preserve the conditional permission. GPT Image chooses whether a feasible displacement improves the scene; neither stage must force movement.

The surrounding room is newly generated, so it can be constructed with vanishing geometry consistent with the translated reference. The prompts must not simultaneously require original frame-anchored vanishing points. Product projection remains unchanged; the scene is built to fit it.

A consequence worth making explicit: **translation cannot repair an intrinsically inconsistent Stage-A support layout**. If its relative geometry is already wrong, moving it as a unit will not fix that. Record that limitation rather than silently allowing support redesign.

---

## 3. Contradiction checklist

Inspect source strings **and fully assembled runtime prompts**, including the demo wrapper.

| Remaining phrase or behavior | Required treatment |
|---|---|
| “fixed product,” “fixed geometry,” “do not change it” | Qualify as fixed view/scale and relative support geometry, not fixed x-y. |
| “exact framing,” “exact frame region,” “same Image 3 framing” | Replace with baseline location plus invariant scale/view. |
| “position unchanged,” “never move,” “unchanged in its place” | Replace with conditional common-translation permission. |
| “keep those product pixels unchanged” | Clarify preservation under translation, not preservation at original coordinates. |
| “tabletop covers exactly that area” | Make it the baseline area or its common translated equivalent. |
| “edge at the same frame location,” absolute contact coordinates | Identify as baseline coordinates sharing the displacement. |
| “match Image 1 exactly” / “GEOMETRY — highest priority” | Subordinate geometry to product invariants and state the exception. |
| “new camera angle,” “reframe,” “better viewpoint,” “fit perspective” | Remove; these invite viewpoint, projection or scale changes. |
| “align/square the product with the desk” | Align the support to the unchanged product, never the reverse. |
| “move closer,” “move farther back,” “make prominent,” “center” | Do not use as movement instructions; they invite depth/scale changes or arbitrary placement. |
| “support can move freely” or “gray polygon is only inspiration” | Replace with common translation and preserved relative geometry. |
| “camera unchanged” | Preserve viewpoint/projection; do not use it to reintroduce an absolute x-y lock. |
| “no object touching silhouette” | Preserve no occlusion while allowing required underside support contact. |
| Blue/style/layout overrides | Must not independently authorize movement or orientation changes. |
| Unseen output-field descriptions, examples, wrapper suffixes | Audit for the same conflicts; supplied excerpts cannot establish their absence. |

---

## 4. Controlled smoke test

Use four fixtures, with **one control and one treatment generation per fixture**—eight outputs, no retries or selection of best results.

| Fixture | Purpose |
|---|---|
| Open laptop, close framing | Screen/chassis viewpoint, hinge state, edge clearance, contact. |
| Same laptop, wide framing | Conditional repositioning without enlarging or centering by default. |
| Printer, close framing | Front/side face preservation, square support alignment, access. |
| Same printer, wide framing | Furniture/room perspective and contact consistency. |

Where practical, include an awkward baseline placement and an already usable placement within these four fixtures. Choose fixtures before seeing treatment outputs.

Hold product assets, source scale, request, style/blue requirements, model, generation settings and guide constant within each pair. Use identical seeds if the interface supports them; do not assume determinism. For the image-generation comparison, reuse each fixture’s baseline guide. Separately verify that the revised Stage-A prompt still produces baseline geometry rather than pretranslating it.

### Mechanical success: prove the experiment was delivered

Capture:

- PR/source identifier, treatment prompt-file hashes or version label.
- Stage-A and Stage-B rendered system/user prompts and structured outputs.
- Guide image, product bounds/contact point, and guide hash.
- Fully assembled GPT Image prompt, actual model identifier and input-image list.
- Evidence that the image call remains guide-only, without a mask.
- Output and evidence that no coordinate repair ran.

Pass only if:

1. Every relevant prompt layer contains compatible translation semantics.
2. No effective absolute-position lock or viewpoint-change invitation remains.
3. Stage A still uses baseline coordinates.
4. The final image prompt explicitly preserves exact view and fixed scale.
5. No unrelated settings or pipeline behavior changed.

The port-8016 label is useful context, **not proof** of the live prompt lineage.

### Visual acceptance: separate gates

**Product invariant gate — mandatory**

After accounting for only one x-y displacement, compare source and output:

- Matching silhouette and width/height.
- Matching chassis, screen, tray and panel landmarks.
- Matching visible faces, edge slopes and foreshortening.
- No mirroring, yaw/pitch/roll change, scale change, warp or changed open/closed state.
- No altered logos, ports, display content, controls or invented product features.

A diagnostic translation-only overlay is appropriate for inspection, not repair. If matching requires rotation, resizing, perspective adjustment or warping, reject. State measurement tolerance in advance; it is measurement uncertainty, not permission for orientation drift.

**Support/scene gate — mandatory**

- Support/contact relationship moves coherently with the product.
- Planned relative distances and edge directions remain intact.
- Furniture anatomy and room perspective are consistent.
- Contact shadow and weight-bearing contact are plausible.
- Product is fully visible and unoccluded.
- No gray polygon, guide lines, ghost product or old-position remnants remain.

**Hypothesis signal**

For a moved result, record the specific improvement: access, support plausibility, furniture alignment or composition. Movement alone is not success.

An unchanged result is allowed and can pass visual acceptance, but provides no positive evidence that translation helped. If no challenging fixture moves, this smoke test is inconclusive about the hypothesis.

**Downstream compatibility — separate gate**

Evaluate whether the unchanged digital-twin view/scale fits the generated product footprint at its final location. Separately document how the existing downstream consumer locates that footprint.

If it pastes only at the original coordinates, **any nonzero translation fails that downstream path**, even when the image passes every visual gate. Prompt wording cannot resolve that coordinate-contract conflict.

---

## 5. Risks and cheapest follow-up

- **Maskless redraw:** Exact-view language reduces ambiguity but cannot guarantee unchanged product pixels. Treat any redraw or view drift as failure.
- **Guide anchoring:** The embedded product and polygon may overpower translation permission, yielding no movement.
- **Partial movement:** The product may move while support edges, contact shadow or room perspective remain anchored.
- **Overconstraint:** Preserving the whole relative layout may leave no useful translation, especially in close crops.
- **Downstream location contract:** Orientation and scale preservation are necessary but not sufficient if paste coordinates are fixed.

The cheapest follow-up is to classify the failures from this single smoke test, inspect the assembled prompts for residual conflicts, and tighten only the ambiguous sentence in a subsequent controlled prompt revision. Do not retry failed images to obtain a passing sample.

If the prompts are mechanically coherent but outputs still rotate, redraw, resize or move incoherently, report that **prompt-only translation is insufficient under these constraints**. Do not relax the exact-view requirement or quietly admit scale/support redesign. If the blocker is fixed-coordinate downstream placement, identify that incompatibility explicitly rather than presenting this experiment as production-ready.
