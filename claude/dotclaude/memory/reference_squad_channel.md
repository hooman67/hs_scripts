---
name: Consumer Squad Slack Channel
description: Foundry Consumer Squad main Slack channel — channel ID, name, and how to access it
type: reference
---

Channel name: `foundry_consumer_squad`
Channel ID: `C0AKWLP0MCY`
Enterprise ID: `E23RE8G4F`

This is the main channel for Hooman's Consumer Squad team. All engineering updates, data sharing, training results, and coordination happen here.

**Workspace:** Adobe Research (NOT Creative Cloud E2E). This is a private channel.

**Access (RESOLVED 2026-03-20):** The bot token (xoxb-...) is on Creative Cloud E2E workspace and CANNOT see this channel. Must use the **user token** (xoxp-...) from credentials.yaml, which Hooman reinstalled on the Adobe Research workspace via the Chiron Slack app.

**How to apply:** Always use the user_token from credentials.yaml for this channel. Use `conversations.history` and `conversations.replies` Slack APIs directly with the user token. Do NOT use the slack_read.py script (it uses the bot token).
