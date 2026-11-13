Find Pluto jobs that violate the node-allocation canvas and recommend kill candidates. **READ ONLY — never stops any job.** Advisory output for the user to act on.

Usage: /find_node_violation

Cross-references currently-running Pluto jobs against the "Weekly Thu→Thu node request and allocation" canvas and ranks kill candidates:
1. **Running work the canvas REJECTED** (red ❌) — the clearest violation.
2. **Dev boxes using > 2 GPUs** — dev-box rule break.
3. **Demos not declared on the canvas.**
Plus the **queued demand**, so you can prioritise kills that actually unblock waiting jobs.

## Steps

1. Call the MCP tool `mcp__foundry-pluto__list_jobs` with `status_filter="active"`. It's large and auto-saves to a file — note that path.
2. Run the analyzer:
   ```bash
   uv run --script ~/.claude/scripts/find_node_violation.py --jobs-file "<path from step 1>"
   ```
   Add `--names` to resolve the canvas requesters' Slack display names (extra API calls). Override a changed weekly doc with `--canvas-id <Fxxxx>`.
3. Relay the ranked candidates to the user, leading with the rejected-canvas jobs and noting which one(s) match the queued demand (1:1 "kill X → unblocks Y").

## Important

- **Do NOT stop any job.** This skill only recommends. If the user then says to kill one, that's a separate explicit action (and the safety classifier may require the user to do it themselves or grant permission for `mcp__foundry-pluto__stop_job`).
- Matching of rejected canvas rows → running jobs is **keyword-based** (tokens from the rejected row descriptions matched against job/project names), so treat category 1 as "review these," not gospel — eyeball each before recommending a kill. Jobs that also match an *approved* row's keywords are excluded.
- Categories 2 (dev > 2 GPU) and 3 (demos) are deterministic from job fields/names.
- Needs `slack.user_token` (bot token can't read the canvas).
- Pairs with `/allocation_check` (the capacity/approval table).
