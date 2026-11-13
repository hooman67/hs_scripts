# Global Copilot CLI instructions

Hooman Shariati (`hshariati@adobe.com`, LDAP `hshariati`) works on Adobe AI infrastructure and generative models. Project instructions in the working repository still apply.

At the start of a session, read the shared global instructions at `~/.claude/CLAUDE.md`. They are the source of truth for preferences shared with Claude and Codex. For a research session, follow their directions to read `~/.claude/RESEARCH_RULES.md`; do not load that full playbook for unrelated sessions.

The shared skills are generated from `~/.claude/commands/`, with scripts at `~/.claude/scripts/`. Use matching skills proactively. Their source of truth is the Git-backed `hs_scripts/claude/dotclaude` directory; do not maintain a separate copy of a shared workflow in a skill adapter.

Before work where user preferences, project history, Slack/Jira conventions, credentials, or prior operational lessons matter, read `~/.copilot/memory/MEMORY.md` and only the relevant linked memory files. Add durable lessons to that Git-backed index and memory directory, not just to CLI session memory. Treat memory as context, not current verification. Never write credentials into the tracked repo.

When accessing Foundry AWS/S3, use the `aws-creds` skill to obtain temporary credentials. Source `~/.claude/hshariati/aws_creds.env` in the same shell call as `aws`. Never ask the user to paste credentials or place credentials in the shared repository.
