---
name: Preserve user edits when updating Slack canvases
description: When updating any Slack canvas Hooman is maintaining, always pull the current canvas state first and merge — never do a blind full replace that wipes his notes
type: feedback
---

When updating a Slack canvas that Hooman actively uses (especially the C-tech/EM Ticket Tracker at `F0AUTFXEP28`), do **not** regenerate the markdown from scratch and `replace` the full content. That wipes out any notes he has added to the Notes column.

**Why:** Hooman maintains these canvases over time — the Notes column is where he writes his own running commentary that only he has. Blowing it away is destructive and unrecoverable from the Slack side.

**How to apply:**

1. Before any canvas edit, fetch the current canvas content. The canvas file's `url_private` (from `files.info`) returns the current markdown body with auth:
   ```
   GET {url_private}
   Authorization: Bearer {user_token}
   ```
   Parse the returned body as markdown.
2. Identify the existing table rows keyed by ticket key (e.g., `FFP-84817`). Preserve the Notes column text for every row that already exists.
3. For new rows, add them with a blank Notes cell.
4. For rows that no longer match the current ticket filter (closed, reassigned outside the roster), either remove them or keep them with a status marker — don't silently drop them.
5. Only then call `canvases.edit` with `operation: "replace"` and the merged markdown.

**Prefer `insert_at_end` over `replace` when adding a small number of rows**, but make sure the appended markdown is a properly-formed table continuation (same column structure). If insert_at_end produces a stray second table in Slack's rendering, fall back to the fetch-merge-replace flow above rather than doing a blind replace.

**Never** assume "Hooman hasn't added notes yet" — once a canvas is DM'd to him and he's had time with it, treat all Notes column content as user-owned and load-bearing.
