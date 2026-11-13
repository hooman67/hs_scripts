# HP V6.2/V6.3 deterministic 160 → 30 selector

Local-only, standard-library implementation. No model, endpoint, image, judge,
network, or paid jobs. **Do not run on the real V6.3 export until it is provided.**

## API and CLI

Import `selector.py`; `select_prompts(data, seed=42)` returns a **document**
containing 30 V6.3 records plus selection metadata.
`match_baseline(selected, baseline)` returns the corresponding V6.2 document,
using exact `(device_id, camera_tag, bank_rank)` keys in the same order. Both
functions preserve every selected record field, source provenance and other root
metadata without mutating their inputs. Original counts and selection rule are
retained under `selection`; output counts and selection rule describe the subset.

From any working directory:

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109/selection/selector.py \
  /absolute/path/to/provided_v6_3_160.json \
  --baseline /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_surface_diversity_v6_2_20261108/exports/v6.2-surfaces-20261109-r5-final/prompts_all_160.json \
  --output-dir /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109/selection/exports_seed42 \
  --seed 42
```

The output directory must **not exist**. All files use exclusive creation:
`selected_v6_3_30.json`, `selected_v6_3_30.txt`, `selected_v6_2_30.json`,
`selected_v6_2_30.txt`, `selection_report.json`. A failed partial export is not
silently resumed or overwritten. Input bytes are rehashed before writing.
The report includes input byte hashes, canonical JSON hashes, verified snapshot
hashes, output hashes, pair keys, explicit quotas, distributions, both score means,
environment/prop/reference coverage and missing categories for both versions.

## Validation and method

Inputs require nonempty `version`/`selection_rule`, `counts`,
`device_source_mapping`, `prompts`, and a snapshot manifest path/SHA-256.
The actual all-160 counts use `candidates_per_bank: 10`, not the old
`selected_per_bank: 6`. There must be four devices, four views per device,
16 banks, ranks exactly 1–10 in every bank, unique prompt keys, correct UTF-8
text hashes, finite source/CTech scores in [0,100], string-list `prop_ids`
without duplicates, and string-list `creative_departures`. Environment,
relationship and CTech reference ID must be nonempty strings.

The approved-props schema needs no invented profile field or inferred
light/visual-signature/CTech-relationship metadata. Root
`snapshot_manifest_path`/`snapshot_manifest_sha256` are accepted; the real V6.2
r5 export instead supplies `provenance.validation_snapshot.manifest_path` and
`.manifest_sha256`, which are accepted explicitly without rewriting that source.
Missing or malformed root snapshot fields are not masked by the legacy fallback.
The CLI verifies snapshot bytes too; relative manifest paths resolve against the
input JSON's directory. The in-memory API validates declared snapshot hash syntax,
not filesystem contents; canonical JSON hashes are distinct from file byte hashes.

Algorithm `hp-approved-props-160-to30-v1`:

* Sort device/view banks lexicographically and records by rank. Give one slot to
  the first camera in each of the **first two distinct sorted devices**; give two
  slots to the other 14 banks. This fixed, intentionally simple quota allocation
  covers every bank and yields device totals **7, 7, 8, 8**. Quota location is
  not optimized; exact bank quotas are recorded, not inferred from a seed.
* Enumerate all ten singleton or all **45** two-record combinations per bank.
* Target **each full-source feature count × 30/160**, with weights:
  environment 6, device+environment 2, CTech reference ID 2, source relationship 3,
  source-score band `int(score//10)` 1, reference-score band `int(score//5)` 1,
  prop count 2, each approved prop ID 1, boolean creative departure 1, rank 0.5,
  bank+environment 1. Scores of 100 have band indices 10 and 20.
* Minimize weighted absolute feature deviation / 30, plus summed within-bank
  pair Jaccard similarity / 16, plus **1000 per additional exact-text duplicate**
  beyond its first occurrence, plus **1 per missing full-source environment**.
  Tokens are lowercased Unicode word tokens (`\b\w+\b`); duplicate text is
  case-sensitive exact text. Duplicate penalties apply across the whole subset.
* Use seed 42 by default and 12 bounded restarts, at most 12 full sorted-bank
  passes each. Restart zero starts with the first rank combination; others use
  a local seeded PRNG. Options are rank-lexicographic. Only improvements greater
  than 1e-12 move a coordinate; the first improving minimum wins ties, and equal
  objectives across restarts use the lexicographically smallest option vector.

**This is a deterministic coverage heuristic, not a probability sample and not
an optimality guarantee.** V6.2 is never independently optimized. Rank matching
does **not** establish semantic, prop, reference or environment equivalence.
Input schema and matching validate structure and hashes, not the truth of source
scores, approved-catalog membership or semantic quality.

## Focused tests

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover \
  -s /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109/selection \
  -p 'test_selector.py' -v
```

Tests load the real V6.2 source read-only and use synthetic modified copies.
CLI fixtures live only under this selection directory and are removed after the
test. No real V6.3 selection is performed.
