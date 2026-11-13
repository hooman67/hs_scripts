---
type: entity
title: Obsidian
tags: [tool, knowledge-management]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/llm-wiki]]"]
---

# Obsidian

A local-first markdown note app used as the **front-end / IDE** for this wiki. In the
[[wiki/concepts/llm-wiki-pattern|LLM-Wiki pattern]]: Obsidian is the IDE, the LLM is the programmer,
the wiki is the codebase. The human browses in Obsidian in real time while the LLM edits.

## Role in this vault

- Vault lives at `hs_scripts/claude/obsidian/hs_base` (a git repo).
- Claude connects via the **Local REST API** plugin over plain HTTP on port 27123 (see the
  `reference_obsidian_mcp` setup) — enabling `open_file`, search, and read/write from the agent.

## Useful features (from the pattern)

- **Graph view** — see the shape of the wiki: hubs, clusters, orphans.
- **Web Clipper** — browser extension to convert web articles to markdown into `raw/`.
- **Attachment folder** — set to `raw/assets/` + a "Download attachments" hotkey to localize images.
- **Marp** plugin — markdown slide decks generated from wiki content.
- **Dataview** plugin — dynamic tables/lists over page frontmatter (the reason pages carry YAML).

## Related
- [[wiki/concepts/three-layer-architecture]]
- [[wiki/entities/qmd]]
