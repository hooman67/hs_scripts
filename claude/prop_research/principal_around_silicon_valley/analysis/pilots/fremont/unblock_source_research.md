# Fremont Gate-B source-unblock research

**Research date:** 2026-09-12  
**Scope:** lawful source methods for qualifying property observations and repeated commutes; no candidate scoring  
**Evidence ledger:** `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/pilots/fremont/evidence/unblock_source_claims_2026-09-12.csv`

## Bottom line

The commute blocker can be removed now with a no-registration, human-observed Google Maps protocol, which the user approved on 2026-09-12. The property blocker can be removed for **current active discovery** with a manual public MLSListings search plus official county/city joins, but the inspected public interface does not expose closed sales. A complete Gate-B property sample therefore still needs one external input: preferably a licensed agent/MLS export, or secondarily a user-created RentCast API key followed by a coverage audit. `[PRIMARY | HIGH | Gate A v2; INFERRED | HIGH | FRE-UNB-012; FRE-UNB-013]`

No unattended scraper should be built around MLSListings or Google Maps pages. Their offered browser interfaces are usable for manual research, but neither inspected site grants a bulk extraction right; Google explicitly prohibits mass downloads/bulk feeds, and MLSListings notes robot-exclusion headers and grants only a limited license. `[PRIMARY | HIGH | FRE-UNB-003; FRE-UNB-009]`

## Access classification

| Source/method | Classification | What it can supply | What it cannot establish | Recommendation |
|---|---|---|---|---|
| MLSListings public Fremont search and property pages | **Permitted manual workflow; no registration observed** | Current displayed Active/Contingent/Pending listings; public search controls include single-family, minimum bedrooms, square footage, lot size, and status; individual pages expose address and listing details | Public status controls inspected on 2026-09-12 do not offer Closed; coverage completeness, APN, usable yard, condition quality, and every HOA obligation are not guaranteed | Use only for a human-made active-inventory snapshot and source URLs; do not automate or scrape `[PRIMARY | MEDIUM | FRE-UNB-001 through 003]` |
| Alameda County parcel FeatureServer | **Public API/download** | APN, situs address, parcel geometry, use code, and parcel shape; query/extract capability | Bedrooms, living area, usable yard, current listing status, closed price, condition, and HOA | Join a manually supplied or licensed listing address to APN/geometry, then point-in-polygon to the official Fremont neighborhood `[PRIMARY | HIGH | FRE-UNB-004]` |
| City of Fremont Neighborhoods FeatureServer | **Public API/download** | Official neighborhood polygon identity and geometry | Listing or sale facts | Canonical submarket assignment after address/APN geolocation `[PRIMARY | HIGH | FRE-UNB-005]` |
| Alameda County ownership-transfer layer | **Public API/download but stale/incomplete for this use** | Recorded-transfer lookup and corroboration | Current 2026 cohort; bedrooms, finished area, lot/yard, HOA, condition, and reliable arms-length classification | Corroboration only; it cannot select qualifying comps `[PRIMARY | HIGH | FRE-UNB-006]` |
| Licensed MLS export supplied by an agent | **Credential/authorization required; user-supplied file** | Current statuses and recent closes with listing attributes, subject to the export's fields and license | Usable yard and true condition still require human review; APN may need county join | Preferred minimum external input; canonical property-observation source after field/coverage audit `[INFERRED | HIGH | FRE-UNB-007; FRE-UNB-013]` |
| RentCast property/listing APIs | **Credential required; free tier advertised, account/API key required** | U.S. property records searchable by geography and sold-date range, structural attributes, sale history; active sale listings include address, coordinates, type, beds, square footage, lot size, HOA when populated, status and listing history | Not an MLS of record; field availability varies; accuracy/coverage for Fremont is untested; no usable-yard or dependable condition determination | Optional secondary pilot if Hooman supplies a key; benchmark before use in scoring `[PRIMARY | HIGH for documented fields/access; UNKNOWN for Fremont coverage | FRE-UNB-014; FRE-UNB-015]` |
| Google Maps URLs + browser directions UI | **Permitted manual workflow; no API key** | A directions link for exact origin/destination and mode; browser UI supports planned Depart-at/Arrive-by estimates based on estimated traffic/transit schedules | No documented no-key machine endpoint, immutable history, or guarantee that actual conditions match | Use for planned and live human-observed commute rows; retain timestamps and screenshots/notes `[PRIMARY | HIGH | FRE-UNB-008 through 010]` |
| Google Routes API | **Credential and billing account required** | Automatable route computation under Google Maps Platform terms | Not available under the no-registration/no-billing constraint | Do not use unless the user later authorizes a billing-backed project/key `[PRIMARY | HIGH | FRE-UNB-011]` |
| 511 SF Bay Open Data | **Free credential required** | Traffic incidents/work zones/tolls; regional scheduled and real-time transit feeds after token request | The inspected traffic API does not provide arbitrary door-to-door automobile travel-time routing | Useful later for incident-state and transit corroboration, not a substitute for a drive-time engine `[PRIMARY | HIGH | FRE-UNB-016; FRE-UNB-017]` |
| Consumer-portal HTML/undocumented endpoints | **Unusable** | Nothing admissible for this project | Terms, stability, completeness, and provenance are inadequate | Do not scrape, reverse engineer, bypass controls, or treat snippets as evidence `[INFERRED | HIGH]` |

