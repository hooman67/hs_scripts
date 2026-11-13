Glimmer Queue overview
=======================

HS summary
--------------------
0.Quick mental model
  * One server process:
    * In-process `GlimmerClient` (leases from DB, buffers shards).
    * gRPC `GlimmerQueueService` (hands out shards; updates HeartbeatTracker on Handshake).
  * Many external worker processes:
    * Create a channel+stub (or use `GlimmerThinClient`), call `Handshake(...)`, then `DequeueShards`/`UpdateShard`.
    * Each unique handshake id increases the live client count used to scale buffering.


1.glimrelay, or glimmer_queue.start_server is where things start.
  * It defines the factory for db engines and sessions. called db_session_maker
  (see short transactions for why)
  * It creates GlimmerClient(db_session_maker, job_name) and starts it
  * It creates GlimmerQueueService(db_session_maker, client) and adds it to the server

  -     Mental Model
        - GlimmerQueService is a gRPC server (allows others to call its methods) it runs
        on any machine that's running glimmer.
        - It owns one GlimmerClient that it uses to communicate to the RDS.
        - Each glimmer.inference worker, has one GlimmerThinClient that talks to
        GlimmerQueueService using gRPC.
        - GlimmerThinClient fetches work, and reports progress.

2.GlimmerQueueService is jut the implementation of the gRPC handler methods.

3.GlimmerClient: runs inside the same OS process as gRPC server (GlimmerQueueService).
It runs a poll loop that leases shards from db and passes exposes to the GlimmerQueueService
so that it can pass to workers. It also runs a check/maintain loop that (`erase_finished_shards`, `erase_old_shards`, `erase_abandoned_shards`, `renew_lease`).
* Look at notes_on_client.md for details.
  -     Hardcoded numbers
        - we make 1 thread running the poll loop only
        - we make 1 thread runnign the check/maintain loop only
        - on each poll, we request 32 shards (i.e. 32 TaskHandles)
        - in poll loop, group_size = 2 This is the granularity in which shards are
        split: e.g., 2 means that each client gets 2 shards per request.
        - The poll loop sleeps (we call this queue is dormant) if there is two much pressure. That is if out q size is
        bigger than qsize or owned_shards size > owned_shards length. This limits how much we “prefetch” and how much we allow “in flight” at once:
        - qsize (out queue) = how many 2‑shard chunks are buffered for workers to grab. max(8, 4 * #connected_workers). So if we have 10 workers we allows up to 40 chunks (= 80 shards) in the out q.
        - owned_shards_len = how many shards we’ve handed out but haven’t seen completed/pruned yet. Max(16, 4x #connected_workers). So for 10 workers we also allow 40 chunks (80 shards) in the owned_shards q.

4. GlimmerThinClient: is an **external worker client** that connects to the gRPC server to fetch work and report progress. It's called "thin" because it doesn't manage the database directly - it just talks to the server via gRPC.
  - **Async Progress Reporting**: Acks/nacks happen in background threads via `AsyncProxy`
  - **Batched Updates**: `Tracker` accumulates progress and flushes periodically to reduce DB load
  - **Resilient Iteration**: If `dequeue()` fails, returns `[]` to continue looping
  - **Clean Shutdown**: `finally` block ensures all pending acks are flushed

Note:
- HeartbeatTracker
  - Yes: service.Handshake(client_identifier) records a timestamp per unique id; count() is the number of distinct client ids seen.
  - It does NOT decrement on disconnect; it’s a simple “seen” counter with last-seen timestamps.

- Who calls Handshake?
  - External workers (e.g., `GlimmerThinClient`) call `Handshake` when they connect. Example: `scripts/stress-test.py` does `thin_client.handshake("good_client")`.
  - The in-process `GlimmerClient` does not call `Handshake`. There is one `GlimmerClient` per `GlimmerQueueService` (correct).

- What is client_counter used for in GlimmerClient?
  - It’s the same `HeartbeatTracker` instance (wired in start_server) that the service updates. The `GlimmerClient` reads `client_counter.count()` to scale its internal backpressure thresholds.
  - “10 workers connected (client_counter.count() = 10)” means 10 external gRPC clients (e.g., ThinClients / your worker processes) have handshaken.

- Why this matters
  - More workers → allow more queued chunks and more owned shards before backpressure kicks in.
  - Few workers → keep buffers small to avoid hoarding.







Overview
----------------------------
Here’s the high‑level map you need first — what runs where, how the pieces talk, and the rules that keep the system safe and fast.

### What glimmer_queue is
- A sharded task queue backed by Postgres (via SQLAlchemy 2.x).
- Exposes a gRPC service so workers can fetch shards and report progress.
- Optimized for concurrency with leasing, SKIP LOCKED, short transactions, and caching.


Key components (where to look)
----------------------------
- RPC schema: `src/glimmer_queue/protos/glimmer_queue.proto`
- Server entry: `src/glimmer_queue/start_server.py`
- gRPC handlers: `src/glimmer_queue/server.py`
- Queue/DB logic: `src/glimmer_queue/task_queue.py`
- Data model: `src/glimmer_queue/models.py`
- Clients:
  - “Thin” gRPC worker: `src/glimmer_queue/client.py` (`GlimmerThinClient`, `Tracker`)
  - Internal scheduler client (runs inside the server): `GlimmerClient` (same file)
- Engine/pool/timeouts: `src/glimmer_queue/utils.py`
- Logging: `src/glimmer_queue/logging_config.py`
- Config parameters and env variables: `src/glimmer_queue/config.py`



System topology
---------------
```text
[External Workers] --gRPC--> [GlimmerQueueService] --(SQLAlchemy)--> [Postgres]
          ^                         |
          |                         | uses in-process scheduler:
          |                         v
   Tracker + ThinClient     GlimmerClient + TaskQueue
   (acks/nacks/flushes)     (poll DB, lease shards, feed server)
```

```
[External Worker Process]
         |
         v
[GlimmerThinClient] --gRPC--> [GlimmerQueueService] --SQLAlchemy--> [Postgres]
         |                              |
         |                              |
    [Tracker] <--UpdateShard-- [GlimmerClient] (in-process scheduler)
    [AsyncProxy]                      |
    (thread pool)                     v
                               [TaskQueue] (DB operations)
```


### Clients (two flavors)
- Server‑side `GlimmerClient`:
  - Schedules: polls DB, leases shards, feeds `DequeueShards`.
  - Background “maintenance”: erase finished shards (from local ownership), renew leases, clean abandoned and old shards.
- Thin worker (`GlimmerThinClient`) + `Tracker`:
  - Tracks local acks/nacks per row group with roaring bitmaps.
  - Partial flush logic triggers when enough new rows accumulated; avoids duplicate flushes by hashing payload.




RPC surface (protos) (what workers call)
--------------------
- Handshake(client_identifier) → ok (used for client counts/heartbeats)
- QueryJob() → {row_group_size}
- DequeueShards() → either is_empty or list of shards: {row_group, min_ix, max_ix}
- UpdateShard({row_group, succeeded, failed, all_succeeded}) → {state}
- QueryShard({row_group, include_sets}) → QueryShardResponse{row_group,min_ix,max_ix,state,succeeded?,failed?}


Hot paths (how work flows)
--------------------------
### Hot path: Acquire work (leasing):
- Server constructs a long‑running in‑process `GlimmerClient` (scheduler).
- That client’s `poll_loop` uses `TaskQueue.poll()` to acquire shards:
  1) SELECT row_groups WHERE state=Active AND expires<=now() ORDER BY expires LIMIT k FOR UPDATE SKIP LOCKED
  2) UPDATE those rows to set a new lease (`expires=now()+lease`) RETURNING row_groups
  3) Fetch those tasks and convert to `TaskHandle`s
