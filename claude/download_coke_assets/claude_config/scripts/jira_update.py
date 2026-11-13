# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Update a Jira ticket: fields, status transitions, or add comments."""
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
    parser.add_argument("--summary", default=None)
    parser.add_argument("--description", default=None)
    parser.add_argument("--assignee", default=None, help="Assignee username")
    parser.add_argument("--status", default=None, help="Target status name, e.g. 'In Progress', 'Done'")
    parser.add_argument("--comment", default=None, help="Add a comment")
    parser.add_argument("--labels", default=None, help="Comma-separated labels (replaces existing)")
    args = parser.parse_args()

    creds = load_creds()
    token = creds["jira"]["token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    results = []

    # Field updates
    fields = {}
    if args.summary:
        fields["summary"] = args.summary
    if args.description:
        fields["description"] = args.description
    if args.assignee:
        fields["assignee"] = {"name": args.assignee}
    if args.labels:
        fields["labels"] = [l.strip() for l in args.labels.split(",")]

    if fields:
        r = requests.put(
            f"{JIRA_BASE}/rest/api/2/issue/{args.ticket}",
            headers=headers,
            json={"fields": fields},
            verify=False,
        )
        if not r.ok:
            print(json.dumps({"error": f"Field update failed: {r.text}", "status_code": r.status_code}))
            sys.exit(1)
        results.append(f"Updated fields: {list(fields.keys())}")

    # Status transition
    if args.status:
        r = requests.get(
            f"{JIRA_BASE}/rest/api/2/issue/{args.ticket}/transitions",
            headers=headers,
            verify=False,
        )
        r.raise_for_status()
        transitions = r.json().get("transitions", [])
        match = next((t for t in transitions if t["name"].lower() == args.status.lower()), None)
        if not match:
            available = [t["name"] for t in transitions]
            print(json.dumps({"error": f"Status '{args.status}' not available. Available: {available}"}))
            sys.exit(1)
        r = requests.post(
            f"{JIRA_BASE}/rest/api/2/issue/{args.ticket}/transitions",
            headers=headers,
            json={"transition": {"id": match["id"]}},
            verify=False,
        )
        if not r.ok:
            print(json.dumps({"error": f"Transition failed: {r.text}"}))
            sys.exit(1)
        results.append(f"Status → {args.status}")

    # Comment
    if args.comment:
        r = requests.post(
            f"{JIRA_BASE}/rest/api/2/issue/{args.ticket}/comment",
            headers=headers,
            json={"body": args.comment},
            verify=False,
        )
        if not r.ok:
            print(json.dumps({"error": f"Comment failed: {r.text}"}))
            sys.exit(1)
        comment_id = r.json().get("id", "")
        results.append(f"Added comment (id: {comment_id})")

    if not results:
        print(json.dumps({"error": "Nothing to update. Provide at least one of: --summary, --description, --assignee, --status, --comment, --labels"}))
        sys.exit(1)

    print(json.dumps({
        "ok": True,
        "ticket": args.ticket,
        "url": f"{JIRA_BASE}/browse/{args.ticket}",
        "updates": results,
    }, indent=2))


if __name__ == "__main__":
    main()
