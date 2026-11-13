# Design review: translation-only product placement for every camera view

You are reviewing one narrow product image-generation experiment in Adobe Foundry's HP pipeline. Give a concrete design recommendation; do not write a broad essay. The integration uses GPT Image to turn a geometry guide containing the real product into a photographic scene.

## User decision and non-negotiable contract

The previous experiment allowed product translation only for lower-fill/medium-wide views and fixed high-fill/close views. Hooman has corrected that policy: **every camera view, including high-fill and close-up views, may move the product by at most one rigid image-plane x-y translation when useful for a believable composition.**

For every view:

- Product x-y coordinates may change.
- Exact identity, orientation/view, yaw/pitch/roll, visible faces, camera-facing surfaces, projection, perspective, foreshortening, silhouette proportions, pixel width, pixel height, state, finish, details, logo/display content, and full visibility must remain fixed.
- Rotation, mirror, resize, shear, warp, reprojection, redraw, crop, and occlusion are forbidden.
- The support and room may recompose independently around the translated product. Do not preserve baseline support edges, tabletop extents, or product-to-edge distances.
- The output must contain exactly one product and no ghost at the old location.
- If no safe translation exists, keeping the initial x-y location is allowed.

The goal is to let GPT Image make tables, room perspective, access, and composition more believable without changing the product view needed by downstream pixel replacement.

## Exact checkout and current behavior

Checkout: `/home/colligo/foundry-pr4349-position-exp`, base commit `8c358bc7989cb0e137e89db0fd325168249e2a22`.

The current experimental prompt repeats this density split in `hp3p/prompts/system_3p.txt` and `hp3p/pipeline.py`:

```text
HIGH-FILL/CLOSE: Preserve the product's exact initial x-y coordinates ... do not move the product.
LOWER-FILL/MEDIUM-WIDE: Choose product x-y freely ... using rigid image-plane translation only.
```

Current pipeline selection:

```python
fixed_position = res["guide_density_class"] == "HIGH-FILL/CLOSE"
first_guard = assess_product_affine(
    guide, gpt, product_bounds_px,
    fixed_position=fixed_position,
    product_mask=mask,
)
if first_guard["verdict"] == "pass":
    select first output
else:
    make one second GPT Image call using a fixed-position fallback prompt
    assess second output with fixed_position=True
    fail if second guard also rejects
```

The requested policy implies the first guard should permit translation for all views, while the bounded second attempt may still be a conservative fixed-position recovery if that is the safest design.

## Current primary affine guard

`assess_product_affine` detects SIFT landmarks inside the original product bounds, matches them against the full output, fits a full affine transform with RANSAC, then checks:

```python
THRESHOLDS = {
  "min_inliers": 20, "min_inlier_ratio": 0.55,
  "singular_min": 0.98, "singular_max": 1.02,
  "max_anisotropy_ratio": 1.02,
  "max_abs_rotation_deg": 1.0,
  "max_column_shear_cos": 0.02,
  "max_residual_median_px": 1.5, "max_residual_p95_px": 3.5,
  "min_source_span_x_fraction": 0.45,
  "min_source_span_y_fraction": 0.40,
  "min_source_quadrants": 3,
  "min_source_hull_fraction": 0.12,
  "max_fixed_translation_px": 8.0,
}
```

It decomposes the 2x2 affine linear part, checks singular values, anisotropy, rotation, shear and residuals, checks source landmark spatial support, transforms the four source bounds corners, and requires all transformed corners in frame. Translation is checked only when `fixed_position=True`. A reliable dense affine that fails rotation/scale/shear must fail.

## Textureless-product problem

Some products, especially plain printer faces, have few useful SIFT features. The current RGBA-mask fallback is **fixed-position only**. It has the original product alpha mask and guide/output images, searches dx/dy only in `[-8,+8]`, and evaluates translated source silhouette-boundary edge coverage plus internal-edge coverage/high-pass NCC. It cannot verify arbitrary x-y translation. It is currently dispatched only when `fixed_position=True` and affine evidence is absent or structurally unreliable.

A real failed case had exactly three sparse SIFT matches, enough to fit a meaningless affine and bypass an earlier fallback. A later patch classified affine evidence as unreliable when any of inliers/span-x/span-y/quadrants/hull checks failed. This protected fixed-position textureless products, but still does not solve translation verification.

The pipeline has:

- the geometry-guide PNG containing the product and diagram;
- a persisted RGBA product cutout/mask used to build the guide;
- the generated output PNG;
- original product bounds;
- no requirement to preserve x-y position;
- no edit mask sent to GPT Image.

## What I need from you

Recommend the **smallest high-quality prompt/code-policy change** that implements all-view translation while preserving the invariants above.

Answer these exact questions:

1. What exact prompt clauses should replace the density split? Provide compact replacement text suitable for both the Stage-B writer and the executable GPT Image instruction. Identify redundant/contradictory clauses to remove.
2. Should the first attempt use `fixed_position=False` for all views and retain one fixed-position fallback attempt after guard failure? If not, specify a safer bounded retry policy.
3. Design a deterministic guard that accepts arbitrary rigid x-y translation but rejects rotation, scale, anisotropy, shear, warp, crop, occlusion, redraw, or identity drift. It must work for feature-rich and textureless products. Use only the inputs listed above and explain the decision hierarchy.
4. For textureless products, propose the smallest implementable extension to the RGBA fallback. Be precise about how to search or estimate x-y over the full canvas without accidentally matching table/room edges, and how to verify silhouette plus internal appearance. State when the result must be `unverifiable` rather than pass.
5. Give a focused test matrix and rollout gate that can falsify the design. Separate synthetic guard tests from real GPT Image trials. Include close/high-fill cases and failure injections for rotation, resize, shear, crop, occlusion, ghosting, and wrong-product/redraw.

Favor a narrow diff over a redesign. Preserve audit artifacts, deterministic thresholds, one selected output, fail-closed behavior, and the existing hard requirement that output canvas size equal the guide canvas size. Flag any invariant that cannot actually be proven from these inputs.

Format the response as: `Recommendation`, `Prompt replacement`, `Guard design`, `Retry policy`, `Tests and gates`, `Limitations`. Include pseudocode only where it makes the design unambiguous.
