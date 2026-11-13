---
name: html-to-appen-csv-for-humain
description: "Convert a Foundry viz HTML into an Appen/Humain annotation CSV by copying all referenced assets into s3://foundry-appen-humain-enterprise/to_annotate/html_stem/ and producing a CSV with asset_url, reference_url[_N], prompt columns."
---

Read `~/.claude/commands/html-to-appen-csv-for-humain.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
