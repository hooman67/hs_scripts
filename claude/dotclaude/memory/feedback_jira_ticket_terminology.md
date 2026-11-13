---
name: Jira "ticket" means Task — never Epic or Initiative
description: When Hooman says "ticket" he means issue type Task only; epics and initiatives are referred to by their type name
type: feedback
originSessionId: 52ca1b78-05fe-490c-bfbf-a943581e6aa0
---
When Hooman says "ticket", he ALWAYS means issue type **Task** — never an Epic or Initiative.

**Why:** This is project-specific vocabulary in his world. Epics and Initiatives are higher-level containers; "ticket" is the term reserved for the concrete unit of work (Task).

**How to apply:**
- "Create a ticket for X" → create a Task (the existing default in `jira_create.py`).
- "Update the ticket" / "look at the ticket" → assume issue type Task unless he gives an explicit Epic/Initiative key.
- When summarizing or reporting, use "ticket" only for Tasks; call epics "the epic" and initiatives "the initiative" by name. Don't refer to FFP-XXXX as "ticket" if it's an Epic or Initiative.
