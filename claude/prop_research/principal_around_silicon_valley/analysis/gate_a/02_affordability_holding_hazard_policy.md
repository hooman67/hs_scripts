# Affordability, Holding, and Hazard Policy v2

**Status:** Provisional underwriting policy for research; not lending, tax, insurance, or engineering advice

**Prepared:** 2026-09-11; revised 2026-09-12

**Governing inputs:** `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/gate_a/01_decision_inputs_v1.md`

## Recommended working policy

1. **Budget to USD 6,000/month; never screen a property as affordable above USD 7,000/month.** Include mortgage principal and interest, property tax, required insurance, HOA, utilities, and a maintenance reserve. Tuition is outside this ceiling. `PRIMARY` for what the ceiling includes; `INFERRED | HIGH` for the USD 6,000 target.
2. **Model USD 300,000 and USD 400,000 down-payment cases.** The invested funds are freely deployable, but the second case still requires verifying liquidation tax cost and remaining liquidity. `INFERRED | HIGH`.
3. **Keep at least USD 150,000 liquid after closing, preferably USD 175,000–200,000 for a house with renovation or hazard uncertainty.** This is a household risk policy, not a universal financial rule. It roughly protects more than 12 months of the USD 7,000 ceiling plus a meaningful repair/move buffer. `INFERRED | MEDIUM`.
4. **Plan to hold at least seven years; prefer ten.** If a move inside five years becomes likely, continue renting unless a property has a separately validated exit/rental case. This recommendation reflects transaction friction and short-horizon market uncertainty; it is not a guaranteed break-even period. `INFERRED | MEDIUM`.
5. **Use hazard as a first-class cost and family-safety constraint.** A parcel cannot pass final diligence without current hazard overlays, an insurability check, and an actual insurance quote obtained before contingencies are removed. `INFERRED | HIGH`.

## Illustrative affordability envelope

The table is a screening model, not a borrower quote. It assumes:

- 30-year fixed mortgage at 6.76%, the Freddie Mac national average reported for 2026-09-10 (`PRIMARY | HIGH`);
- property tax at 1.20% of purchase price per year (`ESTIMATE | LOW` until parcel/location data);
- homeowners insurance at USD 300/month (`ESTIMATE | LOW` until property quote);
- utilities at USD 500/month (`ESTIMATE | LOW` until actual electricity, gas, water/sewer, trash, and connectivity costs exist);
- maintenance reserve at 1.00% of purchase price per year (`ESTIMATE | MEDIUM` as a planning convention, not an observed bill);
- no HOA, mortgage insurance, points, closing costs, renovation financing, or tax effects.

| Down payment | Economic carry ceiling | Approximate purchase price | Approximate billed P&I + tax + insurance + utilities | Maintenance reserve included in ceiling |
|---:|---:|---:|---:|---:|
| USD 300,000 | USD 5,000/mo | USD 738,000 | USD 4,385/mo | USD 615/mo |
| USD 300,000 | USD 6,000/mo | USD 858,000 | USD 5,285/mo | USD 715/mo |
| USD 300,000 | USD 7,000/mo | USD 979,000 | USD 6,184/mo | USD 816/mo |
| USD 400,000 | USD 5,000/mo | USD 816,000 | USD 4,320/mo | USD 680/mo |
| USD 400,000 | USD 6,000/mo | USD 936,000 | USD 5,220/mo | USD 780/mo |
| USD 400,000 | USD 7,000/mo | USD 1,057,000 | USD 6,119/mo | USD 881/mo |

**Interpretation:** under these assumptions, the useful initial search band is approximately USD 750,000–1,050,000, not the legacy USD 2,000,000 ceiling. The pilot may inspect slightly higher listings to learn about negotiation and sold-price distributions, but it must not label them affordable without a scenario that passes the monthly and reserve rules. `INFERRED | HIGH` given the assumptions; actual figures are `LOW` confidence until quotes, utility history, and parcel taxes exist.

