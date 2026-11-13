# V6.4 writer: structured customer-source compatibility

Isolated successor to frozen V6.3 r2, approved 2026-11-10.
Runtime `v6.4-writer-runtime-r1-structured-sources`.

The only behavior delta is structured-source interpretation and citation
eligibility: section content and labeled field values are substantive;
confidence, template/container IDs and structural labels are not evidence.
Existing metadata exclusions and application-owned evidence normalization
remain in effect. Legacy strings/objects remain accepted.

The source-pair loader accepts paired JSON files or ZIP bundles without
flattening values, changing array order or extracting archive paths. It
reports malformed/missing/duplicate documents and records original hashes.
Provenance is external to the unchanged three-field runtime request.

## Unchanged assets and contract

The V6.3 approved catalogue remains byte-identical, including its original
approval/version identity and filename. All265 entries, the paperweight ban,
camera registry, C-Tech references, lexicon, support rules and scoring are
unchanged. Retaining the catalogue's V6.3 identifier is intentional: no new
prop approval or catalogue revision occurred.

Pass exactly `smart_brief`, `source_messaging` and `camera_tag`. Output remains
ten ranked scenes per bank, with unchanged fields, GPT-5.5/medium/16000 tokens,
and at most one full-bank repair. No image or judge changes are included.

## Local checks and release provenance

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
PYTHONDONTWRITEBYTECODE=1 python -m pytest --import-mode=importlib \
  research/source_messaging_v1_to_v6/versions/v6_4/tests -q
python research/source_messaging_v1_to_v6/versions/v6_4/build_assets.py
```

The asset builder verifies all frozen V6.3 baseline hashes and byte equality of
unchanged assets, then records this version's release hashes. It does not
recompile props or modify its predecessor.

## Generation

```bash
UV_EXTRA_INDEX_URL=https://artifacts.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple \
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_4/cli.py run \
  --input /absolute/path/to/request.json \
  --catalog /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_4/approved-v6.3-20261109.catalog.json \
  --output /absolute/path/to/new-result.json
```

The existing policy-aware Foundry SDK supplies managed Azure credentials;
coding-agent credentials and model substitutions are not used. Original
requests/responses and initial/repair/failure provenance are recorded by the
unchanged CLI journal contract.

Canonical source comparison, selected size/context mappings and empirical
evaluation status:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_4/SUMMARY.md`
