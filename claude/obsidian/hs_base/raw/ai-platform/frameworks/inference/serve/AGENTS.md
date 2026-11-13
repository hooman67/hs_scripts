# The inference (serve) framework

This folder hosts the code for the inference (serve) framework — a standalone `pip install`able Python library for defining inference workers, pipelines, and web apps. It does not depend on managed services or the platform build system.

- **Deployment platform** (Bazel, k8s, Argo CD): [platforms/inference](/platforms/inference/)
- **Managed services ecosystem** (where users contribute code): [colligo/managed_services](https://github.com/Adobe-Firefly/colligo/tree/main/managed_services)

## Important links

API: @./aidoc/api.md
High level use-case: @./aidoc/index.md
Samples: @./aidoc/samples/index.md

## Design docs

Design docs and iterating with agent: @./_design/

This folder is used to lay high level problem, implementation idea, and planning for features or bug fixes.

The workflow is:
* Human write a high level problem statement and design doc.
* Iterate with agent to refine and implement the design.
* Once done, make sure it is in sync with the codebase, then mark it as archive.

Guidelines:
* Each file should start with the ticket number (so they are sortable).
* Each file should have a owner, and a date.

## Project rules and guidelines

### API philosophy

- Any python public API will be exposed to the user as
    ```py
    from frameworks import inference

    inference.X() or inference.namespace.X()
    ```
    This is done by exposing the symbols under @__init__.py. Symbols that need to be exposed under a namespace (e.g. `inference.builtin_webapps`, `inference.types`) live as modules at the package root (e.g. @builtin_webapps.py, @types.py) and are re-exported via @__init__.py.
- A few APIs are executable entrypoints. Those are exposed as `python -m frameworks.inference <subcommand>`. The subcommands are also listed under @aidoc/api.md.
- All public APIs then are documented under @aidoc/api.md.
A few APIs are executable entrypoints. Those are exposed as `python -m frameworks.inference <subcommand>`. The subcommands are also listed under @aidoc/api.md.

All public APIs then are documented under @aidoc/api.md.

### The `inference.types` namespace

The `inference.types` namespace is reserved for symbols that users need for **type annotations** but should **never construct directly**. These are types the framework creates and passes to user code (e.g. callback parameters, injected context objects).

Examples:
- `inference.types.ExecuteKit` (injected into worker `execute()` and webapp endpoints)
- `inference.types.OnCompleteInfo` (passed to `on_complete` callbacks)
- `inference.types.BackgroundJob` (returned by `submit(mode="background")`)
- `inference.types.WorkerHandle` (returned by `inference.depends_on.worker_handle()`)

Types that users **do** construct (e.g. config objects like `BackgroundJobsConfig`) live directly on the `inference` namespace, not under `inference.types`.

### ExecuteKit injection in webapp endpoints

The `ExecuteKit` object provides context-dependent operations (e.g. `kit.query_background_job()`). It is available in both worker `execute()` methods and webapp endpoints.

For webapp endpoints, the `kit` parameter is **optionally** declared in the endpoint signature. The framework detects it by type and injects it automatically:

```py
@inference.endpoints.get("/my-jobs/{job_id}")
async def custom_query(self, job_id: str, kit: inference.types.ExecuteKit):
    result = await kit.query_background_job(job_id)
    ...
```

This keeps APIs that depend on framework context (session managers, job queries) scoped to where they are meaningful, preventing misuse from arbitrary locations in user code.

### Historical note

This framework is an attempt to create a low cognitive overhead over an older inference framework called colligo.

You can find colligo vendored under @./_private/colligo.

We are not trying to reuse most of the old functionalities and just expose them with a more intuitive API, such that one
can just use the new framework by pip installing it. The old way of doing things had the code tightly coupled with a monorepo.

The way currently the two work together is as follows:
    1. We try to minimize the symbols we want to use from `colligo` and have explicit control over it. Any symbol that we need
    to use from colligo in the rest of the framework is aliased to `frameworks.inference._private.colligo.<symbol>`. Then use as
    `from frameworks.inference._private import colligo`. These symbols should never be exposed out to the inference framework public API
    2. There are very few scenarios that it is hard to follow (1) and we need some code that tightly works with internals of colligo.
    In such scenario, we put the code under @_private/colligo/shims. Everything under `colligo` except this folder is vendered. Then we expose what is in @_private/colligo/shims such that it can be used in the rest of the framework as `from frameworks.inference._private import colligo; colligo.X`

**IMPORTANT: Vendored code boundary.** The `_private/colligo/` directory contains vendored colligo v2 code. **Do not modify** any files in `_private/colligo/` except for:
- `_private/colligo/__init__.py` — the interface file that exposes colligo symbols to the rest of the framework
- `_private/colligo/sync.py` — synchronization utilities
- `_private/colligo/shims/` — custom shim code that bridges v3 → v2

All other subdirectories (`aiohttp/`, `base/`, `data/`, `external_services/`, `fastapi/`, `httpx/`, `rhode/`) are vendored and must not be edited directly.

#### Migration layer (v2 → v3 config bridge)

The @migration/ folder provides a unified configuration layer for external services being migrated from colligo v2 to v3:
- CAI (Content Authenticity Initiative)
- IMS (Identity Management Services)
- Business Kit Service (authorization/metering)
- Object Store (session support)
- Temp Storage (blob storage)
- Storage Endpoint (WebApp storage routes)

**Config structure:**
- Users configure via unified `MigrationConfig` in @migration/default_config.py
- The config shim (@_private/colligo/shims/config_shim.py) automatically propagates v3 config → v2 global config
- Migration services are optional dependencies (install with `pip install frameworks.inference[migration]`)

### Use of `Path(__file__).resolve()`

Because we use this library in some ocassions with Bazel, we need to avoid using `Path(__file__).resolve()`. This Bazel puts all files under a runfile tree using symlinks, but using `resolve()` will return the actual path of the file, breaking the expected file structure in runfiles.

E.g. we might expect a file be present under `Path(__file__).parent / "foo.txt"` made a Bazel rule (e.g. genrule, binary_manifest). But if we use `Path(__file__).resolve().parent / "foo.txt"`, it will return the actual path of the file beside which `foo.txt` does not exist.

It is recommended to use `norm_path(__file__)` instead from _private/path_utils.py.

Note that using `resolve()` on other occassions can be fine. E.g. when finding working directory of redis server.

### Use of relative imports

- Relative imports are encouraged as long as they don't go to parent folder.
- When needing parent folder import, use absolute imports.

## Development workflows


### Pre-PR checklist

- `./make lint` passes
- `./make test` passes
- If you modified the public API surface (`__init__.py`, `default_config.py`, `migration/__init__.py`, `migration/default_config.py`, or any class/function they reference), run the `api-docs` skill to regenerate API documentation in `aidoc/api.md`.

### Running tests

Before making a PR we should make sure all tests pass

```
./make test
```

### Running lint

Lint should always pass. It runs ruff and mypy

**Do not run mypy directly**. It won't work due to using `ai.hatch` build backend. Just use the lint command below.

```
./make lint
```

### Building docs

```
./gtools docs build
```

### Agent interact with PRs

Developers may wish to interact with the coding agent through PR comments. In that case, when asked to address feedback for a PR, you can use `gh` to get the active comments of the PR.

If `gh` is not setup, ask the human to install and authenticate it. Give the human the exact commands they need to run.

### Misc notes

- We use the `ai.hatch` build backend. It is a wrapper around hatch, that allows all files here to be importable as `frameworks.inference` without any extra effort. This is defined by the `import_prefix` in `pyproject.toml`.
- Checking in binaries directly are not allowed. We use the `./gtools binaries` tool for this, which is documented under @../../../platforms/dev_tools/aidoc/binary-management.md
- tests are named as `*_test.py` and go beside the file they are testing.
