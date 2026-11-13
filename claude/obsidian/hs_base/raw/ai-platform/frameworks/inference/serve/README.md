# Inference Framework - Internal

Public docs: [](./aidoc/index.md)

Code: [frameworks/inference](.)

## Dev workflows

### Vscode env

```
./make venv
```

you can run tests from vscode normally.

### Other make commands

```
./make --help
```

| Command | Description |
|---------|-------------|
| `./make venv` | Prepare a venv for development |
| `./make lint` | Static analysis (auto-fix); `--check` to only report |
| `./make test` | Run the tests |
| `./make check-changelog VERSION` | Verify a changelog entry exists for VERSION |
| `./make release VERSION` | Validate changelog, tag, and push a release (e.g. `./make release 0.3.10`) |
| `./make publish` | Build and publish the wheel to Artifactory (called by CI) |

## Components

### [`__init__.py`](./__init__.py)

All the public API exposed as `inference.<...>`. Users are only allowed to call such APIs.

### Namespace modules (`builtin_webapps.py`, `depends_on.py`, `types.py`)

Modules at the package root that are exposed to users under a namespace, e.g. `inference.types`, `inference.builtin_webapps`. These are real submodules so that `importlib.import_module` resolves them naturally.

### [`_private`](./_private)

Internal code, not exposed to user.


#### [`_private/colligo`](./_private/colligo)

Vendored portions of colligo (inference v2), needed for distributed communication and logging infrastructure.

 V3 extends V2 through a **shim layer** that bridges v3 configuration with v2 implementation:

- **V2 Implementation**: Proven multiprocess communication, Redis queues, logging formatters
- **V3 Configuration**: Clean, explicit config API with environment variable support
- **Shim Layer**: [`shims/`](./_private/colligo/shims/) contains bridge code that propagates v3 config to v2 global state

**Key Shims**:

```{colligo_list_files} ...
```

**Usage**: Do not use code from `colligo` directly. Alias only required API in its `__init__.py` and use them as `colligo.X` in rest of code. This is to keep a tab on what APIs are relevant.

- **V2 Implementation**: Proven multiprocess communication, Redis queues, logging formatters
- **V3 Configuration**: Clean, explicit config API with environment variable support
- **Shim Layer**: [`shims/`](./_private/colligo/shims/) contains bridge code that propagates v3 config to v2 global state

**Key Shims**:
- `config_shim.py`: Propagates v3 `InferenceFrameworkConfig` → v2 global config (especially logging formatter)
- `task_executor.py`: Bridges v3 workers with v2 Redis task queues  
- `task_submitter.py`: Allows v3 components to submit tasks via v2 infrastructure
- `http_server.py`: HTTP server functionality with v2/v3 serialization bridge

**Usage**: Do not use code from `colligo` directly. Alias only required API in its `__init__.py` and use them as `colligo.X` in rest of code. This is to keep a tab on what APIs are relevant.


#### [`_private/run/distributed`](./_private/run/distributed)

Code needed for API and implementation of distributed serving and communication. Relies on Colligo.

#### [`_private/run/local`](./_private/run/local)

Code needed for API and implementation of local serving and running.

#### [`_private/vendor`](./_private/vendor)

Vendoring binaries that are needed at runtime (Redis server, s5cmd)

#### [`_private/torch`](./_private/torch)

Code that deals with the torch optional dependency.

#### [`_private/worker_api`](./_private/worker_api)

Code for the `Worker` object

#### [`_private/webapp_api`](./_private/webapp_api)

Code for the `WebApp` object

#### [`frameworks_inference_serve.yaml`](./frameworks_inference_serve.yaml)

Github actions CI config. It is a symlink to the same file under `.github/workflows`. Github only picks up files from that location.
