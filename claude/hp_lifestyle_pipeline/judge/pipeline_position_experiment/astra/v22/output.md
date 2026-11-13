## 1. v22 policy

**Replace “translate the product/support relationship together” with “translate only the unchanged product; compose the support around its chosen position.”** Replace the conflicting v21 passages rather than appending another exception.

| Element | v22 contract |
|---|---|
| Product appearance and geometry | Exact identity, view, orientation, projection, foreshortening, silhouette, pixel width/height, state, finish, details, logo/display content. No rotation, mirroring, resizing, warping, reprojection, redraw, crop or occlusion. |
| Product position | One rigid image-plane x-y translation is permitted. Exactly one product remains fully inside the frame. |
| Support | Compose independently beneath the chosen product position. Baseline product-to-edge distances, tabletop extents and edge locations are not binding. |
| Physical relationship | Fully support the base; provide believable edge clearances, contact, access and room perspective. Printer square to support in 3D; laptop oriented toward a usable working/seating edge. Furniture adapts to the unchanged product—not vice versa. |
| Placement objective | Usability, access, support/furniture geometry, alignment, narrative or composition. No movement merely for centering or prominence; no enlargement at all. |
| Baseline status | Evidence, not a preference. Retention and relocation are both valid when justified by the resulting scene. |
| Experiment boundary | Stage A calculations, baseline coordinates, guide rendering, schemas, masks, image-call count and downstream composition remain unchanged. |

## 2. Exact replacement wording

These are replacements for the corresponding v21 policy passages. Keep unrelated instructions intact. Where `system_3p.txt` is shared with Stage A, scope these replacements to **Stage B and final-scene construction only**; do not replace Stage A’s baseline-planning instructions.

### A. Central policy block — `hp3p/pipeline.py`

Replace the entire `TRANSLATION-ONLY EXCEPTION` block with:

```text
TRANSLATION-ONLY PRODUCT PLACEMENT; RECOMPOSED SUPPORT

The guide shows the unchanged product at an initial x-y position and a baseline support diagram. Choose the product position for realistic use, access, support-surface geometry, furniture alignment, scene narrative or composition. The baseline position and baseline support distances have no preference. Retain the baseline position when it already gives the best usable composition; do not force movement. Do not move the product merely to center it or make it more prominent. Never enlarge it.

The only permitted change to the product is one rigid image-plane x-y translation. Keep its exact pixel width and height, yaw, pitch, roll, viewing angle, visible faces, camera-facing surfaces, perspective, projection, foreshortening, silhouette, aspect proportions, open/closed and powered state, finish, details, logo and display content. Do not rotate, mirror, resize, shear, warp, reproject, redraw or activate the product. Do not zoom, reframe or change the viewpoint in a way that alters the product.

At the chosen product position, compose a category- and scenario-appropriate support beneath its weight-bearing base. The support may change independently of the product's translation: do not preserve baseline product-to-edge distances, tabletop extents, or absolute support-edge locations as requirements. Fully support the base without floating or overhang, with believable front, back and side clearances, natural weight-bearing contact, a contact shadow and material-appropriate reflections on the support.

Construct furniture around the unchanged product orientation. A printer must sit square to its support in 3D with usable access to its operating front. A laptop must face a usable seating or working edge with clear access to its keyboard and display. Do not rotate the product or reveal a different face to fit the furniture. Support axes, room perspective, horizon and vanishing geometry must be compatible with the unchanged product projection at its chosen position; do not retain incompatible geometry from the initial layout.

Keep exactly one product, entirely inside the frame and fully visible. No prop, furniture edge or foreground object may occlude it. Remove the gray guide, diagram marks and any ghost or duplicate product. If the product moves, complete the vacated location as part of the scene. If a candidate placement violates any product or support requirement, choose another placement or recompose the support and room without relaxing the product invariants.
```

The last sentence deliberately replaces the baseline fallback. Failure of one candidate does **not** establish that the baseline is preferred or feasible.

### B. Priority order — `hp3p/pipeline.py`

```text
PRIORITY ORDER (strict):
1. The product: exact identity, orientation/view, projection, perspective, foreshortening, pixel size, silhouette, state, finish, details and full visibility. Only rigid image-plane x-y translation is permitted.
2. A believable, category- and scenario-appropriate support and room constructed around the unchanged product at its chosen position, with full base support, usable access and consistent furniture/perspective geometry. Baseline position, product-to-edge distances, tabletop extents and support-edge locations are not requirements.
3. The original user request, followed by defaults, wherever compatible with priorities 1 and 2.
```

