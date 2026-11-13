---
name: read-squad-channel
description: "Read all new messages from the foundry_consumer_squad Slack channel since the last read, and update the channel context history."
---

Read `~/.claude/commands/read-squad-channel.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
