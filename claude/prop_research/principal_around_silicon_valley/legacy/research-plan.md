# Property Research: California Home Purchase (2026–2029)

## Goal

Find the optimal neighborhood and property in California (from Northern CA to Santa Barbara) that maximizes:
1. Career security for an AI engineer at Adobe (Downtown San Jose)
2. Family quality of life (two young daughters, Brazilian wife, dog)
3. Long-term real estate appreciation
4. Survivability and self-sufficiency potential

**Budget**: Up to $2,000,000
**Timeline**: Purchase within 3 years (by mid-2029)
**Minimum property**: 3BR, 1,700+ sqft, backyard

---

## Family Profile

| Factor | Detail |
|--------|--------|
| Hooman | Born 1991, AI engineer, Adobe (DTSJ office), Canadian citizen, born in Iran |
| Wife | Born 1992, Brazilian, homemaker, loves beaches |
| Daughter 1 | Born 2024, will need school ~2029–2030 |
| Daughter 2 | Due Dec 2026 |
| Dog | Needs walkable neighborhood |
| Immigration | TN visa, green card sponsorship in progress (EB-2/EB-3, Iran backlog concern) |
| Vaccination | Limited/no vaccination — needs schools with exemption-friendly policies or alternative schooling |

---

## Evaluation Criteria

### Primary Criteria (Weighted)

| # | Criterion | Weight | Description |
|---|-----------|--------|-------------|
| 1 | Job Proximity & Security | 16% | Commute time to DTSJ and SF; route reliability (single-point-of-failure roads like Hwy 17 penalized); traffic severity; density of AI/ML jobs within 45-min drive |
| 2 | School Quality & Options | 13% | GreatSchools rating; availability of Montessori, co-op, Waldorf, homeschool co-ops; CA personal belief exemption status for private/charter schools |
| 3 | Growth Potential | 12% | YoY appreciation trend; planned infrastructure (transit, commercial); rezoning/development pipeline; population growth trajectory |
| 4 | Safety | 11% | Violent crime rate per 1K; property crime rate; sex offender density; neighborhood walkability at night |
| 5 | Diversity & Inclusion | 10% | Racial/ethnic diversity index; immigrant-friendly attitudes; visible Middle Eastern / South Asian / brown-skinned residents; no history of racial incidents; political climate tolerant of immigrants; sanctuary city/county status |
| 6 | Price & Value | 10% | Median home price; price per sqft; $/lot-size ratio; how much house $2M buys here |
| 7 | Community & Social Bonds | 9% | Neighborhood cohesion; small-town feel vs. transient bedroom community; community events; mutual-aid culture; how easy it is to build deep friendships; Persian/Brazilian diaspora presence |
| 8 | Property Size & Type | 6% | Typical lot size; availability of 3BR+ with >5,000 sqft lot; SFH vs. townhouse mix |
| 9 | Survivability & Environment | 6% | Water source reliability; air quality (no flight paths); wildfire risk; earthquake zone; growing zone; well water feasibility |
| 10 | Beach Proximity | 4% | Drive time to nearest swimmable beach |
| 11 | Climate & Natural Disaster Risk | 3% | Wildfire zone (SRA/LRA); flood zone; earthquake fault proximity; extreme heat days |

### Additional Criteria (Qualitative — evaluated in Step 3 deep dives)

