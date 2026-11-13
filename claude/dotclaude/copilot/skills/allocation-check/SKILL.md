---
name: allocation-check
description: "Compute the Foundry node-allocation table (canvas approved/not-approved vs. Pluto capacity & running) and DM it to Hooman on Slack."
---

Read `~/.claude/commands/allocation_check.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
