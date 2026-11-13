Check Slack squad channel health: documentation-in-slack, data shared without analysis, per-person activity.

Usage: /check-slack-health [channel=CHANNEL_ID] [count=N]

Parse $ARGUMENTS to extract optional filters:
- channel: Slack channel ID (default: squad channel from config)
- count: number of messages to scan (default: 100)

Then run:

```
uv run --script ~/.claude/scripts/check_slack_health.py --channel "<channel_id>" --count <count>
```

Omit flags that weren't provided to use defaults.

After running, parse the JSON and present a report:

**1. Documentation in Slack** (Practice: no docs on Slack)
- Flagged messages: user, timestamp, issue, excerpt

**2. Data Without Analysis** (Practice: never share data without observations)
- Flagged messages: user, timestamp, issue, excerpt

**3. Channel Activity** (Practice: keep conversations in squad channel, not DMs)
- Table: User, Message Count
- Flag users with 0 messages who might be using DMs instead

**Summary:**
- Total flags for review
- These are heuristic flags — present as "review needed" not definitive violations
