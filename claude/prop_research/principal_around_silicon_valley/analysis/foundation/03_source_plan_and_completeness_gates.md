# Source Plan and Completeness Gates (Draft v0.1)

**Status:** Source-design stage; no candidate facts collected  
**Prepared:** 2026-09-10  
**Retrieval/access check for listed landing pages:** 2026-09-10

The URLs below are starting points for collection, not citations supporting a city conclusion. A collector must open the actual table, map layer, report, record, or result; capture the exact excerpt/row and query parameters; and add it to the claim ledger required by `/home/colligo/hs_scripts/claude/prop_research/RESEARCH_METHODOLOGY.md`.

## 1. Source plan by criterion

| Criterion | Preferred source and complete URL | Required unit/query record | Secondary/corroboration | Freshness / acceptance rule |
|---|---|---|---|---|
| Property availability and sold prices | Applicable county assessor/recorder plus MLS data obtained through a licensed professional. Alameda assessor: https://www.acassessor.org/ ; San Mateo Assessor-County Clerk-Recorder: https://www.smcacre.gov/ ; Santa Clara assessor: https://www.sccassessor.org/ | Address/parcel, sale date, sale price, property type, beds, finished area, lot, arms-length status where available | Redfin Data Center https://www.redfin.com/news/data-center/ ; Zillow Research data https://www.zillow.com/research/data/ ; listing portals for property discovery | Active listings <=7 days; sold snapshot <=30 days; use a common 12-month sold window and exact qualifying-home filter. Platform blocks must be logged, not bypassed with snippets. |
| Commute time and resilience | Caltrans PeMS https://pems.dot.ca.gov/ ; 511 SF Bay https://511.org/ ; official transit: BART https://www.bart.gov/schedules , Caltrain https://www.caltrain.com/ , VTA https://www.vta.org/ | Exact origin/destination, mode, weekday, departure/arrival time, date, incident state, transfers, parking/walk time | Reproducible Google/Apple route queries; in-person runs for finalists | Sample the confirmed office windows across multiple weekdays; report median and upper tail. Refresh finalist routes within 30 days and after service changes. |
| Career optionality | Employer career pages and reproducible searches for a frozen occupation/level list | Query terms, radius, location rule, result date, deduplicated employer/job IDs | Reputable job boards and BLS occupational data | <=30 days; job counts remain weak proxies unless deduplicated. Do not turn approximate counts into precise scores. |
| Public-school outcomes and assignment | California DataQuest https://dq.cde.ca.gov/dataquest/ ; California School Dashboard https://www.caschooldashboard.org/ ; official district boundary/enrollment tools | School ID, year, metric, subgroup where relevant, parcel/address assignment, district | NCES and reputable rating sites as contextual secondary evidence | Latest published school year, explicitly named. Parcel assignment must be rechecked for finalist addresses. |
| Lawful alternative/private/home-school options | California Department of Education private schools https://www.cde.ca.gov/sp/ps/ ; applicable CDE/CDPH pages and the program's own written policy | Program identity, legal category, grade coverage, admissions/policy date, address, availability confirmed by program | Direct written response from school/program; attorney/qualified professional for interpretation | Verify at every finalist run. No claim that a program satisfies the family need without direct current confirmation. |
| School immunization/legal policy, if relevant | California Department of Public Health “Shots for School” https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/Immunization/School/shotsforschool.aspx and current California statutes/regulations | Exact rule, covered school type, exception, effective date, official section/page | Written school policy; qualified California counsel or clinician for case-specific advice | Primary authority only for legal claims; verify at decision time. Never infer an exception from enrollment category. |
| Crime and safety | California DOJ OpenJustice https://openjustice.doj.ca.gov/ ; FBI Crime Data Explorer https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/home ; local police open-data portals | Offense definition, period, agency/geography, population denominator, reporting coverage | Local annual reports and traffic-collision/open-street datasets | Use a common multi-year period; flag partial reporting and jurisdiction/submarket mismatch. |
| Demographics | US Census data/API https://api.census.gov/data.html and https://data.census.gov/ | ACS table IDs, vintage, estimate/MOE, tract/place, denominator | Local planning reports only as corroboration | Latest suitable ACS release; show margins of error. Demographics cannot by themselves establish belonging. |
| Belonging/community fit | Official cultural/community organization pages, city calendars, libraries/parks, and direct family fieldwork | Named organization/event, current activity date, location, observed visit/interview notes | Reputable local journalism and user-provided community sources | Recheck activity within 90 days. Subjective assessments must be labeled `ESTIMATE` or recorded as user observation. |
| Wildfire | CAL FIRE Fire Hazard Severity Zones https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones plus local adopted maps | Parcel/address overlay, layer/version/date, responsibility area, distance only if relevant | Local fire authority; insurer inspection/quote | Latest adopted map; parcel-level for finalists; official classification is exposure, not a loss probability. |
| Flood | FEMA Map Service Center https://msc.fema.gov/portal/home plus local flood-control authority | Address/parcel, panel, effective date, zone, base-flood fields where applicable | Seller disclosures, elevation certificate, insurer/lender | Latest effective and preliminary maps; parcel-level before recommendation. |
| Earthquake/geologic hazards | USGS earthquake hazards/faults https://www.usgs.gov/programs/earthquake-hazards/faults and California/local official geologic maps | Parcel coordinates, map/layer/version, fault/liquefaction/landslide classification | Seismic-hazard disclosure and geotechnical review | Latest official map; do not reduce multiple hazards to unsupported “earthquake score.” |
| Insurance | California Department of Insurance https://www.insurance.ca.gov/ and property-specific quotes from licensed carriers/brokers | Address, coverage limits, deductibles, exclusions, admitted/non-admitted/FAIR components, quote date | Seller policy history only as context | Property-specific quote <=30 days before underwriting; city averages cannot pass this gate. |
| Water resilience | California DWR Urban Water Management Plans https://water.ca.gov/Programs/Water-Use-And-Efficiency/Urban-Water-Use-Efficiency/Urban-Water-Management-Plans plus the serving utility's adopted plan and shortage rules | Actual supplier, plan year, demand/supply scenario, shortage stage, parcel service | State Water Resources Control Board and local rate schedules | Latest adopted plan and current restrictions; do not infer a parcel's supplier from city name alone. |
| Air quality, heat, and climate | EPA outdoor air data https://www.epa.gov/outdoor-air-quality-data ; NOAA NCEI https://www.ncei.noaa.gov/ ; Cal-Adapt https://cal-adapt.org/ | Monitor/station or grid, period, pollutant/metric, historical versus projected scenario | Local air district; PurpleAir only as supplemental sensor evidence | Common historical period; projections labeled `ESTIMATE` and kept separate from observations. |
| Aircraft/transport noise | Official airport noise contour reports and local transportation noise elements for each surviving submarket | Contour year, metric (for example CNEL), parcel/location, source map | Field visit and calibrated measurements if warranted | Latest available official contour; do not use distance to runway alone. |
| Broadband | FCC National Broadband Map https://broadbandmap.fcc.gov/home followed by provider address qualification | Address, technology, advertised speeds, provider, check date | Direct provider orderability check and neighbor/field evidence | Address-level at finalist stage; ZIP-level service does not count. |
| Property tax, special assessments, HOA, and land-use flexibility | County tax collector/assessor parcel record, city/county planning code and permit portal, recorded CC&Rs/HOA documents | Parcel tax bill, assessed value, bond/assessment lines, zoning, overlays, recorded restrictions | Title report, agent, attorney, contractor | Parcel-specific before underwriting; generic effective tax rates are screening estimates only. |
| Healthcare | Official facility/provider pages and California licensed-facility lookup | Service type, address, operating status, route query | Health-system directories | Verify current service and travel time for finalists. |
| Nature, parks, dog access, and beach use | Official city/county/state park pages and county beach-water-quality program | Destination, rules, hours, season, water-quality status, exact route/time | Field visit and family evaluation | Check rules/status during intended season; “beach” must meet the family's defined use. |
| Market history and resale risk | County/MLS transactions; consistently defined Redfin/Zillow series only if methodology and geography match | Series name, property type, geography, start/end date, nominal/real, revision date | FHFA or other official broader index for context | Latest release. Historical change is `PRIMARY`/`SECONDARY`; forecasts and scenarios remain `ESTIMATE`. |

