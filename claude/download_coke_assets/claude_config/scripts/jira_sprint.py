# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Show current sprint tickets from Jira."""
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
    parser.add_argument("--assignee", default=None, help="Assignee email. Defaults to jira.email from creds.")
    parser.add_argument("--project", default=None, help="Project key. Defaults to jira.project from creds.")
    parser.add_argument("--jql", default=None, help="Raw JQL override (ignores --assignee and --project)")
    args = parser.parse_args()

    creds = load_creds()
    token = creds["jira"]["token"]
    email = args.assignee or creds["jira"]["email"]
    project = args.project or creds["jira"].get("project")
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    if args.jql:
        jql = args.jql
    else:
        parts = ["sprint in openSprints()"]
        if project:
            parts.append(f'project = "{project}"')
        parts.append(f'assignee = "{email}"')
        parts.append("ORDER BY priority DESC, status ASC")
        jql = " AND ".join(parts[:-1]) + " " + parts[-1]

    r = requests.get(
        f"{JIRA_BASE}/rest/api/2/search",
        headers=headers,
        params={"jql": jql, "maxResults": 50, "fields": "summary,status,priority,assignee,issuetype,customfield_10004"},
        verify=False,
    )

    if not r.ok:
        print(json.dumps({"error": r.text, "status_code": r.status_code}))
        sys.exit(1)

    data = r.json()
    issues = []
    for item in data.get("issues", []):
        f = item["fields"]
        issues.append({
            "key": item["key"],
            "url": f"{JIRA_BASE}/browse/{item['key']}",
            "summary": f.get("summary", ""),
            "status": f.get("status", {}).get("name", ""),
            "priority": (f.get("priority") or {}).get("name", ""),
            "type": (f.get("issuetype") or {}).get("name", ""),
            "story_points": f.get("customfield_10004"),
            "assignee": (f.get("assignee") or {}).get("displayName", "Unassigned"),
        })

    print(json.dumps({
        "ok": True,
        "jql": jql,
        "total": data.get("total", 0),
        "issues": issues,
    }, indent=2))


if __name__ == "__main__":
    main()
