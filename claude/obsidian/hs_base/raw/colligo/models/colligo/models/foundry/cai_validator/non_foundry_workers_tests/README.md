# Non-Foundry worker compliance YAMLs

CAI compliance test-case YAMLs kept **out of** the per-pipeline autodiscovery
trees:

- `models/colligo/models/foundry/workers/<worker>/cai_validator/*.yaml`
- `models/colligo/models/firefly/pipelines/<pipeline>/cai_validator/*.yaml`

Foundry **workers** keep their YAML co-located next to their code. This directory
holds the rest:

- The **lego** (Image 5) pipeline (`lego_v1.yaml`).
- Any worker whose code lives **outside** `foundry/workers/`, where adding a
  `cai_validator/` folder to its (non-Foundry) package would be intrusive.

## Layout

Flat — one file per pipeline/worker, named for it. There is **no**
`<name>/cai_validator/` nesting here; this directory *is* the compliance
location, and discovery globs `non_foundry_workers_tests/*.yaml` directly.

    non_foundry_workers_tests/
      lego_v1.yaml
      <worker>.yaml
      README.md   (this file)

## File format

Identical to the co-located YAMLs — the `EndpointYAML` schema in
`colligo.models.foundry.cai_validator.types`. Each file self-identifies via its
`endpoint.api_path` and `endpoint.pipeline_worker`.

Asset `file:` paths resolve repo-root-relative, so shared LFS fixtures are
referenced the same way as in every other YAML, e.g.
`data/test/cai_compliance/c2pa_signed_ref.jpg`.

Load + schema-validate every discovered YAML (including these) without calling
any endpoint:

    python -m colligo.models.foundry.cai_validator validate