### C. Camera/composition paragraph — `hp3p/pipeline.py`

Replace the paragraph beginning “Your camera, composition and prompt…” with:

```text
Your camera, composition and prompt must preserve the product view and pixel size shown in the guide while describing the chosen product position and support. The gray region is baseline planning evidence, not a required tabletop shape, extent, edge location or product-to-edge distance. Compose the support and room around the unchanged product at its chosen position. Retain restrictions on plausible physical scale, props and product visibility, but do not carry forward baseline tabletop extents or edge clearances as constraints.
```

### D. Stage-B override

Replace the current baseline-edge/common-translation override with:

```text
STAGE-B PLACEMENT AND SUPPORT OVERRIDE

Treat product view, geometry, pixel width and pixel height as authoritative. Treat product frame coordinates as the initial position only. Treat all gray-support edges, distances, extents and support-crop descriptions as baseline evidence that may be replaced.

Choose a usable product position without preferring the baseline and without forcing movement. In the existing output prose, describe the chosen position and the support built beneath it: the usable approach or working edge, full support of the weight-bearing base, believable front/back/side clearances, and consistent furniture and room perspective. Describe the resulting geometry, not baseline distances unless they remain appropriate in the chosen scene.

Support edges may be relocated and tabletop extents recomposed independently of product translation. Construct a printer's support square to its fixed orientation in 3D; construct a laptop's desk/table and user position around its fixed working orientation. Do not change the product view, orientation or pixel size to satisfy furniture or camera wording.

The final image instruction must explicitly preserve the product invariants, permit only x-y product translation, require appropriate support at the chosen position, and require exactly one fully visible product with no gray guide or ghost at its former location. Use "guide", "baseline diagram", "initial layout" or "current canvas" when needed. Mention no additional images or image numbering. Express requested scene appearance directly in words.
```

This uses the existing prose output; it introduces no field or schema requirement.

### E. Final-prompt prefix and legend

Replace the prefix with:

```text
Use the guide for the product's exact appearance, view and pixel size, not as a lock on its x-y position or support layout. Apply the translation-only product-placement and recomposed-support policy below.
```

Keep it immediately before the central policy block.

Replace the support legend with:

```text
GUIDE LEGEND
The real product pixels establish the exact product appearance, view and pixel size to preserve. Their frame position is the initial position only. The flat gray region and its boundaries show an initial support plan, not output pixels or required support edges, distances or extents. At the chosen product position, compose an appropriate support beneath the unchanged product. Remove all gray-guide and diagram remnants from the finished scene.
```

### F. `system_3p.txt` passages

Use this scope statement for the revised scene-construction passages:

```text
The following placement and support policy applies to Stage B and final-scene construction only. Stage A continues to calculate and describe the initial geometry and draw the guide at the supplied baseline coordinates.
```

**Authority replacement:**

```text
Priority for Stage B and final-scene construction: exact product invariants first, with only rigid image-plane x-y translation permitted; then believable support, access and room geometry constructed around the product at its chosen position; then the user request and defaults. Baseline product coordinates and baseline support relationships do not outrank these requirements.
```

**Product-first planning replacement:**

```text
For Stage B and final-scene construction, choose the product's x-y position for realistic use, access, furniture geometry, alignment, narrative or composition, without preferring the baseline or forcing movement. Build an appropriate support beneath the weight-bearing base at that position. Baseline support edges, extents and product-to-edge distances may be replaced independently of product translation. Adapt the support and room to the unchanged product; never adapt the product's orientation, view or pixel size to the furniture.
```

**Geometry replacement:**

```text
For Stage B and final-scene construction, preserve the product's exact view, orientation, projection, foreshortening, silhouette and pixel dimensions. Its frame position may change only by rigid x-y translation. Construct support axes and room perspective, horizon and vanishing geometry consistent with that fixed product projection at the chosen position. Keep a printer square to its support in 3D and a laptop facing a usable working/seating edge. Do not impose baseline frame coordinates, tabletop extents or product-to-edge distances on the new scene.
```

**Final-output replacement:**

