### SQLAlchemy 2.x in this repo (what it “does”)
- SQL toolkit + ORM: maps Python classes to tables and builds SQL via a typed expression API (no string SQL).
- Connection pooling and dialects: creates DB engines, manages pools, and speaks Postgres/SQLite specifics.
- Transaction/session management: short‑lived `Session`s, context‑managed `session.begin()` blocks, and safe rollback on errors.
- Postgres tuning hooks: sets statement/lock/idle timeouts on connect to prevent long waits.

HS basically:
2. alchemy helps manage the db for example adds Postgres tuning hooks that
allow you to set statement/lock/idle timeouts on connect to prevent long waits.
this helps with leasing (which is basically putting an expiry on the job we acquire)
this supposedly prevents duplicate work; if a worker dies, the lease naturally
expires so another worker can reclaim.

Where you see it:
- Models and typed queries:
```58:121:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/models.py
class Task(Base):
    __tablename__ = "tasks"
    job_id = Column(Uuid, ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True)
    row_group = Column(Integer, primary_key=True)
    ...
    __table_args__ = (
        Index("idx_task_acquisition", "job_id", "state", "expires"),
        ...
    )
```
- Engine/pool + Postgres timeouts:
```38:83:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/utils.py
def create_engine_with_envvars(url: str):
    ...
    engine = create_engine(expanded, **pool_kwargs)
    if engine.dialect.name == "postgresql":
        @event.listens_for(engine, "connect")
        def _pg_configure(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("SET statement_timeout = 5000")
            cursor.execute("SET lock_timeout = 2000")
            cursor.execute("SET idle_in_transaction_session_timeout = 15000")
            cursor.close()
```



### SKIP LOCKED (how it’s done, why it helps)
- How: both on acquire and on `UpdateShard` we use `FOR UPDATE SKIP LOCKED` to immediately skip rows another txn is touching.
```110:116:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/server.py
task = (
    session.execute(
        sqlalchemy.select(Task)
        .where(Task.job_id == self.job_id, Task.row_group == request.row_group)
        .with_for_update(skip_locked=True)
    ).scalars().first()
)
```
- Why it helps: avoids head‑of‑line blocking; busy shards don’t stall other work, reducing deadlocks and tail latencies.




### 2) What happens when SKIP LOCKED skips rows?
- On acquisition
  - We select candidate `row_group`s with `FOR UPDATE SKIP LOCKED`. Locked rows are simply omitted.
```470:479:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
select(Task.__table__.c.row_group) ... .with_for_update(skip_locked=True)
.order_by(Task.expires.asc()).limit(target_size)
```
  - We then update only those returned, and fetch them. Skipped rows aren’t waited on; they’ll be considered in the next poll.

- How we eventually process skipped rows
  - The queue keeps polling in a loop; if it didn’t fill the target, it loops again (with small sleeps/backoffs).
```541:551:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
while len(current_tasks) < target_size:
    acquired_tasks = self.acquire_up_to(want, session=s)
    ...
    if loop_cnt % 7 == 0:
        if self.is_done() or self.has_exhausted_available():
            break
    if loop_cnt >= 5:
        time.sleep(5 + random() * 2)
```
  - The server-side client also polls continuously; when no payload, it sleeps briefly and re-tries.
```158:176:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
if not payload:
    time.sleep(0.05 + random() * 0.05)
    ...
    if queue.is_done(): ... return
    continue
```

- On UpdateShard
  - If the shard row is currently locked (another writer), the server tries a `SELECT ... FOR UPDATE SKIP LOCKED`. If nothing is returned, it signals the client with an ACTIVE state (retry later).
```110:127:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/server.py
... .with_for_update(skip_locked=True) ... .first()
if task is None:
    return UpdateShardResponse(state=SHARD_STATE_ACTIVE)
```
  - The client’s `Tracker` backs off briefly and retries on the next flush signal/loop.
```993:1017:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
if getattr(resp, "state", None) == 0:  # ACTIVE
    time.sleep(0.1 + random() * 0.2)
    return
... retry-once path ...
if getattr(resp, "state", None) == 0:
    time.sleep(0.1 + random() * 0.2)
    return
```

- Bottom line: we never block on locked rows; we skip and naturally re-encounter them on subsequent polls/flushes.








### Short transactions (how it’s done, why it helps)
- How: operations wrap in `with session.begin():` or an ephemeral `session_context(begin=True)`; maintenance is batched, commits per batch.
```577:586:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
with self.session_context(begin=True, expire_on_commit=True) as s:
    next_tasks = self.acquire_up_to(request_n_rows, session=s)
    workloads = [TaskHandle(...)]
```
```730:743:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
for batch in chunks(row_groups, 128):
    try:
        with sess.begin():
            sess.execute(sqlalchemy.update(Task) ... .values(expires=new_deadline))
```
- Why it helps: keeps lock hold times tiny; lowers chance of deadlocks; improves concurrency under load and failure.

