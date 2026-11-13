Check for stale branches (older than 7 days) across approved repos.

Usage: /check-branches [max-age=DAYS] [repo=OWNER/NAME]

Parse $ARGUMENTS to extract optional filters:
- max-age: max branch age in days (default: 7 from config)
- repo: single repo to check as owner/name (default: all repos from config)

Then run:

```
uv run --script ~/.claude/scripts/check_branches.py --max-age <days> --repo "<owner/name>"
```

Omit flags that weren't provided to use defaults.

After running, parse the JSON and present a report:

**Per repo:**
- Table with columns: Status (VIOLATION/WARNING), Branch, Author, Age (days), Behind Main
- Sort by age descending

**Summary:**
- Total stale branches across all repos
- Overall status

Note: This uses the `gh` CLI — make sure you're authenticated with GitHub.
