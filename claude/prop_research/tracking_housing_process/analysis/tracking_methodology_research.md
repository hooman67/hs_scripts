# Housing-Market Tracking Methodology Research

**Research date:** 2026-09-10  
**Scope:** methodology and source stack only; no monitoring cities, thresholds, or skill implementation are selected here.  
**Evidence ledger:** `../evidence/source_claims_2026-09-10.csv`

## Bottom line

The best design is a **hybrid, vintage-preserving tracker**:

1. use an authorized MLS feed or agent-provided export for property-level listing history and matched comparables;
2. use official public datasets for slower, independently defined context;
3. use published aggregator datasets only as secondary cross-checks and only through an access method their terms permit; and
4. keep manual review for property-specific tax, insurance, condition, disclosures, and any source whose automation rights are unclear.

This recommendation is `INFERRED | HIGH`: no inspected public government source supplies timely, property-level listing events and closed-sale comparables at neighborhood resolution, while the inspected consumer portals explicitly restrict automated collection. A licensed or explicitly authorized source is therefore the clean way to obtain that layer. [E01-E05, E12-E16]

The tracker should issue **review alerts**, not “buy” calls. A price cut or falling median alone can reflect an undesirable property, a changing sales mix, seasonality, or delayed/revised records. `INFERRED | HIGH` [E02-E04, E07-E10]

## Source stack

Evidence status in this table applies to the proposed use of the source. Direct claims about what a publisher offers are recorded separately in the evidence ledger.

| Tier and source | Data and resolution | Access / cadence | Evidence; confidence | Recommended role | Important limitations |
|---|---|---|---|---|---|
| **Licensed MLS feed or agent export** using the local MLS's schema, preferably RESO Web API where offered | Individual listings, statuses, original/current list price, pending and close dates, closed price, property attributes, agent-only fields where licensed | Credentialed; near-real-time or scheduled export; price and terms depend on the MLS/data license | `PRIMARY | HIGH` for records delivered directly by the governing MLS; `UNKNOWN` until finalist geographies and entitlements are known | Canonical source for the target-home cohort and listing-level alerts | RESO standardizes transport; it does not itself grant data access. Coverage may cross more than one MLS. Retention and display rules are license-specific. [E01]
| **Redfin Data Center: Housing Market Tracker and property-type files** | Monthly city, ZIP, neighborhood, county, state and metro aggregates; weekly metro aggregates; separate monthly property-type dataset | Public download interface; weekly and monthly publications | `SECONDARY | MEDIUM` | Broad trend and cross-check; manually downloaded snapshots unless written permission authorizes scheduling | City/ZIP/neighborhood values use rolling three-month windows; weekly values use rolling four weeks; recent and historical values can be revised. Consumer-site terms prohibit automated crawling or querying without express written permission. Do not scrape listing pages. [E02-E06]
| **Realtor.com Research Data Library** | Monthly listing-side metrics down to ZIP; current and historical CSVs; national weekly file | Public download links; monthly local data | `SECONDARY | MEDIUM` | Human-only independent listing-side cross-check unless express permission covers the skill | Combines single-family and condo/townhome in its residential core files; warns of partial coverage and volatility in smaller geographies; reissues full history and may restate it. General terms prohibit scraping, automated data mining, and using content with AI systems. [E07-E10]
| **MLSListings public market reports** | Monthly county snapshots, with separate single-family and condo/townhouse reports in its covered area | Public PDF/manual; monthly | `PRIMARY | MEDIUM` for the reported MLS aggregate | Local sanity check against national aggregators; not the canonical micro-market series | County-level and report-oriented, not a stable row-level API. Some analyst material is subscriber-only. Relevance depends on finalist MLS coverage. [E11]
| **California Association of Realtors historical housing data** | County existing-SFR sales changes, median prices, unsold inventory index, and median market time | Public web page linking spreadsheets; historical series | `SECONDARY | MEDIUM` | Statewide county cross-check, especially where local MLS public reports differ | Survey-derived from more than 90 REALTOR associations; historical samples have been revised; county series are not seasonally adjusted. [E21]
| **FHFA House Price Index datasets** | Repeat-sales price indexes: monthly national/division, quarterly MSA and other series, and annual county/ZIP/tract developmental files | Public CSV/JSON/XML/XLSX downloads; source-specific release cadence | `PRIMARY | HIGH` at its published geography | Stable government benchmark for price direction; detect disagreement with listing-derived trends | Index, not a price level; many granular series are annual/developmental. Core indexes use conventional conforming mortgage transactions and do not represent every home or financing type. [E12-E14]
| **Freddie Mac PMMS** | National 15- and 30-year conforming fixed mortgage-rate averages; history since 1971 | Official XLSX download; weekly Thursday release | `PRIMARY | HIGH` for the national survey statistic | Financing-context input and payment scenarios | National average, not a borrower quote; based on qualifying applications submitted through Loan Product Advisor. [E15]
| **U.S. Census Building Permits Survey** | Authorized units at national, state, CBSA, county, and permit-issuing place levels | Official public files; monthly, year-to-date, annual | `PRIMARY | HIGH` for reported permits | Slow supply-pipeline context | Permits are not completions or listings and can be revised/benchmarked. Not a property-level signal. [E16]
| **County assessor, recorder, and tax collector** for each finalist | Parcel attributes, recorded transfers, assessed value and actual tax bill, depending on county | Official web search/open data where available; lag and access vary | `PRIMARY | HIGH` when matched to the exact parcel and record | Confirm a candidate's ownership, transfer, parcel, and tax facts | No common cross-county schema; recorder price may require document inspection; lag can be material. Endpoints must be selected only after finalists are known. `INFERRED | MEDIUM`
| **RentCast API (candidate paid supplement)** | U.S. property records, value/rent estimates, sale/rental listings, comps, and ZIP/city market statistics | API key; usage-tier pricing; documentation says internal storage and analytics are licensed uses | `SECONDARY | LOW` until benchmarked | Candidate for rent-vs-buy and lawful automated listing/rent ingestion if its coverage passes a pilot | Proprietary aggregation from public records, deeds, assessors, and online feeds; not an MLS-of-record; accuracy and source coverage require validation. Third-party terms may still apply. [E17-E19]
| **Zillow Research / consumer site** | Potential price, rent, and inventory series | Access attempt returned HTTP 403 during this audit | `UNKNOWN | UNKNOWN` | Exclude from the initial automated stack; reconsider through a documented, permitted export or agreement | The current page and terms could not be inspected, so neither reliability nor automation permission was verified. [E20]

