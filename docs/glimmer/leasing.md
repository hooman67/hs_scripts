### Leasing (how it’s done, why it helps)
- How: when acquiring work, we atomically set a short “lease” (`expires`) so others won’t process the same shard, then fetch those rows.
```468:483:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
want_row_groups = (
    session.execute(
        sqlalchemy.select(Task.__table__.c.row_group)
        .where(Task.job_id == self.job_id, Task.state == TaskState.Active, Task.expires <= func.now())
        .order_by(Task.expires.asc())
        .limit(target_size)
        .with_for_update(skip_locked=True)
    ).scalars().all()
)
```
```497:513:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
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
- Why it helps: prevents duplicate work; if a worker dies, the lease naturally expires so another worker can reclaim.

Lease builder (Postgres vs SQLite):
```126:137:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/utils.py
def make_deadline(session, hours: int = 1):
    dialect_name = session.bind.dialect.name
    if dialect_name == "sqlite":
        return func.DATETIME(func.now(), f"+{hours} hour")
    elif dialect_name == "postgresql":
        return func.now() + timedelta(hours=hours)
```

### Lease extension: how it actually works here
- The lease is time‑based (`tasks.expires`). A task is acquirable when `expires <= now()`.
- Renewal is periodic, not event‑driven:
  - The client’s `check_loop` triggers `renew_lease` every `LEASE_RENEWAL_INTERVAL_MINUTES` (default 30).
  - `renew_lease` extends `expires` for all currently owned row groups out to `now() + LEASE_TIMEOUT_HOURS` (default 1).
  - It only touches shards in `owned_shards`; finished shards are pruned first, so they stop getting renewed.
- Do we monitor progress to decide renewal?
  - We don’t gate renewal on per‑shard progress. Renewal is time‑based for all owned shards.
  - However, UpdateShard calls on the server invoke `client.heartbeat_shard(row_group)`; that updates an “insertion time” used by `erase_old_shards` to identify truly stale locally‑held shards. So progress/heartbeats help avoid being classified as “old,” but renewal itself isn’t tied to UpdateShard frequency.

### 1) Lease expiry: mechanics and where the timeout comes from
- How leases work
  - A lease is a time window on `tasks.expires`. A task is acquirable only when `expires <= now()`.
  - When acquiring, we set a new lease deadline atomically; subsequent renewals extend it.

- Where leases are set/renewed
  - Initial lease (acquire): defaults to 1 hour via `make_deadline(session)` (no hours passed).
```507:513:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
.values(
    expires=make_deadline(session),  # your lease end
    acquired_time=func.now(),
    owner=self.whoami,
)
```
```126:137:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/utils.py
def make_deadline(session, hours: int = 1):
    if dialect_name == "sqlite":
        return func.DATETIME(func.now(), f"+{hours} hour")
    elif dialect_name == "postgresql":
        return func.now() + timedelta(hours=hours)
```
  - Renewal cadence and length:
    - Renewal runs in the client’s background loop.
    - Renewal interval is configurable (default 30 minutes).
    - Renewal extends the lease to a configurable horizon (default 1 hour).
```292:304:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
next_renewal_due = now_m + renewal_interval_s
with self.session_context("renew_lease") as session:
    self.renew_lease(session)
```
```711:729:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
lease_hours = getattr(settings, "LEASE_TIMEOUT_HOURS", 1)
new_deadline = make_deadline(sess, hours=lease_hours)
...
.values(expires=new_deadline)
```
```8:15:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/config.py
class Settings:
    LEASE_TIMEOUT_HOURS: int = 1
    ABANDONED_CLEANUP_HOURS: int = 4
    LEASE_RENEWAL_INTERVAL_MINUTES: int = 30
```
- How a lease expires
  - Purely time-based: once `now()` passes `expires`, the row becomes eligible for acquisition again.
  - Settings are via Dynaconf (`GLIMMER_`-prefixed envs), e.g. `GLIMMER_LEASE_TIMEOUT_HOURS=2`, `GLIMMER_LEASE_RENEWAL_INTERVAL_MINUTES=20`.