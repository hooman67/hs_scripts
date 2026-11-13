# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Check Slack channel health: documentation-in-slack, data without analysis, activity per person."""
import argparse
import json
import re
import sys
from pathlib import Path

import requests
import yaml

CREDS_PATH = Path.home() / ".claude" / "hshariati" / "credentials.yaml"
CONFIG_PATH = Path.home() / ".claude" / "hshariati" / "compliance_config.yaml"

SLACK_BASE = "https://slack.com/api"

# Patterns indicating documentation content (shouldn't live in Slack)
WIKI_URL_PATTERN = re.compile(r"wiki\.corp\.adobe\.com|confluence", re.IGNORECASE)
CANVAS_PATTERN = re.compile(r"slack\.com/(docs|canvas)", re.IGNORECASE)
DATA_URL_PATTERN = re.compile(r"(s3://|gs://|grafana|dashboard|spreadsheet|docs\.google\.com/spreadsheet)", re.IGNORECASE)
STRUCTURED_CONTENT_MARKERS = re.compile(r"(\n[-*]\s|\n\d+\.\s|\n#{1,3}\s|```)", re.MULTILINE)

# Analysis keywords that should accompany data shares
ANALYSIS_KEYWORDS = re.compile(
    r"\b(observ|finding|issue|notice|trend|conclude|analysis|insight|"
    r"next step|recommendation|takeaway|hypothesis|result shows|compared to)\b",
    re.IGNORECASE,
)


def load_creds():
    with open(CREDS_PATH) as f:
        return yaml.safe_load(f)


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def slack_get(token, method, params):
    r = requests.get(
        f"{SLACK_BASE}/{method}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
    )
    if not r.ok:
        return None
    data = r.json()
    if not data.get("ok"):
        return None
    return data


def resolve_user(token, user_id, cache):
    if user_id in cache:
        return cache[user_id]
    data = slack_get(token, "users.info", {"user": user_id})
    if data:
        name = data["user"].get("real_name") or data["user"].get("name", user_id)
        cache[user_id] = name
        return name
    cache[user_id] = user_id
    return user_id


def check_documentation_in_slack(messages, user_cache, token):
    """Flag long structured messages without wiki links, and canvas links."""
    flags = []
    for msg in messages:
        text = msg.get("text", "")
        user_id = msg.get("user", "unknown")
        ts = msg.get("ts", "")
        user_name = resolve_user(token, user_id, user_cache)

        # Check for canvas links
        if CANVAS_PATTERN.search(text):
            flags.append({
                "user": user_name,
                "ts": ts,
                "rule": "canvas_usage",
                "message": "Slack canvas link detected. Canvases should not be used for long-term content — use Confluence.",
                "excerpt": text[:200],
            })
            continue

        # Check for long structured messages without wiki links
        if len(text) > 500 and STRUCTURED_CONTENT_MARKERS.search(text) and not WIKI_URL_PATTERN.search(text):
            flags.append({
                "user": user_name,
                "ts": ts,
                "rule": "documentation_in_slack",
                "message": f"Long structured message ({len(text)} chars) without wiki link. Consider moving to Confluence.",
                "excerpt": text[:200],
            })

    return flags


def check_data_without_analysis(messages, user_cache, token):
    """Flag messages sharing data links without accompanying analysis."""
    flags = []
    for msg in messages:
        text = msg.get("text", "")
        user_id = msg.get("user", "unknown")
        ts = msg.get("ts", "")

        if not DATA_URL_PATTERN.search(text):
            continue

        user_name = resolve_user(token, user_id, user_cache)

        # Check if the message includes analysis
        if not ANALYSIS_KEYWORDS.search(text) and len(text) < 200:
            flags.append({
                "user": user_name,
                "ts": ts,
                "rule": "data_without_analysis",
                "message": "Data/results link shared with minimal context. Include observations, issues, and next steps.",
                "excerpt": text[:200],
            })

    return flags


def check_activity(messages, user_cache, token):
    """Track message count per person."""
    counts = {}
    for msg in messages:
        user_id = msg.get("user", "")
        if not user_id or msg.get("subtype"):  # Skip bot messages, joins, etc.
            continue
        user_name = resolve_user(token, user_id, user_cache)
        counts[user_name] = counts.get(user_name, 0) + 1

    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", default=None, help="Slack channel ID (default from config)")
    parser.add_argument("--count", type=int, default=100, help="Number of messages to scan (default 100)")
    args = parser.parse_args()

    creds = load_creds()
    config = load_config()
    token = creds["slack"].get("user_token") or creds["slack"]["token"]
    channel = args.channel or config["slack"]["squad_channel_id"]

    # Fetch messages
    data = slack_get(token, "conversations.history", {"channel": channel, "limit": args.count})
    if data is None:
        print(json.dumps({"ok": False, "error": "Could not read channel. Check channel ID and bot membership."}))
        sys.exit(1)

    messages = data.get("messages", [])
    user_cache = {}

    # Run checks
    doc_flags = check_documentation_in_slack(messages, user_cache, token)
    data_flags = check_data_without_analysis(messages, user_cache, token)
    activity = check_activity(messages, user_cache, token)

    total_flags = len(doc_flags) + len(data_flags)

    print(json.dumps({
        "ok": True,
        "channel": channel,
        "messages_scanned": len(messages),
        "checks": {
            "documentation_in_slack": {
                "flags": doc_flags,
                "count": len(doc_flags),
            },
            "data_without_analysis": {
                "flags": data_flags,
                "count": len(data_flags),
            },
            "channel_activity": {
                "message_counts": activity,
                "total_messages": len(messages),
            },
        },
        "summary": {
            "total_flags": total_flags,
            "status": "CLEAN" if total_flags == 0 else "REVIEW_NEEDED",
        },
    }, indent=2))


if __name__ == "__main__":
    main()