### Access classification

- **Technically suitable for scheduled adapters, subject to a current terms check:** FHFA downloads and other government downloads/APIs whose published access method is honored. Freddie Mac's published workbook is a candidate for conservative polling against its release calendar. `INFERRED | MEDIUM` [E12-E16]
- **Safe after contract/authorization:** MLS/RESO feeds and paid APIs within their credentials, rate limits, retention, and display terms. `INFERRED | HIGH` [E01, E18]
- **Manual or conditional:** Redfin and Realtor.com published downloads. Their data pages invite downloads, but their general terms restrict automated querying/scraping; Realtor.com's terms also prohibit AI use. This audit does not interpret a download link as permission for unattended or agent ingestion. `CONFLICTED | HIGH` [E02-E10]
- **Never use:** HTML scraping, undocumented endpoints, CAPTCHA bypass, rotating identities, or a fallback scraper after an authorized endpoint fails. `INFERRED | HIGH` [E05, E10]

## What each layer can and cannot answer

| Question | Preferred evidence | Not sufficient alone |
|---|---|---|
| Is the broad market weakening? | FHFA repeat-sales trend plus two listing/sale aggregate series | One month's median sale price |
| Is a target-home cohort gaining negotiating room? | Authorized MLS records filtered to a fixed cohort: inventory, continuous DOM, price reductions, delist/relist behavior, pending/closed ratios, sale-to-original-list | Citywide all-property median |
| Is a particular listing unusually attractive? | Subject-property facts plus recent matched closed comps, active competition, listing history, disclosures, inspection, tax and insurance quotes | AVM, low asking price per square foot, or long DOM |
| Is waiting becoming more affordable? | Target cohort prices, current borrower-specific rate quotes, expected down payment, taxes, insurance, maintenance and alternative rent | National mortgage rate or price index alone |
| Is supply structurally changing? | Building permits, planning pipeline, completions where available, and current inventory | Permit counts alone |