- gRPC DequeueShards returns these handles to external workers.

### Hot path: reporting progress (ack/nack):
1) Client’s Tracker batches acks/nacks per row_group (roaring bitmaps)
- Workers call UpdateShard with serialized roaring bitmaps:
  - Server `UpdateShard` loads the row (`SELECT … FOR UPDATE SKIP LOCKED`) and:
    - and Merges bitmaps: task.nack(failset); task.ack(successset | (all rows if all_succeeded))


4) State transitions: Active → Success or CompletedWithFailures
5) If the row is busy(locked)/missing, server returns ACTIVE to signal retry without blocking.



Transactions, locking, leases
-----------------------------
- Short transactions:
  - Use fresh Session per operation (`session_context(begin=True)`), do one thing, commit/close
  - Maintenance paths (renew, expire-old, abandoned cleanup) run in small batches with a commit per batch
  - Always short transactions; batching is done in small slices with commits per batch.
- Locking:
  - Acquisition and UpdateShard use `FOR UPDATE SKIP LOCKED` to avoid blocking on hot rows
  - Postgres timeouts set at connect and per txn (statement_timeout, lock_timeout)
  - SKIP LOCKED on both acquire and update paths avoids head‑of‑line blocking.
  - Postgres timeouts (statement/lock) are set at connect time and per maintenance txn.
  - Advisory locks used for abandoned‑shard cleanup to elect one leader per job.
  - Deterministic ordering when updating batches reduces deadlock risk.
