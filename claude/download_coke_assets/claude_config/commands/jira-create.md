Create a new Jira ticket.

Usage: /jira-create <summary> [project=KEY] [type=Task|Bug|Story|Epic] [parent=PARENT-KEY] [assignee=USERNAME] [labels=a,b,c] [description=DESC]

Parse $ARGUMENTS to extract:
- Summary text (required — everything that isn't a key=value pair)
- Optional key=value pairs: project, type, parent, assignee, labels, description

Then run:

```
uv run --script ~/.claude/scripts/jira_create.py -- --summary "<summary>" --project "<project>" --type "<type>" --parent "<parent>" --assignee "<assignee>" --labels "<labels>" --description "<description>"
```

Omit flags that weren't provided. The script defaults to project from credentials.yaml and type "Task".

If the user's request is vague, ask for at minimum a summary before running.

After running, show the created ticket key and URL.