These mappings are `INFERRED | HIGH`; they separate leading listing signals from lagging closed sales and property-specific diligence.

## Canonical data model

Use append-only raw snapshots plus normalized observations. Never overwrite a prior download with a publisher's revised history. This is necessary for reproducibility and unbiased backtests. `INFERRED | HIGH` [E04, E09, E13]

### 1. `run_manifest`

One row per run:

```text
run_id,started_at,completed_at,mode,config_version,code_version,
source_set_version,status,warning_count,error_count,report_path
```

### 2. `source_snapshot`

One row per fetched or manually supplied artifact:

```text
snapshot_id,run_id,source_id,retrieved_at,published_at,source_as_of,
source_url,http_status,content_type,bytes,sha256,local_path,
access_mode,license_version,terms_checked_at,parser_version,status,notes
```

`access_mode` is one of `PUBLIC_DOWNLOAD`, `PUBLIC_API`, `LICENSED_API`, `LICENSED_EXPORT`, or `MANUAL`. A new `snapshot_id` is created even when content is unchanged; the hash records that fact. `INFERRED | HIGH`

### 3. `market_observation`

One atomic value per row:

```text
observation_id,snapshot_id,source_id,source_record_id,metric_id,
period_start,period_end,published_at,observed_at,vintage,
geography_type,geography_id,geography_name,boundary_version,
cohort_id,property_type,transaction_stage,statistic,
value,unit,seasonal_adjustment,window_type,sample_size,
evidence_status,confidence,source_location,limitations
```

Required distinctions:

- `transaction_stage`: `ASKING`, `PENDING`, `CLOSED`, `ASSESSED`, `MODELED`;
- `window_type`: point-in-time, calendar month, rolling 28 days, rolling three months, quarter, or year;
- `seasonal_adjustment`: `SA`, `NSA`, or `NOT_APPLICABLE`;
- `statistic`: count, median, mean, ratio, share, index, percentile, or modeled estimate;
- `geography_id` and `boundary_version`: never join on display name alone;
- `vintage`: retrieval/publication version, retained even after later restatements.

These fields prevent the exact category errors identified in the source review. `INFERRED | HIGH` [E03-E04, E08-E09, E12-E14]

### 4. `property_observation`

For an authorized MLS/API export or user-supplied file:

```text
property_observation_id,snapshot_id,source_listing_id,source_property_id,
parcel_id,address_normalized,latitude,longitude,geography_ids,
status,status_date,list_date,pending_date,close_date,
original_list_price,current_list_price,close_price,
dom,continuous_dom,price_change_count,last_price_change_at,
property_type,beds,baths,living_area_sqft,lot_sqft,year_built,
hoa_monthly,new_construction,distressed_sale,source_url,
storage_permission,evidence_status,confidence,limitations
```

Retain the source's raw status and DOM fields as well as normalized versions. Link repeated listings to a property only when the identifier match is defensible; otherwise keep them separate and mark the relationship `UNKNOWN`. `INFERRED | HIGH`

### 5. Reference tables

- `source_registry`: owner, authoritative/secondary status, endpoint, cadence, expected lag, terms URL, permitted automation, retention rule, owner/reviewer.
- `metric_dictionary`: exact source definition, normalized name, unit, direction, denominator, exclusions, and transformation.
- `geography_crosswalk`: source geography ID to Census/ZIP/polygon IDs with effective dates.
- `cohort_definition`: immutable, versioned selection rules.
- `claim_ledger`: the repository-wide evidence schema from `RESEARCH_METHODOLOGY.md`.

`INFERRED | HIGH`

## Comparable-property cohorting

Do not use one citywide median as the target family's market. Maintain three nested views. `INFERRED | HIGH`

1. **Regional context:** metro/county, all relevant residential property types. This is the most stable view but least specific.
2. **Target-market cohort:** exact finalist boundary plus one property type and the family's broad price/size requirements. This detects whether suitable inventory is changing.
3. **Matched-comp cohort:** subject listing plus recent closed and active homes selected by a frozen rule.

The cohort definition must record:

