#!/usr/bin/env bash
# install.sh — wire up symlinks from ~/.claude into this repo.
#
# Run on a fresh machine after cloning hs_scripts. Idempotent: skips links that
# already point to the right place; refuses to overwrite real files (rename
# them first if you want this script to take over).

set -euo pipefail

DOTCLAUDE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_CLAUDE="${HOME}/.claude"

# The memory dir Claude Code uses is derived from the absolute path of the repo,
# with every "/" and "_" turned into "-". hs_scripts lives two levels up from this
# script (dotclaude -> claude -> hs_scripts), so compute it instead of hardcoding
# the laptop's /Users/hshariati path — keeps install.sh portable across machines.
HS_SCRIPTS="$(cd "${DOTCLAUDE}/../.." && pwd)"
PROJECT_SLUG="$(printf '%s' "${HS_SCRIPTS}" | sed 's:[/_]:-:g')"
MEMORY_PARENT="${HOME_CLAUDE}/projects/${PROJECT_SLUG}"

# pairs: <repo path>::<system path>
# CLAUDE.md is the one file loaded in EVERY session regardless of cwd, so linking
# it is what gives Claude your context "from any location on the system".
LINKS=(
  "${DOTCLAUDE}/commands::${HOME_CLAUDE}/commands"
  "${DOTCLAUDE}/scripts::${HOME_CLAUDE}/scripts"
  "${DOTCLAUDE}/memory::${MEMORY_PARENT}/memory"
  "${DOTCLAUDE}/RESEARCH_RULES.md::${HOME_CLAUDE}/RESEARCH_RULES.md"
  "${DOTCLAUDE}/settings.json::${HOME_CLAUDE}/settings.json"
  "${DOTCLAUDE}/CLAUDE.md::${HOME_CLAUDE}/CLAUDE.md"
)

mkdir -p "${HOME_CLAUDE}" "${MEMORY_PARENT}"

for pair in "${LINKS[@]}"; do
  target="${pair%%::*}"
  link="${pair##*::}"

  if [[ ! -e "${target}" ]]; then
    echo "skip: target missing — ${target}"
    continue
  fi

  if [[ -L "${link}" ]]; then
    current="$(readlink "${link}")"
    if [[ "${current}" == "${target}" ]]; then
      echo "ok:   ${link} -> ${target}"
      continue
    fi
    echo "fix:  ${link} -> ${current}  (replacing with ${target})"
    rm "${link}"
  elif [[ -e "${link}" ]]; then
    echo "ERROR: ${link} exists and is not a symlink. Move/rename it first." >&2
    exit 1
  fi

  ln -s "${target}" "${link}"
  echo "link: ${link} -> ${target}"
done

echo
echo "Done. Verify with: ls -la ${HOME_CLAUDE}/{commands,scripts,RESEARCH_RULES.md,settings.json} ${MEMORY_PARENT}/memory"