```text
In the existing final-output prose, describe the chosen product position and the support constructed beneath it, including usable access, full base support and coherent furniture/room perspective. Carry forward the exact product invariants and the x-y-only permission. Do not instruct a common translation of product and support or preservation of baseline support distances. Require exactly one fully visible, unoccluded product and removal of all guide marks and any product ghost. Mention only the current guide; describe scene appearance directly without invoking additional images.
```

### G. `geometry.describe_geometry()` policy prose

Leave every numeric result and guide-drawing input unchanged. Change only the Stage-B-facing prose around those facts.

Precede the unchanged measurements with:

```text
BASELINE DIAGRAM MEASUREMENTS
The following coordinates, support distances, tabletop extents, edge locations and support-crop descriptions describe the initial layout only. They are planning evidence, not required final-scene placement or support geometry. The product's exact view and pixel dimensions remain authoritative.
```

Replace:

> Under a permitted common translation, keep the same support relationship.

with:

```text
For final-scene construction, compose an appropriate support beneath the product at its chosen x-y position. Baseline product-to-edge distances, tabletop extents, support-edge locations and support cropping may be replaced independently of product translation, provided the base is fully supported and access and perspective remain believable.
```

Replace:

> Keep this exact view and pixel size; only the translation-only exception may change these frame coordinates.

with:

```text
Keep this exact product view and pixel size. The listed product frame coordinates identify the initial position only; the entire product may undergo one rigid x-y translation while remaining fully inside the frame and unoccluded. This permission does not allow rotation, resizing, reprojection, cropping or any other product change.
```

## 3. Hidden-contradiction audit

The important audit is semantic, not just a search for “common translation.”

| Residual instruction | Why it conflicts / required treatment |
|---|---|
| “Keep the location unless…” or “preserve frame location” | Establishes baseline preference. Replace with neutral placement selection. |
| “If no feasible translation, retain baseline” | Baseline may also be infeasible; encourages premature fallback. Use candidate rejection and support/room recomposition. |
| “Preserve the planned support relationship” | Retains v21 even without mentioning translation. Remove as an authority. |
| “Keep original tabletop restrictions” | May silently reinstate extents, edge distances or cropping. Retain only physical plausibility, prop and visibility restrictions. |
| Exact frame percentages presented as requirements | Numeric specificity can override permissive prose. Label them as initial measurements adjacent to the facts. |
| “Place beneath the existing contact point” | Locks the absolute contact location. For Stage B, say “beneath the base at the chosen position.” |
| “The gray region defines the tabletop/user edge” | Makes the diagram prescriptive. It depicts an initial plan; the new working edge follows fixed product orientation and usability. |
| “Never relocate support edges independently” | Directly contradicts v22. Remove everywhere in Stage-B-facing policy. |
| “Preserve support-edge directions” | Can preserve baseline furniture geometry rather than geometry compatible with the product. Require 3D consistency instead. |
| Generic camera/lens/crop instructions | May induce zoom, changed product scale or viewpoint. Scene camera wording must remain compatible with the supplied product projection. |
| Examples containing old edge percentages or “same tabletop” | Examples can reintroduce the old policy. Update or remove those particular examples. |
| Shared system instructions applied to Stage A | Would change the experiment boundary. Keep the revised permission explicitly Stage-B/final-scene-only. |

Also audit default furniture instructions: a rule such as “front desk edge must be horizontal” can conflict with the unchanged oblique product view.

## 4. Why “new support beneath the translated product” does not authorize a new view

Separate the two freedoms explicitly:

- **Product:** a fixed raster object with only its image-plane location variable.
- **Support and room:** newly composed geometry constrained by that object’s unchanged projection and functional orientation.

The crucial wording is:

> “Adapt the support and room to the unchanged product; never adapt the product's orientation, view or pixel size to the furniture.”

“Beneath” means supporting the **weight-bearing base**, not placing a generic horizontal patch below the product’s bounding box.

Likewise, “printer square to support in 3D” does not mean making every visible edge parallel in 2D. Corresponding product and furniture axes must have coherent perspective. A laptop’s working edge follows its actual keyboard/user orientation—not whichever side of the canvas is easiest to furnish.

## 5. Focused prompt/output contract tests

Use the existing validation and smoke process. “Close” and “wide” describe fixture compositions at their existing product pixel sizes; they do not authorize zoom or resizing. Judge both Stage-B wording and the generated image.