Extra protection during maintenance:
```585:599:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
s.execute(text("SET LOCAL lock_timeout = '2s'"))
s.execute(text("SET LOCAL statement_timeout = '10s'"))
upd = sqlalchemy.update(Task).where(... expires < cutoff).values(expires=func.now())
```


### 3) Short transactions: what, how, and batching
- What “short transactions” means here
  - Use many small, bounded `BEGIN ... COMMIT` sections that do one thing (lease, update, renew) and finish quickly.
  - Keep sessions ephemeral; avoid holding them across long-running loops.

- How they’re kept short
  - Ephemeral sessions via a context manager; each call yields a fresh `Session`, optional `begin=True`, and always closes.
```371:413:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
@contextmanager
def session_context(self, begin: bool = False, expire_on_commit: bool = False):
    s = self.session_factory()  # real Session
    ...
    cm = s.begin() if begin else nullcontext()
    with cm:
        yield s
```
  - Hot path uses a fresh, brief transaction; and when building payloads, it sets `expire_on_commit=True` so ORM instances don’t retain stale state after commit.
```577:586:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
with self.session_context(begin=True, expire_on_commit=True) as s:
    next_tasks = self.acquire_up_to(request_n_rows, session=s)
    workloads = [TaskHandle(...)]
```

- What does `expire_on_commit=True` mean?
  - After commit, ORM-loaded attributes are expired; the next attribute access will re-load from DB. This avoids stale reads and reduces memory residency of large object graphs. We set it on the per-call session inside `session_context`.
```403:409:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
try:
    s.expire_on_commit = bool(expire_on_commit)
except Exception: ...
```

- “Maintenance is batched, commits per batch”
  - For bulk updates (renewing leases, expiring old shards), we process a sorted list of row_groups in small batches; each batch runs inside its own short transaction, then commits, then we move to the next batch. This caps lock durations and reduces deadlock probability.
```446:476:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
for i in range(0, len(id_list), batch_size):
    batch = id_list[i : i + batch_size]
    with s.begin():  # short transaction
        if is_pg:
            s.execute(text("SET LOCAL lock_timeout = '2s'"))
            s.execute(text("SET LOCAL statement_timeout = '10s'"))
        res = s.execute(upd.where(Task.row_group.in_(batch)) ...)
```
```730:743:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
for batch in chunks(row_groups, 128):
    try:
        with sess.begin():
            sess.execute(sqlalchemy.update(Task) ... .where(Task.row_group.in_(batch)) ...)
```
  - We also set Postgres local timeouts inside those transactions to fail fast rather than wait on locks.
```459:461:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
s.execute(text("SET LOCAL lock_timeout = '2s'"))
s.execute(text("SET LOCAL statement_timeout = '10s'"))
```

If you want, I can surface these knobs in a tiny cheat sheet (env vars and what they affect) and point to the exact lines to tweak for initial lease duration (currently default 1h on acquire).


### Why these four together reduce deadlocks and keep throughput high
- Leasing prevents duplicate work and gives natural recovery.
- SKIP LOCKED prevents blocking on hot shards; work keeps flowing.
- Short transactions minimize lock duration and contention across many workers.
- Caching removes avoidable DB reads, leaving capacity for writes/leases.

If you want, I can sketch a one‑screen “cheat sheet” you can paste into your notes summarizing these with the exact code links above.


### Ack, nack, and flushing (quick recap)
- ack: record succeeded row IDs for a shard (into the success bitmap).
- nack: record failed row IDs (into the error bitmap).
- Flushing: sending the current bitmaps to the server (UpdateShard). The thin client’s `Tracker`:
  - Buffers acks/nacks in memory per row group.
  - Signals a background flush loop; that loop flushes on staleness, full‑shard size, or when enough new rows accumulated (partial flush threshold) and skips duplicates by hashing payloads.

### ORM instances and “stale state” after commit
- ORM instances are mapped Python objects (e.g., `Task`) attached to a SQLAlchemy `Session`.
- After commit, their attributes can remain cached. If another txn updated the row, your object would be stale.
- We set `expire_on_commit=True` on short‑lived sessions so attributes are invalidated at commit; the next access reloads from DB.
- Benefits:
  - Correctness: avoids serving stale values post‑commit.
  - Memory: expired objects don’t keep large graphs “hot”; ephemeral sessions + expiry reduce large object residency.