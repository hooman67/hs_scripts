# V22.4.2 full-160 treatment package report

This package is prepared for root review only. No V22.4.2 endpoint, image generation, full-160 run, report build, or S3 upload has been started.

## Identity

- Root: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2`
- Experiment: `hp-position-flex-v22.4.2-v6.1-full160`
- Run root: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/run`
- Port: `127.0.0.1:8129`
- Sessions: `hp-v2242-full160-endpoint`, `hp-v2242-full160-runner`
- Base commit: `8c358bc7989cb0e137e89db0fd325168249e2a22`
- Pipeline: `unified-blue-scale-v22.4.2-affine-failure-alpha-fallback-twin-camera-guide-only-no-edit-mask`
- Freeze SHA-256: `5825031b902a8bfd7ff6e71fbb86584026c846309bbda77c5ff13e8db0c4d66b`

## Treatment contract

The only policy change from V22.4.1 is dispatch: when fixed-position affine estimation returns `affine_fit_failed` and the RGBA mask exists, the unchanged calibrated alpha fallback runs and the audit preserves `primary_reasons: ["affine_fit_failed"]`. System prompts and all thresholds are unchanged.

The package freezes the same 160 V6.1 records: 16 device/camera banks, 10 ranked prompts per bank. Selection, Stage-A geometry, and geometry guide are replayed; Stage B and image generation are live.

Execution remains serial, locked, atomic, stop-on-first-error, and resumable only after validation. Every completed row must preserve and hash-check all inputs, the RGBA mask, planning/geometry/Stage-B requests and responses, every raw image attempt, invariant audits, live-call audits, and the guard-selected image.

The V22.3.3 and V22.4.1 failed run roots are explicit forbidden destinations and have direct contract tests.

## Frozen source hashes

| Source | SHA-256 |
|---|---|
| `hp3p/prompts/system_3p.txt` | `bb02ad09f86a9a4aa4bdeac7c023d1ece0356ecef298853436af4781fa595ddf` |
| `hp3p/prompts/system_3p_fixed_position.txt` | `67e4d817a5a203912116bb99afbd6c4511d9a5c537b241cc6e980e34e75b1118` |
| `hp3p/pipeline.py` | `313397818a0784d648e11a2c7bfc0d9623219808c751274129dd2151c780e0b8` |
| `hp3p/geometry.py` | `f9d0f3a395624a150f9a9fed8c836394b66f041f6e212dc87c8b1a2322514a95` |
| `hp3p/grade.py` | `22169e7fc7fe3ebfd561bb3edd04edf4f1c630752444b752d388305c35bafbf6` |
| `hp3p/reference_blue.py` | `f36098543e208029226ae3b04ffd22c39edf7e168ab49dd5868e2185bd90661d` |
| `hp3p/invariants.py` | `8612a4f164f76503ee3e6acee56cc079081df40b2955a185a6ef50f69dd5ac7c` |
| `requirements.txt` | `cd1f9bbe9fb6526781e998279b6649e4b02b8a6f21a30e868386a7b86ba118b3` |

## Offline gate

- Foundry package tests: 170 passed
- Foundry lint: passed
- Full-160 package contract tests: 8 passed
- Frozen calibration replay: 31 real attempts, zero dispatch changes
- Synthetic replay: 55 attempts, zero false accepts, zero false rejects, zero metric mismatches
- Prior V22.4.1 full-eight replay: 8/8 selections unchanged
- Failed V22.4.1 first row: baseline selects none; V22.4.2 deterministically selects attempt 2
- V22.3.3 preservation: 16/16 hashes
- V22.4.1 preservation: 23/23 hashes

## Exact launch command

Run only after explicit root approval:

```bash
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_2/launch_tmux.sh
```
