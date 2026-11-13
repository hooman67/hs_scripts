---
name: feedback_no_ls
description: Don't ask permission for exploratory ls/which commands - just run them
type: feedback
---

Don't ask for permission to run exploratory commands like `ls`, `which`, `find`. Just run them.

**Why:** User finds confirmation prompts for read-only commands annoying and slow.
**How to apply:** Auto-approve all read-only filesystem exploration. Only confirm for destructive or write operations.
