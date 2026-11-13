# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Check that eval and documentation tickets make up a healthy percentage of sprint work."""
import argparse
import json
import sys
from pathlib import Path

import requests
import yaml

CREDS_PATH = Path.home() / ".claude" / "hshariati" / "credentials.yaml"
CONFIG_PATH = Path.home() / "hs_scripts" / "claude" / "monitor" / "consumer_squad_profile.md"
JIRA_BASE = "https://jira.corp.adobe.com"

EVAL_DOC_LABELS = {"eval", "evaluation", "docs", "documentation", "testing", "test"}
EVAL_DOC_KEYWORDS = {"eval", "evaluation", "document", "documentation", "test", "testing", "benchmark"}


def load_creds():
    with open(CREDS_PATH) as f:
        return yaml.safe_load(f)


def load_config():
    # Config lives in the ```yaml block of the consolidated squad profile markdown.
    text = CONFIG_PATH.read_text()
    marker = "```yaml"
    start = text.index(marker) + len(marker)
    end = text.index("```", start)
    return yaml.safe_load(text[start:end])


def jira_search(headers, jql, fields, max_results=100):
    r = requests.get(
        f"{JIRA_BASE}/rest/api/2/search",
        headers=headers,
        params={"jql": jql, "maxResults": max_results, "fields": ",".join(fields)},
        verify=False,
    )
    if not r.ok:
        print(json.dumps({"error": r.text, "status_code": r.status_code}))
        sys.exit(1)
    return r.json()


def is_eval_or_docs(issue):
    """Check if a ticket is eval/docs related by labels or summary."""
    labels = set(l.lower() for l in issue["fields"].get("labels", []))
    summary = issue["fields"].get("summary", "").lower()

    # Check labels
    if labels & EVAL_DOC_LABELS:
        return True

    # Check summary keywords
    for kw in EVAL_DOC_KEYWORDS:
        if kw in summary:
            return True

    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=None, help="Jira project key (default from config)")
    parser.add_argument("--threshold", type=int, default=None, help="Min eval/docs percentage (default from config)")
    args = parser.parse_args()

    creds = load_creds()
    config = load_config()
    token = creds["jira"]["token"]
    project = args.project or config["jira"]["project"]
    threshold = args.threshold or config["thresholds"]["eval_docs_sprint_pct"]
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    jql = f'project = "{project}" AND sprint in openSprints() ORDER BY assignee ASC'
    fields = ["summary", "status", "assignee", "labels", "issuetype", "customfield_10004"]
    data = jira_search(headers, jql, fields)

    total_tickets = 0
    eval_doc_tickets = []
    other_tickets = []
    total_points = 0
    eval_doc_points = 0

    for item in data.get("issues", []):
        total_tickets += 1
        points = item["fields"].get("customfield_10004") or 0
        total_points += points

        entry = {
            "key": item["key"],
            "summary": item["fields"].get("summary", ""),
            "assignee": (item["fields"].get("assignee") or {}).get("displayName", "Unassigned"),
            "labels": item["fields"].get("labels", []),
            "points": points,
        }

        if is_eval_or_docs(item):
            eval_doc_tickets.append(entry)
            eval_doc_points += points
        else:
            other_tickets.append(entry)

    ticket_pct = (len(eval_doc_tickets) / total_tickets * 100) if total_tickets > 0 else 0
    points_pct = (eval_doc_points / total_points * 100) if total_points > 0 else 0

    status = "CLEAN" if ticket_pct >= threshold else "VIOLATIONS_FOUND"

    print(json.dumps({
        "ok": True,
        "project": project,
        "sprint_totals": {
            "total_tickets": total_tickets,
            "total_points": total_points,
        },
        "eval_docs": {
            "ticket_count": len(eval_doc_tickets),
            "ticket_percentage": round(ticket_pct, 1),
            "points": eval_doc_points,
            "points_percentage": round(points_pct, 1),
            "tickets": eval_doc_tickets,
        },
        "threshold_pct": threshold,
        "summary": {
            "status": status,
            "message": f"Eval/docs is {ticket_pct:.0f}% of sprint tickets ({len(eval_doc_tickets)}/{total_tickets}). "
                       f"Threshold: {threshold}%.",
        },
    }, indent=2))


if __name__ == "__main__":
    main()