| # | Fixture / request | Stage-B contract | Visual contract |
|---|---|---|---|
| 1 | **Close laptop, baseline already usable** | Allows retention without invoking baseline priority; describes a usable working edge. | Product may remain at baseline; base supported, keyboard accessible, exact size/view. |
| 2 | **Wide laptop, actual relocation**: baseline left; requested right-hand workstation leaves a left-side through-aisle clear | Selects a right-hand working position for access/layout, not prominence; composes its desk there. | Actual product displacement; plausible seating/access; no inherited baseline edge clearances. |
| 3 | **Close printer, actual relocation**: baseline right; requested left-hand printer station preserves right-side packing space | Moves printer for usable workspace; constructs support at destination. | Translation without scale/view change; complete base support and accessible operating front. |
| 4 | **Wide printer, baseline already suitable** | Does not force movement merely to demonstrate permission. | Retention acceptable; room/support coherent at unchanged size. |
| 5 | **Printer near a wall** | Builds wall/support around fixed printer orientation; does not turn printer to face the room. | Operating front remains usable; wall does not intersect device or block required access; plausible rear/side clearance. |
| 6 | **Oblique laptop with misleading baseline front edge** | Repositions/reorients desk and seating around fixed laptop working orientation. | Usable keyboard approach; no laptop rotation or forced alignment to the canvas edge. |
| 7 | **Printer with baseline support axes that would be awkward in the requested room** | Requires square seating in 3D, not preservation of baseline edges. | Printer/support axes share coherent perspective; no device rotation or arbitrary 2D edge-parallel shortcut. |
| 8 | **Baseline gray support too shallow or unnecessarily extensive** | Explicitly permits different depth, extents and edge distances, even if product stays put. | Full base support with believable clearances; new tabletop geometry rather than merely shifted gray footprint. |
| 9 | **Request for cropped hero framing, foreground props or multiple devices** | Product invariants win: one whole product, original size, no occlusion. | No crop, enlargement, foreground obstruction or duplicate product. |
| 10 | **Request conflicting with product view/state**: overhead camera, mirrored orientation, different lid angle or changed screen | Rejects those changes in executable scene instructions while satisfying compatible scene details. | Same faces, lid/state, logo/display, projection and pixel dimensions. |
| 11 | **Relocation exposing former product location and large gray-guide areas** | Requires completed scene at former location and removal of all guide remnants. | No ghost silhouette, duplicate feet, old contact shadow, residual gray region or diagram edge. |
| 12 | **Vocabulary-leakage bait**: request or contextual prose includes “Follow the reference tabletop,” “source image,” “style image,” or “Image 2” | Final executable prompt describes desired appearance directly using current-guide terminology. It does not copy the bait, even as a negated warning. | Existing final-prompt validator accepts the wording; no unseen-image invocation. |

For relocation cases, a sentence saying “move the product” is not a pass: **the rendered product must actually move**. Conversely, do not require one exact destination or one exact new tabletop outline when multiple physically valid solutions exist.

## 6. Limits and required smoke evidence

Prompt-only v22 cannot guarantee:

- Exact product-pixel preservation: the image model may still redraw details, alter logos/screens, resize subtly or introduce local warping.
- Physical correctness from a single view: hidden base geometry, clearances and 3D axis alignment may be inferred incorrectly.
- Actual relocation: strong visual anchoring to the guide may survive permissive text.
- Complete cleanup: ghosts, old shadows and gray boundaries may remain.
- Seamless downstream repasting: mismatched contact shadows, reflections, lighting or generated silhouettes can expose the pasted product.
- Compatibility with a downstream paste operation that assumes baseline coordinates, **if one exists**. This experiment supplies no new placement metadata and does not modify that operation.

The smoke should inspect:

1. **Translation-only preservation:** all product landmarks should share the same displacement; width, height, silhouette, faces and internal geometry must remain unchanged.
2. **Real support recomposition:** changed edge distances/extents where warranted—not just a translated version of the baseline support.
3. **Contact and access:** base coverage, no floating/overhang, plausible shadows/reflections, usable laptop position and printer operating access.
4. **Perspective:** furniture axes and room horizon/vanishing geometry compatible with the product at its chosen position.
5. **Cleanup and containment:** one complete, unoccluded product; no old product, old shadow or guide residue.
6. **Text/image agreement:** distinguish a compliant Stage-B instruction from a compliant generated image.

A smoke showing only baseline retention remains inconclusive for the intended hypothesis. It should include successful **actual relocation with independently recomposed support**, plus a justified baseline-retained case—without any relaxation of product invariants.
