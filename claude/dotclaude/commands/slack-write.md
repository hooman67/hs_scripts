Post a message to Slack. The user provides a message and optionally a channel ID.

Usage: /slack-write <message> [-c CHANNEL_ID] [-t THREAD_TS]

Parse $ARGUMENTS to extract:
- The message text (everything that isn't a flag/option)
- Optional `-c <ID>` or `channel=<ID>` — a Slack channel ID
- Optional `-t <TS>` or `thread_ts=<TS>` — reply in a thread

Then run this command:

```
uv run --script ~/.claude/scripts/slack_post.py --message "<message>" --channel "<channel_id>" --thread-ts "<thread_ts>"
```

Omit `--channel` if not provided (defaults to DMing Hooman).
Omit `--thread-ts` if not provided.

After running, parse the JSON output and confirm to the user what was posted and where.

Note: The bot name in Slack is "colligo-claude". The user's Slack workspace is "Creative Cloud E2E".
