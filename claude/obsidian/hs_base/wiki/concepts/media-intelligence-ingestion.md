---
type: concept
title: Media Intelligence ingestion
tags: [foundry, media-intelligence, ingestion, airflow, feature-registry, postgres, opensearch]
created: 2026-08-25
updated: 2026-08-25
sources: ["[[raw/media-intelligence-operations-research-2026-08-25.md]]"]
---

# Media Intelligence ingestion

**Media Intelligence ingestion** is the isolated Airflow workflow that converts an S3 media manifest into validated Feature Registry outputs, cross-asset database state, and a searchable OpenSearch index.

## End-to-end flow

```text
read-only S3 inventory
→ canonical/deduplicated input parquet
→ foundry_media_intelligence_pipeline
→ stage monitoring + DQ gates
→ foundry_media_intelligence_postprocessing
→ agglomeration + Postgres + OpenSearch
→ count/search validation
```

The current operational guide uses `Adobe-Firefly/foundry-mi-data-ingestion` branch `vananth/ingestion-v2`, normally from an existing or cloned [[wiki/entities/pluto|Pluto]] job. The live Airflow DAG and its parameter descriptions are canonical because stage names and options have evolved.

## Input and provenance

The input parquet requires `s3_url` and may include `title_name`. For multiple prefixes or collection rounds, build a canonical manifest rather than relying on the single-folder generator.

Keep a companion provenance manifest with theme/domain, source prefix/key, delivery date, object metadata, duplicate group, canonical-object decision, and ingestion/retry status. `title_name` is useful for humans but is not a substitute for provenance.

Deduplicate before GPU processing. Compare exact object identity first, then checksums/content hashes where keys differ or multipart ETags are ambiguous. Keep all source occurrences in provenance while ingesting one canonical copy.

## Isolation rules

- **Feature Registry:** new version for every new ingestion; same version only for exact-run retries.
- **Postgres:** fresh schema for every ingestion; the schema is the account/data boundary.
- **OpenSearch:** isolate the index/namespace with the run/schema.
- **S3:** never modify source prefixes; use a separate run root for manifests, previews, stages, retries, and reports.
- **Postprocessing:** reuse the exact ingestion manifest and Feature Registry version.

These rules prevent assets and derived state from unrelated ingestions from colliding.

## Domain context and grouping

Domain information can be plain text or a recursive S3 hierarchy of `.txt` plus same-named image folders. Use authoritative domain definitions and verified exemplars; do not invent rules or embed desired coverage targets that could bias observed-corpus analysis.

Postprocessing franchise/entity instructions define how independently processed assets are united. For non-fiction cultural data, preserve theme/mission distinctions and negative-control groups instead of forcing entertainment-style character/franchise assumptions.

## Validation and retry

Reconcile exact counts from source objects through manifest, every stage, Feature Registry, Postgres, and OpenSearch. Inspect outputs from every domain/theme and exercise known positive, negative, and sparse queries. An unexplained count difference or silent drop blocks completion.

Retry only the missing/failed records from the same manifest/run identity using the same Feature Registry version. Changing the dataset creates a new ingestion and must use fresh isolation state.

## Related

- [[wiki/entities/media-intelligence]]
- [[wiki/concepts/media-intelligence-gap-analysis]]
- [[wiki/entities/pluto]]
- [[wiki/concepts/foundry-aws-access]]
- [[wiki/sources/media-intelligence-operations-research]]
