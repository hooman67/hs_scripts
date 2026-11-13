---
name: v_check
description: Refresh and rank current eight-seat Kia Carnival Hybrid LXS/EX/SX/SX Prestige new, used, and CPO deals near ZIP 95121, within roughly five hours' drive and no shipping. Read-only; never contact sellers.
---

# Kia Carnival deal check

Usage: `/v_check`

Find newly listed or newly attractive 2025–2027 eight-seat Kia Carnival Hybrid LXS, EX, SX, and SX
Prestige vehicles; compare new, leftover-new, used, and Kia CPO paths; and report what changed since
the previous run. This is a read-only research workflow. Never contact a seller,
submit Hooman's data, apply for financing, request a quote, reserve a vehicle, place a deposit, or
make a purchase without explicit approval.

## 1. Resume the durable project

Read these files completely before searching:

1. `/home/colligo/hs_scripts/claude/dotclaude/RESEARCH_RULES.md`
2. `/home/colligo/hs_scripts/claude/v_research/AGENTS.md`
3. `/home/colligo/hs_scripts/claude/v_research/CLAUDE.md`
4. `/home/colligo/hs_scripts/claude/v_research/PROJECT_STATE.md`
5. `/home/colligo/hs_scripts/claude/v_research/DECISIONS.md`
6. `/home/colligo/hs_scripts/claude/v_research/LEARNINGS.md`
7. `/home/colligo/hs_scripts/claude/v_research/research-plan.md`
8. `/home/colligo/hs_scripts/claude/v_research/research/foundation/SUMMARY.md`
9. `/home/colligo/hs_scripts/claude/v_research/listings/SUMMARY.md`

The five diagnostic questions are already answered in those files. Do not ask them again unless a
new material ambiguity appears.

## 2. Apply the fixed buyer filters

- Home ZIP 95121; no shipping.
- Search the Bay Area and Northern/Central California within roughly five hours' normal driving,
  including Sacramento and Fresno/Visalia. Los Angeles and farther markets are out of scope.
- Kia Carnival **Hybrid only**, model years 2025–2027, in LXS, EX, SX, or SX Prestige trim.
- Require eight seats on the exact VIN/build/window sticker. Reject any seven-seat VIP/captain's-
  chair package. Do not infer seating from trim alone.
- Prefer 50,000 miles or less, and approximately 30,000 or less when used savings versus new are
  modest.
- Target $40,000 OTD or less for used/CPO; for new vehicles the current absolute ceiling is
  $47,500 OTD. At the current 10% San Jose tax rate, use roughly $35,500–$35,900 including dealer
  fees as the initial $40,000-OTD alert threshold and roughly $42,600–$42,800 as the new-vehicle
  $47,500-OTD threshold, then refresh tax/fee facts when stale.
- Require clean/unbranded title, no structural/frame/flood/fire/lemon/odometer problem, credible
  seller, strong history and condition evidence, recall resolution, and an independent inspection.
- Kia CPO is preferred but not mandatory. Do not treat dealer “certified” language as Kia CPO.
- Treat appearance as material: record body/interior damage, stains, odors, worn trim, wheel damage,
  mismatched paint, and missing accessories whenever evidence is available.

Equipment rule:

- Hybrid is mandatory; the Carnival Hybrid began with model year 2025, so 2022–2024 vehicles cannot
  qualify even if an aggregator mislabels them.
- Eight-passenger seating is mandatory. Official matrices show eight seats standard across hybrid
  trims, but certain packages can substitute seven seats; verify the exact VIN.
- Rear-seat entertainment is optional. Record exterior and interior colors for every candidate.
- Exclude white exterior colors.

## 3. Refresh live inventory

Use the current date/time and search at least:

- KBB new and used/CPO hybrid searches for 2025–2027 within 300 miles of 95121, then enforce the
  five-hour road boundary rather than trusting marketplace distance labels.
- Official Kia new inventory for series `MAH`, checking 2025, 2026, and 2027 and anchor ZIPs 95121,
  Sacramento, and Fresno/Visalia where needed.
- CarMax, AutoTempest, Kia CPO inventory, and Kia-franchise dealer inventories in the Bay Area and
  Sacramento/Fresno corridors.
- At minimum, run separate trim searches for LXS, EX, SX, and SX Prestige; sort by price and inspect
  all used/CPO results likely to fit $40,000 OTD and new results likely to fit $47,500 OTD.
