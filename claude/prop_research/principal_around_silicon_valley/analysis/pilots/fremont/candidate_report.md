# Fremont source-and-schema pilot report

**As of:** 2026-09-12  
**Decision status:** `NOT READY FOR RANKING`  
**Gate B:** `NOT PASSED`  
**Scope:** source validation for six Fremont submarket hypotheses; no claim that Fremont or any submarket is best.

## Outcome

The pilot established a reproducible official boundary for Ardenwood, Centerville, Irvington, Mission San Jose, Niles, and Warm Springs. It also validated usable primary-source components for school directory/outcomes, parcel and tax lookup, a FEMA flood overlay, and transit infrastructure. `[PRIMARY | HIGH | FRE-BND-001; FRE-SCH-001 through FRE-SCH-005; FRE-TAX-001; FRE-HAZ-001; FRE-COM-003]`

It did **not** establish whether any of the six submarkets currently contains enough affordable, qualifying detached homes; whether any passes the commute requirement; which schools a representative property is assigned to; or whether a property passes the current hazard/insurance policy. Those are `UNKNOWN`, so no submarket may be scored, eliminated, or recommended. `[UNKNOWN | UNKNOWN | FRE-MKT-003; FRE-COM-001; FRE-SCH-006; FRE-HAZ-003]`

## What is validated

### 1. Boundaries

All six names resolve to City of Fremont General Plan neighborhood polygons. Property membership can therefore be repeated with a point-in-polygon join against the official geometry. The stored centroids are route-sampling anchors only. `[PRIMARY | HIGH | FRE-BND-001 through FRE-BND-007; INFERRED | HIGH | FRE-BND-008]`

This resolves a major ambiguity in the prior research design: “Mission San Jose,” for example, now means a specific official polygon, not a ZIP, school area, or informal listing label.

### 2. School source chain

CDE's directory provides active district/school identifiers, grades, coordinates, and update fields. Its 2024-25 CAASPP research file supports reproducible school-level cohort extracts. For a source test, grade-11 all-student ELA/math percentages meeting or exceeding standard were extracted for American, Irvington, Mission San Jose, and Washington high schools. `[PRIMARY | HIGH | FRE-SCH-001 through FRE-SCH-005]`

These figures are **not** a school ranking and do not establish assignment. They cover one grade/cohort and two state tests; they do not by themselves measure school climate, growth, elementary/middle outcomes, services, or family fit. Current assignment remains `UNKNOWN` because the FUSD locator was blocked in this environment and no address confirmation was obtained. `[UNKNOWN | UNKNOWN | FRE-SCH-006]`

### 3. Parcel and tax source chain

Alameda County provides official parcel, secured-tax-roll, transfer, and tax-rate services. The tax table is detailed enough to compute the ad valorem components for a specific tax-rate area: the FY2025-26 rows for Fremont TRA 12-1 sum to 1.1741%. `[INFERRED | HIGH | FRE-TAX-001]`

That is not a generic Fremont property-tax rate. A property must be joined to its actual TRA, tax bill, fixed/special assessments, and purchase-price assessment scenario.

### 4. Flood and transit source components

FEMA's NFHL layer exposes the fields needed to query flood zone and Special Flood Hazard Area status at a property location. No parcel was tested, so this validates the overlay method, not a safety result. `[PRIMARY | MEDIUM | FRE-HAZ-001]`

Warm Springs / South Fremont BART station and its rail lines are confirmed by BART. The 511 Open Data page confirms that Bay Area traffic/transit APIs are available with a token. Neither source establishes a door-to-door commute distribution. `[PRIMARY | HIGH | FRE-COM-002; FRE-COM-003]`

## Hard-constraint screen

| Submarket | Boundary | Current qualifying closed comps | Detached / 3+ bed / usable yard availability | Repeated commute | Current school assignment | Parcel hazards + insurability | Result |
|---|---|---|---|---|---|---|---|
| Ardenwood | PASS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Not screenable |
| Centerville | PASS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Not screenable |
| Irvington | PASS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Not screenable |
| Mission San Jose | PASS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Not screenable |
| Niles | PASS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Not screenable |
| Warm Springs | PASS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Not screenable |

“PASS” above means only that the candidate polygon is reproducibly defined. All other cells remain unknown under claims `FRE-MKT-003`, `FRE-COM-001`, `FRE-SCH-006`, and `FRE-HAZ-003`. An `UNKNOWN` is not a hidden fail and not a hidden pass.

