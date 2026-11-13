---
name: reference_obsidian_mcp
description: "Obsidian MCP setup — plain HTTP on 27123, vault at hs_base, how it's wired and why"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3cbb9457-99e9-403c-afe4-3af9de424b48
---

Obsidian MCP (Local REST API plugin) is registered at **user scope** in `~/.claude.json` as plain HTTP: `http://127.0.0.1:27123/mcp/` with `Authorization: Bearer 5e04d3317ea34aa897a0661ee9cb7c536541dd23b3c24b03682d3bfd52e77be7`.

Vault: `/Users/hshariati/hs_scripts/claude/obsidian/hs_base`. Plugin config at `.obsidian/plugins/obsidian-local-rest-api/data.json`.

Why plain HTTP (not the HTTPS 27124 server): HTTPS uses a self-signed cert that Node (Claude Code, v20.13.1 — too old for `--use-system-ca`) rejects. The fix would need `NODE_EXTRA_CA_CERTS`, but Hooman launches `claude` from VS Code terminals where `~/.zshrc` isn't sourced, so the env var never reaches the process. Plain HTTP (`enableInsecureServer: true` in data.json) removes the cert/env dependency entirely — works from any launch method. Localhost-only, so unencrypted is fine.

Gotchas: after changing the plugin toggle you must reload the plugin (Settings → Community plugins → toggle off/on) for the 27123 server to start. Config changes to `~/.claude.json` require restarting the Claude Code session to take effect. If the plugin is ever reset, re-enable "Non-encrypted (HTTP) Server". Re-register with: `claude mcp remove obsidian -s user` then `claude mcp add-json obsidian '{"type":"http","url":"http://127.0.0.1:27123/mcp/","headers":{"Authorization":"Bearer <token>"}}' -s user`.
