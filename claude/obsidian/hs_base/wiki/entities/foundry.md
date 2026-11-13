---
type: entity
title: Foundry
tags: [foundry, adobe, firefly, monorepo, modeling, ai-platform]
created: 2026-07-05
updated: 2026-09-14
sources: ["[[raw/foundry/README.md]]", "[[raw/foundry/AGENTS.md]]", "[[raw/foundry/docs/project-setup-and-access.md]]"]
---

# Foundry

**Foundry** is the Adobe Firefly org and its monorepo (`Adobe-Firefly/foundry`) — "the home base for every Foundry engineer." It is Hooman Shariati's own team: the group that builds and delivers **customer/partner generative-AI models** (customer deals like NBCU, The Home Depot / THD, TCCC / Coca-Cola, Humain, Tesco, Disney) on top of the Adobe AI platform. The repo holds the **Studio Product**, **Media Intelligence**, shared **modeling infrastructure**, experimental work, and — most importantly — the docs that tie the whole org together.

## The org: five work areas

The README frames Foundry as a five-stage pipeline (data → training → serving → products):

| # | Work area | Where the code lives |
|---|---|---|
| 1 | **Data Preparation** | Glimmer (in [[wiki/entities/genie|Genie]]), ad-hoc (`experimental/`), CaptionLens |
| 2 | **Model Training** | `foundation_exploration` (in [[wiki/entities/colligo|Colligo]] `contrib/Mori/collections/`) |
| 3 | **Model Serving** | v2 gen-foundry (Colligo + `colligo-deploy`); v3 managed services (`colligo/managed_services`) |
| 4 | **Studio Product** | `foundry-studio/` (this repo) → [[wiki/entities/foundry-studio]] |
| 5 | **Media Intelligence** | `media-intelligence/` (this repo) → [[wiki/entities/media-intelligence]] |

Key insight: much of Foundry's *heavy* code deliberately lives in **other repos** — training in Colligo's `foundation_exploration`, data pipelines in Genie's Glimmer, inference in Colligo. This `foundry` repo holds the **supporting infrastructure, products, processes, and documentation** that don't have a home elsewhere.

## Repo layout (this repo)

| Folder | What it is |
|---|---|
| `docs/` | Live agent-readable reference docs (compute jobs, training, 3P models, access, inference). |
| `modeling/` | **Shared modeling infrastructure** — compute tooling, ops processes, Terraform. The priority area → [[wiki/concepts/foundry-modeling]]. |
| `foundry-studio/` | Studio Product — NestJS backend + Lit/TS frontend + Terraform + UXP plugin → [[wiki/entities/foundry-studio]]. |
| `media-intelligence/` | Video-understanding ML pipeline → [[wiki/entities/media-intelligence]]. |
| `experimental/` | Prototypes / staging ground (NOT ingested). |
| `plans/` | Historical planning artifacts (agents ignore these). |
| `tools/` | Repo-internal tooling; Claude Code plugin marketplace of shared agent skills. |

The repo uses a **two-level AGENTS.md system**: a root [[wiki/concepts/foundry-dev-workflow|AGENTS.md]] with repo-wide git/doc conventions, plus a package-level `AGENTS.md` in nearly every subdirectory (with `CLAUDE.md` = `READ AND FOLLOW @AGENTS.md`).

## Cloud accounts

Foundry spans multiple clouds (see [[wiki/concepts/foundry-terraform]]):
- **AWS** — `foundry-prd` (324037283113), `foundry-stg` (457335975320), legacy `asml-stage` (NBCU/sensei-asml, frozen). S3 for customer data, model artifacts, evals.
- **Azure** — `AZR14080`, for Azure OpenAI / GPT endpoints (evals, prompt rewriting, LLM-as-judge).
- **GCP** — `GCP-0805` (`gcp-ml-platform-poc`), for Gemini via Vertex AI (same eval/rewrite use cases).
- **AWS Bedrock** — Claude (Anthropic) for data processing / eval.

Access is tiered: **Foundry-Developer** (all engineers, read-only + scoped write) and **Foundry-Developer-Admin** (capped ~6 people: Hooman Shariati, Shayan Hoshyari, Marian Petre, Eugene Brodsky). Developers get short-lived, scoped credentials from the **Foundry Auth Service** (`foundry-aws-corp.adobe.io`, 12-hour expiry) rather than long-lived keys.

## Relationship to Pluto / Colligo / Firefly

- **[[wiki/entities/pluto|Pluto]]** is the compute platform Foundry runs on. All Foundry compute lives under the **Foundry Initiative (GAI-415)**; since 2026-03-27 all projects share one **"Foundry Unified Compute"** pool (initiative-level quota). Foundry's own compute tooling ([[wiki/concepts/foundry-compute|job_agent + job_police]]) is built on the Pluto SDK.
- **[[wiki/entities/colligo|Colligo]]** hosts Foundry's training (`foundation_exploration`) and inference (gen-foundry v2 + managed_services v3) code. Foundry is effectively a *tenant* of the Colligo platform.
- **Firefly** is the product family; Foundry delivers customer/partner-specific variants of Firefly models and the Studio product that surfaces them.

## Related
- [[wiki/concepts/foundry-modeling]] — the modeling/ area (priority)
- [[wiki/concepts/foundry-compute]] — job_agent + job_police
- [[wiki/concepts/foundry-terraform]] — the Terraform infra
- [[wiki/concepts/foundry-third-party-models]] — the 3P model process
- [[wiki/concepts/foundry-dev-workflow]] — git/build/lint conventions
- [[wiki/entities/foundry-gateway]] · [[wiki/concepts/foundry-aws-access]] · [[wiki/concepts/foundry-gateway-skills]] — access gateway, credential model & skills
- [[wiki/entities/foundry-studio]] · [[wiki/entities/media-intelligence]]
- [[wiki/entities/thd-video]] — a customer app on this stack (Seedance reference-to-video); see also [[wiki/entities/seedance]]
- [[wiki/concepts/media-intelligence-ingestion]] · [[wiki/concepts/media-intelligence-gap-analysis]]
- [[wiki/entities/pluto]] · [[wiki/entities/colligo]] · [[wiki/entities/genie]]
- [[wiki/sources/foundry-repo]]