## Property-data unblock

### Path A — preferred: one licensed export

Ask a California buyer's agent with authorized MLS access to export two Fremont cohorts, preserving the source's raw status labels:

1. all Active, Contingent/Active-under-contract, and Pending detached single-family homes with at least three bedrooms; and
2. all Closed detached single-family homes with at least three bedrooms over the previous 12 months. If a polygon has fewer than 10 fully qualifying observations, request a separate 13–24-month cohort instead of silently pooling it.

The export should contain, when licensed for delivery:

```text
mls_name, mls_number, status, property_subtype, full_address, apn,
latitude, longitude, list_date, pending_date, close_date,
original_list_price, current_list_price, close_price,
bedrooms, bathrooms, living_area_sqft, lot_sqft, year_built,
hoa_monthly, dom, continuous_dom, sale_or_special_condition,
public_remarks, source_exported_at
```

This is the minimum reliable route because RESO states that it defines the data standard but does not provide MLS data; production access and credentials come from local MLSs after their licensing process. `[PRIMARY | HIGH | FRE-UNB-007]`

On receipt:

1. preserve the raw file and its license/retention note;
2. validate required columns, statuses, missingness, duplicates, and extraction time;
3. join exact address/APN to Alameda County parcel geometry;
4. spatially join the parcel/address point to the frozen City of Fremont neighborhood polygons;
5. calculate distributions only after exclusions and missing fields are visible; and
6. cross-check a sample of closes against county transfer records, recognizing the county feed's current lag.

### Path B — available today for active discovery only

A person can use the public MLSListings Fremont search in a normal browser, set `Single Family Residence`, `3+ Beds`, desired price/lot bands, and Active/Contingent/Pending, then transcribe candidate rows and their visible source URLs into the property-observation table. The public form currently exposes those filters, and the service states that a portion is available to the general public without a subscription. `[PRIMARY | MEDIUM | FRE-UNB-001; FRE-UNB-002]`

This path must remain manual. It is not proof of complete market coverage and does not provide the closed-sale cohort. Save retrieval time and the selected controls. Do not make unattended requests, paginate programmatically, or copy listing media. `[INFERRED | HIGH | FRE-UNB-003]`

### Yard, HOA, and condition handling

No inspected source turns lot size into “usable backyard.” Apply these evidence rules after an address is discovered:

- `lot_sqft`: copy the disclosed value and reconcile against parcel geometry; disagreement becomes `CONFLICTED`.
- `yard_evidence`: record `UNKNOWN`, `PHOTO_REVIEW`, `AERIAL/PARCEL_REVIEW`, or `VISITED`; do not infer usability from lot size alone.
- `hoa_monthly`: use the listing/export field only as provisional; verify actual dues, assessments, restrictions, and reserve documents during property diligence.
- `condition_evidence`: keep marketing remarks separate from observed defects. Use photos only for a screening flag; inspection/disclosures control the purchase decision.

