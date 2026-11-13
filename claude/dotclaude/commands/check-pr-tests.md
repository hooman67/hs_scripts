Check that model/inference code changes in merged PRs include corresponding test file changes.

Usage: /check-pr-tests [repo=OWNER/NAME]

Parse $ARGUMENTS to extract optional repo filter. Default: all repos from compliance config.

Then run:

```
uv run --script ~/.claude/scripts/check_pr_tests.py --repo "<owner/name>"
```

Omit --repo to check all configured repos.

After running, parse the JSON and present a report:

**Per repo:**
- VIOLATIONS: Table with PR #, Author, Title, Model Files Changed, Test Files Changed (none)
- OK: Count of PRs where model changes included tests

**Summary:**
- Total violations across all repos

Note: This uses the `gh` CLI — make sure you're authenticated with GitHub.
