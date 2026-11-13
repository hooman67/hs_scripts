---
type: concept
title: Media Intelligence gap analysis
tags: [foundry, media-intelligence, data-curation, gap-analysis, humain, cultural-relevance]
created: 2026-08-25
updated: 2026-08-25
sources: ["[[raw/media-intelligence-operations-research-2026-08-25.md]]", "[[raw/docs/todo_notes.md]]"]
---

# Media Intelligence gap analysis

**Media Intelligence gap analysis** compares a validated corpus's observed semantic coverage with an explicit target taxonomy to turn evidence-backed deficits into new collection briefs.

## A gap needs both observation and intent

MI can describe what exists through metadata, captions, structured outputs, embeddings, and retrieval. It cannot decide the desired distribution by corpus frequency alone. Targets must come from signed-off user stories, business priorities, taxonomy, mission briefs, and evaluation rubrics.

This distinction matters for Humain: its project page identifies the missing who/what/where business-use definition as a blocker even though Saudi-tourism cultural themes already exist.

## Three evidence layers

1. **Deterministic completeness** — unique assets/hours, media quality, source/manifest/stage/database/index counts, and failures.
2. **Semantic coverage** — scenes/events, places, activities, clothing, foods, people/group context, speech, language, OCR, objects, symbols, and production attributes.
3. **Retrieval and embeddings** — saved query suites, visual/semantic clusters, near duplicates, outliers, sparse cells, irrelevant results, and timestamped evidence.

Agent answers should return asset IDs/timestamps and be reconciled with deterministic data. The agent is useful for exploration but MVP1.1 documents prompt sensitivity and answer variability.

## Diagnose before collecting

An empty or weak query result has four possible causes:

```text
source absence
or ingestion failure
or labeling/understanding failure
or retrieval/index failure
```

Only the first is a verified collection gap. Check the provenance manifest, stage health, Postgres/OpenSearch state, and raw samples before asking for more data.

## Humain coverage matrix

Core themes are places/landmarks, food, lifestyle, events, and clothing/fashion. Useful cross-axes include:

- Saudi-positive versus Arab/non-Saudi negative controls;
- region, urban/rural, indoor/outdoor, and modern/traditional settings;
- formal/casual clothing and context-dependent appropriateness;
- food still life, preparation, dining, utensils, and drinks;
- national, religious, and seasonal events;
- religious/cultural symbols, Saudi flags, and false-positive symbols;
- time of day, lighting, weather, activity, people/group context, language/signage, and shot/composition;
- cultural relevance, cultural alignment, technical quality, tourism relevance, and business value; and
- exact/near-duplicate density and semantic-cluster diversity.

Compare every target cell using unique assets/hours, not raw file count alone. Dense redundant clusters do not compensate for an empty target cell.

## Output: a collection brief

For every verified high-priority deficit, specify:

- theme/subtheme and business use case;
- positive-target or negative-control role;
- geography, setting, activity, and cultural context;
- current versus target unique assets/hours;
- requested quantity and diversity constraints;
- explicit exclusions and anti-duplication rules;
- required provenance/metadata; and
- MI queries plus deterministic checks used for acceptance.

Each new round is ingested under a fresh Feature Registry/schema/index, measured against the preserved baseline, and consolidated only through another explicitly isolated ingestion if a combined view is required.

## Related

- [[wiki/entities/media-intelligence]]
- [[wiki/concepts/media-intelligence-ingestion]]
- [[wiki/entities/foundry]]
- [[wiki/sources/media-intelligence-operations-research]]
