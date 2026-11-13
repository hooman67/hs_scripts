# V6.3 writer: HP association-aware scene choices

Implemented 2026-11-09 as an isolated successor to frozen V6.2. Runtime
`v6.3-writer-runtime-r1-hp-associations`; catalogue
`hp-v6.3-approved-props-v1`, revision `v6.3-hp-associations-20261109-r1`.
Offline verification is complete; no new GPT-5.5 or image generations have
been performed. This is not a production deployment or an image-quality claim.

## Changes

- Compact laptop/printer environment associations connect ordinary subsettings,
  suitable supports and compatible approved objects. They are options, never
  frequency targets, repeated mandatory bundles or source-relevance evidence.
- Primary support, neutral output items, background furnishings and separate
  activity areas remain distinct. Pottery vessels must stay off printer supports.
- Six new environment-specific entries: bags/backpacks in Cafe and Education;
  pottery cups, bowls and plates in Creative Studio; an analog clock in Office.
  Bags are explicitly closed and unbranded. Clocks are explicitly unnumbered
  and unbranded. Their treatments must attach to the actual object.
- All paperweights and loose decorative stone props are excluded. The last
  inherited Office glass-paperweight entry is removed; the old Home stone
  arrangement stays absent. No replacement ornament is added. Stone furniture
  materials and approved coasters remain permitted.
- The catalogue contains 265 entries: 260 baseline entries minus one paperweight
  plus six approved entries. All 259 retained entries are unchanged.

The three-field request, ten-prompt schema, source scoring/sorting, 18 C-Tech
references, camera registry, global prop/phrase uniqueness and one complete-bank
repair are preserved. Laptop banks still need two round primary tables and
round tables for every Cafe candidate. Printer banks still need three support
families and five non-table supports, with dedicated standing access.

The new associations address laptops and printers only. Other inherited camera
records are preserved, not reinterpreted or newly evaluated.

## Approval and provenance

Hooman approved execution of the proposal and removal or replacement of rock
paperweights on 2026-11-09. The implementation chooses complete omission.
The six approval records and two explicit rejection records are in:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/approved_additions.csv`

The new bags reuse `laptop_bag`; studio vessels reuse `drinkware`, `food_bowl`
and `food_plate`. A new `clock` family spans wall/desk variants. Removed-object
phrases remain in the recognition lexicon so prose cannot silently bypass
catalogue removal. Recognition is not approval.

Canonical evidence, source limitations, original proposal and implementation:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/prompt_writer_v6_3/SUMMARY.md`

## Assets and use

System prompt:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/system_prompt.md`

Executable approved catalogue:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/approved-v6.3-20261109.catalog.json`

Pass exactly `smart_brief`, `source_messaging` and `camera_tag`. Both source
fields accept text or JSON. Use the V6.3 CLI or injected-provider runtime with
these version-matched assets, not a V6.2 catalogue.

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/cli.py check-catalog \
  --catalog /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/approved-v6.3-20261109.catalog.json
```

The standalone runtime has no V6.2 imports. Asset rebuilding alone reads frozen
V6.2, verifies all 28 baseline file hashes, compiles the explicit approvals and
writes the catalogue, recognition lexicon and release hash manifest:

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/build_v63_catalog.py
```

## Verification and remaining boundary

317 offline tests passed, including inherited regressions, new prop acceptance,
environment restrictions, family collisions, shelf contents, object-local
bag/clock safety, paperweight rejection and unchanged baseline hashes. After
type annotations were added, the affected runtime/CLI subset passed 38 tests.
Ruff correctness checks and Ty passed; Ty used the installed dependency source
paths because the cached tool did not discover UV's environment automatically.
No type diagnostics were suppressed.

```bash
cd /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline
PYTHONDONTWRITEBYTECODE=1 python -m pytest --import-mode=importlib \
  /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/source_messaging_v1_to_v6/versions/v6_3/tests -q
```

Offline checks establish the deterministic contract, not model compliance,
better scene quality or visible-image improvements. A fresh, lineage-preserving
text evaluation on the same 16 input banks is the next empirical gate. It was
not launched by this implementation.
