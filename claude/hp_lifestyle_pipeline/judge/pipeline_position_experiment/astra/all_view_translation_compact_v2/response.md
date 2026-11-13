## Recommendation

Make a narrow change: **allow translation on the first attempt for every view, and extend the existing RGBA verifier into a translation-only verifier shared by both attempts.** Keep the two-call limit and fail closed.

The important addition is that **a passing affine fit must not, by itself, select an output**. It cannot establish unchanged appearance, full visibility, or absence of a second product. Require mask/appearance verification after a geometrically acceptable affine fit as well.

Keep density classification for diagnostics or composition guidance, but remove it from placement permissions and guard selection.

## Prompt replacement

Use one common contract in `hp3p/prompts/system_3p.txt` and the executable GPT Image instruction assembled in `hp3p/pipeline.py`. Tell the Stage-B writer to preserve this contract without adding density-dependent exceptions.

> **PRODUCT PLACEMENT — ALL CAMERA VIEWS, INCLUDING CLOSE/HIGH-FILL:** Keep the product at its initial location, or reposition it using only one rigid image-plane x-y translation when that improves composition. This changes position only, not the product view or size.
>
> Preserve the exact product identity, orientation/view, yaw/pitch/roll, visible faces and camera-facing surfaces, projection, perspective, foreshortening, silhouette proportions, pixel width and height, state, finish, details, and logo/display content. Do not rotate, mirror, resize, shear, warp, reproject, redraw, crop, or occlude the product. Keep the entire product visible and inside the canvas.
>
> Recompose the support and room independently to create believable contact, perspective, access, and composition. Do not preserve the guide’s support edges, tabletop extents, or product-to-edge distances.
>
> Show exactly one product, at its final location, with no duplicate, ghost, or product remnant at the original location. If no safe translation exists, retain the initial x-y location. Preserve the guide’s exact output canvas dimensions.

Remove:

- Both existing `HIGH-FILL/CLOSE` and `LOWER-FILL/MEDIUM-WIDE` placement clauses.
- Any first-attempt “do not move,” “exact initial coordinates,” or “position locked” wording elsewhere.
- Any requirement to retain support boundaries, tabletop extents, or product-to-edge distances.
- Any generic instruction to preserve *all* guide geometry; scope preservation to the product.
- Redundant position directives that could override the common contract.

For recovery, **replace**, rather than append to, the first paragraph:

> **RECOVERY PLACEMENT:** Keep the product at its original x-y location. Recompose only the support and room. All product-preservation requirements below remain mandatory.

## Guard design

### 1. Preserve three outcomes

Return `pass`, `fail`, or `unverifiable`.

- `fail`: positive evidence of a forbidden change.
- `unverifiable`: insufficient, ambiguous, or unobservable evidence.
- Only `pass` can select an output. Both other outcomes consume the recovery attempt or terminate the run.

Keep the canvas-size check as an unconditional first check. A mismatch cannot be rescued by another verifier.

### 2. Decision hierarchy

```python
def guard(guide, output, bounds, rgba, fixed_position):
    if output.size != guide.size:
        return FAIL("canvas_size")

    affine = assess_existing_affine_evidence(...)

    if affine.structurally_reliable:
        # Preserve the existing reliability classification:
        # inliers and source spatial support, independently of transform quality.
        if affine.violates_geometry_or_residual_limits:
            return FAIL("reliable_affine_forbidden_change")

        # Fit y = x + d, not merely the translation column of a full affine.
        candidate = robust_translation(affine.inlier_correspondences)
        if not translation_residuals_pass(candidate):
            return FAIL("not_translation_only")

        placement = verify_rgba_translation(candidate, ...)
    else:
        # Three sparse matches must never become sufficient evidence.
        placement = search_and_verify_rgba_translation(
            allowed_domain(fixed_position), ...
        )

    if placement.verdict != PASS:
        return placement

    # Full-canvas search even during fixed-position recovery.
    uniqueness = check_duplicate_and_ghost_evidence(placement, ...)
    if uniqueness.verdict != PASS:
        return uniqueness

    return PASS(translation=placement.translation)
```

**Do not rescue a reliable affine that establishes rotation, scale, anisotropy, or shear through a better-looking mask match.** Conversely, do not interpret an arbitrary affine from three matches as evidence of either valid geometry or a reliable violation.

For a supported affine, estimate translation from the inlier displacements and evaluate residuals against that translation-only model. Retain the existing residual ceilings initially; do not silently fit another affine during appearance verification.

The current affine limits are **coarse rejection limits, not permission to change the product by 2% or 1°**. The common verifier must provide the additional evidence.

### 3. Smallest useful RGBA extension: global translation proposal, existing verification plus local checks

Split the existing fallback into:

1. Candidate translation search.
2. Verification at a supplied translation.

Keep the existing silhouette/internal-edge/high-pass machinery where possible. Expand its search domain and add the local appearance and uniqueness checks needed by the contract.

#### Reference preparation

Register the persisted cutout to the guide using its actual placement metadata/bounds. Do not estimate a new scale to make it fit.

Prepare:

