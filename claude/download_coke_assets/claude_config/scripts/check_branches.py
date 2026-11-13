# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Check for stale branches (> N days from main) across approved repos."""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

CONFIG_PATH = Path.home() / ".claude" / "hshariati" / "compliance_config.yaml"


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def gh_api(endpoint):
    r = subprocess.run(
        ["gh", "api", endpoint, "--paginate"],
        capture_output=True, text=True, timeout=30,
    )
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)


def gh_api_single(endpoint):
    r = subprocess.run(
        ["gh", "api", endpoint],
        capture_output=True, text=True, timeout=30,
    )
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)


def check_repo(owner, name, max_age_days):
    repo = f"{owner}/{name}"
    branches_data = gh_api(f"repos/{repo}/branches?per_page=100")
    if branches_data is None:
        return {"repo": repo, "error": "Could not fetch branches", "violations": [], "warnings": []}

    violations = []
    warnings = []
    now = datetime.now(timezone.utc)
    skip = {"main", "master", "develop", "dev"}

    for branch in branches_data:
        bname = branch["name"]
        if bname in skip:
            continue

        # Get detailed branch info for last commit date
        detail = gh_api_single(f"repos/{repo}/branches/{bname}")
        if detail is None:
            continue

        commit_date_str = detail.get("commit", {}).get("commit", {}).get("committer", {}).get("date", "")
        if not commit_date_str:
            continue

        commit_date = datetime.fromisoformat(commit_date_str.replace("Z", "+00:00"))
        age_days = (now - commit_date).days

        # Get comparison with main
        compare = gh_api_single(f"repos/{repo}/compare/main...{bname}")
        behind = compare.get("behind_by", 0) if compare else "unknown"
        ahead = compare.get("ahead_by", 0) if compare else "unknown"

        author = detail.get("commit", {}).get("commit", {}).get("author", {}).get("name", "unknown")

        entry = {
            "branch": bname,
            "repo": repo,
            "author": author,
            "age_days": age_days,
            "last_commit": commit_date_str,
            "behind_main": behind,
            "ahead_of_main": ahead,
        }

        if age_days > max_age_days:
            entry["rule"] = "stale_branch"
            entry["message"] = f"Branch is {age_days} days old (max {max_age_days}). {behind} commits behind main."
            violations.append(entry)
        elif age_days > max_age_days - 2:
            entry["rule"] = "approaching_stale"
            entry["message"] = f"Branch is {age_days} days old, approaching {max_age_days}-day limit."
            warnings.append(entry)

    return {"repo": repo, "violations": violations, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-age", type=int, default=None, help="Max branch age in days (default from config)")
    parser.add_argument("--repo", default=None, help="Single repo to check (owner/name). Default: all from config.")
    args = parser.parse_args()

    config = load_config()
    max_age = args.max_age or config["thresholds"]["branch_max_age_days"]

    if args.repo:
        parts = args.repo.split("/")
        repos = [{"owner": parts[0], "name": parts[1]}]
    else:
        repos = config["repos"]

    results = []
    for repo in repos:
        result = check_repo(repo["owner"], repo["name"], max_age)
        results.append(result)

    total_violations = sum(len(r["violations"]) for r in results)
    total_warnings = sum(len(r["warnings"]) for r in results)

    print(json.dumps({
        "ok": True,
        "max_age_days": max_age,
        "repos_checked": len(results),
        "results": results,
        "summary": {
            "total_violations": total_violations,
            "total_warnings": total_warnings,
            "status": "CLEAN" if total_violations == 0 and total_warnings == 0
                      else "WARNINGS" if total_violations == 0
                      else "VIOLATIONS_FOUND",
        },
    }, indent=2))


if __name__ == "__main__":
    main()
