---
type: entity
title: qmd
tags: [tool, search]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/llm-wiki]]"]
---

# qmd

A local search engine for markdown files — hybrid **BM25 + vector** search with LLM re-ranking, all
on-device. Repo: https://github.com/tobi/qmd. Suggested in the [[wiki/sources/llm-wiki|LLM-Wiki idea]]
as the go-to search tool once a wiki outgrows its [[index]].

## Why / when

At small scale the [[wiki/concepts/index-and-log|index file]] is enough to navigate. As the wiki
grows to many hundreds of pages, proper search helps. qmd exposes both a **CLI** (the LLM can shell
out to it) and an **MCP server** (native tool), so it drops into this setup cleanly.

## Status in this vault

Not installed yet. Current search is ripgrep via `/obs-search`. Adopt qmd if/when ripgrep + index
stop being enough. See [[wiki/concepts/rag-vs-persistent-wiki]] — search complements the wiki, it
doesn't replace the synthesis.

## Related
- [[wiki/entities/obsidian]]
