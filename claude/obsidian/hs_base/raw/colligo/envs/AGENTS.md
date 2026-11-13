# envs

Python environment definitions and constraints. Lock files and package indices are generated; never hand-edit them.

## Boundaries

- NEVER create a new environment without architecture approval.
- NEVER edit `requirements.lock.txt`, `known-packages.txt`, or `linter-roots.txt`; these are generated. Edit `constraints.txt`, `dev.txt`, `testing.txt`, or `common/overrides.txt` instead, then run `./m deps.lock`.

## Commands

- `./m deps.create --env <env>` - create/update a specific env's venv
- `./m deps.lock` - regenerate lock files (run on Linux; some envs don't support macOS)
- `./m deps.lock.docker --env <env>` - **[experimental]** same as above but runs inside a linux/amd64 Docker container; use on macOS when CUDA/GPU envs must be locked locally (requires Docker Desktop and `ARTIFACTORY_UW2_API_TOKEN`)
- `./m deps.lock_check` - verify locks are up to date
- `./m deps.enable <env>` / `./m deps.disable <env>` - toggle an env

## Key files

- `envs/common/overrides.txt` - shared override constraints across all envs
- `envs/dev/constraints.txt` - default dev environment constraints
- `aidoc/monorepo/pyenvs.md` - design doc for multi-env support

## Pitfalls

- Packages may use a non-default env via `custom_pyenv` in their `colligo.yaml`; check before assuming `dev`.
- After editing constraints, regenerate locks and verify the diff in `requirements.lock.txt`, `known-packages.txt`, and `linter-roots.txt`.
