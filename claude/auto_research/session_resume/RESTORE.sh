#!/usr/bin/env bash
# ============================================================================
# RESTORE the "auto-research" Claude Code session on a NEW / reprovisioned machine.
#
# Claude Code discovers prior sessions for a working dir by looking in:
#   ~/.claude/projects/<slugified-absolute-path-of-working-dir>/
# For working dir /home/colligo/hs_scripts/claude/auto_research the slug is:
#   -home-colligo-hs-scripts-claude-auto-research
#
# The durable copy of the transcripts (+ subagent/workflow history + the session
# name-registration files) lives HERE, inside the git-backed repo, so it travels
# with `git clone`/`git pull`. This script copies it back into ~/.claude so that
# `claude --resume "auto-research"` (or `claude -c`) finds the full conversation.
#
# USAGE (on the new machine, after cloning hs_scripts to the SAME path):
#   bash /home/colligo/hs_scripts/claude/auto_research/session_resume/RESTORE.sh
#   cd /home/colligo/hs_scripts/claude/auto_research
#   claude --resume "auto-research"      # or:  claude -c   (continue most recent)
#
# IMPORTANT: the repo MUST be cloned to exactly /home/colligo/hs_scripts (same
# absolute path) — the session slug is derived from the working-dir path. If your
# new username/home differs, edit WORKDIR below and re-run; the slug is recomputed.
# ============================================================================
set -euo pipefail

# --- Derive paths (recomputes the slug from WORKDIR, so it's portable if home changes) ---
WORKDIR="${WORKDIR:-/home/colligo/hs_scripts/claude/auto_research}"
DURABLE="$WORKDIR/session_resume"
SLUG="$(printf '%s' "$WORKDIR" | sed 's#[/_.]#-#g')"   # /,_,. -> -   (Claude's slug rule)
CLAUDE_PROJECTS="$HOME/.claude/projects"
LINK="$CLAUDE_PROJECTS/$SLUG"
SESSIONS_DIR="$HOME/.claude/sessions"

echo "workdir : $WORKDIR"
echo "slug    : $SLUG"
echo "target  : $LINK"

mkdir -p "$CLAUDE_PROJECTS" "$SESSIONS_DIR"

# --- 1. Restore the project transcripts + subagent/workflow history ---
# Merge (don't clobber) so a fresh Claude run on the new box isn't wiped.
if [ -e "$LINK" ] && [ ! -L "$LINK" ]; then
  echo "note: $LINK already exists as a real dir; merging durable copy into it"
fi
mkdir -p "$LINK"
cp -an "$DURABLE/projects/." "$LINK/" 2>/dev/null || cp -rn "$DURABLE/projects/." "$LINK/"
echo "restored transcripts into: $LINK"

# --- 2. Restore the session name-registration files ("auto-research" -> sessionId) ---
# These let `--resume "auto-research"` resolve the name. PID-named files are harmless
# to copy back; Claude reads sessionId+name from them.
if [ -d "$DURABLE/sessions" ]; then
  cp -an "$DURABLE/sessions/." "$SESSIONS_DIR/" 2>/dev/null || cp -rn "$DURABLE/sessions/." "$SESSIONS_DIR/"
  echo "restored session name files into: $SESSIONS_DIR"
fi

echo
echo "=== DONE. Transcripts available to resume: ==="
ls -1 "$LINK"/*.jsonl 2>/dev/null || echo "  (no .jsonl found — check WORKDIR/slug)"
echo
echo "Next:"
echo "  cd $WORKDIR"
echo '  claude --resume "auto-research"     # pick the named session'
echo "  # or:  claude -c                    # continue the most recent session"
echo
echo "If --resume can't find it by name, run 'claude --resume' with no arg and pick"
echo "the session dated newest (id starts 35dcdba6-...), or open the transcript at:"
echo "  $LINK/35dcdba6-451c-4629-b831-e09b25f4e35d.jsonl"
