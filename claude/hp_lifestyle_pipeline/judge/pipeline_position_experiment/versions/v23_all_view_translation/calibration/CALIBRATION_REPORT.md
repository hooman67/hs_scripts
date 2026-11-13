# V23 all-view translation guard calibration — final run 3

**As of:** 2026-11-06  
**Scope:** read-only replay and deterministic guard calibration; no model calls or generations  
**Final guard:** `full-affine-v1.6-all-view-translation-alpha-fallback`  
**Final source SHA-256:** `8c1a8204d27eeb3ba922d6d9519113da7beeff9368301bcc9f8c9a7ec2fb2665`

## Result

The final guard passes both deterministic suites without a mismatch:

- frozen V22.4 synthetic replay: **110/110**, zero false accepts and zero false rejects;
- added V23 suite: **82/82**, zero false accepts, zero false rejects, and zero outcome mismatches.

The added suite contains 40 failures, 21 passes, and 21 fail-closed `unverifiable` results. All **81** 2368×1776 checks behave as expected, including three close/high-fill legal-motion cases.

Prior compatibility also improved:

- run 1 lost 12 previously selected outputs;
- run 2 lost five;
- final run 3 loses four and recovers eight of run 1's 12 losses without introducing a new loss;
- all four remaining losses are wide-view rows rejected by the rigid-translation residual checks;
- across 48 rows with observable old selections, nine selections differ: five old rejections gain a selection and four old selections are lost.

Historical real verdicts retain one proxy false accept and four proxy false rejects among 29 labeled attempts. They are regression proxies rather than independent human labels. The proxy acceptance is old residual-threshold drift; the proxy rejections are the same four rigid-translation residual failures visible in prior selection replay.

No threshold was weakened during calibration.

## Policy evaluated

- First scene attempt for every product, view, and occupancy class: `fixed_position=False`.
- Stage-B recovery only: `fixed_position=True`, retaining the ±8-pixel domain.
- Old failures caused solely by `fixed_translation_x` or `fixed_translation_y` were relabeled as legal V23 passes. Other historical labels were retained.
- Canvas-boundary evidence follows the fail-closed unobservable policy described below.

## Evidence summary

| Evidence set | Checks | False accepts | False rejects | Exact mismatches |
|---|---:|---:|---:|---:|
| Frozen real attempts | 29 labeled of 31 | 1 proxy | 4 proxy | 5 proxy |
| Frozen synthetic, both modes | 110 | 0 | 0 | 0 |
| Added V23 synthetic | 82 | 0 | 0 | 0 |
| Prior selection replay | 48 comparable of 95 | — | — | 9 selection changes |

All 95 compatible prior rows replayed successfully; none were skipped. Forty-seven lack an observable old guard-selection field and are excluded from the selection-change denominator.

## Final behavior

### Large movement and fixed recovery

For every one of the five preserved full-resolution silhouettes:

- a 12-pixel rigid x-y movement passes in all-view mode;
- the same movement fails in fixed-recovery mode on `fixed_translation_x`.

This confirms that first-attempt movement permission and bounded fallback are distinct policies.

### Canvas boundary and one-pixel crop

In-frame evidence cannot prove whether an outer silhouette touching the canvas edge is fully visible or clipped by one pixel. The final guard returns:

`unverifiable: silhouette_unobservable_at_canvas_boundary`

for all 10 exact-edge cases and all 10 one-pixel-crop cases. The generation pipeline treats `unverifiable` as rejection. This prevents false crop acceptance without claiming that unavailable off-canvas evidence proves a legal edge placement.

The duplicate-product case is also `unverifiable`, producing the added suite's 21st fail-closed result.

### Brightness compatibility

All five strong brightness-shift fixtures pass in both all-view and fixed-recovery modes. The four brightness false rejects seen in run 2 are resolved. The complete frozen synthetic result is therefore 110/110.

### Prior selections

Final run 3 recovers eight of run 1's 12 lost selections, including all close-up compatibility losses. Four previously selected wide-view rows remain rejected because matched landmarks do not fit one rigid translation closely enough:

- two Cashmere FrontWide rows;
- two Magic FrontWide rows.

They fail `translation_only_residual_median` and/or `translation_only_residual_p95`. The complete recovered and remaining paths are stored in `run_3/run_comparison.json`.

## Added synthetic coverage

- five preserved 2368×1776 product/camera silhouettes;
- identity and large legal translation;
- 10 exact frame-edge checks and 10 one-pixel-crop checks;
- five rotations, 10 scales, five anisotropic transforms, five shears, and five perspective warps after translation;
- five dark substitutes and five valid products with unrelated dark distractors;
- 10 fixed-recovery boundary checks at 8 and 9 pixels;
- one duplicate/ambiguity case;
- one strict deterministic repeat with identical canonical JSON.

All three `HIGH-FILL/CLOSE` large-translation checks pass. Density uses the production rule: product bounding-box width or height fraction at least 0.45.

## Runtime and determinism

For 81 direct full-resolution alpha checks at 2368×1776:

- median: **338.9 ms**;
- p95: **401.8 ms**;
- maximum: **415.2 ms**;
- aggregate: **27.59 s**.

The fresh end-to-end run, including 31 real attempts in both modes, 110 frozen synthetic mode checks, the added suite, and 95 prior rows, took **602 seconds**. Reliable affine passes do not invoke exhaustive alpha search; fallback search runs only when affine evidence is insufficient.

The deterministic repeat produced identical canonical JSON and result hashes.

## Verification and provenance

- Full Foundry test suite: **178 passed in 38.12 seconds** using `.venv312`.
- Guard source identity before and after run 3: `8c1a8204d27eeb3ba922d6d9519113da7beeff9368301bcc9f8c9a7ec2fb2665`.
- Run 3 used no run-1 or run-2 cache. Checkpoints are keyed by guard source SHA-256.
- The Foundry checkout was not edited by this calibration task.
- Historical evidence remains frozen under `run_1/` and `run_2/`; final evidence is under `run_3/`.
- Root result/checkpoint files mirror run 3 only after all run-3 checks completed.

## Reproduction

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
V23_CALIBRATION_OUT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_all_view_translation/calibration/run_3 \
  python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_all_view_translation/calibration/replay_v23_calibration.py
```

```bash
cd /home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25
.venv312/bin/pytest -q
```

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_all_view_translation/calibration/compare_runs.py
```

## Gate interpretation

The final guard passes all requested deterministic transform and frozen synthetic checks, restores all close-up compatibility losses, preserves fixed-recovery bounds, and fails closed at unobservable canvas boundaries. The four remaining wide prior-selection losses are the intended effect of enforcing one rigid x-y translation rather than allowing locally inconsistent landmark motion.
