---
type: source
title: "Karpathy — LLM Wiki"
raw: "[[raw/llm-wiki]]"
created: 2026-07-04
updated: 2026-07-04
ingested: 2026-07-04
tags: [meta, knowledge-management, llm]
---

# Karpathy — LLM Wiki

Andrej Karpathy's idea file describing a pattern for building personal knowledge bases with LLMs:
the LLM incrementally builds and maintains a persistent, interlinked wiki that sits between you and
your raw sources. Source: [[raw/llm-wiki]].

## Key claims

- **Beyond RAG.** Typical RAG re-discovers knowledge from raw chunks on every query; nothing
  accumulates. See [[wiki/concepts/rag-vs-persistent-wiki]].
- **The wiki is a compounding artifact.** Cross-references, contradiction flags, and synthesis are
  already there and kept current — it gets richer with every source and every question. See
  [[wiki/concepts/llm-wiki-pattern]].
- **Division of labor.** The human curates sources, explores, and asks good questions; the LLM does
  all the summarizing, cross-referencing, filing, and bookkeeping.
- **Three layers:** raw sources (immutable), the LLM-owned wiki, and a schema config file. See
  [[wiki/concepts/three-layer-architecture]].
- **Three operations:** ingest, query, lint.
- **Two navigation files:** content-oriented `index.md` and chronological `log.md`. See
  [[wiki/concepts/index-and-log]].
- **Tooling is optional/modular.** [[wiki/entities/obsidian]] as the browsing IDE; [[wiki/entities/qmd]]
  for search at scale; Web Clipper, Marp, Dataview, graph view as needed. The wiki is just a git repo.
- **Lineage.** A modern realization of [[wiki/entities/memex|Vannevar Bush's Memex]] (1945) — the part
  Bush couldn't solve (who does the maintenance) is now the LLM's job.

## Why it works

Maintenance, not reading or thinking, is what kills human wikis. LLMs don't get bored and can touch
15 files in one pass, so maintenance cost approaches zero and the wiki stays current.

## Related
- [[wiki/overview]]
- [[wiki/concepts/llm-wiki-pattern]]