These are methodological inferences, not property findings. `[INFERRED | HIGH]`

### Credentialed secondary fallback

RentCast advertises 50 free API calls per month but requires a free account/API key. Its property-record endpoint documents filters for city/state, property type, bedroom range, square footage, lot size, and `saleDateRange`, and returns structural attributes and sale history. Its active-sale listing schema includes address, coordinates, type, bedrooms, square footage, lot size, HOA when present, status, list price, and listing history. `[PRIMARY | HIGH | FRE-UNB-014; FRE-UNB-015]`

If Hooman supplies a key, use it only as a **secondary pilot**: query Fremont, paginate without exceeding the plan, spatially join to official polygons, and measure field missingness and disagreement against the agent export/county sample. Until that test is complete, source accuracy and Fremont coverage are `UNKNOWN` and confidence cannot support ranking.

## Commute-data unblock

### No-registration manual protocol

Google's official Maps URL documentation says directions URLs require no API key and display route, distance, and travel time. Its desktop help says `Depart at` and `Arrive by` change the route using estimated traffic and transit schedules. `[PRIMARY | HIGH | FRE-UNB-008; FRE-UNB-010]`

Use this stable launch template in a normal browser:

```text
https://www.google.com/maps/dir/?api=1&origin=<URL-ENCODED-ORIGIN>&destination=345%20Park%20Ave%2C%20San%20Jose%2C%20CA%2095110&travelmode=driving
```

For each of two representative residential origins in every Fremont polygon:

1. Record planned Tuesday, Wednesday, and Thursday estimates for arrivals at 8:00, 9:30, and 11:00 a.m.
2. Record paired returns departing 345 Park Ave at 3:30, 5:30, and 7:00 p.m.
3. Store observation timestamp, origin address/coordinates and selection rule, requested time, displayed primary route, typical low/high when shown, live ETA when observed at that time, alternatives, and incident note.
4. Repeat in a second non-holiday week. Keep planned estimates and contemporaneous live observations as different fields.
5. Save a screenshot or manually written evidence note for each observation; do not mass-download map content.

This yields 72 planned observations per weekly vintage (12 origins × six time/direction windows) and 144 across two weeks. That sample design is an `ESTIMATE | MEDIUM`: it is sufficient to test the source/protocol, not to establish a permanent commute distribution. Actual travel can differ, as Google's terms warn. `[PRIMARY | HIGH for limitation | FRE-UNB-009]`

Transit can use the same manual process with `travelmode=transit`, but store scheduled and actual/real-time evidence separately. Door-to-door time must include walking, transfers, waiting, and the final walk to 345 Park Ave.

### Why this cannot yet be unattended

- Google Maps URLs are keyless launch links, not a documented machine-readable route-duration feed. `[PRIMARY | HIGH | FRE-UNB-008]`
- Google's Routes API requires an API key and a billing-enabled account. `[PRIMARY | HIGH | FRE-UNB-011]`
- 511's data is free only after token request. Its inspected traffic endpoints cover incidents, work zones, and toll data—not arbitrary address-to-address driving time. Its transit feeds can help corroborate scheduled/observed transit after a token is supplied. `[PRIMARY | HIGH | FRE-UNB-016; FRE-UNB-017]`

Therefore, the lawful no-registration solution is a human observation sheet. The minimum input for automation is an authorized routing API key/billing project. A free 511 token is useful but insufficient by itself for driving-time routing.

## Exact external inputs needed

To remove both blockers now, the minimum is:

1. **Property:** one agent-generated MLS CSV/XLSX containing the two cohorts and fields above. The user expects this may be obtainable but has not yet confirmed it. If an export cannot include public remarks or media, omit them and keep yard/condition `UNKNOWN` until manual listing/disclosure review.
2. **Commute:** proceed with manual browser observations; the user approved this method. No credential is required. For later automation, supply a Google Routes or equivalent authorized routing key and its storage/retention terms.

