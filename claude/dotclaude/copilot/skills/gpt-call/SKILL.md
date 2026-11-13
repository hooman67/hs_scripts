---
name: gpt-call
description: "Call Adobe Foundry GPT-5.x (Azure OpenAI) from a single entry point. Default model: gpt-5.6-terra."
---

Read `~/.claude/commands/gpt_call.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
