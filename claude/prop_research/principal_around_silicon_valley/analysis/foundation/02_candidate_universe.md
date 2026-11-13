# Candidate-Universe Proposal (Draft v0.1)

**Status:** Candidate discovery only; no rankings or current city findings  
**Prepared:** 2026-09-10

Every inclusion below is a research hypothesis, not a recommendation. Inclusion has evidence status `SPECULATIVE` and confidence `MEDIUM` as a useful screening choice unless the row says it was explicitly required by the user. No candidate has passed affordability, commute, schools, safety, or hazard gates.

## 1. Candidate definition

A candidate record must have:

- a stable ID;
- jurisdiction and county;
- an explicit geographic boundary (official neighborhood, tract set, or documented polygon);
- applicable school district(s);
- two or more representative origin points when the area is geographically broad;
- a note identifying every metric collected at a coarser geography.

Citywide data can support discovery. It cannot be mixed with neighborhood data in a score without a visible geography-mismatch limitation.

## 2. Sequential pilot

Pilot **Fremont** end to end before fanning out. This is not because Fremont is favored; it is because the mandatory universe includes several distinct Fremont submarkets, making it a useful test of boundary definition, qualifying-home availability, parcel-assigned schools, commute origins, hazards, and cultural-fit evidence.

Initial submarket hypotheses to validate rather than assume: Centerville, Irvington, Mission San Jose, Niles, Ardenwood, and Warm Springs. Boundaries and any additions/mergers must be established before data collection.

**Learning dependency:** audit the Fremont pilot's source accessibility, definitions, sampling burden, and ledger fields. Revise the collection template once. Only then parallelize equivalent collection for the remaining candidates.

## 3. Required reconsideration set

| Candidate ID | City/cluster | Submarket scope to define | Inclusion basis | Evidence status / confidence |
|---|---|---|---|---|
| M-FRE | Fremont | Named submarkets, not one city average | Explicit project mandate; legacy generated candidate names | `SPECULATIVE`; `HIGH` that it must be researched, `UNKNOWN` on suitability |
| M-SMAT | San Mateo | Baywood/Aragon, Hillsdale, San Mateo Village, and other qualifying submarkets found by a boundary/market screen | Explicit project mandate | `SPECULATIVE`; `HIGH` inclusion, `UNKNOWN` suitability |
| M-PLE | Pleasanton | Split where schools, taxes/assessments, hazards, housing stock, or commute origins materially differ | Explicit project mandate | `SPECULATIVE`; `HIGH` inclusion, `UNKNOWN` suitability |
| M-DUB | Dublin | Define central/west/east or a better evidence-based split; preserve assessment/new-construction differences | User explicitly asked that Dublin be reconsidered | `SPECULATIVE`; `HIGH` inclusion, `UNKNOWN` suitability |
| M-BER | Berkeley | Define Berkeley submarkets; treat Albany, El Cerrito, and Kensington as separate comparison jurisdictions if screened | User explicitly asked that Berkeley be reconsidered | `SPECULATIVE`; `HIGH` inclusion, `UNKNOWN` suitability |
| M-WG | San Jose—Willow Glen | Establish a reproducible Willow Glen boundary | Explicit project mandate | `SPECULATIVE`; `HIGH` inclusion, `UNKNOWN` suitability |
| M-SCAR | San Carlos | Split only if school, hazard, housing, or commute evidence requires it | Explicit project mandate | `SPECULATIVE`; `HIGH` inclusion, `UNKNOWN` suitability |
| M-BEL | Belmont | Split only if school, hazard, housing, or commute evidence requires it | Explicit project mandate | `SPECULATIVE`; `HIGH` inclusion, `UNKNOWN` suitability |

## 4. Fresh comparators

These are deliberately included to test whether the inherited shortlist omitted a better trade-off. They must first pass the same low-cost hard-constraint screen.

