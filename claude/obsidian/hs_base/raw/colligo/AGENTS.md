# Colligo

AI Platform monorepo: shared Python libraries, ML models, inference services, and build tooling. ("V2")

## Boundaries

- NEVER modify files in `third_party/`, `uv.lock`, or `*.lock` files
- NEVER modify generated files: `*_pb2.py`, `*_pb2_grpc.py`, `*_pb2.pyi`, `registry/applications.yaml`
- NEVER use plain `assert` in production code; use `validation_assert` or `runtime_assert` from `colligo.base.exceptions`

## Repo map

```
pylibs/              # shared Python libraries (colligo.* namespace)
  colligo/pluto/     #   Compute Platform (Pluto) - GPU/CPU job scheduling, quotas, training observability
  colligo/rhode/     #   Inference Framework internals
models/              # ML model packages
managed_services/    # managed inference services ("V3"); separate Bazel workspace with its own AGENTS.md
contrib/Mori/        # Training Framework (Mori) - GenAI training code and tooling
docker/              # container images
tools/               # build/lint scripts, tasks.py (./m CLI)
envs/                # Python environment configs (UV)
aidoc/               # platform docs; see aidoc/root.md for topic index
data/                # test fixtures (LFS-tracked)
registry/            # generated; do not modify
```

Many subdirectories contain their own `AGENTS.md` with package-specific guidance.
Docs live in co-located `aidoc/` directories near the code they describe; consult `aidoc/root.md` for the top-level topic map.

## Doc routing

| Topic | Start here |
|---|---|
| Inference (serving, workers, Ethos) | `aidoc/inference-platform/index.md` |
| Compute / Pluto (GPU jobs, quotas) | `pylibs/colligo/pluto/aidoc/index.md` |
| Managed Services (V3) | `managed_services/README.md` |
| Deployment (Helm, Ethos, Argo) | `aidoc/inference-platform/infra/colligo-deploy/index.md` |

`colligo-deploy` is a separate repo (`git.corp.adobe.com/firefly/colligo-deploy`) holding Helm charts and Ethos Flex config for V2 inference deployments. This repo has source code; `colligo-deploy` has the per-env `values.yaml` files that Argo CD syncs to clusters.

## Commands

```bash
./m deps.create                     # create dev environment (UV)
source m                            # activate dev environment
./m deps.sync                       # sync submodules + python dependencies
./m lint                            # auto-fix lint + format + mypy
./m lint --check                    # check only, no fixes
./m lint --paths "path1 path2"        # lint specific paths (recommended to speed up slow mypy check)
pytest path/to/test_file.py         # run tests
```

## Coding standards

- Python 3.10+ with strict type annotations on all public functions
- Absolute imports only (`from colligo.base.x import y`); no relative imports
- `validation_assert(condition, details)` for user input errors (HTTP 422)
- `runtime_assert(condition, details)` for internal invariant violations (HTTP 500)
- All source files require the Adobe copyright header
- Google-style docstrings (Args/Returns/Raises) for public functions
- Directories excluded from pytest: `contrib/`, `third_party/`, `managed_services/`, `vendor/`, `_build/`

## Pull request format

PR titles MUST include a JIRA ticket prefix in brackets, e.g. `[FIREFLY-123] Fix memory leak in RGBX worker`. If no Jira ticket exists, use `[NOJIRA]` as the prefix.

PR body MUST follow the repo's PR template at `.github/PULL_REQUEST_TEMPLATE.md`. Read that file and fill in all sections and checklists it specifies. Do not omit any section.
