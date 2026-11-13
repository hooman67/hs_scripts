---
name: c-tech-em-ticket-tracker-canvas
description: Slack canvas ID and purpose for the ongoing C-tech/EM ticket tracker Hooman maintains for PGM Hardy
metadata: 
  node_type: memory
  type: reference
  originSessionId: ca1b2d43-eb4a-430a-84b9-fb70db08031e
---

**Canvas ID:** `F0AUTFXEP28`
**Canvas URL:** https://adobe.enterprise.slack.com/docs/T024FSURM/F0AUTFXEP28
**Title:** C-tech & EM Ticket Tracker

**Purpose:** Tracks active Jira tickets assigned to C-techs and EMs across Consumer Squad customer projects (THD, TCCC, HUMAIN, HP, Tesco, DSG). Hooman documents work here so the squad PGM **Lingyan Zhao** (lingyanz, lingyanz@adobe.com, DM channel D0B9F8A5LJD) can track it. (Lingyan replaced Hardy Han as PGM in 2026-05.)

**Excluded scope:** Platform work (Genie, Glimmer, data-marketplace) — not included in this canvas.

**Content structure:** Two-column table — "Jira Tickets" | "Notes". Column 1 has `[FFP-xxxx](url) — summary · assignee · customer · status`. Notes column is user-maintained.

**How to update — ALWAYS preserve user notes:** Hooman writes notes in the Notes column. Never blind-replace the canvas. See [feedback_canvas_preserve_edits.md](feedback_canvas_preserve_edits.md) for the full rule.

Workflow:
1. Fetch current canvas body via `files.info` → use the `url_private` with the user token to retrieve the markdown.
2. Parse the existing table, keyed by Jira ticket key. Preserve each row's Notes cell verbatim.
3. Re-query Jira for active tickets with `assignee in (C-techs + EMs)` and `status not in (Done, Closed, Resolved, Cancelled)` — see user_profile.md for the current rosters. Filter to customer-project tickets only (skip Genie/Glimmer/data-marketplace); identify customer from epic link (`customfield_11800`) or label.
4. Merge: keep existing rows with their original Notes, add new rows with blank Notes, drop rows for tickets that are now out of scope (or keep with a status marker).
5. `canvases.edit` with `operation: "replace"` using the merged markdown.
