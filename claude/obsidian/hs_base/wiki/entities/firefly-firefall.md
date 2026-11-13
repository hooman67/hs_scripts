---
type: entity
title: Firefall (LLM & 3P model gateway)
tags: [colligo, models, firefall, llm, gateway, 3p-models, routing]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/colligo/models/firefall/auto_model_selector/README.md]]", "[[raw/colligo/models/prompt_forge_llm/CLAUDE.md]]"]
---

# Firefall (LLM & 3P model gateway)

Colligo's **LLM and third-party (3P) model gateway** layer, served from
`models/colligo/models/firefall/` in [[wiki/entities/colligo|Colligo]]. Firefall routes generation and
LLM requests across Adobe's own models and external providers, and picks the best model for a request.

## What it serves
- **firefall_router** — request routing across model providers.
- **pipelines/gen_3p**, **pipelines/llm_3p** — 3P image-generation and LLM pipelines (external models
  reached through the Firefly 3P Gateway).
- **auto_model_selector** — recommends the best model for a request instead of making users pick.
  It reads the internal **Evaluation Hub leaderboard**, filters to 3P-Gateway-supported models,
  augments with credit cost + projected latency, and ranks by workflow intent (edit/generate),
  prompt-derived categories, and ranking method (elo, robust score, weighted linear) with bias toward
  Adobe's own model. Currently enabled for text-to-image and image editing.
- **entity_service**, **cai**, **notification**, **utils** — supporting services.

Related gateway packages: **firefly_gateway**, **firefly/ff_gateway_oss**, and the
`external_services/openai` wrapper. LLM workers backing these (Qwen3.5-27B, Gemma, InternVL, Phi) live
in `firefly/*_vllm*`, `firefly/lego_*`, and `dentro`/`dentro_v2`. Note **prompt_forge_llm** (Qwen3.5-27B
via vLLM) provides prompt moderation + NSFW pre-check for generation safety.

## Related
- [[wiki/concepts/colligo-models]] — the catalog this belongs to.
- [[wiki/entities/flux]] · [[wiki/entities/firefly-clio]] — models routed/compared via the gateway.
- [[reference_eval_hub_skill]] — the Eval Hub whose leaderboard feeds auto model selection.
- [[wiki/concepts/colligo-inference]] · [[wiki/entities/colligo]]