- exact polygon or stable geographic IDs, not an informal neighborhood name;
- detached single-family, townhouse, and condo as separate cohorts;
- bedroom/bathroom bands;
- living-area band (begin with a declared band and tune it only through validation);
- lot-size and age/style bands where they materially affect local value;
- new construction, distressed/non-arm's-length sale, tenancy, and major-condition exclusions;
- lookback window and maximum distance;
- school-attendance boundary only when the boundary is verified for the relevant year;
- minimum usable sample rule and fallback hierarchy.

The fallback order should widen **time**, then **distance**, then **attribute bands**, recording every relaxation. Never silently substitute a ZIP for a neighborhood or mix condos into an SFR cohort to obtain a sample. `INFERRED | HIGH`

For every median, publish the count, 25th/75th percentiles where available, window, and cohort version. If the source does not provide enough information to assess sample adequacy, confidence cannot exceed `MEDIUM`. `INFERRED | HIGH`

## Cadence

| Cadence | Work | Rationale / status |
|---|---|---|
| Each authorized weekly listing refresh | New/active/pending/delisted/relisted records, price changes, continuous DOM, stale inventory, cohort fit | `INFERRED | HIGH`; timely negotiating signals require listing history. Public Redfin weekly data is metro-only and rolling 28 days. [E03]
| Monthly after each source's stated release | Closed sales, sale-to-original/final-list, PPSF distributions, inventory, pending ratio, reductions, cohort medians; reacquire full revised aggregate series and preserve a new vintage | `INFERRED | HIGH`; Redfin and Realtor both revise history. [E04, E09]
| Weekly | Freddie PMMS and borrower-specific quotes when financing is relevant | `PRIMARY/INFERRED | HIGH`; PMMS is published weekly but remains a national benchmark, not Hooman's quote. [E15]
| Quarterly | FHFA MSA/county series where available; local planning and employment context | `PRIMARY/INFERRED | MEDIUM`; useful confirmation, too slow/coarse for listing alerts. [E12-E14]
| Annual or release-driven | FHFA ZIP/tract series, Census final permits, parcel/tax refresh, school/hazard boundary versions | `PRIMARY/INFERRED | MEDIUM`; these are structural/context layers. [E12, E16]
| Event-driven | Source schema/terms changes, finalist changes, major rate or insurance events, boundary changes, failed freshness checks | `INFERRED | HIGH`

A cadence is not proof of freshness. Every adapter must test the source's own `last updated` or period field and alert when no new period appears. `INFERRED | HIGH`

## Opportunity signals

### Do not collapse the data too early

The report should show the raw observations first, then three distinct signal groups. A single weighted score may be added later only after backtesting. `INFERRED | HIGH`

### A. Market negotiating-power signal

For each fixed cohort, compare the latest value with its own seasonal history:

```text
supply_pressure = percentile(inventory or active listings)
seller_friction = percentile(price-cut share, continuous DOM, delisting/relisting)
demand_pressure = percentile(pending/active ratio, fast-pending share)
closing_pressure = percentile(sale-to-original-list ratio, closed-sale PPSF trend)
```

Higher supply and seller friction, combined with lower demand and closing pressure, create a **buyer-review condition**. These are directional constructs, not validated weights. `INFERRED | MEDIUM`

Use year-over-year or same-calendar-period comparisons and seasonally adjusted series where supplied. Never compare a rolling three-month city observation directly with a one-month county observation as though the windows match. `INFERRED | HIGH` [E03]

### B. Affordability signal

Report both cash and financed views:

```text
cash_entry_cost = purchase_price + estimated_closing_costs + immediate_capex

monthly_principal_interest = L * m * (1 + m)^n / ((1 + m)^n - 1)
monthly_carry = principal_interest + property_tax + insurance + HOA
                + maintenance_reserve - tax_benefit_estimate
```

All non-observed inputs remain `ESTIMATE`, and the tax-benefit term remains excluded unless modeled with Hooman's verified tax situation. The tracker should show sensitivity across down payment and rate assumptions rather than a single payment. `INFERRED | HIGH`

### C. Listing-level anomaly signal

Flag for human review when an eligible listing has several independent indicators, for example:

