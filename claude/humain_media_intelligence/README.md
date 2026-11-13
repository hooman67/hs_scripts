# Humain Media Intelligence

Durable project context for the Humain Media Intelligence ingestion and data-gap analysis.

## Current status

- Research and execution plan: complete and approved on 2026-08-25.
- Slack Canvas access: working.
- Obsidian/Confluence context: captured.
- Read-only S3/media preflight: complete; 11,350 videos reduced to 9,436 canonical unique assets after checksum-backed deduplication, and all canonical videos passed `ffprobe`.
- TAC workers completed successfully and Feature Registry contains 9,436/9,436 `mi_tac` records for version `2026-08-25-8642`.
- Control-plane blocker: Pluto still reports the completed TAC job as `Running`, leaving Airflow `stage_tac.monitor_tac` stuck. Event, frame, speech, DQ, and postprocessing have not started.
- Next action: follow the recovery decision tree in the [session handoff](runs/humain-missions-20260825/SESSION_HANDOFF.md); do not trigger postprocessing yet.

Start with [CONTEXT.md](CONTEXT.md), then [PLAN.md](PLAN.md). The exact inputs are in [INPUTS.md](INPUTS.md). For the active run, read [runs/humain-missions-20260825/SESSION_HANDOFF.md](runs/humain-missions-20260825/SESSION_HANDOFF.md).

The source Canvas snapshot is [sources/slack-canvas-media-intelligence-ingestion-guide-2026-08-24.md](sources/slack-canvas-media-intelligence-ingestion-guide-2026-08-24.md). Its screenshots are preserved under `sources/canvas-images/`.
