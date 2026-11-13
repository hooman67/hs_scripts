# Product-LLM follow-up: camera-density conditional for v22.1

This is a bounded prompt-policy review for Adobe Firefly Foundry's HP image pipeline. Do not write application code. Review and tighten the exact model-facing language only.

## Fixed product invariant

The product is a fixed raster object. The only permitted change is rigid image-plane x-y translation. Exact pixel width and height, yaw/pitch/roll, visible faces, projection, perspective/foreshortening, silhouette, state, finish, details, full visibility and lack of occlusion must remain unchanged. Furniture/support and room may be recomposed independently beneath/around the chosen position. Stage A, guide renderer, schema, masks and image call stay unchanged.

## v22 evidence

v22 removed baseline preference and allowed independently recomposed support. An eight-fixture smoke produced these SIFT/RANSAC product-landmark affine estimates against the guide:

- Laptop close neutral: scale 0.8979, rotation +0.301°, translation +334,+38. Fail.
- Laptop close relocation demand: scale 0.8753, rotation +0.140°, translation -355,+62. Fail.
- Laptop wide neutral: scale 0.9984, rotation +0.029°, translation +2,+1. Pass.
- Laptop wide relocation: scale 1.0047, rotation +0.224°, translation +829,-10. Pass and visually successful recomposed support.
- Printer close neutral: scale 0.9755, rotation +0.344°, translation -155,+5. Exact-scale fail.
- Printer close relocation: scale 0.9567, rotation +0.196°, translation +499,-1. Exact-scale fail.
- Printer wide neutral: scale 1.0304, rotation +0.059°, translation -25,-246. Exact-scale fail.
- Printer wide relocation: scale 1.0693, rotation +1.688°, translation +674,-256. Scale/orientation fail.

The v22 policy demonstrated actual useful relocation in the wide laptop case, but high-fill views encouraged shrinking to make movement fit. We must not lose the successful support recomposition behavior.

## Required v22.1 policy

1. Camera-density conditional:
   - Close/high-fill view: the product occupies about 45% or more of either image width or height. Retain its initial x-y position by default. It may move only if exact pixel width and exact pixel height remain unchanged and the whole product stays inside frame.
   - Medium/wide lower-fill view: x-y position is free; choose for usability/composition and independently recompose support.
2. Universal hard fallback: never shrink, enlarge, zoom, reframe, rotate or reproject the product to make movement feasible. If a requested x-y move would require any such change or crop, retain the initial x-y position instead and recompose the support/room around it.
3. Put that fallback in the executable final image prompt, not only the Stage-B planning system.
4. Preserve all v22 rules for usable access, full base support, contact shadow, coherent perspective, printer square to support, laptop facing usable working edge, one product, no ghost/guide remnants.
5. Stage A/guide remain at baseline coordinates. The density class may be stated deterministically from existing guide bounds; this changes prompt text only.
6. Avoid unseen-image leakage. The final prompt may use `Image 1`, `guide`, `initial layout` and `current canvas`, but avoid standalone `reference`, `source image`, `style image` or unseen image numbering. Avoid the substring `preference` because an existing contract test rejects any `reference` substring.

Current v22 central language includes:

```text
Choose the product position for realistic use, access, support-surface geometry, furniture alignment, scene narrative or composition. Do not prioritize the initial position or baseline support distances. Retain the initial position when it already gives the best usable composition; do not force movement.

The only permitted change to the product is one rigid image-plane x-y translation. Keep its exact pixel width and height ...

At the chosen product position, compose ... support beneath its weight-bearing base. The support may change independently ...
```

The final check includes exact identity/view/scale and recomposed support, but does not yet say to retain the initial position rather than shrink when relocation is infeasible.

## Requested answer

Give:

1. Exact smallest replacement/additional text for the central policy block.
2. Exact one- or two-sentence deterministic density-class message for Stage B (`HIGH-FILL/CLOSE` versus `LOWER-FILL/MEDIUM-WIDE`).
3. Exact final executable prompt fallback wording.
4. Any hidden contradiction that could still induce shrinking or suppress valid wide relocation.
5. Focused assertions for the same eight-fixture rerun.

Do not propose masks, pixel pasting, image postprocessing, additional retries, Stage-A changes, coordinate repair, or extra image calls.
