# Full-affine product invariant guard calibration

Status: implemented for bounded smoke as pipeline policy v22.3; full-160 not authorized.

## Evidence set

All 28 available v22, v22.1, v22.2 and v22.2.1 fixtures were recomputed with one deterministic full-affine estimator. The raw row-level record, including matrices, singular values, residuals, landmark coverage and transformed corners, is in:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/affine_guard_calibration.json`

Labels reflect the prior root/human review and exact-contract outcomes. They are development labels, not population-level accuracy estimates.

## Frozen thresholds

- At least 20 full-affine RANSAC inliers and 0.55 inlier ratio.
- Both singular values between 0.98 and 1.02.
- Singular-value anisotropy ratio at most 1.02.
- Absolute polar-decomposition rotation at most 1.0°.
- Absolute column-angle/shear cosine at most 0.02.
- Inlier residual median at most 1.5 px and p95 at most 3.2 px.
- Source landmark spread at least 45% of product width and 40% of product height.
- At least three product quadrants and convex-hull area at least 12% of the product bounds.
- All four full-affine transformed product corners remain within the current canvas.
- HIGH-FILL/fallback attempts additionally require absolute x and y translation no greater than 8 px at 2368×1776.

These are measurement tolerances for an exact prompt contract, not permission to resize or rotate.

## Calibration rationale

The widest accepted full-affine case was the previously reviewed v22.1 printer wide relocation: singular values 0.9810/0.9960, rotation 0.884°, anisotropy 1.0153, residual p95 1.28 px, three quadrants and hull 0.198. The clean controls otherwise cluster much more tightly around unit singular values and zero rotation.

Known failures remain outside at least one threshold:

- v22.2.1 laptop wide: singular values 0.9717/0.9765.
- v22.2.1 printer wide: singular values 1.0384/1.0431 and rotation 1.120°.
- v22.2 printer wide: singular values 0.9630/1.0822, anisotropy 1.1238, rotation 6.018°, shear 0.1138, two quadrants and hull 0.070.
- Earlier close-view shrink cases have singular values roughly 0.87–0.96.

The thresholds separate the frozen accepted/rejected transform examples. The high-fill translation rule also rejects the formerly scale-preserving but policy-invalid printer close relocation.

## Bounded behavior

Attempt 1 uses the active density policy. Failed or unverifiable attempt 1 triggers exactly one extra image call from the same immutable guide with a hard fixed-position prompt override. Attempt 2 must pass the full matrix guard plus the fixed-position translation gate. Otherwise the row returns an explicit error, keeps both raw images/prompts/metrics, and publishes no selected `ours.png`.

The guard does not prove local pixel identity, lack of occlusion, product state, contact, or natural placement. Those remain separate evaluation dimensions.
