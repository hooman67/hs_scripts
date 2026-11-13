Create a new Jira ticket.

Usage: /jira-create <summary> [project=KEY] [type=Task|Bug|Story|Epic] [epic=EPIC-KEY] [parent-initiative=INIT-KEY] [parent=SUB-PARENT] [assignee=USERNAME] [labels=a,b,c] [description=DESC]

Parse $ARGUMENTS to extract:
- Summary text (required — everything that isn't a key=value pair)
- Optional key=value pairs: project, type, epic, parent-initiative, parent, assignee, labels, description

**Terminology — IMPORTANT:**
- "Ticket" ALWAYS means issue type **Task**. If Hooman says "create a ticket", default `--type Task`. Never assume Epic or Initiative.
- Adobe Jira hierarchy: Initiative → Epic → Task. Linking uses two DIFFERENT fields:
  - `--epic <EPIC-KEY>` → sets **Epic Link** (`customfield_11800`). Use for Tasks/Stories/Bugs to link to their Epic.
  - `--parent-initiative <INIT-KEY>` → sets **Parent Link** (`customfield_21401`). Use ONLY when creating an Epic, to link it to its Initiative.
  - `--parent <KEY>` is for sub-tasks ONLY (the REST `parent` field). Do NOT use it to set Epic Link or Parent Link.
- Tasks have Epic Link and NO Parent Link. Epics have Parent Link and NO Epic Link. Never mix them up.

Then run:

```
uv run --script ~/.claude/scripts/jira_create.py -- --summary "<summary>" --project "<project>" --type "<type>" --epic "<epic>" --parent-initiative "<parent-initiative>" --parent "<parent>" --assignee "<assignee>" --labels "<labels>" --description "<description>"
```

Omit flags that weren't provided. The script defaults to project from credentials.yaml and type "Task". The script enforces that `--epic` is only allowed for non-Epic types, and `--parent-initiative` is only allowed when type=Epic.

If the user's request is vague, ask for at minimum a summary before running.

After running, show the created ticket key and URL.
