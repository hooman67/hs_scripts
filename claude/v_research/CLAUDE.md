# Kia Carnival Deal Research — Project Operating Manual

**This is the stable source of truth for the project.** `PROJECT_STATE.md` contains the live
stopping point and current work.

Owner: Hooman Shariati. Created: 2026-09-21.

## 1. Goal

Find a legitimate, low-risk, strong-value **Kia Carnival Hybrid** that Hooman can inspect and collect
without shipping. Search model years 2025–2027 (the hybrid did not exist for 2022–2024) in LXS, EX,
SX, or SX Prestige trim, but require a VIN-specific eight-seat configuration. Benchmark finalists
against the completed 2021+ Toyota Sienna analysis rather than protecting the incumbent choice.

The project must optimize the whole purchase—not merely the lowest advertised number—across:

- out-the-door cost and travel cost;
- mileage, age, condition, and service history;
- title, accident, recall, and ownership history;
- manufacturer or credible third-party warranty coverage;
- seller reliability and transparency; and
- likelihood of dependable use for roughly the next decade.

## 2. Confirmed buyer profile and constraints

- Home ZIP: 95121.
- No vehicle shipping.
- Local purchase is preferred. Search up to roughly a five-hour drive from San Jose in normal
  traffic, including Sacramento and Fresno/Visalia, but exclude Los Angeles and farther markets.
- Required vehicle: Kia Carnival **Hybrid**, model year 2025–2027, in LXS, EX, SX, or SX Prestige.
  The exact VIN/build must seat eight. Seven-seat VIP/captain's-chair packages do not qualify.
  Rear-seat entertainment is optional.
- Toyota alternative: 2021 or newer Sienna; Platinum preferred, with Limited/XSE/XLE acceptable.
  AWD is strongly preferred but FWD is acceptable for a sufficiently better deal. Seven or eight
  seats qualify; if eight becomes mandatory, verify the exact build because premium Sienna trims
  generally seat seven and eight-seat XLE configurations are normally FWD.
- Credit score for financing/lease modeling: approximately 780/top tier, subject to lender approval.
- Model years: 2025–2027 only because hybrid is mandatory. Leftover 2025/2026 vehicles are welcome.
- Mileage: new or used is acceptable; for used vehicles, prefer 50,000 miles or less and strongly
  prefer approximately 30,000 miles or less when the discount over new is modest.
- Target price: $40,000 out the door or less; absolute ceiling $45,000 out the door.
- Purchase deadline: by December 2026. Compare current-new, leftover-new, CPO/used, financing,
  cash, and lease paths.
- Purchase method: cash, financing, and leasing are all open. Compare them explicitly rather than
  assuming one method is preferred.
- Existing vehicle: a 2024 Kia Niro PHEV. Check current Kia loyalty or owner incentives, but never
  count a conditional incentive until eligibility and stacking are verified in writing.
- No trade-in is planned.
- Expected annual mileage is low, and Hooman prefers to keep a purchased vehicle long term.
- Color is not a constraint, but every result must list exterior and interior colors. Exterior and
  interior must be visually well kept because appearance matters to the household.
- Official Kia CPO is desirable but not mandatory. A non-CPO vehicle can qualify when the seller,
  warranty, history, condition, and independent inspection collectively provide comparable
  confidence.

## 3. Safety and quality threshold

Automatically reject vehicles with any of the following unless Hooman explicitly changes the
rule:

- salvage, rebuilt, flood, junk, lemon-law buyback, or branded title;
- structural or frame damage;
- odometer inconsistency or unverifiable VIN;
- evidence of severe collision, water intrusion, fire, or airbag deployment;
- unresolved safety recall that cannot be remedied before delivery;
- material mechanical symptoms or a seller refusing an independent pre-purchase inspection;
- undisclosed mandatory add-ons or pricing that depends on inapplicable rebates; or
- a seller identity, title chain, or payment process that cannot be independently verified.

A single minor cosmetic incident, multiple owners, prior rental/fleet use, or cosmetic wear is not
an automatic rejection, but it must be disclosed, quantified, reflected in price, and evaluated
for long-term risk. Prior rental/fleet vehicles require additional scrutiny.

Neither a clean CARFAX/AutoCheck report nor “certified” wording proves a vehicle is problem-free.
Non-CPO finalists require an independent pre-purchase inspection. Kia CPO finalists should still
receive a buyer-focused inspection or equivalent documented verification when practical.

## 4. Source hierarchy

1. Primary evidence: seller inventory page and buyer's order, VIN-specific window sticker/build
   data, title/history documents, service records, official Kia warranty/CPO/recall material,
   NHTSA records, and an independent inspection.
2. Strong secondary evidence: CARFAX or AutoCheck, established pricing datasets, reputable
   automotive publications, and documented owner/problem datasets with known limitations.
3. Discovery-only evidence: Autotrader, Cars.com, CarGurus, Google vehicle listings, social posts,
   and other aggregators. Use them to discover vehicles, then verify against the seller and VIN.
4. Seller claims: useful leads but unverified until supported in writing or independently checked.

## 5. Working rules

- Persist findings to disk; chat history is not durable memory.
- Maintain state, decisions, learnings, long-term plans, and a canonical listing summary.
- Record full URLs, retrieval timestamps, VIN, stock number, location, mileage, and seller for each
  serious candidate.
- Preserve the exact advertised price and every qualification attached to it.
- Compare out-the-door cost, not list price alone. Separate vehicle price, tax, registration,
  documentation fee, mandatory accessories/add-ons, finance charges, travel, and immediate
  maintenance.
- Do not count trade-in, military, college-graduate, conquest, loyalty, financing, or other
  conditional discounts unless Hooman qualifies and the dealer confirms them in writing.
- Check cash and financed purchase paths independently. A lower financed sale price is not a deal
  if interest, origination cost, prepayment restrictions, or lost rebates erase the benefit.
- Normalize vehicles by year, mileage, history, warranty, condition, location, and included
  equipment before declaring one cheaper.
- Verify hybrid powertrain, trim, and eight-seat capacity from VIN/build/window-sticker evidence;
  dealer titles, search filters, and aggregator labels can be wrong.
- Search for contrary evidence and model-specific failure patterns, not only positive reviews.
- Mark listings sold, stale, or price-changed; do not silently retain obsolete recommendations.
- Make no seller contact or transaction without explicit approval.

## 6. File organization

```text
v_research/
├── AGENTS.md
├── CLAUDE.md
├── PROJECT_STATE.md
├── DECISIONS.md
├── LEARNINGS.md
├── LONG_TERM_PLANS.md
├── research-plan.md
├── research/
│   ├── foundation/
│       └── SUMMARY.md
│   └── sienna-comparison/
│       └── SUMMARY.md
└── listings/
    └── SUMMARY.md
```

Create raw-data or model-specific subfolders only when research begins and the material justifies
them. Do not create competing summaries.

## 7. Definition of success

Hooman receives a short, current, evidence-backed shortlist whose leading vehicle:

- is verified as a 2025–2027 Kia Carnival Hybrid in LXS, EX, SX, or SX Prestige trim with eight
  seats;
- has a clean and coherent title, accident, ownership, service, and recall record;
- is sold by a credible and accountable vendor;
- passes the required inspection and condition checks;
- has a written, fully itemized price with no surprise mandatory products;
- compares favorably with local market alternatives and a current new-vehicle baseline; and
- offers enough savings to justify its age, mileage, warranty position, and any travel.
