# Session Resume — move the "auto-research" Claude conversation to a new machine

> **Codex note (2026-09-28):** this mechanism only snapshots/restores the legacy Claude Code
> transcript under `~/.claude`. It does not capture Codex conversations. For a new Codex session,
> read `../PROJECT_STATE.md` first; its restart checkpoint plus `DECISIONS.md`, `LEARNINGS.md`,
> `LONG_TERM_PLANS.md`, and the linked research reports are the authoritative continuation record.

This folder makes the **entire "auto-research" Claude Code conversation** (this whole chat,
including all background workflow/subagent history) portable via git, so on a new machine you
can `git clone`, run one script, and pick up exactly where we left off.

## Why this is needed
Claude Code stores conversation transcripts in `~/.claude/projects/<slug>/`, which is **outside**
this repo and does **not** travel with `git clone`. This folder holds a committed copy of that
session data plus scripts to snapshot it (SAVE) and rehydrate it (RESTORE).

## What's here
- `projects/` — the committed copy of `~/.claude/projects/-home-colligo-hs-scripts-claude-auto-research/`
  (the main transcript `35dcdba6-…jsonl`, all 16 background workflow runs, subagent logs, workflow scripts).
- `sessions/` — the session name-registration files that map the name **"auto-research"** → session id.
- `SAVE.sh` — snapshot the live session from `~/.claude` into this folder (run before committing).
- `RESTORE.sh` — copy it back into `~/.claude` on the new machine so `--resume` finds it.

## RESTORE — on the NEW machine
1. Clone the repo to the **same absolute path** (the session id is keyed to the working-dir path):
   ```
   git clone <hs_scripts repo> /home/colligo/hs_scripts
   ```
2. Run the restore:
   ```
   bash /home/colligo/hs_scripts/claude/auto_research/session_resume/RESTORE.sh
   ```
3. Open the session:
   ```
   cd /home/colligo/hs_scripts/claude/auto_research
   claude --resume "auto-research"     # or:  claude -c   (continue most recent)
   ```

**If your home dir / username differs on the new machine** (not `/home/colligo/...`): the session
slug is derived from the path, so set it explicitly:
```
WORKDIR=/new/path/to/hs_scripts/claude/auto_research \
  bash .../session_resume/RESTORE.sh
```
and then run `claude` from that same `WORKDIR`. (The conversation still restores; only the
`--resume "auto-research"` name lookup depends on the copied `sessions/` files — if the name
doesn't resolve, run `claude --resume` with no argument and pick the newest session, id `35dcdba6…`.)

## SAVE — to capture later progress before switching machines
```
bash /home/colligo/hs_scripts/claude/auto_research/session_resume/SAVE.sh
cd /home/colligo/hs_scripts && git add -A claude/auto_research && git commit -m "auto-research: snapshot" && git push
```

## Where the actual research lives (this is the real handoff)
Even without the chat transcript, everything we concluded is documented in the repo — start here:
- `../PROJECT_STATE.md` — live status + the current decision in front of Hooman
- `../CLAUDE.md` — operating manual / full context for a fresh agent
- `../DECISIONS.md`, `../LEARNINGS.md`, `../LONG_TERM_PLANS.md`
- `../acquisitions_canada/` (BC Staffing SaaS deep-dive + outreach, sweep kit, 4 deal deep-dives)
- `../acquisitions_500k/` (US wide search, US status/learnings, vending deep-dive)
- `../research_explorer.html` — interactive dashboard