- At least two additional broad discovery sources or search-engine queries using the exact trim,
  year, California, and `VIN` terms.

When a page blocks direct retrieval, `https://r.jina.ai/http://...` may provide a readable snapshot.
Treat it as discovery evidence that may be cached; verify every serious lead on the seller's own
current inventory page. Record blocked sources explicitly and never convert a CAPTCHA or empty
response into “no inventory.”

For a Carvana URL containing `/vehicle/<vehicle_id>`, if the rendered page is blocked, query
`https://apik.carvana.io/merch/vehicledetails/api/v1/inspection/report/<vehicle_id>` to recover the
VIN and stock number, then query
`https://spinnerdata.carvana.io/spinnerdata/<stock_number>/spinnerData.json` for powertrain,
colors, equipment, keys and disclosed imperfections. Cross-check the VIN with NHTSA. Treat an
inspection response with year-0001 dates and all `passed`, `fixedOrReplaced`, and `na` values false
as an unpopulated template—not as evidence that the vehicle either failed or passed inspection.
If price, mileage, history or availability remain blocked, label them unavailable rather than
guessing; a mandatory-filter failure can still be resolved from verified powertrain/build data.

For every previously recorded VIN, recheck availability and price. Label the delta `NEW`, `PRICE
DROP`, `PRICE INCREASE`, `STILL LISTED`, or `SOLD/STALE`. De-duplicate by VIN.

## 4. Verify and normalize every serious lead

Capture:

- year, exact trim, VIN, stock number, seller, location, mileage, colors, and seating;
- dealer URL, discovery URL, and retrieval time;
- sale price, dealer/doc/e-file fees, mandatory accessories, and every discount condition;
- estimated California OTD: sale price + dealer fees + current 95121 use tax + provisional DMV/title
  fees, with the uncertainty range shown;
- estimated travel cost separately;
- title brand, owner count, personal/rental/fleet use, accident/damage, service history, open recalls,
  warranty/CPO terms, and visible condition;
- actual eight-seat configuration, hybrid powertrain, and whether any package changes the seats;
- seller type/reputation, contradictions, missing evidence, confidence, and next validation step.

For any serious new/leftover-new listing, separate customer cash, loyalty, finance, lease, military,
college, trade-in, and other conditional incentives. Owning a 2024 Kia Niro PHEV does not establish
eligibility for a discount; require the program number and stacking rules before counting one.

Use NHTSA VIN decoding only to validate what it actually returns; it does not prove exact trim,
hybrid equipment, or seating. Check the current model-level recall list and require a Kia
VIN-specific recall printout for any finalist, including proof for `26V232` / Kia `SC368` and the
2026 instrument-panel campaign `26V046` when applicable.

An aggregator's “clean history,” “great price,” or “certified” badge is not verification. Open the
dealer page, full history report when accessible, official warranty/CPO terms, and original window
sticker/build evidence. Surface contradictions instead of choosing the more favorable claim.

## 5. Rank and report

Lead with exactly one of:

- `DEAL FOUND` — at least one candidate clears all currently checkable gates; or
- `NO QUALIFIED DEAL TODAY` — none does.

Then show:

1. changes since the last run;
2. every qualified candidate in a compact comparison table;
3. the strongest near-misses and the exact reason each fails;
4. any new, leftover-new, or CPO alternative that materially changes the recommendation;
5. advertised price, estimated OTD, and effective cost including travel as separate figures;
6. material unknowns, contradictions, and blocked-source limitations; and
7. the cheapest next validation step.

Do not recommend travel until the seller has confirmed physical availability and supplied a
written, itemized OTD buyer's order plus the material history/condition disclosures. Any contact
step is a proposed next action that requires Hooman's approval.

## 6. Persist the run

Update `/home/colligo/hs_scripts/claude/v_research/listings/SUMMARY.md` with the new timestamp,
listing statuses, prices, evidence, and links. Update
`/home/colligo/hs_scripts/claude/v_research/PROJECT_STATE.md` with the completed batch, limitations,
open actions, and next exact step. Update `DECISIONS.md`, `LEARNINGS.md`, or `LONG_TERM_PLANS.md` only
when their durable contents changed.

Report a completed check even when no qualified vehicle exists; silence is not a result.