- Full alpha support, including antialiased fringe.
- Outer silhouette and hole contours.
- An opaque, slightly eroded interior mask.
- Internal edges computed strictly inside the product.
- Source RGB and high-pass templates from the guide inside that mask.
- Fixed spatial partitions: contour sectors, interior tiles, and small source-detail patches covering logos, displays, controls, or other high-contrast components.

Do not incorporate diagram lines, table edges, shadows outside the product alpha, or guide background into the reference template.

If the cutout cannot be registered consistently to the guide, return `unverifiable`.

#### Full-canvas translation search

For the first attempt, search all offsets for which the **unchanged product bounds and full alpha support remain in frame**:

\[
-b_{left} \le dx \le W-b_{right},\qquad
-b_{top} \le dy \le H-b_{bottom}.
\]

There is no displacement preference or density-dependent cap. High-fill views simply have a smaller feasible domain.

Use deterministic, fixed-scale correlation maps over this entire domain:

- **Oriented silhouette chamfer score:** correlate the source contour with output edge-distance maps, separated into gradient-orientation bins. Use unsigned orientation because background contrast polarity may change.
- **Masked interior RGB error:** compute fixed-template squared-error maps by correlation/FFT.
- **Masked high-pass correlation/internal-edge score:** reuse the existing fallback signals.

These are translation searches—not scale, angle, perspective, or deformable-template searches. Table-edge alignment can propose a candidate but cannot validate it.

Search integer offsets globally, then refine surviving peaks locally at a documented subpixel resolution, using one fixed interpolation convention. Do not blur or normalize candidates until their differences disappear. Log the resulting registration uncertainty.

Cluster nearby offsets belonging to the same registration peak. Verify every competitive peak. A runtime cap is acceptable, but **hitting it while plausible candidates remain means `unverifiable`**, not “accept the best of the first K.”

#### Verification at each candidate

Require all of the following:

| Check | Required evidence |
|---|---|
| In-frame placement | Unchanged bounds and full alpha support fit inside the canvas, before rounding. |
| Silhouette | Matching contour position and normal direction around the whole object, including holes and every contour sector. |
| Internal geometry | Internal edges remain at their translated locations; no additional alignment transform. |
| Appearance | Both high-pass similarity and direct RGB comparison in the opaque interior. NCC alone cannot protect finish, color, or display content. |
| Local preservation | Per-tile and source-detail checks, not only a whole-product average. A small changed logo or occluder must not be diluted by a large blank face. |
| Observability | Enough actual edge/appearance evidence to support the conclusion. Missing evidence is not a perfect match. |

For a concrete starting configuration, use strict, versioned limits such as:

- Contour matching within one output pixel, with unsigned normal error at most 15°.
- At least 98% contour coverage overall and 95% in every fixed contour sector.
- High-pass NCC at least 0.98 globally and 0.95 in informative local patches.
- Opaque-interior absolute RGB error, in normalized `[0,1]` units: median at most `2/255`, p95 at most `6/255`; apply local limits to tiles and detail patches too.
- No per-candidate exposure, color, or local deformation fitting.

These are **proposed initial engineering thresholds, not validated guarantees**. Freeze them before evaluation; the test gate below must determine whether they are usable. If the existing fallback already has stricter validated limits, retain those.

A near-flat printer face can pass through its complete outline, panel geometry, a few distinctive controls, and direct interior appearance without having twenty SIFT landmarks. But if high-pass/internal evidence is undefined or uninformative, do not simply drop that term and let a rectangle-shaped room edge pass. A product with no usable distinguishing appearance must be `unverifiable`.

#### Exactly one product and no old-location ghost

Reuse the full-canvas score maps for a secondary-occurrence scan:

- Two distinct verified placements: `fail`.
- Explicitly examine the old location, excluding pixels occupied by the selected translated product.
- Search for partial remnants using coherent subsets of source contours and distinctive detail patches at a common second offset.
- Strong coherent duplicate/remnant evidence: `fail`.
- A plausible secondary occurrence that cannot be resolved: `unverifiable`.

Do not use a “best candidate wins” rule or only check the original location. A second product could appear elsewhere.

Do not treat arbitrary extra room edges as ghosts; require product-consistent appearance and geometry. Nevertheless, this remains a detection test, not a proof that every possible ghost is absent.

### 4. Mandatory `unverifiable` cases

At minimum:

- Sparse/unreliable affine evidence and no uniquely verified mask placement.
- Ambiguous registration peaks or excessive translation uncertainty.
- Insufficient silhouette contrast or missing verification coverage.
- No meaningful distinguishing internal appearance.
- Unresolved secondary-product evidence.
- Significant nonopaque product regions whose appearance cannot be checked with the available background information.
- Search exhaustion or inconsistent source-mask registration.

This deliberately prefers rejecting an otherwise good image to accepting a room edge as a printer.

## Retry policy

**Yes: use `fixed_position=False` on the first attempt for every view, and retain one fixed-position recovery attempt.**

