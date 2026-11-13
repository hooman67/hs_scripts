#!/usr/bin/env bash
# ============================================================================
# SAVE (snapshot) the live "auto-research" Claude Code session INTO the git repo.
#
# Run this from the OLD machine (or any time you want to capture the latest
# conversation state) BEFORE you `git add/commit/push`. It copies the live
# transcripts out of ~/.claude and into this git-backed folder so they travel.
#
# USAGE:
#   bash /home/colligo/hs_scripts/claude/auto_research/session_resume/SAVE.sh
#   cd /home/colligo/hs_scripts && git add -A claude/auto_research/session_resume \
#     && git commit -m "auto-research: snapshot session" && git push
# ============================================================================
set -euo pipefail

WORKDIR="${WORKDIR:-/home/colligo/hs_scripts/claude/auto_research}"
DURABLE="$WORKDIR/session_resume"
SLUG="$(printf '%s' "$WORKDIR" | sed 's#[/_.]#-#g')"
SRC="$HOME/.claude/projects/$SLUG"
SESSIONS_DIR="$HOME/.claude/sessions"

echo "source  : $SRC"
echo "durable : $DURABLE"

if [ ! -d "$SRC" ]; then
  echo "ERROR: source session dir not found: $SRC" >&2
  echo "(are you on the machine where this session ran? is WORKDIR correct?)" >&2
  exit 1
fi

# Mirror the live session dir into the durable copy (transcripts + subagents + workflows).
mkdir -p "$DURABLE/projects" "$DURABLE/sessions"
cp -a "$SRC"/. "$DURABLE/projects/"

# Grab the session name-registration files that point at THIS session id.
SID="$(ls -1 "$SRC"/*.jsonl 2>/dev/null | xargs -n1 basename 2>/dev/null | sed 's/\.jsonl$//' | head -1 || true)"
if [ -n "${SID:-}" ] && [ -d "$SESSIONS_DIR" ]; then
  # Copy any session-index file that references this session id (name -> id mapping).
  grep -l "$SID" "$SESSIONS_DIR"/*.json 2>/dev/null | while read -r f; do
    cp -a "$f" "$DURABLE/sessions/"
  done
fi

echo "=== snapshot updated ==="
du -sh "$DURABLE"
ls -1 "$DURABLE/projects/"*.jsonl 2>/dev/null
echo "session name files:"; ls -1 "$DURABLE/sessions/" 2>/dev/null || true
echo
echo "Now commit + push:"
echo "  cd /home/colligo/hs_scripts && git add -A claude/auto_research/session_resume && git commit -m 'auto-research: snapshot session' && git push"
