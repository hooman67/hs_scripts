---
name: obs-query
description: "Answer a question against the Obsidian LLM-wiki, with citations, and optionally file the answer back as a new wiki page so explorations compound."
---

Read `~/.claude/commands/obs-query.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