### Access note

During a command-line landing-page check on 2026-09-10, several official pages returned HTTP 403 and the two market-platform pages returned 403/429. This is `PRIMARY` evidence with `HIGH` confidence only about that automated access attempt—not about browser accessibility or data availability. Collectors must log access failures and use an authorized browser, downloadable dataset, official API, or licensed source; search snippets are never substitutes.

## 2. Required evidence objects

Each candidate receives separate staged files until central audit:

- `candidate_definition`: boundary, jurisdiction, school districts, route origins;
- `claims.csv`: the repository's full claim-ledger schema;
- `source_log.md`: every opened source and failed attempt, including retrieval date;
- `raw/`: permitted downloads or immutable query captures;
- `calculations/`: scripts and outputs derived only from recorded inputs;
- `candidate_report.md`: facts, unknowns, conflicts, and no ranking.

An agent report is not a source. During integration, a reviewer must follow each decision-relevant claim to the underlying opened source.

## 3. Completeness gates

### Gate A — Decision inputs frozen

Pass only when the five questions in `/home/colligo/hs_scripts/claude/prop_research/principal_around_silicon_valley/analysis/foundation/01_criteria_specification.md` are answered, hard thresholds are explicit, preference weights or an alternative decision method are approved, and criteria version `v1.0` is frozen.