```python
first = generate(all_view_translation_prompt)
g1 = guard(first, fixed_position=False)

if g1.verdict == "pass":
    select(first)
else:
    second = generate(fixed_position_recovery_prompt)
    g2 = guard(second, fixed_position=True)

    if g2.verdict == "pass":
        select(second)
    else:
        fail_run()
```

Both calls should use the original guide and source product, not the rejected generated output.

For the narrow diff, retain the existing recovery search of `[-8,+8]` per axis and its existing translation check. However, label this honestly: the prompt requests zero movement; the guard permits a small recovery displacement. Eight pixels is not proof of a fixed position. It is still compatible with the user’s overarching translation-only contract.

Use the same appearance, visibility, and duplicate checks for both attempts. A conservative placement policy must not become a weaker verification policy.

Persist:

- Both prompts and outputs.
- Existing affine diagnostics and structural-reliability reasons.
- Selected translation, bounds, registration uncertainty, and candidate scores.
- Contour coverage, local appearance failures, and duplicate-search findings.
- Guard configuration/version and selection/rejection reasons.

Select exactly one output; never select the “less bad” failed attempt.

## Tests and gates

### Synthetic guard tests

Build fixtures by compositing the real cutout into independently varied backgrounds. Include feature-rich, low-texture, and genuinely uninformative products.

| Group | Cases and expected result |
|---|---|
| Valid translations | Zero, small, large, diagonal, near-frame-limit, and subpixel translations; valid and observable cases pass. |
| Close/high-fill | Only a few pixels of legal motion; legal motion and zero motion pass. Out-of-frame placement fails. |
| Independent scene changes | Changed tabletop extents, support edges, room perspective, and product-to-edge distances must not themselves cause rejection. |
| Background distractors | Tables, windows, rectangles, repeated edges, product-colored walls; no background-only pass. |
| Affine violations | Rotation at 0.25°, 0.5°, 1°, and 2°; resize at 0.5%, 1%, 2%, and 5%; anisotropic resize and shear. Test especially below existing affine ceilings. |
| Non-affine violations | Perspective warp, mirror, local 1–4 pixel deformation, changed face/projection. |
| Crop/occlusion | One-pixel strips, corners, larger crops, small occluders over blank faces and over logos/controls. |
| Identity/appearance | Similar wrong model, changed logo/display, changed finish/color, altered panel geometry, redraw retaining enough landmarks to pass SIFT. |
| Ghosting | Full duplicate, faded duplicate, partial old-location remnant, overlapping small-shift ghost, duplicate elsewhere. |
| Reliability regression | Exactly three matches producing a nonsensical affine; broad reliable affine with forbidden geometry; missing or ambiguous mask evidence. |
| Infrastructure | Canvas mismatch, bad mask registration, capped search, deterministic repeated execution. |

**Synthetic gate:**

- No forbidden, distinguishable negative fixture may receive `pass`.
- Uninformative fixtures must be `unverifiable`, not false positives.
- Predeclare a useful valid-case acceptance target—e.g. at least 95% on observable fixtures, reported separately for rich/textureless and close/wide cases.
- Repeated runs must produce identical guard decisions and translations.
- Any accepted below-threshold rotation/resize injection falsifies the claimed protection; do not redefine it as allowed.

### Real GPT Image trials

Use a small fixed evaluation set: for example, 24 guides with six in each cell:

| | Feature-rich | Low-texture |
|---|---:|---:|
| Close/high-fill | 6 | 6 |
| Lower-fill/medium-wide | 6 | 6 |

Run two independent bounded pipeline trials per guide. Include:

- Close views with little movement room.
- Cases where unchanged placement is sensible.
- Cases with implausible baseline table extents or access.
- Plain printer faces with small logos/displays.
- Backgrounds likely to confuse edge matching.

Manually review every selected output and a sample of both rejection categories using translated-source overlays, difference views, and full-canvas ghost inspection.

**Rollout gate:**

- Zero observed invariant violations among selected outputs.
- Demonstrated valid nonzero translation in close/high-fill cases; otherwise the experiment has not tested the corrected policy.
- Demonstrated improvement in support/composition without retaining baseline support edges.
- A predeclared acceptable yield in each stratum; do not hide textureless failures in an aggregate.
- No more than two GPT calls, one selected output, complete audit artifacts, and no guard bypass.

If thresholds change after evaluation, rerun the gate on held-out cases.

## Limitations

**These inputs cannot prove the literal invariant set.** In particular:

- A redraw that produces identical pixels is indistinguishable from preservation.
- A textureless or symmetric product may not reveal orientation or identity changes.
- Tiny transforms, local edits, and occlusions can fall below rasterization or verification tolerances.
- The original alpha mask is not an independently observed output segmentation; complete silhouette and visibility are inferred.
- Arbitrary faint or heavily altered ghosts cannot be ruled out conclusively.
- The existing affine tolerances already admit some nonzero geometric change.

Accordingly, ship this only as a **conservative, measured translation verifier**, not an exact-preservation certificate. Keep the contract unchanged, expose uncertainty, and fail closed. If literal proof is a release requirement, the listed inputs and a generative image output are insufficient; the narrow patch cannot honestly provide it.
