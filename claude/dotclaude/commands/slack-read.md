Read recent messages from a Slack channel or thread.

Usage: /slack-read <channel_id> [count=N] [thread_ts=TIMESTAMP]

Parse $ARGUMENTS to extract:
- Channel ID (required — starts with C, D, or G)
- Optional `count=N` (default 10)
- Optional `thread_ts=TIMESTAMP` to read a specific thread

Then run:

```
uv run --script ~/.claude/scripts/slack_read.py -- --channel "<channel_id>" --count <N> --thread-ts "<thread_ts>"
```

Omit `--thread-ts` if not provided. Omit `--count` to use the default (10).

After running, parse the JSON output and present messages in a readable format with author names and timestamps.

Important: This bot token does NOT support `conversations.list` or `search.messages`. The user must provide a channel ID directly. You can find channel IDs from Slack URLs: `app.slack.com/client/TEAM_ID/CHANNEL_ID`.
