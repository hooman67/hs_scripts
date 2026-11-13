# V23 all-view translation guard calibration

**As of:** 2026-11-06  
**Scope:** read-only replay and deterministic guard calibration; no model calls or generations  
**Guard:** `full-affine-v1.6-all-view-translation-alpha-fallback`  
**Guard source SHA-256:** `1fead3c08c441bf361a4878d2945265a6ce6398f24fbd379a77b9243a556402d`

## Result

The new purpose-built V23 synthetic suite passed cleanly without changing a threshold: **82/82 expected outcomes**, comprising **50 expected failures**, **31 expected passes**, and **one expected `unverifiable` duplicate case**. All **81** 2368×1776 checks behaved as expected. Three close/high-fill silhouettes accepted legal large motion. Legal frame-edge placement passed, a one-pixel crop failed, and rotation, scale, anisotropy, shear, perspective warp, a dark substitute, and duplicate ambiguity were rejected or failed closed.

The compatibility gate is **not clean**:

- the frozen V22.4 synthetic corpus has **0 false accepts and 6 false rejects** across 110 mode checks; all six are the same three brightness-shift fixtures in both all-view and fixed-recovery mode;
- historical real verdicts show **one proxy false accept and four proxy false rejects** among 29 labeled attempts. These are regression proxies, not independent human labels;
- among 48 prior rows with an observable old guard selection, V23 changes **13** selections: one old rejection becomes attempt 1, while **12 formerly selected rows now select no attempt**;
- 47 additional rows lack an old guard selection field and are explicitly excluded from the selection-change denominator.

This evidence does not justify weakening thresholds. It shows that V23's new guard is internally correct on the requested transform suite but materially stricter than preserved behavior. The brightness-shift expectation and 12 lost prior selections require review before treating the guard as generation-ready.

## Policy evaluated

- First scene attempt for every product, view, and occupancy class: `fixed_position=False`.
- Stage-B recovery only: `fixed_position=True`, retaining the ±8-pixel domain.
- Old failures caused solely by `fixed_translation_x` or `fixed_translation_y` were relabeled as legal V23 passes. Other historical labels were retained.
- The current thresholds were used unchanged.

## Evidence

| Evidence set | Checks | False accepts | False rejects | Notes |
|---|---:|---:|---:|---|
| Frozen real attempts | 29 labeled of 31 | 1 proxy | 4 proxy | Historical guard verdicts, not human truth |
| Frozen synthetic, both modes | 110 | 0 | 6 | All six are brightness-shift positives |
| Added V23 synthetic | 82 | 0 | 0 | Includes full-resolution, ambiguity, and determinism checks |
| Prior selection replay | 48 comparable rows | — | — | 13 changed selections; 12 lose a selection |

### Added synthetic coverage

- five preserved 2368×1776 product/camera silhouettes;
- identity and large legal translation;
- 10 legal frame-extreme checks;
- 10 one-pixel crop checks;
- five rotations, 10 scales, five anisotropic transforms, five shears, and five perspective warps after translation;
- five dark substitutes and five valid products with unrelated dark distractors;
- 10 fixed-recovery boundary checks at 8 and 9 pixels;
- one duplicate/ambiguity case;
- one strict deterministic repeat with byte-identical canonical JSON.

The three `HIGH-FILL/CLOSE` fixtures with large legal translations all pass. Density uses the production rule: product bounding-box width or height fraction at least 0.45.

### Compatibility findings

The one historical proxy false accept is a wide-laptop attempt that failed the old 3.2-pixel residual-p95 limit at 3.2418 pixels. The current guard uses 3.5 pixels. This difference is threshold-history drift, not the removal of the x-y lock.

The four historical proxy false rejects are prior wide-view passes now rejected by `translation_only_residual_median` and/or `translation_only_residual_p95`. The full affine fit was near identity, but matched landmarks do not agree closely enough with one rigid translation under the new checks.

The 12 lost prior selections divide into:

- four wide-view rows rejected by the new rigid-translation residual checks;
- eight close-up rows rejected by the stricter alpha fallback, primarily `appearance`, sometimes also `boundary`.

The single newly selected prior row is the same historical wide-laptop residual-threshold case described above.

The six frozen synthetic false rejects are brightness-shift cases. They passed the former fallback but fail V23's requirement that internal structure and appearance each pass. This is a real preserved-corpus regression, regardless of whether the team later decides a strong product brightness shift should remain legal.

## Runtime and determinism

For 81 direct full-resolution alpha checks at 2368×1776:

- median: **288.8 ms**;
- p95: **301.3 ms**;
- maximum: **305.4 ms**;
- aggregate: **23.03 s**.

The initial end-to-end replay was longer because it also ran public affine assessment in both modes over 31 real attempts and 95 prior rows. Reliable affine passes do not invoke exhaustive alpha search; the fallback runs only for insufficient affine evidence. The runner now checkpoints each phase and can resume without repeating completed image work.

The deterministic repeat produced identical canonical JSON and identical result hashes.

## Verification

- Focused Foundry tests: **14 passed in 3.18 seconds**.
- Compatible prior artifacts: **95 replayed, 0 skipped**.
- Guard source hash was checked before and after replay; it did not change.
- The Foundry checkout was not edited by this calibration task.
- Existing V22 artifacts were not modified.

## Reproduction

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v23_all_view_translation/calibration/replay_v23_calibration.py
```

```bash
cd /home/colligo/foundry-pr4349-position-exp/experimental/adarabi/hp-3p-gpt25
pytest -q tests/test_invariants.py
```

The complete per-case metrics, prior selection changes, phase checkpoints, source/input hashes, stdout, and exit codes are stored beside this report.

## Next gate

Review the 12 lost prior selections and decide whether strong brightness-only changes remain legal. If the strict appearance requirement is intentional, record that semantic change and use a human-reviewed held-out generation pilot. If it is not intentional, change the guard design and rerun this same frozen package; do not lower thresholds merely to force a clean count.
