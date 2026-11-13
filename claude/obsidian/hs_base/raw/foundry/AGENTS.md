# Agent Guidelines - Foundry (Monorepo Root)

**Applicable for all packages within this repository.**

---

## Git Workflow

**Never commit directly to `main`.** Always create a feature branch or worktree first, then push and open a PR.

### Branch Naming

Use the format `USER/<optional-initiative>/<short-description>` where `USER` is your username (`whoami`):

```
raullucero/feat/new-feature
raullucero/nestjs-migration/stage-1
raullucero/fix/auth-bug
```

- kebab-case, 2–3 words max for description
- Package-level AGENTS.md may define additional conventions on top of this

### Branch Creation

```bash
git checkout main
git pull origin main
git checkout -b <branch-name>
```

When work is complete, push the branch and open a PR — never merge directly.

**PR description template:**

```markdown
## Summary
Brief description of what this change accomplishes.

## Changes
- Key change 1
- Key change 2

## Testing
- [ ] Tests passing
- [ ] Linting passing
- [ ] Manual testing completed

## Dependencies
- Depends on: None
- Blocks: (#XXX) if applicable
```

### Worktree Location

**Always use `.worktrees/<branch-name>`** at the repo root — it is gitignored.

```bash
git worktree add .worktrees/my-feature -b feat/my-feature
```

> **Do NOT use `.claude/worktrees/`** (Claude Code's built-in `EnterWorktree` default). That path is not gitignored and will pollute `git status`.

### Checking out external repos

If you need to checkout external repos, also place them under `.worktrees`. Use `--single-branch` cloning them, as other branches might be heavy.

---

## Maintaining AGENTS.md Files

**Keep files concise and actionable** — remove outdated patterns, don't just append. Avoid redundant content; if duplication exists, refactor into a concise single entry.

Trigger updates when:
- New libraries or dependencies are added
- Patterns change (state management, styling, architecture)
- New conventions are introduced (naming, file organization)
- Significant architectural changes land (new modules, routing overhauls, major refactors)

After creating or modifying an `AGENTS.md`, review it for consistency with this root file and the relevant package context.

---

## Documentation

All documentation in this repo must follow [`docs/documentation-rules.md`](docs/documentation-rules.md).

- Root `docs/` contains live reference docs agents may read (overview docs, runbooks, setup guides). It is for content that spans multiple work areas or packages.
- Subfolders may have their own `docs/` for content scoped to that package.
- `plans/` contains historical planning artifacts — agents should ignore these.

> **Do NOT put specs or implementation plans under `docs/`.** Planning artifacts (specs, design docs, implementation plans) belong under `plans/superpowers/specs/` or `plans/superpowers/impl/` — see [`plans/AGENTS.md`](plans/AGENTS.md) for the exact layout. The `docs/` tree is exclusively for live reference documentation that stays current with the codebase.

---

## Answering Questions

When a user asks a question about this repo, follow this process:

0. **Check known issues first.** Before investigating, scan [`docs/common-issues.md`](docs/common-issues.md) for matching symptoms — many user-reported errors have well-known root causes documented there.
1. **Find the right doc.** Start from [`README.md`](README.md) — §1 maps work areas to overview docs, §2 lists cross-cutting reference docs. Pick the one that matches the question.
2. **Follow Related Docs.** Each overview doc has a Related Docs admonition at the top linking to companion docs (deeper detail on the same area) and cross-cutting docs (other areas). Use these to find additional context.
3. **Cite your sources.** In your answer, always tell the user which doc and section you used, as a link — and mention which section of [`README.md`](README.md) led you there. For example: "Based on [`inference-services-v2.md` §2 Environments](docs/inference-services-v2.md#2-environments) (found via [README §1 Model Serving](README.md#1-org-overview)) — ...". This helps the user learn the doc structure and find answers independently in the future.

If the docs don't cover the question, say so and suggest where the answer might live (wiki, external platform docs, or a specific team to ask).
 
---

## Package-Specific Guidelines

Each package has its own `AGENTS.md` with detailed instructions. Package-level files must **not** duplicate conventions already defined here.
