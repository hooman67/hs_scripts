# Session handoff — Humain Media Intelligence baseline

Last consolidated: 2026-08-26 05:31 UTC

## Restart directive

Read the project startup files in the order required by `AGENTS.md`, then read this file. Verify volatile Pluto, Airflow, Feature Registry, S3, schema, and index state before taking action. The evidence below is the last verified state, not a substitute for a fresh status check.

No credential values, presigned URLs, or raw worker logs are stored here. Full Klam credentials remain only at `/Users/hshariati/Downloads/creds.txt`. AWS access must use `/aws-creds` and source `~/.claude/hshariati/aws_creds.env` in the same shell command as each AWS CLI call.

## Current verdict

The canonical dataset and TAC outputs are complete, but the end-to-end MI ingestion is not complete or customer-usable.

- Preflight and canonical manifest generation: complete.
- TAC workers: complete; all four pods exited 0.
- TAC Feature Registry output: 9,436/9,436 records in immutable version `2026-08-25-8642`.
- Control plane: blocked. Pluto still reports the completed TAC parent job as `Running`, leaving Airflow `stage_tac.monitor_tac` stuck.
- TAC DQ, event, frame, speech, health/rerun tasks: not started.
- Postprocessing, Postgres materialization, OpenSearch indexing, and MI search/UI validation: not started.

Do not trigger postprocessing or claim the ingestion is complete.

## Run identifiers and links

| Item | Value |
|---|---|
| Official customer bucket | `foundry-humain-default-adobe-assets` |
| Isolated run root | `s3://foundry-humain-default-adobe-assets/media-intelligence/humain-missions-20260825/` |
| Canonical input parquet | `s3://foundry-humain-default-adobe-assets/media-intelligence/humain-missions-20260825/manifests/input.parquet` |
| Airflow service | `https://pluto-prod-vananth-mi-airflow-dev-11-0-8080.or2.colligo.dev/` |
| Airflow API base | `https://pluto-prod-vananth-mi-airflow-dev-11-0-8080.or2.colligo.dev/api/v2` |
| Ingestion DAG | `foundry_media_intelligence_pipeline` |
| Airflow run ID | `humain_missions_20260825_fr_2026-08-25-8642` |
| Feature Registry version | `2026-08-25-8642` |
| Runtime branch / commit | `vananth/ingestion-v2` / `5da65df746628eeaffcd47aeac845e7abe4188d8` |
| TAC Pluto job | `8e0c6f0d-198c-4f4b-810f-7066c3f84e54` |
| TAC Pluto dashboard | `https://ai.corp.adobe.com/jobs/8e0c6f0d-198c-4f4b-810f-7066c3f84e54` |
| TAC job name | `mi-direct-20260825150747-tac-svc-mediaint` |
| TAC allocation | 4 nodes x 8 H200 GPUs = 32 H200 GPUs, P0 |
| Airflow controller job | `a7e3551b-5f94-489b-b6d5-1a4f9361d054` |
| Airflow controller dashboard | `https://ai.corp.adobe.com/jobs/a7e3551b-5f94-489b-b6d5-1a4f9361d054` |
| Planned Postgres schema | `humain_missions_20260825` |
| Postprocess helper | `scripts/trigger_humain_postprocess.py` |

Planned isolated OpenSearch indexes:

- `mi_humain_missions_20260825_assets_index`
- `mi_humain_missions_20260825_audio_data_index`
- `mi_humain_missions_20260825_embeddings_index`
- `mi_humain_missions_20260825_entities_index`
- `mi_humain_missions_20260825_event_data_index`
- `mi_humain_missions_20260825_frame_data_index`
- `mi_humain_missions_20260825_franchises_index`
- `mi_humain_missions_20260825_speech_data_index`

These are planned names, not evidence that postprocessing created them.

## Dataset and preflight evidence

- Seven source prefixes across six missions and five themes.
- S3 inventory: 11,357 objects, including seven source CSVs and 11,350 videos.
- Exact duplicates: 1,909 checksum groups and 1,914 redundant copies excluded.
- Canonical set: 9,436 unique videos, 21.1214 hours, 274,893,017,268 bytes.
- Video codecs: 8,334 H.264 and 1,102 HEVC.
- Audio streams: 8,292 videos with none, 1,044 with one, and 100 with two.
- All 9,436 canonical videos passed `ffprobe` after local Homebrew ffmpeg was upgraded from 7.1_4 to 9.0.1_1.
- There are 1,303 dimension mismatches and 1,164 orientation swaps, but no decode failures.
- The older `9c3e6442-6e54-4d82-9969-7c0ddbd87d9c` delivery dated 2026-07-27 is fully content-identical to its 2026-08-17 delivery: all 1,870 objects have the same CRC64; 1,270 were renamed from `.mov` to `.mp4`. The newer delivery is canonical and the older delivery remains represented in provenance.

