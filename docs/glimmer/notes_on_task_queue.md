### What Tracker is (and how it connects to GlimmerThinClient)
- Purpose: client-side progress aggregator for acks/nacks that flushes to the server in batches over gRPC (`UpdateShard`).
- Owned by: `GlimmerThinClient` (external worker process).
- Comm path:
  - Thin client creates a gRPC stub, constructs `Tracker(stub)`.
  - Your code calls `thin_client.ack([...])`/`nack([...])`; those are queued to run in background threads and call `Tracker.ack/nack`.
  - Tracker aggregates bitmaps per row-group and a background flush worker calls `UpdateShard` via the same gRPC stub.

Key thin client wiring:
```893:896:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
def generate_stub(addr: str) -> glimmer_queue_pb2_grpc.GlimmerQueueStub:
    channel = grpc.insecure_channel(addr)
    stub = glimmer_queue_pb2_grpc.GlimmerQueueStub(channel)
```
```902:912:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
def __init__(self, addr: str):
    configure_logging()
    self.stub = generate_stub(addr)
    self.tracker = Tracker(client=self.stub)
    self.async_proxy = AsyncProxy()
```
```949:963:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
def ack(self, *args, **kwargs):
    self.async_proxy.enqueue(self.tracker.ack, *args, **kwargs)
def nack(self, *args, **kwargs):
    self.async_proxy.enqueue(self.tracker.nack, *args, **kwargs)
```
```965:981:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
def iterate_row_ids(self):
    while (tasks := self.dequeue()) is not None:
        ...
        for task in tasks:
            for row_id in task:
                yield row_id
    ...
    self.async_proxy.shutdown()
    self.tracker.flush_all()
```

### Tracker internals (what it tracks and when it flushes)
- State: `ack_state[row_group]`, `nack_state[row_group]` are Roaring bitmaps; `acked_locs` (optional storage paths); `staleness[row_group]` timestamps; `_last_flush_hash` for dedup; `_last_partial_total` for partial flush gating.
- Concurrency: guarded by a single `_state_lock`. Flushes are done by a dedicated background thread signaled via a `Condition`.

Construction + background worker:
```808:830:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
def __init__(self, client: GlimmerQueueStub) -> None:
    ...
    self.client = client
    self.row_group_size = client.QueryJob(QueryJobRequest()).row_group_size
    ...
    self._state_lock: Lock = Lock()
    self._flush_cond: Condition = Condition()
    self._flush_request: bool = False
    self._flush_stop: bool = False
    self._flush_thread: Thread = Thread(target=self._flush_loop, daemon=True)
    self._flush_thread.start()
```

Ack/Nack accumulation and signaling:
```856:866:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
def ack(self, rows: Sequence[int], storage_locations: list[str] | None = None) -> None:
    row_groups = self._partition_into_row_groups(rows)
    if storage_locations:
        with self._state_lock:
            for k, k_rows in row_groups.items():
                self.acked_locs[k].update({i: storage_locations[i] for i in k_rows})
    for k in row_groups:
        self._ack(k, row_groups[k])
```
```877:885:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
def _ack(self, row_group: int, rows: BitMap) -> None:
    with self._state_lock:
        self.ack_state[row_group].update(rows)
    self.check_stale(row_group)
```
```887:892:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
def check_stale(self, row_group):
    # Only signal the flush worker; do not flush synchronously
    with self._flush_cond:
        self._flush_request = True
        self._flush_cond.notify()
```

Flush triggers and behavior:
- Triggers:
  - Staleness: no flush in ~3 minutes.
  - Full shard: total rows reached `row_group_size`.
  - Partial progress: “enough” new rows since last partial flush (default 10–20).
  - Explicit `force_ack()` or `flush_all()` on shutdown.
- Behavior:
  - Serialize `ack/nack` bitmaps.
  - Deduplicate by hash to avoid sending identical payloads.
  - Call `UpdateShard` with a short timeout; if shard is ACTIVE (busy), back off.

