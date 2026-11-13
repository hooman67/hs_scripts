# Shared Copilot CLI setup

This is for the **standalone Copilot CLI**, including when you run `copilot` in a VS Code terminal. VS Code Chat's extension and Agent Host have different configuration rules.

On each machine, clone or pull `hs_scripts`, then run:

```bash
bash ~/hs_scripts/claude/dotclaude/install-copilot.sh
```

If you also want to register the five MCP servers from the tracked, secret-free template, first restore the machine-local Claude MCP authorization and server dependencies, then run:

```bash
bash ~/hs_scripts/claude/dotclaude/install-copilot.sh --mcp
```

The installer does not replace existing real files or unrelated symlinks. It links Copilot's **personal** instructions, memory, and skills individually into this repo; it does **not** symlink all of `~/.copilot`, which contains authentication and session state. It also links shared commands, scripts, `CLAUDE.md`, and `RESEARCH_RULES.md` into `~/.claude` if not already linked, so Copilot can use the same global rules without maintaining another copy. Start a new Copilot session (or use `/skills reload` for skill changes). Check `copilot skill list`, `copilot instruction list`, and `copilot mcp list`.

`commands/*.md` is the authoritative workflow source. `copilot/generate-skills.py` generates and refreshes tracked `copilot/skills/*/SKILL.md` adapters whenever the installer runs. After adding or removing a command, rerun the installer and commit the generated adapters. Native Copilot-only skills can be added directly under `copilot/skills/`; the generator leaves them alone. Record lasting lessons in `memory/` and add them to `memory/MEMORY.md`, then commit and push your changes; other machines must pull them. CLI session history and `/memory` runtime state are machine-local, not synchronized automatically.

If Codex is also installed, Copilot may list its `~/.agents/skills` adapters as *inherited* skills ahead of same-named personal skills. Both adapters read the same tracked `commands/*.md` source; rerun `install-codex.sh` after adding shared commands if you also want Codex to discover them.

The five MCP definitions (Foundry Pluto, Microsoft agent, Excel, Obsidian, Glean) are specified in `copilot/mcp-servers.template.json`. With `--mcp`, `copilot/install-mcp.py` expands home-relative executable paths and writes **machine-local** `~/.copilot/mcp-config.json` (mode 600), copying the Obsidian authorization header from `~/.claude.json` without printing it. That file, credentials, auth tokens, and server installation/dependencies must **not** be committed. A new machine needs the executables installed and the local Claude Obsidian header restored before `--mcp` will work. The CLI's built-in GitHub MCP does not need copying. Server registration does not prove a server is installed, authenticated, or reachable; verify each in a fresh CLI session with `/mcp show NAME`.

Claude's `settings.json` permissions/model and Codex's provider/model settings are intentionally not imported: these do not have equivalent safe Copilot settings. This setup does not enable broad permissions, hooks, plugins, or automatic credential transfer.
