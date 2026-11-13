#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Restore the fin-research Claude Code session on a NEW / REPROVISIONED machine.
#
# Claude Code discovers prior sessions for a working directory by looking in:
#     ~/.claude/projects/<slugified-absolute-path-of-working-dir>/*.jsonl
# The slug is the absolute working-dir path with every "/" and "." turned into "-".
#
# The conversation transcript lives at:
#     fin_research/.session_history/*.jsonl
# It is GITIGNORED (it contains personal portfolio + immigration data), so it does
# NOT travel via `git pull`. You must copy .session_history/ to the new machine
# MANUALLY (scp, rsync, or the home-folder backup) BEFORE running this script.
# This script then symlinks Claude's project dir to it so `--resume` finds it.
#
# USAGE on the new machine:
#     1. git clone/pull hs_scripts   (brings the repo + this script + all research files)
#     2. copy .session_history/ over manually, e.g.:
#          scp -r OLDHOST:/home/colligo/hs_scripts/claude/fin_research/.session_history \
#                 /home/colligo/hs_scripts/claude/fin_research/
#     3. bash /home/colligo/hs_scripts/claude/fin_research/RESTORE_SESSION.sh
#     4. cd /home/colligo/hs_scripts/claude/fin_research && claude --resume
#        (pick the session; or `claude -c` for most-recent)
#
# NOTE ON PATHS: the slug below assumes the repo lives at the SAME absolute path
# as the original machine: /home/colligo/hs_scripts/claude/fin_research
# If you clone it elsewhere (e.g. a different username/home), edit WORKDIR below
# to the new absolute path and re-run — the script recomputes the slug for you.
# ---------------------------------------------------------------------------
set -euo pipefail

# The working directory you will run `claude` from. Change if cloned elsewhere.
WORKDIR="/home/colligo/hs_scripts/claude/fin_research"

# Durable, git-backed store of the transcript(s) (lives inside this repo).
DURABLE="${WORKDIR}/.session_history"

# Derive Claude's project-dir slug from the absolute working-dir path.
# Claude replaces every "/", ".", AND "_" with "-" (verified against existing
# project dirs: hs_scripts->hs-scripts, auto_research->auto-research, and the
# cutlog precedent laser_log->laser-log). So:
#   /home/colligo/hs_scripts/claude/fin_research  ->  -home-colligo-hs-scripts-claude-fin-research
SLUG="$(printf '%s' "$WORKDIR" | sed 's/[/._]/-/g')"
LINK="${HOME}/.claude/projects/${SLUG}"

echo "workdir : $WORKDIR"
echo "durable : $DURABLE"
echo "slug    : $SLUG"
echo "link    : $LINK"
echo ""

if [ ! -d "$DURABLE" ]; then
  echo "ERROR: durable store $DURABLE not found — did the repo pull include .session_history/?" >&2
  exit 1
fi

mkdir -p "$(dirname "$LINK")"

# If a real dir already exists there (a fresh Claude run created one), merge then replace.
if [ -e "$LINK" ] && [ ! -L "$LINK" ]; then
  echo "note: $LINK exists as a real dir; merging its sessions into the durable store"
  cp -an "$LINK"/. "$DURABLE"/ 2>/dev/null || true
  rm -rf "$LINK"
fi

# (Re)create the symlink so Claude sees the git-backed transcripts as this project's history.
if [ -L "$LINK" ]; then rm -f "$LINK"; fi
ln -s "$DURABLE" "$LINK"

echo "linked: $LINK -> $DURABLE"
ls -ld "$LINK"
echo ""
echo "sessions available to resume:"
ls -1 "$DURABLE"/*.jsonl 2>/dev/null || echo "  (none found)"
echo ""
echo "Next:  cd $WORKDIR  &&  claude --resume    (pick the session named 'fin-research')"
