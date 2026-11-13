---
type: concept
title: Index and log
tags: [meta, knowledge-management, navigation]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/llm-wiki]]"]
---

# Index and log

Two navigation files that let the LLM (and human) find their way around the wiki as it grows. They
serve different purposes.

## [[index]] — content-oriented

A catalog of everything in the wiki: each page listed with a link and a one-line summary, grouped by
category (overview, entities, concepts, sources, analysis). Updated on every ingest. When answering a
query the LLM reads the index first, then drills into the relevant pages. This works well at moderate
scale (~100 sources / hundreds of pages) and avoids needing embedding-based RAG infrastructure —
though search ([[wiki/entities/qmd]]) helps as it grows.

## [[log]] — chronological

An append-only record of what happened and when — ingests, queries, lint passes, reindexes. Each
entry starts with a consistent prefix so it's greppable:

```
## [2026-07-04] ingest | Article Title
```

`grep "^## \[" log.md | tail -5` gives the last five operations. The log is the timeline of the
wiki's evolution and orients the LLM on what's been done recently.

## Related
- [[wiki/concepts/three-layer-architecture]]
- [[wiki/concepts/llm-wiki-pattern]]