An optional RentCast key can accelerate a secondary property-data trial, and an optional free 511 token can add incident/transit context. Neither is required for the preferred manual-plus-agent-export path.

## No-go findings

- No inspected public government source provides timely Fremont sale/listing status plus bedrooms, closed price, living area, lot, HOA, and condition in one property-level record. `[INFERRED | HIGH | FRE-UNB-006; FRE-UNB-013]`
- The MLSListings public interface is useful for current active discovery but does not expose Closed in the inspected public status controls. `[PRIMARY | HIGH | FRE-UNB-002]`
- Lot size is not usable-yard evidence; listing language/photos are not inspection evidence. `[INFERRED | HIGH]`
- No inspected no-key public API computes repeatable, traffic-aware, arbitrary address-to-address driving durations. `[INFERRED | HIGH | FRE-UNB-008; FRE-UNB-011; FRE-UNB-017]`
- 511 traffic incidents are context, not door-to-door commute measurements. `[PRIMARY/INFERRED | HIGH | FRE-UNB-017]`

## Assumptions and remaining unknowns

Confirmed operating choices and remaining assumptions:

- 345 Park Ave remains the primary commute destination.
- Manual browser observations are acceptable for Gate B even though the eventual tracker should be automated where licensed. This is user-confirmed.
- A buyer's agent can lawfully export the requested fields under their MLS agreement; the actual license must be checked.
- Exact candidate addresses and map screenshots can be retained in this private repository. This is user-confirmed.
- “Current inventory” means Active plus separately labeled Contingent and Pending; these statuses must never be merged silently.

Remaining operational questions:

1. Can Hooman obtain the specified export from an agent, and what storage/redistribution limits accompany it? He expects this is possible but must investigate.
2. Should Contingent and Pending count as available supply or only as demand/absorption signals?
3. Which two representative origins per polygon should be frozen after the first active-property snapshot?
4. Which representative properties should become the twelve origin points after an active-property snapshot is collected?
5. What recurring arrival/departure window emerges as the preferred schedule after the first manual comparison?

## Sources opened

All sources below were opened directly on 2026-09-12. Exact supporting excerpts are in the claim ledger.

- MLSListings, Fremont search results: https://www.mlslistings.com/search/result/city/Fremont
- MLSListings, Terms of Service: https://www.mlslistings.com/more/terms/
- Alameda County Assessor, Parcel Boundaries FeatureServer layer: https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Parcels/FeatureServer/0?f=pjson
- Alameda County Assessor, Ownership Transfer List FeatureServer: https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Assessor_Office_Ownership_Transfer_List/FeatureServer?f=pjson
- City of Fremont GIS, Neighborhoods FeatureServer layer: https://services2.arcgis.com/AVso4yDITKsybTJg/arcgis/rest/services/Neighborhoods/FeatureServer/0?f=pjson
- RESO, “RESO Web API”: https://www.reso.org/reso-web-api/
- RentCast, “Introduction”: https://developers.rentcast.io/reference/introduction.md
- RentCast, “Property Records”: https://developers.rentcast.io/reference/property-records.md
- RentCast, “Sale Listings”: https://developers.rentcast.io/reference/sale-listings.md
- Google for Developers, “Get Started with Google Maps URLs”: https://developers.google.com/maps/documentation/urls/get-started
- Google Maps Help, “Get directions & show routes in Google Maps”: https://support.google.com/maps/answer/144339?hl=en&co=GENIE.Platform%3DDesktop
- Google, “Google Maps Additional Terms of Service”: https://www.google.com/help/terms_maps/
- Google for Developers, “Set up the Routes API”: https://developers.google.com/maps/documentation/routes/get-api-key
- 511 SF Bay, “Open Data”: https://511.org/open-data
- 511 SF Bay, “Traffic Data”: https://511.org/open-data/traffic
- 511 SF Bay, “Open Data FAQs”: https://511.org/open-data/faqs
