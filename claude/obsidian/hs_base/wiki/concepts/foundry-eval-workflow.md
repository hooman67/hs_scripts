---
type: concept
title: Foundry generation eval workflow
tags: [foundry, eval, thd, seedance, fal, methodology]
created: 2026-09-14
updated: 2026-09-14
sources: ["[[raw/thd-seedance-video-pipeline-learnings-2026-09]]"]
---

# Foundry generation eval workflow

How we run generation evals for a Foundry app (learned on [[wiki/entities/thd-video|THD Video]] /
[[wiki/entities/seedance|Seedance]]): reproducible eval sets + the unmodified pipeline + a resilient
runner + published [[wiki/concepts/foundry-eval-html-reports|HTML reports]].

## Principle: fix the eval set, run the UNMODIFIED pipeline
- Put behaviour changes in a **clean, reproducible ingested eval set**, then run the **unmodified
  production pipeline** on it. Never hack the pipeline/driver to force behaviour.
- Feeding per-image `role` via `inference.Binary.metadata` is legitimate — it mirrors exactly what the
  production webapp does (the real contract), not a hack.
- "Typed" eval sets: strip the inline storyboard directive from prompts and add explicit per-asset
  `role`, saved as durable artifacts (`cleaned_prompts_asset_type.json` + an `index_asset_type.html`
  digest) beside the set in S3. Storyboard-vs-reference tagging comes from the set's own
  `ordered_assets` (`entity=="storyboard frame"` / `kind`/ `media/storyboard/` path).

## In-process driver pattern
- Instantiate the pipeline directly (`object.__new__(Pipeline)` + `.load(...)`), monkeypatch temp-storage
  to write local files, and run each shot through `pipe.execute` wrapped in `asyncio.wait_for` (per-row
  hard timeout ~1000s). The editable install means the driver runs the live working-tree code.
- Config wires the real fal key, Azure/OpenAI rewriter, product bank (blurred/v2-anonymized yaml), and
  SAM3 (`preprocessing_method="anonymize"`, which the in-process path CAN set even though the HTTP
  request can't).

## Self-healing supervisor (survives fal hangs)
- Run detached via `setsid`. A supervisor kills + relaunches the driver on a **>~1050s log-mtime stall**
  (blocking fal calls that `asyncio.wait_for` can't cancel), gives up after N attempts, and a finisher
  builds+uploads the reports on `DONE`. Verify liveness by **log mtime**, not just `pgrep`.
- The driver is **resumable** (skips already-succeeded rows).

## Parallelize
- Run multiple eval sets concurrently on **separate fal API keys** (one set per key) to avoid quota
  contention. Always **smoke one shot first** (video returns, expected behaviour) before the full set.

## Access
- S3 via `foundry_aws_gateway.maybe_s3_client(bucket)` with
  `FOUNDRY_AWS_GATEWAY_HOST=https://foundry-aws-pluto.adobe.io` (works when raw broker creds are
  unavailable). Assets live under `seedance_video_eval_sets/<set>/` in
  `foundry-thd-enterprise-adobe-assets`.

## Related
- [[wiki/entities/thd-video]] · [[wiki/entities/seedance]]
- [[wiki/concepts/seedance-prompting]] — what we're usually measuring
- [[wiki/concepts/foundry-eval-html-reports]] — how results are published
- [[wiki/concepts/foundry-aws-access]]
