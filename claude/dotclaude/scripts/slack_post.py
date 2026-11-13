# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Post a message to Slack."""
import argparse
import json
import sys
from pathlib import Path

import requests
import yaml

CREDS_PATH = Path.home() / ".claude" / "hshariati" / "credentials.yaml"


def load_creds():
    with open(CREDS_PATH) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", required=True)
    parser.add_argument("--channel", default=None, help="Channel ID. If omitted, DMs the bot owner.")
    parser.add_argument("--thread-ts", default=None, help="Thread timestamp to reply in.")
    args = parser.parse_args()

    creds = load_creds()
    # Prefer user_token (posts as you) over bot token
    using_user_token = bool(creds["slack"].get("user_token"))
    token = creds["slack"].get("user_token") or creds["slack"]["token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    channel = args.channel
    if not channel:
        # Default to DM channel from credentials
        channel = creds["slack"].get("dm_channel")
        if not channel:
            # Fallback: open a DM via API
            user_id = creds["slack"].get("user_id")
            if not user_id:
                print(json.dumps({"error": "No --channel specified and no slack.dm_channel or slack.user_id in credentials."}))
                sys.exit(1)
            r = requests.post("https://slack.com/api/conversations.open", headers=headers, json={"users": user_id})
            r.raise_for_status()
            dm = r.json()
            if not dm["ok"]:
                print(json.dumps({"error": f"conversations.open failed: {dm.get('error')}"}))
                sys.exit(1)
            channel = dm["channel"]["id"]

    message = f":claude-ai: {args.message}"
    payload = {"channel": channel, "text": message}
    if using_user_token:
        payload["as_user"] = True
    if args.thread_ts:
        payload["thread_ts"] = args.thread_ts

    r = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)
    r.raise_for_status()
    data = r.json()

    if not data["ok"]:
        print(json.dumps({"error": data.get("error"), "needed": data.get("needed", "")}))
        sys.exit(1)

    print(json.dumps({
        "ok": True,
        "channel": data["channel"],
        "ts": data["ts"],
        "message": args.message,
    }))


if __name__ == "__main__":
    main()
