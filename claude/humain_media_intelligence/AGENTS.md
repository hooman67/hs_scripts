# Humain Media Intelligence project instructions

This project is the durable handoff for ingesting Humain mission media into Foundry Media Intelligence and using the result to plan new collection rounds.

At the start of every session, read these files in order:

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `INPUTS.md`
5. `sources/slack-canvas-media-intelligence-ingestion-guide-2026-08-24.md`

Do not repeat the Slack Canvas, Obsidian, or Confluence research unless a runtime fact may have changed. Treat `CONTEXT.md` as the handoff and verify only volatile state such as Pluto job status, the live Airflow DAG version, Feature Registry/schema name availability, credentials, and S3 inventory.

Operational rules:

- Use the global matching skills proactively.
- Any AWS command must first use `/aws-creds`, then source `~/.claude/hshariati/aws_creds.env` in the same shell command as the AWS call.
- Never print or persist Slack, Vault, AWS, GitHub, Postgres, or OpenSearch credentials.
- Preserve the supplied `misions/` spelling in every S3 source path.
- Use only the official customer bucket `foundry-humain-default-adobe-assets`; do not create another bucket. Put generated MI artifacts under a new isolated prefix in that bucket.
- Source prefixes are read-only. Write manifests, previews, stage outputs, and reports under a new isolated run root.
- A Feature Registry version may be reused only for retries of the exact same ingestion. A new dataset or collection round requires a new Feature Registry version.
- Postprocessing must use the same input parquet and Feature Registry version as its ingestion run.
- Every new ingestion needs a fresh Postgres schema and isolated OpenSearch namespace/index.
- The two dated deliveries for mission `9c3e6442-6e54-4d82-9969-7c0ddbd87d9c` are a duplicate-run candidate. Compare them at object level; do not blindly discard either delivery.
- Do not treat an empty MI search result as proof of a source-data gap until ingestion completeness and index/search behavior have been checked.
- Keep full provenance outside MI's minimal `s3_url`/`title_name` input schema.
- Full Klam credentials are available at `/Users/hshariati/Downloads/creds.txt`. Read them only when needed, never print or copy their values into this project, and ask Hooman promptly when Artifactory or another dependency needs missing credentials instead of spending excessive time on workarounds.

Execution has started. Before resuming, read `runs/humain-missions-20260825/SESSION_HANDOFF.md` for the current run state, verified worker evidence, blocker, and recovery sequence. Do not rely on the obsolete earlier status that this project was planning-only.
