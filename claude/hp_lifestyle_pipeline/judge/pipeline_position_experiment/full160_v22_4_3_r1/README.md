# V22.4.3-R1 bounded-retry qualitative assembly

This is a distinct **wrapper-only** package for assembling the requested 160-row qualitative treatment. The Foundry pipeline, system prompts, geometry, guard, thresholds, V6.1 prompts, digital twins, cameras, and frozen Stage-A guides are byte-identical to V22.4.3.

The wrapper submits an initial immutable endpoint job for every row. It submits one additional immutable outer job only if the initial terminal error exactly equals:

```
RuntimeError: pipeline error: ValueError: Product invariant guard rejected both image attempts; raw attempts and metrics kept.
```

The first passing job is selected. Any other first-job error fails immediately. A second-job error fails immediately after preserving its audit. These completion results describe a bounded-retry **qualitative assembly protocol**. They are not native V22.4.3 per-job reliability.

Each outer job uses a unique identity and directory:

```
{row_slug}__outer_job_1
{row_slug}__outer_job_2
```

For every terminal job the package preserves the canonical submission request, terminal status, request hash, artifact manifest hash, and success or failure provenance. Successful jobs preserve all Stage-B, raw image-attempt, and guard evidence. Failed jobs preserve every artifact that the pipeline produced before rejection.

The runner is serial and fail-fast. Its progress file separately reports `first_job_pass`, `recovered_on_retry`, and `terminal_failure` counts and rates.

Prepared only; not launched. No model calls were made during preparation.