Rate source: Freddie Mac, “Mortgage Rates,” retrieved 2026-09-11, https://www.freddiemac.com/pmms. The page reports a 6.76% average 30-year fixed rate as of 2026-09-10 and describes PMMS as a market benchmark. It is not Hooman's rate.

Reproducible calculation:

- `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/calculations/affordability_scenarios.py`
- `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/calculations/affordability_scenarios.csv`
- `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/evidence/gate_a_source_claims_2026-09-11.csv`

## “Great deal” gate

Buying earlier than planned should require all of the following:

1. It passes the USD 7,000 economic-carry ceiling under a current-rate scenario and a reasonable insurance quote.
2. It preserves the post-close liquid reserve.
3. It fits a credible seven-year life plan or has a separately underwritten rental/resale exit.
4. Price is compared with recent, genuinely comparable closed sales—not Zestimate-like valuations, citywide medians, or seller discounts from an aspirational list price.
5. Inspection, title, insurance, school assignment, commute, and parcel hazards pass; urgency is not a reason to waive diligence.

All five rules are `INFERRED`; confidence is `HIGH` that they reduce avoidable decision risk, not that they guarantee a bargain.

## Provisional hazard and insurance limits

### Hard fails before purchase

- Standard admitted-market coverage is unavailable and the remaining coverage structure is not reviewed for gaps, cost, and renewal risk.
- A property-specific required-insurance quote makes economic carry exceed USD 7,000/month.
- The household cannot absorb the quoted deductible plus temporary relocation and an immediate repair without breaching the liquid-reserve floor.
- A decision-critical hazard remains `UNKNOWN` at contingency removal.

### Default screen-outs, subject to an exceptional-value review

- CAL FIRE Very High Fire Hazard Severity Zone exposure.
- FEMA Special Flood Hazard Area exposure requiring flood insurance.
- More than one material site hazard (for example wildfire plus constrained evacuation, or flood plus known drainage/landslide concern) without expert review and a substantial price/cost advantage.

These are conservative family screening policies (`INFERRED | MEDIUM`), not claims that every property in a mapped zone is unsafe or uninsurable. Hazard maps indicate exposure; they do not predict an individual loss.

### Insurance stress test

- Obtain a real quote during diligence; portal estimates do not count.
- Re-run affordability at **2× the quoted annual premium**.
- Require the stressed case to remain at or below USD 7,000/month and retain at least 12 months of stressed housing cost after the largest applicable ordinary-policy deductible.
- Record earthquake coverage and deductible separately. The California Department of Insurance states that homeowners policies do not cover earthquake damage except for fire, and reports that CEA homeowner deductibles include 5%, 10%, 15%, 20%, and 25% options with stated exceptions (`PRIMARY | HIGH`).

The 2× multiplier is a conservative user policy (`INFERRED | MEDIUM`), not a forecast of California premiums.

Official context source: California Department of Insurance, “Wildfire Recovery and Readiness,” retrieved 2026-09-11, https://www.insurance.ca.gov/01-consumers/200-wrr/. The department states that insurers must provide specified wildfire-safety discounts and explains that the FAIR Plan provides limited fire/smoke coverage that may require additional coverage for other risks. Property-specific availability and price remain `UNKNOWN` until quoted.

Earthquake source: California Department of Insurance, “Earthquake Insurance,” retrieved 2026-09-12, https://www.insurance.ca.gov/01-consumers/105-type/95-guides/03-res/eq-ins.cfm.

## Sensitivity requirements for every finalist

Each finalist must show at least these scenarios:

1. Current mortgage benchmark, actual down payment, actual tax estimate, and quoted insurance.
2. Mortgage rate +1 percentage point.
3. Insurance at 2× quote.
4. Immediate repair of USD 25,000 and USD 75,000 from liquid funds.
5. Five-year forced sale, seven-year hold, and ten-year hold with appreciation explicitly modeled as scenarios—not facts.

No appreciation assumption may rescue a property that fails current cash flow or reserve constraints.
