# V22.4.1 full-160 treatment package report

Prepared at 2026-11-06T05:54:10Z. This is a preflight-only package. No endpoint, model generation, full-160 run, report build, or S3 upload was started.

## Package identity

- Package root: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_1`
- Experiment ID: `hp-position-flex-v22.4.1-v6.1-full160`
- Isolated run root: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_1/run`
- Local endpoint: `http://127.0.0.1:8128`
- Endpoint tmux session: `hp-v2241-full160-endpoint`
- Runner tmux session: `hp-v2241-full160-runner`
- Base worktree: `/home/colligo/foundry-pr4349-position-exp`
- Branch at preparation: `hshariati/hp-position-flex-exp-v22-4`
- Frozen base commit: `8c358bc7989cb0e137e89db0fd325168249e2a22`
- Pipeline version: `unified-blue-scale-v22.4.1-calibrated-080-alpha-textureless-invariant-fallback-twin-camera-guide-only-no-edit-mask`

## Frozen treatment sources

| Source | SHA-256 |
|---|---|
| `hp3p/prompts/system_3p.txt` | `bb02ad09f86a9a4aa4bdeac7c023d1ece0356ecef298853436af4781fa595ddf` |
| `hp3p/prompts/system_3p_fixed_position.txt` | `67e4d817a5a203912116bb99afbd6c4511d9a5c537b241cc6e980e34e75b1118` |
| `hp3p/pipeline.py` | `b0730eb08d036a139f34a3a95f36829984857d963f09d84d0e6e859de5285467` |
| `hp3p/geometry.py` | `f9d0f3a395624a150f9a9fed8c836394b66f041f6e212dc87c8b1a2322514a95` |
| `hp3p/grade.py` | `22169e7fc7fe3ebfd561bb3edd04edf4f1c630752444b752d388305c35bafbf6` |
| `hp3p/reference_blue.py` | `f36098543e208029226ae3b04ffd22c39edf7e168ab49dd5868e2185bd90661d` |
| `hp3p/invariants.py` | `a064e65cbedf2c3e3df92e78cebcce009bc3a4d6deb8ea57d2a26cc821d56b30` |
| `requirements.txt` | `cd1f9bbe9fb6526781e998279b6649e4b02b8a6f21a30e868386a7b86ba118b3` |

The frozen policy is V22.4.1 density-aware x-y translation with the full-affine guard, the calibrated alpha-masked fixed-position fallback for no/too-few descriptors at boundary agreement >= 0.80, and one bounded fixed-position image retry.

## Frozen V6.1 inputs

- Prompt export: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/revisions/v6.1-expanded-20261103-r6/exports/final/prompts_all_160.json`
- Prompt export SHA-256: `adcb9edb2643e45acb0cb882cdc4d65b8c256a52d58ad4a44ddd9c235287b3cd`
- Rows: 160
- Banks: 16
- Prompts per bank: 10, with every bank containing ranks 1 through 10
- Frozen record-list digest: `76b766d3b67b07ea948412904e7b6b0c4e709752d56fe726cc8bb70da579b1cd`
- Freeze manifest: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_1/freeze.json`
- Freeze manifest SHA-256: `dc86b061a64259e42d098df6b908e4265f7d81e05394c487ed303ab2823e5646`

Each of the 160 source record files is pinned separately in `freeze.json`. Selection, Stage-A geometry, and the geometry guide are replayed from those V6.1 records. Stage B and image generation are the live treatment steps.

## Execution and audit contract

- One endpoint worker and one serial runner.
- Exclusive progress lock and atomic progress replacement.
- Stop on the first row error. The runner has no automatic retry.
- Only the pipeline's single bounded fixed-position image retry is allowed.
- Resume refuses a preserved `first_error` and revalidates all completed rows.
- A completed row must have a guard-selected passing attempt.
- The selected output must hash-match its selected raw attempt.
- The provenance manifest must include and hash-validate the product input, RGBA alpha mask, reference, guide and geometry files, planning files, every Stage-B request/response, every image request/raw result, every invariant audit, and the live-call audit.

## Isolation and preservation

The preflight requires all treatment output paths to remain under `full160_v22_4_1`. It explicitly forbids the historical full-160 path, smoke treatment path, and the failed V22.3.3 run tree:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_3_3/run`

All 16 persisted hashes for the failed V22.3.3 first-row artifacts still match. The check output is in:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_1/V22_3_3_PRESERVATION_CHECK.txt`

At preflight time, port 8128 was free, both V22.4.1 tmux sessions were absent, and the V22.4.1 run tree did not exist.

## Validation result

- Freeze live verification: pass
- Fresh-package preflight: pass
- Contract tests: 7/7 pass, including a direct preflight rejection test against the V22.3.3 failed tree and a representative smoke-provenance test proving progress reads `selected_attempt` from `product_invariant_guard`
- Grouped-source validation: 160 rows, 16 banks, 10 prompts per bank
- V22.3.3 failed-row preservation: 16/16 hashes pass
- Endpoint/model calls from this package: 0
- S3 operations from this package: 0

The complete captured validation output is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_1/PREFLIGHT_VALIDATION.txt`

## Exact launch command

Run only after explicit root approval:

```bash
/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_1/launch_tmux.sh
```

This command runs preflight again, refuses tmux-session collisions, starts the endpoint on `127.0.0.1:8128`, waits for matching health, and only then starts the serial fail-fast runner.