Local and S3 run artifacts include:

- `manifests/input.parquet` — 9,436 canonical rows.
- `manifests/provenance.parquet` — 11,350 source-video rows.
- `manifests/duplicates.parquet`.
- `reports/media_probe.parquet`.
- `reports/dimension_mismatches.parquet`.
- `reports/PREFLIGHT_REPORT.md`, `reports/DATASET_CARD.md`, `reports/GAP_ANALYSIS.md`, and `reports/preflight_summary.json`.
- `run-config/ingestion_conf.json`.

The raw downloaded source CSVs were deleted and were never uploaded because they contained presigned URLs. Source prefixes were not modified. Only the official customer bucket and isolated run root were used.

The last S3 inventory check showed no preview, stage-output, or postprocessing artifacts yet. Recheck this after restart because it is volatile.

## Last verified Airflow and Pluto state

At the last check, the Airflow DAG run remained `running`; its last scheduling decision was `2026-08-26T05:30:53.005593Z`.

| Task | State |
|---|---|
| `make_input_parquet` | success |
| `stage_tac.register_fr_tac` | success |
| `stage_tac.submit_tac` | success |
| `stage_tac.monitor_tac` | running since `2026-08-25T22:07:58.962623Z` |
| `stage_tac.dq_check_tac` | not started |
| Event, frame, speech, health, and rerun tasks | not started |

Pluto still reported TAC job `8e0c6f0d-198c-4f4b-810f-7066c3f84e54` as `Running`, approximately 7 hours 24 minutes old at the last check, even though the worker evidence proves all four pods exited successfully.

## Worker-log evidence from `run-1.zip`

Hooman supplied `/Users/hshariati/Downloads/run-1.zip`, an approximately 11 MiB compressed archive containing logs for all four TAC pods. The archive was inspected read-only. The temporary extraction directory was removed; the original ZIP is untouched. Raw logs were deliberately not copied into this project because of their size and potential sensitivity.

All four `main_scripts/1/exit_code` files contain `0`. Every pod logs:

- prediction completion;
- OpenTelemetry shutdown;
- NCCL `Destroy COMPLETE`; and
- VLLM shutdown signal.

There are no tracebacks or fatal worker errors. Seven prediction processes started and completed per pod, consistent with the per-node process layout. This corrects the earlier tentative diagnosis that a worker might still be hung: the workers are finished; parent-job/control-plane finalization is stuck.

## Multi-pod duplication concern

The four nodes appear to have processed heavily overlapping data instead of partitioning the dataset:

| Pod | Unique assets queued |
|---|---:|
| 0 | 8,977 |
| 1 | 8,917 |
| 2 | 8,982 |
| 3 | 9,402 |
| Union | 9,436 |
| Present in all four pods | 8,698 |

Across pods there were 36,278 processing attempts, 9,436 successful Feature Registry writes, and 26,842 duplicate writes rejected as `Overwrite prevented`. Average computation was approximately 3.84 attempts per canonical asset. The many log lines marked `ERROR` are these immutable-record collision rejections, not worker crashes.

The result preserved exactly one `mi_tac` record per asset, but the first successful writer won and most computation was wasted. Confirm whether this is an expected behavior or a multi-pod sharding defect before allowing the same pattern to consume event/frame/speech compute.

One real partial output requires DQ attention:

`s3://foundry-humain-default-adobe-assets/ingest/misions/3d6deadb-f65a-4489-bb16-9192e44cb8e5/17-08-2026/videos/2153062060.mp4`

All four pods reported `[tac:embed] 1/2 shots embedded (1 failed)` for this asset. Do not silently waive it; let TAC DQ inspect it and retry the exact ingestion if necessary.

## Recovery decision tree

