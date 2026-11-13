---
name: Canvas modifications via paste-markdown only — never API
description: When Hooman asks to edit any Slack canvas, generate complete updated markdown for him to paste manually. NEVER call canvases.edit. Always show the colorful warning banner first.
type: feedback
originSessionId: 22ddc624-2589-4eb3-9813-dbb9679793af
---
**Rule:** When Hooman asks to modify ANY Slack canvas, do **NOT** call `canvases.edit` / `canvases.sections.lookup` / any canvas-write API. Generate the **complete** updated canvas markdown and output it for him to paste into the Slack canvas UI manually.

**Why:** We tried it. The Slack canvas API operates only on paragraph-level `section_id`s. It cannot extend a table, add a column, or do any structural edit cleanly. On canvas `F0AUTFXEP28` (C-tech & EM Ticket Tracker) we attempted:

1. `insert_at_end` with a markdown row → rendered as a literal-pipe paragraph below the table.
2. `insert_after` with a full markdown table fragment → produced a stray second table.
3. Cleanup via `delete` of the cell `section_id`s → left an unrecoverable empty 2×3 table scaffold (cells without addressable IDs).

Every attempt either failed visibly or required Hooman to clean up the canvas in the Slack UI. The paste-markdown approach is fast, reliable, and preserves user-maintained content (Notes column, manual fixes) perfectly.

**How to apply** when asked to modify a canvas:

1. Fetch current canvas state via `files.info` → download `url_private` body with the user_token.
2. Parse the HTML rows/cells into structured data (regex on `<tr>`/`<td>`, convert `<lnk>` → `[text](url)`, `<i>` → `*…*`).
3. Apply the requested transformation (add row, add column, reorder, etc.) on the parsed data.
4. Render to clean markdown.
5. **Output the markdown to Hooman with the colorful banner below — DO NOT touch any canvas write API.**

**Colorful banner to display ABOVE the markdown every time:**

```
🌈🎨🚨 HEY HOOMAN — WE'VE BEEN HERE BEFORE 🚨🎨🌈
🟥🟧🟨🟩🟦🟪 Slack canvas API = 💔 pain. We've tried. It loses every time. 🟪🟦🟩🟨🟧🟥
✨🪄 Just paste the markdown below into the canvas in Slack 🪄✨
🎉🎊🎈 Cmd-A → Cmd-V → done. No API thrash. 🎈🎊🎉
```

Use it verbatim — the colors (emojis as proxies for color) and tone are intentional. Hooman asked for "colorful and fun" so this banner stays bright.

**Exception:** None. Even for "small" edits, paste-markdown wins. The prior failures showed that even appending a single row breaks the table.
