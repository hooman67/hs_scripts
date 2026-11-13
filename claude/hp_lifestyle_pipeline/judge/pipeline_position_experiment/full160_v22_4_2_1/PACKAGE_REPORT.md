# V22.4.2.1 wrapper-only package report

## Outcome

Prepared and validated an isolated full-160 package. It has not been launched.

The prior V22.4.2 first-row pipeline execution produced the correct standard-branch artifacts, including `stage_b_attempt_1_request.json` and `stage_b_attempt_1_response.json`. The wrapper then incorrectly rejected the completed row because it required `planning_request.json` and `planning_response.json`, which are emitted only by the `reference_blue` branch. The frozen experiment calls `run_row` without `reference_blue`, so this was a wrapper contract defect rather than a pipeline, prompt, guard, or model failure.

## Exact scope

- New package revision: `hp-position-flex-v22.4.2.1-wrapper-v6.1-full160`
- Pipeline version remains: `unified-blue-scale-v22.4.2-affine-failure-alpha-fallback-twin-camera-guide-only-no-edit-mask`
- Foundry base commit remains: `8c358bc7989cb0e137e89db0fd325168249e2a22`
- Pipeline source hashes remain unchanged: `9d5faa0821ae2239fa17ab16c3b4335afdb4000a6842cbead1b847f75233b249` (manifest-map digest)
- Frozen input records: 160
- Banks: 16 × 10
- Prior failed V22.4.2 tree digest before and after preparation: `9dde0a63ddad1ec454f6a73fc00620097c279ef6c78b007252f9daa8bdeb5468`

The exact wrapper diff is stored in `WRAPPER_ONLY_DIFF.patch`. No file under `/home/colligo/foundry-pr4349-position-exp` was changed by this wrapper correction.

## Validation

- Freeze verification: pass
- Local preflight: pass
- Contract tests: 13/13 pass
- Python compilation: pass
- Ruff fatal/static-error selection (`E9,F63,F7,F82`): pass
- Port `8130`: free at preflight
- No `run/` tree exists
- No model calls were made

The tests prove that the standard branch passes without planning artifacts, rejects a missing Stage-B request, requires raw retry evidence for a second Stage-B call, verifies every declared artifact hash, and rejects a selected-output mismatch.
