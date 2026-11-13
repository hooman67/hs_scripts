# Deterministic product-affine guard proposal

Status: proposal pending fresh v22.2.1 smoke and root review. No implementation or full-160 launch yet.

## Scope

The image model may translate the product only in LOWER-FILL; it may not change scale, orientation, projection, crop, or identity. HIGH-FILL may not translate. The guard compares product landmarks in the immutable geometry guide against the generated scene. It is a contract gate, not an aesthetic score or best-of selector.

## Provisional measurable contract

Use SIFT features detected only inside the guide's product bounds and matched against the full output. Fit a partial affine transform with deterministic RANSAC seed and record every raw match and matrix.

- Verifiable fit: at least 20 RANSAC inliers and at least 50% inlier ratio. Insufficient evidence is `unverifiable`, never an automatic pass.
- Scale: `abs(scale - 1.0) <= 0.01`.
- Rotation: `abs(rotation_deg) <= 0.75`.
- HIGH-FILL translation: `abs(tx) <= 8 px` and `abs(ty) <= 8 px` at 2368×1776. Scale and rotation thresholds also apply.
- LOWER-FILL translation: unrestricted, provided transformed product corners remain fully inside the canvas. Scale and rotation thresholds still apply.

These are measurement tolerances, not permission to resize or rotate. Prompt contract remains exact.

Evidence for the provisional scale/rotation bands:

- Clean/fixed controls: scale 0.9986–1.0029, rotation 0.011–0.125°.
- Accepted relocation diagnostics: v22 laptop wide 1.0047/0.224°; v22.1 printer wide 0.9932/0.583°.
- Rejected relocation diagnostics: v22.2 laptop wide 0.9707 scale; v22.2 printer wide 2.808° rotation.

## One bounded fallback attempt

1. Generate attempt 1 under the active branch and save image, final prompt, Stage-B response, request, matrix, matches, thresholds, and verdict.
2. If attempt 1 passes, publish it.
3. If attempt 1 fails or is unverifiable, make exactly one additional image call from the same immutable guide. Add a deterministic fixed-position override: keep exact initial x-y, exact pixel size, exact orientation/view/projection, and independently compose support/room around it. This retry is the fixed-position fallback, not another free relocation draw.
4. Run the same guard on attempt 2, including the HIGH-FILL translation threshold.
5. If attempt 2 passes, publish attempt 2 and retain attempt 1 as rejected provenance. If attempt 2 fails/unverifiable, return an explicit contract error and retain both attempts. Never silently publish either failure and never manually repair pixels.

The retry reuses the already accepted Stage-B scene plan where compatible, removes conflicting product-position clauses, and changes no Stage A geometry, guide bytes, camera metadata, product pixels, seed/settings, or user prompt.

## Limitations and companion checks

A partial-affine fit measures landmark scale, in-plane rotation, and translation. It does not by itself prove full silhouette fidelity, absence of local warp, correct device state, unoccluded edges, contact, or natural placement. Preserve the existing placement judge and add deterministic checks for transformed-corner in-frame status. A future local-warp/coverage diagnostic can be calibrated separately; it should not be invented from this small smoke set.
