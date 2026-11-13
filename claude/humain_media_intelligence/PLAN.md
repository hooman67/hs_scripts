# Approved execution plan

Approved by Hooman on 2026-08-25. The prior session stopped before execution so the work can continue from this dedicated project.

## 1. Read-only preflight

1. Run `/aws-creds`.
2. Inventory all seven prefixes from `INPUTS.md` without modifying them.
3. Record object count, bytes, extensions, media modality, resolution/duration where available, empty/corrupt/unsupported files, and prefix-level differences.
4. Confirm the exact live MI branch supports the observed modality mix. The operational guide is video-centric even though the product RPD describes video and image support.
5. Compare the two dated deliveries for mission `9c3e6442-...` and scan for duplicates across all prefixes.

Stop before compute if access is missing, media is unsupported, paths are empty, or the source differs materially from the supplied table.

## 2. Canonical manifests and run root

Create a canonical unique-asset input parquet with `s3_url` and `title_name`, plus a full companion provenance parquet.

Use only the official customer bucket `foundry-humain-default-adobe-assets`; do not create another bucket. Keep all writes below a new isolated prefix. The descriptive `media-intelligence/` namespace below is preferred over a generic folder name such as `video_data_ingested_in_media_intelligence`, and remains subject to a read-only collision check before creation.

Proposed run root, subject to an existence check:

```text
s3://foundry-humain-default-adobe-assets/media-intelligence/humain-missions-20260825/
  manifests/input.parquet
  manifests/provenance.parquet
  manifests/duplicates.parquet
  manifests/retry.parquet
  previews/
  stages/
  reports/
```

Allocated unique names (collision checks completed before creation):

```text
Feature Registry: 2026-08-25-8642
Postgres schema:  humain_missions_20260825
```

The isolated run root is `s3://foundry-humain-default-adobe-assets/media-intelligence/humain-missions-20260825/`. The ingestion DAG run is `humain_missions_20260825_fr_2026-08-25-8642`.

Do not create a production canary by expanding a manifest under the same Feature Registry version. If a separate MI canary is genuinely necessary, it requires its own permanent Feature Registry version and scratch schema; prefer strong local/media preflight plus the production DAG's data-quality gates to avoid unnecessary immutable state.

## 3. Verify Airflow runtime

1. Check whether Varun's MI Pluto job `a7e3551b-5f94-489b-b6d5-1a4f9361d054` is running.
2. Prefer its VPN-only live Airflow URL when available.
3. Otherwise clone the job and run `/home/colligo/foundry-mi-data-ingestion/bootup.sh`.
4. Verify repository remote, `vananth/ingestion-v2`, current commit, dependency/runtime health, DAG version, and parameter descriptions.
5. Use a fresh A100 40 GB interactive session only if the existing/cloneable job is unusable.

## 4. Trigger ingestion

Trigger `foundry_media_intelligence_pipeline` with:

- canonical input parquet path
- dedicated preview directory
- fresh Feature Registry version
- approved domain information
- appropriate event granularities
- data-quality gates enabled

Domain information should use authoritative mission/taxonomy definitions and validated exemplars. Do not invent cultural rules. Keep target coverage goals out of descriptive domain context when they might bias the observed-corpus analysis.

Monitor every task group through `monitor_event` and the corresponding data-quality check. Save DAG run ID, configuration, commit, logs, timestamps, per-stage counts, and failures. Retry only missing/failed assets using the same manifest/run identity and Feature Registry version.

## 5. Trigger postprocessing

After all ingestion stages and DQ checks pass, trigger `foundry_media_intelligence_postprocessing` with:

- the exact same input parquet and Feature Registry version
- fresh Postgres schema
- Vault-provided Postgres connection
- franchise instructions that preserve theme/mission distinctions and keep negative controls separate
- entity-grouping instructions appropriate to this non-fiction cultural dataset
- Vault-provided OpenSearch host
- isolated OpenSearch namespace/index

Do not reuse an existing schema or index.

## 6. Validate end to end

Reconcile:

```text
source objects
→ canonical unique manifest
→ each MI stage
→ Feature Registry outputs
→ Postgres assets/analyses
→ OpenSearch documents/embeddings
```

Validate representative previews and outputs for every theme. Test transcription, scene/event and frame descriptions, OCR, objects, symbols, embeddings, timestamped retrieval, and known sparse/negative queries. Produce success, failure, and retry reports.

Do not declare success while silent drops or count mismatches remain unexplained.

## 7. Gap-analysis workflow

1. Build a deterministic dataset card by theme, mission, unique asset count, hours, modality, quality, and failure status.
2. Define a target coverage matrix from the Humain taxonomy, mission briefs, Saudi-tourism use cases, and business priorities.
3. Extract MI-observed coverage across cultural, semantic, geographic, activity, clothing, food, event, people, audio/language, and production dimensions.
4. Measure redundancy using exact duplicates, near-duplicate visual clusters, and dense semantic clusters.
5. Run a saved natural-language/visual query suite. Require asset IDs/timestamps and cross-check important results with deterministic data.
6. Classify every apparent deficit as source-data gap, ingestion gap, labeling gap, or retrieval gap.
7. Rank verified collection gaps by business weight, deficit size, diversity/redundancy, evidence confidence, and collectability.
8. Produce new mission briefs with target quantities, diversity constraints, exclusions, provenance requirements, and MI acceptance queries.

## 8. Future rounds

Each new collection round gets a new Feature Registry version, Postgres schema, and index. Compare it to the preserved baseline. If a combined all-rounds view is needed, create a new consolidated ingestion under another fresh isolated namespace.

## Completion artifacts

- canonical input and provenance manifests
- duplicate decision report
- Airflow run configuration and IDs
- stage/DQ/DB/index reconciliation report
- retry manifest and final completion status
- MI dataset card
- target-versus-observed gap matrix
- prioritized next-round collection briefs
- updated Obsidian knowledge pages and run-specific lessons