| # | Criterion | Why It Matters |
|---|-----------|----------------|
| 12 | Healthcare Access | Proximity to pediatric hospitals (Stanford Children's, UCSF, etc.); important with two young kids |
| 13 | Dog & Outdoor Infrastructure | Dog parks, trails, open space preserves; wife walks dog daily |
| 14 | Internet Connectivity | Fiber availability (AT&T Fiber, Google Fiber, Sonic); critical if remote work becomes necessary |
| 15 | Property Tax Rate | Mello-Roos districts, special assessments; can add $5K–$15K/yr to carrying cost |
| 16 | HOA Restrictions | Avoid HOAs that restrict gardening, chickens, solar, water collection, ADU construction |
| 17 | Spouse Happiness | Brazilian community/restaurants; Portuguese-speaking social groups; activities for stay-at-home mom with toddlers |

---

## Execution Model

- **Systematic**: Evaluate EVERY neighborhood in the defined geography (North CA → Santa Barbara)
- **Funnel-based**: Broad screening → Detailed scoring → Deep dive on finalists
- **Data-driven**: Use quantifiable metrics where possible; qualitative assessments where not
- **Persistent**: All results written to disk immediately after each evaluation — no data lives only in memory
- **Iterative**: Can re-run with updated criteria or expanded geography
- **Long-running**: Runs inside tmux (`tmux new -s prop-research`); survives SSH disconnects
- **Resumable**: If interrupted, reads `neighborhood_scorecard.csv` + `coverage_status.md` and continues from last completed item
- **Autonomous**: Once triggered with "run step N", executes to completion without human input

---

## Geographic Scope — Region Breakdown

From North to South, organized by macro-region:

### Region 1: Sacramento & Central Valley
- Sacramento metro (Folsom, Roseville, El Dorado Hills, Elk Grove, Davis)
- Stockton/Modesto (likely filtered out early but included for completeness)

### Region 2: North Bay / Wine Country
- Marin County (San Rafael, Novato, Mill Valley, Tiburon, Larkspur)
- Sonoma County (Petaluma, Sonoma, Santa Rosa, Sebastopol, Windsor)
- Napa County (Napa, American Canyon, Yountville)

### Region 3: East Bay
- Contra Costa (Walnut Creek, Concord, Pleasant Hill, Lafayette, Orinda, Danville, San Ramon)
- Alameda County (Fremont, Pleasanton, Livermore, Dublin, Castro Valley, Alameda, Berkeley, Oakland hills)

### Region 4: Peninsula & South Bay (Primary)
- San Mateo County (Redwood City, San Carlos, Belmont, Foster City, San Mateo, Burlingame, Millbrae, Pacifica, Half Moon Bay, Daly City)
- Santa Clara County (San Jose neighborhoods, Campbell, Los Gatos, Saratoga, Cupertino, Sunnyvale, Mountain View, Milpitas, Morgan Hill, Gilroy)

### Region 5: Santa Cruz & Monterey
- Santa Cruz County (Santa Cruz, Capitola, Scotts Valley, Aptos, Watsonville)
- Monterey County (Monterey, Pacific Grove, Seaside, Marina, Salinas, Carmel Valley)

### Region 6: Central Coast
- San Luis Obispo County (SLO, Arroyo Grande, Pismo Beach, Atascadero, Paso Robles)
- Santa Barbara County (Santa Barbara, Goleta, Carpinteria, Lompoc, Santa Maria, Solvang)

---

## Step 1: Macro Screening (Region-Level Filter)

**Objective**: Eliminate entire regions that fundamentally fail on deal-breaker criteria, so we don't waste time on neighborhood-level analysis for areas that can't work.

### Deal-Breaker Filters (ANY one eliminates the region)

| Filter | Threshold | Rationale |
|--------|-----------|-----------|
| Commute to DTSJ | > 2.5 hours one-way (non-rush) | Unsustainable even 2–3x/week |
| Commute route reliability | Single fragile route with history of multi-day closures as ONLY option | Can't risk being stranded |
| Median home price (3BR+, 1700+ sqft) | > $2.5M across entire region | Nothing in budget even at the low end |
| AI/ML job density within 60 min | < 50 open positions | Career risk too high |
| Violent crime rate | > 8 per 1,000 (region-wide) | Baseline safety threshold |
| Diversity | Region-wide diversity index < 0.2 AND < 5% non-white population | Not safe/comfortable for a brown Middle Eastern family |
| Water supply outlook | Critical shortage / mandatory rationing likely | Survivability concern |

### Data Sources for Step 1
- Google Maps / Waze for commute estimates (weekday 8 AM departure)
- Zillow/Redfin median price data by region
- LinkedIn/Indeed job search: "machine learning engineer" OR "AI engineer" within radius
- FBI UCR / local PD crime statistics
- CA DWR (Dept of Water Resources) drought monitor and groundwater basin status

### Output: Region Scorecard (CSV)

| Column | Description |
|--------|-------------|
| region | Region name |
| commute_to_sj_min | Minutes to DTSJ (weekday 8 AM, rush hour) |
| commute_to_sj_offpeak_min | Minutes to DTSJ (off-peak) |
| commute_to_sf_min | Minutes to SF Financial District |
| primary_route | Main highway/road (e.g., "101-S", "Hwy 17→880") |
| route_reliability | Reliable / Moderate / Fragile |
| route_alt_count | Number of alternative routes to DTSJ |
| median_price_3br | Median price for 3BR+ 1700+ sqft SFH |
| ai_jobs_60min | # AI/ML job postings within 60-min drive |
| violent_crime_per_1k | Regional average |
| diversity_index_avg | Average diversity index across region |
| pct_non_white | % non-white population |
| water_status | Adequate / Stressed / Critical |
| pass_filter | YES / NO |
| rejection_reason | If NO, which deal-breaker triggered |

---

## Step 2: Neighborhood Identification & Scoring

**Objective**: For each region that passes Step 1, identify all distinct neighborhoods/cities and score them across all criteria.

### Neighborhood Definition
- For cities > 50K population: break into recognized neighborhoods (e.g., "San Jose — Willow Glen", "San Jose — Evergreen")
- For cities < 50K: treat as single unit
- Use Zillow/Redfin neighborhood boundaries as canonical reference

### Scoring Rubric (1–10 scale per criterion)

#### Criterion 1: Job Proximity & Security
| Score | Definition |
|-------|-----------|
| 10 | < 15 min to DTSJ via reliable freeway (101/280/87); 500+ AI jobs within 30 min |
| 8 | 15–30 min to DTSJ, multiple route options, predictable traffic; 300+ AI jobs within 30 min |
| 6 | 30–45 min to DTSJ, route generally reliable; 100+ AI jobs within 45 min |
| 4 | 45–60 min to DTSJ, OR route has known reliability issues (single-lane mountain roads, frequent closures); 50+ AI jobs within 60 min |
| 2 | 60–90 min OR route has single-point-of-failure (e.g., Hwy 17 — windy, accident-prone, landslide closures); some jobs but sparse |
| 0 | > 90 min OR no viable commute route; minimal AI job presence |

**Route reliability factors** (penalize by 1–2 points):
- Single road with no alternative (e.g., Hwy 17, Hwy 1 stretches)
- Mountain pass prone to landslides, fog, or ice
- Rush-hour commute 2x+ the off-peak time
- History of multi-day closures (mudslides, accidents blocking both directions)
- Bridge-dependent (Bay Bridge, Golden Gate) — adds vulnerability but usually has alternatives

#### Criterion 2: School Quality & Options
| Score | Definition |
|-------|-----------|
| 10 | District avg GreatSchools ≥ 9/10 AND 3+ alternative schools (Montessori/Waldorf/co-op) within 10 min |
| 8 | District avg ≥ 8 AND 2+ alternative schools within 15 min |
| 6 | District avg ≥ 7 AND at least 1 alternative school within 20 min |
| 4 | District avg ≥ 6 OR alternatives available but > 20 min away |
| 2 | District avg ≥ 5, no alternatives nearby |
| 0 | District avg < 5, no alternatives |

**Note on vaccination**: In California, SB 277 eliminated personal belief exemptions for public schools. However:
- Private schools sometimes have higher exemption rates
- Homeschool / independent study programs have no vaccination requirement
- Charter schools vary
- Medical exemptions still available (though tightened by SB 276)
- Co-ops and forest schools are often outside the system

#### Criterion 3: Growth Potential
| Score | Definition |
|-------|-----------|
| 10 | 5-yr appreciation > 40%; new transit/commercial planned; prices still below peak; strong population inflow |
| 8 | 5-yr appreciation > 30%; some development pipeline |
| 6 | 5-yr appreciation > 20%; stable with moderate upside |
| 4 | 5-yr appreciation 10–20%; mature market, limited upside |
| 2 | 5-yr appreciation < 10%; stagnant or declining area |
| 0 | Declining prices; population outflow |

#### Criterion 4: Safety
| Score | Definition |
|-------|-----------|
| 10 | Violent crime < 1/1K; property crime < 10/1K; feels safe walking at any hour |
| 8 | Violent crime < 2/1K; property crime < 15/1K |
| 6 | Violent crime < 3/1K; property crime < 25/1K |
| 4 | Violent crime < 5/1K; property crime < 35/1K |
| 2 | Violent crime 5–8/1K; property crime > 35/1K |
| 0 | Violent crime > 8/1K; high-profile safety concerns |

#### Criterion 5: Diversity & Inclusion
| Score | Definition |
|-------|-----------|
| 10 | Highly diverse (diversity index > 0.7); large Middle Eastern / South Asian / Latino populations; sanctuary city; no recorded hate incidents; progressive political climate; visibly multicultural streetscape |
| 8 | Diverse (index > 0.5); meaningful non-white population; welcoming to immigrants; no racial tension history |
| 6 | Moderately diverse; some visible minorities; generally tolerant but not explicitly welcoming; few cultural institutions for non-white groups |
| 4 | Low diversity (index < 0.3); predominantly white; few immigrants; may feel unwelcoming but no overt hostility |
| 2 | Very homogeneous; history of racial incidents or unwelcoming attitudes toward minorities; "sundown town" reputation or similar |
| 0 | Actively hostile environment; documented hate crimes targeting Middle Eastern / brown people; white nationalist presence |

**Data sources for diversity scoring:**
- Census ACS: racial/ethnic composition, foreign-born %, languages spoken at home
- Simpson Diversity Index by census tract
- FBI hate crime statistics by jurisdiction
- SPLC hate group map
- Local news search for racial incidents
- Persian/Iranian business directories (restaurants, markets, cultural centers)
- Brazilian/Portuguese community organizations
- Mosque/cultural center presence (signals Middle Eastern community)
- Election results as proxy for political tolerance (not partisan preference — look at anti-immigrant ballot measures)

#### Criterion 6: Price & Value
| Score | Definition |
|-------|-----------|
| 10 | Median 3BR price < $800K; $2M buys 4BR+ with > 0.5 acre |
| 8 | Median < $1.2M; $2M buys 4BR with large yard |
| 6 | Median < $1.5M; $2M buys solid 3BR with good yard |
| 4 | Median $1.5M–$2M; $2M buys minimum acceptable (3BR/1700sqft/yard) |
| 2 | Median $2M–$2.5M; might find something at budget edge |
| 0 | Median > $2.5M; nothing in budget |

#### Criterion 7: Community & Social Bonds
| Score | Definition |
|-------|-----------|
| 10 | Small-town feel with active civic life; block parties, neighborhood watch, co-ops; diverse (Persian/Brazilian/immigrant families present); strong parent networks; people know their neighbors; low resident turnover |
| 8 | Active community events; good mix of families; local institutions (churches, clubs, sports leagues) that foster connection; some cultural diversity |
| 6 | Decent family presence; some organized activities; people are friendly but community isn't a defining feature; moderate turnover |
| 4 | Primarily a commuter/bedroom community; people keep to themselves; high turnover; few gathering spots or community events |
| 2 | Transient population; mostly renters; no neighborhood identity; isolated feeling |
| 0 | Hostile or fragmented community; high conflict; no social infrastructure |

**Indicators of strong community** (what to look for):
- Nextdoor activity and tone (helpful vs. complaint-driven)
- Local Facebook groups (buy-nothing groups, parent groups, neighborhood groups)
- Community gardens, tool libraries, little free libraries
- Annual events (block parties, holiday parades, farmers markets run by residents)
- Religious/cultural institutions that serve as social hubs
- Walkable "third places" (coffee shops, parks, plazas where regulars gather)
- Owner-occupancy rate (higher = more invested neighbors)
- Median years in residence (longer = more stable relationships)
- Small local businesses vs. chains (indicates neighborhood identity)

#### Criterion 8: Property Size & Type
| Score | Definition |
|-------|-----------|
| 10 | Typical lot > 1 acre; SFH dominant; room for garden, animals, well |
| 8 | Typical lot 0.25–1 acre; mostly SFH |
| 6 | Typical lot 7,000–10,000 sqft; SFH common |
| 4 | Typical lot 5,000–7,000 sqft; mix of SFH and townhomes |
| 2 | Typical lot < 5,000 sqft; dense, mostly attached homes |
| 0 | Condo/apartment dominant; no yards |

#### Criterion 9: Survivability & Environment
| Score | Definition |
|-------|-----------|
| 10 | Own well feasible; no flight path; no wildfire zone; excellent air quality; long growing season; water rights available |
| 8 | Municipal water reliable + some self-sufficiency options; good air; good growing |
| 6 | Water adequate; some environmental concerns (moderate fire risk OR moderate air issues) |
| 4 | Stressed water; under flight path OR in wildfire interface zone |
| 2 | Multiple environmental concerns; water uncertainty |
| 0 | Critical water issues; severe pollution; high multi-hazard risk |

#### Criterion 10: Beach Proximity
| Score | Definition |
|-------|-----------|
| 10 | < 10 min drive to swimmable beach |
| 8 | 10–20 min |
| 6 | 20–35 min |
| 4 | 35–50 min |
| 2 | 50–75 min |
| 0 | > 75 min |

#### Criterion 11: Climate & Natural Disaster Risk
| Score | Definition |
|-------|-----------|
| 10 | No wildfire zone; no flood zone; no major fault; < 10 extreme heat days/yr; mild climate |
| 8 | Minimal hazard exposure; 1 moderate risk factor |
| 6 | 1 elevated risk (e.g., moderate fire zone but defensible) |
| 4 | 2 moderate risks or 1 high risk |
| 2 | High wildfire + earthquake; or in floodplain |
| 0 | Multiple severe hazards; uninsurable or extremely expensive insurance |

### Data Sources for Step 2
- **Commute**: Google Maps (weekday 8 AM to Adobe DTSJ), Waze historical; route reliability from Caltrans closure history
- **Schools**: GreatSchools.org, Niche.com, CA DOE school finder, private school directories
- **Growth**: Zillow Home Value Index (ZHVI) historical; Redfin market trends; city general plans; transit project timelines
- **Safety**: CrimeMapping.com, NeighborhoodScout, local PD annual reports, SpotCrime
- **Price**: Zillow, Redfin, Realtor.com (filter: 3BR+, 1700+ sqft, SFH, sold last 12 months)
- **Property size**: Redfin lot size filter; county assessor parcel data
- **Community**: Nextdoor/Facebook group activity; local event calendars; owner-occupancy rate (Census ACS); median years in residence; cultural community directories
- **Environment**: AirNow.gov, CAL FIRE FHSZ maps, USGS fault maps, CA DWR groundwater, EPA flight path noise maps
- **Beach**: Google Maps drive time
- **Disaster**: FEMA flood maps, MyHazards (CA), ClimateCheck

### Output: Neighborhood Scorecard (CSV)

| Column | Description |
|--------|-------------|
| id | Unique ID (e.g., R4-SC-WillowGlen) |
| region | Parent region |
| city | City name |
| neighborhood | Neighborhood name |
| commute_sj_min | Minutes to Adobe DTSJ (rush hour) |
| commute_sj_offpeak_min | Minutes to Adobe DTSJ (off-peak) |
| commute_sf_min | Minutes to SF (rush hour) |
| commute_route | Primary route (e.g., "101-S", "Hwy 17 → 880") |
| commute_route_reliability | Reliable / Moderate / Fragile (single-point-of-failure) |
| commute_alt_routes | Number of viable alternative routes |
| ai_jobs_30min | AI/ML jobs within 30-min drive |
| greatschools_avg | Average school rating (district) |
| alt_schools_count | # Montessori/Waldorf/co-op/forest within 15 min |
| appreciation_5yr_pct | 5-year price appreciation % |
| development_pipeline | Notable planned projects |
| violent_crime_per_1k | Rate |
| property_crime_per_1k | Rate |
| median_price_3br | Median price 3BR+ SFH |
| price_per_sqft | $/sqft |
| what_2m_buys | Description of typical $2M property here |
| typical_lot_sqft | Median lot size |
| water_source | Municipal / well / both |
| water_reliability | Adequate / Stressed / Critical |
| wildfire_zone | Non / Moderate / High / Very High |
| flight_path | Yes / No (within 2 mi of major runway approach) |
| air_quality_aqi_avg | Average AQI |
| growing_zone | USDA zone |
| beach_drive_min | Minutes to nearest swimmable beach |
| flood_zone | Yes / No (FEMA 100-yr) |
| fault_proximity_mi | Distance to nearest active fault |
| fiber_internet | Yes / No |
| diversity_index | Simpson Diversity Index (0–1) for census tract |
| pct_foreign_born | % foreign-born residents |
| middle_eastern_presence | None / Some / Significant (Persian markets, mosques, cultural centers) |
| brazilian_latino_presence | None / Some / Significant |
| hate_incidents_5yr | Count of reported hate crimes in jurisdiction (last 5 years) |
| sanctuary_status | Yes / No / Partial |
| owner_occupancy_pct | % owner-occupied (vs rental) from Census |
| median_yrs_residence | Median years residents have lived there |
| community_events | Description of regular community activities |
| cultural_communities | Persian/Brazilian/immigrant community presence |
| score_jobs | 1–10 |
| score_schools | 1–10 |
| score_growth | 1–10 |
| score_safety | 1–10 |
| score_diversity | 1–10 |
| score_price | 1–10 |
| score_community | 1–10 |
| score_property | 1–10 |
| score_survival | 1–10 |
| score_beach | 1–10 |
| score_climate | 1–10 |
| weighted_total | Weighted composite score |
| tier | A / B / C / D |

### Tiering
- **Tier A** (weighted ≥ 7.5): Deep-dive candidates — proceed to Step 3
- **Tier B** (weighted 6.0–7.4): Strong contenders — proceed to Step 3 if < 20 Tier A neighborhoods
- **Tier C** (weighted 4.5–5.9): Acceptable but not ideal — document and set aside
- **Tier D** (weighted < 4.5): Eliminated — record reason

---

## Step 3: Deep Neighborhood Analysis (Top Candidates)

**Objective**: For Tier A (and top Tier B) neighborhoods, perform deep research that goes beyond aggregate statistics.

### 3a. Market Deep Dive
- Actual listings in $1.5M–$2M range right now (screenshot/link 3–5 representative properties)
- Sold comps in last 6 months
- Days on market trend (rising = cooling, falling = heating up)
- Price reduction frequency (% of listings with price cuts)
- Investor activity (% cash purchases, rental ratio)
- Upcoming developments that could affect value (positive or negative)
- Property tax rate including Mello-Roos and special assessments

### 3b. School Deep Dive
- Specific schools the property would be zoned for (elementary, middle, high)
- Individual school ratings and test scores
- Class sizes
- Named Montessori/Waldorf/co-op schools with:
  - Tuition
  - Vaccination policy (explicit)
  - Availability (waitlist status)
  - Philosophy alignment
  - Distance from target neighborhood
- Homeschool co-op groups active in the area
- California "independent study" charter options

### 3c. Community & Lifestyle
- Persian/Iranian community presence
- Brazilian community presence
- Portuguese-speaking social groups
- Mom groups / toddler activities
- Farmers markets, organic food access
- Dog parks and off-leash areas
- Hiking trails accessibility
- Cultural amenities (libraries, museums, community centers)
- Religious institutions (if relevant)

### 3d. Survivability Deep Dive
- Specific water district and their supply outlook (25-year projection)
- Well drilling feasibility (county regulations, depth to water table, cost estimate)
- Soil quality for food production
- Average frost-free days / growing season length
- Rainwater collection legality and feasibility
- Solar potential (roof orientation, tree cover, HOA rules)
- Nearest hospital / ER and drive time
- Nearest fire station and response time (relevant for wildfire areas)
- Backup power feasibility (generator, battery, solar)
- Cell coverage reliability

### 3e. Immigration & Legal Considerations
- County political climate (relevant for immigration comfort)
- Sanctuary city/county status
- Diversity index of the neighborhood
- Any local regulations affecting non-citizens (unlikely but worth checking)

### Output per Neighborhood (Markdown Report)
- Executive summary (2–3 sentence verdict)
- All metrics from Step 2 with citations
- Representative properties (3–5 listings with links)
- School options detail
- Community assessment
- Survivability assessment
- Pros/cons table
- Overall recommendation: STRONG BUY / BUY / HOLD / PASS

---

## Step 4: Financial Analysis & Comparison

**Objective**: For neighborhoods rated STRONG BUY or BUY in Step 3, perform detailed financial modeling.

### 4a. Purchase Scenarios

For each target neighborhood, model:
- **Conservative**: $1.5M purchase price
- **Mid-range**: $1.75M purchase price
- **Stretch**: $2.0M purchase price

For each scenario:
- Down payment required (20%, 25%, 30%)
- Monthly mortgage (P&I at current 30-yr fixed rate)
- Monthly property tax
- Monthly insurance (including fire if applicable)
- Monthly HOA (if applicable)
- Total monthly housing cost
- Required household income for 28% DTI / 36% DTI
- Comparison to current rent/housing cost

### 4b. Appreciation Modeling

For each neighborhood, project:
- **Bear case**: 2% annual appreciation
- **Base case**: Historical average appreciation rate continues
- **Bull case**: Accelerated growth (e.g., new transit line effect)

5-year and 10-year equity projections for each scenario.

### 4c. Cost of Living Comparison
- Grocery costs
- Utility costs (gas, electric, water, internet)
- Childcare costs (if wife needs help)
- Transportation costs (gas, car maintenance, tolls)
- Local tax implications (city vs. unincorporated)

### 4d. Investment Risk Assessment
- What could cause values to DROP in this area?
- Climate risk pricing (insurance availability and cost trends)
- Remote work impact on housing demand in this area
- Tech layoff sensitivity (what happened in 2022–2023?)
- Supply pipeline (new construction that could dilute value)

### Output: Financial Comparison Table (CSV)

| Column | Description |
|--------|-------------|
| neighborhood | Name |
| target_price | Purchase price |
| monthly_total | Total monthly housing cost |
| income_required_28pct | Income needed for 28% DTI |
| appreciation_5yr_base | Projected equity gain (base case) |
| appreciation_10yr_base | Projected equity gain (base case) |
| climate_risk_score | Insurance cost trajectory |
| overall_financial_score | 1–10 |

---

## Step 5: Final Ranking & Decision Framework

**Objective**: Produce a definitive ranked list with clear trade-off analysis.

### 5a. Head-to-Head Comparison Matrix

Top 5–10 neighborhoods compared across all dimensions with weighted scores.

### 5b. Trade-off Analysis

For each finalist, explicitly state:
- **What you gain**: The standout advantages of this location
- **What you give up**: The compromises you make
- **Deal-breaker test**: Is there anything here that could become untenable in 5–10 years?
- **Regret minimization**: If you buy here and X happens (tech crash, wildfire, drought, etc.), how bad is it?

### 5c. Timeline & Action Items
- When to start actively looking (based on market conditions)
- Pre-approval timeline
- Green card status consideration (should you wait for GC before buying?)
- Seasonal buying strategy (when are prices lowest in target areas?)
- Visit schedule (which weekends to tour which neighborhoods)

### 5d. Immigration Risk Assessment
- What happens if green card is denied / takes 10+ years (Iran EB backlog)?
- Can you maintain property if you have to leave the US?
- Should you buy in both spouses' names? (Wife's visa status matters)
- TN visa renewal risk while holding property
- Should you wait for a more stable immigration status before a $2M purchase?

