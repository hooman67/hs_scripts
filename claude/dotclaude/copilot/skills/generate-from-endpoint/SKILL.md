---
name: generate-from-endpoint
description: "Run a customer's generation endpoint over a prompt set, upload outputs to S3, and produce a foundry-aws-corp gallery."
---

Read `~/.claude/commands/generate-from-endpoint.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
