---
type: source
title: THD Seedance video pipeline learnings (session, 2026-09)
tags: [thd, seedance, foundry, video-generation, deployment, eval]
created: 2026-09-14
updated: 2026-09-14
raw: "[[raw/thd-seedance-video-pipeline-learnings-2026-09]]"
sources: ["[[raw/thd-seedance-video-pipeline-learnings-2026-09]]"]
---

# THD Seedance video pipeline learnings (session, 2026-09)

Distilled from an engineering session on the [[wiki/entities/thd-video|THD Video]] app — building,
prompting, deploying, debugging, and evaluating a [[wiki/entities/seedance|Seedance]]-via-fal
reference-to-video generator in [[wiki/entities/foundry|Foundry]] / [[wiki/entities/colligo|Colligo]] V3.

## Key claims
- [[wiki/entities/seedance|Seedance 2.5]] on fal: `duration:"auto"` **sizes the clip to the prompt**
  (4–30s); 2.0 only for caller-supplied reference video.
- The [[wiki/concepts/seedance-prompting|structured rewriter]] builds an Event Script + roles; the LLM is
  **multimodal** and re-roles images itself (hardcoded input "scene" is just a hint). The old 10s cap
  was ours (`MAX_SECONDS`); raising it + the system prompt (and `MAX_BEATS`) yields longer clips while
  still sending `auto`.
- Request per-image role is only `reference | storyboard`; richer roles aren't in the request.
- [[wiki/concepts/foundry-standalone-app-pipeline|Pipeline]]: SKU search → rewriter → IP Guard →
  preprocessing (SAM3 `anonymize` or Nano-Banana `remove`) → Seedance; unified envelope + async jobs;
  SAM3 must use the ethos-direct host (edge rejects `foundry-services` as `x-api-key`).
- [[wiki/concepts/foundry-dev-deploy|Dev deploy]] is a GitOps two-hop (colligo → `colligo-v3-deploy`
  mirror → ArgoCD); the environment blockers were Artifactory perms and a parked buildkit
  (`uidmap` missing).
- [[wiki/concepts/foundry-local-debugging|Local debug]] needs `pathMappings` because the editable install
  symlinks the app into the venv; Vault auth is on-demand.
- [[wiki/concepts/foundry-eval-workflow|Eval]]: fix the eval set, run the unmodified pipeline, feed role
  via `Binary.metadata`; self-healing supervisor; two-fal-key parallelization; publish plain +
  [[wiki/concepts/foundry-eval-html-reports|two-file fe_html]] reports.

## Pages created/updated
Entities: [[wiki/entities/seedance]], [[wiki/entities/thd-video]]. Concepts:
[[wiki/concepts/seedance-prompting]], [[wiki/concepts/foundry-standalone-app-pipeline]],
[[wiki/concepts/foundry-dev-deploy]], [[wiki/concepts/foundry-local-debugging]],
[[wiki/concepts/foundry-eval-workflow]], [[wiki/concepts/foundry-eval-html-reports]].
