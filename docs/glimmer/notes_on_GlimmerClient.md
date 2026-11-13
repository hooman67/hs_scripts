## HS summary
GlimmerClient runs inside the same OS process as gRPC server (GlimmerQueueService).
It runs a poll loop that leases shards from db and passes exposes to the GlimmerQueueService
so that it can pass to workers. It also runs a check/maintain loop that (`erase_finished_shards`, `erase_old_shards`, `erase_abandoned_shards`, `renew_lease`).

  - in-process means this client runs inside the same OS process as the gRPC server
        (created in start_server.py). It is not a separate service.
  - During the poll loop, It leases work directly from the database and buffers it so the
        server can hand shards to external workers via DequeueShards RPC.
      -It Polls the
        DB via `TaskQueue` to lease shards and pushes them into an internal queue.
    - Exposes `dequeue_batch()` for the service to hand shards to external workers.
  -     Leased vs. owned shards:
        - Leased shards are freshly acquired from the DB by TaskQueue.poll()
          with a lease (tasks.expires pushed into the future). Leased shards
          enter the outbound queue `self.out`.
        - Owned shards are the shards we have handed to external workers via
          DequeueShards and are currently tracked locally in `self.owned_shards`.
          While owned, we maintain their lease, prune completed ones, and may
          force-expire very old ones to let others proceed.

  -     TaskHandle
        - an immutable class defining a single shard of work.
        - task_queue.TaskHandle(row_group, min_ix, max_ix, succeeded_bitmap).
        - row_group: integer shard identifier
        - [min_ix, max_ix]: inclusive row-id bounds this shard covers
        - succeeded: roaring bitmap of already-completed row ids in this shard
  - Batches `ack`/`nack` via `CachedAcker`, runs maintenance loop (called check_loop)
  which does (`erase_finished_shards`, `erase_old_shards`, `erase_abandoned_shards`, `renew_lease`).
  - `client_counter = HeartbeatTracker()` lets it adjust backpressure based on active clients.
  - `client.start()` launches its background threads (poll loop + maintenance loop).


## Poll loop details
        Continuously lease work and enqueue it for the gRPC service.

        - Uses TaskQueue(self.db_session_maker(), self.name) to talk to the DB.
        - Each poll performs a short transaction to lease up to N shards via
          SELECT..FOR UPDATE SKIP LOCKED + UPDATE lease.
        - Enqueues small groups of TaskHandle into `self.out` for DequeueShards.
        - Applies backpressure using queue size and owned shard count, scaled
          by the current number of connected clients (HeartbeatTracker).
          hs: this means that if the size of out (leased shards) or size of
          owned_shards is bigger than the bounds we calculate for them, we just sleep.
          Think of it as two dials limiting how much we “prefetch” and how much we allow “in flight” at once:
          - qsize (out queue) = how many 2‑shard chunks are buffered for workers to grab
          - owned_shards_len = how many shards we’ve handed out but haven’t seen completed/pruned yet

        - Enables work-stealing when the DB reports no available tasks so workers
          can keep busy with already-owned shards.
        - Signals termination (self.done=True, self.out.put(None)) when the
          underlying queue.is_done() indicates job completion.




## Explain to me what's happening in the lines below with a concerete example:
```python
            group_size = 2  # The granularity in which shards are split: e.g., 2 means that each client gets 2 shards per request.
            if not payload:
                logger.debug("Polled, length is 0")
                time.sleep(0.05 + random() * 0.05)
                logger.debug("Polled workstealing:", workstealing=self.enable_work_stealing.load())
                logger.debug("Queue has exhausted available:", exhausted=queue.has_exhausted_available())
                if not self.enable_work_stealing.load() and queue.has_exhausted_available():
                    logger.debug("Queue has exhausted available. Allowing work stealing.")
                    self.enable_work_stealing.store(True)
                if queue.is_done():
                    logger.info("Queue is completely done (hooray!). Sending termination signal.")
                    self.done = True
                    self.out.put(None)
                    return
                # FIXME: Simplify the stop_signal checks.
                if self.stop_signal.is_set():
                    return
                logger.debug("Polled, length is 0. Continuing.")
                continue
            logger.debug("Putting in out queue")
            for i in chunks(payload, group_size):
                self.out.put(i)
            logger.debug("Put in out queue complete ")
            qsize_bound = 8
            owned_shards_len_bound = 16
            if self.client_counter is not None:
                logger.debug("Client counter is not None", client_counter=self.client_counter.count())
                qsize_bound = max(qsize_bound, self.client_counter.count() * 4)
                owned_shards_len_bound = max(owned_shards_len_bound, self.client_counter.count() * 4)
```