---

## Step 6: Deep Research on Finalists

**Objective**: For the top 3 neighborhoods, do on-the-ground-level research.

### 6a. Specific Property Search
- Identify 5–10 specific properties currently listed or recently sold that match criteria
- For each: full analysis (sqft, lot, condition, renovation needs, rental potential)
- Estimate true cost (purchase price + immediate repairs/upgrades needed)

### 6b. Visit Planning
- Optimal time of year to visit (weather representative, school in session)
- Checklist for in-person neighborhood evaluation
- Drive-by checklist (weekday morning, weekday evening, weekend)
- Questions for neighbors
- Local real estate agent recommendations

### 6c. Expert Consultation List
- Immigration attorney (green card timeline and property ownership implications)
- Real estate agent specializing in area
- Financial advisor (mortgage strategy, tax implications)
- Home inspector recommendations
- Well driller consultation (if rural)
- Insurance broker (fire, flood, earthquake quotes)

---

## Record Keeping

### File Structure

```
prop_research/
├── research-plan.md              # This file
├── runs/
│   ├── step1_region_screening/
│   │   ├── region_scorecard.csv
│   │   └── step1_report.md
│   ├── step2_neighborhood_scoring/
│   │   ├── neighborhood_scorecard.csv
│   │   ├── tier_a_list.md
│   │   └── step2_report.md
│   ├── step3_deep_analysis/
│   │   ├── {neighborhood_slug}/
│   │   │   ├── market_analysis.md
│   │   │   ├── schools.md
│   │   │   ├── community.md
│   │   │   ├── survivability.md
│   │   │   ├── listings/         # screenshots, links
│   │   │   └── report.md         # consolidated report
│   │   └── ...
│   ├── step4_financial/
│   │   ├── financial_comparison.csv
│   │   ├── mortgage_scenarios.md
│   │   └── step4_report.md
│   ├── step5_ranking/
│   │   ├── final_ranking.csv
│   │   ├── tradeoff_matrix.md
│   │   ├── immigration_risk.md
│   │   └── decision_report.md
│   └── step6_deep_research/
│       ├── {neighborhood_slug}/
│       │   ├── specific_properties.md
│       │   ├── visit_plan.md
│       │   └── expert_contacts.md
│       └── ...
├── data_sources.md               # Curated list of reliable data sources
├── assumptions.md                # Key assumptions and when to re-validate
└── decision_log.md               # Record of choices made and reasoning
```

