"""Check reviewed, local study examples without running the archive's application tools."""
import ast
import contextlib
import hashlib
import io
import json
from pathlib import Path
import random
import runpy
import sqlite3

HERE = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((HERE / 'data/source-manifest.json').read_text())
SOURCE = Path('/mnt/localssd/dev_research_inputs/friend-plan-2026-10-14')

for entry in MANIFEST['files']:
    data = Path(entry['extracted_path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['archive_path']

results = {'as_of': '2026-10-14', 'source_hashes_match': True, 'original_examples': {}}
for name in ['rotate-image.py', 'hit-counter.py', 'ttl-cache.py']:
    with contextlib.redirect_stdout(io.StringIO()):
        runpy.run_path(str(SOURCE / 'prep/coding' / name), run_name='__main__')
    results['original_examples'][name] = 'passed built-in assertions'

rotate = runpy.run_path(str(SOURCE / 'prep/coding/rotate-image.py'))['rotate_image']
with contextlib.redirect_stdout(io.StringIO()):
    for n in range(1, 21):
        matrix = [[i*n+j for j in range(n)] for i in range(n)]
        expected = [list(row) for row in zip(*matrix[::-1])]
        rotate(matrix)
        assert matrix == expected
results['rotation_sizes_1_to_20'] = 'passed against independent reference'

HitCounter = runpy.run_path(str(SOURCE / 'prep/coding/hit-counter.py'))['HitCounter']
rng = random.Random(14)
c, hits, now = HitCounter(), [], 0
for _ in range(1000):
    now += rng.randrange(0, 20)
    if rng.random() < 0.7:
        c.hit(now)
        hits.append(now)
    assert c.getHits(now) == sum(now-300 < t <= now for t in hits)
results['hit_counter_monotonic_checks'] = 1000

# Verify the archive's own test calls against its stated monotonic-time contract.
tree = ast.parse((SOURCE / 'prep/coding/hit-counter.py').read_text())
test = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'test_1')
calls = sorted((node.lineno, node.func.attr, node.args[0].value)
               for node in ast.walk(test)
               if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
               and isinstance(node.func.value, ast.Name) and node.func.value.id == 'counter'
               and node.args and isinstance(node.args[0], ast.Constant))
results['hit_test_time_reversals'] = [
    {'earlier_call': a, 'later_call': b} for a, b in zip(calls, calls[1:]) if b[2] < a[2]
]

classes = runpy.run_path(str(SOURCE / 'prep/coding/ttl-cache.py'))
map_cache, heap_cache, reference, now = classes['MapTTLCache'](), classes['HeapTTLCache'](), {}, 0
for _ in range(1000):
    now += rng.randrange(0, 5)
    key = str(rng.randrange(20))
    if rng.random() < 0.6:
        value, ttl = rng.randrange(1000), rng.randrange(1, 100)
        reference[key] = (value, now+ttl)
        map_cache.put(now, key, value, ttl)
        heap_cache.put(now, key, value, ttl)
    expected = reference.get(key)
    answer = expected[0] if expected and now < expected[1] else -1
    assert map_cache.get(now, key) == heap_cache.get(now, key) == answer
    size = sum(now < expiry for _, expiry in reference.values())
    assert map_cache.size(now) == heap_cache.size(now) == size
results['ttl_cache_monotonic_checks'] = 1000

# Redis documents binary64 scores; full-width Snowflake IDs need a different cursor encoding.
results['binary64_score_collision'] = {
    'ids': [2**60, 2**60+1], 'distinct_ids': True,
    'same_float_score': float(2**60) == float(2**60+1),
}

# Counterexample to the book-purchase note's exclusive-worker claim predicate.
db = sqlite3.connect(':memory:')
db.execute('CREATE TABLE requests (id INTEGER PRIMARY KEY, status TEXT)')
db.execute("INSERT INTO requests VALUES (1, 'pending')")
claim = "UPDATE requests SET status='running' WHERE id=1 AND status IN ('pending', 'running')"
results['book_purchase_claim_counterexample'] = {
    'first_claim_rows': db.execute(claim).rowcount,
    'second_claim_rows': db.execute(claim).rowcount,
    'conclusion': 'Predicate alone does not establish exclusive ownership; both claims match.',
}

out = HERE / 'data/example-validation.json'
out.write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
