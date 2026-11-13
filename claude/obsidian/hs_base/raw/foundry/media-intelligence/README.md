# Media Intelligence

Video understanding pipeline for Foundry: ingests videos, extracts scenes, runs ML inference (OCR, transcription, audio tagging, face detection, NSFW, brand classification), and exposes a search API.

## Structure

- `backend/` — Python application (FastAPI API, data processing pipelines, ML cog services, SearchCut client)
- `terraform/` — AWS infrastructure (S3, RDS, security groups) for staging and production
- `frontend/` — Accidentally deleted during a cleanup of legacy code. The last version can be found at the [`archive/root-web`](https://github.com/Adobe-Firefly/foundry/tree/archive/root-web) tag — pull relevant parts back as needed.
