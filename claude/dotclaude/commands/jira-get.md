Get details of a Jira ticket.

Usage: /jira-get <TICKET-KEY>

Parse $ARGUMENTS to extract the ticket key (e.g. FFP-123, PROJ-456).

Then run:

```
uv run --script ~/.claude/scripts/jira_get.py -- <TICKET-KEY>
```

After running, parse the JSON output and present:
- Ticket key, summary, status, priority, type
- Assignee and reporter
- Description (if any)
- Recent comments (if any)
- Subtasks (if any)
- Link to the ticket
