# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Check that merged PRs reference a Jira ticket in branch name or title."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

CONFIG_PATH = Path.home() / "hs_scripts" / "claude" / "monitor" / "consumer_squad_profile.md"
TICKET_PATTERN = re.compile(r"[A-Z]{2,}-\d+")


def load_config():
    # Config lives in the ```yaml block of the consolidated squad profile markdown.
    text = CONFIG_PATH.read_text()
    marker = "```yaml"
    start = text.index(marker) + len(marker)
    end = text.index("```", start)
    return yaml.safe_load(text[start:end])


def gh_pr_list(owner, name, days):
    """List recently merged PRs."""
    r = subprocess.run(
        [
            "gh", "pr", "list",
            "--repo", f"{owner}/{name}",
            "--state", "merged",
            "--search", f"merged:>=$(date -v-{days}d +%Y-%m-%d)",
            "--json", "number,title,author,headRefName,mergedAt,url",
            "--limit", "100",
        ],
        capture_output=True, text=True, timeout=30,
    )
    if r.returncode != 0:
        # Fallback: try without date filter
        r2 = subprocess.run(
            [
                "gh", "pr", "list",
                "--repo", f"{owner}/{name}",
                "--state", "merged",
                "--json", "number,title,author,headRefName,mergedAt,url",
                "--limit", "50",
            ],
            capture_output=True, text=True, timeout=30,
        )
        if r2.returncode != 0:
            return None
        return json.loads(r2.stdout)
    return json.loads(r.stdout)


def check_repo(owner, name, days):
    repo = f"{owner}/{name}"
    prs = gh_pr_list(owner, name, days)
    if prs is None:
        return {"repo": repo, "error": "Could not fetch PRs", "violations": [], "ok_prs": []}

    violations = []
    ok_prs = []

    for pr in prs:
        title = pr.get("title", "")
        branch = pr.get("headRefName", "")
        number = pr.get("number", "")
        author = pr.get("author", {}).get("login", "unknown")
        url = pr.get("url", "")

        # Check for ticket reference in branch name or PR title
        ticket_in_branch = TICKET_PATTERN.search(branch)
        ticket_in_title = TICKET_PATTERN.search(title)

        if ticket_in_branch or ticket_in_title:
            ticket = (ticket_in_branch or ticket_in_title).group()
            ok_prs.append({
                "pr": number,
                "url": url,
                "author": author,
                "ticket": ticket,
                "found_in": "branch" if ticket_in_branch else "title",
            })
        else:
            violations.append({
                "pr": number,
                "url": url,
                "author": author,
                "title": title,
                "branch": branch,
                "rule": "no_ticket_reference",
                "message": f"PR #{number} has no Jira ticket key in branch name or title.",
            })

    return {"repo": repo, "violations": violations, "ok_prs": ok_prs}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7, help="Look-back days for merged PRs (default 7)")
    parser.add_argument("--repo", default=None, help="Single repo (owner/name). Default: all from config.")
    args = parser.parse_args()

    config = load_config()

    if args.repo:
        parts = args.repo.split("/")
        repos = [{"owner": parts[0], "name": parts[1]}]
    else:
        repos = config["repos"]

    results = []
    for repo in repos:
        result = check_repo(repo["owner"], repo["name"], args.days)
        results.append(result)

    total_violations = sum(len(r["violations"]) for r in results)
    total_ok = sum(len(r["ok_prs"]) for r in results)

    print(json.dumps({
        "ok": True,
        "lookback_days": args.days,
        "repos_checked": len(results),
        "results": results,
        "summary": {
            "total_violations": total_violations,
            "total_ok": total_ok,
            "status": "CLEAN" if total_violations == 0 else "VIOLATIONS_FOUND",
        },
    }, indent=2))


if __name__ == "__main__":
    main()
