## hs
#### 1.
typer allows you to register a python function as a command line.
So instead of having to import the function into a python shell
and then call it normal python way, you can do it from CLI with
```
python -m modeule_name command
```
#### 2.
glimrelay takes this a step further, so that you don't even have to run the pyhon,
pyproject.toml
```
glimrelay = "glimmer_queue.start_server:app"
```
is like you have an installed command glimrelay that essentially runs the gRPC server.


#### 3.
The connection_string is just the url + username and password of the
database. You can also just set it as an env variable:
"GLIMMER_DB": "postgresql://glimmer:CbbHcArD8rS7DyIrKzdQtIT3@glimmer-test.cq0ijarroa7i.us-west-2.rds.amazonaws.com:5432/glimmer"


Look below for details on above:

## which server does python -m glimmer_queue.start_server serve
or glimrelay ...
start exactly?
That command starts the gRPC server.

- It launches the Typer CLI command `serve` in `glimmer_queue.start_server`, which:
  - Creates a gRPC server and registers `GlimmerQueueService` (the handlers for Handshake, DequeueShards, UpdateShard, QueryShard, QueryJob).
  - Binds insecure on [::]:50051 and starts serving.
  - Spins up an in-process `GlimmerClient` that polls the DB and feeds `DequeueShards`.

So workers connect to this process via a gRPC channel (e.g., `localhost:50051`) and call the service methods defined in the proto.




## What is typer?
app = typer.Typer()
@app.command()
def serve()

- Typer is a Python library for building CLIs from functions and type hints (built on Click). It turns your functions into commands, parses args, validates types, and generates help.

- In `start_server.py`, `app = typer.Typer()` creates a CLI app. The `@app.command()` decorator registers `serve` as a subcommand. Typer reads the function signature to define options:
```python
@app.command()
def serve(
    connection_string: str = typer.Option(None, help="SQLAlchemy connection string"),
    job_name: str = typer.Option(None, help="Job name"),
    debug: bool = typer.Option(False, help="Debug mode"),
):
    ...
```
- What happens at runtime:
  - When you run `python -m glimmer_queue.start_server serve --connection-string ... --job-name ...`, Typer parses the flags, converts them to the right types (`str`, `bool`) using the annotations, and calls `serve(...)`.
  - The bottom of the file calls `app()` under `if __name__ == "__main__":`, which starts the Typer app.
  - There’s also a console entry point in pyproject: `glimrelay = glimmer_queue.start_server:app`, so you can run `glimrelay serve ...` the same way.

- Why use Typer here:
  - You get `--help` and nice error messages for free.
  - Options and defaults are declared alongside code, so docs and behavior stay in sync.
  - No manual `argparse` boilerplate; type hints drive parsing/validation.


 What does glimrelay do?

 - It defines a console script entry point named glimrelay.
- When the package is installed, your Python toolchain generates an executable shim (e.g., ~/.venv/bin/glimrelay) that imports glimmer_queue.start_server and calls the callable named app.
- Since app is a Typer application, running glimrelay invokes the CLI (same as python -m glimmer_queue.start_server, but via an installed command).
- Practical use: run glimrelay --help or glimrelay serve --connection-string ... --job-name ....

What's the equivalent of glimrelay --job-name "$GLIMMER_JOB_NAME" ?

Use the module directly with the same Typer command:

```bash
python -m glimmer_queue.start_server serve --job-name "$GLIMMER_JOB_NAME"
```

If you need a DB URL (and haven’t set `GLIMMER_DB`), add:

```bash
python -m glimmer_queue.start_server serve --connection-string "$SQLALCHEMY_URL" --job-name "$GLIMMER_JOB_NAME"
```



## What is the connection_string that the server takes?
It’s a standard SQLAlchemy database URL (the DB your gRPC server uses). Examples:

- Postgres (psycopg v3)
  - No SSL:
    - postgresql+psycopg://myuser:mypassword@db-hostname:5432/mydb
  - With SSL:
    - postgresql+psycopg://myuser:mypassword@db-hostname:5432/mydb?sslmode=require
  - With env-var expansion (supported in our code):
    - postgresql+psycopg://${PGUSER}:${PGPASSWORD}@${PGHOST}:${PGPORT}/${PGDATABASE}

- SQLite
  - File:
    - sqlite:////absolute/path/to/local.db
  - In-memory:
    - sqlite://