- group_size = 2
  - When `payload` (a list of TaskHandle) comes back from `queue.poll(32)`, we break it into chunks of 2 and enqueue those chunks into `self.out`.
  - Each chunk is what the gRPC layer hands to a worker in one dequeue, so workers fetch small batches.

  HS: each chunk (i.e. what we actually put in the queue) is a list of two taskHandles.


- If no payload
  - Sleep a tiny randomized delay: `0.05–0.1s` to avoid hot‑spinning.
  - Log whether work‑stealing is enabled.
  - Check `queue.has_exhausted_available()`: if true and work‑stealing not yet enabled, enable it so workers can keep busy by “stealing” from owned shards.
  - If `queue.is_done()`: set `self.done = True`, push `None` into `out` as a sentinel, and return (client is finished).
  - If a shutdown is requested (`stop_signal`), return early.

- Backpressure bounds (the “magic numbers”)
  - After enqueuing chunks, compute:
    - qsize_bound = 8
    - owned_shards_len_bound = 16
  - If we have a live client counter (HeartbeatTracker), scale both bounds by number of clients:
    - qsize_bound = max(8, clients × 4)
    - owned_shards_len_bound = max(16, clients × 4)
  - Then, while either buffer is above its bound:
    - Sleep `0.15–0.45s` (randomized), re‑compute bounds (clients may change), and re‑check.
    - Exit if `stop_signal` is set.

Think of it as two dials limiting how much we “prefetch” and how much we allow “in flight” at once:
- qsize (out queue) = how many 2‑shard chunks are buffered for workers to grab
- owned_shards_len = how many shards we’ve handed out but haven’t seen completed/pruned yet

### Concrete example

Assume:
- 10 workers connected (client_counter.count() = 10)
- `queue.poll(32)` returns 12 TaskHandles

Step by step:
1) Chunking
   - group_size = 2 → 12 tasks → 6 chunks.
   - Enqueue 6 chunks into `self.out`.

2) Bounds for 10 clients
   - qsize_bound = max(8, 10×4) = 40 chunks
   - owned_shards_len_bound = max(16, 10×4) = 40 shards

3) Backpressure loop
   - Suppose out.qsize() is 6 and owned_shards_len is 0 at this moment:
     - Both are ≤ 40, so we don’t sleep; loop continues to next poll quickly.

4) If we had 2 workers only (count = 2)
   - qsize_bound = max(8, 2×4) = 8
   - owned_shards_len_bound = max(16, 2×4) = 16
   - If out.qsize() grows above 8 (say 12 chunks), the loop sleeps in small intervals until workers drain the queue below 8. This prevents unbounded buffering when few consumers are present.

5) No rows available path
   - `queue.has_exhausted_available()` true → enable work‑stealing.
   - Next `dequeue_batch()` on the server may offer a shard sampled from `owned_shards`, keeping workers busy even when the DB has nothing new to lease (useful under brief scarcity).

6) Completion
   - Once `queue.is_done()` is true, we mark done and put a `None` sentinel into `out` so the consumer side can terminate gracefully.

### Why these numbers exist
- Small chunk size (2) keeps fairness across workers and reduces lockhold time per dequeue.
- qsize_bound and owned_shards_len_bound provide adaptive backpressure:
  - Base floor (8/16) to keep some buffer even with few clients.
  - Scale by clients×4 so more workers permit more prefetched work, but still cap it.
- Randomized short sleeps reduce thundering herds and hot loops when waiting for buffers to drain.

If you want, we can surface these as settings (instead of literals) so you can tune per deployment: group_size, base qsize/owned bounds, per‑client multiplier, and sleep jitter.



## work stealing
5) No rows available path
   - `queue.has_exhausted_available()` true → enable work‑stealing.
   - Next `dequeue_batch()` on the server may offer a shard sampled from `owned_shards`, keeping workers busy even when the DB has nothing new to lease (useful under brief scarcity).


