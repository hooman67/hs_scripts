# V23 four-row pilot result

**Run:** 2026-11-06  
**Outcome:** stopped on row 4; not a scale-up pass

The frozen four-row pilot ran one immutable pipeline job per row and stopped on the first terminal
failure as designed. The endpoint was then stopped. No full-160 run began.

## Results

| Row | Attempts | Guard result | Measured translation |
|---|---:|---|---:|
| Cashmere laptop FrontCloseUp | 1 | pass | +1.23, -0.65 px |
| Cashmere laptop FrontWide | 1 | pass | -0.24, -0.17 px |
| Tassel printer FrontCloseUp | 1 | pass | -0.46, -1.16 px |
| Tassel printer FrontWide | 2 | first attempt failed; fixed recovery unverifiable | +0.18, -1.25 px; -0.09, -0.81 px |

The three completed rows passed on their first image attempt. The printer-wide first attempt had 18
inliers, 0.783 inlier ratio, four source quadrants, broad source span, strong hull coverage, and
passed every scale, rotation, shear, affine-residual and rigid-translation-residual check. It failed
only the frozen minimum of 20 inliers. Dispatching to the textureless full-frame fallback then
selected an unrelated scene location and failed boundary/appearance verification.

The fixed-position recovery had 17 inliers and similarly passed every transform, distribution and
fixed-translation check except the same 20-inlier minimum. Its alpha fallback selected a
canvas-boundary location and correctly returned fail-closed `unverifiable`.

Visual inspection of both printer-wide images shows the supplied printer view and scale retained.
This makes the terminal result a likely guard false rejection, not evidence that either generated
image violated rigid translation. The original 20-inlier threshold cannot simply be weakened from
one case; a narrowly defined strong-affine-evidence rule is being replayed against all frozen,
added and prior evidence before any rerun.

All four generated first attempts retained essentially the starting x-y position. The pilot
therefore verifies that the new prompt no longer forbids translation, but it does not yet provide
empirical evidence of a material product move. A follow-up pilot must include representative cases
whose composition gives the writer a reason to request relocation before scaling to 160.

## Evidence

Progress and terminal failure:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_all_view_translation/run/progress.json`

Printer-wide guard evidence:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_all_view_translation/run/pipeline/rows/tassel__printer_FrontWide__p1__outer_job_1/product_invariant_attempt_1.json`

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_all_view_translation/run/pipeline/rows/tassel__printer_FrontWide__p1__outer_job_1/product_invariant_attempt_2.json`

Contact sheet:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/pilot_v23_all_view_translation/run/four_row_pilot_contact_sheet.jpg`
