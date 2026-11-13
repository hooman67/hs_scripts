# Fremont pilot candidate definition

**Pilot date:** 2026-09-12  
**Purpose:** validate the candidate boundary and evidence-collection method before comparative city research. This file does not rank Fremont or its submarkets.

## Decision unit

The pilot candidate is Fremont, California, decomposed into six pre-existing submarket hypotheses from the active project summary: Ardenwood, Centerville, Irvington, Mission San Jose, Niles, and Warm Springs. For this pilot, each name means the polygon with the identical `NAME` value in the City of Fremont GIS `Neighborhoods` layer—not a ZIP code, school attendance area, MLS area, or informal real-estate label. `[PRIMARY | HIGH | FRE-BND-001]`

The reproducible selection query is:

```text
https://services2.arcgis.com/AVso4yDITKsybTJg/arcgis/rest/services/Neighborhoods/FeatureServer/0/query?where=NAME%20IN%20(%27Ardenwood%27,%27Centerville%27,%27Irvington%27,%27Mission%20San%20Jose%27,%27Niles%27,%27Warm%20Springs%27)&outFields=OBJECTID_1,NAME,Acres,UPD_DATE&returnGeometry=true&returnCentroid=true&outSR=4326&f=json
```

The layer describes neighborhood areas from the General Plan 2030 Community Character chapter. It is maintained by the City of Fremont GIS Division. `[PRIMARY | HIGH | FRE-BND-001]`

## Submarket records and route-sampling anchors

| Submarket | Object ID | Polygon acres | Layer update field | Polygon centroid (lon, lat) | Use |
|---|---:|---:|---:|---|---|
| Ardenwood | 2 | 1,188.8069 | 20240913 | -122.05378079, 37.56541452 | Boundary assignment; centroid is only a route-sampling anchor |
| Centerville | 10 | 909.7388 | 20070201 | -122.00517903, 37.55422347 | Same |
| Irvington | 17 | 627.6808 | 20040617 | -121.96048559, 37.53109448 | Same |
| Mission San Jose | 21 | 2,626.2467 | 20070201 | -121.91044350, 37.53609095 | Same |
| Niles | 23 | 2,662.7205 | 20070201 | -121.98188876, 37.58552470 | Same |
| Warm Springs | 30 | 1,081.1352 | 20240801 | -121.91885127, 37.47938491 | Same |

The exact polygon—not its centroid—must determine whether a property belongs to a submarket. A centroid may begin route testing but cannot represent every origin inside a large polygon. `[PRIMARY | HIGH | FRE-BND-002 through FRE-BND-007; INFERRED | HIGH | FRE-BND-008]`

## Property-eligibility record

A property record is eligible for the hard-constraint screen only when all of these fields are captured:

- address and APN;
- closed-sale date and verified closed price;
- detached single-family property type;
- at least three bedrooms;
- private usable backyard, with the evidence source and any ambiguity recorded;
- finished area and lot area, even though no minimum size is frozen;
- HOA amount/status;
- condition and an explicit renovation allowance when relevant;
- parcel tax/assessment lines, insurance quote, and economic carry;
- polygon membership, assigned schools, route results, and parcel-level hazards.

After the 2026-09-12 Gate A revision added utilities to the housing ceiling, the working search band is approximately USD 750,000–1,050,000. Eligibility still depends on the USD 7,000/month economic-carry ceiling and reserve rules. The price band is a screening range, not proof of affordability. `[PRIMARY | HIGH | FRE-CRT-001; INFERRED | HIGH | FRE-CRT-002]`

## Commute test definition

The current target is no more than 60 minutes one way on the recurring Tuesday–Thursday office pattern, with 90 minutes as a bad-day boundary. The destination is now fixed at 345 Park Ave, San Jose, and arrival time is flexible. No repeated route observations have been collected, so no Fremont submarket can yet pass the commute constraint. `[INFERRED | MEDIUM | FRE-CRT-003; UNKNOWN | UNKNOWN | FRE-COM-001]`

Collect identical drive and transit samples from at least two representative residential origins inside each polygon for flexible arrival scenarios of 8:00, 9:30, and 11:00 a.m. and paired return windows. Store origin, destination, requested arrival/departure time, retrieval timestamp, displayed typical range, live estimate, incident state, mode, transfers, parking, walk time, and source. The origin count and time grid are methodology choices, not observed commute facts. `[ESTIMATE | MEDIUM | FRE-LES-003]`

## Exclusions and non-equivalences

- Citywide medians cannot establish availability of qualifying detached three-bedroom homes with usable yards.
- A school name, nearby location, or neighborhood label cannot establish attendance assignment.
- A neighborhood centroid outside a hazard polygon cannot establish that every parcel is outside it.
- Assessed value and transfer-tax-derived values are not substitutes for verified arms-length closed-sale prices.
- Nothing under a `legacy/` directory was used as evidence.
