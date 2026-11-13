# aidoc

Documentation is distributed across the repo in co-located `aidoc/` directories near the code they describe.
To find docs for a topic, start with `aidoc/root.md`, which maps topics to their doc locations (e.g. inference-platform, compute-platform, data-platform, monorepo).
For code-specific docs (a particular model, library, or service), look for an `aidoc/` directory adjacent to that code.

## Commands

- `./m docs.build`
- `./m docs.serve`
- `./m docs.checklinks`
- `./m docs.sync_assets` (manages `aidoc/_assets`; never edit that directory by hand)
- Entrypoints: `aidoc/make.py`; canonical doc rules: `aidoc/documentation/rules.md`

## Conventions

- Place docs in an `aidoc/` folder as close as possible to the code they describe (including API reference).
- Preserve `document_type` frontmatter; keep each document focused on a single purpose (tutorial, guide, rules, reference, or landing page).
- Use repo-relative on-disk links (`/path/to/file`); never link to GitHub blob URLs for monorepo files.
- Root navigation, landing pages, and redirects live in `aidoc/root.md`.