### Neighborhood Registry Schema (neighborhood_scorecard.csv)

| Column | Type | Description |
|--------|------|-------------|
| id | string | Unique ID (e.g., R4-SC-WillowGlen) |
| region | string | Parent region (1–6) |
| city | string | City |
| neighborhood | string | Neighborhood / area |
| step1_pass | bool | Passed regional screening |
| step2_weighted_score | float | Composite weighted score |
| step2_tier | string | A/B/C/D |
| step3_status | string | STRONG_BUY / BUY / HOLD / PASS / PENDING |
| step4_financial_score | float | Financial viability score |
| step5_final_rank | int | Final position |
| step6_status | string | DEEP_RESEARCHED / PENDING / N/A |
| last_updated | date | Last data refresh |

---

## Iteration & Maintenance Protocol

### When to Re-Run
- **Quarterly**: Refresh price data, crime stats, job market numbers
- **On trigger**: New transit project announced, major employer opens/closes, immigration status changes
- **Annually**: Full re-run of Steps 1–2 to catch shifting markets

### Decision Timeline

| Date | Milestone |
|------|-----------|
| 2026 Q3 | Complete Steps 1–3, identify top 5 neighborhoods |
| 2026 Q4 | Complete Steps 4–5, narrow to top 3 |
| 2027 Q1 | Begin Step 6; get mortgage pre-approval |
| 2027 Q2–Q4 | Active property search in top neighborhoods |
| 2028 | Purchase window (or extend based on immigration status) |
| 2029 (latest) | Final purchase deadline per original goal |

