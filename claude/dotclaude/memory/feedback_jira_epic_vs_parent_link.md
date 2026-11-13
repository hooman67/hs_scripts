---
name: Jira Epic Link vs Parent Link — never confuse them
description: Tasks link to Epics via Epic Link (customfield_11800); Epics link to Initiatives via Parent Link (customfield_21401)
type: feedback
originSessionId: 52ca1b78-05fe-490c-bfbf-a943581e6aa0
---
In Adobe Jira (jira.corp.adobe.com), the linkage hierarchy is **Initiative → Epic → Task**, and there are two DIFFERENT custom fields used:

- **Epic Link** = `customfield_11800` — used ONLY on **Tasks** (and Stories/Bugs) to point at their parent Epic.
- **Parent Link** = `customfield_21401` — used ONLY on **Epics** to point at their parent Initiative.

Tasks have **Epic Link** and NO Parent Link. Epics have **Parent Link** and NO Epic Link. Never mix them up.

**Why:** Hooman caught this on FFP-85853 (created 2026-04-29) where the epic FFP-81146 was incorrectly placed in Parent Link instead of Epic Link, which broke epic-rollup reporting and grouping. The Adobe Jira convention is strict.

**How to apply:**
- Creating a Task linked to an Epic: set `customfield_11800` (Epic Link) to the epic key. Do NOT set `parent` or `customfield_21401`.
- Creating an Epic linked to an Initiative: set `customfield_21401` (Parent Link) to the initiative key. Do NOT set `customfield_11800`.
- The Jira REST `parent` field on issue create is for sub-tasks only — it is NOT the same as Parent Link.
- When fixing a misfiled ticket: set the correct field, then clear the wrong one in the same PUT (`{"customfield_21401": null}` to clear Parent Link).
