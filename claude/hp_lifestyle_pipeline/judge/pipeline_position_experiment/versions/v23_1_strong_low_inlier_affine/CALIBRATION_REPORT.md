# V23.1 strong low-inlier affine calibration

Date: 2026-11-06

## Decision

The narrow candidate resolves the Tassel `printer_FrontWide` false rejection
without changing any frozen or prior-suite decision from accepted V23 run 3.
The ordinary 20-inlier threshold remains intact.

A 17--19-inlier affine fit is accepted only when all of the following hold:

- inlier ratio is at least 0.70;
- source span is at least 0.70 horizontally and 0.60 vertically;
- inliers cover all four quadrants and at least 0.25 of the source hull;
- every existing non-count check passes, including scale, anisotropy, rotation,
  shear, affine residuals, rigid-translation residuals, frame containment, and
  fixed-position translation checks when recovery mode is active.

This is an alternative reliability path, not a lower global threshold. A
16-inlier fit, a 20-inlier fit, or any fit missing one strict gate cannot use the
exception. A normal fit with at least 20 inliers continues through the existing
path.

## Tassel pilot result

Both preserved attempts now pass through primary affine evidence, so the
incorrect alpha-fallback localizations are not used.

| Attempt | Mode | Inliers / matches | Ratio | Span x/y | Quadrants | Hull | Translation x/y | Prior | Candidate |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | all-view first attempt | 18 / 23 | 0.783 | 0.752 / 0.612 | 4 | 0.298 | 0.18 / -1.25 px | fail | pass |
| 2 | fixed recovery | 17 / 24 | 0.708 | 0.775 / 0.627 | 4 | 0.280 | -0.09 / -0.81 px | unverifiable | pass |

Under V23 policy, attempt 1 is selected. The public results include the full
metrics, thresholds, gate decisions, input hashes, and runtimes.

## Replay results

- Frozen synthetic: 110/110 mode checks matched expectation; zero false accepts
  and zero false rejects.
- Added adversarial suite: 82/82 matched expectation; zero false accepts, zero
  false rejects, and zero outcome mismatches.
- Accepted V23 run-3 comparison: all 31 real-proxy decisions, 110 frozen
  decisions, 82 added decisions, 113 prior-attempt decisions, and 95 prior row
  selections are identical. No prior selection changed.
- Historical real proxy: 1 false accept and 4 false rejects remain, exactly as
  in run 3. These labels are historical guard verdicts, not independent human
  truth, so they were reported and not optimized away.
- Brightness cases: 5/5 pass in all-view and 5/5 pass in fixed recovery.
- Large legal translations: 5/5 pass.
- High-fill/close legal-motion checks: 3/3 pass.
- Fixed recovery at 8 px: 5/5 pass. Fixed recovery at 9 px: 5/5 fail on
  `fixed_translation_x`; movement above 8 px remains rejected.
- Exact legal frame extremes and one-pixel crops: 20/20 return
  `unverifiable: silhouette_unobservable_at_canvas_boundary`.
- Rotation, isotropic scale, anisotropy, shear, and perspective-warp cases:
  30/30 fail.
- Dark substitutes: 5/5 fail. Valid products with a dark distractor: 5/5 pass.
- Duplicate product: explicitly unverifiable. Deterministic repeat: byte-equal.
- Full-resolution evidence: 81 checks at 2368x1776; median 379.5 ms, p95
  448.8 ms, max 462.6 ms. Full replay wall time was 640 seconds.
- Focused candidate tests: 5/5 pass, covering strict boundary values, every
  non-count invariant, and both raw Tassel attempts.

The 31 real-proxy attempts still report 1 historical-proxy false accept and 4
historical-proxy false rejects. Those are not accuracy estimates and are
unchanged from V23 run 3.

## Source identity and immutability

The Foundry source was read only and had the same SHA-256 before and after:

`8c1a8204d27eeb3ba922d6d9519113da7beeff9368301bcc9f8c9a7ec2fb2665`

Candidate-copy SHA-256 before and after:

`808bde48be35ba6093dc01d0cc23808f0c7f4509b62e79dce64d1033674c19a6`

No model calls or image generations were made. Accepted V23 run 3 was not
overwritten.

## Evidence

- Candidate source: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_1_strong_low_inlier_affine/candidate_invariants.py`
- Full replay: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_1_strong_low_inlier_affine/calibration/run_1/replay_results.json`
- Tassel replay: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_1_strong_low_inlier_affine/calibration/run_1/tassel_pilot_replay.json`
- Comparison with V23 run 3: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_1_strong_low_inlier_affine/calibration/run_1/comparison_to_v23_run3.json`
- Focused tests: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_1_strong_low_inlier_affine/calibration/candidate_tests.log`
- Exact commands: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_1_strong_low_inlier_affine/COMMANDS.md`