| Cluster | Proposed candidates | Research purpose | Evidence status / confidence |
|---|---|---|---|
| San Jose comparison set | Cambrian, Rose Garden, Almaden Valley, Evergreen, Berryessa, and Santa Teresa | Determine whether Willow Glen is actually the best San Jose fit under the confirmed property and commute requirements | `SPECULATIVE`; `MEDIUM` |
| Near-office incorporated cities | Campbell, Santa Clara, Milpitas, Sunnyvale, Cupertino, and Los Gatos | Prevent a neighborhood-only shortlist from omitting nearby jurisdictional alternatives | `SPECULATIVE`; `MEDIUM` |
| Mid-Peninsula comparison set | Redwood City, Foster City, Burlingame, and Millbrae | Test the San Mateo/San Carlos/Belmont cluster against nearby alternatives with the same schema | `SPECULATIVE`; `MEDIUM` |
| Southern Alameda comparison set | Newark and Union City | Test whether the Fremont hypothesis is city-specific or part of a broader subregional trade-off | `SPECULATIVE`; `MEDIUM` |
| Interior East Bay comparison set | Castro Valley, San Ramon, Danville, and Walnut Creek | Establish the commute/property-space boundary around Pleasanton and Dublin | `SPECULATIVE`; `MEDIUM` |
| Near-coast comparison set | Pacifica and Half Moon Bay | Test the value placed on beach access against commute, property feasibility, and parcel hazards | `SPECULATIVE`; `MEDIUM` |
| South-county comparison set | Morgan Hill and Gilroy | Test the commute-versus-space frontier after commute thresholds are confirmed | `SPECULATIVE`; `MEDIUM` |

Candidate names are discovery labels only. Some are cities, some neighborhoods, and some unincorporated areas; the study must normalize them into explicit submarket units before comparison.

## 5. Scenario-contingent boundary cases

Research these only if Gate A makes the scenario plausible:

| Trigger | Boundary candidates | Purpose | Evidence status / confidence |
|---|---|---|---|
| Office attendance is rare and the family accepts a fragile/long commute | Santa Cruz, Scotts Valley, Aptos | Test the value of coastal/nature access under a remote-heavy work scenario | `SPECULATIVE`; `LOW` until commute rules are known |
| Full-time remote work is a credible, family-approved scenario | Folsom, Davis, selected Sacramento-area candidates | Retain a distant-control group without contaminating the office-access ranking | `SPECULATIVE`; `LOW` until work scenario is confirmed |
| The family accepts urban trade-offs or a different property form | Oakland/selected Oakland Hills, Alameda | Test urban/community alternatives; property-level hazard and insurance gates remain mandatory | `SPECULATIVE`; `LOW` until property/hazard preferences are known |
| Financing conditions or household budget materially change the derived price envelope or minimum-property specification | Additional Peninsula/South Bay candidates surfaced by the market screen | Avoid treating today's modeled USD 750,000–1,050,000 search band as permanent | `SPECULATIVE`; `LOW` until a changed scenario is confirmed |

## 5A. Later Seattle relocation phase

Seattle-area homes are in scope, but they will be evaluated as a separate relocation scenario after the Bay Area collection method passes Gate B. San Jose remains the primary Bay Area commute destination, and San Francisco access is a meaningful secondary factor. A Seattle home must not receive an artificial commute advantage in the Bay Area ranking; it requires its own office destination, attendance assumptions, taxes, climate/hazard profile, schools, and family-fit comparison. `PRIMARY | HIGH` for user-authorized scope; `INFERRED | HIGH` for phase separation.

## 6. Screen order and stopping rules

1. **Freeze Gate A constraints.** No candidate eliminations before thresholds are confirmed.
2. **Run the Fremont pilot.** Validate source access, schema, and time cost.
3. **Screen the required set plus fresh comparators** on only: qualifying-home feasibility, commute viability, lawful education path (if confirmed as a constraint), and any family-defined hazard/financial constraint.
4. **Retain `UNKNOWN`.** An inaccessible source or sparse sample is not a failure.
5. **Expand to submarkets** only for cities that pass or remain plausibly unresolved.
6. **Collect the full preference set** for the surviving submarkets using parallel agents with separate ledgers.
7. **Do not track markets yet.** The price-tracking project should consume only an audited shortlist, as required by the active project summary.

## 7. Anti-anchoring controls

- Present candidate tables alphabetically during collection; hide the legacy rank.
- Use the same schema and stopping rules for every candidate.
- Include at least one near-office, one Peninsula, and one East Bay fresh comparator in the full collection set unless a sourced hard constraint removes the cluster.
- Assign a separate disconfirmation pass to the provisional leader before any recommendation.
- Report a Pareto set (non-dominated trade-offs) before producing any weighted ordering.
