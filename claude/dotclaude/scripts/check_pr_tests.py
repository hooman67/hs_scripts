# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Check that model/inference code changes in PRs include corresponding test changes."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

CONFIG_PATH = Path.home() / "hs_scripts" / "claude" / "monitor" / "consumer_squad_profile.md"

# Patterns that indicate test files
TEST_FILE_PATTERNS = [
    re.compile(r"test_\w+\.py$"),
    re.compile(r"\w+_test\.py$"),
    re.compile(r"tests/"),
    re.compile(r"test/"),
    re.compile(r"\.test\.(ts|js|tsx|jsx)$"),
    re.compile(r"-test\.(ts|js|tsx|jsx)$"),
]


def load_config():
    # Config lives in the ```yaml block of the consolidated squad profile markdown.
    text = CONFIG_PATH.read_text()
    marker = "```yaml"
    start = text.index(marker) + len(marker)
    end = text.index("```", start)
    return yaml.safe_load(text[start:end])


def is_model_file(filepath, model_paths):
    """Check if a file is in a model/inference path."""
    for mp in model_paths:
        if filepath.startswith(mp):
            return True
    # Also catch common inference-related paths
    if re.search(r"(inference|serving|model|training)", filepath, re.IGNORECASE):
        return True
    return False


def is_test_file(filepath):
    """Check if a file is a test file."""
    for pattern in TEST_FILE_PATTERNS:
        if pattern.search(filepath):
            return True
    return False


def get_pr_files(owner, name, pr_number):
    """Get changed files for a PR."""
    r = subprocess.run(
        ["gh", "pr", "diff", str(pr_number), "--repo", f"{owner}/{name}", "--name-only"],
        capture_output=True, text=True, timeout=30,
    )
    if r.returncode != 0:
        return None
    return [f.strip() for f in r.stdout.strip().split("\n") if f.strip()]


def gh_pr_list(owner, name, days):
    """List recently merged PRs."""
    r = subprocess.run(
        [
            "gh", "pr", "list",
            "--repo", f"{owner}/{name}",
            "--state", "merged",
            "--json", "number,title,author,headRefName,mergedAt,url",
            "--limit", "50",
        ],
        capture_output=True, text=True, timeout=30,
    )
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)


def check_repo(owner, name, model_paths):
    repo = f"{owner}/{name}"
    prs = gh_pr_list(owner, name, 7)
    if prs is None:
        return {"repo": repo, "error": "Could not fetch PRs", "violations": [], "ok_prs": []}

    violations = []
    ok_prs = []
    skipped = []

    for pr in prs:
        number = pr.get("number", "")
        title = pr.get("title", "")
        author = pr.get("author", {}).get("login", "unknown")
        url = pr.get("url", "")

        files = get_pr_files(owner, name, number)
        if files is None:
            skipped.append({"pr": number, "reason": "Could not fetch diff"})
            continue

        model_files = [f for f in files if is_model_file(f, model_paths)]
        test_files = [f for f in files if is_test_file(f)]

        if not model_files:
            # No model/inference changes — not applicable
            continue

        if test_files:
            ok_prs.append({
                "pr": number,
                "url": url,
                "author": author,
                "model_files": model_files,
                "test_files": test_files,
            })
        else:
            violations.append({
                "pr": number,
                "url": url,
                "author": author,
                "title": title,
                "model_files_changed": model_files,
                "test_files_changed": [],
                "rule": "model_change_no_tests",
                "message": f"PR #{number} changes model/inference code but has no test file changes.",
            })

    return {"repo": repo, "violations": violations, "ok_prs": ok_prs, "skipped": skipped}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=None, help="Single repo (owner/name). Default: all from config.")
    args = parser.parse_args()

    config = load_config()

    if args.repo:
        parts = args.repo.split("/")
        # Find model_paths from config or use defaults
        model_paths = ["models/", "inference/", "serving/"]
        for r in config["repos"]:
            if r["owner"] == parts[0] and r["name"] == parts[1]:
                model_paths = r.get("model_paths", model_paths)
                break
        repos = [{"owner": parts[0], "name": parts[1], "model_paths": model_paths}]
    else:
        repos = config["repos"]

    results = []
    for repo in repos:
        model_paths = repo.get("model_paths", ["models/", "inference/", "serving/"])
        result = check_repo(repo["owner"], repo["name"], model_paths)
        results.append(result)

    total_violations = sum(len(r["violations"]) for r in results)
    total_ok = sum(len(r.get("ok_prs", [])) for r in results)

    print(json.dumps({
        "ok": True,
        "repos_checked": len(results),
        "results": results,
        "summary": {
            "total_violations": total_violations,
            "total_with_tests": total_ok,
            "status": "CLEAN" if total_violations == 0 else "VIOLATIONS_FOUND",
        },
    }, indent=2))


if __name__ == "__main__":
    main()
