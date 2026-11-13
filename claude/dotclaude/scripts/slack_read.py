# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Read messages from a Slack channel or thread."""
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


def resolve_users(user_ids, headers):
    """Batch resolve user IDs to display names."""
    cache = {}
    for uid in set(user_ids):
        if uid in cache:
            continue
        r = requests.get(f"https://slack.com/api/users.info?user={uid}", headers=headers)
        if r.ok:
            data = r.json()
            if data.get("ok"):
                u = data["user"]
                cache[uid] = u.get("real_name") or u.get("name", uid)
                continue
        cache[uid] = uid
    return cache


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", required=True, help="Channel or DM ID")
    parser.add_argument("--count", type=int, default=10, help="Number of messages")
    parser.add_argument("--thread-ts", default=None, help="Thread timestamp to read replies")
    args = parser.parse_args()

    creds = load_creds()
    token = creds["slack"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    if args.thread_ts:
        r = requests.get("https://slack.com/api/conversations.replies", headers=headers, params={
            "channel": args.channel,
            "ts": args.thread_ts,
            "limit": args.count,
        })
    else:
        r = requests.get("https://slack.com/api/conversations.history", headers=headers, params={
            "channel": args.channel,
            "limit": args.count,
        })

    r.raise_for_status()
    data = r.json()

    if not data["ok"]:
        print(json.dumps({"error": data.get("error"), "needed": data.get("needed", "")}))
        sys.exit(1)

    messages = data.get("messages", [])
    user_ids = [m.get("user", "") for m in messages if m.get("user")]
    user_map = resolve_users(user_ids, headers)

    output = []
    for m in messages:
        output.append({
            "user": user_map.get(m.get("user", ""), m.get("user", "bot")),
            "text": m.get("text", ""),
            "ts": m.get("ts", ""),
            "thread_ts": m.get("thread_ts", ""),
            "reply_count": m.get("reply_count", 0),
        })

    print(json.dumps({"ok": True, "channel": args.channel, "count": len(output), "messages": output}, indent=2))


if __name__ == "__main__":
    main()
