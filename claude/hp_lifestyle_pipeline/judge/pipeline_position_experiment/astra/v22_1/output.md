## 1. Central policy: smallest replacement

Replace only the first paragraph quoted in the question with the following. Keep the existing rigid-product invariant and independently recomposed-support paragraphs unchanged.

```text
For HIGH-FILL/CLOSE views, retain the initial x-y position by default. A move is permitted only if the exact product pixel width and height and all other product invariants remain unchanged and the whole product stays inside the current canvas.

For LOWER-FILL/MEDIUM-WIDE views, choose the product x-y position freely for realistic use, access, support-surface geometry, furniture alignment, scene narrative or composition. Do not prioritize the initial position or baseline support distances. Retain the initial position when it already gives the best usable composition; do not force movement.

For either density class, never shrink, enlarge, zoom, reframe, rotate or reproject the product to make an x-y move feasible. If a requested move would require any such change, alter the exact product pixel width or height, or crop any part of the product, retain the initial x-y position in the guide instead and independently recompose the support and room around it.
```

This preserves free wide-view placement without making the close-view default universal. The existing full invariant remains authoritative in both branches.

## 2. Deterministic Stage-B density message

Use the existing **product** guide bounds divided by the current canvas dimensions—not furniture bounds or the fixture’s camera-name label. Operationalize “about 45%” as **at least 45%** for deterministic selection.

Emit exactly one of these messages:

**HIGH-FILL/CLOSE**
```text
Guide-density class is HIGH-FILL/CLOSE: the existing product guide bounds occupy at least 45% of the current canvas width or height. Apply the high-fill initial-position default and its exact-size, fully-in-frame movement condition.
```

**LOWER-FILL/MEDIUM-WIDE**
```text
Guide-density class is LOWER-FILL/MEDIUM-WIDE: the existing product guide bounds occupy less than 45% of both current canvas dimensions. Choose x-y position freely for usable composition and independently recompose the support, subject to all fixed-product invariants and the universal fallback.
```

Equality belongs to HIGH-FILL/CLOSE. These labels describe guide occupancy; they are not instructions to change the camera or framing.

## 3. Final executable prompt fallback

Include this verbatim in the executable image prompt, alongside the complete product invariant—not only in planning instructions or a planning checklist:

```text
For either density class, never shrink, enlarge, zoom, reframe, rotate or reproject the product to make an x-y move feasible. If a requested move would require any such change, alter the exact product pixel width or height, or crop any part of the product, retain the initial x-y position in the guide instead and independently recompose the support and room around it.
```

The executable prompt must also carry the applicable density branch. A class label and universal fallback alone would not communicate the high-fill default.

## 4. Remaining contradictions to guard against

- **Leaving the old opening paragraph elsewhere:** A global “do not prioritize the initial position” conflicts with the high-fill default. Scope it to lower-fill views only.
- **Treating support geometry as fixed:** An unsuitable initial desk or printer stand does not make translation infeasible. Recompose the support independently before concluding that the requested position requires product distortion.
- **Solving alignment by rotating the product:** “Printer square to support,” “laptop facing the usable working edge” and “coherent perspective” must be satisfied by arranging furniture and room around the unchanged product view—not by turning or reprojecting the product.
- **Treating density as a camera instruction:** Other wording such as “zoom out,” “fit everything,” or “create more breathing room” can silently reintroduce shrinking. Product dimensions override such composition goals.
- **Turning defaults into mandates:** High-fill does not mean “never move.” Lower-fill does not mean “must move.” An infeasible requested move triggers initial-position fallback, not a smaller product or a substitute clamped move.

Preserve full base support, usable access, contact shadow, one product, full visibility, no occlusion and no ghost/guide remnants in both relocation and fallback outcomes.

## 5. Focused eight-fixture rerun assertions

### Text and setup assertions

- Stage A, guide placement, renderer, schema, masks and image call remain unchanged.
- Density is selected from existing guide bounds using the inclusive 45% test.
- The executable prompt contains the active branch, universal fallback and existing product/support constraints.
- Reject unseen-image labels and the forbidden substring, including occurrences embedded in longer words.

### Fixture assertions

Apply each row to **both laptop and printer**, covering all eight fixtures. Use the computed density class if a fixture name disagrees with its bounds.

| Fixture condition | Position assertion |
|---|---|
| Close neutral, classified HIGH-FILL | Initial x-y is the default; reject gratuitous movement undertaken merely to improve framing. |
| Close relocation demand, classified HIGH-FILL | Movement is permitted only with unchanged dimensions/view and full in-frame visibility. An infeasible requested move must retain initial x-y, not shrink-to-move. |
| Wide neutral, classified LOWER-FILL | Either initial placement or useful rigid translation is acceptable; neither movement nor retention is mandatory. |
| Wide relocation demand, classified LOWER-FILL | For a feasible request, useful relocation with independently recomposed support is the behavioral success condition. Infeasible requests must fall back without product changes. |

### Across all eight

- Require exact product pixel width and height, unchanged view/identity/state/finish/details, and translation-only landmark behavior.
- Reject scale, rotation, shear, reprojection, cropping and occlusion; do not introduce a new “close enough” product-scale allowance.
- Check usable access, full weight-bearing-base support, contact shadow and coherent furniture alignment at the resulting position.
- Specifically retain the wide-laptop relocation success: useful movement and recomposed support, not a blanket return to initial placement.
- Treat SIFT/RANSAC affine estimates as diagnostics. Near-unit estimated scale and near-zero estimated rotation alone do not prove exact raster preservation.
