#!/usr/bin/env bash
# install-codex.sh — expose the shared dotclaude setup to Codex.
#
# The tracked Claude command Markdown remains the workflow source of truth.
# This script generates thin Codex SKILL.md adapters and links both supported
# user-skill discovery locations to those generated adapters. It also links the
# global instructions. Optional flags install Slack and import user-scoped MCP
# definitions while keeping credentials in machine-local Codex config.

set -euo pipefail

DOTCLAUDE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_DIR="${HOME}/.codex"
AGENT_SKILLS_DIR="${HOME}/.agents/skills"
CODEX_SKILLS_DIR="${CODEX_DIR}/skills"
GENERATED_SKILLS_DIR="${CODEX_DIR}/dotclaude-generated-skills"
CLAUDE_CONFIG="${HOME}/.claude.json"
CODEX_CONFIG="${CODEX_DIR}/config.toml"
SYNC_MCP=false
INSTALL_SLACK=false

for option in "$@"; do
  case "${option}" in
    --mcp) SYNC_MCP=true ;;
    --slack) INSTALL_SLACK=true ;;
    --all)
      SYNC_MCP=true
      INSTALL_SLACK=true
      ;;
    *)
      echo "Usage: $0 [--mcp] [--slack] [--all]" >&2
      exit 2
      ;;
  esac
done

mkdir -p "${CODEX_DIR}" "${AGENT_SKILLS_DIR}" "${CODEX_SKILLS_DIR}" "${GENERATED_SKILLS_DIR}"

link_exact() {
  local target="$1"
  local link="$2"

  if [[ -L "${link}" ]]; then
    local current
    current="$(readlink "${link}")"
    if [[ "${current}" == "${target}" ]]; then
      echo "ok:   ${link} -> ${target}"
      return
    fi
    echo "fix:  ${link} -> ${current}  (replacing with ${target})"
    rm "${link}"
  elif [[ -e "${link}" ]]; then
    echo "ERROR: ${link} exists and is not a symlink. Move/rename it first." >&2
    exit 1
  fi

  ln -s "${target}" "${link}"
  echo "link: ${link} -> ${target}"
}

frontmatter_value() {
  local file="$1"
  local key="$2"
  awk -v key="${key}" '
    NR == 1 && $0 == "---" { in_frontmatter = 1; next }
    in_frontmatter && $0 == "---" { exit }
    in_frontmatter && index($0, key ":") == 1 {
      sub("^" key ":[[:space:]]*", "")
      gsub(/^"|"$/, "")
      print
      exit
    }
  ' "${file}"
}