### Gate B — Fremont pilot validates the method

Pass only when:

- candidate/submarket boundaries are reproducible;
- at least one complete claim for each source category can be traced from report to ledger to opened source;
- access failures and lawful alternatives are documented;
- property filters, commute sampling, school assignment, and parcel-hazard overlays can be repeated;
- the schema is revised for lessons from the pilot before parallel work begins.

No pilot result is a recommendation.

### Gate C — Hard-constraint screen

For each candidate, all confirmed hard constraints must be either `PASS`, `FAIL`, or `UNKNOWN` with supporting claim IDs.

- A `FAIL` requires current evidence at the correct unit and an explicit threshold comparison.
- Any `UNKNOWN` blocks elimination and blocks scoring; it triggers targeted research.
- Property-feasibility screening requires qualifying sold transactions, not a citywide median. The minimum sample size must be frozen after the pilot. If the sample is too small, extend the period or label `UNKNOWN`; do not pretend absence of observations proves absence of options.
- Commute screening requires the same office scenario and collection protocol for all candidates.
- Legal/school and hazard constraints require current primary authority.

### Gate D — Candidate evidence completeness

A candidate may enter comparative analysis only if:

1. **100% of hard-constraint fields** are resolved with `PRIMARY` or suitable `SECONDARY` support and at least `MEDIUM` confidence; no critical `CONFLICTED` field remains unresolved.
2. **100% of core comparison fields**—PR-01, PR-03, PR-04, PR-06, PR-09, and PR-15—have evidence or are explicitly declared non-applicable by the frozen criteria.
3. **At least 80% of remaining weighted preference coverage** has usable evidence. Coverage is the sum of approved criterion weights with non-`UNKNOWN`, non-`SPECULATIVE` evidence; missing fields receive no score and are not imputed.
4. Geography, property type, time period, units, and asking-versus-sold status are comparable or the mismatch is modeled explicitly.
5. Every material number has an as-of date, source location, excerpt/row, and refresh date.
6. A reviewer recomputes derived values from stored inputs and records their name/date.

### Gate E — Scoring and sensitivity

Scoring is allowed only after Gate D. Before viewing results:

- publish normalization functions, caps/floors, direction, and approved weights;
- keep pass/fail constraints outside the weighted score;
- calculate from the ledger with code; test missing values, units, and score bounds;
- show raw metrics beside normalized utilities;
- publish a Pareto comparison before a single ordering;
- run office-attendance, financing, hazard/insurance, and holding-period downside scenarios;
- run weight sensitivity (including leave-one-criterion-out and plausible weight ranges);
- report rank intervals/stability, not just point scores.

A narrow or unstable lead cannot support “clear winner” language.

### Gate F — Finalist diligence and recommendation

A submarket recommendation requires:

- current qualifying listing/sold-comp refresh;
- property-level tax, hazard, zoning/HOA, school assignment, and insurance checks on representative finalist properties;
- in-person commute and neighborhood visits at relevant times;
- a disconfirmation review aimed at overturning the leading conclusion;
- explicit reversal conditions and confidence per conclusion;
- professional verification flags for finance, tax, insurance, legal/immigration, schooling/health policy, and construction questions.

## 4. Parallel execution rule

After Gate B, parallelize only equivalent independent collection. Each agent owns a separate candidate directory or source-category file. The coordinator alone changes criteria, schemas, indexes, scores, and summaries. If one candidate uncovers a definition/source problem affecting all candidates, pause the fan-out, update the protocol, and rerun affected work.

