Show current sprint tickets from Jira.

Usage: /jira-sprint [assignee=EMAIL] [project=KEY] [jql=RAW_JQL]

Parse $ARGUMENTS to extract optional filters. Defaults to the user's own email and default project from credentials.

Then run:

```
uv run --script ~/.claude/scripts/jira_sprint.py -- --assignee "<email>" --project "<project>" --jql "<jql>"
```

Omit flags that weren't provided to use defaults.

After running, parse the JSON and present as a table with columns: Key, Summary, Status, Priority, Type, Story Points.
