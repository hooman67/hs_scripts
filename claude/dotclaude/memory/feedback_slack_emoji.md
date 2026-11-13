---
name: Slack claude-ai emoji prefix
description: All Slack messages sent on Hooman's behalf MUST start with exactly one :claude-ai: emoji
type: feedback
---

Every Slack message sent on Hooman's behalf must start with exactly one `:claude-ai:` emoji prefix.

**Why:** Hooman wants recipients to know the message was sent by Claude on his behalf. He has corrected this multiple times — sometimes the emoji is missing (when using direct API calls), sometimes duplicated (when the script adds it AND the caller adds it).

**How to apply:**
- When using `slack_post.py`: the script already prepends `:claude-ai:` on line 53. Do NOT add the emoji to the message text — the script handles it.
- When using direct Slack API calls (requests.post to chat.postMessage): ALWAYS prepend `:claude-ai: ` to the message text manually.
- When using `files.completeUploadExternal` with `initial_comment`: ALWAYS prepend `:claude-ai: ` to the initial_comment.
- NEVER add the emoji if it's already present in the message (prevents duplication).
