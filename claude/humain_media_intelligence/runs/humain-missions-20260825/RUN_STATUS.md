# Humain missions MI run status

Last updated: 2026-08-26 05:31 UTC

- Official run root: `s3://foundry-humain-default-adobe-assets/media-intelligence/humain-missions-20260825/`
- Canonical input: `manifests/input.parquet` (9,436 unique videos)
- Provenance input: `manifests/provenance.parquet` (11,350 source-video rows)
- Exact duplicate copies excluded: 1,914
- Canonical duration: 21.1214 hours
- Airflow DAG: `foundry_media_intelligence_pipeline`
- Airflow run: `humain_missions_20260825_fr_2026-08-25-8642`
- Feature Registry version: `2026-08-25-8642` (created by this run)
- Runtime branch/commit: `vananth/ingestion-v2` at `5da65df746628eeaffcd47aeac845e7abe4188d8`
- Current stage: all four TAC worker pods exited 0 and Feature Registry has 9,436/9,436 records, but Pluto still reports the parent job as `Running`; Airflow remains stuck in `stage_tac.monitor_tac`
- Latest observed progress: 9,436/9,436 (100%) at 2026-08-25 23:50 UTC
- TAC Pluto job: `8e0c6f0d-198c-4f4b-810f-7066c3f84e54` (4 nodes, 32 H200 GPUs)
- Worker-log evidence: all pods logged prediction completion, clean NCCL teardown, and VLLM shutdown; the blocker is control-plane finalization, not a running prediction worker
- Multi-pod concern: 36,278 processing attempts produced 9,436 successful immutable writes and 26,842 rejected duplicate writes; 8,698 assets were attempted by all four pods
- Partial output to inspect in TAC DQ: `2153062060.mp4` produced only 1/2 shot embeddings on all four pods
- Downstream state: TAC DQ, event, frame, speech, health/rerun tasks, and postprocessing have not started
- Planned fresh Postgres schema: `humain_missions_20260825`
- Postprocessing: not triggered; it must use the exact same input parquet and Feature Registry version after all ingestion DQ gates pass.

See `SESSION_HANDOFF.md` for the exact recovery sequence and full evidence. Do not clear/retry `stage_tac.submit_tac`, advance postprocessing, or assume MI search is usable yet.

No credentials or presigned source URLs are stored in this run directory.
