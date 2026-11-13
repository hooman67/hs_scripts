# Pluto governance skills — allocation_check / find_node_violation / update-node-utilization-canvas (raw)

> Source: Hooman's `allocation_check` / `find_node_violation` / `update-node-utilization-canvas`
> Claude Code skills (`~/.claude/commands/`) + their backing scripts
> (`~/.claude/scripts/allocation_check.py`, `find_node_violation.py`) and the
> `foundry-pluto` MCP tools they call. Captured to raw on 2026-07-04. Immutable.

These three skills all run **on top of** Pluto quota/job data (fetched via the `foundry-pluto`
MCP — only the agent can call it) plus two shared Slack canvases. The agent fetches the Pluto
blobs and saves them to files; the Python scripts do the parse/math/Slack work. All read the
canvas via `slack.user_token` in `credentials.yaml` (the bot token gets `not_visible` /
`not_authed` on canvases).

Two governance canvases are involved (distinct):
- **Weekly Thu→Thu node request and allocation** — canvas `F0BCU4W3KU6`. A weekly request/approval
  table: requester, node count, GPU type, description, Status. Status `:greencheck:`/✅ = approved;
  red / other emoji / blank = not approved. Strikethrough node numbers are resolved to the current
  value; `B200` in the node cell → counted B200, else H200. Used by allocation_check + find_node_violation.
- **Foundry Node Utilization** — canvas `F0AQ1PFGE5U`
  (https://adobe.enterprise.slack.com/docs/T024FSURM/F0AQ1PFGE5U). A shared daily-summary log.
  Used by update-node-utilization-canvas.

---

## 1. allocation_check  (`/allocation_check [--dry-run]`)  — MUTATING (DMs Slack)

**What it does:** Computes the Foundry node-allocation table (canvas approved/not-approved vs.
Pluto capacity & currently running) and **DMs it to Hooman on Slack**.

**Output:** one table, nodes by GPU type (H200, B200, Total), columns:
**Available (fleet) · Approved ✅ (canvas) · Not approved ❌ (canvas) · Running now (Pluto)**,
plus a per-GPU-type "free / overcommitted" note.

**Data consumed:**
- `mcp__foundry-pluto__get_quota` (no args) → total fleet capacity per instance type. JSON saved
  to a file (e.g. `/tmp/alloc_quota.json`); MCP returns `{"result": "<json string>"}` and the
  script unwraps it.
- `mcp__foundry-pluto__list_jobs` with `status_filter="active"` → nodes currently running per GPU
  type. Large output auto-saved to a file by the MCP; that path is passed as `--jobs-file`.
- Canvas `F0BCU4W3KU6` parsed via `slack.user_token`.

**Computation (allocation_check.py):**
- `GPUS_PER_NODE = 8`. Instance map: `p5en.48xlarge` → H200, `p6-b200.48xlarge` → B200.
- **Capacity (fleet)** = from quota, sum of `total_xpus // 8` for entries with a mapped instance
  type and a `total_xpus` set. The unallocated fleet lives in the central "DO NOT USE" pool.
- **Approved / Not approved** = from the canvas: for each row take first integer node count (after
  removing strikethrough), classify B200 vs H200, then add to approved if Status has greencheck/✅
  else to not_approved.
- **Running** = for jobs with `status == "Running"`, sum `num_nodes × gpus_per_node`, grouped by
  `gpu_type`, then ÷ 8 (rounded) → nodes.
- **Free note:** `free = capacity − running`; if ≤ 0, prints "overcommitted → no free" (H200
  running can exceed the quota's stated fleet because the quota figure is overcommitted/stale — so
  "0 free" means *no headroom*, not an exact number).
- **DM:** posts the table via `chat.postMessage` to Hooman's DM (opens DM via `conversations.open`
  using `slack.user_id` if `dm_channel` not set). `--dry-run` prints only, no DM.

Override changed weekly doc with `--canvas-id <Fxxxx>`.

---

## 2. find_node_violation  (`/find_node_violation [--names]`)  — READ ONLY (advisory)

**What it does:** Finds running Pluto jobs that **violate** the node-allocation canvas and ranks
**kill candidates**. **READ ONLY — never stops any job.** Output is advisory for the user to act on.
If the user then decides to kill, that is a separate explicit action (may require the user to do it
themselves or grant `mcp__foundry-pluto__stop_job` permission).

