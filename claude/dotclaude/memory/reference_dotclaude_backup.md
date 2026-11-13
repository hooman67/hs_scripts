---
name: dotclaude repo backup — source of truth lives in hs_scripts/claude/dotclaude
description: Shared Claude Code, Codex, and Copilot CLI config lives in ~/hs_scripts/claude/dotclaude/ and is linked into the agent homes. Backup = git push.
type: reference
---

**Source of truth:** `/Users/hshariati/hs_scripts/claude/dotclaude/` — a regular directory inside the `hs_scripts` git repo (`github.com/hshariati_adobe/hs_scripts`).

**Symlinks** (created by `dotclaude/install.sh`):

| System path | → | Repo path |
|---|---|---|
| `~/.claude/commands` | → | `dotclaude/commands` (shared workflows) |
| `~/.claude/scripts` | → | `dotclaude/scripts` (shared scripts) |
| `~/.claude/projects/-Users-hshariati-hs-scripts/memory` | → | `dotclaude/memory` (indexed memory files) |
| `~/.claude/CLAUDE.md` | → | `dotclaude/CLAUDE.md` |
| `~/.claude/RESEARCH_RULES.md` | → | `dotclaude/RESEARCH_RULES.md` |
| `~/.claude/settings.json` | → | `dotclaude/settings.json` |

Codex uses the same source of truth through links created by `dotclaude/install-codex.sh`:

| System path | → | Repo path |
|---|---|---|
| `~/.codex/AGENTS.md` | → | `dotclaude/CLAUDE.md` |
| `~/.codex/RESEARCH_RULES.md` | → | `dotclaude/RESEARCH_RULES.md` |

**Backup:** automated via launchd. Every day at 02:00 local time (catches up on next wake if the laptop is asleep), `~/Library/LaunchAgents/com.user.autocommit.plist` runs `~/hs_scripts/auto_commit.py`, which stages all changes (`git add -A`), commits with a `daily snapshot` message, and pushes to `origin/main`. Logs go to `/tmp/autocommit.log` and `/tmp/autocommit.err`.

Manual backup if you want to push immediately: `cd ~/hs_scripts && git add -A && git commit -m "..." && git push` — or just run `python ~/hs_scripts/auto_commit.py`.

> ⚠️ **`origin` must be the SSH URL.** HTTPS pushes 400 on this repo's large packs, so the cron's `git push` fails silently and commits pile up unseen. See [[reference_git_push_ssh_not_https]].

**Auto-commit history:** Prior implementation was a watchdog-based file-watcher that committed every modified file individually (one commit per file) via `KeepAlive=true` LaunchAgent. Replaced 2026-04-29 with the daily batch model — fewer/cleaner commits, catches new files and deletions (the watcher only saw modifications), no long-running daemon. Backups of the old script and plist are at `~/hs_scripts/auto_commit.py.watcher.bak` and `~/Library/LaunchAgents/com.user.autocommit.plist.watcher.bak`.

**Restore on a fresh machine:**
1. `git clone git@github.com:hshariati_adobe/hs_scripts.git ~/hs_scripts`
2. `bash ~/hs_scripts/claude/dotclaude/install.sh`
3. `bash ~/hs_scripts/claude/dotclaude/install-codex.sh` when Codex is installed.
4. `bash ~/hs_scripts/claude/dotclaude/install-copilot.sh` when Copilot CLI is installed.
5. Restore credentials manually (NOT in repo) to `~/.claude/hshariati/credentials.yaml`.

**Copilot CLI (including a VS Code terminal):** Run `bash ~/hs_scripts/claude/dotclaude/install-copilot.sh` after cloning/pulling. This links the tracked global instructions, memory, and generated skill adapters individually under `~/.copilot`. Run with `--mcp` only after restoring the local Obsidian MCP credential and installing the required local servers. MCP connection definitions live in a tracked secret-free template; machine-local `~/.copilot/mcp-config.json` is never tracked. See `copilot/README.md`. New skills and lessons become available on other machines after committing/pushing the tracked files and pulling/rerunning the installer there; runtime session memory is not synchronized.

**NOT in the repo (intentionally):**
- `~/.claude/hshariati/credentials.yaml` — secrets
- `~/.claude/sessions/`, `~/.claude/history.jsonl`, `~/.claude/projects/*/sessions*` — session/conversation logs (private + large)
- `~/.claude/cache/`, `~/.claude/paste-cache/`, `~/.claude/telemetry/`, `~/.claude/shell-snapshots/`, `~/.claude/session-env/` — ephemeral runtime state
- `~/.claude/.claude.json` — auto-managed by harness; contains machine-specific paths
- `~/.claude/projects/<other-projects>/` — only the `-Users-hshariati-hs-scripts/memory` subtree is symlinked; sibling project memories are not in the repo (we consolidated everything to one path on 2026-04-28)

**Defense in depth:** `dotclaude/.gitignore` blocks `credentials.yaml`, `*.token`, `.env*`, and `copilot/mcp-config.json` from ever being staged — even if a future edit accidentally writes one into the dotclaude tree.

**How to apply this memory:**
- When asked "where does my config live", point here.
- When editing memory/skills/scripts/settings, edits flow through symlinks and are immediately tracked by git — no extra step is needed beyond `git commit && git push`.
- If `~/hs_scripts/claude/dotclaude/` is missing on a new machine, run `install.sh` to recreate symlinks.
