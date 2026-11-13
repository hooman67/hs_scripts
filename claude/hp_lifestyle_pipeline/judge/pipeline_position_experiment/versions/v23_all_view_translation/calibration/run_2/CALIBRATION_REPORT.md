# V23 all-view translation guard calibration — corrected run 2

**As of:** 2026-11-06  
**Scope:** read-only replay and deterministic guard calibration; no model calls or generations  
**Run-2 guard:** `full-affine-v1.6-all-view-translation-alpha-fallback`  
**Run-2 source SHA-256:** `67cdf7608b6315792542ad95dadf15fafc5f41f879116a14463b5d6b11531ccb`  
**Run-1 source SHA-256:** `1fead3c08c441bf361a4878d2945265a6ce6398f24fbd379a77b9243a556402d`

## Result

The corrected guard passes the purpose-built V23 suite with **82/82 exact expected outcomes**: 40 failures, 21 passes, and 21 fail-closed `unverifiable` results. It has zero false accepts, zero false rejects, and zero outcome mismatches on this suite. All **81** 2368×1776 checks behave as expected, including three close/high-fill legal-motion cases.

Compatibility improved substantially over run 1:

- run 1 lost 12 previously selected outputs;
- run 2 recovers seven of those 12 and loses no new selection;
- five formerly selected outputs remain rejected: four wide-view rows fail the rigid-translation residual checks, and one close-up fails the silhouette-boundary check;
- across all 48 rows with observable old selections, nine selections differ in run 2: four old rejections gain a selection and five old selections are lost.

The frozen V22.4 synthetic corpus still has **four false rejects and zero false accepts** across 110 mode checks. All four are strong brightness-shift positives on two fixtures, each evaluated in both all-view and fixed-recovery modes. Three other brightness fixtures pass both modes.

Historical real verdicts retain one proxy false accept and four proxy false rejects among 29 labeled attempts. These are regression proxies, not independent human labels. The one proxy acceptance is old residual-threshold drift; the four proxy rejections are the intentional rigid-translation residual checks.

No threshold was weakened during calibration.

## Policy evaluated

- First scene attempt for every product, view, and occupancy class: `fixed_position=False`.
- Stage-B recovery only: `fixed_position=True`, retaining the ±8-pixel domain.
- Old failures caused solely by `fixed_translation_x` or `fixed_translation_y` were relabeled as legal V23 passes. Other historical labels were retained.
- Canvas-boundary evidence follows the corrected fail-closed policy described below.

## Evidence summary

| Evidence set | Checks | False accepts | False rejects | Exact mismatches |
|---|---:|---:|---:|---:|
| Frozen real attempts | 29 labeled of 31 | 1 proxy | 4 proxy | 5 proxy |
| Frozen synthetic, both modes | 110 | 0 | 4 | 4 |
| Added V23 synthetic | 82 | 0 | 0 | 0 |
| Prior selection replay | 48 comparable of 95 | — | — | 9 selection changes |

All 95 compatible prior rows replayed successfully; none were skipped. Forty-seven lack an observable old guard-selection field and are excluded from the selection-change denominator.

## Specific corrected-guard behavior

### Large movement and fixed recovery

For every one of the five preserved full-resolution silhouettes:

- a 12-pixel rigid x-y movement passes in all-view mode;
- the same movement fails in fixed-recovery mode on `fixed_translation_x`.

This confirms that first-attempt movement permission and bounded fallback are distinct policies.

### Canvas boundary and one-pixel crop

The available in-frame evidence cannot prove whether an outer silhouette touching the canvas edge is fully visible or clipped by one pixel. The corrected guard therefore returns:

`unverifiable: silhouette_unobservable_at_canvas_boundary`

for all 10 exact-edge cases and all 10 one-pixel-crop cases. The generation pipeline treats `unverifiable` as rejection. This avoids falsely accepting a crop without claiming that a legal exact-edge placement can be verified from unavailable off-canvas evidence.

The duplicate-product case is also `unverifiable`, producing the added suite's 21st fail-closed result.

### Brightness compatibility

Brightness-shift outcomes by fixture, in both modes:

- pass: Cashmere FrontCloseUp, Cashmere FrontWide, Magic FrontWide;
- fail: Cashmere BackRightCloseUp, Magic FrontCloseUp.

The two failing fixtures do not satisfy the frozen `structure_or_appearance` evidence requirement after the strong synthetic shift. This produces four frozen-mode false rejects. The result is preserved rather than hidden through threshold adjustment.

### Previously lost selections

Run 2 recovers seven of run 1's 12 lost selections. Five remain rejected:

- four wide-view rows fail `translation_only_residual_median` and/or `translation_only_residual_p95`;
- Cashmere BackRightCloseUp prompt 4 fails alpha-boundary coverage: 0.7792 against the unchanged 0.80 threshold.

The complete recovered and remaining row paths are in `run_2/run_comparison.json`.

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

- median: **299.3 ms**;
- p95: **310.9 ms**;
- maximum: **315.3 ms**;
- aggregate: **23.74 s**.

The fresh end-to-end run, including 31 real attempts in both modes, 110 frozen synthetic mode checks, the added suite, and 95 prior rows, took **545 seconds**. Reliable affine passes do not invoke exhaustive alpha search; fallback search runs only when affine evidence is insufficient.

The deterministic repeat produced identical canonical JSON and result hashes.

## Verification and provenance

- Full Foundry test suite: **178 passed in 37.10 seconds** using `.venv312`.
- Focused invariant tests: **15 passed in 3.39 seconds**.
- Guard source identity before and after run 2: `67cdf7608b6315792542ad95dadf15fafc5f41f879116a14463b5d6b11531ccb`.
- The initial system-Python full-suite attempt is preserved and failed collection only because that interpreter lacked `openai`; the project `.venv312` run passed all tests.
- Run 2 used no run-1 cache. Cache/checkpoint identity is keyed by guard source SHA-256.
- The Foundry checkout was not edited by this calibration task.
- All run-1 evidence is frozen under `run_1/`; run-2 evidence is under `run_2/`.

## Reproduction

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
V23_CALIBRATION_OUT=/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_all_view_translation/calibration/run_2 \
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

The corrected guard resolves the broad close-up compatibility regression from run 1 and passes the complete requested transform suite. The remaining evidence gap is bounded and visible: four frozen brightness mode checks, four wide rigid-residual rejections, and one close-up boundary rejection. These should be reviewed as semantic/quality decisions rather than removed through threshold weakening.
