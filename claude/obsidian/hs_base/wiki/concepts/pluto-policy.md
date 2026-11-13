---
type: concept
title: Pluto policies
tags: [adobe-infra, compute, pluto, policy, governance, quota]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/pluto-docs-extras]]"]
---

# Pluto policies

[[wiki/entities/pluto|Pluto]] enforces platform-wide policies on GPU utilization, quota overuse, and job archival; initiatives and projects can layer **stricter** (never more permissive) policies on top.

## Platform (global) policies

### 1. Low GPU utilization

Utilization is averaged hourly across the **last six hours** per job. Thresholds:

| Job kind | Threshold |
|---|---|
| Training jobs (all sizes) | below **75%** |
| Interactive large/medium (16+ GPUs) | below **75%** |
| Interactive small (<16 GPUs) | below **50%** |

Enforcement: two Slack DMs to the job owner every six hours while below threshold; a final escalation to the initiative/project Slack channel if configured; a "Recovered" notification (and cleared prior violations) once utilization improves.

### 2. Quota overuse

Monitors project-level guaranteed GPU/CPU usage vs. allocated [[wiki/concepts/quota-and-utilization|quota]] by instance type. Sequence: up to three Slack warnings to project + initiative admins (1 hour apart) → configurable grace period (default 1 hour) → automatic preemption of the **minimum** jobs needed to restore compliance → recovery notification.

Preemption order (see [[wiki/concepts/allocation-priority-tiers|priority tiers]]): Quota Reclaimable (P1) first, then Quota Guaranteed (P0) only if P1 is insufficient; within each group — full-node jobs, then newest, then smallest. Opportunistic projects: only Quota Reclaimable jobs are eligible.

### 3. Inactive job archival

Jobs older than **two weeks** in status Succeeded, Stopped, or Failed are deleted. Archival is done manually by the platform team, periodically. (Matches the archival note in [[wiki/concepts/pluto-job-lifecycle]].)

## Project & initiative policies

Initiative admins can override global defaults but only **stricter**: "You can set initiative and project policies that are stricter than the platform policy (but not more permissive)."

Configurable parameters: **Job Type** (training vs interactive), **Job Size** (Small/Medium/Large by GPU/node count), **GPU Utilization Threshold** (stricter must exceed platform-level), **Monitoring Window** (averaging hours), and **Grace Period** (time between final notification and enforcement). Configured through the Initiatives/Projects interfaces from policy templates. Violations trigger Slack notifications to job owners, with optional dedicated escalation channels.

## Related
- [[wiki/entities/pluto]]
- [[wiki/concepts/quota-and-utilization]]
- [[wiki/concepts/allocation-priority-tiers]]
- [[wiki/concepts/pluto-operations]]
- [[wiki/concepts/pluto-job-lifecycle]]
- [[wiki/sources/pluto-docs-extras]]
