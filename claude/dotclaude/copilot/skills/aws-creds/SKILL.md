---
name: aws-creds
description: "Fetch temporary AWS credentials for Foundry S3 access using the permanent Pluto machine token (no interactive IMS sign-in)."
---

Read `~/.claude/commands/aws-creds.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
