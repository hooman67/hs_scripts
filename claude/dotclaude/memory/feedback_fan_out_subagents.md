---
name: feedback_fan_out_subagents
description: Parallelize with subagents and keep the main session free — but respect sequential dependencies
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 988e6174-d494-4ea5-a025-8678b58141b2
  modified: 2026-08-23T00:35:24.634Z
---

When work can be parallelized, **fan out subagents (Agent tool) to run it concurrently and keep the
main session empty** for coordination/integration. Hooman asked for this explicitly on the THD video
rewriter ([[project_thd_video_rewriter]]) and wants it applied whenever possible.

**Why:** faster throughput; the main session stays responsive instead of blocking on long generations.

**How to apply:**
- Split independent work (e.g. separate generation batches) into one subagent each; launch them in a
  single message so they run in parallel/background.
- **Respect sequential dependencies:** if step C needs the result or learning of A/B, run A/B first
  (in parallel), then design/run C from their output. Don't parallelize across a real dependency.
- Avoid races on shared resources: have subagents write to their OWN output dirs and report back;
  keep edits to shared files (e.g. the gallery `manifest.json`) in ONE place and integrate centrally.