1. Recheck the Airflow run, task instances, Pluto job, and Feature Registry count. Do not trigger postprocessing.
2. The TAC job is a zombie holding 32 H200 GPUs. Stopping it is a mutating action: do it only with Hooman's explicit authorization in the restarted session, after confirming the workers are still complete and the job is still `Running`.
3. Watch whether `stage_tac.monitor_tac` settles to failed after the Pluto job stops. Do not clear or retry `stage_tac.submit_tac`; that could relaunch already-completed TAC work.
4. Before manually advancing the monitor, coordinate with Varun about the multi-pod duplication so the remaining stages do not repeat roughly 3.84x computation.
5. If Varun confirms the overlap is expected/acceptable, stop the zombie if necessary, let the monitor settle, and—if it fails only because the finished parent job was stopped—manually mark only `stage_tac.monitor_tac` successful. Then let `stage_tac.dq_check_tac` run naturally.
6. If TAC DQ flags `2153062060.mp4`, retry only the missing/failed output using the same manifest and Feature Registry version. This is the exact same ingestion, so version reuse is required and allowed.
7. If the overlap is a sharding bug, correct the configuration/branch or use an approved single-pod override before advancing event/frame/speech. Do not silently move to a new Feature Registry version for this same dataset retry.
8. Allow all ingestion stages, stage DQs, health checks, and approved reruns to complete before running `scripts/trigger_humain_postprocess.py`. The helper refuses to run before ingestion success and obtains reference runtime secrets in memory without persisting them.
9. Validate Postgres, all eight OpenSearch indexes, previews, counts, and representative queries before calling MI usable.

Suggested message to Varun:

> Humain run `humain_missions_20260825_fr_2026-08-25-8642`: all four TAC pods exited 0 and FR contains 9,436/9,436 records, but Pluto job `8e0c6f0d-198c-4f4b-810f-7066c3f84e54` remains Running and Airflow `monitor_tac` is stuck. The four pods collectively made 26,842 rejected duplicate writes; 8,698 assets were processed by all four pods. One asset `2153062060.mp4` had 1/2 shot embeddings fail on all pods. Is this expected multi-pod behavior? Can we stop the zombie and mark `monitor_tac` successful, and how should we prevent duplication in remaining stages?

## Verification and usage gates

Usable now:

- The canonical and provenance manifests for deterministic inventory and analysis.
- The preflight report, dataset card, and initial gap-analysis artifacts.
- TAC Feature Registry feature `mi_tac` at version `2026-08-25-8642`, programmatically, subject to the partial-shot caveat above.

Not usable yet:

- MI search or agent results.
- Franchises, entities, and cross-asset grouping.
- Customer-facing MI UI conclusions.
- Final cultural/collection-gap conclusions derived from MI outputs.

End-to-end acceptance requires all of the following:

- every ingestion task and all four stage DQ gates succeed;
- Feature Registry counts reconcile against 9,436 canonical assets and the problem asset is resolved or explicitly reported;
- postprocessing succeeds using the exact same input parquet and Feature Registry version;
- the fresh Postgres schema contains 9,436 assets with reconciled related-table counts;
- all eight isolated OpenSearch indexes exist and their document counts reconcile;
- previews resolve and representative search/agent queries work across landmarks/places, food, lifestyles, events, and clothing/fashion;
- empty search results are checked against ingestion completeness, index behavior, provenance, and raw samples before being labeled source-data gaps.

The exact MI frontend/search URL was not verified in the final session because the Confluence reader returned HTTP 401 for an invalid cookie. This does not block control-plane recovery. If the UI link is needed, refresh Confluence authentication or ask Varun. Authoritative page:

`https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3916579437/Media+Intelligence+Documentation`

The local immutable research capture is:

`/Users/hshariati/hs_scripts/claude/obsidian/hs_base/raw/media-intelligence-operations-research-2026-08-25.md`

## Do not do these things

- Do not create another S3 bucket or write into any source prefix.
- Do not change the preserved source spelling `misions/`.
- Do not clear/retry `stage_tac.submit_tac` as the first recovery action.
- Do not trigger postprocessing before the full ingestion DAG and DQ gates succeed.
- Do not use a new Feature Registry version for a retry of this exact manifest.
- Do not reuse the planned Postgres schema or OpenSearch indexes for a different dataset or collection round.
- Do not commit raw ZIP/log contents, credentials, Vault values, or presigned URLs.
- Do not infer a source-data gap from an empty MI result without checking ingestion and retrieval completeness.
