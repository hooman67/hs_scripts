#!/usr/bin/env bash
# Install shared Copilot CLI instructions, memory, skills, and optional MCPs.
set -euo pipefail

DOTCLAUDE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COPILOT_HOME="${HOME}/.copilot"

if [[ "${1:-}" != "" && "${1:-}" != "--mcp" ]] || [[ $# -gt 1 ]]; then
  echo "Usage: $0 [--mcp]  (--mcp registers MCP servers using local Claude credentials)" >&2
  exit 2
fi

link_exact() {
  local target="$1" link="$2"
  if [[ -L "${link}" && "$(readlink "${link}")" == "${target}" ]]; then
    echo "ok:   ${link}"
  elif [[ -e "${link}" || -L "${link}" ]]; then
    echo "ERROR: ${link} already exists; move it manually before installing" >&2
    exit 1
  else
    ln -s "${target}" "${link}"
    echo "link: ${link} -> ${target}"
  fi
}

python3 "${DOTCLAUDE}/copilot/generate-skills.py"
mkdir -p "${COPILOT_HOME}" "${HOME}/.claude"
link_exact "${DOTCLAUDE}/commands" "${HOME}/.claude/commands"
link_exact "${DOTCLAUDE}/scripts" "${HOME}/.claude/scripts"
link_exact "${DOTCLAUDE}/CLAUDE.md" "${HOME}/.claude/CLAUDE.md"
link_exact "${DOTCLAUDE}/RESEARCH_RULES.md" "${HOME}/.claude/RESEARCH_RULES.md"
link_exact "${DOTCLAUDE}/copilot/skills" "${COPILOT_HOME}/skills"
link_exact "${DOTCLAUDE}/memory" "${COPILOT_HOME}/memory"
link_exact "${DOTCLAUDE}/copilot/copilot-instructions.md" "${COPILOT_HOME}/copilot-instructions.md"

if [[ "${1:-}" == "--mcp" ]]; then
  python3 "${DOTCLAUDE}/copilot/install-mcp.py"
fi

echo "Restart Copilot CLI to load instructions and MCPs; use /skills reload for skills."
