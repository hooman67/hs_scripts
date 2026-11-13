# Humain Media Intelligence — durable context

Last consolidated: 2026-08-25

## Objective

Ingest the supplied Humain mission assets into Foundry Media Intelligence (MI), validate the ingestion end to end, and use MI's deterministic metadata, semantic analysis, embeddings, search, and agent layer to identify collection gaps that should inform new Saudi-tourism data missions.

There are seven S3 prefixes, six mission UUIDs, five top-level themes, and one explicitly identified duplicate-run candidate. The exact table is in `INPUTS.md`.

## Work already completed

The planning session successfully:

- Loaded the Slack Canvas `F0BNRGLJ1HB`, titled **Media Intelligence Ingestion Guide**, via Slack `files.info` and its private download URL using the machine-local `slack.user_token`.
- Read all Canvas text and downloaded its five supporting screenshots.
- Searched the Obsidian vault with both ripgrep and Obsidian-native search.
- Read the existing shallow MI wiki entity and Humain working notes.
- Read the authoritative Media Intelligence Confluence documentation, MVP/MVP1.1 RPDs, Humain project page, and Cultural Taxonomy page.
- Reconstructed and received user approval for the execution plan in `PLAN.md`.

Execution began on 2026-08-25. The completed preflight found 11,350 source videos, 1,914 redundant copies in 1,909 exact-checksum groups, and 9,436 canonical unique videos totaling 21.12 hours. All canonical videos passed `ffprobe`. The production Airflow ingestion is `humain_missions_20260825_fr_2026-08-25-8642` against immutable Feature Registry version `2026-08-25-8642`.

The four TAC worker pods all exited with code 0 and Feature Registry contains 9,436/9,436 TAC records. However, Pluto still reports their parent job as `Running`, so Airflow remains stuck in `stage_tac.monitor_tac`. No TAC DQ, event, frame, speech, overall health, rerun, or postprocessing work has started. The worker logs also reveal substantial multi-pod duplicate computation and one asset with a partial shot-embedding result. The exact evidence, identifiers, recovery sequence, and acceptance gates are preserved in `runs/humain-missions-20260825/SESSION_HANDOFF.md`. Treat that file as the operational handoff and verify volatile status before acting.

## Authoritative sources

1. Slack Canvas — current operational guide, marked updated August 24:
   https://adobe.enterprise.slack.com/docs/T024FSURM/F0BNRGLJ1HB
2. Media Intelligence Documentation — Varun Ananth, modified 2026-06-16:
   https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3916579437/Media+Intelligence+Documentation
3. Foundry Media Intelligence MVP1.1 RPD — modified 2026-08-17:
   https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3973012644/Foundry+Media+Intelligence+MVP1.1+RPD
4. Foundry Media Intelligence MVP RPD:
   https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3913491086/Foundry+Media+Intelligence+MVP+RPD
5. Humain project page:
   https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3684386241/Project+Page+HUMAIN
6. Cultural Taxonomy:
   https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3687812013/Cultural+Taxonomy
7. Obsidian source notes:
   `/Users/hshariati/hs_scripts/claude/obsidian/hs_base/raw/docs/todo_notes.md`
8. Existing MI wiki node, which was shallow before this handoff:
   `/Users/hshariati/hs_scripts/claude/obsidian/hs_base/wiki/entities/media-intelligence.md`

## What Media Intelligence is

MI is an offline multimedia-understanding and retrieval system. Its two intended roles are:

1. An automatic first pass over new Foundry customer media libraries so engineers can explore large S3 data dumps.
2. A customer-facing intelligence layer for natural-language discovery, analytics, and recommendations over customer-owned media.

The ingestion pipeline is **memoryless per asset**: each video/media object is processed independently. Cross-asset understanding appears later through postprocessing/agglomeration and the agent/search layer.

The main analysis signals documented by MI are:

- Timestamped transcription and shot boundaries from TAC.
- Story/event/scene-level descriptions and narrative structure.
- Speech segments, speakers, emotion/context, and transcriptions.
- Fine-grained shot or event descriptions.
- Original-resolution center-frame analysis including OCR, faces, objects, brands, NSFW signal, and best-frame timestamps.
- AdobeOne embeddings used for quick/semantic search.
- Postprocessing that groups assets into franchises and subjects/characters into entities.
- Natural-language search and recommendations returning timestamped media with rationale.

