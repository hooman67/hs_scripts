Check Jira ticket hygiene for the consumer squad: descriptions, expected outcomes, artifacts on done tickets.

Usage: /check-jira-hygiene [project=KEY] [days=N] [check=all|open|done]

Parse $ARGUMENTS to extract optional filters:
- project: Jira project key (default: FFP from compliance config)
- days: look-back period for done ticket checks (default: 7)
- check: which checks to run — "all" (default), "open" (sprint tickets only), "done" (recently closed only)

Then run:

```
uv run --script ~/.claude/scripts/check_jira_hygiene.py -- --project "<project>" --days <days> --check "<check>"
```

Omit flags that weren't provided to use defaults.

After running, parse the JSON and present a compliance report with two sections:

**1. Open Sprint Tickets** (description quality)
- Table with columns: Status (VIOLATION/WARNING), Ticket, Assignee, Issue
- Group by assignee

**2. Recently Done Tickets** (artifact completeness)
- Table with columns: Status (VIOLATION/WARNING), Ticket, Assignee, Issue
- Group by assignee

**3. Summary**
- Total violations and warnings
- Overall status: CLEAN / WARNINGS / VIOLATIONS_FOUND
- If violations found, suggest specific actions (e.g., "Ask @engineer to add description to FFP-123")
