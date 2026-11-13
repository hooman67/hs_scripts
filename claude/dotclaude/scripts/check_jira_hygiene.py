# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Check Jira ticket hygiene: descriptions, artifacts, closing comments."""
import argparse
import json
import re
import sys
from pathlib import Path

import requests
import yaml

CREDS_PATH = Path.home() / ".claude" / "hshariati" / "credentials.yaml"
CONFIG_PATH = Path.home() / "hs_scripts" / "claude" / "monitor" / "consumer_squad_profile.md"
JIRA_BASE = "https://jira.corp.adobe.com"

OUTCOME_KEYWORDS = re.compile(
    r"\b(goal|expected|outcome|acceptance|deliver|result|objective|success criteria|definition of done)\b",
    re.IGNORECASE,
)
URL_PATTERN = re.compile(r"https?://\S+")


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


def jira_search(headers, jql, fields, max_results=50):
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


def jira_get_issue(headers, key):
    r = requests.get(
        f"{JIRA_BASE}/rest/api/2/issue/{key}",
        headers=headers,
        params={"fields": "comment,description"},
        verify=False,
    )
    if not r.ok:
        return None
    return r.json()


def check_open_tickets(headers, project):
    """Check open sprint tickets for description quality."""
    jql = (
        f'project = "{project}" AND sprint in openSprints() '
        f"AND status != Closed AND status != Done "
        f"ORDER BY assignee ASC"
    )
    fields = ["summary", "status", "assignee", "description", "issuetype"]
    data = jira_search(headers, jql, fields)

    violations = []
    warnings = []

    for item in data.get("issues", []):
        f = item["fields"]
        key = item["key"]
        assignee = (f.get("assignee") or {}).get("displayName", "Unassigned")
        summary = f.get("summary", "")
        desc = f.get("description") or ""

        if not desc.strip():
            violations.append({
                "key": key,
                "url": f"{JIRA_BASE}/browse/{key}",
                "assignee": assignee,
                "summary": summary,
                "rule": "empty_description",
                "message": "Ticket has no description. Must have context and expected outcome.",
            })
        elif len(desc.strip()) < 50:
            warnings.append({
                "key": key,
                "url": f"{JIRA_BASE}/browse/{key}",
                "assignee": assignee,
                "summary": summary,
                "rule": "short_description",
                "message": f"Description is only {len(desc.strip())} chars (min 50). Likely missing context or expected outcome.",
            })
        elif not OUTCOME_KEYWORDS.search(desc):
            warnings.append({
                "key": key,
                "url": f"{JIRA_BASE}/browse/{key}",
                "assignee": assignee,
                "summary": summary,
                "rule": "no_expected_outcome",
                "message": "Description exists but no expected outcome keywords found (goal, expected, outcome, acceptance, result, etc.).",
            })

    return violations, warnings, data.get("total", 0)


def check_done_tickets(headers, project, days=7):
    """Check recently closed tickets for artifacts and closing comments."""
    jql = (
        f'project = "{project}" AND status in (Done, Closed) '
        f"AND resolved >= -{days}d "
        f"ORDER BY assignee ASC"
    )
    fields = ["summary", "status", "assignee", "description", "comment", "issuetype"]
    data = jira_search(headers, jql, fields)

    violations = []
    warnings = []

    for item in data.get("issues", []):
        f = item["fields"]
        key = item["key"]
        assignee = (f.get("assignee") or {}).get("displayName", "Unassigned")
        summary = f.get("summary", "")
        desc = f.get("description") or ""
        comments = f.get("comment", {}).get("comments", []) or []

        # Combine all text for URL search
        all_text = desc + " ".join(c.get("body", "") for c in comments)
        has_urls = bool(URL_PATTERN.search(all_text))
        has_pr_link = bool(re.search(r"github\.com/.+/pull/\d+", all_text))

        if len(comments) == 0 and not has_urls:
            violations.append({
                "key": key,
                "url": f"{JIRA_BASE}/browse/{key}",
                "assignee": assignee,
                "summary": summary,
                "rule": "no_artifacts",
                "message": "Done ticket has 0 comments and no URLs in description. Missing work artifacts (PR links, results, conclusions).",
            })
        elif not has_urls:
            warnings.append({
                "key": key,
                "url": f"{JIRA_BASE}/browse/{key}",
                "assignee": assignee,
                "summary": summary,
                "rule": "no_links",
                "message": f"Done ticket has {len(comments)} comment(s) but no URLs found anywhere. Consider linking PRs, results, or wiki pages.",
            })
        elif not has_pr_link:
            warnings.append({
                "key": key,
                "url": f"{JIRA_BASE}/browse/{key}",
                "assignee": assignee,
                "summary": summary,
                "rule": "no_pr_link",
                "message": "Done ticket has URLs but no GitHub PR link found. If code was changed, link the PR.",
            })

    return violations, warnings, data.get("total", 0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=None, help="Jira project key (default from config)")
    parser.add_argument("--days", type=int, default=7, help="Look-back days for done tickets (default 7)")
    parser.add_argument("--check", choices=["all", "open", "done"], default="all", help="Which checks to run")
    args = parser.parse_args()

    creds = load_creds()
    config = load_config()
    token = creds["jira"]["token"]
    project = args.project or config["jira"]["project"]
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    result = {"ok": True, "project": project, "checks": {}}

    if args.check in ("all", "open"):
        v, w, total = check_open_tickets(headers, project)
        result["checks"]["open_tickets"] = {
            "total_checked": total,
            "violations": v,
            "warnings": w,
            "violation_count": len(v),
            "warning_count": len(w),
        }

    if args.check in ("all", "done"):
        v, w, total = check_done_tickets(headers, project, args.days)
        result["checks"]["done_tickets"] = {
            "total_checked": total,
            "lookback_days": args.days,
            "violations": v,
            "warnings": w,
            "violation_count": len(v),
            "warning_count": len(w),
        }

    # Summary
    total_violations = sum(c["violation_count"] for c in result["checks"].values())
    total_warnings = sum(c["warning_count"] for c in result["checks"].values())
    result["summary"] = {
        "total_violations": total_violations,
        "total_warnings": total_warnings,
        "status": "CLEAN" if total_violations == 0 and total_warnings == 0
                  else "WARNINGS" if total_violations == 0
                  else "VIOLATIONS_FOUND",
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