- asking PPSF below a matched-comp prediction interval;
- a material price-cut path rather than a one-time rounding change;
- continuous DOM high relative to the same cohort;
- active competition declining while recent matched closes remain stronger;
- a relist or fall-through that creates negotiating leverage.

Exact thresholds must be learned in the pilot and validated out of sample. A flagged listing is not a bargain until condition, disclosures, title, insurability, taxes, location externalities, and closed comps are checked. `INFERRED | HIGH`

### Alert states

- `NORMAL`: no unusual configuration.
- `WATCH`: one source family or one metric cluster is unusual.
- `REVIEW`: at least two independent source families and multiple metric clusters agree, with completeness above the configured gate.
- `PROPERTY_DILIGENCE`: a specific listing passes cohort screening; manual professional checks remain.
- `INSUFFICIENT_DATA` or `CONFLICTED`: never converted into a bullish or bearish score.

These state names and gates are proposed design choices, `INFERRED | MEDIUM`; calibration is still `UNKNOWN`.

## Validation and backtesting

### Source qualification pilot

Run one representative finalist end to end before implementing the other finalists. This is a learning dependency, because it establishes MLS jurisdiction, permitted access, stable identifiers, status semantics, duplication patterns, coverage, and realistic cohort sample sizes. `INFERRED | HIGH`

For the pilot:

1. compare a stratified sample of active, pending, sold, relisted, and price-reduced records across the licensed/export source and one secondary aggregate/listing source;
2. verify dates, original versus current list price, close price, DOM versus continuous DOM, property type, square footage, and geography;
3. reconcile selected closed sales against the county recorder/assessor after the expected recording lag;
4. calculate missingness, duplicate rate, revision size, status-lag distribution, and metric disagreement;
5. define thresholds only after observing the error distribution; and
6. document sources not found or fields that cannot legally be retained as `UNKNOWN`.

`INFERRED | HIGH`

### Backtest without look-ahead

- Store each source exactly as it appeared on each retrieval date. Re-issued historical files must become new vintages, not replacements. `INFERRED | HIGH` [E04, E09, E13]
- Evaluate each alert using only data available as of that run. A backtest using today's restated history is labeled **retrospective/revised**, not point-in-time. `INFERRED | HIGH`
- Compare against simple baselines: no alert, seasonally matched prior year, and broad metro trend. `INFERRED | MEDIUM`
- For market alerts, evaluate subsequent 3-, 6-, and 12-month cohort closing-price trend, sale-to-original-list movement, and inventory absorption. `INFERRED | MEDIUM`
- For listing alerts, evaluate eventual close discount versus the contemporaneous matched-comp interval, time to contract, and whether the listing was withdrawn. Do not use later-discovered property defects as if they were known at alert time. `INFERRED | MEDIUM`
- Report precision, false-alert rate, coverage, median lead time, and results by geography/property type. Do not optimize only for price direction. `INFERRED | MEDIUM`
- Freeze thresholds before the holdout period and perform walk-forward evaluation. Recalibration creates a new version. `INFERRED | HIGH`

An honest point-in-time backtest is initially limited because aggregator history is restated and the project has not yet accumulated vintages. This remains `UNKNOWN` until snapshots exist. [E04, E09]

## Automation architecture for the later repository-local skill

```text
versioned project config
        |
        v
source registry + access-policy gate
        |
        +--> official download/API adapters
        +--> licensed MLS/API adapter
        +--> manual-drop inbox validator
        |
        v
immutable raw snapshot + hash + run manifest
        |
        v
schema validation -> normalization -> identity resolution -> QA quarantine
        |
        v
append-only observations (DuckDB/Parquet or SQLite)
        |
        v
cohort metrics -> opportunity states -> evidence-labeled report
```

Architecture recommendation: `INFERRED | HIGH`.

### Required controls

1. **Fail closed on access:** an unknown or expired permission state disables an adapter; it never falls back to scraping.
2. **Immutable raw layer:** date-partitioned files, SHA-256, response metadata, source URL, parser version, and terms-review date.
3. **Schema contracts:** required columns, allowed units/statuses, value bounds, duplicate keys, and freshness checks. Unexpected columns quarantine the run.
4. **Idempotency:** rerunning the same snapshot does not duplicate normalized observations.
5. **Revision tracking:** compare each new vintage with the previous one and report revisions separately from new-period movement.
6. **Identity confidence:** exact MLS/property/APN matches are separate from probabilistic address matches.
7. **No credential leakage:** keys remain outside tracked files and logs; reports contain source IDs, not tokens.
8. **Human gate:** no automated contacting, offers, or trades; the skill generates a report and diligence queue only.
9. **Source-health report:** freshness, missingness, response status, schema drift, and last terms review precede market conclusions.
10. **Auditability:** every displayed number links to its observation, raw snapshot, metric definition, and source claim.

