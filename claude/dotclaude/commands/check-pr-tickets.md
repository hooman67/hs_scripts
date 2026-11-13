Check that recently merged PRs reference a Jira ticket in their branch name or title.

Usage: /check-pr-tickets [days=N] [repo=OWNER/NAME]

Parse $ARGUMENTS to extract optional filters:
- days: look-back period for merged PRs (default: 7)
- repo: single repo as owner/name (default: all repos from config)

Then run:

```
uv run --script ~/.claude/scripts/check_pr_tickets.py --days <days> --repo "<owner/name>"
```

Omit flags that weren't provided to use defaults.

After running, parse the JSON and present a report:

**Per repo:**
- VIOLATIONS: Table with PR #, Author, Title, Branch — PRs missing ticket reference
- OK: Count of PRs with valid ticket references

**Summary:**
- Total violations and compliant PRs across all repos

Note: This uses the `gh` CLI — make sure you're authenticated with GitHub.
