#!/bin/bash
set -euo pipefail
#
# Sets up Claude Code + your settings on a fresh remote machine.
# Run this ONCE after copying the folder to the remote.
#
# Usage: ./setup_remote.sh
#

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "=== 1/4: Installing Claude Code CLI ==="
if command -v claude &>/dev/null; then
  echo "Claude CLI already installed: $(claude --version 2>&1 | head -1)"
else
  echo "Installing via npm..."
  npm install -g @anthropic-ai/claude-code
  echo "Installed: $(claude --version 2>&1 | head -1)"
fi

echo ""
echo "=== 2/4: Setting up Claude config ==="
mkdir -p "$CLAUDE_DIR/commands"
mkdir -p "$CLAUDE_DIR/scripts"
mkdir -p "$CLAUDE_DIR/hshariati"

# Copy settings
cp "$SCRIPT_DIR/claude_config/settings.json" "$CLAUDE_DIR/settings.json"
cp "$SCRIPT_DIR/claude_config/settings.local.json" "$CLAUDE_DIR/settings.local.json"

# Copy slash commands and scripts
cp "$SCRIPT_DIR/claude_config/commands/"*.md "$CLAUDE_DIR/commands/"
cp "$SCRIPT_DIR/claude_config/scripts/"*.py "$CLAUDE_DIR/scripts/"

# Copy credentials
cp "$SCRIPT_DIR/claude_config/hshariati/"*.yaml "$CLAUDE_DIR/hshariati/"

# Copy CLAUDE.md to home dir
cp "$SCRIPT_DIR/claude_config/CLAUDE.md" "$HOME/CLAUDE.md"

echo "Copied settings, commands, scripts, and credentials to $CLAUDE_DIR"

echo ""
echo "=== 3/4: Installing Node.js dependencies ==="
cd "$SCRIPT_DIR"
npm install

echo ""
echo "=== 4/4: Verify ==="
echo "Claude CLI:  $(command -v claude || echo 'NOT FOUND')"
echo "Node.js:     $(node --version)"
echo "Project dir: $SCRIPT_DIR"
echo "Files:"
ls -la "$SCRIPT_DIR/src/" "$SCRIPT_DIR/creds/" "$SCRIPT_DIR/image_manifest.json" 2>&1

echo ""
echo "============================================"
echo "Setup complete! Next steps:"
echo ""
echo "  1. Update aws_creds.env with fresh AWS credentials"
echo "  2. Run:  cd $SCRIPT_DIR && ./run.sh"
echo "  3. Or use Claude:  cd $SCRIPT_DIR && claude"
echo ""
echo "  NOTE: You'll need to authenticate Claude on first run"
echo "        (it will prompt for your Anthropic API key or login)"
echo "============================================"
