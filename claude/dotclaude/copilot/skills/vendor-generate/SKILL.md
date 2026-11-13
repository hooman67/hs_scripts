---
name: vendor-generate
description: "Submit each row of a Foundry viz HTML to the Deccan Media Studio API and produce a new viz HTML with a \"Generated\" column added. Resumable, parallelizable, runs against any model_id (UUID or slug) on https://media-studio-core.platform.deccan.ai."
---

Read `~/.claude/commands/vendor-generate.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