### Immigration-Dependent Decision Tree
```
IF green card approved or I-485 pending (EAD in hand):
  → Proceed with purchase; full flexibility
ELIF TN visa stable and employer committed:
  → Proceed but ensure liquid reserves for 6+ months mortgage if job change needed
ELIF immigration uncertain:
  → Consider renting in target neighborhood first (1-year lease as trial)
  → OR purchase in wife's name if she has independent status
  → OR delay purchase until status resolves
```

---

## Quality Guidelines

- **Cite sources**: Every data point should reference where it came from and when it was retrieved
- **Verify recency**: Real estate data older than 6 months is stale — always check dates
- **Ground-truth**: Don't rely solely on aggregate stats — look at actual listings and sold properties
- **Be honest about uncertainty**: Flag assumptions, distinguish "data says" from "I estimate"
- **Update, don't append**: When data changes, update the entry — don't just add a new row
- **Photos over descriptions**: For Step 6, capture actual streetview/listing photos where possible
- **Bias check**: Am I rating a neighborhood high because data supports it, or because it "sounds nice"? Always refer back to the scoring rubric.

---

## Special Considerations for This Search

### California Vaccination Laws & Schooling
- **SB 277 (2016)**: Eliminated personal belief exemptions for K–12 public and private schools
- **SB 276 (2019)**: Tightened medical exemption process
- **Options for unvaccinated children**:
  1. Homeschool (no requirement) — can use umbrella/charter school for resources
  2. Independent study programs through public school districts
  3. Some private schools with high medical exemption rates (research specific ones)
  4. Homeschool co-ops (not subject to same rules)
  5. Virtual/online charter schools (enrollment may not require vaccines)
  6. Move to a state with philosophical exemptions (if CA becomes untenable)
