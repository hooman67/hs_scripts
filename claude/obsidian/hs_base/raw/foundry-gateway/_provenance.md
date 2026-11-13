# Provenance — foundry-gateway ingest

Immutable record of sources for the Foundry gateway / AWS-access ingest.
Date: **2026-07-05**. Do not edit.

## Sources read

### Live fetch (auth-gated)
- `WebFetch https://foundry-aws-corp.adobe.io/` — authenticated IMS endpoint. WebFetch
  returned an **unverified** summary (no hard error), captured verbatim in
  `gateway-docs.md`. Not treated as authoritative page content. The signed-in gateway UI
  (the "Get Foundry Developer Credentials" button, provider tabs) was **not** directly
  observable.

### Skills (copied here, `raw/foundry-gateway/skills/`)
- `aws-creds.md` — backing script `~/.claude/scripts/foundry_aws_creds.py` (read, not copied — outside vault).
- `generate-from-endpoint.md` — backing script `~/.claude/scripts/generate_from_endpoint/runner.py`.
- `render-s3-gallery.md` — templates at `~/hs_scripts/claude/temp_work/lifestyle_gallery/`.
- `eval_hub_upload.md` — backing script `~/.claude/scripts/eval_hub_upload.py`.
- `html-to-appen-csv-for-humain.md` — backing script `~/.claude/scripts/html_to_appen_csv.py`.
- `vendor-generate.md` — backing script `~/.claude/scripts/vendor_generate.py`.
- `gcp-gemini.md` — backing script `~/.claude/scripts/gcp_gemini.py`.

### Foundry repo docs (read only, NOT modified)
- `/Users/hshariati/foundry/docs/project-setup-and-access.md` — the canonical access doc
  (§2.2 How Credentials Work, §2.3 AWS, §2.9 IMS clients, §3 admin).
- `/Users/hshariati/foundry/docs/gen-foundry-auth-allowlisting.md` — gen-foundry two-layer
  auth (CGW client-id allowlist + per-model allowlist).
- `/Users/hshariati/foundry/modeling/terraform/foundry-prd/aws_gateway/` — the IAM plumbing
  (`service_iam_user.tf`, `client_iam_role.tf`, `client_iam_policy.tf`, `README.md`).

## Backing script paths (not copied — live outside the vault)
- `/Users/hshariati/.claude/scripts/foundry_aws_creds.py`
- `/Users/hshariati/.claude/scripts/generate_from_endpoint/runner.py`
- `/Users/hshariati/.claude/scripts/eval_hub_upload.py`
- `/Users/hshariati/.claude/scripts/html_to_appen_csv.py`
- `/Users/hshariati/.claude/scripts/vendor_generate.py`
- `/Users/hshariati/.claude/scripts/gcp_gemini.py`

## Auth-blocked / uncovered
- The authenticated gateway web UI and any docs it links behind IMS login could not be
  directly fetched. `credential-vending-service.md` is referenced by the auth-allowlisting
  doc but was not present in the local `foundry/docs/` snapshot.
