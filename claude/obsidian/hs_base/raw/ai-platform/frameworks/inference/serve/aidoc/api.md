---
sectnum: true
children:
  - ../migration/metrics/aidoc/metrics.md
---

# Inference Framework API

Here we list all the public API of the inference framework.

The API documentation serves as an index when you are somewhat familiar with the framework. If you are new, you might find the [sample apps](https://docs.ai.corp.adobe.com/managed_services/services/samples/README.html) a good companion with the API documentation for ramp up.

## Stateful actors

(api-doc-worker)=
[**`frameworks.inference.Worker`**](api-doc-worker)

Base class for every server-side "worker" that is run by the inference
platform.  A *worker* is the smallest deployable unit that can
receive a typed request, run arbitrary user code, and return a typed
response.

**`Config`**

If your base class needs to be configurable, you must
redefine in child classes.

**`Input`**

You must redefine this in child classes to define the worker
input type.

**`Output`**

You must redefine this in child classes to define the worker
output type.

- **`*classmethod* bind(*, config: Any | None = None, serve_config: ServeConfig | None = None, binary_groups: dict[str, Path] | None = None) -> Self`**

  Bind the class with configs, data, and other serve related configs
(e.g. max num requests, ...) to create variations.

- **`ref -> str`** *(property)*

  Return the full path to this worker instance, e.g. if you have

- **`execute(input: Any, kit: ExecuteKit) -> Any | Coroutine[Any, None, None]`**

  Run the worker on an input and return the output.

- **`load(params: LoadParams) -> None | Coroutine[Any, Any, None]`**

  Load the worker.

(api-doc-webapp)=
[**`frameworks.inference.WebApp`**](api-doc-webapp)

Base class for defining web applications in the inference framework.

**`Config`**

If your base class needs to be configurable, you must
redefine in child classes.

- **`*classmethod* bind(*, binary_groups: dict[str, Path] | None = None, config: Any | None = None) -> Self`**

  Bind the class with configs, data, and other serve related configs.

- **`ref -> str`** *(property)*

  Return the full path to this webapp instance, e.g. if you have

- **`load(params: LoadParams) -> None | Coroutine[Any, Any, None]`**

  Load the web app. Override this if you need a load operation.
Can be either sync or async.

(api-doc-serveconfig)=
[**`frameworks.inference.ServeConfig`**](api-doc-serveconfig)

Configuration needed for serving a worker. E.g. things like back pressure, hardware requirement,
etc .

This v3 equivalent of [DeployInfo, RhodeOptions, SessionStorageOptions] (only the parts that are still relevant)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `xpu_requirement` | CpuRequirement \\| GpuRequirement | `CpuRequirement()` | The XPU (hardware) requirement for the worker |
| `num_processes` | `int` | `1` | Number of subprocess replicas to spawn for this worker in the distributed path (``serve()`` / ``python -m frameworks.inference workers``). Each process gets its own GPU allocation. Redis queue distribution handles load balancing across processes automatically. Ignored in the ``initialize()`` path. |

(api-doc-cpurequirement)=
[**`frameworks.inference.CpuRequirement`**](api-doc-cpurequirement)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `xpu` | `Literal['cpu']` | `'cpu'` |  |
| `size` | `Literal['small', 'medium', 'large']` | `'small'` |  |

(api-doc-gpurequirement)=
[**`frameworks.inference.GpuRequirement`**](api-doc-gpurequirement)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `xpu` | `Literal['gpu']` | `'gpu'` |  |
| `num` | `int` | `1` |  |
| `memory` | `float` | *required* |  |
| `preferred_family` | `Literal['ampere', 'hopper', 'blackwell', None]` | `None` |  |


## `inference.endpoints`

Decorators for defining FastAPI style endpoints on the Web App.

(api-doc-post)=
[**`frameworks.inference.post(path: str, *, response_model: Any = None, status_code: int | None = None, tags: list[str | enum.Enum] | None = None, summary: str | None = None, description: str | None = None, response_description: str = 'Successful Response', responses: dict[int | str, dict[str, Any]] | None = None, deprecated: bool | None = None, operation_id: str | None = None, include_in_schema: bool = True, name: str | None = None, openapi_extra: dict[str, Any] | None = None) -> Callable[[CallableT], CallableT]`**](api-doc-post)

Register a POST endpoint.

(api-doc-put)=
[**`frameworks.inference.put(path: str, *, response_model: Any = None, status_code: int | None = None, tags: list[str | enum.Enum] | None = None, summary: str | None = None, description: str | None = None, response_description: str = 'Successful Response', responses: dict[int | str, dict[str, Any]] | None = None, deprecated: bool | None = None, operation_id: str | None = None, include_in_schema: bool = True, name: str | None = None, openapi_extra: dict[str, Any] | None = None) -> Callable[[CallableT], CallableT]`**](api-doc-put)

Register a PUT endpoint.

(api-doc-get)=
[**`frameworks.inference.get(path: str, *, response_model: Any = None, status_code: int | None = None, tags: list[str | enum.Enum] | None = None, summary: str | None = None, description: str | None = None, response_description: str = 'Successful Response', responses: dict[int | str, dict[str, Any]] | None = None, deprecated: bool | None = None, operation_id: str | None = None, include_in_schema: bool = True, name: str | None = None, openapi_extra: dict[str, Any] | None = None) -> Callable[[CallableT], CallableT]`**](api-doc-get)

Register a GET endpoint.

(api-doc-delete)=
[**`frameworks.inference.delete(path: str, *, response_model: Any = None, status_code: int | None = None, tags: list[str | enum.Enum] | None = None, summary: str | None = None, description: str | None = None, response_description: str = 'Successful Response', responses: dict[int | str, dict[str, Any]] | None = None, deprecated: bool | None = None, operation_id: str | None = None, include_in_schema: bool = True, name: str | None = None, openapi_extra: dict[str, Any] | None = None) -> Callable[[CallableT], CallableT]`**](api-doc-delete)

Register a DELETE endpoint.


## `inference.depends_on`

These APIs are used to declare dependencies from a worker or webapp on another worker.

### What is a dependency?

Sometimes one worker needs to call another. For example, a "Generate Image" worker might first want to run an "NSFW check" worker on the input. Instead of copying the NSFW code into your worker, or making an HTTP call yourself, you **declare** that your worker depends on the NSFW worker, and the framework gives you a small object (a *handle*) you can use to call it.

The framework uses these declarations to:
- make sure the NSFW worker is actually deployed wherever your worker runs,
- give you typed inputs/outputs (autocomplete works, mistakes are caught early),
- handle the network/serialization/retries for you.

### How to declare a dependency

Declare the handle **as a class attribute** on your `Worker` or `WebApp`, next to `Input` / `Output` / `Config`. Do *not* create the handle inside `load()` or `execute()`.

```python
from frameworks import inference
from services.nsfw import nsfw_v1  # somebody else's worker, already bound with .bind()

class MyWorker(inference.Worker):
    class Input(pydantic.BaseModel):
        image: inference.Binary

    class Output(pydantic.BaseModel):
        caption: str

    # Declared here, at the class body — the framework picks this up at startup.
    nsfw = inference.depends_on.worker_handle(nsfw_v1)

    ImplRef = ".impl.MyWorkerImpl"

my_worker_v1 = MyWorker.bind()
```

Then, inside your implementation, you use `self.nsfw` to call it:

```python
class MyWorkerImpl(MyWorker):
    def execute(self, input, kit):
        # Call the NSFW worker and wait for the result.
        check = self.nsfw.submit(self.nsfw.api.Input(image=input.image))
        if not check.is_safe:
            ...
```

### Using the handle — `WorkerHandle`

(api-doc-worker-handle)=
[**`frameworks.inference.worker_handle(worker: WorkerT) -> WorkerHandle[WorkerT]`**](api-doc-worker-handle)

Declare dependency on another worker from an orchestrator worker.


`depends_on.worker_handle(...)` returns an `inference.types.WorkerHandle`. It has two ways to call the other worker. You pick based on whether your `execute()` (or endpoint) is **regular** (`def`) or **async** (`async def`):

- **`submit(input, ...)`** — use inside a regular `def execute(...)`.
- **`submit_from_el(input, ...)`** — use inside an `async def execute(...)` or any `WebApp` endpoint (endpoints are always async). You must `await` it.

If you use the wrong one for your context, the framework raises a clear error telling you to switch.

Each of them supports two **modes**:

- **`mode="immediate"`** (default) — call the other worker and wait for its answer. Good for quick calls where you need the result right now.
- **`mode="background"`** — put the request on a queue and get back a `BackgroundJob` object immediately. Good for long-running work (e.g. a 5-minute video generation) where you don't want to hold a connection open. You can later check the job's status, or register callbacks via `on_complete=` (run when the job finishes) and `on_store_result=` (run on the output before it is stored — useful for uploading big binaries to S3 and storing only a URL).

### Getting the input/output types from a handle

The handle also lets you access the other worker's `Input` / `Output` classes so you can construct inputs in a type-safe way:

- `self.nsfw.api.Input(...)` — recommended. Editors and `mypy` understand the type.
- `self.nsfw.Input(...)` — shorter but type checkers see it as a plain `type`.

(api-doc-workerhandle)=
[**`frameworks.inference.WorkerHandle`**](api-doc-workerhandle)

A handle to call a worker from an orchestrator

- **`api -> WorkerT`** *(property)*

  You can use the .api object to access the Input and Output types.

- **`Input -> type`** *(property)*

  Alias for :class:`inference.WorkerHandle.api.Input`. The disadvantage with it is vscode/mypy cannot deduce its type.

- **`Output -> type`** *(property)*

  Alias for :class:`inference.WorkerHandle.api.Output`. The disadvantage with it is vscode/mypy cannot deduce its type.

- **`submit(input: Any, mode: Literal['immediate', 'background'] = 'immediate', *, background_config: BackgroundJobsConfig | None = None, on_complete: Callable[..., Any] | None = None, on_store_result: Callable[..., Any] | None = None) -> Any`**

  Request to run the worker. Background thread version.
When within the function :func:`inference.Worker.execute` you should call this function. These are cases
that run in background threads.

- **`submit_from_el(input: Any, mode: Literal['immediate', 'background'] = 'immediate', *, background_config: BackgroundJobsConfig | None = None, on_complete: Callable[..., Any] | None = None, on_store_result: Callable[..., Any] | None = None) -> Any`**

  Submit event loop: request to run the worker. Event loop version.
When within the async variant of the function :func:`inference.Worker.execute` or within `inference.Webapp`
routes you should call this function. These are cases that run in the event loop thread.

## `inference.builtin_webapps`

Framework-provided webapps that you can mount alongside your own to get common
infrastructure endpoints for free. Each is an independent `WebApp.bind()` instance —
include only what you need.

| Webapp | Endpoints | Purpose |
|--------|-----------|---------|
| `jobs_app` | `GET /jobs/result/{id}`, `PUT /jobs/cancel/{id}` | Background job polling and cancellation |
| `storage_app` | `POST /v2/storage/{image,document,video,audio,block/*}` | File upload to temporary storage |

### Mounting builtin webapps

In managed services, add them to `roots` in the BUILD file. The build system
auto-discovers all `WebApp.bind()` instances and populates the http_server's
`serves` list in the deployment chart:

```python
inference_application(
    name = "my_service",
    roots = [
        "my.webapps.app.app",
        "frameworks.inference.builtin_webapps.jobs_app",
        "frameworks.inference.builtin_webapps.storage_app",
    ],
    deps = [...],
)
```

For local development, pass them as additional arguments to `initialize` or `serve`:

```python
from frameworks import inference

universe = inference.initialize(
    my_app,
    inference.builtin_webapps.jobs_app,
    inference.builtin_webapps.storage_app,
)
```

### Jobs webapp response contract

When polling `GET /jobs/result/{id}`:

- **In-progress**: HTTP 200, header `X-Task-Status: IN_PROGRESS`, body with `status`, `links`, `progress`
- **Succeeded**: HTTP 200, header `X-Task-Status: COMPLETED`, body is the worker output (same as a sync response)
- **Failed**: HTTP 500, header `X-Task-Status: FAILED`, body with `error_code` and `message`
- **Cancelled/Timeout**: HTTP 410 with error JSON
- **Unknown**: HTTP 404

When cancelling `PUT /jobs/cancel/{id}`:

- **Success**: HTTP 200
- **Unknown or terminal**: HTTP 404

### Storage webapp endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v2/storage/image` | Upload an image (JPEG, PNG, WebP, JXL, TIFF) |
| POST | `/v2/storage/document` | Upload a document (PDF, plain text) |
| POST | `/v2/storage/video` | Upload a video (MP4, MOV, WebM) |
| POST | `/v2/storage/audio` | Upload audio (MP3, WAV, FLAC, AAC, OGG, etc.) |
| POST | `/v2/storage/block/init` | Initiate a chunked block upload |
| POST | `/v2/storage/block/complete` | Complete a block upload |

All upload endpoints accept the file as the raw request body with the appropriate
`Content-Type` header. Response is `{"images": [{"id": "..."}]}` for images or
`{"assets": [{"id": "..."}]}` for other types. The returned `id` is a UUID
referencing the file in temporary storage, usable as input to worker requests.

## Request / Response types

These types can be used in addition to JSON types to define request and response types for workers.

```{eval-rst}
.. py:module:: frameworks.inference
   :no-index:

   .. py:class:: Tensor
     :no-index:

      A tensor type that can be used in worker inputs and outputs. When ``torch`` is installed, this
      is exactly ``torch.Tensor`` (see https://docs.pytorch.org/docs/stable/tensors.html). When ``torch``
      is NOT installed, it is a same-named stub class that can still be referenced in pydantic field
      annotations but raises ``"Did you forget to install torch?"`` if you try to instantiate an
      Input/Output that contains it.

      **Always use this alias instead of ``torch.Tensor`` directly** when defining worker APIs. Torch
      is a heavy optional dependency (~1GB+, CUDA wheels, slow install), and worker API modules — the
      ``__init__.py`` files that declare ``Input`` / ``Output`` / ``bind()`` — are imported by lots of
      code that does not intend to run the worker, for example:

      * the deploy-manifest generator (``inference_json_gen.py``) which imports every webapp module
        during a bazel build to walk the dependency graph,
      * other workers that declare ``depends_on.worker_handle(your_worker)`` to get typed
        ``Input`` / ``Output`` for submission,
      * SDK clients in downstream services that want typed request/response models,
      * Sphinx doc builds, CI lint jobs, and type-checkers.

      If you wrote ``torch.Tensor`` directly, every one of those paths would need torch installed just
      to read the schema. With ``inference.Tensor``, the module imports cleanly without torch; torch
      is only required on the path that actually instantiates tensors (i.e. the worker pod at runtime).

      In short: the alias saves you at **import time**, not at **call time**. Pods that run workers
      still need torch installed.
```

```{eval-rst}
.. py:module:: frameworks.inference
   :no-index:

   .. py:class:: Binary
     :no-index:

      Use ``inference.Binary`` for any field in your ``Input`` / ``Output`` that holds **raw bytes** —
      an image, an audio clip, a PDF, a model weight file, anything that isn't text or numbers.

      **Why not just use Python's ``bytes`` type?**

      Workers talk over the network, and the default way to send request/response data is as JSON —
      a text format. You cannot put raw bytes into text, so if you declared ``image: bytes``, the
      framework would have to convert those bytes to a text-safe encoding (base64) before sending.
      That has two costs:

      * base64 makes the payload ~33% bigger,
      * both sides have to spend CPU encoding and decoding it.

      For a tiny byte string that's fine. For a 5 MB image or a 50 MB tensor, it becomes the dominant
      cost of the call.

      ``inference.Binary`` tells the framework "this field is bytes — do not try to stuff them into
      the JSON." The framework then sends the JSON (small, no bytes in it) and the raw bytes
      **side-by-side in the same HTTP request**, the way a file upload works in a web form. On the
      other end, the framework puts them back together and hands your worker the reconstructed
      ``Binary``. You never see the transport details — you just work with a normal Python object.

      A small but important nuance: yes, the bytes themselves still travel over the network —
      there is no magic compression. The win is not in sending less *information*, but in how it is
      packaged. With base64 in JSON you send ~33% *more* bytes than you need (base64 inflation), plus
      both sides spend CPU on encode/decode and the JSON parser has to walk the entire base64 string.
      With ``inference.Binary`` the bytes go over as-is, with tiny multipart framing around them, and
      the JSON body stays small and fast to parse. For small payloads the difference is negligible;
      for MB-scale payloads (images, tensors, video) it dominates the cost of the call.

      Two fields:

      * ``value: bytes`` — the actual byte content.
      * ``metadata: dict[str, Any]`` — any JSON-safe extra info you want to carry along (file format,
        dimensions, mime type, etc.). Optional; defaults to ``{}``.

      Minimal example:

      .. code-block:: python

         class MyWorker(inference.Worker):
             class Input(pydantic.BaseModel):
                 image: inference.Binary     # 5 MB PNG, for example

             class Output(pydantic.BaseModel):
                 result: inference.Binary    # processed image, also raw bytes

         # Constructing one (e.g. inside execute):
         out = inference.Binary(
             value=png_bytes,                      # the actual bytes
             metadata={"format": "png", "w": 1024, "h": 1024},  # optional tagging
         )

      ``Binary`` is also the base for richer typed binaries the framework knows about (``Tensor``,
      plus image/video types used internally). They all get the same efficient transport for free.

      Rule of thumb: **if a field carries more than a few hundred bytes and isn't human-readable,
      make it an ``inference.Binary``.**
```


## Running the inference stack

### Locally, all in one process (prototyping)

`inference.initialize(...)` runs **the entire stack in a single Python process**: your web apps, every worker they depend on, the background event loop for async code, the job store, and the session manager. There is no redis, no separate worker pods, no HTTP between components — worker-to-worker calls happen as in-process function calls through `LocalRunHandle`.

What you get back is an `inference.types.InferenceUniverse`, which exposes:

- `universe.fastapi` — the mounted `FastAPI` app with all web-app endpoints. Pass this to `uvicorn.run(...)` or to an HTTP test client (`TestClient`, `httpx`) to drive the web apps.
- `universe.w.<worker_short_name>` — direct handles to each worker in the universe. `universe.w.nsfw_v1.submit(...)` calls the worker without going through HTTP — handy for notebooks and unit tests.

Use this mode when you want to:

- **Iterate quickly**: no process boot, no redis bring-up, restart = re-import in the REPL.
- **Debug**: everything is in one process, so you can set breakpoints in workers and webapp endpoints and hit them from a single debugger session.
- **Write tests**: construct the universe, make HTTP requests against `universe.fastapi` or call workers via `universe.w.*`, tear down.

It is **not suitable for production**:

- No process isolation — a crashing worker takes down the whole universe.
- No GPU process isolation — all workers share the same CUDA context. Multi-GPU works (the framework still assigns `devices` per worker from `GpuRequirement`), but if you need proper isolation, use `inference.serve` instead.
- No background queue durability — the job store is in-memory (`LocalJobStore`); background jobs disappear on restart.

(api-doc-initialize)=
[**`frameworks.inference.initialize(*args, configs: Mapping[str, Mapping[str, Any] | BaseModel] | None = None) -> InferenceUniverse`**](api-doc-initialize)

Initialize the inference universe

(api-doc-serve)=
[**`frameworks.inference.serve(*args, manage_redis: ManagedRedis | None = None, http_port: int | None = None, work_dir: Path | None = None, configs: dict[str, dict[str, Any] | BaseModel] | None = None) -> None`**](api-doc-serve)

Serve workers and web apps on separate processes while communicating similar to how they would on cloud

(api-doc-inferenceuniverse)=
[**`frameworks.inference.InferenceUniverse`**](api-doc-inferenceuniverse)

- **`fastapi -> FastAPI`** *(property)*

  A fastapi app that has all the endpoints that the user provided as web app.

- **`w -> Workers`** *(property)*

  Use this to access all the model workers in the universe.

- **`teardown() -> None`**

  Clean up resources. Stops the background event loop.


### Locally, on separate processes (cloud-like)

`inference.serve(...)` runs **each worker in its own OS subprocess** and **each webapp in its own process**, with real HTTP and real redis between them — the same wiring your code will use in production, just all on your laptop.

**What "on separate processes" gives you**

`initialize()` puts everything in one Python process — shared memory, one CUDA context, one event loop; if one worker crashes, the whole universe goes down. `serve()` starts a fresh OS subprocess per worker (and per webapp). They get their own Python interpreter, their own RAM, their own `CUDA_VISIBLE_DEVICES`. If one crashes, the supervisor restarts only that process.

**What "communicating similar to how they would on cloud" means**

In production:

- Users hit your webapp over **HTTP** on port 8000 of a k8s Service.
- The webapp dispatches work to a worker by putting a task on a **redis queue**; the worker pod is consuming from that queue.
- Worker-to-worker calls also go through that redis queue (via `RedisWorkerHandle` — see `inference.depends_on`).

`serve()` reproduces all three on your machine:

- Starts an HTTP server (uvicorn) on `localhost:8000` (or a port you pass via `http_port`).
- Starts a redis instance — either one it manages for you, or it connects to one you point it at (`manage_redis=...`).
- Workers pull tasks from redis queues exactly the way they would in prod.

So the **code path** exercised when you run `serve()` is the same as the code path exercised when your service is deployed. The transport layers (`RedisWorkerHandle`, `HttpWorkerHandle`, FastAPI, the task submitter) are the real thing, not mocks.

**Where it sits on the spectrum**

|  | `initialize()` — prototyping | `serve()` — cloud-like local | `python -m frameworks.inference` — prod pods |
|---|---|---|---|
| Where | your laptop, 1 process | your laptop, N processes | k8s cluster, N pods |
| Worker → worker | in-process function calls | redis queue | redis queue |
| Webapp front door | FastAPI app you mount yourself | real HTTP on localhost | real HTTP through k8s Service |
| Redis | none | local (managed) | managed redis cluster |
| Isolation | none | process-level (OS) | process + container + k8s |
| GPU isolation | shared CUDA context | per-process `CUDA_VISIBLE_DEVICES` | per-pod GPU allocation |
| Restart on crash | no (takes everything down) | yes (supervisor restarts one) | yes (k8s restarts the pod) |

`serve()` is the middle rung — cheap to run (it's still your laptop), but exercises the **same runtime architecture** as prod.

[**`frameworks.inference.serve(*args, *, manage_redis: ManagedRedis | None = None, http_port: int | None = None, work_dir: Path | None = None, configs: dict[str, dict[str, Any] | BaseModel] | None = None) -> None`**](api-doc-serve)

Serve workers and web apps on separate processes while communicating similar to how they would on cloud

(api-doc-managedredis)=
[**`frameworks.inference.ManagedRedis`**](api-doc-managedredis)

If user wants to use inference.serve(...) to lauch redis, then they can pass a dictionary,
ManagedRedis, to configure it. Note that this is just a TypedDict, you don't need to import
the type.


### Locally, with some workers called remotely (mixed)

Sometimes you want to iterate locally, but one worker in your graph needs a GPU (or a set of GPUs) your laptop does not have — an image generator, a large video model, a big LLM. Rather than running the whole stack locally (impossible) or the whole stack in the cloud (slow to iterate), you run *most* of it locally and point *that one worker* at a remote instance that is already running.

This is configured via the framework config, under `dev.remote_execution`. When set, the framework replaces the matching workers' handles with an `HttpWorkerHandle` that POSTs to a remote endpoint instead of the usual `RedisWorkerHandle` / in-process call.

**Minimal example — delegate a single worker to a remote HTTP server**

```python
inference.initialize(
    my_webapp,
    configs={
        "frameworks.inference.default_config": {
            "dev": {
                "remote_execution": {
                    "select": ("include", ["services.imaging.flux.flux_v1"]),  # which workers go remote
                    "default_endpoint": "http://bigbox.internal:8000",         # where to send them
                },
            },
        },
    },
)
```

`select` has two forms:

- `("include", [refs])` — *only* the listed refs go remote; everything else runs locally.
- `("exclude", [refs])` — the listed refs stay local; everything else goes remote.

For per-worker endpoints (different workers on different servers), use `endpoint_by_worker: {ref: url}` alongside `default_endpoint`.

**Works with both local modes**

The same config works with `inference.initialize(...)` and `inference.serve(...)` — the `RemoteQuery` check runs in both paths. Use `initialize` for fastest iteration; use `serve` if you want the *rest* of the stack to also run cloud-like (separate processes, real redis).

**Caveat: immediate mode only**

`HttpWorkerHandle` currently only supports `mode="immediate"` for submissions. Calling a remote worker with `mode="background"` raises `NotImplementedError("Background mode over HTTP is not implemented yet")` (tracked as FFP-76371 in the code). If your local-to-remote call needs background execution, you have to run that worker locally for now.

**End-to-end example in the repo**

`frameworks/inference/serve/samples/a_basic/__test__.py::test_remote_execution` shows the pattern: start a uvicorn server exposing the heavy worker, then bring up a second universe that calls it over HTTP via `remote_execution`.

### The `python -m frameworks.inference` CLI

These are the commands that launch a single supervised process. **They are also how each process inside a deployed container image is started** — the k8s pods (worker pods, webapp pods, watchdog, dashboard) all run one of these as their entrypoint. Whether you are running locally or in production, the same CLI is the entry into the inference framework.

Use `python -m frameworks.inference --help` to see the full arguments; here we just list the subcommands and their description.

```
python -m frameworks.inference --help

Commands:
  dashboard  Launch a single supervisor that has process for the dashboard http server.
  dev        Development commands that are not really used in production.
  watchdog   Launch a single supervisor with the job watchdog process.
  webapps    Launch a single supervisor that has http server process that serves the passed web apps (comma separated).
  workers    Launch a single supervisor that has processes for distinct passed workers (comma separated).
```

---

```
python -m frameworks.inference dev --help

Commands:
  dist-serve     Launch all components in separate processes.
  local-serve    Launch all components in a single process.
  redis-cluster  Start a redis cluster.
```

### Deploying to cloud

If a user wants to deploy things themselves, they need to setup the pods shown below manually.
If they use the managed service ecosystem (see [colligo managed_services](https://docs.ai.corp.adobe.com/managed_services/README.html)), the [deployment API](/platforms/inference/aidoc/deployment/index.md) will do this out of the box.

```sh
# The pod serving the web apps will run this
# argument 1: comma separated list of all web app objects
# --config: a config file (the k8s chart typically mounts this as config)
# --http-port: port the http server binds to
python -m frameworks.inference webapps services.firefly.video.workers.imaging.imaging_api,... --config /path/to/config --http-port <...>
 
# The pod serving a worker will run this
# argument 1: comma separated list of distinct worker objects
# --config: a config file (the k8s chart typically mounts this as config)
python -m frameworks.inference workers services.firefly.video.workers.imaging_api.imaging_api,... --config /path/to/config
 
# The pod running the job watchdog (monitors background job queue health)
# argument 1: a config file with background.watchdog_queues populated
python -m frameworks.inference watchdog --config /path/to/config

# The pod serving the dist tracing dashboard
# argument 1: comma separated list of all web app objects
# argument 2: a config file (the k8s chart typically to mounts this as config)
python -m frameworks.inference dashboard --config /path/to/config
 
# If a user wants to use an unreliable but quick redis server, they can do
python -m frameworks.inference dev redis-cluster --config /path/to/config
```

The `workers` CLI argument is a comma-separated list of distinct worker refs. To launch multiple
replicas of the same worker in one supervisor, set `<worker_ref>.serve_config.num_processes` in the
runtime config.

## `inference.types`

These are types that you should not construct directly, but are useful as type hints when overriding base functions of interfaces. Do not instantiate these objects directly.

(api-doc-backgroundjob)=
[**`frameworks.inference.BackgroundJob`**](api-doc-backgroundjob)
Handle returned by ``submit(mode="background")``.
Wrapping the URN in a model allows adding fields (e.g. queue position,
estimated wait) in the future without breaking callers.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `urn` | `str` | *required* |  |
(api-doc-jobresult)=
[**`frameworks.inference.JobResult`**](api-doc-jobresult)
Result of querying a background job.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `status` | `Literal['accepted', 'in_progress', 'succeeded', 'failed', 'cancelled', 'timeout']` | *required* |  |
| `output` | Any \\| None | `None` |  |
| `error` | Any \\| None | `None` |  |
| `progress` | float \\| None | `None` |  |
| `intermediate_results` | dict[str, Any] \\| None | `None` |  |
(api-doc-oncompleteinfo)=
[**`frameworks.inference.OnCompleteInfo`**](api-doc-oncompleteinfo)
Payload passed to the ``on_complete`` callback after a background job
reaches a terminal state.
Exactly one of ``output`` / ``error`` is set.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `input` | `Any` | *required* |  |
| `output` | Any \\| None | `None` |  |
| `error` | BaseException \\| None | `None` |  |
| `reason` | Literal['succeeded', 'failed', 'cancelled', 'timeout'] \\| None | `None` |  |

(api-doc-executekit)=
[**`frameworks.inference.ExecuteKit`**](api-doc-executekit)

Interface for context-dependent operations available to workers and webapp endpoints.

- **`async_endpoint_url -> str`** *(property)*

  The deployment's externally-reachable base URL for constructing
absolute background job links (e.g. ``https://firefly-dev-eso851234.adobe.io``).

- **`cancel_background_job(job_id: str) -> bool`**

  Cancel a running or queued background job.

- **`get_completed_response(job_id: str) -> dict[str, Any] | None`**

  Return the stored response payload for a completed job.

- **`query_background_job(job_id: str) -> JobResult | None`**

  Query the status and result of a background job.

- **`set_background_progress(progress: float) -> None`**

  Report progress for the currently executing background job.

- **`set_background_intermediate_results(intermediate_results: dict[str, Any]) -> None`**

  Report partial/intermediate results for the currently executing background job.


## Configuration

### Inference framework's configuration

(api-doc-inferenceframeworkconfig)=
[**`frameworks.inference.InferenceFrameworkConfig`**](api-doc-inferenceframeworkconfig)

Default configuration for the inference framework.

(api-doc-supervisor)=
[**`frameworks.inference.InferenceFrameworkConfig.Supervisor`**](api-doc-supervisor)
Config for supervisor(s) that is shared among all of them.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `status_port` | `int` | `8001` | The port for the status server (k8s probes). |
| `metrics_port` | `int` | `8002` | The port for the metrics server (Prometheus scraper). |
(api-doc-redis)=
[**`frameworks.inference.InferenceFrameworkConfig.Redis`**](api-doc-redis)
Config for connecting to Redis.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `host` | `str` | `'127.0.0.1'` | Redis host. |
| `port` | `int` | `6379` | Redis port. |
| `namespace` | `str` | `'default'` | Prefix for Redis keys so different apps can share one instance. |
| `username` | str \\| None | `None` | Redis username. |
| `password` | str \\| None | `None` | Redis password. |
(api-doc-s3)=
[**`frameworks.inference.InferenceFrameworkConfig.S3`**](api-doc-s3)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `default_profile` | Profile \\| None | `None` | Default profile to use for s3. If not passed, will query the default from vault. |
| `profiles` | `dict[str, Profile]` | `{}` | The profiles (buckets can reference them). |
| `buckets` | `dict[str, Bucket]` | `{}` | configuration for connecting to the buckets |
(api-doc-development)=
[**`frameworks.inference.InferenceFrameworkConfig.Development`**](api-doc-development)
Configuration for local development, not relevant to production.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `remote_execution` | RemoteExecution \\| None | `None` | Delegate execution of selected workers to a remote endpoint. |
(api-doc-metrics)=
[**`frameworks.inference.InferenceFrameworkConfig.Metrics`**](api-doc-metrics)
Configuration for metrics reporting.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `app_name` | `str` | `'FireflyBackend'` | Application name used as a label in metrics (Prometheus app_name label). |
(api-doc-newrelic)=
[**`frameworks.inference.InferenceFrameworkConfig.Newrelic`**](api-doc-newrelic)
Configuration for NewRelic metric reporting.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `app_name` | `str` | `'FireflyBackend'` | Application name reported to NewRelic (the NewRelic `app_name` label). |
| `license_key` | str \\| None | `None` | NewRelic license/API key. v3 reads nothing from the env by default, so the chart sets this from a vault secret via `{_env: NEWRELIC_API_KEY}`; it is then propagated to the colligo metrics backend. |
(api-doc-background)=
[**`frameworks.inference.InferenceFrameworkConfig.Background`**](api-doc-background)
Ops/deployment-level configuration for background (resilient async) jobs.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `watchdog_cadence_s` | `int` | `60` | How often (seconds) the watchdog checks for abandoned jobs. |
| `watchdog_mark_and_terminate` | `bool` | `False` | Enable mark-and-terminate logic for unhealthy executors. |
| `watchdog_attempts_count` | `int` | `2` | Consecutive failed pings before marking an executor unhealthy. |
| `watchdog_queues` | `list[str]` | `[]` | Queue names for the watchdog to monitor. |
| `job_config` | `BackgroundJobsConfig` | `BackgroundJobsConfig()` | Deployment-level defaults for per-job config (timeouts, retries). |
| `concurrency_limiter` | ConcurrencyLimiter \\| None | `None` | Redis-backed concurrency limits for background job submission. |
| `backpressure` | Backpressure \\| None | `None` | Queue-level backpressure. Rejects with HTTP 429 when workers are overloaded. |
| `enable_multi_task_async_context` | `bool` | `False` | Allow multiple concurrent async tasks per session_id in the job manager. When disabled (default), only one task per session_id is allowed (legacy behavior). |
(api-doc-logging)=
[**`frameworks.inference.InferenceFrameworkConfig.Logging`**](api-doc-logging)
Configuration for logging behavior.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `formatter` | `FormatterType` | `'default'` | Log format: 'default' (text), 'json' (structured), or 'splunk_text'. |
(api-doc-experimentalconfig)=
[**`frameworks.inference.InferenceFrameworkConfig.ExperimentalConfig`**](api-doc-experimentalconfig)
Experimental settings that may change or be removed in future versions.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enable_worker_warming` | `bool` | `False` | Enable the worker warming feature (warm API endpoint and metrics reporter). Required for scale-to-zero (KEDA) to work correctly, as it exposes the colligo_worker_warm_trigger metric that enables pre-scaling workers before actual load arrives. |
| `enable_queue_length_metrics_reporter` | `bool` | `False` | Enable the periodic queue length metrics reporter. When enabled, each process periodically reports queue length to keep the colligo_last_know_exact_queue_length metric from going stale when traffic stops. |
| `keda_enabled_workers` | `list[str]` | `[]` | Short names of workers that have KEDA scale-to-zero enabled. Used by the http_server's warmup UI/state endpoint to filter out workers that aren't actually warmable (e.g. CPU pipelines deployed alongside GPU workers). Set by the deployment chart on Ethos. Empty for local dev defaults to treating every deployed worker as KEDA-enabled. |
(api-doc-debugconfig)=
[**`frameworks.inference.InferenceFrameworkConfig.DebugConfig`**](api-doc-debugconfig)
Debug and development settings. These are intended for non-production use only.
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `return_stack_trace` | `bool` | `False` | Include the Python stack trace in error responses. Intended for dev/stage only; do not enable in production. TODO: add a workflow check for it |
| `enable_cors_headers` | `bool` | `False` | Emit permissive CORS headers from the HTTP server so debug tools (e.g. the built-in debug UI, local browser frontends) can call the inference service from a different origin. This is a debug/local-development convenience; production ingress should handle CORS at the gateway level. |


### Register your own configuration

(api-doc-registerdefaultconfig)=
[**`frameworks.inference.RegisterDefaultConfig`**](api-doc-registerdefaultconfig)

This class provides a way to define and manage default configuration values on a
**per-module basis**, while keeping things **explicit** and **modular**.

- **`value -> T`** *(property)*

  Access the value of the config. We recommend to only use this as default value


### Environment variable substitution in config

For security reasons, secrets often cannot be written to files on disk and must be kept as
environment variables. To reference env vars in `runtime_config`, use `{_env: ENV_VAR_NAME}`:

```yaml
runtime_config:
  my_app.default_config:
    api_key: {_env: MY_API_KEY}
    azure_endpoint: {_env: AZURE_ENDPOINT}
```

At startup, the framework resolves `{_env: VAR}` → `os.getenv("VAR")` before Pydantic
validation. Works with any `pydantic.BaseModel` — no special base class needed.

- Resolved values are always **strings**. Pydantic coerces where possible (e.g. `"6379"` → `int`).
  For non-string types that Pydantic cannot coerce from a string (e.g. `list`, `dict`), add a
  Pydantic `@field_validator` on your Config to handle the conversion.
- Missing env var → key is dropped → Pydantic applies normal required/optional rules.
- Resolution is recursive into nested dicts.



## Migration API

```{eval-rst}
.. include:: ../migration/README.md
   :parser: myst_parser.sphinx_
```
