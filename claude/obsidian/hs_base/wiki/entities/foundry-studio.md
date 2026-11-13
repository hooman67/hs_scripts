---
type: entity
title: Foundry Studio
tags: [foundry, foundry-studio, nestjs, lit, typescript, product]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/foundry/foundry-studio/README.md]]"]
---

# Foundry Studio

**Foundry Studio** is the Studio Product work area (`foundry-studio/` in the [[wiki/entities/foundry|Foundry]] repo) — the web application (and supporting infra) through which Foundry's generative-AI capabilities are surfaced to users, plus a plugin for Adobe DVA (desktop) apps.

## Packages

| Package | What it is | Stack |
|---|---|---|
| `web/` | Frontend | Lit + TypeScript |
| `backend/` | CRUD API for the web app | NestJS |
| `colligo-contracts/` | Shared [[wiki/entities/colligo|Colligo]] contract library consumed by backend + web | TS |
| `terraform/` | AWS infra for Studio (corp, prod, stage environments) | Terraform |
| `uxp/` | UXP plugin for Foundry Studio in Adobe DVA apps | UXP/TS |

## Dev setup (high level)

- **pnpm** for all TS projects; **nvm** for `web/`; **docker** for local backend dev.
- The `.vscode/` directory lives in `foundry-studio/` (not the repo root) — open `foundry-studio/` as the workspace to get launch configs.
- **Husky + lint-staged** pre-commit hooks (auto-installed on first `pnpm install`); projects opt in via `.lintstagedrc.mjs`.
- Also has `cms/`, `docs/`, `scripts/`, and `acpc-storage-guidelines.md`.

This page is an overview only — Studio was not deep-ingested. See the package `README.md`/`AGENTS.md` files for detail.

## Related
- [[wiki/entities/foundry]]
- [[wiki/concepts/foundry-dev-workflow]]
- [[wiki/entities/colligo]]
- [[wiki/entities/media-intelligence]]