## Post-pilot input update

On 2026-09-12, the user confirmed 345 Park Ave, San Jose as the primary destination, flexible arrival time, freely deployable invested savings, and that utilities belong inside the housing ceiling. The affordability model was revised to an approximate USD 750,000–1,050,000 search band. These updates remove the missing-destination blocker but do not supply qualifying closed sales or route observations. `[PRIMARY | HIGH | FRE-CRT-004; INFERRED | MEDIUM | FRE-CRT-002; UNKNOWN | UNKNOWN | FRE-COM-001]`

## Why current affordability remains unknown

The county ownership-transfer service describes itself as a two-year rolling list, but its latest Fremont `transfer_dt` was 2025-03-30 when queried on 2026-09-12. Its schema also lacks bedrooms, finished area, lot area, usable-yard status, and an arms-length flag. `[PRIMARY | HIGH | FRE-MKT-001; FRE-MKT-002]`

Therefore, county data alone cannot answer the actual question: recent closed prices for detached, three-plus-bedroom homes with usable backyards inside each official polygon. A licensed MLS export with the required fields, followed by an APN/address join and manual yard/condition review, is the lawful next source. Consumer-portal snippets were intentionally not substituted. `[UNKNOWN | UNKNOWN | FRE-MKT-003]`

## Why commute remains unknown

The Adobe destination is now 345 Park Ave, San Jose and arrival is flexible, but no repeated Tuesday–Thursday route sample has been collected. A centroid-to-downtown query would be false precision for large polygons such as Niles and Mission San Jose. `[UNKNOWN | UNKNOWN | FRE-COM-001]`

The next collection run should use two representative residential origins per polygon, the 345 Park Ave destination, flexible arrival scenarios of 8:00, 9:30, and 11:00 a.m., paired return windows, and the same observation schedule. It should separately store driving and door-to-door transit, including parking/walk/transfer time. This is a proposed protocol, not commute evidence. `[ESTIMATE | MEDIUM | FRE-LES-003]`

## Why current hazard clearance remains unknown

The FEMA NFHL service is usable for address/APN overlays, but no property was supplied. The accessible Fremont fire layer has a 2020 last-edit timestamp and all three records cite `CO 33-2007`, so it cannot satisfy the policy requiring the latest adopted fire map. The current OSFM page was blocked by the network edge. `[PRIMARY | MEDIUM | FRE-HAZ-001; PRIMARY | HIGH | FRE-HAZ-002; UNKNOWN | UNKNOWN | FRE-HAZ-003]`

No parcel has current earthquake/geologic overlays or a property-specific insurance quote. Neighborhood-wide “safe” labels would therefore be unsupported.

## Source-category completeness

| Source-plan category | Pilot result | Usable claim/source | What remains |
|---|---|---|---|
| Candidate boundary | Complete for pilot | `FRE-BND-001`–`008` | Snapshot geometry/version for production |
| Property availability and sold prices | Blocked | `FRE-MKT-001`–`003` | Authorized MLS export and qualifying-comp review |
| Commute | Blocked | `FRE-COM-001`–`003` | Office inputs, token/tool, repeated observations |
| Public schools | Partial | `FRE-SCH-001`–`006` | Address assignment; elementary/middle and multi-measure comparison |
| Crime/safety | Blocked | `FRE-SAF-001` | Comparable incident records or explicit coarser-geography treatment |
| Wildfire | Blocked | `FRE-HAZ-002`–`003` | Current adopted official layer and parcel overlay |
| Flood | Method validated only | `FRE-HAZ-001`, `003` | Parcel query, effective panel/source date |
| Property tax | Method validated only | `FRE-TAX-001` | Parcel TRA, tax bill, assessments |
| Every other source-plan category | Not collected | none | Remains `UNKNOWN`; see source log |

Gate B requires a complete claim in every source category plus repeatable property, commute, assignment, and hazard procedures. This bounded pilot intentionally stops rather than filling those gaps with weak proxies. Gate B is therefore `NOT PASSED`.

## Conclusion

**No Fremont location can yet be recommended or rejected.** Confidence is `HIGH` that the boundary and several source chains are reproducible, and `UNKNOWN` on the decision itself because all four central gates—qualifying supply/price, commute, assigned schools, and parcel hazard/insurance—remain unresolved.

The next step is not a broader city ranking. It is to resolve the four blockers using the revised schema in `schema_lessons.md`, then rerun this pilot and audit it before parallel candidate collection.
