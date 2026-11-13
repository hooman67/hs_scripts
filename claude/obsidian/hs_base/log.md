---
type: log
title: Wiki Log
updated: 2026-07-04
---

# Wiki Log

Append-only, chronological record of every operation. Newest at the bottom.
Format: `## [YYYY-MM-DD] <op> | <title>` where `<op>` ∈ `ingest | query | lint | reindex | setup`.

Quick peek at recent activity: `grep "^## \[" log.md | tail -5`.

## [2026-07-04] setup | LLM-wiki initialized
Scaffolded the vault: `raw/` (+ symlinked Hooman's `hs_scripts/docs` notes at `raw/docs`),
`wiki/{entities,concepts,sources,analysis}`, `index.md`, `log.md`, `WIKI_SCHEMA.md`.
Created the `/obs-ingest`, `/obs-query`, `/obs-search`, `/obs-lint`, `/obs-index` skills.

## [2026-07-04] ingest | Karpathy — LLM Wiki
Added `raw/llm-wiki.md`. Seeded the wiki with the pattern itself: overview, source summary,
4 concept pages (llm-wiki-pattern, rag-vs-persistent-wiki, three-layer-architecture,
index-and-log), 3 entity pages (obsidian, qmd, memex). Updated index.

## [2026-07-04] ingest | Pluto (compute platform)
Added `raw/pluto-skill.md` (/pluto skill + foundry-pluto MCP) and `raw/pluto-docs.md`
(index.html + concepts.html). Created entity [[wiki/entities/pluto]]; concepts
pluto-resource-hierarchy, allocation-priority-tiers, quota-and-utilization; sources pluto-docs,
pluto-skill. Flagged a cross-source contradiction on priority-tier labels (docs vs skill vs MCP).
Updated overview + index. Dead-link stubs left for genie/glimmer/foundry/Mori (future ingests).
8 pages touched.

## [2026-07-04] ingest | Pluto docs sub-pages
Ingested 11 operational sub-pages (jobs, editing, projects, scheduler, clusters, CLI, SDK,
compute-cap) into `raw/pluto-docs-operations.md`; created concepts pluto-job-lifecycle (10 job
states, submit flow, snapshots), pluto-console, pluto-cli-sdk (`aip` CLI + adobe-aip-sdk) + a
source-summary. Many more doc pages remain (roles, docker, ssh, jupyter, s3-access, policy/*, blogs/*).

## [2026-07-04] ingest | Pluto governance skills
Ingested allocation_check, find_node_violation, update-node-utilization-canvas into
`raw/pluto-governance-skills.md` + a "Pluto operations" concept and source-summary. Found two
distinct canvases (F0BCU4W3KU6 = weekly approval table; F0AQ1PFGE5U = daily utilization log);
flagged a future `node-allocation-canvas` concept page. Ties into quota-and-utilization.

## [2026-07-04] lint | health-check + mechanical fixes
Ran /obs-lint. Clean on orphans/index-drift. Resolved the priority-tier contradiction (canonical =
`aip` CLI flags; MCP "Critical/Normal" are cosmetic outliers, left in code due to `_GUARANTEED_PRIORITIES`
coupling in the installed foundry-jobs package). Fixed overview folder-links; added Mori stub link +
snapshot/CLI cross-refs. Standardized frontmatter on `created`/`updated` (`ingested` now optional;
created == ingested) across schema, the 5 source pages, and the obs-ingest skill.

## [2026-07-04] ingest | Pluto docs — storage/secrets/docker/jupyter/policy/troubleshooting
Ingested 10 operational Pluto aidoc pages into `raw/pluto-docs-extras.md` + 6 new concept pages
(storage, secrets, docker-images, jupyter, troubleshooting, policy) + 1 source summary; enriched the
pluto-job-lifecycle Snapshots section (Save vs Pause, auto-restore).

## [2026-07-04] ingest | Colligo monorepo
Ingested Adobe Firefly's Colligo AI-platform monorepo (main @ 8f0cef36) — 1 entity + 8 concept + 3
source pages covering architecture, inference (V2 Rhode + V3 managed-services), training (Mori), the
`colligo.pluto` SDK, dev workflow, and philosophy, backed by 26 curated raw docs in `raw/colligo/`.
Uncovered for later: rhode internals, models/ catalog, V3 Bazel tutorials, CI/static-analysis.

## [2026-07-05] ingest | AI-platform docs portal (overview + inference infra)
Mapped docs.ai.corp.adobe.com and ingested the inference-platform infrastructure layer (Ethos
clusters/gateway, autoscaling Oshiya/QBS/KEDA, colligo-deploy/ArgoCD canary rollout, SLO framework,
observability, capability registry) into `raw/ai-platform-docs.md` + ai-platform-overview and
colligo-inference-infra concepts + a source page. Note: inference fleet (A10/A100/H100) ≠ Pluto
training tiers (B200/H200/H100/A100) — different fleets.

## [2026-07-05] ingest | Colligo models catalog
Ingested `models/` (commit 8f0cef36dc): ~52 model packages / 602 sub-packages grouped by modality,
707 docs copied to `raw/colligo/models/`. Created the colligo-models catalog + 6 flagship entity
pages (Clio, Clineto, DI Imaging, FLUX, Substance3D, Firefall) + a source summary.

## [2026-07-05] ingest | Mori training platform
Ingested Mori (Firefly's PyTorch/MoriX training framework) from `contrib/Mori` + the V3 docs portal —
resolved the `mori` stub with an entity hub + 8 concept pages (architecture, training-workflow,
parallelism, config, checkpointing, observability, pluto-agent, dependency-management) + 2 source
pages + raw copies. Uncovered: collections/** code, the standalone ai-platform core repo,
AdobeDiffusion (gen-1), data_chef.

## [2026-07-05] lint | full health-check (post models/Mori/portal ingests)
62 wiki pages. Clean: all index links resolve, no drift, no orphans, all core frontmatter present.
`mori` stub resolved; only genie/glimmer/foundry remain (intentional). Fixed one duplicate basename —
renamed `wiki/sources/colligo-models.md` → `colligo-models-ingest.md` (concept keeps `colligo-models`)
and updated its 2 refs. No contradictions; noted nuances (inference fleet A10/A100/H100 ≠ Pluto
training tiers; Mori legacy Run.ai vs morictl flow) captured inline, not conflicts.

## [2026-07-05] ingest | ai-platform repo (V3 model deployment)
Cloned `github.com/Adobe-Firefly/ai-platform` (main @ 127e0a0e4a) to `/Users/hshariati/ai-platform`.
Created the ai-platform-repo entity + v3-inference-framework / v3-deployment / v3-models-hub /
v3-vs-v2 concepts + source. V3 = framework wheel (`frameworks.inference`) + `@platforms_inference`
Bazel→ArgoCD→Ethos deploy machinery, both in ai-platform; colligo `managed_services` consumes it via
`release/inference/v*` tags. Reconciling note added (V3 spans two repos; still pre-1.0, V2 stable).

## [2026-07-05] ingest | Foundry monorepo (modeling focus)
Ingested the Foundry team monorepo (`/Users/hshariati/foundry`, main @ a2c807d4b), resolving the
`foundry` stub. Deep on `modeling/` — foundry-compute (job_agent = the foundry-pluto MCP/dashboard;
job_police = Claude-driven allocation enforcer off GH issue #728), foundry-terraform (per-customer S3
storage model, per-cloud/env roots), foundry-third-party-models, foundry-dev-workflow — plus
foundry-studio + media-intelligence overviews and 3 source pages. Ignored `experimental/`.

## [2026-07-05] ingest | Foundry gateway + access skills
Ingested `foundry-aws-corp.adobe.io` (Foundry Auth Service) + Hooman's 7 access skills → foundry-gateway
entity, foundry-aws-access + foundry-gateway-skills concepts, source summary, raw skill copies. Access
model: IMS + permanent Pluto machine token → broker → 12h STS creds (`aws_creds.env`); dropbox vs
adobe-assets buckets; no-delete S3 policy. Gateway root is IMS-gated → page content captured as
UNVERIFIED (WebFetch couldn't validate the signed-in page); `credential-vending-service.md` uncovered.

## [2026-07-05] lint | full health-check (post V3 / Foundry / gateway)
83 wiki pages, 207 raw docs. Clean: all index links resolve, no drift, no orphans, frontmatter complete.
`foundry` stub resolved; only genie/glimmer remain (intentional). Fixed two duplicate basenames —
renamed `sources/ai-platform-repo.md` → `ai-platform-repo-ingest.md` and
`sources/foundry-gateway-skills.md` → `foundry-gateway-ingest.md` (+ updated refs). No contradictions;
reconciling notes captured (V3 spans ai-platform + colligo; V3 pre-1.0 with V2 stable). Caveat:
foundry-gateway page content is UNVERIFIED (IMS-gated).

## [2026-07-08] ingest | Slack — HP endpoint email allowlist
Added raw/hp-email-allowlist-slack.md + concept foundry-customer-gateway-allowlist (how external
customer users are allowlisted to hit a Foundry endpoint via the customer_gateway configmap in
managed_services V3) + a source summary. Captures HP's 2 emails + the pending PR. Linked from
colligo-managed-services and foundry-gateway; updated index. 5 files touched.

## [2026-07-08] rename | endpoint email-allowlist note (was HP-specific)
Renamed to a reusable how-to: raw → `endpoint-email-allowlist-slack`, concept →
`foundry-endpoint-email-allowlist` ("Allowlist an email on a Foundry pre-release endpoint"); removed the
redundant source page. Updated to reflect Hooman already shipped it via **PR #28089** (HP's 2 emails on
the prerelease customer_gateway configmap). Fixed refs in index + colligo-managed-services + foundry-gateway.

## [2026-07-22] ingest | DSG Foundry token + data-access Slack thread
Added raw/dsg-foundry-token-slack.md + concept foundry-inference-auth-tokens (IMS: 24h endpoint token
= testing-only; UI→OAuth2 refresh tokens, backend→S2S "Service" client, self-serve via IMSS; no VPN).
Captured the open scope issue (exposing customer assets to a customer UI is out of ML-deployment scope
→ Theos/Foundry-4.0 or Mary/Studio). Linked from foundry-aws-access; indexed.

## [2026-08-25] ingest | Media Intelligence operations and Humain gap analysis
Deepened the Media Intelligence entity and added focused ingestion and gap-analysis concepts, backed by
a current Slack/Confluence/Humain research capture and source summary. Updated Foundry cross-links,
overview, and index. Six wiki pages touched (3 created, 3 updated), plus navigation/log changes.

## [2026-08-25] lint | Media Intelligence subgraph clean and pruned
Validated frontmatter, index entries, inbound links, duplicate basenames, and stale overview wording.
Kept one entity plus two focused concepts and one source node; no new orphan/dead-link/index-drift issues.
Pre-existing unrelated stubs and the GR6 orphan/index drift were left untouched.

## [2026-09-14] ingest | THD Seedance video pipeline learnings
Ingested a Claude Code session on the THD Video (Seedance-via-fal reference-to-video) Foundry app.
Created 8 wiki pages — entities `seedance`, `thd-video`; concepts `seedance-prompting`,
`foundry-standalone-app-pipeline`, `foundry-dev-deploy`, `foundry-local-debugging`,
`foundry-eval-workflow`, `foundry-eval-html-reports` — plus a raw source and its source summary.
Updated index (entities + a new video-generation concept group + sources), overview, and foundry.md
backlinks. ~12 pages touched. No contradictions with existing pages.
