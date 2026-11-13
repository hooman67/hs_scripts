---
type: concept
title: LLM-Wiki pattern
tags: [meta, knowledge-management]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/llm-wiki]]"]
---

# LLM-Wiki pattern

A pattern where an LLM **incrementally builds and maintains a persistent, interlinked wiki** from
raw sources, instead of retrieving raw chunks at query time. Knowledge is compiled once and kept
current, so it compounds rather than being re-derived per question.

## The loop

1. **Ingest** a source → the LLM reads it, extracts key info, and integrates it: updates entity and
   concept pages, revises summaries, flags contradictions, strengthens the synthesis.
2. **Query** the wiki → the LLM finds relevant pages, synthesizes an answer with citations, and can
   file good answers back as new pages so explorations accumulate too.
3. **Lint** periodically → catch contradictions, stale claims, orphans, and gaps.

## Why it's different from RAG

The wiki is a **compounding artifact**: the cross-references exist, contradictions are already
flagged, and the synthesis reflects everything read so far. Contrast: [[wiki/concepts/rag-vs-persistent-wiki]].

## Division of labor

The human curates sources, directs analysis, and asks good questions. The LLM does the grunt work —
summarizing, cross-referencing, filing, bookkeeping — the maintenance that makes humans abandon wikis.

## In this vault

Realized through the [[wiki/concepts/three-layer-architecture|three-layer architecture]], the
[[wiki/concepts/index-and-log|index and log]], and the `/obs-*` skills. Browsed in
[[wiki/entities/obsidian|Obsidian]].

## Related
- [[wiki/sources/llm-wiki]]
- [[wiki/entities/memex]]
