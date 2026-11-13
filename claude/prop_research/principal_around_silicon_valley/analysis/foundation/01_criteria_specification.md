# Principal-Residence Criteria Specification (v1)

**Status:** Gate A inputs recorded; approved for the first source-and-schema pilot, not final scoring  
**Prepared:** 2026-09-10  
**Scope:** Principal residence with practical access to Adobe's Downtown San Jose office  
**Governing method:** `/home/colligo/hs_scripts/claude/prop_research/RESEARCH_METHODOLOGY.md`

This document converts the prior brief into a testable decision specification. It does not endorse the legacy weights or rankings. Statements about the family's circumstances below describe what the active project summary or legacy brief records; they are not independently verified current facts.

## 1. Decision and unit of analysis

The decision is which **defined submarket** should advance to property-level diligence for a principal-residence purchase. A city is only a discovery/screening unit. It is too coarse for final comparisons because school assignment, commute origin, hazards, lot characteristics, taxes, and insurance can differ inside the same city.

The research units are:

1. **Regional/city screen:** retain or eliminate only on a confirmed hard constraint.
2. **Submarket comparison:** a documented boundary or a reproducible set of census tracts/ZIP-plus-neighborhood intersections.
3. **Property diligence:** parcel, address, assigned schools, tax bill, hazard overlays, insurance quote, condition, and route tests.

This is a research design decision, not a factual claim about any candidate.

## 2. Active inputs

The current, user-confirmed specification is maintained in:

- `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/gate_a/01_decision_inputs_v1.md`
- `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/gate_a/02_affordability_holding_hazard_policy.md`
- `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/gate_a/03_property_and_school_tradeoff_policy.md`

The table below is retained only to show how the inherited brief was triaged. Where it conflicts with the Gate A files, the Gate A files control.

| Input | Current treatment | Evidence status | Confidence | Required action |
|---|---|---|---|---|
| Principal residence with practical access to Adobe Downtown San Jose | Active decision statement | `PRIMARY` (active project artifact) | `HIGH` that it is the recorded objective; `MEDIUM` that every detail is still current | Confirm exact office destination, attendance pattern, and acceptable commute distribution. |
| Purchase ceiling of USD 2,000,000 | Superseded: price is derived from USD 5,000–7,000 monthly economic-carry ceiling and available capital | `PRIMARY` for current budget inputs; derived price is `ESTIMATE` | `HIGH` for inputs | Use the live affordability model. |
| Purchase within approximately three years; earlier for an exceptional deal | Active timing window | `PRIMARY` | `HIGH` | Apply the great-deal gate and recommended hold policy. |
| Detached house, at least 3 bedrooms, and a backyard | Active hard constraint | `PRIMARY` | `HIGH` | Interior-area and minimum-yard thresholds remain open; record rather than invent them. |
| Two young children, Brazilian spouse who values beach access, and a dog | Family-fit inputs | `QUOTED` from earlier user input in the active summary | `MEDIUM` | Reconfirm only details that change criteria; do not infer preferences from nationality or family status. |
| Canadian citizenship, Iranian birthplace, Adobe employment, and US immigration considerations | Scenario inputs, not location scores | `QUOTED` from earlier user input in the active summary | `LOW` for current legal/employment state | Reconfirm before any financial/legal conclusion; refer legal questions to qualified counsel. |
| Public-school quality matters strongly; Montessori and homeschooling are acceptable alternatives | Active preference and option set; former health-policy screen removed | `PRIMARY` | `HIGH` | Keep assigned public-school evidence distinct from alternatives and tuition. |

Source inspected for the first six rows: `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/principal_around_silicon_valley.md` (retrieved 2026-09-10). The final row is deliberately `UNKNOWN`; it must not inherit the legacy report's assumptions.

## 3. Constraint versus preference classification

No candidate may be eliminated until the corresponding threshold is confirmed. Until then, the labels below are **provisional design classifications**.

### 3.1 Provisional hard constraints

| ID | Constraint | Pass/fail measure | Current threshold |
|---|---|---|---|
| HC-01 | Purchase feasibility | Evidence that qualifying properties fit the live affordability model; do not use an all-home city median as the test | USD 7,000/month hard economic-carry ceiling; USD 6,000 target; price is derived |
| HC-02 | Minimum property utility | Bedrooms, private usable outdoor space, property type, and condition/renovation scope | Detached, 3+ bedrooms, backyard; area and minimum yard dimensions remain open |
| HC-03 | Commute viability | Door-to-door distribution for Tuesday–Thursday office windows, including disruption alternatives | 60-minute recurring target and 90-minute bad-day hard boundary (`INFERRED` interpretation) |
| HC-04 | Education viability | Assigned public-school evidence plus separately reported Montessori/private/home-school options | Strong preference for better public schools; no health-policy constraint |
| HC-05 | Insurability and hazard tolerance | Property-specific coverage plus hazard-policy tests | Apply the provisional policy in Gate A file 02 |
| HC-06 | Financial resilience | Purchase preserves reserves and passes rate/insurance/repair scenarios | USD 150,000 minimum post-close liquidity (`INFERRED`); income/debt qualification remains `UNKNOWN` |

**Elimination rule:** a candidate fails only when a current, correctly scoped observation violates a confirmed threshold. Low sample size, unavailable evidence, or a high citywide median produces `UNKNOWN`, not failure.

### 3.2 Preferences to compare after constraints pass