- **Action**: In Step 3, specifically identify schools/programs that accommodate this

### Iranian Birth Country & Green Card
- EB-2/EB-3 for Iran has significant backlog (potentially 5–10+ years)
- Consider EB-1 extraordinary ability route (shorter wait)
- National Interest Waiver (NIW) another option for AI engineers
- Property ownership is NOT affected by immigration status in CA
- But ability to STAY in the US long-term affects whether buying makes sense
- **Action**: Step 5 includes immigration risk assessment; consider consulting attorney before purchase

### Remote Work Hedge
- If remote work becomes permanent/more common, job proximity weight decreases
- Consider: Adobe's remote work policy trajectory
- Consider: Would you take a remote-only role if it meant living in a better area?
- **Action**: Score neighborhoods with AND without the job proximity criterion to see what changes

---

## Execution Protocol & Operations

### Triggering & Running

When triggered with "run step N":
1. Create the appropriate directory under `runs/`
2. Load the global registry (`neighborhood_scorecard.csv`) to check what's already been evaluated
3. Execute the research using web search, data sources, and analysis
4. Write results to disk AFTER EACH neighborhood/region (not in batch at end)
5. Apply scoring rubrics consistently — refer back to rubric definitions, don't drift
6. Produce the step report with clear PROMOTE/ELIMINATE decisions
7. Update the neighborhood registry
8. Append observations to `decision_log.md`