Partial flush guard:
```898:941:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
def flush_partial(self, row_group: int, min_rows: int = 20) -> bool:
    if min_rows >= self.row_group_size: return False
    with self._state_lock:
        ack_bitmap = BitMap(self.ack_state.get(row_group, BitMap()))
        nack_bitmap = BitMap(self.nack_state.get(row_group, BitMap()))
        last_total = self._last_partial_total.get(row_group, 0)
        last_hash = self._last_flush_hash.get(row_group)
    total_rows = len(ack_bitmap | nack_bitmap)
    if total_rows - last_total < min_rows: return False
    succeeded_data = ack_bitmap.serialize()
    failed_data = nack_bitmap.serialize()
    current_data_hash = hash((succeeded_data, failed_data))
    if last_hash == current_data_hash: return False
    self.flush(row_group); return True
```

gRPC flush (UpdateShard) and post-flush cleanup:
```983:997:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
resp = self.client.UpdateShard(
    UpdateShardRequest(succeeded=succeeded_data, failed=failed_data, row_group=row_group),
    timeout=timeout_seconds,
)
if getattr(resp, "state", None) == 0:  # SHARD_STATE_ACTIVE
    time.sleep(0.1 + random() * 0.2)
    return
```
```1027:1036:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
total_rows = len(ack_bitmap | nack_bitmap)
with self._state_lock:
    self._last_flush_hash[row_group] = current_data_hash
    self.staleness[row_group] = datetime.datetime.now()
    self._last_partial_total[row_group] = total_rows
    if total_rows >= self.row_group_size:
        if row_group in self.ack_state: del self.ack_state[row_group]
        if row_group in self.nack_state: del self.nack_state[row_group]
```

Practical mental model:
- Thin client emits progress → Tracker coalesces per row-group → background thread flushes small, deduped payloads → server merges them into DB task bitmaps.

### TaskQueue (server-side, DB leasing and queries)
- Purpose: all DB operations for leasing tasks and status queries (used by the in-process `GlimmerClient`).
- Key operations:
  - `poll(n)`: grab up to n shards ready to work; short transaction; return `TaskHandle`s.
  - `acquire_up_to`: SELECT available rows with `FOR UPDATE SKIP LOCKED`, then UPDATE to set `expires` (lease), `owner`, and return only rows we actually acquired.
  - `count_tasks`, `is_done`, etc.: cached queries via TTL cache.

Poll and leasing flow:
```577:597:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
with self.session_context(begin=True, expire_on_commit=True) as s:
    next_tasks = self.acquire_up_to(request_n_rows, session=s)
    workloads = [TaskHandle(row_group=int(t.row_group), min_ix=t.min_ix, max_ix=t.max_ix, succeeded=t.completed_set())
                 for t in next_tasks]
    return workloads
```
```495:513:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
acquired_ids = (
    session.execute(
        update(Task)
        .where(Task.job_id == self.job_id, Task.__table__.c.row_group.in_(task_row_groups),
               Task.state == TaskState.Active, Task.expires <= func.now())
        .values(expires=make_deadline(session), acquired_time=func.now(), owner=self.whoami)
        .returning(Task.__table__.c.row_group)
    ).scalars().all()
)
```
```525:533:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
return (
    session.query(Task)
    .filter(Task.job_id == self.job_id, Task.__table__.c.row_group.in_(acquired_ids))
    .all()
)
```

Notes:
- Transactions are intentionally short; objects expire on commit to avoid stale ORM state and reduce memory residency.
- `SKIP LOCKED` means contention-free concurrent leasing.

### CachedAcker (server-side, DB batch writer)
- Purpose: server-side equivalent of `Tracker` that writes progress directly to the DB (no gRPC). Used by the in-process `GlimmerClient`.
- State mirrors `Tracker` (ack/nack bitmaps, staleness), but methods operate in DB transactions and can lazily create missing `Task` rows.

Structure and init:
```644:654:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
class CachedAcker:
    """A client that sends acks to the database in batches."""
    job_id: UUID
    ack_state: defaultdict[int, BitMap]
    nack_state: defaultdict[int, BitMap]
    ...
```
```656:669:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
def __init__(..., session, job: Job):
    with session.begin():
        self.job_id = job.id
        self.row_group_size = job.row_group_size
    self.ack_state = defaultdict(BitMap)
    self.nack_state = defaultdict(BitMap)
    self.session = session
    self.lock = Lock()
```

