# Moving fin-research to a new machine & resuming this Claude session

Last updated: 2026-07-06 by Claude (Opus 4.8). Owner: Hooman Shariati.

This folder is a git-backed value-investing research project. This note explains how to
pick the whole thing up on a **new / reprovisioned machine** and resume the Claude Code
conversation with full context.

## What's where

| Thing | Tracked in git? | Travels via `git pull`? |
|---|---|---|
| Research files (`CLAUDE.md`, `PROJECT_STATE.md`, `LEARNINGS.md`, `DECISIONS.md`, `LONG_TERM_PLANS.md`, `research-plan.md`, `sources.md`, `screens/`, `deep_dives/`, `data/*.py`, Damodaran CSVs) | ✅ yes | ✅ yes |
| `RESTORE_SESSION.sh`, `RESUME_README.md` | ✅ yes | ✅ yes |
| **Conversation transcript** (`.session_history/*.jsonl`) | ❌ **gitignored** | ❌ **no — move manually** |
| `data/cache/` (API-result caches) | ❌ gitignored | ❌ no (reproducible from scripts) |

**Why the transcript is gitignored:** it contains personal data — actual portfolio
holdings (tickers, share counts, dollar values) and immigration/family details — and the
remote (`github.com/hshariati_adobe/hs_scripts`) should not carry that. This matches the
existing `cutlog_claud_resume` precedent. So the transcript moves between machines by
**you**, not by git.

## New-machine procedure

```bash
# 1. Get the repo (brings all research files + the two helper scripts)
git clone https://github.com/hshariati_adobe/hs_scripts.git    # or: git pull
#    → land it at the SAME path if possible: /home/colligo/hs_scripts
#      (if you must use a different path, see "Different path" below)

# 2. Move the transcript over MANUALLY (it is NOT in git). From the OLD machine:
scp -r OLD_HOST:/home/colligo/hs_scripts/claude/fin_research/.session_history \
       /home/colligo/hs_scripts/claude/fin_research/
#    (or restore it from your home-folder backup)

# 3. Recreate the Claude project symlink so --resume can find the session
bash /home/colligo/hs_scripts/claude/fin_research/RESTORE_SESSION.sh

# 4. Resume
cd /home/colligo/hs_scripts/claude/fin_research
claude --resume        # pick the session (named "fin-research")
#   or: claude -c       # continue the most-recent session
```

## How resume works (the mechanics)

Claude Code finds a working directory's past sessions in
`~/.claude/projects/<slug>/*.jsonl`, where `<slug>` is the absolute working-dir path with
every `/`, `.`, and `_` replaced by `-`. For this project:

```
/home/colligo/hs_scripts/claude/fin_research
  → slug:  -home-colligo-hs-scripts-claude-fin-research
```

`RESTORE_SESSION.sh` symlinks that project dir to the git-backed `.session_history/`, so
Claude reads the transcript from inside the repo. (Verified: the `_`→`-` rule matches the
existing `hs-scripts`/`auto-research` project dirs and the cutlog `laser-log` precedent.)

## Different path / different machine layout

If you clone the repo somewhere other than `/home/colligo/hs_scripts` (e.g. a new username),
edit the `WORKDIR=` line near the top of `RESTORE_SESSION.sh` to the new absolute path of
this `fin_research` folder and re-run it — it recomputes the slug automatically.

## Where to start reading after resuming

If the conversation context is ever lost, the project is fully reconstructable from the
tracked files — read in this order:
1. `CLAUDE.md` — goal, scope, operating rules, data sources
2. `PROJECT_STATE.md` — live status: every phase, all findings, what's next
3. `DECISIONS.md` / `LEARNINGS.md` — what was decided and learned (incl. the Canadian-citizen
   correction that reopened CNOOC, and the durable data-source/market learnings)
4. `screens/ranked_output.md` — the master ranked comparison of all 16 finalists
5. `deep_dives/{TICKER}/` — per-name deep dives + buy diligence

## Current state (as of 2026-07-06)

Phases 1–4 complete. Buy-ready shortlist (quality + ownable on Schwab/Questrade): **INTU, CI,
SPGI, PUK**, plus the **OXY→EOG swap** in the energy sleeve; **Buzzi** needs Interactive
Brokers. Open thread: an optional portfolio-construction / position-sizing view. See
`PROJECT_STATE.md` for the authoritative, detailed status.
