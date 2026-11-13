---
name: feedback-make-blockers-obvious
description: "When blocked on missing access (tokens, creds, files, permissions), make it the FIRST and LOUDEST thing in the message — never bury in a status report. Use AskUserQuestion. Pre-check access before doing setup."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8f411ee2-3202-480f-a5e4-aab81247a23e
---

When blocked on a missing or expired credential / token / file / permission: make the blocker the **first line** of the response with a clear BLOCKED indicator. Use `AskUserQuestion` to ask for the specific thing. Do NOT continue working on adjacent things or wrap the blocker in a long status update. Mark blocked tasks as blocked (not `in_progress`).

**Why:** Hooman lost a full day on the Humain retry because I left "still blocked on a fresh bearer token at /tmp/auth_token.txt" buried in the middle of a multi-paragraph status report after a long session. From the task list it looked like work was in progress; he assumed things were moving. Compounding mistake: I'd picked an arbitrary path (`/tmp/auth_token.txt`) that doesn't survive reboots and never confirmed it with him.

**How to apply:**
- **Pre-check access first.** Before starting setup work for any task that needs an external token / cred / file, verify it exists and is current. If not, stop and ask before doing anything else.
- **When blocked mid-task, surface it loudly.** First line of the next message must be the blocker (e.g. "**BLOCKED — need fresh bearer token.**"). Use `AskUserQuestion` so the ask is impossible to miss.
- **Don't propose unblocking and then keep doing other busywork** — the message should be the ask, nothing else, until acknowledged.
- **Don't pick arbitrary system paths (`/tmp/...`) for secrets.** Ask Hooman where it should live, or use a stable location like `~/.claude/hshariati/`.
- **Mark blocked tasks correctly.** Don't leave them as `in_progress` — that misleads him at a glance. Either mark them as blocked in the description, or delete and re-create when unblocking.

Applies to: bearer tokens, AWS/Foundry creds, Slack tokens, Jira/Confluence creds, missing config files, missing permissions, expired sessions — anything that requires Hooman to take an action outside the chat for me to proceed.
