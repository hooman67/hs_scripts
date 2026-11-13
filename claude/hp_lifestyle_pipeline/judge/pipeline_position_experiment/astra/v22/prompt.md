# Product-LLM prompt design review: PR4349 v22 movable product on newly composed support

You are reviewing a bounded prompt-policy experiment for Adobe Firefly Foundry's HP image pipeline. This is product LLM integration work. Do not write general application code. Propose the smallest coherent model-facing prompt delta, identify contradictions, and give exact replacement wording plus focused validation cases.

## Pipeline and downstream constraint

The pipeline uses an approved 2D digital-twin render of an HP laptop or printer. Stage A derives product/camera geometry and draws a gray support guide. Stage B sees that guide with the real product pixels plus the user scene request and writes the final GPT Image edit instruction. GPT Image then produces the scene. Later downstream stages may paste the exact digital-twin product pixels back into the generated result.

Therefore the scene model may change only the product's x-y position in the output image. It must preserve, exactly:

- yaw, pitch, roll, viewing angle, visible faces and camera-facing surfaces;
- perspective, projection, foreshortening, silhouette and aspect proportions;
- pixel width and height (scale), full visibility, state, finish, details, logo/display content;
- no rotation, mirroring, resizing, warping, reprojection, crop or occlusion.

Stage A and the guide renderer must remain unchanged at the baseline coordinates. The gray guide is planning evidence, not an output pixel lock.

## Experiment history and why v21 is rejected

The baseline pipeline told the image model to keep the product at the exact position in the guide. That often forced desks/tables and room perspective to be generated awkwardly around a fixed product.

v21 allowed one common x-y translation of the product **and its planned support relationship as a unit**. It required product-to-edge distances, support edge locations/extents relative to the product, and support/contact geometry to remain fixed. A four-fixture smoke and a 12-row pilot were mechanically coherent, but Stage B retained the baseline position in almost every composition. This overconstrained the hypothesis and is now frozen as an inconclusive pilot.

v22 must test the intended hypothesis more directly:

- Keep the product invariants above exact.
- Allow the product to translate freely in x-y relative to a newly composed support surface.
- The model must build a new, believable support **beneath the product at its chosen position**. The support need not preserve Stage A's baseline product-to-edge distances, tabletop extents, or absolute edge locations.
- The new support must be category- and scenario-appropriate, fully support the base without floating/overhang, have believable front/back/side edge distances, natural weight/contact shadow/reflection, clear user access, and consistent room perspective/horizon/vanishing geometry.
- Furniture axes must make sense with the unchanged product view. A printer sits square to its support in 3D; construct the support around the fixed printer orientation. A laptop should face a usable seating/working edge; construct the desk/table and user position around the fixed laptop orientation. Never rotate the device to fit furniture.
- Placement may be moved for usability, access, support/furniture geometry, alignment, scene narrative or composition. It must not be moved merely to center, enlarge or emphasize the product.
- Do not force movement when the baseline is already the best usable composition, but do not treat baseline position or baseline support distances as preferred.
- Keep exactly one product, fully inside frame and unoccluded. Remove guide remnants and any ghost product at the former location.
- This is prompt-only. No mask, coordinate repair, extra image retry, Stage-A change, guide-renderer change, or schema change.

## Current v21 prompt fragments that must be revised

From `hp3p/pipeline.py`:

```text
TRANSLATION-ONLY EXCEPTION
The guide gives the baseline product location and support layout. Keep that location unless one rigid 2D translation improves realistic product use, access, support-surface geometry, furniture alignment or composition. Do not move the product merely to center it or make it more prominent.

Only a common image-plane x-y translation of the product and its planned support relationship is allowed. Keep product pixel width and height unchanged. Preserve the exact original yaw, pitch, roll, viewing angle, visible faces, camera-facing surfaces, perspective and foreshortening, silhouette, aspect proportions, open/closed state and all product details. Do not rotate, mirror, resize, shear, warp, reproject, redraw or activate the product. Do not zoom or change the product's camera viewpoint.

If translated, shift the planned support/contact geometry by the same displacement: preserve support-edge directions, the user-facing edge, product-to-edge distances and tabletop extents relative to the product. Do not move the product independently of its support relationship. Construct the surrounding furniture and room with perspective consistent with this translated geometry; do not retain incompatible vanishing geometry anchored to the original frame location.

Keep the entire product inside the frame and fully visible, with plausible weight-bearing contact and a corresponding contact shadow. No prop, furniture edge or foreground object may occlude the product. If no feasible translation meets all these constraints, retain the baseline location.
```

