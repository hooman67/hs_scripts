---
type: source
title: Media Intelligence operations research
tags: [foundry, media-intelligence, ingestion, search, humain, source]
created: 2026-08-25
updated: 2026-08-25
raw: "[[raw/media-intelligence-operations-research-2026-08-25.md]]"
sources: ["[[raw/media-intelligence-operations-research-2026-08-25.md]]"]
---

# Media Intelligence operations research

Distilled operational source for Media Intelligence ingestion, postprocessing, validation, search, and Humain collection-gap analysis.

## Key claims

- [[wiki/entities/media-intelligence|Media Intelligence]] is an offline, memoryless-per-asset understanding pipeline capped by cross-asset postprocessing and an agent/search layer.
- [[wiki/concepts/media-intelligence-ingestion|Ingestion]] is orchestrated through Airflow; input is a parquet with `s3_url` and optional `title_name`.
- Feature Registry versions are immutable isolation boundaries: reuse is only valid for retries of the exact same ingestion.
- Postprocessing must use the same manifest and Feature Registry version, plus a fresh Postgres schema and isolated OpenSearch namespace.
- A complete run reconciles source → manifest → stage → Feature Registry → Postgres → OpenSearch counts and failures.
- [[wiki/concepts/media-intelligence-gap-analysis|Gap analysis]] combines deterministic completeness, semantic outputs, embeddings/search, and an explicit target taxonomy.
- An empty search result is ambiguous until source absence, ingestion failure, labeling failure, and retrieval failure are separated.

## Humain-specific findings

The Humain target is Saudi-tourism cultural relevance/alignment across places/landmarks, food, lifestyle, events, and clothing/fashion. Important coverage axes include Saudi versus non-Saudi Arab negatives, indoor/outdoor balance, traditional/modern and formal/casual contexts, food presentation/use, national/religious events, cultural symbols, language/signage, and business-use relevance.

The initial Humain baseline should be a single deduplicated ingestion with a separate provenance manifest. Future rounds require fresh Feature Registry/database/index isolation and should be measured against the preserved baseline.

## Version caution

The August Canvas's live-DAG screenshot and the June system documentation use partially different stage names. Treat the current Airflow DAG and parameter descriptions as canonical runtime truth and preserve the actual commit/DAG version in every run report.

## Related

- [[wiki/entities/media-intelligence]]
- [[wiki/concepts/media-intelligence-ingestion]]
- [[wiki/concepts/media-intelligence-gap-analysis]]
- [[wiki/entities/foundry]] · [[wiki/entities/pluto]]
- [[wiki/concepts/foundry-aws-access]]
