# V22.4.3 fresh first-row failure analysis

As of 2026-11-05 PST. This was a read-only analysis of preserved artifacts. It made no model call, changed no package or pipeline file, and launched nothing.

## Conclusion

**VERIFIED:** The guard did not falsely reject an unchanged laptop. Both fresh outputs preserve the rear three-quarter orientation and most internal product structure, but their outer extents do not match the fixed-position guide closely enough for the HIGH-FILL/CLOSE contract. The failure is concentrated in the silhouette, especially the lower lid/base extent, rather than in product identity.

Do not lower the `0.80` boundary threshold or change V22.4.3 based on these two outputs. The narrow next action depends on the intended experiment:

- If the run measures per-job pipeline reliability, keep this row as a failure and stop. An outer retry changes the measured execution policy.
- If the immediate objective is to produce 160 guard-valid treatment images for qualitative inspection, a single bounded outer retry is acceptable only as a separately named execution protocol with complete failure accounting. It must not be reported as the original V22.4.3 per-job result.

## Evidence

Row:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/full160_v22_4_3/run/pipeline/rows/cashmere__laptop_BackRightCloseUp__p1`

The branch requires the product's exact initial x-y coordinates and exact pixel width and height. Both fresh attempts exhausted the existing two-attempt pipeline policy.

| Evidence | Earlier raw attempt that V22.4.3 replay passes | Fresh attempt 1 | Fresh attempt 2 |
|---|---:|---:|---:|
| Boundary coverage within 2 px | 0.8110 | 0.6911 | 0.7429 |
| Boundary p90 distance | 2.865 px | 8.595 px | 5.730 px |
| Internal-edge coverage within 2 px | 0.9534 | 0.9451 | 0.9212 |
| Best translation | (+1, 0) px | (+1, -1) px | (+1, -1) px |
| SIFT matches | 3 | 0 | 1 |

The high internal-edge coverage confirms that the generated object retains substantial laptop structure. The materially worse boundary agreement shows that its outer geometry moved relative to the frozen alpha silhouette. Translation search cannot explain the mismatch because each fresh best translation is only `(+1,-1)` pixels and the residual boundary distance remains high.

A deterministic Hough-line diagnostic provides independent corroboration. These are prominent-line proxies, not ground-truth 3D measurements, so they should be interpreted with the overlay and guard metrics:

| Prominent edge | Guide | Earlier replay-pass | Fresh attempt 1 | Fresh attempt 2 |
|---|---:|---:|---:|---:|
| Lid top length | 873.4 px | 882.4 px | 898.5 px | 878.5 px |
| Long left extent | 856.1 px | 857.0 px | 881.2 px | 887.1 px |
| Lid top angle | 1.77° | 1.82° | 1.91° | 1.89° |
| Long left angle | -84.37° | -84.44° | -84.40° | -84.50° |

The nearly unchanged angles show that orientation is preserved. The changed extents, together with the red-guide/cyan-output overlay, show scale/silhouette drift. Attempt 1 is visibly wider and taller. Attempt 2 preserves the top width more closely but extends materially farther at the lower lid/base boundary. That is exactly the distinction the fixed-position guard is intended to enforce before downstream pixels are pasted back.

Diagnostics:

- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/fresh_failure_product_crops.jpg`
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/fresh_failure_edge_overlays.jpg`
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/fresh_failure_diagnostics.json`
- `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment/versions/v22_4_3/fresh_failure_line_offsets.txt`

## Outer retry assessment

### What an outer retry changes

The frozen pipeline already performs one image-level repair attempt after the first guard failure. A new outer job would rerun the stochastic Stage-B rewrite and then permit up to two more image generations. Therefore it raises the maximum search from two images under one Stage-B result to four images across two Stage-B executions.

That is an execution-policy change even when prompt templates, pipeline code, guard code, and thresholds remain byte-identical. It increases the chance of finding a guard-valid sample and conditions the delivered dataset on the guard. It cannot be silently treated as if the original first job passed.

### When it is methodologically acceptable

**ASSUMED objective: assembling a guard-valid qualitative treatment set.** A bounded retry is acceptable if all of the following are fixed before continuation:

1. Create a separately named wrapper/protocol revision, such as `V22.4.3 + outer-job-retry-1`; do not alter or overwrite the preserved failed run.
2. Allow every row the same policy: one initial job plus at most one outer retry only after both internal image attempts fail the frozen guard.
3. Select the first guard-passing job deterministically; do not choose by visual preference.
4. Preserve both job trees, all raw attempts, prompts, guard audits, and failure reasons.
5. Report first-job pass rate, retry recovery rate, total image calls, total Stage-B calls, and terminal failures separately.
6. Use fresh run/session/job IDs and a fresh output prefix. Do not adopt or relabel the failed job's outputs.
7. Stop explicitly if the outer retry also fails.

Under that protocol, the dataset answers: “What guard-valid result does the system produce with one operational job retry?” It does not answer: “What does a single V22.4.3 job produce?”

### When it invalidates the experiment

An outer retry invalidates a per-job reliability comparison if it is added only to this observed row, hidden from accounting, allowed until success, or pooled with one-job results without identifying the different call budget. It also invalidates claims that the original V22.4.3 run completed 160/160 on its frozen two-image policy.

## Recommended next action

Do not change the guard. Preserve this as a genuine first-job product-invariant failure.

If Hooman's priority is the requested 160-image qualitative treatment, define one transparent wrapper-only outer retry for every row and continue under a new protocol identity. Keep the original failure in the audit and report the two success rates separately. If the priority is estimating the current pipeline's native reliability, do not retry; this row is the observed outcome.
