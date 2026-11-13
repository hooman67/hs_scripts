# V22.4.2 affine-failure dispatch report

## Decision

V22.4.2 is ready for root review and a deliberate full-160 launch decision. It has not made any model call.

The V22.4.1 first-row failure was caused by a narrow dispatch omission. Attempt 2 had four ratio-test matches, affine estimation returned `None`, and V22.4.1 stopped at `affine_fit_failed` even though its frozen alpha fallback passed that artifact. V22.4.2 applies the same fallback to this branch when and only when `fixed_position=true` and an RGBA mask is present.

## Exact change

- Guard version: `full-affine-v1.4-affine-failure-alpha-fallback`
- Pipeline version: `unified-blue-scale-v22.4.2-affine-failure-alpha-fallback-twin-camera-guide-only-no-edit-mask`
- Added dispatch from `affine_fit_failed` to `_assess_fixed_textureless` under the existing fixed-position plus RGBA-mask gate.
- Preserved `primary_verdict: unverifiable` and `primary_reasons: ["affine_fit_failed"]` in the audit.
- Preserved the fallback's final verdict and reasons as the public guard result.

No threshold, system prompt, geometry policy, generation prompt, retry count, or selection rule changed. The two system prompt SHA-256 values remain:

- `system_3p.txt`: `bb02ad09f86a9a4aa4bdeac7c023d1ece0356ecef298853436af4781fa595ddf`
- `system_3p_fixed_position.txt`: `67e4d817a5a203912116bb99afbd6c4511d9a5c537b241cc6e980e34e75b1118`

The exact source diff is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_2/invariants_v22_4_1_to_v22_4_2.diff`

## Tests and lint

- Focused invariant tests: 7 passed.
- Full documented suite: 170 passed.
- Documented lint command: passed.
- New tests force affine estimation failure and verify:
  - fixed-position plus RGBA dispatches to fallback, preserves the primary reason, and can pass;
  - absent mask or lower-fill input remains unverifiable and does not use fallback.

Logs:

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_2/pytest_full.log`
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_2/ruff.log`

## Frozen calibration replay

The replay uses the exact V22.4.1 calibration corpus and artifacts:

- 31 real attempts: zero V22.4.1-to-V22.4.2 dispatch changes.
- 55 deterministic synthetic attempts across five real silhouettes.
- Synthetic false accepts: 0.
- Synthetic false rejects: 0.
- Frozen metric mismatches at tolerance `5e-5`: 0.

All thresholds remain frozen:

- maximum translation: 8 px;
- minimum boundary coverage within 2 px: 0.80;
- minimum internal-edge floor: 0.20;
- minimum internal-edge acceptance: 0.80;
- high-pass override: 0.80;
- minimum internal-edge samples: 100.

Replay data:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_2/replay_results.json`

## Artifact replay

No model calls were made.

- Preserved failed V22.4.1 row, baseline replay: attempt 1 fails boundary; attempt 2 remains `affine_fit_failed`; no selection.
- Same row under V22.4.2: attempt 1 fails boundary; attempt 2 preserves `primary_reasons: ["affine_fit_failed"]`, then passes the alpha fallback at boundary `0.803566`, internal coverage `0.921244`, and translation `(0,-2)`; selected attempt is 2.
- Prior full-eight V22.4.1 artifacts: all eight selected attempts remain unchanged under V22.4.2.

## Preservation

- V22.3.3 failed first-row tree: 16/16 hashes pass.
- V22.4.1 failed full-160 tree: 23/23 hashes pass.
- V22.4.1 prepared package checksum manifest still passes.
- All source and evidence for V22.4.2 are frozen below this directory; older version directories were not altered.

## Prepared full-160 package

Package:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2`

Exact launch command, not executed:

```bash
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/launch_tmux.sh
```
