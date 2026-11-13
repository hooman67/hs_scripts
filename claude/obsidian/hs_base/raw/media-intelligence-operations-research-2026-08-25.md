# Media Intelligence operations research capture

Provenance: captured 2026-08-25 from the current Slack Canvas, Adobe Confluence pages, and Hooman's Humain working notes. This raw note is immutable; follow the live sources for later changes.

## Sources

- Slack Canvas, “Media Intelligence Ingestion Guide” (says updated August 24): https://adobe.enterprise.slack.com/docs/T024FSURM/F0BNRGLJ1HB
- Media Intelligence Documentation (Varun Ananth, modified 2026-06-16): https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3916579437/Media+Intelligence+Documentation
- Foundry Media Intelligence MVP1.1 RPD (modified 2026-08-17): https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3973012644/Foundry+Media+Intelligence+MVP1.1+RPD
- Foundry Media Intelligence MVP RPD: https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3913491086/Foundry+Media+Intelligence+MVP+RPD
- Humain project page: https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3684386241/Project+Page+HUMAIN
- Cultural Taxonomy: https://wiki.corp.adobe.com/spaces/FOUNDRY/pages/3687812013/Cultural+Taxonomy
- Hooman's working notes: [[raw/docs/todo_notes.md]]

## System purpose and data flow

Media Intelligence has two roles: automatically analyze new Foundry customer media libraries on S3, and provide a customer-facing intelligence/search layer over those libraries. It processes media offline with scale-to-zero compute, writes structured understanding to a database, indexes embeddings for quick search, and exposes natural-language retrieval, analytics, and recommendations.

The ingestion pipeline is memoryless per asset. Cross-asset understanding is added after ingestion through postprocessing/agglomeration, which groups assets into franchises and related subjects or characters into entities, and through the search/agent layer.

Documented analysis signals include timestamped transcription and shot boundaries; story, scene, or event descriptions; speech/speaker context; detailed shot or event descriptions; frame-level OCR, faces, objects, brands, NSFW signal, and best-frame timestamps; and AdobeOne embeddings.

## Current Airflow runbook

The orchestration repository is `https://github.com/Adobe-Firefly/foundry-mi-data-ingestion`, branch `vananth/ingestion-v2`. The preferred setup is Varun's existing Pluto job/live Airflow link. If it is down, clone the job and run `bash bootup.sh` under `/home/colligo/foundry-mi-data-ingestion`. A fresh interactive Pluto node with at least an A100 40 GB is the last fallback.

The ingestion DAG is `foundry_media_intelligence_pipeline`. Its input parquet must contain `s3_url` and may contain `title_name`. Critical configuration also includes the preview-upload S3 directory, a Feature Registry version, domain information, additional event granularities, and data-quality gates.

Feature Registry versions cannot be deleted. A new ingestion must use a new version because assets from unrelated ingestions can clash. Reusing the same version is allowed only for a retry of the exact same ingestion to fill failed/missing assets.

Domain information can be a plain text string or an S3 hierarchy. In S3 mode, recursive scanning pairs each `.txt` file with images in a same-named sibling subfolder; text precedes the images as context supplied to MI stages.

The Canvas says to monitor each stage through its `monitor_event` task. Its August screenshot shows TAC, event, speech, and frame groups; older June documentation also describes story and shot stages, so the live DAG and UI parameter descriptions must be checked at runtime.

After ingestion succeeds, trigger `foundry_media_intelligence_postprocessing` with the exact same input parquet and Feature Registry version. The Postgres connection comes from Vault path `dme_colligo/services/foundry/media_intelligence/dev_foundry_postgres`; the Postgres schema is the account-isolation boundary and must be new. Agglomeration uses franchise/entity grouping instructions. The OpenSearch host comes from `dme_colligo/services/foundry/media_intelligence/dev_foundry_opensearch`. Completion of postprocessing makes the library fully ingested.

## Validation and limitations

End-to-end validation must reconcile source objects, canonical manifest, every stage, Feature Registry output, Postgres rows, and OpenSearch documents/embeddings. Silent drops and unexplained count differences are failures. The MVP target is raw-ingestion failure below 1%, but the actual run must report exact failures and retries.

The MVP1.1 RPD documents agent prompt sensitivity, answer variability, and occasional response failures. Agent answers are exploratory evidence, not authoritative counts; important answers require asset IDs/timestamps and deterministic reconciliation with manifests, health checks, database state, and raw samples.

## Humain use and gap-analysis context

Humain's objective is a historically and culturally aligned model focused first on Saudi tourism. Its pillars are landmarks/places, foods, lifestyles, and events; current collection inputs also distinguish clothing/fashion.

Existing questions include Saudi-positive versus Arab/non-Saudi negative data, outdoor overconcentration, modern/traditional and formal/casual clothing, food still life/preparation/dining/drinks, national/religious/seasonal events, religious or cultural symbols and false positives, tourism relevance, cultural relevance/alignment, technical quality, and business value.

Media Intelligence can describe observed corpus coverage through deterministic metadata, semantic annotations, embeddings, and search. A data gap still requires a desired distribution from signed-off business use cases, mission briefs, and taxonomy. The Humain project page identifies business-value definition—the who/what/where generation use case—as a blocker.

An empty MI result can mean one of four things: source data is absent; the asset failed ingestion; MI labeled it poorly; or retrieval/indexing failed. All apparent gaps must be classified before launching new collection.

New collection briefs should record the target theme/subtheme, business use case, positive or negative-control role, geography/context, current and target unique assets/hours, diversity constraints, exclusions/anti-duplication rules, provenance requirements, and MI queries/quantitative checks used for acceptance.

## Humain baseline ingestion decision

The supplied baseline has seven S3 prefixes, six mission UUIDs, five themes, and two dated deliveries for one Events mission. Build one combined canonical input parquet after object-level deduplication so themes can be analyzed together. Keep a companion provenance parquet because MI's minimal input schema does not formally preserve theme, mission, delivery date, or duplicate decisions.

The two deliveries for mission `9c3e6442-6e54-4d82-9969-7c0ddbd87d9c` are a duplicate-run candidate, not a reason to discard one whole prefix. Compare keys, size, ETag/checksum, and content hashes where necessary; keep objects unique to either delivery and ingest one canonical copy of identical media.

Every later collection round is a new ingestion with a new Feature Registry version, Postgres schema, and OpenSearch namespace. A combined all-rounds analysis requires another fresh consolidated ingestion rather than silently extending the baseline version.