## check maintain loop details
        Runs four tasks on their own schedules:
          1) erase_finished_shards: prune locally-owned shards that are no longer Active in DB
          2) erase_old_shards: force-expire shards held locally longer than OWNED_SHARD_TIMEOUT_HOURS
          3) erase_abandoned_shards: global cleanup of truly abandoned shards (advisory lock leader)
          4) renew_lease: extend leases for currently owned shards out to LEASE_TIMEOUT_HOURS
        """

All this does is on 4 timers, updates the owned_shards_queue. On 3 timers,it will query the database and erase all the shards from the owned_shards_queue that it no longer needs. And on another (4th) timer, it will renew all the leases of all the shards that are on the owned_shards_queue.


## dequeue_batch function (and work stealing details)

  - overview
    Pop a small batch of leased shards for the gRPC layer.

    - Prefer freshly leased shards from `self.out`.
    - When work-stealing is enabled and queue is empty, yield one shard from
      current ownership so external workers can continue making progress.
    - Moves returned shards into `self.owned_shards` and records insertion
      time so maintenance loops can renew/inspect them.


  1. retrieve as many shards from out as your timer allows
  so much less for when work stealing than normal times
  ```
  timeout = 0.05 if self.enable_work_stealing.load() else 0.5
  tasks = self.out.get(timeout=timeout)
  ```

  2. IF out queue is empty, if work stealing is enabled,
  then try to give out one of the owned_shards. If the owned_shards,
  is also empty, create a fake work.


  3. If the out is empty, and work stealing is disabled, then increase the
  number of clients on the queue (using fake client), this gives the queue more reason to pull more work from RDS. Then try pulling again.
  ```
            self.client_counter.heartbeat(str(randint(0, 2047)))
                logger.debug(
                    "Increasing pressure on the queue.",
                    num_clients=self.client_counter.count(),
                )
                try:
                    tasks = self.out.get(timeout=0.5)
  ```
  4. Finally, if the shards that returned were not previously owned, add them to owned shards, and also record their insertion time.








## Teach mea glimmer client
### GlimmerClient: what it is
- In‑process scheduler/worker manager used by the server.
- Leases shards from DB, buffers them, hands them to gRPC handlers, and maintains leases/cleanup in the background.
- Batches acks/nacks to the DB efficiently.

### Core state
- **db_session_maker**: factory returning a Session; enables short‑lived, per‑op sessions.
- **name/job_id/row_group_size**: resolved at init.
- **out: Queue**: buffer of leased shards for gRPC to dequeue.
- **owned_shards: RWDeque[TaskHandle]**, **owned_shards_len: AtomicInt**: shards handed out to workers and still “owned”.
- **owned_shards_insertion_time: dict[int, datetime]**: last activity per shard for cleanup heuristics.
- **threads**: poll loop + maintenance loop.
- **executor**: small pool for offloading acker ops.
- **acker: CachedAcker**: batches DB updates for acks/nacks.
- **client_counter: HeartbeatTracker | None**: used to scale backpressure.
- **enable_work_stealing: AtomicBool**, **done: bool**: control flow flags.
- **query_cache: QueryCache(ttl=60s)**: caches “finished shards” sets per owned‑set hash.

### Lifecycle
- **__init__(db_session_maker, name, client_counter=None)**
  - Configures logging, resolves job metadata, constructs `CachedAcker`, starts in “stopped” state.
- **start() / stop()**
  - Start joins the poll + maintenance threads; stop signals and joins them.

### Public API used by the server
- **dequeue_batch() -> list[TaskHandle]**
  - Pulls a small batch of leased shards from `out` (or steals one if enabled and idle).
  - Moves returned shards into `owned_shards` and tracks insertion time.
- **ack(rows, storage_locations=None) / nack(rows, exception=None)**
  - Enqueue batched ack/nack work to `CachedAcker` via `executor`.
- **flush_all()**
  - Forces `CachedAcker` flush, then shuts down the acker executor.
- **metadata() -> dict**
  - Returns job payload (e.g., num_rows) for info/telemetry.
- **__iter__()**
  - Iteration interface: starts, yields leased tasks from `out`, then flushes/stop on exit.

### Internal loops
- **poll_loop()**
  - Creates a `TaskQueue` and repeatedly:
    - `queue.poll(32)` to lease up to 32 tasks (short DB txn).
    - If empty: short sleep, enable work‑stealing when `has_exhausted_available()`, return termination signal when `queue.is_done()`.
    - If tasks: split into small groups (default group_size=2) and `put` into `out`.
    - Backpressure: while `out.qsize()` or `owned_shards_len` exceeds bounds, sleep; bounds scale with `client_counter.count()`.
- **check_loop()**
  - Periodic maintenance with jitter/backoff:
    - Every ~5s (+backoff): `erase_finished_shards(session)` removes locally owned shards that DB marks non‑Active.
    - Every ~10s (+backoff): `erase_old_shards(session)` force‑expires locally held shards older than threshold.
    - Every ~60m (by default 30m renewal interval): `renew_lease(session)` extends leases for all currently owned shards.
    - Every ~1h (+jitter/backoff): `erase_abandoned_shards(session)` makes genuinely abandoned shards available (PG advisory lock to elect a leader).

### Maintenance methods (high level)
- **erase_finished_shards(session)**
  - Builds a cache key from the current owned row_groups; looks up a 60s TTL cache of finished groups.
  - Queries DB on cache miss, then prunes finished from `owned_shards`.
- **_query_finished_shards(session, row_groups)**
  - Read‑only query for `Task.row_group` where state != Active; rolls back auto‑begun txn to keep the session clean.
- **erase_old_shards(session)**
  - Finds owned shards whose “age since insertion time” exceeds `OWNED_SHARD_TIMEOUT_HOURS`.
  - Removes them from `owned_shards`, then in short, timed batches updates `expires` to the past (immediately visible).
  - Sets `SET LOCAL lock_timeout` and `statement_timeout` in Postgres; deterministic ordering reduces deadlocks.
- **erase_abandoned_shards(session)**
  - With a session‑level PG advisory lock (one leader per job), updates Active rows whose `expires < now()-ABANDONED_CLEANUP_HOURS` to `expires=now()` (or slightly before) in one pass. Plays nicely with existing transactions.
- **renew_lease(session)**
  - For all currently owned shards, extends `expires` to `now()+LEASE_TIMEOUT_HOURS`.
  - If in a transaction, executes updates directly; otherwise, commits per 128‑id batch to keep locks short.
- **heartbeat_shard(row_group)**
  - Updates the shard’s insertion time; used to avoid classifying active shards as “old.”

### Session and concurrency helpers
- **session_context(name)**
  - Yields a fresh Session from the factory; always closes; logs and re‑raises on errors.
- **submit(f, *args, **kwargs)**
  - Runs a callable in the acker executor and drains completed futures.

### How it fits with the server
- The gRPC service calls `client.dequeue_batch()` to serve `DequeueShards`, and `client.heartbeat_shard()` during `UpdateShard`.
- The client’s loops keep the pipeline flowing: leasing new shards, renewing leases, and cleaning up ownership to avoid hoarding.

If you want, I can annotate the methods inline in your editor with brief docstrings so this mental model lives next to the code.




## more details
    """
    In-process scheduler and shard manager used by the gRPC server.

    What "in-process" means:
        This client runs inside the same OS process as the gRPC server
        (created in start_server.py). It is not a separate service. It
        leases work directly from the database and buffers it so the
        server can hand shards to external workers via DequeueShards.

    What a TaskHandle is:
        A lightweight, immutable view of a single shard of work defined in
        task_queue.TaskHandle(row_group, min_ix, max_ix, succeeded_bitmap).
        - row_group: integer shard identifier
        - [min_ix, max_ix]: inclusive row-id bounds this shard covers
        - succeeded: roaring bitmap of already-completed row ids in this shard

    Leased vs. owned shards:
        - Leased shards are freshly acquired from the DB by TaskQueue.poll()
          with a lease (tasks.expires pushed into the future). Leased shards
          enter the outbound queue `self.out`.
        - Owned shards are the shards we have handed to external workers via
          DequeueShards and are currently tracked locally in `self.owned_shards`.
          While owned, we maintain their lease, prune completed ones, and may
          force-expire very old ones to let others proceed.

    Leader election for abandoned cleanup:
        erase_abandoned_shards uses a Postgres session-level advisory lock
        (pg_try_advisory_lock) on a stable bigint key derived from job_id.
        Only the client instance that acquires the advisory lock performs the
        cleanup pass, preventing duplicate work across multiple server instances.
    """