---
name: azure-openai
description: "Call an Azure OpenAI chat deployment (GPT-5 / GPT-5.5 / GPT-5-mini) with an Azure AD bearer token."
---

Read `~/.claude/commands/azure-openai.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
