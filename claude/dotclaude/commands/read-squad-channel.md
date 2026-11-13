Read all new messages from the foundry_consumer_squad Slack channel since the last read, and update the channel context history.

## Channel Details
- **Channel ID:** C0AKWLP0MCY
- **Channel name:** foundry_consumer_squad
- **Workspace:** Adobe Research (private channel)
- **Access:** Must use `user_token` from `~/.claude/hshariati/credentials.yaml` (NOT the bot token)

## Workflow

### Step 1: Determine where we left off

Read the memory file at `~/.claude/projects/-Users-hshariati-hs-scripts/memory/project_squad_channel_history.md` to find the last message timestamp that was processed. If no previous read, default to 2 weeks ago.

### Step 2: Fetch new messages

Use the Slack API directly with the user token (do NOT use slack_read.py — it uses the bot token which cannot access this channel):

```python
import yaml, requests, json, time
from datetime import datetime

with open('/Users/hshariati/.claude/hshariati/credentials.yaml') as f:
    creds = yaml.safe_load(f)
token = creds['slack']['user_token']
headers = {'Authorization': f'Bearer {token}'}

# Fetch messages since last read
params = {'channel': 'C0AKWLP0MCY', 'limit': 200, 'oldest': LAST_TIMESTAMP}
r = requests.get('https://slack.com/api/conversations.history', headers=headers, params=params)
```

Paginate if needed (check `response_metadata.next_cursor`).

### Step 3: Fetch all threads

For every message with `reply_count > 0`, fetch the full thread:

```python
r = requests.get('https://slack.com/api/conversations.replies', headers=headers,
                  params={'channel': 'C0AKWLP0MCY', 'ts': thread_ts, 'limit': 200})
```

Rate limit: add 0.3s delay between thread fetches.

### Step 4: Resolve user IDs

Resolve all unique user IDs to display names using `users.info` API. Cache results.

### Step 5: Analyze and summarize

For each distinct workstream/topic, extract:
1. What work was done and by whom
2. Current status
3. Blockers or issues raised
4. Decisions made
5. Action items mentioned

Group by customer/initiative:
- **THD** (Home Depot) — Initiative FFP-55497
- **TCCC** (Coca-Cola) — Initiative FFP-55486
- **HUMAIN** — Initiative FFP-55500
- **Cross-Customer** — Initiative FFP-79125

Key team members: Hooman (hshariati), Harish (Hareesh Ravi), Abhinav (Abhinav Sharma), Pratyusha (Prathyusha Charagondla), Joshua (Joshua Munoz-ramos), Kanak (Kanak Mahadik), Dongsheng (Dongsheng An), Arpit (Arpit Mathur), Sudeep (Sudeep Katakol), Tyler (Tyler Termini)

### Step 6: Update the history memory

Update `~/.claude/projects/-Users-hshariati-hs-scripts/memory/project_squad_channel_history.md` with:
- New last read date
- Last message timestamp processed
- Count of messages processed
- Brief summary of new context learned

### Step 7: Present findings

Present the summary to the user organized by customer/initiative. Highlight:
- New information since last read
- Action items and blockers
- Any items that may need Jira ticket creation or updates
