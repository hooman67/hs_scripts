---
type: entity
title: Media Intelligence
tags: [foundry, media-intelligence, multimodal, video-understanding, ingestion, search, agent]
created: 2026-07-05
updated: 2026-08-25
sources: ["[[raw/foundry/media-intelligence/README.md]]", "[[raw/media-intelligence-operations-research-2026-08-25.md]]"]
---

# Media Intelligence

**Media Intelligence** is Foundry's offline multimodal-understanding and retrieval system for turning large customer media libraries into structured metadata, semantic search, analytics, and recommendations.

## Purpose

MI serves two connected roles:

1. Automatically analyze a new [[wiki/entities/foundry|Foundry]] customer's S3 media library so engineers can understand the corpus without reviewing it manually.
2. Provide an intelligence layer through which users search, retrieve, analyze, and receive recommendations over customer-owned media.

The system is POC/internal-dogfooding scale in MVP1.1. Its product direction is **Deep Understanding → Intelligent Search → Recommendations → Creation**.

## Architecture

```text
S3 media
  → offline per-asset processing
  → Feature Registry + stage outputs
  → postprocessing/agglomeration
  → Postgres + OpenSearch/embeddings
  → natural-language search and agent
```

The pipeline is **memoryless per asset**: it processes each asset independently. Cross-asset meaning comes from agglomeration—which groups assets into franchises and subjects/characters into entities—and from the search/agent layer.

See [[wiki/concepts/media-intelligence-ingestion]] for the operational runbook.

## Understanding signals

Documented outputs include:

- timestamped transcription and shot boundaries from TAC;
- story, scene, or event analysis;
- speech segments, speaker/context, and transcription;
- fine-grained shot/event descriptions;
- original-resolution frame analysis with OCR, faces, objects, brands, NSFW signal, and best-frame timestamps;
- AdobeOne embeddings for quick/semantic search; and
- cross-asset franchise/entity groupings after postprocessing.

The exact live stage graph is version-dependent. The August 2026 Airflow screenshot shows TAC, event, speech, and frame groups; older documentation also names story and shot stages. Record the live DAG version and commit rather than assuming a historical graph.

## Storage and isolation boundaries

| Boundary | Rule |
|---|---|
| Input manifest | Parquet contains `s3_url`; `title_name` is optional. Keep richer provenance separately. |
| Feature Registry version | Immutable; fresh for every new ingestion. Reuse only for retrying the exact same ingestion. |
| Postgres schema | Account/data-isolation boundary; fresh for each ingestion. |
| OpenSearch namespace/index | Keep isolated with the corresponding schema/run. |
| Source media | Customer-owned source remains read-only; MI stores indices, transcodes, and metadata rather than treating source as mutable pipeline state. |

## How to use it responsibly

MI supports natural-language queries such as finding scenes by subject, setting, activity, emotion, spoken words, OCR text, object, landmark, or visual semantics, with timestamped retrieval and rationale. It is also useful for dataset exploration and collection planning through [[wiki/concepts/media-intelligence-gap-analysis]].

Agent output is exploratory evidence, not authoritative accounting. MVP1.1 documents prompt sensitivity and answer variability. Important counts and apparent gaps must be reconciled against manifests, health reports, Postgres, OpenSearch, and representative raw samples.

## Repository structure

The Foundry monorepo contains the MI application area (`media-intelligence/`), including Python backend/data processing, infrastructure, and newer pipeline work. Current ingestion orchestration is documented separately in `Adobe-Firefly/foundry-mi-data-ingestion`, with Genie/Glimmer providing core processing stages.

## Related

- [[wiki/entities/foundry]] · [[wiki/entities/pluto]]
- [[wiki/concepts/media-intelligence-ingestion]]
- [[wiki/concepts/media-intelligence-gap-analysis]]
- [[wiki/concepts/foundry-aws-access]]
- [[wiki/concepts/foundry-dev-workflow]]
- [[wiki/sources/media-intelligence-operations-research]]