Notes:
- You can pass it via the flag:
  - python -m glimmer_queue.start_server serve --connection-string "postgresql+psycopg://user:pass@host:5432/db" --job-name JOB
- Or set env and omit the flag (the app reads `settings.db` with GLIMMER_ prefix):
  - export GLIMMER_DB="postgresql+psycopg://user:pass@host:5432/db"
  - python -m glimmer_queue.start_server serve --job-name JOB

- Pool sizing/timeouts are controlled via env (e.g., GLIMMER_DB_POOL_SIZE, GLIMMER_DB_MAX_OVERFLOW); SSL and driver options can go in the URL query.

this is an actual example:
"GLIMMER_DB": "postgresql://glimmer:CbbHcArD8rS7DyIrKzdQtIT3@glimmer-test.cq0ijarroa7i.us-west-2.rds.amazonaws.com:5432/glimmer"



## what is Dynaconf (from /glimmer_queue/config.py)
### Dynaconf (what it is)
- A Python configuration library that merges settings from multiple sources (env vars, files, defaults) with type-casting and layering.
- Lets you read config as attributes, e.g., `settings.db`, with environment-variable overrides.

### How it’s used here
- In `glimmer_queue/config.py`:
```python
from dynaconf import Dynaconf
settings = Dynaconf(envvar_prefix="GLIMMER")
```
- With `envvar_prefix="GLIMMER"`, any `GLIMMER_*` environment variable is exposed on `settings` without the prefix:
  - `GLIMMER_DB` → `settings.db`
  - `GLIMMER_LEASE_TIMEOUT_HOURS` → `settings.LEASE_TIMEOUT_HOURS`
  - `GLIMMER_ABANDONED_CLEANUP_HOURS` → `settings.ABANDONED_CLEANUP_HOURS`
- Code reads `settings.db` in `start_server.py` if `--connection-string` isn’t provided.

### Practical examples
- Set DB URL via env:
```bash
export GLIMMER_DB="postgresql+psycopg://user:pass@host:5432/db"
python -m glimmer_queue.start_server serve --job-name JOB
```
- Tune leases/cleanup:
```bash
export GLIMMER_LEASE_TIMEOUT_HOURS=2
export GLIMMER_LEASE_RENEWAL_INTERVAL_MINUTES=20
export GLIMMER_ABANDONED_CLEANUP_HOURS=6
```

### Behavior highlights
- Precedence: CLI options > environment variables (via Dynaconf) > code defaults.
- Types: Dynaconf will cast simple types when possible (e.g., “2” → int 2).
- Access: read anywhere with `from glimmer_queue.config import settings`.


## why do we have the dyconf but also a Settings class?
- settings = Dynaconf(...): the live config object. It reads GLIMMER_* environment variables and exposes them as attributes (e.g., GLIMMER_DB → settings.db). This is what the code actually uses at runtime.

- class Settings: a typed defaults sketch. It documents intended defaults (e.g., LEASE_TIMEOUT_HOURS=1) and provides type hints. It’s not wired into Dynaconf here (Dynaconf isn’t told to load from this class), so it mainly serves as human/IDE reference.

- Current usage pattern in code:
  - Read from env-backed settings with a literal fallback, e.g. getattr(settings, "LEASE_RENEWAL_INTERVAL_MINUTES", 30).
  - The literal fallbacks mirror the values in class Settings, but the class isn’t referenced directly.

- If you want the class to be the single source of defaults, you could change call sites to use Settings.<name> as the fallback:
  - getattr(settings, "LEASE_TIMEOUT_HOURS", Settings.LEASE_TIMEOUT_HOURS)
Or configure Dynaconf to load defaults from a file/object and drop the separate class.




## what's up with ThreadPoolExecutor in
server = grpc.server(futures.ThreadPoolExecutor(max_workers=128))
- Yes, that ThreadPoolExecutor is the gRPC server’s worker pool. Each incoming RPC is scheduled onto a worker thread to run the handler (e.g., Handshake, DequeueShards, UpdateShard, QueryShard). More workers = more concurrent RPCs can be processed; too few = requests queue; too many = contention.

- What the workers do here:
  - Run your handler code in `GlimmerQueueService`.
  - For UpdateShard/QueryShard they open a short‑lived SQLAlchemy Session and hit the DB (SELECT … FOR UPDATE SKIP LOCKED, updates).
  - For DequeueShards they call into the in‑process `GlimmerClient` (which itself has threads and DB access via `TaskQueue`).
  - Handshake/QueryJob are cheap but still occupy a worker briefly.

