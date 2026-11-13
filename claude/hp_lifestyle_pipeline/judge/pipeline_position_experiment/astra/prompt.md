# HP image pipeline prompt-design review: allow translation, preserve orientation

You are reviewing a narrow prompt-policy experiment for Adobe's HP lifestyle-image pipeline. This is a product LLM integration experiment, not a request to write application code. Give precise prompt-language changes and validation guidance. Do not broaden the experiment.

## Decision and experimental hypothesis

The current image-generation prompt requires GPT Image 2.5 to keep the target laptop or printer at the exact same x-y pixel position as a geometry-guide render. In many generations, the scene model then bends the table/desk geometry, vanishing points, focal geometry, or furniture anatomy around that fixed product position.

For the experiment, GPT Image 2.5 may translate the target product to a more natural x-y location in the frame so that it can build a believable support surface and composition. It must preserve the target product's exact 3D orientation/viewpoint: same yaw, pitch, roll, visible faces, camera-facing surfaces, perspective/foreshortening, silhouette, aspect proportions, open/closed state, and product details. Downstream stages paste or relight pixels from the digital twin, so rotating, mirroring, changing the viewing angle, changing which faces are visible, changing perspective, or redrawing the product creates an unusable result. Translation is allowed; orientation/view is not.

This is a controlled one-variable experiment. Keep the source product scale unchanged unless there is a compelling reason that scale must move with the translation; in your recommendation, explicitly decide whether scale should remain fixed and explain why. Preserve full visibility, contact with a plausible support surface, physical weight/contact shadow, and no occlusion. The scene model should choose the translated location only when it improves realistic product use, support-surface geometry, access, furniture alignment, or composition. Do not invite arbitrary repositioning.

## Verified code lineage and image call

- Repository PR: `Adobe-Firefly/foundry#4349`
- Fetched PR head when this prompt was prepared: `8c358bc7989cb0e137e89db0fd325168249e2a22`
- Package: `experimental/adarabi/hp-3p-gpt25`
- Runtime flow: Astra Stage A plans structured camera/support geometry; code draws a geometry guide containing the real digital-twin product pixels and a gray support polygon; Astra Stage B writes layout/camera/composition/edit text; GPT Image 2.5 receives only that guide plus text, without a mask; no post-generation coordinate repair.
- GPT Image model: `gpt-image-2.5-sunburst-2026-09-08`
- Stage A and Stage B use GPT-6 Astra. This review is about their system/user prompt wording and the final GPT Image prompt.

The deployed demo at port 8016 labels itself `Adobe-Firefly/foundry#4349 / Twin camera · Guide-only, no mask · Text blue` and exposes a scene-only generation route. Its web-server wrapper is not in PR #4349, but the generation package above is the identified source lineage.

## Current prompt language that locks position

File `hp3p/prompts/system_3p.txt` contains:

```text
- Priority: {product_image}'s fixed product first, then the planned geometry (camera,
  support, user-facing edge and the product's place on the support), then the
  user request, then defaults.
- {product_image} defines the product's exact orientation, position, size, visible faces,
  silhouette, finish, ports, logo and display content. Do not move, rotate,
  enlarge, shrink, crop, redraw or activate the product.

1. Identify the product category, visible front/top/side faces, chassis edge
   directions, exact frame region and user side. Use the supplied pixel bounds
   and contact point, not a newly centered or resized product.
...
4. Arrange the scene around the fixed product and planned support.
...
- Preserve {product_image}'s exact framing. The product may be small or off-center and
  need not dominate the image. Never shrink it to reveal furniture; crop the
  furniture at the frame instead.
...
- A printer sits square on its support: its front and side faces are parallel
  in 3D to the support edges.
- A laptop need not sit exactly square to its desk; the desk follows the
  laptop's estimated chassis yaw.
...
- Keep the product fully visible: no object crossing or touching its silhouette,
  no foreground occluder, no invented cables or irrelevant floor clutter.
...
- "prompt": one 180-320-word photorealistic edit instruction starting
  "Turn {guide_image} into a photograph; keep the [category] exactly as shown". State unchanged product framing and details ...
```

File `hp3p/pipeline.py` contains:

