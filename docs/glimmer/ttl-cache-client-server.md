### Caching (how it’s done, why it helps)
- How: a tiny TTL cache avoids repeated expensive queries per job (completion checks, availability, counts) and per‑owned shard set.
```436:456:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
def has_exhausted_available(self) -> bool:
    cache_key = f"exhausted_{self.job_id}"
    cached = self.query_cache.get(cache_key)
    if cached is not None: return cached
    with self.session_context(begin=True) as s:
        available_task = s.query(Task).filter(...).limit(1).first()
        result = available_task is None
        self.query_cache.set(cache_key, result)
```
```553:575:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/task_queue.py
def is_done(self) -> bool:
    cache_key = f"is_done_{self.job_id}"
    cached = self.query_cache.get(cache_key)
    if cached is not None: return cached
    ... .limit(1).first()
    self.query_cache.set(cache_key, result)
```
```322:339:/mnt/localssd/genie/glimmer_queue/src/glimmer_queue/client.py
cache_key = f"finished_shards_{self.job_id}_{hash(tuple(sorted(row_groups)))}"
cached_result = self.query_cache.get(cache_key)
if cached_result is not None:
    completed_ids = cached_result
else:
    completed_ids = self._query_finished_shards(session, row_groups)
    self.query_cache.set(cache_key, completed_ids)
```
- Why it helps: slashes repetitive read load, keeps hot paths fast, and still correct under short TTL + invalidation when states change.

### TTL cache (what it is)
- Time-to-live cache stores key → (value, timestamp).
- On get: if now - timestamp < ttl, return value; else evict and miss.
- On set: store (value, now).
- Benefits: cuts repeated DB reads in tight loops; eventual freshness via TTL.
- In this repo, `QueryCache` is thread-safe (internal `Lock`), minimal API: `get`, `set`, `clear`, `size` (`src/glimmer_queue/cache.py`).

### TTL cache in TaskQueue
- Purpose: cache expensive read queries about job state to reduce DB load during polling.
- Instance: `TaskQueue.query_cache = QueryCache(ttl_seconds=30)` (30s).
- Cached calls and keys:
  - `is_done()` → key `is_done_{job_id}`: “any non-completed tasks remain?” Uses LIMIT 1 EXISTS-style query, cached 30s.
  - `has_exhausted_available()` → key `exhausted_{job_id}`: “any Active tasks with expires <= now()?” Cached 30s.
  - `count_tasks()` → key `task_counts_{job_id}`: conditional aggregation counts (active/done/abandoned). Cached 30s.
- Invalidation:
  - Explicit method `TaskQueue._invalidate_cache()` calls `clear()` (used in tests and can be called after state-changing ops).
  - Otherwise TTL gives eventual consistency (stale up to 30s).
- Why it helps: `poll()` and status checks run continuously; caching eliminates redundant reads while not being correctness-critical (actual leasing/updating is transactional and not cached).

### TTL cache in Client (GlimmerClient/GlimmerThinClient side)
- Purpose: avoid re-querying finished shard sets on every maintenance tick when pruning `owned_shards`.
- Instance: `GlimmerClient.query_cache = QueryCache(ttl_seconds=60)` (60s).
- Cached call and key:
  - In `erase_finished_shards(session)`, cache key:
    - `finished_shards_{job_id}_{hash(tuple(sorted(row_groups)))}`.
    - Ties the cache entry to the exact current set of owned row_groups (order-independent).
- Behavior:
  - If the same owned set repeats within TTL → skip DB, use cached finished set; quickly remove any completed shards from local ownership.
  - If owned set changes → hash changes → new key → DB query happens.
  - If owned set is unchanged but TTL expires → refresh from DB.
- Why 60s here: maintenance runs periodically (seconds to minutes). Slight staleness is acceptable; this path is an optimization, not the source of truth.

### Trade-offs and safeguards
- Staleness window: up to 30s (TaskQueue) / 60s (Client) for cached entries. Chosen for load reduction; not used for critical write paths.
- Consistency: leasing (`FOR UPDATE SKIP LOCKED`), `UpdateShard`, and renewals are transactional and do not use caches.
- Memory: caches are bounded by usage pattern; `clear()` wipes them; `size()` is available for inspection. Thread-safety prevents races.

### Mental model summary
- TaskQueue’s TTL cache: caches “is the job done?”, “is there anything available?”, and “counts” for 30s to keep the poll loop light.
- Client’s TTL cache: caches “which of my currently-owned shards are finished?” for 60s, keyed by the exact owned set, to prune without spamming the DB.

If you want, I can add a short section in `docs/one_pager.md` that lists these keys and TTLs so you have them at a glance.