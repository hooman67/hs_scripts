Compute the Foundry node-allocation table (canvas approved/not-approved vs. Pluto capacity & running) and DM it to Hooman on Slack.

Usage: /allocation_check [--dry-run]

Produces one table, nodes by GPU type (H200, B200, Total):
**Available (fleet) · Approved ✅ (canvas) · Not approved ❌ (canvas) · Running now (Pluto)**

## Why the agent has to help

The capacity + running numbers come from the **foundry-pluto MCP** (only the agent can call it). The canvas parse, math, and Slack DM are all done by `~/.claude/scripts/allocation_check.py`. So the flow is: agent fetches the two Pluto blobs → saves to files → runs the script.

## Steps

1. **Quota** — call the MCP tool `mcp__foundry-pluto__get_quota` (no args). Write its JSON result to a file, e.g. `/tmp/alloc_quota.json`. (The result is `{"result": "<json string>"}` — save it as-is; the script unwraps it.)

2. **Jobs** — call `mcp__foundry-pluto__list_jobs` with `status_filter="active"`. This output is large and the MCP **auto-saves it to a file** and returns that path in the message — use that path directly as `--jobs-file` (no need to re-save). If it ever returns inline, save it to `/tmp/alloc_jobs.json`.

3. **Run the script:**
   ```bash
   uv run --script ~/.claude/scripts/allocation_check.py \
     --quota-file /tmp/alloc_quota.json \
     --jobs-file  "<path from step 2>"
   ```
   It parses the canvas (via `slack.user_token`), computes the table, prints it, and DMs Hooman. Add `--dry-run` to print without sending.

4. Relay the printed table back to the user and confirm the DM was sent.

## Notes

- **Canvas:** default file `F0BCU4W3KU6` ("Weekly Thu→Thu node request and allocation"). Approved = `:greencheck:`/✅ in the Status column; red/other/blank = not approved. Strikethrough numbers are resolved to the current value; `B200` in the node cell → counted as B200, else H200. Override a changed weekly doc with `--canvas-id <Fxxxx>`.
- **Capacity** = total fleet from the central pool (`total_xpus`/8): `p5en.48xlarge`→H200, `p6-b200.48xlarge`→B200.
- **Running** = Running jobs' `num_nodes × gpus_per_node ÷ 8`, by `gpu_type`.
- Caveat to mention: H200 running can exceed the quota's stated fleet (the quota figure is overcommitted/stale) — so a "0 free" / "overcommitted" note means *no headroom*, not an exact number.
- Requires `slack.user_token` in `credentials.yaml` (the bot token can't read the canvas — it returns `not_visible`).
