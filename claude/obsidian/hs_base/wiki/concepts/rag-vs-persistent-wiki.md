---
type: concept
title: RAG vs. persistent wiki
tags: [meta, knowledge-management, llm]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/llm-wiki]]"]
---

# RAG vs. persistent wiki

The core distinction motivating the [[wiki/concepts/llm-wiki-pattern|LLM-Wiki pattern]].

| | Classic RAG | Persistent wiki |
|---|---|---|
| When knowledge is assembled | At **query time**, from raw chunks | At **ingest time**, once |
| Accumulation | None — re-derived every question | Compounds — synthesis is kept current |
| Cross-references | Rediscovered per query | Already present in the pages |
| Contradictions | Not tracked | Flagged explicitly at ingest |
| Multi-doc synthesis | Re-pieced each time | Pre-synthesized, refined over time |
| Examples | NotebookLM, ChatGPT uploads, most RAG | This vault |

RAG works, but the LLM rediscovers everything from scratch on each question. A subtle question
spanning five documents forces the model to find and reassemble fragments every time. The wiki does
that work once and maintains it, so the answer is mostly already written.

## Related
- [[wiki/concepts/llm-wiki-pattern]]
- [[wiki/entities/qmd]] — search still helps *within* the wiki as it grows.
