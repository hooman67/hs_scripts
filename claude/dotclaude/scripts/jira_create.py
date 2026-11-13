# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Create a Jira ticket."""
import argparse
import json
import sys
from pathlib import Path

import requests
import yaml

CREDS_PATH = Path.home() / ".claude" / "hshariati" / "credentials.yaml"
JIRA_BASE = "https://jira.corp.adobe.com"

# Adobe Jira hierarchy: Initiative -> Epic -> Task. Two DIFFERENT fields:
#   Epic Link   (customfield_11800): used on Tasks/Stories/Bugs to point at parent Epic
#   Parent Link (customfield_21401): used on Epics to point at parent Initiative
EPIC_LINK_FIELD = "customfield_11800"
PARENT_LINK_FIELD = "customfield_21401"

# FFP project requires Components and Assigned Team on every ticket.
FFP_REQUIRED_FIELDS = {
    "components": [{"id": "270800"}],          # Foundry
    "customfield_13401": [{"id": "185325"}],   # Assigned Team: AI Platform Technology
}


def load_creds():
    with open(CREDS_PATH) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--type", default="Task", help="Issue type: Task, Bug, Story, Sub-task, Epic")
    parser.add_argument("--project", default=None, help="Project key. Defaults to credentials.yaml jira.project")
    parser.add_argument("--parent", default=None, help="Parent ticket key — for sub-tasks ONLY (not for Epic Link)")
    parser.add_argument("--epic", default=None, help="Epic key for Epic Link (Tasks/Stories/Bugs only)")
    parser.add_argument("--parent-initiative", default=None, dest="parent_initiative",
                        help="Initiative key for Parent Link (Epics only)")
    parser.add_argument("--assignee", default=None, help="Assignee username")
    parser.add_argument("--labels", default=None, help="Comma-separated labels")
    args = parser.parse_args()

    # Guardrails: Epic Link is for non-Epic types; Parent Link is for Epic type.
    if args.epic and args.type.lower() == "epic":
        print(json.dumps({"error": "Epics use --parent-initiative (Parent Link), not --epic (Epic Link)."}))
        sys.exit(1)
    if args.parent_initiative and args.type.lower() != "epic":
        print(json.dumps({"error": "--parent-initiative (Parent Link) is only valid when --type Epic."}))
        sys.exit(1)

    creds = load_creds()
    token = creds["jira"]["token"]
    project = args.project or creds["jira"].get("project", "PROJ")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    fields = {
        "project": {"key": project},
        "summary": args.summary,
        "issuetype": {"name": args.type},
    }

    if args.description:
        fields["description"] = args.description
    if args.parent:
        fields["parent"] = {"key": args.parent}
    if args.epic:
        fields[EPIC_LINK_FIELD] = args.epic
    if args.parent_initiative:
        fields[PARENT_LINK_FIELD] = args.parent_initiative
    if args.assignee:
        fields["assignee"] = {"name": args.assignee}
    if args.labels:
        fields["labels"] = [l.strip() for l in args.labels.split(",")]

    if project == "FFP":
        for k, v in FFP_REQUIRED_FIELDS.items():
            fields.setdefault(k, v)

    r = requests.post(
        f"{JIRA_BASE}/rest/api/2/issue",
        headers=headers,
        json={"fields": fields},
        verify=False,
    )

    if not r.ok:
        print(json.dumps({"error": r.text, "status_code": r.status_code}))
        sys.exit(1)

    data = r.json()
    print(json.dumps({
        "ok": True,
        "key": data["key"],
        "url": f"{JIRA_BASE}/browse/{data['key']}",
        "summary": args.summary,
    }, indent=2))


if __name__ == "__main__":
    main()