Weights are intentionally unset. The former 16/13/12/... weights are historical inputs only and must not be reused without a fresh elicitation.

| ID | Preference | Observable components | Main anti-hallucination rule |
|---|---|---|---|
| PR-01 | Commute quality and resilience | Median and upper-tail door-to-door time; mode choice; number and quality of alternatives; variability; office-day cost | Store route, origin, destination, date/time, mode, and query method. Never call one map estimate “the commute.” |
| PR-02 | Career optionality | Access to plausible employment clusters and transit; spouse career needs if relevant | Do not use raw job-board hit counts without a reproducible query, deduplication, date, and role definition. |
| PR-03 | Education quality and fit | Parcel-assigned schools; outcomes; climate; special programs; lawful private/home/independent options; travel burden | Keep government outcomes separate from third-party ratings; verify program rules directly. |
| PR-04 | Personal safety | Comparable violent/property incident rates and trends; pedestrian/traffic safety; family field observations | Match years, offense definitions, denominator, reporting coverage, and geography. Do not translate citywide crime into a block-level guarantee. |
| PR-05 | Belonging and inclusion | Foreign-born/language/ancestry context; relevant cultural institutions; hate-incident evidence; family observations and conversations | Demographics are context, not proof of welcome or hostility. Never infer belonging from race percentages alone. |
| PR-06 | Purchase value and carrying cost | Distribution of qualifying sold comps; active supply; price/sqft and lot utility; taxes; insurance; HOA; repairs; commute cost | Compare the same property filter and sold period. Asking price and sold price remain distinct. |
| PR-07 | Community and social infrastructure | Parent networks, civic events, recurring third places, tenure/owner occupancy, cultural groups, family field assessment | Separate observed institutions from subjective fit; avoid invented group counts or sentiment. |
| PR-08 | Property flexibility | Lot/yard usability; bedrooms; layout; ADU/garden/solar potential; HOA/zoning/permit constraints | Citywide “typical lot” is not a substitute for parcel data or actual qualifying inventory. |
| PR-09 | Hazard, environment, and resilience | Parcel wildfire/flood/fault/landslide/liquefaction exposure; air/noise/heat; water supplier; outage resilience; insurance | Treat maps as exposure indicators, not loss predictions. Finalists require parcel overlays and an insurance quote. |
| PR-10 | Nature, beach, and daily outdoor life | Door-to-door access to user-defined usable beach/nature destinations; parks, trails, dog infrastructure | “Nearest beach” is insufficient; define swim suitability, season, traffic window, parking, and family use. |
| PR-11 | Healthcare access | Door-to-door access to appropriate pediatric, emergency, and routine care | Confirm facility/service type and current operation from the provider or regulator. |
| PR-12 | Connectivity and home-work utility | Address-level broadband availability, upload/download options, cellular backup, outage history where available | Provider marketing at ZIP/city level does not prove service at an address. |
| PR-13 | Climate comfort | Temperature distributions, heat days, fog, rain, smoke exposure, and household preference | Use a common historical baseline and label future projections separately. |
| PR-14 | Resale/downside resilience | Supply constraints, buyer-pool concentration, transaction history through prior cycles, property-specific liquidity | Historical appreciation is not a forecast. Scenario returns are `ESTIMATE`, never observed evidence. |
| PR-15 | Spouse and whole-family enjoyment | Beach use, walkability, activities, cultural/linguistic connections, social opportunities, and each adult's stated priorities | Obtain preferences directly from each decision-maker; nationality is not a preference proxy. |

## 4. Measurement principles

1. **Preserve raw observations.** Scores, if later used, must be calculated from stored facts rather than typed by an agent.
2. **Use distributions, not a single point.** Commute, price, days on market, and climate require medians plus ranges/upper tails.
3. **Match the decision property.** Market analysis filters for the confirmed property type, bedrooms, interior size, yard/lot proxy, condition, and price.
4. **Separate levels.** City-level screening, submarket evidence, school-district facts, and parcel facts occupy separate fields; no silent substitution.
5. **Separate present from future.** Current observations, historical changes, approved projects, proposed projects, and forecasts are distinct columns.
6. **Separate preference from safety/legal review.** The research can identify issues; attorneys, lenders, insurers, inspectors, school administrators, and tax professionals verify decision-critical professional matters.
7. **Never score missingness as neutral.** `UNKNOWN` stays visible and blocks a decision-critical comparison.

## 5. Avoid double counting

The old categories overlap. The replacement model should enforce these boundaries:

- Commute performance belongs in PR-01; access to alternative jobs belongs in PR-02.
- Minimum size/yard is an HC-02 pass/fail test; extra space or flexibility belongs in PR-08.
- Purchase price and recurring cost belong in PR-06; future resale scenarios belong in PR-14.
- Wildfire/flood/fault, water, air, noise, extreme heat, and insurance consequences are analyzed once under PR-09; climate comfort alone belongs in PR-13.
- Demographic context belongs in PR-05; presence of actual recurring social institutions belongs in PR-07 or PR-15.
- Beach/nature access belongs in PR-10; it should not be embedded again in generic “spouse happiness.”

## 6. Gate A disposition

The user answered the five opening questions on 2026-09-11. The first Fremont pilot may now validate sources, collection fields, and feasibility. Final scoring remains blocked on comparable evidence across candidates and the unresolved details listed in Gate A file 01. The holding and hazard rules in Gate A file 02 are provisional recommendations and must remain visibly labeled `INFERRED` until the user adopts or revises them.
