---
name: foundry-sftp
description: "Create or manage a Foundry customer SFTP endpoint (AWS Transfer Family) for uploading data into a dropbox S3 bucket, and manage a user's SSH keys. Generates Terraform, opens a PR, and applies ONLY after the PR is approved. Triggers: \"create sftp\", \"sftp endpoint\", \"add sftp user\", \"add ssh key\", \"rotate sftp key\", \"transfer family\"."
---

Read `~/.claude/commands/foundry-sftp.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