- Leasing:
  - A task is claimable when `expires <= now()`
  - Acquire sets a new deadline: `expires = now() + LEASE_TIMEOUT_HOURS`
  - Background renewal extends leases at `LEASE_RENEWAL_INTERVAL_MINUTES`
- Abandoned & old shards:
  - Abandoned: Active rows with `expires < now() - ABANDONED_CLEANUP_HOURS` → set `expires = now()` (PG advisory lock elects a leader)
  - Old locally-owned shards: force-expire if held > OWNED_SHARD_TIMEOUT_HOURS (batched, short txns)


Caching (where and why)
-----------------------
- `TaskQueue` caches outcomes of expensive queries (`is_done`, `has_exhausted_available`, `count_tasks`) with a short TTL.
- Client caches finished shard sets per owned‑shard set hash to avoid requerying.
- Bulk insert for task creation; conditional aggregation for counts; EXISTS/limit‑1 patterns for boolean checks.

- TaskQueue: TTL cache (30s) for expensive read queries
  - `is_done()` (any non-completed tasks exist?)
  - `has_exhausted_available()` (any Active tasks with `expires <= now()`?)
  - `count_tasks()` (conditional aggregation)
- Client: TTL cache (60s) of finished shards for current owned set
  - Keyed by stable hash of owned row_groups
- Benefit: reduces repeat reads under load; correctness preserved via short TTL + state-change invalidation



Key settings & knobs
--------------------
Dynaconf (env prefix `GLIMMER_`):
- `LEASE_TIMEOUT_HOURS` (default 1)
- `LEASE_RENEWAL_INTERVAL_MINUTES` (default 30)
- `ABANDONED_CLEANUP_HOURS` (default 4)
- `OWNED_SHARD_TIMEOUT_HOURS` (default 4)

DB engine/pool (env):
- `GLIMMER_DB_POOL_SIZE` (default 64)
- `GLIMMER_DB_MAX_OVERFLOW` (default 64)
- `GLIMMER_DB_POOL_TIMEOUT` (seconds, default 5)
- `GLIMMER_DB_POOL_RECYCLE` (seconds, default 180)
- `GLIMMER_DB_POOL_PRE_PING` (default true)

### Ops knobs you’ll actually use
- DB pool: `GLIMMER_DB_POOL_SIZE`, `GLIMMER_DB_MAX_OVERFLOW`, `GLIMMER_DB_POOL_TIMEOUT`, `GLIMMER_DB_POOL_RECYCLE`, `GLIMMER_DB_POOL_PRE_PING`.
- Leases/cleanup (Dynaconf): `LEASE_TIMEOUT_HOURS`, `LEASE_RENEWAL_INTERVAL_MINUTES`, `ABANDONED_CLEANUP_HOURS`, `OWNED_SHARD_TIMEOUT_HOURS`.
- Logging: set `GLIMMER_QUEUE_DEBUG=true` to see DEBUG.
- Start server: `python -m glimmer_queue.start_server serve --connection-string <SQLALCHEMY_URL> --job-name <JOB>`
- Local pressure test: `python -m glimmer_queue.scripts.stress-test heartrend`




Operational cheatsheet
----------------------
- Start server:
  - `python -m glimmer_queue.start_server serve --connection-string <SQLALCHEMY_URL> --job-name <JOB>`
- Debug-seed job (serve `--debug`):
  - Creates a large mock job named `heartrend` and populates tasks
- Thin client stress (local):
  - `python -m glimmer_queue.scripts.stress-test heartrend` (acks/nacks loop)
- Run tests:
  - `pytest -q glimmer_queue/tests`

Failure modes & mitigations (quick scan)
---------------------------------------
- DB/connection hiccups on UpdateShard → server rolls back and returns ACTIVE; client retries
- Locked/busy shards → SKIP LOCKED avoids stalls; retried naturally by polling/flush loops
- Deadlocks → reduced by short txns, deterministic batch ordering, SKIP LOCKED, and PG timeouts
- Duplicate work → prevented by leasing; recovery via lease expiry and cleanup jobs

### The data model (Task essentials)
- PK: `(job_id, row_group)`, with `min_ix`, `max_ix`, `expires`, `completed` (bitmap), `errored` (bitmap), `state`, `owner`.
- Key indexes: `(job_id,state,expires)` for acquisition; `(job_id,row_group)` for lookups; plus others for counts/completion.
- Validation: `row_group` must be an int and <= 2,147,483,647 (reject bools and overflow).




