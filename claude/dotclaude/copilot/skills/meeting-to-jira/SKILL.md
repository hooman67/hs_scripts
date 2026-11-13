---
name: meeting-to-jira
description: "Process engineering sync meeting transcripts to extract action items, status updates, blockers, and decisions, then map them to Jira tickets for batch update. Use when the user provides a meeting transcript, meeting notes, standup notes, or asks to update Jira from a meeting."
---

Read `~/.claude/commands/meeting-to-jira.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
