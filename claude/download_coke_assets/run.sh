#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

# ─── AWS Credentials ───────────────────────────────────────────────────────
# Option 1: Export these before running, or
# Option 2: Put them in aws_creds.env and this script sources it automatically.
if [ -f aws_creds.env ]; then
  echo "Loading AWS credentials from aws_creds.env"
  source aws_creds.env
fi

if [ -z "${AWS_ACCESS_KEY_ID:-}" ]; then
  echo "ERROR: AWS_ACCESS_KEY_ID not set."
  echo "Either export it or create aws_creds.env with:"
  echo "  export AWS_ACCESS_KEY_ID=..."
  echo "  export AWS_SECRET_ACCESS_KEY=..."
  echo "  export AWS_SESSION_TOKEN=..."
  exit 1
fi

# ─── Install dependencies ─────────────────────────────────────────────────
if [ ! -d node_modules ]; then
  echo "Installing dependencies..."
  npm install
fi

# ─── Step 1: Generate AEM bearer token ────────────────────────────────────
echo ""
echo "=== Step 1: Generating AEM bearer token ==="
node src/get_token.js

# ─── Step 2: Run bulk download ────────────────────────────────────────────
echo ""
echo "=== Step 2: Starting bulk download ==="

# Use --skip-crawl to reuse existing image_manifest.json (saves ~2 min)
# Remove --skip-crawl to do a fresh crawl of the DAM
if [ -f image_manifest.json ] && [ "${FRESH_CRAWL:-}" != "1" ]; then
  echo "Using cached manifest (set FRESH_CRAWL=1 to re-crawl)"
  node src/bulk_download.js --skip-crawl
else
  node src/bulk_download.js
fi