When triggered with "deep research on [neighborhood]":
1. Create `runs/step3_deep_analysis/{neighborhood_slug}/`
2. Execute all sub-sections (3a–3e)
3. Produce consolidated report with recommendation
4. Update registry with new status

When triggered with "continue" or "resume":
1. Read `neighborhood_scorecard.csv` to find last completed entry
2. Identify next region/neighborhood in sequence
3. Continue from where it left off

### Deduplication & Coverage Strategy
- Before starting any step, load the registry and identify all previously evaluated neighborhoods
- Track which regions have been FULLY covered vs. partially covered
- Use a coverage tracker file (`runs/coverage_status.md`) showing:
  - Which regions are complete
  - Which neighborhoods within each region have been scored
  - Which are pending
- If a neighborhood appears under multiple names (e.g., "SoFA" vs. "South First Area" in San Jose), deduplicate by canonical Zillow/Redfin boundary name
- If new data surfaces that contradicts a previous evaluation, UPDATE the existing entry (mark `last_updated`) rather than creating a new row

### Progress Tracking

After each work session, update `runs/coverage_status.md`:
```
## Coverage Status (last updated: YYYY-MM-DD)

### Step 1: Region Screening
- [x] Region 1: Sacramento & Central Valley — COMPLETE (PASS/FAIL)
- [x] Region 2: North Bay / Wine Country — COMPLETE (PASS/FAIL)
- [ ] Region 3: East Bay — IN PROGRESS (3/7 cities done)
- [ ] Region 4: Peninsula & South Bay — PENDING
- [ ] Region 5: Santa Cruz & Monterey — PENDING
- [ ] Region 6: Central Coast — PENDING

### Step 2: Neighborhood Scoring
- [ ] {Region}: {X}/{Y} neighborhoods scored

### Neighborhoods Evaluated This Session:
- {list with timestamps}
```

