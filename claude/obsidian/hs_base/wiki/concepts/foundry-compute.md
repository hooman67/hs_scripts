---
type: concept
title: Foundry compute (job_agent + job_police)
tags: [foundry, modeling, compute, pluto, mcp, gpu, governance]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/foundry/modeling/compute/job_agent/README.md]]", "[[raw/foundry/modeling/compute/job_agent/CLAUDE.md]]", "[[raw/foundry/modeling/compute/job_police/README.md]]", "[[raw/foundry/modeling/compute/job_police/skill.md]]", "[[raw/foundry/docs/compute-jobs.md]]"]
---

# Foundry compute (job_agent + job_police)

`modeling/compute/` holds Foundry's two homegrown tools for managing its GPU jobs on [[wiki/entities/pluto|Pluto]]. Both build on the **Pluto SDK** (`colligo.pluto`, shipped from [[wiki/entities/colligo|Colligo]]) and both are driven by Claude Code / Cursor. Together they give Foundry admins **visibility** (job_agent) and **enforcement** (job_police) over the shared compute pool.

Context: all Foundry compute runs under the **Foundry Initiative (GAI-415)**. Since 2026-03-27 there is a **single shared pool** — the "Foundry Unified Compute" project holds the aggregate initiative-level quota, and per-project quotas read zero by design. Priority tiers map to Pluto's [[wiki/concepts/allocation-priority-tiers|preemption policies]]: P0 Guaranteed, P1 Reclaimable (the default), P2 Spare Capacity (quota-free), Limited-time access.

## job_agent — the Foundry Jobs MCP + dashboard

An **MCP server** ([FFP-77972](https://jira.corp.adobe.com/browse/FFP-77972)) that gives natural-language access to Foundry jobs from any directory in Claude Code or Cursor. This is exactly the **`foundry-pluto` MCP** Hooman drives via the `/pluto` skill (see [[wiki/sources/pluto-skill]]).

- **Install:** `curl -s https://dit-scale-up.s3.us-west-2.amazonaws.com/foundry-jobs/latest/install.py | bash` — anonymous S3 download, works on laptops and Pluto nodes. Registers the MCP in `~/.claude.json` and `~/.cursor/mcp.json`.
- **Auth:** say "login" → Pluto device-code flow; tokens cached at `~/.colligo/pluto_cli/msal-pluto-auth.secret`, auto-refreshed.
- **MCP tools:** `login`, `list_jobs`, `get_quota`, `stop_job`, `render_dashboard` (live browser dashboard, auto-reloads every 10s), `generate_report` (static HTML snapshot uploaded to S3 for sharing).
- **Extras:** opens pre-filtered Grafana **utilization / HFU / cost** dashboards; customizable dashboard layouts (default `v1` is read-only, so it clones a runtime copy to edit).
- **AI-native development:** `design/` is the human-reviewed source of truth (`app.md`, `runtime-context.md`, `layouts/*.md`); `src/` is agent-maintained derived code kept in sync with `design/`; `plans/` holds one plan per change. Releases via `scripts/release.py` (vendors the `adobe-aip` wheel, uploads to the public `dit-scale-up` bucket).
- **SDK gotchas** (from CLAUDE.md): Pluto uses an entity-component system — `job_type` and `preemption_policy` live on `ComponentModels.job.get(entity)` (the `JOB_COMPONENT`), not on `get_state()` (where they read 0). `PreemptionPolicy` enum → labels: `NON_PREEMPTABLE`=P0, `IN_QUOTA_PREEMPTABLE`=P1, `PREEMPTABLE`/`ELASTIC_PREEMPTABLE`=P2, `LIMITED_TIME_ACCESS`. P0/P1 are quota-charged; P2/LTA are quota-free. Instance map: `p6-b200.48xlarge`=B200, `p5en.48xlarge`=H200, `p5.48xlarge`=H100, `p4de.24xlarge`=A100, all 8 GPUs/node; `c6id.24xlarge`=CPU.

## job_police — automated allocation enforcer

An **automated GPU-allocation enforcer** that runs as a Claude Code skill in a loop. It closes the loop on the shared pool: since there are no hard per-project quotas, admins agree on weekly usage rules and job_police enforces them.

- **Rules source:** the body of **GitHub issue [Adobe-Firefly/foundry#728](https://github.com/Adobe-Firefly/foundry/issues/728)** — admins edit the issue in plain bullets ("NBCU has priority over N nodes", "project X ≤ Y GPUs", expiry dates). job_police applies **only** rules written there; it never invents rules.
- **Loop:** `run.py` (a `uv` script) runs every 15 min (configurable). Each cycle invokes Claude Code (Opus via Bedrock) with `skill.md` as the playbook: fetch #728 via `gh`, list active jobs via the `foundry-pluto` MCP, compare, act.
- **Escalation:** new violation → alert count 1; repeat → increment; at `--kill-threshold` (default 3) it calls `stop_job` to kill the job. **P2 jobs are never violations.** State (`alerts.json`, `daily_thread.json`) lives in `~/.cache/foundry_job_police_state/` and is ephemeral (lost state = fresh warnings).
- **Notification:** posts a single daily message (one thread/day) to Slack `#foundry-ersin-eng-team`, @-mentioning owners (resolved via `users.lookupByEmail`), with a `generate_report` dashboard snapshot link and the #728 rules link.
- **Run modes:** `--once --dry-run` (test — still posts to a test channel but never kills), production loop, or `--submit-to-pluto` (runs as a CPU job on Pluto under project *Foundry-Presale-And-Partnership-Support*, with secrets forwarded as env vars).

> This is the enforcement counterpart to the governance side documented in [[wiki/concepts/pluto-operations]] and the `/find_node_violation` skill; job_police is Foundry's automated, Slack-facing version.

## Related
- [[wiki/concepts/foundry-modeling]]
- [[wiki/entities/foundry]]
- [[wiki/entities/pluto]] · [[wiki/concepts/pluto-cli-sdk]] · [[wiki/concepts/allocation-priority-tiers]] · [[wiki/concepts/quota-and-utilization]] · [[wiki/concepts/pluto-operations]]
- [[wiki/concepts/colligo-pluto-sdk]]
- [[wiki/sources/pluto-skill]]
- [[wiki/sources/foundry-compute-jobs]]
