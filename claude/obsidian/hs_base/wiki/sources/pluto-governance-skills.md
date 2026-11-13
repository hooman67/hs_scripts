---
type: source
title: "Pluto governance skills (allocation_check / find_node_violation / update-node-utilization-canvas)"
raw: "[[raw/pluto-governance-skills]]"
created: 2026-07-04
updated: 2026-07-04
ingested: 2026-07-04
tags: [adobe-infra, compute, pluto, governance, tooling]
---

# Pluto governance skills

Three of Hooman's Claude Code skills that run on [[wiki/entities/pluto|Pluto]] quota/job data plus
Slack canvases to govern Foundry compute allocation. Source: [[raw/pluto-governance-skills]].
Synthesis: [[wiki/concepts/pluto-operations]].

All three read the [[wiki/sources/pluto-skill|foundry-pluto MCP]] (`get_quota`, `list_jobs`) — only
the agent can call it, so the agent saves the JSON blobs to files and the scripts consume them — and
read Slack canvases via `slack.user_token` (the bot token gets `not_visible` on canvases).

## The three skills

- **`allocation_check`** (`~/.claude/scripts/allocation_check.py`) — **mutating (DMs Slack).**
  Builds the node-allocation table by GPU type: **Available (fleet, from `get_quota`) · Approved ✅
  · Not approved ❌ (both from the weekly canvas) · Running now (from active `list_jobs`)**, with a
  free/overcommitted note, and DMs it to Hooman. `--dry-run` prints only. 8 GPUs/node;
  `p5en.48xlarge`→H200, `p6-b200.48xlarge`→B200.

- **`find_node_violation`** (`~/.claude/scripts/find_node_violation.py`) — **READ ONLY, advisory.**
  Ranks kill candidates: (1) running work the canvas rejected (keyword-matched on job name —
  "review these," excludes jobs also matching an approved row), (2) dev boxes > 2 GPU
  (deterministic), (3) demos not on the canvas (deterministic); plus queued demand a kill would
  unblock. **Never stops a job** — `stop_job` is a separate explicit action.

- **`update-node-utilization-canvas`** (agent-driven, no single script) — **mutating (edits the
  shared canvas).** Writes executive-level daily compute summaries for TCCC/THD/Humain into the
  Foundry Node Utilization canvas, merging into existing date sections without touching the other
  squad's content.

## Canvases

- Weekly Thu→Thu node request and allocation — `F0BCU4W3KU6` (approval table; used by the first two).
- Foundry Node Utilization — `F0AQ1PFGE5U` (daily-summary log; shared with another squad).

## Related
- [[wiki/concepts/pluto-operations]]
- [[wiki/entities/pluto]]
- [[wiki/concepts/quota-and-utilization]]
- [[wiki/concepts/allocation-priority-tiers]]
- [[wiki/sources/pluto-skill]]