```text
_PRIORITY = """STAGE B. Geometry is already fixed and drawn in Image 1 around the real product, at the exact Image 3 framing. Do not change it.

PRIORITY ORDER (strict):
1. The product ...: its pixel position, size, orientation and visibility. Never move, resize, rotate, crop or occlude it.
2. The FIXED GEOMETRY ...: table orientation, the user-facing edge and its position in the frame, the product-to-edge distance, how far the tabletop extends to each side, frame crop and camera.
...
When the user request asks for a different layout, extent, emphasis, framing, focal point, product size, or a table that fills or dominates the foreground, drop that part and follow 1 and 2. Your camera, composition and prompt must describe exactly the geometry of Image 1: the same table orientation, the user-facing edge along the near edge of the gray support area, tabletop only on the drawn support, nothing beyond the user-facing edge, props on the drawn tabletop at plausible scale beside the product, and nothing occluding the product.
"""

_WRITE_OVERRIDE = "... geometry is a fixed input ... layout opens the image prompt as its GEOMETRY section ... which edge faces the user and where it sits relative to the laptop; how close the laptop sits to that edge; how much tabletop continues on each side ... and the laptop unchanged in its place."

_LEGEND = "Image 1 is the canvas to edit: a geometry-only diagram at the final framing whose product pixels are the real product. Keep those product pixels unchanged. The flat gray area ... is the exact top surface of the support: the tabletop covers exactly that area, with its edges where the gray area's edges are ..."

_FINAL_CHECK = "Final check before rendering: the product is unchanged in position, size and orientation; the table orientation, user-facing edge, product-to-edge distance and tabletop extent match the GEOMETRY section and Image 1."
```

Stage A's user text additionally says:

```text
The fixed product and planned support geometry take priority over requested layout, extent and emphasis; adapt those to the geometry.
Keep the product's color, finish, orientation, position, scale and visibility unchanged; never change the product or camera to make room for blue.
```

Final prompt assembly adds:

```text
GEOMETRY — highest priority. Follow Image 1 exactly.
...
Keep the product's original color, finish, orientation, position, scale and visibility; never change the product or camera to make room for blue.
```

The geometry guide itself embeds the actual target-product pixels at the original x-y coordinates and draws the planned support around that original location. Because no mask is sent, GPT Image can technically edit and move the product, but current text repeatedly forbids it.

## What I need from you

Recommend the smallest coherent prompt delta that tests the hypothesis while preserving all unrelated behavior. Address all prompt layers that would otherwise contradict each other:

1. `system_3p.txt` authority, product-first planning, geometry, restrictions, and output wording.
2. `pipeline.py` `_PRIORITY`, `_WRITE_OVERRIDE`, `_LEGEND`, `_FINAL_CHECK`, Stage-A body, and final prompt assembly.
3. Whether the structured Stage-A support geometry should still be planned around the original product location or should be treated as orientation/perspective guidance whose whole product-plus-support relationship may translate. The experiment should not require redesigning the guide renderer unless prompt-only change cannot be coherent.
4. How to tell Stage B and GPT Image that only a rigid 2D translation is allowed: preserve exact orientation/view/perspective/scale, translate product and its support relationship coherently, maintain believable contact/shadow, and choose a usable location.
5. Failure modes: accidental yaw/pitch/roll or mirroring, changed visible faces, product redraw, changed scale, guide remnants, the product moving without its support relationship, support moving while the room perspective does not, clipping/occlusion, and downstream paste mismatch.
6. A small controlled smoke-test matrix covering at least one laptop and one printer, close and wide framing where practical. Define what debug/prompt evidence and visual checks prove the intended prompt lineage. Separate mechanical success from visual acceptance.

Return:

- A short recommendation and explicit scale decision.
- Exact replacement wording or a minimal unified-diff-style proposal for the prompt constants/sections above. Do not write Python implementation logic beyond showing string changes.
- A contradiction checklist showing every remaining phrase that would still freeze x-y location or invite orientation drift.
- Smoke-test acceptance criteria.
- Risks and the cheapest follow-up if prompt-only translation is insufficient.

Do not recommend masks, compositing, automatic alignment repair, outpainting, multiple image retries, a new model, or a broad pipeline redesign. Do not weaken the exact orientation/view requirement.
