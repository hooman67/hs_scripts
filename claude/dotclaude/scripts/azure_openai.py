# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.50"]
# ///
"""Call Azure OpenAI chat deployments with an Azure AD bearer token.

Credentials (endpoint + short-lived AD token) are read, in order, from:
  1. --creds <file>           (a sourceable file with export AZURE_OPENAI_* lines)
  2. $AZURE_OPENAI_ENDPOINT / $AZURE_OPENAI_AD_TOKEN already in the env
  3. ~/.claude/hshariati/azure_openai.env
  4. ~/Desktop/temp_cred.txt  (where ad-hoc creds are dropped)

The AD token is short-lived (~1h). On 401/expired, refresh the creds file and re-run.

Examples:
  uv run --script azure_openai.py "Summarize this in one line: ..."
  uv run --script azure_openai.py -d gpt-5.5 -s "You are terse." "ping"
  echo "long text" | uv run --script azure_openai.py -d gpt-5-mini-deployment-0e739
  uv run --script azure_openai.py --list           # show deployments named in creds file
  uv run --script azure_openai.py --json '{...}'    # raw: pass full prompt, get JSON-only reply
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

API_VERSION = "2024-12-01-preview"
DEFAULT_DEPLOYMENT = "gpt-5-mini-deployment-0e739"  # cheapest text model; fine for most tasks
CRED_CANDIDATES = [
    Path.home() / ".claude" / "hshariati" / "azure_openai.env",
    Path.home() / "Desktop" / "temp_cred.txt",
]


def load_creds(explicit: str | None) -> None:
    """Populate AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_AD_TOKEN in os.environ."""
    if os.environ.get("AZURE_OPENAI_ENDPOINT") and os.environ.get("AZURE_OPENAI_AD_TOKEN"):
        return
    files = [Path(explicit)] if explicit else CRED_CANDIDATES
    for f in files:
        if not f.exists():
            continue
        for line in f.read_text().splitlines():
            m = re.match(r'\s*export\s+(AZURE_OPENAI_\w+)\s*=\s*"?([^"]*)"?\s*$', line)
            if m:
                os.environ.setdefault(m.group(1), m.group(2))
        if os.environ.get("AZURE_OPENAI_ENDPOINT") and os.environ.get("AZURE_OPENAI_AD_TOKEN"):
            return


def deployments_from_creds(explicit: str | None) -> list[str]:
    files = [Path(explicit)] if explicit else CRED_CANDIDATES
    for f in files:
        if f.exists():
            # lines like:  #   gpt-5  (gpt-5)
            return re.findall(r"^#\s+([\w.\-]+)\s+\(", f.read_text(), re.M)
    return []


def main() -> int:
    p = argparse.ArgumentParser(description="Call an Azure OpenAI chat deployment.")
    p.add_argument("prompt", nargs="?", help="User prompt (or pipe via stdin).")
    p.add_argument("-d", "--deployment", default=DEFAULT_DEPLOYMENT)
    p.add_argument("-s", "--system", help="Optional system prompt.")
    p.add_argument("-m", "--max-tokens", type=int, default=2000,
                   help="max_completion_tokens (reasoning models bill reasoning here; keep >=2000).")
    p.add_argument("--creds", help="Path to a sourceable creds file.")
    p.add_argument("--list", action="store_true", help="List deployments named in the creds file and exit.")
    p.add_argument("--json", action="store_true", help="Print only the model's raw content (no metadata).")
    args = p.parse_args()

    if args.list:
        deps = deployments_from_creds(args.creds)
        print("\n".join(deps) if deps else "(no deployments listed in creds file)")
        return 0

    prompt = args.prompt or (sys.stdin.read().strip() if not sys.stdin.isatty() else None)
    if not prompt:
        print("ERROR: no prompt (positional arg or stdin)", file=sys.stderr)
        return 2

    load_creds(args.creds)
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    token = os.environ.get("AZURE_OPENAI_AD_TOKEN")
    if not endpoint or not token:
        print("ERROR: no Azure creds. Set AZURE_OPENAI_ENDPOINT/AD_TOKEN, pass --creds, "
              "or drop them in ~/Desktop/temp_cred.txt.", file=sys.stderr)
        return 2

    from openai import AzureOpenAI

    client = AzureOpenAI(azure_endpoint=endpoint, azure_ad_token=token, api_version=API_VERSION)
    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": prompt})

    try:
        resp = client.chat.completions.create(
            model=args.deployment, messages=messages, max_completion_tokens=args.max_tokens,
        )
    except Exception as e:
        print(f"ERROR calling {args.deployment}: {e}", file=sys.stderr)
        return 1

    choice = resp.choices[0]
    content = choice.message.content or ""
    if args.json:
        print(content)
        return 0
    print(f"deployment:    {args.deployment}")
    print(f"finish_reason: {choice.finish_reason}")
    print(f"usage:         {resp.usage}")
    print("---")
    print(content or "<empty> (raise --max-tokens if finish_reason=length)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
