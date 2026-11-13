Update an existing Jira ticket: change fields, transition status, or add comments.

Usage: /jira-update <TICKET-KEY> [summary=TEXT] [description=TEXT] [status=STATUS] [assignee=USERNAME] [comment=TEXT] [labels=a,b,c] [epic=EPIC-KEY] [parent-initiative=INIT-KEY]

Parse $ARGUMENTS to extract:
- Ticket key (required, e.g. FFP-123)
- Optional updates as key=value pairs

**Terminology — IMPORTANT:**
- "Ticket" ALWAYS means issue type **Task**. Epics and Initiatives are referred to by type name.
- `--epic` sets **Epic Link** (`customfield_11800`) — for Tasks/Stories/Bugs only.
- `--parent-initiative` sets **Parent Link** (`customfield_21401`) — for Epics only.
- Tasks must NOT have Parent Link set; Epics must NOT have Epic Link set. To clear either field, pass an empty string (e.g. `epic=""`).

Then run:

```
uv run --script ~/.claude/scripts/jira_update.py -- <TICKET-KEY> --summary "<summary>" --status "<status>" --comment "<comment>" --assignee "<assignee>" --labels "<labels>" --description "<description>" --epic "<epic>" --parent-initiative "<parent-initiative>"
```

Only include flags for values that were provided.

For status transitions: the script checks available transitions. If the requested status isn't available, it reports what statuses are possible.

After running, confirm what was updated.
