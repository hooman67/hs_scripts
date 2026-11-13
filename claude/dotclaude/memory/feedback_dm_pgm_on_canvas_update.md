---
name: DM the PGM on every C-tech/EM canvas update
description: Whenever the C-tech & EM Ticket Tracker canvas (F0AUTFXEP28) is updated, draft a DM to the squad PGM (currently Lingyan Zhao) summarizing what changed and confirm with Hooman before sending.
type: feedback
originSessionId: 22ddc624-2589-4eb3-9813-dbb9679793af
---
**Rule:** After any update to the C-tech & EM Ticket Tracker canvas (`F0AUTFXEP28`) — whether the update is done via paste-markdown, via the Slack UI directly by Hooman, or via API — draft a DM to the squad PGM summarizing the change and **confirm with Hooman before sending**. Send only on explicit "yes".

**Current PGM: Lingyan Zhao** (lingyanz, lingyanz@adobe.com). Replaced Hardy Han in 2026-05. See [[user_profile]].

**Why:** The PGM uses this canvas to track active C-tech/EM tickets across customer projects. They should be notified each time the canvas changes so their tracking stays current. Hooman wants the confirmation gate so he controls outbound Slack content.

**How to apply:**

1. After any canvas modification (or when Hooman tells you he updated it himself), draft a short DM summarizing the change. Cover: ticket key + link, summary, assignee, customer, due date if relevant, what action was taken (added / removed / status updated).
2. Show the draft to Hooman and ask for explicit approval.
3. On "yes", send via `chat.postMessage` to the PGM's DM channel.
4. Use the user_token (Adobe Research workspace), prepend `:claude-ai: ` per the slack-emoji feedback rule.
5. Use Slack mrkdwn: `<URL|text>` for links, `_text_` for italic, `*text*` for bold (NOT markdown's `[text](URL)` or `*italic*`).

**Reference IDs (also in [[user_profile]]):**
- Lingyan Zhao (current PGM): username `lingyanz`, email `lingyanz@adobe.com`, DM channel `D0B9F8A5LJD`
- Hardy Han (former PGM): Slack user ID `U0AMJBCB78S`, DM channel `D0AU1559XLG`, username `hardyh`

**Sample DM template:**
```
:claude-ai: Just <added|updated|removed> <jira_url|FFP-XXXXX> — _<summary>_ (assigned <Assignee>, <customer>, <due YYYY-MM-DD>) — to/from the C-tech & EM Ticket Tracker canvas.
```
