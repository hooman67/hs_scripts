# Python Build System

The Python build system enables the following:
- Registration of different Python modules.
- Collection and locking of fixed dependency versions for these modules in a [single lock file](https://docs.astral.sh/uv/pip/compile/).
- Creation of a Python virtual environment for development with these dependencies and modules.

## File Structure

The system is primarily controlled by the following files:
  - [root pyproject.toml](/pyproject.toml) under `tool.colligo.repo` section: General configuration.
  - [envs/dev/requirements.lock.txt](/envs/dev/requirements.lock.txt): Versions of all dependencies used in the monorepo.
  - [envs/dev/known-packages.txt](/envs/dev/known-packages.txt): A mapping of package imports to package names, used in [static analysis](/aidoc/static-analysis/overview.md).
  - [envs/dev/constraints.txt](/envs/dev/constraints.txt): Input for generating `requirements.lock.txt`, with constraints on dependency versions and sources.
  - [envs/common/constraints-darwin-exclusions.txt](/envs/common/constraints-darwin-exclusions.txt): Input for generating `requirements.lock.txt`, listing packages incompatible with macOS.
  - [envs/common/overrides.txt](/envs/common/overrides.txt): Input for generating `requirements.lock.txt`. Similar to `envs/dev/constraints.txt`, but overrides all constraints specified in dependency tree. Should be rarely used in `main`; more useful for experimental branches.
  - Various [colligo.yaml](https://github.com/search?q=repo%3AAdobe-Firefly/colligo%20path%3Acolligo.yaml&type=code) files within the monorepo under the [models/](/models/) and [pylibs/](/pylibs/) folders[^cstructure]. These files configure Python packages within the monorepo and allow specifying dependencies with less boilerplate than native `pyproject.toml`. [Static analysis](/aidoc/static-analysis/overview.md) helps populate and maintain these files.
  - `pyproject.toml` files only for code under [contrib](/contrib) and [third_party](/third_party) folders[^cstructure]. These folders are not fully integrated with monorepo tooling, so configuration reading from `pyproject.toml` is still allowed.
  - [./m](/m) command dispatcher for executing build commands.
  
## Commands

### Changing Dependencies

- `./m lint`: Runs static analysis to ensure all dependencies are referenced in `colligo.yaml` files.
- `./m deps.lock`: Regenerates `requirements.lock.txt`. Should be run whenever dependencies or constraints are changed; updated files should be checked in. Must run on Linux for CUDA/GPU environments.
- `./m deps.lock.docker` *(experimental)*: Same as `deps.lock` but executes inside a `linux/amd64` Docker container. Use on macOS to lock CUDA/GPU environments that are otherwise skipped locally. Requires Docker Desktop and `ARTIFACTORY_UW2_API_TOKEN`.

### Building

- `./m deps.sync`: Prepares the local development environment for development and runs generation scripts for modules with `.proto` files.
- `source m`: Activates the development environment.
- `./m package.rhode`, `./m package.pluto`: Packages release candidates for inference and compute platform services.

## Configuration

### root pyproject.toml

```{colligo_docstring} colligo.repo.types:AnalyzeConfig
```

### colligo.yaml Files

```{colligo_docstring} colligo.repo.types:ColligoPackageConfig
```

```{colligo_docstring} colligo.repo.types:PublicPackageInfo
```

## Frozen Environments

These are files like `envs/frozen/torch-2.1.0.lock.txt`, used for dependency migrations that cannot be updated all at once. For example, [see the process we used to update Torch from 2.1 to 2.3](/aidoc/announcements/2024-09-01-torch-migration.md).

At any given time, only one frozen environment is supported to keep monorepo operations manageable.

[^cstructure]: [What Each Folder Means](/aidoc/source-control/index.md)
