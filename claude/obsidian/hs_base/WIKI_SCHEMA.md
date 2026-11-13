---
type: schema
title: Wiki Schema
updated: 2026-07-04
---

# Wiki Schema

The configuration file for this LLM-maintained wiki. **Every `/obs-*` skill reads this first.**
It defines the layers, page types, conventions, and workflows. Hooman and the LLM co-evolve it
over time — when we discover a convention that works, we write it here.

Pattern reference: [[wiki/sources/llm-wiki|Karpathy's LLM-Wiki idea]] ([[wiki/concepts/llm-wiki-pattern]]).

## The three layers

1. **`raw/`** — immutable source documents. The LLM reads from these but **never edits them**.
   This is the source of truth. Hooman's notes are symlinked in at `raw/docs/`. Clipped
   articles, pasted text, and downloaded assets (`raw/assets/`) also live here.
2. **`wiki/`** — LLM-owned markdown. The LLM creates and maintains every page here. Hooman reads
   it; the LLM writes it. Subfolders:
   - `wiki/overview.md` — the top-level synthesis of the whole knowledge base.
   - `wiki/entities/` — pages for concrete things (systems, tools, people, projects, services).
   - `wiki/concepts/` — pages for ideas, patterns, techniques, processes.
   - `wiki/sources/` — one distilled summary page per ingested raw source.
   - `wiki/analysis/` — answers to `/obs-query` questions, filed back so explorations compound.
3. **Navigation files** (vault root):
   - `index.md` — content catalog. Every page listed with a one-line summary, grouped by category.
   - `log.md` — append-only chronological record of every operation.

## Page conventions

- **Filenames:** kebab-case, `.md`, descriptive (`glimmer-task-queue.md`, not `notes1.md`).
- **Links:** use Obsidian `[[wikilinks]]` liberally and in both directions. A `[[link]]` to a page
  that doesn't exist yet is fine — it marks a page worth writing (shows up in the graph as a stub).
- **Frontmatter** (YAML) on every wiki page — **every page uses `created`/`updated`**:
  ```yaml
  ---
  type: entity | concept | source | overview | analysis
  title: Human Readable Title
  tags: [topic, area]
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  sources: ["[[raw/docs/...]]"]   # which raw docs back this page (omit for pure-synthesis pages)
  ---
  ```
  Source-summary pages additionally use `raw: "[[raw/docs/...]]"`. For a source page, **`created` ==
  the day it was ingested** — i.e. `created` and the old `ingested` field mean the same thing.
  Standardize on `created`/`updated` going forward; `ingested` may be kept as an optional alias but
  is **no longer required**.
- **Structure of a page:** H1 title, a one-line definition/summary (used verbatim in the index),
  then body sections. End entity/concept pages with a `## Related` list of `[[links]]`.

## Contradiction discipline

When a new source disagrees with an existing claim, **never silently overwrite.** Flag it inline:

```markdown
> [!warning] Contradiction
> [[wiki/sources/old-source]] says X; [[wiki/sources/new-source]] (2026-07-04) says Y. Unresolved.
```

Keep both claims visible until Hooman resolves it. Prefer the newer source but note the conflict.

## Dates

Get today's date from the session environment (the `currentDate` context line) — never guess it.
Convert relative dates ("last week") to absolute `YYYY-MM-DD` before writing.

## Workflows (skills)

| Skill | Purpose |
|---|---|
| `/obs-ingest` | Read a raw source → summary page → update entities/concepts → update index + log. |
| `/obs-query`  | Answer a question from the wiki with citations; optionally file the answer back. |
| `/obs-search` | ripgrep + Obsidian search across `wiki/` and `raw/`. |
| `/obs-lint`   | Health-check: contradictions, stale claims, orphans, dead links, index drift. |
| `/obs-index`  | Rebuild `index.md` from scratch by scanning `wiki/`. |

## Operating notes for the LLM

- The vault is a local git repo at `/Users/hshariati/hs_scripts/claude/obsidian/hs_base`.
  Prefer direct file tools (Read/Write/Edit/Grep/Glob) — faster and more reliable than MCP.
- Use the **obsidian MCP** for Obsidian-native touches: `open_file` to surface a page in the app
  so Hooman can browse live (do this after writing key pages), `search_query` for tag/frontmatter
  filters, `search_simple` for quick text search, `command_execute` for Obsidian commands.
- One ingest can legitimately touch 10-15 pages. Thorough cross-referencing is the whole point —
  the value is in the links and the synthesis, not just the summaries.
- Stay collaborative: on ingest, discuss takeaways before writing so Hooman can steer emphasis.

## Graph view / raw naming

- **`raw/` is excluded from the graph** via the filter `-path:"raw/"` in `.obsidian/graph.json`, so
  the graph shows only the well-named wiki (entities/concepts/sources), not the hundreds of source
  copies. Raw files are still readable and stay clickable from `[[raw/...]]` links — they're just
  hidden from the graph *view*.
- Because of that, **raw source files keep their original repo filenames** (`README.md`, `AGENTS.md`,
  `CLAUDE.md`, `index.md`, …) so they mirror the source repos verbatim. Do NOT rename them to satisfy
  the graph — the filter handles the clutter. **Wiki pages**, by contrast, must always have
  descriptive kebab-case names (generic names like `readme`/`index` are not allowed in `wiki/`).
