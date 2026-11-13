---
name: ssh-devbox
description: "Connect to, run commands on, or copy files to/from the user's Pluto dev-box over SSH. Discovers the current dev-box ssh alias dynamically (the box name can change; the access mechanism does not). Triggers: \"ssh to devbox\", \"connect to my dev box\", \"copy to dev box\", \"scp to pluto devbox\", \"push files to devbox\", \"pull from devbox\", \"run on dev box\"."
---

Read `~/.claude/commands/ssh-devbox.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
