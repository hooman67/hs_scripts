# Global user instructions (Claude Code + Codex)

Loaded in **every** Claude Code session regardless of project or working directory.
Keep this small — only cross-cutting rules that must apply everywhere. Project-specific
detail and the full skill catalog live in `/Users/hshariati/CLAUDE.md` (loads for projects
under the home dir).

Codex loads this same file through `~/.codex/AGENTS.md`. The adapter is installed by
`dotclaude/install-codex.sh`; do not maintain a second copy of these instructions.

## User

Hooman Shariati (hshariati@adobe.com), engineering manager at Adobe — AI platform infra,
generative models (Firefly). LDAP / username everywhere: `hshariati`.

## File paths

Whenever referencing a file in a response, always provide its full absolute filesystem path.
Never give Hooman a relative file path. Render local paths as plain text inside inline or fenced
code blocks so the UI cannot collapse them to a basename or descriptive Markdown-link label. If a
clickable link is also useful, provide it in addition to—not instead of—the visible plain-text path.

## Skills are global

All slash-command skills live in `~/.claude/commands/` (symlinked to the tracked
`hs_scripts/claude/dotclaude/commands`), backed by `~/.claude/scripts/`. They are available
in every project. Codex skill adapters are generated from those same command files, so the
command Markdown remains the single workflow source. Use matching skills proactively.
Credentials: `~/.claude/hshariati/credentials.yaml`.

## Shared memory

The canonical memory index is `hs_scripts/claude/dotclaude/memory/MEMORY.md`. Before work
where user preferences, project history, Slack/Jira conventions, credentials, or prior
operational lessons could matter, read that index and only the relevant linked memory files.
Treat memory as context, not as a substitute for current verification. Never expose or copy
credential values into tracked files.

## Pluto storage

For **all Pluto projects**, keep source code and Git checkouts under `/home/colligo`, but put
bulk datasets, media, generated outputs, raw model traces, environments and caches under
`/mnt/localssd`, not inside the `colligo` or `hs_scripts` checkouts. Small source-controlled
prompts, schemas and provenance manifests may stay with the code. Existing paths may use
symlinks into `/mnt/localssd`; verify copies before removing originals and do not relocate
data or environments used by active jobs. The local SSD is volatile: retain remote backups
for irreplaceable data, not another bulk copy in the home checkout.

## Research sessions — mandatory playbook

When Hooman explicitly says or clearly implies that a session or agent is doing research:

1. Before substantive research work, read the complete `RESEARCH_RULES.md` playbook linked into
   the active agent home: `${HOME}/.claude/RESEARCH_RULES.md` for Claude Code or
   `${HOME}/.codex/RESEARCH_RULES.md` for Codex.
2. Apply the playbook for the entire research session, including when resuming existing work.
3. Complete its mandatory storage preflight: `/mnt/localssd` is volatile scratch; on the Pluto
   host, verify the real `hs_scripts` checkout is under backed-up `/home/colligo` and warn Hooman
   if it is elsewhere. Keep needed research work durable as specified in playbook section 11.
4. If it is unclear whether the session is a research session, ask Hooman before applying the
   playbook.

Do not load the full playbook for unrelated sessions. Project instructions may add research
requirements, but the user's latest explicit instruction takes precedence.

## Pre‑Answer Diagnostic Rule (Global)

Before answering anything non‑trivial (research, recommendations, plans, or changes):

1) List every assumption you are making about the user and their situation.
2) List the five most important unknowns you must clarify to give safe, correct advice.
3) Ask those questions explicitly.
4) Do not write the plan or final answer until the user replies.

Notes:
- Use judgment to skip this only for clearly mechanical actions (e.g., printing a file, running a single command the user asked for verbatim) or when the user has already answered those exact questions in the current thread.
- Always pull the latest state before proposing changes; merge on top of the live source of truth to avoid overwriting user edits.

## AWS / S3 access — always use `/aws-creds`

Whenever an `aws` CLI command needs credentials (any Foundry S3 bucket, e.g.
`foundry-thd-enterprise-adobe-assets`, `foundry-tccc-enterprise-adobe-assets`):

- Run `/aws-creds` (or `uv run --script ~/.claude/scripts/foundry_aws_creds.py`) to fetch
  temporary AWS credentials via the permanent Pluto machine token. **Never** ask Hooman to
  paste credentials manually.
- Then source the env file in the **same** shell command as the `aws` call (env vars do not
  persist across Bash tool calls):
  `source ~/.claude/hshariati/aws_creds.env && aws s3 ls s3://<bucket>/ --region us-west-2`
- Broker creds are short-lived (~24h). On `Unable to locate credentials` / `ExpiredToken`,
  re-run `/aws-creds` to refresh, then re-source.
- Pluto token is stored in `credentials.yaml` under `foundry_aws.pluto_token` (expires
  2026-11-27). To rotate, replace it there or drop a fresh raw token into `~/Downloads/creds.txt`.