The exact live DAG may have evolved beyond the June documentation. The August Canvas screenshot shows task groups including `stage_tac`, `stage_event`, `stage_speech`, and `stage_frame`, whereas older documentation also describes story and shot stages. Inspect the live Airflow DAG and its parameter descriptions before relying on hard-coded stage names.

## Current ingestion mechanism

The Canvas names this orchestration repository and branch:

- Repository: `https://github.com/Adobe-Firefly/foundry-mi-data-ingestion`
- Branch: `vananth/ingestion-v2`
- Existing Pluto path when using Varun's job: `/home/colligo/foundry-mi-data-ingestion`
- Boot command: `bash bootup.sh`

Airflow access preference:

1. If Varun's MI Pluto job is running, use its live link on VPN/Adobe Wi-Fi.
2. If it is not running, clone the job, SSH to it, navigate to the repository, and run `bootup.sh`.
3. Create a fresh interactive Pluto node only as a fallback; use at least an NVIDIA A100 40 GB so it lands on `colligo-laser02-prod-uw2`.

The laptop GitHub credential was logged in as `hshariati_adobe` but could not resolve the orchestration repository. This is not yet a blocker because the Canvas directs execution from the existing Pluto checkout. Before triggering anything, verify the repo remote, branch, commit, and clean/runtime state on the node. Stop before writes if it is missing or inconsistent.

## Airflow ingestion parameters that matter

The current Canvas says to trigger `foundry_media_intelligence_pipeline` and carefully read every parameter description. Critical fields are:

- **Input parquet path** — must contain `s3_url`; may contain `title_name` (pretty name). The DAG can also generate a parquet from one S3 folder, but this project has seven prefixes, so a canonical combined parquet is safer.
- **Preview upload S3 directory** — destination for scaled videos/previews generated by Genie and required by the UI. Preserve this path in the run record.
- **Feature Registry version** — immutable and collision-sensitive. A new ingestion must use a new version. Reusing the same version is allowed only to retry missing/failed assets from the exact same ingestion.
- **Domain info** — either plain text or an S3 hierarchy. In S3 mode, every `.txt` file is paired with images in a same-named sibling subfolder; scanning is recursive and builds nested text/image context.
- **Additional granularities** — clip durations in seconds for event analysis; multiple levels are allowed.
- **Data quality gates** — must pass before postprocessing.

The Canvas recommends monitoring progress through each stage's `monitor_event` subtask.

## Postprocessing parameters that matter

Trigger `foundry_media_intelligence_postprocessing` only after ingestion completes.

- **Input parquet path and Feature Registry version** must exactly match the ingestion run.
- **Postgres connection string** comes from Vault path `dme_colligo/services/foundry/media_intelligence/dev_foundry_postgres`.
- **Postgres schema** is the account/isolation boundary. Never reuse an existing schema for a different ingestion.
- **Franchise grouping instructions** guide how assets are grouped across the library.
- **Entity grouping instructions** guide subject/character identity resolution across assets.
- **OpenSearch host** comes from Vault path `dme_colligo/services/foundry/media_intelligence/dev_foundry_opensearch`.

When this DAG completes and its outputs validate, the data is considered fully ingested.

## Dataset organization decision

Use **one combined baseline ingestion** after object-level deduplication, not seven independent MI tenants. This allows cross-theme analysis in one schema/index while retaining theme and source delivery in a companion provenance manifest.

MI's documented input schema has only `s3_url` and optional `title_name`, so provenance must not depend on MI alone. The companion manifest should include:

- `s3_url`
- `title_name`
- canonical theme
- mission UUID
- delivery date
- original prefix and object key
- object size, ETag/checksum, media metadata
- duplicate group/canonical-object decision
- ingestion and retry status

Encode the theme/mission into `title_name` for usability, but keep the companion manifest as the source of truth.

The two paths for mission `9c3e6442-6e54-4d82-9969-7c0ddbd87d9c` must be compared by key, size, checksum/ETag, and content hash where necessary. Retain objects unique to either delivery and ingest only one canonical copy of identical assets. Also check for cross-theme duplicates.

## Isolation and retry invariants

