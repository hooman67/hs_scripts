# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Fetch temporary AWS credentials from the Foundry AWS broker using a permanent
Pluto machine token (no interactive IMS sign-in required).

Token resolution order:
  1. --token CLI arg
  2. env var PLUTO_TOKEN
  3. credentials.yaml -> foundry_aws.pluto_token
  4. ~/Downloads/creds.txt (raw token on a single line)

Writes a sourceable env file with `export AWS_*` lines (default
~/.claude/hshariati/aws_creds.env) and prints a JSON summary to stdout.
"""
import argparse
import json
import os
import sys
from pathlib import Path

import requests
import yaml

CREDS_YAML = Path.home() / ".claude" / "hshariati" / "credentials.yaml"
DOWNLOADS_FALLBACK = Path.home() / "Downloads" / "creds.txt"
DEFAULT_ENDPOINT = "https://foundry-aws-dev-corp.adobe.io/iam/credentials/aws"
DEFAULT_OUTPUT = Path.home() / ".claude" / "hshariati" / "aws_creds.env"


def load_yaml():
    if CREDS_YAML.exists():
        with open(CREDS_YAML) as f:
            return yaml.safe_load(f) or {}
    return {}


def resolve_token(cli_token: str | None) -> str:
    if cli_token:
        return cli_token.strip()
    if os.environ.get("PLUTO_TOKEN"):
        return os.environ["PLUTO_TOKEN"].strip()
    cfg = load_yaml().get("foundry_aws", {})
    if cfg.get("pluto_token"):
        return str(cfg["pluto_token"]).strip()
    if DOWNLOADS_FALLBACK.exists():
        txt = DOWNLOADS_FALLBACK.read_text().strip()
        # Only treat as a token if it looks like a JWT (three dot-separated parts)
        if txt.count(".") == 2 and " " not in txt:
            return txt
    raise SystemExit(
        "No Pluto token found. Add foundry_aws.pluto_token to "
        f"{CREDS_YAML}, set PLUTO_TOKEN, or pass --token."
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--token", help="Pluto token (overrides all other sources)")
    ap.add_argument("--endpoint", help="Credential broker URL")
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                    help=f"Env file to write (default {DEFAULT_OUTPUT})")
    ap.add_argument("--no-write", action="store_true",
                    help="Do not write the env file, only print")
    args = ap.parse_args()

    token = resolve_token(args.token)
    cfg = load_yaml().get("foundry_aws", {})
    endpoint = args.endpoint or cfg.get("endpoint") or DEFAULT_ENDPOINT

    try:
        r = requests.get(endpoint, headers={"x-pluto-token": token}, timeout=30)
    except requests.RequestException as e:
        print(json.dumps({"error": f"request failed: {e}"}))
        sys.exit(1)

    if r.status_code != 200:
        print(json.dumps({
            "error": f"broker returned HTTP {r.status_code}",
            "body": r.text[:500],
        }))
        sys.exit(1)

    data = r.json()
    ak = data.get("access_key_id")
    sk = data.get("secret_access_key")
    st = data.get("session_token")
    if not (ak and sk and st):
        print(json.dumps({"error": "missing credential fields", "body": data}))
        sys.exit(1)

    region = data.get("region") or "us-west-2"
    env_lines = [
        f"export AWS_ACCESS_KEY_ID={ak}",
        f"export AWS_SECRET_ACCESS_KEY={sk}",
        f"export AWS_SESSION_TOKEN={st}",
        f"export AWS_DEFAULT_REGION={region}",
        f"export AWS_REGION={region}",
    ]

    out_path = None
    if not args.no_write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text("\n".join(env_lines) + "\n")
        os.chmod(args.output, 0o600)
        out_path = str(args.output)

    print(json.dumps({
        "ok": True,
        "endpoint": endpoint,
        "env_file": out_path,
        "region": region,
        "expiration": data.get("expiration"),
        "access_key_id": ak,
        "source_cmd": f"source {out_path}" if out_path else None,
    }, indent=2))


if __name__ == "__main__":
    main()
