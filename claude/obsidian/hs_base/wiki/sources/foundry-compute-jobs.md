---
type: source
title: Foundry compute-jobs & job tooling docs
tags: [foundry, compute, source, pluto, job-agent, job-police]
created: 2026-07-05
updated: 2026-07-05
raw: "[[raw/foundry/docs/compute-jobs.md]]"
sources: ["[[raw/foundry/docs/compute-jobs.md]]", "[[raw/foundry/modeling/compute/job_agent/README.md]]", "[[raw/foundry/modeling/compute/job_agent/CLAUDE.md]]", "[[raw/foundry/modeling/compute/job_police/README.md]]", "[[raw/foundry/modeling/compute/job_police/skill.md]]"]
---

# Foundry compute-jobs & job tooling docs

Distilled summary of Foundry's compute documentation (branch `main`, commit `a2c807d4b`, ingested 2026-07-05):

- `docs/compute-jobs.md` — how Foundry uses Pluto: Foundry Initiative (GAI-415), the **shared pool** since 2026-03-27 ("Foundry Unified Compute" holds aggregate quota, per-project quota reads 0), priority tiers (P0/P1/P2/LTA), how to submit (Pluto UI / `aip` / `morictl`), utilization/HFU/cost Grafana dashboards, and allocation enforcement via GitHub issue #728 + the Jobs Agent.
- `modeling/compute/job_agent/` (README + CLAUDE) — the `foundry-pluto` MCP server + browser dashboard; install, auth, tools, AI-native `design/`↔`src/` dev model, and the Pluto SDK entity-component gotchas + preemption-policy mapping.
- `modeling/compute/job_police/` (README + skill.md) — automated allocation enforcer looping Claude Code against #728 rules, alerting/killing violators in Slack.

Full synthesis: [[wiki/concepts/foundry-compute]].

## Related
- [[wiki/concepts/foundry-compute]]
- [[wiki/entities/pluto]] · [[wiki/sources/pluto-skill]]
- [[raw/foundry/_provenance]]
