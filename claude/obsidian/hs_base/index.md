---
type: index
title: Wiki Index
updated: 2026-09-14
---

# Wiki Index

Content catalog of the wiki. Auto-maintained by `/obs-ingest` and rebuilt by `/obs-index`.
Each entry links a page with a one-line summary. To navigate: read this first, then drill in.

See also: [[WIKI_SCHEMA]] (conventions) · [[log]] (timeline) · [[wiki/overview|Overview]].

## Overview
- [[wiki/overview|Overview]] — top-level synthesis of the knowledge base.

## Entities

**Adobe AI platform**
- [[wiki/entities/ai-platform-repo|ai-platform repo (V3)]] — the standalone framework-wheel + Bazel deploy repo; the current model-deployment stack.
- [[wiki/entities/colligo|Colligo]] — Firefly's AI-platform monorepo (V2) for training & inference; ships the Pluto SDK.
- [[wiki/entities/mori|Mori]] — Firefly's PyTorch-native training framework (MoriX); runs on Pluto.
- [[wiki/entities/pluto|Pluto]] — Adobe's compute platform: GPU/CPU training & interactive jobs.

**Foundry (Hooman's team)**
- [[wiki/entities/foundry|Foundry]] — the Firefly team & monorepo delivering customer/partner generative models.
- [[wiki/entities/foundry-gateway|Foundry gateway]] — `foundry-aws-corp.adobe.io`, the team's access gateway (short-lived scoped creds).
- [[wiki/entities/foundry-studio|Foundry Studio]] — the Studio product (NestJS backend + Lit/TS frontend + UXP).
- [[wiki/entities/media-intelligence|Media Intelligence]] — Foundry's offline multimodal-understanding and retrieval system for structured metadata, semantic search, analytics, and recommendations.
- [[wiki/entities/thd-video|THD Video]] — Foundry standalone app: The Home Depot reference-to-video via Seedance 2.5 / fal.
- [[wiki/entities/seedance|Seedance (via fal.ai)]] — ByteDance reference-to-video model consumed as a 3P model on fal.

**Firefly models (served by Colligo)**
- [[wiki/entities/di-imaging|DI Imaging]] — Digital Imaging editing suite (MultiEdit, upscaler, relighting, masking).
- [[wiki/entities/firefly-clineto|Firefly Clineto]] — production Firefly video pipeline (T2V/I2V/V2V) on the Filix2 DiT.
- [[wiki/entities/firefly-clio|Firefly Clio]] — flagship Firefly text/image-to-image diffusion family.
- [[wiki/entities/firefly-firefall|Firefly Firefall]] — Firefly LLM/3P model gateway with auto model selection.
- [[wiki/entities/firefly-substance3d|Firefly Substance3D]] — 3D generation (MeshLRM/Materia + Foundry gen6).
- [[wiki/entities/flux|FLUX]] — Black Forest Labs FLUX image DiT support via sglang_diffusion.

**Meta / tooling**
- [[wiki/entities/memex|Memex]] — Vannevar Bush's 1945 vision that prefigures this pattern.
- [[wiki/entities/obsidian|Obsidian]] — the markdown app used as the wiki's front-end / IDE.
- [[wiki/entities/qmd|qmd]] — local hybrid BM25/vector markdown search engine (CLI + MCP).

## Concepts

**Meta / knowledge-management**
- [[wiki/concepts/index-and-log|Index and log]] — the two navigation files and why they work.
- [[wiki/concepts/llm-wiki-pattern|LLM-Wiki pattern]] — LLM incrementally builds/maintains a persistent wiki.
- [[wiki/concepts/rag-vs-persistent-wiki|RAG vs. persistent wiki]] — re-deriving knowledge vs. compounding it.
- [[wiki/concepts/three-layer-architecture|Three-layer architecture]] — raw sources / wiki / schema.

**Pluto (compute platform)**
- [[wiki/concepts/allocation-priority-tiers|Allocation priority tiers]] — P0/P1/P2/limited-time & preemption.
- [[wiki/concepts/pluto-cli-sdk|Pluto CLI & SDK]] — the `aip` CLI and async adobe-aip-sdk: install, auth, job commands.
- [[wiki/concepts/pluto-console|Pluto console]] — web-console ops: editing jobs, project admin, quota/capacity, clusters view.
- [[wiki/concepts/pluto-docker-images|Pluto Docker images]] — certified base images, custom builds, Docker-in-Containerd.
- [[wiki/concepts/pluto-job-lifecycle|Pluto job lifecycle]] — job types, the 10 states, submit flow, snapshots, scheduling.
- [[wiki/concepts/pluto-jupyter|Pluto Jupyter]] — JupyterLab in an interactive session (VS Code Web / port 8888).
- [[wiki/concepts/pluto-operations|Pluto operations]] — governance layer: allocation checks, node-violation detection, utilization canvas.
- [[wiki/concepts/pluto-policy|Pluto policy]] — platform policies: low-util & quota-overuse preemption, 2-week archival.
- [[wiki/concepts/pluto-resource-hierarchy|Pluto resource hierarchy]] — initiative/project/job & cluster/node/pod.
- [[wiki/concepts/pluto-secrets|Pluto secrets]] — Vault-backed secrets injected as env vars, never persisted.
- [[wiki/concepts/pluto-storage|Pluto storage]] — the four storage tiers + IAM-role S3 access.
- [[wiki/concepts/pluto-troubleshooting|Pluto troubleshooting]] — queued-job reasons, exit codes, NCCL timeouts, SSH fixes.
- [[wiki/concepts/quota-and-utilization|Quota and utilization]] — quota, capacity, UA & HFU metrics.

**Adobe AI platform (cross-cutting)**
- [[wiki/concepts/ai-platform-overview|AI-platform overview]] — portal map of the whole platform (Pluto/inference/training/data/registry).

**ai-platform / V3 (model deployment)**
- [[wiki/concepts/v3-deployment|V3 deployment]] — Bazel (`inference_application`+`ethos_deployment`) → Argo CD → Ethos; release tags.
- [[wiki/concepts/v3-inference-framework|V3 inference framework]] — `frameworks.inference`: Worker/WebApp/pipelines, Redis queues, 3 run modes.
- [[wiki/concepts/v3-models-hub|V3 models hub]] — Model Hub packaging (`models.<name>`).
- [[wiki/concepts/v3-vs-v2|V3 vs V2]] — concept mapping, reuse-via-shims, migration status (spans ai-platform + colligo).

**Colligo (AI-platform monorepo)**
- [[wiki/concepts/colligo-architecture|Colligo architecture]] — package roots, `colligo.yaml` deps model, build system.
- [[wiki/concepts/colligo-dev-workflow|Colligo dev workflow]] — the `./m` CLI, UV envs, lint/mypy/pytest, PR rules.
- [[wiki/concepts/colligo-inference|Colligo inference]] — V2 (Rhode) serving: workers/apps, multi-model GPU sharing, endpoint types.
- [[wiki/concepts/colligo-inference-infra|Colligo inference infra]] — Ethos clusters/gateway, autoscaling, colligo-deploy/ArgoCD rollout, SLOs.
- [[wiki/concepts/colligo-inference-sdk|Colligo inference SDK]] — pip/notebook SDK; HttpClient vs NativeClient.
- [[wiki/concepts/colligo-managed-services|Colligo managed services]] — Inference V3: Bazel + Argo CD (release candidate).
- [[wiki/concepts/colligo-models|Colligo models]] — catalog of the ~52 model packages served, grouped by modality.
- [[wiki/concepts/colligo-philosophy|Colligo philosophy]] — why-monorepo; short- vs long-lived code.
- [[wiki/concepts/colligo-pluto-sdk|Colligo Pluto SDK]] — `colligo.pluto` = the Pluto SDK/CLI shipped from Colligo.
- [[wiki/concepts/colligo-training|Colligo training]] — the Mori training framework + contrib; runs on Pluto.

**Mori (training framework)**
- [[wiki/concepts/mori-architecture|Mori architecture]] — core lib vs collections; the MoriX accelerator & Plugin/Strategy design.
- [[wiki/concepts/mori-checkpointing|Mori checkpointing]] — S3 checkpointing via experiment manager, `--resume`, s5cmd, HSDP throttling.
- [[wiki/concepts/mori-config|Mori config]] — YAML config rules + KnapFormer sequence balancer, auto data-source splitting.
- [[wiki/concepts/mori-dependency-management|Mori dependency management]] — deps-as-code: requirements/lock.yaml, S3-materialized, torch/cuda groups.
- [[wiki/concepts/mori-observability|Mori observability]] — on-demand PyTorch profiler + OpenTelemetry.
- [[wiki/concepts/mori-parallelism|Mori parallelism]] — FSDP2, context/sequence parallelism, distributed attention.
- [[wiki/concepts/mori-pluto-agent|Mori Pluto Agent]] — in-job HTTP service (separate process) with REST task handlers.
- [[wiki/concepts/mori-training-workflow|Mori training workflow]] — install → config-validate → launch (`morictl`/torchrun) → checkpoint/monitor on Pluto.

**Foundry (team infra & access)**
- [[wiki/concepts/foundry-aws-access|Foundry AWS access]] — IMS + Pluto-machine-token → broker → 12h STS creds; dropbox vs adobe-assets buckets.
- [[wiki/concepts/foundry-compute|Foundry compute]] — job_agent (foundry-pluto MCP + dashboard) and job_police (allocation enforcer off issue #728).
- [[wiki/concepts/foundry-dev-workflow|Foundry dev workflow]] — two-level AGENTS.md, git/worktree/branch conventions, per-language tooling.
- [[wiki/concepts/foundry-gateway-skills|Foundry gateway skills]] — catalog of Hooman's 7 access skills (aws-creds, generate-from-endpoint, …).
- [[wiki/concepts/foundry-modeling|Foundry modeling]] — the `modeling/` area: compute tooling, ops processes, Terraform (not training code).
- [[wiki/concepts/foundry-terraform|Foundry terraform]] — isolated roots per cloud/env; per-customer S3 storage model; IAM/gateways.
- [[wiki/concepts/foundry-endpoint-email-allowlist|Allowlist an email on a Foundry endpoint]] — how-to: add an email to the customer-gateway configmap (prerelease/prod) + PR.
- [[wiki/concepts/foundry-inference-auth-tokens|Foundry inference auth tokens (IMS)]] — the 24h token is testing-only; UI→refresh tokens, backend→S2S client (self-serve).
- [[wiki/concepts/foundry-third-party-models|Foundry third-party models]] — the approved-access process for 3P model source/weights.
- [[wiki/concepts/media-intelligence-ingestion|Media Intelligence ingestion]] — isolated Airflow workflow from canonical S3 manifest through Feature Registry, Postgres, OpenSearch, and end-to-end validation.
- [[wiki/concepts/media-intelligence-gap-analysis|Media Intelligence gap analysis]] — target-versus-observed corpus analysis that separates collection gaps from ingestion, labeling, and retrieval failures.

**THD Video / Seedance (video generation)**
- [[wiki/concepts/seedance-prompting|Seedance prompting & the structured rewriter]] — Event Script, asset roles, multimodal re-roling, duration control.
- [[wiki/concepts/foundry-standalone-app-pipeline|Foundry standalone-app pipeline]] — orchestrator stages, unified envelope + async jobs, product bank, SAM3 anonymize.
- [[wiki/concepts/foundry-dev-deploy|Deploying a Foundry app to dev]] — build/image/lint/PR flow, GitOps two-hop, Artifactory + buildkit prereqs.
- [[wiki/concepts/foundry-local-debugging|Local debugging (VS Code)]] — make debug/attach + one-step launch; editable-symlink pathMappings; on-demand Vault.
- [[wiki/concepts/foundry-eval-workflow|Foundry generation eval workflow]] — clean eval sets, unmodified pipeline, self-healing supervisor, two-key parallelization.
- [[wiki/concepts/foundry-eval-html-reports|Eval result HTML reports]] — plain + two-file fe_html, IMS scaffold, absolute asset URLs, badges.

## Sources
- [[wiki/sources/ai-platform-docs|AI-platform docs portal]] — portal overview + inference-infra pages.
- [[wiki/sources/thd-seedance-video-pipeline-learnings|THD Seedance video pipeline learnings]] — session (2026-09): prompting, pipeline, deploy, debug, eval.
- [[wiki/sources/ai-platform-repo-ingest|ai-platform repo]] — the V3 repo docs ingest summary.
- [[wiki/sources/colligo-agents|Colligo AGENTS/CLAUDE]] — the repo's root agent guide (identical AGENTS.md/CLAUDE.md).
- [[wiki/sources/colligo-dependency-management|Colligo dependency management]] — deps + build-system docs.
- [[wiki/sources/colligo-inference-framework|Colligo inference framework]] — the inference-platform docs.
- [[wiki/sources/colligo-models-ingest|Colligo models]] — the models-catalog ingest summary.
- [[wiki/sources/foundry-compute-jobs|Foundry compute-jobs docs]] — job_agent/job_police + compute-jobs docs.
- [[wiki/sources/foundry-gateway-ingest|Foundry gateway + skills]] — gateway/access-model + skills ingest summary.
- [[wiki/sources/foundry-modeling-docs|Foundry modeling docs]] — modeling README/terraform/3P/training docs.
- [[wiki/sources/foundry-repo|Foundry repo]] — root README + AGENTS summary.
- [[wiki/sources/llm-wiki|Karpathy — LLM Wiki]] — the idea file this system is built from.
- [[wiki/sources/mori-docs-portal|Mori docs (portal)]] — the V3 portal Mori/training docs.
- [[wiki/sources/mori-repo|Mori repo docs]] — the `contrib/Mori` in-repo docs.
- [[wiki/sources/media-intelligence-operations-research|Media Intelligence operations research]] — current ingestion/postprocessing rules, validation boundaries, and Humain gap-analysis context.
- [[wiki/sources/pluto-docs|Pluto documentation]] — official Adobe AI Platform docs (index + concepts).
- [[wiki/sources/pluto-docs-extras|Pluto docs — extras]] — storage, secrets, docker, jupyter, policy, troubleshooting.
- [[wiki/sources/pluto-docs-operations|Pluto docs — operations]] — the operational sub-pages (jobs, CLI/SDK, scheduler, capacity).
- [[wiki/sources/pluto-governance-skills|Pluto governance skills]] — allocation_check / find_node_violation / update-node-utilization-canvas.
- [[wiki/sources/pluto-skill|/pluto skill + foundry-pluto MCP]] — how Hooman drives Pluto from Claude Code.

## Analysis
_(none yet — `/obs-query` answers get filed here)_