Ack/Nack and flush-on-stale/full:
```695:705:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
def ack(self, rows: Sequence[int], storage_locations: list[str] | None = None) -> None:
    row_groups = self._partition_into_row_groups(rows)
    if storage_locations:
        for k, k_rows in row_groups.items():
            self.acked_locs[k].update({i: storage_locations[i] for i in k_rows})
    with self.lock:
        with self.session.begin():
            for k in row_groups:
                self._ack(k, row_groups[k])
```
```722:726:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
def check_stale(self, row_group):
    if (now - self.staleness[row_group] > timedelta(seconds=30)) or len(ack|nack) >= row_group_size:
        self.flush(row_group)
```

Flush to DB (merging bitmaps and creating Task on demand):
```728:736:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
task = (self.session.execute(select(Task).where(Task.job_id == self.job_id, Task.row_group == row_group))
        .scalars().first())
if task is None:
    job = self.session.execute(select(Job).where(Job.id == self.job_id)).scalars().one()
    ...
    task = Task(job_id=self.job_id, row_group=row_group, min_ix=min_ix, max_ix=upper_bound, state=TaskState.Active, ...)
    self.session.add(task)
```
```764:767:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
if task.completed is not None:
    task.ack(BitMap.deserialize(task.completed) | self.ack_state[row_group])
else:
    task.ack(self.ack_state[row_group])
```
```776:779:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
self.staleness[row_group] = datetime.datetime.now()
del self.ack_state[row_group]
del self.nack_state[row_group]
```

Lease renewal helper (server-side):
```787:797:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
def renew_lease(self) -> None:
    with self.lock:
        with ctx:
            for row_group in self.ack_state:
                self.session.execute(
                    update(Task).where(Task.job_id == self.job_id, Task.row_group == row_group)
                    .values(expires=make_deadline(self.session))
                )
```

### How they fit together
- External worker uses `GlimmerThinClient`:
  - Fetches shards via `DequeueShards`, iterates row IDs, calls `ack`/`nack`.
  - Those calls enqueue to `Tracker`, which batches and periodically calls `UpdateShard` to the server.
- Server process uses `GlimmerClient`:
  - Leases shards from DB via `TaskQueue.poll` and serves them to external workers.
  - Batches server-side progress via `CachedAcker` when it itself must write progress directly to DB (e.g., maintenance, merges).

- Difference:
  - `Tracker`: gRPC to server (external).
  - `CachedAcker`: direct DB (internal to server).
  - `TaskQueue`: DB leasing and status queries (internal).

- Why bitmaps: compactly represent many row IDs; efficient set union/serialize for network and DB.

- Why short transactions and object expiry: minimize lock time and memory, avoid stale ORM state across long-lived sessions.

- Partial flushes: reduce risk window (progress is durable sooner), avoid sending redundant payloads, and keep memory low by pruning completed groups.

- TTL caching (in `TaskQueue`): limits repetitive DB reads for status checks during tight polling loops.

- SKIP LOCKED (in `acquire_up_to`): prevents deadlocks and lets multiple servers lease in parallel without blocking.

- Lease renewal (server-side and client-side): periodic, time-based; renews only for shards still in flight.

- Ownership: Thin client is owned by your worker processes; `TaskQueue` and `CachedAcker` are owned by the in-process `GlimmerClient` that lives inside the gRPC server.

- Summary of key responsibilities:
  - Tracker: batch and send progress over gRPC; dedupe; partial/stale flush; thread-safe.
  - TaskQueue: DB leasing/queries with short transactions; SKIP LOCKED; TTL cache.
  - CachedAcker: batch and write progress to DB; lazy task creation; merge bitmaps; renew leases.

- If you want, we can step through a concrete end-to-end example with sample rows and show each state change across `Tracker` → `UpdateShard` → server merge.