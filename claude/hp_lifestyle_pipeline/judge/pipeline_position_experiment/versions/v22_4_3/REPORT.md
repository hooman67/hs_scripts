# V22.4.3 structurally-unreliable affine dispatch report

## Decision

V22.4.3 is ready for root review. The candidate and a distinct full-160 package are prepared, but no endpoint, model call, or generation was launched for this version.

The V22.4.2.1 first row was rejected because each attempt produced exactly three SIFT matches. Three points are the mathematical minimum for a full affine, so OpenCV returned a numerically exact fit with three inliers, but the source landmarks occupied only one quadrant and less than 0.21% of the product-box area. The resulting scale, rotation, shear, and translation estimates were not meaningful measurements of the whole laptop.

V22.4.3 treats this as insufficient affine evidence, not as verified product deformation. For fixed-position inputs with the persisted RGBA product mask, it preserves the complete primary affine metrics, verdict, and reasons, then invokes the already-frozen alpha-mask fallback. Lower-fill inputs and reliable dense affine failures remain affine-only.

## Exact source change

- Guard version: `full-affine-v1.5-unreliable-affine-alpha-fallback`
- Pipeline version: `unified-blue-scale-v22.4.3-unreliable-affine-alpha-fallback-twin-camera-guide-only-no-edit-mask`
- New fallback gate requires all of:
  - `fixed_position=true`;
  - a persisted RGBA product mask; and
  - at least one failed affine reliability check among minimum inliers, source x/y span, source quadrant coverage, or source hull coverage.
- The public audit retains `primary_verdict`, `primary_reasons`, all primary affine metrics, the per-check reliability map, and `fallback_dispatch_reason`.
- The final verdict comes from the unchanged calibrated alpha fallback only after this narrow gate.

No threshold, prompt, camera policy, geometry policy, model-call policy, retry count, selection rule, or fallback implementation changed. The system prompts remain byte-identical:

- `system_3p.txt`: `bb02ad09f86a9a4aa4bdeac7c023d1ece0356ecef298853436af4781fa595ddf`
- `system_3p_fixed_position.txt`: `67e4d817a5a203912116bb99afbd6c4511d9a5c537b241cc6e980e34e75b1118`

Exact diffs:

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/invariants_v22_4_2_to_v22_4_3.diff`
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/pipeline_v22_4_2_to_v22_4_3.diff`
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/test_invariants_v22_4_2_to_v22_4_3.diff`

## Targeted failed-row result

The frozen V22.4.2.1 first row is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2_1/run/pipeline/rows/cashmere__laptop_BackRightCloseUp__p1`

- Attempt 1: primary affine still fails and all original reasons remain. The fallback passes at boundary coverage `0.811003`, internal-edge coverage `0.953368`, and translation `(+1, 0)` pixels.
- Attempt 2: primary affine still fails. The fallback rejects it at boundary coverage `0.734114`, despite internal-edge coverage `0.930570` and translation `(+1, -1)` pixels.
- Selection changes from no passing attempt under V22.4.2 to attempt 1 under V22.4.3.
- This matches visual inspection: attempt 1 preserves the laptop silhouette and placement; attempt 2 has weaker boundary agreement and remains rejected.

## Calibration replay

The complete frozen calibration replay is recorded in:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/replay_results.json`

- 31 real attempts: zero V22.4.2-to-V22.4.3 verdict changes.
- The real corpus contains one pre-existing label disagreement: both V22.4.2 and V22.4.3 pass the same lower-fill relocation artifact whose frozen label is `fail`. V22.4.3 induced zero new false accepts and zero new false rejects.
- 55 deterministic synthetic attempts: zero false accepts, zero false rejects, and zero metric mismatches against the frozen values.
- All fallback thresholds remain unchanged.

## Prior artifact replay

The replay discovered every prior smoke/full-run row with raw generated attempts and guard inputs.

- 60 schema-compatible rows replayed: 35 fixed-position and 25 lower-fill.
- Exactly one selection changed: the intended V22.4.2.1 first row changed from no selection to attempt 1.
- No other compatible prior selection changed.
- 25 older pre-guard rows were inventoried but could not be replayed because their historical result schema does not contain guide-density class or product bounds. Each skipped path and reason is explicit in `replay_results.json`; none was silently dropped.

## Tests

- Focused invariant tests: 9 passed.
- Full package suite: 172 passed.
- Ruff `F,E9,I`: passed.
- `git diff --check`: passed.
- New tests prove both sides of the gate:
  - a fixed-position RGBA input with a fitted but structurally insufficient affine dispatches to the fallback while preserving primary evidence;
  - a reliable dense affine failure caused by excess fixed-position translation does not dispatch to the fallback.

Logs:

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/pytest_full.log`
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/ruff.log`

## Preservation

- The V22.4.2.1 package manifest still verifies 14/14 files.
- Its failed run tree was read only; no file there was overwritten or adopted into the new package.
- The V22.4.3 package has a fresh run root, endpoint port, tmux names, experiment ID, S3 prefix, and freeze.

Preservation evidence:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/V22_4_2_1_PACKAGE_PRESERVATION_CHECK.txt`

## Prepared full-160 package

Package:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3`

Offline validation:

- exact 160 rows in 16 banks of 10;
- 13/13 wrapper contract tests;
- freeze verification passed;
- preflight passed;
- package lint and compilation passed;
- port `8131` was free;
- no `run/` or `logs/` tree exists;
- no launch occurred.

The launch command is prepared in `launch_tmux.sh` but was deliberately not executed.