```text
PRIORITY ORDER (strict):
1. The product: exact identity, orientation/view, perspective, foreshortening, scale, silhouette, state, details and full visibility.
2. The planned product-to-support relationship: support orientation, user-facing edge, product-to-edge distances and tabletop extents relative to the product. Preserve this relationship under any permitted common translation.
3. The original user request, followed by defaults.
```

```text
Your camera, composition and prompt must describe Image 1's baseline geometry in product-relative terms. The gray support defines the baseline tabletop and its user-facing edge, not immutable frame coordinates. If translated, use the corresponding translated tabletop region and edge locations. Keep the original restrictions on tabletop extent, props, plausible scale and product visibility relative to that translated geometry.
```

The Stage-B override currently says to describe how close the product sits to the baseline user edge and how much tabletop continues around it, to treat absolute coordinates as baseline positions sharing a common translation, and to never relocate support edges independently.

The final prompt prefix currently says:

```text
Use Image 1 as the baseline layout, not an absolute x-y lock. Preserve its product-to-support geometry under the translation-only exception below.
```

The legend currently says the flat gray region defines baseline support top/edge locations, preserve its geometry relative to the product, and translate support by exactly the same displacement.

From `system_3p.txt`, the same common-translation language appears in authority, product-first planning, geometry, and final-output instructions. Examples:

```text
Priority: product invariants first; then the planned support relationship under the translation-only exception; then user request.
```

```text
Place [the support] beneath the existing contact point ... Stage A plans that relationship at the supplied baseline location. Subsequent scene construction may translate the relationship as a unit, but must preserve its relative geometry.
```

```text
Preserve the product's frame location unless the translation-only exception improves the scene.
```

```text
Describe the support relative to the product, not as immutable absolute frame coordinates; state coherent support translation.
```

From `geometry.describe_geometry()`, the Stage-A factual summary currently emits baseline product-to-edge distances, tabletop extents, crop, and exact baseline frame percentages. It adds model-facing policy such as:

```text
Under a permitted common translation, keep the same support relationship.
Keep this exact view and pixel size; only the translation-only exception may change these frame coordinates.
```

Stage A numeric geometry and guide drawing stay unchanged, but its Stage-B text must clearly label support distances/extents/edges as baseline evidence that may be replaced by a newly composed, perspective-consistent support. Exact product view and pixel size remain authoritative.

## Leakage constraint learned from v21

The final image prompt is validated before the image call. Standalone words such as `reference`, `source image`, `style image`, or unseen-image numbering can be rejected because the image model receives only the current guide plus text. A prior v21 smoke failed when Stage B copied `Follow the reference tabletop`. Use terms such as `guide`, `baseline diagram`, `initial layout`, or `current canvas` where needed, and keep executable final prompt wording free of unseen-image references.

## Requested answer

1. State the v22 policy in a short invariant/permission table.
2. Give exact replacement text for the central policy block, priority order, Stage-B override, final-prompt prefix/legend, system-prompt authority/planning/geometry/output passages, and `describe_geometry()` policy sentences. Keep edits as small and coherent as possible.
3. Audit for hidden contradictions that would still bias Stage B to baseline position or fixed support distances.
4. Explain how to say “new support beneath the translated product” without letting the model change product orientation, viewpoint or scale.
5. Give 8-12 focused prompt/output contract tests, including laptop/printer, close/wide, baseline retained, actual relocation, user access, printer wall placement, support-edge alignment, product fully visible, no ghost/remnant, and forbidden unseen-image vocabulary.
6. Identify failure modes that this prompt-only experiment cannot prevent and what visual evidence the smoke must inspect.

Do not propose implementation beyond model-facing prompt text and tests. Do not change Stage A, the guide renderer, image-call count, masks, schemas, or downstream composition.
