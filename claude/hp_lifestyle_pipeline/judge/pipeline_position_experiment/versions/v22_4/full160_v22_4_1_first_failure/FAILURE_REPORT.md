# V22.4.1 full-160 first-row failure diagnosis

## Conclusion

The serial runner behaved correctly and preserved the first failure, but the overall row rejection is **another guard false negative relative to the frozen V22.4.1 acceptance contract**.

- Attempt 1 was conservatively and consistently rejected by the calibrated alpha fallback: its boundary coverage was `0.781035`, below the frozen `0.80` threshold.
- Attempt 2 reached four SIFT ratio-test matches, both affine fits failed, and the guard returned `unverifiable: affine_fit_failed` without invoking the alpha fallback.
- A diagnostic, read-only replay of the unchanged V22.4.1 alpha fallback on attempt 2 passes every frozen check: boundary `0.803566`, internal edges `0.921244`, translation `(0,-2)` pixels, and `verdict: pass`.
- The contact sheet shows attempt 2 retaining the guide's lid outline, scale, orientation, visible faces, and internal structure. Its mismatch is concentrated along the lower/contact silhouette where the product meets the recomposed table. There is no visual or metric evidence of scale, rotation, or warp comparable to the synthetic rejects used for calibration.

The defect is control flow, not the `0.80` calibration threshold: fixed-position alpha fallback is called for `no_descriptors` and fewer than three matches, but not when a small, degenerate match set makes `estimateAffine2D` or `estimateAffinePartial2D` return `None`.

## Preserved failure

- Row: `cashmere__laptop_BackRightCloseUp__p1`
- Ordinal: 1 of 160
- Pipeline: `unified-blue-scale-v22.4.1-calibrated-080-alpha-textureless-invariant-fallback-twin-camera-guide-only-no-edit-mask`
- Persisted result: both attempts rejected; `selected_attempt: null`
- Progress: zero completed rows; `first_error` preserved
- Source run tree: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_1/run`

No run artifact was modified, deleted, regenerated, or resumed. No endpoint or model call was made during this diagnosis.

## Attempt comparison

| Evidence | New attempt 1 | New attempt 2 | Previous development attempt 1 | Previous development attempt 2 |
|---|---:|---:|---:|---:|
| Primary affine result | `too_few_matches` | `affine_fit_failed` | `too_few_matches` | `too_few_matches` |
| Good matches | 1 | 4 | 2 | 2 |
| Alpha fallback invoked in persisted run | Yes | **No** | Yes | Yes |
| Best translation | `(1,-1)` | `(0,-2)` diagnostic | `(1,-1)` | `(0,0)` |
| Boundary coverage within 2 px | `0.781035` | **`0.803566` diagnostic** | `0.832331` | `0.655255` |
| Boundary distance p90 | `3.2793 px` | `4.7750 px` diagnostic | `2.8650 px` | `4.7750 px` |
| Internal-edge coverage within 2 px | `0.925389` | **`0.921244` diagnostic** | `0.889119` | `0.956477` |
| High-pass NCC | `0.483042` | `0.384555` diagnostic | `0.502344` | `0.403151` |
| Frozen V22.4.1 fallback verdict | Fail | **Pass** | Pass | Fail |

The new and previous development comparisons use byte-identical guide, RGBA mask, and product input:

- Guide SHA-256: `e40edb10c76206ec3a83cd9a72039af3ce3855bef156cc807ecb116a6c3ad10e`
- Mask SHA-256: `2c22d6018a588964d249c00d206c3062686cbe560e8b9c3dda3e6715704d380f`
- Product input SHA-256: `3eab7a98c9915f892cfb811dce341730522b9c5ae70dcd75986553c51948ef7e`

The previous development attempt 1 is development evidence, not held-out validation. It is included only to interpret the new failure using the already frozen `0.80` rule.

## Visual interpretation

Attempt 1 preserves most of the upper lid but falls below the aggregate boundary gate. Its lower-half coverage is `0.7022` and bottom-quarter coverage is `0.6373`; the red overlay is concentrated along the base and contact edge. Rejecting it is consistent with the frozen gate.

Attempt 2 improves the top, right, and aggregate silhouette:

- upper-half coverage: `0.9434`
- right-half coverage: `0.9152`
- top-quarter coverage: `0.9389`
- right-quarter coverage: `0.9257`

Its weaker lower/contact edge explains the `4.775 px` p90, but p90 is diagnostic rather than a frozen fallback gate. Aggregate boundary coverage exceeds `0.80`, internal structure exceeds `0.80`, support is sufficient, and translation stays within eight pixels. Thus this exact artifact satisfies the calibrated alpha fallback that V22.4.1 claims to apply to texture-poor fixed-position products.

Contact sheet:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4/full160_v22_4_1_first_failure/contact_sheet.png`

Overlay legend: green is the translated source-alpha boundary within two pixels of an output edge; red is farther than two pixels; cyan marks output Canny edges.

Full diagnostic metrics:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4/full160_v22_4_1_first_failure/metrics.json`

## Required next decision

Do not resume this frozen V22.4.1 full-160 run. A separately versioned candidate should evaluate the same alpha fallback when a fixed-position product has `affine_fit_failed`, then replay calibration negatives and this preserved row before any new smoke or generation gate. The threshold should remain `0.80`; this failure does not support lowering it.
