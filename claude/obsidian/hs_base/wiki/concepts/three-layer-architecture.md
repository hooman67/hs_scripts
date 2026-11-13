---
type: concept
title: Three-layer architecture
tags: [meta, knowledge-management, architecture]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/llm-wiki]]"]
---

# Three-layer architecture

How an [[wiki/concepts/llm-wiki-pattern|LLM-Wiki]] is structured. Three layers with a clear
ownership boundary.

1. **Raw sources** (`raw/`) — the curated, **immutable** source of truth. Articles, papers, images,
   notes. The LLM reads but never modifies them. Here: Hooman's `docs/` notes are symlinked at
   `raw/docs/`, plus the [[wiki/sources/llm-wiki|founding idea file]].
2. **The wiki** (`wiki/`) — LLM-generated, LLM-owned markdown: summaries, entity pages, concept
   pages, analyses, an overview. The human reads it; the LLM writes and maintains it.
3. **The schema** ([[WIKI_SCHEMA]]) — the config that tells the LLM the structure, conventions, and
   workflows. This is what makes the LLM a *disciplined maintainer* rather than a generic chatbot.
   Co-evolved by human + LLM over time. (Analogue: `CLAUDE.md` / `AGENTS.md`.)

Navigation across it all: the [[wiki/concepts/index-and-log|index and log]].

## Ownership boundary

The immutability of `raw/` is what makes the system trustworthy — synthesis can always be traced
back and re-derived from untouched sources. The LLM's write access is confined to `wiki/` + the
navigation files.

## Related
- [[wiki/concepts/llm-wiki-pattern]]
- [[wiki/entities/obsidian]]