- The only approved bucket for generated artifacts is the official Humain customer bucket, `foundry-humain-default-adobe-assets`; do not create a separate bucket.
- Source prefixes are immutable/read-only.
- Use a new run root under the Humain customer bucket for manifests, previews, stage outputs, and reports.
- Use one fresh Feature Registry version for the combined production baseline.
- A retry uses the exact same manifest/run identity and Feature Registry version and fills only missing/failed assets.
- A changed manifest, additional collection round, or different dataset is a new ingestion and needs a new Feature Registry version.
- Use a fresh Postgres schema and isolated OpenSearch namespace/index for every new ingestion.
- If a later collection round must be analyzed together with this baseline, create a new consolidated ingestion under another fresh Feature Registry/schema rather than silently extending the baseline version.

## Humain-specific analysis goals

The Humain project objective is a historically and culturally aligned Saudi tourism model. The established pillars are landmarks/places, foods, lifestyles, and events; the supplied data also separates clothing/fashion as an explicit theme.

Existing working questions and known risks include:

- Saudi-positive data versus Arab-but-non-Saudi negative controls.
- Too much outdoor Saudi content and insufficient coverage of other contexts.
- Traditional versus modern, formal versus casual clothing and context-dependent appropriateness.
- Food still life versus preparation, dining, utensils, and drinks/non-alcoholic ambiguity.
- National, religious, and seasonal events.
- Religious/cultural symbols, Saudi flags, and false positives such as Bindi-like symbols.
- Tourism relevance, cultural relevance, cultural alignment, technical quality, and business value.
- Regional, urban/rural, indoor/outdoor, modern/traditional, time-of-day, lighting, weather, activity, people/group, language/signage, and shot/composition diversity.
- Near-duplicate density and visually redundant clusters.

The Humain project page explicitly says business value remains a blocker because the who/what/where use case is insufficiently defined. MI can measure observed coverage, but a gap exists only relative to a desired distribution. The target matrix must therefore be derived from signed-off use cases, mission briefs, taxonomy, and business weights—not from corpus frequencies alone.

## Correct way to use MI for gap analysis

Use three complementary evidence layers:

1. **Deterministic completeness** — source/manifest/stage/DB/index counts, duration, resolution, failure rates, and health reports.
2. **Semantic coverage** — MI captions and structured outputs across places, events, clothing, food, activities, people, audio, language, OCR, objects, symbols, and production attributes.
3. **Retrieval/embedding behavior** — natural-language query suites, semantic/visual cluster density, near duplicates, outliers, sparse cells, and irrelevant retrieval.

An empty or weak result can mean source absence, failed ingestion, poor labeling, or poor retrieval. Always reconcile agent/search results with the provenance manifest, stage outputs, DB counts, and raw samples before declaring a collection gap.

The agent is useful for exploration but not the sole authority for totals. The MVP1.1 RPD documents answer variability and prompt sensitivity. Require the agent to return supporting asset IDs/timestamps and cross-check important counts deterministically.

The deliverable for a new collection round should state:

- priority theme/subtheme and business use case
- positive target or negative-control role
- geography/setting/context
- current unique asset count/hours and target minimum
- requested number of new unique assets/hours
- required diversity across people/activity/lighting/shot/language/etc.
- explicit exclusions and anti-duplication rules
- metadata/provenance requirements
- MI queries and quantitative checks used for acceptance

## Credential and access lessons

- Full Klam credentials are available locally at `/Users/hshariati/Downloads/creds.txt`. Access the file only if execution requires it; never print or persist its secret values.
- Slack Canvas reading works with `slack.user_token` from `~/.claude/hshariati/credentials.yaml`; the bot token is insufficient for Canvas visibility.
- Never expose token values. Canvas content can be fetched through `files.info` followed by an authenticated download of `url_private_download`/`url_private`.
- AWS access must use `/aws-creds`; credentials are short lived and written to `~/.claude/hshariati/aws_creds.env`.
- Source that env file in the same shell invocation as every AWS CLI call.
- Postgres and OpenSearch secrets stay in Vault/runtime environment and must never be copied into this project or Obsidian.
- If Artifactory or another runtime dependency needs a token/key that is not already available, ask Hooman promptly rather than spending excessive time attempting unsupported workarounds.

## Obsidian context

Before this handoff, the wiki's `media-intelligence` entity was explicitly only a shallow overview. The prior session found the relevant Humain notes and authoritative internal docs and then updated the wiki in the same session that created this project. See the Obsidian vault for the resulting entity/concepts/source page.