- Why increase max_workers 64 → 128:
  - To raise concurrency headroom for bursts of UpdateShard/Handshake/DequeueShards from many clients (reduces queueing latency).
  - Handlers are largely I/O‑bound (DB, gRPC I/O), so extra threads can progress while others wait on the DB/network (GIL isn’t a blocker here).
  - It better aligns with DB pool capacity so workers don’t stall waiting on a connection:
    - Defaults: `GLIMMER_DB_POOL_SIZE=64`, `GLIMMER_DB_MAX_OVERFLOW=64` → up to ~128 concurrent DB connections.
    - Server handlers open a per‑request Session; sizing workers to ≤ pool_size+max_overflow avoids connection starvation.
  - Matches test realities (e.g., 100 concurrent Handshakes) and many clients flushing UpdateShard in parallel.

- Tradeoffs to watch:
  - If workers >> DB pool, threads will block on connections; latency rises.
  - If workers are too high, you can increase context switching and amplify DB lock contention.
  - Tune together: max_workers, DB pool (GLIMMER_DB_POOL_SIZE/GLIMMER_DB_MAX_OVERFLOW), and gRPC client concurrency.



## what does this function do?
def db_session_maker():
        return session_from_db_path(connection_string)


- It’s a tiny factory that returns a SQLAlchemy session factory bound to the given DB URL.
```python
def db_session_maker():
    return session_from_db_path(connection_string)
```
- Under the hood, `session_from_db_path`:
  - Expands env vars in the URL, creates the Engine and a `scoped_session(sessionmaker(...))`.
  - Calls `Base.metadata.create_all(engine)` once.
  - Applies Postgres sane defaults on connect (statement_timeout, lock_timeout, idle_in_transaction timeout).
  - Honors pool knobs via env (e.g., `GLIMMER_DB_POOL_SIZE`, `GLIMMER_DB_MAX_OVERFLOW`, `GLIMMER_DB_POOL_PRE_PING`).

Why it’s useful
- Per-request sessions: call sites get a fresh, short‑lived `Session` each time, which helps keep transactions short and avoids cross‑request state.
- Pool reuse/thread safety: under `scoped_session`, each thread gets its own `Session`, backed by the shared pool.
- Testability/decoupling: pass a callable (factory) instead of a concrete `Session`; consumers don’t need to know the DB URL or engine wiring.

Where it’s used
- In debug seeding:
  - `session = db_session_maker()` → then create/drop/populate a job.
- In the in‑process scheduler client:
  - `client = GlimmerClient(db_session_maker, job_name)`; the client uses the factory to open/close sessions in its loops.
- In the gRPC service:
  - `service = GlimmerQueueService(db_session_maker, client)`; handlers do `session = self.session_maker()` per request (`UpdateShard`, `QueryShard`) to run short transactions.



## More details on GlimmerClient and GlimmerQueueService

- GlimmerClient: in-process scheduler.
  - Polls the DB via `TaskQueue` to lease shards and pushes them into an internal queue.
  - Exposes `dequeue_batch()` for the service to hand shards to external workers.
  - Batches `ack`/`nack` via `CachedAcker`, runs maintenance loops (`erase_finished_shards`, `erase_old_shards`, `erase_abandoned_shards`, `renew_lease`).
  - `client_counter = HeartbeatTracker()` lets it adjust backpressure based on active clients.
  - `client.start()` launches its background threads (poll loop + maintenance loop).

- GlimmerQueueService: gRPC handler implementation.
  - Implements proto methods by delegating to the client/DB:
    - `Handshake` records heartbeats.
    - `QueryJob` returns `row_group_size`.
    - `DequeueShards` pulls from `client.dequeue_batch()` and serializes shards.
    - `UpdateShard` uses a per-request DB `Session`, merges succeeded/failed bitmaps into the `Task`, and returns shard state.
    - `QueryShard` returns current state for a given row group.

- glimmer_queue_pb2_grpc.add_GlimmerQueueServicer_to_server(glimmer_queue_service, server):
  - Registers your `GlimmerQueueService` instance with the gRPC server (generated glue).
  - After this, incoming RPCs on that server are routed to the corresponding methods on your service instance.