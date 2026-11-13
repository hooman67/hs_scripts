---
type: concept
title: Foundry dev workflow
tags: [foundry, dev-workflow, git, agents-md, conventions]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/foundry/AGENTS.md]]", "[[raw/foundry/README.md]]"]
---

# Foundry dev workflow

Repo-wide conventions for the [[wiki/entities/foundry|Foundry]] monorepo, defined in the root `AGENTS.md` (which `CLAUDE.md` just delegates to via `READ AND FOLLOW @AGENTS.md`).

## Two-level AGENTS.md system

- The **root `AGENTS.md`** holds repo-wide conventions (git, docs, how to answer questions).
- **Nearly every package** carries its own `AGENTS.md` with detailed, package-specific instructions — and must **not** duplicate conventions already in the root. `CLAUDE.md` files are one-liners pointing to their sibling `AGENTS.md`.
- Keep AGENTS.md files concise and actionable; refactor rather than append.

## Git workflow

- **Never commit directly to `main`.** Always branch or worktree first, push, and open a PR (never merge directly).
- **Branch naming:** `USER/<optional-initiative>/<short-description>`, `USER` = `whoami`, kebab-case, 2–3 word description (e.g. `raullucero/nestjs-migration/stage-1`).
- **Worktrees:** always at `.worktrees/<branch-name>` (repo root, gitignored). **Do NOT** use `.claude/worktrees/` (Claude Code's default) — that path pollutes `git status`. External repos also go under `.worktrees`, cloned `--single-branch`.
- A standard **PR description template** (Summary / Changes / Testing / Dependencies) is in the root AGENTS.md.

## Docs conventions

- All docs follow `docs/documentation-rules.md`.
- **`docs/`** = live reference docs that stay current with the code (agents may read). Package-scoped content can live in a package's own `docs/`.
- **`plans/`** = historical planning artifacts (specs, design docs, impl plans) → agents ignore these. Specs belong under `plans/superpowers/specs/` or `.../impl/`, never under `docs/`.
- No new top-level folders without the global repo owners (`.github/CODEOWNERS`).

## How agents should answer repo questions

The root AGENTS.md prescribes a process: (0) check `docs/common-issues.md`, (1) start from `README.md` §1 (work-area → overview doc) / §2 (cross-cutting docs), (2) follow each doc's "Related Docs" links, (3) **cite sources** as links, including which README section led there — to teach the doc structure.

## Per-language tooling (from package docs)

- **TS** (foundry-studio): `pnpm`, `nvm`, Husky + lint-staged pre-commit.
- **Python** (media-intelligence, modeling tools): `uv`, `ruff`; job_police/job_agent are `uv` scripts with `make check` (ruff + pytest).
- **Terraform** (modeling): `make lint`/`make fix` = `terraform fmt`; no CI, admin-applied.

## Related
- [[wiki/entities/foundry]]
- [[wiki/entities/foundry-studio]] · [[wiki/entities/media-intelligence]]
- [[wiki/concepts/foundry-modeling]]
- [[wiki/concepts/colligo-dev-workflow]] — the sibling monorepo's workflow
- [[wiki/sources/foundry-repo]]
