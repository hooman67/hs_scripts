# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Check customer wiki landing pages for required sections."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

CONFIG_PATH = Path.home() / ".claude" / "hshariati" / "compliance_config.yaml"
WIKI_SCRIPT = Path.home() / ".claude" / "scripts" / "wiki_read.py"

REQUIRED_SECTIONS = [
    {"name": "Problem Statement", "patterns": [r"problem\s+statement", r"problem\b"]},
    {"name": "Requirements / Use Cases", "patterns": [r"requirement", r"use\s+case"]},
    {"name": "Data PoE", "patterns": [r"data\s+po[e]", r"data\s+point\s+of\s+entry", r"data\s+proof"]},
    {"name": "Eval PoE", "patterns": [r"eval\s+po[e]", r"eval(uation)?\s+point\s+of\s+entry", r"eval(uation)?\s+proof"]},
    {"name": "Experiments / Results PoE", "patterns": [r"experiment", r"results?\s+po[e]"]},
    {"name": "JIRA Initiative", "patterns": [r"jira\s+initiative", r"jira\b", r"initiative"]},
]


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def read_wiki_page(page_id):
    """Use the existing wiki_read.py script to fetch a page."""
    r = subprocess.run(
        ["uv", "run", "--script", str(WIKI_SCRIPT), str(page_id)],
        capture_output=True, text=True, timeout=30,
    )
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def check_sections(body):
    """Check which required sections are present in the page body."""
    body_lower = body.lower()
    found = []
    missing = []

    for section in REQUIRED_SECTIONS:
        matched = False
        for pattern in section["patterns"]:
            if re.search(pattern, body_lower):
                matched = True
                break
        if matched:
            found.append(section["name"])
        else:
            missing.append(section["name"])

    return found, missing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-ids", nargs="*", help="Specific page IDs to check (space-separated)")
    args = parser.parse_args()

    config = load_config()
    customer_pages = config.get("confluence", {}).get("customer_page_ids", {})

    # Build page list
    pages_to_check = {}
    if args.page_ids:
        for pid in args.page_ids:
            pages_to_check[pid] = pid
    elif customer_pages:
        pages_to_check = customer_pages
    else:
        print(json.dumps({
            "ok": False,
            "error": "No customer page IDs configured. Add them to compliance_config.yaml under confluence.customer_page_ids",
        }, indent=2))
        sys.exit(1)

    results = []
    for label, page_id in pages_to_check.items():
        page = read_wiki_page(page_id)
        if page is None or not page.get("ok"):
            results.append({
                "label": label,
                "page_id": page_id,
                "error": "Could not fetch page",
                "found_sections": [],
                "missing_sections": list(s["name"] for s in REQUIRED_SECTIONS),
            })
            continue

        body = page.get("body", "")
        found, missing = check_sections(body)

        results.append({
            "label": label,
            "page_id": page_id,
            "title": page.get("title", ""),
            "url": page.get("url", ""),
            "last_modified": page.get("modified_when", ""),
            "modified_by": page.get("modified_by", ""),
            "found_sections": found,
            "missing_sections": missing,
            "compliant": len(missing) == 0,
        })

    total_violations = sum(1 for r in results if not r.get("compliant", False))

    print(json.dumps({
        "ok": True,
        "pages_checked": len(results),
        "results": results,
        "summary": {
            "total_violations": total_violations,
            "total_compliant": len(results) - total_violations,
            "status": "CLEAN" if total_violations == 0 else "VIOLATIONS_FOUND",
        },
    }, indent=2))


if __name__ == "__main__":
    main()