first_description_line() {
  local file="$1"
  awk '
    NR == 1 && $0 == "---" { in_frontmatter = 1; next }
    in_frontmatter && $0 == "---" { in_frontmatter = 0; next }
    in_frontmatter { next }
    NF {
      sub(/^#+[[:space:]]*/, "")
      print
      exit
    }
  ' "${file}"
}

normalize_name() {
  printf '%s' "$1" |
    tr '[:upper:]_' '[:lower:]-' |
    sed -E 's/[^a-z0-9-]+/-/g; s/-+/-/g; s/^-//; s/-$//'
}

yaml_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

link_exact "${DOTCLAUDE}/CLAUDE.md" "${CODEX_DIR}/AGENTS.md"
link_exact "${DOTCLAUDE}/RESEARCH_RULES.md" "${CODEX_DIR}/RESEARCH_RULES.md"

generated_count=0
for command_file in "${DOTCLAUDE}"/commands/*.md; do
  base_name="$(basename "${command_file}" .md)"
  declared_name="$(frontmatter_value "${command_file}" name)"
  skill_name="$(normalize_name "${declared_name:-${base_name}}")"
  description="$(frontmatter_value "${command_file}" description)"
  description="${description:-$(first_description_line "${command_file}")}"
  # Codex skill metadata rejects angle brackets in descriptions. Remove common
  # Markdown decoration and reserved brackets while preserving the source text.
  description="$(printf '%s' "${description}" | sed -E 's/[`*<>]+//g; s/[[:space:]]+/ /g')"
  description="${description:-Use the shared ${base_name} workflow.}"
  description="${description:0:360}"

  generated_dir="${GENERATED_SKILLS_DIR}/${skill_name}"
  mkdir -p "${generated_dir}"
  {
    printf '%s\n' '---'
    printf 'name: %s\n' "${skill_name}"
    printf 'description: "%s"\n' "$(yaml_escape "${description}")"
    printf '%s\n\n' '---'
    printf 'This is a Codex adapter for the shared workflow at `%s`.\n\n' "${command_file}"
    printf 'Before taking task actions, read that command file completely and follow it as the authoritative workflow. '
    printf 'Translate Claude-specific tool names to the closest available Codex tool while preserving all safety, approval, credential, and stopping boundaries. '
    printf 'The shared scripts remain available through `~/.claude/scripts`, which is linked to `%s/scripts`. ' "${DOTCLAUDE}"
    printf 'If a required MCP server or app is unavailable, report that dependency clearly rather than inventing a substitute.\n'
  } > "${generated_dir}/SKILL.md"
  printf '%s\n' "${command_file}" > "${generated_dir}/.dotclaude-source"

  link_exact "${generated_dir}" "${AGENT_SKILLS_DIR}/${skill_name}"
  link_exact "${generated_dir}" "${CODEX_SKILLS_DIR}/${skill_name}"
  generated_count=$((generated_count + 1))
done

# Codex only treats CLAUDE.md as project guidance when configured as a fallback.
# Insert this top-level setting without disturbing existing model or trust config.
if [[ -f "${CODEX_CONFIG}" ]] && ! grep -q '^project_doc_fallback_filenames[[:space:]]*=' "${CODEX_CONFIG}"; then
  CODEX_CONFIG_PATH="${CODEX_CONFIG}" ruby -e '
    path = ENV.fetch("CODEX_CONFIG_PATH")
    text = File.read(path)
    line = "project_doc_fallback_filenames = [\"CLAUDE.md\"]\n"
    first_table = text.index(/^\[/) || text.length
    text.insert(first_table, line + "\n")
    File.write(path, text)
  '
  chmod 600 "${CODEX_CONFIG}"
  echo "config: added CLAUDE.md as a Codex project-instruction fallback"
fi

# Keep Codex in the terminal's normal scrollback (same as `codex --no-alt-screen`).
if [[ -f "${CODEX_CONFIG}" ]] && ! grep -q '^alternate_screen[[:space:]]*=' "${CODEX_CONFIG}"; then
  CODEX_CONFIG_PATH="${CODEX_CONFIG}" python3 - <<'PY'
import os, re
path = os.environ["CODEX_CONFIG_PATH"]
text = open(path).read()
line = 'alternate_screen = "never"\n'
m = re.search(r"^\[tui\][ \t]*(#.*)?\n", text, re.M)
if m:
    text = text[:m.end()] + line + text[m.end():]
else:
    text = text.rstrip("\n") + "\n\n[tui]\n" + line
open(path, "w").write(text)
PY
  chmod 600 "${CODEX_CONFIG}"
  echo "config: disabled the Codex TUI alternate screen"
fi

if [[ "${SYNC_MCP}" == true ]]; then
  command -v codex >/dev/null || { echo "ERROR: codex not found" >&2; exit 1; }
  command -v jq >/dev/null || { echo "ERROR: jq not found" >&2; exit 1; }
  [[ -f "${CLAUDE_CONFIG}" ]] || { echo "ERROR: ${CLAUDE_CONFIG} not found" >&2; exit 1; }

  while IFS= read -r server_name; do
    server_type="$(jq -r --arg name "${server_name}" '.mcpServers[$name].type // "stdio"' "${CLAUDE_CONFIG}")"
    server_url="$(jq -r --arg name "${server_name}" '.mcpServers[$name].url // empty' "${CLAUDE_CONFIG}")"
    server_command="$(jq -r --arg name "${server_name}" '.mcpServers[$name].command // empty' "${CLAUDE_CONFIG}")"

    codex mcp remove "${server_name}" >/dev/null 2>&1 || true
    if [[ -n "${server_url}" || "${server_type}" == "http" ]]; then
      codex mcp add "${server_name}" --url "${server_url}"
    elif [[ -n "${server_command}" ]]; then
      server_args=()
      while IFS= read -r server_arg; do
        server_args+=("${server_arg}")
      done < <(jq -r --arg name "${server_name}" '.mcpServers[$name].args[]?' "${CLAUDE_CONFIG}")
      codex mcp add "${server_name}" -- "${server_command}" "${server_args[@]}"
    else
      echo "skip: unsupported MCP definition ${server_name}" >&2
    fi
  done < <(jq -r '.mcpServers | keys[]' "${CLAUDE_CONFIG}")

  # Static MCP headers are credentials. Copy the existing Obsidian header only
  # between machine-local files; never place it in dotclaude or command output.
  obsidian_auth="$(jq -r '.mcpServers.obsidian.headers.Authorization // empty' "${CLAUDE_CONFIG}")"
  if [[ -n "${obsidian_auth}" ]]; then
    CODEX_CONFIG_PATH="${CODEX_CONFIG}" OBSIDIAN_AUTH_VALUE="${obsidian_auth}" ruby -e '
      path = ENV.fetch("CODEX_CONFIG_PATH")
      auth = ENV.fetch("OBSIDIAN_AUTH_VALUE")
      text = File.read(path)
      marker = "[mcp_servers.obsidian]"
      start = text.index(marker)
      abort "obsidian MCP block not found" unless start
      finish = text.index(/^\[/, start + marker.length) || text.length
      block = text[start...finish]
      block = block.lines.reject { |line| line.start_with?("http_headers =") }.join
      block << "http_headers = { Authorization = #{auth.dump} }\n"
      text[start...finish] = block
      File.write(path, text)
    '
    chmod 600 "${CODEX_CONFIG}"
    echo "mcp: copied Obsidian authorization header into machine-local Codex config"
  fi
fi

if [[ "${INSTALL_SLACK}" == true ]]; then
  command -v codex >/dev/null || { echo "ERROR: codex not found" >&2; exit 1; }
  if codex plugin list 2>/dev/null | grep -Eq '^slack@openai-curated[[:space:]]+installed, enabled'; then
    echo "plugin: Slack is already installed and enabled"
  else
    codex plugin add slack@openai-curated
  fi
fi

echo
echo "Done: ${generated_count} shared command workflows exposed to Codex."
echo "Restart Codex to reload global instructions, skills, MCP servers, and plugins."
