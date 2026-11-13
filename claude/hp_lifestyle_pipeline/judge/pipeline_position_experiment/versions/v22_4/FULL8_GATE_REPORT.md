# V22.4.1 predetermined full-eight smoke gate

As of 2026-11-06, this gate ran the eight predetermined V22.3.3 smoke fixtures under the frozen V22.4.1 source hashes. The earlier `cashmere__laptop_BackRightCloseUp__p1` fresh retry is development evidence and is excluded from every result below. No full-160 run or S3 upload was started.

## Gate result

- Fixtures completed successfully: **8 / 8**.
- Guard-selected passing outputs: **8 / 8**.
- Passed on image attempt 1: **5 / 8**.
- Used the single bounded fallback and passed on attempt 2: **3 / 8**.
- Total raw image attempts: **11**.
- Unselected raw attempts, prompts, Stage-B audits, and invariant audits are preserved.
- Runner exit status: **0**.

The eight fixtures cover laptop/printer, close/wide, and retained-control/relocation-demand combinations.

## Selected invariant metrics

| Fixture | Selected | Singular values | Rotation | Translation px | Residual p95 |
|---|---:|---|---:|---:|---:|
| laptop close relocation | 1 | 1.00055, 0.99903 | 0.047° | +0.65, -0.42 | 2.192 |
| laptop close retained | 2 | 1.00010, 0.99870 | 0.021° | +1.25, -1.28 | 2.201 |
| laptop wide relocation | 2 | 0.99935, 0.99585 | 0.104° | +1.26, -0.51 | 2.929 |
| laptop wide retained | 1 | 1.00604, 1.00580 | 0.080° | -5.01, -12.42 | 2.011 |
| printer close relocation | 1 | 1.00017, 0.99619 | -0.018° | +0.60, +0.72 | 2.599 |
| printer close retained | 1 | 1.00101, 0.99946 | 0.038° | -0.41, -1.19 | 1.627 |
| printer wide relocation | 2 | 1.00023, 0.99824 | 0.121° | +2.15, -1.23 | 1.195 |
| printer wide retained | 1 | 1.00041, 0.99530 | 0.092° | +3.32, +2.72 | 0.891 |

The laptop-wide retained fixture is lower-fill, so its translation is intentionally not subject to the fixed-position eight-pixel limit.

## Rejected first attempts

Three first attempts were rejected and never selected:

- laptop close retained: scale below threshold and fixed x/y translation outside tolerance;
- laptop wide relocation: scale below threshold;
- printer wide relocation: scale above threshold.

Their one bounded replacements passed and were selected.

## Scope limitation

All eight fixtures had enough SIFT landmarks for the primary affine guard. Therefore this gate verifies that V22.4.1 preserves the established affine behavior and bounded retry contract, but it does not independently exercise the new alpha-mask fallback. Evidence for that fallback remains the independent 31-real/55-synthetic calibration plus the explicitly labeled development retry; it is not counted in this full-eight gate.

## Artifacts

- Gate manifest: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/v22_4_1_guard/manifest.json`
- Compact audit summary: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/v22_4_1_guard/gate_summary.json`
- Aggregate contact sheet: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/v22_4_1_guard/all_fixtures_contact_sheet.jpg`
- Per-fixture contact sheets and raw artifacts: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/smoke/v22_4_1_guard/`
