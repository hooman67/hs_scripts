---
type: entity
title: THD Video
tags: [thd, foundry, seedance, video-generation, standalone-app, v3]
created: 2026-09-14
updated: 2026-09-14
sources: ["[[raw/thd-seedance-video-pipeline-learnings-2026-09]]"]
---

# THD Video

**THD Video** is the Foundry standalone app that generates reference-to-video for **The Home Depot**,
using [[wiki/entities/seedance|Seedance 2.5 via fal.ai]]. It lives at
`managed_services/services/firefly/foundry/standalone_apps/thd_video` in [[wiki/entities/colligo|Colligo]]
V3 ([[wiki/concepts/colligo-managed-services|managed_services]]) and speaks the shared Foundry unified
inference envelope. It replaced a former self-hosted Runway Gen-4.5 GPU worker.

## What it does
`ThdVideoPipeline` is a CPU orchestrator: **SKU search → GPT rewriter → IP Guard → image preprocessing
→ Seedance (fal)**. See [[wiki/concepts/foundry-standalone-app-pipeline|the pipeline architecture]] for
the stages, the async job model, product/motion bank, and SAM3 anonymize.

## Endpoints
- `POST /v2/video/generate` and `POST /v2/video/prompt-rewrite` — async: submit → `{jobId,
  links.result.href}` → poll. Upload references first via `POST /v2/storage/image` → `tempStorage`
  source. Per-image `role` is `reference | storyboard`.

## Where it runs (dev)
- ArgoCD app **`foundry-thd-video-ethos851-dev-or2`** (cluster `ethos851-dev-or2`).
- Hosts: developer endpoint `https://thd-video-dev.ethos851-stage-or2.ethos.adobe.net`; edge/CGW backend
  `https://thd-video-dev.private.adobe.io`; [[wiki/entities/foundry-gateway|customer gateway]] route
  `model_id: thd-video`.
- Deploy config: `deploys/thd_video/dev/values.inference.yaml` (image tag, SAM3 host, IMS). See
  [[wiki/concepts/foundry-dev-deploy|the dev-deploy runbook]].

## Docs & tooling in the app
- `AGENTS.md` (operational guide — Seedance routing, motion bank, eval, deployment), `DEBUGGING.md`
  (local run under the debugger), `eval_htmls.md` (published result links), the `/dev_deploy` skill.

## Notable specifics
- **Image roles:** the request only carries `reference | storyboard`; storyboard-role images get a
  storyboard directive appended to the prompt. Richer roles are LLM-inferred (see
  [[wiki/concepts/seedance-prompting]]).
- **Duration:** send `duration:"auto"` and the clip sizes to the prompt (4–30s).
- **Dev gotchas:** default preprocessing is `remove` (paint-out), not SAM3 anonymize; `pickMotionVideo`
  is gated off in dev (motion bank attaches as a grid, not a clip).

## Related
- [[wiki/entities/seedance]] — the generation model
- [[wiki/concepts/foundry-standalone-app-pipeline]] — pipeline architecture (+ SAM3 anonymize)
- [[wiki/concepts/seedance-prompting]] — rewriter, roles, duration
- [[wiki/concepts/foundry-dev-deploy]] · [[wiki/concepts/foundry-local-debugging]]
- [[wiki/concepts/foundry-eval-workflow]] · [[wiki/concepts/foundry-eval-html-reports]]
- [[wiki/entities/foundry]] · [[wiki/entities/foundry-gateway]] · [[wiki/concepts/colligo-managed-services]]