### Batch Execution Order

Process regions from most likely to yield results (South Bay / Peninsula) to least likely (Sacramento / Central Valley), so high-value data is captured first:

1. **Region 4**: Peninsula & South Bay (closest to DTSJ, highest job density)
2. **Region 3**: East Bay (good commute options, diverse, more affordable)
3. **Region 5**: Santa Cruz & Monterey (beach access, but route reliability concerns)
4. **Region 2**: North Bay / Wine Country (lifestyle, but far from DTSJ)
5. **Region 6**: Central Coast (beach + land, but very far commute)
6. **Region 1**: Sacramento & Central Valley (affordable but far, hot, less diverse near SJ)

### Error Handling & Data Quality
- If a data source is unavailable or returns stale data, note it in the entry and mark confidence level
- If scoring requires a judgment call not clearly covered by the rubric, document the reasoning in `decision_log.md`
- If two sources disagree (e.g., GreatSchools vs. Niche rating), use the average and note the discrepancy
- Every factual claim should include: source, date retrieved, confidence (HIGH / MEDIUM / LOW)

### Session Management
- Each execution session should aim to complete at minimum one full region (Step 1) or 5 neighborhoods (Step 2)
- At end of each session, commit progress: `git add . && git commit -m "prop_research: step N progress — {summary}"`
- If running in tmux, use session name `prop-research` for easy reattachment: `tmux new -s prop-research` / `tmux attach -t prop-research`
