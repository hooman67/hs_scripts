# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Get Jira ticket details."""
import argparse
import json
import sys
from pathlib import Path

import requests
import yaml

CREDS_PATH = Path.home() / ".claude" / "hshariati" / "credentials.yaml"
JIRA_BASE = "https://jira.corp.adobe.com"


def load_creds():
    with open(CREDS_PATH) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ticket", help="Ticket key, e.g. PROJ-123")
    args = parser.parse_args()

    creds = load_creds()
    token = creds["jira"]["token"]
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    r = requests.get(
        f"{JIRA_BASE}/rest/api/2/issue/{args.ticket}",
        headers=headers,
        params={"expand": "renderedFields"},
        verify=False,
    )

    if r.status_code == 404:
        print(json.dumps({"error": f"Ticket {args.ticket} not found"}))
        sys.exit(1)
    r.raise_for_status()

    issue = r.json()
    fields = issue["fields"]

    comments = []
    for c in (fields.get("comment", {}).get("comments", []) or [])[-5:]:
        comments.append({
            "author": c.get("author", {}).get("displayName", ""),
            "created": c.get("created", ""),
            "body": c.get("body", "")[:500],
        })

    subtasks = [{"key": s["key"], "summary": s["fields"]["summary"], "status": s["fields"]["status"]["name"]}
                for s in (fields.get("subtasks") or [])]

    print(json.dumps({
        "key": issue["key"],
        "url": f"{JIRA_BASE}/browse/{issue['key']}",
        "summary": fields.get("summary", ""),
        "status": fields.get("status", {}).get("name", ""),
        "assignee": (fields.get("assignee") or {}).get("displayName", "Unassigned"),
        "reporter": (fields.get("reporter") or {}).get("displayName", ""),
        "priority": (fields.get("priority") or {}).get("name", ""),
        "type": (fields.get("issuetype") or {}).get("name", ""),
        "description": (fields.get("description") or "")[:2000],
        "comments": comments,
        "subtasks": subtasks,
        "labels": fields.get("labels", []),
        "created": fields.get("created", ""),
        "updated": fields.get("updated", ""),
    }, indent=2))


if __name__ == "__main__":
    main()
