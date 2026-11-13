Update an existing Jira ticket: change fields, transition status, or add comments.

Usage: /jira-update <TICKET-KEY> [summary=TEXT] [description=TEXT] [status=STATUS] [assignee=USERNAME] [comment=TEXT] [labels=a,b,c]

Parse $ARGUMENTS to extract:
- Ticket key (required, e.g. FFP-123)
- Optional updates as key=value pairs

Then run:

```
uv run --script ~/.claude/scripts/jira_update.py -- <TICKET-KEY> --summary "<summary>" --status "<status>" --comment "<comment>" --assignee "<assignee>" --labels "<labels>" --description "<description>"
```

Only include flags for values that were provided.

For status transitions: the script checks available transitions. If the requested status isn't available, it reports what statuses are possible.

After running, confirm what was updated.
