# Slack Canvas snapshot — Media Intelligence Ingestion Guide

Source: https://adobe.enterprise.slack.com/docs/T024FSURM/F0BNRGLJ1HB  
Canvas ID: `F0BNRGLJ1HB`  
Loaded: 2026-08-25  
Canvas title: **Media Intelligence Ingestion Guide**  
Canvas says updated: **August 24**

This is a durable Markdown capture of the operational content loaded from Slack. The original Canvas remains the authority for later changes. Supporting screenshots are preserved in `canvas-images/`.

## Setup

The orchestration repository is:

https://github.com/Adobe-Firefly/foundry-mi-data-ingestion

All work should use branch `vananth/ingestion-v2`.

### Option 1 — live link

If Varun's MI Pluto job is running:

https://ai.corp.adobe.com/compute/jobs/a7e3551b-5f94-489b-b6d5-1a4f9361d054?view=owner

The Canvas-listed Airflow live link is available only on VPN or Adobe Wi-Fi:

https://pluto-prod-vananth-mi-airflow-dev-11-0-8080.or2.colligo.dev/

### Option 2 — cloned Pluto node

If the job is not running, clone it, SSH into the node, navigate to:

```text
/home/colligo/foundry-mi-data-ingestion
```

Then run:

```bash
bash bootup.sh
```

Airflow should be available at `http://localhost:8080/`. A shareable Colligo link can be formed as:

```text
https://<POD_NAME>-8080.or2.colligo.dev/
```

The pod name is in the Pluto job's Technical Details.

### Option 3 — fresh Pluto node

Use only when the cloneable job is unavailable/broken. Create an interactive session with at least an NVIDIA A100 40 GB so the job lands on `colligo-laser02-prod-uw2`; clone the repository and follow Option 2.

## Triggering ingestion

Open Airflow's **Dags** page and trigger `foundry_media_intelligence_pipeline` with a single run. The UI groups parameters under Pluto Configuration, Media Input, Feature Registry, Domain-specific configuration, Data quality gates, Development, and Advanced Options.

Critical fields:

### Input parquet path

Must contain the `s3_url` column and may include `title_name` as a pretty name. It defines what gets ingested. A parquet can also be generated from an S3 folder.

### Preview upload S3 directory

Where scaled video previews go. These are generated on the Genie side and are required by the UI. Save the exact path.

### Feature Registry version

Feature Registry versions cannot be deleted after creation. Assets from different ingestions can clash if a new ingestion reuses an old ingestion's Feature Registry version.

Reusing the same Feature Registry version is allowed only when retrying the same ingestion to fill assets that failed to parse.

### Domain info

May be:

- a plain text string passed to MI stages as-is; or
- an S3 path containing domain-information text and image files.

In the S3 form, scanning looks for `.txt` plus same-named subfolder pairs. For example, `mycharacter.txt` pairs with all images under `mycharacter/`. The scan is recursive, allowing nested contexts. Text is inserted before paired images and the combined context is supplied to MI stages.

### Additional granularities

A list of clip durations, in seconds, used for different levels of event analysis. Multiple levels are allowed.

After configuration, trigger the run and monitor stage progress through each stage's `monitor_event` task. One screenshot shows a live DAG whose groups include TAC, event, speech, and frame processing, with data-quality checks after stage monitoring.

## Postprocessing

Once ingestion completes, trigger `foundry_media_intelligence_postprocessing`.

The UI groups parameters under Feature Registry, Database, Agglomeration, OpenSearch Indexing, Development, and Advanced Options.

Critical fields:

### Input parquet path and Feature Registry version

These unite ingestion and postprocessing and must be exactly the same values used by the ingestion DAG.

### Postgres connection string

Retrieve from Vault:

```text
dme_colligo/services/foundry/media_intelligence/dev_foundry_postgres
```

### Postgres schema

The database account/isolation boundary. Do not point a new ingestion at an existing schema because it can corrupt or mix database state.

### Franchise and entity grouping instructions

Used by agglomeration to group related assets into franchises and related subjects across assets into entities. These instructions are supplied as context to guide grouping.

### OpenSearch host

Retrieve from Vault:

```text
dme_colligo/services/foundry/media_intelligence/dev_foundry_opensearch
```

When postprocessing completes successfully, the data is considered fully ingested.