All controls are `INFERRED | HIGH`.

### Suggested project layout after implementation

```text
tracking_housing_process/
  tracking_housing_process.md
  config/
    finalists.yaml
    cohorts.yaml
    sources.yaml
  evidence/
    source_claims_YYYY-MM-DD.csv
  data/
    raw/<source>/<retrieval-date>/
    normalized/
  analysis/
    tracking_methodology_research.md
  runs/<run-id>/
    manifest.json
    source_health.csv
    observations.csv
    report.md
  .agents/skills/track-housing-market/
    SKILL.md
```

The layout is a proposed design, `INFERRED | MEDIUM`; create only directories with actual content.

## Recommended implementation sequence

1. Finish and audit the principal-residence finalist research.
2. Freeze exact finalist boundaries and target-home cohort rules.
3. Pilot one finalist and one representative source stack end to end.
4. Decide whether to obtain a licensed MLS export/feed and whether to trial a paid rent/listing API.
5. Validate coverage and definitions; set completeness and alert thresholds from observed data.
6. Implement the repository-local skill with official/authorized adapters and a manual-drop path.
7. Run in shadow mode; accumulate immutable vintages before treating backtest results as point-in-time evidence.
8. Only then fan out equivalent adapters/cohorts to the other finalists.

This ordering follows the project's explicit learning-dependency rule. `INFERRED | HIGH`

## Confidence and unresolved items

| Conclusion / unknown | Status |
|---|---|
| Hybrid architecture is preferable to relying on a single portal | `INFERRED | HIGH` |
| Fine-grained unattended tracking should use a licensed/explicitly authorized feed | `INFERRED | HIGH` |
| Redfin and Realtor aggregate files are useful secondary cross-checks | Evidence: `INFERRED` from `SECONDARY` inputs; confidence: `MEDIUM` |
| Scheduled ingestion of those public download endpoints is permitted | `CONFLICTED | UNKNOWN`; download interfaces exist, but inspected general terms restrict automation |
| RentCast is accurate enough for finalist-level rent and listing decisions | `UNKNOWN`; requires a benchmark pilot |
| One local MLS will cover every eventual finalist | `UNKNOWN`; resolve after cities are selected |
| Optimal alert weights and thresholds | `UNKNOWN`; must be learned without look-ahead |
| A complete historical point-in-time backtest can be created now | `UNKNOWN`; historical files are restated and no local vintage archive yet exists |

## Sources

Full source metadata, exact supporting excerpts, retrieval dates, limitations, and claim-level labels are in `../evidence/source_claims_2026-09-10.csv`. The principal sources opened were:

- Redfin Data Center downloads: https://www.redfin.com/news/data-center/downloads/
- Redfin Data Center methodology: https://www.redfin.com/news/data-center/methodology/
- Redfin terms: https://www.redfin.com/about/terms-of-use
- Realtor.com Research Data Library: https://www.realtor.com/research/data/
- Realtor.com terms: https://www.realtor.com/terms-of-service/
- California Association of Realtors historical housing data: https://www.car.org/marketdata/data/housingdata
- FHFA HPI datasets: https://www.fhfa.gov/data/hpi/datasets
- FHFA HPI technical description: https://www.fhfa.gov/research/papers/house-price-indexes-hpi-technical-description
- Freddie Mac PMMS: https://www.freddiemac.com/pmms
- U.S. Census Building Permits Survey: https://www.census.gov/construction/bps/index.html
- RESO Web API: https://www.reso.org/reso-web-api/
- MLSListings market reports: https://www.mlslistings.com/media-center/market-data-reports/
- RentCast API documentation: https://developers.rentcast.io/reference/introduction
- RentCast API terms: https://www.rentcast.io/terms-api