**Output — three ranked categories + queued demand:**
1. **RUNNING work the canvas REJECTED** (red ❌) — the clearest violation.
2. **Dev boxes using > 2 GPUs** — dev-box rule break.
3. **Demos not declared on the canvas.**
Plus **queued demand** (GPU/nodes waiting per GPU type) so kills can be prioritised to unblock
waiting jobs (1:1 "kill X → unblocks Y"), and a headline recommendation (rejected jobs free ~N H200
nodes; kill those first).

**Data consumed:**
- `mcp__foundry-pluto__list_jobs` with `status_filter="active"` (auto-saved file → `--jobs-file`).
- Canvas `F0BCU4W3KU6` via `slack.user_token`. `--names` resolves requester Slack display names
  (extra `users.info` calls).

**Computation (find_node_violation.py):**
- Splits jobs into `Running` and `Queued`.
- Canvas rows parsed with node count, GPU type, description, requester, approved flag, is_demo flag.
- **Category 1 (rejected running):** keyword match — tokens (≥4 chars, minus a STOP list of generic
  training/infra/vendor words) from each *rejected* row's description matched against the job
  **name only** (matching project_name caused too many false positives — e.g. every
  Media-Intelligence job hit the rejected "MI Ingestion" row). A job that also matches an *approved*
  row's keywords is **excluded**. So category 1 is "review these," not gospel — eyeball each.
- **Category 2 (dev > 2 GPU):** deterministic — job name matches `dev` and `num_nodes ×
  gpus_per_node > 2`.
- **Category 3 (demos off-canvas):** deterministic — job name matches `demo` and does not match any
  declared demo row's keywords.
- **Queued demand:** sum GPU per `gpu_type` over queued jobs.

Pairs with `/allocation_check`. Override with `--canvas-id <Fxxxx>`.

---

## 3. update-node-utilization-canvas  — MUTATING (edits shared Slack canvas)

**What it does:** Updates the **Foundry Node Utilization** canvas (`F0AQ1PFGE5U`) with **daily
compute summaries** for Hooman's squad's customers — **TCCC, THD, Humain**. Agent-driven (no
single backing script); uses Slack canvas APIs + the Pluto MCP.

**Shared canvas — two squads:**
- Hooman's squad: **TCCC, THD, Humain** (projects `Foundry-TCCC`, `Foundry-THD`, `Foundry-Humain`).
- Other squad: NBCU, Lionsgate, Paramount, WDI, GW base model.
A date "needs our updates" if it doesn't exist, or exists but has only the other squad's entries.

**Workflow:**
1. Read the canvas via its private URL
   (`https://files.slack.com/files-pri/T23RE8G4F-F0AQ1PFGE5U/canvas`, `user_token`); parse `<h2>`
   date headers; check each for `[TCCC]`/`[THD]`/`[Humain]`.
2. `mcp__foundry-pluto__list_jobs` with `status_filter="all"`; filter to the three
   `Foundry-*` projects and to jobs whose `started_at` falls in the missing date range. (list_jobs
   can be 800K+ chars → saved to file, parse with Python.)
3. Research unclear job names: FFP- ticket refs → `/jira-get`; search squad Slack channel
   (`C0AKWLP0MCY`, user_token); map owners via monitor `user_profile.md`.
4. Write executive-level daily summaries per customer (no raw job IDs/UUIDs; active voice; aggregate
   short-lived failed/stopped debug runs into one "debugging" bullet; distinguish
   interactive/demo/inference from training; note GPU/node counts and milestones; "No activity" if none).
5. **Insert via `canvases.edit`** (newest-first):
   - Scenario A (date already exists, other squad posted): `insert_after` that date's `<h2>`
     section ID — append our bullets WITHIN the same date section (both squads under one header).
   - Scenario B (date absent): `insert_before` the next chronologically-later date section to
     create a new date section.
   - **NEVER** create duplicate date headers; **NEVER** delete/modify the other squad's content.
6. Print the canvas URL and the dates added.

---

## Read-only vs mutating summary

| Skill | Reads | Writes / side effect | Canvas |
|---|---|---|---|
| allocation_check | quota, active jobs, canvas | **DMs the table to Hooman** (unless `--dry-run`) | F0BCU4W3KU6 (read) |
| find_node_violation | active jobs, canvas | **none — advisory only** | F0BCU4W3KU6 (read) |
| update-node-utilization-canvas | all jobs, canvas, Jira, Slack | **edits the shared canvas** | F0AQ1PFGE5U (read + write) |

None of the three stops jobs. Only Pluto job-stopping tool is `mcp__foundry-pluto__stop_job`, which
these skills deliberately never call.
